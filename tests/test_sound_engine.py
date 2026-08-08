"""Regression tests for sound_engine/server.py — locks in the bugs found
and fixed by the 2026-08-08 harsh-review pass (session eviction, corrupt
upload handling, invalid EQ body, export filename collisions)."""
import io
import os
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
pytest.importorskip("pedalboard")
pytest.importorskip("fastapi")

os.environ["SOUND_ENGINE_NO_BROWSER"] = "1"  # app's startup event would
                                              # otherwise open a real
                                              # browser tab during pytest

from fastapi.testclient import TestClient  # noqa: E402

from sound_engine import server  # noqa: E402

client = TestClient(server.app)


def _wav_bytes(seconds=0.5, sr=44100):
    t = np.arange(int(sr * seconds)) / sr
    sig = (np.sin(2 * np.pi * 440 * t) * 0.4 * 32767).astype("<i2")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(sig.tobytes())
    return buf.getvalue()


def _upload(name="t.wav", data=None):
    return client.post("/api/upload",
                        files={"file": (name, data or _wav_bytes(), "audio/wav")})


def test_upload_process_export_round_trip():
    r = _upload()
    assert r.status_code == 200
    file_id = r.json()["file_id"]

    r2 = client.post(f"/api/process/{file_id}", json={"low_db": 3.0, "high_db": -2.0})
    assert r2.status_code == 200

    r3 = client.post(f"/api/export/{file_id}")
    assert r3.status_code == 200
    out_path = Path(r3.json()["path"])
    assert out_path.exists()
    out_path.unlink()


def test_corrupt_upload_returns_400_and_leaves_no_orphan():
    before = list(server.UPLOADS.iterdir())
    r = _upload(name="bad.wav", data=b"not audio data")
    assert r.status_code == 400
    after = list(server.UPLOADS.iterdir())
    assert len(after) == len(before)  # no file left behind


def test_invalid_eq_body_returns_400_not_500():
    file_id = _upload().json()["file_id"]
    r = client.post(f"/api/process/{file_id}", json={"low_db": "not a number"})
    assert r.status_code == 400


def test_unknown_file_id_returns_404_not_500():
    assert client.post("/api/process/doesnotexist", json={}).status_code == 404
    assert client.post("/api/export/doesnotexist").status_code == 404
    assert client.get("/api/audio/doesnotexist/dry").status_code == 404


def test_session_count_is_capped():
    for _ in range(server.MAX_SESSIONS + 4):
        _upload()
    assert len(server.SESSIONS) <= server.MAX_SESSIONS


def test_concurrent_exports_never_collide_on_filename():
    file_id = _upload().json()["file_id"]
    client.post(f"/api/process/{file_id}", json={})
    paths = set()
    for _ in range(3):
        r = client.post(f"/api/export/{file_id}")
        p = Path(r.json()["path"])
        assert p not in paths  # each export is a distinct file
        paths.add(p)
    for p in paths:
        p.unlink()


def test_upload_rejects_path_traversal_in_filename():
    file_id = _upload(name="../../evil.wav").json()["file_id"]
    session = server.SESSIONS[file_id]
    assert ".." not in session["name"]
    assert "/" not in session["name"]
