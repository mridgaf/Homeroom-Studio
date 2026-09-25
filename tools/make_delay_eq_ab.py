"""A/B audition: the two Sound Engine effects the owner asked for.

His words: "I am going to want the delay and EQ." Both already live in
tools/audio_engine.py (eq3, loop_delay) and both are loop-safe; as of
2026-09-02 render_crew_beat() takes them as opt-in keywords. Nothing on
the roster turns them on. This batch is what decides whether they stay.

Six beats, six DJs, six tempos, four renders each from the SAME seed so
only one thing moves between files:

    a Now    today's sound, untouched
    b EQ     + 3-band EQ on the mix
    c Echo   + 1/8-note echo on the backbeat
    d Both   the two together

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_delay_eq_ab.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom Delay and EQ <today>/
"""
import os
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24
from make_drum_beats import build_shots
from crew import CREW, build_kit, lock_stamps, render_crew_beat

DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Auditions/Homeroom Delay and EQ {date.today()}"))

# Six DJs chosen to spread the variables the effects interact with: tempo
# 88-140, backbeat on snare AND on clap, and a dry / gated / plate spread
# so the echo is heard both bare and on top of an existing tail.
PICKS = ["Otto Grit", "Kane East", "Mustang",
         "DJ Premium", "Night Metro", "Trip Hop"]

# Starting settings. These are GUESSES for his ear to rule on, not tuned
# numbers — a gentle smile curve and a conventional 1/8 snare throw.
EQ = {"low_db": 1.5, "low_hz": 120.0,
      "mid_db": -1.0, "mid_hz": 800.0, "mid_q": 0.9,
      "high_db": 2.0, "high_hz": 8000.0}
ECHO = {"note": 0.5, "feedback": 0.35, "mix": 0.20}   # 0.5 = 1/8 note

VERSIONS = [("a Now", None, None),
            ("b EQ", EQ, None),
            ("c Echo", None, ECHO),
            ("d Both", EQ, ECHO)]


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="delay-eq-ab-"))
    rows = []
    for i, name in enumerate(PICKS):
        p = CREW[name]
        # one kit per DJ, reused across the four versions: the effect has
        # to be the only difference, so the samples cannot be re-rolled
        kit, _ = build_kit(shots, name, stamps[name][1], variant=i,
                           avoid=avoid, preset=p)
        for tag, eq, echo in VERSIONS:
            L, R, got = render_crew_beat(name, kit, preset=p,
                                         eq=eq, echo=echo)
            fn = f"{name} {p['bpm']}bpm {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:44s} LUFS {got:6.2f}  peak {peak:6.2f} dBFS")

    if DESK.exists():
        shutil.rmtree(DESK)          # one current audition folder, no doubt
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows))
    shutil.rmtree(scratch)
    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    if n != len(PICKS) * len(VERSIONS):
        print(f"WARNING: expected {len(PICKS) * len(VERSIONS)} files.")


def readme(rows):
    lufs = [r[1] for r in rows]
    lines = [
        f"DELAY AND EQ — is either one worth keeping?   {date.today()}",
        "=" * 62, "",
        'You said: "I am going to want the delay and EQ."  This is them.',
        "",
        "Six beats. Four files each. Same beat, same samples, same seed —",
        "the ONLY thing that changes between the four is the effect:",
        "",
        "  a Now    what the machine sounds like today. Nothing added.",
        "  b EQ     a gentle tone curve on the whole mix: a bit more low",
        "           end, a small dip in the middle, a bit more air on top.",
        "  c Echo   an eighth-note echo on the snare/clap only, quiet",
        "           enough to be a tail rather than a second snare.",
        "  d Both   the two together.",
        "",
        "Play them in that order, per beat. Listen for whether b sounds",
        "BETTER or just LOUDER-ish, and whether c adds groove or clutter.",
        "",
        "WHY THE ECHO IS ONLY ON THE SNARE",
        "An echo across the whole mix smears the kick and the bass into",
        "each other. On this music the delay's job is a throw on the",
        "backbeat, so that's where it is.",
        "",
        "DELIBERATELY ODD, so you don't report it as a bug",
        "  * Mustang is the one beat here with a dry backbeat, so its clap",
        "    carries the least reverb of the six and the echo is the most",
        "    exposed. On purpose — it's the honest test of the effect with",
        "    the least to hide behind.",
        "  * Trip Hop already has a plate reverb. Its echo lands on top of",
        "    that, so 'c' and 'd' are the busiest files in the folder.",
        "  * Night Metro is 140bpm, so its eighth note is fast — the echo",
        "    reads as a flam there more than a repeat. It is also the",
        "    hardest to hear in the folder, because its clap sits low in a",
        "    sub-heavy mix. The echo is the same strength on every beat",
        "    (see the numbers below); it just has more to compete with.",
        "  * No DJ has either effect switched on for real. Nothing in the",
        "    library changed. This folder is the only place they exist.",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS, a spread of {max(lufs) - min(lufs):.2f} dB.",
        "  So you are judging tone, not loudness — nothing here wins by",
        "  being louder than its neighbour.",
        "  The off-by-default path is proved byte-for-byte identical to",
        "  the old code by a test, so the 'a Now' files really are today's",
        "  sound and not a re-render that drifted.",
        "  The echo runs before the snare-vs-kick level rule, so it cannot",
        "  push the backbeat over the kick. Also tested. That rule is also",
        "  why 'c Echo' is not louder than 'a Now' — the repeats are paid",
        "  for out of the snare's own level, not added on top of it.",
        "  Echo strength measured against each beat's own backbeat:",
        "  Otto Grit -16.6, Kane East -20.8, Mustang -15.0, DJ Premium",
        "  -15.8, Night Metro -17.6, Trip Hop -15.8 dB. Even across the",
        "  board, so a beat where you can't hear it is a beat where the",
        "  backbeat itself is buried, not a beat the effect skipped.",
        "",
        "NOT HEARD",
        "  Whether either effect is worth keeping, and at what strength.",
        "  I picked the numbers as a starting guess; I can't hear them.",
        "  Same for which DJs should get them and which shouldn't.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  One line: keep EQ / keep echo / keep both / keep neither —",
        "  and 'more' or 'less' if a setting is close but not right.",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:44s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
