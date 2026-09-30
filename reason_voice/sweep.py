"""Sweep one knob over N bars while Reason records (OPEN-ISSUES 31, first phrase).

    "sweep the filter up over four bars"      tempo remembered from last time
    "sweep the filter down over 8 bars at 90" tempo said, then remembered

The bridge can only set one knob value at a time, so a sweep is a timed ramp of
set_value() calls with Reason's Record running. Proven by hand 2026-09-25
(experiments/automation-test-2026-09-25): the device needs its own sequencer
track and must be locked to ReasonVoice.

ponytail: 4/4 only and wall-clock timing (a real clock drifts a few ms), ends
are the knob's own ends (0 or 127), no shaped curves. Upgrade when he asks.
"""
import re

from .dial_llm import _SPELLED

_SWEEP = re.compile(
    r"^sweep\s+(?:the\s+)?(.+?)\s+(up|down)\s+over\s+(\w+)\s+bars?"
    r"(?:\s+at\s+(\d{2,3})(?:\s*bpm)?)?$")
_COUNT = dict(_SPELLED, **{"for": 4})     # whisper hears "four" as "for"


def parse_sweep(text):
    """{"what","way","bars","bpm"} or None. `bpm` is None when not said."""
    m = _SWEEP.match((text or "").strip().lower().rstrip(".!?,"))
    if not m:
        return None
    what, way, n, bpm = m.groups()
    bars = int(n) if n.isdigit() else _COUNT.get(n)
    if not bars or bars < 1:
        return None
    return {"what": what, "way": way, "bars": bars,
            "bpm": int(bpm) if bpm else None}


def bars_to_seconds(bars, bpm):
    return bars * 4 * 60.0 / bpm


def plan(start, end, seconds):
    """[(seconds_from_start, position)]: every whole position from start to end,
    evenly spaced, so the recorded lane is a straight line."""
    n = abs(end - start)
    if n == 0:
        return []
    step = 1 if end > start else -1
    return [(seconds * i / n, start + step * i) for i in range(1, n + 1)]


def demo():
    assert parse_sweep("Sweep the filter up over four bars.") == {
        "what": "filter", "way": "up", "bars": 4, "bpm": None}
    assert parse_sweep("sweep the low pass down over 8 bars at 90")["bpm"] == 90
    assert parse_sweep("sweep the filter up over for bars")["bars"] == 4
    assert parse_sweep("sweep the filter up") is None
    assert parse_sweep("sweep the filter up over zero bars") is None
    assert bars_to_seconds(4, 120) == 8.0
    p = plan(0, 127, 8.0)
    assert len(p) == 127 and p[-1] == (8.0, 127) and p[0][1] == 1
    assert plan(100, 0, 4.0)[-1] == (4.0, 0) and plan(5, 5, 1.0) == []
    print("sweep ok")


if __name__ == "__main__":
    demo()
