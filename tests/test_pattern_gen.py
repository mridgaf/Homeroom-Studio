"""The 2026-07-17 verdict: every generation composes a FRESH pattern in
the DJ's style — different rhythm, different kick flavor, guest colors."""
import copy
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import pattern_gen
from crew import CREW


@pytest.fixture(autouse=True)
def pat_hist(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "pat.json")


def _composed(name, variant, boom_bap=False):
    p = copy.deepcopy(CREW[name])
    notes = pattern_gen.compose(p, name, variant, boom_bap=boom_bap)
    return p, notes


def _kick_a(p):
    return p["lanes"]["kick"][3][0]


def test_euclid_spreads_k_hits():
    for k in (3, 5, 7):
        assert pattern_gen.euclid(k, 16).count("x") == k


# ---------------------------------------------- the frame (2026-07-22)
# The audit of 702 rendered beats found the backbeat welded to steps 4
# and 12 — 41% of the whole library shared ONE snare line, because three
# of the four modes then available all anchored there. These guard the
# widened vocabulary that fixed it.

PLAIN_24 = "----X-------X---"


def _backbeat(spec, seed):
    import random
    return pattern_gen.gen_backbeat(spec, random.Random(seed))


def test_every_backbeat_mode_places_hits():
    """No mode may silently produce an empty bar — a frame that renders
    nothing would read as 'the snare dropped out', not as a new feel."""
    for mode in pattern_gen.BACKBEAT_MODES:
        spec = dict(modes=[[mode, 1.0]], ghosts=[0, 0], gcells=[])
        bar, got = _backbeat(spec, 1)
        assert got == mode
        assert len(bar) == 16
        assert bar.count("-") < 16, mode


def test_the_new_modes_actually_move_the_frame():
    """The point of the fix: these must NOT land on the plain 2&4."""
    for mode in ("four", "push", "tresillo", "offbeat"):
        spec = dict(modes=[[mode, 1.0]], ghosts=[0, 0], gcells=[])
        bar, _ = _backbeat(spec, 3)
        assert bar != PLAIN_24, mode
        # ...and none of them may sit on BOTH 4 and 12, which is what
        # made displaced/sparse fail to add variety before
        assert not (bar[4] != "-" and bar[12] != "-"), mode


def test_home_lean_leaves_room_for_the_rest():
    """A DJ's home mode should be the likeliest roll, never the default.
    Before the fix the home weight was 0.45 of a four-mode board (~72%
    of beats landing on step 4 or 12)."""
    modes = pattern_gen._bb("backbeat")
    weights = dict(modes)
    assert len(modes) == len(pattern_gen.BACKBEAT_MODES)
    assert abs(sum(weights.values()) - 1.0) < 1e-6
    assert abs(weights["backbeat"] - pattern_gen.HOME_LEAN) < 0.01
    assert weights["backbeat"] < 0.35            # leaned, not dominant
    assert weights["backbeat"] == max(weights.values())


def test_plain_two_and_four_is_no_longer_the_default():
    """The headline guard: rolling one DJ's board many times must not
    keep landing on the same line."""
    import random
    spec = dict(modes=pattern_gen._bb("backbeat"), ghosts=[0, 0], gcells=[])
    bars = [_backbeat(spec, s)[0] for s in range(600)]
    plain = bars.count(PLAIN_24) / len(bars)
    assert plain < 0.35, "plain 2&4 still dominates (%.0f%%)" % (100 * plain)
    assert len(set(bars)) >= len(pattern_gen.BACKBEAT_MODES)


def test_traditional_stays_conventional_but_not_identical():
    """'Traditional' means familiar, not literally the same bar. It may
    only reach conventional hip-hop backbones — never the exotic cells."""
    exotic = {"tresillo", "offbeat", "push", "four"}
    seen = set()
    for name in ("Otto Grit", "Cutz"):
        for v in range(2, 40):
            p = copy.deepcopy(CREW[name])
            pattern_gen.compose(p, name, v, traditional=True)
            for lane in ("snare", "clap"):
                if lane in p["lanes"]:
                    seen.add(p["lanes"][lane][3][0])
                    break
    assert len(seen) > 1, "traditional collapsed to one line again"
    # every traditional frame keeps a hit on 2, on 4, or the halftime 3
    for bar in seen:
        anchored = bar[4] != "-" or bar[12] != "-" or bar[8] != "-"
        assert anchored, "traditional wandered off the backbone: %s" % bar


def test_compose_is_deterministic(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "a.json")
    p1, _ = _composed("Otto Grit", 42)
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "b.json")
    p2, _ = _composed("Otto Grit", 42)
    assert p1["lanes"] == p2["lanes"]
    assert p1["kit"] == p2["kit"]


