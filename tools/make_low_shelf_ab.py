"""A/B audition: the low shelf, on its own.

The mix EQ he approved 2026-09-02 was three moves at once — a low lift, a
mid dip, an air lift. Then 2026-09-03, asked which effects are universal
in hip hop, I checked make_drum_loops.master() and found it ALREADY does
two of them on every beat: an air shelf above 9 kHz and a dip through the
300-900 Hz boxiness. So the only genuinely new part of that EQ is the LOW
SHELF, and that is the only part worth a decision.

This batch asks that one question and nothing else. Same six DJs, same
kits, same seeds. Mid and air are pinned to 0 dB so the low shelf is the
ONLY thing moving between files — judging a low shelf inside a three-band
curve is how the question got blurred the first time.

    a Now        today's sound, untouched
    b A little   +1.5 dB below 120 Hz — the amount inside the EQ he approved
    c More       +3.0 dB below 120 Hz

Three amounts, not two, because "Now" is the zero: a / b / c is a ladder
from none to more, so he can say "further" or "back" instead of just
yes/no.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_low_shelf_ab.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom Low Shelf <today>/
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
from groove import OWNER_TASTE

DESK = Path(os.path.expanduser(f"~/Desktop/Homeroom Auditions/Homeroom Low Shelf {date.today()}"))

PICKS = ["Otto Grit", "Kane East", "Mustang",
         "DJ Premium", "Night Metro", "Trip Hop"]

# The approved shelf, taken from his own parked EQ rather than retyped.
APPROVED_DB = OWNER_TASTE["mix_eq"]["low_db"]      # 1.5
SHELF_HZ = OWNER_TASTE["mix_eq"]["low_hz"]         # 120.0


def only_low(db):
    """His approved EQ with the two bands the master stage ALREADY does
    pinned flat, so this batch moves one thing."""
    return {"low_db": db, "low_hz": SHELF_HZ,
            "mid_db": 0.0, "mid_hz": 800.0, "mid_q": 0.9,
            "high_db": 0.0, "high_hz": 8000.0}


# FOUR rungs, not three. The first render of this batch stopped at +3 and
# MEASURED almost nothing: in the finished files a +1.5 dB shelf arrived as
# +0.54 dB and a +3 dB shelf as +0.99 dB, because master() peak-normalises,
# soft-clips and then loudness-normalises AFTER the EQ, and a low boost
# raises the kick's peaks — which is exactly what those three stages exist
# to take back. About a third gets through, proportionally (+3 lands at
# roughly double +1.5, so it is give-back and not a ceiling).
#
# +0.54 dB is at or under what most people can hear on a broad band. So
# the first ladder would have asked him to choose between three files that
# sound the same, and the answer would have been "it does nothing" — true
# of the batch, false of the effect. +6 lands near +2 dB, which is audible,
# and gives the ladder a top he can actually hear.
VERSIONS = [("a Now", None),
            (f"b A little (+{APPROVED_DB:g})", only_low(APPROVED_DB)),
            ("c More (+3)", only_low(3.0)),
            ("d A lot (+6)", only_low(6.0))]


def low_band_db(L, R, hz=SHELF_HZ):
    """ABSOLUTE energy below the shelf corner in the FINISHED file. The
    house rule is to measure where the sound comes out, not the buffer the
    effect was applied to — master() normalises peak AND loudness after
    the EQ, so a boost that survives the maths can still be given back.

    Absolute, NOT a share of the total: the first version of this measured
    low energy as a fraction of the whole file, which moves whenever
    anything else moves and reported +0.22 dB where the real change was
    +0.42. A ruler that undersells the thing being auditioned by half is
    worse than no ruler."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    freqs = np.fft.rfftfreq(len(mono), 1 / SR)
    return 10 * np.log10(spec[freqs <= hz].sum() / len(mono) + 1e-30)


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="low-shelf-ab-"))
    rows, lows = [], []
    for i, name in enumerate(PICKS):
        p = CREW[name]
        kit, _ = build_kit(shots, name, stamps[name][1], variant=i,
                           avoid=avoid, preset=p)
        base_low = None
        for tag, eq in VERSIONS:
            L, R, got = render_crew_beat(name, kit, preset=p, eq=eq)
            lb = low_band_db(L, R)
            if base_low is None:
                base_low = lb
            else:
                lows.append((f"{name} {tag}", lb - base_low))
            fn = f"{name} {p['bpm']}bpm {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(), np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:48s} LUFS {got:6.2f}  peak {peak:6.2f}  "
                  f"low {lb:6.2f} dB")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, lows))
    shutil.rmtree(scratch)
    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    if n != len(PICKS) * len(VERSIONS):
        print(f"WARNING: expected {len(PICKS) * len(VERSIONS)} files.")
    weak = [f"{k} ({v:+.2f} dB)" for k, v in lows if abs(v) < 0.10]
    if weak:
        print("WARNING: the shelf barely survived the master stage on:\n  "
              + "\n  ".join(weak))


