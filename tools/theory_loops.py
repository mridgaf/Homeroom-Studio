#!/usr/bin/env python3
"""College-theory MIDI loops (Production Research Hub, Chapter 13).

Builds 8-bar MIDI loops from rules that are SOURCED in Chapter 13:
  * chord-loop schemas (Open Music Theory, Pop unit)
  * voice-leading rules (Berklee Online + OMT jazz "lazy voices")
  * drum grids (OMT "Drumbeats" + Berklee College hip-hop article)
and then re-opens every file it wrote and CHECKS each rule on the file itself.

Nothing here is invented: where a number is not in a source it is not used
(no swing amount, no dembow, no low-register spacing table).

Python 3.9 safe. No third-party packages.
Usage:  python3 theory_loops.py OUTPUT_FOLDER
"""
from __future__ import annotations

import itertools
import os
import struct
import sys

PPQ = 480
STEP = PPQ // 4            # one 16th
BAR = PPQ * 4
BARS = 8                   # OMT/Chapter 13: loops 2, 4 or 8 bars -> 8-bar audition
KEY_TONIC = 0              # C; transpose by changing this (pitch class)

# --------------------------------------------------------------------------
# 1. Chord-loop schemas. (root semitones above tonic, quality). Source: OMT Pop.
#    One chord per bar, 4 chords, played twice = 8 bars.
# --------------------------------------------------------------------------
SCHEMAS = {
    "Doo-wop I-vi-IV-V":            [(0, "maj"), (9, "min"), (5, "maj"), (7, "maj")],
    "Singer-songwriter I-V-vi-IV":  [(0, "maj"), (7, "maj"), (9, "min"), (5, "maj")],
    "Hopscotch IV-V-vi-I":          [(5, "maj"), (7, "maj"), (9, "min"), (0, "maj")],
    "Lament i-bVII-bVI-V":          [(0, "min"), (10, "maj"), (8, "maj"), (7, "maj")],
    "Aeolian shuttle i-bVII-bVI-bVII": [(0, "min"), (10, "maj"), (8, "maj"), (10, "maj")],
    "Dorian shuttle i-IV":          [(0, "min"), (5, "maj"), (0, "min"), (5, "maj")],
    "Double plagal bVII-IV-I":      [(10, "maj"), (5, "maj"), (0, "maj"), (0, "maj")],
    "Plagal sigh IV-iv-I":          [(5, "maj"), (5, "min"), (0, "maj"), (0, "maj")],
}
QUALITY = {"maj": (0, 4, 7), "min": (0, 3, 7)}

# --------------------------------------------------------------------------
# 2. Drum grids, 16 steps per bar. GM drum map (kick 36, snare 38, hat 42).
#    Sources: OMT Drumbeats (backbeat 2&4, half-time = snare on beat 3 only,
#    double-time = backbeat on 2nd 8th of every beat, four-on-the-floor),
#    Berklee College (kick lands on beat 1 of a 1-2 bar phrase).
# --------------------------------------------------------------------------
KICK, SNARE, HAT_C = 36, 38, 42
EIGHTHS = list(range(0, 16, 2))
SIXTEENTHS = list(range(16))
SYNC_POOL = [3, 6, 7, 10, 11, 14]   # off-beat steps for a syncopated kick


