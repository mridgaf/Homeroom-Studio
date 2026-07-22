"""MIDI ingestion (punch list step 4) — the pure note-math, no drive
needed. `scan()` walks `sample_packs.json` roots and isn't covered here
(same reason test_samples.py doesn't require the drive to be mounted);
this guards the functions a mislabeled or ambiguous file depends on.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from key_context import KeyContext                                   # noqa: E402
from midi_packs import detect_key, key_in_name, progression          # noqa: E402


def test_key_in_name_reads_common_labels():
    assert key_in_name("Cymatics - Python MIDI 12 - C# Min.mid") \
        == KeyContext("C#", "minor")
    assert key_in_name("Some Loop - F Maj.mid") == KeyContext("F", "major")


def test_key_in_name_none_when_absent():
    assert key_in_name("no key here.mid") is None


def test_detect_key_uses_bass_to_break_the_relative_tie():
    # A-C-E with A held in the bass: A minor and C major share every
    # note, so only the bass anchor (song-keys.md's 808-root rule) can
    # tell them apart.
    notes = [(0.0, 4.0, 45, 100),    # A2, bass
             (0.0, 4.0, 60, 80),     # C4
             (0.0, 4.0, 64, 80)]     # E4
    assert detect_key(notes) == KeyContext("A", "minor")


def test_detect_key_empty_notes_is_none():
    assert detect_key([]) is None


def test_progression_collapses_a_repeated_chord():
    notes = [
        (0.0, 1.0, 60, 90), (0.0, 1.0, 64, 90), (0.0, 1.0, 67, 90),  # C
        (1.0, 2.0, 57, 90), (1.0, 2.0, 60, 90), (1.0, 2.0, 64, 90),  # Am
        (2.0, 3.0, 57, 90), (2.0, 3.0, 60, 90), (2.0, 3.0, 64, 90),  # Am again
    ]
    chords = progression(notes)
    assert [(root, quality) for _, root, quality, _ in chords] \
        == [(0, "major"), (9, "minor")]


def test_progression_ignores_single_note_stacks():
    notes = [(0.0, 1.0, 60, 90)]
    assert progression(notes) == []
