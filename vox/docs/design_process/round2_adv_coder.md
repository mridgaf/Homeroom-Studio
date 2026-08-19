# ROUND 2 — ADVERSARIAL ARCHITECTURE REVIEW
## Target: `round1_coder.md` (VOX — Coder's Design Document)

**Reviewer:** THE ADVERSARIAL SOFTWARE ARCHITECT
**Authority:** Veto. This document does not advance to implementation until the BLOCKING items below are closed in writing.
**Verdict:** **BLOCKED** (see §6 for the conditions that convert this to a conditional pass)

---

## 0. What is actually good here, stated once so I never say it again

The Stage/Param/Chain spine, the `HopBuffer` block-size-independence rule, the import-policy AST test, the `assistMin/assistMax` cage as a *product* concept, §5's "where the prototype will lie to us," and the refusal to build an end-to-end neural mixer are all correct and above the category average. The document is not naive. That is precisely why it is dangerous: it reads as complete, and the things it is missing are the things that kill plugin projects in month 14 rather than month 2.

Everything below is a concrete failure with a named mechanism. No style preferences.

---

# 1. BLOCKING OBJECTIONS — REAL-TIME SAFETY

### B1. There is no RT-safe structural reconfiguration path, and the design requires one on every preset load.

**Claim under attack:** §1.4 — "`setState(json)`: Params only. Never touches DSP state. Applied via the param FIFO so it's ramped, not stepped."

**Why it fails:** The preset format in §3.4 is not a flat param vector. It contains:
- `eq_static.params.nodes` — a **variable-length array** (2 nodes in the example, up to 4+ from the assistant).
- `eq_dynamic.params.nodes` — same.
- `deesser.params.mode: "split"` — a topology switch (split-band vs wideband are different signal graphs with different latencies).
- `"oversample": 4` — a **per-stage structural decorator**.
- `denoise.params.model: "denoise_v1"` — a model identity, i.e. a different ONNX graph with different IO shapes.
- `gate.params.lookahead_ms`, `limiter.params.lookahead_ms` — latency-bearing.

None of these can travel through a `SpscRing<ParamProposal>` of `(uint32_t paramIdx, float native)`. Loading a preset that changes node count or de-esser mode requires constructing and `prepare()`-ing new objects — allocation, off the RT thread — and then *swapping* them into a chain that the RT thread is actively reading. The design has no such mechanism. There is no double-buffered chain, no atomic chain-pointer swap, no reclaim queue to return the retired chain to the message thread for destruction, and no crossfade across the swap.

**Concrete failure:** User is playing back, clicks a factory preset that has 4 EQ nodes instead of 2 and `deess.mode: wideband`. Either (a) the message thread mutates `stages[]` while `Chain::process` iterates it — use-after-free / torn `std::vector` under the audio thread, a hard crash in front of the customer; or (b) the message thread takes a lock and the audio thread blocks on it — dropout; or (c) preset loading is deferred to `prepare()`, which means every preset change causes a full re-prepare, a PDC renegotiation, and an audible gap. All three ship as bug reports.

**Same failure, second path:** the assistant. §2.4 emits "at most 4 nodes" of surgical EQ with `(freq, gain, Q, dynamic:bool)`. `proposeParam(uint32_t paramIdx, float native)` cannot express "create a node." So the assistant's single highest-value output — the feature the strategy note in §6.3 says is the entire wedge against Nectar — has no transport to the audio thread.

**Required fix:**
1. Fixed structural capacity, always instantiated: exactly N static EQ nodes, M dynamic nodes, both de-esser topologies, the oversampler, all permanently present and `prepare()`d, with "disabled" expressed as gain 0 / mix 0 / bypass-with-matched-delay. Structural variability becomes parameter variability. State this as a hard rule and accept the permanent CPU cost (see B18).
2. For anything that genuinely cannot be pre-instantiated (ML model swap, sample-rate change), a formal **prepared-object handoff**: build off-RT → publish via a single `std::atomic<Chain*>` release-store → RT acquire-loads once per block → retired object pushed to a reclaim SPSC ring drained by a timer on the message thread. Never `delete` on the audio thread. This is a real subsystem, roughly 2–3 person-weeks, and it is nowhere in the WBS.
3. `setState` while transport is running must apply as one atomic generation flip at a block boundary with an equal-power crossfade over ~20 ms, not as a stream of independent FIFO writes.

---

### B2. Parameter handoff is torn. The three-layer resolve reads three unrelated relaxed atomics.

**Claim under attack:** §1.2 `Param::updateBlock()`:
```cpp
float user   = denormalize(userNorm.load(std::memory_order_relaxed));
float assist = assistTarget.load(std::memory_order_relaxed);
float amt    = assistAmount.load(std::memory_order_relaxed);
```
and §1.8 `drainProposals()` writing one `(paramIdx, value)` at a time.

**Why it fails:** The assistant does not produce independent scalars. §2.4 explicitly Newton-solves `comp.threshold` *against* `comp.ratio` and the measured histogram, and solves `deess.threshold` to hit a target GR at a given `deess.freq`. These are **coupled solutions**. Delivering them as independent atomic stores, drained by a bounded per-block loop, guarantees that some blocks see threshold from solution N and ratio from solution N+1.

**Concrete failure:** Assistant re-solves during a loud chorus. Old solution: `threshold −18, ratio 3.0, makeup +3`. New solution: `threshold −30, ratio 1.6, makeup +9`. The proposal ring is drained mid-set (or the RT thread's block boundary falls between two of the analysis thread's stores). One block runs `threshold −30, ratio 3.0, makeup +9` → roughly 14 dB more gain reduction *plus* 9 dB of makeup on a signal that is already near 0 dBFS. That is an audible slam followed by limiter overshoot, once, unreproducibly, ten minutes into a session. This is the exact class of bug that gets logged as "the AI randomly makes it loud sometimes" and is never reproduced by the developer.

**Required fix:** The assistant's output is a **snapshot**, not a stream of scalars. Double-buffer a POD `AssistFrame { uint32_t generation; float values[NUM_ASSISTABLE_PARAMS]; }`, publish by `std::atomic<int> liveIndex` release-store, RT acquire-loads the index once per block and reads that buffer for the whole block. Per-param atomics may remain only for genuinely independent GUI-driven user values. Also: `drainProposals` as written is an unbounded RT loop proportional to producer rate — cap it, or delete it in favour of the snapshot.

---

### B3. Sample-accurate automation is silently discarded, and the flagship test suite cannot detect it.

**Claim under attack:** §1.2 — "Called ONCE per block on the RT thread." §3.6 — `assert_block_size_invariant` is "THE most valuable test in the suite."

**Why it fails:** VST3 (`IParameterChanges` with sample offsets), AU (`AudioUnitScheduleParameters` with `inFramesToProcess` offsets) and AAX all deliver parameter changes **with sample offsets inside the block**. The design collapses every change to the block boundary and then ramps with `LinearSmoothedValue` over `smoothMs`. Two consequences:

1. **Automation renders differently at different block sizes.** During an offline bounce many hosts use 1024–4096-sample blocks; Logic's freeze and Pro Tools AudioSuite use larger. A filter-sweep automation drawn on `eq.node[0].freq` quantises to 21 ms at 1024 and 85 ms at 4096. The bounce does not match playback. This is the single most common "your plugin is broken" support ticket in the industry.
2. **`assert_block_size_invariant` renders with static parameters.** It will pass at −140 dB while automation is completely block-quantised. The document's own most-valued test provides false confidence about the exact property it claims to protect. §5.8's `--automate` LFO mode is mentioned as a mitigation for zipper noise but is not wired into the block-size invariance assertion, so nothing in CI compares *automated* renders across block sizes.

