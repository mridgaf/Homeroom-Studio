# Chapter 01: How producers and engineers work
## Part 6 of 9

_What working producers and engineers actually do, who to study, and the forum/community knowledge. Includes the vox producer + engineer interviews and the "expert mode" master prompt._

**In this part:**
- round1_engineer.md (piece 2 of 2) — ROUND 1 — DSP + ML ARCHITECTURE SPECIFICATION

(Next: Part 7 of 9)


=====================================================
SOURCE FILE: round1_engineer.md (piece 2 of 2)
ORIGINAL LOCATION: WT:vox/docs/design_process/round1_engineer.md
=====================================================

### 4.12 Saturation / harmonic excitation

**Curves:**
- `tanh` (odd harmonics), asymmetric-with-DC-bias (2nd harmonic, "tube"), piecewise soft-clip with Chebyshev shaping (explicit control of the h2:h3:h5 ratio), "tape" (static curve + 1st-order hysteresis + HF-loss filter + wow/flutter LFO), "diode/console" (asymmetric with frequency-dependent bias).

**Antialiasing — do it properly.**
- **First-order ADAA** (antiderivative antialiasing; Parker/Zavalishin/Bright, DAFx-16) for memoryless curves:
  `y[n] = (F₁(x[n]) − F₁(x[n−1])) / (x[n] − x[n−1])`, where `F₁` is the antiderivative of the shaper.
  Guard the ill-conditioned branch: when `|x[n] − x[n−1]| < 1e−5`, fall back to `f((x[n]+x[n−1])/2)`. Failing to guard this produces loud clicks on near-DC input — it is the classic ADAA bug.
- ADAA-1 delivers roughly the alias rejection of 2–4× oversampling at ~¼ the cost; ADAA-2 approaches 8–16×. **Recommended operating point: ADAA-1 + 2× oversampling**, which comfortably clears a −70 dBFS alias floor at a fraction of the cost of naïve 8× OS.
- Oversampling filters: **polyphase IIR elliptic half-band cascade** (Valimaki/Niemitalo) for the Live/Tracking tiers (~0.3 ms, non-linear phase, inaudible at 2×); **FIR half-band** (127-tap, 100 dB stopband) for the Mix tier (~1.0 ms, linear phase).
- ADAA introduces a ½-sample delay and a mild HF rolloff (it is an averaging operation) — compensate with a fixed 0.5-sample fractional delay on the dry path and a gentle HF shelf.

