"""2026-10-18 reachability fixes in tools/melodic_loops.py (BOTC Sorted Loops).

Each case is a real file/folder name from his library that was being skipped.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import melodic_loops as m  # noqa: E402


def test_full_drum_loops_are_drum_loops():
    # "Full" next to a drum word means the whole drum loop, not a full mix
    assert m.is_drum_loop(("Drums",), "FL_BC_175_Drum_Full_Jungle")
    assert m.is_drum_loop(("Drums", "ROCK", "162BPM"), "Full_Beat_Hats_162")
    # a folder called "Full Drum Loops" is still a drum folder
    assert m.is_drum_loop(("Drums", "Full Drum Loops"), "PLAYOFFS - DL Sailor 111")


def test_full_still_blocks_real_full_mixes_and_melodic_drum_files():
    assert not m.is_drum_loop(("Drums",), "FL_MP_80_Synth_Lead_Cowbell_Breaks_D#m")
    assert not m.is_drum_loop(("Drums",), "Drum Full Mix")
    assert not m.is_drum_loop(("Drums",), "080_sky_D_lofi strings")


def test_conga_loops_in_a_percussion_folder_count_as_drum_loops():
    assert m.is_drum_loop(("Percussion - Conga",), "DRDY1019")


def test_note_label_with_octave_or_chord_number_is_a_key():
    f = m.label_key_from_tokens
    assert f(["Bass", "Disease", "150", "Eb6", "1"]) == ("Eb", None)
    assert f(["Synths", "Mogue", "Toeggle", "120", "C1"]) == ("C", None)
    assert f(["Manta", "Em7", "164", "long"]) == ("E", "minor")


def test_note_label_is_ignored_when_ambiguous_or_not_a_note():
    f = m.label_key_from_tokens
    assert f(["Deepmind", "Arp", "Am5", "F7", "Am5", "Dm9"]) is None   # two roots
    assert f(["Dork", "120", "C5", "to", "F5"]) is None                # two roots
    assert f(["Kick", "808", "Loop"]) is None
    assert f(["Gm"]) is None   # bare keys are the strict reader's job
