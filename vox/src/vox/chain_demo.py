"""
Reference signal chain, phase-1 order (subject to revision once the master
spec from the adversarial design workflow lands):

  1. Gate            -- remove room tone between phrases before anything else
                         sees it (matches producer guidance: gate before comp)
  2. De-reverb        -- statistical late-reverb suppression. VERIFIED BROKEN
                          on sustained content (destroys a dry sustained tone
                          by ~20 dB, see docs/06_REAL_STEM_FINDINGS.md) --
                          OFF by default. Do not re-enable until it's rebuilt
                          to distinguish sustained-dry from actual reverb.
  3. Denoise (ML)     -- DeepFilterNet3. VERIFIED to over-suppress sustained
                          non-speech-like content (dry tone -18 to -21 dB at full
                          wet) -- OFF by default for the same reason.
  4. De-esser         -- ahead of the compressor, so sibilance isn't pumped by
                          gain reduction downstream (producer's ordering call)
  5. EQ (corrective)  -- subtractive resonance control
  6. Compressor       -- two-stage in the real product; one stage here
  7. Saturation       -- 8x oversampled tanh, glue/warmth
  8. EQ (tonal)       -- broad musical shaping (air, low-end)
  9. Reverb send      -- pedalboard-backed (Phase 1 only, see
                          dsp/pedalboard_modules.py), mix=0 by default --
                          available, verified, not engaged
  10. Dimension       -- chorus/phaser, pedalboard-backed, mix=0 by default --
                          creative effect, not a default cleanup stage
  11. Limiter         -- true-peak safe final stage, always on, always last

This module exists to PROVE the pieces interoperate and to produce a
measurable before/after. It is a scaffold, not the final product chain --
that comes out of the adversarial workflow synthesis.
"""
from __future__ import annotations

import numpy as np

from . import dsp, meter
from .core import Chain


def build_chain(fs: float) -> Chain:
    modules = [
        dsp.Gate(fs, open_db=-42.0, close_db=-48.0, ratio=6.0,
                 attack_s=0.001, release_s=0.12),
        dsp.DeEsser(fs, freq_hz=7000.0, threshold_db=-22.0, ratio=4.0,
                    range_db=10.0, mix=1.0),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="highpass", freq=80.0, q=0.707),
            dict(kind="bell", freq=300.0, gain_db=-2.0, q=1.2),   # mud control
            dict(kind="bell", freq=3200.0, gain_db=1.5, q=1.0),   # presence
        ]),
        dsp.Compressor(fs, threshold_db=-20.0, ratio=3.0, knee_db=6.0,
                       attack_s=0.008, release_s=0.15, makeup_db=6.0, mix=1.0),
        dsp.Saturation(fs, drive_db=4.0, mix=0.15, mode="tanh", oversample=8),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="high_shelf", freq=9000.0, gain_db=2.0, q=0.707),
        ]),
    ]
    if getattr(dsp, "_HAS_PEDALBOARD", False):
        modules += [
            dsp.ReverbSend(fs, room_size=0.5, damping=0.5, mix=0.0),   # off by default
            dsp.Dimension(fs, mode="chorus", mix=0.0),                 # off by default
        ]
    modules.append(dsp.Limiter(fs, ceiling_dbtp=-1.0, lookahead_ms=5.0, release_s=0.08))
    return Chain(fs, modules)


def run_dsp_chain(x: np.ndarray, fs: float) -> np.ndarray:
    """The non-ML, per-block-legal part of the chain."""
    c = build_chain(fs)
    x2 = x[:, None] if x.ndim == 1 else x
    y = c.process(x2)
    return y[:, 0] if x.ndim == 1 else y


def run_full_pipeline(x: np.ndarray, fs: float, dereverb: bool = False,
                      denoise_blend: float = 0.0, clear: bool = False) -> dict:
    """Cleanup stage (dereverb + ML denoise, offline/two-pass) followed by the
    real-time-legal shaping chain. Returns every intermediate stage so the
    contribution of each can be measured independently.

    Defaults are OFF for both cleanup stages: both are verified to damage
    sustained content (docs/06_REAL_STEM_FINDINGS.md). Opt in explicitly and
    listen critically -- don't trust the numbers alone, see that doc for why."""
    from .dsp import suppress_late_reverb

    stages = {"input": x}
    y = x

    if clear:
        # Supertone Clear replaces BOTH broken cleanup stages below with real
        # source separation -- but it is a commercial plugin that cannot ship
        # (see engines/clear_plugin.py). Opt-in, and it wins if both are asked
        # for, because the native ones are documented broken.
        from .engines.clear_plugin import clean
        y = clean(y, fs)
        stages["after_clear"] = y
        dereverb, denoise_blend = False, 0.0

    if dereverb:
        y, _info = suppress_late_reverb(y, fs)
        stages["after_dereverb"] = y

    if denoise_blend > 0:
        from .engines.denoise_dfn import denoise
        r = denoise(y, fs, blend=denoise_blend)
        y = r.audio[: len(y)] if len(r.audio) >= len(y) else np.pad(r.audio, (0, len(y) - len(r.audio)))
        stages["after_denoise"] = y

    y = run_dsp_chain(y, fs)
    stages["output"] = y
    return stages


def measure_stages(stages: dict, fs: float) -> dict:
    return {name: meter.report(sig_, fs, name) for name, sig_ in stages.items()}
