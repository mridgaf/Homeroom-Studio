"""Regression tests for sound_engine/server.py — locks in the bugs found
and fixed by the 2026-08-08 harsh-review pass (session eviction, corrupt
upload handling, invalid EQ body, export filename collisions), plus the
multi-channel project model (single-file upload or a beat's stems)."""
import io
import json
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


def test_eq_frequency_params_reach_export():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"low_db": 6.0, "low_hz": 60.0})
    wet_low_hz_60 = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"low_db": 6.0, "low_hz": 300.0})
    wet_low_hz_300 = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(wet_low_hz_60[0], wet_low_hz_300[0])


def test_compressor_makeup_gain_reaches_export():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"comp_ratio": 4.0, "comp_makeup_db": 0.0})
    quiet = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"comp_ratio": 4.0, "comp_makeup_db": 12.0})
    loud = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert np.abs(loud[0]).max() > np.abs(quiet[0]).max()


def test_reverb_wet_and_dry_are_independent():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.4, "reverb_dry": 1.0})
    both = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.4, "reverb_dry": 0.0})
    wet_only = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(both[0], wet_only[0])


# --- Convolve (2026-08-12): run a channel through any sound the owner drops in

def _load_ir(project_id, lane="upload", data=None, name="ir.wav"):
    return client.post(f"/api/project/{project_id}/channel/{lane}/ir",
                        files={"file": (name, data or _wav_bytes(0.1), "audio/wav")})


def test_conv_mix_without_an_ir_is_a_no_op():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                    json={"conv_mix": 1.0})
    assert r.status_code == 200
    assert np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


def test_loaded_ir_changes_the_sound():
    project_id = _upload().json()["project_id"]
    assert _load_ir(project_id).status_code == 200
    client.post(f"/api/project/{project_id}/channel/upload/process", json={"conv_mix": 0.0})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={"conv_mix": 1.0})
    wet = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(dry[0], wet[0])


def test_ir_longer_than_the_stem_does_not_crash():
    # loop_convolve requires len(ir) <= len(sig); a 2s door slam dropped on
    # a 0.5s stem must be trimmed, not raise
    project_id = _upload().json()["project_id"]
    assert _load_ir(project_id, data=_wav_bytes(2.0)).status_code == 200
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                    json={"conv_mix": 1.0})
    assert r.status_code == 200


def test_convolve_does_not_explode_the_level():
    # unnormalized convolution multiplies energy — a full-wet channel must
    # stay near the dry peak instead of clipping to mud
    project_id = _upload().json()["project_id"]
    _load_ir(project_id, data=_wav_bytes(0.2))
    client.post(f"/api/project/{project_id}/channel/upload/process", json={"conv_mix": 0.0})
    dry_peak = np.abs(server.PROJECTS[project_id]["channels"]["upload"]["wet"][0]).max()
    client.post(f"/api/project/{project_id}/channel/upload/process", json={"conv_mix": 1.0})
    wet_peak = np.abs(server.PROJECTS[project_id]["channels"]["upload"]["wet"][0]).max()
    assert wet_peak <= dry_peak * 1.2


def test_unreadable_ir_upload_is_rejected():
    project_id = _upload().json()["project_id"]
    r = _load_ir(project_id, data=b"not audio at all", name="junk.wav")
    assert r.status_code == 400


def test_clearing_the_ir_restores_the_dry_sound():
    project_id = _upload().json()["project_id"]
    _load_ir(project_id)
    client.post(f"/api/project/{project_id}/channel/upload/process", json={"conv_mix": 0.0})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    assert client.delete(f"/api/project/{project_id}/channel/upload/ir").status_code == 200
    client.post(f"/api/project/{project_id}/channel/upload/process", json={"conv_mix": 1.0})
    assert np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


# --- fixes from the 2026-08-12 harsh-critic pass on Convolve

def _silent_wav_bytes(seconds=0.2, sr=44100):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(np.zeros(int(sr * seconds), dtype="<i2").tobytes())
    return buf.getvalue()


def test_ir_at_a_different_sample_rate_is_resampled_to_the_stem():
    # the browser resamples in decodeAudioData; the server used to keep the
    # raw samples, so a 48k IR exported ~8.8% fast — live and export differed
    project_id = _upload().json()["project_id"]  # stem is 44100
    assert _load_ir(project_id, data=_wav_bytes(0.1, sr=22050)).status_code == 200
    ir = server.PROJECTS[project_id]["channels"]["upload"]["ir"]
    # 0.1s at 22050 must become ~0.1s at 44100, not 2205 raw samples
    assert abs(len(ir[0]) - 4410) < 50


