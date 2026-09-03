"""The 2026-07-16 spec features: config file, recipes + swap, MIDI +
stems, sample history, and the 50/50 collab blend."""
import json
import random
import re
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
    # crew_config.json holds the eleven; the Legends live in their own file
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
    # prefix ("kick - <sample>"), never just the generic role.
    #
    # 2026-08-01: this used to require a stem for kick AND snare AND hat.
    # generate() rolls its pattern from an unseeded RNG, so a lane can
    # legitimately come out with no hits in any bar — and since write_stems
    # stopped writing all-zero stems that day, such a lane now has no file
    # instead of a silent one. The old form passed only because the silent
    # file was always there. It is an intermittent failure, not a fixed one:
    # it survived several full-suite runs before showing up.
    #
    # So: the kick must always be there (a beat with no kick is broken), the
    # naming rule is enforced on whatever DID render, and at least two of the
    # three must be present so this cannot pass on an almost-empty beat.
    present = {lane: [s for s in stems if s.startswith(lane)]
               for lane in ("kick", "snare", "hat")}
    assert present["kick"], ("no kick stem", stems)
    assert sum(1 for v in present.values() if v) >= 2, \
        ("beat came out nearly empty", stems)
    for lane, match in present.items():
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
    # "no chords" pins the drums-only context this rule lives in: since
    # chords_default went roster-wide (2026-07-25) a default beat carries
    # harmony's own bassN lanes instead of the static sub — the second
    # half of this test asserts exactly that skip.
    root, shots = machine_env
    assert beat_machine.ADD_THE_ROOT_808, "the rule is off"
    random.seed(1)
    path, report = beat_machine.generate(["Mustang"], root=root, shots=shots,
                                         traditional=True, notes="no chords")
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert rec.get("root_note"), report        # a real musical root
    assert "sub" in rec["preset"]["lanes"]
    stem_dir = next(d for d in path.parent.glob("* Stems")
                    if d.name.startswith(str(no)))
    # the stem is named for what the sound IS: the tuned 808 under the kick
    # is a BASS DRUM, not a "sub" (owner's vocabulary, 2026-07-25)
    assert any(f.stem.startswith("bass drum - synth 808 sub, root")
               for f in stem_dir.glob("*.wav")), list(stem_dir.iterdir())
    # owner 2026-07-23 ("control the volume for all sounds"): a synthesized
    # lane like this one has no sample to swap, so it's not in kit_spec —
    # but it must still show up in the app's stem list with a volume
    # control (locked=True, no swap dropdown, per the existing UI
    # convention for stamps). Before this fix it wasn't listed at all.
    ui_lanes = {s["lane"]: s for s in beat_machine._beat_stems(no, root)}
    assert "sub" in ui_lanes, sorted(ui_lanes)
    assert ui_lanes["sub"]["locked"] is True
    assert ui_lanes["sub"]["stem"] is True     # the solo-play button works too
    path_v, _ = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                       trims={"sub": -4.0})
    assert path_v.exists()                     # a volume-only rebuild works
    # ...and a chords beat skips it on purpose: harmony's own bass owns
    # the low end there, and a static sub under it just fights.
    path2, _ = beat_machine.generate(["Mustang"], root=root, shots=shots,
                                     traditional=True, notes="chords")
    rec2 = beat_recipes.load_recipe(root, int(path2.name.split()[0]))
    assert rec2.get("root_note") is None
    assert "sub" not in rec2["preset"]["lanes"]


def test_rebuild_regenerates_chord_audio_and_stacks_sequential_trims(machine_env):
    # owner 2026-07-23 ("control the volume for all sounds") surfaced this:
    # a chord/bass-chord lane is synthesized, so unlike a real sample lane
    # it has nothing in kit_paths to reload on rebuild. render_crew_beat
    # KeyErrors on the missing kit entry the moment a volume slider is
    # actually moved on one — which only became POSSIBLE once the sibling
    # fix (test_add_the_root_...) made these lanes visible in the app.
    # _build_chords (extracted out of generate()) regenerates the audio
    # deterministically from the recipe's saved `variant`, same trick
    # _root_sub already used for the tuned 808 sub.
    root, shots = machine_env
    random.seed(1)
    # Timberline's chord_source is synth-only — avoids the real-library
    # scan a "loop"/"strings" voice would otherwise need in this test env.
    path, report = beat_machine.generate(["Timberline"], root=root,
                                         shots=shots, notes="chords")
    no = int(path.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    assert "chord0" in rec["preset"]["lanes"], report   # a real chords beat
    # a volume-only rebuild must not crash — this is the bug that was found
    path2, _ = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                      trims={"chord0": 5.0})
    assert path2.exists()
    rec2 = beat_recipes.load_recipe(root, int(path2.name.split()[0]))
    g_c0 = rec2["preset"]["lanes"]["chord0"][1]
    # bass0 never exists (owner 2026-07-29 hard rule: no melodic bassline)
    assert "bass0" not in rec2["preset"]["lanes"]
    # the OPENING level comes from groove.OWNER_TASTE (owner 2026-07-25 —
    # it used to be a flat 0.5, which sat the pad above the hats). Read
    # from the constant so tuning the house mix doesn't look like a
    # broken test.
    base_c = beat_machine._CHORD_GAIN * beat_machine._ACCENTS[0]
    assert g_c0 == pytest.approx(base_c * 10 ** (5 / 20))
    # a SECOND rebuild trimming chord0 again must STACK on round 1, not
    # reset it back to the deterministic default (0.5) — the trap a naive
    # "just regenerate everything from scratch" fix would fall into.
    path3, _ = beat_machine.swap_many(int(path2.name.split()[0]), {},
                                      root=root, shots=shots,
                                      trims={"chord0": 2.0})
    rec3 = beat_recipes.load_recipe(root, int(path3.name.split()[0]))
    assert rec3["preset"]["lanes"]["chord0"][1] == pytest.approx(
        base_c * 10 ** (5 / 20) * 10 ** (2 / 20))


