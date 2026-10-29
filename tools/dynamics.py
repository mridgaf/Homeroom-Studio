"""Written loud/soft for the chords and the bass (owner 2026-10-29: "louder
and softer hits written into the chord and bass patterns. Velocity ...
back in August it sounded horrible ... we need to do a better job").

What went wrong in August, measured then (see groove.velocity and
beat_machine CHORD_LEVEL_VAR_DB): a RANDOM per-hit wobble that put one hit
up to 17 dB under its neighbour, so ghosts vanished, plus whole chords
louder or quieter than the next one (a 6.7 dB spread on one beat). Both
stay gone. This does the opposite:

- nothing random: a hit's level comes from its written character
  (X accent, x normal, o soft, . ghost) times WHERE it sits in the bar,
  by the style's accent shape (boom bap leans on the downbeat, club on
  the off-beats, funk on the syncopations);
- a floor: no hit ever plays more than FLOOR_DB under the loudest one,
  so a soft note is soft, never gone;
- every bar and every chord gets the same shape, so nothing wanders;
- a soft hit is also a little darker (soften), the way a real player's
  soft note is. Turning a sample down alone is what sounds fake.

The same level goes into the MIDI file as velocity (127 * level).
"""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

VERSION = 1
FLOOR_DB = -10.0
FLOOR = 10 ** (FLOOR_DB / 20.0)
CHAR = {"X": 1.0, "x": 0.86, "o": 0.66, ".": 0.5}
# (downbeat, other beats, 8th off-beats, 16ths) -- Claude's starting shapes
SHAPES = {
    "boom_bap": (1.0, 0.86, 0.78, 0.62),
    "jazz": (1.0, 0.8, 0.88, 0.62),
    "funk": (1.0, 0.8, 0.9, 0.7),
    "trap": (1.0, 0.92, 0.86, 0.74),
    "club": (0.9, 0.8, 1.0, 0.66),
    "latin": (1.0, 0.8, 0.9, 0.76),
    "soul": (1.0, 0.84, 0.76, 0.6),
    "lofi": (0.96, 0.82, 0.74, 0.6),
    "rock": (1.0, 0.9, 0.8, 0.66),
}
SHAPE_OF = {"rap": "boom_bap", "memphis": "boom_bap", "jazz_rap": "jazz",
            "gfunk": "funk", "drill": "trap", "emo_rap": "trap",
            "rnb": "soul", "gospel": "soul", "trip_hop": "lofi"}
SOFT_HZ = 2800.0         # where a soft hit's top end rolls off
SOFT_MIX = 0.55          # how much of the darker copy the softest hit gets


def shape_for(style):
    return SHAPE_OF.get(style, style if style in SHAPES else "boom_bap")


def level(ch, step16, shape):
    """0..1 for one written hit; 0 for a rest. Never below FLOOR."""
    base = CHAR.get(ch, 0.0)
    if not base:
        return 0.0
    down, beat, off, six = SHAPES.get(shape, SHAPES["boom_bap"])
    s = step16 % 16
    pos = down if s == 0 else beat if s % 4 == 0 else off if s % 2 == 0 \
        else six
    return float(max(FLOOR, min(1.0, base * pos)))


def soften(seg, lvl, sr=44100):
    """`seg` at `lvl`, with the top end eased off in step with how soft
    the hit is. A full-level hit comes back untouched (just scaled)."""
    if seg is None or lvl >= 0.97:
        return None if seg is None else seg * lvl
    mix = SOFT_MIX * min(1.0, (1.0 - lvl) / (1.0 - FLOOR))
    a = 1.0 - np.exp(-2 * np.pi * SOFT_HZ / sr)
    dark = lfilter([a], [1.0, a - 1.0], seg, axis=0)
    return lvl * ((1.0 - mix) * seg + mix * dark)


if __name__ == "__main__":
    for sh in SHAPES:
        lv = [level(c, s, sh) for c in "Xxo." for s in range(16)]
        assert all(FLOOR - 1e-9 <= v <= 1.0 for v in lv), sh
        assert level("X", 0, sh) >= max(lv) - 1e-9 or sh == "club"
    assert level("-", 0, "trap") == 0.0
    x = np.random.RandomState(0).randn(4410)
    assert np.allclose(soften(x, 1.0), x)
    assert np.max(np.abs(soften(x, 0.4))) < np.max(np.abs(x))
    print("dynamics ok; floor %.1f dB" % FLOOR_DB)
