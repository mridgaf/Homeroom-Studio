"""Pedalboard-based effects/mastering engine — additive, opt-in.

groove.py's hand-rolled DSP (tanh soft-clip "limiter", single-speed glue
compressor, synthetic exponential-decay reverb IRs) works and stays the
default. This module wraps pedalboard (Spotify's JUCE-backed audio library,
cp39 arm64, verified installed 2026-08-08) for the pieces where a real
plugin-grade algorithm is a genuine upgrade over the hand-rolled version:
a lookahead brickwall limiter instead of tanh, a two-speed attack/release
compressor instead of one lp1 envelope, and a real algorithmic (FDN) reverb
alongside the IR convolution reverb already in groove.py.

Nothing here is wired into render_crew_beat() by default. Callers opt in
per-render; existing beats and existing DJ character are untouched.
"""
from __future__ import annotations

import numpy as np
import pedalboard as pb

from make_drum_loops import SR
from groove import lufs


def _to_pb(L, R):
    return np.stack([L, R]).astype(np.float32)


def _from_pb(stereo):
    return stereo[0].astype(np.float64), stereo[1].astype(np.float64)


def eq3(L, R, low_db=0.0, low_hz=120.0, mid_db=0.0, mid_hz=800.0, mid_q=0.9,
        high_db=0.0, high_hz=8000.0, sr=None):
    """3-band parametric: low shelf, mid peak/bell, high shelf. sr defaults
    to this project's fixed beat-render rate (44100); the standalone Sound
    Engine app passes the uploaded file's own rate, since it isn't always
    44100 and pedalboard filters are rate-dependent."""
    board = pb.Pedalboard([
        pb.LowShelfFilter(cutoff_frequency_hz=low_hz, gain_db=low_db),
        pb.PeakFilter(cutoff_frequency_hz=mid_hz, gain_db=mid_db, q=mid_q),
        pb.HighShelfFilter(cutoff_frequency_hz=high_hz, gain_db=high_db),
    ])
    return _from_pb(board(_to_pb(L, R), sr or SR))


def glue_compressor(L, R, threshold_db=-14.0, ratio=2.5, attack_ms=12.0,
                     release_ms=180.0, makeup_db=2.0, sr=None):
    """Bus glue with real attack/release, unlike groove.glue_compress's
    single symmetric time constant (see that function's own upgrade-path
    note). sr — see eq3()'s docstring."""
    board = pb.Pedalboard([
        pb.Compressor(threshold_db=threshold_db, ratio=ratio,
                      attack_ms=attack_ms, release_ms=release_ms),
        pb.Gain(gain_db=makeup_db),
    ])
    return _from_pb(board(_to_pb(L, R), sr or SR))


def brickwall_limit(L, R, ceiling_db=-0.3, release_ms=100.0, sr=None):
    """Lookahead limiter. Replaces the tanh soft-clip in
    groove.master_to_lufs, which adds harmonic distortion at the ceiling
    instead of just stopping peaks. Not passive: like most mastering
    limiters it applies automatic makeup gain toward its own threshold
    even on material well under the ceiling — see master_chain()'s
    docstring for the measured effect and why LUFS trim runs after it.
    sr — see eq3()'s docstring; was hardcoded to SR until harsh-critic
    re-review caught it as the one stage in this module not honoring a
    caller's real sample rate (release_ms was ~8.8% off at 48kHz)."""
    board = pb.Pedalboard([pb.Limiter(threshold_db=ceiling_db, release_ms=release_ms)])
    return _from_pb(board(_to_pb(L, R), sr or SR))


def gate(L, R, threshold_db=-45.0, ratio=4.0, attack_ms=1.0, release_ms=100.0):
    board = pb.Pedalboard([pb.NoiseGate(threshold_db=threshold_db, ratio=ratio,
                                          attack_ms=attack_ms, release_ms=release_ms)])
    return _from_pb(board(_to_pb(L, R), SR))


