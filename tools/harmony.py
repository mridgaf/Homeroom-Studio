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

from key_context import MINORISH, KeyContext, mode_family   # noqa: E402

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
    return name, compose_chords(key, PROGRESSIONS[name]["chords"], octave)


def compose_chords(key, rel, octave=3):
    """compose()'s chord dicts for any [[offset, quality], ...] list --
    a progressions_config loop or one chord_gen.py made."""
    chords = []
    for offset, quality in rel:
        root_pc = (key.pc + offset) % 12
        chords.append({
            "root": key.spell(root_pc),
            "quality": quality,
            "chord": key.chord_name(root_pc, quality),
            "roman": key.roman(root_pc, quality),
            "notes": key.voice(root_pc, quality, octave),
        })
    return chords


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
MINOR_QUALITIES = MINORISH

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


# ONE CHORD (owner 2026-10-31, beats stamped `one_chord`): "There shouldn't
# really be any chord changes in such a short pattern", and every note stays
# in the key. The loop plays ONE chord on the key's home note, the
# turnaround is off, colour notes must be key notes, and the bass / melody /
# riff scale drops the AVOID notes -- a key note a half step above a chord
# tone (chord-scale theory, Hub ch.13 part 2: chord tones on the downbeats;
# a half step above a chord tone is the classic clash).
def home_chord(key, chords):
    """The loop's one chord: the first of `chords` on the home note with
    every note in the key, else the key's own home triad."""
    sc = set(key.scale())
    for c in chords:
        if c["notes"][0] % 12 == key.pc and all(n % 12 in sc
                                                for n in c["notes"]):
            return c
    return _chord(key, 0, key.triad(1)[1])


# TWO CHORDS (owner 2026-11-03, Gomez-Peck 2023 / Adams 2020): real hip-hop
# loops are repetitive (1 chord), oscillating (2 chords, "special and
# particularly common", most often i-iv) or expansional. Dark identities stay
# on one chord; soul and melodic ones shuttle between two. Both chords stay
# in the key, and every 2-chord bar plan ends on the SECOND chord (an open
# loop that pulls back to the start).
TWO_CHORD_P = {"dark": 0.10, "grit": 0.35, "soul_jazz": 0.60,
               "dreamy": 0.55, "bright_funk": 0.50}
_PARTNER_MINOR = ((4, 4), (7, 3), (3, 2), (6, 2), (5, 1))   # iv bVII bIII bVI v
_PARTNER_MAJOR = ((4, 4), (5, 3), (6, 2), (7, 1))           # IV V vi VII


def wants_two(sig, rng):
    """True when this beat's loop shuttles between two chords."""
    p = (sig or {}).get("two_chord_p",
                        TWO_CHORD_P.get((sig or {}).get("chord_family"), 0.4))
    return rng.random() < float(p)


def second_chord(key, loop, home, rng):
    """The home chord's partner: first a chord from the genre loop `loop`
    (chord dicts) that is whole-in-key, off the tonic, not dim/aug/bare 5th;
    else a triad on iv / bVII / bIII / bVI / v (IV / V / vi in major).
    None if nothing fits."""
    sc = set(key.scale())
    ok = [c for c in loop
          if c["notes"][0] % 12 != home["notes"][0] % 12
          and all(n % 12 in sc for n in c["notes"])
          and c["quality"] not in ("dim", "aug", "5", "dim7", "m7b5")]
    if ok:
        return dict(rng.choice(ok))
    pool = (_PARTNER_MINOR if mode_family(key.mode) == "minor"
            else _PARTNER_MAJOR)
    opts = []
    for deg, w in pool:
        root, q = key.triad(deg)
        if q in ("dim", "aug", "5") or root == home["notes"][0] % 12:
            continue
        opts.append(((root, q), w))
    if not opts:
        return None
    root, q = rng.choices([o for o, _ in opts], [w for _, w in opts])[0]
    return _chord(key, (root - key.pc) % 12, q)


def safe_scale_pair(key, chords):
    """safe_scale over several chords: a note must be safe against all."""
    out = None
    for c in chords:
        s = safe_scale(key, c["notes"])
        out = s if out is None else tuple(x for x in out if x in s)
    return out or safe_scale(key, chords[0]["notes"])


def safe_scale(key, tones):
    """The key's notes minus the avoid notes over a chord of `tones`."""
    ct = {n % 12 for n in tones}
    return tuple(pc for pc in key.scale()
                 if pc in ct or (pc - 1) % 12 not in ct)


