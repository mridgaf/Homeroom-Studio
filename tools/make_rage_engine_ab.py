"""A/B audition: Rage Engine, third of the per-DJ pass.

Two research findings, both measured before anything was touched:

  * His stacked saturation has NEVER PLAYED. kick_dist=6.0 (highest on
    the roster) AND mix_sat=4.0 (the only nonzero one) AND drive=1.55
    (highest) are all switched off by the 2026-07-18 clean-render rule.
    His research calls that stack "the core of the 'wall of sound'
    identity" — so the one persona built on saturation is the one
    persona rendering without any. This needs allow_dirt=True, not
    Night Metro's "low": his research asks for element-level AND
    mix-bus grit, explicitly stacked.
  * "Wall-to-wall 32nd hat rolls; sparse hats are WRONG for this
    persona." Measured across 24 composed beats: 12 of 24 come out with
    hats under 50% density. His grammar gives rolls 0.35 and spreads
    the rest across seven shapes including an explicitly sparse one.
    Owner's call 2026-09-03: "rolls usually, some variety left."

    a Now         today's sound.
    b Rolls       the hat grammar only. Every other lane is IDENTICAL —
                  the hat lane is swapped in from a second composition
                  of the same beat, so nothing else can move.
    c Wall half   b + half the written saturation + the approved EQ.
    d Wall full   b + the saturation numbers exactly as written.

The EQ rides in c and d rather than being its own rung. It is already
approved and his research asks for bright aggressive highs, so it is not
the question — the saturation is, and it has never been heard at all.

DELIBERATELY LEFT OUT: echo, chorus, phaser. His research says the mix is
glued by SATURATION, not modulation, and that there is no letup to carve
into. Adding a delay to a wall of sound is clutter, not character.

NOT CHANGED, and deliberately: the extra snare fill stays a coin flip
(burst_p 0.5) rather than the every-4-bars rule the research states —
his call, 2026-09-03. And "never leave a bar empty" is left alone: only
1 bar in 124 measured fully empty, so the 2026-07-29 rule that allows
silence is barely touching him.

Run:  ./.venv/bin/python tools/make_rage_engine_ab.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom Rage Engine <today>/
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
    f"~/Desktop/Homeroom Auditions/Homeroom Rage Engine {date.today()}"))
NAME = "Rage Engine"
NBEATS = 3

EQ = OWNER_TASTE["mix_eq"]      # unchanged — his research wants bright

# ROLLS USUALLY, SOME VARIETY LEFT (owner 2026-09-03). rolls32 takes
# three quarters of the weight; `sparse` is removed for him alone,
# because his research names it as wrong for this persona; the remaining
# quarter is spread evenly over the six shapes that are still in
# character. Nobody else's grammar is touched.
ROLL_MODES = [["eighths", 0.0417], ["sixteenths", 0.0417],
              ["broken", 0.0417], ["offbeats", 0.0417],
              ["gallop", 0.0417], ["answer", 0.0417],
              ["rolls32", 0.75]]

# (tag, rolling hats, dirt, kick_dist, mix_sat, drive, eq)
VERSIONS = [
    ("a Now",       False, None, None, None, None, None),
    ("b Rolls",     True,  None, None, None, None, None),
    ("c Wall half", True,  True, 3.0,  2.0,  1.25, EQ),
    ("d Wall full", True,  True, 6.0,  4.0,  1.55, EQ),
]


def _hits_per_bar(bars):
    return sum(b.count("x") + b.count("o") + b.count("X")
               for b in bars) / max(1, len(bars))


def measure_roll_rate(base, n=60):
    """How often the hat lane comes out ROLLING, across n composed beats,
    stock grammar vs the new one.

    Counts the mode the hat lane was built in — a 32-step bar means
    rolls32, the only hat mode on that grid. Deliberately NOT an average
    hits-per-bar across all beats: that number moves with the loop length
    and with vary_preset's thinning as well as with the grammar, and the
    first version of this reported 10.0 -> 10.3 for a change that is
    plainly larger than that. The mode pick is what the weight controls,
    so the mode pick is what gets reported."""
    out = []
    for modes in (None, ROLL_MODES):
        hit = seen = 0
        for v in range(n):
            q = json.loads(json.dumps(base))
            if modes:
                q["grammar"] = dict(q["grammar"],
                                    hat=dict(q["grammar"]["hat"],
                                             modes=modes))
            compose(q, NAME, v)
            lane = q["lanes"].get("hat")
            if lane:
                seen += 1
                hit += len(lane[3][0]) == 32
        out.append(hit / max(1, seen))
    return out[0], out[1]


def hat_density(preset):
    """HITS PER BAR in the hat lane — the ruler for the grammar change,
    read off the PATTERN because that is what changed.

    Hits per bar, NOT share-of-steps, and the difference matters. The
    first version of this measured the share and reported the rolling
    grammar as LESS dense, which the fail-loud check caught. Cause:
    `rolls32` returns a 32-STEP bar (16ths on a 32nd grid, plus roll
    bursts) while `sixteenths` returns a 16-step bar. A share compares
    those two as if their steps were the same size — 16 hits in 32 steps
    reads as 50% and 16 hits in 16 steps reads as 100%, for exactly the
    same number of hats in the same bar of music. Counting hits is
    grid-independent; a share is not.

    Also worth writing down, since the name misled me: `rolls32` is NOT
    wall-to-wall 32nds. It is steady 16ths on the 32nd grid with one to
    three accelerating bursts landing on beat 3 and the bar line — which
    is the trap hat the research actually describes ("rolls that ramp
    INTO the snare"), just not what its name suggests."""
    lane = preset["lanes"].get("hat")
    if not lane:
        return 0.0
    bars = lane[3]
    return _hits_per_bar(bars)


def crest_db(L, R):
    """Peak-to-RMS, in dB, of the FINISHED file. This is the ruler for
    saturation: distortion and glue fill in the gaps between the peaks,
    so a squashed mix has a SMALLER crest than an open one. Loudness
    normalisation cannot hide it the way it hides a band boost — it
    scales peak and RMS together, so their ratio survives."""
    m = 0.5 * (np.asarray(L) + np.asarray(R))
    return (20 * np.log10(np.abs(m).max() + 1e-12)
            - 20 * np.log10(np.sqrt((m ** 2).mean()) + 1e-12))


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the finished file — not a share of
    the total, which moves whenever anything else moves."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def build_pair(base, v):
    """One beat, composed twice — stock hat grammar and rolling hat
    grammar — then returned as (now, rolls) where the ONLY difference is
    the hat lane. Composing each version separately would let the loop
    length and the kick move too, and then 'b' would not be a test of
    the hats at all. Returns None if the two compositions disagree on
    length (compose() carries repeat history across calls, so the same
    variant can land on a different roll)."""
    stock = json.loads(json.dumps(base))
    compose(stock, NAME, v)
    rolling = json.loads(json.dumps(base))
    rolling["grammar"] = dict(rolling["grammar"],
                              hat=dict(rolling["grammar"]["hat"],
                                       modes=ROLL_MODES))
    compose(rolling, NAME, v)
    if bars_of(stock) != bars_of(rolling) or "hat" not in stock["lanes"] \
            or "hat" not in rolling["lanes"]:
        return None
    # AND the roll has to have actually landed. He kept a quarter of the
    # weight on the other shapes, so about one beat in four still rolls
    # a non-rolling hat — those are the setting WORKING, but they are
    # not the sound he is being asked to judge. Selecting for the roll
    # is deliberate and it is stated in the READ ME with the real rate,
    # rather than quietly stacking the deck.
    now = json.loads(json.dumps(rolling))
    now["lanes"]["hat"] = stock["lanes"]["hat"]
    for q in (now, rolling):
        vary_preset(q, v, base["num"], tempo_locked=True)
    # Check AFTER vary_preset, not before. vary_preset thins lanes, and a
    # pair that looked busier at composition can come out quieter once it
    # has run — one beat slipped through exactly that way and the
    # fail-loud check caught it.
    if _hits_per_bar(rolling["lanes"]["hat"][3]) \
            <= _hits_per_bar(now["lanes"]["hat"][3]):
        return None
    return now, rolling


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="rage-ab-"))
    base = CREW[NAME]

    print("Measuring the roll rate over 60 composed beats…")
    rate = measure_roll_rate(base)
    print(f"  beats whose hats roll: {rate[0] * 100:.0f}% -> "
          f"{rate[1] * 100:.0f}%")
    pairs, v = [], 0
    while len(pairs) < NBEATS and v < 120:
        got = build_pair(base, v)
        if got:
            pairs.append((v, got))
        v += 1
    if len(pairs) < NBEATS:
        print("WARNING: could not build enough matched pairs.")

    rows, dens, crests, lows = [], [], [], []
    import crew as _crew
    for i, (v, (now, rolling)) in enumerate(pairs):
        ref_crest = ref_low = None
        for tag, roll, dirt, kd, ms, dr, eq in VERSIONS:
            p = json.loads(json.dumps(rolling if roll else now))
            if dirt:
                p["allow_dirt"] = True
                p["kick_dist"], p["mix_sat"], p["drive"] = kd, ms, dr
            p = _crew.normalize_preset(p)
            kit, _ = build_kit(shots, NAME, stamps[NAME][1], variant=v,
                               avoid=set(avoid), preset=p)
            L, R, got = render_crew_beat(NAME, kit, preset=p, eq=eq)
            cr, low = crest_db(L, R), band_db(L, R, hi=100.0)
            d = hat_density(p)
            dens.append((f"beat {i + 1} {tag}", d))
            if ref_crest is None:
                ref_crest, ref_low = cr, low
            crests.append((f"beat {i + 1} {tag}", cr - ref_crest))
            lows.append((f"beat {i + 1} {tag}", low - ref_low))
            fn = f"{NAME} {p['bpm']}bpm beat {i + 1} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:48s} LUFS {got:6.2f}  peak {peak:6.2f}  "
                  f"hats {d * 100:5.1f}%  crest {cr:5.2f}  low {low:6.2f}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, dens, crests, lows, rate))
    shutil.rmtree(scratch)

    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    want = NBEATS * len(VERSIONS)
    if n != want:
        print(f"WARNING: expected {want} files.")
    # FAIL LOUD — each version has to prove its own premise
    # AVERAGE, not per beat: he asked to keep some variety, so roughly
    # one beat in four is expected to roll a non-rolling shape. A single
    # beat going the other way is the setting working; the AVERAGE going
    # the other way is a bug.
    if _avg(dens, "b Rolls") <= _avg(dens, "a Now"):
        print(f"WARNING: hats did not get denser on average — "
              f"{_avg(dens, 'a Now'):.1f} -> {_avg(dens, 'b Rolls'):.1f} "
              f"hits/bar")
    quiet = [k for k, d in dens if "b Rolls" in k
             and d <= dict(dens)[k.replace("b Rolls", "a Now")]]
    if quiet:
        print("WARNING: a selected beat's hats did NOT get busier:\n  "
              + "\n  ".join(quiet))
    soft = [f"{k} ({c:+.2f} dB)" for k, c in crests
            if "Wall" in k and c > -0.2]
    if soft:
        print("WARNING: the saturation did NOT squash the mix on:\n  "
              + "\n  ".join(soft))


