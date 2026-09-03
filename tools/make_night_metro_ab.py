"""A/B audition: Night Metro, second of the per-DJ pass.

Same shape as the Otto batch, one rung longer, because he asked for the
arrangement fix in this batch rather than after it — and an arrangement
change and an effects change have to be separable by ear or the verdict
means nothing.

What the research says, and what the code was doing instead:

  * "Bar 5 drops to the 808 alone" is his signature moment. It was true
    of his one prototype file and 0 of 12 generated beats — compose()
    and vary_preset() rebuild his lanes from grammar every time, and
    neither knows about it. Now pinned.
  * "Distort the 808/kick specifically — don't apply that grit to the
    whole mix." His kick_dist=5.0 is the second-heaviest on the roster
    and has never played once, because the 2026-07-18 clean-render rule
    switches all dirt off. He opened it for the LOW END ONLY (his
    words, 2026-09-03), which is why allow_dirt="low" exists and Otto's
    plain True does not go on this preset.
  * "Heaviest low end in the roster... hats crisp and bright." That is
    the roster mix_eq exactly as approved — heavier lows, more air. Note
    this is the OPPOSITE call to Otto's, and for the same reason: the
    research on each one wins.

    a Now       today's sound.
    b Drop      the bar-5 breakdown, and nothing else.
    c Research  b + the 808 grit + the approved EQ.
    d Plus      c + the echo on the clap and the chorus on the riser.

DELIBERATELY LEFT OUT: the phaser, and the chorus on the CLAP or HATS.
His research says keep hats and clap clean and bright against the heavy
low end; a sweep or a wobble on either argues with the same source the
rest of this batch follows. The chorus goes on the STAMP alone — the
reversed cymbal riser, a sound-design element where width is the point.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_night_metro_ab.py
Out:  ~/Desktop/Homeroom Night Metro <today>/
"""
import json
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
from crew import CREW, bars_of, build_kit, lock_stamps, render_crew_beat
from groove import OWNER_TASTE
from pattern_gen import compose
from beat_machine import vary_preset

DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Night Metro {date.today()}"))
NAME = "Night Metro"
NBEATS = 3

# His approved EQ, unchanged — read from the parked taste, not retyped.
# Otto's was darkened because his research says matte; this one's research
# says the opposite, so it stays exactly as he approved it.
EQ = OWNER_TASTE["mix_eq"]
ECHO = OWNER_TASTE["backbeat_echo"]
# the approved chorus AMOUNT, but on the riser only — see the module note
CHORUS = dict(OWNER_TASTE["chorus"], lanes=("stamp",))

BREAKDOWN = {"bar": 5, "keep": ["kick"]}

