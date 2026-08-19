"""Measure our DSP modules against the commercial plugins installed on this
machine, on the same material and the same meters.

    PYTHONPATH=src ../.venv/bin/python tools/ab_reference.py

NOTHING HERE SHIPS OR IS IMPORTED BY THE PRODUCT. These plugins are closed
source and cannot be linked into the Phase-2 JUCE build. The point is purely
to stop guessing: doc 07 says "modelling each box by ear is how you land at
'in the lane' and stop", so this puts a number on the gap instead.

Compared:
  Saturation vs Newfangled Obliterate  -- alias floor and THD off the same
      sine sweep our own -90 dB bar is measured with (meter.aliasing_floor_db)
  DeEsser    vs Techivation T-De-Esser -- sibilance-band reduction on the real
      acapella, AND how much body (<4 kHz) each one damages getting there
"""
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vox import dsp, meter  # noqa: E402

VST3 = Path("/Library/Audio/Plug-Ins/VST3")
OBLITERATE = VST3 / "Newfangled Audio/Obliterate.vst3"
T_DEESSER = VST3 / "T-De-Esser.vst3"
ACAPELLA = Path.home() / "Desktop/vox references/acapellas/eminem lose vocal.wav"


def _plugin(path, **params):
    import pedalboard as pb
    p = pb.load_plugin(str(path))
    for k, v in params.items():
        setattr(p, k, v)
    return p


def _run(plugin, x, fs):
    """Mono (n,) in, mono (n,) out, length-matched."""
    stereo = np.repeat(np.asarray(x, dtype=np.float32)[:, None], 2, axis=1)
    y = plugin(np.ascontiguousarray(stereo.T), fs, reset=True).T.astype(np.float64)
    y = y.mean(axis=1)
    if len(y) < len(x):
        y = np.pad(y, (0, len(x) - len(y)))
    return y[:len(x)]


def band_db(x, fs, lo, hi, pct=None):
    """RMS in a band; with pct, the pct-th percentile of 512-sample frames --
    a de-esser only moves the loudest frames, so the mean hides its work."""
    from scipy import signal as sg
    b, a = sg.butter(4, [lo / (fs / 2), min(hi / (fs / 2), 0.999)], btype="band")
    y = sg.lfilter(b, a, x)
    if pct is None:
        return 20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-12)
    n = 512
    f = y[:len(y) // n * n].reshape(-1, n)
    return 20 * np.log10(np.percentile(np.sqrt((f ** 2).mean(1)), pct) + 1e-12)


def saturation_vs_obliterate(fs=48000):
    print("\n== Saturation: ours vs Obliterate (alias floor / THD) ==")
    ours = dsp.Saturation(fs, drive_db=4.0, mix=1.0, mode="tanh", oversample=8)
    r = meter.aliasing_floor_db(lambda s: ours.process(s[:, None])[:, 0], fs)
    print(f"  vox.Saturation   alias {r['alias_db']:7.1f} dB   THD {r['thd_db']:7.1f} dB")

    if not OBLITERATE.exists():
        print("  Obliterate       not installed")
        return
    pl = _plugin(OBLITERATE, mix=100.0, obliterate=25.0)
    r2 = meter.aliasing_floor_db(lambda s: _run(pl, s, fs), fs)
    print(f"  Obliterate       alias {r2['alias_db']:7.1f} dB   THD {r2['thd_db']:7.1f} dB")
    print(f"  -> we are {r['alias_db'] - r2['alias_db']:+.1f} dB on alias "
          f"(negative = ours is cleaner)")


def deesser_vs_tdeesser():
    print("\n== De-esser: ours vs T-De-Esser (on the real acapella) ==")
    if not ACAPELLA.exists():
        print("  reference acapella missing")
        return
    x, fs = sf.read(ACAPELLA, always_2d=True)
    x = x[:fs * 20].mean(axis=1)

    from vox import presets
    sib = presets.sibilance_level_db(x, fs)
    thr = presets._threshold_for(sib, presets.DEESS_RATIO, presets.DEESS_TARGET_GR_DB)
    print(f"  (stem esses peak at {sib:.1f} dB; both set to the derived "
          f"threshold {thr:.1f} dB, 4:1, targeting {presets.DEESS_TARGET_GR_DB:.0f} dB GR)")
    ours = dsp.DeEsser(fs, freq_hz=presets.DEESS_FREQ_HZ, threshold_db=thr,
                       ratio=presets.DEESS_RATIO, range_db=10.0, mix=1.0)
    y_ours = ours.process(x[:, None])[:, 0]

    rows = [("vox.DeEsser", y_ours)]
    if T_DEESSER.exists():
        # matched to ours as closely as the two controls allow: same band,
        # -22 dB threshold, 4:1
        pl = _plugin(T_DEESSER, frequency_lo_khz=7.0, frequency_hi_khz=16.0,
                     processing_db=round(thr, 1), intensity=4.0, mix=100.0)
        rows.append(("T-De-Esser", _run(pl, x, fs)))
    else:
        print("  T-De-Esser not installed")

    peak_dry = band_db(x, fs, 7000, 16000, pct=99)
    body_dry = band_db(x, fs, 200, 4000)
    for name, y in rows:
        print(f"  {name:14} loudest esses {band_db(y, fs, 7000, 16000, pct=99) - peak_dry:+.2f} dB   "
              f"body damage {band_db(y, fs, 200, 4000) - body_dry:+.2f} dB")
    print("  -> want: esses several dB down, body within a few tenths of 0")


if __name__ == "__main__":
    saturation_vs_obliterate()
    deesser_vs_tdeesser()
    # ponytail: these VST3s segfault in their own destructors when Python
    # tears the process down. Nothing here needs cleanup, so skip it.
    sys.stdout.flush()
    os._exit(0)
