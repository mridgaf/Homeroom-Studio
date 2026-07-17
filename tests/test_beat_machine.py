"""The 2026-07-16 spec features: config file, recipes + swap, MIDI +
stems, sample history, and the 50/50 collab blend."""
import json
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import beat_machine
import beat_recipes
import crew
import pattern_gen
from crew import CREW

SR = 44100


@pytest.fixture(autouse=True)
def _pat_hist(tmp_path, monkeypatch):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "pat.json")


# ------------------------------------------------------------ config file

def test_config_file_round_trips_the_roster(tmp_path):
    cfg = tmp_path / "crew_config.json"
    first = crew.load_crew(cfg)
    assert cfg.exists()                      # written on first run
    again = crew.load_crew(cfg)              # loaded ever after
    assert set(first) == set(CREW)
    assert first == again
    # shapes survive the JSON round-trip (tests elsewhere rely on tuples)
    assert isinstance(first["Otto Grit"]["kit"]["kick"][3], tuple)
    assert isinstance(first["Otto Grit"]["lanes"]["kick"][2], tuple)


def test_config_edit_takes_effect(tmp_path):
    cfg = tmp_path / "crew_config.json"
    crew.load_crew(cfg)
    doc = json.loads(cfg.read_text())
    doc["Otto Grit"]["bpm"] = 84
    cfg.write_text(json.dumps(doc))
    assert crew.load_crew(cfg)["Otto Grit"]["bpm"] == 84


def test_broken_config_falls_back_to_builtins(tmp_path, capsys):
    cfg = tmp_path / "crew_config.json"
    cfg.write_text("{not json")
    loaded = crew.load_crew(cfg)
    assert set(loaded) == set(crew.DEFAULT_CREW)
    assert "WARNING" in capsys.readouterr().out


# ------------------------------------------------------------------- MIDI

def test_midi_file_is_valid_smf(tmp_path):
    f = tmp_path / "beat.mid"
    beat_recipes.write_midi(f, {"kick": [(0.0, 1.0), (0.5, 0.7)],
                                "snare": [(0.25, 0.9)],
                                "empty": []}, bpm=96)
    b = f.read_bytes()
    assert b[:4] == b"MThd"
    assert int.from_bytes(b[10:12], "big") == 3   # tempo + 2 non-empty lanes
    assert b.count(b"MTrk") == 3
    # the kick's second hit: 0.5 s at 96 bpm = 0.8 quarters = 384 ticks
    assert int.from_bytes(b[12:14], "big") == 480  # tpq


def test_midi_velocities_keep_accents(tmp_path):
    f = tmp_path / "beat.mid"
    beat_recipes.write_midi(f, {"hat": [(0.0, 0.36), (0.1, 0.26)]}, bpm=120)
    b = f.read_bytes()
    i = b.index(b"\x99\x2a")                  # first note-on, note 42
    j = b.index(b"\x99\x2a", i + 1)
    assert b[i + 2] > b[j + 2]                # louder hit = higher velocity


# ------------------------------------------------------------ 50/50 blend

def test_collab_splits_the_jobs_evenly():
    p, _ = beat_machine.collab_preset(["Otto Grit", "Sunday Chop"], 7, None)
    parents = set(p["lane_parent"].values())
    assert parents == {"Otto Grit", "Sunday Chop"}
    jobs = {}
    for lane, parent in p["lane_parent"].items():
        job = beat_machine.LANE_JOB.get(lane, "color")
        jobs.setdefault(job, set()).add(parent)
    # each job comes wholly from one parent, two jobs each
    assert all(len(v) == 1 for v in jobs.values())
    per_parent = [sum(1 for v in jobs.values() if v == {n})
                  for n in ("Otto Grit", "Sunday Chop")]
    assert sorted(per_parent) == [2, 2]
    # every blended lane can be picked and rendered
    assert set(p["kit"]) == {ln for ln in p["lanes"]
                             if not ln.startswith("stamp")}
    assert all(ln in p["lanes"] for ln in p["space"][1])
    # both stamps ride
    assert "stamp" in p["lanes"] and "stamp2" in p["lanes"]
    # tempo meets in the middle
    assert p["bpm"] == round((88 + 96) / 2)


def test_collab_deal_varies_by_variant():
    deals = {tuple(sorted(beat_machine.collab_preset(
        ["Cutz", "Night Metro"], v, None)[0]["lane_parent"].items()))
        for v in range(8)}
    assert len(deals) > 1                    # the split isn't frozen


