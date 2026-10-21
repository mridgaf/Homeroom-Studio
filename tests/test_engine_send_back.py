"""Effects page round trip (owner 2026-10-15), on a tiny fake library:
send-back files a NEW numbered beat with its stems; chunks/rebuilds of
that beat are mixes of those stems (volume, pan, remove), never a
re-render, and sound swaps are refused."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import beat_machine as bm  # noqa: E402
from beat_recipes import lane_label, save_recipe  # noqa: E402
from make_drum_loops import read_wav24, write_wav24  # noqa: E402


def _fake_beat(root, no=100):
    dj = root / "Test DJ"
    dj.mkdir(parents=True)
    tone = np.full(1000, 0.25)
    write_wav24(dj / f"{no} Test DJ Song Drums 90bpm.wav", tone, tone)
    stems = dj / f"{no} Test DJ Song Stems"
    stems.mkdir()
    for ln in ("kick", "hat"):
        write_wav24(stems / f"{lane_label(ln)} - x.wav", tone / 2, tone / 2)
    save_recipe(root, no, {
        "names": ["Test DJ"], "title": "Song", "folder": "Test DJ",
        "file": f"{no} Test DJ Song Drums 90bpm.wav",
        "preset": {"bpm": 90, "lanes": {"kick": [0.0, 1, 0, 1],
                                         "hat": [0.0, 1, 0, 1]}},
        "kit_spec": {"kick": ["kick"], "hat": ["hat"]},
        "kit_paths": {}, "stamp_paths": {}})
    return {f.name: read_wav24(f) for f in stems.glob("*.wav")}


def test_send_back_then_chunk_mix(tmp_path):
    stems = _fake_beat(tmp_path)
    mix = (np.full(1000, 0.25), np.full(1000, 0.25))
    path, _ = bm._file_engine_beat(100, stems, mix, "FX", tmp_path)
    no = int(path.name.split(" ")[0])
    assert no > 100 and path.exists()
    assert bm.load_recipe(tmp_path, no)["engine_fx"] is True
    assert len(list(bm._stems_dir(no, tmp_path).glob("*.wav"))) == 2

    # untouched: kick + hat = 0.125 + 0.125 per side
    L, R = bm.swap_many(no, {}, root=tmp_path, render_only=True)
    assert np.allclose(L, 0.25, atol=1e-4) and np.allclose(R, 0.25, atol=1e-4)
    # hat removed, kick panned hard left
    L, R = bm.swap_many(no, {}, root=tmp_path, drops=["hat"],
                        pans={"kick": -100}, render_only=True)
    assert L[0] > 0.17 and abs(R[0]) < 1e-4

    with pytest.raises(ValueError, match="swaps are off"):
        bm.swap_many(no, {"kick": "/some/file.wav"}, root=tmp_path,
                     render_only=True)

    # rebuild of the effected beat: new number, hat gone from its recipe
    p2, _ = bm.swap_many(no, {}, root=tmp_path, drops=["hat"])
    rec2 = bm.load_recipe(tmp_path, int(p2.name.split(" ")[0]))
    assert "hat" not in rec2["kit_spec"] and rec2["engine_fx"]


def test_import_refuses_folders_outside_exports(tmp_path):
    with pytest.raises(ValueError):
        bm.import_engine_send(100, tmp_path, root=tmp_path)


def test_chunks_file_under_the_dj_on_the_desktop(tmp_path, monkeypatch):
    _fake_beat(tmp_path)
    monkeypatch.setattr(bm, "CHUNKS_ROOT", tmp_path / "Homeroom Chunks")
    d = bm.chunk_dir(100, tmp_path)
    assert d == tmp_path / "Homeroom Chunks" / "Test DJ" / "100 Test DJ Song Drums 90bpm Chunks"


def test_effects_button_stages_the_rack_without_a_new_number(tmp_path):
    """Owner 2026-10-21: Effects opens the beat AS SET (here: hat removed)
    with no new number, in a place the Sound Engine can open and its picker
    never lists."""
    from sound_engine import library
    stems = _fake_beat(tmp_path)
    mix = (np.full(1000, 0.25), np.full(1000, 0.25))
    path, _ = bm._file_engine_beat(100, stems, mix, "FX", tmp_path)
    no = int(path.name.split(" ")[0])
    before = bm.next_number(tmp_path)
    se_id = bm.swap_many(no, {}, root=tmp_path, drops=["hat"], stage=True)
    assert se_id == f"Test DJ/{bm.STAGE_DIR}/Beat {no} (your mix)"
    assert bm.next_number(tmp_path) == before                  # no new number
    beat = library.find_beat(tmp_path, se_id)
    assert beat and beat["dj"] == "Test DJ" and beat["stem_count"] == 1
    assert not any(b["beat_id"] == se_id for b in library.list_beats(tmp_path))
    # a second click replaces it: hat back in
    bm.swap_many(no, {}, root=tmp_path, pans={"kick": 0}, stage=True)
    assert library.find_beat(tmp_path, se_id)["stem_count"] == 2
    # the Sketch button's folder sits next to it
    assert bm.sketch_stage_dir(no, tmp_path).parent == tmp_path / "Test DJ" / bm.STAGE_DIR
