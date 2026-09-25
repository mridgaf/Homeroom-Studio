"""The low end set up the way a hip-hop producer would (owner 2026-09-23):
one bass note at a time, every bass ducks under the kick, the kick stays on
top, chords stay out of the bass's room, no machine-made tones -- and the
Loops page is left exactly as it was."""
import copy
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import crew  # noqa: E402
from crew import CREW, SR, render_crew_beat  # noqa: E402


def _preset(lanes, sidechain=0.0, sub_sidechain=0.0):
    p = copy.deepcopy(CREW["Cutz"])
    p["lanes"] = lanes
    p["space"] = ("dry", [])
    p["sidechain"] = sidechain
    p["sub_sidechain"] = sub_sidechain
    return p


def _kick():
    t = np.arange(SR // 8) / SR
    return np.sin(2 * np.pi * 60 * t) * np.exp(-t * 30)


def _stem(parts, lane):
    sL, sR = parts["stems"][lane]
    return (sL + sR) / 2


def test_one_bass_note_at_a_time():
    """Each new 808 note cuts the last (a sampler's "cut itself"). With a
    constant tone, the level after the 2nd hit is the 2nd hit alone -- not
    the two tails summed, which is what used to happen."""
    p = _preset({"kick": (0.0, 1.0, (0, 0, 50, 1), ["X---------------"]),
                 "bass": (0.0, 1.0, (0, 0, 50, 2), ["X-------X-------"])})
    kit = {"kick": _kick(), "bass": np.full(20 * SR, 0.3)}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    (t1, v1), (t2, v2) = parts["events"]["bass"][:2]
    x = _stem(parts, "bass")
    a = x[int((t1 + (t2 - t1) / 2) * SR)]
    b = x[int((t2 + (t2 - t1) / 2) * SR)]
    assert abs(b / a - v2 / v1) < 0.02, (b / a, v2 / v1)


def test_the_bass_line_ducks_as_deep_as_the_808():
    """bass0..N are bass too: kick first, then the bass swells back in."""
    def dip(sub_sc):
        p = _preset({"kick": (0.0, 1.0, (0, 0, 50, 1), ["X-------X-------"]),
                     "bass0": (0.0, 1.0, (0, 0, 50, 2), ["X---------------"])},
                    sidechain=0.2, sub_sidechain=sub_sc)
        kit = {"kick": _kick(), "bass0": np.full(20 * SR, 0.3)}
        _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                                want_parts=True)
        x = _stem(parts, "bass0")
        k = parts["events"]["kick"][1][0]
        return x[int((k + 0.005) * SR)] / x[int((k - 0.02) * SR)]
    import beat_machine as bm
    deep = dip(bm.SUB_DUCK_DEFAULT)
    assert deep < 0.65, deep                 # a ~5 dB dip, like the 808
    assert deep < dip(0.2) - 0.1             # and deeper than the mix duck


def test_the_kick_stays_on_top_of_the_bass_at_true_levels(monkeypatch):
    monkeypatch.setattr(crew, "TRUE_LEVELS", True)
    p = _preset({"kick": (0.0, 1.0, (0, 0, 50, 1), ["X-------X-------"]),
                 "bass": (0.0, 1.0, (0, 0, 50, 2), ["X-------X-------"]),
                 "bass0": (0.0, 1.0, (0, 0, 50, 3), ["----X-----------"])})
    kit = {"kick": _kick() * 0.2, "bass": np.full(SR // 4, 0.9),
           "bass0": np.full(SR // 4, 0.9)}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    kick = np.abs(np.stack(parts["stems"]["kick"])).max()
    for lane in ("bass", "bass0"):
        pk = np.abs(np.stack(parts["stems"][lane])).max()
        assert 20 * np.log10(pk / kick) <= crew.LOW_END_UNDER_DB + 0.05, lane


def _loudest(x):
    n = int(crew.LOUD_WINDOW_S * SR)
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([x, x[:n]]) ** 2)])
    return np.sqrt((c[n:] - c[:-n]).max() / n)


