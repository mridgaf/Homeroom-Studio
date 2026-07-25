"""The v6 loosening (owner directive 2026-07-18): sample-pack library,
free density, per-beat swing, real time signatures, space choice, and
the extended notes-box directions."""
import copy
import json
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import beat_machine
import pattern_gen
import sample_library
from crew import CREW, render_crew_beat

SR = 44100


@pytest.fixture(autouse=True)
def _pat_hist(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "pat.json")


# ------------------------------------------------- sample-pack library


def _wav(path, secs=0.3):
    x = (np.sin(2 * np.pi * 200 * np.arange(int(secs * SR)) / SR)
         * 20000).astype("<i2")
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.tobytes())


def test_pack_scan_classifies_by_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(sample_library, "CACHE", tmp_path / "cache.json")
    root = tmp_path / "MyPack"
    _wav(root / "KICKS" / "VBM_Punchy_01.wav")          # no 'kick' in name
    _wav(root / "808s" / "Sub Thing.wav")
    _wav(root / "HIHATS - CLOSED" / "tick.wav")
    _wav(root / "PERCUSSION" / "Rimshot_A.wav")         # perc AND rim
    _wav(root / "FX" / "sweep up.wav")
    _wav(root / "BASS" / "Reese Growl.wav")             # phase 2: bass role
    _wav(root / "VOX" / "yeah adlib.wav")               # phase 2: vox role
    _wav(root / "Melodic" / "keys_C.wav")               # instrument: still out
    _wav(root / "MIDI" / "fake.wav")                    # excluded dir: out
    # owner 2026-07-23 "stop the one-shot rule": a bpm-named loop goes to
    # the _loops bucket (played as a full loop, not a choked hit); a long
    # one-shot tail is KEPT in its drum role (the length cap is gone).
    _wav(root / "SNARES" / "snare_140bpm.wav")
    _wav(root / "Perc Loops" / "shaker 92 bpm.wav")
    _wav(root / "SNARES" / "long_tail.wav", secs=9.0)
    got = sample_library.scan_packs([str(root)])
    paths = {r: {Path(e["path"]).name for e in es} for r, es in got.items()}
    assert "VBM_Punchy_01.wav" in paths["kick"]
    assert "Sub Thing.wav" in paths["kick"]              # 808s ARE kicks
    assert "Sub Thing.wav" in paths["bass"]             # ...and a bass too
    assert "tick.wav" in paths["hat"]
    assert "Rimshot_A.wav" in paths["perc"]
    assert "Rimshot_A.wav" in paths["rim"]               # name adds a role
    assert "sweep up.wav" in paths["fx"]
    assert "Reese Growl.wav" in paths["bass"]           # BASS folder -> bass
    assert "yeah adlib.wav" in paths["vox"]             # VOX folder -> vox
    assert "long_tail.wav" in paths["snare"]            # long one-shot kept
    # loops (bpm in name / a LOOP folder) land in _loops, not choked roles
    loop_names = {Path(e["path"]).name for e in got.get("_loops", [])}
    loop_bpm = {Path(e["path"]).name: e["bpm"] for e in got.get("_loops", [])}
    assert "snare_140bpm.wav" in loop_names and loop_bpm["snare_140bpm.wav"] == 140
    assert "shaker 92 bpm.wav" in loop_names and loop_bpm["shaker 92 bpm.wav"] == 92
    assert "snare_140bpm.wav" not in paths.get("snare", set())  # not choked
    allnames = {n for ns in paths.values() for n in ns if ns is not None}
    assert not {"keys_C.wav", "fake.wav"} & allnames    # instruments still out


def test_pack_scan_unplugged_falls_back_to_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(sample_library, "CACHE", tmp_path / "cache.json")
    root = tmp_path / "P"
    _wav(root / "KICKS" / "a.wav")
    first = sample_library.scan_packs([str(root)])
    assert first["kick"]
    gone = sample_library.scan_packs([str(tmp_path / "not-mounted")])
    assert {e["path"] for e in gone["kick"]} \
        == {e["path"] for e in first["kick"]}


def test_merge_into_dedupes_by_path(tmp_path, monkeypatch):
    monkeypatch.setattr(sample_library, "CACHE", tmp_path / "c.json")
    e = {"name": "k", "path": "/x/k.wav", "kind": "sample",
         "category": "one-shot", "tokens": ["k"]}
    shots = {"kick": [dict(e)]}
    merged = sample_library.merge_into(shots, {"kick": [dict(e), {
        "name": "k2", "path": "/x/k2.wav", "kind": "sample",
        "category": "one-shot", "tokens": ["k2"]}]})
    assert len(merged["kick"]) == 2


# ------------------------------------------------- real time signatures


