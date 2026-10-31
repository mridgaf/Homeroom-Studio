"""Small arrangement moves inside a generated beat loop.

New beats are stamped with ``arrange_flow`` and carry the exact plan in
their preset.  Old recipes have neither key, so rebuilding them never reaches
this module.  A plan contains at most one structural move plus an optional
fill into bar 1:

* stop: melodic lanes rest for the final one or two beats;
* thin_bar: one bar of drums keeps only kick and hats;
* melodic_drop: chords rest for one bar while bass and melody continue;
* fill: a stronger snare/clap/perc fill in the loop's final beat.

The numbers are starting points under the owner's 2026-10-19 creative-control
grant.  They still need a listening verdict.
"""
from __future__ import annotations

import random

import numpy as np


FLOW_VERSION = 1
# owner 2026-10-30: no stop / thin_bar / melodic_drop on new beats. The
# fill into bar 1 stays.
STRUCTURE_P = 0.0
FILL_P = 0.65
DRUM_PREFIXES = ("kick", "snare", "clap", "hat", "perc", "rim", "bongo",
                 "conga", "shaker", "tom", "cym", "ride", "crash")


def plan(variant, nbars):
    """Return a deterministic, JSON-safe plan for one loop."""
    nbars = int(nbars)
    if nbars < 4:
        return {"moves": []}
    rng = random.Random(int(variant) * 1877 + 101)
    moves = []
    if rng.random() < STRUCTURE_P:
        kind = rng.choices(("stop", "thin_bar", "melodic_drop"),
                           weights=(4, 3, 3))[0]
        if kind == "stop":
            moves.append({"kind": kind, "bar": nbars - 1,
                          "step": rng.choice((8, 12)), "end_step": 16})
        else:
            # Never remove bar 1's downbeat.  Keeping the last bar available
            # lets the optional fill answer the drop before the loop returns.
            moves.append({"kind": kind,
                          "bar": rng.randrange(1, nbars),
                          "step": 0, "end_step": 16})
    if rng.random() < FILL_P:
        moves.append({"kind": "fill", "bar": nbars - 1,
                      "step": 12, "end_step": 16})
    return {"moves": moves}


def _replace_bars(spec, bars):
    """Preserve the lane tuple/list shape while replacing its bar list."""
    vals = list(spec)
    vals[3] = bars
    return tuple(vals) if isinstance(spec, tuple) else vals


def apply_patterns(preset, arrangement):
    """Apply the drum-only parts of a plan to ``preset['lanes']`` in place."""
    moves = (arrangement or {}).get("moves") or []
    lanes = preset.get("lanes") or {}
    for move in moves:
        kind, bar = move.get("kind"), int(move.get("bar", -1))
        if kind == "thin_bar":
            for lane, spec in list(lanes.items()):
                if not lane.startswith(DRUM_PREFIXES) \
                        or lane.startswith(("kick", "hat")):
                    continue
                bars = list(spec[3])
                if 0 <= bar < len(bars):
                    bars[bar] = "-" * len(bars[bar])
                    lanes[lane] = _replace_bars(spec, bars)
        elif kind == "fill":
            import pattern_gen
            targets = [ln for prefix in ("snare", "clap", "perc", "rim")
                       for ln in lanes if ln.startswith(prefix)]
            if not targets:
                continue
            lane = targets[0]
            spec = lanes[lane]
            bars = list(spec[3])
            if 0 <= bar < len(bars):
                rng = random.Random(int(preset.get("num", 0)) * 1999 + bar)
                bars[bar] = pattern_gen._fill(bars[bar], rng, big=True)
                lanes[lane] = _replace_bars(spec, bars)
    return preset


def _mute(buf, start, end, fade):
    """Mute [start, end), with short ramps and no wrap-boundary click."""
    n = len(buf)
    start, end = max(0, int(start)), min(n, int(end))
    if start >= end:
        return buf
    out = buf.copy()
    f = min(int(fade), end - start)
    if f:
        out[start:start + f] *= np.linspace(1.0, 0.0, f, endpoint=True)
    out[start + f:end] = 0.0
    if end < n:
        f2 = min(int(fade), n - end)
        out[end:end + f2] *= np.linspace(0.0, 1.0, f2, endpoint=True)
    return out


def apply_buffers(bufs, arrangement, bar_s, sr):
    """Bake stop/drop silence into rendered loop buffers."""
    moves = (arrangement or {}).get("moves") or []
    fade = max(1, round(0.005 * sr))
    for move in moves:
        kind = move.get("kind")
        if kind not in ("stop", "melodic_drop"):
            continue
        start = (int(move["bar"]) + int(move.get("step", 0)) / 16.0) \
            * bar_s * sr
        end = (int(move["bar"]) + int(move.get("end_step", 16)) / 16.0) \
            * bar_s * sr
        for lane, buf in list(bufs.items()):
            melodic = lane.startswith(("chord", "bass", "melody"))
            target = melodic if kind == "stop" else lane.startswith("chord")
            if target:
                bufs[lane] = _mute(buf, start, end, fade)
    return bufs