def test_the_bass_sounds_quieter_than_the_kick(monkeypatch):
    """Owner 2026-09-24: "The bass note or instrument is significantly louder
    than everything." A held bass note can peak UNDER the kick and still
    sound far louder, so the peak cap alone let it through. This bass peaks
    at half the kick -- the peak cap never fires -- and must still come out
    LOW_END_LOUD_UNDER_DB under the kick by loudness."""
    monkeypatch.setattr(crew, "TRUE_LEVELS", True)
    p = _preset({"kick": (0.0, 1.0, (0, 0, 50, 1), ["X---X---X---X---"]),
                 "bass": (0.0, 1.0, (0, 0, 50, 2), ["X-------X-------"])})
    kit = {"kick": _kick(), "bass": np.full(20 * SR, 0.5)}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    kick = _loudest(_stem(parts, "kick"))
    bass = _loudest(_stem(parts, "bass"))
    assert 20 * np.log10(bass / kick) <= crew.LOW_END_LOUD_UNDER_DB + 0.1


def test_chords_stay_out_of_the_bass_room():
    p = _preset({"kick": (0.0, 1.0, (0, 0, 50, 1), ["X---------------"]),
                 "chord0": (0.0, 0.5, (0, 0, 50, 3), ["X---------------"])})
    t = np.arange(20 * SR) / SR
    kit = {"kick": _kick(),
           "chord0": 0.3 * (np.sin(2 * np.pi * 50 * t)
                            + np.sin(2 * np.pi * 1000 * t))}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    x = _stem(parts, "chord0")
    spec = np.abs(np.fft.rfft(x))
    f = np.fft.rfftfreq(len(x), 1 / SR)
    lo = spec[np.abs(f - 50) < 2].max()
    hi = spec[np.abs(f - 1000) < 2].max()
    assert 20 * np.log10(lo / hi) < -40


def test_no_sine_is_layered_into_the_kick(monkeypatch, tmp_path):
    """Owner hard rule: no tones created by machine. Otto Grit and Doc Day
    still carry sub_layer in their configs; it must never be applied."""
    called = []
    monkeypatch.setattr(crew, "LOCK", tmp_path / "crew_kits.json")
    monkeypatch.setattr(crew, "kick_sub_reinforce",
                        lambda x, **k: called.append(1) or x)
    shots = crew.build_shots()
    stamps = crew.lock_stamps(shots)
    for name in ("Otto Grit", "Doc Day"):
        assert CREW[name].get("sub_layer"), "fixture proves nothing"
        crew.build_kit(shots, name, stamps[name][1], variant=0)
    assert not called


def test_the_loops_page_is_untouched_by_the_low_end_rules(monkeypatch):
    """Turning every new low-end knob to an extreme changes nothing on a
    loops beat: its chordloop keeps its lows, nothing chokes, nothing caps."""
    bpm, nbars = 120, 2
    n = int(round(nbars * 4 * 60 / bpm * SR))
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)
    loops = {"kick": rng.standard_normal(n) * 0.05,
             "bassloop": np.sin(2 * np.pi * 45 * t) * 0.5,
             "chordloop": np.sin(2 * np.pi * 70 * t) * 0.3}
    p = copy.deepcopy(CREW["Cutz"])
    p["bpm"] = bpm
    p["lanes"] = {ln: (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),))
                  for ln in loops}

    def render():
        L, _R, *_ = render_crew_beat(
            "Test", kit={}, preset=copy.deepcopy(p), want_parts=True,
            loop_bufs={ln: (x, x) for ln, x in loops.items()},
            nbars_override=nbars)
        return L
    before = render()
    monkeypatch.setattr(crew, "CHORD_LOW_CUT_HZ", 2000.0)
    monkeypatch.setattr(crew, "LOW_END_UNDER_DB", -30.0)
    monkeypatch.setattr(crew, "LOW_END_LOUD_UNDER_DB", -30.0)
    assert np.array_equal(before, render())
