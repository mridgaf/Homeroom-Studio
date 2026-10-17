# Chapter 06: Vocal processing research
## Part 2 of 3

_The AI vocal processor research: spec, findings from real stems, reference vocals, handoff._

**In this part:**
- 05_FINDINGS.md — Measured findings so far (not opinions — every number below has a test behind it)
- 06_REAL_STEM_FINDINGS.md — Real-stem findings (delo mirror 18 13 26.wav)

(Next: Part 3 of 3)


=====================================================
SOURCE FILE: 05_FINDINGS.md
ORIGINAL LOCATION: WT:vox/docs/05_FINDINGS.md
=====================================================

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

=====================================================
SOURCE FILE: 06_REAL_STEM_FINDINGS.md
ORIGINAL LOCATION: WT:vox/docs/06_REAL_STEM_FINDINGS.md
=====================================================

# Real-stem findings (delo mirror 18 13 26.wav)

First real material tested (synthetic test bench findings are in
`05_FINDINGS.md`; everything below is from an actual vocal take, 44.1 kHz
stereo, dual-mono, ~3:54, −17.9 LUFS raw, no clipping).

## User-reported: processed output sounded muffled
Isolation tests (drive each stage with a pure dry sustained tone that has
*zero* reverb and *is* clearly voice-like energy — a fair stand-in for a held
vowel) confirmed two real, serious bugs:

- **De-reverb** (`dsp/dereverb.py`): a dry sustained tone with NO reverb
  dropped **~20 dB**. Root cause: the algorithm models "late reverberant
  energy" as anything whose STFT-bin energy persists past a fixed number of
  frames (`direct_frames`). It cannot distinguish "this is a decaying reverb
  tail" from "this is a note being held" — both look identical to a
  frame-persistence detector. On real sung/spoken vocal with sustained
  vowels, this guts exactly the content that should survive.
  **Consequence: OFF by default now** (`chain_demo.run_full_pipeline`,
  `dereverb=False`). This needs a redesign, not a parameter tweak — see
  "What would actually fix this" below.
- **ML denoise** (DeepFilterNet3): the same dry tone dropped **18.5-21.5 dB** at
  full wet. It's a speech/VoIP model; a pure sustained tone doesn't match
  its learned speech manifold, so it's suppressed as non-speech. On real
  singing (sustained vowels, vibrato, held notes) this is the same failure
  shape as de-reverb, for a different reason. **Consequence: OFF by default
  now** (`denoise_blend=0.0`).

Both stages were engaged (dereverb full-strength, denoise at 0.35 blend) on
the first real-stem test and stacked — confirmed via band-energy
measurement to cut 300 Hz–8 kHz by 2–7 dB compared to raw, which is what
read as "muffled." Re-rendered with both disabled, DSP-chain-only
(gate → de-ess → EQ → compressor → saturation → limiter): −3.5 to +4 dB
band deltas, no destructive cuts. That corrected file is what the user
confirmed sounded right.

### What would actually fix de-reverb (for whoever picks this up)
The frame-persistence model is the wrong tool. Options, roughly in order of
effort:
1. **Coherence/onset-gated suppression**: only start subtracting "late
   energy" after a detected onset, and re-arm on the next onset — so a note
   that's simply held past `direct_frames` isn't treated as decaying.
