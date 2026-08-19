"""Chain-level behaviour: per-module dry mix, delay compensation, lifecycle.

These exist because the Chain docstring promised "dry-path delay compensation"
that was not implemented -- the same latency bug as Saturation, one level up.
"""
import numpy as np
import pytest
from scipy import signal as sg

from vox import dsp, meter
from vox.core import Chain, Module

FS = 48000


def _ripple_db(y, x, fs=FS, lo=100.0, hi=15000.0):
    f, pxx = sg.welch(x, fs, nperseg=8192)
    _, pyy = sg.welch(y, fs, nperseg=8192)
    band = (f >= lo) & (f < hi)
    h = 10 * np.log10(pyy[band] / pxx[band])
    return h.min(), h.max()


@pytest.mark.parametrize("mix", [0.25, 0.5, 0.75])
def test_chain_partial_mix_compensates_module_latency(mix):
    """REGRESSION: Chain.process blended each module's wet output against an
    UNDELAYED dry signal, so mixing down any module that reports latency combed
    -- exactly the Saturation bug, at chain level, and the Chain docstring
    claimed the compensation existed.

    Saturation reports 32 samples; the Limiter reports its full lookahead
    (240 samples at the 5 ms default), so this matters more here, not less.
    """
    x = np.random.RandomState(0).randn(8 * FS) * 0.02
    c = Chain(FS, [dsp.Saturation(FS, drive_db=0.0, mix=1.0, oversample=8, mode="tanh")])
    c.mix[0] = mix
    y = c.process(x[:, None])[:, 0]
    lo, hi = _ripple_db(y, x)
    assert lo > -0.5 and hi < 0.5, f"chain comb at mix={mix}: {lo:+.2f}/{hi:+.2f} dB"


def test_chain_dry_mix_is_block_size_independent():
    """The dry delay line must carry across process() calls."""
    x = np.random.RandomState(1).randn(FS) * 0.05
    def run(blk):
        c = Chain(FS, [dsp.Saturation(FS, drive_db=6.0, mix=1.0)])
        c.mix[0] = 0.5
        return np.concatenate([c.process(x[i:i + blk, None]) for i in range(0, len(x), blk)])[:, 0]
    assert meter.null_test_db(run(len(x)), run(512)) < -200


def test_chain_is_a_usable_module():
    """REGRESSION: Chain.__init__ never called Module.__init__, so self._p was
    never created and the inherited get()/set() raised AttributeError. Harmless
    while nothing called them, but core.py's Module interface is explicitly
    designed to transliterate to JUCE -- a subclass that silently isn't one is
    exactly the trap that port would fall into."""
    c = Chain(FS, [dsp.Saturation(FS)])
    assert isinstance(c, Module)
    assert hasattr(c, "_p")
    with pytest.raises(ValueError):
        c.set("nonexistent_param", 1.0)


def test_chain_reports_summed_latency():
    c = Chain(FS, [dsp.Saturation(FS), dsp.Limiter(FS)])
    assert c.latency_samples() == sum(m.latency_samples() for m in c.modules)
    c.bypassed.add(0)
    assert c.latency_samples() == c.modules[1].latency_samples()
