# ROUND 2 — ADVERSARIAL DSP REVIEW
## Hostile peer review of `round1_engineer.md` (VOX architecture brief)
**Reviewer:** The Adversarial DSP Engineer · **Date:** 2026-08-13 · **Authority:** veto

---

## 0. Posture

The brief is well-written, and being well-written is exactly the problem. It reads as if the hard parts are solved. They are not. §9 ("brutal honesty") is doing enormous rhetorical work: it pre-empts criticism of the *risks the author already knows about* while leaving the actual engineering errors — arithmetic, latency, numerics, detector topology, metric validity, corpus economics — untouched and unflagged.

I independently verified the ML claims (§3 of this review, and B7/B8 below). Some check out. The ones that check out are cited from the wrong model version. The ones that matter most — cost and corpus — are off by one to two orders of magnitude.

**Twenty blocking objections. Twenty-one non-blocking.** Every one names a failure mode or a broken arithmetic step. Verdict at the end.

---

# PART A — BLOCKING OBJECTIONS

*Must be fixed, in writing, before this spec advances to implementation.*

---

## B1. The latency budget (§5) omits the analysis rail entirely. The LIVE tier as specified is mathematically impossible.

**The claim.** §2.1: "The audio rail is delayed by the analysis rail's algorithmic latency in Mix/Tracking tiers, so every detector decision is **available before the sample it applies to arrives**. This is what makes attacks inaudible without per-module lookahead stacking." §2.1 also specifies the analysis rail as "STFT 1024/2048 @48k · 10 ms hop", and §4.5 concedes CREPE has "30 ms of frame latency."

**The failure.** §5's budget table has **no line item for the analysis rail.** It sums only per-module lookaheads. A 1024-point analysis window at 48 kHz is 21.3 ms; a 2048-point window is 42.7 ms. A decision about the samples inside that window cannot exist until the window is full. Add the 10 ms hop quantisation and the CREPE-tiny arbiter's 30 ms and the analysis rail's true decision latency is **~31 ms (1024 + hop) to ~73 ms (2048 + hop + CREPE)**.

The LIVE tier claims a **17.3 ms total**. That is less than the analysis window alone. Therefore in LIVE tier one of two things is true, and the spec says neither:

- (a) The audio rail is *not* delayed to the analysis rail, so every module keyed on the bus — the gate's SPP branch, the de-esser's sibilance ratio, the transient shaper's voicing gate, the rider's phrase segmentation, the suppressor's F0 harmonic protection — is acting on data that is **21–73 ms stale**. At a 100 Hz control rate that is 2–7 control frames of lag. The voicing-aware transient shaper (§4.14) will emphasise the *end* of the consonant it was supposed to emphasise; the phrase-boundary rider (§4.15b) will make its "fast move at a boundary" 40 ms into the next word.
- (b) The audio rail *is* delayed, in which case the LIVE total is ≥ 31 ms, TRACKING is ≥ 50 ms, MIX is ≥ 140 ms, and every published number in §5 and §2.2 is wrong.

The brief's §5 "honest note" admits Tracking overshoots by 1 ms. It is overshooting by 25–50 ms.

**Named breaking signal.** A staccato consonant-led phrase ("stop-start-stop") tracked in LIVE tier. The gate's SPP branch opens 20+ ms late, the level branch has 3 ms lookahead, so the gate opens on the level detector and the SPP branch never contributes — the entire "gate ate my consonants" differentiator (§4.4) silently degrades to a level gate in the tier where it matters most.

**Required fix.**
1. Add an explicit `ANALYSIS_RAIL` row to §5 with per-tier values, decomposed as window + hop + arbiter.
2. Specify, per module, whether it consumes **leading** (audio-delayed) or **lagging** (stale) bus data, and quantify the lag for the lagging ones.
3. Republish §2.2's tier budgets against the corrected totals. If LIVE cannot carry the bus, say so and specify the reduced LIVE analysis config (e.g. 256-pt window, 5.3 ms, MPM only, no CREPE) and which differentiators are disabled in that tier.

---

## B2. The resonance suppressor's LF multi-resolution path is off by a factor of seven in latency and produces ~170 ms of pre-echo on the fundamental.

**The claim.** §4.7 Engine A: "split at 500 Hz with a linear-phase complementary crossover; the low band is decimated 8× and processed with its own 2048-pt STFT, yielding **5.3 Hz resolution below 500 Hz** at *lower* total cost… **Latency: 43 ms (window) + crossover ≈ 48 ms**."

**The failure — three separate errors compounding.**

1. **The resolution number is wrong.** 48000 / 8 = 6000 Hz. A 2048-point FFT at 6 kHz gives **2.93 Hz** bin spacing, not 5.3 Hz. (5.3 is the *hop in milliseconds* from the HF path; the number has been copied from the wrong column.)

2. **The window length is catastrophic.** 2048 samples at 6 kHz is **341.3 ms**. Not 43 ms. The LF path's analysis window is a third of a second long. The two paths must be delay-aligned, so the *entire module* — not just the LF band — inherits **≥341 ms**, plus the crossover. The stated 48 ms is wrong by **7.1×**, and the MIX-tier total of 110 ms in §5 is wrong by **~3.5×** on this line alone.

3. **The pre-echo is disqualifying.** A zero-phase spectral gain applied over a 341 ms window smears its effect symmetrically, i.e. roughly **±170 ms**. On a vocal, every note onset in the 80–500 Hz region gets a 170 ms ghost of the *post*-onset processing applied *before* the onset. This is audible as a soft, breathy pre-swell in front of every sung note — the single most-mocked artifact class in spectral processing.

4. **The cost claim is unsupported.** A "linear-phase complementary crossover" at 500 Hz with a transition band narrow enough to be useful requires an FIR on the order of 4096+ taps at 48 kHz (85 ms), whose own cost and latency are also absent from §5 and §6.

**Named breaking signal.** A male vocal at F0 = 110 Hz singing a legato phrase into a room with a 180 Hz mode. The suppressor must resolve 110 Hz from 180 Hz — exactly the case that motivated the LF path. With a 341 ms window it will do so, and every note onset in that phrase will be preceded by 170 ms of pre-echo. The module fails on precisely the material that justified building it.

**Required fix.** Abandon the "long window at a decimated rate" approach. Either:
- (a) Use a **multirate filter-bank / complex-modulated LF analysis** with a window matched to the *time* resolution you can tolerate (≤ 60 ms), accepting 16–20 Hz LF resolution and compensating with the harmonic model rather than raw resolution; or
- (b) Run the LF band entirely on **Engine B** (tracked TPT peaking filters), which has no window and no pre-echo, and reserve the spectral engine for ≥ 500 Hz. This is the honest architecture and it should be the default.

Republish §5 and §6 for whichever is chosen.

---

## B3. Engine A's gain field is real and non-negative, therefore zero-phase, therefore its impulse response is symmetric and it pre-echoes. §4.7 step 7's stated theory of ringing is wrong.

**The claim.** §4.7 step 7: "**Un-smoothed spectral gain fields produce time-domain ringing** — this is the 'watery/phasey' artifact, and it is a *frequency-domain discontinuity* problem, not a time-domain one." §4.7 attributes zero pre-echo only to Engine B, and never states Engine A's pre-echo magnitude.

**The failure.** This is a half-truth stated as a whole one, and it will cause the wrong mitigation to be built. A real, non-negative, smooth gain field `G[k]` has **zero phase by construction**. Its inverse transform is therefore an even, symmetric impulse response centred at zero. Smoothing `G[k]` in frequency shortens that impulse response — that is the true and useful part of the claim — but it **cannot make it causal**. A perfectly smooth 12 dB notch still has a symmetric IR, and the ringing energy before the impulse equals the ringing energy after it.

At 2048 points / 42.7 ms, the worst-case pre-ring is ~21 ms even in the HF path. For the 60 dB notches §4.7 step 5 explicitly permits (`MaxReduction` range 0–60 dB), the notch's Q is extreme and the IR fills the window. The "transient freeze for 10 ms" mitigation (§4.7, item 3) addresses gain-field *modulation*, which is a different artifact; it does nothing about the pre-ring of a *static* notch.

**Named breaking signal.** A hard consonant onset ("K", "T") immediately following silence, on a source where the suppressor is holding a 20 dB notch at 3 kHz for a room resonance. The notch's symmetric IR spreads the pre-onset silence into a 10–20 ms pre-swish. The spec's own §9.6 lists pre-echo as a review-killer and then specifies an architecture that guarantees it.

**Required fix.**
1. State Engine A's pre-echo budget as a **measured gate** in §8.1: energy in the 20 ms preceding a detected onset, relative to the unprocessed signal, ≤ −40 dB.
2. Reconstruct the gain field as **minimum-phase** (cepstral / Hilbert minimum-phase lift of `log G[k]`) so all ringing is post-transient, and window the resulting IR to **< hop length** before applying. Yes, this costs a further FFT pair per frame — count it in §6 (see N10).
3. Delete or heavily qualify the "not a time-domain problem" sentence. It is the sentence most likely to cause an engineer to build the wrong fix.

---

## B4. F0-aware harmonic protection — the headline differentiator — is a no-op below ~2 kHz as specified.

**The claim.** §4.7: "compute per-bin harmonicity `h[k] = max over n of exp(−(cents(k, n·F0)/30)²)`", i.e. a Gaussian of **±30 cents** around each harmonic. §4.6/§1.2 stake the entire competitive claim against soothe2 on this: "a directly A/B-demonstrable win."

**The failure — unit mismatch.** Engine A's HF path has **42.7 Hz bins**. Convert to cents at the frequencies where the claim matters:

| Frequency | One bin (42.7 Hz) in cents | Protection width (±30 c) in bins |
|---|---:|---:|
| 200 Hz | ~330 cents | ±0.09 bins |
| 400 Hz | ~170 cents | ±0.18 bins |
| 1 kHz | ~72 cents | ±0.42 bins |
| 2 kHz | ~36 cents | ±0.83 bins |
| 6 kHz | ~12 cents | ±2.5 bins |

Below ~2 kHz, a ±30-cent window is **narrower than a single FFT bin**. `h[k]` evaluates to ≈ 0 for every bin except by coincidence, so `E'[k] = E[k] · (1 − 0.7·h·HP)` reduces to `E'[k] = E[k]`. **Harmonic protection is switched off in the 100 Hz – 2 kHz region — which is where sung fundamentals, the singer's formant, and every "belted note mistaken for a resonance" complaint actually live.** The differentiator is a no-op in its own use case.

