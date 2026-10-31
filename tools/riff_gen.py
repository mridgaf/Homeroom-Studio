"""Chord TEXTURE (owner 2026-10-29): "Every beat doesn't have to be so
chord-heavy ... It can just be a note progression. Or a couple of notes of
the chord."

What he said he loves: a short riff, a sampled loop, sparse 1-2 note
stabs. Full keys/pads he did NOT pick, so full chords are rare. Each new
beat rolls ONE texture (seeded from the beat, so a rebuild matches):

- full: the whole chord, as before.
- two:  two notes of each chord (3rd + 7th when it has one, else root +
        3rd), played as stabs/comp only.
- riff: a 2-bar single-note riff from riff_tables.json -- his MIDI pack
        melodies or a real Lakh rap/R&B hook -- fitted to OUR chords (beat
        hits land on a chord tone, the rest on the key's scale). Half of
        riff beats add a soft two-note bed under it.
- loop: one of his sampled melodic loops carries the beat.

TEXTURES and BED_* are Claude's starting numbers (owner had no
preference on the split; full chords rare per his pick). Tune by ear.

Per identity (VERSION 2, 2026-10-30, owner: "rare, research decides"):
signature["texture_full"] overrides the full-chord chance for identities
whose researched listen line says keys/strings/choir carry the music.
Beats stamped texture_flow 1 ignore it, so they rebuild as made.

VERSION 3 (2026-10-30, owner: "Half + three notes", after 170 beats came
out 78% two-note): full chords 50% for everyone, 70% for the identities
whose texture_full is 0.4 (keys/strings/choir carry the music); the thin
texture plays three notes (3rd + 5th + 7th, else the triad) instead of
two. Beats stamped 2 or lower rebuild as made.

    ./.venv/bin/python tools/riff_gen.py      # self-check
"""
from __future__ import annotations

import json
import random
from pathlib import Path

VERSION = 3
FULL_V3, FULL_V3_KEYS = 0.50, 0.70   # v3 full-chord chance: all / keys-led
TABLES = Path(__file__).resolve().parent.parent / "riff_tables.json"
TEXTURES = (("full", 0.10), ("two", 0.30), ("riff", 0.30), ("loop", 0.30))
BED_P = 0.5              # riff beats with a soft two-note bed under them
BED_LEVEL = 0.35         # the bed's level against the riff
PACK_P = 0.5             # riff from his packs vs from Lakh
# chord-gen styles whose riffs come from Lakh R&B rather than Lakh rap
RNB_STYLES = {"rnb", "soul", "gospel", "jazz", "jazz_rap", "lofi", "funk",
              "trip_hop"}

_T = None


def tables():
    global _T
    if _T is None:
        try:
            _T = json.loads(TABLES.read_text())["styles"]
        except (OSError, ValueError, KeyError):
            _T = {}
    return _T


def roll(variant, full=None):
    """This beat's texture name. `full` (0..1) replaces the full-chord
    chance; the other textures share the rest in their usual ratio."""
    rng = random.Random(variant * 1409 + 3)
    r, acc = rng.random(), 0.0
    if full is not None:
        if r < full:
            return "full"
        f0 = TEXTURES[0][1]
        r = f0 + (r - full) / (1.0 - full) * (1.0 - f0) if full < 1 else 0
    for name, w in TEXTURES:
        acc += w
        if r < acc:
            return name
    return TEXTURES[-1][0]


def no_riff(variant):
    """A riff beat's stand-in when MIDI is off (owner 2026-10-29): two
    notes or a loop, even odds, own seed."""
    return "two" if random.Random(variant * 1409 + 7).random() < 0.5 \
        else "loop"


def two_notes(root_pos):
    """Two notes of a root-position chord: 3rd + 7th, else root + 3rd."""
    ns = sorted(root_pos)
    if len(ns) <= 2:
        return ns
    return [ns[1], ns[3]] if len(ns) >= 4 else [ns[0], ns[1]]


def full_chance(texture_full, version):
    """The full-chord chance roll() gets for a beat stamped `version`."""
    if version >= 3:
        return FULL_V3_KEYS if (texture_full or 0) >= 0.4 else FULL_V3
    return texture_full if version >= 2 else None


def three_notes(root_pos):
    """Three notes of a root-position chord: 3rd + 5th + 7th (the bass has
    the root), else the triad as it stands."""
    ns = sorted(root_pos)
    return ns[1:4] if len(ns) >= 4 else ns