def test_ir_is_trimmed_to_the_stem_at_load_time():
    # both a memory guard and a live/export parity guard — the browser trims
    # to the same length, so an over-long IR can't sound different in each
    project_id = _upload().json()["project_id"]  # 0.5s stem
    _load_ir(project_id, data=_wav_bytes(2.0))
    ir = server.PROJECTS[project_id]["channels"]["upload"]["ir"]
    stem_len = len(server.PROJECTS[project_id]["channels"]["upload"]["dry"][0])
    assert len(ir[0]) == stem_len


def test_oversized_ir_is_rejected():
    project_id = _upload().json()["project_id"]
    huge = b"RIFF" + b"\0" * (server.MAX_IR_BYTES + 1)
    r = _load_ir(project_id, data=huge, name="huge.wav")
    assert r.status_code == 400
    assert "too big" in r.json()["error"]


def test_silent_ir_is_rejected():
    project_id = _upload().json()["project_id"]
    r = _load_ir(project_id, data=_silent_wav_bytes(), name="silence.wav")
    assert r.status_code == 400


def test_conv_level_does_not_drift_when_an_earlier_knob_moves():
    # the scale used to be recomputed post-EQ on every call, while the
    # browser measured once against the raw buffer — so any EQ move pulled
    # live and export apart. Compare the wet/dry peak RATIO with EQ flat vs
    # EQ boosted: a recompute-post-EQ implementation forces both to 1.0,
    # this one lets the boost show through exactly as it does live.
    def ratio(**eq):
        project_id = _upload().json()["project_id"]
        _load_ir(project_id, data=_wav_bytes(0.2))
        client.post(f"/api/project/{project_id}/channel/upload/process",
                    json=dict(conv_mix=0.0, **eq))
        dry = np.abs(server.PROJECTS[project_id]["channels"]["upload"]["wet"][0]).max()
        client.post(f"/api/project/{project_id}/channel/upload/process",
                    json=dict(conv_mix=1.0, **eq))
        wet = np.abs(server.PROJECTS[project_id]["channels"]["upload"]["wet"][0]).max()
        return wet / dry

    flat = ratio()
    boosted = ratio(low_db=12.0, high_db=12.0)
    assert abs(flat - boosted) > 0.02, (
        "wet/dry ratio identical under a 12 dB boost — the scale is being "
        "recomputed after the EQ again, which is what drifts from live")


def test_ir_that_trims_down_to_silence_is_rejected():
    # a sample with a long silent lead-in, dropped on a short stem: the
    # usable head is all zeros, so the channel would convolve to digital
    # silence and the export would "succeed"
    sr = 44100
    quiet = np.zeros(int(sr * 0.6), dtype="<i2")
    click = (np.ones(1000) * 12000).astype("<i2")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.concatenate([quiet, click]).tobytes())
    project_id = _upload().json()["project_id"]  # 0.5s stem
    r = _load_ir(project_id, data=buf.getvalue(), name="late.wav")
    assert r.status_code == 400
    assert server.PROJECTS[project_id]["channels"]["upload"]["ir"] is None


def test_clear_during_an_ir_load_wins(monkeypatch):
    # the Clear used to run to completion while the POST was still reading,
    # and then the resumed POST wrote the IR back onto the channel the owner
    # had just cleared
    project_id = _upload().json()["project_id"]
    channel = server.PROJECTS[project_id]["channels"]["upload"]
    real_read = server._read_ir_head

    def clear_midway(path, ch):
        out = real_read(path, ch)
        client.delete(f"/api/project/{project_id}/channel/upload/ir")
        return out

    monkeypatch.setattr(server, "_read_ir_head", clear_midway)
    r = client.post(f"/api/project/{project_id}/channel/upload/ir",
                    files={"file": ("ir.wav", _wav_bytes(0.1), "audio/wav")})
    assert r.status_code == 200
    assert r.json().get("superseded") is True
    assert channel["ir"] is None
    assert channel["ir_name"] is None


def test_only_the_usable_head_of_a_long_ir_is_decoded():
    # MAX_IR_BYTES caps the upload, not the decode — a long file used to be
    # expanded to float64 in full before being trimmed
    project_id = _upload().json()["project_id"]  # 0.5s stem
    _load_ir(project_id, data=_wav_bytes(20.0))
    ir = server.PROJECTS[project_id]["channels"]["upload"]["ir"]
    stem_len = len(server.PROJECTS[project_id]["channels"]["upload"]["dry"][0])
    assert len(ir[0]) == stem_len


