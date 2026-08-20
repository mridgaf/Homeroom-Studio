"""
Artist vocal-chain presets, built one at a time per the owner's protocol
(see DECISIONS.md 2026-08-18) -- wait for "continue" before the next one.
Quality bar for these is deliberately lighter than the core DSP modules:
does it run, does it sound like the reference. Not the full adversarial
review loop.

Each preset is just chain_demo.build_chain()'s cleanup stages (gate,
de-esser, HPF) with the mix-character stages (compressor, saturation,
reverb) swapped for the artist's documented numbers. No new DSP modules --
every preset here is buildable from what vox.dsp already has.
"""
from __future__ import annotations

import numpy as np

from . import dsp
from .core import Chain

# The RMS-detector peak level of a well-recorded rap vocal stem, measured as
# the 99th percentile of the compressor's own detector envelope.
#
# CALIBRATION SOURCE (corrected 2026-08-20): this used to be -14.0, set
# because "both reference acapellas land within ~1 dB of this". That was a
# contaminated calibration -- the acapellas are commercial releases, already
# compressed and mastered, so they sit hot and tight. A DRY vocal does not:
# `debbie8 13 26 vc loop reason.wav` measures -18.3 dB. Calibrating a
# threshold default on finished masters biases every derived threshold ~4 dB
# high, i.e. toward doing less than the preset claims. Defaults now come from
# dry material; anything real should still pass its own measured level in.
#
# WHY THIS EXISTS: the research docs quote HARDWARE thresholds ("~0 dB", i.e.
# near 0 VU on a desk running +4 dBu nominal). Setting a digital compressor's
# threshold to 0 dBFS from that number makes it completely inert -- measured
# on `eminem lose vocal.wav`, a 0 dBFS threshold engaged on 0.0% of the file,
# because the detector never gets above -12.4 dB. Thresholds below are
# therefore derived from program level, the way the engineer set them by ear,
# not copied from the hardware faceplate.
NOMINAL_PROGRAM_DB = -18.3

# Same trap, one stage earlier: the de-esser threshold was a flat -22 dB in all
# three presets, copied from nothing in particular. Measured on the reference
# acapellas, the 7 kHz+ band only reaches -22.6 dB (Eminem) / -27.3 dB (Tupac)
# at its 99th percentile, so -22 caught essentially nothing (0.03 dB of
# sibilance reduction -- tools/ab_reference.py). Threshold is therefore derived
# from the stem's own sibilance level, like the compressor's is from program
# level, and the threshold is then derived to land a target gain reduction on
# the loudest esses -- a percentile used AS the threshold does not work, the
# detector's 60 ms release smears each ess across enough frames to drag any
# percentile up into the esses themselves. Default is measured on the dry
# vocal (-17.0), not on an acapella -- see NOMINAL_PROGRAM_DB.
NOMINAL_SIBILANCE_DB = -17.0
DEESS_RATIO = 4.0
# WITHDRAWN 2026-08-19 TUNING, CORRECTED 2026-08-20. The 2026-08-19 pass moved
# the crossover 7000 -> 5500 Hz because "63% of the ess energy on `eminem lose
# vocal.wav` sits below 7 kHz". That measurement was taken on a commercial
# acapella that has ALREADY been de-essed and mastered: its energy above 10 kHz
# is 0.92% of total, against 3.06% on a dry vocal. Prior processing had scooped
# the top of its own ess band, which drags the apparent ess distribution down --
# so the number described the reference's mastering, not sibilance.
#
# Measured as the 15th-percentile lower edge of ess-EXCESS energy (sibilant
# frames over voiced frames, so program content cancels out):
#     dry vocal   7192 Hz        eminem acapella 5340 Hz    tupac acapella 5814 Hz
# A fixed 5500 Hz is ~1.7 kHz below the real ess band on dry material, which is
# where the de-esser is meant to run -- it reaches into presence and consonants
# instead. The crossover is therefore DERIVED from the stem now, the same
# two-pass pattern the thresholds already use. The constant is only a fallback.
DEESS_TARGET_GR_DB = 6.0
DEESS_FREQ_HZ = 7200.0


def program_level_db(x: np.ndarray, fs: float) -> float:
    """Level the compressor's RMS detector actually sees, as a robust
    'loudest passages' figure (99th percentile, not the single max sample).

    This is an OFFLINE analysis pass whose result gets pushed into a normal
    per-block Module's threshold -- the pattern core.py's docstring sanctions
    for two-pass decisions. It does not make process() non-real-time-legal.
    """
    mono = x.mean(axis=1) if np.ndim(x) > 1 else x
    det = dsp.Detector(fs, mode="rms", rms_window_s=0.006,
                       attack_s=0.015, release_s=0.05)
    return float(np.percentile(det.process(mono), 99))


