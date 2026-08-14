"""
Single-channel late-reverberation suppression.

nara_wpe (tested, see docs/03_engineer.md addendum) needs multiple microphones
to do meaningful work; on a single vocal-stem channel it left the reverb tail
untouched (-77.5 -> -77.8 dB on our synthetic test). A vocal stem is one
channel, so we hand-roll the classic single-channel approach instead:

  Lebart, Boucher & Denbigh (2001) / Habets (2007) statistical model:
  the late reverberant tail is treated as decaying stochastic energy per
  STFT bin, its variance estimated from the DECAY RATE (RT60) already
  observed in that bin, and subtracted spectrally (generalized Wiener /
  spectral-subtraction gain) from the current frame.

  sigma_late[k, n]^2 = exp(-2 * delta[k] * hop_s) * sigma_late[k, n-1]^2
                        + (1 - exp(-2*delta[k]*hop_s)) * |X[k, n-D]|^2
  delta[k] = 3*ln(10) / RT60[k]     (energy decay constant, natural log domain)

This is a RECURSIVE, causal, per-bin estimator -- no whole-file lookahead
beyond one STFT frame delay `D`, so unlike WPE's batch solve it degrades
gracefully to a streaming/real-time form (fixed D-frame latency), per the
architecture adversary's requirement that nothing offline-only be presented
as real-time-capable.

RT60 per band can be supplied (from a room analysis pass) or blind-estimated
via `estimate_rt60_bands`.
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sig

EPS = 1e-12


def _stft(x, n_fft=1024, hop=256):
    f, t, Z = sig.stft(x, nperseg=n_fft, noverlap=n_fft - hop, boundary="zeros")
    return Z  # (freq, frames)


def _istft(Z, n_fft=1024, hop=256, length=None):
    _, y = sig.istft(Z, nperseg=n_fft, noverlap=n_fft - hop, boundary=True)
    if length is not None:
        y = y[:length] if len(y) >= length else np.pad(y, (0, length - len(y)))
    return y


def estimate_rt60_bands(x, fs, n_fft=1024, hop=256, band_edges=None):
    """
    Blind per-band RT60 via Schroeder backward-integration on the STFT energy
    envelope of each bin, using the -5 to -25 dB decay slope (avoids the
    direct-sound onset and the noise-floor knee). Bands are grouped in
    octave-ish ranges and averaged for a stable estimate from a short clip.
    Returns rt60 array shaped (n_freq_bins,).
    """
    Z = _stft(x, n_fft, hop)
    mag2 = np.abs(Z) ** 2
    n_bins, n_frames = mag2.shape
    hop_s = hop / fs

    if band_edges is None:
        band_edges = [0, 200, 500, 1000, 2000, 4000, 8000, fs / 2]
    freqs = np.fft.rfftfreq(n_fft, 1 / fs)

    rt60 = np.full(n_bins, 0.35)  # sane default if a band can't be estimated
    for lo, hi in zip(band_edges[:-1], band_edges[1:]):
        idx = np.where((freqs >= lo) & (freqs < hi))[0]
        if idx.size == 0:
            continue
        env = mag2[idx].mean(axis=0)
        if env.sum() <= 0:
            continue
        # Schroeder backward integral (energy decay curve)
        edc = np.cumsum(env[::-1])[::-1]
        edc_db = 10 * np.log10(np.maximum(edc, EPS) / (edc[0] + EPS))
        # fit slope between -5 and -25 dB
        mask = (edc_db <= -5) & (edc_db >= -25)
        if mask.sum() < 3:
            continue
        t = np.arange(n_frames) * hop_s
        slope, _ = np.polyfit(t[mask], edc_db[mask], 1)  # dB/s, negative
        if slope >= -0.5:
            continue
        band_rt60 = -60.0 / slope
        band_rt60 = float(np.clip(band_rt60, 0.05, 3.0))
        rt60[idx] = band_rt60
    return rt60


def suppress_late_reverb(x, fs, rt60_bands=None, n_fft=1024, hop=256,
                          direct_frames=2, floor_db=-20.0, strength=1.0):
    """
    Subtract the estimated late-reverberant energy from each STFT bin.

    Parameters
    ----------
    rt60_bands : per-bin RT60 seconds, from estimate_rt60_bands() or a room
                 analysis. If None, blind-estimated from `x` itself.
    direct_frames : D, the number of frames treated as "direct + early"
                    before late-reverb subtraction begins (latency of the
                    causal estimator, in STFT hops).
    floor_db : spectral floor relative to the input magnitude, prevents
               musical-noise artifacts from over-subtraction (standard
               spectral-subtraction practice).
    strength : 0..1+, scales the subtracted late-energy estimate. 1.0 = the
               model's own estimate; <1 is conservative, >1 is aggressive.

    Returns (y, info) where info carries the rt60 estimate used, for logging
    and for the "why did it do that" transparency the architecture spec
    requires (no black boxes).
    """
    Z = _stft(x, n_fft, hop)
    n_bins, n_frames = Z.shape
    hop_s = hop / fs

    if rt60_bands is None:
        rt60_bands = estimate_rt60_bands(x, fs, n_fft, hop)

    delta = 3.0 * np.log(10.0) / np.maximum(rt60_bands, 0.05)   # per bin
    a = np.exp(-2.0 * delta * hop_s)                             # per bin, decay per hop

    mag2 = np.abs(Z) ** 2
    sigma_late = np.zeros((n_bins, n_frames))
    D = max(int(direct_frames), 1)

    for n in range(n_frames):
        src = n - D
        if src < 0:
            continue
        prev = sigma_late[:, n - 1] if n > 0 else np.zeros(n_bins)
        sigma_late[:, n] = a * prev + (1.0 - a) * mag2[:, src]

    floor = 10 ** (floor_db / 20.0)
    gain = np.sqrt(np.maximum(mag2 - strength * sigma_late, (floor ** 2) * mag2) / np.maximum(mag2, EPS))
    gain = np.clip(gain, floor, 1.0)

    Y = Z * gain
    y = _istft(Y, n_fft, hop, length=len(x))
    info = {
        "rt60_bands_hz_s": rt60_bands,
        "mean_rt60": float(np.mean(rt60_bands)),
        "latency_frames": D,
        "latency_ms": 1000.0 * (D * hop) / fs,
    }
    return y, info