def test_clearing_the_ir_resets_its_scale():
    project_id = _upload().json()["project_id"]
    _load_ir(project_id, data=_wav_bytes(0.2))
    client.delete(f"/api/project/{project_id}/channel/upload/ir")
    assert server.PROJECTS[project_id]["channels"]["upload"]["ir_scale"] == 1.0


# --- Beat Repeat (2026-08-12): grab a slice, stutter it

def test_beat_repeat_off_by_default_is_bit_identical():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"br_mix": 0.0, "br_cell_s": 0.125, "br_repeats": 4, "br_chance": 1.0})
    assert np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


def test_beat_repeat_tiles_the_head_of_each_cell():
    # tested on the function, not the endpoint: the EQ stage always runs and
    # smears sample-exactness even at 0 dB
    sr = 44100
    L = np.random.RandomState(0).randn(sr).astype(np.float64)
    outL, _ = server._beat_repeat(L, L.copy(), sr, cell_s=0.1, repeats=4,
                                   chance=1.0, mix=1.0)
    cell = int(round(0.1 * sr))
    slice_len = cell // 4
    head = outL[:slice_len]
    for k in range(1, 4):
        assert np.array_equal(head, outL[k * slice_len:(k + 1) * slice_len])
    assert np.array_equal(head, L[:slice_len])  # the head itself is untouched


def test_beat_repeat_reaches_the_export_path():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"br_mix": 1.0, "br_cell_s": 0.1, "br_repeats": 4, "br_chance": 1.0})
    assert not np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


def test_beat_repeat_chance_zero_changes_nothing():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"br_mix": 1.0, "br_cell_s": 0.1, "br_repeats": 4, "br_chance": 0.0})
    assert np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


def test_beat_repeat_chance_is_deterministic_not_random():
    # live and export must pick the SAME cells — a seeded hash of the cell
    # index, not a random draw
    ids = [_upload().json()["project_id"] for _ in range(2)]
    outs = []
    for pid in ids:
        client.post(f"/api/project/{pid}/channel/upload/process",
                    json={"br_mix": 1.0, "br_cell_s": 0.05, "br_repeats": 3, "br_chance": 0.5})
        outs.append(server.PROJECTS[pid]["channels"]["upload"]["wet"][0])
    assert np.array_equal(outs[0], outs[1])


def test_beat_repeat_cell_selection_matches_the_browser_hash():
    # these are the values app.js's brCellIsPicked() produces for the same
    # inputs, captured from the running browser. If either side's formula
    # drifts, live and export stutter on different beats.
    from_browser = [0, 2, 3, 8, 9, 10, 11, 14, 18, 19, 20, 22, 25, 26, 28,
                    29, 30, 32, 33, 37]
    picked = [i for i in range(200) if server._br_cell_is_picked(i, 0.5)]
    assert picked[:20] == from_browser
    assert len(picked) == 96


def test_beat_repeat_cell_length_rounds_like_the_browser():
    # 0.125s * 44100 = 5512.5 exactly — Python's round() gives 5512
    # (banker's), the browser's Math.round gives 5513. Every odd multiple of
    # the ms slider's 5ms step lands on .5, so this is the default case.
    # A ramp makes every sample unique, so the cell boundary is visible:
    # sample 5512 is inside cell 0 (tiled, so != itself) only when the cell
    # is 5513 long; at 5512 it would be the untouched head of cell 1.
    sr = 44100
    L = np.arange(sr, dtype=np.float64) / sr
    outL, _ = server._beat_repeat(L, L.copy(), sr, cell_s=0.125, repeats=2,
                                   chance=1.0, mix=1.0)
    assert outL[5513] == L[5513], "5513 must be the head of cell 1"
    assert outL[5512] != L[5512], "5512 must still be inside cell 0's tiling"


def test_beat_repeat_leaves_a_partial_final_cell_alone():
    # tiling into a cut-off cell puts a hard step at the loop seam
    sr = 44100
    n = int(sr * 0.25) + 1000  # 0.1s cells -> a 1000-sample remainder
    L = np.random.RandomState(1).randn(n)
    outL, _ = server._beat_repeat(L, L.copy(), sr, cell_s=0.1, repeats=4,
                                   chance=1.0, mix=1.0)
    tail = int(sr * 0.2)  # start of the last, partial cell
    assert np.array_equal(outL[tail:], L[tail:])


