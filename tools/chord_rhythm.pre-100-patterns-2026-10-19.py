"""The chord PERFORMANCE grammar (owner build 2026-09-05).

Why this exists. The drums have had a real grammar for months — per-lane
16-cell step weights, hit counts, 14 backbeat modes, 13 timekeeper modes,
ghost cells, per-lane offset/jitter/swing — while the chords had ONE word,
`"arp"` or `"sustain"`, rolled once per beat. `arp` was a single fixed
figure (ascending, one note per eighth, forever, no rests, no seed) and
`sustain` was a held block. Nine of the twelve legends set no
`chord_rhythm` at all, so they were dead held pads. The `signature` block
chooses good NOTES; nothing chose how they were PLAYED. See DECISIONS.md
2026-09-05.

Where the rhythm has to live, and why it is not in the bar strings. A
drum lane's bar string is the rhythm: one char per 16th, and the render
loop triggers a one-shot per char. A chord lane's bar string is NOT —
`kit[lane]` holds the whole multi-bar slot as a single buffer and the
lane's lone `X` triggers it once. Putting more X's in a chord bar string
would retrigger the entire chord blob on top of itself, not play a stab.
So the figure is rendered INTO the slot buffer, exactly where arp_riff
always did it.

What IS reused, rather than rebuilt (the drum side already solved these):
- `pattern_gen._weighted` for every roll,
- written hit characters + `groove.velocity` for level,
- `groove.LaneFeel` for offset / jitter / MPC swing,
- `chord_synth.add_wrapped` / `finish_riff` for loop-safe placement.

OWNER RULE 2026-08-03 carried through: levels come from the WRITTEN
character (X accent, x normal, o softer re-attack, . ghost) and never
from a random wobble. `groove.velocity` already enforces that; this module
must not multiply anything on top of it.

Every DJ since 2026-09-14 (owner: the old arp is "repetitious and
boring"; he chose these rhythms for everyone, with arps half as often as
before). A DJ with no `chord_grammar` key gets the house DEFAULT figures,
its arp share set to half of what its old two-word `chord_rhythm` gave it.
Genre presets keep the opt-in: absent key -> None -> the old path.
"""
from __future__ import annotations

import numpy as np

import chord_synth
import groove
from pattern_gen import BEATS, _weighted

FIGURES = ("stab", "arp", "pad", "comp")
SHAPES = ("up", "down", "updown", "broken", "walk")

# Every key optional; this is what an identity that opts in with `true`
# rather than a dict gets. Weights lean to stabs because that is the sound
# the layer was most obviously missing.
DEFAULT = {
    "figures": [["stab", 3], ["comp", 2], ["arp", 2], ["pad", 1]],
    # 16 step weights. Front-loaded on the beats and the "and"s, the same
    # shape the kick maps use, so a figure lands musically before any
    # identity bothers to tune it.
    "w": [10, 1, 3, 2, 7, 1, 4, 2, 8, 1, 3, 2, 6, 1, 4, 3],
    "hits": [3, 6],          # per bar
    "shape": [["up", 3], ["updown", 2], ["broken", 2], ["down", 1],
              ["walk", 1]],
    "rest_p": 0.18,          # chance a repeat bar drops one of its hits
    "ghost_p": 0.25,         # chance a non-beat hit is written quiet
    "seg": 1.6,              # stab length, in 16th steps (>1 = legato)
    "arp_step": 2,           # 16ths per arp step (2 = eighths, as before)
    "swells": [1, 2],        # pad re-attacks per beat
    "feel": [0, 3, 50],      # offset_ms, jitter_ms, swing
    "pan": 0.0,
}


# Owner 2026-09-14: "1 but 50% less than now" — every DJ on this grammar,
# arps HALF as often as each one had them.
ARP_CUT = 0.5

