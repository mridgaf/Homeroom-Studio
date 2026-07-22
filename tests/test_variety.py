"""The variety scorer (tools/variety.py) and the sameness-drift
regression: compose fresh variants for every DJ and hold the floors the
owner's ears demanded (2026-07-16, "every beat significantly different").
"""
import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import crew
import pattern_gen
import variety
from crew import CREW


@pytest.fixture(autouse=True)
def _pat_hist(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "pat.json")


# ------------------------------------------------------------ primitives


def test_moves_is_hamming_and_grids_never_collide():
    assert variety.moves("X---", "X---") == 0
    assert variety.moves("X---", "X--x") == 1
    # different grid lengths = maximal distance, not an error
    assert variety.moves("X" * 16, "X" * 20) == 20


def test_longest_streak():
    assert variety.longest_streak([]) == 0
    assert variety.longest_streak([1]) == 1
    assert variety.longest_streak([1, 1, 2, 2, 2, 1]) == 3


def test_density():
    assert variety.density(["x-x-", "----"]) == 1.0
    assert variety.density([]) == 0.0


# --------------------------------------------------------- recipe scoring


def _fake_recipe(no, kick_bars, kit, must="808", secs=1.5, bpm=90,
                 dj="Otto Grit", guests=None):
    preset = {"lanes": {"kick": [0.0, 1.0, [0, 3, 50, 1], kick_bars],
                        "hat": [0.1, 0.4, [0, 2, 50, 2], ["x-" * 8] * 8]}}
    if guests:
        preset["_guests"] = guests
    return {"file": f"{no} beat.wav", "folder": dj, "names": [dj],
            "bpm": bpm, "preset": preset,
            "kit_spec": {"kick": ["kick", must, ["deep"], secs]},
            "kit_paths": {ln: p for ln, p in kit.items()}}


def _write(root, recs):
    d = root / ".recipes"
    d.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(recs, 1):
        (d / f"{i}.json").write_text(json.dumps(r))


def test_identical_beats_flag_everything(tmp_path):
    bars = ["X-----x---X-----"] * 8
    kit = {"kick": "/k/a.wav", "snare": "/s/a.wav", "hat": "/h/a.wav"}
    _write(tmp_path, [_fake_recipe(i, bars, kit) for i in range(1, 5)])
    out = variety.score_dj(tmp_path, "Otto Grit", last=4)
    assert out["kick_min"] == 0
    assert out["kit_overlap_max"] == 1.0
    assert out["flavor_streak"] == 4
    assert out["flags"]                       # loudly unhealthy


def test_varied_beats_pass_clean(tmp_path):
    kicks = ["X------x--X-----", "X--X--X-X-X-X---",
             "X---x-x-X---x-x-", "X-----X-----X--X"]
    musts = ["808", None, "808", None]
    recs = []
    for i, (k, m) in enumerate(zip(kicks, musts), 1):
        kit = {"kick": f"/k/{i}.wav", "snare": f"/s/{i}.wav",
               "hat": f"/h/{i}.wav"}
        recs.append(_fake_recipe(i, [k] * 8, kit, must=m,
                                 secs=0.4 + 0.3 * i, bpm=88 + i))
    _write(tmp_path, recs)
    out = variety.score_dj(tmp_path, "Otto Grit", last=4)
    assert out["flags"] == []
    assert out["kick_min"] >= variety.FLOORS["kick_min"]
    assert out["kit_overlap_max"] == 0.0
    assert out["flavor_kinds"] >= 2


def test_quick_check_never_raises(tmp_path):
    # empty library, garbage file — both come back quiet, not crashing
    assert variety.quick_check(tmp_path, "Otto Grit") is None
    d = tmp_path / ".recipes"
    d.mkdir()
    (d / "1.json").write_text("{broken")
    assert variety.quick_check(tmp_path, "Otto Grit") is None


def test_quick_check_reports_sameness(tmp_path):
    bars = ["X-----x---X-----"] * 8
    kit = {"kick": "/k/a.wav", "snare": "/s/a.wav"}
    _write(tmp_path, [_fake_recipe(i, bars, kit) for i in range(1, 5)])
    msg = variety.quick_check(tmp_path, "Otto Grit")
    assert msg and msg.startswith("variety check:")


