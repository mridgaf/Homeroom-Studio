"""Sound Engine — standalone local web app, separate from the beat
generator and separate from Reason Voice. Drag in any audio file (WAV,
MP3, M4A, AIFF, FLAC, ...), shape it with the pedalboard engine, export
the result as a new file — or load a beat from the library as a
multi-channel project, one channel per stem. Never touches the original.

Run:  ./.venv/bin/python -m sound_engine.server   ("Sound Engine.command" does this)
Serves http://localhost:8767 and auto-opens it in the browser.

Chain order (both live preview and this file's export path): EQ ->
Compressor -> Saturation -> Width -> Reverb. Each stage is skipped when
its knobs sit at the transparent/off default, matching the live graph's
"no change until you touch it" behavior.
"""
from __future__ import annotations

import asyncio
import math
import os
import re
import uuid
import webbrowser
from datetime import datetime
from pathlib import Path

import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import dsp, library

import groove  # noqa: E402  (tools/ is on sys.path once dsp is imported)

PORT = 8767
STATIC_DIR = Path(__file__).parent / "static"
# ephemeral working files — not the owner's library, safe to clear anytime
WORK_DIR = Path(os.path.expanduser("~/.homeroom_engine"))
UPLOADS = WORK_DIR / "uploads"
RENDERS = WORK_DIR / "renders"
EXPORT_DIR = Path(os.path.expanduser("~/Desktop/Homeroom Sound Engine Exports"))
for d in (UPLOADS, RENDERS, EXPORT_DIR):
    d.mkdir(parents=True, exist_ok=True)

app = FastAPI()


@app.on_event("startup")
async def _open_browser():
    async def _later():
        await asyncio.sleep(0.4)
        webbrowser.open(f"http://localhost:{PORT}")
    if not os.environ.get("SOUND_ENGINE_NO_BROWSER"):
        asyncio.create_task(_later())


@app.middleware("http")
async def no_stale_ui(request, call_next):
    """Force revalidation of static/app.js etc — a server-side fix (like
    the stop-on-backgrounding safety net) is worthless if the browser
    just keeps serving its cached old copy of app.js instead of fetching
    the new one. Matches reason_voice/server.py's same fix."""
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-cache"
    return response


BEATS_ROOT = library.resolve_beats_root()

# project state: project_id -> {name, channels: {lane_id -> {...}},
# src_paths}. In-memory, single local user, gone on restart. Capped at
# MAX_PROJECTS — a multi-channel project holds 10+ stereo float64 arrays
# instead of one file's 2, so the per-entry memory cost is proportionally
# higher than the old single-file SESSIONS; cap lower to compensate.
PROJECTS: dict[str, dict] = {}
MAX_PROJECTS = 3
# an IR is held in RAM as float64 (8 bytes/sample/channel) for as long as
# the project lives — cap what can be dropped in before it is read
MAX_IR_BYTES = 50 * 1024 * 1024


def _evict_old_projects():
    while len(PROJECTS) > MAX_PROJECTS:
        old_id, old = next(iter(PROJECTS.items()))
        del PROJECTS[old_id]
        for p in old.get("src_paths", []):
            Path(p).unlink(missing_ok=True)
        for lane_id in old.get("channels", {}):
            for variant in ("dry", "wet"):
                (RENDERS / f"{old_id}_{lane_id}_{variant}.wav").unlink(missing_ok=True)


def _new_channel(label, L, R, sr):
    return {"label": label, "sr": sr, "dry": (L, R), "wet": (L, R),
            "gain_db": 0.0, "pan": 0.0, "muted": False, "solo": False,
            "ir": None, "ir_name": None, "ir_scale": 1.0, "ir_seq": 0}


def _project_response(project_id, project):
    return {
        "project_id": project_id,
        "name": project["name"],
        "channels": [
            {"lane_id": lane_id, "label": ch["label"],
             "sample_rate": ch["sr"],
             "duration_s": round(len(ch["dry"][0]) / ch["sr"], 2)}
            for lane_id, ch in project["channels"].items()
        ],
    }


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/library/beats")
async def library_beats():
    if not BEATS_ROOT.is_dir():
        return JSONResponse({"beats": [],
                              "warning": f"Beat library not found at {BEATS_ROOT} "
                                         "— is the drive plugged in?"})
    beats = library.list_beats(BEATS_ROOT)
    return JSONResponse({
        "beats": [{"beat_id": b["beat_id"], "dj": b["dj"],
                    "display_name": b["display_name"], "bpm": b["bpm"],
                    "stem_count": b["stem_count"]} for b in beats],
        "warning": None,
    })