def drum_pattern(name: str, bar: int):
    """Return (kick_steps, snare_steps, hat_steps) for one bar."""
    if name == "boom-bap":
        return [0, 8], [4, 12], EIGHTHS
    if name == "boom-bap-16th-hats":
        return [0, 8], [4, 12], SIXTEENTHS
    if name == "half-time":
        return [0], [8], EIGHTHS
    if name == "double-time":
        return [0, 8], [2, 6, 10, 14], SIXTEENTHS
    if name == "four-on-the-floor":
        return [0, 4, 8, 12], [4, 12], [2, 6, 10, 14]   # off-beat hats (OMT: Heart of Glass)
    if name == "syncopated-kick":
        # kick ALWAYS on step 0 (OMT: HUMBLE.; Berklee). Extras are fixed per bar-pair
        # (no randomness) so the file is repeatable.
        extra_sets = [[6, 10], [7, 11], [6, 14], [3, 10]]
        return [0] + extra_sets[(bar // 2) % len(extra_sets)], [4, 12], EIGHTHS
    raise ValueError(name)


# (title, schema, drum, bpm). BPMs stay inside ranges quoted in Chapter 13:
#   normal feel 80-160 (OMT); East Coast 100-120; West Coast 90-120; Southern 80 or 160.
BATCH = [
    ("01 Doo-wop boom-bap",            "Doo-wop I-vi-IV-V",             "boom-bap",           96),
    ("02 Singer-songwriter 16th hats", "Singer-songwriter I-V-vi-IV",   "boom-bap-16th-hats", 100),
    ("03 Hopscotch syncopated kick",   "Hopscotch IV-V-vi-I",           "syncopated-kick",    110),
    ("04 Lament half-time",            "Lament i-bVII-bVI-V",           "half-time",          140),
    ("05 Aeolian shuttle double-time", "Aeolian shuttle i-bVII-bVI-bVII", "double-time",       80),
    ("06 Dorian shuttle four-floor",   "Dorian shuttle i-IV",           "four-on-the-floor",  120),
    ("07 Double plagal boom-bap",      "Double plagal bVII-IV-I",       "boom-bap",           90),
    ("08 Plagal sigh half-time",       "Plagal sigh IV-iv-I",           "half-time",          100),
]

# --------------------------------------------------------------------------
# 3. Voice leading. Rules (Berklee Online + OMT):
#    keep common tones in the SAME voice; move others by step if possible;
#    no upper voice moves more than a third (<=4 semitones); bass may leap.
# --------------------------------------------------------------------------
UP_LO, UP_HI = 55, 76       # upper-voice window (G3..E5): practical piano middle
BASS_LO, BASS_HI = 36, 47   # bass root: C2..B2
MAX_MOVE = 4                # a major third


def pcs_of(root: int, quality: str):
    return [(KEY_TONIC + root + i) % 12 for i in QUALITY[quality]]


def close_voicings(pcs):
    """All 3-note close voicings (one of each pitch class), ascending, span <= 12."""
    out = []
    for notes in itertools.product(range(UP_LO, UP_HI + 1), repeat=3):
        if not (notes[0] < notes[1] < notes[2]):
            continue
        if notes[2] - notes[0] > 12:
            continue
        if sorted(n % 12 for n in notes) != sorted(pcs):
            continue
        out.append(notes)
    return out


def cost(a, b):
    """Movement cost between two voicings; None if a hard rule is broken."""
    moves = [abs(x - y) for x, y in zip(a, b)]
    if max(moves) > MAX_MOVE:
        return None
    # common tones must stay in the same voice
    shared = set(n % 12 for n in a) & set(n % 12 for n in b)
    for pc in shared:
        if not any(x == y and x % 12 == pc for x, y in zip(a, b)):
            return None
    return sum(moves)


def best_cycle(chords):
    """Pick one voicing per chord so the whole loop (including wrap) is smoothest."""
    cands = [close_voicings(pcs_of(r, q)) for r, q in chords]
    best, best_c = None, None
    # fix the first chord voicing near the middle, search the rest exhaustively
    first_opts = [v for v in cands[0] if 60 <= v[1] <= 67] or cands[0]
    for v0 in first_opts:
        # dynamic program over remaining chords
        layer = {v0: (0, [v0])}
        for ci in range(1, len(chords)):
            nxt = {}
            for v, (c, path) in layer.items():
                for w in cands[ci]:
                    k = cost(v, w)
                    if k is None:
                        continue
                    t = c + k
                    if w not in nxt or t < nxt[w][0]:
                        nxt[w] = (t, path + [w])
            layer = nxt
        for v, (c, path) in layer.items():
            k = cost(v, v0)           # wrap back to the start of the loop
            if k is None:
                continue
            t = c + k
            if best_c is None or t < best_c:
                best, best_c = path, t
    if best is None:
        raise RuntimeError("no voice-led cycle found for %r" % (chords,))
    return best, best_c


def bass_note(root: int) -> int:
    pc = (KEY_TONIC + root) % 12
    return BASS_LO + ((pc - BASS_LO) % 12)


# --------------------------------------------------------------------------
# 4. Tiny MIDI writer / reader (format 1, 480 PPQ)
# --------------------------------------------------------------------------
def vlq(n: int) -> bytes:
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(out))


def track_bytes(events):
    """events: list of (tick, order, bytes). Sorted, delta-encoded."""
    events = sorted(events, key=lambda e: (e[0], e[1]))
    data = b""
    last = 0
    for tick, _, msg in events:
        data += vlq(tick - last) + msg
        last = tick
    data += vlq(0) + b"\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + data


def meta_name(text):
    b = text.encode("ascii", "replace")
    return b"\xff\x03" + bytes([len(b)]) + b


def note_events(ch, note, start, length, vel):
    return [(start, 1, bytes([0x90 | ch, note, vel])),
            (start + length, 0, bytes([0x80 | ch, note, 0]))]


def build_midi(title, schema, drum, bpm):
    chords = SCHEMAS[schema]
    voicings, _ = best_cycle(chords)

    tempo = [(0, 0, meta_name(title)),
             (0, 0, b"\xff\x51\x03" + struct.pack(">I", int(60_000_000 / bpm))[1:]),
             (0, 0, b"\xff\x58\x04\x04\x02\x18\x08")]
    chord_ev = [(0, 0, meta_name("Chords")), (0, 0, bytes([0xC0, 4]))]    # GM Electric Piano 1
    bass_ev = [(0, 0, meta_name("Bass")), (0, 0, bytes([0xC1, 33]))]      # GM Electric Bass (finger)
    drum_ev = [(0, 0, meta_name("Drums"))]

    for bar in range(BARS):
        t0 = bar * BAR
        ci = bar % len(chords)
        for n in voicings[ci]:
            chord_ev += note_events(0, n, t0, BAR - 10, 78)
        chord_root = chords[ci][0]
        bass_ev += note_events(1, bass_note(chord_root), t0, BAR - 10, 96)
        k, s, h = drum_pattern(drum, bar)
        for st in k:
            drum_ev += note_events(9, KICK, t0 + st * STEP, STEP, 110)
        for st in s:
            drum_ev += note_events(9, SNARE, t0 + st * STEP, STEP, 100)
        for st in h:
            drum_ev += note_events(9, HAT_C, t0 + st * STEP, STEP, 85 if st % 4 == 0 else 65)

    head = b"MThd" + struct.pack(">IHHH", 6, 1, 4, PPQ)
    return head + b"".join(track_bytes(t) for t in (tempo, chord_ev, bass_ev, drum_ev))


def read_midi(path):
    """Return dict(tempo_bpm, timesig, notes=[(tick, ch, note, vel, length)])."""
    b = open(path, "rb").read()
    assert b[:4] == b"MThd", "not a MIDI file"
    fmt, ntr, ppq = struct.unpack(">HHH", b[8:14])
    pos = 14
    notes, tempo, timesig = [], None, None
    for _ in range(ntr):
        assert b[pos:pos + 4] == b"MTrk"
        ln = struct.unpack(">I", b[pos + 4:pos + 8])[0]
        i, end, tick, run = pos + 8, pos + 8 + ln, 0, None
        open_n = {}
        while i < end:
            d = 0
            while True:
                c = b[i]; i += 1
                d = (d << 7) | (c & 0x7F)
                if not c & 0x80:
                    break
            tick += d
            st = b[i]
            if st == 0xFF:
                typ, ln2 = b[i + 1], b[i + 2]
                body = b[i + 3:i + 3 + ln2]
                if typ == 0x51:
                    tempo = 60_000_000 / int.from_bytes(body, "big")
                if typ == 0x58:
                    timesig = (body[0], 2 ** body[1])
                i += 3 + ln2
                continue
            if st & 0x80:
                run = st; i += 1
            status = run
            hi, ch = status & 0xF0, status & 0x0F
            if hi in (0x90, 0x80):
                note, vel = b[i], b[i + 1]; i += 2
                if hi == 0x90 and vel:
                    open_n[(ch, note)] = (tick, vel)
                else:
                    t, v = open_n.pop((ch, note), (tick, 0))
                    notes.append((t, ch, note, v, tick - t))
            elif hi in (0xC0, 0xD0):
                i += 1
            else:
                i += 2
        pos = end
    return {"ppq": ppq, "tempo": tempo, "timesig": timesig, "notes": sorted(notes)}


# --------------------------------------------------------------------------
# 5. Rule checker: reads the FILE back and tests every sourced rule.
# --------------------------------------------------------------------------
def check_file(path, schema, drum, bpm):
    problems = []
    m = read_midi(path)
    chords = SCHEMAS[schema]
    # MIDI gate (project skill): tempo, time signature, drum channel, GM range, non-empty
    if m["tempo"] is None or abs(m["tempo"] - bpm) > 0.5:
        problems.append("tempo missing/wrong")
    if m["timesig"] != (4, 4):
        problems.append("time signature not 4/4")
    drums = [n for n in m["notes"] if n[1] == 9]
    if not drums:
        problems.append("no drum notes on channel 10")
    if any(not (35 <= n[2] <= 81) for n in drums):
        problems.append("drum note outside GM range 35-81")
    if not 80 <= bpm <= 160:
        problems.append("tempo outside 80-160 normal-feel range")

    bars = {}
    for t, ch, note, vel, ln in m["notes"]:
        bars.setdefault(t // BAR, []).append((t % BAR, ch, note))
    if sorted(bars) != list(range(BARS)):
        problems.append("expected %d bars" % BARS)

    prev_up = None
    first_up = None
    for bar in range(BARS):
        ev = bars.get(bar, [])
        up = sorted(n for off, ch, n in ev if ch == 0)
        bass = sorted(n for off, ch, n in ev if ch == 1)
        chord_starts = {off for off, ch, n in ev if ch == 0}
        r, q = chords[bar % len(chords)]
        want = sorted(pcs_of(r, q))
        if chord_starts != {0}:
            problems.append("bar %d: chord does not change on beat 1" % bar)
        if sorted(n % 12 for n in up) != want:
            problems.append("bar %d: chord notes are not the schema chord" % bar)
        if len(bass) != 1 or bass[0] % 12 != (KEY_TONIC + r) % 12:
            problems.append("bar %d: bass is not the chord root" % bar)
        if bass and up and bass[0] >= min(up):
            problems.append("bar %d: bass is not the lowest note" % bar)
        if len(set(n % 12 for n in up)) != 3:
            problems.append("bar %d: chord missing a note" % bar)
        if prev_up is not None and cost(tuple(prev_up), tuple(up)) is None:
            problems.append("bar %d: voice-leading rule broken" % bar)
        prev_up = up
        if first_up is None:
            first_up = up
        # drums
        k = sorted(off // STEP for off, ch, n in ev if ch == 9 and n == KICK)
        s = sorted(off // STEP for off, ch, n in ev if ch == 9 and n == SNARE)
        ek, es, _ = drum_pattern(drum, bar)
        if k != sorted(ek) or s != sorted(es):
            problems.append("bar %d: drums differ from the sourced grid" % bar)
        if 0 not in k:
            problems.append("bar %d: no kick on beat 1" % bar)
        if drum not in ("half-time", "double-time"):
            if not (4 in s and 12 in s):
                problems.append("bar %d: backbeat (steps 4 and 12) missing" % bar)
        elif drum == "half-time" and s != [8]:
            problems.append("bar %d: half-time snare must be on beat 3 only" % bar)
        elif drum == "double-time" and s != [2, 6, 10, 14]:
            problems.append("bar %d: double-time backbeat wrong" % bar)
    # loop wraps smoothly (last chord back to first)
    if prev_up is not None and first_up is not None and cost(tuple(prev_up), tuple(first_up)) is None:
        problems.append("loop wrap: voice-leading rule broken")
    return problems


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    report = []
    ok_all = True
    for title, schema, drum, bpm in BATCH:
        path = os.path.join(out_dir, "%s %dbpm.mid" % (title, bpm))
        with open(path, "wb") as f:
            f.write(build_midi(title, schema, drum, bpm))
        probs = check_file(path, schema, drum, bpm)
        voicings, total = best_cycle(SCHEMAS[schema])
        mx = max(max(abs(a - b) for a, b in zip(voicings[i], voicings[(i + 1) % 4]))
                 for i in range(4))
        report.append((title, schema, drum, bpm, total, mx, probs))
        ok_all = ok_all and not probs
        print(("PASS " if not probs else "FAIL ") + os.path.basename(path)
              + "  biggest voice move %d semitones" % mx)
        for p in probs:
            print("   -", p)
    return ok_all, report


if __name__ == "__main__":
    ok, _ = main(sys.argv[1] if len(sys.argv) > 1 else "theory_loops_out")
    sys.exit(0 if ok else 1)
