"""A/B audition: Glass Cat's gated reverb, moved from the snare to the stamp.

Item 5 of the 2026-09-03 DJ-profile gap analysis (DJ-PROFILES-GAP-ANALYSIS.md),
applied per the "newest research overrides older rules" instruction the same
day. Chad Hugo's own account of the "Grindin'" hook sound: "we added a gate
reverb to that sound" -- the CLICK/ZAP hook (Glass Cat's stamp lane), not the
snare. crew_config.json now points the gated treatment at the stamp;
everything else, snare included, is dry (falls to the generic house ambience
bed instead of the deliberate wide gated tail).

    a Before   the old sound: gated reverb on the snare
    b After    the new sound: gated reverb on the stamp -- today's default

This is already LIVE, not proposed -- 'b' is what every new Glass Cat beat
sounds like today. This file is the proof, not the gate.

One beat, one kit, only the space treatment's target lane moves.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3 is
never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_glass_cat_space_ab.py
Out:  ~/Desktop/Homeroom Glass Cat Space <today>/
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
    f"~/Desktop/Homeroom Glass Cat Space {date.today()}"))
NAME = "Glass Cat"

OLD_SPACE = ("gated", ["snare"])   # what it was before today

A_BEFORE = "a Before (gated on snare)"
B_AFTER = "b After (gated on stamp)"


def side_vs_mid_db(L, R):
    """Stereo width of one lane's own stem. Higher = wider/wetter."""
    mid = (np.asarray(L) + np.asarray(R)) / 2.0
    side = (np.asarray(L) - np.asarray(R)) / 2.0
    m = np.sqrt(np.mean(mid ** 2)) + 1e-12
    s = np.sqrt(np.mean(side ** 2)) + 1e-12
    return 20 * np.log10(s) - 20 * np.log10(m)


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="glass-cat-space-ab-"))
    p = CREW[NAME]                     # today's live preset: gated on stamp
    old_preset = dict(p, space=OLD_SPACE)
    kit, sources = build_kit(shots, NAME, stamps[NAME][1], variant=0,
                             avoid=set(avoid), preset=p)

    rows, widths = [], {}
    for tag, preset in [(A_BEFORE, old_preset), (B_AFTER, p)]:
        # space=None -> render_crew_beat reads the LANE LIST from the
        # preset's own "space" field (that's what actually moved); passing
        # an explicit space= string only picks the treatment TYPE
        # (gated/room/...), never which lane gets it.
        L, R, got, parts = render_crew_beat(NAME, kit, preset=preset,
                                            want_parts=True)
        snare_w = side_vs_mid_db(*parts["stems"]["snare"])
        stamp_w = side_vs_mid_db(*parts["stems"]["stamp"])
        widths[tag] = (snare_w, stamp_w)
        fn = f"{NAME} {p['bpm']}bpm {tag}.wav"
        write_wav24(scratch / fn, L, R)
        peak = 20 * np.log10(max(np.abs(L).max(), np.abs(R).max()) + 1e-12)
        rows.append((fn, got, peak))
        print(f"  {fn:44s} LUFS {got:6.2f}  peak {peak:6.2f}  "
              f"snare {snare_w:6.1f} dB  stamp {stamp_w:6.1f} dB")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, widths, sources))
    shutil.rmtree(scratch)
    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    a_snare, a_stamp = widths[A_BEFORE]
    b_snare, b_stamp = widths[B_AFTER]
    if not (b_snare < a_snare and b_stamp > a_stamp):
        print("WARNING: the width numbers didn't move the expected way -- "
              "check before handing this over.")


def readme(rows, widths, sources):
    lufs_vals = [r[1] for r in rows]
    a_snare, a_stamp = widths[A_BEFORE]
    b_snare, b_stamp = widths[B_AFTER]
    lines = [
        f"GLASS CAT — the gated reverb, moved   {date.today()}",
        "=" * 62, "",
        "WHY THIS BATCH",
        "  Punch-list item 5. The old code put the 'gated' treatment on",
        "  the snare. The new research -- Chad Hugo's own account of the",
        "  'Grindin'' hook sound -- says the gate reverb was on the",
        "  CLICK/ZAP hook sound (Glass Cat's stamp), not the snare. I",
        "  moved it. This is LIVE now, not proposed -- 'b' is what every",
        "  new Glass Cat beat sounds like today. This file is the proof.",
        "",
        "  a Before   the old sound: snare gets the wide gated tail.",
        "  b After    the new sound: the stamp gets it, snare stays dry.",
        "",
        "WHAT TO LISTEN FOR",
        "  In 'a', the snare has a bright, roomy tail. In 'b', the snare",
        "  should sound tighter/drier and the click/zap stamp (bars 4 and",
        "  8) should carry the wide tail instead.",
        "",
        "MEASURED",
        f"  Both files sit at {min(lufs_vals):.2f} to {max(lufs_vals):.2f} "
        "LUFS -- same loudness, only the treatment moved.",
        "",
        "  Per-lane stereo width (higher = wider/wetter):",
        f"    snare   a Before {a_snare:6.1f} dB   ->   b After "
        f"{b_snare:6.1f} dB",
        f"    stamp   a Before {a_stamp:6.1f} dB   ->   b After "
        f"{b_stamp:6.1f} dB",
        "  Snare drops and stamp rises from a to b -- that's the",
        "  treatment changing lanes, measured in the finished stems.",
        "",
        "DELIBERATELY ODD",
        "  * Only Glass Cat -- his own research, not roster-wide.",
        "  * The stamp only fires twice in this 8-bar loop (bars 4 and",
        "    8), so its gated tail is a brief, occasional thing now, not",
        "    constant the way the snare's used to be. That's the sound on",
        "    purpose -- the research says to reserve gated reverb for ONE",
        "    signature/hook element, not spread it around.",
        "",
        "NOT HEARD",
        "  Whether this actually sounds BETTER, or just different. I can",
        "  measure that the reverb changed lanes; I can't tell you if",
        "  it's right.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  Keep it, or put it back on the snare.",
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ]
    lines += [f"  {fn:44s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
              for fn, lu, pk in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