def test_beat_repeat_repeats_knob_changes_the_result():
    sr = 44100
    L = np.random.RandomState(2).randn(sr)
    two, _ = server._beat_repeat(L, L.copy(), sr, 0.1, 2, 1.0, 1.0)
    eight, _ = server._beat_repeat(L, L.copy(), sr, 0.1, 8, 1.0, 1.0)
    assert not np.array_equal(two, eight)


def test_beat_repeat_mix_is_a_real_crossfade():
    sr = 44100
    L = np.random.RandomState(3).randn(sr)
    dry = L.copy()
    wet, _ = server._beat_repeat(L, L.copy(), sr, 0.1, 4, 1.0, 1.0)
    half, _ = server._beat_repeat(L, L.copy(), sr, 0.1, 4, 1.0, 0.5)
    assert np.allclose(half, dry * 0.5 + wet * 0.5)


def test_beat_repeat_survives_the_export_endpoint():
    # the wet buffer changing is not proof the WAV writer sees it
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"br_mix": 1.0, "br_cell_s": 0.1, "br_repeats": 4,
                      "br_chance": 1.0})
    r = client.post(f"/api/project/{project_id}/export")
    assert r.status_code == 200
    out = Path(r.json()["path"])
    try:
        assert out.exists()
        from sound_engine import dsp
        L, R, sr = dsp.load_audio(out)
        assert np.abs(L).max() > 0.0  # not a silent "success"
        cell = int(np.floor(0.1 * sr + 0.5))
        slice_len = cell // 4
        start = next(i for i in range(6) if server._br_cell_is_picked(i, 1.0)) * cell
        assert np.allclose(L[start:start + slice_len],
                           L[start + slice_len:start + 2 * slice_len], atol=2e-3)
    finally:
        out.unlink(missing_ok=True)


def test_beat_repeat_rejects_a_nonsense_cell_length():
    project_id = _upload().json()["project_id"]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                    json={"br_mix": 1.0, "br_cell_s": 0.0, "br_repeats": 4, "br_chance": 1.0})
    assert r.status_code == 400


# --- Echo / delay (step 7, 2026-09-01) ---------------------------------
# The house rule is that every beat loops clean, so the ONE thing these
# tests exist to protect is that the echo wraps the seam instead of dying
# at the end of the buffer — which is exactly what the pedalboard.Delay
# wrapper this replaced would have done.

def test_echo_off_by_default_is_bit_identical():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"dly_mix": 0.0, "dly_time_s": 0.25, "dly_feedback": 0.5})
    assert np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


def test_echo_changes_the_buffer_when_mixed_in():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process", json={})
    dry = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    r = client.post(f"/api/project/{project_id}/channel/upload/process",
                    json={"dly_mix": 0.5, "dly_time_s": 0.05, "dly_feedback": 0.4})
    assert r.status_code == 200
    assert not np.array_equal(dry[0], server.PROJECTS[project_id]["channels"]["upload"]["wet"][0])


def test_echo_wraps_the_loop_seam():
    # the whole point of loop_delay: a hit near the END of the loop has to
    # echo onto the START, or bar 8 -> bar 1 has an audible hole
    ae = server.dsp.audio_engine
    n = 44100
    x = np.zeros(n)
    x[n - 100] = 1.0
    outL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=0.25, feedback=0.0,
                             mix=1.0, sr=44100)
    landed = (n - 100 + int(round(0.25 * 44100))) % n
    assert landed < n - 100          # it really did wrap around
    assert outL[landed] == pytest.approx(1.0)


def test_echo_taps_decay_by_the_feedback_amount():
    # 0.05 s at 44.1k = 2205 samples, and feedback 0.5 dies out (-80 dB)
    # after 14 taps — 14 * 2205 < 44100, so no tap wraps back onto another
    # one and each position holds exactly one echo. A delay that divides
    # the buffer evenly would stack tap 11 onto tap 1 and the levels below
    # would be off by feedback^10, which is real behaviour, not a bug.
    ae = server.dsp.audio_engine
    sr, n = 44100, 44100
    x = np.zeros(n)
    x[0] = 1.0
    d = int(round(0.05 * sr))
    outL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=0.05, feedback=0.5,
                             mix=1.0, sr=sr)
    assert outL[d] == pytest.approx(1.0)
    assert outL[2 * d] == pytest.approx(0.5)
    assert outL[3 * d] == pytest.approx(0.25)


