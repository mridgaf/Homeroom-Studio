"""The famous figures: Amen, Funky Drummer, Levee, Big Beat and the rest.

Every test here exists because the 2026-08-04 review found the rule had a
choke point and no test — the exact failure the hard-rule-invariant skill
was written to stop. Each one fails loudly if a figure stops being played
the way it was drummed.
"""
import copy
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import beat_machine
import pattern_gen
from crew import CREW


@pytest.fixture(autouse=True)
def _pat_hist(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "pat.json")


def _break_preset(notes, name="Otto Grit", variant=0):
    dirs = beat_machine.parse_directions(notes)
    p = copy.deepcopy(CREW[name])
    p["break_beat"] = dirs["break_beat"]
    p["break_name"] = dirs["break_name"]
    pattern_gen.compose(p, name, variant)
    return p


def _figure(name_fragment):
    return next(p for p in pattern_gen.break_list()
                if name_fragment in p["name"])


# ------------------------------------------- naming one gets you that one

def test_naming_a_break_selects_that_break():
    """THE 2026-08-04 BUG: every song name set break_beat=True and was then
    thrown away, so typing "amen" landed on the Amen 1 roll in 10."""
    import random
    for word, fragment in beat_machine.BREAK_WORDS:
        dirs = beat_machine.parse_directions(word)
        assert dirs["break_beat"], word
        for seed in range(25):
            got = pattern_gen._pick_break(random.Random(seed),
                                          dirs["break_name"])
            assert fragment in got["name"], (word, got["name"])


def test_every_picker_option_selects_its_figure():
    """The dropdown and the notes box must be the same code path: every
    option's value has to be a trigger the parser recognises."""
    for p in pattern_gen.break_list():
        word = beat_machine._break_word(p["name"])
        assert word, "%s is in the pack but nothing selects it" % p["name"]
        assert beat_machine.parse_directions(word)["break_name"] in p["name"]


def test_a_bare_break_request_still_rolls_the_dice():
    import random
    seen = {pattern_gen._pick_break(random.Random(s), None)["name"]
            for s in range(60)}
    assert len(seen) > 1


def test_punctuation_does_not_swallow_the_word():
    """Only "," and "." were stripped, so "funky drummer!" did nothing."""
    for typed in ("funky drummer!", "amen?", "(apache)", "levee -- heavy"):
        assert beat_machine.parse_directions(typed)["break_beat"], typed


def test_an_ordinary_sentence_is_not_a_break_request():
    for typed in ("i think it should be dark", "make it dusty", ""):
        assert not beat_machine.parse_directions(typed)["break_beat"], typed


# --------------------------------------------- played exactly as written

@pytest.mark.parametrize("word,fragment", list(beat_machine.BREAK_WORDS))
def test_the_figure_reaches_the_beat_exactly_as_transcribed(word, fragment):
    """Every figure, not just the easy ones. Checking only the Amen hid a
    real bug (2026-08-04): Apache and The Big Beat are drummed on a plain
    2 and 4, and the "a bare 2&4 seed teaches nothing" guard threw their
    backbeat away and substituted the DJ's own — while the beat's own notes
    still said "played straight"."""
    p = _break_preset(word)
    written = _figure(fragment)
    for lane in ("kick", "snare", "hat"):
        if lane not in p["lanes"] or lane not in written:
            continue
        bars = p["lanes"][lane][3]
        want = pattern_gen.seed_bars(written[lane])
        assert want, (word, lane)
        # the figure cycles across however many bars the beat has — a
        # one-bar figure repeats, a four-bar one runs its whole cycle
        for i, bar in enumerate(bars):
            assert bar == want[i % len(want)], (word, lane, i)


def test_the_variety_pass_leaves_the_figure_alone():
    """compose() spares a break its thinning; vary_preset used to undo that
    afterwards — density mutation, and treatments that blank whole bars."""
    for variant in range(12):
        p = _break_preset("funky drummer", variant=variant)
        before = {ln: list(p["lanes"][ln][3])
                  for ln in beat_machine.BREAK_LANES if ln in p["lanes"]}
        beat_machine.vary_preset(p, variant, 1, tempo_locked=False)
        for lane, bars in before.items():
            assert list(p["lanes"][lane][3]) == bars, (variant, lane)


def test_a_break_beat_never_blanks_a_guest_lane():
    """REGRESSION 2026-08-04: protecting kick/snare/hat from the variety
    pass left the guests as the only lane a structural treatment could
    pick, so every break beat aimed its hole at a guest — and the guests
    are the only off-centre content a break beat has. Beat 1803 came out
    mono (-28 dB side-to-mid) because its shaker sat out half the beat."""
    holes = ("drops out", "thins out", "sit out", "only in the")
    for variant in range(30):
        p = _break_preset("amen", variant=variant)
        notes = beat_machine.vary_preset(p, variant, 1, tempo_locked=False)
        got = [n for n in notes if any(h in n for h in holes)]
        assert not got, (variant, got)


