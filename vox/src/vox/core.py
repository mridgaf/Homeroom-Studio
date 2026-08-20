"""
Module interface contract. Every DSP block in this project implements Module,
processes in fixed-size blocks, and must be transliterable to C++ later:
no whole-file tricks, no Python-only magic in process().

Two-pass / offline-only algorithms (e.g. reverb RT60 estimation from the full
clip) live OUTSIDE this class, in an analysis pass that produces target
parameters which get pushed into normal per-block Modules. That keeps the
process() call real-time-legal even though the *decision* was made offline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
import numpy as np


@dataclass
class ParamSpec:
    name: str
    kind: str            # "float" | "int" | "bool" | "enum"
    default: float
    lo: float = 0.0
    hi: float = 1.0
    unit: str = ""
    choices: tuple = ()
    curve: str = "linear"  # "linear" | "log" -- how a UI should map a knob to this range


class Module:
    """Base class for every processing block."""

    name: str = "module"
    params: tuple[ParamSpec, ...] = ()

    def __init__(self, fs: float, **kwargs):
        self.fs = float(fs)
        self._p = {p.name: p.default for p in self.params}
        for k, v in kwargs.items():
            if k not in self._p:
                raise ValueError(f"{self.name}: unknown param '{k}'")
            self._p[k] = self._clamped(k, v)
        self.prepare(self.fs)

    # -- parameter access --------------------------------------------------
    def _clamped(self, name: str, value):
        """Hold `value` inside the ParamSpec's declared range.

        Specs carried lo/hi that nothing enforced, so an out-of-range value
        propagated into buffer sizing and index arithmetic. Limiter is the
        sharp edge -- lookahead_ms above its 20 ms maximum made an internal
        offset negative and raised `zero-size array to reduction operation
        maximum` from inside process(). Clamping here fixes every module at
        once rather than one guard per module.
        """
        spec = next((p for p in self.params if p.name == name), None)
        if spec is None or spec.kind not in ("float", "int"):
            return value
        v = min(max(value, spec.lo), spec.hi)
        return int(round(v)) if spec.kind == "int" else v

    def set(self, name: str, value: float):
        if name not in self._p:
            raise ValueError(f"{self.name}: unknown param '{name}'")
        value = self._clamped(name, value)
        self._p[name] = value
        self.on_param_changed(name, value)

    def get(self, name: str) -> float:
        return self._p[name]

    def on_param_changed(self, name: str, value: float):
        """Override to recompute cached coefficients when a param changes."""
        pass

    # -- lifecycle (override as needed) -------------------------------------
    def prepare(self, fs: float):
        """Called on construction and on sample-rate change. Allocate state here."""
        self.fs = float(fs)

    def reset(self):
        """Clear delay lines / envelope state without reallocating. Must not
        introduce clicks worse than a normal bypass transition would."""
        pass

    def latency_samples(self) -> int:
        """Reported algorithmic latency (lookahead, filter group delay, etc.)
        at the current fs. Used by the host for delay compensation."""
        return 0

    def process(self, x: np.ndarray) -> np.ndarray:
        """x: (n, channels) float64. Must return the same shape. Must be
        callable repeatedly across arbitrary block sizes with continuous
        state (i.e. correct at block size 1 and at block size 8192 alike)."""
        raise NotImplementedError


class Chain(Module):
    """Ordered list of modules with per-module bypass/solo/mix and dry-path
    delay compensation, mirroring Nectar's rearrangeable module rack."""

    name = "chain"

    def __init__(self, fs: float, modules: list[Module] | None = None):
        self.modules: list[Module] = modules or []
        self.bypassed: set[int] = set()
        self.solo: int | None = None
        self.mix: dict[int, float] = {}
        self._dry_bufs: dict[int, np.ndarray] = {}
        # Module.__init__ was NOT being called here, so self._p never existed
        # and the inherited get()/set() raised AttributeError. This class is
        # part of an interface designed to transliterate to JUCE -- a subclass
        # that silently isn't one is precisely the trap that port would hit.
        super().__init__(fs)

    def latency_samples(self) -> int:
        return sum(m.latency_samples() for i, m in enumerate(self.modules)
                   if i not in self.bypassed)

    def reset(self):
        self._dry_bufs = {}
        for m in self.modules:
            m.reset()

    def _delayed_dry(self, key: int, y: np.ndarray, lat: int) -> np.ndarray:
        """`y` delayed by `lat` samples, with the tail carried across blocks.

        Without this, blending a module's wet output against the undelayed dry
        signal is a comb filter (see test_chain_partial_mix_compensates_module_latency).
        """
        if lat <= 0:
            return y
        buf = self._dry_bufs.get(key)
        if buf is None or buf.shape != (lat,) + y.shape[1:]:
            buf = np.zeros((lat,) + y.shape[1:])
        ext = np.concatenate([buf, y], axis=0)
        self._dry_bufs[key] = ext[len(ext) - lat:].copy()
        return ext[:len(y)]

    def process(self, x: np.ndarray) -> np.ndarray:
        if self.solo is not None:
            m = self.modules[self.solo]
            return m.process(x)
        y = x
        for i, m in enumerate(self.modules):
            if i in self.bypassed:
                continue
            wet = m.process(y)
            mix = self.mix.get(i, 1.0)
            if mix < 1.0:
                # Keyed by id(m), not by list index: reordering or inserting a
                # module would otherwise hand one module's delay tail to a
                # different module, silently misaligning its dry path.
                dry = self._delayed_dry(id(m), y, m.latency_samples())
                y = dry * (1 - mix) + wet * mix
            else:
                y = wet
        return y


def db2lin(db: np.ndarray | float) -> np.ndarray | float:
    return 10.0 ** (np.asarray(db) / 20.0)


def lin2db(x: np.ndarray | float, floor_db: float = -120.0) -> np.ndarray | float:
    x = np.asarray(x, dtype=np.float64)
    floor = 10.0 ** (floor_db / 20.0)
    return 20.0 * np.log10(np.maximum(np.abs(x), floor))


def one_pole_coeff(time_const_s: float, fs: float) -> float:
    """alpha for y[n] = y[n-1] + alpha*(x[n]-y[n-1]), from a target time
    constant (63.2% settling). This is the formula the adversary demanded
    we state explicitly rather than hand-wave 'a smoothing filter'."""
    if time_const_s <= 0:
        return 1.0
    return 1.0 - np.exp(-1.0 / (time_const_s * fs))
