"""A/B audition: chorus and phaser, wired 2026-09-03.

He asked "wire the chorus and the phaser?" and, asked where, said BOTH —
the Sound Engine rack and per-DJ at make time. Both are wired and both
are OFF: no DJ and no preset turns them on, because he has not heard
them. This batch is what decides whether they stay and at what strength.

Same shape as tools/make_delay_eq_ab.py, deliberately: same six DJs, same
tempos, one kit per DJ reused across all four versions so the effect is
the only thing that moves between files.

    a Now      today's sound, untouched
    b Chorus   chorus on the backbeat and the stamp
    c Phaser   phaser on the hats
    d Both     the two together, each still on its own lane

WHY THOSE LANES, and not the chords. Chorus belongs on chords and pads —
that is its real job, and it is what the rack version is for. This A/B
path renders DRUMS ONLY (the lanes are kick/snare/clap/hat/stamp; chord
lanes are built further up in beat_machine and never reach here), so a
chorus aimed at its default "chord" lanes would have rendered four
IDENTICAL files and asked him to judge silence. Aimed at the backbeat and
the stamp it is audible on every beat in the folder. The chord question
is a separate audition and the READ ME says so.

Chorus and phaser sit on DIFFERENT lanes in "d Both" on purpose: stacked
on one lane they smear each other and he could not tell which he was
hearing.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_chorus_phaser_ab.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom Chorus and Phaser <today>/
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
    f"~/Desktop/Homeroom Auditions/Homeroom Chorus and Phaser {date.today()}"))

# The same six as the delay/EQ batch, so he can put the two folders side
# by side: tempo 88-140, backbeat on snare AND on clap, and a dry / gated
# / plate spread.
PICKS = ["Otto Grit", "Kane East", "Mustang",
         "DJ Premium", "Night Metro", "Trip Hop"]

# Starting settings. GUESSES for his ear to rule on, not tuned numbers.
# Rates are slow on purpose — one lazy sweep across an 8-bar loop reads as
# movement, four fast ones read as a broken sample.
# mix was 0.35 on the first render of this batch and MEASURED too quiet:
# level-matched against its own "a Now", the chorus moved Night Metro by
# only -27 dB, Mustang -21.9, Kane East -20.2. Round 1 of the rack presets
# sat at -33 to -10 dB and his verdict on it was "not enough effects", so
# shipping those three would have burned an audition to be told the same
# thing again. 0.5 pulls the weakest beat up into the phaser's band.
CHORUS = {"rate_hz": 0.8, "depth": 0.35, "mix": 0.50,
          "lanes": ("snare", "clap", "stamp")}
PHASER = {"rate_hz": 0.5, "depth": 0.60, "mix": 0.35,
          "lanes": ("hat",)}

VERSIONS = [("a Now", None, None),
            ("b Chorus", CHORUS, None),
            ("c Phaser", None, PHASER),
            ("d Both", CHORUS, PHASER)]


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="chorus-phaser-ab-"))
    rows = []
    silent = []
    strength = []      # how far each version moved from its own "a Now"
    for i, name in enumerate(PICKS):
        p = CREW[name]
        # one kit per DJ, reused across the four versions: the effect has
        # to be the only difference, so the samples cannot be re-rolled
        kit, _ = build_kit(shots, name, stamps[name][1], variant=i,
                           avoid=avoid, preset=p)
        base = None
        for tag, chorus, phaser in VERSIONS:
            L, R, got = render_crew_beat(name, kit, preset=p,
                                         chorus=chorus, phaser=phaser)
            if base is None:
                base = (L, R)
            else:
                # HOW MUCH did it move? Level-matched against this beat's
                # own untouched render, which is the only fair reference —
                # a median across the folder hides the one beat where the
                # effect did nothing. Round 1 of the rack presets measured
                # -33 to -10 dB here and his verdict was "not enough".
                d = np.concatenate([L - base[0], R - base[1]])
                ref = np.concatenate(base)
                strength.append((f"{name} {tag}", 20 * np.log10(
                    np.sqrt((d ** 2).mean())
                    / (np.sqrt((ref ** 2).mean()) + 1e-12) + 1e-12)))
            if base is not None and tag != "a Now" and \
                    np.array_equal(L, base[0]) and np.array_equal(R, base[1]):
                # the failure this project keeps repeating: an effect that
                # is switched on, renders, and changes nothing. Caught here
                # rather than discovered by him playing two identical files.
                silent.append(f"{name} {tag}")
            fn = f"{name} {p['bpm']}bpm {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:46s} LUFS {got:6.2f}  peak {peak:6.2f} dBFS")

    if DESK.exists():
        shutil.rmtree(DESK)          # one current audition folder, no doubt
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, silent, strength))
    shutil.rmtree(scratch)
    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    if n != len(PICKS) * len(VERSIONS):
        print(f"WARNING: expected {len(PICKS) * len(VERSIONS)} files.")
    if silent:
        print("WARNING: these renders came out IDENTICAL to their 'a Now' "
              "— the effect did nothing:\n  " + "\n  ".join(silent))


def readme(rows, silent, strength):
    lufs = [r[1] for r in rows]
    lines = [
        f"CHORUS AND PHASER — are either of them worth keeping?   {date.today()}",
        "=" * 66, "",
        'You said: "wire the chorus and the phaser" — on both sides, the',
        "rack and the DJs. They are wired. Nothing turns them on yet.",
        "This folder is the only place they exist.",
        "",
        "Six beats. Four files each. Same beat, same samples, same seed —",
        "the ONLY thing that changes between the four is the effect:",
        "",
        "  a Now      what the machine sounds like today. Nothing added.",
        "  b Chorus   a slow wobble on the snare/clap and the stamp. It",
        "             makes a single hit sound like two slightly detuned",
        "             copies of itself — wider and thicker, not louder.",
        "  c Phaser   a notch that sweeps up and down the hats. Reads as",
        "             a slow whoosh moving through the top end.",
        "  d Both     the two together, each still on its own lane.",
        "",
        "Play them in that order, per beat.",
        "",
        "WHAT I ACTUALLY NEED YOU TO LISTEN FOR",
        "  Chorus: does the backbeat sound BIGGER, or does it sound",
        "  smeared and out of tune? Both are what a chorus does; only",
        "  you can say which side of the line these settings are on.",
        "  Phaser: does the hat lane move, or does it sound like a",
        "  broken sample / a phone speaker?",
        "",
        "DELIBERATELY ODD, so you don't report it as a bug",
        "  * THE CHORUS IS NOT ON THE CHORDS, and chords are where a",
        "    chorus actually belongs. These six renders are drums only —",
        "    this test bench has no chord lane at all — so putting it",
        "    where it belongs would have given you four identical files.",
        "    On the backbeat you can at least hear what it does. The",
        "    chords test is a separate batch; say the word.",
        "  * In 'd Both' the two effects are on DIFFERENT lanes. Stacked",
        "    on one lane they smear each other and you could not tell",
        "    which one you were hearing.",
        "  * Night Metro gets the least out of the chorus by a long way",
        "    (see the numbers below — 15 dB less than DJ Premium). It is",
        "    140bpm and sub-heavy and its clap sits low in the mix, so",
        "    the SETTING is the same as everywhere else but the RESULT is",
        "    not. If you like the effect elsewhere and not here, that is",
        "    a per-DJ amount to set, not a bug.",
        "  * Trip Hop already has a plate reverb, so the chorus lands on",
        "    top of an existing tail. Busiest files in the folder.",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS, a spread of {max(lufs) - min(lufs):.2f} dB.",
        "  So you are judging tone, not loudness.",
        "  The off-by-default path is proved byte-for-byte identical to",
        "  the old code by a test, so 'a Now' really is today's sound.",
        "  Both effects run BEFORE the snare-vs-kick level rule, so",
        "  neither can push the backbeat over the kick.",
        "  EVERY 'b'/'c'/'d' file was checked against its own 'a Now' and",
        "  confirmed different" + (
            "." if not silent else
            " — EXCEPT these, which came out IDENTICAL "
            "and are a real bug: " + ", ".join(silent)) ,
        "",
        "  THE LOOP SEAM. Both effects were broken when I found them —",
        "  the wobble started from cold at bar 1 and stopped mid-sweep at",
        "  bar 8, so the loop clicked. Fixed before wiring. Measured, the",
        "  step across the loop point went from 49x and 69x a normal",
        "  sample step down to 1.9x and 1.6x, which is no step at all.",
        "  These files loop clean.",
        "",
        "  HOW MUCH EACH EFFECT ACTUALLY MOVES THE BEAT, measured against",
        "  that same beat's own 'a Now'. Bigger number = more obvious:",
    ] + [f"    {n:26s} {v:6.1f} dB" for n, v in strength] + [
        "  For scale: the rack presets you called 'not enough effects'",
        f"  measured -33 to -10 dB. This batch is "
        f"{min(v for _, v in strength):.0f} to "
        f"{max(v for _, v in strength):.0f}.",
        "",
        "NOT HEARD",
        "  Whether either effect is worth keeping, and at what strength.",
        "  I picked the numbers as a starting guess; I can't hear them.",
        "  Same for which DJs should get them and which shouldn't, and",
        "  what a chorus does to your chords.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  One line: keep chorus / keep phaser / keep both / keep",
        "  neither — and 'more' or 'less' if a setting is close.",
        "",
        "-" * 66,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:46s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
