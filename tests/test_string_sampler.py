"""Strings sampler (harmonizer step 2) — the pure token-parsing and
chord-stacking math, no drive needed. `scan()` walks the library root
and isn't covered here (same reason test_melodic_loops.py skips it).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import string_sampler                                          # noqa: E402
from make_drum_loops import SR                                # noqa: E402
from string_sampler import nearest, note_from_tokens, play_chord  # noqa: E402


def test_note_from_tokens_reads_the_single_note():
    assert note_from_tokens(["pizz", "55", "ff", "RR1", "c"]) == 55


def test_note_from_tokens_drops_legato_transition_two_notes():
    # susbowleg_55_56_17_17: two plausible-note tokens (the bow moving
    # 55->56) -> not one playable pitch, so it's excluded.
    assert note_from_tokens(["susbowleg", "55", "56", "17", "17"]) is None


def test_note_from_tokens_ignores_out_of_range_numbers():
    # "17" is below the piano floor, so a name whose only note-ish token
    # is 17 has no playable note.
    assert note_from_tokens(["down", "17", "c"]) is None


def test_note_from_tokens_none_when_no_number():
    assert note_from_tokens(["down", "c"]) is None


def _entry(note, instrument="violin", artic="pizz"):
    return {"path": "/x", "note": note, "instrument": instrument,
            "artic": artic}


def test_nearest_picks_closest_pitch():
    idx = [_entry(50), _entry(60), _entry(72)]
    assert nearest(idx, 64)["note"] == 60      # 64 is closer to 60 than 72


def test_nearest_filters_by_instrument():
    idx = [_entry(60, instrument="violin"), _entry(60, instrument="basses")]
    assert nearest(idx, 60, instrument="basses")["instrument"] == "basses"


def test_nearest_empty_pool_is_none():
    assert nearest([], 60) is None


def test_play_chord_length_and_no_clipping(monkeypatch):
    idx = [_entry(60), _entry(64), _entry(67)]
    monkeypatch.setattr(string_sampler, "load_audio",
                        lambda path: np.ones(SR // 2))   # 0.5s mono per note
    chord = play_chord(idx, [60, 64, 67], dur=1.0)
    assert chord.shape == (SR,)                          # tiled to a full sec
    assert np.max(np.abs(chord)) < 1.0


def test_play_chord_none_when_nothing_voiced():
    assert play_chord([], [60, 64, 67], dur=1.0) is None


def test_play_chord_peak_guard_prevents_clipping(monkeypatch):
    # a hot transient (crest well above the RMS target) must be pulled
    # back under 1.0, not handed back clipping.
    idx = [_entry(60), _entry(64), _entry(67)]
    spike = np.zeros(SR // 2)
    spike[0] = 8.0                                       # huge crest, tiny RMS
    monkeypatch.setattr(string_sampler, "load_audio", lambda path: spike)
    chord = play_chord(idx, [60, 64, 67], dur=1.0)
    assert np.max(np.abs(chord)) <= 0.99