def test_echo_a_whole_loop_long_is_a_no_op_not_a_gain_boost():
    # d % n == 0 would stack every echo straight back onto the dry
    ae = server.dsp.audio_engine
    x = np.random.RandomState(3).randn(44100)
    outL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=1.0, feedback=0.5,
                             mix=1.0, sr=44100)
    assert np.array_equal(outL, x)


def test_echo_feedback_is_clamped_so_it_cannot_run_away():
    ae = server.dsp.audio_engine
    x = np.random.RandomState(4).randn(44100)
    outL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=0.05, feedback=50.0,
                             mix=1.0, sr=44100)
    assert np.isfinite(outL).all()
    # documented bound is 1 + mix/(1 - 0.9) = 11x the dry peak
    assert np.abs(outL).max() <= 11.0 * np.abs(x).max()


def test_echo_rejects_a_nonsense_time():
    project_id = _upload().json()["project_id"]
    # strings, because a bare float("nan") is not JSON-encodable — same
    # shape as test_width_rejects_a_non_finite_value above
    for bad in ({"dly_time_s": "nan"}, {"dly_time_s": 99.0},
                {"dly_feedback": "inf"}, {"dly_mix": 2.0}):
        body = {"dly_mix": 0.5}
        body.update(bad)
        r = client.post(f"/api/project/{project_id}/channel/upload/process",
                        json=body)
        assert r.status_code == 400, bad


def test_echo_survives_the_export_endpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "EXPORT_DIR", tmp_path)
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"dly_mix": 0.6, "dly_time_s": 0.05, "dly_feedback": 0.4})
    r = client.post(f"/api/project/{project_id}/export")
    assert r.status_code == 200
    assert Path(r.json()["path"]).exists()


# --- Per-DJ FX presets (step 7, 2026-09-01) ----------------------------

def test_the_sub_is_never_given_effects(monkeypatch, tmp_path):
    """The owner's mix rule treats the sub as the kick's low end and leaves
    it alone. Written against a preset file that DOES define effects for
    every low-end lane: no shipped preset has a bass/sub entry today, so
    testing against the real file would pass with the guard deleted and
    prove nothing (it did — caught by mutation testing)."""
    from sound_engine import fx_presets
    # "bass drum" MUST be in this list. It is the name the 808 actually
    # has on disk (37 files), and without it here the test passed with
    # that entry deleted from _LOW_END — the one element that makes the
    # guard fire on a real beat. Caught by the second adversarial review;
    # the earlier version of this test proved nothing about it.
    loud = {"Otto Grit": {lane: {"sat_mix": 0.9, "sat_drive_db": 12.0}
                          for lane in ("bass", "bass drum", "sub", "808",
                                        "sub808", "kick")}}
    f = tmp_path / "fx_presets.json"
    f.write_text(json.dumps(loud))
    monkeypatch.setattr(fx_presets, "_PRESETS_PATH", f)
    for lane in ("bass0 - sampled bass (X), D# root", "sub - tuned sub",
                 "808 - long 808", "sub808 - x",
                 "bass drum - MZ Crash [808]", "bass drum - Oracle 808 5 - C"):
        assert fx_presets.for_lane("Otto Grit", lane, 91) == {}, lane
    # ...while the SAME file reaches the kick, which is not low end. That
    # is what makes this a test of the guard and not of an unloadable file.
    assert fx_presets.for_lane("Otto Grit", "kick - k", 91)["sat_mix"] == 0.9


def test_lane_role_strips_the_sample_name_and_the_family_number():
    from sound_engine import fx_presets
    assert fx_presets.lane_role("chord0 - piano stack + sample_ Bbm") == "chord"
    assert fx_presets.lane_role("bass2 - sampled bass (X), A# root") == "bass"
    assert fx_presets.lane_role("kick - swink_kick") == "kick"
    assert fx_presets.lane_role("upload") == "upload"   # no ' - ' at all


def test_note_values_resolve_against_the_beats_own_tempo():
    from sound_engine import fx_presets
    slow = fx_presets.for_lane("Otto Grit", "snare - x", 88)
    fast = fx_presets.for_lane("Otto Grit", "snare - x", 176)
    # a dotted 1/8 is a dotted 1/8 at either tempo, so the SECONDS must halve
    assert slow["dly_time_s"] == pytest.approx(2 * fast["dly_time_s"])
    assert slow["dly_note"] == fast["dly_note"] == 0.75


def test_a_beat_with_no_tempo_gets_no_timed_effects():
    # nothing to resolve a note value against — better off than sitting on
    # a guessed default bpm
    from sound_engine import fx_presets
    p = fx_presets.for_lane("Otto Grit", "snare - x", None)
    assert "dly_time_s" not in p and "dly_mix" not in p
    assert p["sat_mix"] > 0          # the untimed effects still apply


