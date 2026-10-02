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
    r"^(?:sweep|sweet|swipe)\s+(?:the\s+)?(.+?)\s+(up|down)\s+over\s+(\w+)\s+bars?"
    r"(?:\s+at\s+(\d{2,3})(?:\s*(?:bpm|beats per minute))?)?$")
_COUNT = dict(_SPELLED, **{"for": 4})     # whisper hears "four" as "for"
_THROW = re.compile(
    r"^throw\s+(?:the\s+)?(.+?)\s+for\s+(\w+)\s+bars?"
    r"(?:\s+at\s+(\d{2,3})(?:\s*(?:bpm|beats per minute))?)?$")
_FILL = re.compile(
    r"^fill[\s-]?in\s+over\s+(\w+)\s+bars?"
    r"(?:\s+at\s+(\d{2,3})(?:\s*(?:bpm|beats per minute))?)?$")
_SNAP = re.compile(r"^snap[\s-]?back$")


def _clean(text):
    """Lowercase, no end punctuation; "x x" said once but heard twice -> "x"."""
    t = (text or "").strip().lower().rstrip(".!?,")
    half = len(t) // 2
    if len(t) % 2 == 1 and t[:half].strip() == t[half + 1:].strip() and t[half] == " ":
        t = t[:half].strip().rstrip(".!?,")
    return t


def _bars(n):
    bars = int(n) if n.isdigit() else _COUNT.get(n)
    return bars if bars and bars >= 1 else None


def parse_sweep(text):
    """{"what","way","bars","bpm"} or None. `bpm` is None when not said."""
    m = _SWEEP.match(_clean(text))
    if not m:
        return None
    what, way, n, bpm = m.groups()
    bars = _bars(n)
    if not bars:
        return None
    return {"what": what, "way": way, "bars": bars,
            "bpm": int(bpm) if bpm else None}


def parse_throw(text):
    """"throw the reverb for one bar" -> {"what","bars","bpm"} or None."""
    m = _THROW.match(_clean(text))
    bars = _bars(m.group(2)) if m else None
    if not bars:
        return None
    return {"what": m.group(1), "bars": bars,
            "bpm": int(m.group(3)) if m.group(3) else None}


def parse_fill_in(text):
    """"fill in over eight bars": the DJ-intro sound, thin to full. It is the
    high pass (low cut) swept down, so it comes back as a sweep. Both words are
    said because the knob picker reads names literally: on a Scream 4 "high
    pass" picked Cut Hi (a top cut) and "low cut or high pass" picked Cut Lo."""
    m = _FILL.match(_clean(text))
    bars = _bars(m.group(1)) if m else None
    if not bars:
        return None
    return {"what": "low cut or high pass", "way": "down", "bars": bars,
            "bpm": int(m.group(2)) if m.group(2) else None, "fill": True}


def is_snap_back(text):
    return bool(_SNAP.match(_clean(text)))


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
    assert parse_sweep("sweep the filter up over 4 bars at 90 beats per minute")["bpm"] == 90
    assert parse_sweep("sweep the filter up") is None
    assert parse_throw("Throw the reverb for one bar.") == {
        "what": "reverb", "bars": 1, "bpm": None}
    assert parse_throw("throw the delay for 2 bars at 90")["bpm"] == 90
    assert parse_throw("throw the reverb") is None
    assert parse_fill_in("Fill in over eight bars.") == {
        "what": "low cut or high pass", "way": "down", "bars": 8, "bpm": None}
    assert parse_fill_in("fill-in over 4 bars at 90")["bpm"] == 90
    assert parse_fill_in("fill in") is None
    assert is_snap_back("Snap back.") and is_snap_back("snapback")
    assert not is_snap_back("snap back the filter")
    assert parse_sweep("sweep the filter up over zero bars") is None
    assert bars_to_seconds(4, 120) == 8.0
    p = plan(0, 127, 8.0)
    assert len(p) == 127 and p[-1] == (8.0, 127) and p[0][1] == 1
    assert plan(100, 0, 4.0)[-1] == (4.0, 0) and plan(5, 5, 1.0) == []
    print("sweep ok")


if __name__ == "__main__":
    demo()
