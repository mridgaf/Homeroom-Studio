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

Opt-in only. A preset without a top-level `chord_grammar` key behaves
exactly as it did before this file existed.
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


def spec_for(preset):
    """The identity's chord grammar, or None if it hasn't opted in.

    Absent -> None -> the other twenty-two render unchanged. `true` means
    "the house default"; a dict overrides only the keys it names, so an
    identity can ask for stabs alone without restating the step weights.
    Same shape as `own_soundbank` / `snare_locked_24`: a top-level key,
    read at one decision point, falsy by absence."""
    raw = preset.get("chord_grammar")
    if not raw:
        return None
    spec = dict(DEFAULT)
    if isinstance(raw, dict):
        spec.update(raw)
    return spec


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


def gen_figure(spec, rng, nbars, busy=None):
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
    order = _order(notes, shape)
    k = 0
    for b, bar in enumerate(bars):
        for step, ch in enumerate(bar[:16]):
            if ch == "-":
                continue
            lvl = groove.velocity(ch, step, None)
            if lvl <= 0:
                continue
            if figure == "arp":
                seg = render_note(order[k % len(order)], seg_dur)
                k += 1
            elif figure == "pad" and ch == "X":
                # the head of a pad is still a HELD block: it fills the
                # slot the way sustain always did, and the re-attacks
                # below are what's new.
                seg = render_chord(notes, dur)
            else:
                seg = render_chord(notes, seg_dur)
            if seg is None:
                continue
            t = feel.hit_time(b * bar_s, step, bpm)
            chord_synth.add_wrapped(out, seg * lvl, int(round(t * sr)))
    return chord_synth.finish_riff(out, sr)
