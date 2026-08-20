"""
DeepFilterNet3 wrapper (MIT/Apache-2.0, pretrained weights included).

MEASURED, not assumed (see /tmp session notes, to be folded into
docs/05_findings.md): on a 48 kHz synthetic vocal, DFN cuts the noise floor
in silent passages by ~36 dB. On the same synthetic signal it does NOT show a
clear full-signal SNR win, likely because DFN is trained on real human speech
statistics and this project's LF-pulse/formant synthesis isn't a great match,
and because DFN is a speech/VoIP model, not a singing model -- it may treat
sustained vowels and vibrato as content to smooth over.

CONSEQUENCE FOR THE PRODUCT: this stage ships as an operator-controlled BLEND
(dry/wet), defaulting conservative, not as a forced full-strength stage. It
must be validated again on a real vocal stem before the default blend amount
is finalized.

Runs entirely offline / two-pass in Phase 1 (loads a ~2 s of context-free
model; no whole-file dependency, so it CAN run block-wise for the future
real-time port -- DeepFilterNet's own design targets low-latency streaming).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .. import _torchaudio_shim  # noqa: F401  (must run before `import df`)

_MODEL = None
_STATE = None
_DF_SR = 48000


def _lazy_init():
    global _MODEL, _STATE
    if _MODEL is None:
        import torch  # noqa: F401
        from df.enhance import init_df
        _MODEL, _STATE, _ = init_df()
    return _MODEL, _STATE


@dataclass
class DenoiseResult:
    audio: np.ndarray
    blend: float
    model_sr: int
    latency_ms: float
    vad_duty: float | None = None   # fraction of the take judged "voice present"


def voice_activity_mask(x: np.ndarray, fs: float, threshold_db: float | None = None,
                        margin_db: float = 12.0, min_range_db: float = 15.0,
                        attack_s: float = 0.005, release_s: float = 0.250) -> np.ndarray:
    """1.0 where voice is present, 0.0 where it isn't, smoothly.

    Deliberately asymmetric: fast attack so a phrase onset is protected before
    it arrives, slow release so the tail of a word (and a singer's decay) is
    not chopped. This mask protects content -- when in doubt it should say
    "voice", because a false "voice" costs nothing but a bit of unremoved
    noise, while a false "silence" hands a vocal to a model that was never
    trained on singing.

    threshold_db is derived per take, not hardcoded -- the same rule presets.py
    uses for program level and sibilance, and for the same reason: a fixed
    threshold is inert on material whose level differs from whatever it was
    tuned on.

    The rule has two steps, and the first one matters more than the second:

    1. **Are there any gaps at all?** If the level envelope's dynamic range
       (p90 - p10) is under `min_range_db`, this take has no silence in it --
       a held note, a continuous sustain, a dense stem -- so there is nothing
       to denoise and the mask is all ones. Nothing gets touched.
    2. Otherwise the quiet frames really are noise, so the threshold is
       floor + margin in the classic way.

    Step 1 exists because level alone cannot tell a held note from a noise
    floor. The first version of this function used floor+margin alone, and on
    a signal with no silence the 10th percentile IS the content: the threshold
    landed above the tone, the whole performance read as "silence", and got
    handed to the model to be smoothed away (measured -18.4 dB on a sustained
    440 Hz tone -- gating had changed nothing). A level-relative fallback
    (program - N) does not fix it either: with a noise floor only ~25 dB below
    program, any N that protects the tone also protects the noise.

    "No gaps" therefore means "do nothing", which is the right failure mode --
    a false "voice" costs some unremoved noise, while a false "silence" hands
    a vocal to a model never trained on singing.
    """
    from ..dsp.modules import Detector

    env_db = Detector(fs, mode="rms", rms_window_s=0.020,
                      attack_s=attack_s, release_s=release_s).process(np.asarray(x))
    if threshold_db is None:
        floor_db, program_db = np.percentile(env_db, [10, 90])
        if program_db - floor_db < min_range_db:
            return np.ones_like(env_db)
        threshold_db = float(floor_db) + margin_db
    # soft knee over 6 dB so the mask doesn't switch abruptly
    return np.clip((env_db - threshold_db) / 6.0 + 0.5, 0.0, 1.0)


def denoise(x: np.ndarray, fs: float, blend: float = 0.35,
            vad_gated: bool = True, vad_threshold_db: float | None = None) -> DenoiseResult:
    """
    x: mono float64/32 array at any fs (resampled to the model's native 48k
       internally, then back -- DeepFilterNet3 is trained at 48 kHz only).
    blend: 0..1 dry/wet. With vad_gated=True this is the blend applied in the
           GAPS; voiced passages stay dry regardless.
    vad_gated: only denoise where there is no voice.

    Why gated by default. DeepFilterNet3 is a speech/VoIP model, not a singing
    model, and it measurably suppresses sustained non-speech-like content
    (~59 dB at full wet on a pure tone -- docs/05_FINDINGS.md, and the reason
    this stage shipped OFF). But the thing it is genuinely good at, ~25 dB of
    noise-floor reduction, lives almost entirely in the gaps BETWEEN phrases,
    where by definition there is no vocal to damage.

    So rather than trying to make a speech model safe for singing -- a
    research problem -- this restricts it to the part of the take where the
    distinction does not arise. It is the lowest-risk option in HANDOFF.md's
    list for exactly that reason: it sidesteps the problem instead of solving
    it. The cost is that noise UNDER a sustained note is left alone, which is
    the correct trade: that noise is masked by the note anyway.
    """
    import torch
    from scipy.signal import resample_poly
    from df.enhance import enhance

    x = np.asarray(x, dtype=np.float64)

    if vad_gated:
        # Computed on the INPUT, before any resampling, so that a take with no
        # gaps can return untouched rather than merely unprocessed: a 44.1k
        # source would otherwise still eat a 44.1->48->44.1 round trip
        # (measured 5.4e-03 of error) for a stage that was going to be a no-op.
        # Also skips loading the model entirely on such takes.
        mask_in = voice_activity_mask(x, fs, threshold_db=vad_threshold_db)
        if float(np.min(mask_in)) >= 1.0:
            return DenoiseResult(audio=x.copy(), blend=blend, model_sr=_DF_SR,
                                 latency_ms=40.0, vad_duty=1.0)

    model, state = _lazy_init()
    if fs != _DF_SR:
        from math import gcd
        g = gcd(int(fs), _DF_SR)
        xin = resample_poly(x, _DF_SR // g, int(fs) // g)
    else:
        xin = x

    audio = torch.from_numpy(xin).float().unsqueeze(0)
    enhanced = enhance(model, state, audio).squeeze(0).numpy()

    n = min(len(xin), len(enhanced))
    wet = enhanced[:n]
    dry = xin[:n]
    duty = None
    if vad_gated:
        mask = voice_activity_mask(dry, _DF_SR, threshold_db=vad_threshold_db)
        duty = float(np.mean(mask))
        # blend only where the mask says "no voice"
        eff = blend * (1.0 - mask)
        mixed = dry + eff * (wet - dry)
    else:
        mixed = blend * wet + (1.0 - blend) * dry

    if fs != _DF_SR:
        g = gcd(int(fs), _DF_SR)
        mixed = resample_poly(mixed, int(fs) // g, _DF_SR // g)
        mixed = mixed[: len(x)] if len(mixed) >= len(x) else np.pad(mixed, (0, len(x) - len(mixed)))

    # DeepFilterNet3 processes in ~10ms frames with lookahead; reported model
    # latency per its own docs is ~40ms algorithmic. We surface that number
    # rather than measure it per-call (measuring would require a click track).
    return DenoiseResult(audio=mixed, blend=blend, model_sr=_DF_SR, latency_ms=40.0,
                         vad_duty=duty)
