"""Deterministic, range-limited patch randomizer."""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from .config import ObjektConfig


def _move(rng: np.random.Generator, value: float, amount: float, low: float, high: float) -> float:
    span = high - low
    return float(np.clip(value + rng.uniform(-1.0, 1.0) * span * amount * 0.22, low, high))


def _ratios(rng: np.random.Generator, values: tuple[float, ...], amount: float) -> tuple[float, ...]:
    result = []
    for value in values:
        moved = value * (2.0 ** rng.uniform(-0.25, 0.25) * amount)
        result.append(float(np.clip(moved, 0.25, 18.0)))
    return tuple(result)


def randomize_config(config: ObjektConfig, *, seed: int, amount: float = 0.5) -> ObjektConfig:
    amount = float(np.clip(amount, 0.0, 1.0))
    rng = np.random.default_rng(seed)
    exciter = replace(
        config.exciter,
        hardness=_move(rng, config.exciter.hardness, amount, 0.0, 1.0),
        impact_tone=_move(rng, config.exciter.impact_tone, amount, 0.0, 1.0),
        diffuser=_move(rng, config.exciter.diffuser, amount, 0.0, 1.0),
        noise_level=_move(rng, config.exciter.noise_level, amount, 0.0, 0.8),
        noise_color=_move(rng, config.exciter.noise_color, amount, 0.0, 1.0),
    )
    modal = replace(
        config.modal,
        ratios=_ratios(rng, config.modal.ratios, amount),
        decay=_move(rng, config.modal.decay, amount, 0.03, 8.0),
        decay_scale=_move(rng, config.modal.decay_scale, amount, -0.8, 0.5),
    )
    object1 = replace(
        config.object1,
        ratios=_ratios(rng, config.object1.ratios, amount),
        decay=_move(rng, config.object1.decay, amount, 0.03, 8.0),
        damping=_move(rng, config.object1.damping, amount, 0.0, 0.98),
        dispersion=_move(rng, config.object1.dispersion, amount, -0.8, 1.0),
        collision=_move(rng, config.object1.collision, amount, 0.0, 0.9),
        coupling=_move(rng, config.object1.coupling, amount, 0.0, 0.55),
    )
    object2 = replace(
        config.object2,
        ratios=_ratios(rng, config.object2.ratios, amount),
        decay=_move(rng, config.object2.decay, amount, 0.03, 8.0),
        damping=_move(rng, config.object2.damping, amount, 0.0, 0.98),
        dispersion=_move(rng, config.object2.dispersion, amount, -0.8, 1.0),
        collision=_move(rng, config.object2.collision, amount, 0.0, 0.9),
        coupling=_move(rng, config.object2.coupling, amount, 0.0, 0.55),
    )
    effects = replace(
        config.effects,
        distortion=_move(rng, config.effects.distortion, amount, 0.0, 0.65),
        delay_mix=_move(rng, config.effects.delay_mix, amount, 0.0, 0.35),
        reverb_mix=_move(rng, config.effects.reverb_mix, amount, 0.0, 0.45),
    )
    return replace(config, exciter=exciter, modal=modal, object1=object1, object2=object2, effects=effects, master_gain=min(config.master_gain, 1.0))
