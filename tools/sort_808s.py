"""Measure every 808 in the sorted folder: note, length, dirt.

Writes sample_808_index.json in the project root -- the engine reads a
sampled 808's ROOT NOTE from there so it can shift the sample into the
beat's key. Nothing else knows what note an 808 is: 324 of his 411 are
in C (packs ship them that way so you can tune them), which is also why
the folders below split on LENGTH and DIRT and not on note.

  ./.venv/bin/python tools/sort_808s.py            measure + report only
  ./.venv/bin/python tools/sort_808s.py --move     also file them

--move only touches loose files at the top of 808s/; his own subfolders
(Grime) are left alone. Nothing is ever deleted, and a name clash is
skipped rather than overwritten.
"""
import os, sys, json, re
import numpy as np, soundfile as sf

INDEX = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "sample_808_index.json")

D = "/Volumes/TBOTC 3/Sample Packs/BOTC Sorted Samples/808s"
NAMES = ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")
FLAT = {"Db":"C#","Eb":"D#","Gb":"F#","Ab":"G#","Bb":"A#"}
LONG_SECS, DIRTY = 1.5, 0.10


def name_key(stem):
    tail = stem.rsplit(" - ", 1)[-1].strip()
    return tail if tail in NAMES else FLAT.get(tail)


def analyse(path):
    try:
        x, sr = sf.read(path, always_2d=True)
    except Exception:
        return None
    x = x.mean(1).astype(np.float64)
    if len(x) < 4096:
        return None
    e = np.abs(x); pk = e.max()
    if pk < 1e-5:
        return None
    idx = np.where(e > pk * 0.1)[0]
    sustain = (idx[-1] - idx[0]) / sr if len(idx) > 1 else 0.0
    w = min(len(x), int(0.5 * sr))
    X = np.abs(np.fft.rfft(x[:w] * np.hanning(w)))
    fr = np.fft.rfftfreq(w, 1.0 / sr)
    dirt = float(X[fr > 300].sum() / max(X.sum(), 1e-9))
    # note: autocorrelation over the 808 range, 25-200 Hz
    y = x[:int(1.5 * sr)] - x[:int(1.5 * sr)].mean()
    on = int(np.argmax(np.abs(y) > 0.3 * np.abs(y).max()))
    y = y[on:on + int(0.8 * sr)]
    midi = clar = None
    if len(y) >= 4096:
        y = y * np.hanning(len(y))
        n = 1 << (2 * len(y) - 1).bit_length()
        f = np.fft.rfft(y, n)
        ac = np.fft.irfft(f * np.conj(f))[:len(y)]
        if ac[0] > 0:
            ac /= ac[0]
            lo, hi = int(sr / 200.0), int(sr / 25.0)
            seg = ac[lo:hi]
            if len(seg) >= 3 and seg.max() > 0:
                best = float(seg.max())
                pks = np.where((seg[1:-1] >= seg[:-2]) &
                               (seg[1:-1] >= seg[2:]))[0] + 1
                near = [int(p) for p in pks if seg[p] >= 0.9 * best]
                k = (near[0] if near else int(np.argmax(seg))) + lo
                midi = 69.0 + 12.0 * np.log2((sr / k) / 440.0)
                clar = float(ac[k])
    return {"sustain": round(sustain, 2), "dirt": round(dirt, 3),
            "midi": None if midi is None else round(midi, 2),
            "clarity": 0.0 if clar is None else round(clar, 2)}


def bin_of(a):
    return ("Long" if a["sustain"] >= LONG_SECS else "Short",
            "Dirty" if a["dirt"] >= DIRTY else "Clean")


def main(move=False):
    rows = {}
    for dp, _, fs in os.walk(D):
        if os.path.basename(dp) in ("Long", "Short", "Clean", "Dirty"):
            pass
        for f in sorted(fs):
            if not f.lower().endswith((".wav", ".aif", ".aiff")):
                continue
            p = os.path.join(dp, f)
            a = analyse(p)
            if a is None:
                continue
            stem = os.path.splitext(f)[0]
            nk = name_key(stem)
            if nk:
                a["note"], a["note_src"] = nk, "name"
            elif a["midi"] is not None and a["clarity"] >= 0.5:
                a["note"] = NAMES[int(round(a["midi"])) % 12]
                a["note_src"] = "measured"
            else:
                a["note"], a["note_src"] = None, "unclear"
            rows[p] = a
    
    import collections
    cnt = collections.Counter(bin_of(a) for a in rows.values())
    print("%d files" % len(rows))
    for k in sorted(cnt):
        print("  %-6s %-6s %3d" % (k[0], k[1], cnt[k]))
    print("  no note:", sum(1 for a in rows.values() if a["note"] is None))
    json.dump({"_readme": "Measured 808 index. note = detected root, "
                          "sustain = seconds above -20 dB, dirt = share of "
                          "energy above 300 Hz. Rebuild: tools/sort_808s.py",
               "files": rows},
              open(INDEX, "w"), indent=1)
    if not move:
        print("\ndry run. add --move to move the files.")
        return rows
    moved = 0
    for p, a in rows.items():
        if os.path.dirname(p) != D:      # already in a subfolder (Grime) - leave
            continue
        lo, dirt = bin_of(a)
        dest = os.path.join(D, lo, dirt)
        os.makedirs(dest, exist_ok=True)
        tgt = os.path.join(dest, os.path.basename(p))
        if os.path.exists(tgt):
            print("SKIP name clash:", os.path.basename(p)); continue
        os.rename(p, tgt)
        moved += 1
    print("moved", moved)


if __name__ == "__main__":
    main("--move" in sys.argv)
