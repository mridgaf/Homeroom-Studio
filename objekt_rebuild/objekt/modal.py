"""Eight-mode resonant filter bank."""

from __future__ import annotations

import math
import numpy as np

from .config import ModalConfig
from .dsp import midi_hz, pan_mono


def render_modal(excitation: np.ndarray, sr: int, note: float, cfg: ModalConfig) -> np.ndarray:
    length = len(excitation)
    stereo = np.zeros((length, 2), dtype=np.float64)
    if not cfg.enabled:
        return stereo
    tracked_note = 60.0 + (note - 60.0) * cfg.keytrack + cfg.tuning
    fundamental = midi_hz(tracked_note)
    for index, (ratio, gain, pan) in enumerate(zip(cfg.ratios, cfg.gains, cfg.pans)):
        frequency = min(fundamental * ratio, sr * 0.46)
        if frequency < 18.0:
            continue
        decay = float(np.clip(cfg.decay * (ratio ** cfg.decay_scale), 0.02, 12.0))
        radius = 10.0 ** (-3.0 / (decay * sr))
        coefficient = 2.0 * radius * math.cos(2.0 * math.pi * frequency / sr)
        radius2 = radius * radius
        mode = np.zeros(length, dtype=np.float64)
        y1 = 0.0
        y2 = 0.0
        injection = 1.0 - radius
        for n, sample in enumerate(excitation):
            y = coefficient * y1 - radius2 * y2 + float(sample) * injection
            mode[n] = y
            y2, y1 = y1, y
        stereo += pan_mono(mode * gain * cfg.level, pan)
    return stereo
