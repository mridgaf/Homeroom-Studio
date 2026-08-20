"""Render the Eminem chain one stage at a time, cumulatively, for the owner's ear.

    PYTHONPATH=src ../.venv/bin/python tools/render_ladder.py [wav]

Each file adds ONE module to the previous one, so a stage that damages the
vocal is audible on its own instead of hidden inside the finished mix.

Stages are produced by bypassing every module past index k on a FRESH chain
(core.Chain.bypassed) -- no new DSP, and no reuse of a chain whose filter and
detector state has already been run.

Levels: nothing is trimmed on the way IN. The source's sample peak is
-0.33 dBFS -- it does not clip in float, and an input trim would silently move
the chain's three ABSOLUTE constants (gate -42/-48 dB, saturation drive, limiter
ceiling) against the material while leaving the derived thresholds where they
were. An earlier version did trim 1 dB in and claimed "everything downstream is
derived, so the trim moves with it"; that claim was false for exactly those
three modules.

Instead ONE monitoring trim is applied on the way OUT, MONITOR_TRIM_DB, the same
number on every file here AND in render_clear.py -- so the whole calibration set
can be A/B'd without a level difference deciding the owner's opinion for him.
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vox import meter, presets  # noqa: E402

DRY_SOURCE = Path.home() / "Desktop/debbie dry vocal full reason.wav"
OUT_DIR = Path.home() / "Desktop/vox references/renders/ladder"

# One shared monitoring trim for every file in the calibration set. Measured:
# the hottest stage is the compressor, which peaks +3.35 dBFS on its own,
# because its makeup gain is a fixed +4.0 dB while its threshold is derived --
# on a hot stem the limiter at the end is what rescues that. -4.5 dB puts the
# hottest file at about -1.2 dBFS and leaves the quietest well above the noise.
# check() below refuses to write anything that still exceeds full scale, so if
# a future stage gets hotter this fails loudly instead of clipping on disk.
# Applied identically everywhere, so it changes no level RELATIONSHIP.
MONITOR_TRIM_DB = -4.5

def check(y: np.ndarray, label: str):
    """Refuse to deliver a render that is broken in a way the ear would only
    notice after wasting the owner's time on it."""
    if not np.all(np.isfinite(y)):
        raise AssertionError(f"{label}: NaN/Inf in output")
    peak = float(np.max(np.abs(y)))
    if peak < 1e-4:
        raise AssertionError(f"{label}: silent output (peak {peak:.2e})")
    if peak > 1.0:
        raise AssertionError(f"{label}: clipped, peak {20*np.log10(peak):+.2f} dBFS")
    return peak


def ladder(x: np.ndarray, fs: float):
    """Yield (index, name, audio) for dry, then each cumulative stage."""
    a = presets.analyse(x, fs)
    print(f"analysed: program={a['program_db']:.1f} dB  "
          f"sibilance={a['sibilance_db']:.1f} dB  ess from {a['deess_freq_hz']:.0f} Hz")
    # Names come off the modules themselves, so a preset change can never
    # mislabel a file. The reverb stage is conditional on pedalboard.
    names = [m.name for m in presets.build_eminem_chain(fs, **a).modules]
    n = len(names)
    yield 0, "dry", x
    for k in range(n):
        chain = presets.build_eminem_chain(fs, **a)
        chain.bypassed = set(range(k + 1, n))
        name = names[k] if k < n - 1 else f"FINAL {names[k]}"
        yield k + 1, name, chain.process(x)


def main(argv=()):
    src = Path(argv[0]) if argv else DRY_SOURCE
    x, fs = sf.read(src, always_2d=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{src.name}  fs={fs}  {len(x)/fs:.1f} s  "
          f"monitoring trim {MONITOR_TRIM_DB:+.1f} dB on every file\n")
    g = 10.0 ** (MONITOR_TRIM_DB / 20.0)
    for i, name, y in ladder(x, fs):
        y = y * g
        check(y, name)
        out = OUT_DIR / f"{i:02d} {name}.wav"
        sf.write(out, y, int(fs), subtype="PCM_24")
        print(f"  {out.name:24}", meter.report(y.mean(axis=1), fs, name))


if __name__ == "__main__":
    main(sys.argv[1:])
