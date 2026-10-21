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
    # a whole song (owner 2026-10-21: 2:30-4:00): 10 x 8 bars at 120 = 2:40
    recipe = {"section_bars": 8, "amount": 0.6,
              "sections": [{"scene": "intro", "move": "bloom"},
                           {"scene": "pocket", "move": "echo"},
                           {"scene": "break", "move": "breath"}]
                          + [{"scene": "full", "move": "none"}] * 7}
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
    assert np.max(np.abs(kick[: 8 * BAR])) < 1e-6


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


def test_old_single_move_recipes_still_validate_and_too_long_is_refused():
    ok = dsp.validate_recipe({"bpm": 120, "section_bars": 2,
                              "sections": [{"scene": "full", "move": "echo"}]}, ["a"])
    assert ok["sections"][0]["moves"] == ["echo"]
    with pytest.raises(ValueError):
        dsp.validate_recipe({"bpm": 60, "section_bars": 8,
                             "sections": [{"scene": "full", "moves": []}] * 8}, ["a"])


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


# ---- six arrangement types, genres, 4-bar cuts, drum variations (2026-10-21)

def _drum_stems():
    return [{"lane": k, "role": dsp.guess_role(k), "kind": dsp.guess_kind(k)}
            for k in ("kick", "snare", "hat", "perc", "shaker", "sub", "chord0", "air")]


def test_there_are_six_types_and_six_genres():
    assert len(dsp.TYPES) == 6 and len(dsp.GENRES) == 6
    assert len({str(t["head"] + t["body"] + t["tail"]) for t in dsp.TYPES.values()}) == 6


@pytest.mark.parametrize("bpm", [40, 60, 75, 90, 110, 140, 170, 200])
@pytest.mark.parametrize("key", list(dsp.TYPES))
def test_every_type_is_a_whole_song_at_any_tempo(key, bpm):
    form = dsp.type_form(key, bpm)
    secs = sum(s["bars"] for s in form) * 240 / bpm
    assert dsp.SONG_MIN <= secs <= dsp.SONG_MAX and len(form) <= 40
    assert all(s["bars"] in (4, 8) and s["half"] in (None, "front", "back") for s in form)


@pytest.mark.parametrize("key", list(dsp.TYPES))
def test_every_plan_validates_follows_habits_and_skips_muted_lanes(key):
    stems = _drum_stems()
    lanes = [s["lane"] for s in stems]
    for fx in [None, *dsp.GENRES, *dsp.STYLES]:
        plan = dsp.type_plan(0, key, 90, stems, fx)
        assert plan == dsp.type_plan(0, key, 90, stems, fx)              # same every time
        clean = dsp.validate_recipe({"bpm": 90, "sections": plan}, lanes)
        assert len(clean["sections"]) == len(plan)
        assert len(plan[-1]["moves"]) <= 1                             # the ending carries nothing on
        for sec in plan:
            levels = dsp.SCENES[sec["scene"]]["levels"]
            for lane, moves in sec["lanes"].items():
                st = next(s for s in stems if s["lane"] == lane)
                assert lane not in sec["mute"]                          # a lane sitting out gets no effect
                assert levels[dsp.ROLES.index(st["role"])] > 0
                assert all(m in dsp.HABITS[st["kind"]] for m in moves)


def test_genres_give_different_effects():
    stems = _drum_stems()
    used = {g: {m for seed in range(3) for s in dsp.type_plan(seed, "radio", 90, stems, g)
                for m in s["moves"]} for g in dsp.GENRES}
    assert len({frozenset(v) for v in used.values()}) == 6
    assert "pump" in used["trap"] and "phase" in used["dub"]


def test_drum_variations_rotate_and_keep_the_core():
    stems = _drum_stems()
    form = [{"drums": d} for d in ("thin", "thin", "thin", "core", "kick", "hats", "all")]
    mutes = dsp.drum_mutes(form, stems)
    assert mutes[0] != mutes[1] != mutes[2] and all(len(m) == 1 for m in mutes[:3])
    assert set(mutes[3]) == {"hat", "perc", "shaker"}                # kick + snare only
    assert set(mutes[4]) == {"snare", "hat", "perc", "shaker"}       # kick only
    assert mutes[5] == ["kick"] and mutes[6] == []
    assert not any(m in ("sub", "chord0", "air") for mu in mutes for m in mu)   # drums only


def test_front_and_back_halves_of_an_8_bar_loop():
    bpm, bar = 120, int(SR * 4 * 60 / 120)
    x = np.zeros(8 * bar, dtype=np.float32)
    x[: 4 * bar] = 0.2                       # front half loud, back half quiet
    x[4 * bar:] = 0.05
    ch = {"chord0": {"dry": (x, x.copy()), "sr": SR}}
    base = {"bpm": bpm, "amount": 0, "roles": {"chord0": "music"}}
    for half, want in (("front", 0.2), ("back", 0.05)):
        stems, *_ , meta = dsp.render(ch, {**base, "sections": [
            {"scene": "full", "bars": 4, "half": half}, {"scene": "full", "bars": 4, "half": half}]})
        g = 10 ** (meta["gain_db"] / 20)
        mid = stems["chord0"][bar: 7 * bar, 0] / g
        assert np.allclose(np.median(mid), want, atol=1e-3)


def test_a_muted_lane_is_silent_only_in_its_section():
    ch = _channels(120)
    stems, mix, _, _ = dsp.render(ch, {"bpm": 120, "amount": 0, "sections": [
        {"scene": "full", "bars": 2, "mute": ["kick"]}, {"scene": "full", "bars": 2}]})
    bar = int(SR * 2)
    assert np.max(np.abs(stems["kick"][: 2 * bar])) < 1e-6
    assert np.max(np.abs(stems["kick"][2 * bar + 500: 4 * bar - 500])) > 0.05
    assert np.max(np.abs(sum(stems.values()) - mix)) < 1e-4


def test_build_refuses_a_sketch_that_is_not_a_whole_song(tmp_path):
    rows = song_sketch.rows_for(ROWS)
    short = {"section_bars": 4, "sections": [{"scene": "full"}] * 4}     # 32 s
    with pytest.raises(ValueError, match="2:30 to 4:00"):
        song_sketch.build(7, BPM, rows, lambda ln: _loop(100), short, root=tmp_path)
    assert not list(tmp_path.iterdir())


def test_options_carry_every_type_and_effect_choice():
    opts = song_sketch.options(song_sketch.rows_for(ROWS), 90)
    assert set(opts["types"]) == set(dsp.TYPES) and set(opts["genres"]) == set(dsp.GENRES)
    for k in dsp.TYPES:
        for fx in ["built_in", "random", *dsp.GENRES]:
            assert opts["plans"][f"{k}|{fx}"]
    assert len(opts["plans"]["radio|random"]) == len(opts["styles"]) == len(dsp.STYLES)
