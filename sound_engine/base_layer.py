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

import sys
from pathlib import Path

import numpy as np
import pedalboard as pb

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import base_clean  # noqa: E402
from base_clean import hp12 as _hp12, is_low_end, mono_below  # noqa: E402,F401

HEADROOM_DB = -6.0
MATCH_LIMIT_DB = 6.0
_run = base_clean.run


def tail_cut_hz(role):
    return 300.0 if role in ("snare", "clap") else 200.0


def tail_cut(before, after, sr, role, dry_gain=1.0):
    """Keep the dry as it was; high-pass only what the effect added."""
    bL, bR = before
    aL, aR = after
    tL, tR = aL - dry_gain * bL, aR - dry_gain * bR
    if max(np.abs(tL).max(), np.abs(tR).max()) <= 1e-9:
        return after
    fL, fR = _run(pb.Pedalboard(_hp12(tail_cut_hz(role))), tL, tR, sr)
    return dry_gain * bL + fL, dry_gain * bR + fR


def clean_input(L, R, sr, role, pre_clean=False):
    """Steps 6, 1, 2, 3. Returns (L, R) trimmed and cleaned. pre_clean=True:
    the stems were already low-cut and centred when the beat was made
    (tools/base_clean.py), so only the headroom trim is done here."""
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-12)
    ceil = 10 ** (HEADROOM_DB / 20)
    if peak > ceil:
        L, R = L * (ceil / peak), R * (ceil / peak)
    if pre_clean:
        return L, R
    board = base_clean.lowcuts(role)
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