def test_an_untuned_dj_falls_through_to_the_gentle_default():
    from sound_engine import fx_presets
    p = fx_presets.for_lane("Some DJ Nobody Tuned Yet", "snare - x", 90)
    assert p == {"sat_drive_db": 3.0, "sat_mix": 0.08}


def test_a_broken_preset_file_does_not_stop_a_beat_opening(monkeypatch, tmp_path):
    from sound_engine import fx_presets
    bad = tmp_path / "fx_presets.json"
    bad.write_text("{ this is not json")
    monkeypatch.setattr(fx_presets, "_PRESETS_PATH", bad)
    assert fx_presets.for_lane("Otto Grit", "snare - x", 90) == {}


def test_from_beat_opens_the_rack_on_the_djs_settings(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Otto Grit"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(8820) / 44100) * 0.3
    write_wav24(dj / "9 Otto Grit Probe Drums 88bpm.wav", sig, sig)
    stems = dj / "9 Otto Grit Probe Stems"
    stems.mkdir()
    write_wav24(stems / "kick - k.wav", sig, sig)
    write_wav24(stems / "bass0 - b, D# root.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)

    r = client.post("/api/project/from-beat",
                     json={"beat_id": "Otto Grit/9 Otto Grit Probe"})
    assert r.status_code == 200
    by_lane = {c["lane_id"]: c["fx"] for c in r.json()["channels"]}
    assert by_lane["kick - k"]["sat_mix"] == 0.30     # Otto's kick
    assert by_lane["bass0 - b, D# root"] == {}        # the sub, untouched

    # and the preset is PRINTED, not just advertised: wet must differ from dry
    pid = r.json()["project_id"]
    chans = server.PROJECTS[pid]["channels"]
    assert not np.array_equal(chans["kick - k"]["dry"][0],
                              chans["kick - k"]["wet"][0])
    assert np.array_equal(chans["bass0 - b, D# root"]["dry"][0],
                          chans["bass0 - b, D# root"]["wet"][0])


def test_a_lane_name_containing_a_sharp_is_url_encoded_by_the_client():
    """Stem names carry note names, so '#' is everywhere in this library
    (D#, F#, A#). Unencoded in a URL it starts a fragment, and the request
    reached the server truncated at the sharp — every beat with a sharp in
    a stem name 404'd on load and could not be opened at all. There is no
    JS test runner in this project, so this scans the source for the one
    mistake that caused it."""
    app_js = (Path(__file__).resolve().parents[1]
              / "sound_engine/static/app.js").read_text()
    for bad in ("/channel/${ch.lane_id}", "/channel/${laneId}"):
        assert bad not in app_js, (
            f"{bad} builds a channel URL from an unencoded lane id — "
            "wrap it in encodeURIComponent()")


def test_the_owner_facing_stem_names_map_back_to_lanes():
    """Stems are written with the owner's names, not the internal lane
    keys (tools/beat_recipes.py:134): kick -> 'kick drum', and sub/bass ->
    'bass drum'. Found live: every preset silently missed the kick, and
    the leave-the-sub-dry guard never fired on a real beat, because both
    were matching names that only exist inside the generator."""
    from sound_engine import fx_presets
    assert fx_presets.lane_role("kick drum - HELLA KICK 016.wav") == "kick"
    assert fx_presets.for_lane("Night Metro", "kick drum - k", 147)["sat_mix"] == 0.38
    # the 808 under the kick, by its real filename — must stay untouched
    assert fx_presets.for_lane("Night Metro", "bass drum - MZ Crash [808]", 147) == {}
    assert fx_presets.for_lane("Rage Engine", "bass drum - x", 150) == {}


def test_a_lane_the_dj_was_never_tuned_for_still_gets_the_default():
    """Night Metro has no snare line, and plenty of its beats have a
    snare. Found live: that channel sat bone dry beside processed ones,
    which reads as a broken preset rather than a choice."""
    from sound_engine import fx_presets
    p = fx_presets.for_lane("Night Metro", "snare - PLAYOFFS", 147)
    assert p == {"sat_drive_db": 3.0, "sat_mix": 0.08}


def test_a_second_voicing_lane_matches_its_family():
    """chord0v1 is the second voicing of chord0 ('brass stack (lead)'
    beside 'strings (support)') and must get the DJ's chord settings.
    Found live on Rage Engine 1323, where those two lanes came back dry
    beside their own chord0/chord1."""
    from sound_engine import fx_presets
    assert fx_presets.lane_role("chord0v1 - brass stack (lead), Cm (i)") == "chord"
    assert (fx_presets.for_lane("Otto Grit", "chord0v1 - brass", 88)
            == fx_presets.for_lane("Otto Grit", "chord0 - strings", 88))


def test_an_all_digit_lane_name_still_hits_the_low_end_guard():
    """'808' is entirely digits, so stripping the family number emptied it
    and it slipped past the leave-the-sub-dry check."""
    from sound_engine import fx_presets
    assert fx_presets.lane_role("808 - long 808") == "808"
    assert fx_presets.for_lane("Rage Engine", "808 - long 808", 150) == {}


def test_echo_is_a_send_the_dry_never_ducks():
    """mix must ADD echoes on top of an untouched dry, not crossfade
    against it. Both the docstring and the live Web Audio graph promise
    this, and the browser's dry gain is hard-wired to unity — a server
    that crossfaded instead would quietly drop the dry by up to 6 dB on
    every channel with echo up, and live and export would disagree.

    Adversarial review found the original echo tests could not tell the
    two apart: `L*(1-mix) + mix*wet` and `0.5*L + mix*wet` both passed all
    eight of them."""
    ae = server.dsp.audio_engine
    sr, n = 44100, 44100
    x = np.zeros(n)
    x[0] = 1.0
    d = int(round(0.05 * sr))
    outL, outR = ae.loop_delay(x.copy(), x.copy(), seconds=0.05,
                               feedback=0.0, mix=0.5, sr=sr)
    # sample 0 carries dry only (the single echo lands at d, not here)
    assert outL[0] == 1.0 and outR[0] == 1.0
    assert outL[d] == pytest.approx(0.5)      # ...and the echo is scaled
    # raising mix must not move the dry at all
    hotL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=0.05,
                            feedback=0.0, mix=1.0, sr=sr)
    assert hotL[0] == 1.0


def test_echo_keeps_the_two_channels_independent():
    """Every original echo test passed the same array as L and R, so a wet
    path that fed both channels from L — collapsing the tail to mono —
    passed all of them. This echo sits BEFORE the reverb, so a mono tail
    then gets stereo width applied to it. (Adversarial review.)"""
    ae = server.dsp.audio_engine
    sr, n = 44100, 44100
    L = np.zeros(n); L[0] = 1.0        # impulse on the left only
    R = np.zeros(n)                    # right is silent
    d = int(round(0.05 * sr))
    outL, outR = ae.loop_delay(L, R, seconds=0.05, feedback=0.5, mix=1.0, sr=sr)
    assert outL[d] == pytest.approx(1.0)
    assert outR[d] == 0.0              # nothing may leak across
    assert not np.array_equal(outL, outR)


def test_an_echo_longer_than_the_material_is_dropped_not_folded():
    """A circular delay of 2 s on a 1.5 s buffer IS a 0.5 s delay once the
    buffer repeats — but the live DelayNode does not fold, so the browser
    played one rhythm and the export wrote another. Refusing the echo
    keeps both paths saying the same thing. (Adversarial review.)"""
    ae = server.dsp.audio_engine
    sr = 44100
    x = np.random.RandomState(7).randn(int(1.5 * sr))
    for seconds in (1.5, 2.0, 4.0):
        outL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=seconds,
                                feedback=0.5, mix=1.0, sr=sr)
        assert np.array_equal(outL, x), seconds
    # just under the buffer still works
    outL, _ = ae.loop_delay(x.copy(), x.copy(), seconds=1.4,
                            feedback=0.0, mix=1.0, sr=sr)
    assert not np.array_equal(outL, x)