@app.post("/api/project/from-beat")
async def project_from_beat(body: dict):
    beat_id = body.get("beat_id", "")
    beat = library.find_beat(BEATS_ROOT, beat_id)
    if beat is None:
        return JSONResponse({"error": "unknown or stem-less beat_id"}, status_code=404)
    project_id = uuid.uuid4().hex[:12]
    channels = {}
    for wav in sorted(beat["stems_dir"].glob("*.wav")):
        lane_id = wav.stem
        try:
            L, R, sr = dsp.load_audio(wav)
        except Exception:
            continue  # one bad stem shouldn't sink the whole load
        channels[lane_id] = _new_channel(lane_id, L, R, sr)
    if not channels:
        return JSONResponse({"error": "no readable stems in that beat"}, status_code=400)
    PROJECTS[project_id] = {"name": beat["display_name"], "channels": channels,
                              "src_paths": []}
    _evict_old_projects()
    return JSONResponse(_project_response(project_id, PROJECTS[project_id]))


@app.post("/api/project/from-upload")
async def project_from_upload(file: UploadFile = File(...)):
    # .name strips any directory components from the client-supplied
    # filename — a "../../x" filename can't escape UPLOADS (found in review)
    safe_name = Path(file.filename or "upload").name
    project_id = uuid.uuid4().hex[:12]
    src = UPLOADS / f"{project_id}_{safe_name}"
    with open(src, "wb") as f:
        f.write(await file.read())
    try:
        L, R, sr = dsp.load_audio(src)
    except Exception as e:
        src.unlink(missing_ok=True)  # don't leave an orphaned upload behind
        return JSONResponse({"error": f"couldn't read that as audio ({e})"},
                             status_code=400)
    PROJECTS[project_id] = {
        "name": safe_name,
        "channels": {"upload": _new_channel(safe_name, L, R, sr)},
        "src_paths": [src],
    }
    _evict_old_projects()
    return JSONResponse(_project_response(project_id, PROJECTS[project_id]))


def _finite_float(v, lo=None, hi=None):
    # float("nan")/float("inf") raise neither TypeError nor ValueError, so
    # a NaN/Inf param would otherwise sail past every caller's validation
    # and silently poison a channel's buffer (found in harsh-critic
    # re-review — export "succeeded" with an all-zero WAV, no error).
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(f"{v!r} is not finite")
    if lo is not None and v < lo:
        raise ValueError(f"{v!r} is below {lo}")
    if hi is not None and v > hi:
        raise ValueError(f"{v!r} is above {hi}")
    return v


def _convolve_through(L, R, ir, mix, scale):
    """Run the channel through an arbitrary sound (a snare, a door slam,
    a vocal) instead of a room. loop_convolve is circular, so the tail
    that runs past the end wraps onto the start — the house loop-safety
    rule, same as the reverb path.

    `scale` is the level correction measured ONCE against this channel's
    raw dry audio when the IR was loaded (see _measure_conv_scale), not
    recomputed here. Recomputing it post-EQ/comp/saturation made the
    export drift away from the live preview every time an earlier knob
    moved — the browser measures against the raw buffer and can't see
    those stages (found in harsh-critic review).
    """
    n = len(L)
    wetL = groove.loop_convolve(L, ir[0][:n]) * scale
    wetR = groove.loop_convolve(R, ir[1][:n]) * scale
    return L * (1 - mix) + wetL * mix, R * (1 - mix) + wetR * mix


def _measure_conv_scale(L, R, ir):
    """Level rule, shared with the browser: the 100%-wet signal peaks
    where the dry peaked. Raw convolution levels differ by ~800x between
    numpy and Chrome's ConvolverNode, so the two sides can't share a
    scale FACTOR — they apply the same RULE, each measured in its own
    engine, both against the raw (pre-chain) buffer and both circular."""
    n = len(L)
    wetL = groove.loop_convolve(L, ir[0][:n])
    wetR = groove.loop_convolve(R, ir[1][:n])
    dry_peak = max(np.abs(L).max(), np.abs(R).max())
    wet_peak = max(np.abs(wetL).max(), np.abs(wetR).max())
    return dry_peak / wet_peak if (wet_peak > 0 and dry_peak > 0) else 1.0


