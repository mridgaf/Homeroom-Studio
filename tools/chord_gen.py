"""Genre chord-progression GENERATOR (owner 2026-10-29: "a whole new
selection of chord progressions ... something that generates chord
progressions ... so it can generate different genres").

Replaces the hand-written progressions_config.json loops on NEW beats
(owner pick: replace; old beats rebuild exactly as made). Plays from
chord_tables.json, built by tools/build_chord_tables.py out of the
Chordonomicon dataset: for each style (boom bap, trap, soul, G-funk,
club, ...) the chord loops real songs in that style repeat, and which
chord follows which.

Two ways a loop is made, both seeded from the beat:
- REAL (REAL_P): a loop real songs in the style play, picked with weight
  count ** FLATTEN so the five most common loops don't take every beat.
- NEW (the rest): a Markov walk over that style's chord moves, 2-4
  chords, no chord twice, and the last chord has to be one that style
  really moves back to the first from, so the loop wraps.

Each identity leans on its own styles (STYLE_FOR, Claude's picks from each
identity's listen line); a free beat rolls any style.

    ./.venv/bin/python tools/chord_gen.py            # 8 samples
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from key_context import mode_family                     # noqa: E402

TABLES = Path(__file__).resolve().parent.parent / "chord_tables.json"
VERSION = 1
REAL_P = 0.5
FLATTEN = 0.5            # count ** FLATTEN when picking a real loop
SIZES = ((4, 6), (3, 3), (2, 1))     # (chords, weight) for a NEW loop
SHORT_W = 0.35           # a REAL 2-chord loop is picked this much as often

# identity -> {style: weight}. Claude's picks from each listen line.
STYLE_FOR = {
    "Otto Grit": {"jazz_rap": 3, "soul": 2, "rnb": 1, "boom_bap": 1},
    "Cutz": {"boom_bap": 3, "jazz_rap": 2, "jazz": 1},
    "Crate Prophet": {"boom_bap": 3, "soul": 2, "jazz_rap": 1},
    "Chrome Dial": {"rnb": 2, "funk": 1, "club": 1, "trap": 1},
    "Glass Cat": {"rnb": 2, "funk": 2, "club": 1},
    "Sunday Chop": {"soul": 3, "gospel": 2, "rnb": 1},
    "Night Metro": {"trap": 3, "emo_rap": 1, "memphis": 1},
    "Rage Engine": {"trap": 3, "emo_rap": 1, "rock": 1},
    "New Math": {"club": 3, "trap": 1, "funk": 1},
    "Half Light": {"lofi": 3, "rnb": 1, "trip_hop": 1},
    "Fast Water": {"emo_rap": 2, "trap": 1, "lofi": 1},
    "Farrow": {"rock": 2, "funk": 2, "soul": 1},
    "Doc Day": {"gfunk": 3, "rap": 2, "rnb": 1},
    "Kane East": {"trap": 2, "rock": 1, "emo_rap": 1, "club": 1},
    "J Dillo": {"jazz_rap": 3, "soul": 2, "rnb": 2},
    "Mustang": {"trap": 2, "club": 2, "rnb": 1},
    "Swish Beatz": {"trap": 2, "rap": 2, "rock": 1},
    "DJ Premium": {"boom_bap": 3, "jazz": 2, "jazz_rap": 1},
    "Timberline": {"rnb": 2, "club": 2, "funk": 1},
    "Just Flame": {"soul": 3, "gospel": 1, "boom_bap": 1},
    "Razor": {"boom_bap": 2, "memphis": 1, "soul": 1},
    "Hitt Kid": {"trap": 2, "rnb": 1, "rap": 1},
    "No Alias": {"soul": 2, "boom_bap": 2, "jazz_rap": 1},
    "DJ Light Green": {"trap": 3, "emo_rap": 1},
    "Well Damn": {"club": 2, "trap": 2},
    "Tenth Wonder": {"soul": 3, "boom_bap": 2, "rnb": 1},
    "DJ Hint": {"soul": 2, "funk": 2, "boom_bap": 2},
    "Memphis": {"memphis": 3, "trap": 1},
    "Crunk": {"trap": 3, "club": 1},
    "Organized Noize": {"soul": 2, "funk": 2, "rnb": 2},
    "Houston Screw": {"trap": 2, "rnb": 1, "soul": 1, "memphis": 1},
    "Emo Hip Hop": {"emo_rap": 3, "rock": 1},
    "Acid Rap Detroit": {"rock": 2, "memphis": 1, "boom_bap": 1},
    "Acid Rap Bright": {"jazz_rap": 2, "funk": 1, "soul": 1},
    "Horror Rap": {"memphis": 3, "boom_bap": 1},
    "Wonky": {"jazz_rap": 2, "lofi": 2, "funk": 1},
    "Trip Hop": {"trip_hop": 3, "lofi": 1},
    "Baltimore Club": {"club": 3},
    "Miami Bass": {"club": 3, "funk": 1},
    "New Orleans Bounce": {"club": 2, "trap": 1, "funk": 1},
    "G-Funk": {"gfunk": 3, "funk": 2},
    "Reggaeton Alt": {"latin": 3},
    "Detroit": {"boom_bap": 2, "jazz_rap": 1, "soul": 1},
    "Plug": {"emo_rap": 2, "trap": 2, "rnb": 1},
    "Chiptune": {"club": 1, "funk": 1, "rap": 1},
}
# an identity not named above leans by its chord_family
FAMILY_STYLES = {
    "soul_jazz": {"soul": 2, "jazz_rap": 2, "boom_bap": 1},
    "dark": {"trap": 2, "memphis": 1, "emo_rap": 1},
    "grit": {"boom_bap": 3, "rap": 1},
    "dreamy": {"lofi": 2, "rnb": 2, "emo_rap": 1},
    "bright_funk": {"funk": 2, "club": 2, "gfunk": 1},
}
DEFAULT_STYLES = {"rap": 2, "soul": 1, "trap": 1}

_T = None


def tables():
    global _T
    if _T is None:
        try:
            _T = json.loads(TABLES.read_text())["styles"]
        except (OSError, ValueError, KeyError):
            _T = {}
    return _T


def styles_for(who, sig=None, free=False):
    """{style: weight} for this identity, only styles the table has."""
    have = tables()
    if free:
        return {s: 1 for s in have}
    want = (STYLE_FOR.get(who)
            or FAMILY_STYLES.get((sig or {}).get("chord_family"))
            or DEFAULT_STYLES)
    got = {s: w for s, w in want.items() if s in have}
    return got or {s: w for s, w in DEFAULT_STYLES.items() if s in have}


def _pick(rng, weighted):
    items = list(weighted)
    tot = sum(w for _, w in items)
    r = rng.random() * tot
    for k, w in items:
        r -= w
        if r <= 0:
            return k
    return items[-1][0]


def _real(tab, rng):
    # i-VI-i7 is really a two-chord loop: one root, one chord
    rows = [(lp, c ** FLATTEN * (SHORT_W if len(lp) == 2 else 1))
            for lp, c in tab["loops"]
            if len({x.split(":")[0] for x in lp}) == len(lp)]
    return list(_pick(rng, rows)) if rows else None


def _new(tab, rng, tries=40):
    nxt = tab["next"]
    starts = {}
    for lp, c in tab["loops"]:
        starts[lp[0]] = starts.get(lp[0], 0) + c
    if not starts:
        return None
    for _ in range(tries):
        size = _pick(rng, SIZES)
        seq = [_pick(rng, starts.items())]
        while len(seq) < size:
            used = {s.split(":")[0] for s in seq}
            opts = [(b, c ** 0.7) for b, c in nxt.get(seq[-1], {}).items()
                    if b.split(":")[0] not in used]
            if not opts:
                break
            seq.append(_pick(rng, opts))
        if len(seq) == size and seq[0] in nxt.get(seq[-1], {}):
            return seq
    return None


def generate(styles, mode, rng):
    """One loop for a key in `mode`: {"style", "made": "real"|"new",
    "seen": songs that play it (real only), "chords": [[offset, quality]]}.
    None if the table is missing."""
    styles = {s: w for s, w in styles.items() if s in tables()}
    if not styles:
        return None
    style = _pick(rng, styles.items())
    fam = mode_family(mode)
    tab = tables()[style].get(fam) or next(iter(tables()[style].values()))
    made = "real" if rng.random() < REAL_P else "new"
    seq = _real(tab, rng) if made == "real" else _new(tab, rng)
    if not seq:
        made, seq = "real", _real(tab, rng)
    seen = dict((tuple(lp), c) for lp, c in tab["loops"]).get(tuple(seq))
    chords = [[int(c.split(":")[0]), c.split(":")[1]] for c in seq]
    return {"style": style, "made": made, "seen": seen, "chords": chords}


if __name__ == "__main__":
    r = random.Random(7)
    for who in ("Cutz", "Doc Day", "Night Metro", "G-Funk", "Sunday Chop",
                "Baltimore Club", "Reggaeton Alt", "Plug"):
        g = generate(styles_for(who), "minor", r)
        assert g and 2 <= len(g["chords"]) <= 4, g
        print(who, g)
