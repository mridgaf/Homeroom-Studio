"""Audition CHORD FLOW (owner 2026-09-26): same beat, flow off vs on.

Both versions share the identity, its kit, its composed drum bars and its
variant seed. The only difference is the preset's `chord_flow` key:
  OFF = the chords as every beat before today got them
  ON  = smooth voicings, varied chord lengths, turnarounds, fewer 1-2
        chord loops, and (genres) the stab/comp/pad playing styles.
Because ON also picks short loops half as often, a pair can land on a
different progression -- that is part of the change, and the READ ME says
which chords each side played.

    .venv/bin/python tools/make_chord_flow_ab.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

import beat_machine as bm                                           # noqa
import harmony                                                      # noqa
from crew import (CREW, build_kit, lock_stamps, normalize_preset,   # noqa
                  render_crew_beat)
from make_drum_beats import build_shots                             # noqa
from make_drum_loops import write_wav24                             # noqa
from pattern_gen import compose, free_beat                          # noqa

WHO = ("Cutz", "Sunday Chop", "Doc Day", "G-Funk", "Trip Hop")
CHORDS = {"chords": True, "chord_feel": None}
NSCAN = 24

READ_ME = """WHAT THIS IS

Five beats, each rendered twice:
    "a OLD"  - the chords the way every beat got them before today
    "b NEW"  - the same beat with CHORD FLOW on

Same drums, same samples, same DJ. Only the chords changed.

WHAT CHORD FLOW CHANGES
  - Chords glide into each other instead of jumping as blocks.
  - Chords don't always change on the same bars any more
    (some hold longer, some repeat back and forth).
  - One- and two-chord loops show up half as often.
  - Short loops sometimes get a quick "turnaround" chord at the end.
  - Genre beats (G-Funk, Trip Hop here) get stabs/comping, not only
    one held pad or one climbing arpeggio.

WHAT TO LISTEN FOR
  - Does NEW have more going on in the chords, without sounding busy?
  - Does anything sound wrong or off-key?
  - Does each DJ still sound like himself?

Beats made BEFORE today are not affected, even if you rebuild them.

Picked for this test: each DJ's own style (no "free" beats), and a NEW
side that uses the new smooth voicing. In normal use 1 beat in 5 still
stacks chords the old way, on purpose, so the old sound stays in the mix.

{rows}
"""



def main():
    force = "--force" in sys.argv
    desk = Path(os.path.expanduser(
        "~/Desktop/Homeroom Auditions/Homeroom CHORD FLOW %s v3" % date.today()))
    if desk.exists() and not force:
        raise SystemExit("%s already exists. Move it aside, or re-run with "
                         "--force if it is disposable." % desk)
    print("Scanning library for one-shots...")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="chord-flow-ab-"))
    rows, fired = [], 0
    for idx, name in enumerate(WHO):
        live = normalize_preset(json.loads(json.dumps(CREW[name])))
        live.pop("chord_flow", None)
        # Each DJ gets its OWN seeds (v1 of this bench gave all five the
        # same seed 0 -- a free beat -- so all five played one progression),
        # skipping free beats (they ignore the DJ) so every pair is in
        # character.
        for v in range(1000 + 137 * idx, 1000 + 137 * idx + NSCAN * 4):
            if free_beat(v):
                continue
            seed_q = json.loads(json.dumps(live))
            compose(seed_q, name, v)
            bm.vary_preset(seed_q, v, CREW[name]["num"], tempo_locked=True)
            renders = {}
            for tag, flow in (("a OLD", False), ("b NEW", True)):
                q = normalize_preset(json.loads(json.dumps(seed_q)))
                if flow:
                    q["chord_flow"] = harmony.FLOW_VERSION
                kit, sources = build_kit(shots, name, stamps[name][1],
                                         variant=v, avoid=set(avoid), preset=q)
                _midi, harm = bm._build_chords(q, kit, sources, v,
                                               dict(CHORDS), [])
                if not harm or not any(r["voice"] for r in harm["chords"]):
                    renders = {}
                    break
                # the NEW side must show the new voicing: skip the 20% of
                # beats that keep the old root-up stacks (READ ME says so)
                if flow and (harm.get("flow") or {}).get("voicing") == "root":
                    renders = {}
                    break
                L, R, got = render_crew_beat(name, kit, preset=q)
                renders[tag] = (q, L, R, got, harm)
            if not renders:
                continue
            ref = np.asarray(renders["a OLD"][1])
            for tag, (q, L, R, got, harm) in renders.items():
                fn = "%s %dbpm beat %d %s.wav" % (name, q["bpm"], v, tag)
                write_wav24(scratch / fn, L, R)
                bars = [r["bar"] for r in harm["chords"]]
                fl = harm.get("flow") or {}
                rows.append("    %-44s %s | %s | chords start on bars %s%s"
                            % (fn, harm["progression"],
                               " ".join(r["chord"] for r in harm["chords"]),
                               bars, " | voicing: %s" % fl["voicing"]
                               if fl else ""))
                print(rows[-1])
                if tag.startswith("b"):
                    La = np.asarray(L)
                    d = (float("inf") if len(La) != len(ref)
                         else float(np.abs(La - ref).max()))
                    fired += d > 0
                    if d == 0.0:
                        print("      *** IDENTICAL - flow did not fire")
            break
    if not rows:
        raise SystemExit("no beat got chords - is the TBOTC 3 drive plugged in?")
    if not fired:
        raise SystemExit("every pair rendered identically: chord flow is not "
                         "reaching the render. Nothing handed over.")
    desk.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, desk / f.name)
    (desk / "READ ME.txt").write_text(READ_ME.format(rows="\n".join(rows)))
    print("\n%s\n%d files." % (desk, len(list(desk.glob('*')))))


if __name__ == "__main__":
    main()
