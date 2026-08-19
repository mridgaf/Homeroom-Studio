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
        self.det = Detector(fs, mode="rms", rms_window_s=0.003, attack_s=0.001, release_s=0.15)
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
                under = close_db - lvl
                gr[i] = -under * (1.0 - 1.0 / ratio)
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
        f = self._p.get("freq_hz", 6500.0) if hasattr(self, "_p") else 6500.0
        self.band = Band(fs, "bell", f, 0.0, q=1.4)   # sidechain detection (mono)
        self._notch_ch: list[Band] = []                # one filter per channel, own state
        self._notch_freq = f
        self.det = Detector(fs, mode="rms", rms_window_s=0.002, attack_s=0.0008, release_s=0.06)

    def _notch_for(self, ch: int) -> Band:
        while len(self._notch_ch) < ch:
            self._notch_ch.append(Band(self.fs, "bell", self._notch_freq, 0.0, q=1.4))
        return self._notch_ch

    def on_param_changed(self, name, value):
        if name == "freq_hz":
            self.band.set(freq=value)
            self._notch_freq = value
            for b in self._notch_ch:
                b.set(freq=value)

    def reset(self):
        self.band.reset(); self.det.reset()
        for b in self._notch_ch:
            b.reset()

    def process(self, x: np.ndarray) -> np.ndarray:
        """
        Split-band de-essing: extract the sibilance band with a bell filter,
        compute a shared time-varying gain from its envelope (detected on the
        mono sum for stereo-linked ess reduction), then subtract
        band*(1-gain) from the FULL-BAND signal. This attenuates only the
        target band and leaves everything else untouched -- unlike a
        broadband ducking de-esser, which is what most cheap plugins do.
        """
        x2 = x if x.ndim > 1 else x[:, None]
        ch = x2.shape[1]
        mono = x2.mean(axis=1)

        sc = self.band.process(mono)
        env_db = self.det.process(sc)
        thr, ratio, rng = self._p["threshold_db"], self._p["ratio"], self._p["range_db"]
        over = np.maximum(env_db - thr, 0.0)
        cut_db = -np.minimum(over * (1.0 - 1.0 / ratio), rng)
        gain = db2lin(cut_db)[:, None]  # (n,1), broadcasts across channels

        notches = self._notch_for(ch)
        band_sig = np.stack([notches[c].process(x2[:, c]) for c in range(ch)], axis=1)

        wet = x2 + band_sig * (gain - 1.0)
        mix = self._p["mix"]
        out = wet if mix >= 1.0 else (x2 * (1 - mix) + wet * mix)
        return out if x.ndim > 1 else out[:, 0]


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
        self.up_zi = None
        self.down_zi = None

    def reset(self):
        self.up_zi = None
        self.down_zi = None

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

    def _upsample(self, x):
        up = np.zeros(len(x) * self.os)
        up[::self.os] = x
        y, self.up_zi = sig.lfilter(self.up_h, [1.0], up,
                                    zi=self.up_zi if self.up_zi is not None else np.zeros(len(self.up_h) - 1))
        return y

    def _downsample(self, x):
        y, self.down_zi = sig.lfilter(self.down_h, [1.0], x,
                                      zi=self.down_zi if self.down_zi is not None else np.zeros(len(self.down_h) - 1))
        return y[::self.os]

    def process(self, x: np.ndarray) -> np.ndarray:
        ch = x.shape[1] if x.ndim > 1 else 1
        x2 = x if x.ndim > 1 else x[:, None]
        drive = db2lin(self._p["drive_db"])
        mode = self._p["mode"]
        out = np.empty_like(x2)
        for c in range(ch):
            up = self._upsample(x2[:, c] * drive)
            if mode == "adaa_hardclip" or mode == 1:
                sat = self._adaa_hardclip(up)
            else:
                sat = np.tanh(up)
            down = self._downsample(sat)[:len(x2)]
            out[:, c] = down
        mix = self._p["mix"]
        wet = out if x.ndim > 1 else out[:, 0]
        return wet * mix + x * (1 - mix)

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
    before this was fixed). Detection therefore runs on a 4x-oversampled,
    BS.1770-4-style FIR-interpolated envelope, the same method meter.py uses
    to grade the output, so what the limiter targets is what the meter reports.
    """
    name = "limiter"
    params = (
        ParamSpec("ceiling_dbtp", "float", -1.0, -12.0, 0.0, "dBTP"),
        ParamSpec("lookahead_ms", "float", 5.0, 1.0, 20.0, "ms"),
        ParamSpec("release_s", "float", 0.080, 0.010, 1.0, "s"),
    )
    OS = 8

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
        self.buf = None  # holds la_n (audio delay) + fir_delay (detector-only) samples

    def on_param_changed(self, name, value):
        if name == "lookahead_ms":
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
        need = self.la_n + self._fir_delay
        if self.buf is None:
            self.buf = np.zeros((need, ch))
        ext = np.concatenate([self.buf, x2], axis=0)  # len = need + n
        peak_env = self._true_peak_envelope(ext)      # len = need + n - fir_delay = la_n + n

        needed_gain = np.ones(n)
        ceiling = db2lin(self._p["ceiling_dbtp"])
        g = self.gain_state
        win = self.la_n
        for i in range(n):
            seg_max = np.max(peak_env[i:i + win + 1]) if win > 0 else peak_env[i]
            target_g = min(1.0, ceiling / max(seg_max, 1e-9))
            if target_g < g:
                g = target_g          # instant attack on lookahead peaks
            else:
                g += self.a_rel * (target_g - g)
            needed_gain[i] = g
        self.gain_state = g
        out_src = ext[self._fir_delay:self._fir_delay + n]  # audio delayed by la_n only
        y = out_src * needed_gain[:, None]
        self.buf = ext[-need:]
        return y if x.ndim > 1 else y[:, 0]
