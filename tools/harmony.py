"""Chord progression generator (punch list step 2, 2026-07-22).

pattern_gen.compose() writes the drums. This is the harmony half: turn
theory/progressions.md — already transcribed as data in
progressions_config.json — into an actual chord sequence in whatever
KeyContext the beat is in.

Nothing here decides taste beyond what the owner's own doc already
decided; this module only transposes and voices it, the same way
midi_packs.py transposes a MIDI phrase with KeyContext.shift_from.
Picking WHICH progression fits a feeling, and stacking these chords
under real audio/MIDI export, are later punch-list steps (5-7).

    ./.venv/bin/python tools/harmony.py                 # random pick, F minor
    ./.venv/bin/python tools/harmony.py Bb minor dreamy  # a named one
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from key_context import KeyContext                        # noqa: E402

CONFIG = Path(__file__).resolve().parent.parent / "progressions_config.json"
PROGRESSIONS = {k: v for k, v in json.loads(CONFIG.read_text()).items()
                 if not k.startswith("_")}


def names():
    """Every progression name, for a picker UI."""
    return sorted(PROGRESSIONS)


def compose(key, name=None, octave=3, rng=None):
    """A chord progression in `key`, from `name` (or a random pick if
    `name` isn't one of `names()`).

    Returns (name, chords) where chords is a list of dicts, one per
    chord, in order: {"root": "F", "quality": "minor", "chord": "Fm",
    "roman": "i", "notes": [53, 56, 60]} — `notes` are real MIDI note
    numbers (key_context.voice), ready for a synth or a MIDI file.
    """
    rng = rng or random
    if name not in PROGRESSIONS:
        name = rng.choice(names())
    chords = []
    for offset, quality in PROGRESSIONS[name]["chords"]:
        root_pc = (key.pc + offset) % 12
        chords.append({
            "root": key.spell(root_pc),
            "quality": quality,
            "chord": key.chord_name(root_pc, quality),
            "roman": key.roman(root_pc, quality),
            "notes": key.voice(root_pc, quality, octave),
        })
    return name, chords


# ---------------------------------------------------------------------------
# CHORD FLOW (owner 2026-09-26: "a lot of similar chord progressions ...
# not very much variety"). Measured cause, in order of size: 45% of beats
# were 1-2 chord loops, every chord was stacked root-up in the same octave,
# and every beat changed chords on the same bars (an even split starting on
# bar 1). The three tools below fix those, and ONLY for beats made with
# `chord_flow` set (beat_machine.add_bass_and_chords sets it on new beats),
# so rebuilding a beat made before today gives back the sound it had.
# ---------------------------------------------------------------------------

FLOW_VERSION = 1
SHORT_LOOP_WEIGHT = 0.5    # a 1-2 chord loop is picked half as often
TURNAROUND_P = 0.4         # share of 1-2 chord loops that get a 4th-bar turn
VOICE_LEAD_P = 0.8         # share of beats voiced smoothly (rest: root-up)
OPEN_VOICING_P = 0.3       # share of smooth beats spread wider (one note up)
VOICE_LO, VOICE_HI = 50, 79   # D3..G5, where a comping hand sits
MINOR_QUALITIES = ("minor", "min7", "min9", "dim")

# A turnaround is one short chord in the loop's last bar that leans back
# into bar 1. [semitones from the tonic, quality].
TURN_MINOR = ((7, "dom7"), (10, "major"), (5, "minor"), (8, "major"))
TURN_MAJOR = ((7, "dom7"), (5, "major"), (10, "major"), (2, "min7"))

# (chord count, loop bars, has turnaround) -> weighted bar plans. A plan is
# a list of (which chord, bars). "T" is the turnaround. Never more than four
# slots: each slot is its own rack row, and a 4-chord loop already had four.
BAR_PLANS = {
    (1, 4, False): [([(0, 4)], 1)],
    (1, 8, False): [([(0, 8)], 1)],
    (1, 4, True): [([(0, 3), ("T", 1)], 1)],
    (1, 8, True): [([(0, 7), ("T", 1)], 1), ([(0, 6), ("T", 2)], 1)],
    (2, 4, False): [([(0, 2), (1, 2)], 2), ([(0, 1), (1, 1), (0, 1), (1, 1)], 1),
                    ([(0, 3), (1, 1)], 1)],
    (2, 8, False): [([(0, 4), (1, 4)], 2), ([(0, 2), (1, 2), (0, 2), (1, 2)], 2),
                    ([(0, 3), (1, 1), (0, 3), (1, 1)], 1),
                    ([(0, 6), (1, 2)], 1)],
    (2, 4, True): [([(0, 2), (1, 1), ("T", 1)], 1),
                   ([(0, 1), (1, 1), (0, 1), ("T", 1)], 1)],
    (2, 8, True): [([(0, 2), (1, 2), (0, 2), ("T", 2)], 2),
                   ([(0, 4), (1, 3), ("T", 1)], 1),
                   ([(0, 3), (1, 3), ("T", 2)], 1)],
    (3, 4, False): [([(0, 1), (1, 1), (2, 2)], 2), ([(0, 2), (1, 1), (2, 1)], 1),
                    ([(0, 1), (1, 2), (2, 1)], 1)],
    (3, 8, False): [([(0, 2), (1, 2), (2, 4)], 2), ([(0, 3), (1, 3), (2, 2)], 1),
                    ([(0, 4), (1, 2), (2, 2)], 1), ([(0, 2), (1, 4), (2, 2)], 1)],
    (4, 4, False): [([(0, 1), (1, 1), (2, 1), (3, 1)], 1)],
    (4, 8, False): [([(0, 2), (1, 2), (2, 2), (3, 2)], 2),
                    ([(0, 3), (1, 1), (2, 3), (3, 1)], 1),
                    ([(0, 2), (1, 2), (2, 3), (3, 1)], 1)],
}


def pick_weights(spec):
    """A signature's `progressions` list with 1-2 chord loops weighted by
    SHORT_LOOP_WEIGHT, as [[name, weight], ...] (flat lists get weight 1)."""
    if not spec:
        return spec
    rows = [list(x) if isinstance(x, (list, tuple)) else [x, 1] for x in spec]
    return [[n, w * (SHORT_LOOP_WEIGHT if n in PROGRESSIONS and
                     len(PROGRESSIONS[n]["chords"]) <= 2 else 1)]
            for n, w in rows]


def _chord(key, offset, quality, octave=3):
    root_pc = (key.pc + offset) % 12
    return {"root": key.spell(root_pc), "quality": quality,
            "chord": key.chord_name(root_pc, quality),
            "roman": key.roman(root_pc, quality),
            "notes": key.voice(root_pc, quality, octave)}


def arrange(key, chords, bars, rng):
    """Lay `chords` (compose()'s list) over a `bars`-long loop.

    Returns a list of chord dicts in play order, each a COPY with "bars"
    added; a turnaround chord also carries "turnaround": True. Loop
    lengths with no plan in BAR_PLANS fall back to the old even split."""
    n = len(chords)
    turn = None
    if n <= 2 and rng.random() < TURNAROUND_P:
        tonic_off = (chords[0]["notes"][0] - key.voice(key.pc, "major", 3)[0]) % 12
        pool = TURN_MINOR if chords[0]["quality"] in MINOR_QUALITIES \
            else TURN_MAJOR
        have = {((c["notes"][0] - key.voice(key.pc, "major", 3)[0]) % 12,
                 c["quality"]) for c in chords}
        opts = [(o, q) for o, q in pool
                if ((o + tonic_off) % 12, q) not in have]
        if opts:
            o, q = rng.choice(opts)
            turn = _chord(key, (o + tonic_off) % 12, q)
            turn["turnaround"] = True
    plans = BAR_PLANS.get((n, bars, turn is not None))
    if not plans:
        per = max(1, bars // n)
        out = []
        for i, c in enumerate(chords):
            start = i * per
            if start >= bars:
                break
            end = bars if i == n - 1 else min(start + per, bars)
            out.append(dict(c, bars=end - start))
        return out
    plan = rng.choices([p for p, _ in plans], [w for _, w in plans])[0]
    return [dict(turn if which == "T" else chords[which], bars=b)
            for which, b in plan]


def _candidates(notes, lo=VOICE_LO, hi=VOICE_HI):
    """Every inversion of a chord's pitch classes that fits lo..hi."""
    pcs = []
    for n in notes:
        if n % 12 not in pcs:
            pcs.append(n % 12)
    out = []
    for r in range(len(pcs)):
        order = pcs[r:] + pcs[:r]
        for base in range(lo - 12, hi + 1):
            if base % 12 != order[0] or base < lo:
                continue
            stack = [base]
            for pc in order[1:]:
                nxt = stack[-1] + 1
                while nxt % 12 != pc:
                    nxt += 1
                stack.append(nxt)
            if stack[-1] <= hi:
                out.append(stack)
    return out


def _move(a, b):
    """How far the hand travels from voicing a to b (smaller = smoother)."""
    return (sum(min(abs(x - y) for y in a) for x in b)
            + sum(min(abs(x - y) for y in b) for x in a))


def voice_lead(chords, rng):
    """Give each chord a "voiced" note list: the inversion closest to the
    chord before it, so the chords flow instead of jumping as blocks.
    `notes` (root position) is left alone -- the bass line, the 808 and the
    multi-part split all read their root from notes[0].

    Returns the style used: "smooth", "open", or "root" (the old sound,
    kept on 1 - VOICE_LEAD_P of beats so it stays in the mix)."""
    roll = rng.random()
    if roll >= VOICE_LEAD_P:
        for c in chords:
            c["voiced"] = list(c["notes"])
        return "root"
    spread = rng.random() < OPEN_VOICING_P
    prev = None
    centre = rng.choice((58, 60, 62, 64, 66))
    for c in chords:
        cands = _candidates(c["notes"]) or [list(c["notes"])]
        if prev is None:
            cands.sort(key=lambda v: abs(sum(v) / len(v) - centre))
            best = rng.choice(cands[:3])
        else:
            scored = sorted(cands, key=lambda v: (_move(prev, v),
                                                  rng.random()))
            best = scored[0]
        prev = best
        v = list(best)
        if spread and len(v) >= 3 and v[1] + 12 <= VOICE_HI + 5:
            v = sorted([v[0]] + [v[1] + 12] + v[2:])
        c["voiced"] = v
    return "open" if spread else "smooth"


def lead_parts(splits, lo=40, hi=88):
    """Voice-lead a multi-part beat. `splits` is one (support, lead,
    passing) per chord slot, from beat_machine._split_chord_roles. Each
    PART moves by whole octaves, note by note, to sit closest to where that
    same part was on the chord before -- so the low part and the top part
    each glide instead of jumping. The split itself (root+5th low, colour
    notes above -- theory/arrangement.md) is never changed, and each part
    stays above the part under it."""
    out, prev = [], [None, None, None]
    for parts in splits:
        new = []
        floor = lo
        for k, part in enumerate(parts):
            part = list(part)
            if not part:
                new.append(part)
                continue
            best = part
            if prev[k] is not None:
                shifts = [(-12,), (0,), (12,)]
                for _ in part[1:]:
                    shifts = [s + (d,) for s in shifts for d in (-12, 0, 12)]
                cands = []
                for sh in shifts:
                    c = sorted(n + d for n, d in zip(part, sh))
                    if c[0] < max(lo, floor) or c[-1] > hi:
                        continue
                    if c[-1] - c[0] > 19:          # one hand's reach
                        continue
                    cands.append((_move(prev[k], c), sum(map(abs, sh)), c))
                if cands:
                    best = min(cands)[2]
            new.append(best)
            prev[k] = best
            floor = max(best) + 1
        out.append(tuple(new))
    return out


def _report(root="F", mode="minor", name=None):
    key = KeyContext(root, mode)
    picked, chords = compose(key, name)
    print("key         : %s   (808 root %.2f Hz)" % (key, key.hz))
    print("progression : %s — %s\n" % (picked, PROGRESSIONS[picked]["label"]))
    for c in chords:
        print("  %-6s %-6s  %s" % (c["chord"], c["roman"], c["notes"]))


if __name__ == "__main__":
    _report(*sys.argv[1:4])
