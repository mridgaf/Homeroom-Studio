"""London Symphonic Strings as a playable instrument (harmonizer step 2,
2026-07-22).

The other harmony sources read a KEY off a filename and fit a whole
clip (melodic_loops.py) or a whole phrase (midi_packs.py). This one is
different: the Strings library is real pitched note one-shots, so it's a
SAMPLER — you don't fit a loop, you PLAY the exact MIDI notes
harmony.compose() already hands you, one sample per note, summed into a
chord. The note number is right in the file name, so there is no pitch
detection at all.

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
Those slides are ~36,400 of the library's 52,667 files; using them is a
separate feature he parked (2026-09-14).

The library is recorded EVERY OTHER NOTE (sus_48, 49, 51, 53... on
disk), so a chord tone usually has no exact file. Every voiced note is
therefore shifted onto its exact pitch — at most a step here, which is
what keeps the tape-speed shift inaudible as a shift.

What gets indexed is his pick list in sample_packs.json (owner
2026-09-14): `strings_sections` and `strings_styles`. The playing STYLE
comes from the vendor's own folder under samples/ ("Pizzicato Samples",
"tremolo"), not the file name, because the file names lie: Violin I's
Glissando folder names its slides "sustain_*", and its SFX folder names
noises "100_c.wav", which parses as MIDI 100. All four mic positions are
indexed (`mic`: c close, m, r, a); the render uses the close mic in
character and one rolled mic on a free beat.

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
# the de-click/length-fit/shift helpers live next door because the SAME
# defects were found there first (owner 2026-07-23: a click at the end of
# every sustained chord). Shared rather than copied so a fix lands once.
from instrument_sampler import MAX_SHIFT, _declick, _fit_length, _shift  # noqa: E402
from sample_library import AUDIO_EXTS, PACKS_CONFIG          # noqa: E402

ROOT = "/Volumes/TBOTC 3/Sample Packs/London Symphonic Strings Volume I"
CACHE = Path(os.path.expanduser("~/.reason_voice/string_sampler_index.json"))

# folder name -> instrument family. First match wins.
FAMILIES = [("basses", "LSS BASSES"), ("cello", "LSS CELLO"),
            ("viola", "LSS VIOLA"), ("violin", "LSS VIOLIN")]

CLOSE = "c"                            # driest mic: sits in a beat unwashed
MICS = ("c", "m", "r", "a")
NOTE_LO, NOTE_HI = 21, 108             # piano range; 17-token "RR" numbers fall out
_SPLIT = re.compile(r"[\s_\-]+")

# The four playing styles he kept (2026-09-14), keyed by the vendor's own
# folder names under samples/ (lowercased). Everything else in the library
# (legato, harmonics, col legno, sul pont, sordino, glissando, SFX...) is
# left out on his call, not because it failed to parse.
STYLES = {
    "sustain": ("sus", "sustain samples", "susrel"),
    "pizz": ("pizz", "pizzicato samples"),
    "short": ("spicc", "spiccato", "sorspic", "sordino spiccato",
              "sordino spiccato samples", "mart", "martele",
              "martele samples"),
    "tremolo": ("trem", "tremolo", "tastrem", "tast tremo"),
}
_STYLE_OF = {d: s for s, dirs in STYLES.items() for d in dirs}
# a plucked or bounced note is one hit that rings out; tiling it to fill a
# held chord would re-pluck it every half second
SHORT_STYLES = ("pizz", "short")


def _family(path, rootp):
    up = str(path.relative_to(rootp)).upper()
    for name, marker in FAMILIES:
        if marker in up:
            return name
    return None


def _style(path, rootp):
    """The playing style from the folder right under samples/, or None."""
    parts = [p.lower() for p in path.relative_to(rootp).parts[:-1]]
    if "samples" in parts:
        i = parts.index("samples")
        if i + 1 < len(parts):
            return _STYLE_OF.get(parts[i + 1])
    return None


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


def load_picks():
    """(sections, styles) from sample_packs.json — his pick list. A missing
    key means everything this module knows, so a config without the keys
    never silently empties the strings voice."""
    try:
        cfg = json.loads(PACKS_CONFIG.read_text())
    except (OSError, ValueError):
        cfg = {}
    sections = cfg.get("strings_sections") or [f for f, _ in FAMILIES]
    styles = cfg.get("strings_styles") or list(STYLES)
    return set(sections), set(styles)


def scan(root=None):
    """Walk the Strings library -> one entry per playable note sample in
    his picked sections and styles, all four mics. Falls back to the last
    good scan when the drive's unplugged, same contract as
    melodic_loops.scan. Walks every call on purpose: generation is sized
    for variety, not speed (owner 2026-09-14)."""
    sections, styles = load_picks()
    rootp = Path(os.path.expanduser(root or ROOT))
    if not rootp.exists():
        try:
            saved = json.loads(CACHE.read_text())
        except (OSError, ValueError):
            return []
        # entries written before 2026-09-14 carry no style/mic: unusable
        return [e for e in saved if e.get("style") in styles
                and e.get("instrument") in sections and e.get("mic")]
    found = []
    for path in sorted(rootp.rglob("*")):
        if path.suffix.lower() not in AUDIO_EXTS or not path.is_file():
            continue
        tokens = _tokens(path.stem)
        mic = tokens[-1].lower()
        if mic not in MICS:
            continue
        family, style = _family(path, rootp), _style(path, rootp)
        if family not in sections or style not in styles:
            continue
        note = note_from_tokens(tokens)
        if note is None:
            continue
        found.append({"path": str(path), "note": note,
                      "instrument": family, "style": style, "mic": mic})
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(found))
    except OSError:
        pass
    return found


def nearest(index, midi_note, instrument=None, style=None, prefer=None):
    """The sample needing the smallest shift to play `midi_note`
    (optionally within one section/style), or None if the pool's empty.
    Closest-note rather than exact: this library skips every other note,
    and play_chord/note_slice shift the pick onto the exact pitch.

    `prefer`, if given, is an entry already chosen for an earlier note of
    the same chord/beat. Owner 2026-07-29: a chord stays ONE instrument
    sound. Here that means the pinned entry's section, style and mic —
    each note still gets its OWN recording. (Until 2026-09-14 this handed
    back the pinned FILE, and since nothing here shifted pitch, every
    chord played one note: C-E-G came out C-C-C.) When the pinned section
    can't reach the note within MAX_SHIFT, the same style and mic from
    any section plays it, rather than stretching the wrong way."""
    pool = [e for e in index
            if (instrument is None or e["instrument"] == instrument)
            and (style is None or e["style"] == style)]
    if prefer is not None:
        pool = [e for e in pool if e["style"] == prefer["style"]
                and e["mic"] == prefer["mic"]] or pool
        own = [e for e in pool if e["instrument"] == prefer["instrument"]]
        if own:
            pick = min(own, key=lambda e: abs(e["note"] - midi_note))
            if abs(pick["note"] - midi_note) <= MAX_SHIFT:
                return pick
    if not pool:
        return None
    return min(pool, key=lambda e: abs(e["note"] - midi_note))


def by_articulation(index, kind):
    """Sub-index of `index` for one playing style ('sustain' bed, 'pizz',
    'short', 'tremolo'). No style named -> sustain: the strings voice was
    built as a chord bed, and the identities that never set one had been
    landing on whichever file sorted first (owner 2026-09-14). A style
    with nothing indexed -> the whole index, so this never empties a pool
    the caller expected to have."""
    got = [e for e in index if e["style"] == (kind or "sustain")]
    return got or index


def beat_pool(index, style=None, mic=CLOSE, basses=True):
    """One beat's strings: one style (see by_articulation), one mic, and
    the basses only when nothing else holds the low end. Style and mic
    fall back rather than empty the pool; the basses do NOT — one low
    sound per beat is a hard rule (owner 2026-09-14), so a beat that
    already has a sub/808/bass keeps the strings above it even if that
    leaves nothing to play."""
    pool = by_articulation(index, style)
    pool = [e for e in pool if e["mic"] == mic] or pool
    if not basses:
        pool = [e for e in pool if e["instrument"] != "basses"]
    return pool


def _voice(pick, note):
    """The pick's audio, mono, shifted onto `note`, or None."""
    x = load_audio(pick["path"])
    if x is None:
        return None
    mono = x.mean(axis=1) if x.ndim == 2 else x
    return _shift(mono, note - pick["note"])


