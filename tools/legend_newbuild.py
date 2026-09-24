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
BACKUP = "legends_config.pre-"


def use_genres():
    """--genres (owner 2026-09-24): the genres get the same pass, A-Z, one
    at a time. Same checks, their own config, status file and backups."""
    global CONFIG, STATUS, BACKUP
    CONFIG = ROOT / "genres_config.json"
    STATUS = ROOT / "genre_newbuild_status.json"
    BACKUP = "genres_config.pre-"

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
    # every real note is written "NEW-BUILD <date>" (Doc Day onward), so a
    # bare "NEW BUILD" test reported "no new-build research note" for a
    # legend that had one. Only ever visible on an unconfirmed legend,
    # which is why it survived ten builds. Accept either spelling.
    if "NEW BUILD" not in note.upper().replace("-", " "):
        out.append("no new-build research note")
    backups = sorted(ROOT.glob(BACKUP + "*.json"))
    slug = name.lower().replace(" ", "-")
    if not any(slug in b.name.lower() for b in backups):
        out.append("no 'before' backup file to A/B against")
    return out


def absolutes(p):
    line = (p.get("listen") or "").lower()
    return [w.strip() for w in ABSOLUTES if w in line]


def role_of(p, lane):
    """The bucket a lane actually draws from — the thing a tag is judged
    against, and the thing that is wrong when a word has a home elsewhere."""
    return (p.get("kit") or {}).get(lane, ("?",))[0]


def tag_audit(name, p):
    """How many real samples each lane's taste tags actually match.

    This is the check that found the Doc Day fault: his kick tags
    punch/knock/deep matched ONE file in the whole library, and `boom`
    matched three of which two were 808s. Tags match FILENAMES, not intent
    — a word that reads right in a description can match nothing, or match
    exactly the thing you were trying to avoid.

    It also says WHERE ELSE a dead word lives, because "dead" and "dead in
    this bucket" are different claims and this tool only ever looked in the
    lane's own bucket. That blind spot has now cost twice: Mustang's "Hey!"
    chant asked `fx` for hey/vocal/chant and matched 0 of 356, while the
    `vox` bucket literally holds "Cymatics - Hey Vox" (2026-09-05); and on
    2026-09-06 a build note claimed the library had no horns at all on the
    strength of a drum-bucket search, when the melodic instrument index
    holds 38 brass samples. A word with a real home somewhere else is a
    lane pointed at the wrong bucket — which is a fix — while a word that
    lives nowhere is just a dead word.

    Read the ELSEWHERE column with judgement, not obedience: `crack` in the
    fx bucket is not a snare and moving a snare there would be worse than
    leaving it. It flags candidates; it does not make the call.

    NOT COVERED HERE, and do not read silence as a pass: this walks the
    drum one-shot buckets only. Melodic voices (`chord_source`) live in a
    separate index and are checked against instrument_sampler.VOICES —
    never against GROUP_NAMES, which makes horns/strings/loop/chip all look
    dead when every one of them is real."""
    sys.path.insert(0, str(Path(__file__).parent))
    from make_drum_beats import build_shots
    from flavor_tags import matches as flavor_matches
    shots = build_shots()
    # flavor_match (2026-09-09): if this preset opted in, audit counts
    # reflect what _pick_path will actually do at runtime (synonym-aware
    # matching); every existing legend has no such flag and is audited
    # exactly as before -- see flavor_tags.py for the scope decision.
    use_flavor = bool(p.get("flavor_match"))

    def _hit(w, nm):
        return flavor_matches(w, nm) if use_flavor else w in nm

    rows = []
    for lane, spec in (p.get("kit") or {}).items():
        if not isinstance(spec, (list, tuple)) or len(spec) < 3:
            continue
        role, wants = spec[0], spec[2]
        if not isinstance(wants, list) or not wants:
            continue
        pool = shots.get(role, [])
        per = {w: sum(1 for e in pool if _hit(w, e["name"].lower()))
               for w in wants}
        # for each DEAD word, where does it actually live? Loops are
        # excluded (not one-shot material) and a single stray file is
        # noise, not a home.
        home = {}
        for w, c in per.items():
            if c:
                continue
            found = {b: n for b, n in
                     ((b, sum(1 for e in items if _hit(w, e["name"].lower())))
                      for b, items in shots.items()
                      if b != role and not b.startswith("_"))
                     if n >= 2}
            if found:
                home[w] = found
        rows.append((lane, per, len(pool), home))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--legend")
    ap.add_argument("--tags", action="store_true")
    ap.add_argument("--genres", action="store_true",
                    help="the genre roster instead of the legends")
    a = ap.parse_args()
    if a.genres:
        use_genres()

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
            for lane, per, n, home in tag_audit(name, p):
                bad = [w for w, c in per.items() if c == 0]
                print("    tags %-6s %-34s pool %d%s"
                      % (lane, ", ".join("%s=%d" % kv for kv in per.items()),
                         n, "   DEAD: " + ",".join(bad) if bad else ""))
                for w, found in home.items():
                    where = ", ".join("%s=%d" % kv for kv in
                                      sorted(found.items(),
                                             key=lambda kv: -kv[1]))
                    print("             '%s' is dead in %s but ALIVE in %s"
                          % (w, role_of(p, lane), where))
        print()

    # counted over the WHOLE roster, never the filtered view — this said
    # "0 of 12" while looking at one not-started legend.
    every = legends()
    done = sum(1 for n in every if st.get(n, {}).get("stage") == "confirmed")
    print("%d of %d %s confirmed." % (done, len(every),
                                     "genres" if a.genres else "legends"))
    print("Next: pick one 'not started', read the skill "
          "(.claude/skills/legend-new-build/SKILL.md).")


if __name__ == "__main__":
    main()