def sibilance_level_db(x: np.ndarray, fs: float,
                       freq_hz: float = DEESS_FREQ_HZ) -> float:
    """Level the de-esser's own sidechain sees on the LOUDEST esses (99.9th
    percentile of its detector). Offline analysis feeding a per-block param,
    same two-pass pattern as program_level_db."""
    mono = x.mean(axis=1) if np.ndim(x) > 1 else x
    for _ in range(2):  # LR4 highpass, matching DeEsser's crossover
        mono = dsp.Band(fs, "highpass", freq_hz, q=0.707).process(mono)
    det = dsp.Detector(fs, mode="rms", rms_window_s=0.002,
                       attack_s=0.0008, release_s=0.06)
    return float(np.percentile(det.process(mono), 99.9))


def sibilance_freq_hz(x: np.ndarray, fs: float,
                      lo_hz: float = 4500.0, hi_hz: float = 9500.0) -> float:
    """Where this stem's ess band actually starts, as the lower edge of its
    ess-EXCESS energy. Offline analysis feeding a per-block param, same
    two-pass pattern as program_level_db.

    "Excess" means the sibilant-frame spectrum divided by the voiced-frame
    spectrum, so steady program content cancels and only the ess-specific lift
    is left. That distinction is the whole point: a plain ess-band spectrum is
    dominated by whatever the source's HF balance happens to be, which is how
    a fixed 5500 Hz got calibrated on an already-de-essed master (see
    DEESS_FREQ_HZ). Clamped to [lo_hz, hi_hz] -- an estimator this cheap should
    not be trusted to pick an arbitrary frequency.
    """
    from scipy.signal import stft
    mono = x.mean(axis=1) if np.ndim(x) > 1 else x
    f, _, Z = stft(mono, fs, nperseg=1024)
    P = np.abs(Z) ** 2
    body = P[(f >= 300) & (f < 3000)].sum(0)
    top = P[(f >= 5000) & (f < 12000)].sum(0)
    active = (body + top) > np.percentile(body + top, 60)
    if active.sum() < 8:
        return DEESS_FREQ_HZ
    ratio = top / (body + 1e-20)
    ess = active & (ratio > np.percentile(ratio[active], 90))
    voiced = active & (ratio < np.percentile(ratio[active], 50))
    if ess.sum() < 4 or voiced.sum() < 4:
        return DEESS_FREQ_HZ
    S, V = P[:, ess].mean(1), P[:, voiced].mean(1)
    # Weight by the ess energy ITSELF, gated to bins the esses actually lift.
    # Weighting by the lift ratio instead biases the edge ~1 kHz high: the
    # ratio is smallest exactly at the bottom of the ess band, which is the
    # edge being looked for.
    w_all = np.where(S > V * 1.5, S, 0.0)
    band = (f >= 3000) & (f <= 14000)
    w = w_all[band]
    if w.sum() <= 0:
        return DEESS_FREQ_HZ
    edge = f[band][np.searchsorted(np.cumsum(w) / w.sum(), 0.15)]
    return float(np.clip(edge, lo_hz, hi_hz))


def _threshold_for(program_db: float, ratio: float, target_gr_db: float) -> float:
    """Threshold that yields `target_gr_db` of gain reduction at `program_db`,
    inverting the compressor's own static curve above the knee."""
    return program_db - target_gr_db / (1.0 - 1.0 / ratio)


def analyse(x, fs):
    """Everything a preset needs measured off the stem itself, in one pass.

    Use this instead of the builders' defaults for any real material: the
    defaults are a dry-vocal fallback, and a wrong one biases every derived
    threshold (see NOMINAL_PROGRAM_DB). The de-esser crossover and its
    threshold MUST come from the same frequency, or the sidechain measures a
    different band than the gain stage acts on.
    """
    freq = sibilance_freq_hz(x, fs)
    return dict(program_db=program_level_db(x, fs),
                sibilance_db=sibilance_level_db(x, fs, freq_hz=freq),
                deess_freq_hz=freq)


