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
import re
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
GM_NOTE = {"kick": 36, "sub": 35, "snap": 37, "snare": 38, "clap": 39, "hat": 42,
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


def write_midi(path, events, bpm, tpq=480, tsig=(4, 4), chords=None):
    """Format-1 SMF: a tempo track plus one track per lane, note events
    on channel 10. The humanized timing (swing, per-lane offsets, jitter)
    is baked into the tick positions so the groove survives the import;
    velocities are normalized per lane (accents survive, mix balance is
    the Reason mixer's job). tsig writes the time-signature meta so a
    3/4 or 6/8 beat lands on the right grid in Reason.

    `chords` (punch list step 7, 2026-07-22) is an optional list of
    {"start_sec", "dur_sec", "notes": [midi, ...]} dicts — harmony.py's
    exact chord voicings, written as a real polyphonic track on channel
    1 (not 10, so Reason doesn't read it as a drum hit). Every existing
    call site omits it, so old behavior is untouched."""
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
    if chords:
        msgs = []
        for c in chords:
            on = int(round(c["start_sec"] / spq * tpq))
            off = int(round((c["start_sec"] + c["dur_sec"]) / spq * tpq))
            for note in c["notes"]:
                msgs.append((on, 0, 0x90, note, 90))
                msgs.append((off, 1, 0x80, note, 64))
        msgs.sort()
        nm = b"chords"
        data = bytearray(b"\x00\xff\x03" + bytes([len(nm)]) + nm)
        last = 0
        for tick, _, status, nt, vel in msgs:
            data += _vlq(max(tick - last, 0)) + bytes([status, nt, vel])
            last = tick
        data += b"\x00\xff\x2f\x00"
        chunks.append(b"MTrk" + len(data).to_bytes(4, "big") + bytes(data))
    ntracks = len(lanes) + (1 if chords else 0)
    head = (b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big")
            + (1 + ntracks).to_bytes(2, "big") + tpq.to_bytes(2, "big"))
    Path(path).write_bytes(head + b"".join(chunks))


# ------------------------------------------------------------------ stems


# Stems print at TRACK volume: what a stem sounds like on its own is
# exactly its level in the beat (owner 2026-07-25). This replaced a +6 dB
# print (his 2026-07-21 call, "solo stems are too quiet to sample") — he
# asked for it to go so previewing a stem and hearing the mix agree.
# Left as a knob, not deleted: set non-zero to bring the hot print back.
STEM_BOOST_DB = 0.0

# What each lane is CALLED, for the stem filename and the rack row. Three
# separate low sounds, three separate words (owner 2026-07-25, his exact
# distinction — these had been used interchangeably and it hid what was
# actually playing):
#   kick drum — the punchy drum sample
#   bass drum — the long low 808 boom under it (sampled 808 or tuned sub)
#   bass      — the melodic low LINE that follows the chords
# `sub` and `bass` are mutually exclusive in a preset (see
# _add_sample_lanes), so they never collide as filenames.
LANE_LABELS = {"kick": "kick drum", "sub": "bass drum", "bass": "bass drum"}


def lane_label(lane):
    """The owner-facing name for a lane — 'bass' the 808 drum is a BASS
    DRUM; the melodic line lives on bass0..N and is just 'bass'."""
    return LANE_LABELS.get(lane, lane)


_AUDIO_SUFFIXES = (".wav", ".aif", ".aiff", ".mp3", ".flac",
                   ".ogg", ".m4a")


def write_stems(folder, stems, sources=None):
    """One 24-bit stereo wav per lane. When `sources` maps lane -> the
    sample file it was built from, the stem carries the REAL sample name
    ("kick drum - Cymatics Kong Kick 9.wav") — owner 2026-07-18: show
    WHICH drum was used, not a generic role name. The lane prefix keeps
    filenames starting with a letter, so the global beat numbering
    (next_number's leading-digit rglob) never counts them."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    empty = []
    for lane, (sL, sR) in stems.items():
        # 2026-07-31: never write a stem that is digital silence. Measured
        # 17 of 506 stems (3.4%, across 15 of 60 beats) were all zeros while
        # still being listed as live lanes — e.g. beat 1623's "blips" had a
        # real sample, pan 0.30 and gain 0.26, but a pattern with ZERO hits
        # in every bar, so the renderer faithfully produced nothing. Dragging
        # that file into Reason gets you an empty track. Skipping it here is
        # the containment fix; the upstream cause (a lane can be dealt into
        # the kit with an empty pattern) is still open.
        if float(max(np.abs(sL).max(), np.abs(sR).max())) <= 0.0:
            empty.append(lane_label(lane))
            continue
        name = lane_label(lane)
        src = (sources or {}).get(lane)
        if src:
            # a source is EITHER a real sample path or a free-text
            # description the renderer wrote ("horns stack, Dm7 (ii7)",
            # "synth 808 sub, root F", "Kick 9.wav  [Cutz's stamp]").
            # Path().stem on a description truncates it at the first dot
            # and throws away everything before a slash — measured
            # 2026-09-01: "Cymatics Piano 2.5, Dm7 (ii7)" printed as
            # "Cymatics Piano 2", losing the chord. So only strip a
            # suffix when the source really is an audio file.
            raw = str(src)
            if Path(raw).suffix.lower() in _AUDIO_SUFFIXES:
                raw = Path(raw).stem
            real = re.sub(r'[\\/:*?"<>|]', "_", raw).strip()
            if real:
                name = f"{name} - {real}"
        g = 10 ** (STEM_BOOST_DB / 20.0)
        peak = float(max(np.abs(sL).max(), np.abs(sR).max()))
        if peak * g > 0.94:
            g = max(1.0, 0.94 / peak)
        write_wav24(folder / f"{name}.wav", sL * g, sR * g)
    if empty:
        print(f"  note: {len(empty)} lane(s) made no sound, so no stem was "
              f"written for them: {', '.join(empty)}")
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
