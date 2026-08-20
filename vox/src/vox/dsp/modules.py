"""
Core processing modules. Every class here is a vox.core.Module: block-based,
sample-rate agnostic, and written so a JUCE port is a mechanical transliteration
(no numpy-only tricks in the per-sample math -- vectorized only where the
underlying operation truly is a filter applied over a block).
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sig

from ..core import Module, ParamSpec, db2lin, lin2db, one_pole_coeff


# =============================================================================
# EQ -- biquads, RBJ cookbook formulas, cascaded. Up to N bands like Nectar's 24.
# =============================================================================
def _rbj_biquad(kind: str, fs: float, f0: float, gain_db: float = 0.0, Q: float = 0.707):
    f0 = min(max(f0, 1.0), fs / 2 - 1.0)
    A = 10 ** (gain_db / 40.0)
    w0 = 2 * np.pi * f0 / fs
    cw, sw = np.cos(w0), np.sin(w0)
    alpha = sw / (2 * Q)

    if kind == "bell":
        b0, b1, b2 = 1 + alpha * A, -2 * cw, 1 - alpha * A
        a0, a1, a2 = 1 + alpha / A, -2 * cw, 1 - alpha / A
    elif kind == "low_shelf":
        rA = np.sqrt(A)
        b0 = A * ((A + 1) - (A - 1) * cw + 2 * rA * alpha)
        b1 = 2 * A * ((A - 1) - (A + 1) * cw)
        b2 = A * ((A + 1) - (A - 1) * cw - 2 * rA * alpha)
        a0 = (A + 1) + (A - 1) * cw + 2 * rA * alpha
        a1 = -2 * ((A - 1) + (A + 1) * cw)
        a2 = (A + 1) + (A - 1) * cw - 2 * rA * alpha
    elif kind == "high_shelf":
        rA = np.sqrt(A)
        b0 = A * ((A + 1) + (A - 1) * cw + 2 * rA * alpha)
        b1 = -2 * A * ((A - 1) + (A + 1) * cw)
        b2 = A * ((A + 1) + (A - 1) * cw - 2 * rA * alpha)
        a0 = (A + 1) - (A - 1) * cw + 2 * rA * alpha
        a1 = 2 * ((A - 1) - (A + 1) * cw)
        a2 = (A + 1) - (A - 1) * cw - 2 * rA * alpha
    elif kind == "highpass":
        b0, b1, b2 = (1 + cw) / 2, -(1 + cw), (1 + cw) / 2
        a0, a1, a2 = 1 + alpha, -2 * cw, 1 - alpha
    elif kind == "lowpass":
        b0, b1, b2 = (1 - cw) / 2, 1 - cw, (1 - cw) / 2
        a0, a1, a2 = 1 + alpha, -2 * cw, 1 - alpha
    else:
        raise ValueError(kind)
    return (np.array([b0, b1, b2]) / a0, np.array([a0, a1, a2]) / a0)


class Band:
    """One biquad with its own persistent filter state (so block processing
    is seamless across calls)."""

    def __init__(self, fs, kind="bell", freq=1000.0, gain_db=0.0, q=0.707):
        self.fs, self.kind, self.freq, self.gain_db, self.q = fs, kind, freq, gain_db, q
        self._design()
        self.zi = None

    def _design(self):
        self.b, self.a = _rbj_biquad(self.kind, self.fs, self.freq, self.gain_db, self.q)

    def set(self, freq=None, gain_db=None, q=None):
        if freq is not None: self.freq = freq
        if gain_db is not None: self.gain_db = gain_db
        if q is not None: self.q = q
        self._design()

    def reset(self):
        self.zi = None

    def process(self, x: np.ndarray) -> np.ndarray:
        ch = x.shape[1] if x.ndim > 1 else 1
        x2 = x if x.ndim > 1 else x[:, None]
        if self.zi is None:
            self.zi = np.zeros((2, ch))
        y = np.empty_like(x2)
        for c in range(ch):
            y[:, c], self.zi[:, c] = sig.lfilter(self.b, self.a, x2[:, c], zi=self.zi[:, c])
        return y if x.ndim > 1 else y[:, 0]


class ParametricEQ(Module):
    """Multi-band EQ. Static bands here; dynamic (level-dependent) EQ is
    DynamicEQ below, which wraps this per-band with a detector."""

    name = "eq"

    def __init__(self, fs, bands: list[dict] | None = None):
        super().__init__(fs)
        self.bands = [Band(fs, **b) for b in (bands or [])]

    def add_band(self, kind, freq, gain_db=0.0, q=0.707):
        self.bands.append(Band(self.fs, kind, freq, gain_db, q))

    def reset(self):
        for b in self.bands:
            b.reset()

    def process(self, x):
        y = x
        for b in self.bands:
            y = b.process(y)
        return y


# =============================================================================
# Dynamics detector -- shared by Gate, Compressor, De-esser (sidechain).
# Feed-forward, log-domain, program-dependent release. This is the exact
# topology the adversary required us to name.
# =============================================================================
class Detector:
    """
    Level detector: rectify -> (optional RMS window) -> log domain ->
    asymmetric one-pole smoothing (attack/release), matching the classic
    feed-forward VCA-style detector used in most software compressors.

    RMS mode uses a leaky integrator with time constant `rms_window_s`
    (an exponential "RMS", not a boxcar -- avoids a second buffer).
    """

    def __init__(self, fs, mode="rms", rms_window_s=0.010,
                attack_s=0.003, release_s=0.100):
        self.fs = fs
        self.mode = mode
        self.a_rms = one_pole_coeff(rms_window_s, fs)
        self.attack_s, self.release_s = attack_s, release_s
        self.a_att = one_pole_coeff(attack_s, fs)
        self.a_rel = one_pole_coeff(release_s, fs)
        self.y_sq = 0.0
        self.env_db = -120.0

    def set_times(self, attack_s=None, release_s=None):
        if attack_s is not None:
            self.attack_s = attack_s
            self.a_att = one_pole_coeff(attack_s, self.fs)
        if release_s is not None:
            self.release_s = release_s
            self.a_rel = one_pole_coeff(release_s, self.fs)

    def reset(self):
        self.y_sq = 0.0
        self.env_db = -120.0

    def process(self, x_mono: np.ndarray) -> np.ndarray:
        n = len(x_mono)
        out = np.empty(n)
        x2 = x_mono * x_mono
        ysq, env = self.y_sq, self.env_db
        a_rms = self.a_rms
        a_att, a_rel = self.a_att, self.a_rel
        if self.mode == "rms":
            for i in range(n):
                ysq += a_rms * (x2[i] - ysq)
                lvl_db = lin2db(np.sqrt(max(ysq, 1e-20)))
                a = a_att if lvl_db > env else a_rel
                env += a * (lvl_db - env)
                out[i] = env
        else:  # peak
            for i in range(n):
                lvl_db = lin2db(abs(x_mono[i]))
                a = a_att if lvl_db > env else a_rel
                env += a * (lvl_db - env)
                out[i] = env
        self.y_sq, self.env_db = ysq, env
        return out


# =============================================================================
# Compressor
# =============================================================================
class Compressor(Module):
    name = "compressor"
    params = (
        ParamSpec("threshold_db", "float", -18.0, -60.0, 0.0, "dB"),
        ParamSpec("ratio", "float", 3.0, 1.0, 20.0, ":1", curve="log"),
        ParamSpec("knee_db", "float", 6.0, 0.0, 24.0, "dB"),
        ParamSpec("attack_s", "float", 0.008, 0.0001, 0.5, "s", curve="log"),
        ParamSpec("release_s", "float", 0.120, 0.005, 2.0, "s", curve="log"),
        ParamSpec("makeup_db", "float", 0.0, -24.0, 24.0, "dB"),
        ParamSpec("mix", "float", 1.0, 0.0, 1.0, ""),
    )

    def prepare(self, fs):
        self.fs = fs
        self.det = Detector(fs, mode="rms", rms_window_s=0.006,
                            attack_s=self._p.get("attack_s", 0.008) if hasattr(self, "_p") else 0.008,
                            release_s=self._p.get("release_s", 0.12) if hasattr(self, "_p") else 0.12)

    def on_param_changed(self, name, value):
        if name in ("attack_s", "release_s"):
            self.det.set_times(attack_s=self._p["attack_s"], release_s=self._p["release_s"])

    def reset(self):
        self.det.reset()

    def _gain_curve_db(self, level_db):
        """Soft-knee downward compression. Static curve, evaluated per-sample
        on the SMOOTHED detector envelope (so this is a true program-dependent
        gain computer, not a lookup on unsmoothed level)."""
        thr, ratio, knee = self._p["threshold_db"], self._p["ratio"], self._p["knee_db"]
        x = level_db
        half = knee / 2.0
        if x < thr - half:
            gr = 0.0
        elif x > thr + half:
            gr = (x - thr) * (1.0 / ratio - 1.0)
        else:
            t = (x - (thr - half)) / max(knee, 1e-9)
            gr = (1.0 / ratio - 1.0) * (t * t * half)
        return gr

    def process(self, x: np.ndarray, key: np.ndarray = None) -> np.ndarray:
        """`key` is an optional EXTERNAL SIDECHAIN: the detector listens to it
        instead of to x (same length as x). This is what makes ducking
        possible -- compress the delay return while the dry vocal is present --
        without writing a second compressor. ARBITER will key off the vocal
        the same way."""
        src = key if key is not None else x
        mono = src.mean(axis=1) if src.ndim > 1 else src
        env_db = self.det.process(mono)
        gr_db = np.array([self._gain_curve_db(v) for v in env_db])
        gain = db2lin(gr_db + self._p["makeup_db"])
        wet = x * gain[:, None] if x.ndim > 1 else x * gain
        mix = self._p["mix"]
        return wet if mix >= 1.0 else (x * (1 - mix) + wet * mix)

    def latency_samples(self):
        return 0  # no lookahead in this variant


# =============================================================================
# Gate / expander (hysteresis via separate open/close thresholds, per bar)
# =============================================================================
class Gate(Module):
    name = "gate"
    params = (
        ParamSpec("open_db", "float", -45.0, -80.0, 0.0, "dB"),
        ParamSpec("close_db", "float", -50.0, -80.0, 0.0, "dB"),
        ParamSpec("ratio", "float", 4.0, 1.0, 100.0, ":1"),
        ParamSpec("attack_s", "float", 0.001, 0.0001, 0.2, "s"),
        ParamSpec("release_s", "float", 0.150, 0.005, 2.0, "s"),
    )

    def prepare(self, fs):
        self.fs = fs
        p = getattr(self, "_p", {})
        self.det = Detector(fs, mode="rms", rms_window_s=0.003,
                            attack_s=p.get("attack_s", 0.001),
                            release_s=p.get("release_s", 0.150))
        self.is_open = False

    def on_param_changed(self, name, value):
        if name in ("attack_s", "release_s"):
            self.det.set_times(attack_s=self._p["attack_s"], release_s=self._p["release_s"])

    def reset(self):
        self.det.reset()
        self.is_open = False

    def process(self, x: np.ndarray) -> np.ndarray:
        mono = x.mean(axis=1) if x.ndim > 1 else x
        env_db = self.det.process(mono)
        open_db, close_db, ratio = self._p["open_db"], self._p["close_db"], self._p["ratio"]
        gr = np.empty(len(env_db))
        state = self.is_open
        for i, lvl in enumerate(env_db):
            if state and lvl < close_db:
                state = False
            elif not state and lvl > open_db:
                state = True
            if state:
                gr[i] = 0.0
            else:
                # Two constraints, and it takes both clamps to satisfy them.
                #
                # NEVER BOOST. The original `close_db - lvl` goes negative
                # anywhere inside the hysteresis window (close_db < lvl <
                # open_db), turning gr into a positive GAIN -- measured
                # +2.95 dB at -45 dB in on the preset settings, i.e. the gate
                # amplified the room tone it exists to remove.
                #
                # STAY CONTINUOUS AT THE CLOSE THRESHOLD. Measuring the
                # shortfall against open_db instead fixes the boost but makes
                # the gain jump from 0 dB to -(open_db-close_db)*(1-1/ratio)
                # the instant the gate closes -- 5.03 dB on the preset values,
                # per-sample, unsmoothed: a click on every breath and phrase
                # tail. Trading a boost for a click is not a fix.
                #
                # max(...,0) holds unity across the hysteresis window and
                # starts attenuating only below close_db, where the expander
                # curve leaves 0 dB continuously. Measured max gain step:
                # 5.03 dB -> 0.05 dB. See
                # test_gate_never_boosts_inside_the_hysteresis_window and
                # test_gate_has_no_step_discontinuity.
                under = max(close_db - lvl, 0.0)
                gr[i] = min(-under * (1.0 - 1.0 / ratio), 0.0)
        self.is_open = state
        gain = db2lin(gr)
        return x * gain[:, None] if x.ndim > 1 else x * gain


# =============================================================================
# De-esser: split-band dynamic attenuation in the sibilance region only.
# =============================================================================
class DeEsser(Module):
    name = "deesser"
    params = (
        ParamSpec("freq_hz", "float", 6500.0, 800.0, 12000.0, "Hz", curve="log"),
        ParamSpec("threshold_db", "float", -24.0, -60.0, 0.0, "dB"),
        ParamSpec("ratio", "float", 4.0, 1.0, 20.0, ":1"),
        ParamSpec("range_db", "float", 12.0, 0.0, 24.0, "dB"),
        ParamSpec("mix", "float", 1.0, 0.0, 1.0, ""),
    )

    def prepare(self, fs):
        self.fs = fs
        self._f = self._p.get("freq_hz", 6500.0) if hasattr(self, "_p") else 6500.0
        self._sc = self._make_hp()                     # sidechain (mono)
        self._split: dict[int, tuple] = {}             # per channel, own state
        self.det = Detector(fs, mode="rms", rms_window_s=0.002,
                            attack_s=0.0008, release_s=0.06)

    # Linkwitz-Riley 4th order = two cascaded Butterworth (q=0.707) sections.
    # LP + HP sums back to an allpass, i.e. FLAT magnitude, which is what makes
    # gaining only the HP half safe: at gain=1 the body is untouched.
    def _make_hp(self):
        return [Band(self.fs, "highpass", self._f, q=0.707) for _ in range(2)]

    def _make_lp(self):
        return [Band(self.fs, "lowpass", self._f, q=0.707) for _ in range(2)]

    def _split_for(self, c: int):
        if c not in self._split:
            self._split[c] = (self._make_lp(), self._make_hp())
        return self._split[c]

    @staticmethod
    def _cascade(bands, sig_):
        for b in bands:
            sig_ = b.process(sig_)
        return sig_

    def on_param_changed(self, name, value):
        if name == "freq_hz":
            self._f = value
            self._sc = self._make_hp()
            self._split.clear()

    def reset(self):
        self.det.reset()
        for b in self._sc:
            b.reset()
        for lp, hp in self._split.values():
            for b in (*lp, *hp):
                b.reset()

    def process(self, x: np.ndarray) -> np.ndarray:
        """
        Split-band de-essing: a Linkwitz-Riley crossover at freq_hz splits the
        signal, a detector on the high half drives a gain applied ONLY to that
        half, and the two halves are summed. Below the crossover nothing is
        touched -- unlike a broadband ducking de-esser, which is what most
        cheap plugins do.

        BUG FIX 2026-08-19: this used to detect on, and subtract, a bell at
        0 dB gain. A bell at 0 dB is a mathematical identity (A=1 makes b==a),
        so the "band" was the whole signal and this was a broadband ducker --
        exactly what the paragraph above claims it isn't. Measured against
        Techivation T-De-Esser on the reference acapella: 4.8 dB of body
        (200 Hz-4 kHz) damage to get 2.2 dB of sibilance reduction. The
        obvious repair (highpass instead of bell, still subtracted from the
        full signal) does NOT work either: the highpass phase-rotates the band
        so the subtraction is incoherent and the level barely moves. Hence a
        real crossover. See tools/ab_reference.py for the measurement.
        """
        x2 = x if x.ndim > 1 else x[:, None]
        ch = x2.shape[1]
        mono = x2.mean(axis=1)

        env_db = self.det.process(self._cascade(self._sc, mono))
        thr, ratio, rng = self._p["threshold_db"], self._p["ratio"], self._p["range_db"]
        over = np.maximum(env_db - thr, 0.0)
        cut_db = -np.minimum(over * (1.0 - 1.0 / ratio), rng)
        gain = db2lin(cut_db)[:, None]  # (n,1), stereo-linked

        lo = np.empty_like(x2)
        hi = np.empty_like(x2)
        for c in range(ch):
            lp, hp = self._split_for(c)
            lo[:, c] = self._cascade(lp, x2[:, c])
            hi[:, c] = self._cascade(hp, x2[:, c])

        # Mix scales the GAIN, not the signal. The wet path (lo + hi) is an
        # LR4 sum: magnitude-flat but allpass, i.e. NOT phase-flat. Blending
        # it against the dry signal therefore combs -- measured a -70.1 dB
        # null at mix=0.5, freq=5500. Interpolating the gain toward unity
        # keeps the output a single allpass sum at every mix value, which is
        # also what "50% de-essing" should mean: half the gain reduction.
        # See test_deesser_partial_mix_does_not_notch.
        mix = self._p["mix"]
        if mix <= 0.0:
            # Must be a true bypass. The wet path is an LR4 sum: flat in
            # magnitude but allpass, so returning lo+hi at mix=0 leaves the
            # phase rotated and any parallel dry path around this module combs
            # (measured null of only -6.6 dB against the input). Every other
            # module here nulls at mix=0; this one has to as well.
            return x
        # Gain interpolated in the LOG domain: gain**mix, not
        # 1 + mix*(gain-1). "50% de-essing" should mean half the gain
        # reduction in dB -- linear interpolation of a -6 dB reduction gives
        # -2.5 dB, not -3 dB.
        wet = lo + hi * gain ** mix
        return wet if x.ndim > 1 else wet[:, 0]


# =============================================================================
# Saturation -- oversampled nonlinearity. MEASURED FINDING baked in as defaults:
# tanh needs >=8x OS to clear -90 dBFS alias floor; hard-knee clippers need ADAA.
# =============================================================================
class Saturation(Module):
    name = "saturation"
    params = (
        ParamSpec("drive_db", "float", 6.0, 0.0, 24.0, "dB"),
        ParamSpec("mix", "float", 0.35, 0.0, 1.0, ""),
        ParamSpec("mode", "enum", 0, choices=("tanh", "adaa_hardclip")),
        ParamSpec("oversample", "int", 8, 4, 16, "x"),
    )

    def prepare(self, fs):
        self.fs = fs
        self._design_filters()

    def on_param_changed(self, name, value):
        if name == "oversample":
            self._design_filters()

    def _design_filters(self):
        os = int(self._p.get("oversample", 8)) if hasattr(self, "_p") else 8
        self.os = os
        n_taps = 32 * os + 1
        h = sig.firwin(n_taps, 0.95 / os, window=("kaiser", 9.0))
        self.up_h = h * os
        self.down_h = h
        # Resampling filter state is PER CHANNEL. A single shared zi lets one
        # channel's filter tail seed the next channel's history -- measured on
        # true-stereo material as a 0.76-amplitude error over the first 64
        # samples of the right channel (larger than the signal itself), i.e. an
        # audible pop at every block boundary. See
        # test_saturation_channels_are_independent.
        self.up_zi: dict[int, np.ndarray] = {}
        self.down_zi: dict[int, np.ndarray] = {}
        # Dry-path delay line. The wet path comes out latency_samples() late
        # (oversampling FIR group delay), so mixing it against the UNDELAYED
        # input is a comb filter, not a blend -- measured -3.81/+0.86 dB of
        # ripple across 100 Hz-15 kHz at the mix values the presets ship. The
        # dry path is delayed to match. See
        # test_saturation_partial_mix_does_not_comb.
        self.dry_buf = None

    def reset(self):
        self.up_zi = {}
        self.down_zi = {}
        self.dry_buf = None

    @staticmethod
    def _adaa_hardclip(x: np.ndarray) -> np.ndarray:
        """First-order antiderivative anti-aliasing for y=clip(x,-1,1).
        F1(x) is the antiderivative of clip(x); ADAA1 = (F1(x2)-F1(x1))/(x2-x1)
        where consecutive samples differ, else falls back to clip(x)."""
        def F1(v):
            return np.where(np.abs(v) <= 1, 0.5 * v * v, np.abs(v) - 0.5)
        x1 = x[:-1]
        x2 = x[1:]
        dx = x2 - x1
        f1, f2 = F1(x1), F1(x2)
        safe = np.abs(dx) > 1e-6
        y = np.where(safe, (f2 - f1) / np.where(safe, dx, 1.0), np.clip((x1 + x2) / 2, -1, 1))
        return np.concatenate([[np.clip(x[0], -1, 1)], y])

    def _upsample(self, x, c=0):
        up = np.zeros(len(x) * self.os)
        up[::self.os] = x
        zi = self.up_zi.get(c)
        y, self.up_zi[c] = sig.lfilter(self.up_h, [1.0], up,
                                       zi=zi if zi is not None else np.zeros(len(self.up_h) - 1))
        return y

    def _downsample(self, x, c=0):
        zi = self.down_zi.get(c)
        y, self.down_zi[c] = sig.lfilter(self.down_h, [1.0], x,
                                         zi=zi if zi is not None else np.zeros(len(self.down_h) - 1))
        return y[::self.os]

    def process(self, x: np.ndarray) -> np.ndarray:
        ch = x.shape[1] if x.ndim > 1 else 1
        x2 = x if x.ndim > 1 else x[:, None]
        drive = db2lin(self._p["drive_db"])
        mode = self._p["mode"]
        out = np.empty_like(x2)
        for c in range(ch):
            up = self._upsample(x2[:, c] * drive, c)
            if mode == "adaa_hardclip" or mode == 1:
                sat = self._adaa_hardclip(up)
            else:
                sat = np.tanh(up)
            down = self._downsample(sat, c)[:len(x2)]
            out[:, c] = down
        mix = self._p["mix"]
        dry = self._delayed_dry(x2)
        wet, dry = (out, dry) if x.ndim > 1 else (out[:, 0], dry[:, 0])
        return wet * mix + dry * (1 - mix)

    def _delayed_dry(self, x2: np.ndarray) -> np.ndarray:
        """The input delayed by latency_samples(), so it lines up with the wet
        path. Block-size independent: the tail carries across calls."""
        lat = self.latency_samples()
        if lat <= 0:
            return x2
        if self.dry_buf is None or self.dry_buf.shape != (lat, x2.shape[1]):
            self.dry_buf = np.zeros((lat, x2.shape[1]), dtype=float)
        ext = np.concatenate([self.dry_buf, x2], axis=0)
        self.dry_buf = ext[len(ext) - lat:].copy()
        return ext[:len(x2)]

    def latency_samples(self):
        return (len(self.up_h) // 2 + len(self.down_h) // 2) // max(self.os, 1)


# =============================================================================
# True-peak lookahead limiter -- last stage. Uses the SAME oversampled peak
# measurement as meter.true_peak_db so what the limiter targets is what the
# meter reports.
# =============================================================================
class Limiter(Module):
    """
    True-peak lookahead limiter. The bar (docs/00_BAR.md) requires true-peak
    accuracy to +/-0.1 dBTP -- a sample-peak-only detector WILL overshoot on
    inter-sample peaks (measured: 0.4 dB over ceiling on a 997 Hz test tone
    before this was fixed). Detection therefore runs on an oversampled,
    BS.1770-4-style FIR-interpolated envelope, the same method meter.py uses
    to grade the output, so what the limiter targets is what the meter reports.

    OS is 16 to match meter.true_peak_db's default, and for the same reason:
    at 8x the interpolated envelope under-reads by up to 0.139 dB at exact
    submultiples of fs, so a limiter detecting at 8x can overshoot its ceiling
    by that much -- outside the bar. Detecting at a lower rate than the meter
    grades at would mean targeting a number the meter then refuses to confirm.
    """
    name = "limiter"
    params = (
        ParamSpec("ceiling_dbtp", "float", -1.0, -12.0, 0.0, "dBTP"),
        ParamSpec("lookahead_ms", "float", 5.0, 1.0, 20.0, "ms"),
        ParamSpec("release_s", "float", 0.080, 0.010, 1.0, "s"),
    )
    OS = 16

    def prepare(self, fs):
        self.fs = fs
        la = self._p.get("lookahead_ms", 5.0) if hasattr(self, "_p") else 5.0
        self.la_n = int(round(la * 1e-3 * fs))
        self.gain_state = 1.0
        self.a_rel = one_pole_coeff(self._p.get("release_s", 0.08) if hasattr(self, "_p") else 0.08, fs)

        n_taps = 48 * self.OS + 1
        self._tp_h = sig.firwin(n_taps, 1.0 / self.OS, window=("kaiser", 8.0)) * self.OS
        # FIR group delay in ORIGINAL-rate samples. numtaps-1 = 48*OS is always
        # divisible by 2*OS, so this is exactly 24 regardless of OS -- the
        # interpolation filter's own latency, which the detector must look
        # PAST or every peak appears 24 samples later than it really is and
        # the gain reduction arrives too late (this was the source of the
        # measured 0.3-0.7 dB ceiling overshoot at high frequencies before
        # this was accounted for).
        self._fir_delay = (n_taps - 1) // 2 // self.OS
        # History is always the MAXIMUM lookahead, not the current one, so that
        # raising lookahead_ms mid-stream pulls real audio out of history
        # instead of silence. Sizing it to the current la_n meant a change had
        # to resize the buffer, and any padding introduced showed up in the
        # output as a splice (measured: two discontinuities 40x the signal's
        # own slew on a clean sine). With max-sized history a lookahead change
        # is just a different index into audio we already have.
        la_max = next(p.hi for p in self.params if p.name == "lookahead_ms")
        # 2x _fir_delay, not 1x: the interpolating FIR needs history on BOTH
        # sides of the window it reads. At the maximum lookahead `off` reaches
        # 0, and with only one margin peak_env[0] is produced by an FIR that
        # has half the samples it needs -- it starts cold at every block
        # boundary, breaking block-size invariance (measured 5.45e-03 between
        # whole-file and 512-sample chunks at lookahead_ms=20, exactly 0.0 at
        # every smaller value). The old code had this margin wrong at EVERY
        # lookahead; sizing history to the maximum only moved where it showed.
        self._hist = int(round(la_max * 1e-3 * fs)) + 2 * self._fir_delay
        self.buf = None  # holds self._hist samples of input history

    def on_param_changed(self, name, value):
        if name == "lookahead_ms":
            # No buffer surgery needed: self.buf is always self._hist long
            # (max lookahead), so this only changes where the window is read
            # from. The audio delay genuinely changes with lookahead, so a
            # host must renegotiate PDC -- see latency_samples().
            # ponytail: one unavoidable sample-step at the change (the delay
            # line length really did change). A short crossfade between the old
            # and new read positions would remove it -- add that if lookahead
            # ever becomes an automatable knob rather than a setup parameter.
            self.la_n = int(round(value * 1e-3 * self.fs))
        if name == "release_s":
            self.a_rel = one_pole_coeff(value, self.fs)

    def latency_samples(self):
        """Reported/compensable latency: only the intentional lookahead. The
        FIR alignment delay is absorbed internally and does not add to the
        audio path delay (detection-only, does not touch out_src)."""
        return self.la_n

    def reset(self):
        self.buf = None
        self.gain_state = 1.0

    def _true_peak_envelope(self, ext: np.ndarray) -> np.ndarray:
        """
        True (inter-sample) peak per ORIGINAL-rate sample position, realigned
        for the FIR's own group delay.

        MUST interpolate the SIGNED per-channel waveform and rectify AFTER
        filtering. Rectifying first (as an earlier version of this method
        did) fabricates spurious high-frequency content at every
        zero-crossing -- |sin(t)| has a kink every half-cycle that a sine
        never had -- and the interpolator then reconstructs THAT, silently
        under-estimating the true peak (measured: up to 2.3 dB off, i.e. a
        limiter that thinks it's 2.3 dB under ceiling when it is over it).
        `ext` is (n, channels).
        """
        n, ch = ext.shape
        d = self._fir_delay * self.OS
        peak = None
        for c in range(ch):
            up = np.zeros(n * self.OS)
            up[::self.OS] = ext[:, c]
            y = np.abs(sig.lfilter(self._tp_h, [1.0], up))
            y = y[d:]
            usable = len(y) // self.OS
            y = y[: usable * self.OS].reshape(usable, self.OS).max(axis=1)
            peak = y if peak is None else np.maximum(peak, y)
        return peak  # peak[i] = true inter-sample peak covering [sample_i, sample_i+1)

    def process(self, x: np.ndarray) -> np.ndarray:
        ch = x.shape[1] if x.ndim > 1 else 1
        x2 = x if x.ndim > 1 else x[:, None]
        n = len(x2)
        hist = self._hist
        if self.buf is None or self.buf.shape != (hist, ch):
            self.buf = np.zeros((hist, ch))
        ext = np.concatenate([self.buf, x2], axis=0)  # len = hist + n
        peak_env = self._true_peak_envelope(ext)      # peak_env[j] <-> ext[j + fir_delay]
        # Output is delayed by la_n, so output sample i is ext[off_a + i] and
        # its lookahead window starts at peak_env[off + i].
        off_a = hist - self.la_n
        off = off_a - self._fir_delay

        needed_gain = np.ones(n)
        ceiling = db2lin(self._p["ceiling_dbtp"])
        g = self.gain_state
        win = self.la_n
        for i in range(n):
            seg_max = np.max(peak_env[off + i:off + i + win + 1]) if win > 0 else peak_env[off + i]
            target_g = min(1.0, ceiling / max(seg_max, 1e-9))
            if target_g < g:
                g = target_g          # instant attack on lookahead peaks
            else:
                g += self.a_rel * (target_g - g)
            needed_gain[i] = g
        self.gain_state = g
        out_src = ext[off_a:off_a + n]  # audio delayed by la_n only
        y = out_src * needed_gain[:, None]
        self.buf = ext[-hist:].copy()
        return y if x.ndim > 1 else y[:, 0]


# =============================================================================
# Stack -- harmonizer-style doubler (pitch-shift + micro-delay + pan)
# =============================================================================
class Stack(Module):
    """Printed vocal thickening: dry centre + one copy pitched UP `cents` on a
    long micro-delay panned left, one pitched DOWN on a shorter one panned
    right. Source: ~/Desktop/vox references/TUPAC-VOCAL-STACKING-TECHNIQUE.md
    (+12c/25ms/L, -12c/10ms/R).

    WHY NOT pedalboard.PitchShift: it is Rubber Band, which buffers ~52k
    samples (1.08 s at 48k) before it returns anything and does not return a
    block of the same length it was given -- it cannot satisfy core.Module's
    "same shape out, correct at any block size" contract. What is built here
    instead is the classic two-tap crossfading delay-line (Doppler) shifter,
    which is also what the hardware harmonizers this technique came off of
    actually did. Zero latency, exact at block size 1.

    Each voice reads the delay line at a slightly wrong rate, so the read
    delay ramps; when the ramp has travelled one window it wraps, and a second
    tap half a window out of phase is crossfaded in so the wrap is inaudible.
    """

    name = "stack"
    params = (
        ParamSpec("cents", "float", 12.0, 0.0, 50.0, "cents"),
        ParamSpec("delay_l_s", "float", 0.025, 0.001, 0.100, "s"),
        ParamSpec("delay_r_s", "float", 0.010, 0.001, 0.100, "s"),
        ParamSpec("window_s", "float", 0.050, 0.010, 0.200, "s"),
        ParamSpec("mix", "float", 0.35, 0.0, 1.0, ""),
    )

    def prepare(self, fs):
        self.fs = float(fs)
        self._alloc()

    def _alloc(self):
        p = self._p if hasattr(self, "_p") else {}
        self._win = max(int(round(p.get("window_s", 0.050) * self.fs)), 16)
        base = max(p.get("delay_l_s", 0.025), p.get("delay_r_s", 0.010))
        # + one extra window of headroom: process() writes at most a window
        # of new samples per pass, and must not overwrite history a tap is
        # still reading (same chunking rule ThrowDelay uses)
        self._len = int(round(base * self.fs)) + 2 * self._win + 4
        # one delay line per (voice, channel) -- no shared state across
        # channels, the bug Saturation shipped with once (DECISIONS 2026-08-18)
        self._buf = {}
        self._w = {}
        self._phase = {}

    def on_param_changed(self, name, value):
        if name in ("cents", "delay_l_s", "delay_r_s", "window_s"):
            self._alloc()

    def reset(self):
        self._alloc()

    def latency_samples(self) -> int:
        return 0  # the dry path is untouched; the voices are meant to be late

    def _voice(self, src: np.ndarray, key, ratio: float, delay_s: float) -> np.ndarray:
        # chunk so a long block can't overwrite history the taps still need;
        # keeps the result identical at block size 1 and at 8192
        out = np.empty(len(src))
        pos = 0
        while pos < len(src):
            k = min(self._win, len(src) - pos)
            out[pos:pos + k] = self._voice_chunk(src[pos:pos + k], key, ratio, delay_s)
            pos += k
        return out

    def _voice_chunk(self, src: np.ndarray, key, ratio: float, delay_s: float) -> np.ndarray:
        n = len(src)
        L = self._len
        if key not in self._buf:
            self._buf[key] = np.zeros(L)
            self._w[key] = 0
            self._phase[key] = 0.0
        buf, w, phase = self._buf[key], self._w[key], self._phase[key]

        k = np.arange(n)
        buf[(w + k) % L] = src

        win = float(self._win)
        base = delay_s * self.fs
        # delay must move at (1 - ratio) samples per sample to shift pitch by
        # `ratio`; expressed as a 0..1 sawtooth over one window
        dph = (1.0 - ratio) / win
        f = (phase + k * dph) % 1.0
        out = np.zeros(n)
        for frac in (f, (f + 0.5) % 1.0):
            pos = (w + k) - (base + frac * win)
            i0 = np.floor(pos).astype(np.int64)
            a = pos - i0
            tap = buf[i0 % L] * (1.0 - a) + buf[(i0 + 1) % L] * a
            out += tap * (0.5 - 0.5 * np.cos(2.0 * np.pi * frac))

        self._w[key] = (w + n) % L
        self._phase[key] = float((phase + n * dph) % 1.0)
        return out

    def process(self, x: np.ndarray) -> np.ndarray:
        x2 = x[:, None] if x.ndim == 1 else x
        ch = x2.shape[1]
        src = x2.mean(axis=1)
        r = 2.0 ** (self.get("cents") / 1200.0)
        up = self._voice(src, "up", r, self.get("delay_l_s"))
        dn = self._voice(src, "dn", 1.0 / r, self.get("delay_r_s"))
        mix = self.get("mix")

        out = x2.copy()
        if ch >= 2:
            out[:, 0] += mix * up
            out[:, 1] += mix * dn
        else:
            # mono in, mono out: both voices collapse to centre. The panning
            # is the point of this technique, so a mono chain gets the
            # thickness but not the width -- widening the channel count
            # mid-chain would be worse.
            out[:, 0] += mix * 0.5 * (up + dn)
        return out if x.ndim > 1 else out[:, 0]