def build_eminem_chain(fs: float, program_db: float = NOMINAL_PROGRAM_DB,
                       sibilance_db: float = NOMINAL_SIBILANCE_DB,
                       deess_freq_hz: float = DEESS_FREQ_HZ) -> Chain:
    """Eminem / Dr. Dre chain (Sony C800G -> Neve 1073 -> dbx 160X/SSL 4000G).
    Source: ~/Desktop/vox references/EMINEM-DR-DRE-VOCAL-CHAIN.md (engineer
    Vito/Mauricio Iragorri interview data). Chosen as the first preset: it's
    the only one of the three researched artists with concrete numeric
    settings and no DSP vox doesn't already have (Tupac needs a pitch-shift
    harmonizer; Jay-Z's chain is "minimal comp + manual fader automation",
    not a static preset).

    Mapping notes (qualitative -> numeric, since the source names ranges,
    not exact values):
      - "Attack: Medium" / "Release: Fast" -> 15ms / 50ms, ballpark vocal-comp
        medium/fast.
      - "Ratio 7:1, threshold ~0 dB, catches 3-7 dB on loudest peaks" -> ratio
        is used as-is; the threshold is DERIVED from program level to land 5 dB
        of GR (middle of the documented range). Do not hardcode 0 dBFS here --
        see NOMINAL_PROGRAM_DB for the measurement showing why that is inert.
      - Neve 1073 "harmonic warmth" -> light saturation (2 dB drive, 10% mix),
        not modeled as EQ since 1073 coloration is subtly harmonic, not tonal.
      - AMS RMX16 "Chamber" -> a short, dark-ish room at a low send level:
        "spatial depth", not audible wash.
        CORRECTED 2026-08-20 (owner's ear: "too much reverb on the eminem one").
        The original settings were room_size=0.35, damping=0.2, mix=0.12, on
        the reasoning that low damping = "bright". Measured, that is a
        misreading of what the knob does:
          damping 0.2 -> 0.9 moves the tail LENGTH by 0.03 s (0.56 -> 0.53 s),
          but its HF TILT by 6.4 dB (+9.5 -> +3.1 dB, 4-16 kHz over 200-1k).
        So damping is a brightness control, not a decay control, and 0.2 gave
        a tail tilted +9.5 dB toward HF -- a splashy wash sitting directly on
        the sibilance band, on top of a 0.84 s decay from room_size=0.35.
        Now 0.59 s and +5.9 dB tilt, at a lower send.
    Not implemented: the "mono reference rule" -- that's a mix-bus QA habit
    (check the full mix in mono), not a per-vocal-stem chain effect.

    `program_db`: measure it with program_level_db(x, fs) for a stem that
    isn't at typical level; the default suits a normal vocal bounce.
    """
    modules = [
        dsp.Gate(fs, open_db=-42.0, close_db=-48.0, ratio=6.0,
                 attack_s=0.001, release_s=0.12),
        dsp.DeEsser(fs, freq_hz=deess_freq_hz,
                    threshold_db=_threshold_for(sibilance_db, DEESS_RATIO,
                                                DEESS_TARGET_GR_DB),
                    ratio=DEESS_RATIO, range_db=10.0, mix=1.0),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="highpass", freq=80.0, q=0.707),
        ]),
        dsp.Compressor(fs, threshold_db=_threshold_for(program_db, 7.0, 5.0),
                       ratio=7.0, knee_db=2.0,
                       attack_s=0.015, release_s=0.05, makeup_db=4.0, mix=1.0),
        dsp.Saturation(fs, drive_db=2.0, mix=0.10, mode="tanh", oversample=8),
    ]
    if getattr(dsp, "_HAS_PEDALBOARD", False):
        modules.append(dsp.ReverbSend(fs, room_size=0.15, damping=0.6, mix=0.07))
    modules.append(dsp.Limiter(fs, ceiling_dbtp=-1.0, lookahead_ms=5.0, release_s=0.08))
    return Chain(fs, modules)


def build_jayz_chain(fs: float, program_db: float = NOMINAL_PROGRAM_DB,
                     sibilance_db: float = NOMINAL_SIBILANCE_DB,
                     deess_freq_hz: float = DEESS_FREQ_HZ) -> Chain:
    """Jay-Z / Young Guru chain (Neumann/AKG -> Neve 1073 -> Tube-Tech CL1B,
    Mercer Hotel era). Source: INTERVIEWS-ANALYSIS-2026-08-15.md (transcribed
    interview) + JAYZ-YOUNG-GURU-VOCAL-CHAIN.md (web research, 3-era timeline).

    Unlike Eminem's chain, no era gives exact comp numbers -- no ratio,
    threshold, or attack/release for CL1B or the "99 Problems" 1176 (see
    INTERVIEWS-ANALYSIS's own "Known Gaps" section). What's documented
    instead is a PHILOSOPHY, applied here as numbers:
      - "Anti-compression": very minimal comp, rides the fader instead of
        limiting -> low ratio (2.5:1) and a threshold derived for only 2 dB
        of GR at program level -- deliberately less than half the 5 dB the
        Eminem chain targets, so the difference is audible, not nominal.
      - CL1B character: "musical, smooth leveling; glues fast cadences
        without pumping/clamping" -> medium attack, medium release, no
        fast/aggressive settings.
      - "Subtractive EQ first... does NOT scoop mid-range" -> cut mud/
        harshness only, no shelf boost (contrast with Eminem/base chain's
        default air-shelf, deliberately omitted here).
      - Minimal gain-stage coloration ("transparency over character") ->
        no saturation stage at all.
    Not implemented: the "non-linear reverb" on aux 1 (Interview 2, cut off
    mid-sentence, type never specified). pedalboard's algorithmic FDN
    reverb is the wrong topology to approximate an unspecified non-linear
    (likely gated) reverb -- guessing would be worse than leaving it out.
    """
    modules = [
        dsp.Gate(fs, open_db=-42.0, close_db=-48.0, ratio=6.0,
                 attack_s=0.001, release_s=0.12),
        dsp.DeEsser(fs, freq_hz=deess_freq_hz,
                    threshold_db=_threshold_for(sibilance_db, DEESS_RATIO,
                                                DEESS_TARGET_GR_DB),
                    ratio=DEESS_RATIO, range_db=10.0, mix=1.0),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="highpass", freq=80.0, q=0.707),
            dict(kind="bell", freq=350.0, gain_db=-2.0, q=1.2),   # mud, not mid body
            dict(kind="bell", freq=3000.0, gain_db=-1.5, q=1.3),  # harshness, not presence
        ]),
        dsp.Compressor(fs, threshold_db=_threshold_for(program_db, 2.5, 2.0),
                       ratio=2.5, knee_db=6.0,
                       attack_s=0.010, release_s=0.15, makeup_db=2.0, mix=1.0),
        dsp.Limiter(fs, ceiling_dbtp=-1.0, lookahead_ms=5.0, release_s=0.08),
    ]
    return Chain(fs, modules)