def test_a_figure_keeps_every_bar_it_was_written_with():
    """seed_bars must not truncate. His chart writes the Amen and Apache as
    FOUR bars (2026-08-04) — the four-bar cycle is most of what makes the
    Amen the Amen, and load_library used to accept only 16 and 32 steps, so
    a four-bar figure was dropped on the floor."""
    lens = set()
    for p in pattern_gen.break_list():
        assert p["steps"] % 16 == 0, p["name"]
        assert len(pattern_gen.seed_bars(p["kick"])) == p["steps"] // 16, \
            p["name"]
        lens.add(p["steps"])
    assert 64 in lens, "the four-bar figures are being dropped again"


def test_written_accents_are_not_moved_to_the_downbeats():
    """A figure's accents must survive parsing. The old kick parser only
    honoured velocity when some hit fell under 90, so figures written
    without ghost kicks had every accent replaced with accents on
    0/8/16/24. Assembly Line's accents on 11 and 27 ARE that break."""
    kick = _figure("Assembly Line")["kick"]
    assert kick[11] == "X" and kick[27] == "X"
    # off his chart: the backbeat is the accent, extra snares are ghosts
    snare = _figure("Funky Drummer")["snare"]
    assert snare[4] == "X" and snare[12] == "X"
    assert snare.count(".") >= 1, "the syncopated snares should be ghosts"


def test_the_hats_are_transcribed_not_a_metronome():
    """Nine of ten hat lanes once shipped byte-identical straight 8ths at a
    flat 100. His chart (2026-08-04) gives the real thing: hats that STOP in
    places, and open hats where the drummer opened them."""
    hats = {p["name"]: p.get("hat", "") for p in pattern_gen.break_list()}
    assert len(set(hats.values())) > 1, "every figure has the same hat"
    assert any("o" in h for h in hats.values()), "no open hats anywhere"
    fd = hats["Funky Drummer Figure"]
    assert "o" in fd, "the Funky Drummer's open hats are gone"
    # the hat rests where the open hat sounds — this is the "the hi hats
    # just run straight over the beats" complaint, 2026-08-04
    assert any(h.count("-") for h in hats.values() if h), \
        "no hat lane ever rests"


# --------------------------------------------------- ask-only, never rolled

def test_a_famous_figure_never_arrives_by_accident():
    """Owner call 2026-08-04: these are asked for, never rolled — and never
    as a thinned influence, which is the treatment that makes a break stop
    sounding like the record."""
    import random
    rng = random.Random(0)
    spec = {"p": 1.0, "tags": [["breaks", 10], ["hiphop", 10]]}
    for _ in range(200):
        got = pattern_gen._pick_library(spec, rng)
        assert got is None or got["subgenre"] != "breaks"


# ------------------------------------- the flat library keeps its old shape

def test_flat_grids_keep_the_reading_they_always_had():
    """The velocity parse is library-wide (owner call 2026-08-04), but a
    grid with no written dynamics has nothing to read: the kick keeps its
    positional accents and the backbeat keeps playing its hits."""
    flat = [100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0]
    assert pattern_gen._lib_kick(flat) == "X-x-X-x-X-x-X-x-"
    assert pattern_gen._lib_snare(flat) == "X-X-X-X-X-X-X-X-"
    ghosts = [118, 0, 55, 0, 118, 0, 0, 0, 118, 0, 55, 0, 118, 0, 0, 0]
    assert pattern_gen._lib_kick(ghosts) == "X-.-X---X-.-X---"
    spread = [118, 0, 0, 0, 100, 0, 0, 0, 118, 0, 0, 0, 100, 0, 0, 0]
    assert pattern_gen._lib_kick(spread) == "X---x---X---x---"


# ------------------- hard rules that had a choke point and no test until now

def test_the_stamp_lane_stays_off(monkeypatch):
    """Owner rule 2026-08-01: "Remove the stamp lane." STAMP_LANE could be
    flipped back to True, or a new entry point could skip _drop_stamp, and
    nothing failed."""
    assert beat_machine.STAMP_LANE is False
    p = {"kit": {"kick": 1, "stamp": 2, "stamp2": 3},
         "lanes": {"kick": 1, "stamp": 2, "stamp3": 4}}
    beat_machine._drop_stamp(p)
    assert not [k for k in p["kit"] if k.startswith("stamp")]
    assert not [k for k in p["lanes"] if k.startswith("stamp")]


def test_the_vocal_lane_stays_off():
    """Owner rule 2026-08-01: "Kill the vocal hits completely." """
    assert beat_machine.VOX_LANE_P == 0.0
