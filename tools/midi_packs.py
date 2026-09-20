"""MIDI ingestion (punch list step 4, 2026-07-19).

The harmony half of "point it at your own sample bank". This reads the
MIDI packs sitting in the same pack roots the drum scanner already
walks (`sample_packs.json`) — 273 files today, mostly Cymatics.

Why MIDI first, before any audio: **MIDI is already notes.** There is no
pitch detection here and therefore nothing to get wrong — the file says
C-Eb-G, so the chord IS C minor. Audio loops need key AND tempo
detection (punch list steps 5-6) and both can be wrong; this can't. It
is the safe seed material for the harmony generator, which is the whole
reason it's built ahead of the audio path.

The packs label their own key in the file name ("... 12 - C Min.mid").
That label is treated as a CROSS-CHECK, not as truth: the key is
detected from the notes, and `scan()` records whether the two agree so
a mislabeled file shows up as a disagreement instead of quietly
poisoning a beat. Run this module directly for that report.

    ./.venv/bin/python tools/midi_packs.py            # library report
    ./.venv/bin/python tools/midi_packs.py --demo     # chords in a key
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import mido                                              # noqa: E402

from key_context import (KeyContext, MODES, SHARPS,              # noqa: E402
                        mode_family, name_chord)
from sample_library import load_midi_roots, load_midi_sorted_root  # noqa: E402

CACHE = Path(os.path.expanduser("~/.reason_voice/midi_index.json"))
MIDI_EXTS = {".mid", ".midi"}
DRUM_CHANNEL = 9                    # 0-indexed: "channel 10" in every DAW

# folder/file words -> what this MIDI is FOR. First match wins, so
# "Essential Chord MIDI" beats a generic "MIDI".
ROLE_WORDS = [
    ("drum", ("HIHAT", "HI HAT", "HI-HAT", "DRUM", "PERC", "KICK",
              "SNARE", "CLAP", "GROOVE", "BEAT")),
    ("chord", ("CHORD", "HARMON", "PROGRESSION", "PAD")),
    ("bass", ("BASS", "808", "SUB")),
    ("melody", ("MELOD", "LEAD", "ARP", "TOPLINE", "PLUCK")),
]

# BOTC Sorted MIDI folder name -> role (folder wins over file name there)
SORTED_FOLDER_ROLE = {"chords": "chord", "chord": "chord",
                      "melody": "melody", "bass": "bass",
                      "drums": "drum", "drum": "drum"}

# "Cymatics - Python MIDI 12 - C# Min.mid" -> ("C#", "minor")
KEY_IN_NAME = re.compile(
    r"(?:^|[\s\-_])([A-G][#b]?)\s*(min|maj)", re.I)


def key_in_name(name):
    """The key the pack ITSELF claims, from the file name, or None."""
    hit = KEY_IN_NAME.search(str(name))
    if not hit:
        return None
    try:
        return KeyContext(hit.group(1),
                          "minor" if hit.group(2).lower() == "min"
                          else "major")
    except ValueError:
        return None


def read_notes(path):
    """Every note in a MIDI file as (start, end, note, velocity), with
    times in BEATS — not seconds, because these phrases get dropped onto
    a beat at whatever tempo the beat is, and the file's own tempo is
    just the tempo it happened to be auditioned at.

    Drum-channel notes are dropped: on channel 10 a "note" is a drum
    key, not a pitch, and feeding those to a key detector is nonsense.
    """
    mf = mido.MidiFile(str(path))
    tpq = mf.ticks_per_beat or 480
    sounding = {}
    notes = []
    now = 0
    for msg in mido.merge_tracks(mf.tracks):
        now += msg.time
        if msg.type not in ("note_on", "note_off"):
            continue
        if getattr(msg, "channel", 0) == DRUM_CHANNEL:
            continue
        if msg.type == "note_on" and msg.velocity > 0:
            sounding.setdefault(msg.note, []).append((now, msg.velocity))
        else:                                    # note_off, or on at vel 0
            queue = sounding.get(msg.note)
            if queue:
                start, vel = queue.pop(0)
                notes.append((start / tpq, now / tpq, msg.note, vel))
    for note, queue in sounding.items():         # never released: hold to end
        for start, vel in queue:
            notes.append((start / tpq, now / tpq, note, vel))
    notes.sort()
    return notes


def _weights(notes):
    """Pitch-class weights by how LONG each note sounds. A held root
    should outvote a passing 16th, which counting note-ons wouldn't do."""
    total = [0.0] * 12
    low = [0.0] * 12
    if not notes:
        return total, low
    split = sorted(n for _, _, n, _ in notes)[len(notes) // 2]
    for start, end, note, vel in notes:
        held = max(end - start, 0.0625)          # a 16th is the floor
        total[note % 12] += held
        if note <= split:                        # the bottom half = the bass
            low[note % 12] += held
    return total, low


def detect_key(notes):
    """The key these notes are in, as a KeyContext.

    Scores all 24 candidates (12 roots x major/minor) on how much of the
    sounding weight lands inside the scale, then leans on the bass to
    break the tie that pure scale content CAN'T break: A minor and C
    major contain identical notes, and only the anchor note tells them
    apart. That's song-keys.md's 808 root rule doing the deciding.
    """
    weight, low = _weights(notes)
    if not sum(weight):
        return None
    best = None
    for pc in range(12):
        for mode in ("minor", "major"):
            scale = set((pc + step) % 12 for step in MODES[mode])
            score = (sum(weight[n] for n in scale)
                     + 0.8 * weight[pc]                    # tonic
                     + 0.3 * weight[(pc + 7) % 12]         # its fifth
                     + 1.2 * low[pc])                      # the bass anchor
            if best is None or score > best[0]:
                best = (score, pc, mode)
    return KeyContext(SHARPS[best[1]], best[2])


def progression(notes, grid=0.25):
    """The chords in a phrase, in order:
    [(start beat, root pitch class, quality, [midi notes]), ...].

    Sampled at every note onset quantized to a 16th, so a chord that was
    played slightly rolled (these packs are humanized — the notes of one
    stab land a tick or two apart) still reads as ONE chord. Consecutive
    identical stacks collapse, so a chord held for a bar is one entry.
    """
    if not notes:
        return []
    snapped = [(round(start / grid) * grid, end, note)
               for start, end, note, _ in notes]
    out = []
    for when in sorted(set(start for start, _, _ in snapped)):
        stack = sorted(note for start, end, note in snapped
                       if start <= when < end)
        if len(stack) < 2:
            continue
        named = name_chord(stack, min(stack) % 12)
        if not named:
            continue
        root, quality = named
        if out and out[-1][1:3] == (root, quality):
            continue                              # same chord, still ringing
        out.append((when, root, quality, stack))
    return out


def _role(parts, notes):
    """What this MIDI is for. The pack's own folders say it most of the
    time; when they don't, the notes do — three-plus notes at once is a
    chord part, one at a time is a melody."""
    for part in reversed(parts):
        up = part.upper()
        for role, words in ROLE_WORDS:
            if any(w in up for w in words):
                return role
    stacks = progression(notes)
    if stacks and sum(len(s[3]) >= 3 for s in stacks) > len(stacks) / 2:
        return "chord"
    return "melody"


def scan(roots=None):
    """Walk the pack roots -> a list of MIDI entries with their key,
    chords, and length. Falls back to the last good scan when the drive
    is unplugged, the same way the drum scanner does.

    Do not change this back to load_roots() -- that's the DRUM switch
    and finds 0 of these files (2026-09-15 fix, same starvation bug as
    the 2026-09-13 instrument fix and the 2026-09-14 loop fix)."""
    roots = roots if roots is not None else load_midi_roots()
    sorted_root = str(load_midi_sorted_root() or "").rstrip("/").lower()
    found = []
    seen_any = False
    for root in roots:
        rootp = Path(os.path.expanduser(root))
        if not rootp.exists():
            continue
        seen_any = True
        is_sorted = str(root).rstrip("/").lower() == sorted_root
        for path in sorted(rootp.rglob("*")):
            if path.suffix.lower() not in MIDI_EXTS or not path.is_file():
                continue
            try:
                notes = read_notes(path)
            except Exception:                     # a malformed file is data
                continue                          # we don't have, not a crash
            parts = path.relative_to(rootp).parts
            role = _role(list(parts), notes)
            if is_sorted and len(parts) > 1:
                # BOTC Sorted MIDI: the FOLDER he filed it in is the
                # answer (Chords/Melody/Bass/Drums), never the file name
                # (owner 2026-09-19, same rule as the other sorted folders)
                role = SORTED_FOLDER_ROLE.get(parts[0].lower(), role)
            entry = {"name": path.stem, "path": str(path), "kind": "midi",
                     "role": role, "notes": len(notes),
                     "beats": round(max((e for _, e, _, _ in notes),
                                        default=0.0), 3)}
            if role != "drum" and notes:
                heard = detect_key(notes)
                claimed = key_in_name(path.name)
                entry["key"] = heard.root
                entry["mode"] = heard.mode
                entry["claimed"] = str(claimed) if claimed else None
                entry["agrees"] = bool(claimed) and claimed == heard
                entry["chords"] = [(round(t, 3), r, q)
                                   for t, r, q, _ in progression(notes)]
            found.append(entry)
    if not seen_any:                              # drive unplugged
        try:
            return json.loads(CACHE.read_text())
        except (OSError, ValueError):
            return []
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(found))
    except OSError:
        pass
    return found