Above ~4 kHz, where the width finally spans multiple bins, harmonic partials are dense and unresolved anyway, and the protection becomes a broadband HF sensitivity reduction — the opposite of surgical.

**Named breaking signal.** A tenor belting a sustained A3 (220 Hz). The 4th harmonic at 880 Hz is a genuine, loud, sustained spectral peak. `h[880 Hz]` ≈ 0 because 30 cents at 880 Hz is 15 Hz, one third of a bin. The suppressor sees a 12 dB excess over the cepstral envelope and notches the note. **This is the exact soothe2 failure the spec promises to beat, reproduced identically.**

**Required fix.** Define the protection kernel in a **bin-aware** width: `σ[k] = max(30 cents, 1.5 · binwidth_in_cents(k))`, and additionally weight by F0 confidence and by whether the bin is within the resolvable-harmonic region (`n·F0` separated by > 2 bins). Re-derive and state the achievable protection band per engine and per tier. If Engine A cannot protect below 2 kHz, that band must be delegated to Engine B (which tracks discrete peaks and *can* be told not to place a filter on a harmonic).

---

## B5. The "single shared analysis bus" is tapped only at the input. Every detector from stage 6 onward is keying on a spectrum that no longer exists.

**The claim.** §2.1 diagram: `IN ──► ANALYSIS RAIL`. §2.1: "The analysis rail is computed **once**. No module runs a private FFT or private pitch tracker." §1: "A **single shared analysis bus** … feeding all modules is both cheaper and audibly better."

**The failure.** By stage 8 the signal has passed through: neural denoise + de-reverb (a full time-varying spectral gain field), a gate, a resonance suppressor capable of 60 dB notches, and a dynamic EQ. By stage 14 it has additionally passed two compressors, a de-esser, a multiband saturator (which *creates* new harmonics), a tonal EQ, and a transient shaper. The input LTAS, input sibilance ratio, input per-band crest and input loudness are **not** descriptions of the signal these modules see.

Concrete breakages, in order of severity:

1. **The output rider (§4.15b) targets LUFS-S.** LUFS-S of *what*? It must be the post-chain signal — that is the entire point of an output fader. §4.15b says it "consumes the already-delayed analysis rail," which is the **input** analysis. As written, the rider rides to the input's loudness, so any gain the chain applies (auto-makeup, saturation drive, EQ boosts, limiter GR) is invisible to it. The module does not work.

2. **The compressor sidechain de-emphasis (§3, §4.9).** The −6 dB detector shelf is "keyed by the bus sibilance ratio." That ratio is measured pre-denoise, pre-suppressor, pre-dynamic-EQ. On a source where the suppressor has already removed 10 dB at 7 kHz, the bus reports high sibilance, the compressor de-emphasises 7 kHz that is no longer there, and the compressor **under-reacts to real transients** for the duration. This is a detector desensitised by a stale measurement — the exact class of bug the "shared bus" was sold as eliminating.

3. **The de-esser (§4.11) at stage 10** uses `S_dB` from the bus, but the saturator at 11 and tonal EQ at 12 are downstream and will re-add HF. The chain de-esses against a measurement taken before three stages of HF modification.

4. **The excitation gating (§4.12)** is "gated by SPP and by de-esser activity" — SPP is from stage 3, de-esser activity is from stage 10, and the exciter is at stage 11. Only one of those is a *current* measurement.

**Required fix.** Replace "computed once" with a specified **multi-tap** analysis bus: enumerate the tap points (minimum: post-input-conditioning, post-neural-cleanup, post-dynamics, post-chain-pre-limiter), state which features are published from which tap, and state the per-tap cost. Then rewrite the §6 CPU table, because the "one FFT for everything" saving is the basis of the 1.2% analysis-rail line and it is now 3–4 taps. If a feature is intentionally consumed stale, say so and bound the staleness.

---

## B6. The 16 kHz band-split ML resampling scheme is out-of-distribution for the model, does not save cost, and its latency is unbudgeted.

**The claim.** §2.3: "rather than resampling the whole signal to 48 k and back… **band-split at 16 kHz with a linear-phase complementary crossover**. The 0–16 kHz band is decimated to 48 k (well, to 32 k — 16 kHz band needs 32 k; in practice decimate to 48 k and feed the model its native band) and processed; the >16 kHz band is delay-matched and has the model's top-ERB-band gain envelope applied to it. Preserves air, halves resample cost at high SR."

The parenthetical is the author arguing with himself mid-sentence and losing. Setting that aside:

**Failure 1 — the model is fed out-of-distribution input.** DeepFilterNet3 operates at **48 kHz full band**, 481 bins, **32 ERB bands** spanning 0–24 kHz. Its top ERB bands *are* the 16–24 kHz region. Feed it a signal whose 16–24 kHz is empty (because you just crossed it over and removed it) and:
- The network sees a spectral shape it has never encountered in training — a hard cliff at 16 kHz. ERB-gain networks are strongly conditioned on global spectral shape; the encoder's normalisation statistics shift.
- The gains predicted for the top ERB bands are predictions **about silence**. They are noise.
- The spec then takes those garbage gains and applies them to the real 16–24 kHz band it held aside. This is not "preserving air." It is modulating the air band with an untrained network's response to a synthetic cliff.

**Failure 2 — it does not save cost.** At a 96 kHz host rate, the 0–16 kHz band after the crossover is still a **96 kHz** stream. Getting it to 48 kHz still requires 2:1 decimation — the exact polyphase stage the scheme claims to avoid. You have added a long linear-phase crossover FIR and a delay line and saved nothing. At 192 kHz you save one halving stage out of two, at the cost of a crossover far more expensive than the stage you removed.

**Failure 3 — 44.1 kHz is not addressed at all.** The most common session rate in music requires a **147:160** rational resample to reach the model's 48 kHz. That is the most expensive ratio in the table and it appears nowhere in §2.3 or §6. §2.3's claim "CPU is flat from 44.1 k to 192 k" is therefore false in the ML path specifically (see also N17 for the analysis rail).

**Failure 4 — unbudgeted latency.** A 16 kHz linear-phase crossover steep enough not to leak adds tens of milliseconds. §5 has no row for it.

**Required fix.** Delete the scheme. Specify a conventional, measured resampling strategy: high-quality polyphase to/from 48 kHz for all host rates, with the 44.1 k ratio explicitly costed. If HF preservation above 16 kHz is a goal, achieve it by **bypassing the model above 16 kHz with a delay-matched, gain-of-one path** (or a slow, smoothed broadband gain derived from the *speech-present* frames), not by feeding the model a truncated band and trusting its extrapolation.

---

## B7. There is no realtime scheduling model for the ML stage. The stated CPU figure, the threading plan, and the 99.9th-percentile gate are mutually incompatible — and the RTF number is cited from the wrong model.

**Verified facts** (I checked these independently):

| Claim in spec | Verified | Actual |
|---|---|---|
| DFN3 PESQ-WB 3.17 / STOI 0.944 / CSIG 4.34 / CBAK 3.61 / COVL 3.77 on VoiceBank+DEMAND | ✅ correct | Matches the Interspeech 2023 paper's table (DFN 2.81, DFN2 3.08, DFN3 3.17) |
| 40 ms latency, 20 ms window / 10 ms hop, 2-frame look-ahead | ✅ correct | Paper: "look-ahead of 2 frames… overall latency of 40 ms" |
| 32 ERB bands, 5-tap deep filter | ✅ correct | Paper: 32 ERB bands from 481 bins; N=5 |
| Deep filter "to ~5 kHz" | ⚠️ imprecise | Paper: lowest **96 bins, i.e. up to 4.8 kHz** |
| **"RTF 0.19 single-thread on i5-8250U"** for DFN3 | ❌ **misattributed** | 0.19 is the **DeepFilterNet v1** figure, repeated in the umbrella paper's abstract. **DeepFilterNet2 reports RTF 0.04** on the same i5-8250U. DFN3 is described in the paper as "the slightly modified DeepFilterNet model" trained on full multilingual DNS4 — architecturally ≈ DFN2, so ~0.04 is the honest figure. |
| Code dual MIT / Apache-2.0 | ✅ correct | README verbatim: "dual-licensed under either: MIT License… Apache License, Version 2.0… at your option" |
| Weight license not separately stated | ✅ correct, and the spec is right to flag it | README's licence section covers "all code in this repository" only. No weights clause, no commercial contact. |

So the citation is 5× pessimistic. That is not the problem. **The problem is that RTF is the wrong metric entirely and the spec has built its CPU budget and its realtime gate on it.**

**The failure.** RTF is measured by processing a whole file offline. It says nothing about the *distribution* of work in a realtime callback. DFN processes a **10 ms frame**. At the spec's own reference config (48 kHz, **128-sample buffer = 2.67 ms**), the inference does not spread across buffers — it lands **entirely inside one buffer out of every ~3.75**, and that buffer must absorb the whole frame's compute.

At RTF 0.04 on a 2017 mobile i5, one 10 ms frame = 0.4 ms of compute; on a modern P-core call it 0.15–0.25 ms. That fits. But:
- The spec's model is **not stock DFN3.** It adds a **second decoder head** (§4.2 item 2) — call it +25–40%.
- ONNX Runtime `Run()` call overhead at **100 calls/second** is 20–100 µs each, not counted.
- §6's own hard gate is "**99.9th-percentile** block processing time < 50% of the buffer period (not the mean — the mean is a lie)." The author correctly identifies that the mean is a lie and then budgets the ML stage entirely from a **mean-based metric (RTF)**. The 99.9th percentile of block time is, by construction, the ML-frame buffer. The gate is evaluated against the wrong number.
- At **64-sample buffers (1.33 ms)** — routine for tracking, which is a named tier — a single 10 ms frame's inference cannot be guaranteed to complete. It must be pipelined across buffers, which adds a buffer of latency that appears nowhere in §5.

