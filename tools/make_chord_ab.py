"""Audition the chord PERFORMANCE grammar: same beat, chords off vs on.

One variable only. Both versions share the identity's config, its kit, its
composed drum bars and its variant seed — the ONLY difference is whether
the preset's top-level `chord_grammar` key is present. So anything you
hear is the chord layer, not a different beat.

Why its own script instead of make_legend_newbuild.py: that one auditions
a config BACKUP against the live config and needs a backup file to diff.
There is no backup here — the grammar is a new key, and "off" means the
key removed, which is a one-line toggle rather than a two-config compare.

Nothing here is confirmed by measurement. The numbers printed are a sanity
check that the two renders actually differ; the verdict is his ear.

    .venv/bin/python tools/make_chord_ab.py --name "Swish Beatz"
"""
from __future__ import annotations

import argparse
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
from crew import (CREW, build_kit, lock_stamps, normalize_preset,   # noqa
                  render_crew_beat)
from make_drum_beats import build_shots                             # noqa
from make_drum_loops import write_wav24                             # noqa
from make_legend_newbuild import band_db                            # noqa
from pattern_gen import compose                                     # noqa

# _build_chords reads these two directly. render_crew_beat does NOT build
# chords on its own — the chord audio is put into `kit` beforehand — which
# is why the first cut of this bench rendered two byte-identical files and
# the "did the grammar fire" check below exists at all.
CHORDS = {"chords": True, "chord_feel": None}

NJUDGE = 2      # beats rendered off-vs-on
NSCAN = 24     # variants tried before giving up on finding chorded ones

READ_ME = """WHAT THIS IS

{name}, four files: two beats, each rendered twice.

    "a chords OFF"  - the chords as they have always been
    "b chords ON"   - the same beat with the new chord performance

Everything else is identical - same drums, same samples, same key, same
chords. The only thing that changed is HOW the chords are played.

WHAT CHANGED

Before today the chords could do two things: hold one long block, or run
straight up the notes, one per eighth, forever. No rests, no swing, dead
centre, one volume. {name} was on the held block.

Now they can play stabs (short chord hits on chosen beats), comp (chords
answering the drums, in the gaps), a real arpeggio (up, down, up-down,
broken, with rests), or a pad that breathes instead of just sitting there.
The hits are also loud or quiet depending on where they land, they can
sit slightly off dead centre instead of straight up the middle, and they
land a hair loose rather than exactly on the grid.

{name} is the first and only one. Nobody else changed - the other
twenty-two identities render exactly as they did yesterday.

WHAT TO LISTEN FOR

    Do the chords have a RHYTHM now, or do they just sound busy?
    Do they fight the drums, or answer them?
    Is anything too loud, too quiet, or too often?

If "on" is worse, say so - the whole thing is one key in one config file
and comes straight back out.

{rows}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    name = a.name
    if name not in CREW:
        raise SystemExit("no identity named %r" % name)
    live = CREW[name]
    if not live.get("chord_grammar"):
        raise SystemExit(
            "%r has no chord_grammar key, so there is nothing to A/B: "
            "both versions would render identically." % name)

    on = normalize_preset(json.loads(json.dumps(live)))
    off = normalize_preset(json.loads(json.dumps(live)))
    off.pop("chord_grammar", None)

    desk = Path(os.path.expanduser(
        "~/Desktop/Homeroom Auditions/Homeroom %s CHORD GRAMMAR %s" % (name, date.today())))
    # Checked BEFORE rendering: rmtree does not go to the Trash, and this
    # exact pattern deleted an approved batch on 2026-09-05.
    if desk.exists() and not a.force:
        raise SystemExit(
            "%s\nalready exists and may be a batch he already has.\n"
            "Move it aside, or re-run with --force if it is disposable."
            % desk)

    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="chord-ab-"))

    def _one(v, base, seed_q):
        """One version of one beat. `seed_q` is the ALREADY-composed beat,
        copied per version so both sides play the same bars — compose()
        re-rolls from a persisted history, so composing twice would hand
        back two different beats wearing an A/B label."""
        q = normalize_preset(json.loads(json.dumps(seed_q)))
        for k in ("chord_grammar",):
            q.pop(k, None)
            if k in base:
                q[k] = json.loads(json.dumps(base[k]))
        kit, sources = build_kit(shots, name, stamps[name][1], variant=v,
                                 avoid=set(avoid), preset=q)
        vnotes = []
        _midi, harm = bm._build_chords(q, kit, sources, v, dict(CHORDS),
                                       vnotes)
        return q, kit, harm, vnotes

    rows, made, fired = [], 0, 0
    for v in range(NSCAN):
        if made >= NJUDGE:
            break
        seed_q = json.loads(json.dumps(on))
        compose(seed_q, name, v)
        bm.vary_preset(seed_q, v, CREW[name]["num"], tempo_locked=True)
        renders = {}
        for tag, base in (("a chords OFF", off), ("b chords ON", on)):
            q, kit, harm, _vn = _one(v, base, seed_q)
            if not harm:
                renders = {}
                break                       # this variant got no chords
            L, R, got = render_crew_beat(name, kit, preset=q)
            renders[tag] = (q, L, R, got, harm)
        if not renders:
            continue
        made += 1
        ref = np.asarray(renders["a chords OFF"][1])
        for tag, (q, L, R, got, harm) in renders.items():
            La = np.asarray(L)
            fn = "%s %dbpm beat %d %s.wav" % (name, q["bpm"], v, tag)
            write_wav24(scratch / fn, L, R)
            rows.append("    %-46s LUFS %6.2f  mids %6.2f"
                        % (fn, got, band_db(L, R, 200.0, 4000.0)))
            print(rows[-1])
            if tag.startswith("b"):
                d = (float("inf") if len(La) != len(ref)
                     else float(np.abs(La - ref).max()))
                print("      key %s | differs from OFF by %.4f peak"
                      % (harm.get("key", "?"), d))
                fired += d > 0
                if d == 0.0:
                    print("      *** IDENTICAL — the grammar did not "
                          "fire; do NOT hand this over")
    if not made:
        raise SystemExit("no variant in 0..%d got a chord lane at all — "
                         "nothing to audition." % NSCAN)
    if not fired:
        raise SystemExit("every pair rendered identically: the grammar is "
                         "not reaching the render. Fix that before "
                         "handing him anything.")

    desk.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, desk / f.name)
    (desk / "READ ME.txt").write_text(
        READ_ME.format(name=name, rows="\n".join(rows)))
    print("\n%s\n%d files." % (desk, len(list(desk.glob('*')))))


if __name__ == "__main__":
    main()
