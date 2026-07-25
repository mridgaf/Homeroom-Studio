"""Build full hip hop tracks (24-bit WAV) from HIS sample library.

Ten 94-100 bpm instrumentals. Each track is one construction-kit family
from the library (bass/melody/drum stems that already share key and tempo)
plus: his drum one-shots layered as a kit, an 808 sub tuned to the family
key, MPC-style equal-slice chops for verse 2, sidechain ducking under the
kick, and the shared mastering chain from make_drum_loops.

RETIRED as a script (2026-07-25) — see the note where build_pool() used to be.
It still matters as a LIBRARY: load_audio, norm_rms and edge_fade are imported
by crew, chord_synth, string_sampler, instrument_sampler and make_drum_beats.
To make beats, run:  ./.venv/bin/python tools/beat_machine.py
"""
import aifc
import contextlib
import os
import struct
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import (SR, bandpass, env, highpass, hat, kick808,
                             lowpass, master, snare808, sub808, write_wav24)

OUT_DIR = Path(os.path.expanduser("~/Music/Claude Hip Hop Tracks"))
rng = np.random.default_rng(94100)

NOTE_FREQ = {"C": 32.70, "C#": 34.65, "D": 36.71, "D#": 38.89, "E": 41.20,
             "F": 43.65, "F#": 46.25, "G": 49.00, "G#": 51.91, "A": 55.00,
             "A#": 58.27, "B": 61.74}

# ------------------------------------------------------------- audio io

def _read_float_wav(p):
    """A 32/64-bit IEEE-float WAV -> (raw bytes, dtype, ch, sr, sampwidth).

    Python's `wave` module refuses format code 3 ("unknown format: 3"), so
    every float WAV in the library was silently unreadable — load_audio
    returned None and the caller quietly skipped the file. Measured
    2026-07-25: 96 of 1418 melodic wavs, ~7% of his instrument material,
    including every 8-bit/arcade FX he owns. Found while answering "do I
    own real chiptune sounds", which is exactly the kind of question that
    was getting a wrong answer. Minimal RIFF chunk walk — no dependency.
    """
    with open(str(p), "rb") as f:
        head = f.read(12)
        if head[:4] != b"RIFF" or head[8:12] != b"WAVE":
            return None
        ch = sr = bits = None
        while True:
            hdr = f.read(8)
            if len(hdr) < 8:
                return None
            cid, sz = hdr[:4], struct.unpack("<I", hdr[4:8])[0]
            body = f.read(sz + (sz & 1))[:sz]
            if cid == b"fmt ":
                code, ch, sr = struct.unpack("<HHI", body[:8])
                bits = struct.unpack("<H", body[14:16])[0]
                if code != 3:                     # not float: let wave try
                    return None
            elif cid == b"data":
                if not bits:
                    return None
                dt = "<f4" if bits == 32 else "<f8" if bits == 64 else None
                return None if dt is None else (body, dt, ch, sr)


def load_audio(path):
    """WAV/AIFF -> float stereo (n, 2) at 44.1k, or None if unreadable."""
    p = Path(path)
    if p.suffix.lower() == ".wav":
        try:
            got = _read_float_wav(p)
        except (OSError, struct.error):
            got = None
        if got is not None:
            raw, dt, ch, sr = got
            x = np.frombuffer(raw, dtype=dt).astype(np.float64)
            ch = max(int(ch or 1), 1)
            x = x[:len(x) - (len(x) % ch)].reshape(-1, ch)
            x = np.column_stack([x[:, 0], x[:, min(1, ch - 1)]])
            if sr and sr != SR:
                m = int(round(len(x) * SR / sr))
                idx = np.linspace(0, len(x) - 1, m)
                x = np.column_stack([np.interp(idx, np.arange(len(x)), x[:, c])
                                     for c in range(2)])
            return x
    try:
        mod = wave if p.suffix.lower() == ".wav" else aifc
        with contextlib.closing(mod.open(str(p), "rb")) as f:
            sw, ch, sr, n = (f.getsampwidth(), f.getnchannels(),
                             f.getframerate(), f.getnframes())
            raw = f.readframes(n)
        big = p.suffix.lower() != ".wav"          # aiff is big-endian
        if sw == 2:
            x = np.frombuffer(raw, dtype=">i2" if big else "<i2").astype(np.float64)
            x /= 2 ** 15
        elif sw == 3:
            b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
            if big:
                b = b[:, ::-1]
            x = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8)
                 | (b[:, 2].astype(np.int32) << 16))
            x = (x - (x >> 23 << 24)).astype(np.float64) / 2 ** 23
        else:
            return None
        x = x.reshape(-1, ch)
        x = np.column_stack([x[:, 0], x[:, min(1, ch - 1)]])
        if sr != SR:
            m = int(round(len(x) * SR / sr))
            idx = np.linspace(0, len(x) - 1, m)
            x = np.column_stack([np.interp(idx, np.arange(len(x)), x[:, c])
                                 for c in range(2)])
        return x
    except Exception:
        return None


