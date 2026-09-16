"""Part 4 step 0 of LOOPS-MODE-GAP-ANALYSIS.md: the boundary test.

Loop mode must be provably decoupled from beat-arrangement rules. Those
rules (one-instrument-per-chord PREFER_MAX_SHIFT, the 4-bar-if-loop pin
_pin_bars_for_loop_voice) govern fitting a pick into a chord SLOT; the
Loops page has no slot, so tools/loop_mode.py must never reference them
and must never import the chord/arrangement slot-fitting modules
(chord_synth.py, instrument_sampler.py, harmony.py). See Part 4a: this is
a scoped exception for the Loops page, not a repeal of those rules for
compose()/full-beat generation.
"""
from __future__ import annotations

import ast
import pathlib

import pytest

LOOP_MODULE = pathlib.Path(__file__).resolve().parent.parent / "tools" / "loop_mode.py"

FORBIDDEN_NAMES = {"_pin_bars_for_loop_voice", "PREFER_MAX_SHIFT"}
# the chord/arrangement slot-fitting path — fine to import audio_engine,
# sample_library, melodic_loops, key_context, or a beat_machine mix-chain
# helper; not fine to import the modules that fit a pick into a chord slot.
FORBIDDEN_IMPORT_MODULES = {"chord_synth", "instrument_sampler", "harmony"}


def _collect_names(tree):
    return ({n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
            | {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)})


def _collect_import_modules(tree):
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    return mods


def test_loop_mode_module_exists():
    assert LOOP_MODULE.exists(), (
        "tools/loop_mode.py not built yet -- Part 4 steps 1-5 of "
        "LOOPS-MODE-GAP-ANALYSIS.md create it."
    )


def test_loop_mode_never_touches_arrangement_rules():
    if not LOOP_MODULE.exists():
        pytest.skip("tools/loop_mode.py not built yet")
    tree = ast.parse(LOOP_MODULE.read_text())

    hit_names = _collect_names(tree) & FORBIDDEN_NAMES
    assert not hit_names, (
        f"tools/loop_mode.py references arrangement-only rule(s): {hit_names} "
        "-- loop mode has no chord slot, so it must not depend on slot-"
        "fitting rules (Part 4a)."
    )

    hit_mods = _collect_import_modules(tree) & FORBIDDEN_IMPORT_MODULES
    assert not hit_mods, (
        f"tools/loop_mode.py imports from the chord/arrangement slot-fitting "
        f"path: {hit_mods} -- that couples loop mode to compose()'s rules."
    )
