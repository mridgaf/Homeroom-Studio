"""Song Sketch: synthetic stems only - no beats rendered, no drive needed."""
import json
import zipfile

import numpy as np
import pytest

import song_sketch
import song_sketch_dsp as dsp
from make_drum_loops import SR, read_wav24

BPM = 120
BAR = int(SR * 4 * 60 / BPM)          # one bar of audio


def _loop(freq, bars=2):
    t = np.arange(BAR * bars) / SR
    x = (0.3 * np.sin(2 * np.pi * freq * t)).astype(np.float32)
    return x, x.copy()


ROWS = [{"lane": "kick", "label": "kick drum", "stem": True},
        {"lane": "sub", "label": "808", "stem": True},
        {"lane": "chord0", "label": "horns stack", "stem": True},
        {"lane": "stamp", "label": "producer tag", "stem": True},
        {"lane": "snare", "label": "snare", "stem": False}]


def test_rows_for_drops_tag_and_missing_stems_and_guesses_roles():
    got = {r["lane"]: r["role"] for r in song_sketch.rows_for(ROWS)}
    assert got == {"kick": "drums", "sub": "bass", "chord0": "music"}


def test_build_stems_sum_to_mix_and_files_exist(tmp_path):
    rows = song_sketch.rows_for(ROWS)
    audio = {"kick": _loop(60), "sub": _loop(45), "chord0": _loop(440)}
    recipe = {"section_bars": 2, "amount": 0.6,
              "sections": [{"scene": "intro", "move": "bloom"},
                           {"scene": "pocket", "move": "echo"},
                           {"scene": "break", "move": "breath"},
                           {"scene": "full", "move": "none"}]}
    got = song_sketch.build(7, BPM, rows, audio.get, recipe, root=tmp_path)
    folder = tmp_path / got["id"]
    for name in ("sketch.wav", "original.wav", "stems-and-mix.zip", "recipe.json"):
        assert (folder / name).is_file()
    mL, mR = read_wav24(folder / "sketch.wav")
    sL = sum(read_wav24(f)[0] for f in sorted((folder / "stems").glob("*.wav")))
    assert np.max(np.abs(mL - sL)) < 1e-4          # stems add back to the mix
    assert np.isfinite(mL).all() and np.max(np.abs(mL)) < 10 ** (-0.9 / 20)
    assert len(list((folder / "stems").glob("*.wav"))) == 4   # 3 + transitions
    assert "recipe.json" in zipfile.ZipFile(folder / "stems-and-mix.zip").namelist()
    assert json.loads((folder / "recipe.json").read_text())["beat"] == 7
    # the intro scene silences drums and bass: kick stem is empty in section 1
    kick = read_wav24(next((folder / "stems").glob("01 *.wav")))[0]
    assert np.max(np.abs(kick[: 2 * BAR])) < 1e-6


def test_bad_recipe_is_refused(tmp_path):
    rows = song_sketch.rows_for(ROWS)
    bad = {"section_bars": 4, "sections": [{"scene": "nope", "move": "none"}] * 4}
    with pytest.raises(ValueError):
        song_sketch.build(7, BPM, rows, lambda ln: _loop(100), bad, root=tmp_path)
    assert not list(tmp_path.iterdir())            # nothing half-written


def test_file_path_only_serves_known_names_and_ids(tmp_path):
    d = tmp_path / "Beat 7 2026-10-16 12.00.00"
    d.mkdir()
    (d / "sketch.wav").write_bytes(b"x")
    ok = song_sketch.file_path("Beat 7 2026-10-16 12.00.00", "sketch.wav", tmp_path)
    assert ok == d / "sketch.wav"
    assert song_sketch.file_path("../etc", "sketch.wav", tmp_path) is None
    assert song_sketch.file_path("Beat 7 2026-10-16 12.00.00", "../x", tmp_path) is None
    assert song_sketch.file_path("Beat 7 2026-10-16 12.00.00", "recipe.json", tmp_path) is None


