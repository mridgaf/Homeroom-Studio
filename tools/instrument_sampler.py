"""Every melodic instrument, played from the owner's OWN sample banks
(owner directive 2026-07-23: "I'm using samples created from my banks
for every instrument as much as possible").

This started as brass only, after he auditioned the synthesized horn and
rejected it outright. The same treatment now covers the major instrument
groups — piano, guitar, bell, organ, brass, wood, string, choir, pluck,
pad, synth — and the synthesized chord voices it replaced (chord_synth's
pad_voice and _pluck, tools/lead_synth.py entirely) have been DELETED.
There is deliberately no synth fallback left anywhere in the chord path.
Standing instruction: his samples over generated audio, always. If a
group sounds wrong, fix the POOL (which files are indexed, MIN_CLARITY),
never by reintroducing an oscillator.

How it works, and why it's this way:

- The pitch a sample SOUNDS is detected here (autocorrelation, numpy
  only, no new dependency) rather than read from the file name. His packs
  name the SONG KEY, not the note ("89 Bpm_Cm_BLEECH_Muted Horns 1"),
  which is the one thing that makes this different from string_sampler.py
  — the London Strings library names an exact MIDI note per file, so that
  module can pick a note and never pitch-shift. Nothing else here is new;
  the scan/index/nearest/play_chord shape is string_sampler's.
- MULTI-SAMPLE, required by the owner and for the obvious reason: one
  sample stretched across three octaves is a chipmunk going up and mud
  going down. `nearest` picking the closest source note IS the zone map,
  so there's no zone table to keep in sync. Run this file to print the
  per-group coverage — it reports the worst shift any note in the chord
  range has to make, which is the number that decides whether a group
  sounds natural.
- His melodic material is mostly LOOPS (median ~9.6s), not one-shots, so
  a long source is chopped to its FIRST HIT before being used as a note —
  otherwise a "note" would drag a whole phrase in behind it. That's
  melodic_loops.chop_onsets, already used by chord_synth.loop_voice for
  exactly this reason. Short one-shots are used whole, unchanged.

    ./.venv/bin/python tools/instrument_sampler.py    # coverage report
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
from chord_synth import PEAK_CEILING                        # noqa: E402
from make_hiphop_tracks import load_audio, norm_rms         # noqa: E402
from melodic_loops import chop_onsets                       # noqa: E402
from melodic_loops import scan as scan_melodic              # noqa: E402
from sample_library import load_instrument_roots             # noqa: E402

CACHE = Path(os.path.expanduser("~/.reason_voice/instrument_sampler_index.json"))
# Bump whenever detect_pitch changes: cached notes were measured by the
# OLD detector and would otherwise be trusted forever. v2 = sub-octave fix.
DETECT_VERSION = 2

# name tokens -> instrument group. ORDERED, first match wins, so a
# "Melody_Flute" loop is a wood instrument and not a generic lead — the
# same first-match-wins precedence sample_library.DIR_ROLES and
# melodic_loops.ROLE_WORDS already use. Specific instruments first,
# catch-all synth voices last.
GROUPS = [
    ("piano", ("piano", "pianos", "rhodes", "wurli", "wurlitzer", "epiano",
               "keys", "clav", "clavinet", "harpsichord")),
    ("guitar", ("guitar", "guitars", "gtr", "strum", "acoustic", "banjo",
                "mandolin", "sitar", "koto", "ukulele")),
    ("bell", ("bell", "bells", "glock", "glockenspiel", "celeste", "chime",
              "chimes", "kalimba", "marimba", "vibes", "vibraphone",
              "xylophone", "toybox")),
    ("organ", ("organ", "organs", "hammond", "accordion", "harmonium")),
    ("brass", ("brass", "trumpet", "trumpets", "horn", "horns", "flugel",
               "fanfare", "trombone", "tuba", "cornet")),
    ("wood", ("flute", "flutes", "clarinet", "oboe", "bassoon", "sax",
              "saxx", "saxophone", "whistle", "recorder", "ocarina",
              "wood", "woods", "woodwind", "woodwinds")),
    ("string", ("string", "strings", "violin", "violins", "cello", "viola",
                "harp", "fiddle", "orchestra", "orchestral")),
    ("choir", ("choir", "choirs", "voices", "aah", "ooh", "vocalise")),
    ("pluck", ("pluck", "plucks", "plucked")),
    ("pad", ("pad", "pads", "atmos", "ambient", "ambience", "drone")),
    ("synth", ("synth", "synths", "saw", "square", "lead", "leads", "arp",
               "arps", "bleep", "stab", "stabs",
               # "chop"/"chops" added 2026-09-20 (owner): the "Instrument
               # Chops" folder is a grab-bag of chopped instrument stabs
               # with no single family, so it plays as the generic sampled
               # voice. Reached by folder name via _dir_group.
               "chop", "chops")),
]
GROUP_NAMES = tuple(g for g, _ in GROUPS)

# Which BOTC Sorted Instruments folders a MIDI phrase may be played on
# (owner 2026-09-19: "MIDI able to use the instruments you suggest" -
# Pianos, Organs, Guitars, Bells on top of the Synths/Plucks/Pads it
# already used). One instrument per beat, chosen from the ones that can
# actually cover the phrase's notes; the synth family stays behind it as
# the fall-through so a note never goes silent.
MIDI_VOICES = ("piano", "organ", "guitar", "bell", "synth", "pluck", "pad")
MIDI_FALLBACK = ("synth", "pluck", "pad")


def midi_groups(index, notes, rng):
    """The group order a beat's MIDI chords are played with: one primary
    group (random, but only among those with a sample near EVERY note of
    the phrase, so a 1-file group like Organs can't be stretched across
    the whole range), then the synth family as backup. Falls back to the
    old synth-only order when nothing covers."""
    cands = [g for g in MIDI_VOICES if covers(index, notes, g)]
    if not cands:
        return MIDI_FALLBACK
    primary = rng.choice(cands)
    return (primary,) + tuple(g for g in MIDI_FALLBACK if g != primary)

# A signature's `chord_source` word -> the group(s) it may draw from, best
# first. "synth" stays a valid identity word (9 of the 12 legends are
# built on it) but now means SAMPLED synth/pluck/pad material out of his
# own banks, not an oscillator — so no config had to be rewritten when
# pad_voice was deleted. "strings" is NOT here: that one keeps going to
# string_sampler.py, whose library names an exact MIDI note per file and
# so never has to pitch-shift at all.
VOICES = {
    "synth": ("synth", "pluck", "pad"),
    "horns": ("brass",),
    "piano": ("piano",),
    "guitar": ("guitar",),
    "bell": ("bell",),
    "organ": ("organ",),
    "wood": ("wood",),
    # only 2 usable choir samples in his banks, so a sustained pad backs it
    # up — the closest thing he owns to a held vocal bed.
    "choir": ("choir", "pad"),
    "pad": ("pad", "synth"),
    "pluck": ("pluck", "synth"),
    "orchestral": ("string", "brass"),
    # his OWN 8-bit/video-game files. No second group behind it on
    # purpose: the point of asking for chip is the chip timbre, and
    # handing off to "synth" would quietly answer a different question.
    # When this can't cover a beat the caller uses the synthesized chip
    # voice instead — see _build_chords (owner rule 2026-07-25).
    "chip": ("chip",),
}

# Autocorrelation peak height needed to trust a detected pitch. 0.70 was
# measured, not guessed: below it the reads stop agreeing with the files'
# own key labels (a "brass moan" bend has no one pitch to find), and an
# out-of-tune source is worse than a slightly bigger shift, since it lands
# every note built from it at the wrong pitch.
MIN_CLARITY = 0.70
NOTE_LO, NOTE_HI = 33, 96      # a detected pitch outside this is a bad read
CHOP_SECS = 3.0                # longer than this = a phrase; take one hit
# How far a note may be pitch-shifted from its source before the group is
# considered unable to cover it and the NEXT group in the VOICES list is
# tried instead. A major third is about where the tape-speed shift starts
# reading as wrong rather than as the instrument. Measured coverage says
# the big groups (piano/guitar/brass/string/synth) never come close to
# this; it exists for the thin ones — see the report's WIDE markers.
MAX_SHIFT = 4
# How far an ALREADY-CHOSEN sample (nearest()'s `prefer`) is allowed to
# stretch before a chord/arp gives up on it and picks a fresh nearest
# match instead — deliberately wider than MAX_SHIFT above. Owner
# 2026-07-29: a chord routinely spans more than a major third (MAX_SHIFT),
# so capping reuse at MAX_SHIFT meant most chords still switched packs
# mid-chord — the "strings and synths stacked with other instruments" bug.
# Given the choice between (a) stretching one real recording up to an
# octave, which can start sounding a little pitch-shifted/"chipmunked",
# or (b) hunting a same-pack fallback file (more code, more testing), he
# picked (a) — fast, and one consistent instrument color beats an exactly
# in-tune note from a different one.
PREFER_MAX_SHIFT = 12
# De-click envelope. A sampled note has to START and END at zero, or the
# step from silence into a mid-waveform sample (measured up to 0.35) fires
# a broadband impulse — which is the harsh "digital" tick the owner heard
# at the end of every sustained chord. 8ms/60ms are the numbers note_slice
# already used successfully, kept identical rather than invented fresh.
ATTACK_S, RELEASE_S = 0.008, 0.060
XFADE_S = 0.030                # crossfade for repeats — see _fit_length
_SPLIT = re.compile(r"[\s_\-]+")


def _tokens(name):
    return {t.lower().strip("().,") for t in _SPLIT.split(name) if t}


# 8-bit / video-game material, by name. A regex rather than a token list
# because the naming is irregular ("8 Bit", "8-bit", "8bit", "Game Boy").
# Owner rule 2026-07-25: "if there are eight bit or sixteen bit or video
# game sounds in my real library, use those" — so this group exists to let
# his own files beat the synthesized chip voice whenever they can.
# Deliberately NOT matched: "coin" (his "Cymatics - Bitcoin Perc" is not a
# game sound), "retro" ("PLAYOFFS - SNR Retro" is a snare) and "pixel" —
# each was checked against real filenames and produced false positives.
CHIP_RE = re.compile(
    r"(\b8\s*-?\s*bit\b|\b16\s*-?\s*bit\b|\b8bit\b|\b16bit\b|chiptune"
    r"|\bchip\s*tune\b|\bnes\b|\bsnes\b|famicom|\bgame\s*boy\b|gameboy"
    r"|\barcade\b|\batari\b|\bc64\b|\bblip\b|\bbleep\b|\bvideo\s*game\b)",
    re.I)


def group_of(name):
    """The instrument group a file name belongs to, or None. Whole-TOKEN
    matching, not substring — the real trap being "Cymatics - LEAD Hornet",
    a synth lead that a substring match reads as a horn."""
    if CHIP_RE.search(name):
        return "chip"
    toks = _tokens(name)
    for group, words in GROUPS:
        if toks & set(words):
            return group
    return None


def _dir_group(path_str, roots):
    """Group from the nearest classifying ancestor folder under one of
    `roots`, or None. Mirrors sample_library._dir_role for the drum pool:
    under the OWNER-sorted instrument folder, the folder name is
    authoritative, so a file keeps its real family even when the name
    lies — same class of bug as the horns-correction/vocal-vox miss on
    the drum side (owner 2026-09-13, BOTC Sorted Instruments). Checked
    BEFORE group_of()'s filename guess, never after."""
    p = Path(path_str)
    for root in roots:
        rootp = Path(root).expanduser()
        try:
            rel = p.relative_to(rootp)
        except ValueError:
            continue
        for seg in reversed(rel.parts[:-1]):        # nearest ancestor first
            if CHIP_RE.search(seg):
                return "chip"
            toks = _tokens(seg)
            for group, words in GROUPS:
                if toks & set(words):
                    return group
        return None
    return None


