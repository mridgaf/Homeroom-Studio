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


# ---- chord flow (owner 2026-09-26: "not very much variety") ----

def test_arrange_always_fills_the_loop_exactly_and_never_needs_a_fifth_row():
    """Every progression, both loop lengths, many seeds: the chord lengths
    add up to the loop, and there are never more than four chord slots
    (each slot is its own rack row; a 4-chord loop already had four)."""
    for name in harmony.names():
        for bars in (4, 8):
            for seed in range(40):
                key = KeyContext("F", "minor")
                _n, chords = harmony.compose(key, name)
                out = harmony.arrange(key, chords, bars, random.Random(seed))
                assert sum(c["bars"] for c in out) == bars, (name, bars, out)
                assert 1 <= len(out) <= 4, (name, bars, len(out))
                assert all(c["bars"] >= 1 for c in out)


def test_arrange_varies_where_the_chords_change():
    """The old layout was ONE even split for every beat. Now a 2-chord
    loop over 8 bars lands on several different layouts."""
    key = KeyContext("A", "minor")
    _n, chords = harmony.compose(key, "vamp_i_VI")
    layouts = {tuple((c["chord"], c["bars"]) for c in
                     harmony.arrange(key, chords, 8, random.Random(s)))
               for s in range(200)}
    assert len(layouts) >= 5, layouts


def test_a_turnaround_is_a_new_chord_in_the_last_bar():
    key = KeyContext("A", "minor")
    _n, chords = harmony.compose(key, "vamp_static_riff")
    seen = 0
    for s in range(200):
        out = harmony.arrange(key, chords, 4, random.Random(s))
        if any(c.get("turnaround") for c in out):
            seen += 1
            assert out[-1].get("turnaround")
            assert out[-1]["chord"] != "Am"
    # TURNAROUND_P is 0.4; 200 rolls land well inside 50..110
    assert 50 <= seen <= 110, seen


def test_voice_lead_keeps_the_chord_and_moves_less_than_root_position():
    """Same notes (pitch classes), a comping range, and the hand travels
    less between chords than the old root-up stacks did."""
    key = KeyContext("C", "minor")
    smooth_total = root_total = 0
    for name in harmony.names():
        for s in range(10):
            _n, chords = harmony.compose(key, name)
            rng = random.Random(s)
            out = harmony.arrange(key, chords, 8, rng)
            style = harmony.voice_lead(out, rng)
            for c in out:
                assert c["notes"][0] % 12 == key.voice(
                    (c["notes"][0]) % 12, c["quality"], 3)[0] % 12
                assert {n % 12 for n in c["voiced"]} == \
                    {n % 12 for n in c["notes"]}
                if style != "root":
                    assert min(c["voiced"]) >= harmony.VOICE_LO
                    assert max(c["voiced"]) <= harmony.VOICE_HI + 12
            if style == "smooth":
                for a, b in zip(out, out[1:]):
                    smooth_total += harmony._move(a["voiced"], b["voiced"])
                    root_total += harmony._move(a["notes"], b["notes"])
    assert smooth_total < root_total * 0.8, (smooth_total, root_total)


def test_voice_lead_leaves_root_position_notes_for_the_bass():
    """The bass line, the 808 and the multi-part split read the root from
    notes[0]. Voicing must never touch `notes`."""
    key = KeyContext("D", "minor")
    _n, chords = harmony.compose(key, "sad_accepting")
    before = [list(c["notes"]) for c in chords]
    out = harmony.arrange(key, chords, 8, random.Random(3))
    harmony.voice_lead(out, random.Random(3))
    assert [c["notes"] for c in chords] == before
    for c in out:
        assert c["notes"] == key.voice(c["notes"][0] % 12, c["quality"], 3)


def test_pick_weights_halves_the_one_and_two_chord_loops():
    got = dict((n, w) for n, w in harmony.pick_weights(
        [["vamp_i_VI", 2], ["sad_accepting", 2], "vamp_static_riff"]))
    assert got == {"vamp_i_VI": 1.0, "sad_accepting": 2,
                   "vamp_static_riff": 0.5}


def test_lead_parts_glides_each_part_and_keeps_the_top_part_on_top():
    """Multi-part beats (about 45%) never used the smooth voicing, so a
    chord-flow A/B pair came out byte-identical (Sunday Chop, 2026-09-26).
    Each part now moves by octaves toward where it just was; the split's
    notes are unchanged and the top part stays above the low part."""
    import beat_machine
    key = KeyContext("C", "minor")
    moved_new = moved_old = 0
    for name in harmony.names():
        _n, chords = harmony.compose(key, name)
        old = [beat_machine._split_chord_roles(c["notes"]) for c in chords]
        new = harmony.lead_parts(old)
        for o, n in zip(old, new):
            for po, pn in zip(o, n):
                assert sorted(x % 12 for x in po) == sorted(x % 12 for x in pn)
            if n[0] and n[1]:
                assert min(n[1]) > max(n[0]), (name, n)
        for k in (0, 1):
            for a, b in zip(old, old[1:]):
                if a[k] and b[k]:
                    moved_old += harmony._move(a[k], b[k])
            for a, b in zip(new, new[1:]):
                if a[k] and b[k]:
                    moved_new += harmony._move(a[k], b[k])
    assert moved_new < moved_old, (moved_new, moved_old)