def test_every_variant_is_a_new_rhythm():
    # fresh pattern per generation (owner call 2026-07-21: different is
    # the promise — the old >=3-moves distance floor is gone)
    kicks = [_kick_a(_composed("Otto Grit", v)[0]) for v in range(12)]
    assert len(set(kicks)) == 12


def test_form_rolls_both_shapes():
    """Owner call 2026-07-21: some beats state the loop straight
    through, some answer it A/B. 2026-07-22: the loop is also no longer
    a fixed 8 bars, so the note now reads "<n>-bar loop" / "<n>-bar
    A/B". Both shapes must still occur and keep their promise (the loop
    repeats exactly, B answers A)."""
    import crew
    seen = set()
    for v in range(40):
        p, notes = _composed("Otto Grit", v)
        bars = p["lanes"]["kick"][3]
        n = crew.bars_of(p)
        assert len(bars) == n, (v, len(bars), n)
        if any(x.endswith("-bar A/B") for x in notes):
            assert n == 8, v            # only 8 bars can hold an answer
            assert bars[0] != bars[4], v
            seen.add("ab")
        else:
            assert any(x.endswith("-bar loop") for x in notes), notes
            if n == 8:                  # heard twice, exactly
                assert bars[:4] == bars[4:], v
            seen.add("loop")
    assert seen == {"ab", "loop"}


def test_loop_length_varies_and_centres_on_four():
    """Owner call 2026-07-22: "make the loops half as long", and let the
    length vary per beat. 4 bars is the new normal (half the old fixed
    8); 2 and 8 both still occur."""
    import collections
    import crew
    lens = collections.Counter()
    for name in ("Otto Grit", "Cutz", "Glass Cat"):
        for v in range(60):
            p, _ = _composed(name, v)
            n = crew.bars_of(p)
            lens[n] += 1
            # whatever the length, every lane must actually supply it
            for ln, spec in p["lanes"].items():
                if not ln.startswith("stamp"):
                    assert len(spec[3]) == n, (name, v, ln)
    assert set(lens) == {2, 4, 8}, lens
    total = sum(lens.values())
    assert lens[4] / total > 0.45, lens          # 4 is the norm
    assert sum(n * c for n, c in lens.items()) / total < 6.0, lens


def test_style_is_a_lean_not_a_cage():
    """v6 law (owner 2026-07-18): every mode is reachable for every DJ,
    but the weights still LEAN home — over many variants the home mode
    is the plurality, and the character quirk copy-lanes still mirror."""
    from collections import Counter

    def bb_mode(bar):
        if bar[8] == "X" and bar[4] != "X":
            return "halftime"
        if bar[4] == "X" and any(bar[i] == "X" for i in (11, 12, 13)):
            return "backbeat-ish"
        return "other"

    homes = {"Night Metro": ("clap", "halftime"),
             "Cutz": ("snare", "backbeat-ish"),
             "Rage Engine": ("snare", "halftime")}
    # 120 variants, not a couple dozen: "backbeat-ish" catches both the
    # backbeat and displaced modes, so it sums to a weight close to the
    # home mode's and a small sample swings on noise alone.
    for name, (lane, home) in homes.items():
        seen = Counter()
        for v in range(120):
            p, notes = _composed(name, v)
            # a backbeat borrowed from a groove seed (2026-07-21) is the
            # library's voice, not this DJ's grammar — count grammar
            # rolls only, the lean law is about the weights
            if any(n.startswith(lane + ": seed:") for n in notes):
                continue
            seen[bb_mode(p["lanes"][lane][3][0])] += 1
        assert seen[home] >= max(seen.values()) * 0.6, (name, seen)
        assert len(seen) >= 2, (name, "modes never vary", seen)
    # the Neptunes flam: Glass Cat's clap still mirrors his snare
    for v in range(8):
        gc, _ = _composed("Glass Cat", v)
        assert gc["lanes"]["clap"][3] \
            == [b.replace(".", "-") for b in gc["lanes"]["snare"][3]]
    # New Math's quintuplets and Rage's 32nd walls still occur — the
    # window is wide because library hat seeds (more frequent since
    # 2026-07-21) take the timekeeper roll's place when they land
    assert any(len(b) == 20
               for v in range(60)
               for b in _composed("New Math", v)[0]["lanes"]["hat"][3])
    assert any(len(b) == 32
               for v in range(60)
               for b in _composed("Rage Engine", v)[0]["lanes"]["hat"][3])


