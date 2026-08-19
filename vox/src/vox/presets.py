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
# the 99th percentile of the compressor's own detector envelope. Both
# reference acapellas land within ~1 dB of this.
#
# WHY THIS EXISTS: the research docs quote HARDWARE thresholds ("~0 dB", i.e.
# near 0 VU on a desk running +4 dBu nominal). Setting a digital compressor's
# threshold to 0 dBFS from that number makes it completely inert -- measured
# on `eminem lose vocal.wav`, a 0 dBFS threshold engaged on 0.0% of the file,
# because the detector never gets above -12.4 dB. Thresholds below are
# therefore derived from program level, the way the engineer set them by ear,
# not copied from the hardware faceplate.
NOMINAL_PROGRAM_DB = -14.0


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


def _threshold_for(program_db: float, ratio: float, target_gr_db: float) -> float:
    """Threshold that yields `target_gr_db` of gain reduction at `program_db`,
    inverting the compressor's own static curve above the knee."""
    return program_db - target_gr_db / (1.0 - 1.0 / ratio)


def build_eminem_chain(fs: float, program_db: float = NOMINAL_PROGRAM_DB) -> Chain:
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
      - AMS RMX16 "Chamber" -> small, bright room (low room_size, low damping)
        at a low send level -- "spatial depth", not audible wash.
    Not implemented: the "mono reference rule" -- that's a mix-bus QA habit
    (check the full mix in mono), not a per-vocal-stem chain effect.

    `program_db`: measure it with program_level_db(x, fs) for a stem that
    isn't at typical level; the default suits a normal vocal bounce.
    """
    modules = [
        dsp.Gate(fs, open_db=-42.0, close_db=-48.0, ratio=6.0,
                 attack_s=0.001, release_s=0.12),
        dsp.DeEsser(fs, freq_hz=7000.0, threshold_db=-22.0, ratio=4.0,
                    range_db=10.0, mix=1.0),
        dsp.ParametricEQ(fs, bands=[
            dict(kind="highpass", freq=80.0, q=0.707),
        ]),
        dsp.Compressor(fs, threshold_db=_threshold_for(program_db, 7.0, 5.0),
                       ratio=7.0, knee_db=2.0,
                       attack_s=0.015, release_s=0.05, makeup_db=4.0, mix=1.0),
        dsp.Saturation(fs, drive_db=2.0, mix=0.10, mode="tanh", oversample=8),
    ]
    if getattr(dsp, "_HAS_PEDALBOARD", False):
        modules.append(dsp.ReverbSend(fs, room_size=0.35, damping=0.2, mix=0.12))
    modules.append(dsp.Limiter(fs, ceiling_dbtp=-1.0, lookahead_ms=5.0, release_s=0.08))
    return Chain(fs, modules)


def build_jayz_chain(fs: float, program_db: float = NOMINAL_PROGRAM_DB) -> Chain:
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
        dsp.DeEsser(fs, freq_hz=7000.0, threshold_db=-22.0, ratio=4.0,
                    range_db=10.0, mix=1.0),
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


def build_tupac_chain(fs: float, program_db: float = NOMINAL_PROGRAM_DB) -> Chain:
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
        dsp.DeEsser(fs, freq_hz=7000.0, threshold_db=-22.0, ratio=4.0,
                    range_db=10.0, mix=1.0),
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