def _avg(rows, tag):
    v = [r[1] for r in rows if tag in r[0]]
    return float(np.mean(v)) if v else 0.0


def readme(rows, dens, crests, lows, rate):
    lufs = [r[1] for r in rows]
    lines = [
        f"RAGE ENGINE — the wall of sound he has never heard   {date.today()}",
        "=" * 64, "",
        "WHY THIS BATCH",
        "  Third DJ in the pass. Two things the research says, and what",
        "  the code was doing instead:",
        "",
        "   * He is the only DJ on the roster built on DISTORTION — grit",
        "     on the 808 and glue across the whole mix, stacked. His",
        "     research calls that stack the core of who he is. None of",
        "     it has ever played, not once, because the clean rule",
        "     switches all of it off. The loudest, dirtiest personality",
        "     you have is the one rendering completely clean.",
        "   * Wall-to-wall 32nd hat rolls, and sparse hats are flat out",
        "     wrong for him. Measured on 24 of his beats: half of them",
        "     came out with the hats under half density. You said rolls",
        "     usually, some variety left. That is what b does.",
        "",
        "THREE BEATS. FOUR VERSIONS EACH:",
        "",
        "  a Now         today's sound.",
        "  b Rolls       the hats, and ONLY the hats. Every other lane",
        "                is note-for-note identical to a.",
        "  c Wall half   b, plus half the grit, plus the EQ.",
        "  d Wall full   b, plus the grit at the numbers written in his",
        "                file all along — 808 at 6, mix glue at 4.",
        "",
        "  The EQ is not its own rung. You already approved it and his",
        "  research asks for bright aggressive highs, so it is not the",
        "  question. The grit is the question, and c vs d is the ladder.",
        "",
        "WHAT TO LISTEN FOR",
        "  a -> b: do the hats now run wall to wall? This is the only",
        "  change, so if a and b sound the same, tell me — that means",
        "  the hats were not the thing making him feel tame.",
        "  b -> c -> d: does he get harder and heavier, or does he just",
        "  get squashed and smaller? That is the real risk with grit",
        "  this heavy, and it is why d is here rather than assumed.",
        "",
        "MEASURED",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS — you are judging",
        "  character, not loudness.",
        "",
        "  How busy the hats are, in hits per bar (counting hits, not",
        "  the share of the grid — his rolling pattern uses a finer grid,",
        "  so a percentage would compare two different rulers):",
        f"    a Now         {_avg(dens, 'a Now'):.1f} hits per bar",
        f"    b / c / d     {_avg(dens, 'b Rolls'):.1f} hits per bar",
        "",
        "  ACROSS ALL HIS BEATS, not just these three — measured over",
        "  60 composed beats, so you see the real rate and not only the",
        "  ones I picked. How often his hats come out ROLLING:",
        f"      {rate[0] * 100:.0f}%  ->  {rate[1] * 100:.0f}%",
        "",
        "  THAT IS LOWER THAN IT SOUNDS LIKE IT SHOULD BE, and here is",
        "  the honest reason. About two beats in three take their pattern",
        "  from your drum-pattern library instead of composing one, and",
        "  when a library pattern brings its own hats, the grammar never",
        "  gets a say. Measured: 40 of 60. So this change can only reach",
        "  the third of his beats that actually compose their hats.",
        "  If you want him rolling wall-to-wall EVERY time, the lever is",
        "  the library, not this setting — a bigger change, and yours to",
        "  call after you hear this one.",
        "",
        "  THE THREE BEATS HERE WERE SELECTED so the new setting",
        "  actually chose a rolling hat. You kept a quarter of the",
        "  weight on the other shapes, so roughly one beat in four will",
        "  still come out with a different hat pattern — that is the",
        "  setting working as you asked, not a fault. But those beats",
        "  would not let you hear the thing being auditioned, so they",
        "  are not in the folder. Saying so rather than stacking the",
        "  deck quietly.",
        "",
        "  Per beat, in this folder:",]
    for k, d in dens:
        if "b Rolls" in k:
            was = dict(dens)[k.replace("b Rolls", "a Now")]
            lines.append(f"    {k.split()[1]}  {was:5.1f} -> {d:5.1f}"
                         " hits per bar")
    lines += [
        "",
        "  How squashed the mix is, against each beat's own 'a Now'.",
        "  Grit fills in the gaps between the peaks, so a wall of sound",
        "  measures SMALLER here. This is the ruler that cannot be",
        "  hidden by the loudness stage:",
        f"    c Wall half   {_avg(crests, 'c Wall half'):+.2f} dB",
        f"    d Wall full   {_avg(crests, 'd Wall full'):+.2f} dB",
        "",
        "  Weight under 100 Hz, against each beat's own 'a Now':",
        f"    c Wall half   {_avg(lows, 'c Wall half'):+.2f} dB",
        f"    d Wall full   {_avg(lows, 'd Wall full'):+.2f} dB",
        "",
        "DELIBERATELY LEFT OUT",
        "  * Echo, chorus, phaser. His research says the mix is glued by",
        "    saturation, not by modulation, and that there is no gap to",
        "    put a delay in. Adding one to a wall of sound is clutter.",
        "  * The extra snare fill stays a coin flip, not the every-4-bars",
        "    rule the research states. Your call, and it is already",
        "    happening about half the time.",
        "  * 'Never leave a bar empty' — measured 1 empty bar in 124, so",
        "    the rule that allows silence is barely touching him. Left",
        "    alone rather than overriding a decision you made.",
        "",
        "NOT HEARD",
        "  Whether 6.0 and 4.0 are right, or whether they are numbers",
        "  someone wrote down years ago that nobody ever listened to.",
        "  That is the honest state of it: those two values have been in",
        "  his file the whole time and have never made a sound.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  Two lines. One: a / b / c / d.",
        "  Two: did b alone change anything you could hear?",
        "",
        "-" * 64,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:48s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