# ARP FLOW (owner 2026-10-19, beats stamped `arp_flow`): "this consistent
# arpeggio thing in almost every beat". Arps capped at 15% of chords for
# every identity (owner pick; was up to 50%), and an arp no longer walks
# straight 8ths forever: each bar picks a written rhythm, and every second
# bar rests in its back half -- the phrase tail the answer melody and the
# rapper use (Hub ch.04 s.11). Repetition raises liking but wears out
# unless varied (Margulis 2014, Hub ch.04 part 3). The 3+3+2 cell is the
# medium-syncopation groove sweet spot (Witek 2014, Hub ch.04 s.8). Cell
# weights and the 50% keep are NOT sourced -- tune by ear.
ARP_MAX = 0.15
ARP_CELLS = (((0, 2, 4, 6, 8, 10, 12, 14), 2),     # straight 8ths
             ((0, 3, 6, 8, 11, 14), 3),             # 3+3+2, twice
             ((0, 4, 6, 8, 12), 2),                 # pulse
             ((0, 6, 8), 1))                        # sparse
ARP_KEEP_P = 0.5         # a bar keeps the last bar's cell (some repetition)
ARP_RING = 4             # 16ths: longest an arp note rings into a gap


def arp_bars(rng, nbars, rest_p):
    """Written arp bars for an arp_flow beat (see ARP_CELLS)."""
    bars, cell = [], None
    for b in range(nbars):
        if cell is None or rng.random() >= ARP_KEEP_P:
            cell = _weighted(rng, [[c, w] for c, w in ARP_CELLS])
        s = ["-"] * 16
        for c in cell:
            if b % 2 == 1 and c >= 8:
                continue                  # the phrase-tail hole
            if c and rng.random() < rest_p:
                continue
            s[c] = "X" if c in BEATS else "x"
        bars.append("".join(s))
    return bars


# COMP FLOW (owner 2026-10-19, beats stamped `comp_flow`): the stabs, chord
# parts and comp were "the same old" rhythms. Measured in the code: stab and
# comp drew from ONE library, the bar count restarted at every chord change
# (a 1-bar chord always played bar 1 of its pattern), nothing shaped the
# phrase, and every hit rang the same length. Now, on comp_flow beats:
# - bars count across the whole loop (`bar0`), not per chord;
# - bar 2 of each pair sometimes skips beat 1 (lands late);
# - phrase shape as the arps have it: every 2nd bar may rest in its back
#   half (Hub ch.04 s.11 phrase-tail room), every 4th bar pushes into the
#   next phrase on the "and" of 4 (anticipation, Hub ch.04 s.7);
# - comp gets its own words (COMP_CELLS), leaning away from the kick and
#   snare only (the hats cover every cell, so counting them hid nothing);
# - a hit rings to the next hit, capped at the pattern's hold, so short
#   and long chords mix (Hub ch.13 part 3: a loop's middle chords are
#   shorter and syncopated).
# Cell weights, COMP_HOLD, the 50%/35% keep / rest / late numbers are NOT
# sourced -- tune by ear.
COMP_CELLS = (((0, 6), 2),            # 1, and-of-2 (jazz Charleston; not Hub)
              ((6, 14), 2),           # off-beat jabs, no downbeat
              ((0, 3, 6), 2),         # 3+3+2 front half (tresillo, ch.04 s.7)
              ((2, 10), 1),           # "and" of 1 and 3, round the snare
              ((0, 10, 14), 2),       # land, then push (anticipation)
              ((0, 2, 6, 10), 1),     # straight syncopation (ch.13 part 3)
              ((0, 6, 10), 2),        # the same, one hit fewer
              ((3, 6, 11), 1),        # all anticipations, no downbeat
              ((8, 14), 1),           # back-half answer
              ((0, 11), 1))           # land, then a late jab
COMP_HOLD = 3            # 16ths: longest a comp hit rings
PUSH = 14                # the "and" of 4


def _kit_cells(busy):
    """Cells the kick and snare/clap hit (hats left out on purpose)."""
    return _busy_cells({k: v for k, v in (busy or {}).items()
                        if k.startswith(("kick", "snare", "clap"))})


def _phrase(bar, gb, rng):
    """Phrase shape on a written bar at loop bar `gb` (comp_flow)."""
    cells = list(bar)
    hits = [i for i, ch in enumerate(cells) if ch != "-"]
    if gb % 2 == 1 and any(h < 8 for h in hits) and rng.random() < 0.5:
        for h in hits:
            if h >= 8:
                cells[h] = "-"            # the phrase-tail hole
    hits = [i for i, ch in enumerate(cells) if ch != "-"]
    if gb % 2 == 1 and cells[0] != "-" and len(hits) > 1 \
            and rng.random() < 0.35:
        cells[0] = "-"                    # bar 2 lands late
    if gb % 4 == 3 and all(cells[c] == "-" for c in (PUSH - 1, PUSH, PUSH + 1)):
        cells[PUSH] = "x"                 # push into the next phrase
    return "".join(cells)


