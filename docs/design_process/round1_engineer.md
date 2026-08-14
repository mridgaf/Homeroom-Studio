# ROUND 1 — DSP + ML ARCHITECTURE SPECIFICATION
## AAA AI Vocal Processor ("VOX") — Engineering Brief
**Author:** The Engineer · **Round:** 1 (architecture, no production code) · **Date:** 2026-08-13

---

## 0. Executive posture

Nectar 4's individual DSP modules are **competent, not exceptional**. Their moat is (a) the Vocal Assistant's decision quality, (b) preset/ecosystem lock-in (Tonal Balance Control, inter-plugin comms), and (c) brand. Two structural gaps are exploitable:

1. **Nectar 4 has no denoiser and no de-reverb.** iZotope deliberately silos that in RX. A vocal chain that cleans the source *inside the same plugin*, with the noise model shared to every downstream detector, is a category difference — not a feature bullet.
2. **Every Nectar module has its own private detector.** Its de-esser, dynamic EQ and compressor independently rediscover the same 7 kHz sibilant and fight over it. A **single shared analysis bus** (F0, voicing, speech-presence probability, sibilance ratio, noise floor, onset flux) feeding all modules is both cheaper and audibly better.

We will not win on "better biquads." We win on **shared analysis, correct stage ordering, artifact discipline, and decision quality**. Section 9 is brutally honest about where this gets hard.

---

## 1. Competitive teardown

### 1.1 iZotope Nectar 4 (Advanced)

Confirmed module inventory and chain from the vendor docs and the *Sound On Sound* review: **Auto-Level Module (ALM), Compressor ×2, EQ ×2, Gate, De-esser, Saturation, Pitch, Voices, Backer, Reverb, Delay, Dimension.** In Advanced, **the ALM initiates the processing chain** — i.e. gain riding is placed *pre-everything*.

- **Vocal Assistant** — analyses the incoming vocal, compares its spectrum against a target/reference curve, exposes two macro controls (**Shape** = tone match amount, **Intensity** = dynamics, linked to compressor threshold), and constructs a full chain behind the scenes that is editable in Detailed View.
- **Auto-Level (Advanced only)** — a *learning* leveler, not a compressor. Has Target, Mix, **Tame Noise** (prevents non-sung material being pushed up), a max operation range, and a speed control.
- **Voices** — key detection + interval/style presets (thirds, octaves) for generated harmonies.
- **Backer** — voice-persona transformation, 8 presets, with tone and formant adjustment. This is a generative/transform feature and is the thing we should *not* chase in v1 (§7.6, §9.4).
- **Unmask** — inter-plugin ducking of a companion track's spectrum against the vocal.

**Assessment.** ALM-first is a defensible choice (it calibrates thresholds) but it is the *wrong place for musical fader rides*, because a leveler placed before nonlinear stages changes how hard those stages are driven. We split this into two riders (§4.15) — a genuine improvement, not a repaint.

### 1.2 oeksound soothe2 — dynamic resonance suppression

From the vendor manual: it is explicitly a *dynamic resonance suppressor* applying reduction "only to harsh and resonant parts of the signal, where and when needed." Key facts worth stealing/beating:

- **Soft vs Hard mode** — fundamentally different laws (a depth of 3.0 is not equivalent between them). Soft preserves transients, is less level-dependent, fewer artifacts, avoids drastic cuts. Hard is more aggressive and easier to over-apply.
- **Depth** ±18 dB *referential* (not absolute); extreme settings reach ~**60 dB notches**.
- **Sharpness** 0–10 controls cut width/Q; excessive sharpness produces "distortion" that the manual concedes is "noise and non-resonant residue."
- **Selectivity** 0–10 — how peak-selective vs broadband the reduction is.
- **Attack/Release are frequency-dependent**, with faster response at high frequencies. This is correct and we replicate it.
- The EQ-node curve works as an **"inverse EQ"**: boosting a node *increases sensitivity* there. 2 cut bands + 4 general bands (peak/shelf/band-reject/tilt), each with Freq/Sens/Q/Balance.
- **Spectral oversampling** is required for LF accuracy and for smooth results at high Sharpness — confirming that the engine is FFT-based and that bin resolution is its binding constraint.
- **Resolution/time-domain** setting (Eco/High/Ultra) controls filter refresh rate; artifacts on transient-heavy material are "easily audible" at low settings.
- Delta mode (global and per-band), external sidechain, M/S, stereo link 0–100%, separate offline-render quality.

**The gap we exploit:** soothe has **no pitch awareness**. It cannot distinguish "an unwanted 2.8 kHz box resonance" from "the singer is belting a sustained note whose 4th harmonic sits at 2.8 kHz." Our F0-aware harmonic protection (§4.7) is a real, demonstrable, A/B-able win.

### 1.3 Waves Vocal Rider — automatic gain riding

Level-detector against a target range, with an optional **music sidechain** so the target is relative to the mix bus rather than absolute; range limits; a "sensitivity to breaths/noise" behaviour; and — critically — **the rider curve is written as automation** so the engineer can print and edit it. Automation write-out is table stakes, not a differentiator.

