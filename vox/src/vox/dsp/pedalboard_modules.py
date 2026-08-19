"""
Phase-1-only modules built on `pedalboard` (Spotify's JUCE-adjacent audio
library). These fill in Reverb and Dimension (chorus/phaser), which we had
not hand-built yet, rather than spending the time hand-rolling an FDN reverb
and modulated all-pass network when a real, tested implementation is already
available.

HONEST SCOPE NOTE: pedalboard is a Python package. It cannot be linked into
the eventual real-time JUCE/C++ plugin (Phase 2) — these modules exist so we
can validate the PRODUCT'S sonic quality now, not as the final shipped DSP.
When Phase 2 starts, these get reimplemented natively in C++ (most likely
directly against juce::dsp, which is what pedalboard itself is built on for
several of these effects) and re-verified against the same bar. Do not ship
a plugin that shells out to Python.

Do NOT use pedalboard.Limiter or pedalboard.Distortion anywhere in this
project -- both measured failing (Limiter: true-peak overshoot up to 4.1 dB,
worse than our own pre-fix bug; Distortion: -19.4 dB alias floor, far short
of the -90 dB bar). Our own Limiter and Saturation modules replace them and
are what's used everywhere in the chain.

pedalboard's Reverb does NOT null cleanly at wet=0/dry=1 (measured -6.6 dB
difference against silence) -- its internal "dry" path is not a transparent
bypass. So every module here computes its OWN dry/wet mix externally, using
our untouched input signal for the dry side, never pedalboard's.
"""
from __future__ import annotations

import numpy as np
import pedalboard as pb

from ..core import Module, ParamSpec


def _to_pb(x2: np.ndarray) -> np.ndarray:
    """(n, ch) float64 -> pedalboard's (ch, n) float32."""
    return np.ascontiguousarray(x2.T.astype(np.float32))


def _from_pb(stereo: np.ndarray, ch: int) -> np.ndarray:
    y = stereo.T.astype(np.float64)
    if ch == 1:
        return y[:, :1] if y.ndim > 1 else y[:, None]
    return y


class ReverbSend(Module):
    """Algorithmic reverb (JUCE-style FDN via pedalboard.Reverb), used as a
    send: we take a 100% wet tap from pedalboard and mix it against our OWN
    unprocessed dry signal, because pedalboard's internal dry/wet mixing does
    not null cleanly (see module docstring)."""

    name = "reverb"
    params = (
        ParamSpec("room_size", "float", 0.5, 0.0, 1.0, ""),
        ParamSpec("damping", "float", 0.5, 0.0, 1.0, ""),
        ParamSpec("width", "float", 1.0, 0.0, 1.0, ""),
        ParamSpec("mix", "float", 0.15, 0.0, 1.0, ""),
    )

    def prepare(self, fs):
        self.fs = fs
        self._board = None
        self._design()

    def _design(self):
        self._board = pb.Pedalboard([pb.Reverb(
            room_size=self._p.get("room_size", 0.5) if hasattr(self, "_p") else 0.5,
            damping=self._p.get("damping", 0.5) if hasattr(self, "_p") else 0.5,
            wet_level=1.0, dry_level=0.0,
            width=self._p.get("width", 1.0) if hasattr(self, "_p") else 1.0,
        )])

    def on_param_changed(self, name, value):
        if name in ("room_size", "damping", "width"):
            self._design()
            self.reset()  # avoid a discontinuity from swapping tank state mid-stream

    def reset(self):
        self._design()

    def process(self, x: np.ndarray) -> np.ndarray:
        ch = x.shape[1] if x.ndim > 1 else 1
        x2 = x if x.ndim > 1 else x[:, None]
        stereo_in = np.concatenate([x2, x2], axis=1) if ch == 1 else x2[:, :2]
        wet = _from_pb(self._board(_to_pb(stereo_in), self.fs, reset=False), 2)
        wet_mono = wet.mean(axis=1, keepdims=True) if ch == 1 else wet
        mix = self._p["mix"]
        out = x2 * (1 - mix) + wet_mono * mix
        return out if x.ndim > 1 else out[:, 0]

    def latency_samples(self):
        return 0  # pedalboard.Reverb is a streaming plugin, no reported lookahead


class Dimension(Module):
    """Chorus / phaser modulation send (pedalboard.Chorus / pedalboard.Phaser).
    Both null cleanly at their own mix=0, verified, so this wraps them
    directly rather than re-deriving a dry path."""

    name = "dimension"
    params = (
        ParamSpec("mode", "enum", 0, choices=("chorus", "phaser")),
        ParamSpec("rate_hz", "float", 0.8, 0.01, 4.0, "Hz", curve="log"),
        ParamSpec("depth", "float", 0.25, 0.0, 1.0, ""),
        ParamSpec("mix", "float", 0.0, 0.0, 1.0, ""),  # off by default: creative, not corrective
    )

    def prepare(self, fs):
        self.fs = fs
        self._design()

    def _design(self):
        mode = self._p.get("mode", "chorus") if hasattr(self, "_p") else "chorus"
        rate = self._p.get("rate_hz", 0.8) if hasattr(self, "_p") else 0.8
        depth = self._p.get("depth", 0.25) if hasattr(self, "_p") else 0.25
        mix = self._p.get("mix", 0.0) if hasattr(self, "_p") else 0.0
        if mode in ("phaser", 1):
            self._board = pb.Pedalboard([pb.Phaser(rate_hz=rate, depth=depth, mix=mix)])
        else:
            self._board = pb.Pedalboard([pb.Chorus(rate_hz=rate, depth=depth, mix=mix)])

    def on_param_changed(self, name, value):
        self._design()

    def reset(self):
        self._design()

    def process(self, x: np.ndarray) -> np.ndarray:
        ch = x.shape[1] if x.ndim > 1 else 1
        x2 = x if x.ndim > 1 else x[:, None]
        stereo_in = np.concatenate([x2, x2], axis=1) if ch == 1 else x2[:, :2]
        out = _from_pb(self._board(_to_pb(stereo_in), self.fs, reset=False), 2)
        out_mono = out.mean(axis=1, keepdims=True) if ch == 1 else out
        return out_mono if x.ndim > 1 else out_mono[:, 0]

    def latency_samples(self):
        return 0