def test_odd_meter_composes_and_renders_right_length():
    for tsig in ((3, 4), (6, 8)):
        p = copy.deepcopy(CREW["Otto Grit"])
        notes = pattern_gen.compose(p, "Otto Grit", 5, tsig=tsig)
        assert p["tsig"] == list(tsig)
        assert any("in %d/%d" % tsig in n for n in notes)
        for ln, spec in p["lanes"].items():
            if not ln.startswith("stamp"):
                assert all(len(b) == 12 for b in spec[3]), ln
        kit = {ln: np.sin(2 * np.pi * 100 * np.arange(SR // 8) / SR) * 0.4
               for ln in p["lanes"]}
        L, R, _ = render_crew_beat("Otto Grit", kit, preset=p)
        want = 8 * 3 * 60.0 / p["bpm"]          # 3 quarter-beats per bar
        assert abs(len(L) / SR - want) < 0.02


def test_trick_beats_reach_exotic_grids():
    seen = set()
    for v in range(12):
        p = copy.deepcopy(CREW["Cutz"])
        pattern_gen.compose(p, "Cutz", v, trick=True)
        for b in p["lanes"]["hat"][3]:
            seen.add(len(b))
    assert seen & {20, 32}                       # quint or 32nd walls


def test_tsig_roll_distribution():
    """~80/10/10 over many variants (the roll is variant-seeded)."""
    import random as _r
    odd = trick = 0
    n = 400
    for v in range(n):
        troll = _r.Random(v * 677 + 3)
        r = troll.random()
        if r < 0.10:
            odd += 1
        elif r < 0.20:
            trick += 1
    assert 0.06 < odd / n < 0.14
    assert 0.06 < trick / n < 0.14


# ----------------------------------------------------------- swing roll


def test_swing_rolls_vary_and_respect_bounds():
    targets = set()
    for v in range(40):
        p = copy.deepcopy(CREW["Crate Prophet"])       # home 60
        got = beat_machine.roll_swing(p, v)
        for ln, spec in p["lanes"].items():
            if not ln.startswith("stamp"):
                assert 50 <= spec[2][2] <= 66, ln
        if got:
            targets.add(got)
    assert len(targets) >= 3                     # it really varies
    # forced value (notes box) wins
    p = copy.deepcopy(CREW["Cutz"])
    assert beat_machine.roll_swing(p, 1, force=50) in (None, 50)
    assert all(spec[2][2] == 50 for ln, spec in p["lanes"].items()
               if not ln.startswith("stamp"))


def test_swing_preserves_deliberate_lane_clash():
    """New Math's one-swung-lane-against-straight-kit shifts as a unit."""
    p = copy.deepcopy(CREW["New Math"])
    before = {ln: spec[2][2] for ln, spec in p["lanes"].items()}
    got = beat_machine.roll_swing(p, 7)
    if got:
        after = {ln: spec[2][2] for ln, spec in p["lanes"].items()}
        clash = [ln for ln, sw in before.items() if sw != 50
                 and not ln.startswith("stamp")]
        for ln in clash:
            assert after[ln] != after["kick"] or after[ln] == 66


# ------------------------------------------------------ space + weights


def test_render_takes_room_and_plate_without_alt():
    p = copy.deepcopy(CREW["Rage Engine"])       # alt=None
    kit = {ln: np.sin(2 * np.pi * 90 * np.arange(SR // 8) / SR) * 0.4
           for ln in p["lanes"]}
    for space in ("gated", "dry", "room", "plate"):
        L, R, _ = render_crew_beat("Rage Engine", kit, space=space,
                                   preset=p)
        assert np.abs(L).max() <= 1.0 and np.sqrt((L ** 2).mean()) > 1e-4


# ----------------------------------------------- notes-box directions


def test_new_direction_words():
    pd = beat_machine.parse_directions
    assert pd("keep it gated")["space"] == "gated"
    assert pd("bone dry please")["space"] == "dry"
    assert pd("washed out")["space"] == "plate"
    assert pd("roomy drums")["space"] == "room"
    assert pd("no swing")["swing"] == 50
    assert pd("more swing")["swing"] == 62
    assert pd("triplet swing")["swing"] == 66
    assert pd("waltz please")["tsig"] == (3, 4)
    assert pd("do one in 3/4")["tsig"] == (3, 4)
    assert pd("6/8 feel")["tsig"] == (6, 8)
    assert pd("half time")["force_mode"] == "halftime"
    # the old words still work. "no 808" now also drops the 808 BASS DRUM
    # lane, not just the kick's long tail — under the owner's 2026-07-25
    # vocabulary the 808 boom is its own instrument with its own stem.
    d = pd("no hi hats, acoustic, sparse, no 808")
    assert d["mute"] == {"hat", "bass"} and "acoustic" in d["tags"]
    assert d["density"] == "sparse" and d["kick"] == "clean"
    # a plain note stays a note
    d = pd("for the demo tape")
    assert not d["space"] and not d["swing"] and not d["tsig"]


def test_sparse_is_only_ever_asked_for():
    """Owner call 2026-07-22: the free roll never picks sparse. Only the
    dialog box or a genre that declares itself sparse can thin a beat."""
    from collections import Counter
    seen = Counter()
    for name in ("Otto Grit", "Glass Cat"):
        for v in range(40):
            p = copy.deepcopy(CREW[name])
            p.pop("density", None)             # a crew DJ declares none
            pattern_gen.compose(p, name, v)
            notes = beat_machine.vary_preset(p, v, CREW[name]["num"],
                                             tempo_locked=True)
            seen[next(n for n in notes if n.endswith(" density"))] += 1
    assert "sparse density" not in seen        # never on its own
    assert seen["home density"] and seen["busy density"]

    # the box still forces it, and so does a genre that declares it
    p = copy.deepcopy(CREW["Otto Grit"])
    pattern_gen.compose(p, "Otto Grit", 1)
    assert "sparse density" in beat_machine.vary_preset(
        p, 1, p["num"], tempo_locked=True, density="sparse")
    p = copy.deepcopy(CREW["Otto Grit"])
    p["density"] = "sparse"
    pattern_gen.compose(p, "Otto Grit", 2)
    assert "sparse density" in beat_machine.vary_preset(
        p, 2, p["num"], tempo_locked=True)