**And the threading plan is self-contradictory.** §7.5: "`intra_op_num_threads = 1` **with our own thread pool** (ONNX's default pool will fight the host's audio thread)." If inference runs on *our* thread, the audio thread must synchronise with it. §2.3 forbids **locks** on the audio thread. The only lock-free options are (a) a lock-free ring with a **one-frame pipeline delay** (+10 ms, unbudgeted), or (b) spinning on the audio thread, which is worse than a lock. The spec picks neither and the contradiction is unresolved.

**Required fix.**
1. Correct the RTF citation and state which model version it belongs to.
2. Replace the RTF-derived CPU line with a **measured worst-case per-frame inference time** on the reference CPU, for the actual dual-head model, at fp32 and int8.
3. Specify the **frame-to-buffer scheduling model** explicitly: which thread, what synchronisation primitive, how many frames of pipeline, and the resulting added latency, per buffer size (64/128/256/512/1024) and per tier. Add that latency to §5.
4. Re-evaluate the 99.9th-percentile gate against the ML burst, not against the mean.

---

## B8. "$15k–40k to train our own weights" is off by one to two orders of magnitude. There is not enough commercially-licensable sung-vocal data in existence to execute the plan.

**The claim.** §7.4: "train our own weights on licensed data… **Cost estimate: $15k–40k in GPU time plus data licensing/collection.**" §4.2 mod 1 specifies the corpus: "sung vocals (multi-genre, multi-language, both genders, **≥ 200 h**) × room IR convolution × real noise."

**The failure.** The GPU line is plausible and irrelevant. The corpus line is the entire project and it is not costed. I checked availability:

| Corpus | Approx. hours (vocal) | Licence | Commercially usable? |
|---|---:|---|---|
| **MUSDB18-HQ** | ~10 h vocals | Explicitly: "**provided for educational purposes only… should not be used for any commercial purpose without the express permission of the copyright holders**"; composed partly of MedleyDB (CC BY-NC-SA 4.0) and Easton Ellises (CC BY-NC-SA 3.0) | ❌ **No** |
| **MedleyDB** | ~7 h | CC BY-NC-SA 4.0 | ❌ No |
| **M4Singer** | ~30 h | Custom dataset licence, research-oriented; terms not stated in README, must be accepted per-user | ❌ Not without written clearance |
| **OpenSinger / Opencpop / NUS-48E / CSD / GTSinger** | ~2–50 h each | Research / NC / custom | ❌ Mostly no |
| **VocalSet** | ~10 h | CC BY 4.0 | ✅ Yes — but it is 20 singers performing *techniques*, not songs. Genre and language coverage ≈ zero. |

**The total pool of commercially-clean, permissively-licensed sung-vocal audio is on the order of 20–40 hours, and most of it is technique exercises, not performances.** The spec asks for 200 hours across genres, languages and genders. That data has to be *created* or *licensed per-track*:

- **Licensing multitrack stems** from labels/publishers for ML training: per-catalogue negotiation, master + publishing clearance, ML-training-rights riders that most 2020s contracts do not contemplate. Realistic: **$500k–$5M and 6–18 months of legal**, and no guarantee of coverage.
- **Recording it yourself:** 200 h of finished, dry, studio-captured singing ≈ **200+ session-days**, singer fees, studio, engineering, editing, metadata, across ≥6 genres and ≥4 languages. Realistic: **$300k–$1M+ and 9–18 months.**

**And the noise/IR side has the same problem, which the spec does not mention at all.** DFN3 is trained on **DNS4**. DNS4's noise is largely AudioSet- and Freesound-derived, carrying a mixture of CC licences **including CC BY-NC and CC BY-SA**. So:
- (i) It is a real reason to doubt the public checkpoint's commercial cleanliness — a stronger reason than "the README doesn't say," which is all §7.3 offers; **and**
- (ii) **we cannot train on DNS4 either.** §7.4's plan to "train our own weights" inherits the same corpus problem for noise that it has for voice, and specifies no alternative.

**Compounding:** §7.4 proposes to "Ship v0.1 internal builds against the public checkpoint to de-risk the integration, and swap in our weights before beta." Fine-tuning a checkpoint of unresolved provenance produces a **derivative work of that checkpoint**. If the plan is fine-tune-then-ship, the provenance question is not eliminated, it is inherited.

**Required fix.**
1. Rewrite §7.4's cost line as three separate numbers: GPU, **voice corpus acquisition**, **noise/IR corpus acquisition**. Show the arithmetic.
2. State the corpus acquisition *strategy* — record, license, or synthesise — with a schedule and an owner. §9.1 already says "budget more engineering time for the corpus than for the model." That sentence and "$15k–40k" cannot both be in the same document.
3. Hard process rule, stated in the spec: **no artefact containing third-party checkpoint weights or weights fine-tuned from them leaves the building** — including betas, demos, trade-show builds and screenshots-with-audio. From-scratch training only for anything shipped.
4. Specify the from-scratch noise/IR corpus. Candidates that are actually clean: DEMAND (CC BY-SA — note the share-alike), self-recorded room tone and device noise, self-measured IRs. Budget it.

---

## B9. The neural quality gates (§8.2) are speech-communication metrics applied to sung music. Two of the three are blind to the bands this product claims to protect, and the SI-SDR gate directly contradicts two of the design's own headline features.

**The claim.** §8.2 gates: PESQ-WB ≥ 3.00, STOI ≥ 0.93, **SI-SDR improvement ≥ 12 dB**, plus LSD-on-speech-frames ≤ 1.5 dB and clean-input LTAS change above 8 kHz ≤ 0.3 dB. The brief correctly says "PESQ and SI-SDR reward aggressive removal" — and then gates on them anyway.

**Failure 1 — PESQ-WB physically cannot see the air band.** PESQ wideband (ITU-T P.862.2) is defined at a **16 kHz sampling rate**, i.e. it evaluates content up to 8 kHz. To compute it on a 48 kHz vocal you must downsample to 16 k, discarding **8–24 kHz**. The spec's §2.3 band-split exists to protect 16–24 kHz; §8.2's clean-passthrough row measures above 8 kHz. **PESQ is structurally incapable of scoring either.** A model that destroys everything above 8 kHz scores identically to one that preserves it.

Worse: PESQ's perceptual model and MOS mapping were fitted on **telephony degradations** (codecs, packet loss, level, noise) judged for *communication quality*. It is documented to be insensitive to spectral tilt and HF loss and to correlate poorly with music quality. On sung material it is close to a random number with a plausible-looking magnitude.

**Failure 2 — STOI measures intelligibility, in 1/3-octave bands up to ~4.3 kHz.** Intelligibility of a sung lyric the listener already knows is not a quality axis anybody cares about. STOI is blind above 4.3 kHz. The gate "STOI ≥ 0.93" is passed by stock DFN3 (0.944) before any of our work; it discriminates nothing.

**Failure 3 — the SI-SDR gate contradicts the design.** SI-SDR is scale-invariant and waveform-referenced; it rewards nulling the residual and **penalises any added signal, benign or not**. The spec specifies:
- §4.2 item 3, **gain floor at −18 dB** — deliberately leaves 1/8 of the noise in. Lowers SI-SDR.
- §4.2 item 5, **noise-floor re-injection at −20 dB** — deliberately *adds* synthesised noise. Lowers SI-SDR, and it is uncorrelated with the reference so it is penalised at full weight.

These two are described as "the difference between 'sounds processed' and 'sounds like a better room.'" **The design's two best ideas are the two things the gate punishes.** Tuning to pass "SI-SDR improvement ≥ 12 dB @ 5 dB SNR" means turning both of them off. Ship the gate as written and it will drive the product toward exactly the "underwater/dropout" character §4.2 item 3 exists to prevent.

**Required fix.** Demote PESQ/STOI/SI-SDR to *non-gating regression telemetry* (useful for catching a training collapse, worthless as a quality bar) and replace the gates with:

**Full-band, music-valid perceptual:**
- **ViSQOL v3 in audio mode** (48 kHz, music-capable) — gate.
- **PEAQ (ITU-R BS.1387) Advanced** ODG — sensitive to exactly the HF/artifact classes PESQ ignores.
- **DNSMOS P.835** — reported as three separate numbers. **SIG is the one that matters**: it is the "did you damage the voice" axis PESQ lacks. Gate on SIG *and* BAK, never on OVRL alone.
- **NISQA** dimensional output (noisiness / coloration / discontinuity / loudness) — "discontinuity" is a direct warble/dropout detector.

**Sung-vocal-specific (these must be built; none exist off the shelf):**
- **Harmonic-to-noise ratio (HNR) delta on voiced frames** — ≤ 1 dB degradation. Directly detects the "warble on held notes" failure of §9.1.
- **F0 trajectory RMSE** and **vibrato preservation**: modulation rate error ≤ 2%, modulation depth error ≤ 5%, over sustained voiced segments. This is the single best proxy for the #1 stated risk.
- **Formant drift** F1–F4 ≤ 2%.
- **Mel-cepstral distortion (MCD)** on voiced frames.

**Artifact-specific:**
- **Musical-noise metric** — kurtosis ratio of per-band power distributions, pre/post (Uemura/Miyazaki). Gate it; it is the metric that catches the classic subtractive-denoise artifact and nothing else in §8.2 does.
- **Pre-echo metric** — energy in the 20 ms window preceding each detected onset, referenced to clean. Gate ≤ −40 dB. (Ties to B2/B3.)
- **Transient smearing** — plosive attack-time delta ≤ 1 ms.
- **Clean-input passthrough extended to full band** plus an F0-trajectory identity check and a **null test on clean input**, not just an LTAS check above 8 kHz.

**Test material:** the §8.2 test set must include the failure classes §9.1 names — **vocal fry, whisper/breath textures, falsetto, screamed vocals, heavy vibrato, sustained held notes** — as *separately scored strata*, not averaged into a pooled number. Pooled means the 5% of material that breaks catastrophically is invisible.

---

## B10. float32 + TPT SVF does not meet the spec's own −120 dBFS null and −110 dB THD+N gates at low `fc/fs`. The claim of float32 sufficiency is asserted, not derived.

**The claim.** §2.3: "TPT is stable under audio-rate modulation and **numerically well-conditioned in float32 down to 10 Hz at 192 k**." §8.1 gates: null test ≤ **−120 dBFS**, THD+N ≤ **−110 dB**.

**The failure.** TPT/ZDF fixes the *coefficient* conditioning problem — that part is true and is why the topology is right. It does not fix the **state** problem, which is what sets the noise floor.

