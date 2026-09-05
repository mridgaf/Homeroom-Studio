"""Where every Legend stands in the new-build pass, and what is wrong with
the ones not done yet.

WHY THIS EXISTS. Owner 2026-09-05, after Doc Day's new build landed: "I'll
want this same for all remaining legends. Not in the 9. Create something to
make that easy and clear for each session" — "So you remember."

A fresh session has no memory of which of the twelve have been rebuilt. This
prints it, and prints the specific faults in the ones that haven't, so a
session can pick one up and start work without re-deriving anything.

Read-only. Writes nothing, renders nothing.

    ./.venv/bin/python tools/legend_newbuild.py                 the table
    ./.venv/bin/python tools/legend_newbuild.py --legend "Razor"  one, in full
    ./.venv/bin/python tools/legend_newbuild.py --tags          add the
        tag audit (needs TBOTC 3 mounted — it scans the sample library)

STAGE comes from legend_newbuild_status.json, which is hand-kept because
the last stage is his ear and nothing can derive that. Everything in the
CHECKS column is read live off legends_config.json, so it cannot go stale.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONFIG = ROOT / "legends_config.json"
STATUS = ROOT / "legend_newbuild_status.json"

# Words in a `listen` line that mean the owner stated an ABSOLUTE. A rule
# written as NEVER is an invariant, not a weight — see the
# hard-rule-invariant skill. These are what a session must find a choke
# point for before calling a legend done.
ABSOLUTES = ("never", "always", "no matter what", "zero ", "dead straight",
             "locked", "completely", "every ")


def legends():
    d = json.loads(CONFIG.read_text())
    return {n: p for n, p in d.items() if isinstance(p, dict)}


def status():
    if not STATUS.exists():
        return {}
    return json.loads(STATUS.read_text())


def checks(name, p):
    """What is verifiably true about this legend's config, right now."""
    out = []
    if not p.get("own_soundbank"):
        out.append("open sound bank still on (taste tags are dead code)")
    note = p.get("_research_note") or ""
    if "NEW BUILD" not in note.upper():
        out.append("no new-build research note")
    backups = sorted(ROOT.glob("legends_config.pre-*.json"))
    slug = name.lower().replace(" ", "-")
    if not any(slug in b.name.lower() for b in backups):
        out.append("no 'before' backup file to A/B against")
    return out


def absolutes(p):
    line = (p.get("listen") or "").lower()
    return [w.strip() for w in ABSOLUTES if w in line]


def tag_audit(name, p):
    """How many real samples each lane's taste tags actually match.

    This is the check that found the Doc Day fault: his kick tags
    punch/knock/deep matched ONE file in the whole library, and `boom`
    matched three of which two were 808s. Tags match FILENAMES, not intent
    — a word that reads right in a description can match nothing, or match
    exactly the thing you were trying to avoid."""
    sys.path.insert(0, str(Path(__file__).parent))
    from make_drum_beats import build_shots
    shots = build_shots()
    rows = []
    for lane, spec in (p.get("kit") or {}).items():
        if not isinstance(spec, (list, tuple)) or len(spec) < 3:
            continue
        role, wants = spec[0], spec[2]
        if not isinstance(wants, list) or not wants:
            continue
        pool = shots.get(role, [])
        per = {w: sum(1 for e in pool if w in e["name"].lower())
               for w in wants}
        rows.append((lane, per, len(pool)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--legend")
    ap.add_argument("--tags", action="store_true")
    a = ap.parse_args()

    ros, st = legends(), status()
    if a.legend:
        if a.legend not in ros:
            raise SystemExit("no legend named %r. Roster: %s"
                             % (a.legend, ", ".join(ros)))
        ros = {a.legend: ros[a.legend]}

    print()
    for name, p in ros.items():
        s = st.get(name, {})
        stage = s.get("stage", "not started")
        print("%-12s  %s" % (name, stage.upper()))
        if s.get("date"):
            print("              %s%s" % (s["date"],
                  "  — " + s["verdict"] if s.get("verdict") else ""))
        if a.legend or stage == "not started":
            print("    listen:  %s" % (p.get("listen") or "(none)"))
            ab = absolutes(p)
            if ab:
                print("    ABSOLUTES in his own words: %s" % ", ".join(ab))
                print("             each one needs a choke point that "
                      "REFUSES, not a weight")
            for c in checks(name, p):
                print("    todo:    %s" % c)
            if s.get("notes"):
                print("    note:    %s" % s["notes"])
        if a.tags:
            for lane, per, n in tag_audit(name, p):
                bad = [w for w, c in per.items() if c == 0]
                print("    tags %-6s %-34s pool %d%s"
                      % (lane, ", ".join("%s=%d" % kv for kv in per.items()),
                         n, "   DEAD: " + ",".join(bad) if bad else ""))
        print()

    # counted over the WHOLE roster, never the filtered view — this said
    # "0 of 12" while looking at one not-started legend.
    every = legends()
    done = sum(1 for n in every if st.get(n, {}).get("stage") == "confirmed")
    print("%d of %d legends confirmed." % (done, len(every)))
    print("Next: pick one 'not started', read the skill "
          "(.claude/skills/legend-new-build/SKILL.md).")


if __name__ == "__main__":
    main()