def _read_ir_head(path, channel):
    """Read only as much of the dropped file as this channel can use.

    MAX_IR_BYTES caps the UPLOAD, not the decode: 50 MB of 128 kbps MP3 is
    ~52 minutes, which `dsp.load_audio` would expand to gigabytes of float64
    before the trim ever ran (found in re-review). Reading just the head
    bounds it at the stem's own size.
    """
    import pedalboard.io as pbio
    with pbio.AudioFile(str(path)) as f:
        ir_sr = f.samplerate
        stem_seconds = len(channel["dry"][0]) / channel["sr"]
        wanted = min(f.frames, int(stem_seconds * ir_sr) + 1)
        audio = f.read(wanted)
    if audio.shape[0] == 1:
        audio = np.vstack([audio[0], audio[0]])
    elif audio.shape[0] > 2:
        audio = audio[:2]
    return audio[0].astype(np.float64), audio[1].astype(np.float64), ir_sr


def _prepare_ir(irL, irR, ir_sr, channel):
    """An IR is only usable against THIS channel: same sample rate, and no
    longer than the stem (loop_convolve requires len(ir) <= len(sig)).
    Both are done once, at load time — resampling was previously skipped
    entirely, so a 48 kHz IR exported ~8.8% fast while the browser (which
    resamples in decodeAudioData) played it correctly."""
    sr = channel["sr"]
    if ir_sr != sr:
        import soxr
        irL = soxr.resample(irL, ir_sr, sr)
        irR = soxr.resample(irR, ir_sr, sr)
    n = len(channel["dry"][0])
    return np.asarray(irL[:n], dtype=np.float64), np.asarray(irR[:n], dtype=np.float64)


def _apply_channel_chain(L, R, sr, p, ir=None, conv_scale=1.0):
    ae = dsp.audio_engine
    low_db = _finite_float(p.get("low_db", 0.0))
    low_hz = _finite_float(p.get("low_hz", 120.0))
    mid_db = _finite_float(p.get("mid_db", 0.0))
    mid_hz = _finite_float(p.get("mid_hz", 800.0))
    mid_q = _finite_float(p.get("mid_q", 0.9))
    high_db = _finite_float(p.get("high_db", 0.0))
    high_hz = _finite_float(p.get("high_hz", 8000.0))
    comp_threshold_db = _finite_float(p.get("comp_threshold_db", -24.0))
    comp_ratio = _finite_float(p.get("comp_ratio", 1.0))
    comp_attack_ms = _finite_float(p.get("comp_attack_ms", 12.0))
    comp_release_ms = _finite_float(p.get("comp_release_ms", 180.0))
    comp_makeup_db = _finite_float(p.get("comp_makeup_db", 0.0))
    sat_drive_db = _finite_float(p.get("sat_drive_db", 6.0))
    sat_mix = _finite_float(p.get("sat_mix", 0.0))
    width = _finite_float(p.get("width", 1.0))
    reverb_size_s = _finite_float(p.get("reverb_size_s", 2.0))
    reverb_mix = _finite_float(p.get("reverb_mix", 0.0))
    reverb_dry = _finite_float(p.get("reverb_dry", 1.0 - reverb_mix))
    reverb_damping = _finite_float(p.get("reverb_damping", 0.5))
    reverb_width = _finite_float(p.get("reverb_width", 1.0))
    reverb_freeze = bool(p.get("reverb_freeze", False))
    conv_mix = _finite_float(p.get("conv_mix", 0.0), lo=0.0, hi=1.0)

    L, R = ae.eq3(L, R, sr=sr, low_db=low_db, low_hz=low_hz,
                   mid_db=mid_db, mid_hz=mid_hz, mid_q=mid_q,
                   high_db=high_db, high_hz=high_hz)
    if comp_ratio > 1.0:
        L, R = ae.glue_compressor(L, R, sr=sr, threshold_db=comp_threshold_db,
                                    ratio=comp_ratio, attack_ms=comp_attack_ms,
                                    release_ms=comp_release_ms, makeup_db=comp_makeup_db)
    if sat_mix > 0.0:
        L, R = ae.saturate(L, R, sr=sr, drive_db=sat_drive_db, mix=sat_mix)
    if width != 1.0:
        L, R = ae.stereo_width(L, R, width=width)
    if conv_mix > 0.0 and ir is not None:
        L, R = _convolve_through(L, R, ir, conv_mix, conv_scale)
    if reverb_mix > 0.0 or reverb_freeze:
        room_size = min(1.0, reverb_size_s / 6.0)
        L, R = ae.loop_algo_reverb(L, R, sr=sr, room_size=room_size,
                                     damping=reverb_damping, wet=reverb_mix,
                                     dry=reverb_dry, width=reverb_width,
                                     freeze=reverb_freeze)
    return L, R


