"""Recipes, MIDI + stems export, and the sample-usage history for the
Beat Machine (owner spec 2026-07-16, dj-drone-machine-spec.md).

- Every render saves a RECIPE at <beats root>/.recipes/NN.json: the final
  preset, every sample path, and the treatment — enough to rebuild the
  exact beat with ONE drum swapped ("same beat, different snare").
- Every render also ships as MIDI (same basename, .mid) and per-lane
  24-bit stems (a "NN ... Stems" folder) so a beat drops straight into
  Reason 12 for editing; the WAV stays the instant-listen reference.
- ~/.reason_voice/sample_history.json remembers each DJ's recent drums so
  no recent kick/snare/hat comes back across generations — the spec's
  anti-repetition hard rule, surviving between sessions.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import write_wav24

HIST = Path(os.path.expanduser("~/.reason_voice/sample_history.json"))
HIST_KEEP = 6                    # recent picks remembered per DJ per lane

# General MIDI drum notes (channel 10) per lane; numbered stamp lanes
# (collab guests) strip their digits before lookup. The second block maps
# the composer's guest lanes (pattern_gen extras).
GM_NOTE = {"kick": 36, "snap": 37, "snare": 38, "clap": 39, "hat": 42,
           "perc": 63, "bongo": 61, "stamp": 49,
           "shaker": 70, "rims": 37, "toms": 47, "foundfx": 55,
           "cutfx": 55, "congas2": 64, "exotic2": 65, "blips": 80,
           "clicks": 75, "woods": 76, "crash2": 57, "swellfx": 55,
           "risers": 55, "bells": 56, "impacts": 49, "sirens": 55,
           "glitches": 75, "mathperc": 77}

# ------------------------------------------------------------------- MIDI


def _vlq(n):
    """MIDI variable-length quantity."""
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(out))


def write_midi(path, events, bpm, tpq=480, tsig=(4, 4)):
    """Format-1 SMF: a tempo track plus one track per lane, note events
    on channel 10. The humanized timing (swing, per-lane offsets, jitter)
    is baked into the tick positions so the groove survives the import;
    velocities are normalized per lane (accents survive, mix balance is
    the Reason mixer's job). tsig writes the time-signature meta so a
    3/4 or 6/8 beat lands on the right grid in Reason."""
    spq = 60.0 / bpm
    tempo = int(round(60000000 / bpm))
    num, den = tsig
    dd = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}.get(den, 2)
    t0 = (b"\x00\xff\x51\x03" + tempo.to_bytes(3, "big")
          + b"\x00\xff\x58\x04" + bytes([num, dd, 24, 8])
          + b"\x00\xff\x2f\x00")
    chunks = [b"MTrk" + len(t0).to_bytes(4, "big") + t0]
    lanes = [(ln, evs) for ln, evs in events.items() if evs]
    for lane, evs in lanes:
        note = GM_NOTE.get(lane.rstrip("0123456789"), 47)
        vmax = max(v for _, v in evs)
        msgs = []
        for t, v in evs:
            tick = int(round(t / spq * tpq))
            vel = int(np.clip(round(30 + 97 * v / vmax), 1, 127))
            msgs.append((tick, 0, 0x99, note, vel))          # note on
            msgs.append((tick + tpq // 4, 1, 0x89, note, 64))  # note off
        msgs.sort()
        nm = lane.encode()
        data = bytearray(b"\x00\xff\x03" + bytes([len(nm)]) + nm)
        last = 0
        for tick, _, status, nt, vel in msgs:
            data += _vlq(tick - last) + bytes([status, nt, vel])
            last = tick
        data += b"\x00\xff\x2f\x00"
        chunks.append(b"MTrk" + len(data).to_bytes(4, "big") + bytes(data))
    head = (b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big")
            + (1 + len(lanes)).to_bytes(2, "big") + tpq.to_bytes(2, "big"))
    Path(path).write_bytes(head + b"".join(chunks))


# ------------------------------------------------------------------ stems


def write_stems(folder, stems):
    """One 24-bit stereo wav per lane. Filenames stay number-free so the
    global beat numbering (next_number's rglob) never counts them."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for lane, (sL, sR) in stems.items():
        write_wav24(folder / f"{lane}.wav", sL, sR)
    return folder


# ---------------------------------------------------------------- recipes


def recipe_dir(root):
    return Path(root) / ".recipes"


def save_recipe(root, no, data):
    d = recipe_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{no}.json").write_text(json.dumps(data, indent=1))


def load_recipe(root, no):
    f = recipe_dir(root) / f"{int(no)}.json"
    if not f.exists():
        have = sorted(int(p.stem) for p in recipe_dir(root).glob("*.json")
                      if p.stem.isdigit())
        hint = (f"beats {have[0]}-{have[-1]} have recipes" if have
                else "no beats have recipes yet — only beats made from "
                     "2026-07-16 on can be swapped")
        raise FileNotFoundError(f"No recipe saved for beat {no} ({hint}).")
    return json.loads(f.read_text())


# ---------------------------------------------------------------- history


def _load_hist():
    try:
        return json.loads(HIST.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def history_avoid(names):
    """Every sample any of these DJs used recently — feed it to the
    picker's avoid set. _pick_path already waives the avoid list when a
    role's pool runs dry, so a small library degrades gracefully."""
    h = _load_hist()
    return {p for n in names
            for lst in h.get(n, {}).values() for p in lst}


def record_history(lane_parents, sources):
    """Remember what just got used. lane_parents maps lane -> the DJ whose
    taste picked it (host for solos, the lane's parent in a collab);
    stamps are locked identities, not picks, so they're skipped."""
    h = _load_hist()
    for lane, path in sources.items():
        dj = lane_parents.get(lane)
        if not path or not dj or lane.startswith("stamp"):
            continue
        lst = h.setdefault(dj, {}).setdefault(lane, [])
        if path in lst:
            lst.remove(path)
        lst.insert(0, path)
        del lst[HIST_KEEP:]
    HIST.parent.mkdir(parents=True, exist_ok=True)
    HIST.write_text(json.dumps(h, indent=1))