# ---- 2:30 song: many sections, many moves ---------------------------------

def _channels(bpm, bars=2):
    n = int(SR * 4 * 60 / bpm) * bars
    t = np.arange(n) / SR
    mk = lambda f: (lambda x: (x, x.copy()))((0.3 * np.sin(2 * np.pi * f * t)).astype(np.float32))
    return {k: {"dry": mk(f), "sr": SR} for k, f in
            (("kick", 60), ("sub", 45), ("chord0", 440), ("air", 2000))}


@pytest.mark.parametrize("move", [m for m in dsp.MOVES if m != "none"])
def test_every_move_renders_clean_and_stems_sum(move):
    ch = _channels(120)
    recipe = {"bpm": 120, "section_bars": 2, "amount": 0.6, "sections": [
        {"scene": "full", "moves": [move]}, {"scene": "full", "moves": []}]}
    stems, mix, _, meta = dsp.render(ch, recipe)
    assert np.isfinite(mix).all() and np.max(np.abs(mix)) < 10 ** (-0.9 / 20)
    assert np.max(np.abs(sum(stems.values()) - mix)) < 1e-4
    # no click: biggest sample-to-sample jump stays small for 0.3-amp tones
    assert np.max(np.abs(np.diff(mix, axis=0))) < 0.5


def test_song_150_is_two_and_a_half_minutes_and_edits_survive():
    plan = dsp.PRESETS["song_150"]
    assert len(plan["scenes"]) == 7 and plan["bars"] == 8
    ch = _channels(90)
    secs = [{"scene": s, "moves": m} for s, m in zip(plan["scenes"], plan["moves"])]
    stems, mix, _, meta = dsp.render(ch, {"bpm": 90, "section_bars": 8, "amount": 0.6,
                                          "sections": secs})
    assert 145 <= meta["music_duration_s"] <= 155
    assert np.max(np.abs(sum(stems.values()) - mix)) < 1e-4
    assert len(meta["sections"]) == 7


def test_auto_plans_follow_the_producer_rules():
    plans = dsp.auto_plans()
    assert plans == dsp.auto_plans() and len({str(p) for p in plans}) > 6
    for plan in plans:
        assert [s["scene"] for s in plan] == [t[0] for t in dsp.TEMPLATE]
        assert all(len(s["moves"]) <= 2 for s in plan)
        ends = [s["moves"][-1] for s in plan[:-1]]
        assert all(a != b for a, b in zip(ends, ends[1:]))   # no back-to-back repeat
        assert plan[-1]["moves"] in ([], ["phase"], ["drift"])


def test_old_single_move_recipes_still_validate_and_too_long_is_refused():
    ok = dsp.validate_recipe({"bpm": 120, "section_bars": 2,
                              "sections": [{"scene": "full", "move": "echo"}]}, ["a"])
    assert ok["sections"][0]["moves"] == ["echo"]
    with pytest.raises(ValueError):
        dsp.validate_recipe({"bpm": 60, "section_bars": 8,
                             "sections": [{"scene": "full", "moves": []}] * 8}, ["a"])


@pytest.mark.parametrize("key", list(dsp.TEMPLATES))
def test_every_sketch_type_is_a_valid_distinct_song(key):
    preset = dsp.PRESETS[key]
    n = len(preset["scenes"])
    assert preset["auto"] and 5 <= n <= 12 and n * preset["bars"] * 240 / 90 <= 180
    for plan in dsp.auto_plans(key=key):
        assert plan[-1]["moves"] in ([], ["phase"], ["drift"])
        ends = [s["moves"][-1] for s in plan[:-1]]
        assert all(a != b for a, b in zip(ends, ends[1:]))
    secs = [{"scene": s, "moves": m} for s, m in zip(preset["scenes"], preset["moves"])]
    stems, mix, _, meta = dsp.render(_channels(120), {"bpm": 120, "section_bars": 1, "amount": 0.6,
                                                      "sections": secs})
    assert len(meta["sections"]) == n
    assert np.max(np.abs(sum(stems.values()) - mix)) < 1e-4
    assert np.max(np.abs(mix)) < 10 ** (-0.9 / 20)


