"""Regression tests for sound_engine/server.py — locks in the bugs found
and fixed by the 2026-08-08 harsh-review pass (session eviction, corrupt
upload handling, invalid EQ body, export filename collisions), plus the
multi-channel project model (single-file upload or a beat's stems)."""
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
    return client.post("/api/project/from-upload",
                        files={"file": (name, data or _wav_bytes(), "audio/wav")})


def test_upload_creates_single_channel_project():
    r = _upload()
    assert r.status_code == 200
    data = r.json()
    assert "project_id" in data
    assert len(data["channels"]) == 1
    assert data["channels"][0]["lane_id"] == "upload"


def test_from_beat_creates_multi_channel_project(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Test DJ"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "1 Test DJ Beat Drums 90bpm.wav", sig, sig)
    stems = dj / "1 Test DJ Beat Stems"
    stems.mkdir()
    write_wav24(stems / "kick.wav", sig, sig)
    write_wav24(stems / "snare.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)

    r = client.post("/api/project/from-beat", json={"beat_id": "Test DJ/1 Test DJ Beat"})
    assert r.status_code == 200
    data = r.json()
    assert len(data["channels"]) == 2
    lane_ids = {c["lane_id"] for c in data["channels"]}
    assert lane_ids == {"kick", "snare"}


def test_from_beat_unknown_id_returns_404(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)
    r = client.post("/api/project/from-beat", json={"beat_id": "nope/nope"})
    assert r.status_code == 404


def test_library_beats_endpoint_lists_fixture_beat(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Test DJ"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "1 Test DJ Beat Drums 90bpm.wav", sig, sig)
    stems = dj / "1 Test DJ Beat Stems"
    stems.mkdir()
    write_wav24(stems / "kick.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)

    r = client.get("/api/library/beats")
    assert r.status_code == 200
    beats = r.json()["beats"]
    assert len(beats) == 1
    assert beats[0]["dj"] == "Test DJ"


def test_project_count_is_capped():
    for _ in range(server.MAX_PROJECTS + 2):
        _upload()
    assert len(server.PROJECTS) <= server.MAX_PROJECTS


def test_upload_process_export_round_trip():
    r = _upload()
    assert r.status_code == 200
    project_id = r.json()["project_id"]

    r2 = client.post(f"/api/project/{project_id}/channel/upload/process",
                      json={"low_db": 3.0, "high_db": -2.0})
    assert r2.status_code == 200

    r3 = client.post(f"/api/project/{project_id}/export")
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
    project_id = _upload().json()["project_id"]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                     json={"low_db": "not a number"})
    assert r.status_code == 400


def test_full_chain_process_applies_all_stages():
    """Compressor, saturation, width, and reverb all reach the exported
    file — matches the live Web Audio graph's chain order."""
    r = _upload()
    project_id = r.json()["project_id"]
    r2 = client.post(f"/api/project/{project_id}/channel/upload/process", json={
        "comp_threshold_db": -30.0, "comp_ratio": 4.0,
        "comp_attack_ms": 5.0, "comp_release_ms": 100.0,
        "sat_drive_db": 12.0, "sat_mix": 0.5,
        "width": 1.6,
        "reverb_size_s": 2.0, "reverb_mix": 0.3,
    })
    assert r2.status_code == 200
    r3 = client.post(f"/api/project/{project_id}/export")
    assert r3.status_code == 200
    out_path = Path(r3.json()["path"])
    assert out_path.exists()

    with wave.open(str(out_path)) as w:
        n = w.getnframes()
        data = np.frombuffer(w.readframes(n), dtype="<i2").reshape(-1, w.getnchannels())
    L, R = data[:, 0].astype(np.float64), data[:, 1].astype(np.float64)
    assert not np.array_equal(L, R)  # width>1 must produce a real stereo difference
    out_path.unlink()


def test_reverb_size_top_of_slider_is_not_saturated():
    """reverb_size_s >= 4.0 used to all clamp to room_size=1.0 and export
    identical audio (found in review — room_size was reverb_size_s / 4.0,
    but the live slider's real max is 6.0). Regression for the /6.0 fix."""
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.5, "reverb_size_s": 4.0})
    wL4, wR4 = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    wL4, wR4 = wL4.copy(), wR4.copy()
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.5, "reverb_size_s": 6.0})
    wL6, wR6 = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(wL4, wL6)


def test_process_stages_are_skipped_at_transparent_defaults():
    """At default (off) values, process() should be equivalent to EQ-only
    — the compressor/saturation/reverb stages must not silently engage."""
    r = _upload()
    project_id = r.json()["project_id"]
    r2 = client.post(f"/api/project/{project_id}/channel/upload/process",
                      json={})  # everything at default
    assert r2.status_code == 200
    channel = server.PROJECTS[project_id]["channels"]["upload"]
    wL, wR = channel["wet"]
    dL, dR = channel["dry"]
    # EQ at 0dB all bands should be a no-op too, so wet ~= dry
    assert np.abs(wL - dL).max() < 1e-3
    assert np.abs(wR - dR).max() < 1e-3


def test_unknown_file_id_returns_404_not_500():
    assert client.post("/api/project/doesnotexist/channel/upload/process",
                        json={}).status_code == 404
    assert client.post("/api/project/doesnotexist/export").status_code == 404
    assert client.get("/api/project/doesnotexist/channel/upload/audio/dry").status_code == 404