def test_phase2_bass_and_vox_lanes_but_never_a_drum_loop(machine_env, tmp_path,
                                                         monkeypatch):
    # owner phase 2 (2026-07-23): the unlocked bass/808 and vocal samples get
    # real lanes. Force both rolls on (they are <1 by design) and hand the
    # engine a matching pool, so this is deterministic.
    # A drum-loop lane was built the same day and REMOVED on the owner's call
    # ("the drum loops cause problems... there are enough drum sounds"), so a
    # loaded _loops pool must produce NO loop lane. That's asserted below.
    root, shots = machine_env
    monkeypatch.setattr(beat_machine, "SAMPLED_BASS_P", 1.0)
    monkeypatch.setattr(beat_machine, "VOX_LANE_P", 1.0)
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
    # beat pinned to 96 — the bpm the loop pool would have matched, so if a
    # loop lane could ever fire, it would fire here. "no chords" because
    # the sampled-bass lane is by design only for chord-free beats (a
    # chords beat's harmony bassN owns the low end) — and since
    # chords_default went roster-wide (2026-07-25), chord-free is opt-in.
    p, report = beat_machine.generate(["Cutz"], tempo=96, root=root,
                                      shots=shots, notes="no chords")
    no = int(p.name.split()[0])
    rec = beat_recipes.load_recipe(root, no)
    lanes = rec["preset"]["lanes"]
    assert {"bass", "vox"} <= set(lanes), (report, sorted(lanes))
    assert "loop" not in lanes, ("drum loops are excluded", sorted(lanes))
    stem_dir = next(d for d in p.parent.glob("* Stems")
                    if d.name.startswith(p.name.split()[0]))
    stems = {f.stem for f in stem_dir.glob("*.wav")}
    # the sampled 808 under the kick is a BASS DRUM in his vocabulary
    # (2026-07-25) — "bass" on its own is the melodic line
    assert any(s.startswith("bass drum - ") for s in stems), stems
    assert not any(s.startswith("loop - ") for s in stems), stems
    # bug found 2026-07-23 ("a vocal sound... doesn't show up in the stems
    # but is present in the song"): bass/vox rendered real audio but were
    # never registered into the recipe (kit_spec was snapshot before these
    # lanes existed), so the app's stems/swap list never learned about them.
    # Both must be visible AND swappable — not just present in the audio.
    assert {"bass", "vox"} <= set(rec["kit_spec"]), sorted(rec["kit_spec"])
    assert {"bass", "vox"} <= set(rec["kit_paths"]), sorted(rec["kit_paths"])
    ui_lanes = {s["lane"]: s for s in beat_machine._beat_stems(no, root)}
    assert "bass" in ui_lanes and not ui_lanes["bass"]["locked"], ui_lanes
    assert "vox" in ui_lanes and not ui_lanes["vox"]["locked"], ui_lanes
    # the anti-repeat history also needs these lanes attributed, or a bass/
    # vox sample could repeat across beats without tripping the avoid-set
    assert rec["kit_paths"]["bass"] in beat_recipes.history_avoid(["Cutz"])
    assert rec["kit_paths"]["vox"] in beat_recipes.history_avoid(["Cutz"])
    # a SECOND bug found while checking the first: kit_paths must hold the
    # raw file path (matching every other lane — build_kit: `sources[lane]
    # = path`), not a decorated display string ("vox: <name>"). A decorated
    # string still happens to land IN history_avoid (so the check above
    # alone can't catch it — both sides would be wrong the same way), but
    # it breaks a REBUILD, which reloads kit_paths from disk. Assert it's
    # the exact path the picker chose, and that a volume-only rebuild
    # (the actual feature requested) succeeds.
    assert rec["kit_paths"]["bass"] == shots["bass"][0]["path"]
    assert rec["kit_paths"]["vox"] == shots["vox"][0]["path"]
    path3, _ = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                      trims={"bass": 3.0, "vox": -2.0})
    assert path3.exists()
    # ...and the notes box can switch the two real lanes off
    p2, _ = beat_machine.generate(["Cutz"], tempo=96, root=root, shots=shots,
                                  notes="no vox no bass 808")
    lanes2 = beat_recipes.load_recipe(
        root, int(p2.name.split()[0]))["preset"]["lanes"]
    assert not ({"bass", "vox"} & set(lanes2)), sorted(lanes2)


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

def test_gaps_are_possible_but_rare():
    """OWNER RULE 2026-08-01: "the gaps I want to be rare. One in six."

    This test used to assert only that a fully silent bar CAN happen (owner
    2026-07-29, which removed the old 'never a gap' floor). Measured under
    that rule, 47% of beats had a completely silent bar and 90% had a hole
    of some kind — in the drum stems, which is how he works in Reason, 8 of
    12 beats dropped 17-61 dB. So the test now pins BOTH ends: silence is
    still reachable (the 07-29 rule is not being quietly reinstated as a
    floor), and it is rare (the 08-01 rule actually holds).

    Rate is measured over whole beats, not bars, and the band is wide
    because vary_preset rolls per beat — HOLE_P is 1/6, the observed rate
    sits near 11-16%, and the assertions only catch a real drift back to
    'every beat has a hole' or 'gaps are gone entirely'."""
    import copy as _copy
    saw_silence = False
    holed = total = 0
    for name in ("Otto Grit", "Night Metro", "Glass Cat"):
        for v in range(80):
            p = _copy.deepcopy(CREW[name])
            pattern_gen.compose(p, name, v)
            beat_machine.vary_preset(p, v, CREW[name]["num"],
                                     tempo_locked=False)
            backbone = [ln for ln in p["lanes"]
                        if ln in beat_machine.BACKBONE]
            drums = [ln for ln in p["lanes"]
                     if not ln.startswith(("chord", "bass", "stamp"))]
            total += 1
            beat_has_hole = False
            for b in range(crew.bars_of(p)):
                if sum(sum(c != "-" for c in p["lanes"][ln][3][b])
                       for ln in backbone) == 0:
                    saw_silence = True
                if sum(sum(c not in "-." for c in p["lanes"][ln][3][b])
                       for ln in drums) == 0:
                    beat_has_hole = True
            holed += beat_has_hole
    assert saw_silence, "the backbone can no longer go silent at all"
    rate = holed / total
    assert rate < 0.30, "gaps are back to being common: %.0f%%" % (100 * rate)


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
    # bass0 never exists (owner 2026-07-29 hard rule: no melodic bassline)
    assert "chord0" in lanes and "bass0" not in lanes
    assert "chords: dreamy" in report
    stem_dir = list(path.parent.glob("* Stems"))[0]
    stems = {f.stem for f in stem_dir.glob("*.wav")}
    assert any(s.startswith("chord0") for s in stems)
    assert not any(s.startswith("bass0") for s in stems)
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


# ------------------------------------------- the beat remembers its harmony

