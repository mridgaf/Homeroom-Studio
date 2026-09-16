"""Whole-beat-from-loops (owner 2026-09-16 correction, DECISIONS.md):
loop_mode.match_lengths (the length-matching-by-repetition rule) and
render_crew_beat's loop_bufs/nbars_override override (a loop lane plays
itself instead of one-shots stamped on a grid). Not a full render —
tools/beat_machine.py's _pick_loop_bed needs a real, mounted sample
library and isn't exercised here."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import loop_mode
import variety
from crew import SR, render_crew_beat
from test_audio_quality import _side_vs_mid_db


def test_bars_in_rounds_to_nearest_whole_bar():
    bpm = 120
    bar_samples = int(round(4 * (4 / 4) * 60 / bpm * SR))
    assert loop_mode.bars_in(bar_samples, SR, bpm) == 1
    assert loop_mode.bars_in(bar_samples * 4, SR, bpm) == 4


def test_tile_to_repeats_and_trims_exactly():
    x = np.array([1.0, 2.0, 3.0])
    out = loop_mode.tile_to(x, 8)
    assert len(out) == 8
    assert list(out) == [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0]
    assert list(loop_mode.tile_to(x, 2)) == [1.0, 2.0]


def test_match_lengths_doubles_the_shorter_loop():
    """Owner's own example: a 4-bar loop doubles alongside an 8-bar
    loop, rather than either being cropped or stretched."""
    bpm = 120
    bar_s = 4 * (4 / 4) * 60 / bpm
    short = np.full(int(round(4 * bar_s * SR)), 0.5)   # 4 bars
    long = np.full(int(round(8 * bar_s * SR)), 0.25)   # 8 bars
    matched, common_bars = loop_mode.match_lengths(
        {"kick": short, "chord0": long}, SR, bpm)
    assert common_bars == 8
    assert len(matched["kick"]) == len(matched["chord0"])
    # the short loop actually repeated (not zero-padded or cropped)
    half = len(matched["kick"]) // 2
    assert np.allclose(matched["kick"][:half], matched["kick"][half:])


def _loop_preset(bpm, nbars, space=("dry", [])):
    return dict(
        num=1, bpm=bpm, kick_dist=0.0, dust=0.0, vinyl=0, wow=0.0,
        mix_sat=0.0, drive=1.0, sidechain=0.0, space=space, alt=None,
        lanes={
            "kick": (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),)),
            "chord0": (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),)),
        },
    )


def test_render_crew_beat_loop_lane_plays_the_loop_verbatim():
    """A lane named in loop_bufs skips the one-shot grid and its onsets
    stay empty (owner 2026-09-16: skip sidechain duck for loop lanes —
    duck() only fires at onsets["kick"], so an empty list is a no-op,
    not a special case)."""
    bpm = 120
    nbars = 2
    bar_s = 4 * (4 / 4) * 60 / bpm
    n = int(round(nbars * bar_s * SR))
    loop_sig = np.sin(np.linspace(0, 20 * np.pi, n)) * 0.3
    L, R, lufs, parts = render_crew_beat(
        "Test", kit={}, preset=_loop_preset(bpm, nbars), want_parts=True,
        loop_bufs={"kick": (loop_sig, loop_sig),
                  "chord0": (loop_sig * 0.5, loop_sig * 0.5)},
        nbars_override=nbars)
    assert len(L) == len(R) == n
    assert parts["events"]["kick"] == []      # no discrete hits recorded
    assert not np.allclose(L, 0.0)            # the loop actually sounded


def test_render_crew_beat_loop_lane_keeps_real_stereo_width():
    """Regression for the bug the first real proof render caught: a
    loop lane panned dead center with no reverb rolled came out
    genuinely mono, because nothing else in a 2-lane loop beat carries
    width. render_crew_beat must derive width from the loop's OWN L/R
    difference, not from the random space roll -- checked here across
    both a "dry" roll (nothing fires) and a "gated" roll (fires with
    empty onsets, which used to overwrite width with silence)."""
    bpm = 120
    nbars = 2
    bar_s = 4 * (4 / 4) * 60 / bpm
    n = int(round(nbars * bar_s * SR))
    # broadband noise, not a low sine: the final mix intentionally forces
    # everything below 120 Hz to mono (groove.mono_below, real kick/808
    # mixing practice) -- a real drum loop's cymbals/hats/mids are well
    # above that, which is the content this test actually needs to prove
    # keeps its width.
    rng = np.random.default_rng(0)
    Lsrc = rng.standard_normal(n) * 0.2
    Rsrc = rng.standard_normal(n) * 0.2   # independent channel, real width
    loop_bufs = {"kick": (Lsrc, Rsrc), "chord0": (Lsrc * 0.5, Rsrc * 0.6)}
    for space in (("dry", ["kick", "chord0"]),
                 ("gated", ["kick", "chord0"])):
        L, R, *_ = render_crew_beat(
            "Test", kit={}, preset=_loop_preset(bpm, nbars, space=space),
            want_parts=True, loop_bufs=loop_bufs, nbars_override=nbars)
        assert _side_vs_mid_db(L, R) > -22.0, (
            f"space={space[0]!r} came out mono")


def test_variety_check_ignores_the_loops_only_placeholder_pattern():
    """Every loops-only beat shares the same placeholder kick lane
    (there's no real one-shot pattern -- the sound is a picked loop), so
    comparing it across beats would always read as "zero moves apart"
    and falsely flag every loops-only batch. variety._kick_bars must
    skip a recipe marked loops_only rather than compare that
    placeholder."""
    placeholder = {"lanes": {"kick": (0.0, 1.0, (0, 0, 0, 0), (("x",),))}}
    rec = {"loops_only": True, "preset": placeholder}
    assert variety._kick_bars(rec) is None
    recs = [dict(rec, names=["Test"]) for _ in range(3)]
    assert variety.score_recipes(recs)["flags"] == []
