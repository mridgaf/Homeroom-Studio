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

FLOW_VERSION = 2          # 2 = the "pattern" figure (bass_patterns.json)

FIGURES = ("hold", "kick", "fifth", "octave", "walk", "push", "funk",
           "pulse", "pattern")

# Share of chord slots that play a library pattern on a flow-2 beat.
# Claude's starting point (owner 2026-10-19 asked for 100 new bass
# patterns); tune by ear. A bass_grammar that names "pattern" itself wins.
PATTERN_P = 0.5

# Which pattern tags each chord family leans toward (a tag not named = 1).
PATTERN_TAGS = {
    "soul_jazz": {"walk": 4, "fifth": 2, "push": 2},
    "dark": {"sparse": 4, "root": 3, "pulse": 1},
    "grit": {"sync": 4, "kick": 3, "ghost": 2},
    "dreamy": {"sparse": 3, "push": 3, "long": 2, "fifth": 2},
    "bright_funk": {"funk": 4, "octave": 3, "ghost": 2, "bounce": 2},
}

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
    figs = [[f, w] for f, w in figs if f in FIGURES and w > 0] or DEFAULT
    flow = int(preset.get("bass_flow") or 1)
    if flow >= 2 and library() and not any(f == "pattern" for f, _w in figs):
        total = float(sum(w for _f, w in figs))
        figs = figs + [["pattern", total * PATTERN_P / (1 - PATTERN_P)]]
    elif flow < 2:
        figs = [[f, w] for f, w in figs if f != "pattern"] or DEFAULT
    return {"figures": figs,
            "tags": PATTERN_TAGS.get(sig.get("chord_family"), {})}


_LIB = None


def library():
    """The bass pattern library (bass_patterns.json at the project root).
    Each entry: `bars` (when a note hits) and `roles` (which note), 1-4
    bars of 16 steps. Missing or broken file -> [] and the plain figures
    play."""
    global _LIB
    if _LIB is None:
        import json
        import os
        out = []
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "bass_patterns.json")
            with open(path, encoding="utf-8") as f:
                for e in json.load(f).get("patterns", []):
                    bars, roles = e.get("bars"), e.get("roles")
                    if (isinstance(bars, list) and isinstance(roles, list)
                            and 1 <= len(bars) <= 4
                            and len(bars) == len(roles)
                            and all(isinstance(b, str) and len(b) == 16
                                    and set(b) <= set("Xxo.-")
                                    for b in bars)
                            and all(isinstance(r, str) and len(r) == 16
                                    and set(r) <= set(ROLES + "-")
                                    for r in roles)
                            and all((b[i] == "-") == (r[i] == "-")
                                    for b, r in zip(bars, roles)
                                    for i in range(16))):
                        out.append({"name": e.get("name", "?"),
                                    "tags": list(e.get("tags", [])),
                                    "bars": bars, "roles": roles})
        except (OSError, ValueError):
            out = []
        _LIB = out
    return _LIB


ROLES = "R5L83" + "7udan"


def _pick_entry(lib, rng, tag_w):
    """One library entry, leaning toward the family's tags."""
    wts = [max([float(tag_w.get(t, 1)) for t in e["tags"]] or [1.0])
           for e in lib]
    return rng.choices(lib, weights=wts)[0]


def _pattern_hits(entry, s, scale_up, scale_dn, tones, fits):
    """One slot's hits from a library entry. `a` (approach) and `n` (next
    root) come back as the letter and are resolved in plan_line, where the
    next chord is known. A role the file can't reach plays the root."""
    root, nb = s["root"], s["bars"]
    octave = _pick(fits, root + 12, root)
    fifth = _pick(fits, root + 7, root - 5, root)
    low5 = _pick(fits, root - 5, root + 7, root)
    third = _pick(fits, *([root + i for i in tones if i in (3, 4)]
                          + [root + 7, root]))
    sev = _pick(fits, *([root + i for i in tones if i in (10, 11)]
                        + [root + 7, root]))
    up = _pick(fits, root + scale_up, root) if scale_up else fifth
    dn = _pick(fits, root + scale_dn, root) if scale_dn else low5
    notes = {"R": root, "5": fifth, "L": low5, "8": octave, "3": third,
             "7": sev, "u": up, "d": dn, "a": "a", "n": "n"}
    hits = []
    for b in range(nb):
        # the slot's last bar plays the entry's last bar, so a pattern's
        # turnaround (approach / early next root) lands on the chord change
        k = (len(entry["bars"]) - 1 if b == nb - 1 and nb > 1
             else b % len(entry["bars"]))
        for st, (ch, role) in enumerate(zip(entry["bars"][k],
                                            entry["roles"][k])):
            if ch != "-":
                hits.append((b, st, ch, notes[role]))
    return hits


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


def _figure_hits(fig, s, kick_bars, scale, rng, fits, tag_w=None):
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
    if fig == "pattern":
        lib = library()
        if lib:
            down = sorted((pc - root) % 12 for pc in scale if (pc - root) % 12)
            return _pattern_hits(
                _pick_entry(lib, rng, tag_w or {}), s,
                up[0] if up else 0, (down[-1] - 12) if down else 0, ivs,
                fits)
        fig = "kick"                      # no library: the kick lock
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
                                          fits, spec.get("tags"))})
    n = len(slots)
    for i, (s, p) in enumerate(zip(slots, plan)):
        nxt = slots[(i + 1) % n]["root"]
        last = s["bars"] - 1
        rng = random.Random(variant * 887 + 977 + i)
        if p["figure"] == "pattern":
            # resolve the cross-slot roles: `a` slides in from the side
            # the line is coming from, `n` is the next root played early
            fixed = []
            for h in p["hits"]:
                if h[3] == "n":
                    h = (h[0], h[1], h[2], nxt)
                elif h[3] == "a":
                    prev = max((x for x in fixed if isinstance(x[3], int)),
                               default=None, key=lambda x: (x[0], x[1]))
                    below = prev is None or prev[3] < nxt
                    h = (h[0], h[1], h[2], _pick(
                        fits, *((nxt - 1, nxt + 1) if below
                                else (nxt + 1, nxt - 1)), nxt - 1))
                fixed.append(h)
            p["hits"] = fixed
        elif p["figure"] == "walk":
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
