"""Variety scorer: numbers for the owner's #1 standing rule (2026-07-16,
"every beat significantly different from the next, no matter the DJ").

Ears are still the QA department — but drift toward sameness used to be
invisible until he heard a whole batch. This module measures what he was
hearing, straight from the saved recipes (<beats root>/.recipes/NN.json,
the ground truth of what actually rendered):

- KICK DISTANCE: pairwise moves between rendered kick lines (bar A and
  the whole 8), per DJ. The engine's own guard promises >=3 between
  consecutive rolls; the scorer watches the whole recent window.
- BACKBEAT + TIMEKEEPER SPREAD: do the modes actually vary, or has one
  mode quietly taken over?
- SAMPLE OVERLAP: how much of the kit two beats share. Sample-swapping
  alone is NOT variety, but full-kit repeats are anti-variety.
- FLAVOR STREAKS: the kick-flavor runs the streak-breaker exists to stop.
- TEMPO SPREAD and GUEST RATE: the arrangement-level variety signals.
- BAR SWING (optional, reads the WAVs): the rise-and-fall floor.

Read-only over the library. Used three ways: the CLI report below, the
regression tests in tests/test_variety.py (compose N variants, assert the
floors hold), and the autoresearch loop's objective function.

Run:  ./.venv/bin/python tools/variety.py [--dj "Otto Grit"] [--last 12]
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

ROOT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))

# Floors: below these, a window of beats reads as "the same beat slightly
# changed". Matched to the engine's own guards so a green report means the
# guards are actually doing their job across sessions, not just per-roll.
FLOORS = {
    # 2026-07-21: these are REPORT floors only — the engine no longer
    # enforces a kick distance (variety comes from composition, not
    # rejection), so a flag here is a nudge to tune grammars/configs.
    "kick_min": 3.0,
    "kick_mean": 4.5,       # the window as a whole should sit well apart
    "kit_overlap_max": 0.5, # two beats sharing >half their kit = repeat
    "flavor_streak_max": 2, # the streak-breaker's promise
    "swing_min": 2.5,       # bar-RMS rise and fall (sparse-bed floor)
}


# ------------------------------------------------------------ primitives


def moves(a, b):
    """Distance between two bar strings in 'moves' (the engine's unit:
    one step changed). Different grids don't compare — that's already
    maximal variety, so it scores as a big distance."""
    if len(a) != len(b):
        return max(len(a), len(b))
    return sum(x != y for x, y in zip(a, b))


def pattern_moves(bars_a, bars_b):
    """Whole-pattern distance: mean per-bar moves across the 8 bars."""
    n = min(len(bars_a), len(bars_b))
    if n == 0:
        return 0.0
    return sum(moves(bars_a[i], bars_b[i]) for i in range(n)) / n


def pairwise(values, dist):
    """All pairwise distances in a list. Empty when <2 values."""
    out = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            out.append(dist(values[i], values[j]))
    return out


def longest_streak(seq):
    """Longest run of equal consecutive values."""
    best = run = 1 if seq else 0
    for prev, cur in zip(seq, seq[1:]):
        run = run + 1 if cur == prev else 1
        best = max(best, run)
    return best


def density(bars):
    """Mean hits per bar for a lane's bar list."""
    if not bars:
        return 0.0
    return sum(sum(c != "-" for c in b) for b in bars) / len(bars)


# ------------------------------------------------------------ recipe I/O


def load_recipes(root=ROOT, dj=None, last=12):
    """Newest-first recipes, optionally filtered to one DJ's solo beats
    (collabs count for the first-named DJ, same as the folder rule)."""
    d = Path(root) / ".recipes"
    if not d.exists():
        return []
    recs = []
    for f in sorted(d.glob("*.json"), key=lambda p: int(p.stem)
                    if p.stem.isdigit() else -1, reverse=True):
        try:
            r = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if dj is None or (r.get("names") and r["names"][0] == dj):
            recs.append(r)
        if len(recs) >= last:
            break
    return recs


def _kick_bars(rec):
    lanes = rec.get("preset", {}).get("lanes", {})
    if "kick" not in lanes:
        return None
    return list(lanes["kick"][3])


def _kit_paths(rec):
    return {p for ln, p in rec.get("kit_paths", {}).items()
            if p and not ln.startswith("stamp")}


def _flavor(rec):
    """The kick's rendered flavor: (must-word, rough choke tier)."""
    spec = rec.get("kit_spec", {}).get("kick")
    if not spec:
        return None
    must, secs = spec[1], spec[3]
    if isinstance(secs, (list, tuple)):
        secs = sum(secs) / len(secs)
    tier = "long" if secs >= 1.2 else ("mid" if secs >= 0.6 else "short")
    return (must, tier)


# --------------------------------------------------------------- scoring


