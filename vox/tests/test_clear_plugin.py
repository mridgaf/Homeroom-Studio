"""Supertone Clear wrapper. Skipped anywhere the plugin isn't installed --
it is a commercial dependency that deliberately cannot ship (see
engines/clear_plugin.py), so these can never be required to pass in CI."""
import numpy as np
import pytest

from vox.engines import clear_plugin

pytestmark = pytest.mark.skipif(not clear_plugin.available(),
                                reason="Supertone Clear not installed")
FS = 48000


def test_clear_returns_same_shape_and_stays_aligned():
    """The plugin misreports its latency (says 1636, runs ~5632 late) and
    returns a different sample count than it was given -- the wrapper's whole
    job is hiding that. A drifting result would silently smear every stage
    downstream of it."""
    t = np.arange(3 * FS) / FS
    env = (t % 0.5 < 0.25).astype(float)
    x = (0.3 * np.sin(2 * np.pi * 200 * t) * env)[:, None] * np.ones((1, 2))
    y = clear_plugin.clean(x, FS)
    assert y.shape == x.shape
    from scipy import signal as sig
    c = sig.correlate(y[:, 0], x[:, 0], mode="full")
    lag = int(np.argmax(np.abs(c)) - (len(x) - 1))
    assert abs(lag) <= 64, f"output drifted {lag} samples"