# ---------------------------------------------------------------- history

def test_history_remembers_and_trims(tmp_path, monkeypatch):
    monkeypatch.setattr(beat_recipes, "HIST", tmp_path / "hist.json")
    for i in range(beat_recipes.HIST_KEEP + 3):
        beat_recipes.record_history({"kick": "Otto Grit"},
                                    {"kick": f"/lib/k{i}.wav",
                                     "stamp": "/lib/stamp.wav"})
    avoid = beat_recipes.history_avoid(["Otto Grit"])
    assert len(avoid) == beat_recipes.HIST_KEEP          # trimmed
    assert f"/lib/k{beat_recipes.HIST_KEEP + 2}.wav" in avoid  # newest kept
    assert "/lib/k0.wav" not in avoid                    # oldest gone
    assert "/lib/stamp.wav" not in avoid                 # stamps never
    assert beat_recipes.history_avoid(["Cutz"]) == set()


# ------------------------------------------------- end-to-end + swap flow

def _wav_pool(tmp_path, n=8):
    """A little library: n loadable wavs PER role (roles get their own
    files so the nine locked stamps can't drain the drum pools — that
    pool-dry fallback is tested for real libraries elsewhere)."""
    shots = {}
    for r, role in enumerate(("kick", "snare", "hat", "clap", "snap",
                              "perc", "bongo", "fx", "crash", "rim")):
        files = []
        for i in range(n):
            f = tmp_path / f"{role}_808_{chr(97 + i)}.wav"
            x = (np.sin(2 * np.pi * (55 + 15 * r + 20 * i)
                        * np.arange(SR // 4) / SR) * 32000).astype("<i2")
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(SR)
                w.writeframes(x.tobytes())
            files.append(f)
        shots[role] = [{"name": f.stem, "path": str(f)} for f in files]
    return shots


@pytest.fixture
def machine_env(tmp_path, monkeypatch):
    monkeypatch.setattr(crew, "LOCK", tmp_path / "crew_kits.json")
    monkeypatch.setattr(beat_recipes, "HIST", tmp_path / "hist.json")
    root = tmp_path / "beats"
    root.mkdir()
    return root, _wav_pool(tmp_path)


def test_generate_ships_wav_midi_stems_and_recipe(machine_env):
    root, shots = machine_env
    path, report = beat_machine.generate(["Otto Grit"], root=root,
                                         shots=shots)
    assert path.exists() and path.suffix == ".wav"
    assert path.with_suffix(".mid").exists()
    stem_dir = path.parent / path.name.replace(".wav", "").replace(
        f" Drums {path.stem.split()[-1][:-3]}bpm", " Stems")
    stem_dirs = list(path.parent.glob("* Stems"))
    assert len(stem_dirs) == 1
    stems = {f.stem for f in stem_dirs[0].glob("*.wav")}
    assert {"kick", "snare", "hat"} <= stems
    assert "vinyl" in stems                   # Otto's bed ships as a stem
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert rec["names"] == ["Otto Grit"]
    assert set(rec["kit_paths"]) == set(rec["kit_spec"])
    # history recorded the picks
    assert rec["kit_paths"]["kick"] in beat_recipes.history_avoid(
        ["Otto Grit"])


def test_no_repetition_across_generations(machine_env):
    root, shots = machine_env
    p1, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    p2, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    r1 = beat_recipes.load_recipe(root, int(p1.name.split()[0]))
    r2 = beat_recipes.load_recipe(root, int(p2.name.split()[0]))
    for lane in ("kick", "snare", "hat"):
        assert r1["kit_paths"][lane] != r2["kit_paths"][lane], lane
    # ...and the FINAL rendered kick lines differ too (2026-07-17: two
    # beats once collapsed to the same line during the variety pass)
    k1 = r1["preset"]["lanes"]["kick"][3][0]
    k2 = r2["preset"]["lanes"]["kick"][3][0]
    assert sum(a != b for a, b in zip(k1, k2)) >= 3


def test_final_kick_guard_rerolls(tmp_path, monkeypatch):
    """The generate-level guard: once a kick line is remembered, the
    next roll must land somewhere else."""
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "p.json")
    bar = "X---------X-----"
    pattern_gen.remember_kick("Otto Grit", bar)
    assert pattern_gen.kick_seen("Otto Grit", bar)
    assert pattern_gen.kick_seen("Otto Grit", "X---------X----x")  # 1 off
    assert not pattern_gen.kick_seen("Otto Grit", "X--x--x-X-------")
    assert not pattern_gen.kick_seen("Cutz", bar)   # per-DJ memory


def test_swap_changes_one_drum_and_nothing_else(machine_env):
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    new_path, report = beat_machine.swap(no, "snare", root=root,
                                         shots=shots)
    assert new_path.exists() and path.exists()          # nothing overwritten
    assert "New Snare" in new_path.name
    assert new_path.with_suffix(".mid").exists()
    rec, rec2 = (beat_recipes.load_recipe(root, n)
                 for n in (no, int(new_path.name.split()[0])))
    assert rec2["parent"] == no
    assert rec2["kit_paths"]["snare"] != rec["kit_paths"]["snare"]
    unchanged = {k: v for k, v in rec["kit_paths"].items() if k != "snare"}
    assert unchanged == {k: v for k, v in rec2["kit_paths"].items()
                         if k != "snare"}
    assert rec2["preset"] == rec["preset"]              # pattern locked


def test_swap_rejects_a_lane_the_beat_lacks(machine_env):
    root, shots = machine_env
    path, _ = beat_machine.generate(["Night Metro"], root=root, shots=shots)
    no = int(path.name.split()[0])
    with pytest.raises(ValueError, match="has no 'bongo'"):
        beat_machine.swap(no, "bongo", root=root, shots=shots)


# --------------------------------------- space rules (owner 2026-07-17)

def test_no_silent_bars_ever():
    """Owner rule: room = sparseness, never a gap. Across many variants,
    every bar keeps at least the kick+snare backbone playing."""
    import copy as _copy
    for name in ("Otto Grit", "Night Metro", "Glass Cat"):
        for v in range(25):
            p = _copy.deepcopy(CREW[name])
            pattern_gen.compose(p, name, v)
            beat_machine.vary_preset(p, v, CREW[name]["num"],
                                     tempo_locked=False)
            backbone = [ln for ln in p["lanes"]
                        if ln in beat_machine.BACKBONE]
            for b in range(8):
                hits = sum(sum(c != "-" for c in p["lanes"][ln][3][b])
                           for ln in backbone)
                assert hits > 0, (name, v, b)


def test_direction_parser_reads_his_words():
    pd = beat_machine.parse_directions
    d = pd("no hi hats please, acoustic sounding")
    assert d["mute"] == {"hat"} and "acoustic" in d["tags"]
    # his actual spelling from the 2026-07-17 README — must parse
    assert pd("no high hats")["mute"] == {"hat"}
    assert pd("No High Hats.")["mute"] == {"hat"}
    assert pd("remove the cymbals, acoustic")["mute"] == {"hat"}
    assert pd("take out the kick")["mute"] == {"kick"}
    assert pd("without snare")["mute"] == {"snare"}
    assert pd("no 808")["kick"] == "clean"
    assert pd("long 808 sustained")["kick"] == "808"
    assert pd("keep it sparse and dusty")["density"] == "sparse"
    assert pd("")["mute"] == set() and pd("")["density"] is None
    # a plain note stays a note
    assert pd("for the demo tape")["mute"] == set()


def test_directions_apply_to_that_click_only(machine_env):
    root, shots = machine_env
    p1, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots,
                                  notes="no hats, acoustic sounding")
    rec1 = beat_recipes.load_recipe(root, int(p1.name.split()[0]))
    assert "hat" not in rec1["kit_paths"]              # muted this click
    assert "hat" not in rec1["preset"]["lanes"]
    assert rec1["kit_spec"]["snare"][2][0] == "acoustic"  # tag leads
    # ...and the next click is back to normal
    p2, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    rec2 = beat_recipes.load_recipe(root, int(p2.name.split()[0]))
    assert "hat" in rec2["kit_paths"]
    assert rec2["kit_spec"]["snare"][2][0] != "acoustic"


def test_collab_end_to_end(machine_env):
    root, shots = machine_env
    path, report = beat_machine.generate(["Sunday Chop", "Cutz"],
                                         root=root, shots=shots)
    assert path.parent.name == "Sunday Chop"            # first checked
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert set(rec["preset"]["lane_parent"].values()) \
        == {"Sunday Chop", "Cutz"}
    assert "50/50" in (root / "README.txt").read_text()
