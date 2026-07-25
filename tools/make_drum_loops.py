"""Synthesize a pack of mixed & mastered drum loops (24-bit WAV).

Every sound is generated from scratch the way the original hardware did it:
808 kick = sine wave with a pitch drop, snare = tone + noise snap, hats =
filtered noise. Loops are seamless (the ring-out tail is wrapped back onto
the loop start) and each file gets its BPM in the name so Reason Voice bins
and tempo-search pick it up.

Run:  ./.venv/bin/python tools/make_drum_loops.py
Output: ~/Documents/Samples/Claude Drum Loops/
"""
import io
import os
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT_DIR = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Loops"))
rng = np.random.default_rng(808)

# ---------------------------------------------------------------- helpers

def env(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def fft_gain(x, shape_fn):
    """EQ by shaping the spectrum. shape_fn(freqs) -> linear gain array."""
    X = np.fft.rfft(x)
    X *= shape_fn(np.fft.rfftfreq(len(x), 1 / SR))
    return np.fft.irfft(X, len(x))


def smooth_edge(freqs, f0, width_oct=0.7, rise=True):
    """0..1 raised-cosine edge around f0, width in octaves."""
    lo, hi = f0 * 2 ** (-width_oct / 2), f0 * 2 ** (width_oct / 2)
    t = np.clip((np.log2(np.maximum(freqs, 1)) - np.log2(lo))
                / (np.log2(hi) - np.log2(lo)), 0, 1)
    edge = 0.5 - 0.5 * np.cos(np.pi * t)
    return edge if rise else 1 - edge


def bandpass(x, lo, hi):
    return fft_gain(x, lambda f: smooth_edge(f, lo) * smooth_edge(f, hi, rise=False))


def highpass(x, f0):
    return fft_gain(x, lambda f: smooth_edge(f, f0))


def lowpass(x, f0):
    return fft_gain(x, lambda f: smooth_edge(f, f0, rise=False))

# ---------------------------------------------------------------- drums

def kick808(dur=0.6, f0=170.0, f1=52.0, ptau=0.02, drive=1.0, click=0.6):
    n = int(dur * SR)
    freqs = f1 + (f0 - f1) * np.exp(-np.arange(n) / (ptau * SR))
    body = np.sin(2 * np.pi * np.cumsum(freqs) / SR) * env(n, dur / 4)
    body = np.tanh(body * (1.5 + drive)) / np.tanh(1.5 + drive)
    nc = int(0.004 * SR)
    body[:nc] += highpass(rng.normal(0, 1, nc), 1500) * env(nc, 0.001)[:nc] * click
    return body


def sub808(freq, dur, glide_to=None, drive=1.2):
    n = int(dur * SR)
    f = np.full(n, float(freq))
    if glide_to:
        g0 = int(n * 0.35)
        f[g0:] = freq + (glide_to - freq) * \
            (1 - np.exp(-np.arange(n - g0) / (0.06 * SR)))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = np.tanh(x * drive) / np.tanh(drive)
    a = int(0.005 * SR)
    e = env(n, dur * 0.9)
    e[:a] *= np.linspace(0, 1, a)
    nc = int(0.003 * SR)
    x[:nc] += highpass(rng.normal(0, .8, nc), 2000) * env(nc, 0.001)[:nc] * .5
    return x * e


def snare808(dur=0.35, tone=185.0, snap=1.0):
    n = int(dur * SR)
    t = np.sin(2 * np.pi * tone * np.arange(n) / SR) * env(n, 0.045) * 0.6
    s = bandpass(rng.normal(0, 1, n), 700, 9000) * env(n, 0.09) * 0.8 * snap
    return t + s


def clap(dur=0.5):
    n = int(dur * SR)
    x = np.zeros(n)
    for i, ms in enumerate((0, 11, 23)):
        j = int(ms / 1000 * SR)
        m = int(0.012 * SR)
        x[j:j + m] += rng.normal(0, 1, m) * env(m, 0.004) * (0.8 + 0.1 * i)
    tail = rng.normal(0, 1, n) * env(n, 0.11) * 0.5
    return bandpass(x + tail, 900, 8500)


def hat(dur=0.06, open_=False):
    n = int((0.4 if open_ else dur) * SR)
    metal = sum(np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR))
                for f in (3113, 4160, 5333, 6790))
    x = highpass(rng.normal(0, 1, n) * 0.7 + metal * 0.12, 7200)
    return x * env(n, 0.25 if open_ else 0.018)


