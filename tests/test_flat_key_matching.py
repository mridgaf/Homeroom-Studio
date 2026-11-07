"""Flat key names (Bb, Eb, Ab) must match sharp-spelled index entries."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from key_context import KeyContext, same_root  # noqa: E402
import loop_lanes  # noqa: E402


def test_same_root_ignores_spelling():
    for flat, sharp in (("Bb", "A#"), ("Eb", "D#"), ("Ab", "G#"), ("Db", "C#"), ("Gb", "F#")):
        k = KeyContext(flat, "minor")
        assert same_root(sharp, k) and same_root(flat, k)
    assert not same_root("A", KeyContext("Bb", "minor"))


def test_loop_lane_key_ok_flat_anchor():
    assert loop_lanes._key_ok({"key": "A#", "mode": "minor"}, ("Bb", "minor"))
    assert not loop_lanes._key_ok({"key": "A", "mode": "minor"}, ("Bb", "minor"))
