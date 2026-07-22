"""Chord progression generator (punch list step 2, 2026-07-22).

pattern_gen.compose() writes the drums. This is the harmony half: turn
theory/progressions.md — already transcribed as data in
progressions_config.json — into an actual chord sequence in whatever
KeyContext the beat is in.

Nothing here decides taste beyond what the owner's own doc already
decided; this module only transposes and voices it, the same way
midi_packs.py transposes a MIDI phrase with KeyContext.shift_from.
Picking WHICH progression fits a feeling, and stacking these chords
under real audio/MIDI export, are later punch-list steps (5-7).

    ./.venv/bin/python tools/harmony.py                 # random pick, F minor
    ./.venv/bin/python tools/harmony.py Bb minor dreamy  # a named one
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from key_context import KeyContext                        # noqa: E402

CONFIG = Path(__file__).resolve().parent.parent / "progressions_config.json"
PROGRESSIONS = {k: v for k, v in json.loads(CONFIG.read_text()).items()
                 if not k.startswith("_")}


def names():
    """Every progression name, for a picker UI."""
    return sorted(PROGRESSIONS)


def compose(key, name=None, octave=3, rng=None):
    """A chord progression in `key`, from `name` (or a random pick if
    `name` isn't one of `names()`).

    Returns (name, chords) where chords is a list of dicts, one per
    chord, in order: {"root": "F", "quality": "minor", "chord": "Fm",
    "roman": "i", "notes": [53, 56, 60]} — `notes` are real MIDI note
    numbers (key_context.voice), ready for a synth or a MIDI file.
    """
    rng = rng or random
    if name not in PROGRESSIONS:
        name = rng.choice(names())
    chords = []
    for offset, quality in PROGRESSIONS[name]["chords"]:
        root_pc = (key.pc + offset) % 12
        chords.append({
            "root": key.spell(root_pc),
            "quality": quality,
            "chord": key.chord_name(root_pc, quality),
            "roman": key.roman(root_pc, quality),
            "notes": key.voice(root_pc, quality, octave),
        })
    return name, chords


def _report(root="F", mode="minor", name=None):
    key = KeyContext(root, mode)
    picked, chords = compose(key, name)
    print("key         : %s   (808 root %.2f Hz)" % (key, key.hz))
    print("progression : %s — %s\n" % (picked, PROGRESSIONS[picked]["label"]))
    for c in chords:
        print("  %-6s %-6s  %s" % (c["chord"], c["roman"], c["notes"]))


if __name__ == "__main__":
    _report(*sys.argv[1:4])
