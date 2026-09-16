"""Loops-page selection logic — LOOPS-MODE-GAP-ANALYSIS.md Part 3/4.

Deliberately separate from the beat-arrangement path (chord_synth.py,
instrument_sampler.py, harmony.py, and compose()/_build_chords in
crew.py/beat_machine.py): this module must never call
_pin_bars_for_loop_voice or check PREFER_MAX_SHIFT, and must never import
chord_synth/instrument_sampler/harmony. Those rules fit a pick into a
chord SLOT; the Loops page has no slot, so they don't apply here (Part
4a — a scoped exception, not a rule change). tests/test_loop_mode_boundary.py
enforces this at every future edit.

Owner rule (2026-09-16): no DJ signature field on this page ever EXCLUDES
a sound, only weights toward it — default 50% personality, otherwise the
full pool, wide open. That's `pick_loop()` below, mirroring the same
weighted-roll-then-wide-open shape `pattern_gen._pick_library` already
uses for the groove-library seed, adapted for a scored pool instead of a
tags-only one.
"""
from __future__ import annotations


def apply_dj_finish(L, R, preset, seed=0):
    """Color a bare stereo loop buffer with a DJ's mix fingerprint.

    Reuses the exact same functions render_crew_beat (crew.py) applies to
    a whole beat's mix bus — vinyl bed -> wow -> mix_sat -> dust -> mix EQ
    -> glue compression -> master, in that order — just without the lane-
    building or the kick-sidechain duck above it (a bare loop has no kick
    to duck against). LOOPS-MODE-GAP-ANALYSIS.md Part 3/4 step 3/4: "reuse
    the beat renderer's own per-DJ chain function — do not write a second
    one." None of these live in the chord/arrangement slot-fitting path
    (chord_synth.py/instrument_sampler.py/harmony.py), so importing them
    here doesn't cross the boundary tests/test_loop_mode_boundary.py
    guards.
    """
    from groove import OWNER_TASTE, glue_compress, sat_unity, sp1200, \
        vinyl_bed, wow_flutter
    from make_drum_loops import master
    p = preset or {}
    clean_mix = bool(p.get("clean_mix"))
    n = len(L)
    if not clean_mix and p.get("vinyl"):
        L = L + vinyl_bed(n, level_db=p["vinyl"], seed=seed * 2 + 1)
        R = R + vinyl_bed(n, level_db=p["vinyl"], seed=seed * 2 + 2)
    if not clean_mix and p.get("wow", 0) > 0:
        L = wow_flutter(L, wow_pct=p["wow"], seed=seed, loop=True)
        R = wow_flutter(R, wow_pct=p["wow"], seed=seed, loop=True)
    if not clean_mix and p.get("mix_sat", 0) > 0:
        L, R = sat_unity(L, p["mix_sat"]), sat_unity(R, p["mix_sat"])
    if not clean_mix and p.get("dust", 0) > 0:
        L, R = sp1200(L, amount=p["dust"]), sp1200(R, amount=p["dust"])
    eq = p.get("mix_eq", OWNER_TASTE["mix_eq"])
    if eq:
        from audio_engine import eq3
        L, R = eq3(L, R, **eq)
    L, R = glue_compress(L, R, **p.get("glue", {}))
    L, R = master(L, R, drive=0.7 if clean_mix else p.get("drive", 1.4))
    return L, R


def pick_loop(dj_signature, pool, rng):
    """One pick from `pool` (entries from melodic_loops.in_key_scored() or
    sample_library.loops_scored() — each carries a `fit_score`, lower is a
    closer fit). `rng` is a stdlib random.Random, same as compose() uses.

    dj_signature['loop_taste']['p'] is the odds of an on-taste pick
    (default 0.5). On taste: a weighted pick leaning toward the lowest
    fit_score — a lean, not a filter, everything stays in the running.
    Off taste (the rest of the time, or no taste configured): a uniform
    pick from the WHOLE pool, zero narrowing.

    Returns (entry, on_taste) — on_taste is the coin flip that actually
    happened, so a caller can record it on the loop's sidecar (owner
    2026-09-16: "whether it was a taste-pick or a free-pick"). Returns
    (None, False) for an empty pool.
    """
    if not pool:
        return None, False
    p = ((dj_signature or {}).get("loop_taste") or {}).get("p", 0.5)
    if rng.random() < p and len(pool) > 1:
        scores = [e.get("fit_score", 0.0) for e in pool]
        lo = min(scores)
        weights = [1.0 / (1.0 + (s - lo)) for s in scores]
        return rng.choices(pool, weights=weights)[0], True
    return rng.choice(pool), False