def covers(index, notes, groups, max_shift=MAX_SHIFT):
    """True when `groups` hold a sample within `max_shift` of EVERY note.

    nearest() deliberately returns a least-bad stretched pick rather than
    None, because for the big groups silence would be worse. That is the
    wrong answer for a group the caller is only willing to use when it
    genuinely fits — the owner chose "the backup plays the whole beat"
    over "stretch the instrument further" (2026-07-25). This is the
    explicit yes/no that choice needs.
    """
    got = [e for e in index if e["group"] in _as_groups(groups)]
    if not got:
        return False
    return all(min(abs(e["note"] - n) for e in got) <= max_shift
               for n in notes)


def detect_pitch(mono, sr=SR):
    """(midi_note, clarity) for a sample's ATTACK, or (None, 0.0).

    Autocorrelation over the half second after the onset — the owner's
    instruction is to sample the beginning of the loop, and that's also
    the most reliable place to read pitch, before a delay tail or the
    next chord in a phrase muddies it. `clarity` is the normalized height
    of the winning peak: 1.0 is perfectly periodic, and under MIN_CLARITY
    means unpitched (a growl, a noise-heavy hit) and gets dropped.
    """
    x = np.asarray(mono, dtype=np.float64)[: int(1.2 * sr)]
    if len(x) < 2048:
        return None, 0.0
    x = x - x.mean()
    peak = np.abs(x).max()
    if peak < 1e-5:                                  # silent file
        return None, 0.0
    onset = int(np.argmax(np.abs(x) > 0.2 * peak))
    x = x[onset:onset + int(0.5 * sr)]
    if len(x) < 2048:
        return None, 0.0
    x = x * np.hanning(len(x))
    n = 1 << (2 * len(x) - 1).bit_length()           # FFT autocorrelation
    f = np.fft.rfft(x, n)
    ac = np.fft.irfft(f * np.conj(f))[:len(x)]
    if ac[0] <= 0:
        return None, 0.0
    ac = ac / ac[0]
    lo, hi = int(sr / 1200.0), int(sr / 55.0)        # 55Hz .. 1200Hz
    seg = ac[lo:hi]
    if len(seg) < 3:
        return None, 0.0
    # Take the SHORTEST lag that correlates nearly as well as the best one,
    # not the best one outright. Plain argmax octave-errors: autocorrelation
    # peaks at every MULTIPLE of the true period, and when the period isn't
    # a whole number of samples a longer multiple can land on a sample
    # boundary and score higher than the fundamental — which read G4 and G5
    # as the same G3. Preferring the first near-best peak locks onto the
    # fundamental instead. (Caught by test_instrument_sampler.)
    best = float(seg.max())
    if best <= 0:
        return None, 0.0
    peaks = np.where((seg[1:-1] >= seg[:-2]) & (seg[1:-1] >= seg[2:]))[0] + 1
    near = [int(p) for p in peaks if seg[p] >= 0.9 * best]
    k = (near[0] if near else int(np.argmax(seg))) + lo
    midi = 69.0 + 12.0 * np.log2((sr / k) / 440.0)
    return midi, float(ac[k])


