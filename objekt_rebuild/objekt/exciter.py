"""Impact, noise, and external-audio exciters."""

from __future__ import annotations

import math
import numpy as np

from .config import ExciterConfig
from .dsp import adsr_envelope, midi_hz, one_pole_lowpass


def _impact(length: int, sr: int, note: float, velocity: float, cfg: ExciterConfig, rng: np.random.Generator) -> np.ndarray:
    out = np.zeros(length, dtype=np.float64)
    burst_ms = 12.0 - 10.5 * float(np.clip(cfg.hardness, 0.0, 1.0))
    count = min(length, max(2, int(sr * burst_ms / 1000.0)))
    t = np.arange(count) / sr
    base = midi_hz(note) * (1.0 + 5.0 * cfg.impact_tone)
    tonal = np.sin(2.0 * math.pi * min(base, sr * 0.42) * t)
    noisy = rng.normal(0.0, 1.0, count)
    window = np.exp(-t * (180.0 + 900.0 * cfg.hardness))
    out[:count] = (0.7 * noisy + 0.3 * tonal) * window
    if cfg.diffuser > 0.0:
        diffused = out.copy()
        taps = 1 + int(5 * cfg.diffuser)
        for tap in range(1, taps + 1):
            delay = max(1, int(sr * (0.0004 + tap * 0.0007)))
            if delay < length:
                diffused[delay:] += out[:-delay] * (cfg.diffuser / (tap + 1.0))
        out = diffused
    return out * cfg.impact_level * velocity


def _noise(length: int, sr: int, velocity: float, cfg: ExciterConfig, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(0.0, 1.0, length)
    mode = cfg.noise_mode.lower()
    rate_hz = 0.5 * (2.0 ** (cfg.noise_rate * 10.0))
    t = np.arange(length) / sr
    if mode == "pulse":
        raw *= (np.sin(2.0 * math.pi * rate_hz * t) > 0.0)
    elif mode == "random_pulse":
        probability = min(1.0, rate_hz / sr)
        gates = (rng.random(length) < probability).astype(np.float64)
        width = max(1, int(sr * 0.0015))
        raw *= np.convolve(gates, np.ones(width), mode="same") > 0.0
    elif mode == "static":
        probability = 0.002 + 0.08 * cfg.noise_rate
        raw *= rng.random(length) < probability
    cutoff = 180.0 * (2.0 ** (cfg.noise_color * 6.5))
    colored = one_pole_lowpass(raw, cutoff, sr)
    high_mix = cfg.noise_color
    colored = colored * (1.0 - 0.35 * high_mix) + (raw - colored) * (0.25 + 0.75 * high_mix)
    env = adsr_envelope(length, sr, cfg.noise_attack, cfg.noise_decay, cfg.noise_sustain, cfg.noise_release)
    delay = max(0, int(cfg.noise_delay * sr))
    shaped = colored * env
    if delay:
        shaped = np.pad(shaped, (delay, 0))[:length]
    return shaped * cfg.noise_level * velocity


def build_excitation(length: int, sr: int, note: float, velocity: float, cfg: ExciterConfig, seed: int, external_audio: np.ndarray | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    signal = _impact(length, sr, note, velocity, cfg, rng)
    signal += _noise(length, sr, velocity, cfg, rng)
    if external_audio is not None and cfg.external_level > 0.0:
        external = np.asarray(external_audio, dtype=np.float64)
        if external.ndim == 2:
            external = external.mean(axis=1)
        count = min(length, len(external))
        signal[:count] += external[:count] * cfg.external_level
    return signal
