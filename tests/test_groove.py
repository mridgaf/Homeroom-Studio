"""Numeric verification of the studio engine against the research numbers."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
from groove import (LaneFeel, dist808, euclid, gated_reverb, glue_compress,
                    kick_sub_reinforce,
                    haas, k_weight, kick_layer, lufs, make_ir,
                    master_to_lufs, mono_below, mpc_swing_offset,
                    ratchet_times, sp1200, transient_shape, velocity,
                    vinyl_bed, wow_flutter, zoh_resample)

SR = 44100


# -- MPC swing: the exact published numbers -----------------------------------

def test_swing_straight_and_even_steps_never_move():
    for step in range(16):
        assert mpc_swing_offset(step, 90, 50) == 0.0
    for step in (0, 2, 4, 6, 8):
        assert mpc_swing_offset(step, 90, 62) == 0.0


def test_swing_tick_math_at_90bpm():
    # Linn/DSP research: 54% -> 2 ticks = 13.9 ms, 58% -> 27.8, 62% -> 41.7
    tick = 60 / (90 * 96)
    assert mpc_swing_offset(1, 90, 54) == pytest.approx(2 * tick)
    assert mpc_swing_offset(1, 90, 58) == pytest.approx(4 * tick)
    assert mpc_swing_offset(1, 90, 62) == pytest.approx(6 * tick)
    assert mpc_swing_offset(1, 90, 54) == pytest.approx(0.0139, abs=5e-4)


def test_swing_triplet_and_max():
    t16 = 60 / (90 * 4)
    # 66.7% ≈ a third of the 8th-note pair; 75% = half the pair
    assert mpc_swing_offset(1, 90, 75, tick_round=False) == pytest.approx(0.5 * t16)


# -- Dilla lanes ---------------------------------------------------------------

def test_lane_feel_constant_offset_dominates():
    lane = LaneFeel(offset_ms=25, jitter_ms=4, swing=50, seed=1)
    times = [lane.hit_time(0.0, 4, 90) for _ in range(50)]
    grid = 4 * 60 / (90 * 4)
    devs = np.array(times) - grid
    assert 0.018 < devs.mean() < 0.032      # ~25 ms lane drag survives
    assert devs.std() < 0.004               # jitter is a whisper, not noise


# -- velocity humanization ------------------------------------------------------

def test_velocity_structure_dominates_randomness():
    rng = np.random.default_rng(3)
    accents = [velocity("X", 0, rng) for _ in range(100)]
    es = [velocity("x", 1, rng) for _ in range(100)]     # an "e" 16th
    ghosts = [velocity(".", 2, rng) for _ in range(100)]
    assert np.mean(accents) > np.mean(es) > np.mean(ghosts)
    # ghosts land in the researched 30-50%-of-accent zone
    assert 0.2 < np.mean(ghosts) / np.mean(accents) < 0.55
    # wobble ≈ ±1 dB: std/mean small
    assert np.std(accents) / np.mean(accents) < 0.15


# -- SP-1200 -------------------------------------------------------------------

def test_sp1200_quantizes_to_12bit_at_low_rate():
    x = np.sin(2 * np.pi * 220 * np.arange(SR) / SR) * 0.9
    y = sp1200(x, out_lp=None)
    low = zoh_resample(y, SR, 26040)
    steps = np.unique(np.round(low * 2047))
    assert len(steps) <= 4096                       # 12-bit grid
    # aliasing images exist above the 13.02 kHz Nyquist of the low rate
    Y = np.abs(np.fft.rfft(y))
    f = np.fft.rfftfreq(len(y), 1 / SR)
    assert Y[f > 14000].max() > Y.max() * 1e-4      # images kept (no reconstruction filter)


def test_sp1200_amount_blend():
    from groove import OWNER_TASTE
    x = np.sin(2 * np.pi * 220 * np.arange(SR // 2) / SR) * 0.9
    dry = sp1200(x, amount=0.0)
    half = sp1200(x, amount=OWNER_TASTE["sp1200_amount"])
    full = sp1200(x, amount=1.0)
    assert np.allclose(dry, x)                      # amount=0 is a bypass
    d_half = np.abs(half - x).mean()
    d_full = np.abs(full - x).mean()
    assert 0 < d_half < d_full                      # half dirt sits between


def test_owner_taste_recorded():
    from groove import OWNER_TASTE
    assert OWNER_TASTE["dilla_snare"] == "early"
    assert OWNER_TASTE["sidechain_prob"] == 0.9
    # AB5 said gated; owner revised 2026-07-15 to varying gated/dry
    assert OWNER_TASTE["snare_space"] == "vary"


def test_zoh_resample_lengths():
    x = np.arange(1000, dtype=float)
    assert len(zoh_resample(x, 44100, 26040)) == round(1000 * 26040 / 44100)


# -- kick layering phase check ---------------------------------------------------

def test_kick_layer_rescues_inverted_sub():
    t = np.arange(int(0.4 * SR)) / SR
    sub = np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.2)
    top = np.random.default_rng(5).normal(0, 0.2, len(t)) * np.exp(-t / 0.01)
    good = kick_layer(top, sub)
    flipped = kick_layer(top, -sub)
    def low_rms(a):
        from groove import lp4
        return np.sqrt((lp4(a, 100) ** 2).mean())
    # polarity search should land both stacks at (near) equal low energy
    assert abs(low_rms(good) - low_rms(flipped)) / low_rms(good) < 0.1


# -- 808 distortion adds mids ----------------------------------------------------

def test_dist808_adds_mid_harmonics():
    t = np.arange(SR) / SR
    x = np.sin(2 * np.pi * 55 * t) * 0.8
    y = dist808(x)
    def band(sig, lo, hi):
        S = np.abs(np.fft.rfft(sig))
        f = np.fft.rfftfreq(len(sig), 1 / SR)
        return S[(f > lo) & (f < hi)].sum()
    # phone-audible mids (200-1k) grow relative to the sub
    assert band(y, 200, 1000) / band(y, 30, 80) > \
        band(x, 200, 1000) / band(x, 30, 80) * 5


# -- mono below / Haas -----------------------------------------------------------

def test_mono_below_kills_low_side():
    rng = np.random.default_rng(9)
    L, R = rng.normal(0, .3, SR), rng.normal(0, .3, SR)
    L2, R2 = mono_below(L, R, 120)
    side = 0.5 * (L2 - R2)
    S = np.abs(np.fft.rfft(side))
    f = np.fft.rfftfreq(len(side), 1 / SR)
    assert S[f < 60].mean() < S[(f > 1000) & (f < 8000)].mean() * 0.2


def test_haas_delay_and_level():
    x = np.zeros(SR); x[1000] = 1.0
    L, R = haas(x, ms=12, side_db=-4)
    assert L[1000] == 1.0
    d = int(0.012 * SR)
    assert R[1000 + d] > 0.3                        # delayed copy present


# -- gated reverb -----------------------------------------------------------------

def test_gated_reverb_tail_cut():
    x = np.zeros(2 * SR); x[100] = 1.0
    y = gated_reverb(x, [100], wet=1.0, hold_ms=140, rel_ms=20)
    tail = np.abs(y)
    during = tail[100 + int(0.05 * SR): 100 + int(0.12 * SR)].max()
    after = tail[100 + int(0.30 * SR):].max()
    assert during > after * 8                       # brutal cut after hold


# -- texture ----------------------------------------------------------------------

def test_vinyl_bed_level_and_band():
    bed = vinyl_bed(SR)
    assert np.abs(bed).max() < 0.02                 # ~-42 dB territory
    B = np.abs(np.fft.rfft(bed))
    f = np.fft.rfftfreq(len(bed), 1 / SR)
    assert B[(f > 300) & (f < 8000)].mean() > B[f > 15000].mean()


def test_wow_flutter_preserves_length_and_pitch_wobbles():
    t = np.arange(2 * SR) / SR
    x = np.sin(2 * np.pi * 440 * t)
    y = wow_flutter(x, wow_pct=1.0)
    assert len(y) == len(x)
    assert not np.allclose(y[:SR // 2], x[:SR // 2], atol=1e-3)


# -- Euclid / ratchets -------------------------------------------------------------

def test_euclid_tresillo_and_counts():
    assert euclid(3, 8) == [True, False, False, True, False, False, True, False]
    for k, n in ((5, 8), (5, 16), (7, 16)):
        assert sum(euclid(k, n)) == k


def test_ratchet_ramp():
    hits = ratchet_times(1.0, 0.125, m=3)
    times = [h[0] for h in hits]; vels = [h[1] for h in hits]
    assert times == pytest.approx([1.0, 1.0 + 0.125 / 3, 1.0 + 0.25 / 3])
    assert vels[0] < vels[-1] == 1.0


# -- loudness -----------------------------------------------------------------------

def test_lufs_sine_sanity():
    # BS.1770: a 997 Hz sine at -18 dBFS reads ≈ -18 LUFS (K-weight ~flat @1k)
    t = np.arange(5 * SR) / SR
    x = np.sin(2 * np.pi * 997 * t) * 10 ** (-18 / 20) * np.sqrt(2)
    val = lufs(x, x)
    assert val == pytest.approx(-15.0, abs=2.5)     # stereo sum + tolerance


def test_master_to_lufs_hits_target():
    from groove import OWNER_TASTE
    rng = np.random.default_rng(2)
    env = (np.sin(2 * np.pi * 2 * np.arange(6 * SR) / SR) > 0.6)
    x = rng.normal(0, .15, 6 * SR) * env            # bursty drum-ish signal
    L, R, achieved = master_to_lufs(x.copy(), x.copy())
    assert achieved == pytest.approx(OWNER_TASTE["master_lufs"], abs=1.2)
    ceil = 10 ** (OWNER_TASTE["peak_ceiling_db"] / 20)
    assert np.abs(L).max() <= ceil + 1e-3              # ceiling respected


# -- glue compression (owner 2026-07-29) --------------------------------------------

def test_glue_compress_reduces_loud_signal_more_than_quiet():
    """The basic thing a downward compressor must do: a signal well
    above threshold ends up squashed relatively more than one well
    below it, which never gets touched."""
    t = np.arange(2 * SR) / SR
    loud = np.sin(2 * np.pi * 200 * t) * 0.9     # well above -18 dB threshold
    quiet = np.sin(2 * np.pi * 200 * t) * 0.02   # well below threshold
    gL, _ = glue_compress(loud.copy(), loud.copy())
    qL, _ = glue_compress(quiet.copy(), quiet.copy())
    loud_gain = np.abs(gL).max() / np.abs(loud).max()
    quiet_gain = np.abs(qL).max() / np.abs(quiet).max()
    assert loud_gain < quiet_gain


def test_glue_compress_keeps_stereo_image():
    """Same gain reduction on both channels — a hard-panned signal must
    not shift toward center or the opposite side."""
    t = np.arange(2 * SR) / SR
    L = np.sin(2 * np.pi * 200 * t) * 0.9
    R = np.zeros_like(L)
    _, gR = glue_compress(L.copy(), R.copy())
    assert np.abs(gR).max() < 1e-9


def test_sub_reinforce_never_costs_low_end_or_headroom():
    """The bug this catches (found 2026-09-05, measured on six real
    kicks): the peak guard used to run ONCE at the end, on a winner the
    search had already picked, so the candidate with the loudest low band
    got chosen and then scaled down bodily — taking the kick's own low end
    with it. On four of six kicks that flipped the sign of the whole
    function, -4.57 dB on one of Otto Grit's.

    Two invariants, and they are in tension, which is the whole point:
    the low band may never come out QUIETER than it went in (the
    function's stated job), and the peak may never come out HIGHER (the
    kick is the reference every other lane is scaled against in
    crew.peak_ceiling_for, so an inflated kick silently turns the rest of
    the beat down). A transient-heavy kick is the case that broke it."""
    t = np.arange(int(0.4 * SR)) / SR
    # a click plus a short body — peak lives in the first few samples,
    # which is exactly when adding a 40 Hz tone inflates it most
    kick = np.exp(-t * 60) * np.sin(2 * np.pi * 55 * t)
    kick[:20] += np.linspace(1.0, 0.0, 20)

    def low_band_db(x):
        spec = np.abs(np.fft.rfft(x)) ** 2
        f = np.fft.rfftfreq(len(x), 1 / SR)
        sel = (f >= 30) & (f <= 55)
        return 10 * np.log10(spec[sel].sum() / len(x) + 1e-30)

    for amount in (0.35, 0.45, 0.8):
        out = kick_sub_reinforce(kick.copy(), amount=amount)
        assert low_band_db(out) >= low_band_db(kick) - 1e-9, \
            "sub layer REMOVED low end at amount %s" % amount
        assert np.abs(out).max() <= np.abs(kick).max() + 1e-9, \
            "sub layer inflated the kick peak at amount %s" % amount

    # allow_peak_db lifts the headroom ceiling for ONE preset (Doc Day's
    # new build, owner 2026-09-05). It must lift it by exactly what it
    # says and no more — the kick is the level reference for every other
    # lane, so an unbounded kick would silently crush the rest of the beat
    # — and the low band must still never go backwards.
    for allow in (1.0, 3.0):
        out = kick_sub_reinforce(kick.copy(), amount=0.45,
                                 allow_peak_db=allow)
        ceiling = np.abs(kick).max() * 10 ** (allow / 20.0)
        assert np.abs(out).max() <= ceiling + 1e-9, \
            "kick grew past its allowance at allow_peak_db=%s" % allow
        assert low_band_db(out) >= low_band_db(kick) - 1e-9, \
            "sub layer REMOVED low end at allow_peak_db=%s" % allow

    # NOT asserted by comparing bytes: sub808() adds an unseeded 3 ms noise
    # click (make_drum_loops.py, module-level `rng`), so two identical calls
    # differ by ~0.05 and nothing downstream of it is bit-reproducible. That
    # is pre-existing and module-wide — snare808 and clap do it too — and is
    # noted here so the next person does not mistake it for a bug in this
    # function. The default's contract is the peak bound above at
    # allow_peak_db=0.0, which is the thing that actually matters.


def test_glue_ratio_is_a_per_preset_knob():
    """crew.py passes a preset's `glue` block straight into these
    kwargs (owner 2026-09-05, Doc Day's SSL ratio). Two things have to
    hold or that knob is decoration: a harder ratio must squash a loud
    signal MORE than the house default, and passing nothing must give
    back exactly the house default."""
    t = np.arange(2 * SR) / SR
    loud = np.sin(2 * np.pi * 200 * t) * 0.9
    house, _ = glue_compress(loud.copy(), loud.copy())
    hard, _ = glue_compress(loud.copy(), loud.copy(), ratio=8.0)
    assert np.abs(hard).max() < np.abs(house).max()
    same, _ = glue_compress(loud.copy(), loud.copy(), **{})
    assert np.array_equal(same, house)


# -- transient shaper ----------------------------------------------------------------

def test_transient_shape_boosts_attack_only():
    x = np.ones(SR) * 0.2
    y = transient_shape(x, [1000], gain=1.0, tau_ms=3)
    assert y[1001] > 0.35                            # attack boosted
    assert y[1000 + int(0.05 * SR)] == pytest.approx(0.2, abs=0.01)


def test_make_ir_is_highpassed():
    irL, _ = make_ir(0.4, 5000, hp_hz=400)
    S = np.abs(np.fft.rfft(irL))
    f = np.fft.rfftfreq(len(irL), 1 / SR)
    assert S[f < 100].mean() < S[(f > 800) & (f < 4000)].mean() * 0.25


def test_kick_sub_reinforce_adds_low_end_without_stealing_headroom():
    """Otto Grit's kick sub layer (owner-approved 2026-09-03, "b Light").
    Two things have to hold: the low band gets LOUDER, and the peak does
    not — a reinforced kick that peaks higher would win the level cascade
    on loudness it did not earn."""
    from groove import kick_sub_reinforce, lp4
    t = np.arange(int(0.3 * SR)) / SR
    kick = (np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.06)
            + np.random.default_rng(3).normal(0, 0.15, len(t))
            * np.exp(-t / 0.004))

    def low_rms(a):
        return np.sqrt((lp4(a, 100) ** 2).mean())

    out = kick_sub_reinforce(kick, amount=0.35)
    assert low_rms(out) > low_rms(kick) * 1.05
    assert np.abs(out).max() <= np.abs(kick).max() + 1e-9
    # and it must beat the phase check: an inverted-polarity sub can never
    # come out QUIETER in the low band than the bare kick
    assert low_rms(kick_sub_reinforce(-kick, amount=0.35)) \
        > low_rms(kick) * 1.05