### 1.4 Neural front-ends surveyed

| System | Arch | Latency | Cost | Quality | License |
|---|---|---|---|---|---|
| **DeepFilterNet3** | 2-stage: 32 ERB gains → complex **5-tap deep filter** to ~5 kHz; 48 kHz, 20 ms window / 10 ms hop | **40 ms** (2-frame lookahead) | **RTF 0.19** single-thread on i5-8250U | PESQ-WB **3.17**, STOI **0.944**, CSIG 4.34 / CBAK 3.61 / COVL 3.77 (VoiceBank+DEMAND) | Code **MIT or Apache-2.0** (dual, user's choice) |
| **RNNoise** | ~85k-param GRU, band gains | ~10 ms | negligible | Far below DFN | **BSD-3** (Xiph) — cleanest license in the field |
| **HTDemucs (v4)** | Hybrid transformer/waveform, ~7.8 s receptive field | Non-realtime | Very high | **9.0 dB SDR** (htdemucs_ft) | Code + weights **MIT**; trained on MUSDB18-HQ + 800 extra songs. Repo archived Jan 2025 |
| **Spleeter** | U-Net masks, 11 kHz default | Non-realtime | Moderate | Below Demucs | Code **MIT**; weights trained on Deezer internal catalogue |
| **CREPE** | Conv pitch, 10 ms hop, capacities tiny→full | ~30 ms | tiny is cheap | SOTA-class F0 | **MIT** |
| WPE / NARA-WPE | Linear prediction dereverb, order 20–32 | Iterative, block | Moderate | Good multichannel, weak single-channel | MIT |
| OM-LSA / MMSE-LSA + MCRA | Statistical | ~11 ms | ~1% | Musical noise | Public domain algorithms |

---

## 2. Global architecture

### 2.1 Dual-rail design

```
                    ┌──────────────────────────────────────────────┐
   IN ──┬──────────►│  ANALYSIS RAIL (control rate, mono downmix)  │
        │           │  STFT 1024/2048 @48k · 10 ms hop             │
        │           │  → F0 + confidence, voicing, SPP, noise PSD, │
        │           │    ERB energies, LTAS, per-band crest,       │
        │           │    sibilance ratio, spectral flux/onsets,    │
        │           │    LPC formants, DRR estimate                │
        │           └────────────────┬─────────────────────────────┘
        │                            │  SHARED SIDECHAIN BUS
        │                            ▼  (all modules subscribe)
        └──────────►[ AUDIO RAIL: sample-accurate, minimum-phase ]──► OUT
                     delay-aligned so decisions LEAD their events
```

**Rules:**
- The analysis rail is computed **once**. No module runs a private FFT or private pitch tracker.
- The audio rail is delayed by the analysis rail's algorithmic latency in Mix/Tracking tiers, so every detector decision is **available before the sample it applies to arrives**. This is what makes attacks inaudible without per-module lookahead stacking.
- Analysis runs at a **fixed 100 Hz control rate** (10 ms hop) regardless of host sample rate → CPU is flat from 44.1 k to 192 k.
- Every module exposes `getLatencySamples()`; the host PDC value is the exact measured sum. **Non-negotiable QA gate:** reported PDC == measured impulse delay, ±0 samples (§8).

### 2.2 Latency tiers

| Tier | Budget | Use | What changes |
|---|---|---|---|
| **LIVE** | **< 10 ms** | Tracking/monitoring, live PA | ML denoise in low-latency config or RNNoise; resonance suppressor in filter-bank mode; split-band de-ess; 1.5 ms limiter lookahead; no plosive lookahead |
| **TRACKING** | **< 25 ms** | Overdubs with headphone comfort | ML on at 20 ms; filter-bank suppressor; 3 ms lookaheads |
| **MIX** | unbounded (~110 ms) | Mixing with PDC | Everything at full quality: spectral suppressor, spectral de-ess, DFN at 40 ms, linear-phase EQ option |

Tier is a single global control and, where the plugin API allows, auto-switches on host record-arm. **This doubles the QA matrix (§9.5) — budget for it.**

### 2.3 Numerics and filter core

- **One filter core for everything: the TPT / zero-delay-feedback state-variable filter (Zavalishin).** `g = tan(π·fc/fs)`, `k = 1/Q`; LP/BP/HP available simultaneously from one structure.
  - **Why not RBJ Direct-Form-I biquads:** DF-I has state discontinuity on coefficient change (zipper on modulation) and severe coefficient quantisation noise at low `fc/fs`. TPT is stable under audio-rate modulation and numerically well-conditioned in float32 down to 10 Hz at 192 k.
  - **The critical implementation detail for dynamic EQ and de-essing:** in Zavalishin's *mixing form*, a bell's gain appears as a **linear output-mix coefficient**, not inside the feedback coefficients. Therefore we modulate **only the mix gain** and never the `g`/`k` coefficients. This gives artifact-free, audio-rate gain modulation with zero recalculation cost. Most commercial dynamic EQs recompute coefficients per block and smear/zipper as a result. This is the single highest-leverage detail in the whole document.
- **Time constants:** `a = exp(-1/(τ·fs))`, computed once per parameter change, on the control thread. Cache `exp` via a rational approximation; never call `exp()` per sample.
- **Sample rate:** all filters are specified in normalised frequency → SR-independent by construction. ML runs at a canonical 48 kHz.
  - **Resampling strategy (better than the obvious one):** rather than resampling the whole signal to 48 k and back (2× polyphase cost, and the model destroys the 16–24 kHz air band at 96 k sessions), **band-split at 16 kHz with a linear-phase complementary crossover**. The 0–16 kHz band is decimated to 48 k (well, to 32 k — 16 kHz band needs 32 k; in practice decimate to 48 k and feed the model its native band) and processed; the >16 kHz band is delay-matched and has the model's top-ERB-band gain envelope applied to it. Preserves air, halves resample cost at high SR.
- **Denormals:** FTZ+DAZ set on the audio thread, plus explicit denormal-flush on all recursive state (add-and-subtract a `1e-20` DC offset in IIR feedback paths). Verify with a decay-to-silence test under a profiler.
- **Realtime discipline:** zero heap allocation, zero locks, zero `std::function`, zero logging on the audio thread. Parameter changes cross via a lock-free SPSC ring; all coefficient math on the message thread.

---

## 3. Signal chain — order and justification

```
 0. Input conditioning · trim · polarity · M/S · calibration to internal ref
 1. DC block / rumble HPF (adaptive) + dynamic plosive tamer
 2. ─┐
 3.  ├ JOINT NEURAL CLEAN-UP: denoise + de-reverb (dual-head, one model)
    ─┘
 4. Gate / downward expander / breath control    (SPP-informed)
 5. [PITCH & TIMING HOOKS] — F0, voicing, key, formants published to bus
 6. Subtractive resonance suppression  (soothe-class, F0-aware)
 7. Dynamic EQ  (corrective, pre-dynamics)
 8. COMPRESSOR A — slow leveler   (feedback topology, opto-law, 3–6 dB)
 9. COMPRESSOR B — fast peak      (feedforward, lookahead, 3–6 dB)
10. De-esser                       (post-compression — see justification)
11. Saturation / harmonic excitation (multiband, ADAA + 2× OS)
12. Tonal EQ (additive, static, matched-Z)
13. Transient shaper (differential-envelope, voicing-aware)
14. Output gain rider ("the fader")
15. True-peak limiter (ISP-aware)
16. Loudness normalisation / metering (BS.1770-4) — static trim only
```

Plus **stage 0.5: input normaliser** (see §4.15) — a very slow ±12 dB trim placed *before* stage 1.

### Ordering justifications (the non-obvious ones)

**Denoise before gate (2/3 → 4).** Gating a noisy signal produces noise pumping: the noise floor steps in and out with every gate open/close, which is far more audible than the noise itself. Once the floor is at −70 dB the gate becomes cosmetic and can be gentle. Nectar places its Gate early with **no denoiser at all in the product** — this ordering is only available to us.

**Denoise and de-reverb jointly, not cascaded.** Two schools exist and the choice is forced by the algorithm class:
- If de-reverb is **WPE (linear prediction)**, it *must* precede denoise — WPE models the reverberant tail as an AR process, and a nonlinear denoiser upstream destroys that statistical model. This is why ASR front-ends run WPE → beamform/mask.
- If de-reverb is a **neural mask**, cascading two masking networks compounds artifacts multiplicatively: each net's residual musical noise becomes the next net's input signal.
- **Decision: one model, two heads.** Predict a noise-suppression gain field `G_n` and a late-reverb gain field `G_r` from a shared encoder, combine *in the gain domain* before a single resynthesis. This yields independent user controls with a single set of artifacts. Fallback path (ML off) is WPE → OM-LSA in that order.

**Resonance suppression before dynamics (6 → 8).** A resonance is, by definition, the loudest thing in the spectrum at that moment. Feed it to a compressor and the compressor keys on the resonance instead of the performance — you get gain pumping locked to the room, not the singer. Flattening the spectrum first makes every downstream detector honest. It also must precede saturation: saturating a resonance breeds harmonic *children* of that resonance at 2f, 3f, and those are much harder to remove afterwards.

**Corrective EQ before dynamics, additive EQ after saturation (7 vs 12).** Subtractive moves change what the compressor detects (desirable). Additive moves change the perceived tone and should shape the *final* spectrum, including harmonics the saturator generated. Boosting 10 kHz before a saturator just makes the saturator produce more 20 kHz garbage.

**Serial compression, slow → fast (8 → 9).** Variance reduction cascades better than it stacks. Two stages at 4 dB GR each sound dramatically more transparent than one stage at 8 dB, because each stage's gain signal stays slow relative to its own detector. The slow leveler removes macro range (verse vs chorus, breath vs belt) so that the fast compressor's *threshold actually means something* — a fixed threshold in front of a ±15 dB-varying source is a random number generator. This is the LA-2A → 1176 topology and it is correct for reasons, not nostalgia.

**De-ess AFTER compression (10).** This is the ordering most chains get wrong. A compressor with a 5–20 ms attack lets the sibilant transient through *before* clamping, then ducks the following vowel — the net effect is that compression **raises perceived sibilance**. De-essing before the compressor is therefore partially undone. But raw sibilance can also trigger the compressor. Both problems solve at once with:

> **Two-point de-essing.** (a) A **detector-only** sibilance de-emphasis inside each compressor's sidechain (−6 dB dynamic shelf at 5–9 kHz on the *detector signal only*, never on the audio path) so the compressor stops keying on "s". (b) The **real de-esser** post-compression, where the sibilance level is now stable and the threshold means something.

Nectar exposes a single de-esser instance and a static sidechain filter. This is a concrete, defensible architectural improvement.

**Saturation after de-ess (11).** Saturating sibilance generates intermodulation products across the whole 8–20 kHz band — harsh, non-harmonic, and impossible to de-ess afterwards because they're broadband.

**Transient shaping late (13).** Operating on already-compressed material makes the effect predictable and level-independent; on raw material the same setting does wildly different things verse to chorus.

**Gain riding at 14, limiter at 15.** The rider must be **purely a fader** — the last thing before the limiter — so it does not change how any nonlinear stage is driven. (Nectar's ALM is *first*; it normalises input, which is a different and also-valid job. We do **both**, split: §4.15.)

**Loudness normalisation is a static trim, never dynamic (16).** Dynamic loudness normalisation after a rider is double-riding, and it fights the limiter.

---

## 4. Per-stage algorithm specification

Notation: `fs` = host sample rate; `τ` = time constant; latency figures are Mix-tier unless stated.

---

### 4.0 Input conditioning
- **DC removal:** 2nd-order Butterworth HP @ 12 Hz (TPT, cascaded 1-pole ×2) **plus** an explicit DC servo — a leaky integrator (τ = 100 ms) whose output is subtracted. The HP alone leaves slow sub-10 Hz drift from certain converters; the servo alone has no rolloff. Together: flat above 20 Hz, zero DC.
- Trim (±24 dB), polarity, channel config (mono / stereo / M-S), instance link.
- **Internal level calibration (differentiator):** over the first 3 s of voiced material, measure LUFS-I and store a `calibrationOffset` such that the chain's internal operating point is **−18 LUFS**. All module thresholds are then specified *relative to calibrated reference*, not in absolute dBFS. Consequence: a preset built on a −6 LUFS pop vocal works unchanged on a −30 LUFS home-recorded demo. iZotope's thresholds are absolute; this is why their presets travel badly.
- **Latency: 0.**

---

### 4.1 Rumble HPF + dynamic plosive tamer

**Static HPF.** Cascaded TPT SVF, Butterworth-aligned, 12/24/48 dB/oct.
- **Adaptive cutoff:** from the F0 histogram over the analysed region, set `fc = 0.72 × F0_p5` (5th percentile of voiced F0), clamped to [50, 140] Hz.
  - *Why better than fixed 80 Hz:* a bass singer at F0 = 75 Hz loses his fundamental to a "safe" 80 Hz HPF; a soprano at F0 = 260 Hz keeps 200 Hz of pure mud. Fixed HPFs are always wrong for someone.

**Dynamic plosive tamer.** Detection (from the bus, 10 ms hop):
- `LF_ratio = E(20–120 Hz) / E(20 Hz–20 kHz)` in dB
- LF envelope rise > 20 dB in < 15 ms
- Low spectral flatness above 2 kHz (a plosive is LF-only; a kick bleed is not)
- Trigger when all three coincide, with 150 ms retrigger inhibit.

**Action — this is the improvement:** rather than a wideband gain duck (what RX de-plosive and most competitors do, which dips the note), **sweep the HPF cutoff** 60 → 220 Hz over the plosive: attack 3 ms, hold 20 ms, release 60 ms, cutoff trajectory raised-cosine. The fundamental above 220 Hz is untouched; only the sub-band puff is removed. On a female vocal (F0 ≈ 220 Hz) this is completely inaudible except that the pop is gone.
- Requires **5 ms lookahead** (Mix/Tracking). In Live tier the detector is reactive and the attack is 8 ms — it catches ~80% of the pop energy, which is acceptable.
- **Latency: 5 ms (Mix/Tracking), 0 (Live).**

---

### 4.2/4.3 Joint neural clean-up — denoise + de-reverb

**Primary path — neural.**
- Topology: DeepFilterNet3-class. 48 kHz, 20 ms window, 10 ms hop, **32 ERB-scaled band gains** (stage 1, envelope) + **complex 5-tap deep filter** applied up to ~5 kHz (stage 2, periodicity). This two-stage split is exactly right for voice: ERB gains fix the broadband envelope cheaply, deep filtering restores harmonic fine structure where the ear cares.
- Reference figures: **40 ms latency** (2-frame lookahead), **RTF 0.19** single-thread on an i5-8250U, PESQ-WB 3.17 / STOI 0.944 on VoiceBank+DEMAND.
- Runtime: **ONNX Runtime** with a static graph, fixed batch 1, pre-allocated IO binding, CPU EP with the ARM64/AVX2 kernels; no dynamic shapes, no per-block allocation. GPU EP is *not* used — PCIe round-trip latency destroys the realtime budget for 10 ms hops.

**Our six modifications (this is what makes it a music product, not a conference-call feature):**

1. **Fine-tune on sung vocals.** DFN is trained on *speech*. On sustained vowels with vibrato, a speech-trained model treats steady tonal energy that doesn't match speech statistics as noise and produces **warbling on held notes** — and it will maul vocal fry, whisper, screamed vocals and falsetto. Fine-tune corpus: sung vocals (multi-genre, multi-language, both genders, ≥ 200 h) × room IR convolution × real noise (HVAC, laptop fan, guitar-amp bleed, hiss, mains hum, street). **This is the #1 sound-quality risk in the entire project (§9.1).**
2. **Dual-head output.** Shared encoder → head A predicts a noise gain field `G_n`, head B predicts a *late-reverb* gain field `G_r` (target = direct+early / (direct+early+late), with the early/late split at 50 ms). Combine **in the gain domain**, not by wet/dry audio blending:
   `G = (1−α_n + α_n·G_n) · (1−α_r + α_r·G_r)`
   Blending processed audio against dry audio would comb-filter, because the model path is 40 ms late. Blending gains is phase-coherent by construction. This gives the user two independent, artifact-free "amount" knobs.
3. **Gain floor.** Clamp per-band gain to ≥ **−18 dB** by default (user-adjustable −6 to −60 dB). Full nulling is precisely what produces the "underwater / dropout" character of AI denoisers. Musical denoise ≠ maximum SNR.
4. **Post-net gain smoothing.** 1-pole per band, **τ_attack = 8 ms, τ_release = 60 ms** (asymmetric — fast to duck noise, slow to release so the floor doesn't flutter), plus a 3-tap triangular smoother **across** bands. Removes the residual musical noise the net leaves.
5. **Noise-floor re-injection (nobody ships this well).** Instead of removing noise to digital silence, synthesise a spectrally-matched noise from the estimated noise PSD and re-inject at −20 dB (user-controllable, "Floor" knob). The result is a *continuous* noise floor with the offending noise 20 dB down, instead of a floor that breathes in and out with the voice. This single feature is the difference between "sounds processed" and "sounds like a better room."
6. **Publish SPP to the bus.** The model's speech-presence probability is free and is consumed by the gate, the rider, the de-esser and the transient shaper. **One model, five consumers** — this is the cheapest quality win in the design.

**Classic fallback (Live tier, ML-off, or CPU-constrained sessions):**
- **Denoise:** OM-LSA / MMSE log-spectral-amplitude (Ephraim–Malah) with **MCRA** noise-PSD estimation (minima-controlled recursive averaging). Decision-directed a-priori SNR with `ξ` smoothing 0.98. 512-pt STFT @ 48 k, 75% overlap, √Hann analysis/synthesis (COLA-satisfying WOLA). ~11 ms latency, < 1% CPU. Sounds worse (musical noise) but is deterministic and cheap.
- **De-reverb:** per-band RT60 estimated from the decay slope of the band envelope during offsets; late-reverb PSD modelled as delayed-and-scaled signal PSD (Lebart/Habets); subtract with the same MMSE-LSA gain rule. Single-channel WPE (order 20–32, delay 2 frames, 3 iterations) is available **offline only** — it is block-iterative and unsuitable for realtime.

- **Latency: 40 ms (ML Mix), ~20 ms (ML Tracking, 1-frame lookahead), ~11 ms (classic Live).**

---

### 4.4 Gate / expander / breath control

Post-denoise, so this is tail and bleed control, not noise removal.

- **Topology:** feedforward downward expander, log-domain gain computer. Ratio 1:1 → 1:20, plus hard-gate (∞:1) mode.
- **Dual detector (the improvement):** open on `max( level_detector, SPP_gate )` where
  - `level_detector` = RMS over 10 ms of a 200 Hz–6 kHz bandpassed sidechain
  - `SPP_gate` = the neural speech-presence probability from the bus, thresholded at 0.5
  - *Why:* unvoiced consonants ("t", "f", "th", "k") have very low energy but very high SPP. Every level-only gate chops them, which is exactly the "gate ate my consonants" complaint. Ours doesn't.
- **Hysteresis:** independent open/close thresholds, `close = open − Hyst`, default 6 dB. Prevents chatter on the threshold.
- **Release curve:** *not* a single exponential. Dual-branch — fast (τ = 3 ms) and slow (τ = 200 ms), take the **minimum gain** of the two. Fast enough to close between words, slow enough never to chatter. Single-exponential gates always force a bad compromise here.
- Attack 0.05–50 ms (default 1 ms), Hold 5–500 ms, Release 5–2000 ms, Range (max attenuation) 0–80 dB.
- **Lookahead 3 ms** so the attack ramp *completes* before the transient arrives → gate opening is inaudible.
- **Breath mode (separate, on by default):** detect breaths — high spectral flatness, low F0 confidence, energy concentrated 1–8 kHz, duration 80–400 ms — and apply a fixed −X dB gain (default −9 dB) with 20 ms raised-cosine ramps rather than gating them. **Gating breaths sounds unnatural and robotic; attenuating them sounds professionally mixed.** Also expose "breath boost" for the intimate-pop aesthetic.
- **Latency: 3 ms.**

---

### 4.5 Pitch / timing hooks

**We do not ship a pitch corrector in v1.** We ship the analysis and the hooks. Rationale in §9.4.

Published to the bus at 10 ms hop:
- **F0 + confidence.** Hybrid: **McLeod Pitch Method (NSDF)** in the time domain as the primary (cheap, sub-ms, sample-accurate period) arbitrated by **CREPE-tiny** (ONNX, MIT, ~486 k params) for confidence and octave disambiguation. MPM alone octave-errors on breathy sopranos and vocal fry; CREPE alone is 10× the cost and has 30 ms of frame latency. The hybrid gets MPM's precision with CREPE's robustness.
  - *License note:* the original **pYIN** Vamp implementation is **GPL — do not link it.** Reimplement from the paper or work clean-room from librosa's (ISC) implementation.
- **Voicing probability, key/scale** (chroma-weighted Krumhansl-style template correlation over the F0 histogram), **formants** (LPC order `2 + fs/1000` ≈ 18 at 48 k, autocorrelation + Levinson–Durbin, 25 ms Hann, 10 ms hop).

**If/when a correction engine is built:** PSOLA for shifts within ±3 semitones on voiced frames (best formant and transient preservation, cheapest, needs ~2 pitch periods ≈ 20 ms lookahead at 100 Hz); phase-vocoder with **Laroche–Dolson phase locking** (identity or scaled) for larger shifts and unvoiced material; crossfade between the two by voicing confidence. Formant preservation via LPC envelope resynthesis (extract envelope, shift excitation only, reapply envelope).

- **Latency: 0** (analysis only; already accounted in the analysis rail).

---

### 4.6 *(reserved — merged into 4.2/4.3)*

---

### 4.7 Subtractive resonance suppression — the crown jewel

This is the most differentiating module. Specify it in the most detail.

#### Two engines, one detector

**Engine A — spectral gain field (Mix/Tracking tier, maximum surgical precision).**
- WOLA: 2048-pt FFT @ 48 k (42.7 Hz bin spacing, 42.7 ms window), hop 256 (5.3 ms), √Hann analysis and synthesis (COLA-satisfied at 87.5% overlap → use hop 256 with a 2048 window = 8× overlap; expensive but this is the Mix tier).
- **Multi-resolution split (fixes soothe's binding constraint).** 42.7 Hz bins are far too coarse below 300 Hz — this is precisely why soothe needs a "spectral oversampling" control and why its manual says high oversampling is "imperative" for LF accuracy. We instead **split at 500 Hz with a linear-phase complementary crossover**; the low band is decimated 8× and processed with its own 2048-pt STFT, yielding **5.3 Hz resolution below 500 Hz** at *lower* total cost than brute-force zero-padding the full band. The HF path stays at full rate. Delay-compensate the two paths.
- Latency: 43 ms (window) + crossover ≈ **48 ms**.

**Engine B — dynamic filter bank (Live tier, phase-coherent, no pre-echo).**
- Detect the top **N = 8–16** resonance peaks per analysis frame; allocate N TPT peaking filters with modulated `fc`, `Q`, gain.
- **Peak-track assignment is the hard part.** Naïve per-frame re-sorting makes filters jump between peaks → warble and zipper. Use hysteretic track continuation: each filter keeps its assignment while its peak persists within ±15% in frequency and remains above a −6 dB hysteresis; a Hungarian-style minimum-cost assignment (cost = log-frequency distance + amplitude distance) handles births/deaths; new tracks fade in over 20 ms, dead tracks fade out over 50 ms.
- Latency: **~2 ms.** Slightly less surgical than Engine A, but zero pre-echo and completely phase-coherent — for some material it is *preferable*, and we should say so in the UI rather than hiding it as "low quality."

#### The detector (identical for both engines — the actual secret sauce)

Reduction must be driven by **excess over a perceptual local average**, never by absolute energy.

1. Magnitude `|X[k]|` → dB.
2. **Expected spectral envelope `Env[k]`.** Use **real-cepstrum liftering**: `Env = exp(IFFT(lifter(FFT(log|X|))))` keeping quefrency < 1.5 ms. Cepstral liftering follows *formants* without being pulled by the harmonic comb — a Bark-warped moving average (the obvious approach) gets dragged upward by dense low harmonics and under-detects LF resonances. Lifter cutoff is the **Sharpness** control (0.5–3.0 ms quefrency ↔ Sharpness 0–10).
3. **Excess** `E[k] = dB|X[k]| − Env[k]`.
4. **Weighting** `W[k]` — the user's EQ-node curve, implemented as an **inverse EQ** exactly as soothe does (boosting a node *increases* sensitivity there), multiplied by:
   - an equal-loudness weighting (ISO 226 @ 70 phon), and
   - a **simultaneous-masking spreading function** (Schroeder-style, +25 dB/Bark lower slope, −10 dB/Bark upper slope). *A resonance that is masked does not need removing.* Spending 12 dB of reduction on an inaudible 400 Hz peak is a pure loss of signal.
5. **Gain** `G[k] = −clamp( (E[k]·W[k] − Threshold)₊ × Depth, 0, MaxReduction )`. MaxReduction default 12 dB, range 0–60 dB (matching soothe's demonstrated ceiling).
6. **Frequency-dependent time constants** (soothe does this and it is correct — HF resonances are perceptually shorter):
   `τ_att(f) = clamp(4000/f ms, 0.5, 20)`, `τ_rel(f) = 8 × τ_att(f)`.
7. **Frequency smoothing of `G[k]`** with a Gaussian kernel whose width is inversely proportional to Sharpness (0.15–1.0 ERB). **Un-smoothed spectral gain fields produce time-domain ringing** — this is the "watery/phasey" artifact, and it is a *frequency-domain discontinuity* problem, not a time-domain one. soothe's own manual concedes that high Sharpness produces "distortion... noise and non-resonant residue" — that's exactly this.

#### Three things that make ours better than soothe2

1. **F0-aware harmonic protection.** Using the bus F0 track, compute per-bin harmonicity `h[k] = max over n of exp(−(cents(k, n·F0)/30)²)`, then scale the excess: `E'[k] = E[k] · (1 − 0.7·h[k]·HarmonicProtect)`. Result: we suppress *resonances* and preserve the singer's *notes*. soothe, with no pitch model, will notch a sustained belted note it mistakes for a resonance — this is a well-known complaint and it is a **directly A/B-demonstrable win**.
2. **Masking-aware weighting** (step 4) — reduction budget is spent only where it is audible. Less total processing for the same perceived result = fewer artifacts.
3. **Transient freeze.** Compute spectral flux; when flux exceeds threshold (onset), **freeze the gain field for 10 ms**. Consonant onsets are broadband and briefly look exactly like resonances to any excess-detector; freezing prevents the consonant smearing that soothe's manual admits is "easily audible" at low Resolution settings.

Plus: **Delta/listen mode is mandatory** (global and per-band solo), external sidechain input, M/S and L/R modes, stereo link 0–100%, separate offline-render quality.

- **Latency: 48 ms (Engine A), 2 ms (Engine B).**

---

### 4.8 Dynamic EQ

- 6 bands, each: TPT SVF, type ∈ {bell, low-shelf, high-shelf, HP, LP, notch, tilt}, each independently switchable to dynamic.
- **Detector taps the band's own BP output** — free from the SVF, and it is the correct signal. Detecting on the wideband signal (which several shipping dynamic EQs do) makes a 200 Hz band respond to a 5 kHz sibilant.
- **Detector law: hybrid peak/RMS.** `env = max(peak_fast, k · rms_slow)` with a user "Punch" control morphing `k`. One knob instead of the peak-vs-RMS religious argument.
- Threshold absolute or **relative to the calibrated internal reference** (§4.0); ratio 1:1–20:1 in **both directions** (dynamic cut and dynamic boost); attack 0.1–300 ms; release 5–3000 ms + program-dependent auto; soft knee 0–24 dB (quadratic interpolation of the gain-computer).
- **Sidechain sources:** internal band, external input, and **harmonic-follow** — the detector tracks the `n`-th harmonic of the bus F0, so the band moves with the note. Nectar has no equivalent; it is genuinely useful for taming one problem note across a whole take.
- **Better than textbook:** gain is applied by modulating the SVF **mixing coefficient only** (§2.3) — no coefficient recomputation, no zipper, artifact-free at audio rate, and **zero latency by construction**.
- **Optional linear-phase mode** (Mix tier): compose the total magnitude response and convolve via a 2048-tap zero-phase FIR (partitioned uniform overlap-save), 21 ms latency. **Default OFF**, with a UI note about pre-ringing. Linear-phase EQ on a vocal is almost always the wrong choice and we should say so rather than sell it as "better."
- **Latency: 0** (minimum-phase), 21 ms (linear-phase).

---

### 4.9 Compressor A — slow leveler

**Role:** remove macro variance (3–6 dB GR). Must never be audible *as compression*.

- **Topology: feedback (return-path) detection**, log-domain. Feedback topology yields a soft, program-dependent effective ratio and self-limiting behaviour — measurably smoother than feedforward for slow work, and it's why opto compressors sit so well on vocals. (Trade-off: feedback topology **cannot** use lookahead. That's fine — the attack is 10 ms+.)
- **Detector:** RMS, 20–50 ms window, on a sidechain that is (i) HPF'd at 120 Hz (12 dB/oct) and (ii) **sibilance-de-emphasised** — a dynamic −6 dB shelf at 5–9 kHz keyed by the bus sibilance ratio, applied **to the detector only** (§3, two-point de-essing).
- **Gain law:** ratio 1.5:1–4:1, soft knee 12 dB default.
- **Program-dependent release (the opto behaviour that matters):** two release branches, τ₁ = 60 ms and τ₂ = 800 ms, blended by recent GR history — `w_slow = clamp(GR_avg_400ms / 6 dB, 0, 1)`. More gain reduction → more of the slow branch. This is precisely why an LA-2A "breathes" correctly and a fixed-release compressor pumps.
- **Attack** 10–150 ms (default 30 ms).
- **Auto-makeup** derived from measured average GR, applied smoothly (τ = 500 ms) so that turning the threshold does not change perceived loudness. Directly attacks the "louder = better" bias that makes A/B testing dishonest.
- **Latency: 0.**

---

### 4.10 Compressor B — fast peak

- **Topology:** feedforward, log-domain, **smooth-decoupled peak detector** (per Giannoulis/Massberg/Reiss, *JAES* 2012, "Digital Dynamic Range Compressor Design — A Tutorial and Analysis"). Smooth-decoupled is the right default: it produces continuous, discontinuity-free attack *and* release, unlike branching or simple decoupled designs.
- **Lookahead 1.5–5 ms** (default 3 ms), with the gain trajectory shaped over the lookahead window by a raised-cosine rather than a linear ramp — a linear ramp has a derivative discontinuity at both ends, and that discontinuity *is* the audible "click/spit" on fast attacks.
- Ratio 2:1–20:1, knee 0–24 dB, attack 0.1–100 ms, release 5–1000 ms + auto, RMS/peak blend ("Punch"), parallel Mix with automatic delay compensation.
- **Adaptive release from the bus:** lengthen release during sustained voiced notes (prevents note-level pumping); shorten during consonant clusters (keeps articulation). Keyed on voicing + onset flux.
- **Gain-signal slew limiting (the detail most plugins get wrong).** A gain signal changing at 1 dB/sample at 48 kHz has spectral content far above Nyquist — this, not the static curve, is where fast compressors generate aliasing and intermodulation. Hard-limit the gain slew to **0.35 dB/sample**, which caps intermod products at approximately **−70 dBFS** and removes any need to oversample the compressor at all. Combined with a soft knee (≥ 6 dB), the gain signal is band-limited by construction.
- **Latency: 1.5–5 ms.**

---

### 4.11 De-esser

Three modes:
1. **Broadband duck** — full-band GR keyed by the sibilance detector. Fast, cheap, lisps if pushed.
2. **Split-band (default)** — dynamic high-shelf or bell, 4.5–12 kHz, TPT, **mix-coefficient modulation** (§2.3).
3. **Spectral (Mix tier)** — per-bin reduction confined to the sibilance region, reusing the §4.7 engine with a sibilance-shaped weighting. Most transparent; 20–48 ms.

**Detector — where nearly every de-esser fails.** Do **not** use an absolute HF threshold. Use a **ratio**:

```
S_dB = 10·log10( E(4.5–11 kHz) / (E(200 Hz–3 kHz) + ε) )
gate  = S_dB > S_target  AND  flatness_HF > 0.4  AND  ZCR high
GR    = (S_dB − S_target) × Amount
```

Because `S` is a *ratio*, the de-esser is **level-independent**: the singer gets quieter in the verse, the de-esser keeps working, no threshold re-tweak, no automation. This is the single largest available de-esser improvement and it is not hard. The flatness and ZCR terms discriminate sibilance (noise-like) from a bright sustained vowel (harmonic) — without them, ratio detectors false-trigger on belted high notes.

**Adaptive centre frequency.** Track the spectral centroid within 4–12 kHz per sibilant event and centre the reduction band there, smoothed over the event (τ = 30 ms), clamped. A female "s" lives at 7–9 kHz; a male "sh" at 4–6 kHz; the same singer's "s" and "f" differ by an octave. **A fixed band is always wrong for someone**, and Nectar's adaptive mode is coarse.

- Attack 0.2–5 ms with **3 ms lookahead** (sibilant onsets are 2–5 ms — without lookahead you always miss the leading edge, which is the harsh part), release 20–200 ms, **max-reduction clamp**, and a **Listen** mode that solos the removed signal.
- **Recommended default: two gentle stages** (the compressor-sidechain de-emphasis + this one at ≤ 4 dB) rather than one stage at 8 dB. Serial gentle de-essing is dramatically less lispy for the same measured reduction.
- **Honest limitation (§9.6):** no detector can distinguish an unwanted "s" from a deliberately bright, breathy, airy vocal texture — they are the same signal. Over-de-essing produces a lisp, and that failure is perceptual, not solvable with more DSP.
- **Latency: 3 ms (modes 1–2), 20–48 ms (mode 3).**

---

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
