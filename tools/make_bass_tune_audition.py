"""Audition: the bass line in tune (2026-09-23).

Owner, on folder 2 of "Homeroom 808 On The Kick": "the bass lines are out
of tune." Measured: Otto Grit's line played -36, -39 and +23 cents off its
chord roots. Two faults in how his bass one-shots were read:
  * the pitch reader stopped at 55 Hz and misread 67 of 87 bass files as a
    1225 Hz "D#6", and rounded every other read to a whole note
  * it read only the first half second, so a note that sags as it rings
    (Otto Grit's sub drops 77 cents) looked in tune
Now: a bass reader down to 25 Hz, exact to the cent, over the whole note;
any file whose pitch moves more than 30 cents is kept out of the line.

Re-renders the SAME six beats as tools/make_low_end_audition.py, in the
same order and seeds (sample and pattern history carry across beats, so
order matters), and ships the two bass-line beats next to their old
versions, plus two more bass-line DJs. Scratch only; library untouched.

Fails loud: a re-made beat must match its old drums and length; every
bass-line stem must MEASURE within 15 cents of its chord's root in the
finished stem; one bass file per beat.

Run:  ./.venv/bin/python tools/make_bass_tune_audition.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom Bass In Tune <today>/
"""
import json
import random
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR
from make_drum_beats import build_shots
import beat_machine as bm
import beat_recipes
import crew
import pattern_gen
import make_low_end_audition as le

OUT = Path.home() / "Desktop" / "Homeroom Auditions" / "Homeroom Auditions" / f"Homeroom Bass In Tune {date.today()}"
OLD = Path.home() / "Desktop" / "Homeroom Auditions" / "Homeroom 808 On The Kick 2026-09-23" \
    / "2 Bass-line DJs"
# the old bench's scratch recipes, to prove a re-made beat is the same beat
OLD_RECIPES = {"Otto Grit": 812, "DJ Premium": 813}
OLD_SCRATCH = Path("/var/folders/b9/c2h90xwj60gbp06lw3wq811w0000gn/T/"
                   "low-end-tk4i9s93/beats/.recipes")
ORDER = ["Night Metro", "Mustang", "Hitt Kid", "Memphis",   # replayed, not shipped
         "Otto Grit", "DJ Premium", "Just Flame", "Sunday Chop"]
SHIP = ORDER[4:]
TOL_C = 15
SLIDE_C = 30        # how far one note may move while it sounds


def _f0(stem):
    """The finished stem's fundamental (MIDI, fractional): harmonic sum,
    25-400 Hz, per 0.2 s window, median. Deliberately NOT the reader that
    tuned it. Per window, not whole-stem: a short hit repeated to fill a
    bar (Otto Grit's 0.6 s "BASS Flam") splits a whole-stem spectrum into
    sidebands +21/-28 cents either side of the note, and the biggest one
    is not the note."""
    x = np.asarray(stem, dtype=np.float64)
    x = x.mean(axis=0) if x.ndim == 2 else x
    win, n = int(0.2 * SR), 1 << 18
    f = np.fft.rfftfreq(n, 1 / SR)
    c = np.arange(25, 400, 0.05)
    pk, reads = np.abs(x).max(), []
    for s in range(0, len(x) - win + 1, win):
        w = x[s:s + win]
        if np.abs(w).max() < 0.3 * pk:
            continue
        sp = np.abs(np.fft.rfft(w * np.hanning(win), n))
        score = sum(np.interp(c * k, f, sp) / k ** 0.5 for k in range(1, 6))
        reads.append(69 + 12 * np.log2(c[score.argmax()] / 440))
    r = np.array(reads)
    r = r - 12 * np.round((r - np.median(r)) / 12)     # octave slips
    # middle half only: a sample looping back (Sunday Chop, once a second)
    # or a flam's second hit re-attacks, and that one slice reads 30-45
    # cents off. That is a restart, not the pitch moving; a sag is.
    lo, hi = np.percentile(r, [25, 75])
    return float(np.median(r)), float(100 * (hi - lo))


