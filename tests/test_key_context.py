"""KeyContext — the beat's root note + mode (punch list step 1).

Guards the two things that would quietly poison every chord built on
top of this: the pitch-class math (a wrong `pc` mistunes the sub AND
every chord root), and the diatonic-triad rule that lets `theory/
progressions.md`'s roman numerals come out right without hardcoding a
quality table per key.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from key_context import KeyContext, name_chord, pitch_class          # noqa: E402


def test_pitch_class_accepts_sharps_and_flats():
    assert pitch_class("C") == 0
    assert pitch_class("A#") == 10
    assert pitch_class("Bb") == 10
    assert pitch_class("bb") == 10


def test_pitch_class_rejects_garbage():
    with pytest.raises(ValueError):
        pitch_class("H")


def test_hz_matches_old_root_hz_table():
    # F1 was the old ROOT_HZ value this module had to reproduce exactly.
    assert KeyContext("F", "minor").hz == pytest.approx(43.65, abs=0.01)


def test_scale_is_seven_notes_tonic_first():
    ctx = KeyContext("A", "minor")
    assert ctx.scale()[0] == ctx.pc
    assert len(ctx.scale()) == 7


def test_degree_outside_key_is_none():
    ctx = KeyContext("A", "minor")          # A minor has no C#
    assert ctx.degree(pitch_class("C#")) is None
    assert ctx.degree(pitch_class("C")) == 3


@pytest.mark.parametrize("degree,root_name,quality,roman", [
    (1, "A", "minor", "i"),
    (3, "C", "major", "III"),
    (4, "D", "minor", "iv"),
    (6, "F", "major", "VI"),
    (7, "G", "major", "VII"),
])
def test_triad_matches_progressions_md_a_minor(degree, root_name, quality, roman):
    # theory/progressions.md's i-VI-III-VII / i-iv-VI-V loops, spelled
    # in A minor, built purely from natural-minor scale degrees.
    ctx = KeyContext("A", "minor")
    root_pc, got_quality = ctx.triad(degree)
    assert ctx.spell(root_pc) == root_name
    assert got_quality == quality
    assert ctx.roman(root_pc, got_quality) == roman


def test_roman_marks_a_root_outside_the_key():
    # Dark/menacing: i-bII (Am-Bb) — Bb isn't in A minor's scale.
    ctx = KeyContext("A", "minor")
    assert ctx.roman(pitch_class("Bb"), "major") == "bII"


def test_voice_stacks_intervals_from_chords_md():
    ctx = KeyContext("C", "minor")
    notes = ctx.voice(pitch_class("C"), "minor", octave=3)
    assert [n - notes[0] for n in notes] == [0, 3, 7]


def test_shift_from_takes_the_short_way_round():
    a_minor = KeyContext("A", "minor")
    bb_minor = KeyContext("Bb", "minor")
    # A -> Bb is +1, not -11.
    assert bb_minor.shift_from(a_minor) == 1


def test_name_chord_prefers_the_bass_as_root():
    # C-E-G over an A bass reads as Am7 (bass-anchored), not C major —
    # song-keys.md's "the bass is what the chord IS" rule.
    root, quality = name_chord([60, 64, 67, 69], bass=69)
    assert (root, quality) == (9, "min7")


def test_name_chord_needs_at_least_two_pitch_classes():
    assert name_chord([60, 60, 72]) is None