At `fc` = 10 Hz, `fs` = 192 kHz: `g = tan(π·10/192000) ≈ 1.636 × 10⁻⁴`. The trapezoidal integrator update accumulates an increment proportional to `g` into a state of order-unity magnitude. Each accumulation quantises to float32's ~1.19 × 10⁻⁷ relative resolution. The recursive round-off noise gain of a leaky integrator scales roughly as `1/(2g)`:

    1 / (2 × 1.636e-4) ≈ 3057 ≈ +69.7 dB

Against a float32 quantisation floor of ~−144 dBFS, the filter's output noise floor sits near **−74 dBFS**. That is **46 dB above the −120 dBFS null gate** and **36 dB above the −110 dB THD+N gate**. The two claims in §2.3 and §8.1 cannot both be true.

This is not marginal, and it is not only the 10 Hz/192 k corner: at the far more common **12 Hz DC-blocker at 48 kHz** (`g ≈ 7.9e-4`) the same analysis gives ~−88 dBFS — still failing the null gate by 32 dB. And §4.0 puts *two* such stages (Butterworth HP + DC servo) at the head of the chain, in series, on every instance.

There is a second, related error in the same section: §2.3 prescribes "add-and-subtract a `1e-20` DC offset in IIR feedback paths" for denormal flushing. In float32 the smallest normal is ~1.18 × 10⁻³⁸ and the smallest subnormal ~1.4 × 10⁻⁴⁵; a 1e−20 offset is enormous relative to the values it is protecting and will itself perturb the state. The idiom is inherited from float64 practice and pasted into a float32 design.

**Required fix.**
1. **All recursive filter state in float64.** This is standard practice in every serious plugin and it removes the objection outright. Audio path may remain float32; integrator states must not.
2. Re-derive and state the achievable noise floor per topology per `fc/fs` corner, and gate on it.
3. Replace the 1e−20 DC-offset denormal idiom with FTZ/DAZ (already specified) plus, if needed, a value scaled to the working precision.
4. Re-audit §6's CPU table: float64 SVF state roughly halves SIMD lane count for the filter blocks. The "40 SVFs × ~8 flops = 0.8%" line will move.

---

## B11. "Modulate only the mix coefficient" — billed as "the single highest-leverage detail in the whole document" — produces gain-dependent Q on bells and gain-dependent corner frequency on shelves, violating the ±0.1 dB EQ accuracy gate. And §4.1 contradicts the rule outright.

**The claim.** §2.3: "in Zavalishin's *mixing form*, a bell's gain appears as a **linear output-mix coefficient**… Therefore we modulate **only the mix gain** and never the `g`/`k` coefficients. This gives **artifact-free**, audio-rate gain modulation with zero recalculation cost… **This is the single highest-leverage detail in the whole document.**"

**The failure.** The technique is real and the zipper-elimination claim is correct. "Artifact-free" is not.

1. **Bell bandwidth becomes gain-dependent.** In the SVF mixing form, the bell is `y = x + (A²−1)·k·BP` with the damping `k` fixed. For the response to be a *constant-Q* bell — the same −3 dB bandwidth at +6 dB as at −6 dB — the damping must be co-scaled with `A`. Hold `k` fixed and you get a **proportional-Q** bell whose bandwidth changes with gain. §4.13 explicitly offers proportional-Q as a *user-selectable* "Analog" law and constant-Q as "Digital" — but §2.3's rule makes proportional-Q **mandatory**, so the "Digital / constant-Q" option cannot be implemented as specified. Direct internal contradiction.

2. **Shelf corner frequency moves with gain.** The mixing-form shelf is `y = x + (A−1)·LP` with fixed `g`. In an analog-matched shelf the midpoint transition frequency scales as `fc·√A`. Fixed `g` means an "8 kHz high shelf" at −10 dB has its transition somewhere other than 8 kHz. §8.1 gates EQ magnitude accuracy at **±0.1 dB, 20 Hz–20 kHz**, and §4.13 sells matched-Z accuracy as "a real, measurable, marketable accuracy claim." A gain-dependent shelf corner fails that gate at every non-zero gain.

3. **The de-esser's artifact is now nameable.** §4.11 mode 2 is a *dynamic high shelf* using this exact mechanism, doing up to 12 dB of dynamic cut on a 2–5 ms sibilant. Under the fixed-`g` rule, as the gain sweeps down and back the shelf's effective corner and the bell's Q sweep with it. The band is *moving during the event*. That is precisely the "swooshy / lisping / phasey" de-esser artifact, and it is generated by the mechanism the spec calls artifact-free.

4. **Phase modulates with gain.** A minimum-phase bell's phase response is a function of its gain. Modulating gain at sibilant rates modulates the phase of everything passing through the band — i.e. it frequency-modulates the harmonics in that band. On a sustained bright vowel under heavy dynamic EQ this is audible as a chirp/wobble. Unaddressed.

5. **§4.1 violates the rule on the next page.** The dynamic plosive tamer's entire mechanism is to "**sweep the HPF cutoff** 60 → 220 Hz over the plosive: attack 3 ms." That is modulating `g` on a cascaded 12–48 dB/oct filter, fast, which §2.3 says never to do. Either the rule has exceptions (state them, with the smoothing and the transient analysis) or the plosive tamer needs a different mechanism.

**Required fix.**
1. State the exact mixing-form equations for bell and shelf, and state which Q/corner law each yields.
2. For constant-Q, specify the coefficient co-scaling and its recomputation cost, or withdraw the "Digital / constant-Q" option.
3. Add a §8.1 gate: **EQ magnitude accuracy at ±0.1 dB must hold across the full gain range**, measured at −18, −12, −6, 0, +6, +12, +18 dB, not just at one gain.
4. Downgrade "artifact-free" to "zipper-free," and add a measured gate for Q/corner drift under dynamic action.
5. Reconcile §4.1 with §2.3 explicitly, and gate the plosive HPF sweep by current F0 (never sweep above ~0.8·F0) — see N3.

---

## B12. ADAA-1 + 2× oversampling will not meet the −70 dBFS alias gate under the spec's own test signal.

**The claim.** §4.12: "ADAA-1 delivers roughly the alias rejection of 2–4× oversampling at ~¼ the cost… **Recommended operating point: ADAA-1 + 2× oversampling, which comfortably clears a −70 dBFS alias floor.**" §8.1 test: "**0 dBFS sine sweep 100 Hz–18 kHz**; notch the fundamental and integer harmonics; measure the residual below the fundamental."

**The failure.** ADAA-1's alias suppression is **strongly dependent on input level and input frequency** — it is a first-order approximation to continuous-time convolution, and its accuracy degrades as the signal moves further per sample. It provides on the order of an extra 6 dB/octave of alias rolloff, which is excellent for low-level, low-frequency content and progressively worthless at **high level and high frequency**.

The spec's own gate signal is the worst case for ADAA: **0 dBFS at 18 kHz**. At 48 kHz with 2× OS (96 kHz internal), an 18 kHz fundamental at full scale into a `tanh` puts h2 at 36 kHz and h3 at 54 kHz — h3 folds to 42 kHz then aliases down to 6 kHz after decimation. Published ADAA measurements put ADAA-1 at 2× OS in the **~40–55 dB** alias-rejection range at high level and high frequency, not 70 dB. The HQ target of −85 dBFS is further out of reach.

It gets worse in this specific design: **the multiband split (§4.12) puts the 4 kHz–Nyquist band into its own shaper.** That band's content is entirely in the region where ADAA-1 is weakest, and it is being saturated independently. The spec's rationale for multiband — avoiding LF×HF intermodulation — is sound, but it concentrates the aliasing risk in the worst band.

**Named breaking signal.** A bright female vocal with a strong 8–10 kHz air component, driven into the HF band's shaper. Third-order products fold to 4–8 kHz, non-harmonically, sitting directly on the vocal. That is audible as grit that "gets worse the brighter the singer is" — the classic complaint about undersampled saturators.

