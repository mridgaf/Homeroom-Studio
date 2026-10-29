"""Render a short four-preset audition phrase."""

from pathlib import Path
import numpy as np

from objekt import ObjektConfig, ObjektSynth, write_wav
from objekt.dsp import peak_normalize, soft_limit


SAMPLE_RATE = 48_000


def main() -> None:
    synth = ObjektSynth(SAMPLE_RATE)
    sections = []
    phrases: list[tuple[str, list[tuple[float, float, float, float]]]] = [
        ("glass_bell", [(0.0, 60, 0.9, 0.35), (0.45, 64, 0.78, 0.35), (0.9, 67, 0.84, 0.4), (1.4, 72, 0.72, 0.45)]),
        ("wood_mallet", [(0.0, 48, 0.95, 0.22), (0.28, 55, 0.72, 0.22), (0.56, 60, 0.82, 0.22), (0.84, 55, 0.66, 0.25)]),
        ("metal_plate", [(0.0, 52, 0.86, 0.55), (0.55, 59, 0.68, 0.55), (1.1, 64, 0.76, 0.65)]),
        ("imaginary_string", [(0.0, 45, 0.82, 0.7), (0.65, 52, 0.74, 0.7), (1.3, 57, 0.78, 0.8)]),
    ]
    for seed, (preset, events) in enumerate(phrases, start=10):
        config = ObjektConfig.from_preset(preset)
        sections.append(synth.render_sequence(events, config, tail=1.1, seed=seed))
        sections.append(np.zeros((int(0.25 * SAMPLE_RATE), 2), dtype=np.float32))
    audio = np.concatenate(sections, axis=0)
    audio = peak_normalize(soft_limit(audio, 1.15), 0.94).astype(np.float32)
    target = Path("artifacts/objekt-clean-room-demo.wav")
    write_wav(target, audio, SAMPLE_RATE)
    print(f"wrote {target} ({len(audio) / SAMPLE_RATE:.2f}s)")


if __name__ == "__main__":
    main()