def cowbell(dur=0.25):
    n = int(dur * SR)
    x = sum(np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) * g
            for f, g in ((540, .6), (845, .4)))
    return bandpass(x, 400, 3500) * env(n, 0.06)


def tom808(f0=200, f1=88, dur=0.3):
    n = int(dur * SR)
    freqs = f1 + (f0 - f1) * np.exp(-np.arange(n) / (0.03 * SR))
    return np.sin(2 * np.pi * np.cumsum(freqs) / SR) * env(n, 0.1)


def rim(dur=0.08):
    n = int(dur * SR)
    ring = np.sin(2 * np.pi * 1720 * np.arange(n) / SR) * env(n, 0.008)
    return ring + highpass(rng.normal(0, .6, n), 3000) * env(n, 0.003)

# ---------------------------------------------------------------- sequencer

VEL = {"X": 1.0, "x": 0.75, "o": 0.5, ".": 0.3}


def place(buf, sound, pos, vel):
    end = min(len(buf), pos + len(sound))
    if 0 <= pos < len(buf):
        buf[pos:end] += sound[:end - pos] * vel


def render(bpm, bars, tracks, swing=0.0, humanize=0.0):
    """tracks: list of (sound_fn, pan, gain, [bar strings]). Bar strings are
    16 steps; 32 chars means 32nd-note resolution (for hat rolls)."""
    spb = 60.0 / bpm * 4                      # seconds per bar
    loop_n = int(round(spb * bars * SR))
    tail_n = int(1.2 * SR)
    L = np.zeros(loop_n + tail_n)
    R = np.zeros(loop_n + tail_n)
    for sound_fn, pan, gain, barlist in tracks:
        for bar, pattern in enumerate(barlist):
            res = len(pattern)                # 16 or 32 steps per bar
            for step, ch in enumerate(pattern):
                if ch == "-":
                    continue
                t = (bar + step / res) * spb
                if swing and res == 16 and step % 2 == 1:
                    t += swing * spb / 16
                if humanize:
                    t += rng.uniform(-humanize, humanize)
                vel = VEL[ch] * rng.uniform(0.94, 1.0)
                s = sound_fn() * gain * vel
                gl, gr = np.cos(pan * np.pi / 4 + np.pi / 4), \
                    np.sin(pan * np.pi / 4 + np.pi / 4)
                pos = int(t * SR)
                place(L, s, pos, gl)
                place(R, s, pos, gr)
    # seamless loop: fold the ring-out tail back onto the start
    L[:tail_n] += L[loop_n:]
    R[:tail_n] += R[loop_n:]
    return L[:loop_n], R[:loop_n]

# ---------------------------------------------------------------- master

def master(L, R, drive=1.4):
    for x in (L, R):
        x -= x.mean()
    m = 0.5 * (L + R)
    # keep lows mono, add air, tame boxy mids a touch
    def eq(f):
        g = np.ones_like(f)
        g *= 1 + 0.35 * smooth_edge(f, 9000)            # air shelf
        g *= 1 - 0.15 * smooth_edge(f, 300) * smooth_edge(f, 900, rise=False)
        return g
    L, R = fft_gain(L, eq), fft_gain(R, eq)
    side = 0.5 * (L - R)
    side = highpass(side, 200)                           # mono bass
    L, R = m + side, m - side
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
    L, R = L / peak * drive, R / peak * drive            # push into the glue
    L, R = np.tanh(L) / np.tanh(drive), np.tanh(R) / np.tanh(drive)
    peak = max(np.abs(L).max(), np.abs(R).max())
    L, R = L / peak * 0.94, R / peak * 0.94              # ~-0.5 dBFS
    # no edge fades: these files are loops — the tail fold already makes
    # the seam continuous, and a fade dipped the downbeat at every repeat
    # (owner 2026-07-18: "they don't loop right")
    return L, R


