"""Drums, bass and chords as ONE groove (owner 2026-10-20, `groove_flow`).

The owner's brief: the drums set the pulse and accents; the bass connects
SELECTED kick hits to the harmony; the chords answer or support that
rhythm while leaving space for both. When the kick is busy, bass and
chords get simpler; when the drums leave space, they move or sustain.
Each phrase varies in rests, note lengths, pickups and held notes, and
the kick stays clear.

Before this, the bass's "kick" figure locked to EVERY kick hit and the
other figures ignored the kick; the chords only leaned away from drum
cells on the comp figure. Nothing read how busy a bar's kick was.

This module only edits already-planned hits (bass_rhythm.plan_line's
output, chord_rhythm.gen_figure's bars); it rolls nothing new beyond its
own seeds, so the older rolls do not move. New beats only: a preset
without `groove_flow` never calls it.

BUSY / SPACE come from measuring 40 composes x 45 identities (2026-10-20,
kick hits per bar): median 4-5, >=6 is the busiest ~25%, <=3 the
sparsest ~21%. The 50% sustain-or-move split, the 3-note cap and the
2-16th short note are Claude's starting numbers -- tune by ear.
"""
from __future__ import annotations

import random

BUSY = 6            # kick hits in a bar at or above this = busy
SPACE = 3           # at or below this = the drums leave space
BASS_CAP = 3        # most bass notes in a busy-kick bar
CHORD_CAP = 2       # most chord hits in a busy-kick bar
SHORT = 2           # 16ths a shortened (phrase-rest) bass note rings


def kick_bar(kick_bars, gb):
    if kick_bars:
        kb = kick_bars[gb % len(kick_bars)]
        if isinstance(kb, str) and len(kb) >= 16:
            return kb[:16]
    return "-" * 16


def load(kb):
    n = sum(ch != "-" for ch in kb)
    return "busy" if n >= BUSY else "space" if n <= SPACE else "mid"


def _steps(kb):
    return {i for i, ch in enumerate(kb) if ch != "-"}


def lock_bass(plan, slots, kick_bars, variant, fits):
    """Edit a bass plan in place. Per loop bar:
    busy kick -> the downbeat, any push into the next chord, and at most
      BASS_CAP notes in all, picked from the kick's own hits (accents first);
    otherwise -> drop notes a 16th off a kick (they smear it);
    space -> half the time hold (only downbeat + push), else add a soft
      pickup on the "and" of 4 on a phrase's 2nd/4th bar;
    2nd bar of each 4-bar phrase -> half the time its last note is cut
      short, leaving a rest. Lengths go in p["short"] {(bar, step): 16ths}."""
    n = len(slots)
    for i, (s, p) in enumerate(zip(slots, plan)):
        rng = random.Random(variant * 1009 + 13 + i)
        last = s["bars"] - 1
        nxt = slots[(i + 1) % n]["root"]
        out, short = [], {}
        for b in range(s["bars"]):
            gb = s["start_bar"] + b
            kb = kick_bar(kick_bars, gb)
            ks, ld = _steps(kb), load(kb)
            hits = [h for h in p["hits"] if h[0] == b]

            def core(h):
                return h[1] == 0 or (b == last and h[1] >= 13)
            if ld == "busy":
                keep = [h for h in hits if core(h)]
                cand = [h for h in hits if not core(h) and h[1] in ks]
                rng.shuffle(cand)
                cand.sort(key=lambda h: kb[h[1]] != "X")
                hits = keep + cand[:max(0, BASS_CAP - len(keep))]
            else:
                hits = [h for h in hits if core(h) or h[1] in ks
                        or not ({h[1] - 1, h[1] + 1} & ks)]
                if ld == "space":
                    if rng.random() < 0.5:
                        hits = [h for h in hits if core(h)]      # sustain
                    elif gb % 2 == 1 and not any(h[1] >= 12 for h in hits) \
                            and not ({13, 14, 15} & ks):
                        to = nxt if b == last else s["root"]
                        note = next((c for c in (to - 1, to + 1, to)
                                     if fits(c)), to)
                        hits.append((b, 14, "o", note))           # pickup
            hits.sort(key=lambda h: h[1])
            if gb % 4 == 1 and hits and rng.random() < 0.5:
                h = hits[-1]
                if not (b == last and h[1] >= 13):               # not a tie
                    short[(b, h[1])] = SHORT                     # a rest
            out.extend(hits)
        p["hits"] = out
        p["short"] = short
    return plan


def lock_chords(bars, bar0, kick_bars, rng):
    """A stab/comp slot's written bars, locked to the kick. Returns
    (bars, long): `long` = hit positions (b*16+step) that ring on to the
    next hit -- a sustain in a bar where the drums leave space.
    busy kick -> no chord hit on a kick step, then at most CHORD_CAP hits;
    mid -> no chord hit on an accented kick;
    the slot's first hit (the chord change) always stays, and a bar is
    never emptied by this."""
    out, long = [], set()
    for b, bar in enumerate(bars):
        kb = kick_bar(kick_bars, bar0 + b)
        ld = load(kb)
        cells = list(bar[:16])
        hits = [k for k, ch in enumerate(cells) if ch != "-"]
        keep0 = b == 0 and 0 in hits

        def clash(k):
            if keep0 and k == 0:
                return False
            return kb[k] != "-" if ld == "busy" else kb[k] == "X"
        if ld != "space":
            left = [k for k in hits if not clash(k)]
            if left:
                hits = left
            if ld == "busy" and len(hits) > CHORD_CAP:
                first = [0] if keep0 else []
                rest = [k for k in hits if k not in first]
                hits = first + sorted(rng.sample(rest, CHORD_CAP - len(first)))
        elif len(hits) <= 2 and rng.random() < 0.5:
            long.update(b * 16 + k for k in hits)
        out.append("".join(cells[k] if k in hits else "-"
                           for k in range(16)) + bar[16:])
    return out, long


def invert(notes):
    """The same chord, lowest note moved up an octave (a new voicing,
    same progression)."""
    if len(notes) < 3:
        return list(notes)
    return sorted(list(notes[1:]) + [notes[0] + 12])
