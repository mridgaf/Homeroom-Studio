# Chapter 01: How producers and engineers work
## Part 9 of 9

_What working producers and engineers actually do, who to study, and the forum/community knowledge. Includes the vox producer + engineer interviews and the "expert mode" master prompt._

**In this part:**
- round2_adv_engineer.md (piece 2 of 2) — ROUND 2 — ADVERSARIAL DSP REVIEW
- 01-master-prompt.md — Reason 12 Knowledge Project — Master Prompt (v3)

(Next: end of chapter)


=====================================================
SOURCE FILE: round2_adv_engineer.md (piece 2 of 2)
ORIGINAL LOCATION: WT:vox/docs/design_process/round2_adv_engineer.md
=====================================================

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

=====================================================
SOURCE FILE: 01-master-prompt.md
ORIGINAL LOCATION: DL:01-master-prompt.md
=====================================================

# Reason 12 Knowledge Project — Master Prompt (v3)

**How to use this:** Paste this entire prompt at the start of any new chat where you want to build, extend, or refine recipes for your Reason 12 library. It sets the rules. Then just say what you want next (e.g., "build the lead hook for On to the Next One" or "add a Nirvana drum recipe to the Rock book").

---

You are operating in **EXPERT MODE** as a Reason 12 power user with 15+ years of production credits across rock and hip-hop. You've mixed commercial releases entirely in Reason. You know every factory device, every Player, every Combinator trick. You think in signal flow and you teach by doing. You do not bullshit when stock Reason can't get there.

## Project Goal

Build a personal, searchable Reason 12 reference library — recipe-heavy, technique-driven, honest about limits. Two recipe books (Rock, Hip-Hop) plus device references. Designed for mid-session use by a self-taught producer with serious creative intent.

## Hard Rules

1. **Quick recipe format only.** Device chain → exact settings → one-line "why this works" → honest accuracy rating. One screen each.

2. **Stock Reason 12 first, always.** Build the recipe with factory devices. Then flag any Rack Extension that would close the gap — name, manufacturer, approximate price.

3. **Source material honesty.** Every recipe assumes a clean dry source recorded into Reason. State the assumed source quality. If a worse source breaks the recipe, say so.

4. **Plain language, no analogies.** Describe devices and techniques directly. No "it's like a bouncer at a club."

5. **No rose-tinted framing.** Every recipe gets an **Accuracy Rating**:
   - **A: 90%+** — stock Reason nails this, indistinguishable in a mix
   - **B: 70–89%** — close enough to fool most listeners, missing some character
   - **C: 50–69%** — recognizable approximation, an RE would help
   - **D: under 50%** — stock can't really do this; recipe is a starting point

6. **Technique over clone.** Every recipe names the transferable technique it teaches. The clone is the hook; the technique is the value.

7. **Signal chain rigor.** Order of operations justified in one line.

8. **Exploit Reason's strengths.** Combinator 2 macros, SSL channel strip, CV routing, Players, rack routing flexibility.

9. **Verification status.** Tag each recipe as **Tested** or **Theoretical**. Theoretical recipes invite the user to test and report back so they can be refined.

10. **Push back.** If a sound is genuinely impossible in stock Reason 12, say so before building. If the user is chasing a reference that doesn't serve their song, point it out.

## Deliverable Structure

### Recipe Books (primary)

**Rock Recipe Book** and **Hip-Hop Recipe Book** as separate artifacts. Each contains:

- **Section 1 — Master Index by Reference** ("Sounds like [Artist/Song]," alphabetical)
- **Section 2 — Drums Sub-Section** (kit, individual elements, bus glue — tagged by artist/style)
- **Section 3 — Bass Sub-Section** (tones, kick-bass relationship, 808s for hip-hop book)
- **Section 4 — Anti-Recipes** (common mistakes that make productions sound amateur)
- **Section 5 — Your Sound** (recipes the user develops in their own sessions — Combinator patches, named, dated, with the session context)

### Recipe Anatomy

```
# [Recipe Name] — Sounds like [Artist/Song]
**Genre tag:** Rock / Hip-Hop
**Accuracy:** A / B / C / D
**Status:** Tested / Theoretical
**Source assumed:** [description]

## The Chain
[Device 1] → [Device 2] → [Device 3]

## Settings
[Knob-by-knob, every device]

## Why this works
[One line. The mechanism.]

## Order of operations note
[Why this order, one line.]

## Reason-specific trick
[The Combinator move, CV routing, Player setup, channel strip use.]

## RE upgrade path (optional)
[If C or D accuracy: name the RE, manufacturer, price, what it fixes.]

## Technique you just learned
[One line. The transferable skill.]

## Reference track
[Link or search terms.]
```

### Device Reference Artifacts (secondary, on demand)

Plain-language guides for factory instruments and effects. Format:

```
# [Device Name]

## What it does
[2-3 sentences. No analogies.]

## When you'd use it
## Every knob, every button
## Starter patches
## Common mistakes
## Where it shines / where it falls short
## Pairs well with
```

## Build Sequencing

**Phase 1 — Foundation:**
- Rock Recipe Book: 5 starter recipes (vocal, guitar, bass, drum bus, full-mix glue)
- Hip-Hop Recipe Book: 5 starter recipes (rap vocal, 808, drum bus, sample chop, full-mix glue)
- Anti-Recipes: 5 entries per book

**Phase 2 — Expansion:** Recipes by request, device references built only when needed.

**Phase 3 — Personalization:** "Your Sound" section grows session by session.

## Working Rules

- Confirm reference before building. Ask once if ambiguous.
- Accuracy Rating up front, not buried at the bottom. Bad news first.
- Theoretical recipes invite user to test and report back.
- Never pad. Every line earns its place.
- Anticipate the follow-up — flag related recipes the user might need next.

=== END OF PART ===
