"""Turntable scratch engine — shape and level sanity, same bar as
test_chord_synth.py/test_instrument_sampler.py: wrong length throws off
a lane's timing, clipping or silence swamps or vanishes in the mix.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import scratch as scratch_mod                               # noqa: E402
from make_drum_loops import SR                               # noqa: E402
from scratch import PATTERNS, scratch                        # noqa: E402


def _tone(dur=0.4, freq=220):
    n = int(dur * SR)
    return np.sin(2 * np.pi * freq * np.arange(n) / SR)


def test_scratch_length_matches_duration():
    audio = scratch(_tone(), dur=1.0, pattern="baby")
    assert audio.shape == (int(1.0 * SR),)


def test_scratch_empty_source_is_silence():
    audio = scratch(np.array([]), dur=0.5)
    assert audio.shape == (int(0.5 * SR),)
    assert np.all(audio == 0.0)


def test_scratch_none_source_is_silence():
    audio = scratch(None, dur=0.3)
    assert audio.shape == (int(0.3 * SR),)
    assert np.all(audio == 0.0)


def test_scratch_zero_dur_is_empty():
    audio = scratch(_tone(), dur=0.0)
    assert audio.shape == (0,)


def test_scratch_stays_under_clipping_for_every_pattern():
    for name in PATTERNS:
        audio = scratch(_tone(), dur=0.8, pattern=name)
        assert np.max(np.abs(audio)) <= 0.9 + 1e-9, name


def test_scratch_unknown_pattern_falls_back_to_baby():
    known = scratch(_tone(), dur=0.6, pattern="baby")
    unknown = scratch(_tone(), dur=0.6, pattern="not-a-real-pattern")
    assert np.allclose(known, unknown)


def test_chirp_fader_closes_on_the_pullback():
    # chirp's back half should be much quieter than its front half —
    # that's the whole point of the pattern (hear the push, not the pull).
    audio = scratch(_tone(dur=1.0), dur=1.0, pattern="chirp", hit_dur=0.3)
    half = len(audio) // 2
    front = np.abs(audio[:half - 500]).mean()
    back = np.abs(audio[half + 500:]).mean()
    assert back < front * 0.5


def test_hit_dur_longer_than_source_is_clamped_not_out_of_range():
    # a hit_dur reaching past the source's own length must not read
    # outside the array — np.interp would just clamp, but confirm the
    # call doesn't raise and stays in range.
    short_src = _tone(dur=0.05)
    audio = scratch(short_src, dur=0.5, pattern="baby", hit_dur=5.0)
    assert audio.shape == (int(0.5 * SR),)
    assert np.max(np.abs(audio)) <= 0.9 + 1e-9


def test_scratch_position_curve_reads_forward_then_backward(monkeypatch):
    # sanity on the "baby" gesture itself, not just its audio output:
    # the position array _baby() returns should rise then fall.
    pos, fader = scratch_mod._baby(0.2, 1000)
    assert pos[250] < pos[499]          # rising through the first half
    assert pos[750] < pos[499]          # falling back by the second half
