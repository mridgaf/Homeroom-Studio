"""Always-on base layer for the Sound Engine (owner 2026-10-18).

Invisible clean-up that runs on every stem, under the knobs:
  1. rumble cut      -- 12 dB/oct low cut at 30 Hz (not on kick / 808 / sub / bass,
                        whose lowest notes live there)
  2. chord low cut   -- 12 dB/oct low cut at 150 Hz on chord lanes
  3. bass centred    -- side signal removed below ~85 Hz, fully back above ~170 Hz
  4. tail low cut    -- reverb / echo tails lose their lows (see tail_cut)
  5. level match     -- the finished stem is brought back to the loudness of the
                        cleaned input (+-6 dB), so turning an effect up is never
                        just "louder"
  6. headroom        -- a stem peaking above -6 dBFS is trimmed to -6 before the
                        effects; level match puts the loudness back afterwards

The owner's older "leave the sub / 808 alone" mix rule is overruled for this
layer (2026-10-18): low-end lanes get 3, 5 and 6 too. They still skip 1 and 2,
because a 30 Hz cut would eat an 808's fundamental -- physics, not the old rule.

Filters run on [one copy of the stem + the stem] and keep the second half, so
a looped stem has no click or ringing at the seam. The mono split is an FFT
over the whole stem, which treats it as a loop already.
"""
from __future__ import annotations

import numpy as np
import pedalboard as pb

# two 1st-order stages in a row have their -3 dB point at 0.6436 x stage cutoff
_CORNER = 0.6436
RUMBLE_HZ = 30.0
CHORD_HZ = 150.0
MONO_BELOW_HZ = 120.0
HEADROOM_DB = -6.0
MATCH_LIMIT_DB = 6.0
_LOW_END = {"sub", "bass", "sub808", "808", "bass drum"}


def _hp12(fc):
    s = fc * _CORNER
    return [pb.HighpassFilter(cutoff_frequency_hz=s),
            pb.HighpassFilter(cutoff_frequency_hz=s)]


def _run(board, L, R, sr):
    """Filter with one copy of the stem as pre-roll (loop-safe)."""
    n = len(L)
    st = np.stack([np.concatenate([L, L]), np.concatenate([R, R])]).astype(np.float32)
    out = board(st, sr)[:, n:]
    return out[0].astype(np.float64), out[1].astype(np.float64)


def is_low_end(role):
    return role in _LOW_END


def _skips_rumble_cut(role):
    return is_low_end(role) or role.startswith("kick") or role == "drum loop"


def tail_cut_hz(role):
    return 300.0 if role in ("snare", "clap") else 200.0


def mono_below(L, R, sr, fc=MONO_BELOW_HZ):
    """Side signal removed below fc/sqrt(2), fully kept above fc*sqrt(2), a
    raised-cosine edge between (same shape as tools/groove.mono_below, but
    sample-rate aware)."""
    mid, side = 0.5 * (L + R), 0.5 * (L - R)
    f = np.fft.rfftfreq(len(side), 1.0 / sr)
    lo, hi = fc / np.sqrt(2), fc * np.sqrt(2)
    t = np.clip((np.log2(np.maximum(f, 1.0)) - np.log2(lo))
                / (np.log2(hi) - np.log2(lo)), 0, 1)
    side = np.fft.irfft(np.fft.rfft(side) * (0.5 - 0.5 * np.cos(np.pi * t)), len(side))
    return mid + side, mid - side


def tail_cut(before, after, sr, role, dry_gain=1.0):
    """Keep the dry as it was; high-pass only what the effect added."""
    bL, bR = before
    aL, aR = after
    tL, tR = aL - dry_gain * bL, aR - dry_gain * bR
    if max(np.abs(tL).max(), np.abs(tR).max()) <= 1e-9:
        return after
    fL, fR = _run(pb.Pedalboard(_hp12(tail_cut_hz(role))), tL, tR, sr)
    return dry_gain * bL + fL, dry_gain * bR + fR


def clean_input(L, R, sr, role):
    """Steps 6, 1, 2, 3. Returns (L, R) trimmed and cleaned."""
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-12)
    ceil = 10 ** (HEADROOM_DB / 20)
    if peak > ceil:
        L, R = L * (ceil / peak), R * (ceil / peak)
    board = []
    if not _skips_rumble_cut(role):
        board += _hp12(RUMBLE_HZ)
    if role == "chord":
        board += _hp12(CHORD_HZ)
    if board:
        L, R = _run(pb.Pedalboard(board), L, R, sr)
    return mono_below(L, R, sr)


def _rms(L, R):
    return float(np.sqrt(0.5 * (np.mean(L ** 2) + np.mean(R ** 2))))


def level_match(ref, out):
    rr, ro = _rms(*ref), _rms(*out)
    if rr < 1e-9 or ro < 1e-9:
        return out
    lim = 10 ** (MATCH_LIMIT_DB / 20)
    g = float(np.clip(rr / ro, 1 / lim, lim))
    return out[0] * g, out[1] * g
