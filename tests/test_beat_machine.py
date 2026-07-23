"""The 2026-07-16 spec features: config file, recipes + swap, MIDI +
stems, sample history, and the 50/50 collab blend."""
import json
import random
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
    # crew_config.json holds the nine; the Legends live in their own file
    assert set(first) == {n for n in CREW if n not in crew.LEGEND_NAMES
                          and n not in crew.GENRE_NAMES}
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


def test_midi_chords_add_a_polyphonic_track(tmp_path):
    # punch list step 7: a chord track is opt-in (chords=None changes
    # nothing) and, when given, writes every note on channel 1 (0x90),
    # never channel 10 (0x99) — Reason must not read it as drum hits.
    f = tmp_path / "beat.mid"
    beat_recipes.write_midi(
        f, {"kick": [(0.0, 1.0)]}, bpm=96,
        chords=[{"start_sec": 0.0, "dur_sec": 2.0, "notes": [48, 51, 55]}])
    b = f.read_bytes()
    assert int.from_bytes(b[10:12], "big") == 3   # tempo + kick + chords
    assert b.count(b"MTrk") == 3
    assert b"chords" in b
    for note in (48, 51, 55):
        assert bytes([0x90, note]) in b
        assert bytes([0x99, note]) not in b


def test_midi_without_chords_is_unchanged(tmp_path):
    f1, f2 = tmp_path / "a.mid", tmp_path / "b.mid"
    events = {"kick": [(0.0, 1.0)]}
    beat_recipes.write_midi(f1, events, bpm=96)
    beat_recipes.write_midi(f2, events, bpm=96, chords=None)
    assert f1.read_bytes() == f2.read_bytes()


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
    # owner 2026-07-18: stems carry the real sample name after the lane
    # prefix ("kick - <sample>"), never just the generic role
    for lane in ("kick", "snare", "hat"):
        match = [s for s in stems if s.startswith(lane)]
        assert match, (lane, stems)
        assert all(" - " in s for s in match), (lane, stems)
    # owner 2026-07-18: clean renders — no vinyl bed baked in
    assert not any(s.startswith("vinyl") for s in stems)
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert rec["names"] == ["Otto Grit"]
    assert set(rec["kit_paths"]) == set(rec["kit_spec"])
    # history recorded the picks
    assert rec["kit_paths"]["kick"] in beat_recipes.history_avoid(
        ["Otto Grit"])


def test_add_the_root_puts_a_tuned_sub_under_traditional_beats(machine_env):
    # owner rule 2026-07-18 ("add the root"). It was switched off on
    # 2026-07-23 as collateral of that morning's engine-wide 808 ban, and
    # back on the same day when the ban was reversed — and NOTHING caught
    # either move, because the feature had no test. This is that guard.
    # random.seed fixes `variant`, which is the only input to the 3-in-4
    # roll, so this is deterministic rather than "render until it lands".
    root, shots = machine_env
    assert beat_machine.ADD_THE_ROOT_808, "the rule is off"
    random.seed(1)
    path, report = beat_machine.generate(["Mustang"], root=root, shots=shots,
                                         traditional=True)
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert rec.get("root_note"), report        # a real musical root
    assert "sub" in rec["preset"]["lanes"]
    stem_dir = next(d for d in path.parent.glob("* Stems")
                    if d.name.startswith(str(no)))
    assert any(f.stem.startswith("sub - synth 808 sub, root")
               for f in stem_dir.glob("*.wav")), list(stem_dir.iterdir())
    # ...and a chords beat skips it on purpose: harmony's own bass owns
    # the low end there, and a static sub under it just fights.
    path2, _ = beat_machine.generate(["Mustang"], root=root, shots=shots,
                                     traditional=True, notes="chords")
    rec2 = beat_recipes.load_recipe(root, int(path2.name.split()[0]))
    assert rec2.get("root_note") is None
    assert "sub" not in rec2["preset"]["lanes"]