def score_recipes(recs):
    """Variety metrics over a newest-first recipe window. Returns a dict
    of numbers plus 'flags': plain-words problems, empty when healthy."""
    out = {"n": len(recs), "flags": []}
    if len(recs) < 2:
        return out

    kicks = [k for k in (_kick_bars(r) for r in recs) if k]
    if len(kicks) >= 2:
        d_a = pairwise([k[0] for k in kicks], moves)
        d_full = pairwise(kicks, pattern_moves)
        out["kick_min"] = float(min(d_a))
        out["kick_mean"] = round(sum(d_a) / len(d_a), 2)
        out["kick_pattern_mean"] = round(sum(d_full) / len(d_full), 2)
        if out["kick_min"] < FLOORS["kick_min"]:
            out["flags"].append(
                "two kick lines within %d moves of each other"
                % out["kick_min"])
        if out["kick_mean"] < FLOORS["kick_mean"]:
            out["flags"].append("kick lines cluster (mean %.1f moves, "
                                "floor %.1f)" % (out["kick_mean"],
                                                 FLOORS["kick_mean"]))

    kits = [_kit_paths(r) for r in recs]
    overlaps = []
    for a, b in zip(kits, kits[1:]):
        if a and b:
            overlaps.append(len(a & b) / len(a | b))
    if overlaps:
        out["kit_overlap_max"] = round(max(overlaps), 2)
        out["kit_overlap_mean"] = round(sum(overlaps) / len(overlaps), 2)
        if out["kit_overlap_max"] > FLOORS["kit_overlap_max"]:
            out["flags"].append("consecutive beats share %d%% of their "
                                "kit" % round(out["kit_overlap_max"] * 100))

    flavors = [f for f in (_flavor(r) for r in recs) if f]
    if len(flavors) >= 3:
        # recipes are newest-first; streaks read the same either way
        out["flavor_streak"] = longest_streak(flavors)
        out["flavor_kinds"] = len(set(flavors))
        if out["flavor_streak"] > FLOORS["flavor_streak_max"]:
            out["flags"].append("one kick flavor ran %d beats in a row"
                                % out["flavor_streak"])

    tempos = [r.get("bpm") for r in recs if r.get("bpm")]
    if tempos:
        out["tempo_spread"] = max(tempos) - min(tempos)

    guests = sum(1 for r in recs
                 if r.get("preset", {}).get("_guests"))
    out["guest_rate"] = round(guests / len(recs), 2)

    hat_d = [density(r["preset"]["lanes"][ln][3])
             for r in recs for ln in ("hat", "snap")
             if ln in r.get("preset", {}).get("lanes", {})]
    if len(hat_d) >= 2:
        out["timekeeper_density_spread"] = round(max(hat_d) - min(hat_d), 1)

    return out


def bar_swing_of(path):
    """Bar-RMS swing of a rendered WAV (same math as the engine's floor).
    Returns None when the file can't be read."""
    import numpy as np
    from make_hiphop_tracks import load_audio
    from make_drum_loops import SR                          # noqa: F401
    x = load_audio(str(path))
    if x is None or not len(x):
        return None
    mono = x.mean(axis=1)
    barlen = len(mono) // 8
    if barlen == 0:
        return None
    prof = [max(-30.0, 20 * np.log10(np.sqrt(
        (mono[i * barlen:(i + 1) * barlen] ** 2).mean()) + 1e-12))
        for i in range(8)]
    return round(max(prof) - min(prof), 1)


def score_dj(root=ROOT, dj=None, last=12, with_audio=False):
    """The report for one DJ (or the whole library when dj is None)."""
    recs = load_recipes(root, dj, last)
    out = score_recipes(recs)
    out["dj"] = dj or "(all)"
    if with_audio:
        swings = []
        for r in recs:
            p = Path(root) / r.get("folder", "") / r.get("file", "")
            if p.exists():
                s = bar_swing_of(p)
                if s is not None:
                    swings.append(s)
        if swings:
            out["swing_min"] = min(swings)
            out["swing_mean"] = round(sum(swings) / len(swings), 1)
            if out["swing_min"] < FLOORS["swing_min"]:
                out["flags"].append("a beat's bar swing sits at %.1f dB "
                                    "(floor %.1f)" % (out["swing_min"],
                                                      FLOORS["swing_min"]))
    return out


def quick_check(root, dj, last=6):
    """The post-render hook: one cheap look at this DJ's recent window.
    Returns a short plain-words warning string, or None when healthy.
    Never raises — a scoring hiccup must not block a render."""
    try:
        out = score_dj(root, dj, last)
        if out.get("flags"):
            return "variety check: " + "; ".join(out["flags"])
    except Exception:
        pass
    return None


# ------------------------------------------------------------------ CLI


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dj", default=None, help="one DJ (default: each)")
    ap.add_argument("--last", type=int, default=12,
                    help="how many recent beats per DJ (default 12)")
    ap.add_argument("--audio", action="store_true",
                    help="also read the WAVs for bar-swing (slower)")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output (for autoresearch)")
    a = ap.parse_args()
    root = Path(os.path.expanduser(a.root))

    from crew import CREW
    djs = [a.dj] if a.dj else sorted(CREW, key=lambda n: CREW[n]["num"])
    reports = [score_dj(root, dj, a.last, with_audio=a.audio)
               for dj in djs]
    if a.json:
        print(json.dumps(reports, indent=1))
        return
    for r in reports:
        if r["n"] < 2:
            print(f"{r['dj']:15s} not enough recent beats ({r['n']})")
            continue
        line = (f"{r['dj']:15s} {r['n']:2d} beats | kick moves "
                f"min {r.get('kick_min', 0):.0f} "
                f"mean {r.get('kick_mean', 0):.1f} | kit overlap "
                f"{r.get('kit_overlap_mean', 0):.0%} | flavors "
                f"{r.get('flavor_kinds', 0)}")
        if "swing_min" in r:
            line += f" | swing min {r['swing_min']:.1f} dB"
        print(line)
        for f in r["flags"]:
            print(f"                !! {f}")
    if not any(r.get("flags") for r in reports):
        print("\nAll healthy — every recent window sits above the floors.")


if __name__ == "__main__":
    main()
