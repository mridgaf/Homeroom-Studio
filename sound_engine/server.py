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
import os
import uuid
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import dsp, library

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
            "gain_db": 0.0, "pan": 0.0, "muted": False, "solo": False}


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


# Per-channel process/audio-fetch/export endpoints (replacing the old
# SESSIONS-based /api/process/{file_id}, /api/audio/{file_id}/{variant},
# /api/export/{file_id}) land in the next task, against the PROJECTS/
# channels shape above.


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