def comp_bars(rng, nbars, bar0, busy, rest_p):
    """Written comp bars for a comp_flow slot starting at loop bar `bar0`."""
    kc = _kit_cells(busy)
    pool = [[c, w / (1.0 + len(set(c) & kc))] for c, w in COMP_CELLS]
    bars, cell = [], None
    for b in range(nbars):
        if cell is None or rng.random() >= ARP_KEEP_P:
            cell = _weighted(rng, pool)
        s = ["-"] * 16
        for c in cell:
            if c and rng.random() < rest_p:
                continue
            s[c] = "X" if c in BEATS else "x"
        bar = "".join(s)
        if rng.random() < 0.5:
            bar = _bend(bar, rng)
        bars.append(_phrase(bar, bar0 + b, rng))
    return bars


def _share(weighted, name):
    total = sum(w for _, w in weighted)
    return sum(w for n, w in weighted if n == name) / total if total else 0.0


def _with_arp_share(figures, share):
    """`figures` with the arp weight set so arps are `share` of the rolls.
    The other figures keep their own weights."""
    rest = [[f, w] for f, w in figures if f != "arp" and w > 0]
    if not rest:                         # an all-arp list: borrow the rest
        rest = [[f, w] for f, w in DEFAULT["figures"] if f != "arp"]
    if share <= 0:
        return rest
    other = sum(w for _, w in rest)
    return rest + [["arp", round(other * share / (1.0 - share), 3)]]


def spec_for(preset, free=False):
    """The chord grammar this beat plays, or None for the old two-word path.

    `true` means "the house default"; a dict overrides only the keys it
    names. A DJ with no key gets DEFAULT, with its arp share taken from its
    own old `signature.chord_rhythm` ("arp" = all, "sustain" = none, a
    weighted list = its arp share). Either way the arp share is then cut to
    ARP_CUT of itself. `free` (pattern_gen.free_beat): the house DEFAULT,
    whatever the DJ's own settings. Genre presets without the key -> None,
    their opt-in unchanged."""
    raw = preset.get("chord_grammar")
    # Genres: opt-in only on beats made before chord flow (2026-09-26,
    # owner: all 18 genres were stuck on one held pad or one climbing arp).
    # A new genre beat plays the house figures unless its config says
    # `"chord_grammar": false`; an old one rebuilds exactly as it was.
    if not raw and preset.get("genre") and (
            raw is False or not preset.get("chord_flow")):
        return None
    spec = dict(DEFAULT)
    if isinstance(raw, dict) and not free:
        spec.update(raw)
    if free or raw:
        share = _share(spec["figures"], "arp")
    else:
        rhythm = (preset.get("signature") or {}).get("chord_rhythm")
        share = (_share(rhythm, "arp") if isinstance(rhythm, list)
                 else float(rhythm == "arp"))
    share *= ARP_CUT
    if preset.get("arp_flow"):
        share = min(share, ARP_MAX)
        spec["arp_flow"] = True
    if preset.get("comp_flow"):
        spec["comp_flow"] = True
    spec["figures"] = _with_arp_share(spec["figures"], share)
    # Pattern library (2026-10-11): new beats only, so every older beat
    # rebuilds exactly as it was made.
    if preset.get("chord_flow") and preset.get("chord_library", True):
        spec["library"] = True
        # Per-identity rhythm leanings (2026-10-19 deep pass) live in the
        # signature, not chord_grammar: setting chord_grammar would also
        # switch which arp share applies. A grammar's own tags still win.
        if not spec.get("pattern_tags"):
            spec["pattern_tags"] = ((preset.get("signature") or {})
                                    .get("pattern_tags"))
    return spec


_LIB = None


