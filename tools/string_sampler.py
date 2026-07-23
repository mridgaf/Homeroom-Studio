"""London Symphonic Strings as a playable instrument (harmonizer step 2,
2026-07-22).

The other harmony sources read a KEY off a filename and fit a whole
clip (melodic_loops.py) or a whole phrase (midi_packs.py). This one is
different: the Strings library is 24.5k real pitched note one-shots, so
it's a SAMPLER — you don't fit a loop, you PLAY the exact MIDI notes
harmony.compose() already hands you, one sample per note, summed into a
chord. No pitch-detection risk at all: the note number is right in the
file name.

Filename shape (consistent across the 5 instrument families):
    {articulation}_{note}_{dyn}_{RR}_{mic}.wav
e.g. Violin I "pizz_55_ff_RR1_c.wav" = pizzicato, MIDI 55, forte,
round-robin 1, close mic. Basses nest deeper ("pizz/p/close/
pizz_28_p_RR1_c.wav") but the FILE tokens are the same.

The note is the one plausible-MIDI integer token in the name. That
single rule is also the filter: legato-TRANSITION samples carry two
note numbers ("susbowleg_55_56_17_17.wav" = the bow moving 55->56), so
they have two plausible-note tokens and are dropped — exactly the
"unparseable -> left out" filter melodic_loops uses, no exclude list.

Close mic ("_c") only: driest, sits in a beat without washing it out.

    ./.venv/bin/python tools/string_sampler.py        # library report
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import numpy as np                                          # noqa: E402

from make_drum_loops import SR                              # noqa: E402
from make_hiphop_tracks import load_audio, norm_rms         # noqa: E402
from sample_library import AUDIO_EXTS                        # noqa: E402

ROOT = "/Volumes/TBOTC 3/Sample Packs/London Symphonic Strings Volume I"
CACHE = Path(os.path.expanduser("~/.reason_voice/string_sampler_index.json"))

# folder name -> instrument family. First match wins.
FAMILIES = [("basses", "LSS BASSES"), ("cello", "LSS CELLO"),
            ("viola", "LSS VIOLA"), ("violin", "LSS VIOLIN")]

MIC = "c"                              # close mic only
NOTE_LO, NOTE_HI = 21, 108             # piano range; 17-token "RR" numbers fall out
_SPLIT = re.compile(r"[\s_\-]+")


def _family(path, rootp):
    up = str(path.relative_to(rootp)).upper()
    for name, marker in FAMILIES:
        if marker in up:
            return name
    return "strings"


def note_from_tokens(tokens):
    """The MIDI note a sample plays, or None. It's the single token that
    reads as a plausible MIDI note; two or more distinct such tokens
    means a legato transition (two pitches) -> not a playable single
    note, so drop it."""
    notes = {int(t) for t in tokens
             if t.isdigit() and NOTE_LO <= int(t) <= NOTE_HI}
    return notes.pop() if len(notes) == 1 else None


def _tokens(stem):
    return [t for t in _SPLIT.split(stem) if t]


def scan(root=None):
    """Walk the Strings library -> one entry per playable close-mic note
    sample. Falls back to the last good scan when the drive's unplugged,
    same contract as melodic_loops.scan."""
    rootp = Path(os.path.expanduser(root or ROOT))
    if not rootp.exists():
        try:
            return json.loads(CACHE.read_text())
        except (OSError, ValueError):
            return []
    found = []
    for path in sorted(rootp.rglob("*")):
        if path.suffix.lower() not in AUDIO_EXTS or not path.is_file():
            continue
        tokens = _tokens(path.stem)
        if tokens[-1].lower() != MIC:          # keep close mic only
            continue
        note = note_from_tokens(tokens)
        if note is None:
            continue
        found.append({"path": str(path), "note": note,
                      "instrument": _family(path, rootp),
                      "artic": tokens[0].lower()})
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(found))
    except OSError:
        pass
    return found


def nearest(index, midi_note, instrument=None, artic=None):
    """The sample closest in pitch to `midi_note` (optionally within one
    instrument/articulation), or None if the pool's empty. Closest-note
    rather than exact so a chord tone outside one instrument's range
    still gets voiced by its nearest playable note."""
    pool = [e for e in index
            if (instrument is None or e["instrument"] == instrument)
            and (artic is None or e["artic"] == artic)]
    if not pool:
        return None
    return min(pool, key=lambda e: abs(e["note"] - midi_note))


# an identity's abstract articulation word -> the vendor's own tokens that
# realize it. The London library names sustained samples half a dozen ways
# (sus, sustain, sustainff/mf/mp, susrel); those run 7-9s, so a long held
# chord tiles at most once. Legato ("leg") is deliberately NOT here: those
# run ~2s and would tile 4-5x across a slow chord, one audible seam per
# repeat — it's a transition articulation, not a bed. pizz is the plucked
# stab. Keeps that library-specific spelling here, out of the render.
ARTIC_FAMILY = {
    "sustain": ("sus", "sustain", "sustainff", "sustainmf", "sustainmp",
                "susrel"),
    "pizz": ("pizz",),
}


def by_articulation(index, kind):
    """Sub-index of `index` for an abstract articulation ('sustain' bed /
    'pizz' stab). Unknown or missing `kind` -> the whole index unfiltered,
    so this never empties a pool the caller expected to have."""
    fam = ARTIC_FAMILY.get(kind)
    return [e for e in index if e["artic"] in fam] if fam else index


def note_slice(index, note, dur, sr=SR, cache=None):
    """One arp step's worth of the nearest string sample to `note`: its
    first `dur` seconds with a short attack + release so it reads as a
    rhythmic note, not a swell. `cache` (a dict) holds each note's loaded
    audio so an arp doesn't reload it per step. None if nothing's
    voiceable, so chord_synth.arp_riff can pluck that step instead."""
    if cache is not None and note in cache:
        mono = cache[note]
    else:
        pk = nearest(index, note)
        x = load_audio(pk["path"]) if pk else None
        mono = None if x is None else (x.mean(axis=1) if x.ndim == 2 else x)
        if cache is not None:
            cache[note] = mono
    if mono is None:
        return None
    m = max(int(dur * sr), 1)
    seg = (mono[:m] if len(mono) >= m
           else np.pad(mono, (0, m - len(mono)))).astype(float).copy()
    a = min(int(0.008 * sr), m)               # 8ms attack
    d = min(int(0.06 * sr), m)                # 60ms release so steps don't click
    if a:
        seg[:a] *= np.linspace(0, 1, a)
    if d:
        seg[-d:] *= np.linspace(1, 0, d)
    return seg


def play_chord(index, notes, dur, instrument=None, artic=None, sr=SR):
    """Sum one sample per MIDI note in `notes` into a `dur`-second chord
    bed. Each note is cropped/looped to length the same loop-safe way
    every lane fits a bar (no edge fades), then the stack is RMS-
    normalized so a 4-note chord doesn't clip. Returns None if not one
    note could be voiced (empty index / drive gone), so the caller can
    fall back to the synth pad."""
    n = max(int(dur * sr), 1)
    out = np.zeros(n)
    voiced = 0
    for note in notes:
        pick = nearest(index, note, instrument, artic)
        if pick is None:
            continue
        x = load_audio(pick["path"])
        if x is None:
            continue
        mono = x.mean(axis=1) if x.ndim == 2 else x
        if len(mono) >= n:
            seg = mono[:n]
        else:
            seg = np.tile(mono, n // len(mono) + 1)[:n]
        out = out + seg
        voiced += 1
    if not voiced:
        return None
    out = norm_rms(out, -18.0)
    peak = np.max(np.abs(out))               # a pizz transient's crest can
    if peak > 0.99:                          # top 1.0 even at -18 dBFS RMS;
        out = out * (0.99 / peak)            # never hand back a clipping chord
    return out


def _report():
    index = scan()
    if not index:
        print("No Strings samples found. Is the sample drive plugged in?")
        return
    print("%d playable close-mic note samples\n" % len(index))
    fam = {}
    art = {}
    for e in index:
        fam[e["instrument"]] = fam.get(e["instrument"], 0) + 1
        art[e["artic"]] = art.get(e["artic"], 0) + 1
    for f in sorted(fam, key=lambda k: -fam[k]):
        print("  %-8s %5d" % (f, fam[f]))
    print("\narticulations:", ", ".join(
        "%s(%d)" % (a, art[a]) for a in sorted(art, key=lambda k: -art[k])))


if __name__ == "__main__":
    _report()