def main():
    old = {nm: OLD / f"{i} {nm} {bpm}bpm.wav" for i, nm, bpm in
           ((5, "Otto Grit", 88), (6, "DJ Premium", 96))}
    missing = [str(p) for p in old.values() if not p.exists()]
    if missing:
        sys.exit("old beats missing: " + ", ".join(missing))
    scratch = Path(tempfile.mkdtemp(prefix="bass-tune-"))
    root = scratch / "beats"
    root.mkdir()
    beat_recipes.HIST = scratch / "sample_history.json"
    pattern_gen.PAT_HIST = scratch / "pattern_history.json"
    if crew.LOCK.exists():
        shutil.copy2(crew.LOCK, scratch / "crew_kits.json")
    crew.LOCK = scratch / "crew_kits.json"
    bm.render_crew_beat = le._keep_parts
    print("Scanning library for one-shots…")
    shots = build_shots()

    rows, warnings = [], []
    (scratch / "ship").mkdir()
    try:
        for n, name in enumerate(ORDER, 1):
            random.seed(le._seed_in_character(7000 + 100 * n))
            path, _ = bm.generate([name], root=root, shots=shots)
            num = int(path.name.split()[0])
            rec = beat_recipes.load_recipe(root, num)
            print(f"  {n} {name}")
            if name not in SHIP:
                continue
            stems = le._parts["last"]["stems"]
            chords = (rec.get("harmony") or {}).get("chords", [])
            files = {Path(f).name for ln, fs in ((rec.get("harmony") or {})
                     .get("voice_files") or {}).items()
                     if ln.startswith("bass") for f in fs}
            offs = []
            for i, ch in enumerate(chords):
                st = stems.get(f"bass{i}")
                if st is None:
                    warnings.append(f"{name}: no bass line for {ch['chord']}")
                    continue
                m, slide = _f0(st)
                off = 100 * (((m - (ch["notes"][0] - 12)) + 6) % 12 - 6)
                offs.append((ch["chord"], off, slide))
                if abs(off) > TOL_C or slide > SLIDE_C:
                    warnings.append(f"{name}: bass under {ch['chord']} "
                                    f"measures {off:+.0f} cents, slides "
                                    f"{slide:.0f}")
            if len(files) > 1:
                warnings.append(f"{name}: {len(files)} bass files {files}")
            if name in OLD_RECIPES:
                was = json.loads((OLD_SCRATCH / f"{OLD_RECIPES[name]}.json")
                                 .read_text())
                same = lambda r: (r.get("kit_paths"), [
                    (c["chord"], c["notes"], c.get("voice"))
                    for c in (r.get("harmony") or {}).get("chords", [])])
                if same(was) != same(rec):
                    warnings.append(f"{name}: not the same beat as before "
                                    "(drums or chords differ)")
                a, b = sf.info(str(old[name])).frames, sf.info(str(path)).frames
                if a != b:
                    warnings.append(f"{name}: length {b} vs old {a}")
            tag = f"{SHIP.index(name) + 1}{'b' if name in old else ''}"
            fn = f"{tag} {name} {'NOW ' if name in old else ''}" \
                 f"{rec['preset']['bpm']}bpm.wav"
            shutil.copy2(path, scratch / "ship" / fn)
            if name in old:
                shutil.copy2(old[name], scratch / "ship" /
                             f"{SHIP.index(name) + 1}a {name} BEFORE "
                             f"{rec['preset']['bpm']}bpm.wav")
            rows.append((name, sorted(files), offs))
    finally:
        bm.render_crew_beat = le._real_render

    got = len(list((scratch / "ship").glob("*.wav")))
    if got != len(SHIP) + len(old):
        warnings.append(f"expected {len(SHIP) + len(old)} files, got {got}")
    if warnings:
        print("\nWARNING — do not hand this batch over:")
        for w in warnings:
            print("  " + w)
        print(f"(scratch kept at {scratch})")
        sys.exit(1)
    if OUT.exists():
        shutil.rmtree(OUT)              # only ever this script's own folder
    shutil.copytree(scratch / "ship", OUT)
    (OUT / "READ ME.txt").write_text(readme(rows))
    shutil.rmtree(scratch)
    for name, files, offs in rows:
        print(f"  {name:12s} {', '.join(files)}  "
              + "  ".join(f"{c} {o:+.0f}c/slide {sl:.0f}" for c, o, sl in offs))
    print(f"\n{len(list(OUT.glob('*.wav')))} files -> {OUT}")


def readme(rows):
    lines = [
        f"THE BASS LINE IN TUNE   {date.today()}",
        "=" * 60, "",
        "WHAT YOU SAID",
        '  "Folder 2, the bass lines are out of tune."',
        "",
        "WHAT WAS WRONG",
        "  The app misread the note of most of your bass samples.",
        "  - 67 of your 87 bass files were read as a high squeak, not",
        "    a bass note (the reader couldn't hear below 55 Hz).",
        "  - The rest were rounded to the nearest note, losing up to",
        "    half a semitone.",
        "  - Some bass samples slide or sag as they ring. Otto Grit's",
        "    sub drops 77 cents, so no single tuning could fit it.",
        "  Old Otto Grit: -36, -39, +23 cents off the chords.",
        "",
        "WHAT CHANGED",
        "  - Bass notes are read down to the lowest sub, to the cent.",
        "  - Bass samples that slide or sag more than 30 cents are left",
        "    out of the bass line. 38 of your non-808 bass files are",
        "    steady enough and stay in.",
        "  - Chords, drums and 808s: untouched.",
        "",
        "LISTEN FOR",
        "  1a vs 1b and 2a vs 2b: same beat, old bass vs new bass.",
        "  Does the bass now sit in tune with the chords?",
        "",
        "THE BEATS (measured in the finished file: cents off each root)",
    ]
    for name, files, offs in rows:
        lines.append(f"  {name}: {', '.join(Path(f).stem for f in files)}")
        lines.append("      " + ", ".join(f"{c} {o:+.0f} (slides {sl:.0f})"
                                          for c, o, sl in offs))
    lines += [
        "",
        "MEASURED (not heard)",
        f"  Every bass note above is within {TOL_C} cents of its chord's",
        f"  root and moves less than {SLIDE_C} cents while it sounds. The",
        "  script refuses to write this folder otherwise. Old Otto Grit",
        "  on the same check: its bass slid 44-57 cents on every note.",
        "  Old DJ Premium only slid 18-26, so the numbers don't show",
        "  its problem as clearly -- your ear decides that one.",
        "",
        "NOT CHECKED -- your ear",
        "  Whether in-tune is enough, or whether a sample's tone still",
        "  clashes. The 1b/2b beats had to pick a different bass file,",
        "  because the old ones were the wobbly ones.",
        "  3 of the 4 beats landed on the same bass sample (UNISON_BASS",
        "  Commas). Most of your steady bass samples sit an octave lower",
        "  than where the bass line plays, so only 2 were close enough.",
        "",
        "WHAT I NEED BACK",
        "  Keep the new bass, or what still sounds off.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