**Required fix:**
1. `Param` gains a small per-block event queue `(sampleOffset, normalizedValue)`; `Chain::process` slices the block at event boundaries (a `SampleAccurateSlicer` in the framework, mirrored in Python) or the smoother is advanced with an initial offset. Pick one and make it a framework guarantee, not a per-stage choice.
2. `assert_block_size_invariant` must run in `--automate` mode as its primary configuration, not as an optional extra. Static-parameter invariance is the easy half.
3. Note the tolerance: `tol_db=-140` is below float32 relative precision. The C++ Catch2 mirror of this test will fail on any SIMD path whose chunking depends on block size, and will then be quietly relaxed to whatever passes. Set it now, honestly: bit-exact for the pure-scalar stages, −120 dB for SIMD/FFT stages, and require a written justification for any stage that needs more.

---

### B4. The `assistMin/assistMax` cage — described as "enforced by the framework, not by discipline" — is not enforced by the framework.

**Claim under attack:** §1.2 rule 4 vs the reference implementation two code blocks above it:
```cpp
float target = std::clamp(user + amt * (assist - user), desc.min, desc.max);
```
It clamps to `desc.min/desc.max`. `assistMin/assistMax` never appear in `updateBlock()`, in `setAssistTarget()`, or anywhere else in the document.

**Concrete failure:** A bug or an out-of-distribution profile (a heavily clipped phone recording, an all-silence take with a divide-by-near-zero in the `deess.threshold` solve) produces `assist = -18 dB` on an EQ node whose cage is ±6 dB. Nothing stops it. The document names this exact scenario — "the assistant physically cannot make a -18 dB EQ cut even if the rules say so" — and then ships code that permits it.

**Required fix:** Clamp at the ingress point (`setAssistTarget` clamps to `[assistMin, assistMax]`) *and* in `updateBlock`, and add a unit test per assistable param that drives `setAssistTarget` with ±1e9, NaN, and −0.0 and asserts the resolved target stays in the cage. NaN handling in particular: `std::clamp(NaN, lo, hi)` returns NaN on every mainstream implementation, and one NaN in a recursive filter poisons the instance until `reset()`. The Hypothesis property test in §3.6 tests the *rules*; it does not test the *transport*.

---

### B5. Two concrete interface defects: the scratch arena is unreachable, and `StageContext` is rate-wrong under `Oversampled`.

**5a — scratch memory.** §4.3 prescribes "a per-instance `ScratchArena` (bump allocator over a fixed buffer) handed to stages." The `Stage` interface is `process(AudioBlock& io, const StageContext& ctx)`. There is no arena in either argument, and `prepare(const PrepareSpec&)` doesn't carry one either. Every stage that needs a temp buffer therefore has to own its own preallocated members sized to `maxBlockSize` — which is fine, but it is a *different* design, it multiplies memory per instance (16 instances × ~20 stages × several `maxBlockSize` buffers × oversampled sizes), and it contradicts the stated mitigation. Pick one and put it in the interface signature.

**5b — sidechain and position are at the wrong rate inside the oversampler.** `Oversampled::process` upsamples `io` and calls `inner->process(up, ctx)` with the **unmodified** `ctx`. `ctx.sidechain` is an `AudioBlock*` at the *base* rate with `numSamples = n`, while `up.numSamples = n * factor`. Any oversampled stage that reads the sidechain — a saturator with sidechain-driven drive, an oversampled compressor, anything in a `ParallelSplit` — reads `n` samples where it needs `4n`, or reads past the end of the sidechain buffer. Best case it sounds wrong; worst case it is an out-of-bounds read on the audio thread. `ctx.samplePosition` is likewise at base rate, so any stage using it for analysis timestamps inside the oversampler is off by a factor of 4.

**Required fix:** `Oversampled::process` must construct a rate-adjusted `StageContext` (upsampled sidechain — which means the oversampler must upsample the sidechain too, at real CPU cost, or the interface must forbid sidechain reads inside oversampled stages and assert it in debug). Decide explicitly. Also add an `int oversampleFactor` to `StageContext` so a stage can tell.

---

### B6. The ML worker design makes renders non-deterministic, and offline bounce will not match playback.

**Claim under attack:** §4.5 option 1 — "Fallback on underrun is mandatory: if the mask isn't ready, apply the previous mask… Audio never waits."

That is the correct real-time policy and the wrong *product* policy, because the document never separates the two cases.

**Concrete failure 1 — offline bounce.** During an offline render the host calls `processBlock` as fast as the CPU allows: 20–200× realtime. The ML worker thread runs on wall-clock and cannot possibly keep up — it will underrun on essentially every frame. The output is therefore "previous mask, forever," i.e. the denoiser and dereverb are effectively frozen or off. **The bounce sounds different from what the user heard.** This is not a subtle artifact; on a noisy source it is the difference between a clean vocal and a hissy one. It is also completely reproducible, so it will be found by the first beta tester and it is a v1-blocker.

**Concrete failure 2 — non-reproducibility.** Two consecutive realtime renders of the same material with the same preset produce different audio, because the number and placement of underruns depends on thread scheduling. This destroys: A/B null testing, the golden regression suite in C++ (`voxrender` vs Python), customer-side "render twice and null" verification, and any support workflow that relies on reproducing a report.

**Concrete failure 3 — Pro Tools AudioSuite.** AudioSuite is offline by definition and hands you enormous buffers. The worker-thread pipeline plus the assistant thread has no defined behaviour there at all.

**Required fix:**
1. `AudioProcessor::isNonRealtime()` must select a **synchronous inference path**: on the audio thread, blocking, allocation-permitted, with the identical hop alignment and identical declared latency as the realtime path. This is not optional and it is not free — it is a second execution path through the ML stage that must be tested for bit-parity of latency and for equality with a "realtime path with zero underruns" reference.
2. The realtime path must expose a per-render **underrun counter** in the UI and in the state, and the golden/CI renders must assert zero underruns or be run through the synchronous path.
3. Freeze/bounce in Logic and Live also set non-realtime; verify per host, because several hosts lie about it. Add that to the DAW matrix.
4. The same rule applies to the *assistant* thread in continuous "learn" mode: during a non-realtime render, the assistant must either be frozen at its last state (deterministic) or run synchronously. "It drifts differently every bounce" is not shippable.

---

### B7. "Dropping frames is correct behavior" is false for two of the named estimators, and there is no epoch/flush on transport jump.

**Claim under attack:** §1.8 — "If the analysis thread stalls, the ring fills, `publish` drops… The assistant just gets slightly stale statistics, which is fine because all its estimators are long-window anyway."

**Why it fails:**
- **Martin minimum statistics (F5)** estimates the noise floor as the minimum of a smoothed periodogram over a fixed-length sliding window, with a bias-compensation factor that is a documented function of the *number of observations in the window*. Randomly dropping frames changes the effective window occupancy, which biases the minimum upward and makes the bias compensation wrong. The result is an **overestimated noise floor**, which feeds `gate.threshold = noise_floor + 8 dB` and `denoise.amount = (30 − SNR)/20`. An overestimated floor means the gate threshold rises into the singer's quiet tails and chops them. That is the most complained-about failure mode of every automatic gate ever shipped.
- **BS.1770-4 integrated loudness (F2)** is defined over contiguous 400 ms blocks with 75% overlap and a two-stage gate. Missing blocks change LUFS-I directly. `out.gain = target_lufs − lufs_i_after_chain` then applies a wrong broadband gain.