def algo_reverb(L, R, room_size=0.5, damping=0.5, wet=0.25, dry=0.9,
                 width=1.0, freeze=False, sr=None):
    """FDN-style algorithmic reverb — a different color than groove's
    convolution reverb (synthetic IR), useful where a smoother, more
    'plugin' tail fits better than the gated/convolved house sound.
    sr — see eq3()'s docstring."""
    board = pb.Pedalboard([pb.Reverb(room_size=room_size, damping=damping,
                                       wet_level=wet, dry_level=dry, width=width,
                                       freeze_mode=1.0 if freeze else 0.0)])
    return _from_pb(board(_to_pb(L, R), sr or SR))


def multiband_compress(L, R, crossovers=(200.0, 4000.0), low_kwargs=None,
                         mid_kwargs=None, high_kwargs=None):
    """3-band compression: control a boomy low end or a harsh top without
    the other bands pumping along with it — single-band compression
    (glue_compressor) can't do this, it's the one job Ableton's Multiband
    Dynamics exists for.

    Split is low = lowpass(crossovers[0]), high = highpass(crossovers[1]),
    mid = original - low - high (algebraic remainder, not its own filter).
    That makes low + mid + high == original EXACTLY whenever nothing
    compresses — verified in tests — so the only way this changes the
    signal is where a band's compressor actually reduces gain, not from
    crossover filter error."""
    lo_x, hi_x = crossovers
    stereo = _to_pb(L, R)
    low = pb.Pedalboard([pb.LowpassFilter(cutoff_frequency_hz=lo_x)])(stereo, SR)
    high = pb.Pedalboard([pb.HighpassFilter(cutoff_frequency_hz=hi_x)])(stereo, SR)
    mid = stereo - low - high

    def _comp(band, kwargs, default):
        board = pb.Pedalboard([pb.Compressor(**(kwargs or default))])
        return board(band, SR)

    low_c = _comp(low, low_kwargs, {"threshold_db": -18.0, "ratio": 3.0,
                                     "attack_ms": 15.0, "release_ms": 200.0})
    mid_c = _comp(mid, mid_kwargs, {"threshold_db": -16.0, "ratio": 2.5,
                                     "attack_ms": 8.0, "release_ms": 150.0})
    high_c = _comp(high, high_kwargs, {"threshold_db": -20.0, "ratio": 2.0,
                                        "attack_ms": 3.0, "release_ms": 100.0})
    return _from_pb(low_c + mid_c + high_c)


def stereo_width(L, R, width=1.0):
    """M/S stereo width control — Ableton's Utility "Width" knob. width=1.0
    is unity (unchanged), <1.0 narrows toward mono, 0.0 is full mono,
    >1.0 widens the side channel. Distinct from groove.mono_below, which
    only collapses bass below a cutoff — this scales the FULL side signal
    at any width. Loudness-neutral on the mono sum by construction (mid
    is untouched, only side is scaled), so it can't make a beat quieter
    or louder in mono/club playback, only wider or narrower in stereo."""
    m = 0.5 * (L + R)
    s = 0.5 * (L - R) * width
    return m + s, m - s


def loop_algo_reverb(L, R, room_size=0.5, damping=0.5, wet=0.25, dry=1.0,
                       width=1.0, sr=None):
    """Loop-safe algorithmic reverb. pedalboard.Reverb is a stateful
    streaming plugin — run it straight over one 8-bar buffer and the tail
    just decays at the buffer's end, leaving an audible seam where bar 8
    meets bar 1 (this project's house rule: every beat must loop clean,
    see groove.loop_convolve for the same problem solved for convolution
    reverb). Fix: run the reverb over [dry, dry] concatenated and keep
    only the SECOND copy — its tail is already primed by the first pass,
    the same trick loop_convolve does for FFT convolution."""
    n = len(L)
    dblL, dblR = algo_reverb(np.concatenate([L, L]), np.concatenate([R, R]),
                               room_size=room_size, damping=damping, wet=wet,
                               dry=dry, width=width, sr=sr)
    return dblL[n:], dblR[n:]


