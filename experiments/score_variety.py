"""LOCKED EVAL HARNESS — do not edit during the autoresearch loop.

Scores a candidate crew_config.json for VARIETY, compose-only (no audio,
no sample library, no touching the owner's real state files). For each
DJ: compose 12 fresh variants from the candidate grammar and measure how
far apart they land — the numeric shadow of the owner's 2026-07-16 rule
("every beat significantly different from the next").

Usage:  python experiments/score_variety.py <candidate_config> [SEED]
Prints METRIC lines for autoresearch.sh.
"""
import copy
import os
import sys
import tempfile
from pathlib import Path

CAND = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0
VARIANTS = 12

os.environ["REASON_VOICE_CONFIG"] = str(Path(CAND).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import pattern_gen                                        # noqa: E402
# never touch the owner's real pattern history
pattern_gen.PAT_HIST = Path(tempfile.mkdtemp()) / "pat.json"

from crew import CREW                                     # noqa: E402
import variety                                            # noqa: E402


def cap(x, hi):
    return min(x, hi)


per_dj = []
seed_hits = 0
guest_hits = 0
total = 0
for name in sorted(CREW):
    kicks, patterns, backbeats, tk_dens, flavors = [], [], set(), [], set()
    for i in range(VARIANTS):
        p = copy.deepcopy(CREW[name])
        notes = pattern_gen.compose(p, name, SEED * 1000 + i)
        total += 1
        if any("groove seed" in n for n in notes):
            seed_hits += 1
        if p.get("_guests"):
            guest_hits += 1
        kicks.append(p["lanes"]["kick"][3][0])
        patterns.append(list(p["lanes"]["kick"][3]))
        bb = next((ln for ln in ("snare", "clap") if ln in p["lanes"]),
                  None)
        if bb:
            backbeats.add(p["lanes"][bb][3][0])
        tk = next((ln for ln in ("hat", "snap") if ln in p["lanes"]),
                  None)
        if tk:
            tk_dens.append(variety.density(p["lanes"][tk][3]))
        flavors.add((p["kit"]["kick"][1],
                     round(sum(p["kit"]["kick"][3]) / 2, 1)
                     if isinstance(p["kit"]["kick"][3], tuple)
                     else round(p["kit"]["kick"][3], 1)))
    d_a = variety.pairwise(kicks, variety.moves)
    d_full = variety.pairwise(patterns, variety.pattern_moves)
    score = (cap(min(d_a), 6.0)
             + 0.5 * (sum(d_a) / len(d_a))
             + 0.5 * (sum(d_full) / len(d_full))
             + 0.5 * cap(len(backbeats), 6)
             + 0.25 * (max(tk_dens) - min(tk_dens) if len(tk_dens) > 1
                       else 0.0)
             + 0.5 * cap(len(flavors), 6))
    per_dj.append(score)

variety_score = sum(per_dj) / len(per_dj)
print("METRIC variety=%.3f" % variety_score)
print("METRIC worst_dj=%.3f" % min(per_dj))
print("METRIC seed_rate=%.3f" % (seed_hits / total))
print("METRIC guest_rate=%.3f" % (guest_hits / total))
