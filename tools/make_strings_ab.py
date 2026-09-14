"""Audition the London strings fix: same beat, the old strings player vs the new.

One variable only. Both versions share the DJ, the composed drums, the kit,
the key, the progression and the chord rhythm. "a Now" plays the strings
through string_sampler.py exactly as it was committed (loaded from git
HEAD); "b Fixed" plays them through today's. Everything else in the engine
is today's code on both sides, so anything you hear is the strings player.

The bug (found 2026-09-14): since 2026-07-29 every note of a strings chord
reused ONE recording with no pitch shift, so C-E-G came out C-C-C. The fix
gives each note its own recording from the same section, style and mic,
shifted onto its exact pitch (the library is recorded every other note).

Fails loud and writes nothing unless: every "a" reproduces the bug (it is
measurably missing chord notes, the premise), every "b" differs from its "a"
at the same length, and "b" measurably plays more of each chord's notes than
"a" (energy at each chord tone's own frequency in the strings buffer).

    ./.venv/bin/python tools/make_strings_ab.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

import beat_machine as bm                                           # noqa
import pattern_gen                                                  # noqa
import string_sampler as new_ss                                     # noqa
from crew import (CREW, build_kit, lock_stamps, normalize_preset,   # noqa
                  render_crew_beat)
from make_drum_beats import build_shots                             # noqa
from make_drum_loops import SR, write_wav24                         # noqa
from pattern_gen import compose                                     # noqa

DJS = ("Doc Day", "Razor", "Rage Engine")
CHORDS = {"chords": True, "chord_feel": None}
NSCAN = 60
OUT = Path(os.path.expanduser(
    "~/Desktop/Homeroom Strings + Freedom 2026-09-14/1 Strings before-after"))
REPO = Path(__file__).resolve().parent.parent

READ_ME = """LONDON STRINGS - BEFORE AND AFTER

{n} beats, each rendered twice:

    "a Now"    - the strings as they have played since July 29
    "b Fixed"  - the same beat with the strings fixed

Same drums, same samples, same key, same chords, same rhythm. Only the
strings player changed.

WHAT WAS WRONG

Every strings chord was ONE note. A C-E-G chord came out C-C-C, because
each note reused the first recording without changing its pitch. It hit
every DJ that uses the London strings: Doc Day, Just Flame, Razor, No
Alias, Mustang, Rage Engine, Fast Water.

WHAT CHANGED

- Each note of a chord now gets its own recording, from the same section
  (violins, violas, cellos or basses), so a chord is still one instrument.
- The library only recorded every other note, so each note is nudged at
  most one step onto the right pitch. Before, those notes were a half-step
  off - but you could not hear that, because the chord was one note anyway.
- Only the four playing styles you kept: held, plucked, short, tremolo.
  No more slides, sound effects or knocks slipping in.
- In character a DJ uses the close mic. On free beats it can be any of
  the four mics (you will hear those in folder 2, not here).

WHAT TO LISTEN FOR

    Do the strings in "b" sound like CHORDS now, not one note?
    Does "b" sound in tune?
    Is the section right for each DJ, or too high / too low?

MEASURED (not heard)

Chord notes with real energy at their own pitch, per chord, averaged
across the beat (more = more of the chord is actually sounding):

{rows}

WHAT I COULD NOT CHECK