def test_recipe_records_key_progression_and_chords(machine_env):
    """Packaging step 1 (2026-07-25): a beat on disk used to know its tempo
    and its 808 root but not its key or its chords, so nothing downstream
    could explain it or set up a session to match. The manifest now carries
    the harmony. Timberline is used because his chord_source is synth-only,
    so this doesn't need the real sample drive."""
    import harmony
    from key_context import KeyContext

    root, shots = machine_env
    random.seed(1)
    path, report = beat_machine.generate(["Timberline"], root=root,
                                         shots=shots, notes="chords")
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))

    h = rec["harmony"]
    assert h, report
    for k in ("key", "root", "mode", "progression", "chords", "chord_source"):
        assert k in h, k
    assert h["chords"], "a chords beat must record at least one chord"
    assert rec["lanes"] and "chord0" in rec["lanes"]
    assert "legend" in rec

    # the romans/spellings/notes recorded are the ones harmony.compose gives
    # for this key and progression — compose is deterministic once the
    # progression is named, so this is a real independent recomputation.
    _, expect = harmony.compose(KeyContext(h["root"], h["mode"]),
                                h["progression"])
    got = h["chords"]
    assert [c["roman"] for c in got] == [c["roman"] for c in expect[:len(got)]]
    assert [c["chord"] for c in got] == [c["chord"] for c in expect[:len(got)]]
    assert [c["notes"] for c in got] == [c["notes"] for c in expect[:len(got)]]

    # bars are 1-based and ascending; every chord names the voice that
    # actually sounded it, which is what the "why this works" card reads
    bars = [c["bar"] for c in got]
    assert bars[0] == 1 and bars == sorted(bars)
    assert all(c["voice"] for c in got)
    assert set(h["chord_source"]) == {c["voice"] for c in got}


def test_recipe_never_carries_the_real_producer_name(machine_env):
    """The recipe is a sidecar that travels next to a beat, so it is the one
    file the internal-only `built` attribution must never reach (owner
    decision 2026-07-22). Solo Legend beats leaked it until 2026-07-25."""
    root, shots = machine_env
    random.seed(4)
    # a Legend: CREW carries his real-producer attribution live...
    assert CREW["Timberline"].get("built"), "fixture assumption changed"
    path, _ = beat_machine.generate(["Timberline"], root=root, shots=shots)
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
    # ...and it must not be anywhere in the file that lands on disk.
    assert "built" not in rec["preset"]
    assert CREW["Timberline"]["built"].lower() not in json.dumps(rec).lower()

    # every Legend, without paying for a render each. `built` was only half
    # of it — the research prose in signature["_note"] names producers too,
    # and a built-only strip walked straight past it. Scoped to the Legends
    # because that is what the 2026-07-22 rule covers: the genre identities
    # say what they ARE on purpose, and one of them ("Plug" / "Plugg") is a
    # genre word that a blanket scan reads as a leak.
    assert crew.LEGEND_NAMES, "roster didn't load — this test proves nothing"
    for name in crew.LEGEND_NAMES:
        clean = beat_machine._shareable_preset(CREW[name])
        assert "built" not in clean, name
        blob = json.dumps(clean).lower()
        for real in re.split(r"[/,]| x ", CREW[name].get("built", "")):
            real = real.split("(")[0].strip().lower()
            if len(real) > 3 and real != "no one":
                assert real not in blob, (name, real)


# --------------------------------------- old recipes keep working (step 2)

# A recipe exactly as it was written BEFORE 2026-07-25 — no "harmony", no
# "lanes", no "legend", and `built` still sitting in the preset. Anything
# that reads a recipe has to cope with a file this shape forever, because
# every beat he made up to that date is one.
OLD_RECIPE = {
    "file": "42 Otto Grit Dusty Sunday Drums 88bpm.wav",
    "folder": "Otto Grit", "names": ["Otto Grit"], "title": "Dusty Sunday",
    "variant": 7, "bpm": 88, "space": "room",
    "preset": {"num": 1, "bpm": 88, "built": "J Dilla",
               "lanes": {"kick": [0.0, 1.0, [0, 0, 50, 1], ["X" * 16]],
                         "snare": [0.1, 0.9, [0, 0, 50, 2], ["X" * 16]]},
               "signature": {"_note": "dilla research prose here",
                             "chord_source": [["loop", 3]]}},
    "kit_spec": {"kick": ["kick", "punch", 1.0, 0.4],
                 "snare": ["snare", "crack", 1.0, 0.5]},
    "kit_paths": {"kick": "/lib/k.wav", "snare": "/lib/s.wav"},
    "stamp_paths": {"stamp": "/lib/stamp.wav"}, "stamp_secs": {"stamp": 1.2},
    "root_note": "F", "traditional": False, "dj_cut_bar": None,
    "parent": None, "date": "2026-07-20",
}


@pytest.fixture
def old_beat(tmp_path):
    root = tmp_path / "beats"
    (root / ".recipes").mkdir(parents=True)
    (root / ".recipes" / "42.json").write_text(json.dumps(OLD_RECIPE))
    return root


def test_old_recipes_still_load_and_drive_every_reader(old_beat):
    """Step 2: the step-1 keys are additive, so a beat written before them
    must still work everywhere. Each call below is a real reader in the app
    — a KeyError in any of them is a beat he can no longer swap or open."""
    root = old_beat
    rec = beat_recipes.load_recipe(root, 42)
    assert "harmony" not in rec and "lanes" not in rec   # genuinely old

    assert beat_machine.beat_dj(42, root) == "Otto Grit"
    assert beat_machine._swap_lanes(42, root) == ["kick", "snare"]
    fam, anc = beat_machine._family_dir_for(42, root)
    assert anc == 42 and "Dusty Sunday" in str(fam)
    # the stem rack's lane list: kit_spec lanes + the locked stamp
    rows = beat_machine._beat_stems(42, root)
    assert {r["lane"] for r in rows} >= {"kick", "snare", "stamp"}

    # readers of the NEW keys must find nothing rather than explode — this
    # is the shape step 3's "why this works" card has to survive
    assert rec.get("harmony") is None
    assert rec.get("lanes", []) == []
    assert rec.get("legend") is None


def test_old_recipe_stops_leaking_the_name_the_moment_it_is_rewritten(old_beat):
    """An old recipe on disk still contains `built` and the research prose —
    they can't be unwritten retroactively. What must hold is that anything
    RE-writing one strips them, so a swap of an old beat doesn't carry the
    name into a brand-new file."""
    rec = beat_recipes.load_recipe(old_beat, 42)
    assert rec["preset"]["built"] == "J Dilla"           # the old file, as-is
    clean = beat_machine._shareable_preset(rec["preset"])
    assert "built" not in clean
    assert "_note" not in clean["signature"]
    assert "dilla" not in json.dumps(clean).lower()
    # and the settings that actually drive a rebuild survive the strip
    assert clean["signature"]["chord_source"] == [["loop", 3]]
    assert clean["lanes"]["kick"][1] == 1.0


# ------------------------------------ "why this works" on the card (step 3)

def test_card_theory_reads_the_recipe_and_the_owners_own_words(machine_env):
    """Step 3: pure read-and-display of step 1's data. The plain-English
    line comes from progressions_config.json — the owner's transcription of
    theory/progressions.md — so he can reword any of it without touching
    code, which is the whole reason it isn't a dict in this file."""
    import harmony

    root, shots = machine_env
    random.seed(1)
    path, report = beat_machine.generate(["Timberline"], root=root,
                                         shots=shots, notes="chords")
    no = int(path.name.split()[0])

    th = beat_machine._beat_theory(no, root)
    assert th, report
    h = beat_recipes.load_recipe(root, no)["harmony"]
    assert th["key"] == h["key"]
    # the romans printed are this beat's, in order
    assert th["roman"] == " – ".join(c["roman"] for c in h["chords"])
    # ...and the sentence is the config's, verbatim — not paraphrased here
    assert th["why"] == harmony.PROGRESSIONS[h["progression"]]["why"]
    assert th["progression"] == harmony.PROGRESSIONS[h["progression"]]["label"]


