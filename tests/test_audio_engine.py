"""Objective checks for tools/audio_engine.py — measures the actual
output signal, not the code (per the audio-fix-verify house rule)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

pytest.importorskip("pedalboard")

import audio_engine as ae  # noqa: E402
from make_drum_loops import SR  # noqa: E402
from groove import lufs  # noqa: E402


def _tone(freq, seconds=1.0, amp=0.3):
    t = np.arange(int(SR * seconds)) / SR
    return (np.sin(2 * np.pi * freq * t) * amp).astype(np.float64)


def test_high_shelf_boosts_highs_not_lows():
    low, high = _tone(80), _tone(10000)
    lo_before = np.abs(np.fft.rfft(low)).max()
    hi_before = np.abs(np.fft.rfft(high)).max()
    loL, _ = ae.eq3(low.copy(), low.copy(), high_db=12.0, high_hz=6000.0)
    hiL, _ = ae.eq3(high.copy(), high.copy(), high_db=12.0, high_hz=6000.0)
    lo_after = np.abs(np.fft.rfft(loL)).max()
    hi_after = np.abs(np.fft.rfft(hiL)).max()
    assert abs(20 * np.log10(lo_after / lo_before)) < 1.0
    assert 20 * np.log10(hi_after / hi_before) > 9.0


def test_compressor_reduces_loud_signal_more_than_quiet():
    # measure the SETTLED tail (last quarter second), not the whole
    # buffer — the first ~attack_ms is pre-compression transient and
    # dominates a naive whole-buffer peak, masking steady-state reduction
    loud = _tone(220, seconds=1.0, amp=0.9)
    quiet = _tone(220, seconds=1.0, amp=0.05)
    lL, lR = ae.glue_compressor(loud.copy(), loud.copy(), threshold_db=-14.0,
                                  ratio=4.0, attack_ms=5.0, makeup_db=0.0)
    qL, qR = ae.glue_compressor(quiet.copy(), quiet.copy(), threshold_db=-14.0,
                                  ratio=4.0, attack_ms=5.0, makeup_db=0.0)
    tail = slice(-int(SR * 0.25), None)
    loud_gr_db = 20 * np.log10(np.abs(lL[tail]).max() / np.abs(loud[tail]).max())
    quiet_gr_db = 20 * np.log10(np.abs(qL[tail]).max() / np.abs(quiet[tail]).max())
    assert loud_gr_db < quiet_gr_db - 3.0


def test_reverb_produces_a_tail():
    impulse = np.zeros(SR)
    impulse[0] = 1.0
    wL, wR = ae.algo_reverb(impulse.copy(), impulse.copy(), room_size=0.9,
                              wet=0.8, dry=0.0)
    tail_energy = np.abs(wL[SR // 2:]).sum()
    assert tail_energy > 1.0


def test_stereo_width_scales_side_and_leaves_mono_sum_untouched():
    rng = np.random.default_rng(0)
    n = SR
    L = rng.standard_normal(n) * 0.3
    R = rng.standard_normal(n) * 0.3 + L * 0.3
    mono_before = L + R
    for width in (0.0, 1.0, 2.0):
        wL, wR = ae.stereo_width(L.copy(), R.copy(), width=width)
        assert np.abs((wL + wR) - mono_before).max() < 1e-9
        side_before = 0.5 * (L - R)
        side_after = 0.5 * (wL - wR)
        ratio = (np.sqrt((side_after ** 2).mean())
                 / np.sqrt((side_before ** 2).mean() + 1e-12))
        assert abs(ratio - width) < 1e-6


def test_multiband_compress_reconstructs_exactly_when_transparent():
    t = np.arange(SR) / SR
    mix = np.sin(2 * np.pi * 60 * t) * 0.6 + np.sin(2 * np.pi * 8000 * t) * 0.05
    transparent = {"threshold_db": 0.0, "ratio": 1.0, "attack_ms": 1.0,
                    "release_ms": 100.0}
    L, R = ae.multiband_compress(mix.copy(), mix.copy(), low_kwargs=transparent,
                                   mid_kwargs=transparent, high_kwargs=transparent)
    assert np.abs(L - mix).max() < 1e-5


def test_multiband_compress_is_band_independent():
    t = np.arange(SR) / SR
    mix = np.sin(2 * np.pi * 60 * t) * 0.6 + np.sin(2 * np.pi * 8000 * t) * 0.05
    transparent = {"threshold_db": 0.0, "ratio": 1.0, "attack_ms": 1.0,
                    "release_ms": 100.0}
    hot_low = {"threshold_db": -40.0, "ratio": 8.0, "attack_ms": 5.0,
               "release_ms": 100.0}
    L, _ = ae.multiband_compress(mix.copy(), mix.copy(), low_kwargs=hot_low,
                                   mid_kwargs=transparent, high_kwargs=transparent)
    seg = slice(-int(SR * 0.25), None)
    freqs = np.fft.rfftfreq(len(mix[seg]), 1 / SR)
    before = np.abs(np.fft.rfft(mix[seg]))
    after = np.abs(np.fft.rfft(L[seg]))
    hi_bin = np.argmin(np.abs(freqs - 8000))
    lo_bin = np.argmin(np.abs(freqs - 60))
    assert abs(20 * np.log10(after[hi_bin] / before[hi_bin])) < 0.5  # untouched
    assert 20 * np.log10(after[lo_bin] / before[lo_bin]) < -5  # compressed


def test_saturate_adds_harmonics_and_respects_mix():
    tone = _tone(220, amp=0.6)
    dry_spec = np.abs(np.fft.rfft(tone))
    wL, _ = ae.saturate(tone.copy(), tone.copy(), drive_db=18.0, mix=1.0)
    wet_spec = np.abs(np.fft.rfft(wL))
    freqs = np.fft.rfftfreq(len(tone), 1 / SR)
    fund_bin = np.argmin(np.abs(freqs - 220))
    third_harm_bin = np.argmin(np.abs(freqs - 660))
    # a fully-wet hard waveshaper should raise energy at the 3rd harmonic
    # (odd-order distortion) much more than at the fundamental
    assert wet_spec[third_harm_bin] > dry_spec[third_harm_bin] * 5

    zero_mix_L, _ = ae.saturate(tone.copy(), tone.copy(), drive_db=18.0, mix=0.0)
    assert np.allclose(zero_mix_L, tone, atol=1e-5)  # mix=0 is transparent


def test_loop_algo_reverb_wraps_tail_to_buffer_start():
    n = SR * 2
    sig = np.zeros(n)
    sig[-100] = 1.0  # transient right at the end of the loop
    wL, _ = ae.loop_algo_reverb(sig.copy(), sig.copy(), room_size=0.9,
                                  wet=0.6, dry=1.0)
    start_energy = np.abs(wL[:2000]).sum()
    naive_L, _ = ae.algo_reverb(sig.copy(), sig.copy(), room_size=0.9,
                                  wet=0.6, dry=1.0)
    naive_start = np.abs(naive_L[:2000]).sum()
    assert start_energy > naive_start * 10  # wrap actually happened


def test_loop_algo_reverb_freeze_passthrough_sustains_longer():
    # freeze holds the reverb tank's state instead of letting it decay —
    # tested as "does the tail stay roughly steady across its own window"
    # rather than "is it louder than a same-length non-frozen render",
    # because those two aren't apples-to-apples: freeze primes the tank
    # over a full pass first, then continues frozen from there, so a
    # frozen and a non-frozen render of the same input length sample
    # different absolute points in the tank's timeline. A pedalboard.Reverb
    # engaged frozen from a cold/empty tank (no priming) renders total
    # silence forever instead of sustaining anything — verified directly
    # against pedalboard, not assumed — so this also guards against that
    # regression: a broken "freeze" that's silently all-zero would fail
    # the steady-state check below just as much as one that decays.
    n = SR  # 1s
    sig = np.zeros(n)
    sig[0] = 1.0
    frozen_L, _ = ae.loop_algo_reverb(sig.copy(), sig.copy(), room_size=0.5,
                                        wet=1.0, dry=0.0, freeze=True)
    normal_L, _ = ae.loop_algo_reverb(sig.copy(), sig.copy(), room_size=0.15,
                                        wet=1.0, dry=0.0, freeze=False)

    frozen_first, frozen_second = (np.abs(frozen_L[:n // 2]).mean(),
                                     np.abs(frozen_L[n // 2:]).mean())
    normal_first, normal_second = (np.abs(normal_L[:n // 2]).mean(),
                                     np.abs(normal_L[n // 2:]).mean())

    assert frozen_second > 1e-6  # holding real energy, not just silence
    # frozen: second half stays close to first half (steady, not decaying)
    assert frozen_second > frozen_first * 0.5
    # normal: second half decays hard relative to first half (real contrast)
    assert normal_second < normal_first * 0.1


def test_master_chain_hits_target_lufs_and_respects_ceiling():
    rng = np.random.default_rng(0)
    t = np.arange(SR * 2) / SR
    music = np.sin(2 * np.pi * 220 * t) * 0.5 + rng.standard_normal(len(t)) * 0.08
    music[100] = 1.3
    L, R, got = ae.master_chain(music.copy(), music.copy(), target_lufs=-12.0,
                                  ceiling_db=-1.0)
    peak_db = 20 * np.log10(max(np.abs(L).max(), np.abs(R).max()))
    assert abs(got - (-12.0)) < 0.2
    assert peak_db <= -1.0 + 0.01


def test_master_chain_does_not_inflate_quiet_input_past_target():
    quiet = _tone(220, amp=0.05)
    L, R, got = ae.master_chain(quiet.copy(), quiet.copy(), target_lufs=-12.0,
                                  ceiling_db=-1.0)
    assert abs(got - (-12.0)) < 0.2
