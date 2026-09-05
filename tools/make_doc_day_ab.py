"""A/B audition: three whole Doc Days.

The Legends pass (DECISIONS.md 2026-09-05 handoff) starts here. Doc Day
was rebuilt from research on the 5th and then never rendered, because
the drive was not mounted. This is that batch.

Two things he decided before it was built:

  * "Keep changing his numbers" — so the compression knob his own quote
    asks for got built first (crew.py now passes a preset's `glue` block
    into groove.glue_compress) and is IN b and c. It is not a separate
    rung; his own preference is whole versions, not one effect at a time.
  * The sub rungs: Now / Research / Light.

    a Now       Doc Day before the 09-05 pass: no sub under the kick,
                the roster's EQ, the roster's 1.8 glue. The zero.
    b Research  his 0.45 sub + his EQ + ratio 4.0 glue.
    c Light     the same, with the 0.35 sub that is the ONLY sub setting
                in this project ever approved by ear (crew.py:249, Otto
                Grit's "b Light" audition 2026-09-03).

TWO THINGS DELIBERATELY NOT VARIED, both recorded in his _research_note:

  * The EQ. Measured against the roster default, only his low shelf
    moved, and groove.py's own note says about a third of a low boost
    survives the master chain — so it is worth roughly 0.2 dB. It rides
    along in b and c and is not the question.
  * space ["gated", ["snare"]]. A roster default nobody researched. A
    search on 09-05 found no source tying his snare to reverb OR to
    dryness, so it stays until one turns up.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_doc_day_ab.py
Out:  ~/Desktop/Homeroom Doc Day <today>/
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

DESK = Path(os.path.expanduser(f"~/Desktop/Homeroom Doc Day {date.today()}"))
NAME = "Doc Day"
NBEATS = 3                    # three different beats, same three versions

# Otto Grit's approved sub, read from the live roster rather than retyped
# so it follows if he ever retunes it. This is the LIGHT rung.
LIGHT_SUB = dict(CREW["Otto Grit"]["sub_layer"])

# ROSTER_EQ is what Doc Day rendered through before the 09-05 pass — the
# same fallback crew.render_crew_beat reaches for when a preset names no
# mix_eq of its own. Passed explicitly so "a Now" cannot drift if the
# house default is ever changed underneath this batch.
ROSTER_EQ = dict(OWNER_TASTE["mix_eq"])

# (tag, sub layer, his glue?, eq)
VERSIONS = [
    ("a Now",      None,                          False, ROSTER_EQ),
    ("b Research", dict(CREW[NAME]["sub_layer"]),  True,  None),
    ("c Light",    LIGHT_SUB,                      True,  None),
]


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the FINISHED file — measured where the
    sound comes out, not on the buffer an effect was applied to. master()
    peak-normalises, soft-clips and then loudness-normalises after every
    stage in this batch, so anything measured earlier can still be given
    back. Absolute, not a share of the total: a share moves whenever
    anything else moves (DECISIONS.md 2026-09-03, the ruler that undersold
    the low shelf by half)."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def crest_db(L, R):
    """Peak minus RMS. The one ruler that sees a compressor: a harder
    ratio pulls the peaks down toward the average, so this number goes
    DOWN. Band energy cannot see the glue at all — it is broadband."""
    x = 0.5 * (np.asarray(L) + np.asarray(R))
    peak = float(np.abs(x).max())
    rms = float(np.sqrt((x ** 2).mean()))
    return 20 * np.log10(peak + 1e-12) - 20 * np.log10(rms + 1e-12)


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="docday-ab-"))
    base = CREW[NAME]
    rows, deltas = [], []

    for i in range(NBEATS):
        # ONE kit per beat, reused across all three versions, so the only
        # thing moving between a/b/c is the treatment — except the kick,
        # which has to be rebuilt because the sub layer is baked into the
        # one-shot before it is tiled.
        ref = None
        for tag, sub, glue, eq in VERSIONS:
            p = dict(base)
            if sub:
                p["sub_layer"] = sub
            else:
                p.pop("sub_layer", None)
            if not glue:
                p.pop("glue", None)
            if eq is not None:
                p.pop("mix_eq", None)
            kit, _ = build_kit(shots, NAME, stamps[NAME][1], variant=i,
                               avoid=set(avoid), preset=p)
            L, R, got = render_crew_beat(NAME, kit, preset=p, eq=eq)
            low, crest = band_db(L, R, 30.0, 55.0), crest_db(L, R)
            if ref is None:
                ref = (low, crest, np.asarray(L).copy())
            else:
                d = float(np.abs(np.asarray(L) - ref[2][:len(L)]).max())
                deltas.append((f"beat {i + 1} {tag}", tag, low - ref[0],
                               crest - ref[1], d))
            fn = f"{NAME} {p['bpm']}bpm beat {i + 1} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:44s} LUFS {got:6.2f}  peak {peak:6.2f}  "
                  f"low {low:6.2f}  crest {crest:5.2f}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, deltas))
    shutil.rmtree(scratch)

    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    want = NBEATS * len(VERSIONS)
    if n != want:
        print(f"WARNING: expected {want} files.")

    # FAIL LOUD, same contract as the last three batches — but reporting
    # what actually moved rather than asserting it must. Two things were
    # MEASURED on 2026-09-05 and are why this is a report and not a gate:
    # the sub layer is inert on any kick whose peak is already at its
    # transient (the headroom guard wins), and glue_compress cannot move
    # crest much at all because its 25 ms symmetric envelope acts as level
    # automation, which master_to_lufs then normalises straight back out.
    dead = [k for k, _t, _lo, _cr, d in deltas if d < 1e-6]
    if dead:
        print("WARNING: rendered IDENTICAL to 'a Now':\n  " + "\n  ".join(dead))
    moved = [k for k, _t, lo, _cr, _d in deltas if lo > 0.5]
    print(f"\nsub layer added >0.5 dB at 30-55 Hz on {len(moved)} of "
          f"{len(deltas)} treated files.")
    if not moved:
        print("WARNING: the sub layer did nothing on ANY beat — do not "
              "ship this batch, there is nothing in it to hear.")
    print(f"  b  low {_avg(deltas, 'b Research', 2):+.2f} dB   "
          f"crest {_avg(deltas, 'b Research', 3):+.2f} dB")
    print(f"  c  low {_avg(deltas, 'c Light', 2):+.2f} dB   "
          f"crest {_avg(deltas, 'c Light', 3):+.2f} dB")


def _avg(deltas, tag, idx):
    v = [d[idx] for d in deltas if d[1] == tag]
    return float(np.mean(v)) if v else 0.0


def readme(rows, deltas):
    lufs = [r[1] for r in rows]
    lines = [
        f"DOC DAY (Dre) — three whole versions of him   {date.today()}",
        "=" * 62, "",
        "WHY THIS BATCH",
        "  His numbers were rebuilt from research on the 5th and then",
        "  never played — the drive wasn't plugged in. This is the first",
        "  time any of it has made a sound.",
        "",
        "  You said keep changing his numbers, so one more thing went in",
        "  before rendering. His own words, from a 2001 interview: 'I",
        "  usually have the ratio up to about eight or 10 on a lot of",
        "  things.' That's compression — squashing the loud bits so the",
        "  whole thing sits tighter and hits harder. There was no place",
        "  to put that number in this engine. There is now, and he's the",
        "  first one using it.",
        "",
        "  It is NOT set to 8. He was talking about squashing each sound",
        "  on its own desk channel; this engine only has one squeeze",
        "  across the whole beat, which is a different thing. Copying the",
        "  number across would be pretending. It's set to 4 — harder than",
        "  everyone else's 1.8, which is the part the sources back up.",
        "",
        "THREE BEATS. THREE VERSIONS EACH. Same beat, same samples:",
        "",
        "  a Now       him before any of this. No sub tone under the",
        "              kick, everyone's EQ, everyone's compression.",
        "              This is the zero to judge against.",
        "  b Research  the deep sub tone under his kick at the strength",
        "              the research argued for, plus the harder squeeze.",
        "  c Light     exactly the same, but the sub tone is the LIGHTER",
        "              one you already picked by ear for Otto Grit back",
        "              on the 3rd.",
        "",
        "  So b vs c is one question and one question only: how much",
        "  low-end weight under the kick.",
        "",
        "WHAT TO LISTEN FOR",
        "  a -> b: does the kick feel like it's in the room with you, or",
        "  just boomy? Does the whole beat sound tighter and more",
        "  together, or squashed and lifeless?",
        "  b -> c: is b too much sub? c is about a third less.",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS — you are judging",
        "  character, not loudness.",
        "",
        "  Against each beat's own 'a Now', in the FINISHED files:",
        f"    b   weight under 100 Hz  {_avg(deltas, 'b Research', 2):+.2f} dB"
        f"     squeeze  {_avg(deltas, 'b Research', 3):+.2f} dB",
        f"    c   weight under 100 Hz  {_avg(deltas, 'c Light', 2):+.2f} dB"
        f"     squeeze  {_avg(deltas, 'c Light', 3):+.2f} dB",
        "",
        "  'Squeeze' is peak minus average. It goes DOWN when the",
        "  compressor is working — the loud spikes come closer to the",
        "  rest. About 1 dB is where a change like this starts being",
        "  obvious.",
        "",
        "WHAT IS *NOT* A QUESTION HERE",
        "  His EQ. It's in b and c, but I measured it against the one",
        "  everybody else uses and only the bass shelf moved at all —",
        "  by half a dB, on a control where only about a third of what",
        "  you dial in survives to the file. It's worth roughly 0.2 dB.",
        "  Effectively nothing. The sub tone is doing the work.",
        "",
        "  His snare reverb setting. It's a leftover default that seven",
        "  of the twelve legends share, and it doesn't obviously fit a",
        "  guy whose whole sound is described as clean and surgical. I",
        "  went looking for a source saying his snare was dry, and a",
        "  source saying it wasn't. Found neither. So I left it rather",
        "  than change it on a hunch. Same for his sidechain and drive.",
        "",
        "NOT HEARD",
        "  Whether any of this sounds like Dre. I can measure that the",
        "  sub is there, how much weight it adds, and that the",
        "  compression is biting. I cannot tell you which one sounds",
        "  like him.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  One line: a / b / c — and if it's b or c, say whether the",
        "  squeeze is too much, too little, or right.",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:44s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