def _get_channel(project_id, lane_id):
    project = PROJECTS.get(project_id)
    if project is None:
        return None, None
    # Bump to most-recently-used on every touch — eviction below was
    # FIFO-by-creation, so an actively-edited project (this is the first
    # task that gives one a reason to stay open across requests) could
    # get silently evicted mid-session by newer, untouched projects
    # (found in harsh-critic re-review).
    PROJECTS[project_id] = PROJECTS.pop(project_id)
    channel = project["channels"].get(lane_id)
    return project, channel


@app.post("/api/project/{project_id}/channel/{lane_id}/process")
async def channel_process(project_id: str, lane_id: str, params: dict):
    project, channel = _get_channel(project_id, lane_id)
    if channel is None:
        return JSONResponse({"error": "unknown project_id or lane_id"}, status_code=404)
    try:
        gain_db = _finite_float(params.get("gain_db", channel["gain_db"]))
        pan = _finite_float(params.get("pan", channel["pan"]), lo=-1.0, hi=1.0)
        muted = bool(params.get("muted", channel["muted"]))
        solo = bool(params.get("solo", channel["solo"]))
        L, R = channel["dry"]
        L, R = _apply_channel_chain(L.copy(), R.copy(), channel["sr"], params,
                                     ir=channel["ir"],
                                     conv_scale=channel["ir_scale"])
    except (TypeError, ValueError):
        return JSONResponse({"error": "invalid parameter values"}, status_code=400)
    # Only commit once every field parsed and the chain ran clean — a bad
    # field partway through the old field-by-field mutation order left
    # earlier fields (e.g. gain_db) silently written even on a 400 (found
    # in review).
    channel["gain_db"] = gain_db
    channel["pan"] = pan
    channel["muted"] = muted
    channel["solo"] = solo
    channel["wet"] = (L, R)
    return JSONResponse({"ok": True})


@app.post("/api/project/{project_id}/channel/{lane_id}/ir")
async def channel_load_ir(project_id: str, lane_id: str, file: UploadFile = File(...)):
    """The sound this channel gets run through. Read once, kept in memory
    as (L, R) at its own rate — the file itself is deleted immediately,
    so a dropped IR never accumulates on disk the way uploads do."""
    project, channel = _get_channel(project_id, lane_id)
    if channel is None:
        return JSONResponse({"error": "unknown project_id or lane_id"}, status_code=404)
    safe_name = Path(file.filename or "ir").name  # can't escape UPLOADS
    raw = await file.read()
    if len(raw) > MAX_IR_BYTES:
        return JSONResponse(
            {"error": f"that file is too big to convolve with "
                      f"({len(raw) // 1_000_000} MB, limit "
                      f"{MAX_IR_BYTES // 1_000_000} MB)"},
            status_code=400)
    seq = channel["ir_seq"]  # a Clear during the read below wins over this
                              # load — without it the resumed POST wrote the
                              # IR back onto a channel the owner just cleared
    tmp = UPLOADS / f"{project_id}_ir_{uuid.uuid4().hex[:8]}_{safe_name}"
    try:
        with open(tmp, "wb") as f:
            f.write(raw)
        irL, irR, ir_sr = _read_ir_head(tmp, channel)
    except Exception as e:
        return JSONResponse({"error": f"couldn't read that as audio ({e})"},
                             status_code=400)
    finally:
        tmp.unlink(missing_ok=True)
    ir = _prepare_ir(irL, irR, ir_sr, channel)  # rate-matched and trimmed
    # Silence is checked on the PREPARED IR, not the raw file: a sample with
    # a long silent lead-in dropped on a short stem trims down to all zeros,
    # and the old raw-file check passed it — the channel then convolved to
    # digital silence and the export "succeeded" (found in re-review).
    if not np.any(ir[0]) and not np.any(ir[1]):
        return JSONResponse(
            {"error": "the first part of that file is silent, and that's all "
                      "that fits this stem — nothing to convolve with"},
            status_code=400)
    if channel["ir_seq"] != seq:
        return JSONResponse({"ok": True, "ir_name": None, "superseded": True})
    channel["ir"] = ir
    channel["ir_name"] = safe_name
    channel["ir_scale"] = _measure_conv_scale(*channel["dry"], ir)
    return JSONResponse({"ok": True, "ir_name": safe_name})


