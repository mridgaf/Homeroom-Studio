"""Supertone Clear on the dry vocal, alone and under the Eminem chain.

    PYTHONPATH=src ../.venv/bin/python tools/render_clear.py [wav]

Four files, so the owner can hear what Clear does by itself before judging what
it does underneath the chain:

    C1  Clear, room kept      (dereverb/denoise -12 dB)
    C2  Clear, room removed   (dereverb/denoise -60 dB)
    C3  C1 -> Eminem chain
    C4  C2 -> Eminem chain

REFERENCE ONLY. Clear is a closed-source commercial VST3: it cannot go into the
Phase-2 JUCE build and nothing in dsp/ or presets.py may import it. These
renders exist to define what the native cleanup stage is SUPPOSED to sound
like -- see engines/clear_plugin.py.

C3/C4 re-analyse AFTER Clear, because Clear changes the level and the HF
balance the chain's thresholds are derived from.

These carry the SAME MONITOR_TRIM_DB as the ladder. Without it the Clear
renders sat 4.5 dB louder than the ladder's finished mix, and louder-is-better
would have decided the A/B before the owner heard a single difference.
"""
import sys
from pathlib import Path

import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vox import meter, presets  # noqa: E402
from vox.engines import clear_plugin  # noqa: E402
from render_ladder import DRY_SOURCE, MONITOR_TRIM_DB, check  # noqa: E402

OUT_DIR = Path.home() / "Desktop/vox references/renders/clear"
VARIANTS = {"room kept": -12.0, "room removed": -60.0}


def main(argv=()):
    if not clear_plugin.available():
        raise SystemExit(f"Supertone Clear not found at {clear_plugin.PLUGIN_PATH}")
    src = Path(argv[0]) if argv else DRY_SOURCE
    x, fs = sf.read(src, always_2d=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{src.name}  fs={fs}  {len(x)/fs:.1f} s  "
          f"monitoring trim {MONITOR_TRIM_DB:+.1f} dB on every file\n")
    g = 10.0 ** (MONITOR_TRIM_DB / 20.0)

    for i, (label, db) in enumerate(VARIANTS.items(), start=1):
        cleaned = clear_plugin.clean(x, fs, dereverb_db=db, denoise_db=db)
        a = presets.analyse(cleaned, fs)
        print(f"  (post-Clear: program={a['program_db']:.1f} dB  "
              f"ess from {a['deess_freq_hz']:.0f} Hz)")
        chained = presets.build_eminem_chain(fs, **a).process(cleaned)
        for name, y in ((f"C{i} clear {label}", cleaned),
                        (f"C{i+2} clear {label} + chain", chained)):
            y = y * g
            check(y, name)
            out = OUT_DIR / f"{name}.wav"
            sf.write(out, y, int(fs), subtype="PCM_24")
            print(f"  {out.name:34}", meter.report(y.mean(axis=1), fs, name))


if __name__ == "__main__":
    main(sys.argv[1:])
