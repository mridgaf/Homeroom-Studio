"""Eight-line feedback-delay waveguide array."""

from __future__ import annotations

import math
import numpy as np

from .config import WaveguideConfig
from .dsp import midi_hz, pan_mono


def render_waveguide(excitation: np.ndarray, previous: np.ndarray, sr: int, note: float, cfg: WaveguideConfig) -> np.ndarray:
    length = len(excitation)
    result = np.zeros((length, 2), dtype=np.float64)
    if not cfg.enabled:
        return result
    tracked_note = 60.0 + (note - 60.0) * cfg.keytrack + cfg.tuning
    fundamental = midi_hz(tracked_note)
    mono_previous = previous.mean(axis=1) if previous.ndim == 2 else previous
    source = excitation * cfg.direct_input + mono_previous * cfg.previous_input
    line_outputs = []
    shared = np.zeros(length, dtype=np.float64)
    for index, (ratio, gain, pan) in enumerate(zip(cfg.ratios, cfg.gains, cfg.pans)):
        warped_ratio = ratio ** (1.0 + cfg.dispersion * 0.16)
        frequency = float(np.clip(fundamental * warped_ratio, 25.0, sr * 0.43))
        nominal_delay = max(2.0, sr / frequency)
        max_delay = int(math.ceil(nominal_delay * (1.0 + abs(cfg.pitch_mod) * 0.08))) + 4
        buffer = np.zeros(max_delay, dtype=np.float64)
        write = 0
        damp_state = 0.0
        out = np.zeros(length, dtype=np.float64)
        polarity = cfg.polarity if index % 2 == 0 else 1.0
        decay = float(np.clip(cfg.decay / (1.0 + 0.035 * index), 0.025, 10.0))
        feedback = 10.0 ** (-3.0 * nominal_delay / (sr * decay))
        for n, sample in enumerate(source):
            pitch_env = math.exp(-n / max(1.0, sr * 0.08))
            mod = 1.0 + cfg.pitch_mod * 0.035 * pitch_env
            delay = float(np.clip(nominal_delay / mod, 2.0, max_delay - 2.0))
            read_position = (write - delay) % max_delay
            i0 = int(math.floor(read_position))
            frac = read_position - i0
            delayed = buffer[i0] * (1.0 - frac) + buffer[(i0 + 1) % max_delay] * frac
            damp_state = cfg.damping * damp_state + (1.0 - cfg.damping) * delayed
            coupled = shared[n - 1] if n else 0.0
            drive = float(sample) * gain + coupled * cfg.coupling
            nonlinear = math.tanh((damp_state * feedback * polarity + drive) * (1.0 + 5.0 * cfg.collision))
            buffer[write] = nonlinear
            write = (write + 1) % max_delay
            out[n] = delayed
        line_outputs.append(out)
        shared += out * (gain / max(1, len(cfg.ratios)))
        result += pan_mono(out * gain * cfg.level, pan)
    return result
