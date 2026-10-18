"""Bass / low-end clean-up that runs on EVERY beat as it is made (owner
2026-10-18: "it sounds better with the bass EQ thing... it should just be on
beats when we create them, automatically, for every beat").

Shared by the Beat Machine (tools/crew.py render) and the Sound Engine
(sound_engine/base_layer.py), so both do exactly the same thing:

  * rumble cut      12 dB/oct low cut at 30 Hz on every lane except kick /
                    808 / sub / bass (their lowest notes live there)
  * chord low cut   12 dB/oct low cut at 150 Hz on chord lanes
  * bass centred    side signal removed below ~85 Hz, fully back above ~170 Hz

The owner's older "leave the sub / 808 alone" mix rule is overruled for this
(2026-10-18); low-end lanes are centred like everything else. They only skip
the 30 Hz cut, which would eat an 808's fundamental -- physics, not the rule.

Filters run on [one copy of the audio + the audio] and keep the second half,
so a looped lane has no click or ringing at the seam; the mono split is an FFT
over the whole buffer, which already treats it as a loop.
"""
from __future__ import annotations

import re

import numpy as np
import pedalboard as pb

# two 1st-order stages in a row have their -3 dB point at 0.6436 x stage cutoff
_CORNER = 0.6436
RUMBLE_HZ = 30.0
CHORD_HZ = 150.0
MONO_BELOW_HZ = 120.0
DEFAULT_SR = 44100
LOW_END = {"sub", "bass", "sub808", "808", "bass drum"}
_SUFFIX = re.compile(r"(?:\d+v\d+|\d+)$")
MARKER = ".base_clean"      # dropped in a Stems folder: "already cleaned"


def role_of(lane):
    """'chord0v1' -> 'chord', 'bass0' -> 'bass', 'kick drum - x.wav'-style
    labels -> their head word."""
    head = str(lane).split(" - ", 1)[0].strip().lower()
    head = {"kick drum": "kick"}.get(head, head)
    return _SUFFIX.sub("", head).strip() or head


def is_low_end(role):
    return role in LOW_END


def skips_rumble_cut(role):
    return is_low_end(role) or role.startswith("kick") or role == "drum loop"


def hp12(fc):
    s = fc * _CORNER
    return [pb.HighpassFilter(cutoff_frequency_hz=s),
            pb.HighpassFilter(cutoff_frequency_hz=s)]


def run(board, L, R, sr):
    """Filter with one copy of the audio as pre-roll (loop-safe)."""
    n = len(L)
    st = np.stack([np.concatenate([L, L]), np.concatenate([R, R])]).astype(np.float32)
    out = board(st, sr)[:, n:]
    return out[0].astype(np.float64), out[1].astype(np.float64)


def lowcuts(role):
    """The low-cut filters this kind of lane gets (may be empty)."""
    board = []
    if not skips_rumble_cut(role):
        board += hp12(RUMBLE_HZ)
    if role == "chord":
        board += hp12(CHORD_HZ)
    return board


def lane_lowcut(x, lane, sr=DEFAULT_SR):
    """Low cuts for one MONO lane buffer (the Beat Machine's per-lane bufs)."""
    board = lowcuts(role_of(lane))
    if not board or not len(x):
        return x
    y, _ = run(pb.Pedalboard(board), x, x, sr)
    return y


def mono_below(L, R, sr=DEFAULT_SR, fc=MONO_BELOW_HZ):
    """Side signal removed below fc/sqrt(2), fully kept above fc*sqrt(2), a
    raised-cosine edge between (same shape as groove.mono_below, but sample-
    rate aware)."""
    mid, side = 0.5 * (L + R), 0.5 * (L - R)
    f = np.fft.rfftfreq(len(side), 1.0 / sr)
    lo, hi = fc / np.sqrt(2), fc * np.sqrt(2)
    t = np.clip((np.log2(np.maximum(f, 1.0)) - np.log2(lo))
                / (np.log2(hi) - np.log2(lo)), 0, 1)
    side = np.fft.irfft(np.fft.rfft(side) * (0.5 - 0.5 * np.cos(np.pi * t)), len(side))
    return mid + side, mid - side