def wav24_bytes(L, R):
    """A whole 24-bit stereo WAV as bytes, for handing straight to a
    browser without touching disk."""
    x = np.stack([np.clip(L, -1, 1), np.clip(R, -1, 1)], axis=1)
    ints = (x * (2 ** 23 - 1)).astype("<i4").tobytes()
    data = np.frombuffer(ints, dtype=np.uint8).reshape(-1, 4)[:, :3].tobytes()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(data)
    return buf.getvalue()


def write_wav24(path, L, R):
    Path(path).write_bytes(wav24_bytes(L, R))


def read_wav24(path):
    """(L, R) floats back out of a stem written by write_wav24. Handles
    16- and 32-bit PCM too so an older or hand-edited stem still plays."""
    with wave.open(str(path), "rb") as w:
        ch, sw, n = w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if sw == 3:                       # 24-bit: pad each sample out to 32
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        x = np.zeros((len(b), 4), dtype=np.uint8)
        x[:, 1:] = b                  # low byte 0 -> the value scales by 256
        vals = x.view("<i4").reshape(-1) / (2 ** 31 - 1)
    else:
        dt = {1: np.uint8, 2: "<i2", 4: "<i4"}.get(sw)
        if dt is None:
            raise ValueError(f"{path}: {sw * 8}-bit wav not supported")
        vals = np.frombuffer(raw, dtype=dt).astype(np.float64)
        vals = (vals - 128) / 128 if sw == 1 else vals / float(2 ** (sw * 8 - 1))
    vals = vals.reshape(-1, ch)
    return (vals[:, 0], vals[:, 1]) if ch > 1 else (vals[:, 0], vals[:, 0])

# ---------------------------------------------------------------- loops

K, S, C, H, O, B, T, RM = (lambda: kick808(), lambda: snare808(),
                           lambda: clap(), lambda: hat(),
                           lambda: hat(open_=True), lambda: cowbell(),
                           lambda: tom808(), lambda: rim())

OLD_SCHOOL = [
    ("808 Drums - Boom Bap Corner", 92, 0.06, 0.002, [
        (K, 0.0, 1.0, ["X------x--X-----"] * 3 + ["X------x--X---x-"]),
        (S, 0.0, 0.85, ["----X-------X---"] * 4),
        (H, 0.35, 0.4, ["x-x-x-x-x-x-x-x-"] * 4),
        (O, -0.3, 0.35, ["--------------x-"] * 4),
    ]),
    ("808 Drums - Electro Planet", 112, 0.0, 0.0, [
        (K, 0.0, 1.0, ["X---------X-----", "X---------X---x-"] * 2),
        (S, 0.0, 0.8, ["----X-------X---"] * 4),
        (C, 0.15, 0.55, ["----x-------x---"] * 4),
        (H, -0.35, 0.42, ["xoxoxoxoxoxoxoxo"] * 4),
        (B, 0.4, 0.3, ["--x---x---x--x--"] * 4),
    ]),
    ("808 Drums - Uptown Swing", 96, 0.09, 0.003, [
        (K, 0.0, 1.0, ["X-----x---X--x--"] * 3 + ["X-----x---X-x-x-"]),
        (S, 0.0, 0.85, ["----X--.----X---"] * 4),
        (H, 0.3, 0.4, ["x-xox-x-x-xox-x-"] * 4),
        (RM, -0.4, 0.4, ["-------x--------"] * 4),
    ]),
    ("808 Drums - Cowbell Funk", 104, 0.05, 0.002, [
        (K, 0.0, 1.0, ["X--x-----xX-----"] * 4),
        (S, 0.0, 0.8, ["----X-------X---"] * 4),
        (H, 0.3, 0.38, ["x-x-x-x-x-x-x-x-"] * 4),
        (B, -0.35, 0.42, ["x--x--x---x--x--"] * 4),
        (T, 0.45, 0.5, ["--------------x-"] * 3 + ["----------xx--x-"]),
    ]),
    ("808 Drums - Slow Roller", 84, 0.07, 0.003, [
        (K, 0.0, 1.0, ["X-------x-X-----"] * 4),
        (S, 0.0, 0.85, ["--------X-------"] * 4),
        (H, 0.3, 0.36, ["x--xx--xx--xx--x"] * 4),
        (O, -0.3, 0.32, ["------x---------"] * 4),
        (RM, 0.45, 0.35, ["-----------x----"] * 4),
    ]),
]

