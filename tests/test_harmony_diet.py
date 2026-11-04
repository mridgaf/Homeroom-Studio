"""Harmony diet (owner 2026-11-03): flat names, rap-shaped scale odds,
2-chord shuttles on soul/melodic identities, calmer melodies. Drums are
not touched by any of it."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import beat_machine as bm                     # noqa: E402
import harmony                                # noqa: E402
import melody_rhythm as mr                    # noqa: E402
from key_context import KeyContext, pitch_class, uses_flats  # noqa: E402


def test_flat_keys_spell_flats():
    k = KeyContext("F", "minor")
    names = [k.chord_name(pitch_class(n), "major") for n in ("Ab", "Bb", "Eb")]
    assert names == ["Ab", "Bb", "Eb"]
    assert KeyContext("A#", "minor").chord_name(pitch_class("Bb"),
                                                "minor") == "Bbm"
    assert not uses_flats(pitch_class("F#"), "minor")      # 3 sharps
    assert not uses_flats(pitch_class("E"), "minor")       # 1 sharp
    assert uses_flats(pitch_class("D#"), "minor")          # Eb minor


def _roll(sig, n=400, open_roll=False):
    out = []
    for v in range(n):
        out.append(bm._roll_key(sig, v, {"chords": True, "chord_feel": None},
                                open_roll, random.Random(v * 353 + 17),
                                flow=True, diet=True))
    return out


def test_free_roll_is_rap_shaped_and_flat():
    got = _roll({}, open_roll=True)
    modes = {m for _r, m, _p in got}
    assert not modes & {"lydian", "phrygian_dominant"}
    assert sum(m == "minor" for _r, m, _p in got) > 0.4 * len(got)
    assert not {r for r, _m, _p in got} & {"A#", "D#", "G#"}


def test_in_character_diet_and_keep_modes():
    sig = {"key": {"roots": [["C", 1]],
                   "mode": [["minor", 1], ["lydian", 1]]}}
    plain = sum(m == "lydian" for _r, m, _p in _roll(sig))
    sig["key"]["keep_modes"] = ["lydian"]
    kept = sum(m == "lydian" for _r, m, _p in _roll(sig))
    assert plain < kept * 0.8


def test_second_chord_in_key_and_off_tonic():
    rng = random.Random(1)
    for root, mode in (("C", "minor"), ("F", "minor"), ("G", "major"),
                       ("D", "dorian"), ("E", "phrygian")):
        key = KeyContext(root, mode)
        home = harmony.home_chord(key, [])
        c = harmony.second_chord(key, [], home, rng)
        assert c and c["notes"][0] % 12 != key.pc
        assert all(n % 12 in set(key.scale()) for n in c["notes"])
        assert c["quality"] not in ("dim", "aug", "5")


def test_dark_stays_mostly_one_chord_soul_shuttles():
    def share(fam):
        return sum(harmony.wants_two({"chord_family": fam},
                                     random.Random(i)) for i in range(500))
    assert share("dark") < 90 < 250 < share("soul_jazz")


def test_melody_drops_colour_note_unless_kept():
    key = KeyContext("A", "harmonic_minor")
    s = mr.melody_scale(key.scale(), key.pc, key.mode)
    assert (key.pc + 11) % 12 not in s and len(s) == 6
    assert mr.melody_scale(key.scale(), key.pc, key.mode,
                           ("harmonic_minor",)) == key.scale()


def test_pick_instrument_no_bell_no_world():
    idx = []
    for g, path in (("bell", "x/bell.wav"), ("piano", "x/Dan Tranh/a.wav"),
                    ("wood", "VCSL/Ocarina/a.wav"), ("guitar", "x/guitar.wav")):
        for n in range(30, 100):
            idx.append({"group": g, "path": path + str(n), "note": n})
    for v in range(40):
        ents, _s = mr.pick_instrument(idx, [60, 64], set(), v, diet=True)
        assert ents and ents[0]["group"] == "guitar"
