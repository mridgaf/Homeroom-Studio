"""Render every instrument voice to a folder of listenable WAVs, so the
owner can HEAR a sound before agreeing to wire it into a legend (owner
ruling 2026-07-23: "I would want to hear what those other sounds actually
sound like before agreeing to wire them in" — the same audition-before-
live discipline the beats already follow, applied to instruments).

Every voice here is now SAMPLED from his own banks (owner directive
2026-07-23). The synthesized lead/horn demos this file used to render are
gone along with the engine behind them; the old WAVs were moved, not
deleted, into "Sound Demos/Retired ...".

Nothing here touches legends_config.json or renders a beat. It only
writes demo files.

    ./.venv/bin/python tools/demo_sounds.py
    -> "Sound Demos/" in the project folder, one WAV per voice.

Each instrument gets the SAME chord in three registers — low, middle and
high — because the one thing worth hearing is whether the multi-sample
zoning holds up at the EDGES of the range, not just the comfortable
middle. Each scratch demo uses a real vocal one-shot from his library (a
synth tone would not represent what a scratch sounds like on his stuff).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import numpy as np                                              # noqa: E402

import chord_synth                                              # noqa: E402
import instrument_sampler                                       # noqa: E402
from make_drum_loops import SR, write_wav24                      # noqa: E402
from scratch import PATTERNS, scratch                            # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "Sound Demos"

# same chord shape in three registers, so a thin group's edges show up
REGISTERS = [("low", [43, 47, 50]),
             ("mid", [55, 58, 62]),
             ("high", [67, 70, 74])]


def _stereo(mono, pad=0.3):
    """Mono -> a slightly padded stereo pair so a demo doesn't start
    hard against the file's first sample."""
    lead = np.zeros(int(pad * SR))
    x = np.concatenate([lead, mono, lead])
    return x, x


def _vocal_source():
    """A real vocal/one-shot from the owner's library for the scratch
    demos, or a synth fallback (clearly named) if the drive is
    unplugged — never fail silently into a tone he'd mistake for his
    own sample."""
    try:
        from make_drum_beats import build_shots, pick
        shots = build_shots()
        for kind in ("fx", "perc", "snare"):
            name, x = pick(shots, kind, ["vocal", "vox", "shout", "yeah"],
                           max_secs=1.2, seed=7)
            if not name.startswith("(none"):
                mono = x.mean(axis=1) if x.ndim == 2 else x
                return name, mono
    except Exception as exc:                       # drive gone, bad scan
        print("  (library unavailable: %s)" % type(exc).__name__)
    t = np.arange(int(0.5 * SR)) / SR
    tone = np.sin(2 * np.pi * 300 * t) * np.exp(-t * 3)
    return "SYNTH FALLBACK (sample drive not readable)", tone


def main():
    OUT.mkdir(exist_ok=True)
    written = []

    print("Instruments, all SAMPLED from your own banks:")
    idx = instrument_sampler.scan(status=lambda m: print("   " + m))
    if not idx:
        print("   (no instrument samples found - is the sample drive in?)")
    else:
        print("   %d source samples indexed\n" % len(idx))
        # Demo by the WORD a signature can ask for, through the same
        # VOICES mapping a real beat uses — not by raw group. A thin group
        # hands off to its backup mid-chord in an actual render, so
        # demoing the raw group would have him judging a sound the machine
        # never actually makes.
        for word in sorted(instrument_sampler.VOICES):
            groups = instrument_sampler.VOICES[word]
            got = instrument_sampler.pool(idx, groups)
            if not got:
                continue
            print("   %s  (draws from %s, %d samples)"
                  % (word, "/".join(groups), len(got)))
            for label, notes in REGISTERS:
                audio = instrument_sampler.play_chord(idx, notes, dur=2.2,
                                                      groups=groups)
                if audio is None:
                    continue
                src = instrument_sampler.nearest(idx, notes[0], groups)
                path = OUT / ("%s - %s.wav" % (word, label))
                write_wav24(path, *_stereo(audio))
                written.append(path.name)
                print("      %-20s from %-30s %+d semitones (%s)"
                      % (path.name, src["name"][:30],
                         notes[0] - src["note"], src["group"]))
            # the stab/arp rhythm, the other half of how a voice gets used
            cache = {}
            audio = chord_synth.arp_riff(
                REGISTERS[1][1], 2.4, 88,
                lambda nt, sd: instrument_sampler.note_slice(
                    idx, nt, sd, cache=cache, groups=groups))
            if np.max(np.abs(audio)) > 0:
                path = OUT / ("%s - stabs.wav" % word)
                write_wav24(path, *_stereo(audio))
                written.append(path.name)
                print("      %s" % path.name)

    print("\nScratches (on a real sample from your library):")
    src_name, src = _vocal_source()
    print("   source: %s" % src_name)
    for pattern in PATTERNS:
        audio = scratch(src, dur=1.4, pattern=pattern, hit_dur=0.22)
        path = OUT / ("Scratch - %s.wav" % pattern)
        write_wav24(path, *_stereo(audio))
        written.append(path.name)
        print("   %s" % path.name)

    print("\n%d files -> %s" % (len(written), OUT))


if __name__ == "__main__":
    main()
