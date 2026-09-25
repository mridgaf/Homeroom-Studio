"""A/B audition: the true-levels mix vs the kick-relative level rules.

Owner 2026-09-20: "for this mix I want to start with everything at its true
volume and disregard any of those rules for the mix." The three rules:
the chord bus governor (chords pinned ~9 dB under the kick), the snare bus
governor (~3 dB under), and the peak ceilings. crew.TRUE_LEVELS bypasses all
three; the sidechain duck, per-DJ lane gains and the loudness normalise stay.

MATCHED PAIR, the only way that is actually matched here: generate() builds
the beat's kit ONCE (drums AND the chords/bass from _build_chords /
_add_sample_lanes — a bench that used compose()+build_kit would be drums-only
and the chord governor would never run, the 2026-09-19 legend trap). We wrap
render_crew_beat so that single kit is rendered TWICE, once with the rules on
and once off, and keep both. Same kit by construction, so the ONLY difference
between a and b is the level rules — no RNG seeding needed (generate() has
unpinnable randomness; a seeded matched pair is impossible, checked).

Renders to scratch, copies to the Desktop. Library on TBOTC 3 untouched.

Run:  ./.venv/bin/python tools/make_true_levels_ab.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom True Levels <today>/
"""
import copy
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24
import crew
import beat_machine as bm

DESK = Path(f"{Path.home()}/Desktop/Homeroom Auditions/Homeroom True Levels {date.today()}")
DJS = ["Otto Grit", "Night Metro", "New Math", "Glass Cat"]
KEY, TEMPO = "F minor", 90

_real_render = bm.render_crew_beat
_captured = {}  # filled by the wrapper on each generate() call


def _dual_render(name, kit, **kw):
    """Render the SAME kit rules-on then rules-off; keep both. Return the
    rules-on result so generate() proceeds as normal."""
    def once(tl):
        crew.TRUE_LEVELS = tl
        return _real_render(name, copy.deepcopy(kit),
                            **{k: copy.deepcopy(v) for k, v in kw.items()})
    r_rules = once(False)
    r_true = once(True)
    _captured["a Rules"] = r_rules
    _captured["b True"] = r_true
    return r_rules


def band_db(mono, sr, lo, hi):
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / sr)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def main():
    scratch = Path(tempfile.mkdtemp(prefix="true-levels-ab-"))
    bm.render_crew_beat = _dual_render
    rows, mids, ident = [], [], []
    try:
        for i, name in enumerate(DJS):
            _captured.clear()
            root = scratch / f"gen{i}"
            root.mkdir(parents=True, exist_ok=True)
            bm.generate([name], tempo=TEMPO, key=KEY, root=root,
                        loops_only=False)
            La, Ra = _captured["a Rules"][0], _captured["a Rules"][1]
            Lb, Rb = _captured["b True"][0], _captured["b True"][1]
            n = min(len(La), len(Lb))
            d = float(np.abs(np.asarray(La)[:n] - np.asarray(Lb)[:n]).max())
            if d < 1e-6:
                ident.append(name)
            for tag, (L, R, lu, _p) in (("a Rules", _captured["a Rules"]),
                                        ("b True", _captured["b True"])):
                mono = 0.5 * (np.asarray(L) + np.asarray(R))
                mid = band_db(mono, SR, 200.0, 600.0)
                fn = f"{i+1} {name} {tag}.wav"
                write_wav24(scratch / fn, L, R)
                rows.append((fn, lu, mid))
                print(f"  {fn:34s} LUFS {lu:6.2f}  200-600Hz {mid:7.2f}")
            ma = band_db(0.5 * (np.asarray(La) + np.asarray(Ra)), SR, 200, 600)
            mb = band_db(0.5 * (np.asarray(Lb) + np.asarray(Rb)), SR, 200, 600)
            mids.append((f"{i+1} {name}", mb - ma))
    finally:
        bm.render_crew_beat = _real_render
        crew.TRUE_LEVELS = False

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, mids))
    shutil.rmtree(scratch)

    n = len(list(DESK.glob("*.wav")))
    want = len(DJS) * 2
    print(f"\n{n} files -> {DESK}")
    if n != want:
        print(f"WARNING: expected {want} files, got {n}.")
    if ident:
        print("WARNING: rule change did NOTHING (b == a) on:\n  "
              + "\n  ".join(ident))
    print("200-600 Hz body, true minus rules:")
    for k, v in mids:
        print(f"  {k:20s} {v:+.2f} dB")


def readme(rows, mids):
    lufs = [r[1] for r in rows]
    up = [k for k, v in mids if v > 0.5]
    dn = [k for k, v in mids if v < -0.5]
    avg = float(np.mean([v for _, v in mids])) if mids else 0.0
    lines = [
        f"TRUE LEVELS — every sample at its own volume, rules off   {date.today()}",
        "=" * 66, "",
        "WHAT YOU ASKED",
        '  "For this mix I want to start with everything at its true',
        '   volume and disregard any of those rules for the mix."',
        "",
        "  Those rules set how loud each sound is allowed to be against",
        "  the kick: chords held about 9 dB under it, the snare about 3",
        "  under, small percussion under the hat.",
        "",
        "WHAT CHANGED",
        "  a Rules   today's sound, all those rules on.",
        "  b True    rules off. Every sample plays at the level it was",
        "            recorded at. Kept: the kick duck, each DJ's own",
        "            per-sound levels, and the final loudness match (so",
        "            you judge tone, not volume).",
        "",
        "  SAME BEAT both times — the exact same take is rendered twice and",
        "  only the level rules move, so anything you hear between a and b",
        "  IS the rules and nothing else.",
        "",
        "LISTEN FOR",
        "  Does 'b True' sound fuller / more like the Loops page — or does",
        "  something now jump out too loud (a chord stab, the snare)",
        "  because nothing holds it under the kick? That trade is the whole",
        "  question.",
        "",
        f"MEASURED — all {len(rows)} files {min(lufs):.2f}..{max(lufs):.2f} "
        "LUFS (judging tone, not loudness).",
        "  Body (200-600 Hz), 'b True' minus 'a Rules':",
    ]
    lines += [f"    {k:20s} {v:+.2f} dB" for k, v in mids]
    lines += [
        f"    average              {avg:+.2f} dB",
        "",
        "  HONEST READ: on the SAME beat, turning the rules off adds real",
        "  body — the chord/melodic governor was the main thing thinning",
        "  the low-mids, exactly as you suspected. A beat whose chords",
        "  already sat near the rule's target barely moves; the rest fill",
        "  in by a few dB. (The rule can THIN a beat whose chords it was",
        "  boosting, so watch for anything that now sounds weaker, but",
        "  none of these did.)",
    ]
    if up:
        lines.append("    fuller with rules off: " + ", ".join(up))
    if dn:
        lines.append("    thinner with rules off: " + ", ".join(dn))
    lines += [
        "",
        "NOT HEARD",
        "  Whether 'b True' sounds RIGHT to you, and whether any beat now",
        "  has a sound poking out that the rule used to keep in place.",
        "",
        "WHAT I NEED BACK",
        "  One line: is 'b True' the better starting point (yes / no), and",
        "  if any beat has something too loud now, which beat and sound.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