def norm_rms(x, db=-18.0):
    r = np.sqrt((x ** 2).mean()) + 1e-12
    return x * (10 ** (db / 20) / r)


def edge_fade(x, ms=5):
    n = min(int(ms / 1000 * SR), len(x) // 2)
    if n:
        x[:n] *= np.linspace(0, 1, n)[:, None]
        x[-n:] *= np.linspace(1, 0, n)[:, None]
    return x

# ------------------------------------------------------------- library

# build_pool() lived here. Retired 2026-07-25 (owner's call): it was the only
# thing in tools/ that imported reason_voice, which broke the portability
# boundary in PACKAGING-GAP-ANALYSIS.md Part 4a — the generator must not depend
# on Reason. It fed main() only, and beat_machine/crew superseded this script
# years of beats ago. Rebuilding it means a sample pool from
# tools/sample_library.scan_packs(); nothing else here needs it.


def find_stem(pool, bpm, sub):
    for e in pool.get(bpm, []):
        if sub.lower() in e["name"].lower():
            return e
    return None


def load_stem(entry, bpm, max_bars=8):
    x = load_audio(entry["path"])
    if x is None:
        return None
    bar = int(round(240 / bpm * SR))
    bars = min(max_bars, max(1, len(x) // bar))
    bars = 2 ** int(np.log2(bars))                # 1/2/4/8 keeps loops even
    x = x[:bars * bar]
    if len(x) < bars * bar:
        x = np.vstack([x, np.zeros((bars * bar - len(x), 2))])
    return edge_fade(norm_rms(x), 6)


def pick_shot(shots, kind, seed_ix, max_secs=1.5):
    cands = shots[kind]
    order = rng.permutation(len(cands))
    for i in order[seed_ix:seed_ix + 60]:
        e = cands[int(i)]
        x = load_audio(e["path"])
        if x is not None and 0.02 < len(x) / SR <= max_secs:
            return e["name"], norm_rms(x, -15.0)
    return None, None

# ------------------------------------------------------------- sequencing

def place(buf, snd, pos, gain=1.0):
    end = min(len(buf), pos + len(snd))
    if 0 <= pos < len(buf):
        buf[pos:end] += snd[:end - pos] * gain


def hits(buf, snd, bar_n, bars, pattern, gain, swing=0.05):
    for b in range(bars):
        for s, ch in enumerate(pattern):
            if ch == "-":
                continue
            vel = {"X": 1.0, "x": 0.72, "o": 0.45, ".": 0.28}[ch]
            t = b * bar_n + int(s / 16 * bar_n)
            if s % 2:
                t += int(swing * bar_n / 16)
            place(buf, snd, t, gain * vel * rng.uniform(0.93, 1.0))


def tile(stem, n):
    reps = int(np.ceil(n / len(stem)))
    return np.tile(stem, (reps, 1))[:n]


def chop_seq(stem, bar_n, bars, seed):
    """MPC move: slice the stem into quarter-bar cells, re-order them."""
    cell = bar_n // 4
    cells = [stem[i * cell:(i + 1) * cell] for i in range(len(stem) // cell)]
    r = np.random.default_rng(seed)
    out = np.zeros((bars * bar_n, 2))
    pos = 0
    while pos < len(out) - cell:
        i = int(r.integers(0, len(cells)))
        if r.random() < 0.55:                     # bias to downbeat cells
            i = (i // 4) * 4
        c = edge_fade(cells[i].copy(), 3)
        reps = 2 if r.random() < 0.15 else 1      # occasional stutter
        for _ in range(reps):
            place(out, c, pos)
            pos += cell
    return out


def duck(buf, kick_positions, depth=0.35, rel=0.11):
    g = np.ones(len(buf))
    L = int(rel * 3 * SR)
    dip = 1 - depth * np.exp(-np.arange(L) / (rel * SR))
    for p in kick_positions:
        end = min(len(g), p + L)
        g[p:end] = np.minimum(g[p:end], dip[:end - p])
    return buf * g[:, None]

# ------------------------------------------------------------- the tracks

# name, bpm, key, family stems (role -> name substring), spice singles
TRACKS = [
    ("Black Sand Heat", 95, "F", {
        "bass": "Black Sand_Bass", "melody": "Black Sand_Elec Pian",
        "hook": "Black Sand_Strings", "hook2": "Black Sand_Choir",
        "perc": "Black Sand_Conga", "drums": "Black Sand_Drums"}, []),
    ("Saturday Corner", 95, "F", {
        "bass": "Saturday_Synth Bass", "melody": "Saturday_Bazooki",
        "hook": "Saturday_Organ", "hook2": "Saturday_Trem String",
        "perc": "Saturday_Perc 1", "drums": "Saturday_Drums"}, []),
    ("Toto's Basement", 95, "C", {
        "bass": "Toto_Bass", "melody": "Toto_Strings",
        "hook": "Toto_Bubble Pad", "hook2": "Toto_Synth Delay",
        "drums": "Toto_Drum C#"}, ["Toto_Bird"]),
    ("Warpath", 95, "C", {
        "bass": "HWIP_Bass", "melody": "HWIP_Piano Sketch",
        "hook": "HWIP_Bell Melody", "hook2": "HWIP_Brass Chords",
        "perc": "HWIP_Skull Shake", "drums": "95 Bpm_HWIP_Drum Loop",
        "fill": "HWIP_Fill", "trans": "HWIP_Orkest Transition 1"}, []),
    ("West Coast 06", 95, "D", {
        "bass": "TR06 West Coast Hit 1", "melody": "TR06 West Coast Melod",
        "drums": "TR06 Just Drums"}, ["victorsdream"]),
    ("Award Season", 100, "C", {
        "bass": "Award_Bass", "melody": "100_Vrink_C",
        "drums": "Award_Drums"}, []),
    ("Hype Machine", 100, "F", {
        "bass": "Hype_Synthtar", "melody": "Hype_Bells",
        "hook": "Hype_Pad", "drums": "Hype_Drums"},
     ["BluebirdSynth_F"]),
    ("This Song Knocks", 100, "D", {
        "bass": "ThisSong_Bass", "melody": "ThisSong_Elec Piano",
        "hook": "TR03 E.Piano", "drums": "ThisSong_Drums"}, []),
    ("Organ Grinder", 100, "A", {
        "bass": "TR09 Gtr Hit 1", "melody": "TR09 Organish",
        "hook": "TR09 Synth Sweep", "drums": "TR09 Just Drums"},
     ["Wavesovblix A"]),
    ("Wyrmvoice", 94, "D", {
        "melody": "094_wyrmvoice"}, ["098_rversal"]),
]

KIT_PATTERNS = {
    "kick":  "X------x--X-----",
    "snare": "----X-------X---",
    "hat":   "x-x-x-x-x-x-x-x-",
}

SECTIONS = [("intro", 4), ("verse", 16), ("hook", 8),
            ("verse2", 16), ("hook", 8), ("outro", 4)]


def build_track(ix, name, bpm, key, stem_map, spice_names, pool, shots, log):
    bar_n = int(round(240 / bpm * SR))
    total = sum(b for _, b in SECTIONS)
    n = total * bar_n + int(2.0 * SR)
    used = []

    stems = {}
    for role, sub in stem_map.items():
        e = find_stem(pool, bpm, sub)
        if e:
            s = load_stem(e, bpm)
            if s is not None:
                stems[role] = s
                used.append(e["name"])
    spice = []
    for sub in spice_names:
        for b in pool:
            e = find_stem(pool, b, sub)
            if e:
                s = load_stem(e, b)
                if s is not None:
                    if b != bpm:                  # vinyl-style speed nudge
                        m = int(round(len(s) * b / bpm))
                        idx = np.linspace(0, len(s) - 1, m)
                        s = np.column_stack([
                            np.interp(idx, np.arange(len(s)), s[:, c])
                            for c in range(2)])
                    spice.append(s)
                    used.append(e["name"])
                break

    kit = {}
    for k in ("kick", "snare", "hat"):
        sname, snd = pick_shot(shots, k, ix * 7)
        if snd is None:                           # synth fallback, still solid
            snd = {"kick": kick808(), "snare": snare808(), "hat": hat()}[k]
            snd = norm_rms(np.column_stack([snd, snd]), -15.0)
            sname = f"(synth {k})"
        kit[k] = snd
        used.append(sname)

    mel_bus = np.zeros((n, 2))                    # ducked bus
    drum_bus = np.zeros((n, 2))
    sub_bus = np.zeros((n, 2))
    kick_pos = []

    melody = stems.get("melody")
    root = NOTE_FREQ[key]
    pos_bar = 0
    for sec, bars in SECTIONS:
        p0 = pos_bar * bar_n
        seg = bars * bar_n
        full = sec in ("verse", "hook", "verse2")

        # melodic bed
        if melody is not None:
            if sec == "verse2":
                bed = chop_seq(melody, bar_n, bars, seed=ix * 31 + 7)
            else:
                bed = tile(melody, seg)
            if sec == "intro":
                bed = lowpass_st(bed, 1200) * 0.8
            if sec == "outro":
                bed = lowpass_st(bed, 800) * 0.7
            place(mel_bus, bed * 0.9, p0)
        if sec == "hook":
            for role, g in (("hook", 0.75), ("hook2", 0.55)):
                if role in stems:
                    place(mel_bus, tile(stems[role], seg) * g, p0)
        if full and "bass" in stems:
            place(mel_bus, highpass_st(tile(stems["bass"], seg), 55), p0)
        if full and "perc" in stems:
            place(drum_bus, tile(stems["perc"], seg) * 0.5, p0)
        if spice and sec in ("hook", "verse2"):
            place(mel_bus, tile(spice[0], min(seg, len(spice[0]))) * 0.4, p0)

        # drums
        if full:
            if "drums" in stems:
                place(drum_bus, tile(stems["drums"], seg) * 0.85, p0)
            for k, pat in KIT_PATTERNS.items():
                gain = {"kick": 0.9, "snare": 0.8, "hat": 0.4}[k]
                sub_pat = pat if sec != "hook" else pat.replace("--X", "-xX")
                b = np.zeros((seg, 2))
                hits(b, kit[k], bar_n, bars, sub_pat, gain)
                place(drum_bus, b, p0)
            for bb in range(bars):
                for s, ch in enumerate(KIT_PATTERNS["kick"]):
                    if ch != "-":
                        kick_pos.append(p0 + bb * bar_n + int(s / 16 * bar_n))
        elif sec == "outro":
            b = np.zeros((seg, 2))
            hits(b, kit["hat"], bar_n, bars, "x-x-x-x-x-x-x-x-", 0.3)
            place(drum_bus, b, p0)

        # 808 sub: root on the kicks, fifth answer in hooks
        if full:
            for bb in range(bars):
                base = p0 + bb * bar_n
                place(sub_bus, mono2st(sub808(root, 0.5)), base, 0.8)
                place(sub_bus, mono2st(sub808(root, 0.35)),
                      base + int(7 / 16 * bar_n), 0.6)
                if sec == "hook" and bb % 2 == 1:
                    place(sub_bus, mono2st(sub808(root * 1.5, 0.3)),
                          base + int(10 / 16 * bar_n), 0.5)

        # kit fills / transitions at section edges
        if "fill" in stems and sec in ("verse", "verse2"):
            place(drum_bus, stems["fill"], p0 + (bars - 1) * bar_n, 0.8)
        if "trans" in stems and sec == "hook":
            place(mel_bus, stems["trans"], p0 + (bars - 1) * bar_n, 0.6)
        pos_bar += bars

    mel_bus = duck(highpass_st(mel_bus, 90), kick_pos)
    mix = mel_bus * 0.9 + drum_bus * 1.0 + sub_bus * 0.95
    end = total * bar_n
    tail = mix[end:]
    mix = mix[:end + len(tail)]
    mix[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]
    L, R = master(mix[:, 0].copy(), mix[:, 1].copy())
    log.append((name, bpm, used))
    return L, R


def mono2st(x):
    return np.column_stack([x, x])


def lowpass_st(x, f):
    return np.column_stack([lowpass(x[:, 0], f), lowpass(x[:, 1], f)])


def highpass_st(x, f):
    return np.column_stack([highpass(x[:, 0], f), highpass(x[:, 1], f)])


def main():
    raise SystemExit(
        "This standalone script is retired — its sample scanner was the last\n"
        "thing tying the beat generator to Reason (see the note where\n"
        "build_pool() used to be). Use the Beat Machine instead:\n"
        "  ./.venv/bin/python tools/beat_machine.py\n"
        "Everything else in this file is still live as a library — load_audio,\n"
        "norm_rms and edge_fade are imported by crew, chord_synth,\n"
        "string_sampler, instrument_sampler and make_drum_beats.")


if __name__ == "__main__":
    main()
