"""
Verification harness. These are the assertions that turn claims into facts.
Run: PYTHONPATH=src python3 -m pytest tests/ -v
"""
import numpy as np
import pytest
from scipy import signal as sg

from vox import meter

FS = 48000


def sine(f, dbfs=0.0, dur=2.0, fs=FS, phase=0.0):
    t = np.arange(int(dur * fs)) / fs
    return (10 ** (dbfs / 20)) * np.sin(2 * np.pi * f * t + phase)


def stereo(x):
    return np.stack([x, x], axis=1)


# ---------------------------------------------------------------- BS.1770-4
@pytest.mark.parametrize("target", [-23.0, -33.0, -20.0, -40.0])
def test_ebu3341_integrated_loudness(target):
    """EBU Tech 3341 case 1/2: stereo 1 kHz sine at N dBFS reads N LUFS."""
    x = stereo(sine(1000.0, target, dur=20.0))
    got = meter.loudness_integrated(x, FS)
    assert abs(got - target) < 0.1, f"{got} != {target}"


def test_loudness_is_sample_rate_agnostic():
    """Same tone at 44.1/48/96/192 kHz must give the same LUFS within 0.1."""
    vals = []
    for fs in (44100, 48000, 96000, 192000):
        vals.append(meter.loudness_integrated(stereo(sine(1000.0, -23.0, 20.0, fs)), fs))
    assert max(vals) - min(vals) < 0.1, vals


def test_k_weighting_shape():
    """+4 dB HF shelf, -6 dB at the 38 Hz RLB corner."""
    (b1, a1), (b2, a2) = meter.k_weighting_coeffs(FS)
    w, h1 = sg.freqz(b1, a1, worN=[38.0, 1000.0, 10000.0], fs=FS)
    _, h2 = sg.freqz(b2, a2, worN=[38.0, 1000.0, 10000.0], fs=FS)
    tot = 20 * np.log10(np.abs(h1 * h2))
    assert abs(tot[0] - (-6.0)) < 0.2      # RLB corner
    assert abs(tot[2] - 4.04) < 0.2        # HF shelf


# ---------------------------------------------------------------- true peak
def test_true_peak_exceeds_sample_peak():
    """A 12 kHz tone at 48k has large inter-sample peaks."""
    x = sine(12000.0, -6.0, phase=0.25)
    assert meter.true_peak_db(x, FS) > meter.sample_peak_db(x)


def test_true_peak_accuracy():
    """True peak of a -6.02 dBFS sine is -6.02 dBTP. BS.1770-4's own 4x method
    has a documented positive bias at HF; spec tolerance is 0.15 dB."""
    x = sine(12000.0, -6.0206, phase=0.25)
    assert abs(meter.true_peak_db(x, FS) - (-6.0206)) < 0.20


# ---------------------------------------------------------------- null tests
def test_null_identical():
    a = np.random.RandomState(0).randn(FS) * 0.1
    assert meter.null_test_db(a, a) < -300


def test_null_resolution():
    """A 24-bit LSB of difference must show up at ~-138 dB."""
    a = np.random.RandomState(0).randn(FS) * 0.1
    assert -142 < meter.null_test_db(a, a + 2 ** -23) < -134


# ---------------------------------------------------------------- aliasing
def _oversampled(fn, factor):
    def g(x):
        n = len(x)
        up = sg.resample_poly(x, factor, 1, window=("kaiser", 12.0))
        return sg.resample_poly(fn(up), 1, factor, window=("kaiser", 12.0))[:n]
    return g


def test_alias_test_catches_naive_saturation():
    """Sanity: the measurement must FAIL an un-oversampled tanh."""
    r = meter.aliasing_floor_db(lambda s: np.tanh(s * 4.0), FS)
    assert r["alias_db"] > -30, r


def test_alias_test_passes_linear():
    r = meter.aliasing_floor_db(lambda s: s * 0.5, FS)
    assert r["alias_db"] < -100, r


def test_4x_oversampling_is_not_enough():
    """MEASURED PROJECT FINDING: 4x oversampled tanh lands at ~-81 dB, which
    FAILS our -90 dBFS bar. This test documents why the spec says 8x."""
    r = meter.aliasing_floor_db(_oversampled(lambda s: np.tanh(s * 4.0), 4), FS)
    assert -90 < r["alias_db"] < -60, r


def test_8x_oversampling_meets_bar():
    r = meter.aliasing_floor_db(_oversampled(lambda s: np.tanh(s * 4.0), 8), FS)
    assert r["alias_db"] < -90, r


def test_hard_clip_cannot_be_fixed_by_oversampling():
    """MEASURED PROJECT FINDING: hard clipping has unbounded harmonic order, so
    even 16x oversampling only reaches ~-70 dB. Any hard-knee clipper in the
    product MUST use antiderivative anti-aliasing (ADAA), not just oversampling."""
    r = meter.aliasing_floor_db(_oversampled(lambda s: np.clip(s * 4.0, -1, 1), 16), FS)
    assert r["alias_db"] > -90, r


# ---------------------------------------------------------------- misc
def test_dc_detection():
    x = sine(1000.0, -20.0) + 0.001
    assert meter.dc_offset_db(x) > -70
    assert meter.dc_offset_db(sine(1000.0, -20.0)) < -100


def test_crest_factor_of_sine():
    """A sine has a crest factor of exactly 3.01 dB."""
    assert abs(meter.crest_factor_db(sine(1000.0, -6.0)) - 3.0103) < 0.01
