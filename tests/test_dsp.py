"""DSP module verification: bypass nulls, aliasing bar, and the limiter's
true-peak accuracy (this file exists because that measurement caught two real
bugs during development -- see dsp/modules.py Limiter docstring)."""
import numpy as np
import pytest
from scipy import signal as sg

from vox import dsp, meter

FS = 48000


def sine(f, dbfs=0.0, dur=0.5, fs=FS, phase=0.0):
    t = np.arange(int(dur * fs)) / fs
    return (10 ** (dbfs / 20)) * np.sin(2 * np.pi * f * t + phase)


# ---------------------------------------------------------------- bypass nulls
def test_compressor_unity_ratio_nulls():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.Compressor(FS, threshold_db=0.0, ratio=1.0, makeup_db=0.0, mix=1.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_eq_zero_gain_nulls():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.ParametricEQ(FS, bands=[dict(kind="bell", freq=1000, gain_db=0.0, q=1.0)]).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_saturation_zero_mix_nulls():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.Saturation(FS, mix=0.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_gate_settles_open_and_transparent():
    """After the cold-start attack ramp, an always-above-threshold signal
    must pass through unchanged."""
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.Gate(FS, open_db=-90, close_db=-95).process(x[:, None])[:, 0]
    assert meter.null_test_db(x[2400:], y[2400:]) < -300


# ---------------------------------------------------------------- aliasing bar
def test_saturation_8x_tanh_meets_bar():
    s = dsp.Saturation(FS, drive_db=12.0, mix=1.0, mode="tanh", oversample=8)
    r = meter.aliasing_floor_db(lambda x: s.process(x[:, None])[:, 0], FS)
    assert r["alias_db"] < -90, r


def test_saturation_4x_tanh_fails_bar():
    """Documents WHY the default is 8x: 4x measurably fails our own bar."""
    s = dsp.Saturation(FS, drive_db=12.0, mix=1.0, mode="tanh", oversample=4)
    r = meter.aliasing_floor_db(lambda x: s.process(x[:, None])[:, 0], FS)
    assert r["alias_db"] > -90


def test_saturation_adaa_hardclip_meets_bar():
    s = dsp.Saturation(FS, drive_db=12.0, mix=1.0, mode="adaa_hardclip", oversample=8)
    r = meter.aliasing_floor_db(lambda x: s.process(x[:, None])[:, 0], FS)
    assert r["alias_db"] < -90, r


# ---------------------------------------------------------------- limiter
@pytest.mark.parametrize("f0,phase", [
    (997, 0.0), (12000, 0.7), (12000, 0.3), (19000, 0.0), (20500, 0.3), (8000, 1.1),
])
def test_limiter_never_exceeds_true_peak_ceiling(f0, phase):
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0, lookahead_ms=5.0)
    x = 1.3 * sine(f0, dur=0.5, phase=phase)
    y = lim.process(x[:, None])[:, 0]
    tp = meter.true_peak_db(y, FS)
    assert tp <= -1.0 + 0.15, f"overshoot at {f0}Hz phase {phase}: {tp} dBTP"


def test_limiter_transparent_below_ceiling():
    """A signal already well under the ceiling must pass through essentially
    unchanged (aside from the reported lookahead delay)."""
    x = np.random.RandomState(1).randn(FS) * 0.05
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0)
    y = lim.process(x[:, None])[:, 0]
    la = lim.la_n
    assert meter.null_test_db(x[:-la], y[la:]) < -60


def test_limiter_detector_matches_reference_meter():
    """The detector's own true-peak estimate must agree with meter.true_peak_db
    (independently implemented) to within 0.05 dB -- this is the check that
    caught the rectify-before-interpolate bug."""
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0)
    x = 1.3 * sine(12000, dur=0.5, phase=0.7)
    env = lim._true_peak_envelope(x[:, None])
    got = 20 * np.log10(env.max())
    want = meter.true_peak_db(x, FS)
    assert abs(got - want) < 0.05, (got, want)