def pick(variant, style):
    """{"src", "notes", "bed"} for a riff beat, or None (no table)."""
    rng = random.Random(variant * 1423 + 9)
    src = "pack" if rng.random() < PACK_P else (
        "rnb" if style in RNB_STYLES else "rap")
    riffs = (tables().get(src) or {}).get("riffs") or []
    if not riffs:
        src = next((s for s in ("pack", "rap", "rnb")
                    if (tables().get(s) or {}).get("riffs")), None)
        if not src:
            return None
        riffs = tables()[src]["riffs"]
    e = rng.choice(riffs)
    return {"src": src, "notes": e["notes"], "bed": rng.random() < BED_P}


def _char(vel):
    return "X" if vel >= 100 else "x" if vel >= 70 else "o" if vel >= 45 else "."


def _nearest(target, pcs):
    """The note nearest `target` whose pitch class is in `pcs`."""
    for d in range(12):
        for n in (target - d, target + d):
            if n % 12 in pcs:
                return n
    return target


def riff_bars(riff, nbars, bar0, chord_pcs, scale_pcs, tonic):
    """A riff laid over one chord slot of `nbars` bars that starts at loop
    bar `bar0` (the riff repeats every 2 bars across the whole loop).
    -> (bars, pitches {global 16th: note}, lengths {global 16th: beats}).
    `tonic` is the MIDI note the riff's 0 sits on."""
    bars, pitch, length = [], {}, {}
    for b in range(nbars):
        rb = (bar0 + b) % 2
        s = ["-"] * 16
        for start, dur, semis, vel in riff:
            if not rb * 4 <= start < rb * 4 + 4:
                continue
            st = min(15, int(round((start - rb * 4) * 4)))
            if s[st] != "-":
                continue
            s[st] = _char(vel)
            pcs = chord_pcs if st % 4 == 0 else scale_pcs
            pitch[b * 16 + st] = _nearest(tonic + int(semis), pcs)
            length[b * 16 + st] = float(dur)
        bars.append("".join(s))
    if not pitch and bar0 >= 0:
        # this slot landed on the riff's empty half: play the other half
        # rather than let the beat fall back to a full chord
        return riff_bars(riff, nbars, -1 - bar0, chord_pcs, scale_pcs, tonic)
    return bars, pitch, length


if __name__ == "__main__":
    from collections import Counter
    c = Counter(roll(v) for v in range(4000))
    assert 0.07 < c["full"] / 4000 < 0.13, c
    c4 = Counter(roll(v, 0.4) for v in range(4000))
    assert 0.36 < c4["full"] / 4000 < 0.44, c4
    assert abs(c4["two"] - c4["loop"]) < 200, c4   # rest keeps its ratio
    assert all(roll(v, 0.1) == roll(v) for v in range(500))
    assert two_notes([60, 63, 67, 70]) == [63, 70]
    assert two_notes([60, 64, 67]) == [60, 64]
    assert three_notes([60, 63, 67, 70]) == [63, 67, 70]
    assert three_notes([60, 64, 67]) == [60, 64, 67]
    assert full_chance(0.25, 2) == 0.25 and full_chance(None, 1) is None
    assert full_chance(None, 3) == 0.5 and full_chance(0.4, 3) == 0.7
    c5 = Counter(roll(v, full_chance(None, 3)) for v in range(4000))
    assert 0.46 < c5["full"] / 4000 < 0.54, c5
    riff = [[0.0, 0.5, 0, 110], [1.5, 0.5, 3, 80], [4.0, 1.0, 7, 60],
            [6.5, 0.5, 1, 40]]
    bars, p, ln = riff_bars(riff, 2, 0, {0, 3, 7}, {0, 2, 3, 5, 7, 8, 10}, 60)
    assert bars == ["X-----x---------", "o---------.-----"], bars
    assert p[0] == 60 and p[6] == 63 and p[16] == 67
    assert p[26] % 12 in {0, 2, 3, 5, 7, 8, 10}       # 61 -> in the scale
    bars2, _, _ = riff_bars(riff, 1, 1, {0, 3, 7}, {0, 3, 7}, 60)
    assert bars2 == ["o---------.-----"]               # bar 1 of the riff
    if tables():
        for v in range(50):
            got = pick(v, "trap")
            assert got and got["notes"], v
    half = [[0.0, 0.5, 0, 110], [1.0, 0.5, 3, 90]]       # bar 0 only
    bars3, p3, _ = riff_bars(half, 1, 1, {0, 3, 7}, {0, 3, 7}, 60)
    assert p3 and bars3 == ["X---x-----------"], bars3
    print(c, "ok")
