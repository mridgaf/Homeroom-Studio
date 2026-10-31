"""Owner 2026-10-31, Plan A: real-drummer timing + gentle accents + a tiny
start-point change per hit, on beats stamped `real_feel` only."""
import copy
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import crew  # noqa: E402
import real_groove  # noqa: E402
from crew import CREW, SR, render_crew_beat  # noqa: E402

TPL = {"hat": {"offset16": [0.0, -0.2] + [0.0] * 14,
               "vel": [1.0, 0.3] + [1.0] * 14}}


def _render(monkeypatch, stamp):
    monkeypatch.setattr(crew, "TRUE_LEVELS", True)
    monkeypatch.setattr(real_groove, "_TEMPLATES", {"t:d1": TPL})
    p = copy.deepcopy(CREW["Cutz"])
    p["space"] = ("dry", [])
    p["sidechain"] = 0.0
    p["lanes"] = {"kick": (0.0, 1.0, (0, 0, 50, 1), ["X-------X-------"]),
                  "snare": (0.0, 1.0, (0, 0, 50, 2), ["----X-------X---"]),
                  "hat": (0.0, 1.0, (0, 0, 50, 3), ["xx--------------"])}
    if stamp:
        p["real_feel"] = {"key": "t:d1", "skip": []}
    t = np.arange(SR // 20) / SR
    env = np.exp(-t * 80)
    kit = {"kick": np.sin(2 * np.pi * 60 * t) * env,
           "snare": 0.3 * np.sin(2 * np.pi * 1500 * t) * env,
           "hat": 0.3 * np.sin(2 * np.pi * 3000 * t) * env}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    return [e for e in parts["events"]["hat"]][:2], p["bpm"]


def test_real_feel_moves_and_accents_only_stamped_beats(monkeypatch):
    (a0, a1), bpm = _render(monkeypatch, False)
    (b0, b1), _ = _render(monkeypatch, True)
    six = 60.0 / bpm / 4
    # step 1 moves 0.2 of a 16th early; step 0 stays put
    assert abs((b1[0] - a1[0]) + 0.2 * six) < 0.002
    assert abs(b0[0] - a0[0]) < 0.002
    # the soft step is pulled up to the 4 dB floor, not down to 0.3
    ratio = (b1[1] / b0[1]) / (a1[1] / a0[1])
    assert abs(ratio - real_groove.ACCENT_FLOOR) < 0.01