# (tag, breakdown, dirt, eq, echo, chorus)
VERSIONS = [
    ("a Now",      None,      None,  None, None, None),
    ("b Drop",     BREAKDOWN, None,  None, None, None),
    ("c Research", BREAKDOWN, "low", EQ,   None, None),
    ("d Plus",     BREAKDOWN, "low", EQ,   ECHO, CHORUS),
]


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the FINISHED file — measured where the
    sound comes out, not on the buffer an effect was applied to. Absolute,
    not a share of the total: a share moves whenever anything else moves
    (DECISIONS.md 2026-09-03, the ruler that undersold the low shelf)."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def bar5_rms_db(L, R, bpm, nbars, bars=(4,), hp_hz=2000.0):
    """How loud bar 5 is against the whole beat, ABOVE 2 kHz.

    Two rulers were wrong before this one, and both are worth keeping
    written down. A whole-FILE average buries a one-bar change. And a
    whole-BAND bar measure — which is what this was first — moved only
    about 0.6 dB, because Night Metro's sustained 808 carries most of the
    beat's energy and the 808 is exactly what the breakdown KEEPS. The
    hats and the clap are what leave, and they live up top. Measuring
    where they live is the difference between "the drop does nothing"
    (false) and "everything but the 808 got out of the way" (what
    actually happens)."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    X = np.fft.rfft(mono)
    X[np.fft.rfftfreq(len(mono), 1 / SR) < hp_hz] = 0
    mono = np.fft.irfft(X, len(mono))
    bar_n = int(round(4 * 60.0 / bpm * SR))
    seg = np.concatenate([mono[b * bar_n:(b + 1) * bar_n] for b in bars])
    whole = mono[:nbars * bar_n]
    if not len(seg):
        return 0.0
    return (20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-12)
            - 20 * np.log10(np.sqrt((whole ** 2).mean()) + 1e-12))


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="night-metro-ab-"))
    base = CREW[NAME]
    rows, deltas, drops = [], [], []

    # COMPOSE ONCE PER BEAT, then treat that one composition four ways.
    #
    # Two traps found the hard way, both worth keeping written down:
    #  1. The first render of this batch used the static prototype
    #     CREW["Night Metro"] and every "b Drop" came out BYTE-IDENTICAL
    #     to its "a Now" — the fail-loud check caught it. His prototype
    #     file ALREADY has bar 5 empty on every lane but the kick. It is
    #     the beats you actually generate, where compose() and
    #     vary_preset() rewrite the lanes from grammar, that lose it.
    #     Auditioning the prototype was auditioning the one file that
    #     never had the bug.
    #  2. compose() is deterministic per (name, variant, attempt) but its
    #     repeat guard carries history ACROSS calls, so composing the
    #     same variant four times can land on a different attempt and a
    #     different loop length. Composing once and reusing it is both
    #     the fix and the right bench: only the treatment moves.
    #
    # Only 8-bar compositions are used. compose() rolls 4 or 8 bars
    # (60/40), and a 4-bar Night Metro beat has no bar 5 to drop — the
    # research says one breakdown per 8-BAR phrase. That is a real
    # limitation of the fix and it is in the READ ME, not hidden here.
    composed, v = [], 0
    while len(composed) < NBEATS and v < 40:
        q = json.loads(json.dumps(base))
        compose(q, NAME, v)
        vary_preset(q, v, base["num"], tempo_locked=True)
        if bars_of(q) >= BREAKDOWN["bar"]:
            composed.append((v, q))
        v += 1
    if len(composed) < NBEATS:
        print("WARNING: could not find enough 8-bar compositions.")

    for i, (v, q) in enumerate(composed):
        ref = None
        for tag, bd, dirt, eq, echo, chorus in VERSIONS:
            p = json.loads(json.dumps(q))
            p = __import__("crew").normalize_preset(p)
            p.pop("breakdown", None)
            p.pop("allow_dirt", None)
            if bd:
                p["breakdown"] = bd
            if dirt:
                p["allow_dirt"] = dirt
            kit, _ = build_kit(shots, NAME, stamps[NAME][1], variant=v,
                               avoid=set(avoid), preset=p)
            L, R, got = render_crew_beat(NAME, kit, preset=p, eq=eq,
                                         echo=echo, chorus=chorus)
            low, air = band_db(L, R, hi=100.0), band_db(L, R, lo=8000.0)
            b5 = bar5_rms_db(L, R, p["bpm"], len(p["lanes"]["kick"][3]))
            drops.append((f"beat {i + 1} {tag}", b5))
            if ref is None:
                ref = (low, air, np.asarray(L).copy())
            else:
                deltas.append((f"beat {i + 1} {tag}", low - ref[0],
                               air - ref[1],
                               float(np.abs(np.asarray(L)
                                            - ref[2][:len(L)]).max())))
            fn = f"{NAME} {p['bpm']}bpm beat {i + 1} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:48s} LUFS {got:6.2f}  peak {peak:6.2f}  "
                  f"low {low:6.2f}  air {air:6.2f}  bar5 {b5:+6.2f}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, deltas, drops))
    shutil.rmtree(scratch)

    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    want = NBEATS * len(VERSIONS)
    if n != want:
        print(f"WARNING: expected {want} files.")
    same = [k for k, _lo, _ai, d in deltas if d < 1e-6]
    if same:
        print("WARNING: rendered IDENTICAL to 'a Now':\n  "
              + "\n  ".join(same))
    # the breakdown must actually make bar 5 quieter than the beat
    weak = [f"{k} ({v:+.2f} dB)" for k, v in drops
            if "Now" not in k and v > -1.0]
    if weak:
        print("WARNING: bar 5 did NOT drop on:\n  " + "\n  ".join(weak))


def _avg(rows, tag, idx):
    v = [r[idx] for r in rows if tag in r[0]]
    return float(np.mean(v)) if v else 0.0


def readme(rows, deltas, drops):
    lufs = [r[1] for r in rows]
    lines = [
        f"NIGHT METRO — the drop, the grit, the effects   {date.today()}",
        "=" * 62, "",
        "WHY THIS BATCH",
        "  Second DJ in the pass. Three things the research said, and",
        "  what your code was actually doing instead:",
        "",
        "   * His big moment — bar 5 drops to the 808 alone — was in his",
        "     description and in one prototype file, and in almost none",
        "     of the beats you actually get. Measured: 0 out of 12. It",
        "     is pinned now, so it happens every time.",
        "   * His 808 distortion is the second heaviest on the roster",
        "     and has NEVER played, because the clean rule switches all",
        "     dirt off. You opened it for the low end only. So the 808",
        "     gets its grit and the rest of the mix stays clean, which",
        "     is what his research asks for in as many words.",
        "   * His research wants heavy lows and bright, crisp hats.",
        "     That is the EQ you approved, unchanged. Note this is the",
        "     OPPOSITE of what Otto got — Otto's sources say dull, these",
        "     say bright, and the research wins for each of them.",
        "",
        "THREE BEATS. FOUR VERSIONS EACH. Each step adds ONE thing:",
        "",
        "  a Now       today's sound.",
        "  b Drop      just the bar-5 breakdown. No effects at all.",
        "  c Research  b, plus the 808 grit and the EQ.",
        "  d Plus      c, plus the echo on the clap and a widener on",
        "              the reversed-cymbal riser.",
        "",
        "  Four rungs and not three because you asked for the",
        "  arrangement fix in this batch. If a/b/c/d were one jump you",
        "  could not tell me whether it was the drop or the effects, and",
        "  that is the whole answer I need.",
        "",
        "WHAT TO LISTEN FOR",
        "  a -> b: bar 5 (about 8 seconds in). Does the beat falling",
        "  away to just the 808 sound like drama, or like a mistake?",
        "  b -> c: is the 808 heavier and dirtier in a good way, or",
        "  does it start to sound broken?",
        "  c -> d: does the echo on the clap add scale, or clutter?",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS — you are judging",
        "  character, not loudness.",
        "",
        "  Bar 5 against the rest of the beat, measured up top where",
        "  the hats and the clap live (the 808 stays, so measuring the",
        "  whole sound would just measure the 808):",
        f"    a Now       {_avg(drops, 'a Now', 1):+.2f} dB   "
        "(no drop — bar 5 is just another bar)",
        f"    b Drop      {_avg(drops, 'b Drop', 1):+.2f} dB",
        f"    c Research  {_avg(drops, 'c Research', 1):+.2f} dB",
        f"    d Plus      {_avg(drops, 'd Plus', 1):+.2f} dB",
        "",
        "  Against each beat's own 'a Now', in the FINISHED files:",
        f"    c   weight under 100 Hz  {_avg(deltas, 'c Research', 1):+.2f} dB"
        f"     air above 8 kHz  {_avg(deltas, 'c Research', 2):+.2f} dB",
        f"    d   weight under 100 Hz  {_avg(deltas, 'd Plus', 1):+.2f} dB"
        f"     air above 8 kHz  {_avg(deltas, 'd Plus', 2):+.2f} dB",
        "",
        "  About 1 dB is where a broad change becomes obvious. So the",
        "  low end moving +2 dB is real and you will hear it.",
        "",
        "  BUT READ THE AIR NUMBER HONESTLY: the EQ adds air, and the",
        "  measurement says the top went slightly DOWN. That is not the",
        "  EQ failing. The 808 grit makes the low end much heavier, and",
        "  the loudness stage then pulls the whole file back to hit the",
        "  same target — which takes a little off the top on the way",
        "  past. Net: the beat gets heavier, not brighter. If you want",
        "  him brighter as well, that is a second, separate change.",
        "",
        "DELIBERATELY LEFT OUT",
        "  * The phaser, and any wobble on the hats or the clap. His",
        "    research says keep those clean and bright against the heavy",
        "    low end. The widener in d is on the riser ONLY.",
        "  * Everything for the other seven DJs and the twelve legends.",
        "",
        "NOT HEARD",
        "  Whether bar 5 falling silent reads as his signature or as a",
        "  hole; whether the 808 grit is the right amount (5.0 is a",
        "  number that has never been heard, only written down);",
        "  whether the riser wants widening at all. I can measure that",
        "  each one happens. I cannot tell you if it sounds like him.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  Two lines. One: how far up the ladder to go — a / b / c / d.",
        "  Two: is bar 5 right, or should the drop be somewhere else,",
        "  or shorter?",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:48s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
