"""Does a DJ's written identity survive the engine?

Built 2026-08-08 after Fast Water (slot 11) came out weaker than Half
Light (slot 10) and the owner noticed. The cause was measurable: every
lane's BARS are rewritten from scratch by pattern_gen.compose() on every
single beat, so any trait written as a bar figure is gone before he hears
it. Traits written into the slots compose() never touches survive 12/12.

This script measures that instead of guessing. For each DJ it composes N
beats and reports:

  INVARIANT   slots compose() must never change (lane roster, LaneFeel
              offsets, pan/gain, bpm, mix flavor, space/alt). Anything
              other than 100% here is an engine BUG, not a design flaw.
  FIGURE      how often the bars declared in crew_config.json actually
              survive composition. Low is EXPECTED and is exactly why a
              bar figure is a bad place to keep an identity — unless the
              lane is listed in the preset's `canon`, which is the
              supported way to pin a figure (the genre roster uses it).
  HOME        how often a composed lane came out in its grammar's
              highest-weighted ("home") mode. This is the real strength
              of a pattern-based trait: a 0.30 home weight means the
              trait shows up about a third of the time, no more.

Usage (from the project root):

    ./.venv/bin/python tools/identity_survival.py
    ./.venv/bin/python tools/identity_survival.py --dj "Fast Water" -n 24
    ./.venv/bin/python tools/identity_survival.py --legends --genres

Reads only. Renders nothing, writes nothing, needs no drive mounted.
"""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import crew                                                  # noqa: E402
from crew import CREW                                        # noqa: E402
from pattern_gen import DEFAULT_STYLE, compose               # noqa: E402

HITS = set("Xxo")

# The slots pattern_gen.compose() is documented never to touch ("Timing
# DNA (pan, gain, LaneFeel) is carried over untouched"). Anything that
# moves here is a bug in the engine, not a weak identity.
MIX_KEYS = ("bpm", "dust", "vinyl", "wow", "sidechain", "drive",
            "kick_dist", "mix_sat")


def _cells(bar):
    return {i for i, c in enumerate(bar) if c in HITS}


def _figure_match(declared, composed):
    """Did the composed bar keep the declared figure? Same grid length and
    every declared hit still present (extra hits are allowed — fills and
    ghosts are supposed to move)."""
    if len(declared) != len(composed):
        return False
    return _cells(declared) <= _cells(composed)


def _home_mode(name, lane):
    spec = ((CREW[name].get("grammar") or {}).get(lane)
            or (DEFAULT_STYLE.get(name, {}).get("grammar") or {}).get(lane))
    if not isinstance(spec, dict) or not spec.get("modes"):
        return None, 0.0
    modes = sorted(spec["modes"], key=lambda mw: -mw[1])
    total = sum(w for _, w in spec["modes"]) or 1.0
    return modes[0][0], modes[0][1] / total


def audit(name, n):
    base = CREW[name]
    canon = set((base.get("canon") or {}).keys())
    rows = {
        "lane roster unchanged": 0,
        "LaneFeel (offset/jitter/swing) unchanged": 0,
        "pan + gain unchanged": 0,
        "tempo + mix flavor unchanged": 0,
        "space + alt unchanged": 0,
    }
    figure = {lane: 0 for lane in base["lanes"]}
    home = {}
    for lane in base["lanes"]:
        mode, weight = _home_mode(name, lane)
        if mode:
            home[lane] = [mode, weight, 0]
    guests, borrows = 0, 0

    for v in range(n):
        p = copy.deepcopy(base)
        notes = compose(p, name, v) or []
        extra = set(p["lanes"]) - set(base["lanes"])
        guests += len(extra)
        borrows += sum(1 for t in notes if "borrowed" in t)

        if set(p["lanes"]) >= set(base["lanes"]):
            rows["lane roster unchanged"] += 1
        if all(p["lanes"][l][2] == base["lanes"][l][2] for l in base["lanes"]):
            rows["LaneFeel (offset/jitter/swing) unchanged"] += 1
        if all(p["lanes"][l][:2] == base["lanes"][l][:2]
               for l in base["lanes"]):
            rows["pan + gain unchanged"] += 1
        if all(p.get(k) == base.get(k) for k in MIX_KEYS):
            rows["tempo + mix flavor unchanged"] += 1
        if p.get("space") == base.get("space") \
                and p.get("alt") == base.get("alt"):
            rows["space + alt unchanged"] += 1

        for lane, (_, _, _, dbars) in base["lanes"].items():
            cbars = p["lanes"][lane][3]
            if cbars and all(_figure_match(dbars[i % len(dbars)], b)
                             for i, b in enumerate(cbars)):
                figure[lane] += 1
        for lane, rec in home.items():
            # compose() records the mode it rolled per lane in its notes,
            # e.g. "hat: rolls32" / "snare: displaced" / "hat: seed:funk"
            tag = "%s: %s" % (lane, rec[0])
            if any(t == tag for t in notes):
                rec[2] += 1

    return rows, figure, home, canon, guests, borrows


def report(names, n):
    print("identity survival — %d composed beats per DJ\n" % n)
    weak_total = []
    for name in names:
        rows, figure, home, canon, guests, borrows = audit(name, n)
        print("=" * 66)
        print("%s   (%s BPM, %s)" % (name, CREW[name].get("bpm"),
                                     CREW[name].get("built", "")))
        print("  INVARIANT — anything below %d/%d is an engine bug" % (n, n))
        for k, hit in rows.items():
            flag = "  <-- BUG" if hit < n else ""
            print("    %3d/%-3d  %s%s" % (hit, n, k, flag))
        print("  FIGURE — declared bars still intact after composing")
        for lane, hit in figure.items():
            pin = "  [canon: pinned]" if lane in canon else ""
            print("    %3d/%-3d  %s%s" % (hit, n, lane, pin))
        if home:
            print("  HOME MODE — composed lane came out in its home mode")
            for lane, (mode, weight, hit) in home.items():
                print("    %3d/%-3d  %s = %s (declared weight %.0f%%)"
                      % (hit, n, lane, mode, weight * 100))
        print("  guest lanes added: %.1f per beat   kick borrowed: %d/%d"
              % (guests / float(n), borrows, n))
        fragile = [l for l, h in figure.items() if h < n * 0.5
                   and l not in canon]
        if fragile:
            weak_total.append((name, fragile))
    if weak_total:
        print("\n" + "=" * 66)
        print("Lanes whose declared figure survives less than half the")
        print("time. If the `listen` line describes one of these, the")
        print("description is promising something he mostly won't hear.")
        print("Fix by moving the trait into an invariant slot, raising")
        print("the grammar's home weight, or pinning the lane in `canon`.")
        for name, lanes in weak_total:
            print("  %-14s %s" % (name, ", ".join(lanes)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dj", action="append", help="one DJ (repeatable)")
    ap.add_argument("-n", "--beats", type=int, default=12)
    ap.add_argument("--legends", action="store_true")
    ap.add_argument("--genres", action="store_true")
    a = ap.parse_args(argv)
    if a.dj:
        names = a.dj
    else:
        names = [n for n in CREW
                 if (n in crew.LEGEND_NAMES and a.legends)
                 or (n in crew.GENRE_NAMES and a.genres)
                 or (n not in crew.LEGEND_NAMES and n not in crew.GENRE_NAMES)]
        names.sort(key=lambda n: CREW[n].get("num", 99))
    missing = [n for n in names if n not in CREW]
    if missing:
        raise SystemExit("not on the roster: %s" % ", ".join(missing))
    report(names, a.beats)


if __name__ == "__main__":
    main()