Whether it sounds good. Whether the section each DJ lands on suits him.
Whether the one-step pitch nudge is audible on long held notes.
"""


def _old_string_sampler(scratch):
    """string_sampler.py as committed, loaded under its own name, with the
    two names today's beat_machine calls shimmed to exactly what the old
    call was: by_articulation(scan(), articulation)."""
    src = subprocess.check_output(
        ["git", "show", "HEAD:tools/string_sampler.py"], cwd=REPO)
    path = scratch / "string_sampler_head.py"
    path.write_bytes(src)
    spec = importlib.util.spec_from_file_location("string_sampler", path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    old.CACHE = scratch / "old_string_index.json"      # never his cache
    old.CLOSE = "c"
    old.beat_pool = (lambda idx, style=None, mic="c", basses=True:
                     old.by_articulation(idx, style))
    return old


def _present(x, notes):
    """How many of `notes` have energy at their own fundamental within
    24 dB of the buffer's strongest peak (60 Hz-2 kHz). Measured against the
    WHOLE buffer, not the loudest chord tone: a one-note chord has almost
    nothing at the other tones' frequencies, and a ruler relative to those
    tiny values would call noise a chord."""
    x = np.asarray(x, float)
    if x.ndim == 2:
        x = x.mean(axis=1)
    mag = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    freqs = np.fft.rfftfreq(len(x), 1.0 / SR)
    ref = mag[(freqs > 60) & (freqs < 2000)].max() or 1e-12
    got = []
    for m in sorted(set(notes)):
        f = 440.0 * 2 ** ((m - 69) / 12.0)
        band = (freqs > f * 2 ** (-0.4 / 12)) & (freqs < f * 2 ** (0.4 / 12))
        got.append(mag[band].max() if band.any() else 0.0)
    return sum(20 * np.log10(max(g, 1e-12) / ref) > -24 for g in got)


def main():
    if OUT.exists():
        raise SystemExit("%s already exists. Move it aside first." % OUT)
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="strings-ab-"))
    pattern_gen.PAT_HIST = scratch / "pattern_history.json"
    old_ss = _old_string_sampler(scratch)
    rows, warnings, made = [], [], 0

    for name in DJS:
        live = CREW[name]
        for v in range(2, NSCAN):
            if pattern_gen.free_beat(v):
                continue                  # in character only: see header
            seed_q = normalize_preset(json.loads(json.dumps(live)))
            compose(seed_q, name, v)
            bm.vary_preset(seed_q, v, live["num"], tempo_locked=True)
            got = {}
            for tag, mod in (("a Now", old_ss), ("b Fixed", new_ss)):
                sys.modules["string_sampler"] = mod
                q = normalize_preset(json.loads(json.dumps(seed_q)))
                kit, sources = build_kit(shots, name, stamps[name][1],
                                         variant=v, avoid=set(avoid),
                                         preset=q)
                _midi, harm = bm._build_chords(q, kit, sources, v,
                                               dict(CHORDS), [],
                                               voice="strings")
                sys.modules["string_sampler"] = new_ss
                if not harm or not all(
                        (c["voice"] or "").startswith("strings")
                        for c in harm["chords"]):
                    got = {}
                    break
                L, R, lufs = render_crew_beat(name, kit, preset=q)
                got[tag] = (q, kit, harm, L, R, lufs)
            if len(got) < 2:
                continue
            made += 1
            aq, akit, aharm, aL, aR, _ = got["a Now"]
            bq, bkit, bharm, bL, bR, _ = got["b Fixed"]
            if len(aL) != len(bL):
                warnings.append("%s: a and b differ in LENGTH" % name)
            elif np.array_equal(np.asarray(aL), np.asarray(bL)):
                warnings.append("%s: b is IDENTICAL to a" % name)
            slots = [c for c in range(len(aharm["chords"]))
                     if "chord%d" % c in akit and "chord%d" % c in bkit]
            pa = np.mean([_present(akit["chord%d" % c],
                                   aharm["chords"][c]["notes"]) for c in slots])
            pb = np.mean([_present(bkit["chord%d" % c],
                                   bharm["chords"][c]["notes"]) for c in slots])
            size = np.mean([len(set(aharm["chords"][c]["notes"]))
                            for c in slots])
            # the premise, on the AUDIO: "a" must be missing chord notes. A
            # file count was the first ruler and it was wrong — the old pin
            # re-picked any note more than an octave away, so "a" can use two
            # files and still play mostly one note.
            if not pa < size - 0.25:
                warnings.append("%s: 'a' did NOT reproduce the one-note bug "
                                "(%.1f of %.1f notes)" % (name, pa, size))
            if not pb > pa:
                warnings.append("%s: b does not play more of the chord (%.1f "
                                "vs %.1f)" % (name, pb, pa))
            for tag, (q, kit, harm, L, R, lufs) in got.items():
                fn = "%d %s %s %dbpm %s.wav" % (made, name, harm["key"],
                                                q["bpm"], tag)
                write_wav24(scratch / fn, L, R)
            files = [Path(f).stem for fs in bharm["voice_files"].values()
                     for f in fs][:3]
            rows.append("    %d %-12s %-10s a: %.1f of %.1f notes   b: %.1f of "
                        "%.1f   (b plays e.g. %s)" % (
                            made, name, bharm["key"], pa, size, pb, size,
                            ", ".join(files)))
            print(rows[-1])
            break

    if made != len(DJS):
        warnings.append("made %d of %d beats" % (made, len(DJS)))
    if warnings:
        print("\nWARNING - not handing this over:\n  " + "\n  ".join(warnings))
        raise SystemExit(1)
    OUT.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, OUT / f.name)
    (OUT / "READ ME.txt").write_text(
        READ_ME.format(n=made, rows="\n".join(rows)))
    print("\n%s\n%d files." % (OUT, len(list(OUT.glob("*")))))


if __name__ == "__main__":
    main()