def library():
    """The chord pattern library (chord_patterns.json at the project root).
    Missing or broken file -> [] and the old stab roll runs instead."""
    global _LIB
    if _LIB is None:
        import json
        import os
        out = []
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "chord_patterns.json")
            with open(path, encoding="utf-8") as f:
                for e in json.load(f).get("patterns", []):
                    bars = [b for b in e.get("bars", [])
                            if isinstance(b, str) and len(b) == 16]
                    if bars and len(bars) == len(e.get("bars", [])):
                        out.append({"name": e.get("name", "?"),
                                    "tags": list(e.get("tags", [])),
                                    "hold": float(e.get("hold", 1.6)),
                                    "bars": bars})
        except (OSError, ValueError):
            out = []
        _LIB = out
    return _LIB


def _pick_pattern(lib, spec, rng, busy_cells, comp, near=None, avoid=()):
    """One library entry, weighted by the identity's `pattern_tags` (a tag
    it doesn't name counts 1). A comp figure leans away from entries that
    land on the drums' cells. `near` keeps a second entry's hold close to
    the first so one slot doesn't mix a held chord with a chop."""
    tags = spec.get("pattern_tags") or {}
    pool, wts = [], []
    for e in lib:
        if near is not None and abs(e["hold"] - near["hold"]) > 3:
            continue
        w = max([float(tags.get(t, 1)) for t in e["tags"]] or [1.0])
        if e["name"] in avoid:                    # used by a recent beat
            w *= 0.08
        if comp and busy_cells:
            hit = {i for b in e["bars"] for i, ch in enumerate(b) if ch != "-"}
            w = w / (1.0 + len(hit & busy_cells))
        pool.append(e)
        wts.append(w)
    if not pool:
        return near
    return rng.choices(pool, weights=wts)[0]


def _bend(bar, rng):
    """One small change to a written bar, so no two beats play a library
    pattern exactly alike: slide a hit one 16th, drop one, or add one on a
    free off-beat. Never touches step 0 or makes two hits adjacent."""
    hits = [i for i, ch in enumerate(bar) if ch != "-"]
    cells = list(bar)
    move = rng.choice(("slide", "slide", "drop", "add"))
    if move == "add" and len(hits) < 6:
        free = [c for c in range(1, 16)
                if cells[c] == "-" and all(abs(c - h) >= 2 for h in hits)]
        if free:
            cells[rng.choice(free)] = "x"
    elif move == "drop" and len(hits) > 2:
        k = rng.choice([h for h in hits if h != 0] or hits[1:])
        cells[k] = "-"
    elif move == "slide":
        movable = [h for h in hits if h != 0]
        k = rng.choice(movable) if movable else None
        if k is not None:
            to = k + rng.choice((-1, 1))
            others = [h for h in hits if h != k]
            if 1 <= to <= 15 and all(abs(to - h) >= 2 for h in others):
                cells[to], cells[k] = cells[k], "-"
    return "".join(cells)