def _load_cache():
    try:
        got = json.loads(CACHE.read_text())
    except (OSError, ValueError):
        return {}
    if got.get("version") != DETECT_VERSION:         # stale detector: redo
        return {}
    return got


def _pitched(todo, status, cache_key):
    """Pitch-detect a list of (entry, group) pairs into index rows, with
    the shared per-(path, size) pitch cache. Both indexes (chords and
    bass) go through here so a file's pitch is only ever measured once.

    Pitch detection is cached per (path, size). The first run over a big
    library costs real time (~76ms a file), so `status` gets progress
    lines; every run after is a dict lookup, since a sample's pitch can't
    change without its bytes changing.
    """
    cache = _load_cache()
    pitches = cache.get("_pitches", {})
    found = []
    fresh = 0
    for i, (e, group) in enumerate(todo):
        path = Path(e["path"])
        try:
            key = "%s|%d" % (path, path.stat().st_size)
        except OSError:                              # drive gone mid-scan
            continue
        got = pitches.get(key)
        if got is None:
            if status and fresh % 50 == 0:
                status("indexing instrument samples %d/%d" % (i + 1, len(todo)))
            x = load_audio(str(path))
            if x is None:
                continue
            mono = x.mean(axis=1) if x.ndim == 2 else x
            midi, clarity = detect_pitch(mono)
            got = [None if midi is None else round(midi, 2), round(clarity, 3)]
            pitches[key] = got
            fresh += 1
        midi, clarity = got
        if midi is None or clarity < MIN_CLARITY:
            continue
        note = int(round(midi))
        if not NOTE_LO <= note <= NOTE_HI:
            continue
        found.append({"path": str(path), "name": e["name"], "note": note,
                      "clarity": clarity, "group": group})
    if found:                    # always refresh: writing only when new
        try:                     # files appeared would leave the unplugged
            CACHE.parent.mkdir(parents=True, exist_ok=True)   # fallback
            cache["version"] = DETECT_VERSION                 # index stale
            cache["_pitches"] = pitches
            cache[cache_key] = found
            CACHE.write_text(json.dumps(cache))
        except OSError:
            pass
    if not found:                                    # drive unplugged
        return _load_cache().get(cache_key, [])
    return found


