"""Audition the 70/30 freedom pass: real beats from the real generate().

Owner 2026-09-14: every DJ has every instrument, drum sound, drum pattern,
backbeat, chord and key; 70% of beats stay in character and 30% are a
free-for-all, drum parts borrowed each from a different DJ; one low sound
per beat; arps half as often. There is no "before" to A/B here — variety is
heard across beats, not in a pair — so this renders six FREE beats and six
IN-CHARACTER beats, and the READ ME says beat by beat what each one did.

Renders to a scratch library (its own numbering, its own sample and pattern
history, a copy of the stamp lock), then copies to the Desktop. His library
and his histories are never touched. Fails loud and writes nothing unless:
the seed lands the free/in-character split asked for, no beat has two low
sounds, no beat plays the strings' basses over another low sound, and the
file count is right.

    ./.venv/bin/python tools/make_freedom_batch.py
"""
from __future__ import annotations

import os
import random
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import beat_machine as bm                                           # noqa
import beat_recipes                                                 # noqa
import crew                                                         # noqa
import pattern_gen                                                  # noqa
from make_drum_beats import build_shots                             # noqa

FREE = ("Otto Grit", "Night Metro", "Doc Day", "Mustang", "J Dillo",
        "Fast Water")
KEPT = ("Cutz", "Sunday Chop", "Kane East", "DJ Premium", "Timberline",
        "Razor")
OUT = Path(os.path.expanduser(
    "~/Desktop/Homeroom Auditions/Homeroom Strings + Freedom 2026-09-14/2 Free-for-all beats"))

READ_ME = """FREE-FOR-ALL BEATS

12 beats: 6 FREE (the 30%) and 6 IN CHARACTER (the 70%). Numbers match
the file names. Free beats are listed first.

WHAT CHANGED - your words, 2026-09-14

"all djs have all instruments, chords and keys available to them. keep
djs 70% true to character... the rest is free for all"

- On a free beat EVERYTHING is open at once: the lead instrument, every
  drum sound (your whole library, not the DJ's taste), all 12 keys, all
  47 progressions, and the drum patterns - each part (kick, backbeat,
  hats, percussion) borrowed from a different DJ.
- In character: the DJ as before - except drum sounds now follow his own
  taste. 14 DJs had been picking every drum sound at random, which is how
  sidesticks ended up where snares belong.
- "don't pile lows on lows": the kick plus ONE low sound - sub, 808,
  your synth bass samples, or the strings' basses. A long 808 kick counts
  as the low sound by itself. (Your beat 1191 had an 808 kick AND an 808
  bass on the same hits - that can't happen any more.)
- The old arpeggio (one fixed run up the notes, forever) is gone for
  every DJ. They all use the chord rhythms you approved on Swish Beatz -
  stabs, comping, held chords, arps that change direction and rest - with
  arps half as often as before.

ANYTHING DELIBERATELY ODD

- A free beat can sound nothing like its DJ. That is the 30%.
- Low brass never shows up: your lowest brass sample is F3. Put tuba or
  trombone one-shots in BOTC Sorted Instruments/Brass and it will.
- The sub never plays on a beat with chords - your call from 09-01 stands.

THE BEATS

{rows}

MEASURED (not heard)

{measured}

WHAT I COULD NOT CHECK

Whether 30% free is too much or too little. Whether the borrowed drum
parts clash. Whether the in-character beats still sound like each DJ.
That is your ear.

WHAT I NEED BACK

For each folder: keep it, or what to change.
"""


def _seed_for(want_free, start):
    s = start
    while True:
        random.seed(s)
        v = random.randrange(2, 10000)
        if pattern_gen.free_beat(v) == want_free:
            return s, v
        s += 1


