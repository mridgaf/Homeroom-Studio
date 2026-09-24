"""Melodic-loop ingestion (punch list step 5, via filename metadata) —
the pure token-parsing and fitting math, no drive needed. `scan()` walks
`sample_packs.json` roots and isn't covered here (same reason
test_midi_packs.py skips `scan()`).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from key_context import KeyContext                                    # noqa: E402
from melodic_loops import (bpm_from_tokens, chop_onsets, fit_loop,     # noqa: E402
                            in_key, key_from_tokens)


def test_key_from_tokens_reads_a_bare_minor_token():
    assert key_from_tokens(["FL", "TT", "140", "Bass", "Synth", "Gm"]) \
        == ("G", "minor")


def test_key_from_tokens_reads_a_bare_major_root():
    # Cymatics one-shots carry no mode marker at all — root only.
    assert key_from_tokens(["Cymatics", "KEYS", "Alloy", "C"]) == ("C", None)


def test_key_from_tokens_skips_a_trailing_qualifier():
    # "090_Bounce_F Mod/090_Bounce_Bass F.aif" -> key token isn't last.
    assert key_from_tokens(["090", "Bounce", "F", "Mod"]) == ("F", None)


def test_key_from_tokens_none_when_absent():
    assert key_from_tokens(["FL", "TT", "Drum", "Loops", "Kick", "140"]) is None


def test_key_from_tokens_ignores_non_note_letters():
    assert key_from_tokens(["Function", "Loops", "Vocal", "Pop"]) is None


def test_bpm_from_tokens_reads_the_plausible_number():
    tokens = "FL_TT_140_Bass_Synth_Boston_808_Gm".split("_")
    assert bpm_from_tokens(tokens) == 140


def test_bpm_from_tokens_ignores_808_as_a_tempo():
    assert bpm_from_tokens(["Bass", "808", "Gm"]) is None


def test_bpm_from_tokens_none_when_absent():
    assert bpm_from_tokens(["Cymatics", "KEYS", "Alloy", "C"]) is None


def test_bpm_from_tokens_reads_glued_bpm_suffix():
    # Looperman / Freesound loops are named "..._Am_140bpm" (2026-09-24).
    tokens = "looperman-l-5565495-0328305-spacey-pad_Am_140bpm".replace("-", "_").split("_")
    assert bpm_from_tokens(tokens) == 140
    assert bpm_from_tokens(["loop", "C", "nokey", "80BPM"]) == 80
    assert bpm_from_tokens(["loop", "300bpm"]) is None


def _entry(key, mode, bpm, role="melody", **kw):
    e = {"name": "x", "path": "/x", "kind": "loop", "role": role,
         "key": key, "mode": mode, "bpm": bpm}
    e.update(kw)
    return e


def test_in_key_prefers_exact_match_then_same_mode():
    idx = [
        _entry("C", "minor", 140),     # exact
        _entry("D", "minor", 140),     # same mode, different root
        _entry("C", "major", 140),     # wrong mode entirely -> excluded
    ]
    ranked = in_key(idx, KeyContext("C", "minor"))
    assert [(e["key"], e["mode"]) for e in ranked] == [("C", "minor"), ("D", "minor")]


def test_in_key_root_only_entry_matches_either_mode():
    idx = [_entry("C", None, None)]
    assert in_key(idx, KeyContext("C", "minor")) == idx
    assert in_key(idx, KeyContext("C", "major")) == idx


def test_in_key_sorts_exact_tier_by_bpm_closeness():
    idx = [_entry("C", "minor", 90), _entry("C", "minor", 140)]
    ranked = in_key(idx, KeyContext("C", "minor"), bpm=138)
    assert ranked[0]["bpm"] == 140


def test_in_key_filters_by_role():
    idx = [_entry("C", "minor", 140, role="bass"),
           _entry("C", "minor", 140, role="melody")]
    assert [e["role"] for e in in_key(idx, KeyContext("C", "minor"), role="bass")] \
        == ["bass"]


def test_fit_loop_pitch_shifts_and_shortens_when_pitching_up():
    x = np.sin(2 * np.pi * 110 * np.arange(4410) / 44100)
    out = fit_loop(x, 44100, dst_secs=0.1,
                    src_key=KeyContext("C", "minor"),
                    dst_key=KeyContext("D", "minor"))  # up 2 semitones
    assert len(out) == int(0.1 * 44100)


def test_fit_loop_no_key_change_is_plain_crop():
    x = np.arange(100.0)
    out = fit_loop(x, sr=1000, dst_secs=0.05)  # no keys given -> ratio 1.0
    assert list(out) == list(x[:50])


def test_fit_loop_tiles_a_short_loop_to_fill_the_length():
    x = np.array([1.0, 2.0, 3.0])
    out = fit_loop(x, sr=3, dst_secs=2.0)  # needs 6 samples from 3
    assert list(out) == [1.0, 2.0, 3.0, 1.0, 2.0, 3.0]


def test_chop_onsets_splits_two_separated_bursts():
    x = np.concatenate([np.zeros(200), np.ones(300), np.zeros(100),
                         np.ones(300), np.zeros(100)])
    clips = chop_onsets(x, sr=1000, min_dur=0.15, max_dur=1.0)
    assert len(clips) == 2


def test_chop_onsets_empty_input_is_empty():
    assert chop_onsets(np.array([]), sr=1000) == []


def test_chop_onsets_fades_the_clip_tail():
    x = np.concatenate([np.zeros(200), np.ones(500)])
    clips = chop_onsets(x, sr=1000, min_dur=0.15, max_dur=1.0)
    assert len(clips) == 1
    mid = len(clips[0]) // 2
    assert clips[0][-1] < clips[0][mid]         # faded toward zero at the tail
