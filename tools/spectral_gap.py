"""Spectral A/B gap measure for the from-scratch-mix fix.

Loudness-matches two finished WAVs (BS.1770 integrated LUFS via groove.lufs),
then reports octave-band spectral DENSITY (dB, per-Hz convention so pink noise
reads ~-3 dB/oct like SPAN) and the best-fit tilt. The GAP column (B - A) is
the correction target: where the from-scratch mix sits hotter than the
pre-mixed loop reference.

Usage:
    ./.venv/bin/python -m tools.spectral_gap A.wav B.wav
    # A = reference (loops), B = mix under test (from-scratch)

Self-check:
    ./.venv/bin/python -m tools.spectral_gap --demo
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.signal import welch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import groove  # noqa: E402  (reuse the project's BS.1770 loudness meter)

SR = groove.SR

# Octave centers; edges are center/sqrt2 .. center*sqrt2.
CENTERS = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])


def _read(path):
    import soundfile as sf
    x, native = sf.read(str(path), dtype="float64", always_2d=True)
    if native != SR:
        # resample to the project rate so groove.lufs' k-weighting is valid
        try:
            import soxr
            x = soxr.resample(x, native, SR)
        except Exception:
            n = int(round(x.shape[0] * SR / native))
            x = np.stack([np.interp(np.linspace(0, len(c) - 1, n),
                                    np.arange(len(c)), c) for c in x.T], axis=1)
    L = x[:, 0]
    R = x[:, 1] if x.shape[1] > 1 else x[:, 0]
    return L, R


def band_density_db(mono):
    """Mean PSD (power/Hz) per octave band, in dB. Per-Hz so a pink slope
    reads ~-3 dB/oct."""
    nper = min(len(mono), 16384)
    f, pxx = welch(mono, fs=SR, nperseg=nper)
    out = []
    for c in CENTERS:
        lo, hi = c / np.sqrt(2), c * np.sqrt(2)
        sel = (f >= lo) & (f < hi)
        out.append(pxx[sel].mean() if sel.any() else np.nan)
    out = np.array(out)
    return 10 * np.log10(out + 1e-20)


def tilt_db_per_oct(band_db):
    """Best-fit dB per octave over the valid bands (log2 center as x)."""
    x = np.log2(CENTERS)
    y = band_db
    ok = np.isfinite(y)
    slope, _ = np.polyfit(x[ok], y[ok], 1)
    return slope  # per doubling == per octave


def compare(path_a, path_b):
    La, Ra = _read(path_a)
    Lb, Rb = _read(path_b)
    la, lb = groove.lufs(La, Ra), groove.lufs(Lb, Rb)
    # loudness-match B up/down to A before comparing spectra
    g = 10 ** ((la - lb) / 20)
    Lb, Rb = Lb * g, Rb * g
    a = band_density_db(0.5 * (La + Ra))
    b = band_density_db(0.5 * (Lb + Rb))
    # report each relative to its own broadband mean so tilt, not level, shows
    a_rel = a - np.nanmean(a)
    b_rel = b - np.nanmean(b)
    print(f"A (ref)  : {Path(path_a).name}   LUFS {la:6.2f}")
    print(f"B (test) : {Path(path_b).name}   LUFS {lb:6.2f}  (matched +{20*np.log10(g):.2f} dB)")
    print()
    print(f"{'band Hz':>8} {'A dB':>7} {'B dB':>7} {'GAP B-A':>8}")
    for c, av, bv in zip(CENTERS, a_rel, b_rel):
        print(f"{c:8.0f} {av:7.1f} {bv:7.1f} {bv-av:8.1f}")
    print()
    print(f"tilt A: {tilt_db_per_oct(a):+.2f} dB/oct   "
          f"tilt B: {tilt_db_per_oct(b):+.2f} dB/oct")
    return a_rel, b_rel


def _demo():
    rng = np.random.default_rng(0)
    n = SR * 4
    white = rng.standard_normal(n)
    # pink via 1/f amplitude shaping in freq domain
    F = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    freqs[0] = freqs[1]
    pink = np.fft.irfft(F / np.sqrt(freqs), n)
    slope = tilt_db_per_oct(band_density_db(pink))
    assert -3.4 < slope < -2.6, f"pink tilt should be ~-3 dB/oct, got {slope:.2f}"
    slope_w = tilt_db_per_oct(band_density_db(white))
    assert -0.4 < slope_w < 0.4, f"white tilt should be ~0 dB/oct, got {slope_w:.2f}"
    print(f"OK: pink {slope:+.2f} dB/oct, white {slope_w:+.2f} dB/oct")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        _demo()
    elif len(sys.argv) == 3:
        compare(sys.argv[1], sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
