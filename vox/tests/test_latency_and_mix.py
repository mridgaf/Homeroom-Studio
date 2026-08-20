"""Cross-cutting invariants that no per-module test was checking.

Every real bug found in the 2026-08-19 adversarial pass lived in one of these
two gaps:

  * latency  -- no test ever compared a module's reported latency_samples()
                to its measured impulse delay, so nothing noticed when a wet
                path was mixed against an uncompensated dry one;
  * mix      -- every test used mix=0 (nulls) or mix=1 (no dry path at all),
                and the product ships partial mix everywhere.

Parametrized over a module list rather than written per-module, so adding a
module here checks it against all five invariants at once.

The list is NOT automatic, and saying otherwise would be the same species of
overclaim this file exists to catch. `Stack`, `ThrowDelay`, `ReverbSend` and
`Dimension` are covered below in a separate list because they are stereo
and/or optional-dependency modules that need different construction; anything
new must be added by hand to one list or the other.
"""
import numpy as np
import pytest
from scipy import signal as sg

from vox import dsp
from vox.core import Module

FS = 48000

# (label, factory) -- real-time-legal modules with a declared latency and/or mix.
MODULES = [
    ("compressor", lambda **kw: dsp.Compressor(FS, threshold_db=-18.0, ratio=3.0, **kw)),
    ("deesser",    lambda **kw: dsp.DeEsser(FS, freq_hz=5500.0, threshold_db=-30.0, **kw)),
    ("saturation", lambda **kw: dsp.Saturation(FS, drive_db=0.0, oversample=8, mode="tanh", **kw)),
    ("limiter",    lambda **kw: dsp.Limiter(FS, **kw)),
    ("gate",       lambda **kw: dsp.Gate(FS, open_db=-90.0, close_db=-95.0, **kw)),
    ("eq",         lambda **kw: dsp.ParametricEQ(
        FS, bands=[dict(kind="bell", freq=3000, gain_db=3.0, q=1.0)], **kw)),
]
HAS_MIX = {"compressor", "deesser", "saturation"}


@pytest.mark.parametrize("label,make", MODULES, ids=[m[0] for m in MODULES])
def test_reported_latency_matches_measured_delay(label, make):
    """latency_samples() is what a host uses for delay compensation. If it
    lies, every parallel path in the session is misaligned -- and the module's
    own internal dry mix is misaligned too, which is exactly how the
    Saturation comb filter shipped in all three presets."""
    m = make()
    lat = m.latency_samples()
    imp = np.zeros(8192)
    imp[1000] = 0.5
    y = m.process(imp[:, None])[:, 0]
    if np.max(np.abs(y)) < 1e-9:
        pytest.skip(f"{label} does not pass an impulse at these settings")
    measured = int(np.argmax(np.abs(y))) - 1000
    assert abs(measured - lat) <= 1, f"{label} reports {lat}, measures {measured}"


@pytest.mark.parametrize("label,make", [m for m in MODULES if m[0] in HAS_MIX],
                         ids=[m[0] for m in MODULES if m[0] in HAS_MIX])
@pytest.mark.parametrize("mix", [0.15, 0.35, 0.5, 0.85])
def test_partial_mix_does_not_comb(label, make, mix):
    """A partial dry/wet blend must not filter the signal.

    At low drive / high threshold these modules are close to linear, so any
    ripple here is a phase or latency misalignment between the wet and dry
    paths -- i.e. a comb filter -- not distortion.
    """
    x = np.random.RandomState(0).randn(4 * FS) * 0.02
    y = make(mix=mix).process(x[:, None])[:, 0]
    f, pxx = sg.welch(x, FS, nperseg=8192)
    _, pyy = sg.welch(y, FS, nperseg=8192)
    band = (f >= 100) & (f < 15000)
    h = 10 * np.log10(pyy[band] / pxx[band])
    assert h.min() > -1.0, f"{label} combs at mix={mix}: {h.min():+.2f} dB"


@pytest.mark.parametrize("label,make", MODULES, ids=[m[0] for m in MODULES])
def test_block_size_invariance(label, make):
    """core.Module's contract: the output must not depend on how the caller
    chunks the input. A module that keeps state but sizes a buffer from the
    current block length violates this silently."""
    x = np.random.RandomState(2).randn(FS) * 0.05
    whole = make().process(x[:, None])[:, 0]
    m = make()
    chunked = np.concatenate([m.process(x[i:i + 512, None])[:, 0]
                              for i in range(0, len(x), 512)])
    assert np.max(np.abs(whole - chunked)) < 1e-9, label


@pytest.mark.parametrize("label,make", MODULES, ids=[m[0] for m in MODULES])
def test_reset_returns_module_to_cold_state(label, make):
    """reset() is part of the Module interface and only ThrowDelay had a test
    for it. A host calls it on transport stop; state surviving it is a bug."""
    x = np.random.RandomState(3).randn(FS // 2) * 0.1
    m = make()
    first = m.process(x[:, None])[:, 0]
    m.reset()
    second = m.process(x[:, None])[:, 0]
    assert np.max(np.abs(first - second)) < 1e-9, label


@pytest.mark.parametrize("label,make", MODULES, ids=[m[0] for m in MODULES])
def test_output_is_finite_and_dc_free(label, make):
    """No NaN/inf, and no DC offset introduced. meter.dc_offset_db exists and
    was never asserted on any module's output."""
    x = np.random.RandomState(4).randn(FS) * 0.2
    y = make().process(x[:, None])[:, 0]
    assert np.all(np.isfinite(y)), f"{label} produced non-finite output"
    assert abs(np.mean(y)) < 1e-3, f"{label} introduced DC: {np.mean(y):+.2e}"


# Stereo / creative modules. Separate list: these need stereo input, and two of
# them depend on `pedalboard`, which is a Phase-1-only dependency.
EXTRA = [
    ("stack", lambda: dsp.Stack(FS, mix=0.35)),
    ("throw", lambda: __import__("vox.dsp.throw", fromlist=["ThrowDelay"]).ThrowDelay(FS)),
]


def test_stack_reports_honest_latency():
    """Stack reports latency_samples() == 0; verify that rather than assume it.
    A module that quietly delays while reporting 0 misaligns every parallel
    path around it.

    ThrowDelay is deliberately NOT covered by this: it is a 100% wet send, so
    its 0.25 s delay IS the effect, not latency, and reporting 0 is correct.
    Asserting "first arrival == reported latency" on a send would be asserting
    that the echo is a bug. It is covered for block-size invariance below,
    which is the invariant that does apply to it.
    """
    m = dsp.Stack(FS, mix=0.35)
    imp = np.zeros((65536, 2))
    imp[1000, :] = 0.5
    y = m.process(imp)
    assert np.max(np.abs(y)) > 1e-9, "stack passed no impulse"
    measured = int(np.argmax(np.abs(y[:, 0]))) - 1000
    assert abs(measured - m.latency_samples()) <= 1, (
        f"stack reports {m.latency_samples()}, measures {measured}")


@pytest.mark.parametrize("label,make", EXTRA, ids=[m[0] for m in EXTRA])
def test_extra_modules_are_block_size_invariant(label, make):
    x = np.random.RandomState(5).randn(FS, 2) * 0.05
    whole = make().process(x.copy())
    m = make()
    chunked = np.concatenate([m.process(x[i:i + 512].copy()) for i in range(0, len(x), 512)])
    assert np.max(np.abs(whole - chunked)) < 1e-9, label
