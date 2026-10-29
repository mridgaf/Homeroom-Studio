"""Genre bass-line GENERATOR (owner 2026-10-29: "one for chords and one for
bass lines. So it can generate different genres").

Writes a fresh two-bar bass pattern per chord slot in the SAME format as
bass_patterns.json (`bars` = when + how hard, `roles` = which note), so
bass_rhythm._pattern_hits plays it exactly like a library entry: root,
fifth, octave, third, seventh, scale steps, a chromatic approach (`a`) or
the next chord's root played early (`n`) into the change.

Each style is a recipe, not a list of finished patterns: which 16ths the
bass likes (`w`), how many notes a bar (`hits`), which notes it reaches
for (`roles`), how often it walks into the next chord (`turn`), how many
of the in-between notes are ghosts (`ghost`). Steps where the kick hits
weigh KICK_PULL times more, so bass and kick still move together.
The numbers are Claude's starting points from how each style is played;
tune them by ear.
"""
from __future__ import annotations

import random

KICK_PULL = 2.0
STYLES = {
    "boom_bap": dict(w=[10, 0, 1, 3, 2, 0, 2, 5, 3, 0, 5, 4, 1, 0, 4, 2],
                     hits=(1, 3), gap=2, turn=0.5, ghost=0.15,
                     roles={"R": 5, "8": 2, "5": 2, "L": 1, "d": 1}),
    "jazz": dict(w=[10, 0, 1, 0, 6, 0, 2, 1, 6, 0, 2, 1, 6, 0, 3, 1],
                 hits=(2, 4), gap=2, turn=0.7, ghost=0.1,
                 roles={"3": 3, "5": 3, "u": 2, "d": 2, "7": 1, "R": 1}),
    "soul": dict(w=[10, 0, 1, 2, 2, 0, 5, 2, 6, 0, 3, 2, 2, 0, 5, 2],
                 hits=(2, 4), gap=2, turn=0.6, ghost=0.15,
                 roles={"R": 3, "5": 3, "8": 2, "u": 2, "3": 1}),
    "funk": dict(w=[10, 1, 2, 6, 2, 1, 6, 6, 2, 1, 6, 6, 2, 1, 5, 4],
                 hits=(3, 6), gap=1, turn=0.4, ghost=0.35,
                 roles={"R": 4, "8": 4, "5": 2, "7": 1}),
    "gfunk": dict(w=[10, 0, 1, 4, 1, 0, 5, 4, 3, 0, 5, 3, 1, 0, 5, 3],
                  hits=(2, 4), gap=2, turn=0.5, ghost=0.25,
                  roles={"R": 4, "8": 3, "5": 2, "d": 1}),
    "trap": dict(w=[10, 0, 0, 2, 0, 0, 3, 1, 2, 0, 4, 3, 0, 0, 2, 1],
                 hits=(0, 2), gap=3, turn=0.3, ghost=0.0,
                 roles={"R": 6, "L": 1, "d": 1, "8": 1}),
    "club": dict(w=[6, 0, 8, 0, 3, 0, 8, 0, 4, 0, 8, 0, 3, 0, 8, 1],
                 hits=(3, 5), gap=2, turn=0.3, ghost=0.1,
                 roles={"R": 5, "8": 3, "5": 1}),
    "latin": dict(w=[10, 0, 0, 8, 4, 0, 3, 0, 8, 0, 0, 6, 4, 0, 2, 0],
                  hits=(2, 3), gap=2, turn=0.3, ghost=0.1,
                  roles={"R": 4, "5": 2, "8": 1}),
    "lofi": dict(w=[10, 0, 1, 1, 1, 0, 2, 4, 3, 0, 4, 2, 1, 0, 2, 2],
                 hits=(1, 2), gap=2, turn=0.4, ghost=0.1,
                 roles={"R": 3, "5": 2, "3": 1, "u": 1}),
    "rock": dict(w=[10, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0],
                 hits=(3, 7), gap=2, turn=0.3, ghost=0.0,
                 roles={"R": 6, "5": 1, "8": 1}),
}
STYLE_OF = {"rap": "boom_bap", "jazz_rap": "jazz", "rnb": "soul",
            "gospel": "soul", "drill": "trap", "emo_rap": "trap",
            "memphis": "trap", "trip_hop": "lofi"}


def recipe(style):
    return STYLES.get(STYLE_OF.get(style, style), STYLES["boom_bap"])


def _bar(r, rng, kick, last):
    hits = {0: ("X", "R")}
    w = [r["w"][i] * (KICK_PULL if kick and kick[i] in "Xx" else 1)
         for i in range(16)]
    want = rng.randint(*r["hits"])
    roles = list(r["roles"].items())
    for _ in range(40):
        if len(hits) - (0 in hits) >= want:
            break
        st = rng.choices(range(16), weights=[x + 1e-9 for x in w])[0]
        if any(abs(st - h) < r["gap"] for h in hits):
            continue
        ch = "." if st % 2 and rng.random() < r["ghost"] else (
            "x" if st % 4 == 0 or st % 2 == 0 else "o")
        hits[st] = (ch, rng.choices([k for k, _ in roles],
                                    weights=[v for _, v in roles])[0])
    if last and rng.random() < r["turn"]:
        st = rng.choice((14, 15))
        if all(abs(st - h) >= 2 for h in hits if h != st):
            hits[st] = ("x", rng.choice("an"))
    return ("".join(hits[i][0] if i in hits else "-" for i in range(16)),
            "".join(hits[i][1] if i in hits else "-" for i in range(16)))


def make(style, rng, kick_bars=None):
    """A two-bar entry {"name", "tags", "bars", "roles"} for `style`."""
    r = recipe(style)
    kb = [k for k in (kick_bars or []) if isinstance(k, str) and len(k) == 16]
    a = _bar(r, rng, kb[0] if kb else None, last=False)
    b = _bar(r, rng, kb[1 % len(kb)] if kb else None, last=True)
    return {"name": "gen %s" % style, "tags": ["gen", style],
            "bars": [a[0], b[0]], "roles": [a[1], b[1]]}


if __name__ == "__main__":
    rng = random.Random(3)
    for st in list(STYLES) + ["rap", "memphis"]:
        for _ in range(50):
            e = make(st, rng, ["X-----x---X-----"])
            for bar, role in zip(e["bars"], e["roles"]):
                assert len(bar) == len(role) == 16
                assert set(bar) <= set("Xxo.-")
                assert all((x == "-") == (y == "-") for x, y in zip(bar, role))
            assert "a" not in e["roles"][0] and "n" not in e["roles"][0]
            assert e["bars"][0][0] == e["bars"][1][0] == "X"
        print(st, e["bars"], e["roles"])
