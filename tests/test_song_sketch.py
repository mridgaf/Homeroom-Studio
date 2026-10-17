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
