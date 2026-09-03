"""A/B audition: three whole Otto Grits.

The per-DJ effects pass (DECISIONS.md 2026-09-03 handoff) starts here.
Four effects are built and approved by ear but switched on for nothing;
his rollout decision was PER DJ, one at a time. Otto Grit is first.

Three decisions he made 2026-09-03, which is why this batch looks the
way it does:

  * "Let Otto hear his dust." The 2026-07-18 clean-render rule turns off
    every dirt stage engine-wide, so Otto's own dust=0.5 and vinyl=-42
    have never played. He opened a ONE-DJ exception, not a rule change.
  * "The new research always wins versus the old code." Two primary-
    source engineers describe the reference sound as deliberately matte
    — "wasn't into slick top end". The approved roster EQ adds +2 dB of
    air at 8k. Otto's air goes the other way here: -1.5 dB.
  * "Two or three whole Ottos", not one effect at a time.

The kick sub layer is NOT a variable in this batch — he already picked
"b Light" on the 2026-09-03 kick audition, so it is in his preset now
and rides in b and c as settled.

    a Now       what his library sounds like today: no sub layer, no
                dust, no effects. The zero.
    b Research  the sub layer + his own dust and vinyl + the matte EQ.
                No modulation of any kind.
    c Plus      b, and then the backbeat echo and the chorus at the
                amounts he approved 2026-09-02/03.

DELIBERATELY LEFT OUT: the phaser. It is a top-end sweep on the hats and
his line says the hats are dead straight; the research this batch is
built on says matte. Putting it in would be arguing with the same
sources b and c are built from. It is one line to add if he wants it.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_otto_ab.py
Out:  ~/Desktop/Homeroom Otto <today>/
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

DESK = Path(os.path.expanduser(f"~/Desktop/Homeroom Otto {date.today()}"))
NAME = "Otto Grit"
NBEATS = 3                    # three different beats, same three versions

# His approved EQ with ONE band changed: the air goes DOWN, not up. The
# low shelf and the mid dip are his approved amounts, read from the parked
# taste rather than retyped, so if he ever retunes them this follows.
_EQ = OWNER_TASTE["mix_eq"]
MATTE_EQ = dict(_EQ, high_db=-1.5)

ECHO = OWNER_TASTE["backbeat_echo"]
CHORUS = OWNER_TASTE["chorus"]

# (tag, sub layer on?, dirt on?, eq, echo, chorus)
VERSIONS = [
    ("a Now",      False, False, None,      None, None),
    ("b Research", True,  True,  MATTE_EQ,  None, None),
    ("c Plus",     True,  True,  MATTE_EQ,  ECHO, CHORUS),
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


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="otto-ab-"))
    base = CREW[NAME]
    rows, deltas, under = [], [], []

    for i in range(NBEATS):
        # ONE kit per beat, reused across all three versions, so the only
        # thing moving between a/b/c is the treatment — except the kick,
        # which has to be rebuilt because the sub layer is baked into the
        # one-shot before it is tiled.
        ref = None
        for tag, sub, dirt, eq, echo, chorus in VERSIONS:
            p = dict(base)
            if not sub:
                p.pop("sub_layer", None)
            if dirt:
                p["allow_dirt"] = True
            kit, _ = build_kit(shots, NAME, stamps[NAME][1], variant=i,
                               avoid=set(avoid), preset=p)
            L, R, got = render_crew_beat(NAME, kit, preset=p, eq=eq,
                                         echo=echo, chorus=chorus)
            low, air = band_db(L, R, hi=100.0), band_db(L, R, lo=8000.0)
            if ref is None:
                ref = (low, air, np.asarray(L).copy())
                prev = None
            else:
                d = float(np.abs(np.asarray(L) - ref[2][:len(L)]).max())
                # how far the extra effects moved c off b, as dB under the
                # beat itself — band energy misses it because the echo and
                # the chorus live in the mids, not at either edge
                if prev is not None:
                    n = min(len(L), len(prev))
                    diff = np.asarray(L)[:n] - prev[:n]
                    under.append(
                        20 * np.log10(np.sqrt((diff ** 2).mean()) + 1e-12)
                        - 20 * np.log10(np.sqrt((prev[:n] ** 2).mean())
                                        + 1e-12))
                deltas.append((f"beat {i + 1} {tag}", low - ref[0],
                               air - ref[1], d))
            prev = np.asarray(L).copy()
            fn = f"{NAME} {p['bpm']}bpm beat {i + 1} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:46s} LUFS {got:6.2f}  peak {peak:6.2f}  "
                  f"low {low:6.2f}  air {air:6.2f}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, deltas, under))
    shutil.rmtree(scratch)

    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    want = NBEATS * len(VERSIONS)
    if n != want:
        print(f"WARNING: expected {want} files.")
    # fail loud, same contract as the last two batches
    same = [k for k, _lo, _ai, d in deltas if d < 1e-6]
    if same:
        print("WARNING: rendered IDENTICAL to 'a Now':\n  "
              + "\n  ".join(same))
    bright = [f"{k} ({a:+.2f} dB)" for k, _lo, a, _d in deltas if a > 0]
    if bright:
        print("WARNING: the matte EQ made these BRIGHTER, not darker:\n  "
              + "\n  ".join(bright))


def _avg(deltas, tag, idx):
    v = [d[idx] for d in deltas if tag in d[0]]
    return float(np.mean(v)) if v else 0.0


def readme(rows, deltas, under):
    lufs = [r[1] for r in rows]
    lines = [
        f"OTTO GRIT — three whole versions of him   {date.today()}",
        "=" * 62, "",
        "WHY THIS BATCH",
        "  You have four effects sitting finished and switched on for",
        "  nothing, and you said roll them out one DJ at a time. This is",
        "  Otto, the first one. Three things you told me on the 3rd went",
        "  into it:",
        "",
        "   * let Otto hear his dust — his own dust and vinyl numbers",
        "     have been in his file for months and have never once",
        "     played, because the clean-render rule switches all dirt",
        "     off. This is an exception for HIM ONLY. Nobody else",
        "     changes and the rule is not touched.",
        "   * the new research beats the old code — two engineers who",
        "     actually worked on the records say the top end was",
        "     deliberately dull, 'not into slick top end'. The EQ you",
        "     approved adds brightness. So Otto's goes the OTHER way:",
        "     -1.5 dB of air instead of +2.",
        "   * whole versions, not one effect at a time.",
        "",
        "  The sub tone under his kick is NOT a question here. You",
        "  already picked 'b Light' on the kick batch, so it is his now",
        "  and it just rides along in b and c.",
        "",
        "THREE BEATS. THREE VERSIONS EACH. Same beat, same samples:",
        "",
        "  a Now       what your library sounds like today. Nothing",
        "              added. This is the zero to judge against.",
        "  b Research  his kick sub tone + his own dust and vinyl + the",
        "              darker EQ. No wobble, no echo — just him, dirtier",
        "              and duller.",
        "  c Plus      everything in b, and then the echo on the snare",
        "              and the chorus, at the amounts you already",
        "              approved.",
        "",
        "WHAT TO LISTEN FOR",
        "  a -> b: does he sound more like himself, or just worse? Dust",
        "  and vinyl are noise on purpose. The dull top is on purpose",
        "  too. Both are reversible in one line if you hate them.",
        "  b -> c: does the echo and the wobble add character, or does",
        "  it start sounding like an effect sitting on top of a beat?",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS — you are judging",
        "  character, not loudness.",
        "",
        "  Against each beat's own 'a Now', in the FINISHED files:",
        f"    b   weight under 100 Hz  {_avg(deltas, 'b Research', 1):+.2f} dB"
        f"     air above 8 kHz  {_avg(deltas, 'b Research', 2):+.2f} dB",
        f"    c   weight under 100 Hz  {_avg(deltas, 'c Plus', 1):+.2f} dB"
        f"     air above 8 kHz  {_avg(deltas, 'c Plus', 2):+.2f} dB",
        "",
        "  About 1 dB is where a broad change like this becomes",
        "  obvious, so the top-end drop is well past it — but READ THIS:",
        "  only about 1.5 dB of that is the EQ. The rest is the dust.",
        "  The SP-1200 emulation rolls the top off by itself, which is",
        "  most of why b sounds duller than a. So if b is too dull, the",
        "  first thing to pull back is the dust, not the EQ.",
        "",
        f"  b -> c, the echo and the chorus: they sit "
        f"{abs(float(np.mean(under))):.0f} dB under the",
        "  beat on average. Loud enough to hear, not loud enough to be",
        "  the beat. The band numbers above barely move for c because",
        "  both effects live in the middle of the sound, not at the",
        "  bottom or the top where those two rulers look.",
        "",
        "DELIBERATELY LEFT OUT",
        "  * The phaser. It is a sweep across the hats, and both his own",
        "    description ('hats dead straight') and the research this",
        "    batch is built on point the other way. Say the word and it",
        "    is one line to add and re-render.",
        "  * Everything for the other eight DJs and the twelve legends.",
        "    One at a time was your call.",
        "",
        "NOT HEARD",
        "  Whether the dust reads as HIS grit or as noise on a clean",
        "  beat; whether -1.5 dB of air sounds right or just muffled;",
        "  whether the echo and chorus belong on him. I can measure that",
        "  each one is there and how big it is. I cannot tell you which",
        "  one sounds like Otto Grit.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  One line: a / b / c — and if it is b or c, say whether the",
        "  dust is too much, too little, or right.",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:46s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