def test_every_progression_has_a_why_line():
    """A progression added later with no `why` would print a card with an
    empty explanation — the one visible feature of this whole step."""
    import harmony
    missing = [k for k, v in harmony.PROGRESSIONS.items() if not v.get("why")]
    assert not missing, missing
    # and none of them smuggles a real producer name onto the card, which
    # a label already does ("Metro Boomin style") and a `why` must not,
    # because step 7 exports this sentence next to the beat
    banned = ("metro boomin", "dr. dre", "still d.r.e", "dilla", "premier",
              "timbaland", "pharrell", "kanye", "lex luger", "three 6")
    for k, v in harmony.PROGRESSIONS.items():
        low = v["why"].lower()
        assert not [b for b in banned if b in low], k


def test_card_theory_is_silent_for_a_beat_that_has_none(old_beat):
    """Old beats, drums-only beats, and beats whose recipe is gone must
    render exactly as they always did — no block, no crash."""
    assert beat_machine._beat_theory(42, old_beat) is None    # pre-step-1
    assert beat_machine._beat_theory(999, old_beat) is None   # no recipe
    # a recipe that HAS the key but with nothing in it (drums-only beat)
    rec = dict(json.loads((old_beat / ".recipes" / "42.json").read_text()),
               harmony=None)
    (old_beat / ".recipes" / "43.json").write_text(json.dumps(rec))
    assert beat_machine._beat_theory(43, old_beat) is None


# ---------------------------- instruments by default, "no chords" to opt out

def test_no_chords_actually_means_no(machine_env):
    """Owner 2026-07-25: every identity now plays its chord voice by
    default (chords_default roster-wide). That made the off-switch load-
    bearing — and exposed that "no chords" used to turn chords ON, because
    the parser saw the word "chords" and ignored the "no"."""
    p = beat_machine.parse_directions
    assert p("")["chords"] is False            # empty box: parser asks nothing
    assert p("chords")["chords"] is True
    for phrase in ("no chords", "without chords", "drop the chords",
                   "drums only", "just drums", "no melody"):
        d = p(phrase)
        assert d["no_chords"] and not d["chords"], phrase
    # a mood word still means chords, and isn't broken by the new check
    assert p("dreamy")["chords"] is True

    # end to end: default ON via signature, OFF when asked
    root, shots = machine_env
    random.seed(2)
    path, report = beat_machine.generate(["Timberline"], root=root,
                                         shots=shots)          # empty notes
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
    assert "chord0" in rec["preset"]["lanes"], report
    assert rec["harmony"], "default-on beat must still record its harmony"
    path2, report2 = beat_machine.generate(["Timberline"], root=root,
                                           shots=shots, notes="no chords")
    rec2 = beat_recipes.load_recipe(root, int(path2.name.split()[0]))
    assert not any(ln.startswith("chord") for ln in rec2["preset"]["lanes"]), \
        report2


def test_every_identity_defaults_to_its_chord_voice():
    """The configs are the contract: all 39 identities with a harmonic
    signature have chords_default on (owner 2026-07-25, 'I no longer hear
    any instruments'). A new identity added without it would silently ship
    drums-only beats again."""
    missing = [n for n, p in CREW.items()
               if isinstance(p.get("signature"), dict)
               and not p["signature"].get("chords_default")]
    assert not missing, missing


# ------------------- one instrument, whole beat, from HIS banks (2026-07-25)

def _tone(note, secs=0.8):
    f = 440.0 * 2 ** ((note - 69) / 12.0)
    t = np.arange(int(secs * SR)) / SR
    return 0.4 * np.sin(2 * np.pi * f * t)


def _inst_index(tmp_path, group, notes):
    """A real on-disk index of tones, so the whole load->shift->tile path
    runs. Coverage is controllable: instrument_sampler.MAX_SHIFT means a
    group only 'covers' notes within 4 semitones of one of its samples."""
    from make_drum_loops import write_wav24
    idx = []
    for n in notes:
        p = tmp_path / ("%s_%d.wav" % (group, n))
        x = _tone(n)
        write_wav24(p, x, x)
        idx.append({"path": str(p), "name": "%s %d" % (group, n), "note": n,
                    "clarity": 0.95, "group": group})
    return idx


@pytest.fixture
def only_his_instruments(tmp_path, monkeypatch):
    """A narrow 'bell' group (one sample, so it covers a 9-semitone window)
    and a wide 'piano' group that covers everything."""
    import instrument_sampler
    bell = _inst_index(tmp_path, "bell", [60])
    piano = _inst_index(tmp_path, "piano", range(36, 85, 3))
    bass = _inst_index(tmp_path, "bass", range(28, 61, 3))
    monkeypatch.setattr(instrument_sampler, "scan", lambda *a, **k: bell + piano)
    monkeypatch.setattr(instrument_sampler, "scan_bass", lambda *a, **k: bass)
    return bell, piano, bass


def _voices_of(rec):
    return [c["voice"] for c in rec["harmony"]["chords"]]


def test_one_instrument_plays_the_whole_beat(machine_env, only_his_instruments,
                                             monkeypatch):
    """Owner 2026-07-25: 'I don't want the instrument to change into a
    different instrument halfway through a beat.' Beat 1174 went strings,
    strings, choir because the old code picked a fallback PER CHORD. The
    voice is now committed for the whole beat before any audio is kept."""
    root, shots = machine_env
    # a wide progression the one-sample 'bell' group cannot cover alone
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["bell", 1]],
        "chords_default": True})
    random.seed(3)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
    voices = _voices_of(rec)
    assert len(voices) > 1, "need a multi-chord beat to prove anything"
    assert len(set(voices)) == 1, (report, voices)   # THE guarantee


def test_a_chord_lane_never_drops_out_mid_beat(machine_env,
                                               only_his_instruments,
                                               monkeypatch):
    """'I don't want them to just pull in and out completely halfway
    through a track.' Every chord in the beat gets a lane, or the beat has
    no chord lane at all — never some-but-not-others."""
    root, shots = machine_env
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["bell", 1]],
        "chords_default": True})
    random.seed(5)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
    n_chords = len(rec["harmony"]["chords"])
    chord_lanes = [ln for ln in rec["lanes"] if ln.startswith("chord")]
    assert len(chord_lanes) in (0, n_chords), (report, sorted(rec["lanes"]))
    assert len(chord_lanes) == n_chords, report      # and here it voiced