def readme(rows, lows):
    lufs = [r[1] for r in rows]
    got = [v for k, v in lows if "little" in k]
    more = [v for k, v in lows if "More" in k]
    alot = [v for k, v in lows if "lot" in k]
    lines = [
        f"THE LOW SHELF, ON ITS OWN — how much low end?   {date.today()}",
        "=" * 62, "",
        "WHY THIS IS A SEPARATE BATCH",
        "  The EQ you approved on the 2nd was three moves at once: more",
        "  low, a dip in the middle, more air on top. Checking which",
        "  effects are standard in hip hop, I went and read the master",
        "  stage — and it ALREADY does two of those three on every beat",
        "  you have ever rendered. The air lift and the middle dip are",
        "  not new.",
        "",
        "  So the only part of that EQ that would actually change",
        "  anything is the LOW SHELF. That is this folder, and nothing",
        "  else. Mid and air are pinned flat here so one thing moves.",
        "",
        "Six beats. Four files each. Same beat, same samples, same seed:",
        "",
        "  a Now        today's sound. Nothing added.",
        f"  b A little   +{APPROVED_DB:g} dB under {SHELF_HZ:g} Hz — the amount that was",
        "               inside the EQ you already said yes to.",
        "  c More       +3 dB under the same point.",
        "  d A lot      +6 dB. Probably too much. It is here so the",
        "               ladder has a top you can definitely hear.",
        "",
        "Play a, b, c, d in order, per beat. It is ONE question: how much",
        "weight under the kick. There is no right answer, only yours.",
        "",
        "WHAT TO LISTEN FOR",
        "  Does 'b' sound fuller, or just muddier? Does 'c' sound big,",
        "  or does the kick start to swallow the snare?",
        "  If 'a' already sounds right, say so — that is a real answer",
        "  and it closes the last open piece of the EQ.",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS, a spread of {max(lufs) - min(lufs):.2f} dB.",
        "  So you are judging weight, not loudness.",
        "",
        "  READ THIS BEFORE YOU JUDGE THE BATCH — MOST OF THE BOOST IS",
        "  GIVEN BACK. Your master stage sets the peak, soft-clips, then",
        "  sets the loudness, and all three happen AFTER the EQ. A low",
        "  boost raises the kick's peaks, which is exactly what those",
        "  three stages exist to pull down again. Measured in the",
        f"  finished files — energy under {SHELF_HZ:g} Hz against each beat's",
        "  own 'a Now':",
        "",
        f"    the +{APPROVED_DB:g} dB shelf arrives as  {np.mean(got):+.2f} dB",
        f"    the +3 dB shelf arrives as    {np.mean(more):+.2f} dB",
        f"    the +6 dB shelf arrives as    {np.mean(alot):+.2f} dB",
        "",
        "  So about a third of what you dial in reaches the file, evenly",
        "  — it is a give-back, not a wall. Roughly 1 dB is where a",
        "  change this broad starts being obvious, which means the",
        "  amount you already approved (b) lands UNDER the line and may",
        "  well sound like nothing at all. That is the honest reason",
        "  'd' is in the folder.",
        "",
        "  If you want real weight and 'd' is too much, the lever is not",
        "  this EQ — it is the kick and sub levels themselves, which sit",
        "  before all that normalising. Say the word and I will test",
        "  that instead.",
        "",
        "  Per beat, for the amount you approved:",
    ] + [f"    {n:34s} {v:+6.2f} dB" for n, v in lows if "little" in n] + [
        "",
        "DELIBERATELY ODD",
        "  * The mid dip and the air lift are NOT in this test. They",
        "    already happen on every beat, so testing them would be",
        "    testing nothing.",
        "  * The shelf sits on the whole mix, after the rules that keep",
        "    the snare under the kick. It lifts everything under "
        f"{SHELF_HZ:g} Hz",
        "    equally, so it makes the beat heavier without changing",
        "    which drum is loudest.",
        "  * Same six DJs as the last two batches, on purpose — you can",
        "    line all three folders up against the same beats.",
        "",
        "NOT HEARD",
        "  Which of the three is right. I can measure that the boost is",
        "  there and how big it is; I cannot hear whether it is too much.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  One line: a / b / c — or 'between b and c', which is fine.",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:48s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