def arrange(key, chords, bars, rng, no_half=False, turn_ok=True):
    """Lay `chords` (compose()'s list) over a `bars`-long loop.

    Returns a list of chord dicts in play order, each a COPY with "bars"
    added; a turnaround chord also carries "turnaround": True. Loop
    lengths with no plan in BAR_PLANS fall back to the old even split.
    `no_half` (owner 2026-10-30): never the plan whose only change is
    exactly halfway (4+4, 2+2); a 2-chord fallback splits 3/4 + 1/4."""
    n = len(chords)
    turn = None
    if turn_ok and n <= 2 and rng.random() < TURNAROUND_P:
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
    if plans and no_half:
        plans = [(p, w) for p, w in plans
                 if not (len(p) == 2 and p[0][1] * 2 == bars)] or plans
    if not plans and no_half and n == 2 and bars >= 4:
        a = bars * 3 // 4
        return [dict(chords[0], bars=a), dict(chords[1], bars=bars - a)]
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
    out = _stacks(pcs, lo, hi)
    # 5-6 note colours (11ths, 13ths) that don't fit: drop the plain 5th,
    # the way a keys player does. Only when nothing fit, so every chord
    # that fitted before 2026-10-19 voices exactly as it did.
    if not out and len(pcs) > 4 and (pcs[0] + 7) % 12 in pcs[1:]:
        out = _stacks([p for p in pcs if p != (pcs[0] + 7) % 12], lo, hi)
    return out


def _stacks(pcs, lo, hi):
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


# ---------------------------------------------------------------------------
# CHORD COLOUR (owner 2026-10-19: "simplistic chords ... not specified at
# all towards the DJ's styles"). 101 of the 170 chords in the progression
# pool were plain triads. colorize() swaps some of them for a richer chord
# on the SAME root (Fm -> Fm9, Ab -> Abmaj7, C -> C7b9), so the progression
# and the bass line keep their shape and only the colour deepens. How far
# and which way is the identity's `chord_color` card:
#   {"depth": 0..1   share of chords upgraded,
#    "lean": {quality: weight multiplier}}   e.g. dark DJs lean m7b5/7b9
# No card -> DEFAULT_COLOR. New (chord_flow) beats only, own seed.
# ---------------------------------------------------------------------------

DEFAULT_COLOR = {"depth": 0.55, "lean": {}}

# base quality -> [(richer quality, weight)]. "dominant" = a major chord
# on the 5th of the key (or an existing 7th chord), which wants tension.
UPGRADES = {
    "minor":    [("min7", 3), ("min9", 3), ("min11", 2), ("madd9", 2),
                 ("min6", 1), ("min_maj7", 0.5)],
    "major":    [("maj7", 3), ("maj9", 2), ("add9", 2), ("maj6", 1),
                 ("6/9", 1), ("maj7#11", 1), ("add11", 0.5), ("sus2", 1)],
    "dominant": [("dom9", 3), ("dom13", 2), ("7sus4", 2), ("7b9", 1.5),
                 ("9sus4", 1)],
    "dim":      [("m7b5", 3), ("dim7", 2)],
    "min7":     [("min9", 2), ("min11", 2)],
    "maj7":     [("maj9", 2), ("maj7#11", 1), ("6/9", 1)],
    "dom7":     [("dom9", 3), ("dom13", 2), ("7b9", 1.5), ("7sus4", 1)],
}


def colorize(key, chords, card, rng, in_key=False):
    """Upgrade some of `chords` (compose()'s list) in place to richer
    qualities on the same root. Returns how many changed. `in_key`
    (one_chord): only qualities whose every note is in the key."""
    card = card or DEFAULT_COLOR
    depth = float(card.get("depth", DEFAULT_COLOR["depth"]))
    lean = card.get("lean") or {}
    changed = 0
    for c in chords:
        if rng.random() >= depth:
            continue
        q = c["quality"]
        root_pc = c["notes"][0] % 12
        base = q
        if q == "major" and (root_pc - key.pc) % 12 == 7:
            base = "dominant"
        opts = [(nq, w * float(lean.get(nq, 1))) for nq, w in
                UPGRADES.get(base, [])]
        opts = [(nq, w) for nq, w in opts if w > 0]
        if in_key:
            sc = set(key.scale())
            opts = [(nq, w) for nq, w in opts
                    if all(n % 12 in sc for n in key.voice(root_pc, nq))]
        if not opts:
            continue
        nq = rng.choices([o for o, _ in opts], [w for _, w in opts])[0]
        octave = c["notes"][0] // 12 - 1
        c.update(quality=nq, chord=key.chord_name(root_pc, nq),
                 roman=key.roman(root_pc, nq),
                 notes=key.voice(root_pc, nq, octave))
        changed += 1
    return changed


def _report(root="F", mode="minor", name=None):
    key = KeyContext(root, mode)
    picked, chords = compose(key, name)
    print("key         : %s   (808 root %.2f Hz)" % (key, key.hz))
    print("progression : %s — %s\n" % (picked, PROGRESSIONS[picked]["label"]))
    for c in chords:
        print("  %-6s %-6s  %s" % (c["chord"], c["roman"], c["notes"]))


if __name__ == "__main__":
    _report(*sys.argv[1:4])