def test_phase2_bass_vox_and_full_loop_lanes(machine_env, tmp_path, monkeypatch):
    # owner phase 2 (2026-07-23): the unlocked bass/808, vocal, and full-loop
    # samples get real lanes. Force the three rolls on (they are <1 by design)
    # and hand the engine a matching pool, so this is deterministic.
    root, shots = machine_env
    monkeypatch.setattr(beat_machine, "SAMPLED_BASS_P", 1.0)
    monkeypatch.setattr(beat_machine, "VOX_LANE_P", 1.0)
    monkeypatch.setattr(beat_machine, "LOOP_LANE_P", 1.0)
    lp = tmp_path / "shaker 96 bpm.wav"                  # a loadable loop file
    x = (np.sin(2 * np.pi * 220 * np.arange(SR) / SR) * 12000).astype("<i2")
    with wave.open(str(lp), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.tobytes())
    shots = dict(shots)
    shots["bass"] = [{"name": "deep 808", "path": shots["kick"][0]["path"],
                      "tokens": ["808"]}]
    shots["vox"] = [{"name": "yeah", "path": shots["snap"][0]["path"],
                     "tokens": ["vox"]}]
    shots["_loops"] = [{"name": "shaker 96 bpm", "path": str(lp),
                        "role": "perc", "bpm": 96, "secs": 1.0,
                        "tokens": ["shaker"]}]
    # non-chords beat pinned to 96 so the loop's bpm matches (no drift)
    p, report = beat_machine.generate(["Cutz"], tempo=96, root=root,
                                      shots=shots)
    lanes = beat_recipes.load_recipe(root, int(p.name.split()[0]))["preset"]["lanes"]
    assert {"bass", "vox", "loop"} <= set(lanes), (report, sorted(lanes))
    # the loop plays FULL (spans the whole beat), not a choked hit
    stem_dir = next(d for d in p.parent.glob("* Stems")
                    if d.name.startswith(p.name.split()[0]))
    assert any(f.stem.startswith("loop - ") for f in stem_dir.glob("*.wav"))
    # ...and the notes box can switch them off
    p2, _ = beat_machine.generate(["Cutz"], tempo=96, root=root, shots=shots,
                                  notes="no loop no vox no bass 808")
    lanes2 = beat_recipes.load_recipe(
        root, int(p2.name.split()[0]))["preset"]["lanes"]
    assert not ({"bass", "vox", "loop"} & set(lanes2)), sorted(lanes2)


def test_no_repetition_across_generations(machine_env):
    root, shots = machine_env
    p1, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    p2, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    r1 = beat_recipes.load_recipe(root, int(p1.name.split()[0]))
    r2 = beat_recipes.load_recipe(root, int(p2.name.split()[0]))
    for lane in ("kick", "snare", "hat"):
        assert r1["kit_paths"][lane] != r2["kit_paths"][lane], lane
    # ...and the rendered kick patterns differ (owner call 2026-07-21:
    # the strict >=3-moves policy is gone — different, not far-apart)
    k1 = r1["preset"]["lanes"]["kick"][3]
    k2 = r2["preset"]["lanes"]["kick"][3]
    assert k1 != k2


def test_swap_changes_one_drum_and_nothing_else(machine_env):
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    new_path, report = beat_machine.swap(no, "snare", root=root,
                                         shots=shots)
    # owner rule 2026-07-18: a swapped song and its variations move into
    # one family folder together — the original is MOVED, never lost or
    # overwritten, and both now sit side by side.
    moved = beat_machine.beat_wav(no, root)
    assert new_path.exists()
    assert moved is not None and moved.exists()      # original still there
    assert moved.name == path.name                   # same file, new home
    assert moved.parent == new_path.parent           # living together
    assert new_path.parent.name.endswith("Variations")
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


def test_stem_rack_swaps_several_drums_into_one_rebuild(machine_env):
    """Owner 2026-07-18: staging kick + snare + hat in the stem rack must
    come back as ONE new beat with all three changes, not three beats."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    # one drum he picked by hand, two he left to the machine
    chosen = next(e["path"] for e in shots["kick"]
                  if e["path"] != rec["kit_paths"]["kick"])
    picks = {"kick": chosen, "snare": None, "hat": None}
    before = len(list(root.rglob("*.wav")))
    new_path, _ = beat_machine.swap_many(no, picks, root=root, shots=shots)

    made = [p for p in root.rglob("*.wav")
            if p.name.startswith(f"{int(new_path.name.split()[0])} ")]
    assert len(made) == 1, "one rebuild, one new beat"
    rec2 = beat_recipes.load_recipe(root, int(new_path.name.split()[0]))
    assert rec2["kit_paths"]["kick"] == chosen         # exactly his pick
    for lane in ("snare", "hat"):
        assert rec2["kit_paths"][lane] != rec["kit_paths"][lane], lane
    untouched = {k: v for k, v in rec["kit_paths"].items()
                 if k not in picks}
    assert untouched == {k: v for k, v in rec2["kit_paths"].items()
                         if k not in picks}
    assert rec2["preset"] == rec["preset"]             # pattern still locked
    assert rec2["parent"] == no
    assert before < len(list(root.rglob("*.wav")))     # nothing overwritten


def test_stem_rack_refuses_a_pointless_rebuild(machine_env):
    """Choosing the sample that's already in the lane isn't a change."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    no = int(path.name.split()[0])
    same = beat_recipes.load_recipe(root, no)["kit_paths"]["kick"]
    with pytest.raises(ValueError, match="Nothing to change"):
        beat_machine.swap_many(no, {"kick": same}, root=root, shots=shots)


