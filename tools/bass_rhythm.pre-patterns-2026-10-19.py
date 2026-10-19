"""The bass PERFORMANCE grammar (owner build 2026-10-19).

Why this exists. Until today the sampled bass line (bass0..N) played ONE
note per chord slot: the chord root, struck on the slot's first bar and
held. No rhythm, no lock with the kick, no passing notes, no ghosts, no
swing. chord_rhythm.py (2026-09-05) gave the chords a performance; this
gives the bass one: per-identity figures (kick-locked, root-fifth,
octave, walking with a chromatic approach, push/anticipation, funk with
ghost notes, 8th-note pulse, and the old hold kept as one option).

How it is played. The WHOLE line is rendered as one loop-length,
loop-safe buffer (chord_synth.add_wrapped), then beat_machine cuts it at
the chord-slot boundaries into the existing bass{i} lanes. Cutting one
continuous line, instead of rendering slot by slot, is what lets a pushed
note ring across a chord change and the loop point without a gap. Each
lane keeps a single X on its slot's first bar (a chord lane's X triggers
its whole buffer -- see chord_rhythm's header), so the rack, trims and
rebuilds see the same lanes they always did.

Rules carried over:
- levels come only from the WRITTEN character via groove.velocity
  (X accent, x normal, o soft, . ghost) -- no random wobble (2026-08-03);
- one bass note at a time: each note runs to the next hit (legato);
- his own bass file only, never a synthesized tone (2026-07-25);
- feel = the KICK lane's (offset, swing; jitter capped at 4 ms) so bass
  and kick move as one unit, the way the 808 branch already copies it.

New beats only: add_bass_and_chords stamps `bass_flow`; a preset without
it (every older beat, every rebuild of one) never reaches this module.
The figure weights per chord family are Claude's creative choices under
the owner's 2026-10-19 creative-control grant, not sourced numbers --
tune them by ear.
"""
from __future__ import annotations

import random

import numpy as np

import chord_synth
import groove
from pattern_gen import _weighted

FLOW_VERSION = 1

FIGURES = ("hold", "kick", "fifth", "octave", "walk", "push", "funk",
           "pulse")

# Figure weights per signature.chord_family (Claude's starting point).
FAMILY = {
    "soul_jazz": [["walk", 3], ["kick", 2], ["fifth", 2], ["push", 2],
                  ["hold", 1]],
    "dark": [["hold", 3], ["kick", 3], ["push", 1], ["pulse", 1]],
    "grit": [["kick", 4], ["push", 2], ["fifth", 1], ["hold", 1],
             ["octave", 1]],
    "dreamy": [["hold", 3], ["push", 2], ["fifth", 2], ["walk", 1]],
    "bright_funk": [["funk", 3], ["octave", 3], ["kick", 2], ["push", 1]],
}
DEFAULT = [["kick", 3], ["hold", 2], ["fifth", 2], ["push", 1]]

FUNK_CELLS = (3, 6, 7, 10, 11, 14)
GHOST_LEN = 0.5          # a ghost / dead note, in 16ths
MAX_JIT_MS = 4.0
NO_KICK = "X-------x-------"   # what "kick" locks to when there is no kick


def spec_for(preset):
    """The figure weights this beat's bass rolls from.
    `signature.bass_grammar` ({"figures": [[name, w], ...]}) wins; else the
    identity's chord_family; else the house DEFAULT."""
    sig = preset.get("signature") or {}
    own = sig.get("bass_grammar")
    if isinstance(own, dict) and own.get("figures"):
        figs = own["figures"]
    else:
        figs = FAMILY.get(sig.get("chord_family"), DEFAULT)
    return {"figures": [[f, w] for f, w in figs if f in FIGURES and w > 0]
            or DEFAULT}


def _pick(fits, *cands):
    """The first candidate pitch the bass file can reach; the last one
    (always the root) otherwise."""
    for n in cands:
        if fits(n):
            return n
    return cands[-1]