def note_slice(index, note, dur, sr=SR, cache=None, used=None, pin=None):
    """One arp step's worth of the nearest string sample to `note`: its
    first `dur` seconds with a short attack + release so it reads as a
    rhythmic note, not a swell. `cache` (a dict) holds each note's loaded
    audio so an arp doesn't reload it per step. None if nothing's
    voiceable, so chord_synth.arp_riff can pluck that step instead.
    `pin`: see nearest()'s `prefer` doc — pass the same list across every
    note of one chord/arp to keep them all in one section, style and mic."""
    if cache is not None and note in cache:
        mono = cache[note]
    else:
        pk = nearest(index, note, prefer=pin[0] if pin else None)
        if pin is not None and not pin and pk is not None:
            pin.append(pk)
        if pk is not None and used is not None:
            used.append(pk["path"])          # name the real file — see
        mono = _voice(pk, note) if pk else None
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


def play_chord(index, notes, dur, instrument=None, style=None, sr=SR,
               used=None, pin=None):
    """Sum one sample per MIDI note in `notes` into a `dur`-second chord
    bed, each shifted onto its exact note. A held style is fitted to
    length with CROSSFADED repeats; a plucked/short one rings out once
    and is padded with silence. Both are ramped to zero at the edges,
    then the stack is RMS-normalized so a 4-note chord doesn't clip.
    Returns None if not one note could be voiced (empty index / drive
    gone), so the caller can fall through.

    The crossfade + edge ramps replaced a plain np.tile 2026-07-23. The
    hard splice put a step discontinuity at every repeat seam and left the
    bed ending mid-waveform, which the owner heard as a click at the end
    of sustained chords. Measured on the sibling module: 0.209 step at a
    seam before, 0.007 after. Same defect, same fix, shared helpers.

    `pin` (see nearest()) defaults to a list private to this call, so a
    chord's own notes stay one section even when the caller doesn't pass
    one in to also share it across chord slots."""
    n = max(int(dur * sr), 1)
    out = np.zeros(n)
    pin = [] if pin is None else pin
    voiced = 0
    for note in notes:
        pick = nearest(index, note, instrument, style,
                       prefer=pin[0] if pin else None)
        if pick is None:
            continue
        if not pin:
            pin.append(pick)
        if used is not None:                 # instrument_sampler.voice_note
            used.append(pick["path"])
        seg = _voice(pick, note)
        if seg is None:
            continue
        if pick["style"] in SHORT_STYLES:
            seg = np.pad(seg[:n], (0, max(n - len(seg), 0)))
        else:
            seg = _fit_length(seg, n, sr)
        out = out + _declick(seg, sr)
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
    print("%d playable note samples (all mics)\n" % len(index))
    for key in ("instrument", "style", "mic"):
        got = {}
        for e in index:
            got[e[key]] = got.get(e[key], 0) + 1
        print("%-10s %s" % (key, ", ".join(
            "%s %d" % (k, got[k]) for k in sorted(got, key=lambda k: -got[k]))))


if __name__ == "__main__":
    _report()