def test_clean_punch_drops_808_prefers_punch_tags_never_empties():
    # owner rule 2026-07-23: kicks are clean/punch only, engine-wide —
    # supersedes the 2026-07-17 "not solely 808s" balance below, which
    # kept some 808 in the mix; this drops it outright.
    flavors = [[0.4, "808", ["dust", "boom"], [0.35, 0.9]],
              [0.3, None, ["punch", "knock"], [0.2, 0.5]],
              [0.3, None, ["warm", "round"], [0.4, 0.8]]]  # no clean/punch tag
    out = pattern_gen._clean_punch(flavors)
    assert all(f[1] != "808" for f in out)           # 808 always gone
    assert out == [[0.3, None, ["punch", "knock"], [0.2, 0.5]]]  # punch-tagged wins
    # a style with no punch-tagged survivor still renders (falls back to
    # "just not 808") instead of leaving compose() an empty pool
    only_dark = [[0.5, "808", ["deep"], [0.5, 1.0]],
                [0.5, None, ["warm", "round"], [0.4, 0.8]]]
    assert pattern_gen._clean_punch(only_dark) == [only_dark[1]]
    # an all-808 style (none exist today, but the filter must not crash
    # one into an empty pool if a future config ever is) falls all the
    # way back to the original list
    assert pattern_gen._clean_punch([flavors[0]]) == [flavors[0]]


def test_composed_kicks_are_never_808():
    # real DJs: every composed kick, across many variants and both the
    # main and odd-meter (_compose_odd) paths, is clean/punch — never 808
    for name in ("Otto Grit", "Night Metro", "Chrome Dial", "Rage Engine"):
        for v in range(12):
            p, _ = _composed(name, v)
            assert p["kit"]["kick"][1] != "808", (name, v)
        p_odd = copy.deepcopy(CREW[name])
        pattern_gen.compose(p_odd, name, 1, tsig=(3, 4))
        assert p_odd["kit"]["kick"][1] != "808", name


def test_no_flavor_runs_three_beats_in_a_row():
    # owner report 2026-07-17: the long 808 was landing generation after
    # generation — the streak-breaker forbids any flavor three in a row.
    # Every real DJ's kick_flavors collapses to a single clean/punch
    # entry once 808 is dropped (2026-07-23), so the streak-breaker has
    # nothing left to break FOR REAL CONFIG — cover the mechanism itself
    # with a synthetic style that still has two clean flavors to pick
    # between, same as any DJ would if a second one were added later.
    synthetic = [[0.5, None, ["punch", "knock"], [0.2, 0.5]],
                [0.5, None, ["clean", "tight"], [0.15, 0.4]]]
    name = "Otto Grit"
    fis = []
    for v in range(30):
        p = copy.deepcopy(CREW[name])
        p["kick_flavors"] = synthetic
        pattern_gen.compose(p, name, v)
        fis.append(next(
            i for i, f in enumerate(synthetic)
            if f[1] == p["kit"]["kick"][1]
            and tuple(f[3]) == tuple(p["kit"]["kick"][3])))
    assert all(not (a == b == c)
               for a, b, c in zip(fis, fis[1:], fis[2:]))
    # today's real DJs: the single surviving flavor is what's chosen,
    # every time — the collapse is deterministic, not silently missing
    for name in ("Night Metro", "Rage Engine", "Otto Grit"):
        musts = {_composed(name, v)[0]["kit"]["kick"][1] for v in range(12)}
        assert musts == {None}, name


def test_guest_lanes_appear_from_the_dj_palette():
    pool = {e[2] for e in pattern_gen.DEFAULT_STYLE["Crate Prophet"]
            ["extras"]["pool"]}
    seen = set()
    for v in range(20):
        p, _ = _composed("Crate Prophet", v)
        guests = set(p["lanes"]) - set(CREW["Crate Prophet"]["lanes"])
        assert guests <= pool
        for g in guests:
            assert g in p["kit"]              # pickable, so swappable too
        seen |= guests
    assert seen                               # they do show up


def test_kick_bank_is_valid_and_gets_used():
    for name, bank in pattern_gen.KICK_BANK.items():
        assert len(bank) >= 8, name              # a real library
        assert len(set(bank)) == len(bank), name  # no duplicates
        for bar in bank:
            assert len(bar) == 16 and bar[0] == "X" and set(bar) <= set("Xx-")
    # bank skeletons actually reach the beats: some composed kicks share
    # a bank pattern's anchor shape (>=75% of rolls start from the bank)
    def caps(bar):
        return tuple(i for i, c in enumerate(bar) if c == "X")
    bank_caps = {caps(b) for b in pattern_gen.KICK_BANK["Chrome Dial"]}
    hits = sum(caps(_composed("Chrome Dial", v)[0]["lanes"]["kick"][3][0])
               in bank_caps for v in range(16))
    assert hits >= 6


def test_boom_bap_mode_keeps_hats_on_the_grid():
    for v in range(6):
        p, _ = _composed("New Math", v, boom_bap=True)
        assert all(len(b) == 16 for b in p["lanes"]["hat"][3])
        assert p["kit"]["kick"][3][1] <= 0.8  # no 2-second 808 tails
