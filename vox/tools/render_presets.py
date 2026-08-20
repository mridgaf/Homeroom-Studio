"""Render every artist preset over a clean, unprocessed vocal, for the owner's ear.

    PYTHONPATH=src ../.venv/bin/python tools/render_presets.py [wav ...]

Renders MUST use dry source material. The reference acapellas in
`vox references/acapellas` are commercial releases -- they already carry the
full production chain, so stacking our chain on top grades nothing. They stay
in place as A/B *targets* (tools/ab_reference.py), never as render inputs.

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
OUT_DIR = REFS / "renders"
DRY_SOURCES = [Path.home() / "Desktop/debbie8 13 26 vc loop reason.wav"]


def main(argv=()):
    sources = [Path(a) for a in argv] or DRY_SOURCES
    OUT_DIR.mkdir(exist_ok=True)
    for wav in sources:
        x, fs = sf.read(wav, always_2d=True)
        a = presets.analyse(x, fs)
        print(f"\n{wav.name}  fs={fs}  program={a['program_db']:.1f} dB  "
              f"sibilance={a['sibilance_db']:.1f} dB  ess band from {a['deess_freq_hz']:.0f} Hz")
        print("  dry   ", meter.report(x.mean(axis=1), fs, "dry"))
        for name, build in presets.PRESETS.items():
            y = build(fs, **a).process(x)
            out = OUT_DIR / f"{wav.stem.split()[0]}__{name}.wav"
            sf.write(out, y, int(fs), subtype="PCM_24")
            print(f"  {name:6}", meter.report(y.mean(axis=1), fs, name), "->", out.name)


if __name__ == "__main__":
    main(sys.argv[1:])
