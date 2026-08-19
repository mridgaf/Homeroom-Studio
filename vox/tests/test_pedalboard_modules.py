"""Coverage for dsp/pedalboard_modules.py -- see docs/06_REAL_STEM_FINDINGS.md
for the full evaluation (why Limiter/Distortion are banned, why Reverb needed
an external dry/wet fix, why the -90dB alias bar doesn't apply to modulation
effects)."""
import numpy as np
import pytest

pb = pytest.importorskip("pedalboard")
from vox.dsp.pedalboard_modules import ReverbSend, Dimension  # noqa: E402
from vox import meter  # noqa: E402

FS = 48000


def test_reverb_send_nulls_at_zero_mix():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = ReverbSend(FS, mix=0.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_reverb_send_adds_energy_at_nonzero_mix():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = ReverbSend(FS, mix=0.3, room_size=0.7).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) > -60  # should audibly differ


@pytest.mark.parametrize("mode", ["chorus", "phaser"])
def test_dimension_nulls_at_zero_mix(mode):
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = Dimension(FS, mode=mode, mix=0.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -120  # float32-round-trip limited, not exact


def test_pedalboard_limiter_overshoots_true_peak_ceiling():
    """Documents WHY we never use pedalboard.Limiter: it is a sample-peak
    limiter, not a true-peak one. This is an intentional 'must stay failing'
    test -- if pedalboard ever fixes this upstream, update
    docs/06_REAL_STEM_FINDINGS.md, don't just delete the test."""
    t = np.arange(int(0.5 * FS)) / FS
    x = 1.3 * np.sin(2 * np.pi * 12000 * t + 0.7)
    board = pb.Pedalboard([pb.Limiter(threshold_db=-1.0, release_ms=80.0)])
    y = board(np.stack([x, x]).astype(np.float32), FS)[0].astype(np.float64)
    tp = meter.true_peak_db(y, FS)
    assert tp > -1.0 + 0.15, f"pedalboard.Limiter is apparently fixed now ({tp} dBTP)"
