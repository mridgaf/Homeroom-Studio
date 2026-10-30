"""Build riff_tables.json: short single-note riffs by style (2026-10-29).

Owner pick 2026-10-29 ("iReal chords + Lakh riffs"): most beats carry the
music with a short riff, not full chords, and riff notes come from BOTH
his MIDI pack melodies and real songs.

Sources:
- "rap" / "rnb": the Lakh MIDI Dataset (Raffel 2016, CC BY 4.0), the files
  matched to the Million Song Dataset, split by the tagtraum CD2 genre
  labels (Schreiber 2015). These are transcriptions of real records; their
  single-note lines run ~3 notes a bar inside about an octave.
- "pack": his own melody MIDI (tools/midi_packs.py index), top line only.

A riff here is a 2-bar (8-beat) single-note phrase. From Lakh it must
REPEAT inside its song at least twice note-for-note (a hook comes back;
a solo doesn't). Notes are stored key-relative so the engine can drop a
riff into any key: [start beat, length beats, semitones from the tonic,
velocity]. Nothing in the engine plays this file yet.

    ./.venv/bin/python tools/build_riff_tables.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import mido                                              # noqa: E402

import midi_packs                                        # noqa: E402

LAKH = Path("/Volumes/TBOTC 3/Datasets/Lakh")
OUT = Path(__file__).resolve().parent.parent / "riff_tables.json"
GENRES = {"Rap": "rap", "RnB": "rnb"}
BAR = 4.0
WIN = 8.0                  # 2 bars
NOTES = (3, 16)            # notes per riff, min and max
MAX_SPAN = 15              # semitones, lowest to highest note
TOP = 400                  # riffs kept per style
# GM programs that carry a line rather than a bass or a pad: pianos,
# chromatic perc, organs, guitars, leads, synth/brass/reed/pipe
LINE_PROGS = (set(range(0, 32)) | set(range(56, 88)) | set(range(104, 112)))


def _tracks(path):
    """{(track, channel, program): [(start, end, note, vel)]} in beats."""
    mf = mido.MidiFile(str(path))
    tpq = mf.ticks_per_beat or 480
    out = collections.defaultdict(list)
    for ti, tr in enumerate(mf.tracks):
        now, prog, on = 0, {}, {}
        for m in tr:
            now += m.time
            if m.type == "program_change":
                prog[m.channel] = m.program
            elif m.type in ("note_on", "note_off") and m.channel != 9:
                k = (m.channel, m.note)
                if m.type == "note_on" and m.velocity:
                    on[k] = (now, m.velocity)
                elif k in on:
                    s, v = on.pop(k)
                    out[(ti, m.channel, prog.get(m.channel, 0))].append(
                        (s / tpq, now / tpq, m.note, v))
    return out


def _top_line(notes):
    """One note per onset (the highest), so a stacked line reads as a line."""
    best = {}
    for s, e, n, v in notes:
        k = round(s * 4)
        if k not in best or n > best[k][2]:
            best[k] = (s, e, n, v)
    return [best[k] for k in sorted(best)]


def _windows(line, tonic):
    """Every 2-bar window of a line -> (pattern key, riff notes)."""
    if not line:
        return
    end = max(e for _, e, _, _ in line)
    w0 = 0.0
    while w0 < end:
        inside = [x for x in line if w0 <= x[0] < w0 + WIN]
        w0 += WIN
        if not NOTES[0] <= len(inside) <= NOTES[1]:
            continue
        pitches = [n for _, _, n, _ in inside]
        if max(pitches) - min(pitches) > MAX_SPAN or len(set(pitches)) < 2:
            continue
        # tonic in the octave at or below the riff's lowest note
        base = min(pitches) - ((min(pitches) - tonic) % 12)
        riff = [[round((s - (w0 - WIN)) * 4) / 4,
                 round(min(e - s, WIN) * 4) / 4 or 0.25, n - base, v]
                for s, e, n, v in inside]
        key = tuple((r[0], r[2]) for r in riff)
        yield key, riff


def lakh(style_of):
    """Riffs from Lakh songs whose MSD id has one of GENRES' labels."""
    found = collections.defaultdict(dict)       # style -> key -> [riff, tracks it repeats in]
    for tid, genre in style_of.items():
        d = LAKH / "lmd_matched" / tid[2] / tid[3] / tid[4] / tid
        if not d.is_dir():
            continue
        files = sorted(d.iterdir())
        if not files:
            continue
        try:
            tracks = _tracks(files[0])
        except Exception:                       # broken MIDI: skip the song
            continue
        every = [x for v in tracks.values() for x in v]
        key = midi_packs.detect_key(every)
        if key is None:
            continue
        style = GENRES[genre]
        for (_, _, prog), notes in tracks.items():
            if prog not in LINE_PROGS:
                continue
            reps = collections.Counter()
            first = {}
            for k, riff in _windows(_top_line(notes), key.pc):
                reps[k] += 1
                first.setdefault(k, riff)
            for k, c in reps.items():
                if c >= 2:                      # it comes back: a hook
                    row = found[style].setdefault(k, [first[k], 0])
                    row[1] += 1
    return found


def packs():
    """Riffs from his own pack melody MIDI, top line, every 2-bar window."""
    found = {}
    for e in midi_packs.scan():
        if e.get("role") != "melody":
            continue
        try:
            notes = midi_packs.read_notes(e["path"])
        except Exception:
            continue
        key = midi_packs.detect_key(notes)
        if key is None:
            continue
        for k, riff in _windows(_top_line(notes), key.pc):
            row = found.setdefault(k, [riff, 0, e["name"]])
            row[1] += 1
    return found


def build():
    cls = LAKH / "msd_tagtraum_cd2.cls"
    if not cls.exists():
        sys.exit("Lakh / tagtraum files not found under %s (drive mounted?)"
                 % LAKH)
    style_of = {}
    for line in cls.read_text().splitlines():
        if line and line[0] != "#":
            tid, g = line.split("\t")[:2]
            if g in GENRES:
                style_of[tid] = g
    out = {"_readme": __doc__.strip().splitlines()[0] +
           " Built by tools/build_riff_tables.py; note = [start beat, "
           "length beats, semitones from tonic, velocity].", "styles": {}}
    for style, rows in lakh(style_of).items():
        best = sorted(rows.values(), key=lambda r: -r[1])[:TOP]
        out["styles"][style] = {"source": "lakh",
                                "riffs": [{"notes": r, "seen": c}
                                          for r, c in best]}
    rows = packs()
    out["styles"]["pack"] = {"source": "his packs", "riffs": [
        {"notes": r, "from": name} for r, _, name in rows.values()]}
    OUT.write_text(json.dumps(out, indent=0, ensure_ascii=False))
    for s, v in out["styles"].items():
        print(s, len(v["riffs"]), "riffs")


if __name__ == "__main__":
    build()
