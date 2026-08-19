"""Render every artist preset over the reference acapellas, for the owner's ear.

    PYTHONPATH=src ../.venv/bin/python tools/render_presets.py

Each render measures the stem's own program level first and passes it into the
preset builder -- the thresholds are derived from it, not hardcoded (see
presets.NOMINAL_PROGRAM_DB for the bug that rule exists to prevent).
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vox import meter, presets  # noqa: E402

REFS = Path.home() / "Desktop/vox references"
IN_DIR, OUT_DIR = REFS / "acapellas", REFS / "renders"


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for wav in sorted(IN_DIR.glob("*.wav")):
        x, fs = sf.read(wav, always_2d=True)
        prog = presets.program_level_db(x, fs)
        sib = presets.sibilance_level_db(x, fs)
        print(f"\n{wav.name}  fs={fs}  program={prog:.1f} dB  sibilance={sib:.1f} dB")
        print("  dry   ", meter.report(x.mean(axis=1), fs, "dry"))
        for name, build in presets.PRESETS.items():
            y = build(fs, program_db=prog, sibilance_db=sib).process(x)
            out = OUT_DIR / f"{wav.stem.split()[0]}__{name}.wav"
            sf.write(out, y, int(fs), subtype="PCM_24")
            print(f"  {name:6}", meter.report(y.mean(axis=1), fs, name), "->", out.name)


if __name__ == "__main__":
    main()
