"""Progression generator (punch list step 2) — theory/progressions.md,
transposed onto a KeyContext. The theory content itself (which offsets
mean which roman numeral) is transcribed in progressions_config.json
and isn't re-litigated here; this guards the transposition and voicing
wiring, and that every entry in the config is well-formed.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import harmony                                                       # noqa: E402
from key_context import CHORDS, KeyContext                           # noqa: E402


def test_every_progression_uses_a_known_chord_quality():
    for name in harmony.names():
        for _offset, quality in harmony.PROGRESSIONS[name]["chords"]:
            assert quality in CHORDS, "%s uses unknown quality %r" % (name, quality)


def test_compose_transposes_onto_the_given_key():
    key = KeyContext("F", "minor")
    picked, chords = harmony.compose(key, "dreamy")
    assert picked == "dreamy"
    assert [(c["root"], c["quality"]) for c in chords] \
        == [("F", "maj7"), ("A#", "maj7")]
    assert chords[0]["notes"] == key.voice(key.pc, "maj7", 3)


def test_compose_falls_back_to_a_random_pick_for_an_unknown_name():
    key = KeyContext("C", "minor")
    picked, chords = harmony.compose(key, "not-a-real-progression",
                                      rng=random.Random(1))
    assert picked in harmony.names()
    assert len(chords) == len(harmony.PROGRESSIONS[picked]["chords"])


def test_two_chord_vamps_stay_two_chords():
    key = KeyContext("A", "minor")
    _picked, chords = harmony.compose(key, "vamp_i_VI")
    assert [c["chord"] for c in chords] == ["Am", "F"]
