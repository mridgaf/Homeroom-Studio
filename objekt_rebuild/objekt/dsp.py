"""Low-level DSP used by the clean-room physical-modeling prototype."""

from __future__ import annotations

import math
import numpy as np


def midi_hz(note: float) -> float:
    return 440.0 * (2.0 ** ((note - 69.0) / 12.0))


def pan_mono(signal: np.ndarray, pan: float) -> np.ndarray:
    pan = float(np.clip(pan, -1.0, 1.0))
    angle = (pan + 1.0) * math.pi / 4.0
    return np.column_stack((signal * math.cos(angle), signal * math.sin(angle)))


def soft_limit(stereo: np.ndarray, drive: float = 1.2) -> np.ndarray:
    return np.tanh(stereo * drive) / math.tanh(drive)


def adsr_envelope(length: int, sr: int, attack: float, decay: float, sustain: float, release: float) -> np.ndarray:
    env = np.zeros(length, dtype=np.float64)
    a = min(length, max(0, int(attack * sr)))
    d = min(length - a, max(0, int(decay * sr)))
    r = min(length - a - d, max(0, int(release * sr)))
    body = length - a - d - r
    cursor = 0
    if a:
        env[cursor:cursor + a] = np.linspace(0.0, 1.0, a, endpoint=False)
        cursor += a
    if d:
        env[cursor:cursor + d] = np.linspace(1.0, sustain, d, endpoint=False)
        cursor += d
    if body:
        env[cursor:cursor + body] = sustain
        cursor += body
    if r:
        start = env[cursor - 1] if cursor else sustain
        env[cursor:] = np.linspace(start, 0.0, r, endpoint=True)
    return env


def one_pole_lowpass(signal: np.ndarray, cutoff: float, sr: int) -> np.ndarray:
    cutoff = float(np.clip(cutoff, 10.0, sr * 0.45))
    alpha = 1.0 - math.exp(-2.0 * math.pi * cutoff / sr)
    out = np.zeros_like(signal, dtype=np.float64)
    state = 0.0
    for i, sample in enumerate(signal):
        state += alpha * (float(sample) - state)
        out[i] = state
    return out


def dc_block(stereo: np.ndarray, coefficient: float = 0.995) -> np.ndarray:
    """Remove DC and sub-audio drift from recursive resonators."""
    data = np.asarray(stereo, dtype=np.float64)
    out = np.zeros_like(data)
    for channel in range(data.shape[1]):
        x1 = 0.0
        y1 = 0.0
        for index, sample in enumerate(data[:, channel]):
            y = float(sample) - x1 + coefficient * y1
            out[index, channel] = y
            x1 = float(sample)
            y1 = y
    return out


def peak_normalize(audio: np.ndarray, peak: float = 0.92) -> np.ndarray:
    maximum = float(np.max(np.abs(audio))) if audio.size else 0.0
    if maximum > peak and maximum > 0.0:
        audio = audio * (peak / maximum)
    return audio