def sub_a(): return sub808(55.0, 0.45)
def sub_slide(): return sub808(55.0, 0.6, glide_to=41.2)
def sub_f(): return sub808(43.65, 0.5)
def sub_rage(): return sub808(49.0, 0.5, drive=6.0)
def kick_hard(): return kick808(dur=0.4, f0=220, f1=54, drive=3.0, click=1.0)

MODERN = [
    ("Trap Drums - Cannon", 140, 0.0, 0.0, [
        (kick_hard, 0.0, 0.95, ["X-----X---X-----"] * 3 + ["X-----X-----X---"]),
        (sub_a, 0.0, 0.9, ["X-----------X---"] * 4),
        (C, 0.1, 0.8, ["--------X---------------X-------"] * 4),
        (H, 0.3, 0.42, ["x-x-x-x-x-x-xxxxx-x-x-x-xxx-x-x-"] * 3
         + ["x-x-x-x-xxxxxxxxx-x-x-x-xxxxxxxx"]),
        (O, -0.35, 0.3, ["------x---------"] * 4),
    ]),
    ("Drill Drums - Slide", 144, 0.0, 0.0, [
        (kick_hard, 0.0, 0.9, ["X-------X--X----"] * 4),
        (sub_slide, 0.0, 0.95, ["X----------X----"] * 4),
        (S, 0.1, 0.75, ["--------X-----X-"] * 4),
        (H, -0.3, 0.4, ["x--xx--xx--xx--x"] * 4),
    ]),
    ("Trap Drums - Rage Distortion", 150, 0.0, 0.0, [
        (kick_hard, 0.0, 0.85, ["X-----X---X-----"] * 4),
        (sub_rage, 0.0, 1.0, ["X-----X-----X---"] * 4),
        (C, 0.12, 0.8, ["--------X-------"] * 4),
        (H, 0.32, 0.4, ["xxxxxxxxxxxxxxxx"] * 3 + ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]),
        (O, -0.3, 0.3, ["--x-------x-----"] * 4),
    ]),
    ("Trap Drums - Half-Time Stomper", 130, 0.0, 0.0, [
        (kick_hard, 0.0, 1.0, ["X------------x--"] * 3 + ["X---------x--x--"]),
        (sub_f, 0.0, 0.92, ["X-------------x-"] * 4),
        (C, 0.0, 0.85, ["--------X-------"] * 4),
        (H, 0.3, 0.4, ["x-x-x-x-x-x-x-x-x-x-x-x-x-xxx-x-"] * 4),
        (T, -0.4, 0.45, ["-------------x--"] * 3 + ["---------x---xx-"]),
    ]),
    ("Trap Drums - Festival", 160, 0.0, 0.0, [
        (kick_hard, 0.0, 0.95, ["X-------X---X---"] * 4),
        (sub_a, 0.0, 0.88, ["X-------X-------"] * 4),
        (S, 0.1, 0.8, ["--------X-------"] * 4),
        (C, -0.12, 0.6, ["--------X-------"] * 4),
        (H, 0.33, 0.44, ["x-xxx-xxx-xxx-xx"] * 3
         + ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]),
        (O, -0.33, 0.3, ["----x-------x---"] * 4),
    ]),
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, bpm, swing, human, tracks in OLD_SCHOOL + MODERN:
        L, R = render(bpm, 4, tracks, swing=swing, humanize=human)
        L, R = master(L, R)
        path = OUT_DIR / f"{name} {bpm}bpm.wav"
        write_wav24(path, L, R)
        secs = len(L) / SR
        rms = 20 * np.log10(np.sqrt(0.5 * (L ** 2 + R ** 2).mean()) + 1e-12)
        print(f"  {path.name:44s} {secs:5.2f}s  RMS {rms:5.1f} dBFS")
    print(f"\n{len(OLD_SCHOOL) + len(MODERN)} loops -> {OUT_DIR}")


if __name__ == "__main__":
    main()
