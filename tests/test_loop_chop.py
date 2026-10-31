"""Crate digger: the Loops side chops the lead loop (owner 2026-10-31,
PLAN-B-CRATE-DIGGER.md). Synthetic test tones only, never in a beat."""
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import loop_lanes
import melodic_loops as ml
from make_drum_loops import SR, write_wav24

BPM = 90
BAR = int(round(240.0 / BPM * SR))
C_MAJ, F_SHARP = (261.63, 329.63, 392.0), (369.99, 466.16, 554.37)


def _loop():
    """2 bars, 8 half-note hits: six C major, then two F# major (a chord
    change the chopper must leave out)."""
    x = np.zeros(2 * BAR)
    hit = BAR // 4 * 2 // 2                    # a quarter note
    t = np.arange(hit) / SR
    for i in range(8):
        chord = C_MAJ if i < 6 else F_SHARP
        tone = sum(np.sin(2 * np.pi * f * t) for f in chord) * np.exp(-t * 6)
        x[i * hit:(i + 1) * hit] += 0.2 * tone
    return np.stack([x, x], axis=1)


def _energy(y, freqs):
    mag = np.abs(np.fft.rfft(y.mean(axis=1)))
    f = np.fft.rfftfreq(len(y), 1.0 / SR)
    return sum(mag[np.abs(f - q) < 3].sum() for q in freqs)


def _onsets_off_grid(y):
    six = 2 * BAR / 32.0
    return [s for s in ml.onset_starts(y.mean(axis=1), SR, 0.08)
            if min(s % six, six - s % six) > 0.004 * SR]


def test_each_style_makes_a_new_two_bar_phrase_of_one_chord():
    x = _loop()
    for style in loop_lanes.CHOP_STYLES:
        spec = {"style": style, "seed": 7, "resample": False}
        y = loop_lanes.chop(x, SR, BPM, spec)
        assert y.shape == (2 * BAR, 2)
        assert not np.allclose(y, x)                       # re-ordered
        np.testing.assert_array_equal(y, loop_lanes.chop(x, SR, BPM, spec))
        # one chord: the F# hits never make it into the phrase
        assert _energy(y, F_SHARP) < 0.05 * _energy(y, C_MAJ), style


def test_styles_sound_different():
    x = _loop()
    def silent(style, seed):
        y = loop_lanes.chop(x, SR, BPM, {"style": style, "seed": seed})
        return np.mean(np.abs(y[:, 0]) < 1e-4)
    seeds = range(6)
    # stabs leave gaps, held rings to the next hit
    assert np.mean([silent("stabs", s) for s in seeds]) > \
        np.mean([silent("held", s) for s in seeds]) + 0.1
    off = {st: sum(len(_onsets_off_grid(loop_lanes.chop(
        x, SR, BPM, {"style": st, "seed": s}))) for s in seeds)
        for st in ("stabs", "loose")}
    assert off["loose"] > off["stabs"]                     # Dilla slides


def test_resample_chops_the_chop():
    x = _loop()
    once = loop_lanes.chop(x, SR, BPM, {"style": "loose", "seed": 3})
    twice = loop_lanes.chop(x, SR, BPM, {"style": "loose", "seed": 3,
                                         "resample": True})
    assert twice.shape == once.shape and not np.allclose(twice, once)


def test_chopped_lane_is_eight_bars_and_loops_seamlessly(tmp_path):
    loop = tmp_path / "Piano Loop 90bpm Cmaj.wav"
    x = _loop()
    write_wav24(loop, x[:, 0], x[:, 1])
    spec = {"style": "stabs", "seed": 11, "resample": True}
    L, R = loop_lanes.build_lane("leadloop", str(loop), BPM, SR, chop_spec=spec)
    assert len(L) == 8 * BAR
    for k in (1, 2, 3):                                    # 2-bar phrase x4
        np.testing.assert_array_equal(L[:2 * BAR], L[k * 2 * BAR:(k + 1) * 2 * BAR])
    whole, _ = loop_lanes.build_lane("leadloop", str(loop), BPM, SR)
    assert not np.allclose(L, whole)


def test_only_pack_labelled_keys_chop_and_half_the_beats():
    ok = {"path": "/x/Melody/Piano Loop 90bpm Cm.wav", "key": "C"}
    assert loop_lanes.chop_ok(ok)
    assert not loop_lanes.chop_ok({"path": "/x/Melody/synth100_GMaj_140.wav",
                                   "key": "G"})              # detector guess
    assert not loop_lanes.chop_ok({"path": "/x/Melody/Loop.wav", "key": None})
    assert loop_lanes.chop_roll(None, random.Random(1), ok) is None
    rolls = [loop_lanes.chop_roll("held", random.Random(i), ok) for i in range(1000)]
    chopped = [r for r in rolls if r]
    assert 0.45 < len(chopped) / 1000 < 0.55
    assert 0.18 < sum(r["resample"] for r in chopped) / len(chopped) < 0.32