def test_chord_bass_line_is_never_rendered(
        machine_env, only_his_instruments, monkeypatch):
    """Owner 2026-07-29 hard rule: the melodic bassline is his to play
    himself, in Reason — never rendered by the generator, even when his
    own bass samples (the only_his_instruments fixture) could voice every
    root in the progression. Supersedes the 2026-07-25 rule this test used
    to check (his samples over a synth sub) — now there's no bass line at
    all, sampled or synthesized."""
    root, shots = machine_env
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["piano", 1]],
        "chords_default": True})
    random.seed(7)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    stem_dir = next(d for d in path.parent.glob("* Stems")
                    if d.name.startswith(path.name.split()[0]))
    bass_stems = [f.name for f in stem_dir.glob("bass*.wav")]
    assert not bass_stems, (report, [f.name for f in stem_dir.glob("*.wav")])
    # the chords still play — only the bass line under them is gone
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
    vf = rec["harmony"]["voice_files"]
    assert not any(k.startswith("bass") for k in vf), vf
    assert any(k.startswith("chord") for k in vf), vf


def test_layering_never_happens_always_one_voice(
        machine_env, only_his_instruments, monkeypatch):
    """Owner 2026-07-29 hard rule (overrides the old 'sometimes stacks
    both, sometimes plays one, rolled per beat' rule): never layered —
    always exactly one instrument voice for the whole beat, even for an
    identity assigned two sounds it could have combined."""
    root, shots = machine_env
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["piano", 1], ["bell", 1]],
        "chords_default": True})
    for seed in range(8):
        random.seed(seed)
        path, _ = beat_machine.generate(["Timberline"], root=root, shots=shots)
        rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
        voices = _voices_of(rec)
        assert len(set(voices)) == 1, voices        # locked, every time
        assert " + " not in voices[0], voices       # never layered


def test_the_rack_never_says_built_from_scratch_over_his_own_samples(
        machine_env, only_his_instruments, monkeypatch):
    """THE bug, owner 2026-07-25: 'where are the real instruments from my
    sound bank? All I have is drums and things you're creating.' The audio
    was already 100% his brass/strings — but chord/bass lanes have no
    kit_paths entry, so the stem rack printed "built from scratch" over
    them and there was no way for him to know otherwise. The label was the
    defect, and it is the only thing he can actually see."""
    root, shots = machine_env
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["piano", 1]],
        "chords_default": True})
    random.seed(11)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    no = int(path.name.split()[0])
    rows = {r["lane"]: r for r in beat_machine._beat_stems(no, root)}
    voiced = [ln for ln in rows if ln.startswith(("chord", "bass"))]
    assert voiced, (report, sorted(rows))
    for ln in voiced:
        r = rows[ln]
        assert r["sample"] != "built from scratch", (ln, r)
        assert "piano_" in r["sample"] or "bass_" in r["sample"], (ln, r)
        assert "synthesised" not in r["why"], (ln, r)
        assert "your library" in r["why"], (ln, r)


def test_nothing_but_chip_is_ever_generated(machine_env, monkeypatch):
    """Owner's hard rule 2026-07-25: 'the only thing I want rendered from
    you is the chip tune pack. All other instruments mine every time.'
    With NO instrument samples available at all, the beat must come back
    with no chord and no bass lane — never a synthesized substitute."""
    import instrument_sampler
    monkeypatch.setattr(instrument_sampler, "scan", lambda *a, **k: [])
    monkeypatch.setattr(instrument_sampler, "scan_bass", lambda *a, **k: [])
    root, shots = machine_env
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["piano", 1]],
        "chords_default": True})
    random.seed(13)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
    lanes = rec["preset"]["lanes"]
    assert not [ln for ln in lanes if ln.startswith("chord")], (report, lanes)
    assert not [ln for ln in lanes if ln.startswith("bass")], (report, lanes)
    stem_dir = next(d for d in path.parent.glob("* Stems")
                    if d.name.startswith(path.name.split()[0]))
    names = " ".join(f.name for f in stem_dir.glob("*.wav"))
    assert "synth bass" not in names, names


# ------------------------- chord stems: one row, removable (owner 7-25) ---

def _rack(no, root):
    return {r["lane"]: r for r in beat_machine._beat_stems(no, root)}


def _chords_beat(root, shots, monkeypatch, seed=21):
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["epic", 1]],
        "chord_source": [["piano", 1]],
        "chords_default": True})
    random.seed(seed)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    return int(path.name.split()[0]), path, report


def test_chords_are_one_removable_row_not_four(machine_env,
                                               only_his_instruments,
                                               monkeypatch):
    """Owner 2026-07-25: 'I should be able to remove the chord stems just
    like I can other stems.' They collapse to ONE row per instrument —
    removing bar 2's chord alone would make it vanish mid-beat, which is
    the drop-out he already ruled out."""
    root, shots = machine_env
    no, path, report = _chords_beat(root, shots, monkeypatch)
    rows = _rack(no, root)
    assert beat_machine.CHORD_FAM in rows, (report, sorted(rows))
    assert not [ln for ln in rows if beat_machine._CHORD_LANE.match(ln)]
    fam = rows[beat_machine.CHORD_FAM]
    assert fam["locked"] is False           # removable...
    # ...and swappable since 2026-08-04, but for an INSTRUMENT, not a file
    assert fam["can_swap"] is True
    assert fam["voices"] is True
    assert len(fam["members"]) > 1, fam     # it really does stand for many
    assert "your library" in fam["why"]


def test_every_offered_chord_instrument_actually_plays(
        machine_env, only_his_instruments, monkeypatch):
    """The chord dropdown may only list instruments that will really
    sound (owner 2026-08-04).

    Built naively this listed all fourteen voices and NONE of them
    landed: nearest() shops per note across a whole group, so a 3-note
    chord drew from two folders and the one-instrument-per-stem rule
    (2026-08-03) threw the plan out — every pick fell through to the
    DJ's own instrument. Measured on beat 1776 mid-build. That is the
    same "I picked a sound and nothing changed" this whole session was
    about, so the menu is filtered to what a single folder can voice and
    the pick is pinned to that folder. This test fails if either half
    regresses: an unplayable voice in the menu, or a listed voice that
    quietly hands back something else."""
    root, shots = machine_env
    no, _p, report = _chords_beat(root, shots, monkeypatch)
    rec = beat_machine.load_recipe(root, no)
    offered = beat_machine._chord_voices(rec)
    assert offered, report
    default = beat_machine._build_chords(
        crew.normalize_preset(rec["preset"]), {}, {}, rec["variant"],
        {"chords": True, "chord_feel": None}, [])[1]
    default_voice = sorted(set((default or {}).get("voice_names", {}).values()))
    landed = []
    for c in offered:
        _m, h = beat_machine._build_chords(
            crew.normalize_preset(rec["preset"]), {}, {}, rec["variant"],
            {"chords": True, "chord_feel": None}, [], voice=c["path"])
        got = sorted(set((h or {}).get("voice_names", {}).values()))
        assert got, f"{c['path']} was offered but voiced nothing"
        landed.append(tuple(got))
    # at least one offered voice must differ from what the DJ picks on its
    # own — otherwise the dropdown is decoration
    assert any(list(g) != default_voice for g in landed), (
        default_voice, landed)


