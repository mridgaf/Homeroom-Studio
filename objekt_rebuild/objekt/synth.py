"""Public rendering API."""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from .config import ObjektConfig
from .dsp import dc_block, pan_mono, peak_normalize, soft_limit
from .effects import apply_effects
from .exciter import build_excitation
from .modal import render_modal
from .waveguide import render_waveguide


class ObjektSynth:
    def __init__(self, sample_rate: int = 48_000):
        if sample_rate < 8_000:
            raise ValueError("sample_rate must be at least 8000 Hz")
        self.sample_rate = int(sample_rate)

    def render_note(
        self,
        note: float,
        velocity: float,
        duration: float,
        config: ObjektConfig,
        *,
        seed: int = 0,
        external_audio: np.ndarray | None = None,
    ) -> np.ndarray:
        length = max(1, int(round(duration * self.sample_rate)))
        velocity = float(np.clip(velocity, 0.0, 1.0))
        excitation = build_excitation(length, self.sample_rate, note, velocity, config.exciter, seed, external_audio)
        modal = render_modal(excitation, self.sample_rate, note, config.modal)
        object1 = render_waveguide(excitation, modal, self.sample_rate, note, config.object1)
        object2 = render_waveguide(excitation, object1, self.sample_rate, note, config.object2)

        mix = np.zeros((length, 2), dtype=np.float64)
        modal_mono = modal.mean(axis=1)
        object1_mono = object1.mean(axis=1)
        object2_mono = object2.mean(axis=1)
        mix += pan_mono(modal_mono * config.mixer.modal_level, config.mixer.modal_pan)
        mix += pan_mono(object1_mono * config.mixer.object1_level, config.mixer.object1_pan)
        mix += pan_mono(object2_mono * config.mixer.object2_level, config.mixer.object2_pan)
        mix = dc_block(mix)
        mix = apply_effects(mix, self.sample_rate, config.effects)
        mix = dc_block(mix)
        mix = soft_limit(mix * config.master_gain, 1.1)
        mix = peak_normalize(mix, 0.94)
        return mix.astype(np.float32)

    def render_sequence(
        self,
        events: list[tuple[float, float, float, float]],
        config: ObjektConfig,
        *,
        tail: float = 1.5,
        seed: int = 0,
    ) -> np.ndarray:
        """Render (start_seconds, midi_note, velocity, duration_seconds) events."""
        if not events:
            return np.zeros((1, 2), dtype=np.float32)
        total = max(start + duration for start, _, _, duration in events) + tail
        out = np.zeros((max(1, int(total * self.sample_rate)), 2), dtype=np.float64)
        for index, (start, note, velocity, duration) in enumerate(events):
            voice_duration = duration + tail
            voice = self.render_note(note, velocity, voice_duration, config, seed=seed + index)
            offset = max(0, int(start * self.sample_rate))
            count = min(len(voice), len(out) - offset)
            if count > 0:
                out[offset:offset + count] += voice[:count]
        out = peak_normalize(soft_limit(out, 1.2), 0.94)
        return out.astype(np.float32)
