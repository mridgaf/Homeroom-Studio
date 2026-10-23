"""Backing vocals for G-Funk (owner 2026-10-23: "wire them as a G-Funk-only
layer" -- female backing vocals, from vocal loops already in the sound bank).

Why a module of its own: melodic_loops.scan() throws every `vocal` loop away
(a vocal is not a chord voice), so nothing in the engine could reach
BOTC Sorted Loops/Vocals. This reads that folder, keeps only the sung
female/choir "ooh/aah" loops, and renders ONE loop-length buffer that
beat_machine._build_chords lays on lane melody1 (the same shape as the
answer melody, melody0).

It is opt-in per identity: signature["backing_vox"] = {"p": chance a beat
gets it, "under_db": how far under the chords' peak}. Only G-Funk has it.
The owner's 2026-08-01 "kill the vocal hits" rule is about one-shot hits
(VOX_LANE_P); this is a held, quiet bed, and he chose it for G-Funk.

Real samples only. Pitch is a resample (like fit_loop), then the tempo is
time-stretched back so the phrase sits on the beat's grid.
"""
from __future__ import annotations

import random
from pathlib import Path

import numpy as np

import melodic_loops as ml
from key_context import KeyContext
from sample_library import load_loop_roots

# a sung female / choir pad, by name. Everything else in Vocals (chops,
# percussion, scratches, industrial mouths, stabs) stays out.
WORDS_IN = ("FEMALE", "CHOIR", "AHH", "OOH", "ANGELIC")
WORDS_OUT = ("STAB", "CHOP", "SCRATCH", "PERCUSSION", "DUBSTEP",
             "INDUSTRIAL", "WAIL", "NOKEY", "SCARY", "EVIL", "DARK",
             "GREGORIAN", "ETHNIC", "DRILL")
MAX_TEMPO_RATIO = 1.25          # stretch no more than 25% either way
MAX_SHIFT = 3                   # semitones of pitch move (voices go chipmunk past this)
_cache = None


def _vocal_dirs():
    out = []
    for root in load_loop_roots():
        r = Path(root).expanduser()
        if not r.exists():
            continue
        if r.name.lower().startswith("vocal"):
            out.append(r)
        else:
            out.extend(sorted(d for d in r.glob("Vocal*") if d.is_dir()))
    return out


def _wanted(tokens):
    up = " ".join(tokens).upper()
    return (any(w in up for w in WORDS_IN)
            and not any(w in up for w in WORDS_OUT))


def scan(refresh=False):
    """[{name, path, key, mode, bpm}] for the sung female/choir loops that
    name BOTH a key and a tempo. Empty when the drive is unplugged."""
    global _cache
    if _cache is not None and not refresh:
        return _cache
    found = []
    for d in _vocal_dirs():
        for p in sorted(d.rglob("*")):
            if p.suffix.lower() not in (".wav", ".aif", ".aiff", ".flac") \
                    or not p.is_file():
                continue
            tokens = ml._tokens(p, d)
            if not _wanted(tokens) or ml.is_full_mix(tokens):
                continue
            key = ml.key_from_tokens(tokens) or ml.label_key_from_tokens(tokens)
            bpm = ml.bpm_from_tokens(tokens)
            if not key or not key[0] or not bpm:
                continue
            found.append({"name": p.stem, "path": str(p), "key": key[0],
                          "mode": key[1], "bpm": bpm})
    _cache = found
    return found


def _shift(entry, key):
    """Semitones to move this loop into `key` (same call fit_loop makes)."""
    return key.shift_from(KeyContext(entry["key"], entry["mode"] or key.mode))


def candidates(index, key, bpm):
    """Loops that can reach this beat: pitch move <= MAX_SHIFT semitones and
    tempo within MAX_TEMPO_RATIO after that move. Closest first."""
    out = []
    for e in index:
        semis = _shift(e, key)
        if abs(semis) > MAX_SHIFT:
            continue
        eff = e["bpm"] * 2.0 ** (semis / 12.0)     # the resample moves tempo
        ratio = bpm / eff
        if not (1 / MAX_TEMPO_RATIO <= ratio <= MAX_TEMPO_RATIO):
            continue
        out.append((abs(semis) + abs(1 - ratio) * 10, e["name"], e))
    return [e for _, _, e in sorted(out, key=lambda t: t[:2])]


def pick(index, key, bpm, variant):
    """One loop for this beat, deterministic per variant; None if none fit."""
    c = candidates(index, key, bpm)
    return random.Random(variant * 1741 + 29).choice(c[:3]) if c else None


def render(entry, key, bpm, dst_secs, sr):
    """Mono buffer of exactly dst_secs, in `key`, on `bpm`'s grid, or None."""
    from chord_synth import load_audio, norm_rms
    from instrument_sampler import _declick
    x = load_audio(entry["path"])
    if x is None or not len(x):
        return None
    x = np.asarray(x.mean(axis=1) if x.ndim == 2 else x, dtype=np.float64)
    semis = _shift(entry, key)
    ratio = 2.0 ** (semis / 12.0)
    if ratio != 1.0:
        n = max(int(round(len(x) / ratio)), 1)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    stretch = bpm / (entry["bpm"] * ratio)           # >1 = faster
    if abs(stretch - 1.0) > 0.002:
        import pedalboard
        x = pedalboard.time_stretch(
            np.ascontiguousarray(x[None, :], dtype=np.float32), sr,
            stretch_factor=float(stretch))[0].astype(np.float64)
    x = ml.fit_loop(x, sr, dst_secs)                 # tile/crop to length
    if not np.any(x):
        return None
    return _declick(norm_rms(x, -18.0), sr)