def test_removing_the_chords_row_removes_every_chord_lane(
        machine_env, only_his_instruments, monkeypatch):
    root, shots = machine_env
    no, _p, report = _chords_beat(root, shots, monkeypatch)
    before = beat_machine.load_recipe(root, no)["preset"]["lanes"]
    assert [ln for ln in before if beat_machine._CHORD_LANE.match(ln)], report
    p2, rep2 = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                      drops=[beat_machine.CHORD_FAM])
    rec2 = beat_recipes.load_recipe(root, int(p2.name.split()[0]))
    lanes = rec2["preset"]["lanes"]
    assert not [ln for ln in lanes if beat_machine._CHORD_LANE.match(ln)], \
        (rep2, sorted(lanes))
    # the drums survive, and the file is named for the musical change
    assert "kick" in lanes
    assert "chord0" not in p2.name and "Chords" in p2.name, p2.name


def test_levelling_the_chords_row_moves_every_bar_together(
        machine_env, only_his_instruments, monkeypatch):
    """One row, one fader: a dB nudge has to reach every bar of that
    instrument or the beat would get louder halfway through."""
    root, shots = machine_env
    no, _p, _r = _chords_beat(root, shots, monkeypatch)
    rec = beat_recipes.load_recipe(root, no)
    was = {ln: g for ln, (p, g, f, b) in rec["preset"]["lanes"].items()
           if beat_machine._CHORD_LANE.match(ln)}
    assert len(was) > 1
    p2, _r2 = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                     trims={beat_machine.CHORD_FAM: 4.0})
    rec2 = beat_recipes.load_recipe(root, int(p2.name.split()[0]))
    for ln, before in was.items():
        after = rec2["preset"]["lanes"][ln][1]
        assert after == pytest.approx(before * 10 ** (4 / 20)), ln


def test_the_bass_drum_lane_is_not_swallowed_by_the_chord_bass_family():
    """'bass' with no digit is a REAL drum lane (the phase-2 sampled 808).
    Only bass0/bass1/... belong to the chord family — a startswith() match
    would take the wrong sound out of the beat."""
    assert beat_machine._chord_family("bass") is None
    assert beat_machine._chord_family("bass0") == beat_machine.CHORD_BASS_FAM
    assert beat_machine._chord_family("bassline") is None
    assert beat_machine._chord_family("chord") is None
    assert beat_machine._chord_family("chord12") == beat_machine.CHORD_FAM


def test_harmony_opens_under_the_drums_with_per_bar_dynamics(
        machine_env, only_his_instruments, monkeypatch):
    """Owner 2026-07-25: 'everything starts off the same volume ... it
    sounds loud and crazy.' The chord bass used to open at 0.85 — louder
    than the snare (0.88 is the snare, kick is 1.0) — and the pad at 0.5,
    above the hats. And every bar landed identically."""
    root, shots = machine_env
    no, _p, report = _chords_beat(root, shots, monkeypatch)
    lanes = beat_recipes.load_recipe(root, no)["preset"]["lanes"]
    chords = [g for ln, (p, g, f, b) in lanes.items()
              if beat_machine._CHORD_LANE.match(ln)]
    basses = [g for ln, (p, g, f, b) in lanes.items()
              if beat_machine._CHORD_BASS_LANE.match(ln)]
    kick = lanes["kick"][1]
    # bass0 never exists (owner 2026-07-29 hard rule: no melodic bassline)
    assert chords and not basses, report
    # the harmony sits UNDER the kit, not on top of it
    assert max(chords) < kick, (max(chords), kick)
    assert max(chords) <= beat_machine._CHORD_GAIN + 1e-9
    # ...and every chord opens at the SAME level. This used to assert the
    # opposite — that the bars "breathe" — which was the 2026-07-25 fix for
    # "everything starts off the same volume ... it sounds loud and crazy".
    # That complaint was about the harmony being too LOUD, and the fix bundled
    # a per-bar accent cycle in with the level drop. Owner 2026-08-03, after
    # hearing beat 1761: "I don't like how the samples get louder and quieter
    # like this one. Let's keep those at a steady volume." The level drop
    # stays (asserted above); the accent cycle is gone.
    # NOTE this is the STARTING level only — each chord still decays across
    # its own length, which he asked for and confirmed separately.
    assert len(set(round(g, 6) for g in chords)) == 1, chords
    assert chords[0] == pytest.approx(beat_machine._CHORD_GAIN)


# ---- kick drum / bass drum / bass are three separate sounds (2026-07-25)


def test_the_three_low_sounds_never_share_a_word():
    """His exact distinction: a KICK DRUM, a BASS DRUM (the 808 boom under
    it) and the BASS (the melodic line) are three things. "bass drum" used
    to be a plain synonym for the kick here, so typing it changed the
    wrong sound; "no bass" killed the 808 rather than the line."""
    assert beat_machine.parse_directions("no bass drum")["mute"] == {"bass"}
    assert beat_machine.parse_directions("no bass")["mute"] == {"chordbass"}
    assert beat_machine.parse_directions("no kick")["mute"] == {"kick"}
    # and the longest phrase wins: "no bass drum" contains "no bass", which
    # used to take the bass line out at the same time
    assert "chordbass" not in beat_machine.parse_directions(
        "no bass drum")["mute"]
    assert "kick" not in beat_machine.parse_directions("no bass drum")["mute"]


def test_lane_labels_say_which_low_sound_it_is():
    assert beat_recipes.lane_label("kick") == "kick drum"
    assert beat_recipes.lane_label("bass") == "bass drum"   # the 808 boom
    assert beat_recipes.lane_label("sub") == "bass drum"    # tuned root
    assert beat_recipes.lane_label("hat") == "hat"          # unchanged


def test_muting_the_bass_drum_leaves_the_bass_line_alone():
    """apply_directions groups by FAMILY, not by stripping digits — bass0
    is the bass line, `bass` is the 808 drum, and they must not move
    together."""
    preset = {"lanes": {"kick": 1, "bass": 1, "bass0": 1, "bass1": 1,
                        "chord0": 1},
              "kit": {}, "space": ("dry", []), "sidechain": 0.5,
              "_guests": ()}
    dirs = dict(beat_machine.parse_directions("no bass drum"),
                kick=None, density=None, space=None, swing=None, tsig=None)
    beat_machine.apply_directions(preset, dirs)
    assert "bass" not in preset["lanes"]                    # the 808 went
    assert {"bass0", "bass1", "kick"} <= set(preset["lanes"])   # these stayed


