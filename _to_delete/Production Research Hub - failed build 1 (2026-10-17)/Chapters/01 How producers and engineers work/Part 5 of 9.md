# Chapter 01: How producers and engineers work
## Part 5 of 9

_What working producers and engineers actually do, who to study, and the forum/community knowledge. Includes the vox producer + engineer interviews and the "expert mode" master prompt._

**In this part:**
- round1_engineer.md (piece 1 of 2) — ROUND 1 — DSP + ML ARCHITECTURE SPECIFICATION

(Next: Part 6 of 9)


=====================================================
SOURCE FILE: round1_engineer.md (piece 1 of 2)
ORIGINAL LOCATION: WT:vox/docs/design_process/round1_engineer.md
=====================================================

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


=== END OF PART ===