def test_echo_rejects_mismatched_channel_lengths():
    ae = server.dsp.audio_engine
    with pytest.raises(ValueError):
        ae.loop_delay(np.zeros(1000), np.zeros(500), seconds=0.01,
                      feedback=0.0, mix=1.0, sr=44100)


# --- second adversarial review, 2026-09-01 ----------------------------

@pytest.mark.parametrize("bad", [
    '{"Otto Grit": "grit"}',                       # DJ entry is a string
    '[1, 2, 3]',                                   # top level is an array
    '{"Otto Grit": {"kick": "loud"}}',             # lane entry is a string
    '{"Otto Grit": {"kick": {"dly_note": "half"}}}',   # value is a string
    '{"_default": "gentle"}',
    '"just a string"',
    'null',
])
def test_a_structurally_wrong_preset_file_is_ignored_not_fatal(
        bad, monkeypatch, tmp_path):
    """_load() used to catch only OSError/JSONDecodeError, so valid JSON
    with the wrong SHAPE reached for_lane and raised — outside the try in
    from-beat, so EVERY beat open 500'd. The module docstring promised a
    broken file must not stop a beat opening; it did."""
    from sound_engine import fx_presets
    f = tmp_path / "fx_presets.json"
    f.write_text(bad)
    monkeypatch.setattr(fx_presets, "_PRESETS_PATH", f)
    monkeypatch.setattr(fx_presets, "_CACHE", {"mtime": None, "data": {}})
    assert fx_presets.for_lane("Otto Grit", "kick drum - k", 91) == {}


