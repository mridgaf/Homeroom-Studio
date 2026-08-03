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


def test_no_progression_is_longer_than_the_shortest_loop():
    """_build_chords lays one chord per bar and BREAKS when it runs past the
    loop (`if start_bar >= nb: break`), so a progression with more chords
    than the loop has bars would arrive silently half-played. Since
    2026-08-01 the shortest loop is 4 bars (ALLOWED_BARS in pattern_gen), so
    4 chords is the ceiling. This is the guard that makes a future 6-chord
    progression fail loudly here instead of quietly truncating in a render."""
    longest = max((len(harmony.PROGRESSIONS[n]["chords"]), n)
                  for n in harmony.names())
    assert longest[0] <= 4, (
        "%s has %d chords; the 4-bar loop can only place 4. Either shorten "
        "it or teach _build_chords half-bar chord slots." % (longest[1],
                                                             longest[0]))


def test_the_pool_covers_every_documented_chord_quality():
    """theory/chords.md documents 14 chord flavours and key_context.CHORDS
    implements all 14 — but before 2026-08-01 the progressions only ever
    used 9. aug, add9, sus4, 7#9 and the bare power chord were dead code:
    written down, built, never reachable in a beat. Owner asked to expand
    the chord vocabulary, so this pins that none of them fall out again."""
    used = {q for n in harmony.names()
            for _o, q in harmony.PROGRESSIONS[n]["chords"]}
    missing = set(CHORDS) - used
    assert not missing, "no progression can reach these qualities: %s" % (
        sorted(missing),)


def test_every_progression_renders_in_every_mode():
    """The 2026-08-01 rule opens every mode to every identity, so a
    progression written with a minor-key beat in mind can now be asked for
    in lydian or harmonic minor. All of them must still voice to real MIDI
    notes rather than raising."""
    from key_context import MODES
    for name in harmony.names():
        for mode in sorted(MODES):
            _picked, chords = harmony.compose(KeyContext("C", mode), name,
                                              rng=random.Random(1))
            assert chords, (name, mode)
            for c in chords:
                assert c["notes"], (name, mode, c)
                assert all(0 <= n < 128 for n in c["notes"]), (name, mode, c)
