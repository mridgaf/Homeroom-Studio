"""Audition BASS GROOVE (2026-10-19): same beat, old bass vs new bass.

Both versions share the identity, its kit, its drum bars, its chords and
its variant seed. The only difference is the preset's `bass_flow` key:
  OLD = one held root per chord (every beat before today)
  NEW = a bass figure per chord (tools/bass_rhythm.py), swung with the kick

Two identities per chord family, at least one genre and one legend. 808
beats are skipped -- they play no bass line (owner rule 2026-09-23).

    .venv/bin/python tools/make_bass_groove_ab.py
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

import bass_rhythm                                                  # noqa
import beat_machine as bm                                           # noqa
import harmony                                                      # noqa
from crew import (CREW, build_kit, lock_stamps, normalize_preset,   # noqa
                  render_crew_beat)
from make_drum_beats import build_shots                             # noqa
from make_drum_loops import SR, write_wav24                         # noqa
from pattern_gen import compose, free_beat                          # noqa

# family -> identities (crew first; a legend/genre where the crew's own
# members of that family are 808 DJs and play no bass line)
WHO = (("soul_jazz", "Sunday Chop"), ("soul_jazz", "Otto Grit"),
       ("grit", "Cutz"), ("grit", "Chrome Dial"),
       ("dreamy", "Glass Cat"), ("dreamy", "Half Light"),
       ("dark", "Kane East"), ("dark", "Timberline"),
       ("bright_funk", "G-Funk"), ("bright_funk", "Baltimore Club"))
NSCAN = 40

SAYS = {
    "hold": "holds the root (the old way, kept as one option)",
    "kick": "locks to the kick drum's hits",
    "fifth": "root on beat 1, the fifth on beat 3",
    "octave": "bounces root / octave in 8ths",
    "walk": "walks in quarter notes, slides a half step into the next chord",
    "push": "hits the next chord's note early (an 8th or 16th before)",
    "funk": "syncopated funk line with ghost notes",
    "pulse": "steady 8th-note pulse with soft off-beats",
}

READ_ME = """BASS GROOVE - OLD vs NEW

Ten beats, each rendered twice:
    "a OLD" - the bass the way every beat got it before today:
              one long note per chord.
    "b NEW" - the same beat with the new bass line.

Same drums, same chords, same samples, same DJ. Only the bass changed.

WHAT THE NEW BASS DOES
Each chord gets a bass "figure" picked from the DJ's style. The figures:
{says}
The new bass also swings with the kick drum, so they move together.
"+tied" means the note before was pushed early into that chord.

WHAT TO LISTEN FOR
  - Does NEW groove more without getting busy or muddy?
  - Any wrong notes? Any notes that sound stretched or chipmunky?
  - Can you hear the quiet ghost notes in the funk lines?
  - Does each DJ still sound like himself?

Beats made BEFORE today are not affected, even if you rebuild them.
808 beats are not affected (the 808 rule stands).

THE FILES (figure per chord, in order)
{rows}
"""


def low_rms_db(L, R, hz=150.0):
    """Level of everything under `hz`, in dB -- how loud the low end is."""
    m = (np.asarray(L) + np.asarray(R)) / 2
    f = np.fft.rfft(m)
    f[np.fft.rfftfreq(len(m), 1.0 / SR) > hz] = 0
    low = np.fft.irfft(f, len(m))
    return 20 * np.log10(np.sqrt(np.mean(low ** 2)) + 1e-12)


def main():
    force = "--force" in sys.argv
    desk = Path(os.path.expanduser(
        "~/Desktop/Homeroom Auditions/Homeroom BASS GROOVE %s" % date.today()))
    if desk.exists() and not force:
        raise SystemExit("%s already exists. Move it aside, or re-run with "
                         "--force if it is disposable." % desk)
    print("Scanning library for one-shots...")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="bass-groove-ab-"))
    rows, lows, fired = [], [], 0
    dirs0 = dict(bm.parse_directions(""), chords=True)
    for idx, (fam, name) in enumerate(WHO):
        live = normalize_preset(json.loads(json.dumps(CREW[name])))
        for v in range(3000 + 151 * idx, 3000 + 151 * idx + NSCAN):
            if free_beat(v) or bm._plays_808(v, dirs0, name, shots):
                continue
            seed_q = json.loads(json.dumps(live))
            compose(seed_q, name, v)
            bm.vary_preset(seed_q, v, CREW[name]["num"], tempo_locked=True)
            seed_q["chord_flow"] = harmony.FLOW_VERSION
            bm._pair_kick(seed_q, False, True)
            renders = {}
            for tag, flow in (("a OLD", False), ("b NEW", True)):
                q = normalize_preset(json.loads(json.dumps(seed_q)))
                q.pop("bass_flow", None)
                if flow:
                    q["bass_flow"] = bass_rhythm.FLOW_VERSION
                kit, sources = build_kit(shots, name, stamps[name][1],
                                         variant=v, avoid=set(avoid), preset=q)
                _midi, harm = bm._build_chords(q, kit, sources, v,
                                               dict(dirs0), [])
                if not harm or not harm.get("bass_file"):
                    renders = {}
                    break
                figs = harm.get("bass_figures")
                # the NEW side must actually move: skip all-hold lines
                if flow and (not figs or all(f.startswith("hold")
                                             for f in figs)):
                    renders = {}
                    break
                L, R, _got = render_crew_beat(name, kit, preset=q)
                renders[tag] = (q, L, R, harm)
            if not renders:
                continue
            ref = np.asarray(renders["a OLD"][1])
            for tag, (q, L, R, harm) in renders.items():
                fn = "%s %dbpm beat %d %s.wav" % (name, q["bpm"], v, tag)
                write_wav24(scratch / fn, L, R)
                figs = harm.get("bass_figures") or ["hold (old)"] * len(
                    harm["chords"])
                low = low_rms_db(L, R)
                lows.append((name, tag, low))
                rows.append("    %-46s %s | %s | %s" % (
                    fn, fam, " ".join(r["chord"] for r in harm["chords"]),
                    ", ".join(figs)))
                print(rows[-1], "| low end %.1f dB" % low)
                if tag.startswith("b"):
                    La = np.asarray(L)
                    d = (float("inf") if len(La) != len(ref)
                         else float(np.abs(La - ref).max()))
                    fired += d > 0
                    if d == 0.0:
                        print("      *** IDENTICAL - bass groove did not fire")
            break
        else:
            print("!! %s: no usable beat in %d seeds" % (name, NSCAN))
    if not rows:
        raise SystemExit("no beat got a bass line - is TBOTC 3 plugged in?")
    if not fired:
        raise SystemExit("every pair rendered identically: the bass groove "
                         "is not reaching the render. Nothing handed over.")
    desk.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, desk / f.name)
    says = "\n".join("    %-7s %s" % (k, s) for k, s in SAYS.items())
    (desk / "READ ME.txt").write_text(READ_ME.format(says=says,
                                                     rows="\n".join(rows)))
    print("\nlow end (under 150 Hz), NEW minus OLD:")
    old = {n: lv for n, t, lv in lows if t.startswith("a")}
    for n, t, lv in lows:
        if t.startswith("b") and n in old:
            print("    %-16s %+.1f dB" % (n, lv - old[n]))
    print("\n%s\n%d files." % (desk, len(list(desk.glob('*')))))


if __name__ == "__main__":
    main()