@app.delete("/api/project/{project_id}/channel/{lane_id}/ir")
async def channel_clear_ir(project_id: str, lane_id: str):
    project, channel = _get_channel(project_id, lane_id)
    if channel is None:
        return JSONResponse({"error": "unknown project_id or lane_id"}, status_code=404)
    channel["ir"] = None
    channel["ir_name"] = None
    channel["ir_scale"] = 1.0
    channel["ir_seq"] += 1  # cancels any IR load still being read
    return JSONResponse({"ok": True})


@app.get("/api/project/{project_id}/channel/{lane_id}/{variant}")
async def channel_audio(project_id: str, lane_id: str, variant: str):
    project, channel = _get_channel(project_id, lane_id)
    if channel is None or variant not in ("dry", "wet"):
        return JSONResponse({"error": "not found"}, status_code=404)
    L, R = channel[variant]
    out = RENDERS / f"{project_id}_{lane_id}_{variant}.wav"
    dsp.save_wav(out, L, R, channel["sr"])
    return FileResponse(out, media_type="audio/wav",
                         headers={"Cache-Control": "no-store"})


def _pan_gains(pan):
    # equal-power pan law, -1..1 -> (left_gain, right_gain)
    theta = (pan + 1) * (np.pi / 4)
    return np.cos(theta), np.sin(theta)


@app.post("/api/project/{project_id}/export")
async def project_export(project_id: str):
    project = PROJECTS.get(project_id)
    if project is None:
        return JSONResponse({"error": "unknown project_id"}, status_code=404)
    PROJECTS[project_id] = PROJECTS.pop(project_id)  # touch — see _get_channel
    channels = project["channels"]
    any_solo = any(c["solo"] for c in channels.values())
    audible = [c for c in channels.values()
               if (c["solo"] if any_solo else not c["muted"])]
    if not audible:
        return JSONResponse({"error": "nothing to export — every channel is muted"},
                             status_code=400)
    sr = next(iter(channels.values()))["sr"]
    n = max(len(c["wet"][0]) for c in audible)
    mixL = np.zeros(n)
    mixR = np.zeros(n)
    for c in audible:
        L, R = c["wet"]
        g = 10 ** (c["gain_db"] / 20.0)
        panL, panR = _pan_gains(c["pan"])
        mixL[:len(L)] += L * g * panL
        mixR[:len(R)] += R * g * panR
    ae = dsp.audio_engine
    mixL, mixR = ae.brickwall_limit(mixL, mixR, ceiling_db=-0.3, sr=sr)
    stem = re.sub(r'[\\/:*?"<>|]', "_", project["name"]).strip() or "mix"
    stamp = datetime.now().strftime("%Y-%m-%d %H%M%S.%f")
    out = EXPORT_DIR / f"{stem} (engine) {stamp}.wav"
    dsp.save_wav(out, mixL, mixR, sr)
    return JSONResponse({"path": str(out)})


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _clear_scratch():
    # PROJECTS always starts empty on a fresh process and is never
    # persisted, so anything already in UPLOADS/RENDERS is guaranteed
    # orphaned from a previous run (crash, kill, quit) — per-project
    # eviction only cleans up within one running process (found in
    # review). Only safe to call once we're SURE we're the process about
    # to own these directories — i.e. after the port-in-use check below,
    # never at import time, or a second launch while one is already
    # running would delete files the live process still has open.
    for scratch_dir in (UPLOADS, RENDERS):
        for f in scratch_dir.iterdir():
            if f.is_file():
                f.unlink()


def main():
    if _port_in_use(PORT):
        print(f"Sound Engine is already running — opening "
              f"http://localhost:{PORT} in your browser.")
        webbrowser.open(f"http://localhost:{PORT}")
        return
    _clear_scratch()
    print(f"Ready — http://localhost:{PORT}  "
          f"(leave this window open; Ctrl+C here to quit)")
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
