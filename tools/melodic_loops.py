"""Melodic-LOOP ingestion (punch list step 5, revisited 2026-07-22).

BEAT-GENERATOR-GAP-ANALYSIS.md flagged step 5 as blocked on Essentia
(key) + madmom (tempo) — both heavy, neither a light install on macOS.
That's true for UNLABELED loops. It turns out most of the owner's
melodic library isn't unlabeled: Cymatics one-shots end in "- C.wav",
Function Loops loops are "..._140_..._Gm.wav", and the Live loop cds
packs fold bpm+key right into the folder name ("075_MoveOn_Bm/"). The
vendor already did the detection and put the answer in the file name —
same reasoning midi_packs.py used to go MIDI-first: read the label
instead of guessing, zero pitch/tempo-detection risk, no new dependency.

This is the audio-file twin of midi_packs.py: same scan()/cache/in_key()
shape, but parses key + bpm from path TOKENS (folder names split by the
one packs actually use) instead of reading note data. Files with no
parseable key are left out of the index entirely — that IS the one-
shot/loop-vs-drum filter, no separate exclude-word list needed.

    ./.venv/bin/python tools/melodic_loops.py            # library report

Step 6 (fitting a pick into the beat's key) is `fit_loop` below: pitch-
corrected by resample, then cropped/tiled to length the same loop-safe
way every other lane in this project fits a bar (loop-safe-renders:
crop/tile, no edge fades). No independent tempo-stretch — see its
docstring for the ceiling.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import numpy as np                                          # noqa: E402

from key_context import KeyContext, mode_family, pitch_class   # noqa: E402
from sample_library import AUDIO_EXTS, load_roots            # noqa: E402

CACHE = Path(os.path.expanduser("~/.reason_voice/melodic_loop_index.json"))

# folder/file words -> what this loop is FOR. First match wins scanning
# path parts closest to the file first, same precedence rule midi_packs
# uses ("Essential Chord MIDI" beats a generic "MIDI").
ROLE_WORDS = [
    ("drum", ("DRUM", "PERC", "KICK", "SNARE", "CLAP", "HAT", "COWBELL",
              "CRASH", "FX", "SFX")),
    ("vocal", ("VOCAL", "VOX", "ACAPELLA")),
    ("bass", ("BASS", "808", "SUB")),
    ("chord", ("CHORD", "HARMON", "PAD", "KEYS", "PIANO")),
    ("melody", ("MELOD", "LEAD", "ARP", "TOPLINE", "PLUCK", "GUITAR",
                "SAX", "SYNTH", "INSTR", "MUSIC")),
]

# a bare key token on its own, e.g. "Gm", "C#", "Bb", "F#m" — the shape
# Cymatics/Function Loops/Live loop cds all use. The mode suffix has TWO
# spellings across his packs: bare "m" ("Gm") AND a full word glued on
# ("DbMaj", "Fmin", "EMajor"). The word form was being MISSED (owner
# 2026-07-24: "there are a lot of synth aif ... are we using those") —
# 43 melodic files, incl. the Cymatics Raptor arp/chord loops and the
# Live loop cds Rhodes/Piano/Pad, carry a <Key>Maj/<Key>Min token and
# were silently dropped for "no key". Longer alternatives first so
# "minor" wins over "min" before the $ anchor.
_KEY_TOKEN = re.compile(r"^([A-G])(#|b)?(major|maj|minor|min|m)?$", re.I)
_SPLIT = re.compile(r"[\s_\-]+")


def _mode_from_suffix(suffix):
    """'Maj'/'min'/'m'/None -> the mode label melodic_loops uses. A bare
    key with NO suffix stays None ('fits either', per in_key's tiering)."""
    if not suffix:
        return None
    s = suffix.lower()
    return "major" if s in ("maj", "major") else "minor"


def _tokens(path, rootp):
    parts = list(path.relative_to(rootp).parts)
    parts[-1] = path.stem
    out = []
    for part in parts:
        out.extend(t for t in _SPLIT.split(part) if t)
    return out


def key_from_tokens(tokens):
    """The LAST token that reads as a key, or None. Rightmost because a
    trailing qualifier ("Mod", "Loop") sometimes follows the key token,
    so this scans the whole path but keeps the last true match rather
    than stopping at the very last token."""
    found = None
    for tok in tokens:
        m = _KEY_TOKEN.match(tok)
        if not m:
            continue
        try:
            pitch_class(m.group(1) + (m.group(2) or ""))
        except ValueError:
            continue
        found = (m.group(1) + (m.group(2) or ""), _mode_from_suffix(m.group(3)))
    return found


def bpm_from_tokens(tokens):
    """A plausible BPM: a bare 2-3 digit token in the normal loop range.
    Range-gated so "808" (a bass name, not a tempo) doesn't get read as
    one — 808 is outside 50-220, so it's excluded on its own."""
    for tok in tokens:
        if tok.isdigit() and len(tok) in (2, 3) and 50 <= int(tok) <= 220:
            return int(tok)
    return None


def _role(tokens):
    for tok in reversed(tokens):
        up = tok.upper()
        for role, words in ROLE_WORDS:
            if any(w in up for w in words):
                return role
    return "melody"


# OWNER HARD RULE 2026-08-03: "No matter what the situation, one instrument
# per stem." A loop of a piano is one instrument. A loop labelled ALL / FULL
# / MIX is the whole arrangement — drums included — and putting one on a
# chord lane produces a stem with a full beat inside it. That is exactly what
# he found on beat 1702, whose chord voice was "105_Aiyf_ALL Bb".
#
# Excluding these does NOT cost him the loop voice: these packs ship both
# versions side by side. "070_Ragamuffin_ALL Cm" is dropped and
# "070_Ragamuffin_Organ Cm" is kept, which is the one that was wanted.
#
# Matched on whole tokens, never on substrings — "ALL" must not swallow
# "Ballad", and "MIX" must not swallow "Mixolydian".
FULL_MIX_WORDS = {"ALL", "FULL", "MIX", "MIXDOWN", "MASTER", "BEAT",
                  "FULLMIX", "FULLTRACK", "TRACK", "SONG", "COMPLETE"}


def is_full_mix(tokens):
    """True when the file name says this is a whole arrangement rather than
    a single instrument."""
    for tok in tokens:
        for word in re.split(r"[^A-Za-z0-9]+", str(tok).upper()):
            if word in FULL_MIX_WORDS:
                return True
    return False


def scan(roots=None):
    """Walk the pack roots -> melodic loops/one-shots whose file name
    itself names a key. Falls back to the last good scan when the drive
    is unplugged, same contract as sample_library.scan_packs and
    midi_packs.scan."""
    roots = roots if roots is not None else load_roots()
    found = []
    seen_any = False
    for root in roots:
        rootp = Path(os.path.expanduser(root))
        if not rootp.exists():
            continue
        seen_any = True
        for path in sorted(rootp.rglob("*")):
            if path.suffix.lower() not in AUDIO_EXTS or not path.is_file():
                continue
            tokens = _tokens(path, rootp)
            key = key_from_tokens(tokens)
            if key is None:
                continue
            role = _role(tokens)
            if role in ("drum", "vocal"):
                continue
            if is_full_mix(tokens):
                continue
            parts_up = " ".join(tokens).upper()
            kind = "loop" if "LOOP" in parts_up else "oneshot"
            found.append({
                "name": path.stem, "path": str(path), "kind": kind,
                "role": role, "key": key[0], "mode": key[1],
                "bpm": bpm_from_tokens(tokens),
            })
    if not seen_any:                              # drive unplugged
        try:
            return json.loads(CACHE.read_text())
        except (OSError, ValueError):
            return []
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(found))
    except OSError:
        pass
    return found