def test_a_broken_preset_file_still_lets_a_beat_open(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    from sound_engine import fx_presets
    dj = tmp_path / "Otto Grit"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "9 Otto Grit Probe Drums 88bpm.wav", sig, sig)
    stems = dj / "9 Otto Grit Probe Stems"
    stems.mkdir()
    write_wav24(stems / "kick drum - k.wav", sig, sig)
    bad = tmp_path / "fx_presets.json"
    bad.write_text('{"Otto Grit": "grit"}')
    monkeypatch.setattr(fx_presets, "_PRESETS_PATH", bad)
    monkeypatch.setattr(fx_presets, "_CACHE", {"mtime": None, "data": {}})
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)
    r = client.post("/api/project/from-beat",
                     json={"beat_id": "Otto Grit/9 Otto Grit Probe"})
    assert r.status_code == 200


def test_a_favourited_beat_keeps_its_djs_settings():
    """The Sound Engine names a beat by its FOLDER, so everything in
    Favorites/ reported dj='Favorites' and silently got the generic
    default — 60 beats, the folder he opens most. The DJ is in the
    filename."""
    from sound_engine import fx_presets
    assert fx_presets.resolve_dj("Favorites",
                                  "1219 Otto Grit Basement Stairs") == "Otto Grit"
    assert fx_presets.resolve_dj("Memphis",
                                  "1500 Night Metro Blue") == "Night Metro"
    # a real DJ folder is never overridden by whatever the filename says
    assert fx_presets.resolve_dj("Glass Cat",
                                  "1176 Otto Grit White Space") == "Glass Cat"
    # and an unknown personality stays unknown rather than guessing
    assert fx_presets.resolve_dj("Memphis", "1500 Memphis Thing") == "Memphis"
    assert (fx_presets.for_lane("Favorites", "kick drum - k", 88,
                                 beat_name="1219 Otto Grit Basement Stairs")
            == fx_presets.for_lane("Otto Grit", "kick drum - k", 88))


def test_a_beat_id_cannot_escape_the_library(tmp_path):
    """beat_id arrives from a URL (the FX button links to /?beat=...), and
    '../..' resolved to any '* Stems' folder on the disk."""
    from sound_engine import library
    outside = tmp_path / "outside"
    (outside / "secret Stems").mkdir(parents=True)
    (outside / "secret Stems" / "a.wav").write_bytes(b"x")
    root = tmp_path / "library"
    root.mkdir()
    assert library.find_beat(root, "../outside/secret") is None


def test_an_absurd_tempo_does_not_discard_the_whole_lane():
    """_BPM_RE will read '9999bpm' out of a filename. One out-of-range
    derived value used to take the lane's saturation and EQ down with it."""
    from sound_engine import fx_presets
    p = fx_presets.for_lane("Otto Grit", "snare - x", 9999)
    assert p["sat_mix"] == 0.28          # the untimed effects survive
    assert "dly_time_s" not in p         # the nonsense one is dropped
    assert fx_presets.for_lane("Otto Grit", "snare - x", "not a number")["sat_mix"]


def test_no_lane_is_left_bone_dry_beside_a_processed_one():
    """66 of 119 beats by the tuned four carried a lane nobody listed
    (reversefx, woods, vox, blips, claves, timbales, sirens...). _other is
    the catch-all — but it must never reach the sub."""
    from sound_engine import fx_presets
    for lane in ("reversefx - x", "woods - x", "vox - x", "timbales - x",
                 "claves - x", "sirens - x", "blips - x"):
        assert fx_presets.for_lane("Night Metro", lane, 147), lane
    for lane in ("bass drum - x", "bass0 - x", "sub - x", "808 - x"):
        assert fx_presets.for_lane("Night Metro", lane, 147) == {}, lane
