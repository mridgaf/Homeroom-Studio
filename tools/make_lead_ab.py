"""Audition LEAD (2026-10-19): same beat, old lead rules vs new.

Both versions share the identity, kit, drums, chords, bass groove, melody
stamp and variant seed. The only difference is the preset's `lead_flow`:
  OLD = a lead on 45% of beats; on a plain 7th chord the 7th only played
        when the rare 3rd part did
  NEW = a lead on 25% of beats (owner pick); the lead keeps the 7th
        (guide tones, Open Music Theory + Berklee)

Two kinds of pair, so both changes can be heard:
  "lead gone"  - OLD rolled a lead, NEW plays the plain chord stack
  "keeps 7th"  - both have a lead over a 7th chord; NEW's lead plays it

    .venv/bin/python tools/make_lead_ab.py
"""
from __future__ import annotations

import json
import os
import random
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

import bass_rhythm                                                  # noqa
import beat_machine as bm                                           # noqa
import harmony                                                      # noqa
import melody_rhythm                                                # noqa
from crew import (CREW, build_kit, lock_stamps, normalize_preset,   # noqa
                  render_crew_beat)
from groove import OWNER_TASTE                                      # noqa
from make_drum_beats import build_shots                             # noqa
from make_drum_loops import write_wav24                             # noqa
from pattern_gen import compose, free_beat                          # noqa

WHO = ("Sunday Chop", "Otto Grit", "Cutz", "Chrome Dial", "Glass Cat",
       "Half Light", "Kane East", "Timberline", "G-Funk")
WANT = {"lead gone": 4, "keeps 7th": 4}
NSCAN = 80
SEVENTH = re.compile(r"7")          # m7, maj7, 7 -- a chord with a 7th

READ_ME = """LEAD - OLD vs NEW

Each beat is rendered twice:
    "a OLD" - the lead the way it was this morning.
    "b NEW" - the same beat with today's lead rules.

Same drums, chords, bass, samples, DJ. Only the lead changed.

TWO KINDS OF PAIR
  lead gone  - OLD had a lead part (colour notes above the chords).
               NEW plays the chords as one plain stack, no lead.
               (Leads now on ~25% of beats, was 45% - your pick.)
  keeps 7th  - both have a lead, over 7th chords (like Am7).
               OLD's lead played only the 3rd; the 7th mostly vanished.
               NEW's lead plays the 3rd AND the 7th (music theory:
               those two notes carry a 7th chord).

WHAT TO LISTEN FOR
  lead gone:  more room on top, or too bare?
  keeps 7th:  richer / jazzier, or too busy? Any note that clashes?

If a beat also has the answer melody, it may sit an octave lower on
NEW "lead gone" beats (it always sits above the top chord part).

Beats made BEFORE today are not affected, even if you rebuild them.

THE FILES
{rows}
"""


def _roll(v):
    """The part-count roll's one uniform draw (same draw both sides)."""
    return random.Random(v * 617 + 5).random()


def _has_lead(harm):
    return any("(lead)" in str(n) for n in harm["voice_names"].values())


def main():
    force = "--force" in sys.argv
    desk = Path(os.path.expanduser(
        "~/Desktop/Homeroom Auditions/Homeroom LEAD %s" % date.today()))
    if desk.exists() and not force:
        raise SystemExit("%s already exists. Move it aside, or re-run with "
                         "--force if it is disposable." % desk)
    old_cut = OWNER_TASTE["melody_part_weights"][0]
    new_cut = OWNER_TASTE["lead_part_weights"][0]
    print("Scanning library for one-shots...")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="lead-ab-"))
    rows, got = [], {k: 0 for k in WANT}
    dirs0 = dict(bm.parse_directions(""), chords=True)
    for idx, name in enumerate(WHO * 2):
        if all(got[k] >= WANT[k] for k in WANT):
            break
        live = normalize_preset(json.loads(json.dumps(CREW[name])))
        base = 4000 + 197 * idx
        for v in range(base, base + NSCAN):
            u = _roll(v)
            kind = ("lead gone" if old_cut <= u < new_cut
                    else "keeps 7th" if u >= new_cut else None)
            if kind is None or got[kind] >= WANT[kind] or free_beat(v):
                continue
            seed_q = json.loads(json.dumps(live))
            compose(seed_q, name, v)
            bm.vary_preset(seed_q, v, CREW[name]["num"], tempo_locked=True)
            seed_q["chord_flow"] = harmony.FLOW_VERSION
            seed_q["bass_flow"] = bass_rhythm.FLOW_VERSION
            seed_q["melody_flow"] = melody_rhythm.FLOW_VERSION
            bm._pair_kick(seed_q, False, True)
            renders = {}
            for tag, flow in (("a OLD", False), ("b NEW", True)):
                q = normalize_preset(json.loads(json.dumps(seed_q)))
                q.pop("lead_flow", None)
                if flow:
                    q["lead_flow"] = 1
                kit, sources = build_kit(shots, name, stamps[name][1],
                                         variant=v, avoid=set(avoid), preset=q)
                _midi, harm = bm._build_chords(q, kit, sources, v,
                                               dict(dirs0), [])
                renders[tag] = (q, kit, harm)
            ho, hn = renders["a OLD"][2], renders["b NEW"][2]
            if not ho or not hn or not _has_lead(ho):
                continue
            chords = [r["chord"] for r in hn["chords"]]
            if kind == "lead gone" and _has_lead(hn):
                continue
            if kind == "keeps 7th" and not (
                    _has_lead(hn) and any(SEVENTH.search(c)
                                          for c in chords)):
                continue
            outs = {}
            for tag, (q, kit, harm) in renders.items():
                L, R, _ = render_crew_beat(name, kit, preset=q)
                outs[tag] = (q, np.asarray(L), np.asarray(R))
            a, b = outs["a OLD"][1], outs["b NEW"][1]
            if len(a) == len(b) and np.abs(a - b).max() == 0.0:
                print("  %s %d: IDENTICAL, skipped" % (name, v))
                continue
            got[kind] += 1
            for tag, (q, L, R) in outs.items():
                fn = "%s %dbpm beat %d %s.wav" % (name, q["bpm"], v, tag)
                write_wav24(scratch / fn, L, R)
                rows.append("    %-46s %s | %s" % (fn, kind, " ".join(chords)))
                print(rows[-1])
            break
    if not rows:
        raise SystemExit("no pair found - is TBOTC 3 plugged in?")
    desk.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, desk / f.name)
    (desk / "READ ME.txt").write_text(READ_ME.format(rows="\n".join(rows)))
    print("\n%s\n%d files. pairs: %s" % (desk, len(list(desk.glob("*"))),
                                         got))


if __name__ == "__main__":
    main()