def in_key(index, key, role=None, bpm=None):
    """Picks worth reaching for in a given key: exact root+mode first,
    then a root-only match (a one-shot with no mode marker fits either),
    then same-mode any-root (transposes cleanly via KeyContext.shift_from).
    Sorted within each tier by closeness to `bpm` when both sides know
    a tempo; unknown-bpm entries (most one-shots) sort last in their
    tier, not out of it — they're still usable, just untimed."""
    want = [e for e in index if e.get("role") == role] if role is not None \
        else list(index)

    # Match on the mode's FAMILY, not the mode name. His packs label files
    # "Gm"/"C" and never "G dorian", so comparing a modal key straight
    # against a sample's label matched NOTHING and this function returned
    # an empty list — silently starving the loop voice of every modal
    # identity (DJ Premium is loop-dominant and had been failing over to
    # synth on every beat). Found 2026-07-24.
    want_family = mode_family(key.mode)

    def tier(e):
        fam = None if e["mode"] is None else mode_family(e["mode"])
        if e["key"] == key.root and (fam is None or fam == want_family):
            return 0
        if fam == want_family:
            return 1
        return 2

    def dist(e):
        if bpm is None or e.get("bpm") is None:
            return float("inf")
        return abs(e["bpm"] - bpm)

    ranked = sorted((e for e in want if tier(e) < 2), key=lambda e: (tier(e), dist(e)))
    return ranked


