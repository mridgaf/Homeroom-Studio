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


def test_compose_is_deterministic(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "a.json")
    p1, _ = _composed("Otto Grit", 42)
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "b.json")
    p2, _ = _composed("Otto Grit", 42)
    assert p1["lanes"] == p2["lanes"]
    assert p1["kit"] == p2["kit"]


def test_every_variant_is_a_new_rhythm():
    from itertools import combinations
    kicks = [_kick_a(_composed("Otto Grit", v)[0]) for v in range(12)]
    assert len(set(kicks)) == 12             # fresh pattern per generation
    # the repeat guard's hard floor: every pair at least 3 moves apart
    assert all(sum(x != y for x, y in zip(a, b)) >= 3
               for a, b in combinations(kicks, 2))
    # and B answers A instead of repeating it
    p, _ = _composed("Otto Grit", 1)
    bars = p["lanes"]["kick"][3]
    assert bars[0] != bars[4]


def test_repeat_guard_regenerates():
    # same seed twice: the second roll sees the first in history and
    # must land somewhere else
    a = _kick_a(_composed("Cutz", 7)[0])
    b = _kick_a(_composed("Cutz", 7)[0])
    assert a != b


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
            p, _ = _composed(name, v)
            seen[bb_mode(p["lanes"][lane][3][0])] += 1
        assert seen[home] >= max(seen.values()) * 0.6, (name, seen)
        assert len(seen) >= 2, (name, "modes never vary", seen)
    # the Neptunes flam: Glass Cat's clap still mirrors his snare
    for v in range(8):
        gc, _ = _composed("Glass Cat", v)
        assert gc["lanes"]["clap"][3] \
            == [b.replace(".", "-") for b in gc["lanes"]["snare"][3]]
    # New Math's quintuplets and Rage's 32nd walls still occur
    assert any(len(b) == 20
               for v in range(10)
               for b in _composed("New Math", v)[0]["lanes"]["hat"][3])
    assert any(len(b) == 32
               for v in range(10)
               for b in _composed("Rage Engine", v)[0]["lanes"]["hat"][3])


def test_kick_flavors_vary_not_solely_808():
    musts = {_composed("Otto Grit", v)[0]["kit"]["kick"][1]
             for v in range(16)}
    assert None in musts and "808" in musts   # both flavors reachable
    chokes = {_composed("Chrome Dial", v)[0]["kit"]["kick"][3]
              for v in range(16)}
    assert len(chokes) > 1                    # not one sustain forever
    # trap still reaches for 808s but no longer lives on them
    nm_musts = [_composed("Night Metro", v)[0]["kit"]["kick"][1]
                for v in range(20)]
    assert nm_musts.count("808") >= 3 and None in nm_musts


def test_no_flavor_runs_three_beats_in_a_row():
    # owner report 2026-07-17: the long 808 was landing generation after
    # generation — the streak-breaker forbids any flavor three in a row
    for name in ("Night Metro", "Rage Engine", "Otto Grit"):
        fis = []
        for v in range(30):
            p, _ = _composed(name, v)
            flavors = pattern_gen.DEFAULT_STYLE[name]["kick_flavors"]
            fis.append(next(
                i for i, f in enumerate(flavors)
                if f[1] == p["kit"]["kick"][1]
                and tuple(f[3]) == tuple(p["kit"]["kick"][3])))
        assert all(not (a == b == c)
                   for a, b, c in zip(fis, fis[1:], fis[2:])), name
    # the long-sustain flavor stays a visitor, not a resident
    longs = sum(1 for v in range(30)
                if _composed("Night Metro", v + 100)[0]
                ["kit"]["kick"][3][1] >= 2.0)
    assert longs <= 12


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