def _kick_bar(kick_bars, bar):
    if kick_bars:
        kb = kick_bars[bar % len(kick_bars)]
        if isinstance(kb, str) and len(kb) == 16:
            return kb
    return NO_KICK


def _figure_hits(fig, s, kick_bars, scale, rng, fits):
    """One slot's hits as [(bar, step, char, note)], bar relative to the
    slot. Step 0 of bar 0 is always the root, struck 'X'."""
    root, nb = s["root"], s["bars"]
    octave = _pick(fits, root + 12, root)
    fifth = _pick(fits, root + 7, root - 5, root)
    ivs = sorted({(t - s["chord_root"]) % 12 for t in s["tones"]} - {0})
    tones = [_pick(fits, root + i, root + i - 12, root) for i in ivs] or [
        fifth]
    up = sorted((pc - root) % 12 for pc in scale if (pc - root) % 12)
    step_up = _pick(fits, root + up[0], root) if up else fifth
    hits = []
    for b in range(nb):
        first = "X" if b == 0 else "x"
        if fig == "hold":
            hits.append((b, 0, "X" if b == 0 else "o", root))
        elif fig == "push":
            hits.append((b, 0, "X" if b == 0 else "o", root))
            if nb >= 2 and b % 2 == 1 and rng.random() < 0.5:
                hits.append((b, 8, "x", root))
        elif fig == "fifth":
            hits.append((b, 0, first, root))
            hits.append((b, 8, "x", fifth))
        elif fig == "kick":
            kb = _kick_bar(kick_bars, s["start_bar"] + b)
            last = -9
            for st, ch in enumerate(kb):
                if st == 0 and b == 0:
                    hits.append((b, 0, "X", root))
                    last = 0
                    continue
                if ch not in "Xx" or st - last < 2:
                    continue
                r = rng.random()
                note = octave if r < 0.15 else fifth if r < 0.27 else root
                hits.append((b, st, "x", root if st == 0 else note))
                last = st
        elif fig == "octave":
            for st in range(0, 16, 2):
                if st and rng.random() < 0.2:
                    continue
                ch = (first if st == 0 else "X" if st == 8 else "x")
                hits.append((b, st, ch, root if st % 4 == 0 else octave))
        elif fig == "pulse":
            for st in range(0, 16, 2):
                if st % 4 and rng.random() < 0.1:
                    continue
                ch = first if st == 0 else "x" if st % 4 == 0 else "."
                hits.append((b, st, ch, root))
        elif fig == "walk":
            hits.append((b, 0, first, root))
            for st in (4, 8, 12):
                note = (rng.choice(tones) if rng.random() < 0.7
                        else step_up)
                hits.append((b, st, "x", note))
        elif fig == "funk":
            hits.append((b, 0, "X", root))
            cells = []
            for c in rng.sample(FUNK_CELLS, len(FUNK_CELLS)):
                if len(cells) >= rng.randint(2, 4):
                    break
                if all(abs(c - k) >= 2 for k in cells):
                    cells.append(c)
            for c in sorted(cells):
                if rng.random() < 0.35:
                    hits.append((b, c, ".", root))
                else:
                    r = rng.random()
                    note = octave if r < 0.3 else fifth if r < 0.4 else root
                    hits.append((b, c, "x", note))
    return hits


