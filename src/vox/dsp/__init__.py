"""
vox.dsp -- all processing modules.

Layout:
  modules.py   EQ / Compressor / Gate / De-esser / Saturation / Limiter
               (all real-time-safe, per-block, from vox.core.Module)
  dereverb.py  Single-channel statistical late-reverb suppression
               (causal, fixed-latency, real-time-capable)

Anything ML-based (denoise) lives in vox.engines, kept separate because it
carries a heavy torch/DeepFilterNet dependency the plugin build will not want
for the DSP-only modules above.
"""
from .modules import (
    Band, ParametricEQ, Detector, Compressor, Gate, DeEsser, Saturation, Limiter,
)
from .dereverb import estimate_rt60_bands, suppress_late_reverb

try:
    from .pedalboard_modules import ReverbSend, Dimension
    _HAS_PEDALBOARD = True
except ImportError:
    _HAS_PEDALBOARD = False

__all__ = [
    "Band", "ParametricEQ", "Detector", "Compressor", "Gate", "DeEsser",
    "Saturation", "Limiter", "estimate_rt60_bands", "suppress_late_reverb",
]
if _HAS_PEDALBOARD:
    __all__ += ["ReverbSend", "Dimension"]
