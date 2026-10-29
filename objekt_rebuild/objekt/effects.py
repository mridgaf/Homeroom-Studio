"""Lightweight finishing effects for the prototype."""

from __future__ import annotations

import math
import numpy as np

from .config import EffectsConfig
from .dsp import one_pole_lowpass, soft_limit


def _eq(stereo: np.ndarray, sr: int, low_db: float, high_db: float) -> np.ndarray:
    out = np.empty_like(stereo)
    low_gain = 10.0 ** (low_db / 20.0)
    high_gain = 10.0 ** (high_db / 20.0)
    for channel in range(2):
        low = one_pole_lowpass(stereo[:, channel], 260.0, sr)
        high_base = one_pole_lowpass(stereo[:, channel], 3800.0, sr)
        high = stereo[:, channel] - high_base
        mid = stereo[:, channel] - low - high
        out[:, channel] = low * low_gain + mid + high * high_gain
    return out


def _compress(stereo: np.ndarray, amount: float) -> np.ndarray:
    if amount <= 0.0:
        return stereo
    threshold = 10.0 ** ((-6.0 - 18.0 * amount) / 20.0)
    ratio = 1.0 + 7.0 * amount
    magnitude = np.abs(stereo)
    over = np.maximum(magnitude - threshold, 0.0)
    compressed = threshold + over / ratio
    gain = np.where(magnitude > threshold, compressed / np.maximum(magnitude, 1e-12), 1.0)
    return stereo * gain * (1.0 + 0.45 * amount)


def _delay(stereo: np.ndarray, sr: int, time: float, feedback: float, mix: float) -> np.ndarray:
    if mix <= 0.0:
        return stereo
    delay = max(1, int(time * sr))
    wet = np.zeros_like(stereo)
    for n in range(delay, len(stereo)):
        wet[n, 0] = stereo[n - delay, 1] + wet[n - delay, 1] * feedback
        wet[n, 1] = stereo[n - delay, 0] + wet[n - delay, 0] * feedback
    return stereo * (1.0 - mix) + wet * mix


def _reverb(stereo: np.ndarray, sr: int, size: float, mix: float) -> np.ndarray:
    if mix <= 0.0:
        return stereo
    wet = np.zeros_like(stereo)
    times = (0.0297, 0.0371, 0.0411, 0.0437)
    for channel in range(2):
        for index, base_time in enumerate(times):
            delay = max(1, int(sr * base_time * (0.65 + size)))
            feedback = 0.55 + size * 0.28 - index * 0.025
            comb = np.zeros(len(stereo), dtype=np.float64)
            for n in range(delay, len(stereo)):
                comb[n] = stereo[n - delay, channel] + comb[n - delay] * feedback
            wet[:, channel] += comb / len(times)
    return stereo * (1.0 - mix) + wet * mix


def apply_effects(stereo: np.ndarray, sr: int, cfg: EffectsConfig) -> np.ndarray:
    out = _eq(stereo, sr, cfg.low_db, cfg.high_db)
    if cfg.distortion > 0.0:
        drive = 1.0 + cfg.distortion * 8.0
        distorted = soft_limit(out, drive)
        out = out * (1.0 - cfg.distortion) + distorted * cfg.distortion
    out = _compress(out, cfg.compression)
    out = _delay(out, sr, cfg.delay_time, cfg.delay_feedback, cfg.delay_mix)
    out = _reverb(out, sr, cfg.reverb_size, cfg.reverb_mix)
    return out