def build_tupac_chain(fs: float, program_db: float = NOMINAL_PROGRAM_DB,
                      sibilance_db: float = NOMINAL_SIBILANCE_DB,
                     deess_freq_hz: float = DEESS_FREQ_HZ) -> Chain:
    """Tupac / Death Row chain (Neumann U87 -> Neve or SSL 4000 preamp + its
    console compressor -> Studer A800 tape), plus the printed harmonizer
    stack. Sources: docs/07_REFERENCE_VOCALS.md section 3 (tracking chain,
    "One-Take Tupac", least processed of the three) and
    ~/Desktop/vox references/TUPAC-VOCAL-STACKING-TECHNIQUE.md (the doubling).

    The two sources describe different halves of the same record and both are
    in here, per the owner's call: the tracking chain is the tone, the stack
    is the thickness people actually recognise.

      - Console compressor, not a dedicated box: soft knee (8 dB), low ratio,
        slower release, only ~3 dB of GR -- between Jay-Z's 2 and Eminem's 5.
        Threshold derived from program level, never copied off a faceplate
        (see NOMINAL_PROGRAM_DB).
      - Studer A800 tape: more saturation than Eminem's Neve warmth (4 dB
        drive / 20% vs 2 dB / 10%) plus a gentle high-shelf CUT for tape's
        high-end loss. Doc's warning taken literally: take processing away,
        then add tape -- so no presence boost, no reverb send.
      - Stack: +12c/25ms left, -12c/10ms right, dry centre, and the 350 Hz
        cut both sources call for to keep three overlapping takes out of mud.
        On at mix=0.35; it is printed on the record, not a send.
    Not implemented: the room. Doc says "console comp + tape + room" but never
    says which room, and pedalboard's FDN would be a guess.
    """
    modules = [
        dsp.Gate(fs, open_db=-42.0, close_db=-48.0, ratio=6.0,
                 attack_s=0.001, release_s=0.12),
        dsp.DeEsser(fs, freq_hz=deess_freq_hz,
                    threshold_db=_threshold_for(sibilance_db, DEESS_RATIO,
                                                DEESS_TARGET_GR_DB),
                    ratio=DEESS_RATIO, range_db=10.0, mix=1.0),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="highpass", freq=80.0, q=0.707),
            dict(kind="bell", freq=350.0, gain_db=-2.5, q=1.2),   # stack mud
        ]),
        dsp.Compressor(fs, threshold_db=_threshold_for(program_db, 3.0, 3.0),
                       ratio=3.0, knee_db=8.0,
                       attack_s=0.012, release_s=0.20, makeup_db=3.0, mix=1.0),
        dsp.Stack(fs, cents=12.0, delay_l_s=0.025, delay_r_s=0.010, mix=0.35),
        dsp.Saturation(fs, drive_db=4.0, mix=0.20, mode="tanh", oversample=8),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="high_shelf", freq=10000.0, gain_db=-1.5, q=0.707),  # tape HF loss
        ]),
        dsp.Limiter(fs, ceiling_dbtp=-1.0, lookahead_ms=5.0, release_s=0.08),
    ]
    return Chain(fs, modules)


PRESETS = {
    "eminem": build_eminem_chain,
    "jayz": build_jayz_chain,
    "tupac": build_tupac_chain,
}