def _is_riser(path_str):
    """A riser/sweep transition, by folder or name. Owner 2026-09-20 chose
    to keep risers OUT of the pitched instrument engine -- a swoosh has no
    single note, so pitch-detecting it is meaningless. Whole-token match so
    'Highriser' or 'Sunrise' can't trip it."""
    import re as _re
    toks = {t for p in Path(path_str).parts for t in _re.split(r"[^a-z0-9]+", p.lower())}
    return bool(toks & {"riser", "risers", "uplifter", "uplifters"})


def scan(index=None, status=None):
    """The playable instrument index: one entry per usable file, carrying
    the group it belongs to and the MIDI note it actually sounds. Reads
    the melodic-loop index rather than re-walking the drive — that scan is
    already cached and already has the unplugged-drive fallback, so this
    adds no new disk crawl.
    """
    roots = load_instrument_roots()
    # require_key=False (owner 2026-09-20): the instrument engine detects
    # pitch by ear in _pitched below, so it does not need the key spelled
    # in the file name -- this is what finally lets the keyless Bass, sub
    # and Instrument Chops files in. The loop engine keeps require_key=True.
    entries = scan_melodic(roots=roots, require_key=False) if index is None else index
    todo = []
    for e in entries:
        if e.get("role") == "bass":       # a bass sample voiced as a chord
            continue                      # is mud, whatever its name says
        if _is_riser(e["path"]):          # risers stay out (owner 2026-09-20)
            continue
        group = _dir_group(e["path"], roots) or group_of(e["name"])
        if group is not None:
            todo.append((e, group))
    return _pitched(todo, status, "index")


