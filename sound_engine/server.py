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


# session state: file_id -> {name, sr, dry: (L, R), wet: (L, R)}. In-memory,
# single local user, gone on restart — fine for a working session.
SESSIONS: dict[str, dict] = {}


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex[:12]
    src = UPLOADS / f"{file_id}_{file.filename}"
    with open(src, "wb") as f:
        f.write(await file.read())
    L, R, sr = dsp.load_audio(src)
    SESSIONS[file_id] = {"name": file.filename, "sr": sr, "dry": (L, R),
                          "wet": (L, R)}
    return JSONResponse({
        "file_id": file_id,
        "filename": file.filename,
        "sample_rate": sr,
        "duration_s": round(len(L) / sr, 2),
    })


@app.post("/api/process/{file_id}")
async def process(file_id: str, eq: dict):
    session = SESSIONS.get(file_id)
    if session is None:
        return JSONResponse({"error": "unknown file_id"}, status_code=404)
    L, R = session["dry"]
    wL, wR = dsp.audio_engine.eq3(
        L.copy(), R.copy(), sr=session["sr"],
        low_db=float(eq.get("low_db", 0.0)),
        low_hz=float(eq.get("low_hz", 120.0)),
        mid_db=float(eq.get("mid_db", 0.0)),
        mid_hz=float(eq.get("mid_hz", 800.0)),
        mid_q=float(eq.get("mid_q", 0.9)),
        high_db=float(eq.get("high_db", 0.0)),
        high_hz=float(eq.get("high_hz", 8000.0)))
    session["wet"] = (wL, wR)
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
    stamp = datetime.now().strftime("%Y-%m-%d %H%M%S")
    out = EXPORT_DIR / f"{stem} (engine) {stamp}.wav"
    dsp.save_wav(out, L, R, session["sr"])
    return JSONResponse({"path": str(out)})


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def main():
    if _port_in_use(PORT):
        print(f"Sound Engine is already running — opening "
              f"http://localhost:{PORT} in your browser.")
        webbrowser.open(f"http://localhost:{PORT}")
        return
    print(f"Ready — http://localhost:{PORT}  "
          f"(leave this window open; Ctrl+C here to quit)")
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