def test_fixed_bank_never_varies_the_rhythm(machine_env):
    """Owner request 2026-07-21: a control group — five real, well-known
    hip-hop patterns that never change, so a re-roll can only be the
    kit. Same pattern index twice must give the exact same 8-bar kick
    line every time, and the sample-only reroll/remove actions already
    built for the stem rack must work on these recipes too."""
    root, shots = machine_env
    path1, _ = beat_machine.generate_fixed(0, root=root, shots=shots)
    path2, _ = beat_machine.generate_fixed(0, root=root, shots=shots)
    rec1 = beat_recipes.load_recipe(root, int(path1.name.split()[0]))
    rec2 = beat_recipes.load_recipe(root, int(path2.name.split()[0]))
    assert rec1["preset"]["lanes"]["kick"][3] \
        == rec2["preset"]["lanes"]["kick"][3]
    assert rec1["kit_paths"]["kick"] != rec2["kit_paths"]["kick"], \
        "same rhythm, but the kit should still roll fresh"

    no = int(path1.name.split()[0])
    new_path, _ = beat_machine.swap_many(no, {"kick": None}, root=root,
                                         shots=shots)
    rec3 = beat_recipes.load_recipe(root, int(new_path.name.split()[0]))
    assert rec3["preset"]["lanes"]["kick"][3] == rec1["preset"]["lanes"]["kick"][3]
    assert rec3["kit_paths"]["kick"] != rec1["kit_paths"]["kick"]

    no2 = int(new_path.name.split()[0])
    drop_path, _ = beat_machine.swap_many(no2, {}, root=root, shots=shots,
                                          drops=["hat"])
    rec4 = beat_recipes.load_recipe(root, int(drop_path.name.split()[0]))
    assert "hat" not in rec4["kit_paths"]


def test_stem_removal_drops_the_lane_completely(machine_env):
    """Owner 2026-07-21: the rack's remove button — the new beat has no
    trace of the lane (mix, stems folder, or child recipe)."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert "snare" in rec["kit_paths"]

    new_path, _ = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                         drops=["snare"])
    no2 = int(new_path.name.split()[0])
    rec2 = beat_recipes.load_recipe(root, no2)
    assert "snare" not in rec2["kit_paths"]
    assert "snare" not in rec2["kit_spec"]
    assert "snare" not in rec2["preset"]["lanes"]
    assert "No Snare" in new_path.name
    stem_dir = next(new_path.parent.glob(f"{no2} * Stems"))
    assert not [f for f in stem_dir.glob("snare*")]
    # everything else survived
    for lane in rec2["kit_paths"]:
        assert rec2["kit_paths"][lane] == rec["kit_paths"][lane], lane


# ------------------------------------------- per-stem volume (2026-07-19)


def test_stem_volume_trim_lands_on_the_lane_gain(machine_env):
    """Owner 2026-07-19: a fader in the rack must actually move that
    stem. The trim rides the preset's own per-lane gain, so the new
    beat's recipe carries the changed number and nothing else."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    was = rec["preset"]["lanes"]["snare"][1]

    new_path, report = beat_machine.swap_many(
        no, {}, root=root, shots=shots, trims={"snare": -6.0})
    rec2 = beat_recipes.load_recipe(root, int(new_path.name.split()[0]))
    now = rec2["preset"]["lanes"]["snare"][1]

    assert now == pytest.approx(was * 10 ** (-6.0 / 20), rel=1e-6)
    assert rec2["kit_paths"] == rec["kit_paths"]      # no drum changed
    # every other lane's gain untouched
    for lane, spec in rec["preset"]["lanes"].items():
        if lane != "snare":
            assert rec2["preset"]["lanes"][lane][1] == spec[1], lane
    assert "snare -6 dB" in report
    assert "New Mix" in new_path.name