def scan_bass(index=None, status=None):
    """His BASS one-shots (role 'bass' in the melodic index), pitch-
    detected, for the chord bass LINE. Kept apart from scan() on purpose:
    a bass sample voiced as a whole CHORD is mud — which is why scan()
    excludes them — but a bass line plays one root at a time, and that is
    exactly what these files are. Owner 2026-07-25: the synth bass under
    the chords becomes his own bass sounds wherever they can reach."""
    entries = scan_melodic(roots=load_instrument_roots(), require_key=False) if index is None else index
    todo = [(e, "bass") for e in entries
            if e.get("role") == "bass" and not _is_riser(e["path"])]
    return _pitched(todo, status, "bass_index")


def _as_groups(groups):
    if groups is None:
        return None
    return (groups,) if isinstance(groups, str) else tuple(groups)


def pool(index, groups):
    """The entries belonging to `groups` (a group name or a tuple of them,
    best first). Falls through in order, so a signature asking for a group
    the library can't cover at all still gets its second choice rather
    than silence."""
    groups = _as_groups(groups)
    if groups is None:
        return list(index)
    for g in groups:
        got = [e for e in index if e["group"] == g]
        if got:
            return got
    return []


def _closest(entries, midi_note):
    """Least pitch shift wins; ties break toward the clearer-pitched
    sample, since a confident read shifts more predictably."""
    if not entries:
        return None
    return min(entries,
               key=lambda e: (abs(e["note"] - midi_note), -e["clarity"]))


