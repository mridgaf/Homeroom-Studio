"""Bass / low-end clean-up on every beat as it is made (owner 2026-10-18)."""
import copy
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

import base_clean  # noqa: E402
import crew  # noqa: E402
from crew import CREW, SR, render_crew_beat  # noqa: E402


def _tone(f, secs=4, amp=0.3):
    return amp * np.sin(2 * np.pi * f * np.arange(secs * SR) / SR)


def _rms(x):
    x = x[SR:]                      # skip the first second
    return float(np.sqrt(np.mean(x ** 2)))


def _db(a, b):
    return 20 * np.log10(_rms(a) / _rms(b))


def test_roles_and_who_skips_the_rumble_cut():
    assert base_clean.role_of("chord0v1") == "chord"
    assert base_clean.role_of("bass0") == "bass"
    assert base_clean.role_of("kick drum - Cymatics Kong.wav") == "kick"
    assert all(base_clean.skips_rumble_cut(r) for r in ("kick", "kicklayer", "sub", "bass", "808"))
    assert not base_clean.skips_rumble_cut("hat")


def test_rumble_cut_and_chord_cut_numbers():
    assert _db(base_clean.lane_lowcut(_tone(20), "hat"), _tone(20)) < -5       # 20 Hz rumble
    assert abs(_db(base_clean.lane_lowcut(_tone(1000), "hat"), _tone(1000))) < 0.2
    assert _db(base_clean.lane_lowcut(_tone(80), "chord0"), _tone(80)) < -7    # chord low cut
    assert abs(_db(base_clean.lane_lowcut(_tone(1000), "chord0"), _tone(1000))) < 0.5
    for lane in ("kick", "bass", "sub", "bass0"):                              # fundamentals kept
        assert abs(_db(base_clean.lane_lowcut(_tone(35), lane), _tone(35))) < 0.01


def test_bass_is_centred_below_the_edge_and_left_alone_above():
    x = _tone(60)
    L, R = base_clean.mono_below(x, -x, SR)
    assert _rms(L - R) < 0.001 * _rms(x)
    y = _tone(400)
    L, R = base_clean.mono_below(y, -y, SR)
    assert abs(_db(L - R, 2 * y)) < 0.01


def test_a_looped_lane_has_no_seam_click():
    x = _tone(100, secs=2)                       # whole cycles: wraps cleanly
    y = base_clean.lane_lowcut(x, "chord0")
    assert abs(y[0] - y[-1]) < np.abs(np.diff(y)).max()


def _preset(lanes):
    p = copy.deepcopy(CREW["Cutz"])
    p["lanes"] = lanes
    p["space"] = ("dry", [])
    p["sidechain"] = 0.0
    p["sub_sidechain"] = 0.0
    return p


def test_every_rendered_beat_carries_the_cleanup_in_the_stems(monkeypatch):
    """Same beat rendered with the clean-up switched off and on: a 20 Hz
    rumble on the hat and snare must drop in the stems (the chord 150 Hz cut
    and the 808 are covered by the unit tests above)."""
    lanes = {n: (0.0, 1.0, (0, 0, 50, i + 1), ["X---------------"])
             for i, n in enumerate(["kick", "hat", "snare", "bass"])}
    kit = {"kick": _tone(60, 1), "hat": _tone(20, 20), "snare": _tone(20, 20),
           "bass": _tone(40, 20)}

    def stems():
        _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=_preset(lanes),
                                                want_parts=True)
        return {k: (v[0] + v[1]) / 2 for k, v in parts["stems"].items()}

    def at(x, f):
        k = np.abs(np.fft.rfft(x))
        return float(k[np.argmin(np.abs(np.fft.rfftfreq(len(x), 1 / SR) - f))])

    on = stems()
    monkeypatch.setattr(base_clean, "lane_lowcut", lambda x, lane, sr=44100: x)
    off = stems()
    # stems share one overall gain that moves when a lane changes, so judge
    # each lane against the 808 (which the clean-up leaves alone)
    for lane in ("hat", "snare"):
        assert (at(on[lane], 20) / at(on["bass"], 40)
                < 0.7 * at(off[lane], 20) / at(off["bass"], 40)), lane


def test_write_stems_leaves_the_already_cleaned_marker(tmp_path):
    from beat_recipes import write_stems
    sig = _tone(300, 1)
    folder = write_stems(tmp_path / "S", {"hat": (sig, sig)})
    assert (Path(folder) / base_clean.MARKER).exists()


def test_sound_engine_does_not_cut_a_marked_beat_twice(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from sound_engine import server
    from make_drum_loops import write_wav24
    client = TestClient(server.app)
    dj = tmp_path / "Otto Grit"
    dj.mkdir()
    sig = _tone(20, 2)
    write_wav24(dj / "9 Otto Grit Probe Drums 88bpm.wav", sig, sig)
    stems = dj / "9 Otto Grit Probe Stems"
    stems.mkdir()
    write_wav24(stems / "hat - h.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)

    def wet_level():
        r = client.post("/api/project/from-beat", json={"beat_id": "Otto Grit/9 Otto Grit Probe"})
        assert r.status_code == 200
        ch = server.PROJECTS[r.json()["project_id"]]["channels"]["hat - h"]
        return _rms(ch["wet"][0]) / _rms(ch["dry"][0]), ch["pre_clean"]

    cut, flag = wet_level()
    assert not flag and cut < 0.6                  # old beat: Sound Engine cleans it
    (stems / base_clean.MARKER).write_text("1")
    kept, flag = wet_level()
    assert flag and kept > 0.9                     # new beat: already clean, left alone
