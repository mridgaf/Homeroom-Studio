"""
DeepFilterNet3 wrapper (MIT/Apache-2.0, pretrained weights included).

MEASURED, not assumed (see /tmp session notes, to be folded into
docs/05_findings.md): on a 48 kHz synthetic vocal, DFN cuts the noise floor
in silent passages by ~36 dB. On the same synthetic signal it does NOT show a
clear full-signal SNR win, likely because DFN is trained on real human speech
statistics and this project's LF-pulse/formant synthesis isn't a great match,
and because DFN is a speech/VoIP model, not a singing model -- it may treat
sustained vowels and vibrato as content to smooth over.

CONSEQUENCE FOR THE PRODUCT: this stage ships as an operator-controlled BLEND
(dry/wet), defaulting conservative, not as a forced full-strength stage. It
must be validated again on a real vocal stem before the default blend amount
is finalized.

Runs entirely offline / two-pass in Phase 1 (loads a ~2 s of context-free
model; no whole-file dependency, so it CAN run block-wise for the future
real-time port -- DeepFilterNet's own design targets low-latency streaming).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .. import _torchaudio_shim  # noqa: F401  (must run before `import df`)

_MODEL = None
_STATE = None
_DF_SR = 48000


def _lazy_init():
    global _MODEL, _STATE
    if _MODEL is None:
        import torch  # noqa: F401
        from df.enhance import init_df
        _MODEL, _STATE, _ = init_df()
    return _MODEL, _STATE


@dataclass
class DenoiseResult:
    audio: np.ndarray
    blend: float
    model_sr: int
    latency_ms: float


def denoise(x: np.ndarray, fs: float, blend: float = 0.35) -> DenoiseResult:
    """
    x: mono float64/32 array at any fs (resampled to the model's native 48k
       internally, then back -- DeepFilterNet3 is trained at 48 kHz only).
    blend: 0..1 dry/wet. Default 0.35 is deliberately conservative given the
           measured caveat above; raise it per-source once validated on real
           material.
    """
    import torch
    from scipy.signal import resample_poly
    from df.enhance import enhance

    model, state = _lazy_init()

    x = np.asarray(x, dtype=np.float64)
    if fs != _DF_SR:
        from math import gcd
        g = gcd(int(fs), _DF_SR)
        xin = resample_poly(x, _DF_SR // g, int(fs) // g)
    else:
        xin = x

    audio = torch.from_numpy(xin).float().unsqueeze(0)
    enhanced = enhance(model, state, audio).squeeze(0).numpy()

    n = min(len(xin), len(enhanced))
    wet = enhanced[:n]
    dry = xin[:n]
    mixed = blend * wet + (1.0 - blend) * dry

    if fs != _DF_SR:
        g = gcd(int(fs), _DF_SR)
        mixed = resample_poly(mixed, int(fs) // g, _DF_SR // g)
        mixed = mixed[: len(x)] if len(mixed) >= len(x) else np.pad(mixed, (0, len(x) - len(mixed)))

    # DeepFilterNet3 processes in ~10ms frames with lookahead; reported model
    # latency per its own docs is ~40ms algorithmic. We surface that number
    # rather than measure it per-call (measuring would require a click track).
    return DenoiseResult(audio=mixed, blend=blend, model_sr=_DF_SR, latency_ms=40.0)