def in_key(index, key, role="chord"):
    """The MIDI phrases worth reaching for in a given key: exact matches
    first, then everything else in the same mode FAMILY (any root),
    because a phrase in the right family transposes into the key
    cleanly — that's what KeyContext.shift_from is for.

    Matches on FAMILY, not the exact mode name — same fix as
    melodic_loops.in_key (2026-07-24): these packs only ever get
    detected as plain major/minor (detect_key scores just those two),
    never a modal name, so comparing straight against an exotic beat
    mode (harmonic_minor, phrygian_dominant, ...) matched nothing and
    silently starved this pool for every beat not in a plain major or
    minor key. Found 2026-09-15 verifying the "midi" chord_source wiring
    live: forcing chord_source to 100% "midi" still never produced a
    midi-sourced chord because most rolled beat keys are modal."""
    want_family = mode_family(key.mode)
    want = [e for e in index if e.get("role") == role and e.get("key")]
    hit = [e for e in want
           if e["key"] == key.root and mode_family(e["mode"]) == want_family]
    spot = set(e["path"] for e in hit)
    return hit + [e for e in want
                  if mode_family(e["mode"]) == want_family
                  and e["path"] not in spot]


def _report():
    index = scan()
    if not index:
        print("No MIDI found. Is the sample drive plugged in?")
        return
    print("%d MIDI files in the pack roots\n" % len(index))
    roles = {}
    for e in index:
        roles[e["role"]] = roles.get(e["role"], 0) + 1
    for role in sorted(roles, key=lambda r: -roles[r]):
        print("  %-7s %4d" % (role, roles[role]))

    # the honest bit: the packs label their own key, so the detector can
    # be graded against 200+ ground-truth labels instead of vibes
    graded = [e for e in index if e.get("claimed")]
    if graded:
        agree = sum(e["agrees"] for e in graded)
        root_only = sum(e["claimed"].split()[0] == e["key"] for e in graded)
        print("\nkey detection vs the packs' own file-name labels:")
        print("  root + mode  %3d/%3d  (%.0f%%)"
              % (agree, len(graded), 100.0 * agree / len(graded)))
        print("  root only    %3d/%3d  (%.0f%%)"
              % (root_only, len(graded), 100.0 * root_only / len(graded)))
        for e in graded:
            if not e["agrees"]:
                print("    heard %-10s pack says %-10s  %s"
                      % ("%s %s" % (e["key"], e["mode"]),
                         e["claimed"], e["name"][:52]))


