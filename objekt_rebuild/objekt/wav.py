"""WAV output utilities."""

from __future__ import annotations

from pathlib import Path
import wave
import numpy as np


def write_wav(path: str | Path, audio: np.ndarray, sample_rate: int) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    data = np.asarray(audio, dtype=np.float64)
    if data.ndim == 1:
        data = np.column_stack((data, data))
    if data.ndim != 2 or data.shape[1] != 2:
        raise ValueError("audio must be mono or stereo")
    pcm = np.clip(data, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype("<i2")
    with wave.open(str(target), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(int(sample_rate))
        handle.writeframes(pcm.tobytes())
    return target
