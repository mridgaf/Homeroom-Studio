"""Engine-driven evolution (tools/evolution.py): bounded changes, exact
rollback, one-per-day pacing, and the untouchables staying untouched."""
import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import crew
import evolution
from crew import DEFAULT_CREW


@pytest.fixture
def env(tmp_path, monkeypatch):
    """A sandbox config + journal so the real career files never move."""
    cfg = tmp_path / "crew_config.json"
    monkeypatch.setattr(crew, "CONFIG", cfg)
    monkeypatch.setattr(evolution, "JOURNAL", tmp_path / "journal.json")
    fresh = crew.load_crew(cfg)          # writes the default roster
    crew.CREW.clear()
    crew.CREW.update(fresh)
    yield cfg
    # restore the real roster for other test modules
    monkeypatch.undo()
    crew.CREW.clear()
    crew.CREW.update(crew.load_crew())


def _raw(cfg):
    return json.loads(cfg.read_text())


UNTOUCHABLE = ("lanes", "bpm", "era", "built", "dust", "vinyl", "wow",
               "sidechain", "space", "alt", "drive", "kick_dist", "mix_sat")


@pytest.mark.parametrize("name", sorted(DEFAULT_CREW))
def test_evolve_changes_one_thing_and_rollback_restores_it(env, name):
    before = _raw(env)[name]
    note = evolution.evolve_one(name)
    assert note                              # something applied
    after = _raw(env)[name]
    assert after != before
    # the untouchables: timing DNA, mix flavor, identity numbers
    for k in UNTOUCHABLE:
        assert after.get(k) == before.get(k), (name, k)
    # exact rollback
    change = evolution.rollback(name)
    assert change == note
    assert _raw(env)[name] == before


def test_once_per_day_and_never_same_op_twice(env):
    j = evolution._load_journal()
    assert evolution.evolve_one("Otto Grit", journal=j)
    assert evolution.evolved_today("Otto Grit", j)
    # maybe_evolve refuses a second change the same day
    assert evolution.maybe_evolve(["Otto Grit"]) == []
    # a later day picks a different op
    op1 = j["Otto Grit"][-1]["op"]
    assert evolution.evolve_one("Otto Grit", journal=j, when="2099-01-01")
    assert j["Otto Grit"][-1]["op"] != op1


def test_evolution_is_deterministic_per_day(env, tmp_path, monkeypatch):
    note1 = evolution.evolve_one("Cutz", when="2099-06-01")
    snap1 = _raw(env)["Cutz"]
    # reset and repeat: same day, same change
    evolution.rollback("Cutz")
    monkeypatch.setattr(evolution, "JOURNAL", tmp_path / "j2.json")
    note2 = evolution.evolve_one("Cutz", when="2099-06-01")
    assert note1 == note2
    assert _raw(env)["Cutz"] == snap1


def test_long_808_cap_holds_through_many_leans(env):
    rng_days = ["2099-01-%02d" % d for d in range(1, 15)]
    for day in rng_days:
        evolution.evolve_one("Night Metro", when=day)
    for w, must, _wants, secs in _raw(env)["Night Metro"]["kick_flavors"]:
        hi = secs[1] if isinstance(secs, list) else secs
        if must == "808" and hi >= 1.2:
            assert w <= evolution.LONG_808_CAP + 1e-9


def test_bounds_hold_under_sustained_evolution(env):
    for d in range(1, 25):
        evolution.evolve_one("Rage Engine", when="2099-02-%02d" % d)
        evolution.evolve_one("Glass Cat", when="2099-02-%02d" % d)
    for name in ("Rage Engine", "Glass Cat"):
        p = _raw(env)[name]
        lo, hi = p["kit"]["kick"][3]
        assert 0.2 <= lo < hi <= 2.4, name
        if "library" in p:
            assert 0.05 <= p["library"]["p"] <= 0.6
        assert 0.1 <= p["extras"]["p"] <= 0.9
        for lane, spec in p["grammar"].items():
            for m in spec.get("modes", []):
                assert m[1] >= 0.04, (name, lane)   # every mode stays alive


def test_style_lock_set_so_resync_cant_erase_careers(env):
    evolution.evolve_one("Sunday Chop")
    doc = _raw(env)
    assert doc.get("_style_lock") is True
    # a fake future style bump must NOT clobber the evolved keys
    doc["_style_version"] = 0
    env.write_text(json.dumps(doc))
    snap = doc["Sunday Chop"]
    loaded = crew.load_crew(env)
    assert json.loads(env.read_text())["Sunday Chop"] == snap
    assert set(loaded) == set(DEFAULT_CREW)


def test_in_memory_roster_updates_immediately(env):
    before = copy.deepcopy(crew.CREW["Chrome Dial"])
    evolution.evolve_one("Chrome Dial")
    assert crew.CREW["Chrome Dial"] != before   # same session, new taste


def test_maybe_evolve_never_raises(monkeypatch, tmp_path):
    # a broken config must come back quiet, not crash a render
    monkeypatch.setattr(crew, "CONFIG", tmp_path / "nope.json")
    monkeypatch.setattr(evolution, "JOURNAL", tmp_path / "j.json")
    assert evolution.maybe_evolve(["Otto Grit"]) == []


def test_rollback_with_nothing_active(env):
    assert evolution.rollback("New Math") is None
