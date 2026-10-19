"""ALTERNATE BASS SOUNDS (owner build 2026-10-19).

Until today the bass line could only play files from his "Bass" folder.
Owner 2026-10-19: also try the orchestral bass and cello (London Symphonic
Strings), and let piano, guitar, organ and synth play bass "if they have
the notes capable". This picks that one sound for a beat.

Rules carried over:
- ONE bass sound per beat (hard rule 2026-09-23): one kind, one
  instrument, one playing style. Every note of the line comes from it.
- his own samples only, never a synthesized tone (2026-07-25). If nothing
  of the rolled kind can reach the line, the beat keeps the Bass folder.
- "have the notes capable": every root of the line must sit within REACH
  semitones of a real recording (the line may move by whole octaves to
  meet the instrument, the way the Bass folder's line already does). A
  one-shot with a single recorded pitch therefore only qualifies when the
  whole line sits within REACH of it -- a note-by-note library qualifies
  across its range.
- deterministic from the variant, so a rebuild plays the same sound.

New beats only: add_bass_and_chords stamps `bass_voice_flow`. The kind
weights are Claude's starting point (not sourced) -- tune by ear, or set
`signature.bass_voices` ({kind: weight}) on one identity.
"""
from __future__ import annotations

import random

import numpy as np

import instrument_sampler as ins

# kind -> weight. "bass" = keep his Bass folder (the house sound).
WEIGHTS = {"bass": 4, "contrabass": 3, "cello": 2, "piano": 1, "guitar": 1,
           "organ": 1, "synth": 1}
REACH = 4                 # semitones a note may be stretched from a recording
LOW_LIMIT = 27            # no bass line below this after octave moves
CENTER = 41               # where the default line sits: moves aim here
OCTAVES = (0, -12, 12, -24, 24)
STRING_KIND = {"contrabass": "basses", "cello": "cello"}
STRING_STYLES = {"pizz": 4, "sustain": 3, "short": 2}
LABEL = {"basses": "orchestral bass", "cello": "cello"}


def _reach(entries, notes, reach=REACH):
    return all(any(abs(e["note"] - n) <= reach for e in entries)
               for n in notes)


def _place(entries, roots, reach=REACH):
    """The whole-octave move (or None) that puts every root within `reach`
    of a recording, nearest to where the default line sits."""
    best = None
    for k in OCTAVES:
        line = [r + k for r in roots]
        if min(line) < LOW_LIMIT or not _reach(entries, line, reach):
            continue
        d = abs(sum(line) / float(len(line)) - CENTER)
        if best is None or d < best[0]:
            best = (d, k)
    return None if best is None else best[1]


def _string_voice(kind, strings, roots, rng):
    import string_sampler as ss
    fam = STRING_KIND[kind]
    mine = [e for e in strings if e.get("instrument") == fam]
    styles = [s for s in STRING_STYLES if any(e["style"] == s for e in mine)]
    order = []
    pool = {s: float(STRING_STYLES[s]) for s in styles}
    while pool:                                   # weighted order, no repeats
        s = rng.choices(list(pool), weights=list(pool.values()))[0]
        order.append(s)
        pool.pop(s)
    for style in order:
        ents = [e for e in mine if e["style"] == style]
        ents = [e for e in ents if e.get("mic") == ss.CLOSE] or ents
        k = _place(ents, roots)
        if k is None:
            continue
        held = style not in ss.SHORT_STYLES

        def make_render(cache, used, snap_sec, ents=ents, held=held):
            def render(n, secs):
                key = ("s", n)
                if cache is not None and key in cache:
                    mono = cache[key]
                else:
                    pk = ss.nearest(ents, n)
                    if pk is None:
                        return None
                    if used is not None:
                        used.append(pk["path"])
                    mono = ss._voice(pk, n)
                    if cache is not None:
                        cache[key] = mono
                if mono is None or not len(mono):
                    return None
                m = max(int(secs * ins.SR), 1)
                if held:       # a bowed note: crossfaded repeats to length
                    seg = ins._fit_length(mono, m, ins.SR, snap_sec=snap_sec)
                else:          # a plucked note rings out, then silence
                    seg = np.zeros(m)
                    seg[:min(m, len(mono))] = mono[:m]
                return ins._declick(np.asarray(seg, dtype=float), ins.SR)
            return render
        return {"kind": kind, "label": "%s (%s)" % (LABEL[fam], style),
                "oct": k, "make_render": make_render,
                "fits": lambda n, ents=ents: any(
                    abs(e["note"] - n) <= REACH for e in ents)}
    return None


def _instrument_voice(kind, index, roots, rng):
    import melody_rhythm as mr
    groups = {"piano": ("piano",), "guitar": ("guitar",),
              "organ": ("organ",), "synth": ("synth",)}[kind]
    found = mr._instruments(index, groups)
    ok = []
    for key, ents in sorted(found.items(), key=lambda kv: str(kv[0])):
        k = _place(ents, roots)
        if k is not None:
            ok.append((key, ents, k))
    if not ok:
        return None
    multi = [o for o in ok if o[0][0] == "multi"]     # note-by-note first
    key, ents, k = rng.choice(multi or ok)

    def make_render(cache, used, snap_sec, ents=ents):
        return lambda n, secs: ins.voice_note(
            ents, n, secs, cache=cache, used=used, snap_sec=snap_sec)
    return {"kind": kind, "label": kind, "oct": k,
            "make_render": make_render,
            "fits": lambda n, ents=ents: any(
                abs(e["note"] - n) <= REACH for e in ents)}


def choose(variant, roots, preset, strings=None, instruments=None,
           cache=None, weights=None):
    """The alternate bass sound for this beat, or None (keep the Bass
    folder). `roots`: the bass-register root of each chord slot. `strings`
    / `instruments`: the string_sampler / instrument_sampler indexes, or a
    zero-argument function that returns one (only called if the rolled
    kind needs it). `cache`: the beat's bass audio cache (shared, so the
    check below doesn't load a file twice).

    Returns {"kind", "label", "oct", "fits", "make_render"}; make_render(
    cache, used, snap_sec) -> render(note, seconds) -> audio or None.
    A voice that can't actually voice every root is dropped here, so the
    beat never ends up with no bass lane."""
    rng = random.Random(variant * 617 + 13)
    w = dict(WEIGHTS)
    own = (preset.get("signature") or {}).get("bass_voices")
    if isinstance(own, dict):
        w.update({k: float(v) for k, v in own.items() if k in WEIGHTS})
    w = {k: v for k, v in w.items() if v > 0}
    if not w or not roots:
        return None
    kind = rng.choices(list(w), weights=list(w.values()))[0]
    if kind == "bass":
        return None

    def _get(src):
        return src() if callable(src) else (src or [])
    if kind in STRING_KIND:
        voice = _string_voice(kind, _get(strings), roots, rng)
    else:
        voice = _instrument_voice(kind, _get(instruments), roots, rng)
    if voice is None:
        return None
    render = voice["make_render"](cache if cache is not None else {}, [],
                                  None)
    # every root must actually voice (file present, drive mounted)
    if any(render(r + voice["oct"], 0.2) is None for r in roots):
        return None
    return voice
