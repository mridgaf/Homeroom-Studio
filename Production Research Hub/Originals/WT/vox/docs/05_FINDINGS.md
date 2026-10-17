# Measured findings so far (not opinions — every number below has a test behind it)

## Meter (vox/meter.py) — validated against published standards
- BS.1770-4 integrated loudness reproduces the EBU Tech 3341 conformance
  case (stereo 1 kHz sine at N dBFS → N LUFS) to within 0.01 dB, at
  44.1/48/96/192 kHz.
- K-weighting: +4.04 dB HF shelf, −6.0 dB at the 38 Hz RLB corner — matches
  the published response shape.
- True-peak: **CORRECTED 2026-08-19, see "True-peak accuracy re-measured"
  below.** The original entry here confirmed the 4x meter against a single
  12 kHz tone and called the 0.15 dB error "a documented, known limitation".
  It is a limitation, but the bar in `00_BAR.md` is ±0.1 dBTP, so recording it
  as known was accepting a documented failure of our own spec. Worst case is
  also far larger than one tone suggested: −0.464 dB. The meter default is now
  16x, and the limiter matches at 16x.
- Null test resolves a single 24-bit LSB of difference at −138.5 dB, as
  expected from `20*log10(2^-23)`.

## Aliasing — the bar's −90 dBFS requirement is not automatically met
Measured with a non-commensurate test tone (see `meter.aliasing_floor_db`
docstring for why a naive integer-ratio test tone would hide aliasing):

| Saturation config              | Alias floor | vs. −90 dB bar |
|---------------------------------|------------:|:---------------|
| tanh, no oversampling            | −19.3 dB    | FAIL, badly     |
| tanh, 4× oversampled             | −81.6 dB    | **FAIL**        |
| tanh, 8× oversampled             | −117.4 dB   | PASS            |
| hard clip, 16× oversampled       | −69.6 dB    | **FAIL**        |
| hard clip, ADAA (1st-order), 8×  | −91.9 dB    | PASS            |

Conclusion baked into the product spec: soft nonlinearities need ≥8×
oversampling; hard-knee clippers cannot be fixed by oversampling alone and
require antiderivative anti-aliasing (ADAA).

## Limiter — two real bugs found and fixed during verification, not before
1. **Sample-peak detection instead of true-peak.** First working version
   measured 0.4–2.3 dB over its own ceiling on high-frequency material,
   because it looked at raw sample magnitude, missing inter-sample peaks.
2. **Rectify-before-interpolate.** The fix for (1) still overshot by up to
   2.3 dB at 12 kHz. Root cause: the detector took `abs()` of the signal
   *before* upsampling. Rectifying a sine creates a kink at every
   zero-crossing that was never in the original band-limited signal: the
   interpolator then faithfully reconstructs that fabricated high-frequency
   content and under-estimates the true peak. Fixed by interpolating the
   signed waveform per channel and rectifying only after filtering — the
   same order of operations `meter.true_peak_db` already used.

After both fixes: swept 12 frequencies (200 Hz–20.5 kHz) × 4 phases × a
12 kHz worst case → **0 dB worst-case overshoot**, and the limiter's own
detector matches the reference meter to within 0.003 dB
(`test_limiter_detector_matches_reference_meter`).

**That second clause was never evidence of anything** (corrected 2026-08-19).
`meter.true_peak_db` is not an independent implementation of the detector:
both are `firwin(48*OS+1, 1/OS, kaiser)` zero-stuffed interpolation, same
window, same tap count. Agreement between them can only catch one drifting
from the other, never an error they share — and they did share one. See below.

## True-peak accuracy re-measured (2026-08-19)

Graded against `scipy.signal.resample_poly`, a genuinely different algorithm,
over 11 frequencies × 32 phases:

| meter oversampling | worst error | vs the ±0.1 dBTP bar |
|---|---|---|
| 4x (the old default) | −0.464 dB | fails |
| 8x | −0.139 dB | fails |
| 16x (current) | −0.059 dB | meets it |

The errors cluster at **exact submultiples of fs** — 19200 = fs/2.5,
16000 = fs/3, 12000 = fs/4 — where the interpolation grid lands on the same
phases every cycle and can straddle the true peak indefinitely rather than
converging. A single-frequency spot check cannot see this, which is exactly
why the original 12 kHz check did not.

`meter.true_peak_db` now defaults to 16x and `Limiter.OS` is 16 to match: a
limiter detecting at a lower rate than the meter grades at is targeting a
number the meter will refuse to confirm. On real material — both reference
acapellas driven 12 dB into the limiter — worst overshoot is +0.050 dB.

**Measurement trap, recorded so it isn't re-stepped-in:** every interpolating
true-peak method rings at a signal boundary. Slicing a tone out of the middle
of a buffer, or reading the edges of a resampled one, reads several *tenths of
a dB high*. An adversarial review of this project reported a 0.40 dB limiter
overshoot that was entirely this artifact; the same mistake was then
reproduced and caught while verifying that claim. Fade the test signal
(`_faded()` in `tests/test_dsp.py`), do not slice it.

