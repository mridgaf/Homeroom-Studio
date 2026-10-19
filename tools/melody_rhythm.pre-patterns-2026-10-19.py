"""The ANSWER MELODY (owner build 2026-10-19).

Why this exists. Every melodic part a beat had was a chord part: the
"lead" role is the chord's colour note an octave up, playing the chord's
own rhythm. Nothing played a tune. This writes a short phrase that
ANSWERS the chords: it plays in the back half of bars 2 and 4 (the
phrase tails), moves mostly by step in the key, lands on a chord tone on
the strong beats, states a 2-5 note motif and then answers it (same
rhythm, changed ending), and rests most of the time -- these beats are
for rappers, so sparse is the point.

Where it lives (owner pick 2026-10-19: "new melody part"): its own lane,
`melody0`, its own rack row and stem. The WHOLE phrase is one
loop-length, loop-safe buffer (chord_synth.add_wrapped) triggered once on
bar 1, so a note that rings over the loop point wraps instead of cutting.

Rules carried over:
- his own sampled instruments only, ONE instrument per beat (2026-08-03),
  never the chord's own instrument family when another one can play it;
- levels only from the WRITTEN character via groove.velocity (2026-08-03);
- one note at a time;
- a loop/chip/MIDI-led beat gets no melody (theory/arrangement.md: "If a
  loop is playing, that's the one melodic part") -- the caller checks.

New beats only: add_bass_and_chords stamps `melody_flow`. About half of
stamped beats roll a melody (owner 2026-10-19). Every number below is
Claude's own starting point under the 2026-10-19 creative-control grant,
not sourced -- tune by ear.
"""
from __future__ import annotations

import random

import numpy as np

import chord_synth
import groove
from pattern_gen import _weighted

FLOW_VERSION = 1
PLAY_P = 0.5             # share of stamped beats that get a melody
MAX_SHIFT = 12           # semitones a note may be stretched from its file
STEP_MAX = 4             # semitones: up to a 3rd is a step/skip, a 4th+
                         # is a leap (textbook step/skip/leap definitions)
# Step inertia: after a step, the next step keeps its direction 43.1% vs
# turns 18.3% of the time in the Essen corpus (Temperley 2014, Music
# Perception) -> 0.70 when the next move is a step.
SAME_DIR_P = 0.70
MAX_JIT_MS = 4.0
STRONG = (0, 8)          # steps that must take a chord tone

# Per signature.chord_family: notes per phrase. Direction is sourced
# (more, shorter notes read happier/more energetic, fewer read sadder:
# Juslin 2000, Gabrielsson & Lindstrom 2001, Hub ch.04 part 3); the
# exact counts are not -- tune by ear. No pickup phrases: the Hub (ch.04
# s.11) keeps the other gaps for the player/rapper.
FAMILY = {
    "dark": {"notes": [2, 3]},
    "dreamy": {"notes": [2, 4]},
    "grit": {"notes": [2, 4]},
    "soul_jazz": {"notes": [3, 5]},
    "bright_funk": {"notes": [3, 5]},
}
DEFAULT = {"notes": [2, 4]}

# which families can carry a tune over chords, best first
VOICES = ("bell", "piano", "wood", "pluck", "guitar", "synth")

# 8 cells of a half bar; on-beats lean, the "e" of a beat is rare
HALF_W = [5, 1, 3, 2, 4, 1, 3, 2]
ON_CHORD = 0.25          # weight kept on a cell where the chords hit


def spec_for(preset):
    """This beat's melody spec: `signature.melody_grammar` (any of the
    FAMILY keys) over the identity's chord_family over DEFAULT."""
    sig = preset.get("signature") or {}
    spec = dict(FAMILY.get(sig.get("chord_family"), DEFAULT))
    own = sig.get("melody_grammar")
    if isinstance(own, dict):
        spec.update({k: v for k, v in own.items() if k in DEFAULT})
    return spec


def plays(variant):
    """Does this beat roll a melody at all (about half do)."""
    return random.Random(variant * 1301 + 7).random() < PLAY_P


def _scale_notes(scale, lo=24, hi=108):
    pcs = set(scale)
    return [n for n in range(lo, hi + 1) if n % 12 in pcs]


def _move(scale_ns, prev, steps):
    """`prev` moved `steps` scale steps (prev need not be in the scale)."""
    i = min(range(len(scale_ns)), key=lambda k: abs(scale_ns[k] - prev))
    return scale_ns[max(0, min(len(scale_ns) - 1, i + steps))]