def saturate(L, R, drive_db=6.0, mix=0.35, sr=None):
    """Parallel distortion — mix keeps it musical instead of full-wet
    fuzz (pedalboard's Distortion is a hard waveshaper at full wet).
    sr — see eq3()'s docstring."""
    board = pb.Pedalboard([pb.Distortion(drive_db=drive_db)])
    wL, wR = _from_pb(board(_to_pb(L, R), sr or SR))
    return L * (1 - mix) + wL * mix, R * (1 - mix) + wR * mix


def chorus(L, R, rate_hz=0.8, depth=0.25, mix=0.3):
    board = pb.Pedalboard([pb.Chorus(rate_hz=rate_hz, depth=depth, mix=mix)])
    return _from_pb(board(_to_pb(L, R), SR))


def phaser(L, R, rate_hz=0.5, depth=0.5, mix=0.3):
    board = pb.Pedalboard([pb.Phaser(rate_hz=rate_hz, depth=depth, mix=mix)])
    return _from_pb(board(_to_pb(L, R), SR))


def delay(L, R, seconds=0.25, feedback=0.3, mix=0.25):
    board = pb.Pedalboard([pb.Delay(delay_seconds=seconds, feedback=feedback, mix=mix)])
    return _from_pb(board(_to_pb(L, R), SR))


def master_chain(L, R, target_lufs=-12.0, ceiling_db=-1.0,
                  eq_kwargs=None, comp_kwargs=None, multiband=False,
                  multiband_kwargs=None, width=1.0):
    """Full alternative mastering chain: tone EQ -> glue/multiband
    compressor -> limiter (peak safety) -> linear trim to target LUFS ->
    peak backstop. Drop-in alternative to groove.master() +
    groove.master_to_lufs() — same (L, R, achieved_lufs) return shape, so
    callers can swap chains without touching call sites.

    multiband=True swaps the single-band glue_compressor for
    multiband_compress() (a boomy low end gets controlled without the
    hats pumping along with it) — off by default, same
    "capability, not a change" pattern as everything else in this module.

    pedalboard.Limiter applies automatic makeup gain toward its own
    threshold even on signal well under the ceiling (measured: a -23 dB
    RMS tone came out -18 dB after a -1 dB-threshold limiter) — it is not
    a passive brickwall. Running it BEFORE the final LUFS trim, then
    trimming with a plain multiply afterward, keeps the achieved loudness
    on target instead of compounding with the limiter's own gain.

    A sparse, high-crest-factor source (a few short loud hits over mostly
    silence — measured with a synthetic sparse test kit) can still overshoot
    the ceiling after that trim: its natural crest factor is wider than
    target_lufs - ceiling_db allows, so hitting the loudness target and
    respecting the ceiling are physically in tension. The backstop for that
    case is a SECOND limiter pass (squashes just the peaks, keeping more of
    the gained loudness) rather than a uniform linear scale-down (which
    would undo the trim evenly and undershoot target_lufs by several dB —
    measured on the sparse case: -18.9 vs a -12 target). A final linear
    clamp is the last-resort safety if even that doesn't clear the ceiling."""
    L, R = eq3(L, R, **(eq_kwargs or {}))
    if multiband:
        L, R = multiband_compress(L, R, **(multiband_kwargs or {}))
    else:
        L, R = glue_compressor(L, R, **(comp_kwargs or {}))
    if width != 1.0:
        # runs BEFORE the limiter so widening a side signal that pushes a
        # peak over the ceiling still gets caught by the safety stages
        # below, same reasoning as groove.master()'s width-then-limit order
        L, R = stereo_width(L, R, width=width)
    L, R = brickwall_limit(L, R, ceiling_db=ceiling_db)
    cur = lufs(L, R)
    g = 10 ** ((target_lufs - cur) / 20)
    L, R = L * g, R * g
    ceil = 10 ** (ceiling_db / 20)
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
    if peak > ceil:
        L, R = brickwall_limit(L, R, ceiling_db=ceiling_db)
        peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
        if peak > ceil:
            L, R = L * (ceil / peak), R * (ceil / peak)
    return L, R, lufs(L, R)
