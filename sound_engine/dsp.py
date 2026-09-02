"""Load/save any audio format via pedalboard.io, at the file's own sample
rate — reuses tools/audio_engine.py for the actual effects instead of
duplicating DSP code."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pedalboard.io as pbio

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import audio_engine  # noqa: E402


def load_audio(path):
    """Returns (L, R, sample_rate). Mono sources are duplicated to
    stereo; anything beyond 2 channels is truncated to the first two."""
    with pbio.AudioFile(str(path)) as f:
        sr = f.samplerate
        audio = f.read(f.frames)
    if audio.shape[0] == 1:
        audio = np.vstack([audio[0], audio[0]])
    elif audio.shape[0] > 2:
        audio = audio[:2]
    return audio[0].astype(np.float64), audio[1].astype(np.float64), sr


def save_wav(path, L, R, sr):
    stereo = np.stack([L, R]).astype(np.float32)
    with pbio.AudioFile(str(path), "w", sr, num_channels=2) as f:
        f.write(stereo)