def _nearest_tone(tones, target, prev=None):
    """The chord tone (any octave) nearest `target`; ties lean to `prev`."""
    pcs = {t % 12 for t in tones}
    cands = [n for n in range(target - 6, target + 7) if n % 12 in pcs]
    return min(cands, key=lambda n: (abs(n - target),
                                     abs(n - prev) if prev is not None
                                     else 0))


def _slot_at(slots, bar):
    for s in slots:
        if s["start_bar"] <= bar < s["start_bar"] + s["bars"]:
            return s
    return slots[0]


def _cells(rng, k, half, chord_cells):
    """k distinct steps inside one half bar (half 0 = steps 0-7, 1 = 8-15),
    leaning away from the steps the chords already hit."""
    base = 8 * half
    pool = [(base + c, HALF_W[c] * (ON_CHORD if base + c in chord_cells
                                    else 1.0)) for c in range(8)]
    got = []
    while len(got) < k and pool:
        tot = sum(w for _, w in pool)
        r = rng.random() * tot
        for j, (c, w) in enumerate(pool):
            r -= w
            if r <= 0:
                got.append(c)
                pool.pop(j)
                break
    return sorted(got)


def plan_phrase(slots, scale, spec, variant, nbars, chord_cells=None):
    """Pure: the melody as [(bar, step, char, note)], bar absolute.

    `slots`: [{"tones", "top", "start_bar", "bars"}] in play order (tones =
    the chord's MIDI notes, top = its highest voiced note). `scale`: the
    key's pitch classes. `chord_cells`: {bar: set(steps)} where the chord
    parts hit. Returns [] when there is nothing to write."""
    if not slots or not scale or nbars < 2:
        return []
    rng = random.Random(variant * 1301 + 59)
    chord_cells = chord_cells or {}
    scale_ns = _scale_notes(scale)
    lo, hi = spec["notes"]
    k = rng.randint(lo, hi)
    # the motif: k steps in the back half, k-1 scale moves, <= 1 leap
    cells = _cells(rng, k, 1, chord_cells.get(1, set()))
    # scale moves of 1-2 degrees; a step keeps its direction 70% of the
    # time (inertia, Temperley 2014)
    moves, d = [], rng.choice((-1, 1))
    for _ in range(len(cells) - 1):
        if moves and rng.random() >= SAME_DIR_P:
            d = -d
        moves.append(d * rng.choice((1, 1, 2)))
    # one leap per phrase when there is room for it, UP (large intervals
    # tend to ascend, Huron 2006) and then a step back down (gap-fill /
    # post-skip reversal, von Hippel & Huron 2000)
    leap_at = None
    if len(moves) >= 2:
        leap_at = rng.randrange(len(moves) - 1)
        moves[leap_at] = rng.choice((3, 4))
        moves[leap_at + 1] = -1
    top = max(s["top"] for s in slots)
    start = top + rng.randint(3, 9)
    # call/response bars: every odd bar's back half (bars 2, 4, ...)
    phrase_bars = list(range(1, nbars, 2))
    hits = []
    prev = None
    for n, bar in enumerate(phrase_bars):
        s = _slot_at(slots, bar)
        last_phrase = n == len(phrase_bars) - 1
        resp = n % 2 == 1
        note = None
        for j, st in enumerate(cells):
            if j == 0:
                target = start if prev is None else _move(
                    scale_ns, prev, rng.choice((-1, 1)))
                note = _nearest_tone(s["tones"], target, prev)
            else:
                note = _move(scale_ns, note, moves[j - 1])
            need = None                   # chord tones this note must hit
            if j == len(cells) - 1 and (resp or last_phrase):
                # the answer: same rhythm, it ENDS on a chord tone -- the
                # loop's last one on the chord that lands on bar 1
                land = slots[0] if last_phrase else _slot_at(slots, bar + 1)
                need = land["tones"]
            elif st in STRONG:
                need = s["tones"]
            if need:
                note = _nearest_tone(need, note, note)
            if (j and abs(note - hits[-1][3]) > STEP_MAX
                    and j - 1 != leap_at):
                # snapping made an unplanned leap: nearest legal tone to
                # the last note instead (a chord tone is never > 3 away)
                note = _nearest_tone(need or scale_ns, hits[-1][3],
                                     hits[-1][3])
            ch = "X" if st in STRONG else "x"
            if j + 1 < len(cells) and cells[j + 1] - st == 1:
                ch = "o"                  # a quick passing note, softer
            hits.append((bar, st, ch, note))
        prev = note
    hits.sort(key=lambda h: (h[0], h[1]))
    # always ABOVE the chords and the lead: separate by octave first
    # (2026 producer guidance); whole octaves, so every note keeps its name
    up = 0
    while hits and min(h[3] for h in hits) + up <= top:
        up += 12
    return [(b, st, ch, n + up) for b, st, ch, n in hits]