def _library_bars(spec, rng, nbars, comp, busy, avoid=(), trace=None,
                  bar0=0):
    """A slot's bars from the library: two entries mixed in an A-B pattern,
    so no bar-run repeats the same bar. Returns (bars, hold) or None.
    comp_flow: bars count from the slot's loop bar `bar0`, with _phrase."""
    lib = library()
    if not lib:
        return None
    cells = _busy_cells(busy) if comp else set()
    a = _pick_pattern(lib, spec, rng, cells, comp, avoid=avoid)
    b = (_pick_pattern(lib, spec, rng, cells, comp, near=a, avoid=avoid)
         if rng.random() < 0.7 else a)
    if trace is not None:
        trace.extend([a["name"], b["name"]])
    rest_p = spec.get("rest_p", DEFAULT["rest_p"])
    bend_p = spec.get("bend_p", 0.5)
    flow = spec.get("comp_flow")
    bars = []
    for i in range(nbars):
        if flow:
            i += bar0
        e = a if (i // len(a["bars"])) % 2 == 0 else b
        if rng.random() < 0.25:                    # now and then, flip
            e = b if e is a else a
        bar = e["bars"][i % len(e["bars"])]
        if rng.random() < bend_p:
            bar = _bend(bar, rng)
        if i != (bar0 if flow else 0) and rng.random() < rest_p:  # drop one
            idx = [k for k, ch in enumerate(bar) if ch in "xo."]
            if idx:
                k = rng.choice(idx)
                bar = bar[:k] + "-" + bar[k + 1:]
        bars.append(_phrase(bar, i, rng) if flow else bar)
    return bars, a["hold"]


def _cells(w, lo, hi, rng, avoid=()):
    """Pick between lo and hi step cells by weight, never two adjacent —
    the same rejection gen_kick uses, for the same reason: two hits a 16th
    apart read as a flam, not as two hits."""
    w = list(w)
    for c in avoid:
        w[c] = w[c] * 0.15                # discouraged, not forbidden
    hits = set()
    target = rng.randint(lo, hi)
    for _ in range(60):
        if len(hits) >= target:
            break
        s = rng.choices(range(16), weights=w)[0]
        if s in hits or (s - 1 in hits) or (s + 1 in hits):
            continue
        hits.add(s)
    return hits


def _write(hits, rng, ghost_p):
    """Hit cells -> a written bar. Beats accent, off-beats normal, and
    some off-beats drop to a ghost. Characters only — the level itself is
    groove.velocity's business, not ours."""
    out = []
    for i in range(16):
        if i not in hits:
            out.append("-")
        elif i in BEATS:
            out.append("X")
        elif rng.random() < ghost_p:
            out.append(".")
        else:
            out.append("x")
    return "".join(out)


def _busy_cells(busy):
    """Which 16ths the drums already occupy, across all their bars."""
    cells = set()
    for bars in (busy or {}).values():
        for bar in bars:
            for i, ch in enumerate(bar[:16]):
                if ch not in "-":
                    cells.add(i)
    return cells


def gen_figure(spec, rng, nbars, busy=None, avoid=(), trace=None, bar0=0):
    """Roll one figure for one chord slot.

    Returns `(figure, bars, shape)` — `bars` is one written 16-char string
    per bar of the slot, `shape` is the arp note order (None otherwise).
    Bars are re-rolled per bar so a four-bar slot isn't the same bar four
    times, which is the fault the drum grammar's per-bar composition fixed
    and the chord layer never had.
    """
    figure = _weighted(rng, spec.get("figures", DEFAULT["figures"]))
    w = spec.get("w", DEFAULT["w"])
    lo, hi = spec.get("hits", DEFAULT["hits"])
    ghost_p = spec.get("ghost_p", DEFAULT["ghost_p"])
    rest_p = spec.get("rest_p", DEFAULT["rest_p"])
    nbars = max(int(nbars), 1)
    shape = None

    if figure == "pad":
        # The old held block, but breathing: bar 1 lands the chord, and a
        # rolled number of softer re-attacks land on later beats. This is
        # the figure the nine no-`chord_rhythm` legends have been stuck on
        # with the re-attacks missing.
        slo, shi = spec.get("swells", DEFAULT["swells"])
        bars = []
        for b in range(nbars):
            s = ["-"] * 16
            if b == 0:
                s[0] = "X"
            for c in rng.sample(sorted(BEATS),
                                min(rng.randint(slo, shi), len(BEATS))):
                if s[c] == "-":
                    s[c] = "o"
            bars.append("".join(s))
        return figure, bars, shape

    if figure == "arp":
        shape = _weighted(rng, spec.get("shape", DEFAULT["shape"]))
        if spec.get("arp_flow"):
            return figure, arp_bars(rng, nbars, rest_p), shape
        step = max(int(spec.get("arp_step", DEFAULT["arp_step"])), 1)
        bars = []
        for _ in range(nbars):
            s = ["-"] * 16
            for c in range(0, 16, step):
                if rng.random() < rest_p:     # a rest, which the old fixed
                    continue                  # eighth-note arp never had
                s[c] = "X" if c in BEATS else "x"
            bars.append("".join(s))
        return figure, bars, shape

    # stab / comp: the same cell picker, but comp is told to stay out of
    # the drums' way — chords answering the kit rather than doubling it.
    if figure == "comp" and spec.get("comp_flow"):
        return figure, comp_bars(rng, nbars, bar0, busy, rest_p), \
            "hold:%g" % COMP_HOLD
    if spec.get("library"):
        got = _library_bars(spec, rng, nbars, figure == "comp", busy,
                           avoid=avoid, trace=trace, bar0=bar0)
        if got:
            # `shape` is the arp note order for arps; for stab/comp it
            # carries how long each hit rings ("hold:<16ths>").
            return figure, got[0], "hold:%g" % got[1]
    avoid = _busy_cells(busy) if figure == "comp" else ()
    first = _cells(w, lo, hi, rng, avoid=avoid)
    bars = []
    for b in range(nbars):
        hits = set(first) if b == 0 else {
            c for c in first if rng.random() >= rest_p}
        bars.append(_write(hits, rng,
                           ghost_p * (1.6 if figure == "comp" else 1.0)))
    return figure, bars, shape


def _order(notes, shape):
    """The note order an arp walks. `up` is the old fixed figure, kept
    byte-identical (chord notes then the octave), so an identity that
    rolls `up` sounds like it always did."""
    up = list(notes) + [notes[0] + 12]
    if shape == "down":
        return list(reversed(up))
    if shape == "updown":
        return up + list(reversed(up))[1:-1]
    if shape == "broken" and len(up) > 2:
        return [up[0], up[2], up[1]] + up[3:]
    if shape == "walk":
        return up + [up[-1] + 2]
    return up


def render_figure(bars, dur, bpm, notes, render_note, render_chord,
                  figure="stab", shape=None, spec=None, seed=0,
                  sr=chord_synth.SR):
    """Play a written figure into a `dur`-second, loop-safe chord buffer.

    `render_note(note, seg_dur)` voices one note (arp steps);
    `render_chord(notes, seg_dur)` voices the whole chord (stab/comp/pad).
    Either may return None for "his library can't voice this" — that step
    is left SILENT, never synthesized. That rule is chord_synth's and it
    does not get relaxed here.
    """
    spec = spec or DEFAULT
    n = max(int(dur * sr), 1)
    out = np.zeros(n)
    if not notes or not bars:
        return out
    beat_s = 60.0 / bpm
    bar_s = beat_s * 4
    off_ms, jit_ms, swing = spec.get("feel", DEFAULT["feel"])
    feel = groove.LaneFeel(off_ms, jit_ms, swing, seed=seed)
    seg_dur = beat_s / 4 * float(spec.get("seg", DEFAULT["seg"]))
    if isinstance(shape, str) and shape.startswith("hold:"):
        seg_dur = beat_s / 4 * float(shape[5:])
        shape = None
    order = _order(notes, shape)
    # arp_flow: a note rings to the next hit (at most ARP_RING 16ths), so
    # the written rhythm also sets the note lengths
    hits = [b * 16 + s for b, bar in enumerate(bars)
            for s, ch in enumerate(bar[:16]) if ch != "-"]
    ring = {}
    cap = None
    if figure == "arp" and spec.get("arp_flow"):
        cap = ARP_RING
    elif figure in ("stab", "comp") and spec.get("comp_flow"):
        cap = seg_dur / (beat_s / 4)      # the pattern's hold, in 16ths
    if cap and hits:
        total = 16 * len(bars)
        for j, h in enumerate(hits):
            gap = (hits[(j + 1) % len(hits)] - h) % total or total
            ring[h] = beat_s / 4 * min(gap, cap) * 0.9
    k = 0
    for b, bar in enumerate(bars):
        for step, ch in enumerate(bar[:16]):
            if ch == "-":
                continue
            lvl = groove.velocity(ch, step, None)
            if lvl <= 0:
                continue
            if figure == "arp":
                seg = render_note(order[k % len(order)],
                                  ring.get(b * 16 + step, seg_dur))
                k += 1
            elif figure == "pad" and ch == "X":
                # the head of a pad is still a HELD block: it fills the
                # slot the way sustain always did, and the re-attacks
                # below are what's new.
                seg = render_chord(notes, dur)
            else:
                seg = render_chord(notes, ring.get(b * 16 + step, seg_dur))
            if seg is None:
                continue
            t = feel.hit_time(b * bar_s, step, bpm)
            chord_synth.add_wrapped(out, seg * lvl, int(round(t * sr)))
    return chord_synth.finish_riff(out, sr)