2. **Externally-supplied RT60**, measured once from actual room tone (silence
   between phrases, which this file has plenty of) rather than blind
   full-clip estimation — blind estimation was independently confirmed
   unreliable on both the synthetic bench (guessed 2.9 s vs true 0.45 s) and
   this real file (guessed ~3.0 s, clamped at the estimator's own ceiling).
3. A proper direct/reverberant split via a decay-rate-consistency check per
   bin (does this bin's energy trajectory actually match an exponential
   decay from the last onset, vs. staying roughly flat like sustained
   voicing) before subtracting anything.

### What would actually fix the denoiser
Not a bug to "fix" so much as a scope mismatch: DeepFilterNet3 is trained on
speech, not singing. Either (a) keep it strictly for the noise-floor-only
regions (gate it to engage only where a VAD says there's no vocal, e.g.
between phrases), or (b) find/train a model on sung material, or (c) accept
it as an optional, clearly-labeled "aggressive" mode the user engages
per-source and A/Bs themselves, not a default.

## pedalboard evaluation (user asked to check the "Homeroom" sound_engine code)
`reason_voice/` (voice control for the Reason DAW) is unrelated — no audio
DSP, not applicable here. `sound_engine/` + `tools/audio_engine.py` wrap
`pedalboard` (Spotify's JUCE-adjacent audio library) and are genuinely
relevant. Installed and measured it with the same rigor as our own modules:

- **`pedalboard.Limiter`: do not use.** Same true-peak test that caught our
  own limiter bug: swept 5 frequencies × 3 phases, worst-case overshoot
  **+4.1 dB** past its own ceiling (ours, after the fix, is 0 dB over the
  same sweep). It's a sample-peak limiter; it does not see inter-sample
  peaks at all. Their own `audio_engine.py` docstring already documents a
  different real issue with it (unwanted makeup gain under threshold) —
  good sign that whoever built it was verifying things too — but hadn't
  caught this one.
- **`pedalboard.Distortion`: do not use.** −19.4 dB alias floor, nowhere
  close to our −90 dB bar. Not oversampled.
- **`pedalboard.Reverb`: usable, with a catch.** Does NOT null cleanly at
  `wet=0, dry=1` (−6.6 dB against silence) — its "dry" path is not a
  transparent bypass. Fixed by never using its internal dry/wet: our
  `ReverbSend` module takes a 100%-wet tap and mixes it against our own
  untouched input externally. Verified null at our own `mix=0`: −400 dB.
- **`pedalboard.Chorus` / `pedalboard.Phaser`: usable directly.** Both null
  cleanly at their own internal `mix=0` (−156 dB, float32-precision-limited,
  not a real defect). Wrapped as `Dimension`.
- Note: the −90 dB aliasing bar does not meaningfully apply to modulation
  effects (chorus/phaser/reverb) — they're linear/time-varying, and
  deliberately spread energy around the fundamental via modulation (that's
  what chorus *is*). Measuring them with the harmonic-distortion aliasing
  test produces numbers that look alarming (chorus showed "+6.5 dB alias")
  but that's expected modulation sidebands, not digital aliasing. The bar
  stays enforced on `Saturation`, where it's the right test.

**Decision:** keep every hand-rolled, already-verified module (Gate,
DeEsser, ParametricEQ, Compressor, Saturation, Limiter) exactly as is — they
already passed adversarial-grade verification and pedalboard's equivalents
don't clearly beat them (the limiter is worse). Added `ReverbSend` and
`Dimension` (pedalboard-backed) to fill in the two modules we hadn't built
yet, both wired into the default chain but **mix=0 (inert) by default** —
available, verified, not forced on.

**Scope honesty**: pedalboard is Python-only and cannot ship inside the
eventual JUCE/C++ plugin. These two modules are a Phase-1 stand-in to prove
the product's reverb/modulation quality now; Phase 2 needs a native
reimplementation (most plausibly directly against `juce::dsp`, which is
plausibly what pedalboard itself wraps for these effects, though that
internal detail isn't independently confirmed here — verify before
assuming bit-for-bit equivalence).

---

## 2026-08-14 — de-reverb FIXED and re-verified on this same file

The frame-persistence bug above is fixed. `suppress_late_reverb` now gates
every bin's subtraction by whether that bin's energy is actually **decaying**:

    w = clip(measured_decay_slope / expected_reverb_slope, 0, 1)

Sustained content has slope ~0, so w ~0 and nothing is subtracted from it.
A genuine tail decays at (or faster than) the modeled reverb rate, so w -> 1
and the full Habets estimate is subtracted. The slope is measured on a
**smoothed log envelope** — the first attempt used a linear frame-to-frame
ratio, which measured 0.25..13.5 *inside a real decaying tail* (bin
magnitudes are stochastic; their arithmetic mean is meaningless). Log-domain
averaging is the part that makes this work at all.

### Measured on the same 20 s segment (2:56–3:16) of `delo mirror 18 13 26.wav`

| Band (Hz) | OLD (broken) | NEW (fixed) |
|---|---|---|
| 80–300 | −1.09 dB | **−0.33 dB** |
| 300–1000 | **−3.65 dB** | **−0.84 dB** |
| 1000–3000 | −2.61 dB | −0.49 dB |
| 3000–8000 | −2.11 dB | −0.34 dB |
| 8000–16000 | −2.01 dB | −0.38 dB |
| Overall RMS | −2.85 dB | −0.58 dB |

The OLD column reproduces the original "muffled" complaint exactly — it sits
inside the 2–7 dB, 300 Hz–8 kHz destructive cut documented above. The NEW
column is 3–6× smaller in every band. Mean decay weight on this file is
**0.464**, i.e. the gate is genuinely engaging, not passing everything
through untouched (there is a test asserting exactly that,
`test_decay_gate_separates_sustained_from_reverberant`).

### The honest trade — read this before re-enabling it by default
The old version scored a uniform ~18 dB tail-RMS drop on the synthetic bench
**because it floored every bin indiscriminately**, including the ones
carrying the vocal. The fixed version is selective, so tail suppression is
now condition-dependent: across a seed × RT60 sweep it ranged **3.9 to 18 dB**
(weakest at RT60 1.2 s, where 0.15 s of "tail" is still mid-decay). The
SNR-vs-dry-reference proxy, which is the metric that actually tracks quality,
improved consistently: **+1.0 to +2.9 dB in every one of the nine conditions.**

Less tail suppression, far less collateral damage. That is the right trade
and it should not be tuned back.

**Still not done:** this is a measurement, not a listening test. Nobody has
yet A/B'd the fixed version by ear on real material, and `chain_demo.py`
still defaults `dereverb=False`. Do not flip that default on these numbers
alone — that is precisely the mistake documented at the top of this file.

=== END OF PART ===