def _instruments(index, voices):
    """Every playable instrument in `index`, as {key: [entries]}: a
    note-by-note library is one instrument per (library, articulation); any
    other file is an instrument of one."""
    out = {}
    for e in index:
        if e.get("group") not in voices:
            continue
        key = (("multi", e["multi"], e.get("art")) if e.get("multi")
               else ("file", e["path"]))
        out.setdefault(key, []).append(e)
    return out


def _covers(entries, notes, max_shift=MAX_SHIFT):
    return all(any(abs(e["note"] - n) <= max_shift for e in entries)
               for n in notes)


def pick_instrument(index, notes, avoid_groups, variant, floor=None):
    """(entries, octave_shift) for ONE instrument that plays every note
    within MAX_SHIFT of a recording, or (None, 0). Tries the phrase as
    written, then an octave up/down (the whole phrase, never one note).
    Avoids the chord's own families when anything else can play it;
    note-by-note libraries before single files. A shift must keep every
    note above `floor` (the chords' and lead's top)."""
    rng = random.Random(variant * 1301 + 211)
    groups = [g for g in VOICES if g not in avoid_groups] or list(VOICES)
    for shift in (0, 12, -12, 24, -24):
        ns = [n + shift for n in notes]
        if ns and floor is not None and min(ns) <= floor:
            continue
        insts = _instruments(index, groups)
        ok = {k: v for k, v in insts.items() if _covers(v, ns)}
        if not ok:
            continue
        have = sorted({v[0]["group"] for v in ok.values()},
                      key=groups.index)
        g = rng.choice(have)
        mine = sorted((k for k, v in ok.items() if v[0]["group"] == g),
                      key=str)
        multi = [k for k in mine if k[0] == "multi"]
        return ok[rng.choice(multi or mine)], shift
    return None, 0


def render_line(hits, bar_s, bpm, loop_n, render_note, feel,
                sr=chord_synth.SR, seed=0):
    """Play the planned phrase into one loop-length, loop-safe buffer.
    A note runs to the next hit, but a phrase's last note rings 2-4
    sixteenths and stops. Returns (audio, notes) with notes =
    [(start_s, dur_s, note, level)], or (None, None) if a note can't be
    voiced (the beat then ships without a melody, never a synth)."""
    if not hits:
        return None, None
    rng = random.Random(seed)
    loop_s = loop_n / float(sr)
    six = bar_s / 16.0
    evs = sorted((feel.hit_time(b * bar_s, st, bpm) % loop_s, b, st, ch, n)
                 for b, st, ch, n in hits)
    out = np.zeros(loop_n)
    notes = []
    for k, (t, b, st, ch, n) in enumerate(evs):
        nb_, nst = evs[(k + 1) % len(evs)][1:3]
        gap = (evs[(k + 1) % len(evs)][0] - t) % loop_s or loop_s
        tail = (nb_ * 16 + nst) - (b * 16 + st) > 4 or k == len(evs) - 1
        dur = min(gap, rng.randint(2, 4) * six) if tail else gap
        dur = max(dur, 0.03)
        lvl = groove.velocity(ch, st, None)
        seg = render_note(n, dur)
        if seg is None:
            return None, None
        chord_synth.add_wrapped(out, seg * lvl, int(round(t * sr)))
        notes.append((t, dur, n, lvl))
    return out, notes


def feel_for(lanes, seed):
    """The melody's LaneFeel: the hats' offset and swing (they carry the
    pocket a top line sits in), jitter capped; straight-ish otherwise."""
    for ln in ("hat", "ohat", "kick"):
        t = (lanes or {}).get(ln)
        if t:
            _p, _g, (off, jit, swing, _s), _bars = t
            return groove.LaneFeel(off, min(jit, MAX_JIT_MS), swing,
                                   seed=seed)
    return groove.LaneFeel(0, 2, 50, seed=seed)
