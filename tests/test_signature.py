"""Signature chord-chooser helpers (HARMONY-IDENTITY-PROPOSAL 2026-07-22).

The weighted picker and the per-chord voice-order fallback are the only
new branchy logic behind the identity-aware harmonizer; the render path
that consumes them is exercised by test_beat_machine's chords test.
"""
import copy
import random
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent / "tools"))

import beat_machine                                        # noqa: E402
import chord_synth                                         # noqa: E402
import string_sampler                                      # noqa: E402
from crew import CREW                                       # noqa: E402


def test_wpick_flat_weighted_and_empty():
    r = random.Random(0)
    assert beat_machine._wpick(["F", "G", "C"], r) in ("F", "G", "C")
    assert beat_machine._wpick(None, r) is None
    assert beat_machine._wpick([], r) is None
    # a lopsided weight should dominate over many draws
    picks = [beat_machine._wpick([["a", 99], ["b", 1]], random.Random(i))
             for i in range(50)]
    assert picks.count("a") > picks.count("b")


def test_source_order_default_and_signature():
    r = random.Random(1)
    # no signature -> the historical loop-then-pad default, unchanged
    assert beat_machine._source_order(None, r) == ("loop", "synth")
    # a signature order always ends reachable at the synth-pad floor and
    # keeps every source the identity declared
    order = beat_machine._source_order([["strings", 2], ["synth", 1]], r)
    assert set(order) == {"strings", "synth"} and "synth" in order
    # a pref without synth still gets the pad appended as the never-fails floor
    order = beat_machine._source_order([["strings", 1]], r)
    assert order[0] == "strings" and order[-1] == "synth"


def test_by_articulation_styles():
    idx = [{"style": "sustain"}, {"style": "pizz"}, {"style": "short"}]
    assert string_sampler.by_articulation(idx, "pizz") == [{"style": "pizz"}]
    # no style named -> the held bed, not whichever file sorts first
    assert string_sampler.by_articulation(idx, None) == [{"style": "sustain"}]
    # a style with nothing indexed -> the whole index, never an empty pool
    assert string_sampler.by_articulation(idx, "bogus") == idx


def test_arp_riff_length_pattern_and_unvoiceable_steps():
    SR = chord_synth.SR
    dur, bpm = 2.0, 120.0                       # eighths = 0.25s -> 8 steps
    # render_note returning None used to fall back to a synthesized pluck.
    # That synth is deleted (owner 2026-07-23) — an unvoiceable step is now
    # left SILENT, so an all-None render_note gives a silent buffer, which
    # is what _build_chords reads as "this voice failed, try the next".
    buf = chord_synth.arp_riff([48, 51, 55], dur, bpm, lambda n, d: None)
    assert len(buf) == int(dur * SR)
    assert np.max(np.abs(buf)) == 0.0           # silent, and no NaN
    assert not np.isnan(buf).any()
    # a real sampled step is audible and peak-guarded
    loud = chord_synth.arp_riff(
        [48, 51, 55], dur, bpm,
        lambda n, d: np.ones(int(d * SR)) * 0.8)
    assert 0.0 < np.max(np.abs(loud)) <= 1.0
    # render_note is actually driven, ascending through the octave, cycling
    calls = []
    chord_synth.arp_riff([48, 51, 55], dur, bpm,
                         lambda n, d: calls.append(n) or np.zeros(int(d * SR)))
    assert len(calls) == 8 and calls[:4] == [48, 51, 55, 60] \
        and calls[4:] == [48, 51, 55, 60]
    # empty chord -> silent buffer, no crash
    assert np.max(np.abs(chord_synth.arp_riff(
        [], dur, bpm, lambda n, d: None))) == 0.0


def test_signature_tempo_range_clamps_the_lean():
    # owner request 2026-07-23: Dre's keepers all sat 90-93; the 98bpm
    # rolls missed. A signature's tempo range keeps vary_preset's normal
    # +/-5% wander inside the identity's pocket instead of drifting out.
    lo, hi = CREW["Doc Day"]["signature"]["tempo"]
    for v in range(60):
        p = copy.deepcopy(CREW["Doc Day"])
        beat_machine.vary_preset(p, v, p["num"], tempo_locked=False)
        assert lo <= p["bpm"] <= hi, (v, p["bpm"])
    # an explicit typed tempo still wins — the lean/clamp never runs
    p = copy.deepcopy(CREW["Doc Day"])
    p["bpm"] = 120
    beat_machine.vary_preset(p, 1, p["num"], tempo_locked=True)
    assert p["bpm"] == 120
