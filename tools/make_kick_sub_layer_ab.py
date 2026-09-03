"""A/B audition: Otto Grit's kick reinforced with a short gated sub-oscillator.

Item 3 of the 2026-09-03 DJ-profile gap analysis (DJ-PROFILES-GAP-ANALYSIS.md).
Engineer Todd Fairall's account of the Fantastic Vol. 2 sessions: Dilla's
sampled kick was reinforced with a separate ~40Hz sine, gated tightly to the
kick trigger — short, no sustain, extra sub weight under the sampled hit,
not a second audible drum. groove.kick_layer() already existed for this
shape of thing but had zero callers (2026-09-02 audit); this is the first
real use, via the new groove.kick_sub_reinforce() (additive, not a
kick_layer crossover — see that function's docstring for why).

    a Now      today's sound, untouched
    b Light    +0.35 amount — a conservative first guess
    c Full     +0.60 amount — noticeably more weight

freq_hz (40) and dur_s (0.12s) are pinned across b/c so only the amount
moves, same one-thing-at-a-time discipline as the low-shelf batch. Not
roster-wide: this is Otto Grit's own researched trait and nobody else's
preset carries the field.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3 is
never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_kick_sub_layer_ab.py
Out:  ~/Desktop/Homeroom Kick Sub Layer <today>/
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
from groove import lp4

DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Kick Sub Layer {date.today()}"))
NAME = "Otto Grit"

VERSIONS = [("a Now", None),
            ("b Light", dict(freq_hz=40.0, dur_s=0.12, amount=0.35)),
            ("c Full", dict(freq_hz=40.0, dur_s=0.12, amount=0.60))]


def low_band_db(L, R, hz=100.0):
    """ABSOLUTE energy under 100 Hz in the FINISHED file — same ruler as
    the low-shelf batch, for the same reason: kick_sub_reinforce runs on
    the raw kick sample, well before glue_compress/master()/
    master_to_lufs, and those stages peak-normalise, soft-clip, then
    loudness-normalise — a low-end addition that survives the buffer can
    still be given back before it reaches the file."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    freqs = np.fft.rfftfreq(len(mono), 1 / SR)
    return 10 * np.log10(spec[freqs <= hz].sum() / len(mono) + 1e-30)


def sample_low_rms(x, hz=100.0):
    """Low-band RMS of the RAW KICK SAMPLE itself, not the finished mix —
    the per-hit number. The whole-file measure above averages a short
    ~120ms addition over an entire 8-bar loop of mostly silence between
    kick hits, which undersells a real per-hit effect the same way a
    share-of-total ruler undersold the low shelf (see DECISIONS.md
    2026-09-03). Both numbers get reported; neither alone is honest."""
    return np.sqrt((lp4(x, hz) ** 2).mean())


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="kick-sub-ab-"))
    p = CREW[NAME]
    rows, lows, kick_gains, sources = [], [], [], {}
    base_low = base_kick_low = None
    for tag, sub_layer in VERSIONS:
        preset = dict(p, sub_layer=sub_layer)
        # fresh avoid copy each pass, same variant/seed -> the SAME kick
        # (and every other lane) gets picked all three times; only the
        # sub layer differs
        kit, sources = build_kit(shots, NAME, stamps[NAME][1], variant=0,
                                 avoid=set(avoid), preset=preset)
        kick_low = sample_low_rms(kit["kick"])
        if base_kick_low is None:
            base_kick_low = kick_low
        else:
            kick_gains.append(
                (tag, 20 * np.log10(kick_low / (base_kick_low + 1e-12))))
        L, R, got = render_crew_beat(NAME, kit, preset=p)
        lb = low_band_db(L, R)
        if base_low is None:
            base_low = lb
        else:
            lows.append((tag, lb - base_low))
        fn = f"{NAME} {p['bpm']}bpm {tag}.wav"
        write_wav24(scratch / fn, L, R)
        peak = 20 * np.log10(max(np.abs(L).max(), np.abs(R).max()) + 1e-12)
        rows.append((fn, got, peak))
        print(f"  {fn:44s} LUFS {got:6.2f}  peak {peak:6.2f}  "
              f"low {lb:6.2f} dB")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(
        readme(rows, lows, kick_gains, sources))
    shutil.rmtree(scratch)
    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    if n != len(VERSIONS):
        print(f"WARNING: expected {len(VERSIONS)} files.")
    flat = [v for _, v in lows if abs(v) < 0.10]
    if flat:
        print("WARNING: the sub layer barely survived the master stage on "
              + ", ".join(t for t, v in lows if abs(v) < 0.10))


def readme(rows, lows, kick_gains, sources):
    lufs_vals = [r[1] for r in rows]
    kick_name = Path(sources.get("kick", "") or "?").name
    lines = [
        f"OTTO GRIT'S KICK — a sub layer underneath it?   {date.today()}",
        "=" * 62, "",
        "WHY THIS BATCH",
        "  Punch-list item 3 (DJ-PROFILES-GAP-ANALYSIS.md). The research",
        "  on Dilla's engineer Todd Fairall says the sampled kick on",
        "  Fantastic Vol. 2 got a second layer under it: a short, quiet",
        "  ~40Hz tone, gated tight to the kick hit. Not a second kick you'd",
        "  notice — just more weight under the one that's already there.",
        "",
        "  This is brand new. Nothing has ever used it before today.",
        "",
        "ONE beat, one kick sample, THREE versions:",
        "",
        "  a Now      today's sound. Nothing added.",
        "  b Light    a little of that sub tone under the kick.",
        "  c Full     more of it.",
        "",
        "WHAT TO LISTEN FOR",
        "  Does the kick feel heavier / rounder in b and c? Or does it",
        "  start to sound like two things instead of one — a separate low",
        "  thump under the kick rather than more weight IN it? That second",
        "  read is the failure mode Fairall's own account says to avoid.",
        "",
        "MEASURED — TWO NUMBERS, READ BOTH",
        f"  All 3 files sit between {min(lufs_vals):.2f} and "
        f"{max(lufs_vals):.2f} LUFS — you're judging weight, not loudness.",
        "",
        "  (1) On the kick SAMPLE itself, right where the sub tone sits:",
    ] + [f"    {tag:10s} {v:+6.2f} dB" for tag, v in kick_gains] + [
        "  That's a real, sizeable addition — well past the ~1 dB line",
        "  where a change this broad is usually audible.",
        "",
        "  (2) Averaged over the WHOLE finished file (8 bars, mostly gaps",
        "  between kick hits):",
    ] + [f"    {tag:10s} {v:+6.2f} dB" for tag, v in lows] + [
        "  Much smaller — because this ruler spreads one ~120ms addition",
        "  across the whole loop's silence, the same way a share-of-total",
        "  ruler undersold the low shelf on 2026-09-03. Don't read (2) as",
        "  'it didn't work' — (1) is what actually happens at the hit;",
        "  (2) just isn't the right ruler for a per-hit effect. Your ear",
        "  hears (1), at the moment of the kick, not an average.",
        "",
        "DELIBERATELY ODD",
        "  * Only Otto Grit — this is his research, not a roster-wide",
        "    effect. Nobody else's preset has this field.",
        "  * Same kick sample all three times, so only the sub layer",
        f"    changes. Source: {kick_name}",
        "",
        "NOT HEARD",
        "  Whether b or c (or neither) is right, and whether it reads as",
        "  weight or as a second drum. I can measure the low-end gain; I",
        "  can't tell you which one sounds like Dilla.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  a / b / c — or 'none of these, drop it'.",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:44s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
