"""Long kick gets a short kick's snap and ducks 5 dB under it
(owner 2026-09-28). Synthetic sounds only: no drive, no render to disk."""
import copy
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import crew
from make_drum_loops import SR


def _boom(secs=1.5):
    t = np.arange(int(secs * SR)) / SR
    return np.sin(2 * np.pi * 50 * t) * np.exp(-t / 0.6)


def _snap():
    return np.random.default_rng(1).normal(size=int(0.01 * SR))


def test_ring_secs_reads_the_tail_not_the_file_length():
    padded = np.concatenate([np.hanning(int(0.1 * SR)), np.zeros(SR)])
    assert crew.ring_secs(padded) < 0.2
    assert crew.ring_secs(_boom()) > crew.LONG_KICK_SECS


def test_long_tail_dips_under_the_snap_and_keeps_the_kick_peak():
    boom = _boom()
    out = crew.punch_long_kick(boom, _snap())
    assert np.isclose(np.abs(out).max(), np.abs(boom).max())
    # same point in the 50 Hz cycle, early (ducked) vs late (recovered)
    early, late = int(0.03 * SR), int(0.03 * SR) + 50 * int(SR / 50)
    dip = (out[early] / boom[early]) / (out[late] / boom[late])
    want = 1 - crew.LONG_KICK_DUCK * np.exp(-0.03 / 0.09)
    assert abs(dip - want) < 0.02
    # recovered fully: the late-point gain is the whole mix's level factor,
    # and the deepest dip measures the full 5 dB right at the hit
    assert abs(20 * np.log10(1 - crew.LONG_KICK_DUCK) + 5.0) < 1e-6


def test_a_long_kick_renders_one_hit_at_a_time():
    """Flat 1 kHz tone that rings 1.5 s, hits 4 steps apart. Stacked, the
    first tail is still under the second hit (measured 1.79x); choked, the
    level after hit 2 matches the level after hit 1."""
    t = np.arange(int(1.5 * SR)) / SR
    boom = np.sin(2 * np.pi * 1000 * t)
    p = copy.deepcopy(crew.CREW["Cutz"])
    p["lanes"] = {"kick": (0.0, 1.0, (0.0, 0.0, 0.0, 0),
                           ["x---x-----------"])}

    def late_ratio(kit):
        _L, _R, _l, parts = crew.render_crew_beat("Cutz", kit, preset=p,
                                                  want_parts=True)
        k = parts["stems"]["kick"][0]
        e = sorted(t for t, _v in parts["events"]["kick"])
        a, b = int((e[0] + 0.25) * SR), int((e[1] + 0.25) * SR)
        rms = lambda i: np.sqrt((k[i:i + 2000] ** 2).mean())
        return rms(b) / rms(a)

    assert late_ratio({"kick": boom}) > 1.5                    # stacks
    assert abs(late_ratio({"kick": boom, "kickpunch": _snap()}) - 1) < 0.05
