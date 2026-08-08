"""Sound Engine — standalone local web app, separate from the beat
generator and separate from Reason Voice. Drag in any audio file (WAV,
MP3, M4A, AIFF, FLAC, ...), shape it with the pedalboard engine, export
the result as a new file. Never touches the original.

Run:  ./.venv/bin/python -m sound_engine.server   ("Sound Engine.command" does this)
Serves http://localhost:8767 and auto-opens it in the browser.

v1 scope (owner 2026-08-08): ONE effect (3-band EQ) end to end — load,
tweak, hear, export — before the rest of tools/audio_engine.py's tools
(saturation, multiband, reverb, width) get their own panels.
"""
from __future__ import annotations

import asyncio
import os
import uuid
import webbrowser
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import dsp

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


# session state: file_id -> {name, sr, dry: (L, R), wet: (L, R), src_path}.
# In-memory, single local user, gone on restart. Capped at MAX_SESSIONS —
# each entry holds full-length float64 stereo arrays (a 4-min track is
# ~170 MB for dry+wet together), so an uncapped dict would grow without
# bound over a working session that loads many files (found in review).
SESSIONS: dict[str, dict] = {}
MAX_SESSIONS = 5


def _evict_old_sessions():
    while len(SESSIONS) > MAX_SESSIONS:
        old_id, old = next(iter(SESSIONS.items()))
        del SESSIONS[old_id]
        paths = [old.get("src_path"), RENDERS / f"{old_id}_dry.wav",
                 RENDERS / f"{old_id}_wet.wav"]
        for p in paths:
            if p:
                Path(p).unlink(missing_ok=True)


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex[:12]
    # .name strips any directory components from the client-supplied
    # filename — a "../../x" filename can't escape UPLOADS (found in review)
    safe_name = Path(file.filename or "upload").name
    src = UPLOADS / f"{file_id}_{safe_name}"
    with open(src, "wb") as f:
        f.write(await file.read())
    try:
        L, R, sr = dsp.load_audio(src)
    except Exception as e:
        src.unlink(missing_ok=True)  # don't leave an orphaned upload behind
        return JSONResponse(
            {"error": f"couldn't read that as audio ({e})"}, status_code=400)
    SESSIONS[file_id] = {"name": safe_name, "sr": sr, "dry": (L, R),
                          "wet": (L, R), "src_path": src}
    _evict_old_sessions()
    return JSONResponse({
        "file_id": file_id,
        "filename": safe_name,
        "sample_rate": sr,
        "duration_s": round(len(L) / sr, 2),
    })


@app.post("/api/process/{file_id}")
async def process(file_id: str, params: dict):
    """Bounces the ORIGINAL upload through the same chain order as the
    live Web Audio graph: EQ -> Compressor -> Saturation -> Width ->
    Reverb. Each stage is skipped entirely when its knobs are at their
    transparent/off value, matching the live graph's "no change until you
    touch it" behavior."""
    session = SESSIONS.get(file_id)
    if session is None:
        return JSONResponse({"error": "unknown file_id"}, status_code=404)
    try:
        low_db = float(params.get("low_db", 0.0))
        mid_db = float(params.get("mid_db", 0.0))
        high_db = float(params.get("high_db", 0.0))
        comp_threshold_db = float(params.get("comp_threshold_db", -24.0))
        comp_ratio = float(params.get("comp_ratio", 1.0))
        comp_attack_ms = float(params.get("comp_attack_ms", 12.0))
        comp_release_ms = float(params.get("comp_release_ms", 180.0))
        sat_drive_db = float(params.get("sat_drive_db", 6.0))
        sat_mix = float(params.get("sat_mix", 0.0))
        width = float(params.get("width", 1.0))
        reverb_size_s = float(params.get("reverb_size_s", 2.0))
        reverb_mix = float(params.get("reverb_mix", 0.0))
    except (TypeError, ValueError):
        return JSONResponse({"error": "invalid parameter values"}, status_code=400)

    sr = session["sr"]
    L, R = session["dry"]
    L, R = L.copy(), R.copy()
    ae = dsp.audio_engine

    L, R = ae.eq3(L, R, sr=sr, low_db=low_db, mid_db=mid_db, high_db=high_db)
    if comp_ratio > 1.0:
        # makeup_db=0 to match the live Web Audio DynamicsCompressorNode,
        # which applies gain reduction only, no automatic makeup gain
        L, R = ae.glue_compressor(L, R, sr=sr, threshold_db=comp_threshold_db,
                                    ratio=comp_ratio, attack_ms=comp_attack_ms,
                                    release_ms=comp_release_ms, makeup_db=0.0)
    if sat_mix > 0.0:
        L, R = ae.saturate(L, R, sr=sr, drive_db=sat_drive_db, mix=sat_mix)
    if width != 1.0:
        L, R = ae.stereo_width(L, R, width=width)
    if reverb_mix > 0.0:
        # reverb_size_s (seconds, matches the live IR-length slider) has
        # no exact equivalent in pedalboard.Reverb's 0-1 room_size — this
        # is an approximate mapping, same accepted live/export divergence
        # as the rest of this app (see 2026-08-08 DECISIONS.md entry)
        room_size = min(1.0, reverb_size_s / 4.0)
        L, R = ae.loop_algo_reverb(L, R, sr=sr, room_size=room_size,
                                     wet=reverb_mix, dry=1 - reverb_mix)
    session["wet"] = (L, R)
    return JSONResponse({"ok": True})


@app.get("/api/audio/{file_id}/{variant}")
async def audio(file_id: str, variant: str):
    session = SESSIONS.get(file_id)
    if session is None or variant not in ("dry", "wet"):
        return JSONResponse({"error": "not found"}, status_code=404)
    L, R = session[variant]
    out = RENDERS / f"{file_id}_{variant}.wav"
    dsp.save_wav(out, L, R, session["sr"])
    return FileResponse(out, media_type="audio/wav",
                         headers={"Cache-Control": "no-store"})


@app.post("/api/export/{file_id}")
async def export(file_id: str):
    session = SESSIONS.get(file_id)
    if session is None:
        return JSONResponse({"error": "unknown file_id"}, status_code=404)
    L, R = session["wet"]
    stem = Path(session["name"]).stem
    # microsecond precision — a same-second double-click (no button lock
    # yet resolved client-side) must not collide and silently overwrite
    # the first export (found in review)
    stamp = datetime.now().strftime("%Y-%m-%d %H%M%S.%f")
    out = EXPORT_DIR / f"{stem} (engine) {stamp}.wav"
    dsp.save_wav(out, L, R, session["sr"])
    return JSONResponse({"path": str(out)})


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _clear_scratch():
    # SESSIONS always starts empty on a fresh process and is never
    # persisted, so anything already in UPLOADS/RENDERS is guaranteed
    # orphaned from a previous run (crash, kill, quit) — per-session
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