def nearest(index, midi_note, groups=None, max_shift=MAX_SHIFT, prefer=None):
    """The source sample needing the smallest pitch shift to play
    `midi_note` — the multi-sample zone lookup.

    Group fall-through is by COVERAGE, not just emptiness: a group that
    exists but has no sample within `max_shift` of this note hands off to
    the next group in the list. That matters because his thin groups are
    thin unevenly — "pluck" has 30 samples but a 6-semitone hole, so
    without this a pluck note landing in the hole would be stretched into
    sounding wrong while a perfectly good synth sample sat unused. If no
    listed group can cover the note, the least-bad pick across all of them
    is returned rather than None; silence would be worse, and the report
    flags those groups as WIDE so the ceiling is visible.

    `prefer`, if given, is an entry already chosen for an earlier note in
    the same chord/arp (owner 2026-07-29: "the strings and synths are
    still stacked... with other instruments" — a thin group like "synth"
    is scattered one-shots from many different vendor packs, so picking
    the objectively closest file PER NOTE was pulling a different pack's
    sound for every note of one chord — same label, several actually-
    different instruments underneath it). `prefer` wins over a closer
    match out to PREFER_MAX_SHIFT (wider than max_shift on purpose — see
    its own comment); losing pitch precision on some notes is worth
    keeping the whole chord one real instrument."""
    if prefer is not None and abs(prefer["note"] - midi_note) <= PREFER_MAX_SHIFT:
        return prefer
    groups = _as_groups(groups)
    if groups is None:
        return _closest(index, midi_note)
    considered = []
    for g in groups:
        got = [e for e in index if e["group"] == g]
        if not got:
            continue
        considered.extend(got)
        pick = _closest(got, midi_note)
        if abs(pick["note"] - midi_note) <= max_shift:
            return pick
    return _closest(considered, midi_note)


def _shift(mono, semitones):
    """Resample `mono` by `semitones`. Speed-change pitch shift (the tape
    trick): duration moves with pitch, which is why the shift has to stay
    small — the multi-sample zoning is what keeps it that way. Same
    one-ratio np.interp resample melodic_loops.fit_loop uses; no phase
    vocoder, no new dependency."""
    if semitones == 0 or not len(mono):
        return np.asarray(mono, dtype=np.float64)
    ratio = 2.0 ** (semitones / 12.0)
    n = max(int(round(len(mono) / ratio)), 1)
    idx = np.linspace(0, len(mono) - 1, n)
    return np.interp(idx, np.arange(len(mono)), np.asarray(mono, dtype=np.float64))


def _attack(mono):
    """From the onset onward — the owner's "sample the beginning of the
    loop". Drops leading silence so a sample with air in front of it
    doesn't play late against the beat grid."""
    x = np.asarray(mono, dtype=np.float64)
    peak = np.abs(x).max() if len(x) else 0.0
    if peak < 1e-5:
        return x
    return x[int(np.argmax(np.abs(x) > 0.2 * peak)):]