def test_volumes_alone_are_a_valid_rebuild(machine_env):
    """No drum has to change for a remix to be worth printing."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Cutz"], root=root, shots=shots)
    no = int(path.name.split()[0])
    new_path, _ = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                         trims={"kick": 2.5})
    assert new_path.exists()
    assert int(new_path.name.split()[0]) != no       # a NEW beat, not a rewrite
    # same family rule as a drum swap: the original is MOVED in beside it
    moved = beat_machine.beat_wav(no, root)
    assert moved is not None and moved.exists() and moved.name == path.name
    assert moved.parent == new_path.parent


def test_trims_stack_from_how_the_beat_sounds_now(machine_env):
    """The child stores the RESULT, so its own faders start at 0 again
    and a second nudge adds to the first rather than replacing it."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Night Metro"], root=root, shots=shots)
    no = int(path.name.split()[0])
    was = beat_recipes.load_recipe(root, no)["preset"]["lanes"]["hat"][1]
    p2, _ = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                   trims={"hat": 3.0})
    n2 = int(p2.name.split()[0])
    p3, _ = beat_machine.swap_many(n2, {}, root=root, shots=shots,
                                   trims={"hat": 3.0})
    got = beat_recipes.load_recipe(
        root, int(p3.name.split()[0]))["preset"]["lanes"]["hat"][1]
    assert got == pytest.approx(was * 10 ** (6.0 / 20), rel=1e-6)


def test_trim_slider_is_bounded_and_checked(machine_env):
    """Clamped to +/-TRIM_DB, a centred fader is not a change, and a lane
    the beat hasn't got is refused rather than silently ignored."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    preset = crew.normalize_preset(
        beat_recipes.load_recipe(root, no)["preset"])
    clean = beat_machine._clean_trims

    assert clean({"kick": 99}, preset, no) == {"kick": beat_machine.TRIM_DB}
    assert clean({"kick": -99}, preset, no) == {"kick": -beat_machine.TRIM_DB}
    assert clean({"kick": 0}, preset, no) == {}          # centred = no change
    assert clean({"KICK ": "3"}, preset, no) == {"kick": 3.0}   # from the form
    assert clean(None, preset, no) == {}
    for bad in ({"bongo": 3}, {"kick": "loud"}, {"kick": float("nan")}):
        with pytest.raises(ValueError):
            clean(bad, preset, no)
    # sliders all centred is still "nothing staged"
    with pytest.raises(ValueError, match="Nothing to change"):
        beat_machine.swap_many(no, {}, root=root, shots=shots,
                               trims={"kick": 0})


def test_stem_rack_lists_every_drum_with_its_real_sample(machine_env):
    """What the rack shows: each lane, the sample actually behind it, and
    the producer stamp visible but locked."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    stems = beat_machine._beat_stems(no, root=root)
    by_lane = {s["lane"]: s for s in stems}
    assert set(by_lane) >= set(rec["kit_spec"])
    for lane, path_ in rec["kit_paths"].items():
        assert by_lane[lane]["sample"] == Path(path_).stem
        assert by_lane[lane]["stem"] is True        # a solo wav to play
    for lane in rec["stamp_paths"]:
        assert by_lane[lane]["locked"] is True      # tag never swappable
    assert all(not s["locked"] for s in stems
               if s["lane"] in rec["kit_spec"] and s["lane"] != "stamp")


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
            # the loop is no longer always 8 bars (2026-07-22) — check
            # exactly the bars this beat actually renders
            for b in range(crew.bars_of(p)):
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
    # punch list step 7: chords opt-in, plain or via a mood word
    assert pd("with chords please")["chords"] is True
    assert pd("make it dreamy")["chords"] is True
    assert pd("make it dreamy")["chord_feel"] == "dreamy"
    assert pd("")["chords"] is False and pd("")["chord_feel"] is None


def test_chords_direction_adds_a_harmony_layer(machine_env):
    root, shots = machine_env
    path, report = beat_machine.generate(["Otto Grit"], root=root,
                                         shots=shots, notes="dreamy chords")
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    lanes = rec["preset"]["lanes"]
    assert "chord0" in lanes and "bass0" in lanes
    assert "chords: dreamy" in report
    stem_dir = list(path.parent.glob("* Stems"))[0]
    stems = {f.stem for f in stem_dir.glob("*.wav")}
    assert any(s.startswith("chord0") for s in stems)
    assert any(s.startswith("bass0") for s in stems)
    # the chord/bass stems actually carry audio, not silence
    with wave.open(str(next(stem_dir.glob("chord0*.wav"))), "rb") as f:
        frames = f.readframes(f.getnframes())
        assert any(b != 0 for b in frames[:10000])
    # MIDI ships a real polyphonic chords track alongside the drum lanes
    midi = path.with_suffix(".mid").read_bytes()
    assert b"chords" in midi
    assert b"\x99" in midi                # drum lanes still on channel 10


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
