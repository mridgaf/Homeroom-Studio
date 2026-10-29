"""Configuration model for the clean-room Objekt-inspired synthesizer."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
import json
from pathlib import Path
from typing import Any


def _construct(cls: Any, data: dict[str, Any]) -> Any:
    allowed = {item.name for item in fields(cls)}
    values = {key: value for key, value in data.items() if key in allowed}
    for key in ("ratios", "gains", "pans"):
        if key in values:
            values[key] = tuple(values[key])
    return cls(**values)


@dataclass(frozen=True)
class ExciterConfig:
    impact_level: float = 0.8
    hardness: float = 0.65
    impact_tone: float = 0.35
    diffuser: float = 0.15
    noise_level: float = 0.1
    noise_mode: str = "color"
    noise_attack: float = 0.001
    noise_decay: float = 0.12
    noise_sustain: float = 0.0
    noise_release: float = 0.08
    noise_delay: float = 0.0
    noise_rate: float = 0.45
    noise_color: float = 0.55
    external_level: float = 0.0


@dataclass(frozen=True)
class ModalConfig:
    enabled: bool = True
    level: float = 0.7
    ratios: tuple[float, ...] = (1.0, 2.0, 2.99, 4.02, 5.1, 6.18, 7.35, 8.5)
    gains: tuple[float, ...] = (1.0, 0.72, 0.55, 0.42, 0.34, 0.28, 0.22, 0.18)
    pans: tuple[float, ...] = (-0.25, 0.2, -0.15, 0.15, -0.1, 0.1, -0.05, 0.05)
    decay: float = 1.5
    decay_scale: float = -0.06
    tuning: float = 0.0
    keytrack: float = 1.0


@dataclass(frozen=True)
class WaveguideConfig:
    enabled: bool = True
    level: float = 0.55
    ratios: tuple[float, ...] = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
    gains: tuple[float, ...] = (1.0, 0.62, 0.48, 0.38, 0.3, 0.24, 0.2, 0.17)
    pans: tuple[float, ...] = (-0.3, 0.3, -0.22, 0.22, -0.14, 0.14, -0.06, 0.06)
    decay: float = 1.2
    damping: float = 0.32
    dispersion: float = 0.0
    collision: float = 0.05
    pitch_mod: float = 0.0
    coupling: float = 0.08
    polarity: float = 1.0
    tuning: float = 0.0
    keytrack: float = 1.0
    direct_input: float = 1.0
    previous_input: float = 0.0


@dataclass(frozen=True)
class MixerConfig:
    modal_level: float = 0.8
    object1_level: float = 0.65
    object2_level: float = 0.5
    modal_pan: float = 0.0
    object1_pan: float = -0.1
    object2_pan: float = 0.1


@dataclass(frozen=True)
class EffectsConfig:
    low_db: float = 0.0
    high_db: float = 0.0
    distortion: float = 0.05
    compression: float = 0.15
    delay_mix: float = 0.06
    delay_time: float = 0.19
    delay_feedback: float = 0.22
    reverb_mix: float = 0.12
    reverb_size: float = 0.55


@dataclass(frozen=True)
class ObjektConfig:
    exciter: ExciterConfig = field(default_factory=ExciterConfig)
    modal: ModalConfig = field(default_factory=ModalConfig)
    object1: WaveguideConfig = field(default_factory=WaveguideConfig)
    object2: WaveguideConfig = field(default_factory=lambda: WaveguideConfig(previous_input=0.55, direct_input=0.35, dispersion=0.12))
    mixer: MixerConfig = field(default_factory=MixerConfig)
    effects: EffectsConfig = field(default_factory=EffectsConfig)
    master_gain: float = 0.72

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ObjektConfig":
        return cls(
            exciter=_construct(ExciterConfig, data.get("exciter", {})),
            modal=_construct(ModalConfig, data.get("modal", {})),
            object1=_construct(WaveguideConfig, data.get("object1", {})),
            object2=_construct(WaveguideConfig, data.get("object2", {})),
            mixer=_construct(MixerConfig, data.get("mixer", {})),
            effects=_construct(EffectsConfig, data.get("effects", {})),
            master_gain=float(data.get("master_gain", 0.72)),
        )

    @classmethod
    def from_json(cls, path: str | Path) -> "ObjektConfig":
        with Path(path).open("r", encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))

    @classmethod
    def from_preset(cls, name: str) -> "ObjektConfig":
        path = Path(__file__).resolve().parents[1] / "presets" / f"{name}.json"
        return cls.from_json(path)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