## De-reverb (vox/dsp/dereverb.py) — real, but with an honest limitation
- Built from Habets (2007) / Lebart-Boucher-Denbigh (2001) causal statistical
  late-reverb suppression, after `nara_wpe` was tried and found to need
  multiple microphones (it did nothing on a single-channel stem: −77.5 →
  −77.8 dB tail energy).
- On the synthetic test bench: reverb-tail energy in the post-phrase silence
  drops from −75.1 dBFS to −93.7 dBFS (≈18.6 dB reduction).
- **Caveat found during this session's verification, not previously
  documented:** blind per-band RT60 estimation on a short (3.3 s) clip is
  unreliable — it estimated ~2.9 s against a ground-truth 0.45 s room.
  Despite the wrong estimate, tail suppression and vocal-region SDR were
  *not* worse than using the correct RT60 (in fact marginally better on this
  synthetic signal), which is itself a mild red flag that the vocal-region
  SDR metric isn't very sensitive here — more validation on a real stem is
  needed before trusting this module's default blind-estimation mode.
  Recommendation for the product: let a longer capture (or a dedicated
  room-tone snippet) drive the RT60 estimate rather than a short vocal take.

## Denoise (vox/engines/denoise_dfn.py) — real pretrained model, real caveats
- DeepFilterNet3 (MIT/Apache-2.0, pretrained weights, ~16 MB, CPU-capable).
- Measured on the synthetic test bench: −75.1 dBFS → −100.0 dBFS noise floor
  in the silent region, a ~25 dB reduction.
- Ships as an operator-controlled dry/wet blend (default 0.35), not forced
  full-strength, because it's a speech/VoIP-trained model and its behavior
  on sustained sung vowels and vibrato has not yet been validated against a
  real vocal performance.

## What still needs a real vocal stem
Every number above comes from the synthetic test bench (`vox/testsignal.py`)
because it has known ground truth. The synthetic voice is a source-filter
model, not a real larynx — it is good for proving DSP correctness and
catching bugs like the two above, but the denoise and de-reverb *quality*
numbers should be treated as provisional until validated on real material.

## Calibrated on the wrong source (2026-08-20)

The reference acapellas are commercial releases. They were used as if they
were clean vocal stems, so several constants were calibrated on material that
already carried a full production chain. Measured against a dry vocal
(`debbie8 13 26 vc loop reason.wav`):

| what | dry vocal | eminem acap | tupac acap |
|---|---|---|---|
| program level (99th pct) | **-18.3 dB** | -14.1 | -16.4 |
| sibilance level | **-17.0 dB** | -19.3 | -25.1 |
| crest | **15.30 dB** | 13.53 | 14.09 |
| energy above 10 kHz | **3.06%** | 0.92% | 0.79% |
| ess band lower edge | **7192 Hz** | 5340 | 5814 |

Consequences, and what changed:

1. **`NOMINAL_PROGRAM_DB` was -14.0**, justified as "both reference acapellas
   land within ~1 dB of this". A dry vocal is 4.3 dB quieter, because the
   acapellas are compressed and mastered. Every threshold derived from the
   default was ~4 dB high, biasing the chain toward doing less than it claims.
   Now -18.3.

2. **The de-esser crossover was moved 7000 -> 5500 Hz** on the finding that
   "63% of ess energy on the Eminem reference sits below 7 kHz". That reference
   has already been de-essed: its energy above 10 kHz is a third of a dry
   vocal's. Prior processing had scooped the top of its own ess band, dragging
   the apparent distribution down -- the number described its mastering, not
   sibilance. On dry material the ess band starts at ~7.2 kHz, so 5500 sat
   ~1.7 kHz low and reached into presence and consonants.
   The crossover is now DERIVED per stem (`presets.sibilance_freq_hz`), the
   same two-pass pattern the thresholds already used. The constant is a
   fallback only.

3. **The gate's -42/-48 dB thresholds have never been validated on material
   with a real noise floor.** Neither source has one, in opposite ways: the dry
   vocal's gaps are digital silence (p10 = -120 dB, already edited), while the
   Tupac acapella's "floor" is -35 dB of printed reverb tail, which holds the
   gate open 99.7% of the time. Open -- needs a stem with actual room tone.

4. **`tools/ab_reference.py` graded our de-esser against T-De-Esser on the
   acapella**, i.e. on a signal missing the thing both exist to remove. Marked
   as a sanity check, not a calibration source. Its grading band was also still
   7-16 kHz, the band finding 2 proved wrong; now 4.5-12 kHz.

**Why the adversarial passes missed all of this.** Both passes graded the code
against the tests, and the tests against the DSP. Neither asked what the input
material was. A reviewer told "find flaws in this code" checks the code; the
error lived one level up, in what the numbers were measured on. Provenance of
calibration data is now part of the review checklist.