def test_collabs_count_for_the_host(tmp_path):
    kit = {"kick": "/k/a.wav"}
    r = _fake_recipe(1, ["X---" * 4] * 8, kit)
    r["names"] = ["Otto Grit", "Cutz"]
    _write(tmp_path, [r])
    assert variety.load_recipes(tmp_path, "Otto Grit")
    assert not variety.load_recipes(tmp_path, "Cutz")


# ------------------------------------- the sameness-drift regression
# The scorer floors, held against the LIVE engine: if a grammar edit or
# a new pass ever collapses a DJ's output back toward one rhythm, these
# fail before the owner's ears have to.


def _compose_kicks(name, n):
    kicks = []
    for v in range(n):
        p = copy.deepcopy(CREW[name])
        pattern_gen.compose(p, name, v)
        kicks.append(p["lanes"]["kick"][3][0])
    return kicks


# The subgenre roster is deliberately EXCLUDED (owner rule 2026-07-19:
# "the genres do not have to follow any of the rules, so they stay true
# to the genre"). A style's kick is supposed to be recognisable — every
# dembow shares one, the Baltimore 8-count IS the genre — so scoring it
# for pairwise distance would measure fidelity as if it were drift.
# tests/test_genres.py holds them to style identity instead.
@pytest.mark.parametrize("name", sorted(set(CREW) - crew.GENRE_NAMES))
def test_every_dj_composes_apart(name):
    kicks = _compose_kicks(name, 10)
    dists = variety.pairwise(kicks, variety.moves)
    # owner call 2026-07-21: different is the promise, distance is not —
    # no exact repeats in a window, and the window still spreads on
    # average (a report-floor nudge, not an engine guard)
    assert min(dists) >= 1, name
    assert sum(dists) / len(dists) >= variety.FLOORS["kick_mean"] - 1, name


def test_backbeat_modes_actually_spread():
    """DJs whose grammar offers several backbeat modes must use them:
    12 variants should not all land on one mode."""
    for name, lane in (("Otto Grit", "snare"), ("Chrome Dial", "clap"),
                       ("New Math", "snare")):
        firsts = set()
        for v in range(12):
            p = copy.deepcopy(CREW[name])
            pattern_gen.compose(p, name, v)
            firsts.add(p["lanes"][lane][3][0])
        assert len(firsts) >= 3, name


def test_groove_library_seeds_reach_the_beats():
    """2026-07-17: the 131-groove library was imported but never wired
    into compose() — this holds the wiring in place. Seeds must appear,
    respect the sparse-bed kick cap, and never touch the backbeat."""
    seen = 0
    for name in ("New Math", "Otto Grit", "Night Metro"):
        for v in range(20):
            p = copy.deepcopy(CREW[name])
            notes = pattern_gen.compose(p, name, v + 900)
            if not any("groove seed" in n for n in notes):
                continue
            seen += 1
            kick = p["lanes"]["kick"][3]
            assert all(set(b) <= set("Xxo.-") for b in kick)
            # sparse-bed: the thinned seed (~<=5) plus _bank_vary's
            # sprinkle/double and phrase-tail fills stays a bed, never
            # a four-on-the-floor wall
            assert sum(c != "-" for c in kick[0]) <= 7
            assert all(sum(c != "-" for c in b) <= 9 for b in kick)
            # identity rule: the backbeat lane stays the DJ's grammar
            bb = next(ln for ln in ("snare", "clap")
                      if ln in p["lanes"])
            assert any(set(b) - {"-"} for b in p["lanes"][bb][3])
    assert seen >= 5                       # the taste p really fires


def test_timekeeper_density_moves_between_variants():
    seen = set()
    for v in range(12):
        p = copy.deepcopy(CREW["Otto Grit"])
        pattern_gen.compose(p, "Otto Grit", v)
        seen.add(round(variety.density(p["lanes"]["hat"][3])))
    assert len(seen) >= 2                  # sparse and busy hats both occur
