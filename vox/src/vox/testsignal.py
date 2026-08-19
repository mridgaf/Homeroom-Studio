"""
Synthetic vocal generator with GROUND TRUTH.

Why this exists: to prove a de-noiser or de-reverber works you must know exactly
what the noise and the reverb were. With a real stem you never do. This builds a
vocal from a source-filter model and hands back the clean reference alongside the
degraded version, so cleanup performance is a number (SNR improvement, ERLE,
spectral distortion) instead of an opinion.

Model:
  glottal source  : Liljencrants-Fant (LF) pulse train, with jitter + shimmer
  vocal tract     : time-varying formant resonators (vowel targets, interpolated)
  fricatives      : shaped noise bursts (s / sh / f)
  plosives        : silence -> impulse -> aspiration (p / t / k)
  degradations    : room IR (image-source), broadband + hum noise floor,
                    proximity boom, harsh sibilance, mild clipping
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sig

# Formant tables (F1, F2, F3, F4 in Hz) - adult male-ish; scale for other voices.
VOWELS = {
    "iy": (270, 2290, 3010, 3500),   # "ee"
    "ih": (390, 1990, 2550, 3400),
    "eh": (530, 1840, 2480, 3400),
    "ae": (660, 1720, 2410, 3300),
    "aa": (730, 1090, 2440, 3400),   # "ah"
    "ao": (570, 840, 2410, 3300),
    "uh": (640, 1190, 2390, 3300),
    "uw": (300, 870, 2240, 3300),    # "oo"
    "er": (490, 1350, 1690, 3300),
}
BW = (60, 90, 120, 180)  # formant bandwidths


def lf_pulse(n: int, fs: float, f0: float, oq: float = 0.6, alpha: float = 0.8):
    """One glottal period, Liljencrants-Fant-ish differentiated flow."""
    t = np.arange(n) / fs
    T = 1.0 / f0
    te = oq * T
    y = np.zeros(n)
    m = t < te
    # rising exponential-modulated sinusoid during open phase
    wg = np.pi / te
    y[m] = np.exp(alpha * t[m] / te) * np.sin(wg * t[m])
    # return phase
    m2 = (t >= te) & (t < T)
    if m2.any():
        ta = 0.08 * T
        y[m2] = -np.exp(-(t[m2] - te) / ta) * y[m].max() * 0.35
    return y


def glottal_train(dur, fs, f0_curve, jitter=0.012, shimmer=0.06, seed=0):
    """Pulse train with cycle-to-cycle period (jitter) and amplitude (shimmer)
    perturbation. Real voices have ~0.5-1% jitter; more sounds rough."""
    rs = np.random.RandomState(seed)
    n = int(dur * fs)
    out = np.zeros(n + fs)
    pos = 0
    while pos < n:
        f0 = float(np.interp(pos / fs, np.linspace(0, dur, len(f0_curve)), f0_curve))
        f0 *= (1.0 + jitter * rs.randn())
        f0 = max(f0, 50.0)
        per = int(fs / f0)
        p = lf_pulse(per, fs, f0)
        amp = 1.0 + shimmer * rs.randn()
        out[pos:pos + per] += p * amp
        pos += per
    return out[:n]


def formant_filter(x, fs, formants, bws=BW):
    """Cascade of resonant biquads = vocal tract."""
    y = x.copy()
    for f, bw in zip(formants, bws):
        if f >= fs / 2:
            continue
        r = np.exp(-np.pi * bw / fs)
        theta = 2 * np.pi * f / fs
        b = [1 - r]                      # normalise peak roughly
        a = [1.0, -2 * r * np.cos(theta), r * r]
        y = sig.lfilter(b, a, y)
    return y


def _seg_envelope(n, attack, release, fs):
    e = np.ones(n)
    na, nr = int(attack * fs), int(release * fs)
    na, nr = min(na, n // 2), min(nr, n // 2)
    if na: e[:na] = np.linspace(0, 1, na) ** 2
    if nr: e[-nr:] = np.linspace(1, 0, nr) ** 2
    return e


def fricative(n, fs, kind="s", seed=0):
    """Shaped noise. 's' peaks ~6-8k, 'sh' ~3-4k, 'f' broad and low-level."""
    rs = np.random.RandomState(seed)
    x = rs.randn(n)
    if kind == "s":
        b, a = sig.butter(4, [4500 / (fs / 2), min(11000 / (fs / 2), 0.99)], "band")
        g = 1.0
    elif kind == "sh":
        b, a = sig.butter(4, [1800 / (fs / 2), min(6000 / (fs / 2), 0.99)], "band")
        g = 0.9
    else:  # f / th
        b, a = sig.butter(2, [1000 / (fs / 2), min(9000 / (fs / 2), 0.99)], "band")
        g = 0.35
    return sig.lfilter(b, a, x) * g * _seg_envelope(n, 0.02, 0.03, fs)


def plosive(n, fs, kind="p", seed=0):
    """Closure silence, burst, then aspiration. 'p' has the big LF thump."""
    rs = np.random.RandomState(seed)
    y = np.zeros(n)
    nclose = int(0.045 * fs)
    burst = min(int(0.008 * fs), n - nclose)
    if burst <= 0:
        return y
    b0 = nclose
    imp = rs.randn(burst) * np.exp(-np.linspace(0, 6, burst))
    if kind == "p":
        b, a = sig.butter(2, 900 / (fs / 2), "low")
        imp = sig.lfilter(b, a, imp) * 3.0            # plosive thump
    elif kind == "t":
        b, a = sig.butter(2, 3000 / (fs / 2), "high")
        imp = sig.lfilter(b, a, imp)
    y[b0:b0 + burst] = imp
    asp = n - (b0 + burst)
    if asp > 0:
        a_n = rs.randn(asp) * np.exp(-np.linspace(0, 8, asp)) * 0.25
        y[b0 + burst:] = a_n
    return y


def room_ir(fs, rt60=0.45, size=1.0, seed=1, pre_delay_ms=8.0):
    """Simple synthetic room: sparse early reflections + exponentially decaying
    noise tail. Returns a normalised IR. rt60 is the ground truth we test against."""
    rs = np.random.RandomState(seed)
    n = int(max(rt60 * 1.5, 0.2) * fs)
    ir = np.zeros(n)
    ir[0] = 1.0
    pd = int(pre_delay_ms * 1e-3 * fs)
    # early reflections
    for k in range(12):
        d = pd + int(rs.uniform(0.004, 0.055) * fs * size)
        if d < n:
            ir[d] += rs.uniform(-0.6, 0.6) * np.exp(-3.0 * d / fs / rt60)
    # diffuse tail
    tail_start = pd + int(0.03 * fs)
    t = np.arange(n - tail_start) / fs
    tail = rs.randn(len(t)) * np.exp(-6.9078 * t / rt60)
    # tails are darker than early energy
    b, a = sig.butter(2, min(6000 / (fs / 2), 0.99), "low")
    ir[tail_start:] += sig.lfilter(b, a, tail) * 0.35
    return ir / np.max(np.abs(ir))


def build_phrase(fs=48000, seed=0, voice="male"):
    """A short sung/spoken phrase with sibilance and plosives baked in."""
    rs = np.random.RandomState(seed)
    scale = 1.0 if voice == "male" else 1.17
    f0_base = 118.0 if voice == "male" else 210.0

    # (kind, payload, duration_s)
    script = [
        ("plos", "p", 0.10), ("vow", "ae", 0.20), ("fric", "s", 0.13),
        ("vow", "iy", 0.26), ("plos", "t", 0.08), ("vow", "aa", 0.30),
        ("fric", "sh", 0.14), ("vow", "ao", 0.22), ("sil", None, 0.12),
        ("vow", "eh", 0.24), ("fric", "s", 0.16), ("vow", "uw", 0.34),
        ("plos", "p", 0.09), ("vow", "er", 0.20), ("fric", "s", 0.12),
        ("vow", "iy", 0.40), ("sil", None, 0.18),
    ]

    parts = []
    for i, (kind, payload, dur) in enumerate(script):
        n = int(dur * fs)
        if kind == "sil":
            parts.append(np.zeros(n))
        elif kind == "fric":
            parts.append(fricative(n, fs, payload, seed=seed + i) * 0.30)
        elif kind == "plos":
            parts.append(plosive(n, fs, payload, seed=seed + i) * 0.5)
        else:
            # pitch contour with vibrato and a phrase-level drift
            t = np.linspace(0, dur, 64)
            vib = 1.0 + 0.018 * np.sin(2 * np.pi * 5.2 * t)
            drift = 1.0 + 0.06 * np.sin(2 * np.pi * 0.35 * (i / 4.0 + t))
            f0c = f0_base * vib * drift * (1.0 + 0.10 * rs.randn() * 0.3)
            src = glottal_train(dur, fs, f0c, seed=seed + i)
            fm = tuple(f * scale for f in VOWELS[payload])
            v = formant_filter(src, fs, fm)
            v *= _seg_envelope(n if len(v) == n else len(v), 0.025, 0.045, fs)[:len(v)]
            parts.append(v[:n] if len(v) >= n else np.pad(v, (0, n - len(v))))

    x = np.concatenate(parts)
    # radiation characteristic: lips differentiate -> +6 dB/oct
    x = sig.lfilter([1.0, -0.97], [1.0], x)
    x /= (np.max(np.abs(x)) + 1e-12)
    return x * 0.5


def degrade(clean, fs, rt60=0.45, noise_db=-52.0, hum_db=-58.0,
            proximity_db=5.0, sibilance_db=6.0, seed=2):
    """
    Apply KNOWN degradations. Returns (dirty, truth) where truth records exactly
    what was added so cleanup can be scored against it.
    """
    rs = np.random.RandomState(seed)
    x = clean.copy()

    # proximity effect: LF shelf boost
    if proximity_db:
        f0 = 160.0
        A = 10 ** (proximity_db / 40)
        w0 = 2 * np.pi * f0 / fs
        alpha = np.sin(w0) / 2 * np.sqrt(2)
        c = np.cos(w0)
        b = [A * ((A + 1) - (A - 1) * c + 2 * np.sqrt(A) * alpha),
             2 * A * ((A - 1) - (A + 1) * c),
             A * ((A + 1) - (A - 1) * c - 2 * np.sqrt(A) * alpha)]
        a = [(A + 1) + (A - 1) * c + 2 * np.sqrt(A) * alpha,
             -2 * ((A - 1) + (A + 1) * c),
             (A + 1) + (A - 1) * c - 2 * np.sqrt(A) * alpha]
        x = sig.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)

    # harsh sibilance: narrow presence-band resonance
    if sibilance_db:
        f0, Q = 7200.0, 2.5
        A = 10 ** (sibilance_db / 40)
        w0 = 2 * np.pi * f0 / fs
        alpha = np.sin(w0) / (2 * Q)
        b = [1 + alpha * A, -2 * np.cos(w0), 1 - alpha * A]
        a = [1 + alpha / A, -2 * np.cos(w0), 1 - alpha / A]
        x = sig.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)

    dry = x.copy()

    # room
    ir = room_ir(fs, rt60=rt60, seed=seed)
    wet = sig.fftconvolve(x, ir)[: len(x)]
    wet *= np.sqrt(np.mean(x ** 2) / (np.mean(wet ** 2) + 1e-20)) * 0.42
    x = x + wet

    # noise floor: broadband + mains hum + harmonics
    rms = np.sqrt(np.mean(dry ** 2)) + 1e-20
    nz = rs.randn(len(x))
    b, a = sig.butter(1, 8000 / (fs / 2), "low")
    nz = sig.lfilter(b, a, nz)
    nz *= (10 ** (noise_db / 20)) * rms / (np.sqrt(np.mean(nz ** 2)) + 1e-20)

    t = np.arange(len(x)) / fs
    hum = sum((0.6 ** k) * np.sin(2 * np.pi * 60 * (k + 1) * t + rs.rand())
              for k in range(4))
    hum *= (10 ** (hum_db / 20)) * rms / (np.sqrt(np.mean(hum ** 2)) + 1e-20)

    noise = nz + hum
    x = x + noise

    truth = {
        "clean_dry": dry,      # after tone problems, before room/noise
        "pristine": clean,     # before everything
        "reverb": wet,
        "noise": noise,
        "ir": ir,
        "rt60": rt60,
        "noise_db_rel": noise_db,
        "hum_db_rel": hum_db,
        "hum_f0": 60.0,
        "sibilance_hz": 7200.0,
        "sibilance_db": sibilance_db,
        "proximity_hz": 160.0,
        "proximity_db": proximity_db,
        "input_snr_db": 20 * np.log10(rms / (np.sqrt(np.mean(noise ** 2)) + 1e-20)),
    }
    peak = np.max(np.abs(x))
    if peak > 0.98:
        x = x / peak * 0.98
    return x, truth


def make_testbench(fs=48000, seed=0, voice="male", **kw):
    clean = build_phrase(fs=fs, seed=seed, voice=voice)
    dirty, truth = degrade(clean, fs, seed=seed + 2, **kw)
    return dirty, truth
