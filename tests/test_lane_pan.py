"""Pan knobs (owner 2026-10-15): -100..100 in, -1..1 stored, clamped."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import beat_machine as bm  # noqa: E402

PRESET = {"lanes": {"hat": (0.2, 1.0, 0, 1), "kick": (0.0, 1.0, 0, 1)}}


def test_clean_pans_scales_and_clamps():
    assert bm._clean_pans({"Hat": -50, "kick": 400}, PRESET, 1) == \
        {"hat": -0.5, "kick": 1.0}


def test_clean_pans_rejects_unknown_lane_and_junk():
    with pytest.raises(ValueError):
        bm._clean_pans({"snare": 10}, PRESET, 1)
    with pytest.raises(ValueError):
        bm._clean_pans({"hat": "left"}, PRESET, 1)


def test_pan_words():
    assert "pan L40" in bm._pan_words({"hat": -0.4})
    assert "pan C" in bm._pan_words({"kick": 0.0})
