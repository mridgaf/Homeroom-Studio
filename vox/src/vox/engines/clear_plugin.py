"""
Supertone Clear (VST3) as the cleanup pre-pass -- source separation into
voice / voice-reverb / ambience, so dereverb and denoise become "turn that
stem down" instead of statistical suppression.

WHY THIS EXISTS: vox's own two cleanup stages are both documented broken on
real material -- dereverb.py destroys a sustained dry tone by ~20 dB and
DeepFilterNet over-suppresses sustained non-speech-like content by 59 dB
(docs/06_REAL_STEM_FINDINGS.md). Both are OFF by default and have been for
months. Clear does the same job properly, and it is already installed on this
machine.

CANNOT SHIP. Read this before building anything on top of it:
  - It is a commercial closed-source plugin. It cannot be linked into the
    Phase-2 JUCE/C++ build, and a render that went through it cannot be
    reproduced by anyone without a Supertone licence.
  - So this is opt-in (clear=False everywhere) and lives in engines/, next to
    the other heavy non-shippable dependency, NOT in dsp/. Nothing in dsp/ or
    presets.py may import it.
  - Its value is that it tells us what the cleanup stage is SUPPOSED to sound
    like. When the native replacement gets rebuilt, this is its target.

Not real-time-legal either: it reports 1636 samples of latency but actually
runs ~5.6k samples late and returns a different number of samples than it was
given, so the wrapper below re-aligns by measured cross-correlation against
the dry input. That is an offline two-pass operation by definition.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

PLUGIN_PATH = Path("/Library/Audio/Plug-Ins/VST3/Clear.vst3")

_PLUGIN = None


def available() -> bool:
    try:
        import pedalboard  # noqa: F401
    except ImportError:
        return False
    return PLUGIN_PATH.exists()


def _lazy_load():
    """One instance, reused: instantiating a VST3 costs ~1 s."""
    global _PLUGIN
    if _PLUGIN is None:
        import pedalboard as pb
        _PLUGIN = pb.load_plugin(str(PLUGIN_PATH))
    return _PLUGIN


def _align_to(dry: np.ndarray, wet: np.ndarray) -> np.ndarray:
    """Trim `wet` back onto `dry`'s timeline and length.

    ponytail: lag is measured by cross-correlating the real signal, because
    the plugin's own reported_latency_samples (1636) does not match what it
    actually does (~5632). An impulse calibration would be cheaper but a
    source separator outputs nothing useful for an impulse -- there's no voice
    in it. If Supertone ever fixes the reported figure, delete this and use it.
    """
    from scipy import signal as sig

    n = min(len(dry), len(wet))
    c = sig.correlate(wet[:n, 0], dry[:n, 0], mode="full")
    lag = int(np.argmax(np.abs(c)) - (n - 1))
    if lag < 0:
        wet = np.vstack([np.zeros((-lag, wet.shape[1])), wet])
    else:
        wet = wet[lag:]
    if len(wet) < len(dry):
        wet = np.vstack([wet, np.zeros((len(dry) - len(wet), wet.shape[1]))])
    return wet[:len(dry)]


def clean(x: np.ndarray, fs: float, dereverb_db: float = -60.0,
          denoise_db: float = -60.0, voice_db: float = 0.0) -> np.ndarray:
    """Separate and rebalance. Defaults kill the room and the ambience bed
    entirely and leave the voice at unity -- the "dry vocal, please" case.

    Dial the cuts back (e.g. -12) to keep some of the original space rather
    than a fully dead stem; full removal of a room the performance was sung
    into can sound sucked-out on its own, which is exactly the trap doc 07
    warns about for the Tupac profile ("take processing away, then add tape").

    x: (n, ch) float64, returned the same shape and time-aligned.
    """
    if not available():
        raise RuntimeError(f"Supertone Clear not found at {PLUGIN_PATH}")
    x2 = x[:, None] if x.ndim == 1 else x
    stereo = np.repeat(x2, 2, axis=1) if x2.shape[1] == 1 else x2[:, :2]

    p = _lazy_load()
    p.voice_gain = float(voice_db)
    p.voice_reverb_gain = float(dereverb_db)
    p.ambience_gain = float(denoise_db)
    p.bypass = False

    # tail padding so the plugin's own latency doesn't eat the last phrase
    fed = np.vstack([stereo, np.zeros((16384, 2))])
    wet = p(np.ascontiguousarray(fed.T.astype(np.float32)), fs,
            reset=True).T.astype(np.float64)
    wet = _align_to(stereo, wet)

    out = wet.mean(axis=1, keepdims=True) if x2.shape[1] == 1 else wet
    return out if x.ndim > 1 else out[:, 0]
