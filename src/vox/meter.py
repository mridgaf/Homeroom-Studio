"""
Measurement primitives. Everything here is a REFERENCE implementation used to
prove claims -- it is not in the audio path.

Implements:
  - ITU-R BS.1770-4 K-weighting + gated loudness (I, S, M) and LRA (EBU R128 / EBU Tech 3342)
  - True-peak (dBTP) via 4x polyphase oversampling per BS.1770-4 Annex 2
  - Sample peak, RMS, crest factor
  - Null test between two signals
  - Aliasing / THD+N measurement for nonlinear stages
  - DC offset

All functions take float64 arrays shaped (n,) mono or (n, ch).
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sig

EPS = 1e-20


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _as2d(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = x[:, None]
    return x


def db(x: float) -> float:
    return 20.0 * np.log10(max(abs(x), EPS))


# ----------------------------------------------------------------------------
# BS.1770-4 K-weighting
# ----------------------------------------------------------------------------
def k_weighting_coeffs(fs: float):
    """
    Stage 1: high-shelf ("head" filter). Stage 2: high-pass (RLB).

    BS.1770-4 tabulates coefficients at 48 kHz only. To stay sample-rate
    agnostic we re-derive both biquads from their analog prototypes and
    bilinear-transform them at `fs`, which reproduces the tabulated 48 kHz
    values to <1e-6.
    """
    # --- Stage 1: high-frequency shelving boost, +4 dB above ~1681 Hz, Q=1/sqrt(2)
    f0 = 1681.974450955533
    G = 3.999843853973347          # dB
    Q = 0.7071752369554196

    K = np.tan(np.pi * f0 / fs)
    Vh = np.power(10.0, G / 20.0)
    Vb = np.power(Vh, 0.4996667741545416)
    a0_ = 1.0 + K / Q + K * K
    b = np.array([
        (Vh + Vb * K / Q + K * K) / a0_,
        2.0 * (K * K - Vh) / a0_,
        (Vh - Vb * K / Q + K * K) / a0_,
    ])
    a = np.array([
        1.0,
        2.0 * (K * K - 1.0) / a0_,
        (1.0 - K / Q + K * K) / a0_,
    ])

    # --- Stage 2: RLB high-pass, fc ~38 Hz
    f0b = 38.13547087602444
    Qb = 0.5003270373238773
    Kb = np.tan(np.pi * f0b / fs)
    denom = 1.0 + Kb / Qb + Kb * Kb
    b2 = np.array([1.0, -2.0, 1.0])
    a2 = np.array([
        1.0,
        2.0 * (Kb * Kb - 1.0) / denom,
        (1.0 - Kb / Qb + Kb * Kb) / denom,
    ])
    return (b, a), (b2, a2)


def k_weight(x: np.ndarray, fs: float) -> np.ndarray:
    (b1, a1), (b2, a2) = k_weighting_coeffs(fs)
    x = _as2d(x)
    y = sig.lfilter(b1, a1, x, axis=0)
    y = sig.lfilter(b2, a2, y, axis=0)
    return y


# channel weights G: L, R, C, Ls, Rs  (BS.1770-4 Table 3)
_G = np.array([1.0, 1.0, 1.0, 1.41, 1.41])


def _block_powers(x: np.ndarray, fs: float, block_s: float, overlap: float):
    """Mean-square of K-weighted signal per gating block, summed over channels."""
    y = k_weight(x, fs)
    n, ch = y.shape
    bl = int(round(block_s * fs))
    hop = int(round(bl * (1.0 - overlap)))
    if n < bl:
        return np.empty(0), np.empty((0, ch))
    starts = np.arange(0, n - bl + 1, hop)
    g = _G[:ch] if ch <= 5 else np.ones(ch)
    z = np.empty((len(starts), ch))
    for i, s in enumerate(starts):
        seg = y[s:s + bl]
        z[i] = np.mean(seg * seg, axis=0)
    loud = -0.691 + 10.0 * np.log10(np.maximum(z @ g, EPS))
    return loud, z


def loudness_integrated(x: np.ndarray, fs: float) -> float:
    """Gated integrated loudness in LUFS (BS.1770-4: 400 ms blocks, 75% overlap,
    absolute gate -70 LUFS then relative gate at -10 LU below the ungated mean)."""
    x = _as2d(x)
    loud, z = _block_powers(x, fs, 0.400, 0.75)
    if loud.size == 0:
        return float("-inf")
    ch = x.shape[1]
    g = _G[:ch] if ch <= 5 else np.ones(ch)

    keep = loud > -70.0
    if not keep.any():
        return float("-inf")
    # ungated (above absolute gate) mean power -> relative threshold
    mean_pow = np.mean(z[keep], axis=0) @ g
    gamma_r = -0.691 + 10.0 * np.log10(max(mean_pow, EPS)) - 10.0
    keep2 = keep & (loud > gamma_r)
    if not keep2.any():
        return float("-inf")
    final_pow = np.mean(z[keep2], axis=0) @ g
    return float(-0.691 + 10.0 * np.log10(max(final_pow, EPS)))


def loudness_short_term(x: np.ndarray, fs: float) -> np.ndarray:
    """3 s window, 1 s hop -> LUFS-S series."""
    loud, _ = _block_powers(_as2d(x), fs, 3.0, 2.0 / 3.0)
    return loud


def loudness_momentary(x: np.ndarray, fs: float) -> np.ndarray:
    """400 ms window, 100 ms hop -> LUFS-M series."""
    loud, _ = _block_powers(_as2d(x), fs, 0.400, 0.75)
    return loud


def loudness_range(x: np.ndarray, fs: float) -> float:
    """EBU Tech 3342 LRA, in LU."""
    st = loudness_short_term(x, fs)
    st = st[st > -70.0]
    if st.size < 2:
        return 0.0
    # relative gate at -20 LU below the mean of the absolute-gated blocks
    mean_l = -0.691 + 10.0 * np.log10(np.mean(np.power(10.0, (st + 0.691) / 10.0)))
    st = st[st > mean_l - 20.0]
    if st.size < 2:
        return 0.0
    return float(np.percentile(st, 95) - np.percentile(st, 10))


# ----------------------------------------------------------------------------
# peaks
# ----------------------------------------------------------------------------
def sample_peak_db(x: np.ndarray) -> float:
    return db(float(np.max(np.abs(_as2d(x)))))


def true_peak_db(x: np.ndarray, fs: float, oversample: int = 4) -> float:
    """
    BS.1770-4 Annex 2: attenuate 12.04 dB, oversample >= 4x with a 48-tap/phase
    polyphase FIR, take the peak, undo the attenuation.
    For fs > 96 kHz, 2x is sufficient per the spec.
    """
    x = _as2d(x)
    if fs > 96000:
        oversample = 2
    n_taps = 48 * oversample + 1
    h = sig.firwin(n_taps, 1.0 / oversample, window=("kaiser", 8.0))
    h = h * oversample
    pk = 0.0
    for c in range(x.shape[1]):
        up = np.zeros(len(x) * oversample)
        up[::oversample] = x[:, c]
        y = sig.lfilter(h, [1.0], up)
        pk = max(pk, float(np.max(np.abs(y))))
    return db(pk)


def crest_factor_db(x: np.ndarray) -> float:
    x = _as2d(x)
    r = float(np.sqrt(np.mean(x * x)))
    p = float(np.max(np.abs(x)))
    return db(p) - db(r)


def dc_offset_db(x: np.ndarray) -> float:
    x = _as2d(x)
    return db(float(np.max(np.abs(np.mean(x, axis=0)))))


# ----------------------------------------------------------------------------
# verification tests
# ----------------------------------------------------------------------------
def null_test_db(a: np.ndarray, b: np.ndarray) -> float:
    """Peak level of (a - b) in dBFS. Bypass paths must null below -120."""
    a, b = _as2d(a), _as2d(b)
    n = min(len(a), len(b))
    return db(float(np.max(np.abs(a[:n] - b[:n]))))


def aliasing_floor_db(process, fs: float, f0: float | None = None,
                      amp_db: float = 0.0, dur: float = 2.0) -> dict:
    """
    Drive `process` with a pure sine and measure every spectral component that
    is neither the fundamental nor a true harmonic below Nyquist. Those are
    alias (foldover) products.

    NOTE ON f0: the test tone MUST be high enough that harmonics exceed Nyquist,
    and must NOT be an integer divisor of fs. If f0 divides fs evenly, every
    folded harmonic lands exactly back on a harmonic bin and the test reports a
    clean spectrum for a badly aliasing process. Default is ~7.4 kHz, chosen
    irrational-ish w.r.t. common rates, so harmonics 3..N fold to off-grid bins.

    Returns 'alias_db' (worst alias product, dB relative to the fundamental),
    'thd_db'/'thd_pct' (in-band harmonics only), and the first few harmonics.
    """
    if f0 is None:
        f0 = fs * 0.15427  # ~7.405 kHz at 48k; deliberately non-commensurate
    n = int(dur * fs)
    t = np.arange(n) / fs
    amp = 10.0 ** (amp_db / 20.0)
    x = amp * np.sin(2 * np.pi * f0 * t)
    y = np.asarray(process(x), dtype=np.float64).reshape(-1)

    w = sig.windows.blackmanharris(len(y))
    # coherent-gain-normalised spectrum
    Y = np.fft.rfft(y * w) / (np.sum(w) / 2.0)
    mag = np.abs(Y)
    freqs = np.fft.rfftfreq(len(y), 1.0 / fs)
    bin_hz = fs / len(y)
    nyq = fs / 2.0

    # Blackman-Harris 4-term mainlobe is 8 bins wide total; guard generously.
    guard = 12

    def _peak_near(f_hz):
        idx = int(round(f_hz / bin_hz))
        lo, hi = max(idx - guard, 0), min(idx + guard + 1, len(mag))
        return float(np.max(mag[lo:hi])), idx

    fund, fund_idx = _peak_near(f0)
    fund = max(fund, EPS)

    # true (non-folded) harmonics that fit below Nyquist
    inband_harm = []
    k = 2
    while k * f0 < nyq:
        inband_harm.append(k * f0)
        k += 1
    k_max = k  # first harmonic above Nyquist

    # Mask out DC, the fundamental, and every in-band harmonic.
    mask = np.ones(len(mag), dtype=bool)
    mask[: guard * 2] = False
    mask[-guard:] = False
    for f_hz in [f0] + inband_harm:
        idx = int(round(f_hz / bin_hz))
        mask[max(idx - guard, 0): min(idx + guard + 1, len(mag))] = False

    if mask.any():
        ai = int(np.argmax(np.where(mask, mag, 0.0)))
        alias_peak = float(mag[ai])
        alias_f = float(freqs[ai])
    else:
        alias_peak, alias_f = EPS, 0.0

    harm_pow = 0.0
    harm_db = []
    for f_hz in inband_harm[:6]:
        p, _ = _peak_near(f_hz)
        harm_pow += p * p
        harm_db.append(20 * np.log10(max(p, EPS) / fund))
    thd = np.sqrt(harm_pow) / fund

    return {
        "f0": f0,
        "n_inband_harmonics": len(inband_harm),
        "first_folded_harmonic": k_max,
        "alias_db": 20 * np.log10(max(alias_peak, EPS) / fund),
        "alias_freq": alias_f,
        "thd_db": 20 * np.log10(max(thd, EPS)),
        "thd_pct": 100 * thd,
        "harmonics_db": harm_db,
    }


def report(x: np.ndarray, fs: float, name: str = "signal") -> dict:
    d = {
        "name": name,
        "lufs_i": loudness_integrated(x, fs),
        "lra_lu": loudness_range(x, fs),
        "sample_peak_db": sample_peak_db(x),
        "true_peak_dbtp": true_peak_db(x, fs),
        "crest_db": crest_factor_db(x),
        "dc_db": dc_offset_db(x),
    }
    st = loudness_short_term(x, fs)
    st = st[st > -70]
    d["lufs_s_p10"] = float(np.percentile(st, 10)) if st.size else float("-inf")
    d["lufs_s_p90"] = float(np.percentile(st, 90)) if st.size else float("-inf")
    return d
