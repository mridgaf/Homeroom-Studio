"""Phase B: deterministic arrangement moves inside a generated loop."""
import copy
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import arrangement as ar  # noqa: E402


def _preset():
    row = lambda bars: (0.0, 1.0, (0.0, 0.0, 50, 1), bars)
    return {"num": 7, "lanes": {
        "kick": row(["X---------------"] * 4),
        "hat": row(["x-x-x-x-x-x-x-x-"] * 4),
        "snare": row(["----X-------X---"] * 4),
        "perc": row(["--x---x---x---x-"] * 4),
        "chord0": row(["X---------------"] * 4),
        "bass0": row(["X---------------"] * 4),
        "melody0": row(["X---------------"] * 4),
    }}


def test_plan_is_deterministic_json_safe_and_never_mutes_bar_one():
    assert ar.plan(41, 4) == ar.plan(41, 4)
    for variant in range(500):
        moves = ar.plan(variant, 4)["moves"]
        assert len(moves) <= 2
        structural = [m for m in moves if m["kind"] != "fill"]
        assert len(structural) <= 1
        assert all(m["bar"] > 0 for m in moves)


def test_all_moves_occur_across_variants_and_fill_is_in_last_beat():
    moves = [m for v in range(500) for m in ar.plan(v, 4)["moves"]]
    assert {m["kind"] for m in moves} == {
        "stop", "thin_bar", "melodic_drop", "fill"}
    assert all((m["bar"], m["step"], m["end_step"]) == (3, 12, 16)
               for m in moves if m["kind"] == "fill")


def test_thin_bar_keeps_kick_hats_and_melodic_lanes():
    p = _preset()
    ar.apply_patterns(p, {"moves": [{"kind": "thin_bar", "bar": 2,
                                      "step": 0, "end_step": 16}]})
    assert p["lanes"]["kick"][3][2] != "-" * 16
    assert p["lanes"]["hat"][3][2] != "-" * 16
    assert p["lanes"]["snare"][3][2] == "-" * 16
    assert p["lanes"]["perc"][3][2] == "-" * 16
    assert p["lanes"]["chord0"][3][2] != "-" * 16


def test_big_fill_adds_last_beat_motion_without_touching_other_bars():
    p = _preset()
    before = copy.deepcopy(p["lanes"]["snare"][3])
    ar.apply_patterns(p, {"moves": [{"kind": "fill", "bar": 3,
                                      "step": 12, "end_step": 16}]})
    after = p["lanes"]["snare"][3]
    assert after[:3] == before[:3]
    assert sum(c != "-" for c in after[3][12:]) >= 2


def test_stop_mutes_all_melodic_lanes_with_loop_end_left_at_zero():
    n, sr, bar_s = 4000, 1000, 1.0
    bufs = {k: np.ones(n) for k in ("chord0", "bass0", "melody0", "kick")}
    plan = {"moves": [{"kind": "stop", "bar": 3,
                       "step": 8, "end_step": 16}]}
    ar.apply_buffers(bufs, plan, bar_s, sr)
    for lane in ("chord0", "bass0", "melody0"):
        assert np.all(bufs[lane][3510:] == 0.0)
        assert bufs[lane][3499] > bufs[lane][3504]
    assert np.all(bufs["kick"] == 1.0)


def test_melodic_drop_only_mutes_chords_and_returns_with_a_ramp():
    n, sr, bar_s = 4000, 1000, 1.0
    bufs = {k: np.ones(n) for k in ("chord0", "bass0", "melody0", "kick")}
    plan = {"moves": [{"kind": "melodic_drop", "bar": 2,
                       "step": 0, "end_step": 16}]}
    ar.apply_buffers(bufs, plan, bar_s, sr)
    assert np.all(bufs["chord0"][2010:3000] == 0.0)
    assert bufs["chord0"][3000] == 0.0 and bufs["chord0"][3004] == 1.0
    for lane in ("bass0", "melody0", "kick"):
        assert np.all(bufs[lane] == 1.0)


def test_no_stamp_path_is_a_no_op():
    p = _preset()
    before = copy.deepcopy(p)
    ar.apply_patterns(p, None)
    assert p == before
    bufs = {"chord0": np.ones(4000)}
    ar.apply_buffers(bufs, None, 1.0, 1000)
    assert np.all(bufs["chord0"] == 1.0)