def test_the_five_types_differ():
    shapes = {(len(p["scenes"]), p["bars"]) for k, p in dsp.PRESETS.items() if p.get("auto")}
    assert len(shapes) == 5


# ---- per-lane moves ---------------------------------------------------------

def _stems4():
    return [{"lane": k, "role": dsp.guess_role(k), "kind": dsp.guess_kind(k)}
            for k in ("kick", "sub", "chord0", "air")]


def test_a_move_on_one_lane_leaves_the_other_lanes_untouched():
    ch = _channels(120)
    base = {"bpm": 120, "section_bars": 2, "amount": 0.6}
    plain, _, _, m1 = dsp.render(ch, {**base, "sections": [{"scene": "full", "lanes": {}}]})
    moved, mix, _, m2 = dsp.render(ch, {**base, "sections": [
        {"scene": "full", "lanes": {"chord0": ["drift"]}}]})
    g1, g2 = 10 ** (m1["gain_db"] / 20), 10 ** (m2["gain_db"] / 20)   # the one shared safety gain
    for lane in ("kick", "sub", "air"):
        assert np.allclose(plain[lane] / g1, moved[lane] / g2, rtol=1e-3, atol=1e-5)   # not touched at all
    assert not np.allclose(plain["chord0"], moved["chord0"])
    assert np.max(np.abs(moved["chord0"][:, 0] - moved["chord0"][:, 1])) > 0.01   # it panned
    assert np.max(np.abs(sum(moved.values()) - mix)) < 1e-4


def test_two_lanes_with_the_same_move_do_not_move_in_lockstep():
    ch = _channels(120)
    ch["air"]["dry"] = ch["chord0"]["dry"]                      # identical audio
    stems, *_ = dsp.render(ch, {"bpm": 120, "section_bars": 2, "amount": 0.6, "sections": [
        {"scene": "full", "lanes": {"chord0": ["drift"], "air": ["drift"]}}]})
    assert not np.allclose(stems["chord0"], stems["air"] / 0.7 * 1.0, atol=1e-3)


def test_lane_habits_and_spotlight_in_auto_plans():
    stems = _stems4() + [{"lane": f"hat{i}", "role": "drums", "kind": "hat"} for i in range(4)]
    for key in dsp.TEMPLATES:
        for seed in range(12):
            plan = dsp.auto_lane_plan(seed, key, stems)
            for sec in plan:
                levels = dsp.SCENES[sec["scene"]]["levels"]
                for lane, moves in sec["lanes"].items():
                    st = next(s for s in stems if s["lane"] == lane)
                    assert levels[dsp.ROLES.index(st["role"])] > 0          # never an inaudible lane
                    assert all(m in dsp.HABITS[st["kind"]] for m in moves)  # kick/bass never panned etc.
                assert len(sec["lanes"]) <= 4                                # spotlight, not everyone
    # not every lane is hit in every section
    assert any(len(s["lanes"]) < len(stems) for s in dsp.auto_lane_plan(0, "song_150", stems))


def test_lane_recipe_is_validated_and_options_carry_lane_plans():
    with pytest.raises(ValueError):
        dsp.validate_recipe({"bpm": 120, "section_bars": 2,
                             "sections": [{"scene": "full", "lanes": {"ghost": ["drift"]}}]}, ["a"])
    opts = song_sketch.options(song_sketch.rows_for(ROWS))
    assert set(opts["plans"]) == set(dsp.TEMPLATES)
    assert all("lanes" in sec for sec in opts["plans"]["song_150"][0])
    assert opts["scenes"]["full"]["levels"] == dsp.SCENES["full"]["levels"]