**Multiband saturation (why Nectar's saturator disappoints on dense vocals).** Saturating full-band means LF energy intermodulates with HF energy — the product is the "mud" that appears the moment you push drive. Split with a **4th-order Linkwitz–Riley crossover in TPT form** (allpass-complementary, magnitude-flat on sum) at ~300 Hz and ~4 kHz, independent drive/curve per band, then sum. LF gets gentle even-harmonic warmth, mids get the character, HF gets almost nothing.

**Drive normalisation.** Measure RMS into the shaper, normalise to a fixed operating point, apply drive, un-normalise. Drive becomes a pure *timbre* control decoupled from level. Without this, "more drive" also means "louder," and no honest A/B is possible.

**Harmonic excitation (separate from saturation).** Two options:
- *Classic (Aphex-style):* rectify + bandpass 2–6 kHz, add back at 6–18 kHz. Cheap; adds noise-like brightness.
- *Better — harmonic synthesis:* using the bus F0, synthesise partials at `n·F0` above the source's measured HF rolloff (detected as the frequency above which the spectrum falls below the noise floor), with amplitudes following the source's own harmonic decay slope extrapolated. This is real, *pitch-coherent* air rather than a noise boost — it survives a dark microphone in a way that shelving EQ does not.
- **Both are gated by SPP and by de-esser activity** so they never excite sibilance or room noise.

- **Latency: ~0.3 ms (IIR 2× OS) / ~1.0 ms (FIR).**

---

### 4.13 Tonal EQ (static, additive)

- 8 bands, same TPT core. **Two Q laws:** "Digital" (constant-Q) and "Analog" (proportional-Q, where Q narrows with gain — this is why a Neve/API boost sounds musical and a constant-Q boost sounds surgical). Also a Pultec-style low band with simultaneous boost/cut interaction.
- **Matched-Z / magnitude-matched biquads** (Vicanek) as the default for shelves and bells above ~5 kHz. The bilinear transform warps the response toward Nyquist, so a "12 kHz +3 dB shelf" at 44.1 kHz is measurably wrong in essentially every shipping plugin. Matched-Z fixes it. This is a real, measurable, marketable accuracy claim (§8: ±0.1 dB, 20 Hz–20 kHz, at 44.1/48/96/192 k).
- **Assistant-driven auto-EQ — deliberately under-fitted.** Match the measured LTAS to a target curve by **constrained least-squares fit on the ERB-warped log-magnitude error**, but restrict to **≤ 6 bands, Q ≤ 2.5, |gain| ≤ 6 dB**. Over-fitting a 30-band match to a target curve is exactly what makes AI EQ sound strange and phasey — it corrects for the singer's own formants and the mic's character, which are the *identity* of the sound. **Deliberate under-fitting is the improvement.**
- **Latency: 0.**

---

### 4.14 Transient shaper

- **Differential-envelope design (no threshold).** `env_fast` (τ = 1–5 ms) and `env_slow` (τ = 30–150 ms) in dB; `gain_attack = (env_fast − env_slow) × AttackAmount`; a second, longer pair drives the sustain term. Because it is a *difference*, the effect is **level-independent** — it works identically on a whispered verse and a belted chorus, which threshold-based designs do not.
- **3-band option** (LR4 crossovers) so consonant emphasis does not pump the chest register.
- **Voicing-aware gating (nobody does this).** Apply attack emphasis **only** on unvoiced→voiced transitions and on plosive/fricative onsets, from the bus. A naïve transient shaper emphasises *vibrato peaks* — which sounds like a artifact — instead of consonants, which is intelligibility. This one gate turns the module from "sometimes useful" to "always on."
- **Latency: 0 (feedforward) / 2 ms (symmetric, with lookahead).**

---

### 4.15 Gain riding — split into two

**(a) Input normaliser — placed at stage 0.5, before everything.**
- Very slow (τ = 1–3 s), range ±12 dB, target = the calibrated internal reference (−18 LUFS).
- **Gated by SPP** so silence does not cause gain runaway (the classic AGC failure).
- Purpose: make every downstream threshold meaningful and make presets portable. This is the job Nectar's ALM does by sitting first in the chain.

**(b) Output rider — stage 14, "the fader."**
- Target: **LUFS-S** (400 ms K-weighted, BS.1770-4), range ±12 dB, speed 50 ms–2 s.
- **Reference modes:** absolute target, or **relative to an external sidechain** (the mix bus) — the Vocal Rider "music" mode, which is how the feature is actually used.
- **"Tame Noise" equivalent:** upward gain is gated by SPP **and** by the estimated noise floor, so breaths, room tone and headphone bleed are never pushed up. Ours is better than Nectar's because our SPP comes from the denoise model, not an energy threshold — it correctly identifies a *quiet consonant* as speech and a *loud HVAC hum* as not.
- **The differentiator — "ride between phrases, hold within phrases."** Human engineers do not ride continuously; they set a level per phrase. Continuous riding inside a held note is audible as level wobble and is the reason auto-levellers "sound like a compressor." Therefore:
  - Segment the performance at phrase boundaries using onset/offset flux + SPP from the bus.
  - Within a segment: **hold** the gain (slew ≤ 0.5 dB/s).
  - At a boundary: allow a fast move (slew ≤ 12 dB/s), shaped raised-cosine over 60 ms.
  - Global slew ceiling 6 dB/s default.
  This is the single biggest perceptual difference between our rider and Vocal Rider / Nectar Auto-Level, and it costs almost nothing.
- **Automation write-out** of the rider curve as an automatable parameter (and MIDI CC), so the engineer can print and hand-edit it. Table stakes.
- **Latency: 0** (control-rate; consumes the already-delayed analysis rail).

---

### 4.16 True-peak limiter

- **Detection:** true-peak, computed on a **4× oversampled** signal — BS.1770-4 specifies ≥ 4× for TP estimation at 48 kHz; use 8× above 96 kHz or explicitly document the spec's known ~0.5 dB underestimate.
- **Architecture:**
  - **Lookahead** 1.5–10 ms. Over the lookahead window the gain trajectory is a **raised-cosine (Hann-shaped) descent**, not a linear ramp. A linear ramp has derivative discontinuities at both ends; those discontinuities *are* the distortion. A C¹-continuous gain trajectory is the entire difference between a transparent limiter and a crunchy one.
  - **Release:** dual time constant, τ = 50 ms + 500 ms, blended by recent GR (as §4.9).
  - **Optional 3-band release** so a low note's limiting does not duck the vocal's HF.
- **Gain applied at base rate** (the gain signal is band-limited by the shaped attack → no aliasing), **then a final 4×-oversampled ADAA soft clipper** catches residual inter-sample peaks without adding any lookahead. This hybrid (smooth limiter + tiny ISP-safe clipper) is how you hit a true-peak ceiling without audibly limiting.
- Ceiling default **−1.0 dBTP**.
- **Latency: 1.5–10 ms.**

---

### 4.17 Loudness normalisation & metering

- **BS.1770-4 K-weighting**: high-shelf pre-filter + RLB high-pass; mean-square over **400 ms blocks at 75% overlap**; **absolute gate −70 LUFS**, **relative gate −10 LU** for Integrated. Momentary = 400 ms, Short-term = 3 s. **LRA** per EBU Tech 3342.
- "Target loudness" applies a **static output trim** only, computed over the analysed region. Never dynamic — dynamic normalisation after a rider is double-riding and it fights the limiter.
- **Latency: 0.**

---

## 5. Latency budget

| Stage | Mix | Tracking | Live |
|---|---:|---:|---:|
| Input / DC | 0 | 0 | 0 |
| HPF + plosive | 5.0 | 5.0 | 0 |
| Neural clean-up | 40.0 | 20.0 | 10.0 |
| Gate | 3.0 | 3.0 | 1.0 |
| Resonance suppressor | 48.0 | 2.0 | 2.0 |
| Dynamic EQ | 0 | 0 | 0 |
| Comp A (slow) | 0 | 0 | 0 |
| Comp B (fast) | 3.0 | 3.0 | 1.5 |
| De-esser | 3.0 | 3.0 | 1.0 |
| Saturation | 1.0 | 0.3 | 0.3 |
| Tonal EQ | 0 | 0 | 0 |
| Transient | 2.0 | 2.0 | 0 |
| Rider | 0 | 0 | 0 |
| Limiter | 5.0 | 3.0 | 1.5 |
| **TOTAL (ms)** | **110.0** | **41.3** | **17.3** |

**Honest note:** the "Tracking" tier as specified overshoots its 25 ms goal. To hit < 25 ms, Tracking must drop the neural clean-up to the 10 ms configuration and the plosive lookahead to 2 ms → ≈ 26 ms, still marginal. **Realistic tier targets are Live < 18 ms, Tracking < 30 ms, Mix ~110 ms.** Do not publish a 25 ms number we cannot hit.

## 6. CPU budget (48 kHz, 128-sample buffer, reference: 2023-class x86-64 P-core, single instance, stereo)

| Block | Budget (% of one core) | Basis |
|---|---:|---|
| Analysis rail (STFT + F0 + features) | 1.2 | ~100 Hz control rate, one 1024-FFT/10 ms |
| Neural clean-up (DFN-class, ONNX) | **9.0** | RTF 0.19 on 2017 mobile i5 → ~0.07–0.09 on modern core |
| Resonance suppressor (Engine A) | 2.5 | 2048-FFT every 256 samples ≈ 187 FFT/s/ch + LF path |
| Resonance suppressor (Engine B) | 0.4 | 16 TPT SVFs + tracking |
| All SVF filtering (dyn EQ, tonal EQ, de-ess, crossovers) | 0.8 | ~40 SVFs × ~8 flops |
| Dynamics (3 detectors + gain computers) | 0.3 | scalar, control-rate-assisted |
| Saturation (3 bands, ADAA + 2× OS) | 1.2 | |
| Limiter (4× OS TP detect) | 0.9 | |
| **TOTAL, ML ON (Mix)** | **~16 %** | |
| **TOTAL, ML OFF (classic)** | **~5.5 %** | |

**The ML stage is 55–60% of our CPU.** Consequences in §9.7.

Hard requirements: zero audio-thread allocation, zero locks, denormals flushed, **99.9th-percentile block processing time < 50% of the buffer period** (not the mean — the mean is a lie under ONNX thread scheduling).

---

## 7. The AI/ML decision

**Principle: ML decides; DSP executes.** Neural networks are used where the task is *statistical inference from messy real-world signals* (what is noise? what is speech? what would a good engineer set?). Classic DSP is used wherever the task is *exactly specifiable and must be deterministic, sample-accurate, zero-latency, automatable and recallable*.

### 7.1 Decision matrix

| Stage | Verdict | Rationale |
|---|---|---|
| **Denoise** | **ML — required** | Statistical methods (OM-LSA/MMSE-LSA) plateau roughly 0.3–0.5 PESQ below neural on non-stationary noise. Non-stationary noise is *all real-world noise*. No contest. |
| **De-reverb** | **ML — required** (2nd head of the same model) | No single-channel classical method is competitive. WPE needs multichannel to shine. |
| **Speech-presence probability / VAD** | **ML — free** | Byproduct of the denoiser. **Never run a second model for this.** |
| **Source separation** (bleed removal, vocal extraction from a stem) | **ML — offline only** | HTDemucs v4, 9.0 dB SDR, MIT code+weights. But ~7.8 s receptive field, GB-scale RAM, seconds of processing. Ship as a **render-time "Extract Vocal" preprocess**, never in the realtime chain. |
| **Pitch confidence / octave arbitration** | **ML — small, optional** | CREPE-tiny (MIT, ~486 k params) as an arbiter over MPM/NSDF. Not as the primary tracker. |
| **The Assistant** (chain selection, target curve, parameter proposal) | **ML — but tiny, feature-based** | See §7.2. |
| **Compression, EQ, gating, limiting, de-essing, saturation, transient shaping, gain-riding *execution*** | **Classic DSP — no ML** | These need sample-accuracy, zero latency, exact automation, instant recall, and predictable behaviour under parameter change. A "neural compressor" is a research demo with 20 ms of latency, non-recallable state and no automation story. There is no version of this that ships. |
| **Resonance suppression** | **Analysis-driven classic DSP** | The *detector* benefits enormously from the neural F0/SPP bus. The *suppression* must be a deterministic gain field. A learned gain field is unpredictable and un-delta-able. |
| **Voice transformation** ("Backer"-class) | **Do not ship v1** | §7.6. |

### 7.2 The Assistant — build it small

The Assistant should be a **gradient-boosted tree ensemble or a 3-layer MLP over ~120 engineered features**, not an end-to-end audio model.

- **Features:** LTAS in 40 ERB bands (normalised), per-band crest factor, per-band LRA, F0 statistics (median, IQR, vibrato rate/depth), voiced fraction, sibilance ratio distribution, estimated noise floor and its spectrum, DRR estimate, spectral flatness, HF rolloff frequency, transient density, plosive count.
- **Output:** a parameter vector for our own chain (HPF cutoff, denoise/dereverb amounts, suppressor depth/sharpness/weighting nodes, 6 EQ band f/Q/g, two compressors' thresholds/ratios/times, de-ess amount and centre, saturation drive per band, rider target/range).
- **Training data:** pairs of (raw vocal stem, professionally mixed vocal stem). Derive ground-truth parameters by **fitting our own chain to the professional target** (numerical optimisation per pair, offline, allowed to be slow), then supervised-train the feature→parameter map. This is the honest way to build a Vocal Assistant.
- Model size: **~200 kB**, inference **< 1 ms**. It runs once on "Learn," not per block.
- Two macro controls in the UI (mirroring the market's expectation): **Shape** (tone-match amount) and **Intensity** (dynamics amount), both interpolating from "neutral" to "full proposal" so the user has a continuous, understandable dial.

**Critical design rule:** the Assistant proposes a **fully visible, fully editable chain**. Anything it does must be inspectable and reversible in Detailed View. Black-box assistants lose professional users on the second session.

### 7.3 License constraints — stated honestly

| Asset | License | Honest assessment |
|---|---|---|
| **DeepFilterNet (code)** | Dual **MIT or Apache-2.0**, user's choice. No commercial restriction. | Clean. |
| **DeepFilterNet (pretrained weights)** | **The README does not separately state weight licensing.** | **Do not assume the code license covers the weights.** This is a legal-review item before ship, not an engineering assumption. Flag it now. |
| **RNNoise** | **BSD-3-Clause** (Xiph) | The cleanest license in the field. ~85 k params, far weaker than DFN. Good honest fallback for the Live tier. |
| **Demucs / HTDemucs** | Code and weights **MIT** | But `htdemucs` was trained on **MUSDB18-HQ (CC BY-NC-SA 4.0 data)** + 800 additional songs. Whether model weights are a derivative work of training data is **legally unsettled**. Under most current reads they are not, but *do not build the business on this*. Repo archived Jan 2025; maintained fork at `adefossez/demucs` with limited maintenance. |
| **Spleeter** | Code **MIT**; weights trained on Deezer's internal catalogue | Same unsettled provenance question, and it is inferior to Demucs. **Skip entirely.** |
| **CREPE** | **MIT** | Clean. Use `tiny` capacity. |
| **pYIN (original Vamp plugin)** | **GPL** | **Do not link.** Reimplement from the paper, or clean-room from librosa's ISC implementation. This is the classic trap. |
| **NARA-WPE** | MIT | Clean, but offline-only in practice. |

### 7.4 Recommended path — train our own denoiser

**Recommendation: use DeepFilterNet's *architecture* (the MIT/Apache-2.0 code explicitly permits this) and train our own weights on licensed data.** Reasons, in order of importance:

1. It eliminates the weight-provenance question entirely.
2. It is the **only** way to fix the sung-vocal problem (§9.1), which off-the-shelf weights cannot solve.
3. It lets us add the second (de-reverb) head, which no off-the-shelf checkpoint has.
4. It lets us export SPP cleanly.

Cost estimate: **$15k–40k** in GPU time plus data licensing/collection. This is not optional spend — it is the core of the product's differentiation. Ship v0.1 internal builds against the public checkpoint to de-risk the integration, and swap in our weights before beta.

### 7.5 Runtime

**ONNX Runtime**, static shapes, IO-binding pre-allocated, CPU EP only, `intra_op_num_threads = 1` with our own thread pool (ONNX's default pool will fight the host's audio thread and cause dropouts). Quantise to int8 where PESQ loss < 0.05 (typically the encoder; keep the deep-filter head in fp32). Ship a fallback fp32 path for platforms where the quantised kernels are slower (common on Apple Silicon).

### 7.6 Voice transformation — the honest answer

Nectar's Backer is a generative/transform feature. Doing it *well* requires a neural vocoder or an RVC-class voice-conversion model. Three blockers:
1. **Provenance.** Most permissively-licensed RVC weights have unclear or plainly non-consensual training-data provenance.
2. **Voice-likeness legal exposure.** Producing a recognisable third-party voice character is an emerging and rapidly-moving liability area (right of publicity, and now multiple state and national statutes).
3. **CPU.** A realtime neural vocoder is 3–10× our entire remaining budget.

**Recommendation for v1:** implement "voice character" with **classic formant shifting + PSOLA + LPC spectral-envelope morphing** — a fixed set of envelope targets, no cloning, no identifiable person. It will be less dramatic than Backer. That is the correct trade.

---

## 8. Measurable quality gates

### 8.1 Objective — signal integrity

| Metric | Gate | Method |
|---|---|---|
| **Null test (neutral bypass)** | ≤ **−120 dBFS** peak residual | All modules at unity/neutral; PDC-aligned subtract from input. **Every module must have a true, sample-aligned bypass.** |
| **THD+N (chain transparent)** | ≤ **−110 dB**, 20 Hz–20 kHz | 1 kHz @ −3 dBFS, saturation off, EQ flat |
| **Alias rejection (saturation)** | ≤ **−70 dBFS** worst case (standard), ≤ **−85 dBFS** (HQ) | 0 dBFS sine sweep 100 Hz–18 kHz; notch the fundamental and integer harmonics; measure the residual **below** the fundamental (aliases fold down — that's where they're audible) |
| **EQ magnitude accuracy** | within **±0.1 dB** of analytic target, 20 Hz–20 kHz | Swept sine / log-chirp deconvolution at **44.1 / 48 / 96 / 192 kHz**. This is where matched-Z earns its keep. |
| **Compressor curve accuracy** | static curve within **±0.2 dB** of spec; attack/release within **±10%** of the labelled value | Stepped-level and tone-burst measurement. Most competitors' labels are fiction; being accurate is a marketing asset. |
| **Limiter true-peak** | **0 overs** above ceiling across a 10 000-file corpus; ISP overshoot ≤ 0.1 dB | BS.1770-4 4× TP meter (8× above 96 k) |
| **Parameter-change discontinuity** | no click > **−60 dBFS** on any single-step parameter change | Automated sweep over every parameter × every step, measure peak transient |
| **Latency correctness** | reported PDC == measured impulse delay, **±0 samples** | Impulse through **every** tier × SR × config permutation |
| **Denormal / decay** | no CPU spike on decay-to-silence | Profile under sustained silence after a loud burst |

### 8.2 Objective — neural clean-up

Test set: held-out **sung** vocals (multi-genre, multi-gender, multi-mic) × room IRs × real noise, at **0 / 5 / 10 / 20 dB SNR**.

| Metric | Gate |
|---|---|
| PESQ-WB @ 5 dB SNR | **≥ 3.00** |
| STOI @ 5 dB SNR | **≥ 0.93** |
| SI-SDR improvement @ 5 dB SNR | **≥ 12 dB** |
| **Log-spectral distortion on speech-present frames** | **≤ 1.5 dB** |
| **Clean-input passthrough:** LTAS change above 8 kHz on already-clean input | **≤ 0.3 dB** |
| De-reverb: DRR improvement | **≥ 6 dB** with LSD ≤ 2.0 dB |

The last two rows are the ones that matter and that the literature ignores. **PESQ and SI-SDR reward aggressive removal; they do not penalise damaging the signal you keep.** A model can score PESQ 3.3 and sound terrible on a sustained vowel. LSD-on-speech-frames and clean-input-passthrough are our artifact gates, and they are **blocking**.

### 8.3 Subjective — A/B protocol

**Non-negotiable: loudness-matched to ±0.1 LU (LUFS-I, BS.1770-4) before every comparison.** Unmatched A/B is the single largest source of dishonesty in plugin evaluation, ours included.

- **MUSHRA-style (ITU-R BS.1534)** with hidden reference and low-/mid-anchors.
- ≥ **12 trained listeners**, ≥ **20 excerpts** spanning genre, gender, register, microphone class and room quality (include deliberately bad sources: phone recording, untreated bedroom, guitar-amp bleed, sibilant condenser).
- Conditions: **VOX** vs **Nectar 4 Advanced (Vocal Assistant)** vs **hand-mixed human reference** vs **unprocessed**.
- **Gate:** VOX mean score ≥ Nectar 4 with **non-overlapping 95% CIs** on **≥ 12 of 20** excerpts. We do *not* gate on beating the human reference — that is not the bar, and pretending it is will produce dishonest tuning.

**Assistant-specific gates** (200-vocal corpus, blind preference test):
- Preferred over unprocessed by **≥ 85%** of listeners.
- **Catastrophic-failure rate ≤ 2%** — i.e. the Assistant produces a result *worse than the input* on no more than 2% of sources.
  The failure rate matters more than the mean. Users forgive a mediocre suggestion; they uninstall over one result that made their vocal worse.

**Regression harness:** a fixed 200-file corpus rendered on every build, with per-file PESQ/STOI/LSD/LUFS/TP and a **bit-exactness check against the previous build** for any module not intentionally changed. Any unintended bit-difference fails CI.

---

## 9. Brutal honesty — what is hard, what will not sound as good as advertised

**9.1 — Neural denoise on *sung* vocals is not a solved problem. This is the #1 risk.**
Every off-the-shelf model in this space (DFN, RNNoise, DCCRN, and the commercial equivalents) is trained on speech. Sung vocals break their assumptions: sustained vowels with vibrato look like tonal noise; vocal fry looks like impulsive noise; whisper and breathy textures look like the thing to remove; screamed vocals look like clipping distortion. You will get **warbling on held notes, truncated vibrato tails, and mangled stylistic textures**. The fix is training data, not architecture. **Budget more engineering time for the corpus than for the model.** Anyone who tells you they'll drop in a checkpoint and ship is wrong.

**9.2 — De-reverb will underdeliver relative to any marketing copy we write.**
It is single-channel, and the reverb is perfectly correlated with the source. Physics limits us. Realistic: **4–8 dB of DRR improvement before the timbre audibly degrades** (it goes phasey/hollow first, then metallic). We must advertise "**reduce** room" and never "**remove** room." iZotope's RX Dereverb has the same limit and gets criticised for it; we will too if we oversell.

**9.3 — Beating Nectar 4 is ~20% DSP and ~80% Assistant + presets + UI.**
Their individual modules are fine. Nobody chooses Nectar because its compressor is better. They choose it because the Assistant produces a usable starting point in five seconds and because it talks to the rest of the iZotope ecosystem. **Better filters will not win the shootout. Better decisions will.** Resource the Assistant, the preset library and the source corpus accordingly — and expect that argument to be unpopular in a room full of DSP people.

**9.4 — Realtime formant-preserving pitch correction that beats Melodyne/Auto-Tune Pro is a multi-year project by itself.** Do not scope it into v1. Ship excellent F0 analysis, key detection, formant frames and clean hooks. Ship a competent tuner if you must. Do not ship a mediocre Auto-Tune clone in a product that is trying to establish a quality reputation.

**9.5 — Latency tiering doubles the QA matrix and it is not optional.**
Three tiers × 4 sample rates × mono/stereo/M-S × ML on/off is 72 configurations, each needing a PDC verification and a null test. Modules with two implementations (resonance suppressor, de-esser, denoise) need both fully tested and, ideally, **tuned to sound similar** — a user who tracks in Live and mixes in Mix should not hear the chain change character. That similarity tuning is real, unglamorous work.

**9.6 — Spectral-processing artifacts are what will kill the reviews, and metrics will not catch them.**
Pre-echo, warble, musical noise, transient smearing. Every mitigation (multi-resolution split, transient freeze, gain smoothing, gain floors, harmonic protection) costs CPU and must be tuned **by ear**, not by metric. Our objective gates will tell us an artifact is fine; a reviewer with a sustained female vowel will tell us it isn't. **Build the listening loop before building the features.** Also, de-essing cannot distinguish an "s" from a deliberately airy texture — they are the same signal — so over-de-essing produces a lisp and no amount of DSP fixes that.

**9.7 — The ML stage is a real product constraint, not just a CPU line item.**
At ~9% of a core per instance, a 12-vocal session spends over a core on denoising alone, and instances cannot share inference (different audio). Required mitigations: **ML off by default** on instances after the first N, an explicit **"ML Freeze/Render"** path that bakes the clean-up to a cached buffer, and honest documentation. Nectar sidesteps this entirely by having no denoiser — that is the cost of our main differentiator, and we should take it knowingly.

**9.8 — Auto-levelling always produces a flatter result than a human, and experienced engineers dislike it.**
The gap between "sounds mixed" and "sounds like a compressor" lives almost entirely in **phrase-boundary segmentation** (§4.15b), not in the gain law. Even done well, the output is more consistent than a human ride, which reads as "lifeless" to some listeners. Ship a **Depth** control and default it below maximum. Do not let the demo be the default.

**9.9 — Things we should expect to be worse at than iZotope on day one:** preset breadth, ecosystem integration (nothing to talk to), GPU-accelerated UI polish, and genre coverage of the Assistant's training data. These are all funding-and-time problems, not intellectual ones, but they are real and they show up in reviews.

---

## Sources

- [iZotope Nectar 4 Advanced review — Sound On Sound](https://www.soundonsound.com/reviews/izotope-nectar-4-advanced)
- [Nectar 4 Help (iZotope documentation)](https://docs.izotope.com/nectar4/en/index.html) · [Auto-Level module](https://docs.izotope.com/nectar4/en/alm/index.html)
- [Nectar 4 product page — iZotope](https://www.izotope.com/products/nectar-advanced)
- [iZotope Nectar 4 review — MusicTech](https://musictech.com/reviews/plug-ins/izotope-nectar-4-brings-valuable-updates-alongside-some-unexpected-creative-tools/)
- [oeksound soothe2 user manual (PDF)](https://storage.googleapis.com/oeksound-downloads/soothe2/soothe2_ManualFAQ.pdf) · [soothe2 manual (web)](https://oeksound.com/manuals/soothe2/) · [soothe3 manual](https://oeksound.com/manuals/soothe3/)
- [Schröter et al., "DeepFilterNet: Perceptually Motivated Real-Time Speech Enhancement," Interspeech 2023 (PDF)](https://www.isca-archive.org/interspeech_2023/schroter23b_interspeech.pdf)
- [Rikorose/DeepFilterNet — GitHub (license, models)](https://github.com/Rikorose/DeepFilterNet) · [DeepFilterNet3 ONNX export](https://huggingface.co/soniqo/DeepFilterNet3-ONNX) · [deepfilter-rt ONNX Runtime realtime implementation](https://github.com/shimondoodkin/deepfilter-rt)
- [facebookresearch/demucs — GitHub (MIT, htdemucs 9.0 dB SDR)](https://github.com/facebookresearch/demucs)
- [xiph/rnnoise — GitHub (BSD)](https://github.com/xiph/rnnoise)
- [deezer/spleeter LICENSE (MIT)](https://github.com/deezer/spleeter/blob/master/LICENSE)
- [marl/crepe — GitHub (MIT)](https://github.com/marl/crepe) · [Kim et al., "CREPE: A Convolutional Representation for Pitch Estimation," arXiv:1802.06182](https://arxiv.org/abs/1802.06182)
- [Waves Vocal Rider user guide (PDF)](https://assets.wavescdn.com/pdf/plugins/vocal-rider.pdf) · [Waves Vocal Rider review — Sound On Sound](https://www.soundonsound.com/reviews/waves-vocal-rider)
- [Parker, Zavalishin, Bright, "Reducing the aliasing of nonlinear waveshaping using continuous-time convolution," DAFx-16 (PDF)](http://dafx16.vutbr.cz/dafxpapers/20-DAFx-16_paper_41-PN.pdf)
- [Chowdhury, "Practical Considerations for Antiderivative Anti-Aliasing"](https://jatinchowdhury18.medium.com/practical-considerations-for-antiderivative-anti-aliasing-d5847167f510) · [ADAA experiments repo](https://github.com/jatinchowdhury18/ADAA)
- [Vicanek, "Note on Alias Suppression in Digital Distortion" (PDF)](https://vicanek.de/articles/AADistortion.pdf)
- [Antialiasing Piecewise Polynomial Waveshapers, DAFx-23 (PDF)](https://www.dafx.de/paper-archive/2023/DAFx23_paper_61.pdf)
- [EBU R128 — Loudness normalisation and permitted maximum level (PDF)](https://tech.ebu.ch/docs/r/r128.pdf) · [EBU Tech 3343 — Practical guidelines (PDF)](https://tech.ebu.ch/files/live/sites/tech/files/shared/tech/tech3343v2_0.pdf)
- [Drude et al., "NARA-WPE: A Python package for weighted prediction error dereverberation" (PDF)](https://groups.uni-paderborn.de/nt/pubs/2018/ITG_2018_Drude_Paper.pdf)

=== END OF PART ===