# ---- one stem per instrument (2026-07-25)


def test_two_layered_instruments_are_two_rows_not_one():
    """A two-sound chord plan is two real instruments, so it gets two rack
    rows, two stems and two volumes — never one 'chords' blob."""
    lanes = ["kick", "chord0", "chord1", "chord0v1", "chord1v1",
             "bass0", "bass1"]
    rows = sorted({beat_machine._chord_family(ln) for ln in lanes} - {None},
                  key=beat_machine._fam_sort)
    assert rows == ["chords", "chords2", "chordbass"]
    # and each row owns only its own instrument's lanes
    assert beat_machine._family_members("chords", lanes) == ["chord0", "chord1"]
    assert beat_machine._family_members("chords2", lanes) == ["chord0v1",
                                                              "chord1v1"]
    assert beat_machine._family_members("chordbass", lanes) == ["bass0",
                                                                "bass1"]
    # the 808 bass DRUM is not swallowed by the bass line's family
    assert beat_machine._chord_family("bass") is None


def test_levelling_one_instrument_moves_only_its_own_lanes():
    preset = {"lanes": {ln: 1 for ln in
                        ("kick", "chord0", "chord1", "chord0v1", "bass0")}}
    out = beat_machine._clean_trims({"chords2": -3}, preset, 1)
    assert out == {"chord0v1": -3.0}          # the second instrument only
    out = beat_machine._clean_trims({"chords": 2}, preset, 1)
    assert out == {"chord0": 2.0, "chord1": 2.0}


# ---- stems preview at track volume (2026-07-25)


def test_stems_print_at_track_volume():
    """He asked for the +6 dB print to go: a stem must be the same volume
    it is in the track, so previewing one tells him the truth."""
    assert beat_recipes.STEM_BOOST_DB == 0.0


def test_wav24_round_trips(tmp_path):
    from make_drum_loops import read_wav24, write_wav24
    t = np.linspace(0, 1, SR, endpoint=False)
    L, R = 0.7 * np.sin(2 * np.pi * 220 * t), 0.3 * np.sin(2 * np.pi * 330 * t)
    p = tmp_path / "x.wav"
    write_wav24(p, L, R)
    l2, r2 = read_wav24(p)
    assert np.abs(l2 - L).max() < 1e-5        # 24-bit quantisation only
    assert np.abs(r2 - R).max() < 1e-5


def _preview(no, root, shots, **q):
    """Drive /mix the way the page does: a query string in, bytes out."""
    from urllib.parse import urlencode, parse_qs
    qs = urlencode({"no": no, "trims": "", "drop": "", "picks": "", **q})
    return beat_machine._preview_render(qs, parse_qs(qs), shots=shots,
                                        root=root)


def test_preview_hears_a_volume_change_before_the_rebuild(machine_env):
    """Nudge a stem, hit play, and the track reflects it — without
    printing a new beat (owner 2026-07-25)."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    quiet = _preview(no, root, shots, trims="kick:-24")
    gone = _preview(no, root, shots, drop="kick")
    assert quiet != gone                       # both did something, differently


def test_preview_matches_what_rebuild_would_print(machine_env):
    """The preview has to BE the rebuild, not an approximation of it.

    It used to sum the printed stems, which is the beat before the master
    bus — measured 8 dB under the real output on beat 1774, so every
    level move was judged against the wrong mix (owner 2026-08-04)."""
    from make_drum_loops import wav24_bytes
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    heard = _preview(no, root, shots, trims="kick:-6")
    L, R = beat_machine.swap_many(no, {}, root=root, shots=shots,
                                  trims={"kick": -6.0}, render_only=True)
    assert heard == wav24_bytes(L, R)          # byte-for-byte, not close


def test_solo_stem_plays_at_its_level_in_the_track(machine_env):
    """The stems are printed with a shared -6 dBFS gain, so soloing one
    used to play it well under its level in the beat. _track_gain undoes
    exactly that shared gain."""
    root, shots = machine_env
    path, _ = beat_machine.generate(["Glass Cat"], root=root, shots=shots)
    no = int(path.name.split()[0])
    beat_machine._TRACK_GAIN.pop(no, None)
    g = beat_machine._track_gain(no, root)
    # applying it to the summed stems lands on the finished beat's LOUDNESS
    from make_drum_loops import read_wav24
    folder = beat_machine._stems_dir(no, root)
    L = R = None
    for f in sorted(folder.glob("*.wav")):
        sL, sR = read_wav24(f)
        if L is None:
            L, R = sL, sR
        else:
            n = min(len(L), len(sL))
            L, R = L[:n] + sL[:n], R[:n] + sR[:n]
    tL, tR = read_wav24(beat_machine.beat_wav(no, root))
    scaled = beat_machine._rms(L * g, R * g)
    track = beat_machine._rms(tL, tR)
    # within a quarter of a dB of the track — an ear can't hear that.
    # How BIG the correction is depends on how hard the master chain
    # worked on this particular beat (about -4.8 dB on a real one, near
    # zero on these synthetic test samples), so only the match is
    # asserted, never the size.
    assert abs(20 * np.log10(scaled / track)) < 0.25


def test_every_rack_row_can_be_previewed(machine_env, only_his_instruments,
                                         monkeypatch):
    """Owner 2026-07-25: "some of the stems do not let me click and preview
    them." The harmony rows stand for several lanes (chord0, chord1, …), so
    their play button asks for "chords" — a name no stem file has. Soloing
    a row sums its lanes instead of reaching for one file."""
    root, shots = machine_env
    no, path, report = _chords_beat(root, shots, monkeypatch)
    rows = beat_machine._beat_stems(no, root=root)
    assert any(r["lane"] == beat_machine.CHORD_FAM for r in rows), report
    for r in rows:
        if not r["stem"]:
            continue
        got = beat_machine._solo_audio(no, r["lane"], root=root)
        assert got is not None, ("row will not play", r["lane"])
        L, R = got
        assert len(L) and float(np.abs(L).max() + np.abs(R).max()) > 0, r["lane"]
    # a made-up row still refuses, rather than serving something wrong
    assert beat_machine._solo_audio(no, "nonsense", root=root) is None


def test_soloing_an_instrument_plays_all_of_its_chords(machine_env,
                                                       only_his_instruments,
                                                       monkeypatch):
    """A harmony row is one instrument across the whole beat, so its
    preview is longer/fuller than any single chord lane of it."""
    root, shots = machine_env
    no, path, report = _chords_beat(root, shots, monkeypatch)
    rec = beat_recipes.load_recipe(root, no)
    members = beat_machine._family_members(beat_machine.CHORD_FAM,
                                           rec["preset"]["lanes"])
    if len(members) < 2:
        pytest.skip("this beat only has one chord slot")
    whole = beat_machine._solo_audio(no, beat_machine.CHORD_FAM, root=root)
    one = beat_machine._solo_audio(no, members[0], root=root)
    assert beat_machine._rms(*whole) > beat_machine._rms(*one)


# ---- separate melodic PARTS instead of one stack (2026-07-25) ----
# Owner: "there should be individual instruments or loops, not everything
# stacked on top of each other, playing the same thing. I wanted one or
# two samples at a time, playing melody, up to three. but those parts
# should be completely separate." theory/arrangement.md is the rulebook;
# these tests hold the code to it.


def test_split_chord_roles_never_repeats_a_note():
    """The whole fix in one assertion: every original chord tone is
    handed to exactly one role — support, lead, or passing, never two —
    on a triad, a 7th chord, and a 9th chord."""
    for notes in ([48, 51, 55], [48, 51, 55, 58], [48, 51, 55, 58, 62]):
        support, lead, passing = beat_machine._split_chord_roles(notes)
        # lead/passing are transposed up an octave/two (rule 1, register
        # separation) — undo that to compare against the original chord
        rebuilt = sorted(support + [n - 12 for n in lead] +
                         [n - 24 for n in passing])
        assert rebuilt == sorted(notes), (notes, support, lead, passing)


def test_lead_and_passing_sit_above_support():
    """Rule 1 from arrangement.md, "different heights", made literal: a
    part that shares support's register isn't a separate part, just a
    relabeled one. Support keeps the chord's own octave; lead moves up
    one octave, passing up two — clear of support's span, not inside it."""
    support, lead, passing = beat_machine._split_chord_roles(
        [48, 51, 55, 58, 62])          # a 9th chord: root,3rd,5th,7th,9th
    assert min(lead) > max(support)
    assert min(passing) > max(lead)