def plan_line(slots, kick_bars, spec, variant, fits, scale=()):
    """Pure planning pass: one figure per chord slot, then the cross-slot
    moves (walk's chromatic approach, push's tie into the next chord).

    `slots`: [{"root", "chord_root", "tones", "bars", "start_bar"}] in
    play order -- root is the bass-register root, tones the chord's MIDI
    notes, chord_root its own root. `kick_bars`: the kick lane's 16-char
    bar strings (or None). `fits(note)`: can the bass file reach it.
    `scale`: the key's pitch classes (walk's scale steps).

    Returns [{"figure", "tied", "hits": [(bar, step, char, note)]}]; the
    last slot's approach/push targets slot 0 (the loop wraps)."""
    plan = []
    for i, s in enumerate(slots):
        rng = random.Random(variant * 887 + 31 + i)
        fig = _weighted(rng, spec["figures"])
        plan.append({"figure": fig, "tied": False,
                     "hits": _figure_hits(fig, s, kick_bars, scale, rng,
                                          fits)})
    n = len(slots)
    for i, (s, p) in enumerate(zip(slots, plan)):
        nxt = slots[(i + 1) % n]["root"]
        last = s["bars"] - 1
        rng = random.Random(variant * 887 + 977 + i)
        if p["figure"] == "walk":
            hits = [h for h in p["hits"] if (h[0], h[1]) != (last, 12)]
            prev = max((h for h in hits if h[0] == last), default=None,
                       key=lambda h: h[1])
            below = prev is None or prev[3] < nxt
            a = _pick(fits, *((nxt - 1, nxt + 1) if below
                              else (nxt + 1, nxt - 1)), nxt - 1)
            p["hits"] = hits + [(last, 12, "x", a)]
        elif p["figure"] == "push":
            st = rng.choice((14, 15))
            p["hits"] = [h for h in p["hits"]
                         if not (h[0] == last and h[1] >= 13)]
            p["hits"].append((last, st, "x", nxt))
            q = plan[(i + 1) % n]
            q["tied"] = True
            q["hits"] = [h for h in q["hits"] if (h[0], h[1]) != (0, 0)]
    for p in plan:
        p["hits"].sort(key=lambda h: (h[0], h[1]))
    return plan


def render_line(plan, slots, bar_s, bpm, loop_n, render_note, feel,
                sr=chord_synth.SR):
    """Play a planned line into one loop-length (`loop_n` samples),
    loop-safe buffer. Every note runs to the next hit (one note at a
    time); a ghost is half a 16th. `render_note(note, secs)` voices one
    note from his bass file, or None.

    Returns (audio, notes) -- notes = per slot [(start_s, dur_s, note,
    level)] for the MIDI export -- or (None, None) if a note can't be
    voiced even as its slot's root, so the caller keeps the old line."""
    loop_s = loop_n / float(sr)
    six = bar_s / 16.0
    evs = []
    for i, (s, p) in enumerate(zip(slots, plan)):
        for b, st, ch, note in p["hits"]:
            t = feel.hit_time((s["start_bar"] + b) * bar_s, st, bpm) % loop_s
            evs.append((t, i, st, ch, note))
    if not evs:
        return None, None
    evs.sort(key=lambda e: e[0])
    out = np.zeros(loop_n)
    notes = [[] for _ in slots]
    for k, (t, i, st, ch, note) in enumerate(evs):
        nt = evs[(k + 1) % len(evs)][0]
        gap = (nt - t) % loop_s or loop_s
        dur = min(gap, GHOST_LEN * six) if ch == "." else gap
        dur = max(dur, 0.02)
        lvl = groove.velocity(ch, st, None)
        seg = render_note(note, dur)
        if seg is None:
            note = slots[i]["root"]
            seg = render_note(note, dur)
            if seg is None:
                return None, None
        chord_synth.add_wrapped(out, seg * lvl, int(round(t * sr)))
        notes[i].append((t, dur, note, lvl))
    return out, notes


def kick_feel(lanes, seed):
    """The bass's LaneFeel: the kick lane's offset and swing, jitter
    capped. No kick lane -> straight with a little life."""
    k = (lanes or {}).get("kick")
    if k:
        _p, _g, (off, jit, swing, _s), _bars = k
        return groove.LaneFeel(off, min(jit, MAX_JIT_MS), swing, seed=seed)
    return groove.LaneFeel(0, 2, 50, seed=seed)