def _demo(root="F", mode="minor"):
    """Punch list steps 1 + 4, end to end: take a beat's KEY, pull a
    real chord phrase out of the owner's MIDI pack, and put it in that
    key."""
    key = KeyContext(root, mode)
    index = scan()
    picks = in_key(index, key)
    if not picks:
        print("No chord MIDI found. Is the sample drive plugged in?")
        return
    src = picks[0]
    notes = read_notes(src["path"])
    from_key = KeyContext(src["key"], src["mode"])
    shift = key.shift_from(from_key)

    print("beat key : %s   (808 root %s = %.2f Hz)"
          % (key, key.root, key.hz))
    print("source   : %s" % Path(src["path"]).name)
    print("           %s, %s -> transposed %+d semitones\n"
          % (from_key, "%d beats" % round(src["beats"]), shift))
    print("  %-6s %-8s %-6s %s" % ("beat", "chord", "numeral", "midi notes"))
    for when, pc, quality, stack in progression(notes):
        pc = (pc + shift) % 12
        moved = [n + shift for n in stack]
        print("  %-6s %-8s %-6s %s"
              % (round(when, 2), key.chord_name(pc, quality),
                 key.roman(pc, quality), moved))


if __name__ == "__main__":
    if "--demo" in sys.argv:
        _demo(*[a for a in sys.argv[1:] if not a.startswith("-")])
    else:
        _report()