def test_split_chord_roles_leaves_lead_empty_on_a_power_chord():
    """A bare root+5th (quality '5') has nothing left to split off — the
    caller reads an empty lead as 'this chord can't be multi-part' and
    falls back to one part, not a silent lead lane."""
    support, lead, passing = beat_machine._split_chord_roles([48, 55])
    assert support == [48, 55]
    assert lead == [] and passing == []


def test_role_sources_prefers_distinct_instruments_but_never_fails():
    order = ["piano", "wood", "synth"]
    # the identity owns two real voices -> support and lead get different
    # ones
    assert beat_machine._role_sources("piano", order, ["piano", "wood"], 2) \
        == ["piano", "wood"]
    # only one real voice -> the SAME instrument voices both roles (a
    # pianist's two hands, not a degraded case — see the docstring)
    assert beat_machine._role_sources("piano", order, ["piano"], 2) \
        == ["piano", "piano"]
    # "loop" and "chip" never fill a role even if the identity owns them
    assert beat_machine._role_sources(
        "piano", order + ["loop"], ["piano", "loop"], 2) == ["piano", "piano"]


@pytest.fixture
def two_real_instruments(tmp_path, monkeypatch):
    """Two REAL, wide, distinct instrument groups (not the narrow 'bell'
    only_his_instruments uses) — wide enough that an octave-shifted lead
    or passing note is still comfortably coverable, so a multi-part plan
    has a fair chance to succeed rather than fail on register alone."""
    import instrument_sampler
    piano = _inst_index(tmp_path, "piano", range(24, 97, 2))
    wood = _inst_index(tmp_path, "wood", range(24, 97, 2))
    monkeypatch.setattr(instrument_sampler, "scan",
                        lambda *a, **k: piano + wood)
    monkeypatch.setattr(instrument_sampler, "scan_bass", lambda *a, **k: [])
    return piano, wood


def _two_part_beat(root, shots, monkeypatch, seed=0, progression="epic"):
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [[progression, 1]],
        "chord_source": [["piano", 1], ["wood", 1]],
        "chords_default": True})
    random.seed(seed)
    path, report = beat_machine.generate(["Timberline"], root=root, shots=shots)
    return int(path.name.split()[0]), path, report


def test_never_more_than_one_melodic_part(
        machine_env, two_real_instruments, monkeypatch):
    """Owner 2026-07-29 hard rule (overrides the 2026-07-25 'up to three
    parts' rule the three tests below this one used to check): exactly
    one melodic voice, always — no stacking, no passing note, ever.
    Sweeps the exact seeds/progressions that used to land on 2 parts
    (seed 0, epic) and 3 parts (seeds 29 and 34, plugg_dream_9) to prove
    the old weighted roll can no longer produce either."""
    root, shots = machine_env
    for seed, progression in ((0, "epic"), (29, "plugg_dream_9"),
                              (34, "plugg_dream_9")):
        no, path, report = _two_part_beat(root, shots, monkeypatch,
                                          seed=seed, progression=progression)
        rec = beat_recipes.load_recipe(root, no)
        lanes = rec["preset"]["lanes"]
        ch_lanes = sorted(l for l in lanes if l.startswith("chord"))
        fams = sorted({beat_machine._chord_family(l) for l in ch_lanes}
                      - {None})
        # NO chord lane at all is a valid outcome since 2026-08-03: the
        # owner's one-instrument-per-stem rule drops the lane rather than
        # voicing a chord from two instruments, and he confirmed "stick
        # with the new rule where every beat does not have to have a chord
        # lane". What must never happen is TWO melodic families in one
        # beat — that is what this test is for, and it still checks it.
        assert fams in ([], ["chords"]), (seed, report, ch_lanes)


def test_loops_always_play_alone(machine_env, monkeypatch):
    """Owner 2026-07-25, answering directly: 'Loops play alone.' A loop
    is already a finished melody; it must never combine with a second
    instrument, no matter how the part-count roll lands."""
    root, shots = machine_env
    monkeypatch.setitem(CREW["Timberline"], "signature", {
        "key": {"roots": ["C"], "mode": "minor"},
        "progressions": [["dreamy", 1]],
        "chord_source": [["loop", 1]],
        "chords_default": True})
    for seed in range(6):
        random.seed(seed)
        path, report = beat_machine.generate(["Timberline"], root=root,
                                             shots=shots)
        no = int(path.name.split()[0])
        rec = beat_recipes.load_recipe(root, no)
        lanes = rec["preset"]["lanes"]
        fams = {beat_machine._chord_family(l) for l in lanes
               if l.startswith("chord")} - {None}
        assert fams <= {"chords"}, (seed, report, sorted(lanes))


# passing-note tests (seeds 29 and 34, 9th-chord progression) folded into
# test_never_more_than_one_melodic_part above — there's no passing part to
# test any more, owner 2026-07-29 hard rule.
