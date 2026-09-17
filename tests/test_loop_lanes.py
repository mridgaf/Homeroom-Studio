"""Five-lane loops beats (owner spec 2026-09-16, DECISIONS.md)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import loop_lanes
from make_drum_loops import SR, write_wav24


def test_categories():
    assert loop_lanes.categories(("Synths - Loops", "Sub Riser.wav")) == ["fx"]
    assert set(loop_lanes.categories(("Keys", "Piano Loop Cm.wav"))) == {"lead", "chords"}
    assert loop_lanes.categories(("Drums", "Kick Loop 90.wav")) == []
    assert loop_lanes.categories(("Melody Loops", "Dreamy 90bpm.wav")) == ["lead"]


def test_tempo_from_name_else_length():
    assert loop_lanes.source_bpm(3.0, 87, 120) == 87.0
    assert abs(loop_lanes.source_bpm(4.0, None, 95) - 120.0) < 1e-6


def test_lanes_are_eight_bars_and_fx_is_sparse(tmp_path):
    bpm, bar = 100, int(round(2.4 * SR))
    tone = 0.3 * np.sin(np.arange(bar * 2) * 2 * np.pi * 220 / SR)   # 2 bars
    loop = tmp_path / "Guitar Loop 100bpm.wav"
    write_wav24(loop, tone, tone)
    L, R = loop_lanes.build_lane("leadloop", str(loop), bpm, SR)
    assert len(L) == 8 * bar
    hit = np.zeros(int(0.5 * SR)); hit[:100] = 0.5
    fx = tmp_path / "Impact FX.wav"
    write_wav24(fx, hit, hit)
    L, _ = loop_lanes.build_lane("fxloop", str(fx), bpm, SR, fx_bars=[2, 6])
    loud = [b for b in range(8) if np.abs(L[b * bar:(b + 1) * bar]).max() > 0.1]
    assert loud == [2, 6]


def test_file_name_beats_folder_name():
    assert loop_lanes.categories(("Vocals", "FL_MP_80_Bass_Synth_Boom_Dm.wav")) == ["bass"]


def test_long_fx_plays_one_bar_per_hit_never_neighbours(tmp_path):
    import random
    bpm, bar = 100, int(round(2.4 * SR))
    long_fx = 0.3 * np.ones(bar * 3)                     # a 3-bar FX file
    fx = tmp_path / "Noise FX.wav"
    write_wav24(fx, long_fx, long_fx)
    L, _ = loop_lanes.build_lane("fxloop", str(fx), bpm, SR, fx_bars=[1, 5])
    loud = [b for b in range(8) if np.abs(L[b * bar:(b + 1) * bar]).max() > 0.1]
    assert loud == [1, 5]
    for seed in range(200):
        spots = loop_lanes.fx_spots(random.Random(seed))
        assert 1 <= len(spots) <= 2
        if len(spots) == 2:
            assert (spots[1] - spots[0]) % 8 not in (0, 1, 7)