- **Transport jump.** `reset()` is specified as "MUST NOT allocate" and zeroes DSP state. It says nothing about the two SPSC rings. After a locate from bar 90 to bar 1, the rings still contain up to 512 `FeatureFrame`s from bar 90 (at hop 512 @48k that's 5.5 seconds of buffered history) and the proposal ring contains decisions derived from them. The assistant will apply chorus settings to the intro. And you cannot naively "clear" a lock-free SPSC ring from the consumer side while the producer is writing without defining exactly who moves which index.

**Required fix:**
1. Add `uint32_t epoch` to `FeatureFrame` and to `ParamProposal`. RT increments the epoch on `reset()`/discontinuity; both consumers discard mismatched epochs. This is an RT-safe flush without touching the other side's index.
2. Add an explicit `droppedFrames` counter published by the RT side. Any estimator whose validity depends on contiguity (minimum statistics, BS.1770, LRA percentiles, RT60 backward integration) must **invalidate and restart** when drops occur rather than silently absorbing them, and must lower its confidence field — which the design already has the machinery for (§2.3 "Low confidence ⇒ the assistant does nothing").
3. Size the feature ring for latency, not capacity: 8–16 frames with drop-*oldest*, not 512 with drop-newest. A 5.5-second-stale assistant is worse than a lossy one.

---

### B8. There is no mechanism for the thing the sibling engineering document calls non-negotiable: analysis→audio delay alignment.

`round1_engineer.md` §2.1 states: "The audio rail is delayed by the analysis rail's algorithmic latency… so every detector decision is **available before the sample it applies to arrives**. This is what makes attacks inaudible without per-module lookahead stacking."

The coder's `AnalysisBus` is **asynchronous by construction**: RT publishes into a ring, another thread pops at its own rate, decisions come back through a second ring drained "once/block." There is no sample alignment, no bounded delivery time, and no way for a stage to consume an analysis result that is time-locked to the sample it is processing. `StageContext::analysis` is explicitly documented as write-only for stages ("where stages PUBLISH measurements (**never read decisions here**)").

Consequently:
- The "one shared STFT" claim in §1.8 is **unimplementable through the Stage interface as specified**. Denoise, dereverb, de-esser, dynamic EQ and the resonance suppressor each need a spectrum *now*, aligned to the audio they are processing. With no read path, each stage builds its own `HopBuffer` + FFT — which is exactly the "four STFTs of the same signal" failure the document names as "the #1 way vocal chains end up at 25% CPU." The file tree in §3.1 confirms this: `denoise.py`, `dereverb.py`, `deesser.py`, `eq_dynamic.py` are independent stages with no shared front-end object.
- The two documents describe two different architectures. One has a synchronous, delay-aligned control rail; the other has an asynchronous, best-effort message bus. They cannot both be built.

**Required fix:** Split the concept in two, explicitly, with different rules:
- **Control rail (synchronous, RT thread, deterministic):** one STFT + feature extraction running on the audio thread inside a `HopBuffer`, published into a plain struct that downstream stages **read** during the same `process` call, with the audio rail delay-matched to it. This is what feeds de-essing, dynamic EQ, resonance suppression, gate, compression detectors. Its latency is real and must be in the budget.
- **Assistant bus (asynchronous, best-effort):** the existing SPSC design, feeding only the slow, non-sample-critical decision layer (target curves, thresholds, styles) via the B2 snapshot.

`StageContext` gains a `const ControlFrame* control` pointer. This is a genuine architectural change, not a refactor, and it is the single largest structural gap in the document.

---

# 2. BLOCKING OBJECTIONS — LATENCY

### B9. The denoise/dereverb latency is understated by roughly 4×. Both published latency targets are unachievable as specified.

**Claim under attack:**
- §1.3 — "`HopBuffer` … Costs exactly `hopSize` samples of latency."
- §1.5 — "FFT denoise / dereverb: `hopSize` (from `HopBuffer`) + any internal frame delay."
- §4.5 — "Added latency = `hopSize × queueDepth`. With hop 256 @48k and depth 2 ⇒ **10.7 ms**."
- §2.1 — "Frame: 2048 samples @ 48 kHz, hop 512 … √Hann analysis + √Hann synthesis with hop = N/4."

**Why it fails:** `hopSize` is the correct latency for a *non-overlapping frame processor* (accumulate H samples, process, emit). It is **not** the latency of a weighted-overlap-add STFT processor. With analysis window `N` and hop `H` and WOLA synthesis, an output sample is not complete until every overlapping synthesis frame that contributes to it has been produced. That requires the analysis frame whose *right edge* is `N` samples ahead. Algorithmic latency is therefore `N` (or `N − H` depending on the exact indexing convention), not `H`.

For the document's own numbers — N = 2048, H = 512 @ 48 kHz — that is **42.7 ms, not 10.7 ms**. The sibling engineering document independently budgets "Neural clean-up: 40.0 ms" in its Mix tier, which corroborates the correct figure and contradicts this one.

**Downstream consequences, all of them breaking stated product constraints:**
- §5.11: "a test asserts the default preset's latency is **< 15 ms**." The default preset in §3.4 contains a `denoise` stage. With the correct WOLA latency the denoise stage alone is 42.7 ms. The default preset cannot meet 15 ms. The test as written would have failed on day one and been "fixed" by changing the number.
- §5.11: "a 'low latency' mode exists at **< 5 ms** with the linear-phase/ML/lookahead stages auto-swapped for causal alternatives." A 5 ms total budget permits a ~128-sample analysis window at 48k — that is a 375 Hz frequency resolution, which is useless for a per-band denoise mask on a vocal (F0 is 80–400 Hz; you cannot resolve harmonics). The "causal alternative" is not a tuning of the same algorithm, it is a **different algorithm** (RNNoise-class time-domain, or a low-order filter-bank suppressor), i.e. a second denoiser to build, tune and QA. There is no line item for it.
- Total chain latency: the engineer's own table sums to **110 ms** in Mix tier. Nothing in the coder's document acknowledges a three-digit millisecond figure or its consequences (PDC interaction with sidechained instruments, monitoring workflow, the "assistant explains itself" UI needing to be latency-compensated too).

**Required fix:** Publish a single, arithmetically checked latency table covering every stage at 44.1/48/88.2/96/176.4/192 kHz, in samples and ms, per tier, with the WOLA latency computed as `N` not `H`. Add a CI test that measures actual impulse group delay through the full chain and asserts **exact** equality with `getLatencySamples()` (±0 samples). Re-derive the product's low-latency mode from that table, and budget the second denoiser.

---

### B10. `Oversampled::latencySamples()` truncates, and the resulting PDC error means bypass cannot null.

**Claim under attack:**
```cpp
int latencySamples() const noexcept override {
    return (int)os.getLatencyInSamples() + inner->latencySamples() / factor;
}
```

Three defects in one line:
1. `inner->latencySamples() / factor` is **integer division**. An inner stage with 34 samples of latency at 4× reports 8, not 8.5. The chain's PDC is then wrong by a fraction, and the error is per-oversampled-stage.
2. `(int)os.getLatencyInSamples()` truncates the oversampler's own group delay, which for FIR halfband cascades is very often a **half-integer** number of base-rate samples (JUCE returns a float precisely because of this).
3. Because latency is truncated, the latency-matched bypass delay in `Chain::rebuildLatency` is also wrong, so `assert_bypass_is_null` — specified at "sample-exact" — cannot pass on any chain containing an oversampled stage. The §3.4 default preset has `"sat": {"oversample": 4}`. So the flagship null test fails on the flagship preset.

**And the same section contradicts itself on bypass:** §1.5 rule 3 requires host bypass to "ramp in/out over ~10 ms." A 10 ms ramp is by definition not a sample-exact null. §3.6 asserts `assert_bypass_is_null(chain, x, tol_db=-120)` "sample-exact." Both cannot be true. Additionally, it is ambiguous whether bypassing the `sat` stage bypasses the *inner* stage (leaving the oversampler's up/down FIR pair in circuit, which has passband ripple and is not transparent) or the whole decorator. The preset schema expresses `oversample` as a stage attribute, which implies the former — the wrong one.

**Required fix:** Latency arithmetic in a rational type (numerator/denominator at the oversampled rate) resolved to an integer exactly once at the outermost boundary, with any residual fraction absorbed by a Thiran allpass or by design constraint (choose FIR lengths that give integer base-rate delay — this is a design *requirement* on the halfband filters, not an afterthought). Bypass must be defined as a two-state contract: *host bypass* = ramped, latency-matched, not null-testable during the ramp; *unit-test bypass* = instantaneous, latency-matched, sample-exact, and it must bypass the decorator including its filters. Test both, separately.

---

### B11. The latency-tier system the product requires is architecturally incompatible with the latency rules this document states.

The engineer's document defines three tiers (LIVE <10 ms, TRACKING <25 ms, MIX ~110 ms) as "a single global control [that] auto-switches on host record-arm." The coder's document states (§1.5 rule 1): "`latencySamples()` is constant between `prepare()` calls," and offers only two remedies — "(a) accept the click and call `setLatencySamples()` + the host's PDC re-negotiation, or (b) keep the max latency reserved and pad with delay. **We choose (b) for anything a user might automate.**"

Apply (b) to tiers: LIVE tier now reports the MIX tier's ~110 ms, which annihilates the entire purpose of a live tier. Apply (a) to tiers: an auto-switch on record-arm triggers a mid-session PDC renegotiation, which in Logic stops playback and re-scans, in Pro Tools can produce a several-hundred-millisecond audio gap, and in Live silently misaligns the track until transport restart. Either way the headline feature is broken.

**Also unbudgeted:** tiers mean every latency-bearing stage needs a low-latency variant (denoiser, resonance suppressor, de-esser, limiter, plosive tamer), the assistant needs tier-aware rules (it must not propose a 48 ms spectral suppressor in LIVE), and the QA matrix multiplies — the engineer's document says so explicitly: "This doubles the QA matrix — budget for it." The coder's WBS has no tier line item at all.

**Required fix:** Declare the latency contract as a *hard, versioned, per-tier constant* determined at `prepare()` from a tier setting that is (i) not automatable, (ii) not preset-recallable in a way that changes it mid-transport, (iii) changed only via an explicit user action that triggers a full `prepare()` while transport is stopped, with a UI warning. Auto-switch on record-arm must be dropped or gated behind "transport stopped." Then add 6 person-weeks for low-latency stage variants and tier-aware assistant rules.

---

### B12. Sample-rate behaviour is unspecified where it is hardest: 44.1 kHz, and the analysis resampler's latency.

The document asserts sample-rate agnosticism and tests it with a sweep at 44.1/48/88.2/96/192. Specific gaps:

**12a — the 44.1 k family and the fixed-hop ML pipeline.** Analysis runs at "a canonical 48 kHz internal analysis rate, resampled from the host rate once" (§2.1). At 44.1 kHz the ratio is 147:160. A "hop 256 @48k" is 235.2 host samples — **not an integer**. The `HopBuffer` design assumes a fixed integer hop. Either the resampler's output-side buffering absorbs it (in which case the effective delay through the ML stage varies by ±1 sample frame-to-frame, and the *declared* latency is only correct on average — PDC drift, and the alignment of the mask to the audio it is applied to wanders) or you need explicit fractional-hop bookkeeping. Neither is described. 44.1 kHz is the majority session rate for pop vocals. This must be designed, not discovered.

**12b — the analysis resampler's latency is nowhere in the budget.** A polyphase 44.1→48 converter of acceptable quality has meaningful group delay (~1–2 ms). If the control rail is delay-aligned to the audio (per B8), that delay is in the audio path. It appears in neither §1.5's list of latency sources nor the engineer's table.

**12c — the oversampling rule is self-contradictory.** §1.6: "factor = `ceil(192000 / sr)` rounded to a power of two. So 44.1/48 → 4x." `ceil(192000/44100) = 5`, rounded up to a power of two = **8**, not 4. If the intent is 4× at 44.1 k, the effective rate is 176.4 kHz, below the stated ≥192 kHz floor — so the plugin does *not* sound the same at 44.1 as at 48, which is the exact claim the rule exists to support.

**12d — the SR golden test does not test what it claims.** §1.6's gate is "render a 1 kHz sweep… assert the magnitude responses agree within 0.25 dB." For **linear** stages that is a valid test. For the **nonlinear** stages the rule is written to protect (saturation, compression knees), the swept magnitude response is not a well-defined quantity, and the actual thing that changes with rate — aliasing products and harmonic distribution — is invisible to it. Add a proper nonlinear SR test: fixed-amplitude two-tone (e.g. 8 kHz + 9 kHz), measure in-band intermodulation and alias-fold energy, assert agreement within a stated dB across rates.

**12e — 0.45·sr clamp.** At 44.1 kHz an "air" high-shelf specified at 20 kHz clamps to 19.845 kHz; at 96 kHz it does not clamp. The §1.6 test only checks to 18 kHz, so it passes while the air band — the thing users A/B most — differs by rate. Either specify shelves by a rate-independent construction or document the difference.

---

# 3. BLOCKING OBJECTIONS — THE "TRANSLITERATES 1:1" CLAIM

### B13. "C++-shaped Python" is self-defeating: the constraint that makes it portable makes it too slow to prototype in, so it will not be obeyed.

**Claim under attack:** §0 — "Written in 'C++-shaped Python.' Explicit state members… This code is *transliterated* to C++, line by line." §4.2 — "The transliteration is mechanical: `self.z1` → `float z1_`, `for n in range(N)` → `for (int n = 0; n < N; ++n)`."

**Why it fails, arithmetically:** A per-sample Python loop runs at roughly 30–100 ns per iteration per operation. A compressor detector alone (envelope follower + gain computer + smoothing) is ~10 operations per sample. The §3.4 chain has ~14 stages, several of which are per-sample recursive (SVF filters, envelope followers, saturation with ADAA, limiter). Call it 300–1000 ns per sample for the chain. At 48 kHz that is **15–50× slower than realtime**, i.e. a 3-minute vocal takes 45 minutes to render, and the golden suite renders it at 7 block sizes × 3 sample rates × N cases.

The consequence is not "it's slow." The consequence is behavioural: engineers under deadline will vectorize. They will replace the per-sample envelope loop with `scipy.signal.lfilter` (which is a C loop with different state semantics), or with a clever `np.maximum.accumulate` trick, or they will write the gain computer as a whole-block array expression. **All of those are correct Python and none of them transliterate**, because a recursive filter cannot be expressed as a block array operation without changing what it computes, and a non-recursive vectorized formulation hides the state that C++ has to make explicit. The import-policy AST test does not catch this — `np.maximum.accumulate` is numpy. The `rt_checked` decorator does not catch it — it only checks that `io` wasn't reallocated.

So the guarantee is enforced by discipline after all, under exactly the schedule pressure that defeats discipline, and the failure is invisible until port time — at which point the "1–3 days per stage" becomes a redesign.

**Required fix — pick one, now, in writing:**
- **(Recommended) Invert the order.** Write `voxdsp` in C++ from day one and expose it to Python via pybind11 as the prototype's `stages/` implementation. Python keeps `analysis/` and `assistant/` (where the flexibility actually pays) and drives renders. You get: no port phase for the audio path, real CPU numbers from week 1 (which §5.7 correctly says you must have), the same code in the prototype and the product so "the sound is approved" means something, and the golden cross-check becomes a triviality instead of a 0.35 dB argument. Cost: slower first two weeks of DSP iteration; C++ build in the loop. This deletes the entire "port" line item and most of B14/B15.
- **Or** keep Python but mandate **Numba `@njit`** on every `stages/` inner loop, add the constraint "no numpy array-level operation may appear inside a per-sample recursive path" to the AST test (detectable: flag `np.` attribute access inside functions marked as per-sample), and accept that Numba-shaped Python and C++-shaped Python are also not the same thing.
- "Discipline plus a code-review rule" is not an acceptable answer. It is what the document currently has.

---

### B14. The 0.35 dB Bark-weighted spectral tolerance is a rubber stamp, and it is calibrated backwards.

**Claim under attack:** §4.2 and §5.13 — "cross-language gate is **Bark-weighted spectral difference < 0.35 dB up to 18 kHz** and **sample-level RMS difference < −70 dB**. Anything failing that is a real bug; anything passing it is not worth investigating."

**What a Bark-weighted long-term magnitude comparison cannot see** — i.e. what will pass this gate while being an obvious, shipping-blocking defect:

| Defect | Why the gate misses it |
|---|---|
| De-esser fires 15 ms late | Timing error; long-term magnitude spectrum is unchanged. The lisp is audible; the number is identical. |
| Compressor release curve wrong (pumping) | Pumping is amplitude modulation of a broadband signal. Time-averaged LTAS is nearly identical. |
| Limiter overshoots on 0.5% of transients | 0.5% of samples contribute nothing to an averaged spectrum. The clipping is audible and the true-peak spec is violated. |
| Gate chatters on breaths | Sub-1% energy events. Invisible. |
| Reverb tail with a completely different density/character | Two FDNs with the same RT60 and the same spectral tilt have the same LTAS and sound nothing alike. |
| Any inter-channel phase or stereo-image error | The metric as described is a magnitude-only, effectively mono measure. |
| **Latency error** | Magnitude spectra are shift-invariant. A 64-sample latency discrepancy — which breaks PDC and bypass null — scores exactly 0.00 dB. |
| Denormal-induced CPU spike | Not a spectral property at all. |

**And what will fail it while being irrelevant:** any nonlinear stage at meaningful drive, where a `tanh` polynomial approximation in C++ vs `np.tanh` in Python changes 3rd/5th harmonic levels by well over 0.35 dB in the Bark bands where those harmonics land. And the ONNX path: the engineer's document specifies **int8 quantisation** of the denoise encoder in the shipping build. A quantised model is a different function; its mask will differ from the fp32 Python prototype's by far more than 0.35 dB in low-SNR bands. So the gate will red-flag the two stages where divergence is expected and green-light the twelve where it is fatal.

**Required fix:** Replace one global tolerance with a **per-stage-class contract**, all of which run in CI:
1. **Latency:** exact. Impulse group delay, ±0 samples. No tolerance.
2. **Linear stages (EQ, filters, delay, oversampler):** frequency-response magnitude *and* phase within 0.05 dB / 0.5° to 0.45·SR. These should be near-exact; 0.35 dB here would hide a real coefficient bug.
3. **Dynamics (comp, gate, de-esser, leveler, limiter):** compare the **gain-reduction trace**, not the audio. Sample-aligned GR envelope within 0.25 dB, and GR *onset timing* within 1 sample. This is the test that catches everything in the table above, it is cheap, and the design already publishes GR on the analysis bus (§1.8) so the plumbing exists.
4. **Nonlinear (saturation):** harmonic and intermodulation levels at fixed drive points, per-harmonic tolerance, plus a mandate that Python and C++ use the **identical** `tanh`/waveshaper approximation (write the approximation once, in C, and call it from both).
5. **Stochastic/ML stages:** not compared numerically at all. Gate on task metrics (SNR improvement, PESQ/STOI delta, mask MSE against a fixed reference) with the *shipping quantised model* on both sides.
6. **Reverb:** EDC (energy decay curve) per octave band + echo density, not LTAS.
7. Keep the −70 dB sample-RMS gate only for stages in classes 1–2, where it is achievable.

---

### B15. The named list of things that will not transliterate, which §4.2 does not mention.

§4.2 lists what maps 1:1 and adds only "float32 vs float64 differences, SIMD, denormal handling, and the coefficient-update-rate optimization" as friction. The following are **redesigns**, not transliterations, and each needs an owner and a budget line:

1. **The reverb (5 pw).** An FDN that is "actually good" is tuned by ear against the target: delay-line prime sets, diffusion topology, modulation depth/rate, damping filter placement, early-reflection pattern. None of that survives a mechanical port because the port target is a *sound*, not a function. Whatever is built in Python will be rebuilt in C++. Budget it as a C++-native task and don't prototype it in Python at all.
2. **The saturator.** Python `np.tanh` (libm, correctly rounded) vs a C++ ADAA polynomial waveshaper (required for anti-aliasing per the engineer's doc §4.12) are different nonlinearities. ADAA also changes the *state* (it needs previous-sample memory), so it is not the same algorithm.
3. **The FFT.** numpy's pocketfft vs whatever C++ FFT is chosen differ in scaling convention, in real-FFT packing, and in accumulated error. Choose the C++ FFT (pffft / KissFFT / Accelerate / IPP) **before** writing the Python, and match conventions explicitly.
4. **Any PRNG.** Dither, reverb diffusion, denoise comfort-noise, doubler randomization. `np.random` is not portable. Specify one PRNG (e.g. xorshift128+) with an explicit seed contract and implement it identically in both. Otherwise every stochastic stage fails every cross-check forever.
5. **ONNX numerics.** fp32 Python vs int8-quantised C++ (engineer §7.5). Different function. §5.14's mitigation ("load models with the same restricted SessionOptions") does not address quantisation at all.
6. **The oversampler.** JUCE `dsp::Oversampling`'s filter design vs a hand-rolled Python polyphase FIR are different filters → different aliasing → different output from every nonlinear stage inside them. Either port JUCE's filter coefficients into Python or (better, per §4.1's own "zero JUCE dependency" goal) write the oversampler in `voxdsp` and use it from both.
7. **Pitch correction (10 pw).** PSOLA / phase-vocoder with formant preservation is a research-flavoured task with sonic tuning throughout. Not a transliteration under any definition.
8. **The `assistant/` and `analysis/` layer**, which the document already concedes is "a rewrite" — but then budgets at 6 + 4 = 10 pw for a subsystem containing Martin minimum statistics, BS.1770-4 with gating, pYIN/CREPE, LPC formant tracking, RT60 backward integration, online quantile estimators, and a 7-phase closed-loop solver. That is optimistic by roughly 2×.
9. **Anything the C++ SIMD-izes.** Once a stage is vectorized over channels or over a 4-sample group, its arithmetic order differs from the scalar Python and the −70 dB RMS gate stops holding. Decide per stage whether SIMD is allowed and re-tier its tolerance (B14).

---

# 4. BLOCKING OBJECTIONS — STATE AND AUTOMATION

### B16. The document contains two mutually exclusive models of how assistant output reaches host parameters, and neither one solves the automation conflict.

**Model A — §1.2:** assist is a *separate layer*, blended per block: `target = user + amt·(assist − user)`. The host parameter holds `user`. The effective value is not a host parameter.

**Model B — §4.6:** "The *result* of the assistant is written into the host params so automation/undo work, but as a single 'Apply Assist' gesture (`beginChangeGesture`/`endChangeGesture` batched)… Continuous 'learn' mode writes to a separate non-automatable layer."

These are incompatible. If the assistant writes its result into `userNorm` (Model B), then on the next block `updateBlock` computes `user + amt·(assist − user)` where `user` is now already the assisted value — the assist offset is applied **a second time**, and if the assistant re-solves, it compounds. Unless `assist` is zeroed at apply-time, which the document does not say, and which then makes `assist_amount` meaningless post-apply (the "dial the AI in/out" macro no longer does anything, because there is nothing left to dial). The document says "This is a UX decision with a hard architectural consequence — decide it now." Correct. **It has not been decided, and the doc ships code for A and prose for B.**

**The conflicts neither model solves:**

1. **User automates a parameter the assistant also wants to write.** In Model A, the user draws an automation curve on `comp.threshold`; the plugin plays back `user + amt·(assist − user)`. **The user does not get the curve they drew.** They will conclude the automation is broken. There is no arbitration, no per-parameter "the user has touched this, hands off" latch, and no UI indication of which value is in force.
2. **Host automation write modes.** In Pro Tools/Logic/Cubase Latch or Write mode, a plugin that calls `setValueNotifyingHost` (which Model B's "Apply Assist" does, and which continuous learn mode would do constantly) **records those values into the automation lane**. Continuous learn mode with the transport in Latch writes a dense automation curve for every assistable parameter across the whole take, permanently, without the user asking. That is data loss in the user's session. It is also a classic feedback loop: written automation plays back → changes the signal → assistant re-solves → writes again.
3. **Undo.** Every `beginChangeGesture/endChangeGesture` pair creates a host undo step and sets the session-modified flag. An assistant that re-solves every few seconds floods the undo stack and makes the DAW prompt to save on every close. Logic and Live additionally have *no* plugin-level undo, so the plugin must implement its own undo stack for the assist layer, node edits and preset changes — a subsystem with zero lines in the WBS.
4. **Displayed value vs actual value.** Hosts display the host parameter. In Model A that is `user`, while the audio reflects the blended value. Pro Tools in particular expects the plugin's displayed value to match automation. Generic-UI hosts will show wrong numbers.
5. **`assist_amount` is itself automatable and is a natural thing to automate** ("pull the AI back in the bridge"). Automating it modulates the *result* of every assistable parameter simultaneously, through each parameter's own smoothing time, with no defined behaviour when `assist` is concurrently re-solved.

**Required fix — this must be specified before any code:**
1. **One model. I recommend Model A with a hard touch-latch.** Every assistable parameter carries a `userOverride` bit set the moment the host sends an automation event or the user touches the control. Once set, `amt` is forced to 0 for that parameter and the UI shows it as user-owned, with an explicit "release to assistant" affordance. The assistant proposes; a touched parameter is not proposed to. This is how every shipping "smart" tool that survived contact with automation works.
2. **"Apply Assist" is the only path that writes host parameters**, it is an explicit user gesture, it zeroes the assist layer for the applied parameters in the same transaction, and it is guarded against firing while the host is in a write-enabled automation mode (query the host's automation state where the API allows, and otherwise refuse to write during transport-rolling record).
3. **Continuous learn mode never calls `setValueNotifyingHost`.** Ever. It writes only the internal assist layer, and the plugin must state in the UI that learn-mode moves are not automation.
4. Implement a plugin-internal undo stack for assist/node/preset operations, and define exactly which host operations it participates in.

---

### B17. Session recall is broken by a file-path reference in the preset, and the state contract is under-specified.

**Claim under attack:** §3.4 — `"assist": { "amount": 1.0, "profileRef": "profile.json", "style": "modern-pop" }`, combined with §4.6 — "`getStateInformation` writes the §3.4 preset JSON embedded in a ValueTree."

**Concrete failure:** The `VocalProfile` is the entire basis of every assistant decision, and it is referenced by an external path. The user sends the session to a collaborator, or moves the project folder, or opens it on the mix machine: `profile.json` is not there. The plugin restores with `amount: 1.0` and no profile. Best case the assist layer is inert and the vocal sounds completely different from what was approved; worst case the resolve path produces garbage. There is no defined behaviour for a missing profile.

**Related gaps in the state contract, none of which are specified:**
- **The ML model version is not in the state.** `denoise.params.model: "denoise_v1"` is a string, but there is no rule that a session saved with v1 must recall v1 after the user updates the plugin to a build shipping v2. A new denoiser is a different sound. Either ship every historical model forever (state the size budget) or version presets and accept audible recall changes (state it in the release notes and the UI). Decide.
- **Cross-format state portability.** VST3, AU and (later) AAX must round-trip the same blob so a user can swap formats without losing the session. Requires a format-independent chunk and a test. Not mentioned.
- **State size.** Embedded profile (31-band LTAS + percentiles + resonances + breaths/plosives segment lists) can reach tens to hundreds of KB per instance. `breaths: list[Segment]` and `plosives: list[Segment]` over a 4-minute vocal is potentially thousands of entries. Multiply by 24 vocal tracks. Some hosts handle multi-MB plugin state badly. Specify a maximum and a truncation/summary policy.
- **`reset()` semantics vs smoothers.** §1.4 says on reset "smoothers **jump to target**." On a transport locate while a parameter is mid-ramp, jumping the makeup gain or a filter cutoff to target produces a discontinuity at exactly the moment the user presses play. Specify: jump is correct only when the output is already silent (post-`reset()` zeroed state), which it is — so this is probably fine, but say so, and test it (`reset()` followed immediately by `process` must not produce a click, and the golden suite has no locate-during-playback case).
- **Editor open/close** is stated not to touch DSP state (correct), but nothing says what happens if the editor is opened while a profile is being computed on the assistant thread, or if `releaseResources()` is called while the assistant thread holds pointers into buffers allocated in `prepare()`. That is a use-after-free with no stated ownership rule. Specify thread lifetime: the assistant thread must be joined (or made to observe a generation counter) before any `prepare()`-allocated memory is freed.

**Required fix:** The profile is **embedded in the state blob**, not referenced. `profileRef` is deleted from the schema. Add a documented state schema with: profile (or explicit "none"), model IDs + versions, assist layer values, per-param `userOverride` bits, tier, and schema version, with a migration chain and a round-trip test across all three formats.

---

### B18. The CPU target contradicts the sibling document by 4×, and the architecture forces worst-case CPU permanently.

**Claim under attack:** §5.7 — "State the target explicitly: **< 4% of one core per instance at 48 kHz / 128-sample blocks** on an M1 / Ryzen 5000, so 16 instances fit in a session."

The engineer's document §6 budgets **~16% of one core with ML on** (Mix tier), of which the neural clean-up alone is 9%. That is 4× the coder's target and it means **~5–6 instances**, not 16. One of these two numbers is going into a marketing claim and a system-requirements page; they cannot both be right.

**And B1's required fix makes it worse:** once structural variability is removed (all EQ nodes, both de-esser topologies, the oversampler always instantiated and running), CPU is worst-case at all times. Worse, the design's stated selling point — "doing nothing is a valid, and often correct, output" — cannot recover any CPU: if the assistant decides a clean 24-bit source needs no denoising, the ML stage must keep running (or its latency changes, per B11). So the plugin pays 9% for a denoiser doing nothing.

**Required fix:** Reconcile to one number with the DSP lead, per tier, with ML on and off. Then add an explicit **structural bypass protocol**: a stage may be fully disabled (skipping its DSP *and* its latency) only via a non-automatable, transport-stopped, `prepare()`-triggering control, exposed as "Modules" enable/disable — the same way every CPU-heavy channel strip does it. And put a CPU-per-instance regression gate in CI against a *chain* preset, not just per-stage µs/sample (§4.7 job 7 measures per-stage regressions, which will not catch the sum drifting past budget).

---

# 5. NON-BLOCKING CONCERNS

**N1. `assert_block_size_invariant` at −140 dB is below float32 precision.** It will pass in float64-contaminated Python and fail in C++ SIMD. Set tiered tolerances now (see B3.3) rather than relaxing the number under pressure later.

**N2. Feature ring sized 512 frames = 5.5 s of latent staleness** at hop 512 @48k. Prefer 8–16 with drop-oldest (see B7.3).

**N3. `publishGR(int stageSlot, float grDb)` has undefined semantics** — is it the block max, the block mean, the final sample? The assistant's closed loop ("I asked for 4 dB, I'm getting 9") depends on it. Specify: block-maximum GR, plus a separate block-mean, both as `float` atomics.

**N4. `Chain::process` bypass leaves stage state stale.** A bypassed compressor's envelope follower and a bypassed filter's memory do not track the signal, so un-bypassing produces a transient. Either keep running the detector while muting the effect (costs CPU, correct behaviour) or crossfade over 20 ms on un-bypass. Also: no crossfade is specified for per-stage bypass at all.

**N5. Denormal policy is right but the test is wrong.** `assert_no_denormal_hazard` asserts "tails reach exactly 0.0 within 5 s." With FTZ/DAZ enabled in the test process, everything trivially reaches 0.0 and the test proves nothing about hosts that do not set FTZ. Run that test with FTZ explicitly **disabled** — that is the whole point.

**N6. `AudioBlock` with `float* const* channels` and no length invariants** is a natural home for out-of-bounds bugs when combined with the oversampler (B5b) and with hosts that exceed `maxBlockSize` (§4.3 rule 5 correctly anticipates this, but nothing in the type enforces it). Add a debug-mode bounds-checked variant used in all tests.

**N7. Golden audio checked into git.** "~10 MB total" grows. Use Git LFS or a content-addressed fetch from day one; retrofitting it after 200 commits of WAV churn is painful.

**N8. `--assist-mode streaming` convergence tolerance is asserted but never numerically specified** (§5.10 says "within a stated tolerance"). State it: e.g. every assistable parameter within 20% of its offline value after 30 s of voiced audio, and add the case where it *cannot* converge (sparse take, one verse) to the golden set.

**N9. `voice_class` is a 6-way classifier over `{"low-male","male","female","high-female","spoken","rap"}`.** Gendered voice categories driving audible processing decisions is a product/PR risk and a correctness risk (they are proxies for F0 and formant scaling, which you already measure directly). Recommend renaming to acoustic descriptors (`f0-range × brightness` buckets) — same math, no headline.

**N10. The AAX deferral is a revenue decision disguised as a scheduling one.** §4.6 defers AAX to v1.1 at "2–3 weeks." Pro Tools remains dominant in professional vocal recording and mixing; a vocal processor without AAX at launch loses a large share of the target buyer, and AudioSuite (offline) support interacts directly with B6 and B1. See the effort table — this is not 2–3 weeks.

**N11. Two documents, two architectures.** The coder's asynchronous analysis bus and the engineer's synchronous delay-aligned dual rail must be reconciled into one document before anyone writes a line of `voxdsp`. Also reconcile: latency (10.7 vs 40 ms ML), CPU (4% vs 16%), and the filter-core detail the engineer flags as highest-leverage (modulate only the TPT mixing-form gain, never `g`/`k`) which the coder's `ControlRateUpdater` "recompute coefficients every 16–32 samples" directly contradicts.

**N12. No `pluginval`-equivalent gate for AU on Apple Silicon under Rosetta**, no test for host sample-rate change mid-session, no test for two instances sharing a static ONNX session. Add to the matrix.

---

# 6. CORRECTED EFFORT ESTIMATE

## 6.1 What the WBS is missing entirely

Every line below is absent from §6.1's 103 person-weeks and is required to ship a commercial plugin.

| # | Missing work | PW | Why it is not optional |
|---|---|---:|---|
| 1 | **Licensing / copy protection / activation** — serial or account auth, machine binding, offline activation, trial mode, seat management, license server, e-commerce webhook integration, revocation | **8** | You cannot sell it without this. Not present in any form in the document. |
| 2 | **Preset management (code)** — browser, tags, favourites, user folders, A/B compare, import/export, factory bank packaging | **4** | §3.4 defines a preset *format*; there is no preset *system*. |
| 3 | **Preset content authoring** — a sound designer building and validating the factory library across voice types and styles | **5** | §6.3 identifies Nectar's preset catalogue as its moat, then budgets zero for ours. Not an engineer's time. |
| 4 | **UX/product design** (not implementation) — a Nectar-class interaction design, visual design, design system, iteration | **10** | The WBS has 16 pw of UI *implementation* and 0 of design. |
| 5 | **UI implementation, corrected** 16 → 26 | **+10** | Spectrum + GR traces + node editing + assist explanation view + resizing + light/dark. 16 is the number teams write down before they start. |
| 6 | **Accessibility** — screen reader (VoiceOver/NVDA) over a custom-rendered JUCE UI, keyboard navigation, contrast, focus order | **4** | Buried inside "UI 16" as a word. Also increasingly a compliance requirement for consumer software in the EU. |
| 7 | **Localization** — string extraction, layout reflow, RTL decision; the rationale/explanation strings are the hard part | **2** | The assistant's explanations are the product's wedge (§6.3). They are prose. |
| 8 | **Installers, corrected** 3 → 6 | **+3** | mac pkg with per-format targets and an uninstaller, Windows WiX with upgrade codes, per-format path handling, ONNX dylib signing/entitlements under hardened runtime, notarization edge cases, silent-install for enterprise. |
| 9 | **AAX + PACE + AudioSuite** | **6** | Not "2–3 weeks." PACE integration, AAX's different parameter/automation model, the offline AudioSuite processing path (which interacts with B1 and B6), Avid submission and compat testing. |
| 10 | **DAW compatibility QA, corrected** 5 → 10 | **+5** | 7 hosts × 2 OS × 2 architectures, and the engineer's tier system doubles the matrix by its own admission. |
| 11 | **Latency tiers + low-latency stage variants + tier-aware assistant rules** | **6** | Required by the sibling document; absent here (B11). Includes a second, causal denoiser. |
| 12 | **RT-safe structural reconfiguration subsystem** (prepared-object handoff, reclaim queue, crossfade) | **3** | B1. Currently does not exist. |
| 13 | **Offline/non-realtime deterministic render path** | **3** | B6. Second execution path through the ML stage + assistant freezing + tests. |
| 14 | **Automation/assist arbitration** (touch latch, apply-gesture guards, internal undo stack, displayed-value reconciliation) | **4** | B16. Includes plugin-internal undo, which no host provides. |
| 15 | **Sample-accurate parameter events + block slicing** | **2** | B3. Framework-level, affects every stage's test. |
| 16 | **ML model shipping, versioning and update path** — model IDs in state, shipping historical models, signature verification, quantisation validation per platform, size/CDN decision | **3** | B17. A new denoiser silently changing old sessions is a support catastrophe. |
| 17 | **Crash telemetry + opt-in analytics + privacy policy/GDPR plumbing** | **3** | You cannot debug a 200-user beta, let alone 10k customers, from forum posts. |
| 18 | **Support tooling + documentation** — log/state bundle export, in-app "report a problem," a Nectar-class manual, tutorial/onboarding for an assistant product | **5** | An assistant that explains itself needs documentation that explains the assistant. |
| 19 | **Reverb, corrected** 5 → 8 | **+3** | "Actually good" FDN with early reflections and modulation, tuned by ear. |
| 20 | **Analysis + assistant in C++, corrected** 10 → 16 | **+6** | Martin minimum statistics, BS.1770-4 with gating, pYIN/CREPE, LPC formants, RT60 integration, online quantile estimators, 7-phase closed-loop solver, streaming/offline parity. 10 pw is roughly half. |

**Total additions: +105 person-weeks.**

## 6.2 The corrected numbers

| | Coder's figure | Corrected |
|---|---:|---:|
| Full-scope v1 subtotal | 103 | **208** |
| Risk buffer | +25% → 129 | **+35% → ~281** |
| Python prototype phase | 8–12 | **16–20** (or **~0** if B13's recommended inversion is adopted, with ~6 pw of pybind11/tooling instead) |
| Data + model track (separate people) | 10–16 | **20–26** (adds corpus licensing/legal review, quantisation validation, and the second low-latency denoiser's training) |

**Corrected full-scope v1: ~280 person-weeks of engineering** (vs 129 claimed — **2.2×**), plus ~18 prototype and ~23 data/ML on parallel tracks.

Why +35% and not +25%: the plan contains one item the author himself scores at 8–16 pw variance (pitch correction), an assistant whose *quality* has no engineering completion criterion, an unreconciled architectural conflict with the sibling document (B8), and a first-time team on this codebase. 25% is the buffer for a project with known unknowns. This one has an unknown architecture in the control path.

**Calendar, full scope:** 6 people at ~60% parallel efficiency ⇒ 281 / 3.6 ≈ **78 weeks ≈ 18 months**. The document's "8–9 months with 6 people" is off by a factor of two.

## 6.3 The trimmed v1 (cutting pitch, reverb, delay, doubler as §6.2 proposes)

Removing those four line items and their share of UI/QA: subtotal 208 − 10 (pitch) − 8 (reverb) − 2 (delay) − 2 (doubler) − 4 (UI/QA share) = **182**, ×1.35 = **~246 person-weeks**.

**Calendar:** 5 people at ~65% ⇒ 246 / 3.25 ≈ **76 weeks**; 6 people at ~60% ⇒ **~68 weeks ≈ 15–16 months**.

**The number I would actually take to a stakeholder: ~250 person-weeks / 15–16 months to a shippable trimmed v1 with a team of six**, against the document's claim of ~100 pw / 7–9 months. The document's closing line — "Any estimate below ~80 person-weeks for a shippable, DAW-compatible, AAA-quality vocal processor is fiction" — is correct in spirit and wrong by a factor of three in magnitude. It is fiction below ~240.

## 6.4 If the number must come down

The only honest levers, in order of value per week saved:
1. **Adopt B13's inversion (C++-first + pybind11).** Deletes the port phase, the cross-language tolerance argument (B14), and most of B15. Saves ~15–20 pw net and removes the single largest schedule risk.
2. **Cut the ML denoiser from v1**; ship a well-tuned spectral-subtraction / filter-bank suppressor. Saves ~9 pw of DSP, ~20 pw of the data track, ~9% CPU, ~40 ms of latency, the entire B6 determinism problem, and the model-versioning problem (B17). The assistant remains the differentiator. This is the highest-leverage cut in the plan and the document does not consider it.
3. **Ship VST3+AU only and say so publicly**, with AAX as a funded 1.1. Defers 6 pw but costs real revenue — a decision for the producer, not the coder.
4. **Cut continuous "learn" mode**; ship analyze-then-apply only. Removes most of B16's automation conflict, the internal undo flood, and a large QA surface. Saves ~4 pw and a category of unfixable bug reports.

---

# 7. VERDICT

## **BLOCKED.**

Not because the design is bad — it is above average for the category — but because three of its load-bearing claims are arithmetically or architecturally false, and the project would discover all three at the point of maximum sunk cost:

- **The ML latency is understated by 4×** (B9), which invalidates both published latency targets and the default preset.
- **There is no path from the assistant's actual output to the audio thread** (B1, B2, B8): the proposal FIFO cannot express EQ nodes, cannot deliver coupled solutions atomically, and the "one shared STFT" the CPU budget depends on is unimplementable through the `Stage` interface.
- **The automation/assist conflict is unsolved and the document knows it** ("decide it now") while shipping two contradictory models (B16).

Add to that a non-deterministic offline bounce (B6) and an effort estimate that is 2.2× low (§6), and advancing this to implementation would produce a project that looks healthy for nine months and then does not converge.

## Conditions to convert to CONDITIONAL PASS

All of the following, in writing, reviewed, before any `voxdsp` implementation begins:

1. **A single reconciled architecture document** merging this and `round1_engineer.md`, resolving: synchronous control rail vs asynchronous assistant bus (B8), ML latency (B9), CPU per instance (B18), and coefficient-modulation policy (N11). One number for each. Signed off by both authors.
2. **A latency contract**: full per-stage, per-tier, per-sample-rate table in samples and ms, WOLA latency computed as window length, tier-change policy stated (B11), and a CI test asserting reported PDC == measured impulse delay ±0 samples.
3. **A parameter/state design doc** covering: snapshot-based assist handoff (B2), sample-accurate automation events (B3), the touch-latch arbitration model with exactly one assist model chosen (B16), the embedded-profile state schema with model versioning and cross-format round-trip (B17), and the cage enforced at ingress (B4).
4. **An RT-safe reconfiguration design** — prepared-object handoff, reclaim queue, crossfade — plus the decision that all structural capacity is fixed and pre-instantiated (B1).
5. **A non-realtime execution path spec** for the ML stage and the assistant, with a determinism test: two renders of the same input must be bit-identical (B6).
6. **A revised cross-language verification plan** with per-stage-class tolerances replacing the single 0.35 dB gate, explicitly including exact latency, GR-trace comparison for dynamics, and task metrics for ML (B14).
7. **A decision on B13** — C++-first with pybind11 (recommended) or Numba-mandated Python with an AST rule that can actually detect vectorized recursion. "Discipline" is not an answer.
8. **A revised WBS and estimate** incorporating §6.1's additions, or an explicit, signed scope cut (§6.4) that removes the corresponding work. If the number that comes back is under 200 person-weeks for the trimmed scope, I want to see which of the 20 missing line items was deleted and who agreed to ship without it.

Close these eight and I will pass it. Until then, nobody writes `Stage.h`.