def main():
    if OUT.exists():
        raise SystemExit("%s already exists. Move it aside first." % OUT)
    scratch = Path(tempfile.mkdtemp(prefix="freedom-"))
    root = scratch / "beats"
    root.mkdir()
    beat_recipes.HIST = scratch / "sample_history.json"
    pattern_gen.PAT_HIST = scratch / "pattern_history.json"
    if crew.LOCK.exists():
        shutil.copy2(crew.LOCK, scratch / "crew_kits.json")
    crew.LOCK = scratch / "crew_kits.json"
    print("Scanning library for one-shots…")
    shots = build_shots()

    rows, warnings, free_n, low_n = [], [], 0, 0
    plan = [(n, True) for n in FREE] + [(n, False) for n in KEPT]
    for i, (name, want_free) in enumerate(plan):
        seed, v = _seed_for(want_free, 1000 * (i + 1))
        random.seed(seed)
        path, report = bm.generate([name], root=root, shots=shots)
        print(report)
        rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
        if rec["variant"] != v:
            warnings.append("%s: seed gave variant %s, expected %s"
                            % (name, rec["variant"], v))
        free = pattern_gen.free_beat(rec["variant"])
        free_n += free
        lanes = rec["preset"]["lanes"]
        lows = [ln for ln in lanes if ln in crew._LOW_END]
        h = rec.get("harmony") or {}
        files = [f for fs in (h.get("voice_files") or {}).values() for f in fs]
        basses = any("LSS Basses" in f for f in files)
        if len(lows) > 1:
            warnings.append("%s: two low sounds %s" % (name, lows))
        if lows and basses:
            warnings.append("%s: strings basses over a low lane" % name)
        sheet = path.with_suffix(".txt").read_text()
        borrowed = next((ln.strip()[len("free beat, drums: "):]
                         for ln in sheet.splitlines()
                         if ln.strip().startswith("free beat, drums:")), "")
        bass_ln = next((ln.strip() for ln in sheet.splitlines()
                        if ln.strip().startswith(("bass ", "root:"))), "")
        if lows or basses:
            low_n += 1
        low = (bass_ln or ("strings basses" if basses else "")
               or ("long 808 kick" if bm._holds_low_end(rec["preset"])
                   else "none"))
        chords = h.get("chords") or []
        lead, figures = set(), set()
        for c in chords:
            voice = c.get("voice") or ""
            if voice.startswith("sample:"):      # a loop, chopped to a figure
                lead.add("loop (%s)" % voice[7:].rsplit(" (", 1)[0].strip())
                figures.add(voice.rsplit("(", 1)[-1].rstrip(")")
                            .replace("chopped ", ""))
            elif voice:
                lead.add(voice.split(" ", 1)[0])
                figures.add(voice.split(" ", 1)[-1])
        lead, figures = sorted(lead), sorted(figures)
        rows.append("  %s  %s  %s\n"
                    "      key %s, %s | lead %s | chord rhythm %s\n"
                    "      low sound: %s%s" % (
                        path.stem.split(" Drums")[0],
                        "FREE" if free else "in character",
                        "" if not borrowed else "- drums: " + borrowed,
                        h.get("key", "no chords"), h.get("progression", "-"),
                        ", ".join(lead) or "-", ", ".join(figures) or "-",
                        low, ""))

    if free_n != len(FREE):
        warnings.append("%d free beats, wanted %d" % (free_n, len(FREE)))
    wavs = sorted(root.rglob("* Drums *bpm.wav"))
    if len(wavs) != len(plan):
        warnings.append("%d beats rendered, wanted %d" % (len(wavs), len(plan)))
    if warnings:
        print("\nWARNING - not handing this over:\n  " + "\n  ".join(warnings))
        raise SystemExit(1)

    OUT.mkdir(parents=True)
    for wav in wavs:
        base = wav.name.split(" Drums ")[0]
        for f in wav.parent.iterdir():
            if f.name.startswith(base):
                dst = OUT / f.name
                (shutil.copytree if f.is_dir() else shutil.copy2)(f, dst)
    measured = ("  %d of 12 beats have a low sound; 0 have two (checked on "
                "every recipe).\n  %d of 12 are free beats." % (low_n, free_n))
    (OUT / "READ ME.txt").write_text(
        READ_ME.format(rows="\n".join(rows), measured=measured))
    print("\n%s\n%d items." % (OUT, len(list(OUT.iterdir()))))


if __name__ == "__main__":
    main()