def fit_loop(x, sr, dst_secs, src_key=None, dst_key=None):
    """Pitch-correct a picked loop into `dst_key`, then crop/tile it to
    `dst_secs` — the same crop/tile-to-length every lane in this project
    already uses instead of edge fades (loop-safe-renders).

    ponytail: one resample ratio can't fix pitch AND tempo independently
    (that needs a phase vocoder). This corrects pitch — the thing
    "in-key" is actually promising — and lets duration drift by the same
    ratio, then crops/tiles the result. Good enough for picks chosen
    close in BPM by `in_key`'s ranking; if drift is ever audible on a
    real beat, upgrade to librosa/rubberband time-stretch instead of
    reaching for a bigger ratio here.
    """
    x = np.asarray(x, dtype=np.float64)
    ratio = 1.0
    if src_key is not None and dst_key is not None:
        ratio = 2.0 ** (dst_key.shift_from(src_key) / 12.0)
    if ratio != 1.0 and len(x):
        n = max(int(round(len(x) / ratio)), 1)
        idx = np.linspace(0, len(x) - 1, n)
        x = np.interp(idx, np.arange(len(x)), x)
    target = max(int(round(dst_secs * sr)), 1)
    if len(x) == 0:
        return np.zeros(target)
    if len(x) >= target:
        return x[:target].copy()
    reps = target // len(x) + 1
    return np.tile(x, reps)[:target]


def chop_onsets(x, sr, min_dur=0.15, max_dur=2.0):
    """Slice a loop into its individual note/chord hits — a fast (10ms)
    envelope crossing well above its own trailing 200ms average, i.e.
    "louder than it's been lately" rather than "loud in absolute
    terms". A global level threshold breaks on a loop that's mostly
    loud throughout (a held chord, a sustained pad); comparing against
    a local trailing floor instead catches the attack regardless of
    how the rest of the file sits. No new dependency — same rectify-
    and-smooth idea as make_drum_loops.env. Each clip gets a 5ms
    fade-out so the chop is click-free.

    This is what makes a kind="loop" melodic file usable as a one-shot:
    fit_loop corrects pitch by resample but can't stretch tempo
    independently, so tiling a whole rhythmic loop to an arbitrary
    chord duration risks drifting against the beat grid (see
    chord_synth.sample_pool) — but a single chopped-out hit carries no
    tempo of its own, so that ceiling never applies to one.
    """
    mono = x.mean(axis=1) if x.ndim == 2 else x
    n = len(mono)
    if n == 0:
        return []
    fast_win = max(int(0.01 * sr), 1)                   # 10ms attack track
    slow_win = max(int(0.2 * sr), 1)                     # 200ms trailing floor
    fast = np.convolve(np.abs(mono), np.ones(fast_win) / fast_win, mode="same")
    cum = np.concatenate(([0.0], np.cumsum(fast)))
    idx = np.arange(n)
    lo = np.maximum(idx - slow_win, 0)
    floor = (cum[idx] - cum[lo]) / np.maximum(idx - lo, 1)
    # the relative-floor check alone fires on convolution leakage at a
    # silence->sound boundary (a few samples of near-zero "rise" before
    # the real attack); require the level to also clear a noise gate
    # relative to the file's own loudest point.
    gate = 0.05 * (fast.max() if n else 0.0)
    rising = (fast > floor * 1.8) & (fast > gate)
    onset_frames = np.where(rising & ~np.concatenate(([False], rising[:-1])))[0]
    min_gap = int(min_dur * sr)
    onsets = []
    for f in onset_frames:
        if not onsets or f - onsets[-1] >= min_gap:
            onsets.append(int(f))
    if not onsets:
        onsets = [0]
    clips = []
    for i, start in enumerate(onsets):
        end = onsets[i + 1] if i + 1 < len(onsets) else n
        end = min(end, start + int(max_dur * sr))
        clip = mono[start:end]
        if len(clip) < min_gap:
            continue
        fade = min(int(0.005 * sr), len(clip) // 4)
        if fade:
            clip = clip.copy()
            clip[-fade:] *= np.linspace(1, 0, fade)
        clips.append(clip)
    return clips


def _report():
    index = scan()
    if not index:
        print("No key-labeled melodic loops found. Is the sample drive "
              "plugged in?")
        return
    print("%d key-labeled melodic files across the pack roots\n" % len(index))
    roles = {}
    for e in index:
        roles[e["role"]] = roles.get(e["role"], 0) + 1
    for role in sorted(roles, key=lambda r: -roles[r]):
        print("  %-8s %4d" % (role, roles[role]))
    timed = sum(1 for e in index if e["bpm"] is not None)
    print("\n%d/%d carry a bpm tag too" % (timed, len(index)))


if __name__ == "__main__":
    _report()
