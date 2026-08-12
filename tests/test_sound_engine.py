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