def _one_hit(mono, sr=SR):
    """A single playable NOTE out of a source file. Short one-shots pass
    through whole (only trimmed to their onset). Anything longer than
    CHOP_SECS is a phrase or a rhythmic loop, so it's chopped and only its
    FIRST hit is kept — otherwise a "note" drags the rest of the phrase in
    behind it, and a tiled loop drifts against the beat grid (the ceiling
    chord_synth.sample_pool documents). The first hit is also the one
    detect_pitch measured, so the note stays honest."""
    x = _attack(mono)
    if len(x) <= CHOP_SECS * sr:
        return x
    chops = chop_onsets(x, sr, max_dur=CHOP_SECS)
    return chops[0] if chops else x[:int(CHOP_SECS * sr)]


def _fit_length(seg, n, sr=SR):
    """`seg` cropped or repeated to exactly `n` samples, CROSSFADING each
    repeat instead of butt-splicing it.

    A plain np.tile puts a step discontinuity at every seam. That was
    audible and it's what the owner reported: a 2.2s brass chord built
    from a 1.07s sample had hard jumps at 1.074s and 2.148s, the second
    landing 52ms before the end — "clipping at the end of the samples".
    A short equal-length crossfade removes the step; the seam is still a
    repeat musically, but it no longer ticks."""
    seg = np.asarray(seg, dtype=np.float64)
    if not len(seg):
        return np.zeros(n)
    if len(seg) >= n:
        return seg[:n].copy()
    xf = min(int(XFADE_S * sr), len(seg) // 4)
    if xf < 2:                                   # too short to crossfade
        return np.tile(seg, n // len(seg) + 1)[:n]
    fade_in = np.linspace(0.0, 1.0, xf)
    hop = len(seg) - xf
    out = np.zeros(n + len(seg))
    pos = 0
    while pos < n:
        piece = seg.copy()
        if pos:                                  # not the first: fade in
            piece[:xf] *= fade_in                # over the previous tail
        piece[-xf:] *= fade_in[::-1]
        out[pos:pos + len(piece)] += piece
        pos += hop
    return out[:n]


def _declick(seg, sr=SR):
    """Ramp the very start and end to zero so the buffer can't step into
    or out of silence. Mutates a copy, never the cached source."""
    seg = np.asarray(seg, dtype=np.float64).copy()
    m = len(seg)
    a = min(int(ATTACK_S * sr), m)
    r = min(int(RELEASE_S * sr), m)
    if a:
        seg[:a] *= np.linspace(0, 1, a)
    if r:
        seg[-r:] *= np.linspace(1, 0, r)
    return seg


def voice_note(index, note, dur, groups=None, sr=SR, cache=None, used=None,
               pin=None):
    """One note at `note`, exactly in tune, `dur` seconds long: nearest
    source -> one hit -> pitch-shift to the target -> fit to length with
    crossfaded repeats -> de-clicked at both edges. None when nothing's
    voiceable, so the caller can fall through. `cache` (a dict) holds
    loaded+trimmed audio so a chord or arp doesn't reload a file per note.

    `pin` (a list, used as an in/out box — pass the SAME list across every
    note of one chord/arp/beat to keep them all preferring one source; see
    nearest()). Empty going in means "nothing chosen yet"; this call fills
    it in with whichever entry actually got used, so the next call reuses
    it. None (the default) keeps the old independent-per-note behavior.

    The edge ramps are a deliberate, narrow exception to the project's
    "no edge fades" loop-safe rule. That rule protects the BEAT's own loop
    point; this is one note inside a bar, handed off to the next chord,
    and 8ms/60ms on a note is an instrument's own attack and release, not
    a fade on the loop. A chord slot that happens to span the entire beat
    pays a 60ms dip at the loop point — far cheaper than a click."""
    pick = nearest(index, note, groups, prefer=pin[0] if pin else None)
    if pick is None:
        return None
    if pin is not None and not pin:
        pin.append(pick)
    # `used` collects the FILE this note actually came from, so the beat's
    # recipe can name it and the stem rack can stop saying "built from
    # scratch" over audio that is entirely his own library (owner
    # 2026-07-25 — the label was the whole reason he believed the
    # his-instruments rule was being ignored).
    if used is not None:
        used.append(pick["path"])
    key = pick["path"]
    if cache is not None and key in cache:
        mono = cache[key]
    else:
        x = load_audio(pick["path"])
        if x is None:
            return None
        mono = _one_hit(x.mean(axis=1) if x.ndim == 2 else x, sr)
        if cache is not None:
            cache[key] = mono
    if not len(mono):
        return None
    seg = _shift(mono, note - pick["note"])
    return _declick(_fit_length(seg, max(int(dur * sr), 1), sr), sr)


def note_slice(index, note, dur, sr=SR, cache=None, groups=None, used=None,
               pin=None):
    """One arp/stab step. Drop-in for string_sampler.note_slice, so
    chord_synth.arp_riff drives any instrument with the same render_note
    callback it uses for strings. The attack/release that used to live
    here now applies to EVERY voiced note (voice_note), because the
    sustained chord bed needed exactly the same de-clicking — it was the
    one path that never got it. `pin`: see voice_note."""
    return voice_note(index, note, dur, groups=groups, sr=sr, cache=cache,
                      used=used, pin=pin)


def play_chord(index, notes, dur, groups=None, sr=SR, used=None, pin=None):
    """A chord: one sampled, in-tune voice per MIDI note, summed into a
    `dur`-second bed — the sampled replacement for chord_synth.pad_voice.
    Same contract string_sampler.play_chord offers (None if not one note
    could be voiced, so the caller falls through). RMS-normalized then
    peak-guarded, because a stack of attacks crests hard even at a polite
    RMS. `pin` (see voice_note) defaults to a list private to this call,
    so a chord's own notes prefer one source even when the caller doesn't
    pass one in to also share it across chord slots."""
    n = max(int(dur * sr), 1)
    out = np.zeros(n)
    cache = {}
    pin = [] if pin is None else pin
    voiced = 0
    for note in notes:
        seg = voice_note(index, note, dur, groups=groups, sr=sr, cache=cache,
                         used=used, pin=pin)
        if seg is None:
            continue
        out = out + seg
        voiced += 1
    if not voiced:
        return None
    out = norm_rms(out, -18.0)
    peak = np.max(np.abs(out))
    if peak > PEAK_CEILING:              # see chord_synth.PEAK_CEILING: a
        out = out * (PEAK_CEILING / peak)  # 0.99 ceiling still clips BETWEEN
    return out                             # samples on playback



def _report():
    index = scan(status=lambda m: print("  " + m))
    if not index:
        print("No instrument samples found. Is the sample drive plugged in?")
        return
    NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    by = {}
    for e in index:
        by.setdefault(e["group"], []).append(e)
    print("\n%d playable pitched samples across %d groups\n"
          % (len(index), len(by)))
    print("%-8s %6s  %-13s  %s"
          % ("group", "count", "range", "worst shift in MIDI 48-77"))
    for group in GROUP_NAMES:
        got = by.get(group)
        if not got:
            print("%-8s %6d  %-13s  --" % (group, 0, "-"))
            continue
        notes = sorted(e["note"] for e in got)
        worst = max(min(abs(t - m) for m in notes) for t in range(48, 78))
        print("%-8s %6d  %-13s  %d semitones%s"
              % (group, len(got),
                 "%s%d..%s%d" % (NOTE[notes[0] % 12], notes[0] // 12 - 1,
                                 NOTE[notes[-1] % 12], notes[-1] // 12 - 1),
                 worst, "   <-- WIDE" if worst > 4 else ""))
    print("\nchord_source words a signature can ask for:")
    for word, groups in sorted(VOICES.items()):
        have = pool(index, groups)
        print("  %-11s -> %-22s %d samples"
              % (word, "/".join(groups), len(have)))


if __name__ == "__main__":
    _report()
