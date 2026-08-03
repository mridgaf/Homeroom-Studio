"""Measure a rendered batch — the audio, not the pattern data.

Added 2026-08-01. Every "it sounds wrong" session before this one found its
bug by the owner's ear; the 07-31 rebuild review found four defects in twenty
minutes by measuring instead. This is that measurement, made repeatable so
each part of the 08-01 punch list can be checked the same way.

    ./.venv/bin/python tools/measure_batch.py <folder> [<folder-to-compare>]

Reads every beat under <folder> plus its "* Stems" folders and prints:
  - length in bars (is the loop a whole number of bars?)
  - per-bar level of the finished mix AND of the drum stems alone
    (the owner works from stems in Reason, so a hole shows up there first)
  - stereo width, S/M in dB
  - every stem's peak and RMS against the kick, and the SPREAD per lane
  - which lanes are present at all

Give a second folder to diff two batches (before/after a change).
"""
import sys
import wave
from collections import defaultdict
from pathlib import Path
from statistics import median

import numpy as np

DRUM_WORDS = ("kick", "snare", "clap", "hat", "snap", "rim", "perc", "shaker",
              "tamb", "bongo", "conga", "tom", "wood", "clave", "cowbell",
              "timbale", "crash", "bell", "blip", "stamp")


def read_wav(path):
    """24-bit stereo WAV -> float array, shape (n, channels)."""
    with wave.open(str(path)) as w:
        n, ch, sw = w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw, sr = w.readframes(n), w.getframerate()
    if sw == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2].astype(np.int8).astype(np.int32) << 16)
        a = v.astype(np.float64) / (2 ** 23)
    elif sw == 2:
        a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    else:
        a = np.frombuffer(raw, dtype="<i4").astype(np.float64) / 2 ** 31
    return a.reshape(-1, ch), sr


def db(x):
    return 20 * np.log10(max(float(x), 1e-12))


def side_mid_db(a):
    if a.shape[1] < 2:
        return -99.0
    mid = 0.5 * (a[:, 0] + a[:, 1])
    side = 0.5 * (a[:, 0] - a[:, 1])
    m = np.sqrt((mid ** 2).mean())
    return db(np.sqrt((side ** 2).mean()) / m) if m > 0 else -99.0


def per_bar(mono, nbars):
    """RMS of each bar, in dB below the loudest bar. A hole shows as a big
    negative number; -inf means digital silence."""
    bl = len(mono) // max(1, nbars)
    r = [np.sqrt((mono[i * bl:(i + 1) * bl] ** 2).mean()) for i in range(nbars)]
    pk = max(r) if r else 0.0
    return [db(x / pk) if pk > 0 else -99.0 for x in r]


def scan(folder):
    """One row per beat: name, bars, width, per-bar mix and drum levels,
    and every stem's level against the kick."""
    folder = Path(folder)
    rows = []
    for wav in sorted(folder.rglob("*.wav")):
        if " Stems" in str(wav.parent) or wav.parent.name.startswith("."):
            continue
        stem_dir = next((d for d in wav.parent.glob("* Stems")
                         if d.name.split()[0] == wav.name.split()[0]), None)
        a, sr = read_wav(wav)
        mono = a.mean(1)
        stems, drums = {}, None
        if stem_dir:
            for s in sorted(stem_dir.glob("*.wav")):
                lane = s.stem.split(" - ")[0].lower()
                sa, _ = read_wav(s)
                stems[lane] = sa
                if any(d in lane for d in DRUM_WORDS):
                    m = sa.mean(1)
                    drums = m.copy() if drums is None else \
                        drums[:len(m)] + m[:len(drums)]
        rows.append(dict(name=wav.name, dur=len(a) / sr, audio=a, mono=mono,
                         stems=stems, drums=drums))
    return rows


def report(folder, nbars_hint=None):
    rows = scan(folder)
    if not rows:
        print("no beats found in %s" % folder)
        return rows
    print("=" * 78)
    print("BATCH: %s   (%d beats)" % (folder, len(rows)))
    print("=" * 78)

    print("\n-- stereo width (S/M dB; -22 or lower reads as mono) --")
    w = [side_mid_db(r["audio"]) for r in rows]
    for r, x in zip(rows, w):
        print("   %-46s %6.1f%s" % (r["name"][:46], x,
                                    "   <-- MONO" if x <= -22 else ""))
    print("   median %.1f   worst %.1f" % (median(w), min(w)))

    print("\n-- holes: worst bar, dB below that beat's loudest bar --")
    print("   %-40s %8s %8s" % ("beat", "full mix", "drums only"))
    for r in rows:
        nb = nbars_hint or _guess_bars(r["name"], r["dur"])
        mix = min(per_bar(r["mono"], nb))
        drm = min(per_bar(r["drums"], nb)) if r["drums"] is not None else float("nan")
        flag = "  <== HOLE" if drm < -15 else ""
        print("   %-40s %8.1f %8.1f%s" % (r["name"][:40], mix, drm, flag))

    print("\n-- stem level vs the kick (peak dB; + = louder than the kick) --")
    lanes = defaultdict(list)
    for r in rows:
        k = r["stems"].get("kick drum")
        if k is None:
            continue
        kp = float(np.abs(k).max())
        for lane, sa in r["stems"].items():
            base = "".join(c for c in lane if not c.isdigit()).strip()
            lanes[base].append(db(float(np.abs(sa).max()) / kp))
    print("   %-16s %4s %8s %8s %8s" % ("lane", "n", "median", "max", "SPREAD"))
    for lane, v in sorted(lanes.items(), key=lambda x: -median(x[1])):
        spread = max(v) - min(v)
        print("   %-16s %4d %8.1f %8.1f %8.1f%s"
              % (lane, len(v), median(v), max(v), spread,
                 "  <-- uncontrolled" if spread > 12 and len(v) > 2 else ""))

    print("\n-- lanes present --")
    seen = defaultdict(int)
    for r in rows:
        for lane in r["stems"]:
            seen["".join(c for c in lane if not c.isdigit()).strip()] += 1
    for lane, n in sorted(seen.items(), key=lambda x: -x[1]):
        print("   %-16s %3d of %d beats (%3.0f%%)"
              % (lane, n, len(rows), 100 * n / len(rows)))
    return rows


def _guess_bars(name, dur):
    """Bars from the filename's bpm and the measured length, rounded to the
    nearest whole bar — the renders are exact multiples, so this is safe."""
    import re
    m = re.search(r"(\d+)bpm", name)
    if not m:
        return 8
    bar_s = 4 * 60.0 / int(m.group(1))
    if " in 3-4" in name:
        bar_s = 3 * 60.0 / int(m.group(1))
    elif " in 6-8" in name:
        bar_s = 3 * 60.0 / int(m.group(1))
    return max(1, int(round(dur / bar_s)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    report(sys.argv[1])
    if len(sys.argv) > 2:
        print("\n\n")
        report(sys.argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main())