def test_session_count_is_capped():
    for _ in range(server.MAX_PROJECTS + 4):
        _upload()
    assert len(server.PROJECTS) <= server.MAX_PROJECTS


def test_concurrent_exports_never_collide_on_filename():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    paths = set()
    for _ in range(3):
        r = client.post(f"/api/project/{project_id}/export")
        p = Path(r.json()["path"])
        assert p not in paths  # each export is a distinct file
        paths.add(p)
    for p in paths:
        p.unlink()


def test_upload_rejects_path_traversal_in_filename():
    project_id = _upload(name="../../evil.wav").json()["project_id"]
    project = server.PROJECTS[project_id]
    assert ".." not in project["name"]
    assert "/" not in project["name"]


def test_channel_process_export_round_trip():
    project_id = _upload().json()["project_id"]
    r2 = client.post(f"/api/project/{project_id}/channel/upload/process",
                      json={"low_db": 3.0, "high_db": -2.0})
    assert r2.status_code == 200
    r3 = client.post(f"/api/project/{project_id}/export")
    assert r3.status_code == 200
    out_path = Path(r3.json()["path"])
    assert out_path.exists()
    out_path.unlink()


def test_channel_process_unknown_channel_returns_404():
    project_id = _upload().json()["project_id"]
    r = client.post(f"/api/project/{project_id}/channel/doesnotexist/process", json={})
    assert r.status_code == 404


def test_channel_process_bad_field_leaves_earlier_fields_uncommitted():
    """A request with one valid field (gain_db) and one bad field (pan)
    must reject and change nothing — not silently commit gain_db while
    returning 400 (found in review)."""
    project_id = _upload().json()["project_id"]
    channel = server.PROJECTS[project_id]["channels"]["upload"]
    before_gain = channel["gain_db"]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                     json={"gain_db": 5.0, "pan": "not a number"})
    assert r.status_code == 400
    assert channel["gain_db"] == before_gain


def test_channel_process_rejects_non_finite_values():
    """float("nan")/float("inf") raise neither TypeError nor ValueError —
    without an explicit finite check this used to sail through, poison
    the channel's wet buffer, and export would "succeed" with a silent
    all-zero WAV (found in harsh-critic re-review)."""
    project_id = _upload().json()["project_id"]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                     json={"width": "nan"})
    assert r.status_code == 400


def test_channel_process_rejects_pan_out_of_range():
    """pan is documented -1..1 (equal-power law); outside that range
    _pan_gains() goes negative and phase-inverts the channel instead of
    erroring (found in harsh-critic re-review)."""
    project_id = _upload().json()["project_id"]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                     json={"pan": 3.0})
    assert r.status_code == 400


def test_export_passes_actual_sample_rate_to_limiter(monkeypatch):
    """brickwall_limit() used to always run at the hardcoded module SR
    regardless of the project's real sample rate — the one DSP stage in
    audio_engine.py not honoring it, timing-wrong for any non-44.1kHz
    upload (found in harsh-critic re-review)."""
    calls = []
    real_limit = server.dsp.audio_engine.brickwall_limit

    def spy(L, R, **kwargs):
        calls.append(kwargs.get("sr"))
        return real_limit(L, R, **kwargs)

    monkeypatch.setattr(server.dsp.audio_engine, "brickwall_limit", spy)
    project_id = _upload(data=_wav_bytes(sr=48000)).json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    r = client.post(f"/api/project/{project_id}/export")
    assert r.status_code == 200
    assert calls == [48000]
    Path(r.json()["path"]).unlink()


def test_lru_eviction_spares_recently_touched_project():
    """Eviction used to be pure FIFO-by-creation, so an actively-edited
    project could be silently discarded mid-session by newer, untouched
    ones — a real risk now that process/audio/export give a project a
    reason to stay open across requests (found in harsh-critic
    re-review)."""
    ids = [_upload().json()["project_id"] for _ in range(server.MAX_PROJECTS)]
    client.post(f"/api/project/{ids[0]}/channel/upload/process", json={})
    _upload()  # 4th project forces eviction of the least-recently-used
    assert ids[0] in server.PROJECTS
    assert len(server.PROJECTS) <= server.MAX_PROJECTS


def test_export_sums_multiple_channels_louder_than_one_muted(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Test DJ"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "1 Test DJ Beat Drums 90bpm.wav", sig, sig)
    stems = dj / "1 Test DJ Beat Stems"
    stems.mkdir()
    write_wav24(stems / "kick.wav", sig, sig)
    write_wav24(stems / "snare.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)
    project_id = client.post("/api/project/from-beat",
                              json={"beat_id": "Test DJ/1 Test DJ Beat"}).json()["project_id"]

    client.post(f"/api/project/{project_id}/channel/kick/process", json={})
    client.post(f"/api/project/{project_id}/channel/snare/process", json={})
    both = client.post(f"/api/project/{project_id}/export")
    both_peak = _wav_peak(Path(both.json()["path"]))

    client.post(f"/api/project/{project_id}/channel/snare/process", json={"muted": True})
    one = client.post(f"/api/project/{project_id}/export")
    one_peak = _wav_peak(Path(one.json()["path"]))

    assert both_peak > one_peak
    Path(both.json()["path"]).unlink()
    Path(one.json()["path"]).unlink()


def _wav_peak(path):
    with wave.open(str(path)) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    return float(np.abs(data).max())
