"""Turntable scratch performance engine (owner request 2026-07-23 — a
gap flagged during the Legends harmony research: DJ Premier's scratched
vocal hooks are a real technique the engine had no way to reproduce,
only a static "scratch" one-shot sound-effect sample used as a single
accent hit).

A scratch isn't a filter or an oscillator — it's a HAND MOTION: the DJ
moves the record forward and back under the needle while the crossfader
opens and closes. Modeled directly as that: a "gesture" is a position-
over-time curve (where in the source sample the needle is reading at
each output moment, non-monotonic — it can go backward) plus a fader
curve (0-1, how open the crossfader is). Reading the source audio at
that position curve (via linear interpolation, `np.interp`) IS the
scratch — no new filter, no new dependency, same numpy-only style as
every other synth module here.

    ./.venv/bin/python tools/scratch.py            # pattern demo
"""
from __future__ import annotations

import numpy as np

from make_drum_loops import SR


def _ramp(a, b, n):
    return np.linspace(a, b, max(n, 1), endpoint=False)


# name -> a builder(hit_dur, n) -> (position_seconds_array, fader_array)
# hit_dur is how far into the source sample the forward push reaches.
def _baby(hit_dur, n):
    half = n // 2
    pos = np.concatenate([_ramp(0, hit_dur, half),
                          _ramp(hit_dur, 0, n - half)])
    fader = np.ones(n)
    return pos, fader


def _chirp(hit_dur, n):
    # forward with the fader open, backward with it CLOSED — the classic
    # "chirp" (you hear the push, not the pull).
    half = n // 2
    pos = np.concatenate([_ramp(0, hit_dur, half),
                          _ramp(hit_dur, 0, n - half)])
    fader = np.concatenate([np.ones(half), np.zeros(n - half)])
    return pos, fader


def _transform(hit_dur, n):
    # steady forward push, fader chopped on/off several times (the
    # "chop chop chop" transform scratch) instead of one smooth open.
    pos = _ramp(0, hit_dur, n)
    chops = 5
    fader = (np.arange(n) * chops // n) % 2
    return pos, fader.astype(float)


def _scribble(hit_dur, n):
    # rapid back-and-forth over a SHORT distance, several cycles —
    # panicked/fast scratch texture rather than one clean gesture.
    cycles = 4
    t = np.linspace(0, cycles * 2 * np.pi, n)
    pos = hit_dur * 0.35 * (1 - np.cos(t)) / 2
    fader = np.ones(n)
    return pos, fader


PATTERNS = {
    "baby": _baby,
    "chirp": _chirp,
    "transform": _transform,
    "scribble": _scribble,
}


def scratch(source, dur, pattern="baby", hit_dur=0.18, fade_ms=4, sr=SR):
    """Scratch `source` (a mono one-shot array, e.g. a found vocal chop
    or horn hit) into a `dur`-second performance. `hit_dur` is how far
    into the source (seconds) the forward push reaches — a short vocal
    chop wants a small hit_dur so the push doesn't run off the end of
    the sample. Silence in, silence out; a source shorter than hit_dur
    gets its reach clamped so the position curve never reads past the
    end. `fade_ms` is a tiny click-guard at every fader transition, not
    a musical parameter."""
    n = max(int(dur * sr), 0)
    if n <= 0 or source is None or len(source) == 0:
        return np.zeros(max(n, 0))
    src_dur = len(source) / sr
    reach = min(hit_dur, src_dur)
    builder = PATTERNS.get(pattern, PATTERNS["baby"])
    pos_s, fader = builder(reach, n)
    pos_samp = np.clip(pos_s * sr, 0, len(source) - 1)
    out = np.interp(pos_samp, np.arange(len(source)), source)
    # smooth the fader's on/off steps a little so a "transform" chop
    # reads as a fast fade, not a sample-accurate click
    f_n = max(int(fade_ms / 1000.0 * sr), 1)
    if f_n > 1:
        kernel = np.ones(f_n) / f_n
        fader = np.convolve(fader, kernel, mode="same")
    out = out * fader
    peak = np.max(np.abs(out))
    return out * (0.9 / peak) if peak > 0.9 else out


def _report():
    src = np.sin(2 * np.pi * 220 * np.arange(int(0.4 * SR)) / SR)
    for name in PATTERNS:
        audio = scratch(src, dur=1.0, pattern=name)
        print("%-10s len=%.2fs  peak=%.3f" %
              (name, len(audio) / SR, np.max(np.abs(audio))))


if __name__ == "__main__":
    _report()