**Required fix.**
1. Either raise the operating point to **ADAA-2 + 4× OS** for the HF band (and re-cost §6's 1.2% line), or
2. Restrict the alias gate honestly: state that −70 dBFS is met for input ≤ −6 dBFS and ≤ 10 kHz, and publish the measured alias floor as a **surface over (level, frequency)**, not a single number.
3. Add a gate row for the **multiband case specifically**, driving the HF band at its maximum drive.
4. Note also that ADAA's error is a function of `|x[n] − x[n−1]|`; the guard threshold `1e−5` (§4.12) is stated for float64 magnitudes. In float32 that threshold is only ~84 dB above epsilon and the ill-conditioned branch will be entered far more often than intended, on quiet material. Specify the threshold per working precision.

---

## B13. The true-peak oversampling rule is backwards, and "0 overs" is not provable with the specified architecture.

**The claim.** §4.16: "true-peak, computed on a **4× oversampled** signal — BS.1770-4 specifies ≥ 4× for TP estimation at 48 kHz; **use 8× above 96 kHz** or explicitly document the spec's known ~0.5 dB underestimate." §8.1 gate: "**0 overs** above ceiling across a 10 000-file corpus; ISP overshoot ≤ 0.1 dB."

**Failure 1 — the rule is inverted.** BS.1770's true-peak method targets an *effective* rate of ~192 kHz. That means:
- 48 kHz → 4× (→192 kHz)
- 96 kHz → **2×** (→192 kHz)
- 192 kHz → **1×**, none needed

The spec prescribes **more** oversampling at **higher** sample rates, which is exactly backwards, and wastes CPU where the problem is smallest. The residual underestimate — the ~0.5–0.7 dB the spec mentions — is a property of the **48 kHz / 4×** case, i.e. the case the spec treats as adequate, not the 96 kHz case where it prescribes 8×.

**Failure 2 — "0 overs" is unachievable with a 4× detector.** A 4× estimator systematically *underestimates* the true (infinitely-interpolated) peak by up to several tenths of a dB. Gating on "0 overs above ceiling" while detecting at 4× means you will pass the gate and still clip a downstream 8×-measuring meter (which is what mastering engineers and streaming platforms use). The gate measures the same estimator the limiter uses — it is marking its own homework.

**Failure 3 — the final clipper's decimation re-introduces ISP.** §4.16: "Gain applied at base rate…, **then a final 4×-oversampled ADAA soft clipper** catches residual inter-sample peaks without adding any lookahead." Clipping at 4× then decimating to base rate does **not** guarantee the ∞×-interpolated peak is under the ceiling: the decimation filter's band-limited reconstruction of a hard-cornered clipped waveform overshoots. This is the standard reason clipper-plus-decimator chains still produce overs on an 8× meter. And the anti-imaging/decimation filters themselves have latency (FIR) or phase distortion (IIR) — §4.16 claims "without adding any lookahead," which is only true for the IIR case, which is not linear-phase, which contradicts §4.16's own transparency argument.

**Failure 4 — the internal claim contradicts itself.** §4.16 says the gain is band-limited by the shaped attack so "no aliasing" — see N8; that is categorically false, multiplication is convolution.

**Required fix.**
1. Rewrite the rule: oversample to an **effective ≥192 kHz** (4× at 44.1/48 k, 2× at 88.2/96 k, 1× at 176.4/192 k).
2. Detect at **8×** at 44.1/48 kHz for the *gate* even if the limiter runs at 4×, so the measurement is stricter than the mechanism.
3. State an explicit **safety margin** between the internal ceiling and the user-facing dBTP ceiling (typically 0.3–0.5 dB) and justify it from the measured estimator error, or the "0 overs over 10 000 files" gate cannot pass.
4. Specify the clipper's up/down filters, their latency, and prove (by 16× measurement) that the post-decimation true peak is under ceiling.

---

## B14. The internal calibration that every threshold in the product depends on is derived from a 3-second LUFS-I measurement. It is a misuse of the metric and it is not stable.

**The claim.** §4.0: "over the **first 3 s of voiced material**, measure **LUFS-I** and store a `calibrationOffset` such that the chain's internal operating point is −18 LUFS. **All module thresholds are then specified relative to calibrated reference**, not in absolute dBFS."

**The failure.** This is the load-bearing pillar of the "our presets travel, iZotope's don't" claim. It is built on sand.

1. **LUFS-I is not defined for 3 seconds.** BS.1770's Integrated loudness is a *programme* measure with a two-pass gating procedure: absolute gate at −70 LUFS, then a relative gate at −10 LU below the ungated mean of the surviving blocks. Over 3 s at 400 ms blocks / 75% overlap you have ~27 blocks. Applying a relative gate to 27 blocks from a single phrase is statistically meaningless; the gate will either pass everything (no effect) or excise the phrase's own dynamics.

2. **The measurement is unstable by several LU.** Three seconds of a verse and three seconds of a chorus of the same take routinely differ by 6–10 LU. The offset is therefore a function of *which 3 seconds the plugin happened to see*. Since §4.0 makes every compressor threshold, gate threshold, de-esser target, suppressor threshold and rider target relative to this offset, **a ±3 LU calibration error shifts the entire chain by ±3 dB** — which is more than the total gain reduction range of Compressor A.

3. **Undefined behaviour is unspecified.** What is "voiced material" before the F0 tracker has warmed up? What happens if the first 3 s is a count-in, a breath, a guitar bleed, or silence? What if the user starts playback mid-phrase? What if they re-trigger analysis — does the whole chain's behaviour silently change under a preset the user already dialled in? None of this is in the spec.

4. **No latch / recall semantics.** For automation and session recall to work, `calibrationOffset` must be a **persisted, user-visible, user-overridable** value, latched at analysis time, saved in plugin state, and stable across a session reload. §4.0 treats it as an internal measurement.

**Named breaking signal.** A song that opens with a whispered intro line. Calibration latches on the whisper at −34 LUFS, offset = +16 dB. The chorus arrives at −8 LUFS, now presented internally at +8 LUFS-equivalent. Compressor B's threshold, being relative, is 26 dB low. The chorus is compressed to a pancake and the limiter is in permanent 20 dB gain reduction. The user's diagnosis will be "this plugin destroys loud vocals," and they will be right.

**Required fix.**
1. Use a **robust statistic over ≥ 30 s** of voiced material: e.g. the **median or 75th percentile of LUFS-S (3 s) over voiced frames**, not LUFS-I over 3 s. Specify the minimum voiced duration required before the offset is considered valid, and the neutral behaviour before then.
2. Make `calibrationOffset` a **first-class, persisted, displayed, overridable parameter** with defined behaviour on re-analysis (propose, don't silently apply).
3. Specify the fallback offset when analysis is impossible (silence, non-vocal, too short).
4. Add a §8.1 gate: for a fixed preset, the offset measured on the same take from 20 different start points must agree within **±1 LU**.

---

## B15. The input normaliser is gated by a speech-presence probability produced downstream of itself. This is a closed loop, and it creates the exact AGC runaway it claims to prevent.

**The claim.** §4.15a: input normaliser at stage 0.5, "very slow (τ = 1–3 s), range ±12 dB… **Gated by SPP so silence does not cause gain runaway (the classic AGC failure).**" SPP is produced by the neural model at stage 3 (§4.2 mod 6).

**The failure.** Stage 0.5 is *upstream* of stage 3. The normaliser's control signal is derived from a signal the normaliser has already modified. That is a feedback loop, and §4.15a does not acknowledge it, let alone analyse it.

The loop is unstable in a specific, realistic direction, because **neural SPP is level-sensitive.** DFN and its class are trained on a bounded input-level distribution; feed them material well below that distribution and SPP collapses toward zero, feed them material at or above it and SPP rises. So:

- Quiet input → SPP low → normaliser gated **off** → input stays quiet → SPP stays low. **The normaliser never engages on exactly the quiet home-recorded source it was designed for.** (Lock-out.)
- Or, tuned the other way: quiet input → normaliser boosts → boosted room tone now looks like speech-band energy to the model → SPP rises above 0.5 → normaliser un-gates and boosts further → room tone at −18 LUFS. (**Runaway.** The failure the paragraph claims to have solved.)

With τ = 1–3 s the loop is slow, so this presents not as oscillation but as **bistability**: the plugin behaves differently depending on how the session started, and the user cannot reproduce it.

**Named breaking signal.** A bedroom vocal recorded at −38 LUFS peak with audible laptop fan. On instantiation the normaliser is at 0 dB, SPP reads ~0.3 on the quiet input, the normaliser stays gated, the user hears no normalisation and every downstream threshold is 20 dB off. On the *next* take, recorded 8 dB hotter, the normaliser engages, SPP rises, and it drives to +12 dB — including on the fan. Two takes from the same session behave completely differently.

**Required fix.** Break the loop. The input normaliser's gate must come from a **level-invariant, open-loop detector computed on the pre-normaliser input**: e.g. spectral flatness + harmonicity + F0 confidence from the analysis rail's own tap (which is at IN and therefore correctly upstream), explicitly *not* from the neural SPP. State this as a rule: **no control signal may be derived from a point downstream of the module it controls, unless the loop is explicitly analysed and its gain margin stated.**

Then audit the rest of the chain against that rule. At least one other violation exists (B16).

---

## B16. Compressor A stacks three feedback loops with no stability analysis, and never states where the detector taps relative to auto-makeup.

**The claim.** §4.9: "**Topology: feedback (return-path) detection**, log-domain." Plus: "Detector… **sibilance-de-emphasised** — a dynamic −6 dB shelf at 5–9 kHz **keyed by the bus sibilance ratio**." Plus: "**Auto-makeup** derived from measured average GR, applied smoothly (τ = 500 ms)."

**The failure.** Three loops, nested:

1. **The compressor's own feedback loop.** Fine, well-understood, and the right choice for slow levelling. No objection.
2. **A time-varying sidechain filter inside that loop.** The detector's shelf is modulated by an external signal. A feedback loop with a time-varying element in the return path is not the classic feedback compressor; its effective ratio and release now depend on a third signal. No analysis is offered. (And per B5, the "bus sibilance ratio" is a stale input-tapped measurement — so the loop is modulated by a signal that does not describe its own input.)
3. **Auto-makeup, unclear tap point, 500 ms time constant.** This is the dangerous one. If the detector taps the output **after** makeup gain: GR rises → makeup rises → output rises → detector sees more → GR rises further. **Positive feedback with a 500 ms constant.** With a soft knee and a 1.5:1–4:1 ratio it will not run away outright, but it will produce a slow, self-reinforcing drift in operating point over several seconds — audible as the compressor "settling in" differently on every phrase, and as an unstable, non-reproducible gain-reduction meter.

The spec never says which side of the makeup gain the detector taps. For a feedback compressor this is *the* defining implementation detail and it is absent.

**Required fix.**
1. State explicitly: **the detector taps pre-makeup** (post-compression, pre-makeup). Draw the block diagram.
2. Provide a loop-gain analysis of the combined system (compressor loop × makeup loop), state the gain margin, and state the worst-case settling time.
3. Specify the sidechain shelf's modulation source as a **current, correctly-tapped** measurement (per B5), and bound its rate of change — a sidechain filter that moves fast inside a feedback loop is a modulator, not a filter.
4. Add a §8.1 gate: **operating-point reproducibility** — the same 10 s excerpt processed from 20 different start offsets must produce GR trajectories agreeing within ±0.3 dB after 2 s.

---

## B17. The "level-independent ratio" de-esser detector is destroyed by breathy and whispered material, which is a core modern pop vocal texture.

**The claim.** §4.11: `S_dB = 10·log10( E(4.5–11 kHz) / (E(200 Hz–3 kHz) + ε) )`, gated by `flatness_HF > 0.4 AND ZCR high`. "Because `S` is a *ratio*, the de-esser is **level-independent**… **This is the single largest available de-esser improvement and it is not hard.**"

**The failure.** It is level-independent. It is not *texture*-independent, and the failure is severe and common.

For a whispered or heavily breathy passage:
- `E(200 Hz–3 kHz)` **collapses** — there is little or no harmonic energy in the low-mid band; the voice is turbulent noise.
- `E(4.5–11 kHz)` **stays high or rises** — that is where breath noise lives.
- Therefore `S_dB` **spikes**, continuously, for the entire passage.

The guard terms do not help: a whisper is by definition **noise-like (high HF flatness)** and **high-ZCR**. The two gates that are supposed to discriminate sibilance from a vowel both *confirm* the false detection. All three conditions are satisfied for seconds at a time.

The `GR = (S_dB − S_target) × Amount` law then applies continuous reduction — not a 40 ms sibilant duck, a **multi-second shelf** on the exact frequencies that constitute the intended texture.

**Named breaking signal.** A modern intimate-pop verse: close-mic'd, whispered/breathy delivery, deliberately airy, sitting at −30 LUFS. The de-esser applies 6–12 dB of continuous 4.5–11 kHz reduction for the entire verse and then releases when the chorus arrives with full voice. The audible result is that the verse sounds dull and distant and the chorus "opens up" — an artefact the user will attribute to the compressor and never find.

§4.11's "Honest limitation" paragraph concedes that "no detector can distinguish an unwanted 's' from a deliberately bright, breathy, airy vocal texture." **That admission and the claim of "the single largest available de-esser improvement" are in the same module spec, two paragraphs apart.** The admission is correct; the claim is therefore overstated, and the detector as written fails in the admitted case rather than degrading gracefully.

**Required fix.** Add the two discriminants that actually separate the cases:
1. **Event duration gating.** Sibilants are **40–200 ms**. Require `S_dB` to be *transient*: reject any detection whose above-threshold duration exceeds ~250 ms, or high-pass the `S_dB` control signal (subtract a 1 s running median of `S_dB`) so the detector responds to **excess over the passage's own recent sibilance**, not to absolute ratio. This makes it texture-adaptive as well as level-adaptive, and it is the real version of the idea the spec is reaching for.
2. **Voicing / SPP term** from the bus, and an **onset-flux** term — a real "s" has a sharp onset; a breathy passage does not.
3. Add a **maximum duty cycle** (e.g. de-esser may not be active more than 25% of a rolling 3 s window at full amount) with a visible indicator when it saturates.
4. Add this signal class to the §8.3 excerpt set as a mandatory category.

---

## B18. The ML stage has no stereo or M/S strategy. The model is mono; the product is not.

**The claim.** §2.1: analysis rail is "control rate, **mono downmix**." §4.0 offers "mono / stereo / M-S." §6's budget is "single instance, **stereo**." §4.7 offers "M/S and L/R modes, stereo link 0–100%." The neural clean-up section (§4.2/4.3) never mentions channels at all.

**The failure.** DeepFilterNet is mono-in / mono-out. There are exactly three options and each has a named artefact, and the spec picks none of them:

1. **One instance on the mono downmix, gain field applied to both channels.** Cheapest, and it is what the §6 budget implicitly assumes (one 9% line, not two). Failure: on a stereo source — a double-tracked vocal, a stereo room pair, a stereo-widened lead — the *noise* is decorrelated between channels but the *gain field* is common. Suppressing L+R's summed noise estimate leaves the difference signal untouched, so the residual noise **collapses toward the sides**: you get a clean centre with a ring of residual hiss around it that breathes with the voice. This is a very recognisable artefact.
2. **Two independent instances.** Doubles the ML cost — §6's 9%/16% totals become 18%/25%, and §9.7's "12-vocal session spends over a core" becomes over two cores. Failure: the two gain fields are independently estimated, so the residual noise **wanders in the stereo image** frame to frame. Worse than option 1 perceptually.
3. **One instance on mid, one on side, or a stereo-linked gain field (max/min/mean of two estimates).** Correct answer, costs 2× inference plus a linking rule, and needs its own tuning.

Because §6 budgets one ML line for a stereo instance, the spec has silently chosen option 1 without saying so or acknowledging the artefact.

**Required fix.** State the channel strategy explicitly, per tier. Specify the gain-field linking law (and expose it, as §4.7 already does for the suppressor: "stereo link 0–100%"). Correct §6 and §9.7's per-session CPU arithmetic for whichever option is chosen. Add a **stereo-image stability** gate to §8.2: inter-channel coherence of the residual noise, and image wander measured as the drift of the correlation coefficient over time.

---

## B19. Auto-switching latency tiers on record-arm changes reported PDC mid-session. This is glitchy in VST3 and effectively prohibited in AAX.

**The claim.** §2.2: "Tier is a single global control and, where the plugin API allows, **auto-switches on host record-arm**." §8.1: "reported PDC == measured impulse delay, ±0 samples."

**The failure.** Latency reporting is not a free-running parameter in any major format:

- **VST3**: changing `getLatencySamples` requires a `restartComponent(kLatencyChanged)`, which forces the host to rebuild its processing graph. Most hosts respond by stopping and restarting audio. Doing this on record-arm — the exact moment the user is about to perform — produces a dropout at best. Some hosts ignore the change while the transport is rolling, in which case **PDC is silently wrong**, which fails the §8.1 gate.
- **AAX / Pro Tools**: latency is negotiated at instantiation. Dynamic latency change is not supported in the way this design needs and will not survive validation.
- **AU**: `kAudioUnitProperty_Latency` changes are advisory; host behaviour varies.

Beyond the format problem, tier switching swaps *implementations* (spectral suppressor ↔ filter-bank suppressor, DFN ↔ RNNoise, spectral de-esser ↔ split-band). §9.5 correctly notes these must be "tuned to sound similar" — but doing the swap **at record-arm**, live, means the user hears the chain change character at the moment they start singing.

**Required fix.**
1. Drop auto-switching. Make tier an **explicit, session-level, transport-stopped** setting, with a clear UI warning that changing it changes latency.
2. Alternatively — and this is the design that actually ships — run **fixed maximum latency in all tiers**, with the low-latency tiers padded to the same PDC. You lose nothing musically (the extra delay is compensated) and you gain a constant PDC. Only "true low-latency monitoring" needs the short path, and that is a separate, explicitly-entered mode.
3. Specify the format matrix (VST3 / AU / AAX Native / AAX DSP?) and the per-format latency semantics. It appears nowhere in the document.

---

## B20. Feature scope: the spec drops five things Nectar 4 ships, including two the brief itself identifies as the reason people buy Nectar.

§9.3 states the thesis plainly: "Beating Nectar 4 is ~20% DSP and **~80% Assistant + presets + UI**." The document then spends **~95% of its length on DSP** and does not specify the Assistant's UI, the preset system, the metering, or five shipping Nectar modules.

**Missing, with the consequence of each:**

1. **No Reverb, no Delay, no Dimension.** Nectar 4 ships all three. The VOX chain (§3) terminates at a limiter. A "complete vocal chain" with no time-based effects is not a channel strip; it is a corrective processor. Every A/B against Nectar will require the reviewer to add a second plugin, which reframes VOX as a *utility* rather than a *chain*. At minimum, specify a send-style reverb + delay with the analysis bus driving ducking (which would be a genuine differentiator: reverb send ducked by SPP and onset flux).

2. **No harmony generation (Nectar's "Voices").** The spec builds **F0, voicing, key/scale detection and formant frames** (§4.5) — every input a harmoniser needs — and then does not build the harmoniser. It also defers pitch correction (§9.4, defensibly). So the entire Pitch/Voices half of Nectar's feature surface has no answer, and the spec does not say what the user sees in its place.

3. **No Unmask / inter-plugin spectral ducking.** §1.1 identifies Unmask as a Nectar feature and then never returns to it. §9.9 dismisses it as "nothing to talk to" — but **the single-instance version needs no ecosystem at all**: an external sidechain input plus a spectral ducking gain field (which the §4.7 engine already computes) gives you vocal-vs-instrumental unmasking in one instance. This is low-cost, high-visibility, and directly answers a named competitor feature. Its absence is a scoping error, not a resourcing one.

4. **No reference-track / target-curve workflow.** §4.13 fits the LTAS "to a target curve." Where does the target come from? Nectar has Tonal Balance Control and a reference-track workflow; the spec has an unspecified curve. Specify: built-in genre targets, user-imported reference file with LTAS extraction, or sidechain-derived — and the analysis window, gating and normalisation for each.

5. **No product-layer spec at all.** Absent: preset format and migration; state serialisation and version compatibility (§8.3 demands "bit-exactness against the previous build" while defining no state contract); undo/redo; A/B compare; parameter automation model and smoothing; MIDI learn; offline-bounce determinism; GUI scaling; metering and visualisation. The last is the most damaging: §9.3 says UI is 80% of the win and the document contains **zero** words specifying it.

**Required fix.** Either (a) expand the spec to cover items 1–5 at the same level of rigour, or (b) state explicitly and in the executive summary that v1 is a **corrective/dynamics chain**, not a Nectar replacement, and that the competitive claim is scoped to the corrective half. Option (b) is honest and defensible. What is not defensible is a document titled "beat Nectar 4" that silently omits five of its modules.

---

# PART B — NON-BLOCKING CONCERNS

*Fix before ship; do not block the round.*

**N1. The Direct-Form-I claim is inverted.** §2.3: "DF-I has state discontinuity on coefficient change." DF-I's states are past **inputs and outputs** — physically meaningful quantities that do not depend on the coefficients — which makes DF-I the *most* robust direct form under coefficient modulation. **Direct-Form-II** is the one whose state is an internal variable that rescales when coefficients change, producing exactly the discontinuity described. The low-`fc/fs` coefficient-quantisation argument against DF-I is correct and sufficient; the state argument is attached to the wrong topology. *Fix: correct the sentence; the conclusion (use TPT) is unchanged.*

**N2. "The servo alone has no rolloff" is false.** §4.0. Subtracting a leaky integrator's output *is* a first-order high-pass at `1/(2πτ)` = **1.59 Hz** for τ = 100 ms. The combination is fine; the justification is wrong. *Fix: state the servo's actual corner and the combined response.*

**N3. The adaptive HPF clamp defeats the spec's own example.** §4.1: `fc = 0.72 × F0_p5`, clamped to **[50, 140] Hz**. The motivating example is "a soprano at F0 = 260 Hz keeps 200 Hz of pure mud" — but 0.72 × 260 = 187, clamped down to 140, so the soprano still keeps 140–200 Hz of mud. The clamp negates the benefit in the case used to justify the feature. *Fix: raise the upper clamp to ~200 Hz, or drop the example.*

**N4. The LPC order formula is arithmetically wrong and the method is wrong for 48 kHz.** §4.5: "LPC order `2 + fs/1000` **≈ 18 at 48 k**." 2 + 48000/1000 = **50**, not 18. The rule of thumb is `2 + fs_kHz`, and it is intended for 8–16 kHz speech (order 10–18). Order-50 autocorrelation LPC at 48 kHz is ill-conditioned and will produce unstable formant estimates. *Fix: decimate to 16 kHz for the formant analysis and use order 18 — which is the number the spec wanted.*

**N5. The cepstral-lifter "Sharpness" range is F0-dependent and the spec does not say so.** §4.7 step 2 maps Sharpness 0–10 to quefrency cutoff 0.5–3.0 ms. The harmonic comb sits at quefrency `1/F0`. At Sharpness 10 (3.0 ms cutoff), a singer at **F0 ≥ 333 Hz** has their comb *inside* the retained quefrency range — the "envelope" tracks the harmonics, `E[k] → 0`, and **the suppressor silently stops working**. At Sharpness 0 (0.5 ms), the envelope is smoother than the formants, so **every formant reads as a resonance** and gets notched. *Fix: make the lifter cutoff a function of the bus F0 (e.g. cutoff ≤ 0.6/F0_median), and re-map Sharpness onto the valid range. Also specify a floor on `log|X|` — near-zero bins produce unbounded negative logs that destroy the cepstrum.*

**N6. The gate's dual-branch `min()` produces the opposite of the stated behaviour.** §4.4: "fast (τ = 3 ms) and slow (τ = 200 ms), take the **minimum gain**… Fast enough to close between words, slow enough never to chatter." Taking the minimum means: during **closing** (gain falling) the fast branch is lower → fast close ✅; during **opening** (gain rising) the fast branch is higher → the slow branch wins → **the gate always re-opens slowly (200 ms)**. So a quiet consonant immediately after a loud syllable is attenuated for 200 ms — the "gate ate my consonants" failure the module exists to prevent. *Fix: restate the intended behaviour and the combination rule; probably you want `min` on close and `max` on open, i.e. an asymmetric dual-branch, and the SPP branch must be able to force a fast open.*

**N7. The compressor's gain-slew "hard limit" is itself the C⁰ discontinuity the document elsewhere identifies as the audible defect.** §4.10: "**Hard-limit** the gain slew to 0.35 dB/sample." A hard slew clamp produces a triangular gain trajectory with **derivative discontinuities at clamp entry and exit** — precisely what §4.10 and §4.16 both correctly identify as "the audible click/spit." *Fix: soft-limit the slew (tanh on the derivative) or low-pass the gain signal with a fixed 1-pole; either is C¹.* Separately, the claim "caps intermod products at approximately −70 dBFS" is asserted with no derivation and is not a standard result — **require the derivation and a measurement** before it is relied upon to eliminate compressor oversampling.

**N8. "Gain applied at base rate → no aliasing" is categorically false.** §4.16. Multiplication in time is convolution in frequency: a signal with content near Nyquist multiplied by a gain signal with *any* bandwidth produces content above Nyquist, which aliases. The effect is small when the gain is smooth — that is the real defence — but the stated reason is wrong and the magnitude is bounded nowhere. *Fix: state it as "aliasing bounded to X dBFS by the gain signal's Y kHz bandwidth," and measure X.*

**N9. LRA uses different gates than Integrated; as written it will be computed wrong.** §4.17 states "absolute gate −70 LUFS, relative gate −10 LU" and then "**LRA** per EBU Tech 3342." Tech 3342's LRA uses **3 s** blocks, an absolute gate of −70 LUFS and a **relative gate of −20 LU**, then takes the **10th to 95th percentile** of the surviving distribution. Implementing LRA with the Integrated gates will produce a systematically wrong number. *Fix: state both gate sets separately.*

**N10. §6's CPU budget for the resonance suppressor is understated by roughly 3–4×.** The line reads "2.5% — 2048-FFT every 256 samples ≈ 187 FFT/s/ch." Actual transform count per frame per channel:
- WOLA analysis: 1 forward FFT
- WOLA synthesis: 1 inverse FFT
- **Cepstral envelope (step 2): 1 forward + 1 inverse** — this is not counted at all
= **4 transforms per frame per channel**, × 187.5 frames/s × 2 channels = **1500 transforms/s**, before the LF path's own STFT and before the crossover FIRs. At ~40 µs per 2048-point real transform that is ~6% of a core in FFTs alone. Add B3's minimum-phase reconstruction (2 more) and it is ~9%. *Fix: rebuild §6 with a per-transform count. The suppressor, not the ML stage, may be the CPU story.*

**N11. §4.11 and §5 disagree about the de-esser.** §4.11 mode 3 (spectral) is described as the Mix-tier mode at "20–48 ms." §5's Mix column lists the de-esser at **3.0 ms**, i.e. mode 2. Pick one and make the tables agree.

**N12. ADAA's half-sample delay is incompatible with the ±0-sample PDC gate.** §4.12 introduces a 0.5-sample delay and proposes "a fixed 0.5-sample fractional delay on the dry path." §8.1 requires "reported PDC == measured impulse delay, **±0 samples**." A non-integer group delay makes integer PDC impossible and a fractional-delay filter is not exactly 0.5 samples across the band. *Fix: make the oversampled path's total delay an integer number of base-rate samples by construction.* Also: ADAA-1's HF rolloff is **level-dependent** (it is a derivative-based approximation), so the proposed "gentle HF shelf" compensation cannot be static.

**N13. Noise-floor re-injection breaks two of the spec's own gates unless it is specified more tightly.** §4.2 item 5 synthesises and injects noise. This (a) fails §8.1's "≤ −120 dBFS null with all modules at unity/neutral" unless re-injection is defined as off at neutral, and (b) fails §8.3's "bit-exactness check against the previous build" unless the synthesis uses a **seeded, deterministic PRNG with defined state on reset and on offline render**. *Fix: specify both.*

**N14. int8 quantisation of a GRU-based model with a complex deep-filter head is a poor bet.** §7.5: "Quantise to int8 where PESQ loss < 0.05 (typically the encoder; keep the deep-filter head in fp32)." DFN's cost is dominated by its **recurrent (GRU) layers**, where quantisation error accumulates in the hidden state across frames and manifests as slow drift and level-dependent behaviour — not as a clean PESQ delta. Quantising only the encoder convolutions targets the cheap part. *Fix: measure before committing; expect near-zero speedup, and validate on long files, not 5 s clips.*

**N15. The GPU rationale is wrong on half the target platforms.** §4.2: "GPU EP is *not* used — **PCIe round-trip latency** destroys the realtime budget." Apple Silicon has **unified memory and no PCIe** for the GPU/ANE. The conclusion (stay on CPU for realtime) may still be right — ANE scheduling is not realtime-safe and CoreML has its own dispatch jitter — but the stated reason is inapplicable. *Fix: give the platform-correct rationale, and evaluate CoreML/ANE for the offline "ML Freeze/Render" path (§9.7), where it is genuinely attractive.*

**N16. The listening-test protocol has three methodological problems.** §8.3:
- **12 listeners is thin.** BS.1534 expects ≥20 assessors *after* post-screening, and post-screening typically rejects 20–30%. Recruit ≥20.
- **No multiplicity correction.** "Non-overlapping 95% CIs on ≥12 of 20 excerpts" runs 20 simultaneous comparisons uncorrected. Use a **mixed-effects model** (listener and excerpt as random effects) or Holm correction, and **pre-register** the analysis before unblinding.
- **MUSHRA requires a true hidden reference.** For *enhancement* of real-world noisy sources there is no clean reference, so MUSHRA is formally invalid for the denoise conditions. *Fix: use MUSHRA only where a genuine clean reference exists (simulated-noise conditions), and use **ITU-T P.835 / P.808** for real-world sources, which is designed for exactly this and yields separate signal/background/overall scores.*

**N17. "CPU is flat from 44.1 k to 192 k" is false for the analysis rail as well as the ML path.** §2.1 argues flatness from a fixed 100 Hz control rate. But a 10 ms hop is 441 samples at 44.1 k and **1920 samples at 192 k**; to analyse the same 10 ms you need a proportionally larger FFT (or a decimation stage, which itself costs and is unspecified). FFT cost per second scales as `N log N / hop`, which grows with `fs`. *Fix: specify decimation of the analysis rail to a canonical 48 kHz (or 16 kHz for the F0/formant features), cost it, and add its latency to §5.*

**N18. The masking spreading function's upper slope must be level-dependent.** §4.7 step 4 gives "+25 dB/Bark lower, −10 dB/Bark upper" as fixed. The standard psychoacoustic form has a **level-dependent** upper slope, roughly `−(22 + 0.23·f_kHz⁻¹ − 0.2·L_dB)` dB/Bark. A fixed upper slope over-estimates masking at low levels — i.e. it will tell you a quiet resonance is masked when it is not, and the module will under-process quiet material. *Fix: use the level-dependent form.*

**N19. Compressor B's raised-cosine lookahead ramp is under-specified against a moving target.** §4.10 shapes "the gain trajectory over the lookahead window by a raised-cosine." Toward *what* target, when the required gain is itself changing within the window? Without a defined procedure this overshoots on dense material. *Fix: specify the standard construction — max-filter (running minimum of the gain) over the lookahead window, then smooth the result with the raised-cosine kernel — so the smoothed gain is guaranteed ≤ the required gain at every sample.*

**N20. Multiband LR4 in M/S is not mono-safe unless the M and S paths are coefficient-identical and identically driven.** §4.12 offers multiband saturation; §4.7 offers M/S. If M and S receive different drive or different dynamic gain, the sum is no longer magnitude-flat and mono-compatibility is lost. *Fix: state the mono-compatibility rule and add a gate: mono-sum of a neutral-settings stereo pass must null against the mono-sum of the input at ≤ −100 dBFS.*

**N21. The Assistant has no failure path.** §7.2 specifies features, model and training. It does not specify what happens when "Learn" is run on silence, on a full mix, on a drum loop, on a 2-second clip, or on a source outside the training distribution. §8.3's "catastrophic-failure rate ≤ 2%" gate is the right instinct, but with no defined abort/neutral path the model will emit *some* parameter vector for a drum loop and the user will hear it. *Fix: specify an input-validity classifier and a defined "cannot analyse — chain left neutral" state, and count abstentions separately from failures in the gate.*

---

# PART C — VERDICT

## **BLOCKED.**

Not conditionally. Blocked.

I want to be precise about why, because "blocked" on a document this competent needs justification. The chain-order reasoning in §3 is largely right — denoise-before-gate is correct, resonance-before-dynamics is correct, the two-point de-essing argument is genuinely good and is the best original idea in the brief, and the split of gain riding into an input normaliser and an output fader is a real improvement over Nectar's ALM-first placement. §9 shows a level of self-awareness that most specs never reach. This is not a bad document.

It is blocked because **four independent classes of defect each individually prevent the product from meeting its own stated goals**, and none of them are acknowledged in §9:

1. **The latency arithmetic is wrong, and it is wrong in the direction that breaks the central architectural premise** (B1, B2, B6). The analysis rail's latency is absent from the budget; the resonance suppressor's LF path is off by 7×; the ML resampling scheme's crossover is unbudgeted. The MIX tier is not 110 ms, and the LIVE tier as specified cannot exist. Every tier number in §2.2 and §5 must be recomputed before anyone writes code, because the tier structure determines which modules get built twice.

2. **The two headline differentiators do not work as specified.** F0-aware harmonic protection is a **no-op below 2 kHz** because its width is given in cents against 42.7 Hz bins (B4) — it fails on the exact signal used to justify it. And the "single shared analysis bus," the other structural claim, is tapped only at the input, so the output rider rides the wrong signal and every downstream detector keys on a stale spectrum (B5). These are the two ideas the executive summary says the product wins on.

3. **The ML plan is not costed and may not be executable.** $15k–40k is off by one to two orders of magnitude once the corpus is priced (B8). The total pool of commercially-clean sung-vocal audio in existence is ~20–40 hours against a stated requirement of 200. The noise corpus has the same problem and is not mentioned. And there is no realtime scheduling model for the inference at all — the CPU budget is derived from a **mean**-based metric (RTF) to satisfy a **99.9th-percentile** gate, using a number cited from the wrong model version (B7). This is a business-plan-level risk sitting inside a DSP document.

4. **The quality gates cannot detect the failures the design is most likely to produce, and two of them punish the design's best features.** PESQ-WB is blind above 8 kHz — it cannot see the air band the architecture is built to protect. STOI is blind above 4.3 kHz and measures intelligibility, which is not a quality axis for singing. And the SI-SDR ≥ 12 dB gate is in direct opposition to the −18 dB gain floor and the noise-floor re-injection, which are the two ideas most likely to make this sound better than the competition (B9). **Ship these gates and they will tune the product toward the artefact §4.2 exists to prevent.** A spec whose measurement plan drives it away from its own design intent cannot advance.

Plus B10's numerics (float32 cannot meet the −120 dB null gate), B11's mix-coefficient rule contradicting both the constant-Q option and the plosive tamer, B12/B13's aliasing and true-peak claims that fail their own test signals, B14/B15/B16's calibration and control-loop problems, and B20's five missing Nectar modules in a document whose stated purpose is beating Nectar.

### Conditions to reach CONDITIONAL PASS

I will re-review on a revision that delivers **all** of the following. Nothing here requires new invention; all of it requires arithmetic, measurement, and honesty.

1. **A corrected §5 latency table** with an explicit analysis-rail row, per-tier and per-buffer-size, including the ML frame-to-buffer pipeline delay and every crossover. Republished tier budgets. If LIVE cannot carry the analysis bus, say which differentiators are disabled there. *(B1, B2, B6, B7, B19)*

2. **A resonance-suppressor redesign** that states its true window lengths, its measured pre-echo, a minimum-phase gain-field reconstruction, and a bin-aware harmonic-protection kernel with the protected band stated per engine and per tier. *(B2, B3, B4, N5, N10)*

3. **A multi-tap analysis-bus specification** — tap points enumerated, features assigned to taps, staleness bounded where intentional, CPU recosted. Plus the control-loop rule ("no control signal from downstream of the module it controls") applied to the input normaliser and Compressor A, with block diagrams and gain margins. *(B5, B15, B16)*

4. **A numerics section that derives, not asserts.** Noise floor per topology per `fc/fs` corner; float64 states for all recursive filters; the mixing-form bell and shelf equations with their actual Q and corner laws; §8.1 EQ accuracy gated across the full gain range. *(B10, B11, N1, N2)*

5. **Measured aliasing and true-peak surfaces**, not single numbers. ADAA alias floor as a function of (level, frequency) for the multiband case; corrected true-peak oversampling rule (effective ≥192 kHz); an explicit ceiling margin justified by measured estimator error; 16×-verified proof that the post-decimation peak is under ceiling. *(B12, B13, N8)*

6. **An ML plan with three separate cost lines** (GPU, voice corpus, noise/IR corpus), a corpus acquisition strategy with a schedule and an owner, a stated no-third-party-weights-ship rule covering betas and demos, a channel/stereo strategy, and a realtime scheduling and threading model with its latency counted. *(B7, B8, B18)*

7. **A replaced §8.2.** PESQ/STOI/SI-SDR demoted to non-gating telemetry. Gates on ViSQOL-audio, PEAQ, DNSMOS-SIG, NISQA-discontinuity, HNR delta, vibrato rate/depth preservation, formant drift, MCD, musical-noise kurtosis ratio, pre-echo energy, and transient smearing. Test material stratified by failure class (fry, whisper, falsetto, scream, heavy vibrato, sustained held notes) and **scored per stratum, never pooled**. *(B9)*

8. **A calibration specification** that is robust (≥30 s, robust statistic), persisted, user-visible, user-overridable, with defined fallback and a reproducibility gate. *(B14)*

9. **A scope decision, stated in the executive summary.** Either specify reverb/delay/dimension, harmony, sidechain Unmask, the reference-track workflow, and the product layer (presets, state, automation, metering, UI) at the same rigour as the DSP — or explicitly rescope the competitive claim to the corrective chain and stop the document claiming it beats Nectar 4. *(B20)*

10. **The named-signal regression set**, built before implementation starts, containing at minimum: the breathy/whispered pop verse (B17), the belted tenor A3 with a 4th harmonic at 880 Hz (B4), the male 110 Hz legato phrase in a 180 Hz-mode room (B2), the whisper-intro/full-chorus song (B14), the stereo double-tracked vocal with decorrelated hiss (B18), and the bright female vocal with 8–10 kHz air into the saturator (B12). §9.6 says "**build the listening loop before building the features**." That is the best sentence in the document. Do it first, and make these six files the loop's first contents.

Item 10 is the one I would do on Monday morning. Everything else is arithmetic; that one is judgement, and it is the only thing that will tell you whether any of the rest of it worked.

---

## Verification notes

Independently checked during this review:

- **DeepFilterNet code licence** — README verbatim: "All code in this repository is dual-licensed under either: MIT License… Apache License, Version 2.0… at your option." ✅ Spec correct.
- **DeepFilterNet weights licence** — the README's licence clause covers *code* only; no weights clause, no commercial-use statement, no commercial contact. ✅ Spec's caution is correct, and B8 strengthens it: DFN3 is trained on **DNS4**, whose noise is largely AudioSet/Freesound-derived with mixed CC terms including NC and SA.
- **DFN3 metrics** — Interspeech 2023 table: DFN 2.81 / DFN2 3.08 / **DFN3 3.17** PESQ; STOI 0.944; CSIG 4.34 / CBAK 3.61 / COVL 3.77 on VoiceBank+DEMAND. ✅ Spec correct.
- **DFN3 latency** — paper verbatim: "48 kHz… 20 ms windows with a hop size of 10 ms… look-ahead of 2 frames resulting in an overall latency of 40 ms." ✅ Spec correct.
- **DFN3 architecture** — 32 ERB bands from 481 bins; N=5 deep filter applied to the **lowest 96 bins, i.e. up to 4.8 kHz**. ✅ Spec correct (its "~5 kHz" is a rounding).
- **RTF 0.19** — ❌ **misattributed.** 0.19 is DeepFilterNet **v1**, repeated in the umbrella paper's abstract. **DeepFilterNet2 reports RTF 0.04** on the same i5-8250U, and DFN3 is described as "the slightly modified DeepFilterNet model" trained on full multilingual DNS4. See B7.
- **DFN3 training data** — paper verbatim: "the **full multi-lingual DNS4 dataset**" with PTDB and VCTK oversampled 10×.
- **MUSDB18-HQ licence** — verbatim: "provided for educational purposes only and the material contained in them should not be used for any commercial purpose without the express permission of the copyright holders." Composed partly of MedleyDB (CC BY-NC-SA 4.0) and Easton Ellises (CC BY-NC-SA 3.0). ❌ **Not commercially usable.** See B8; this also sharpens the spec's own §7.3 caution about HTDemucs weights.

### Sources

- [Rikorose/DeepFilterNet — GitHub](https://github.com/Rikorose/DeepFilterNet) · [README (raw)](https://raw.githubusercontent.com/Rikorose/DeepFilterNet/main/README.md)
- [Schröter et al., "DeepFilterNet: Perceptually Motivated Real-Time Speech Enhancement," Interspeech 2023 (PDF)](https://www.isca-archive.org/interspeech_2023/schroter23b_interspeech.pdf) · [arXiv:2305.08227](https://arxiv.org/abs/2305.08227) · [PDF](https://arxiv.org/pdf/2305.08227)
- [Schröter et al., "DeepFilterNet2," arXiv:2205.05474 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2205.05474) · [PDF](https://arxiv.org/pdf/2205.05474)
- [MUSDB18-HQ — Zenodo record 3338373 (licence terms)](https://zenodo.org/records/3338373)
- [M4Singer — GitHub](https://github.com/M4Singer/M4Singer)
- [microsoft/DNS-Challenge — GitHub](https://github.com/microsoft/DNS-Challenge)
- [Recommendation ITU-R BS.1770-5 (11/2023) — PDF](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf)
- [AES — Learn More: Peak Metering](https://aes2.org/resources/audio-topics/loudness-project/learn-more/)
- [True Peak Measuring: Is it really that simple? — JUCE forum](https://forum.juce.com/t/true-peak-measuring-is-it-really-that-simple/52601)
- [The problem of true peak estimation — Essentia notebook](https://notebook.community/carthach/essentia/src/examples/tutorial/example_truepeakdetector)
- [GTSinger: A Global Multi-Technique Singing Corpus — NeurIPS 2024 (PDF)](https://proceedings.neurips.cc/paper_files/paper/2024/file/023d2c1a17cf35b11a0cbb43a0677c91-Paper-Datasets_and_Benchmarks_Track.pdf)
