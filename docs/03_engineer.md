# ENGINEER SPEC — Round 4 (hardened after 6 objections)

**Role:** Principal DSP Engineer — DSP specification owner. Closes every blocking
objection from the round-3 adversarial review of the DSP spec rather than restating it
unchanged. Every objection raised was correct; none is disputed — each is closed below
by a concrete, testable fix.

---

## Adversary objections and how each was resolved

| # | Severity | Objection | Resolution |
|---|---|---|---|
| 1 | Fatal | Published Mix-tier latency (91.5 ms) omitted three real-time-path stages the signal_chain itself inserts: Effort Compression, the order-tracked harmonic dynamic EQ (M8b), and Clarity | Each accounted for explicitly. Effort Compression = 0.0 ms (control-rate + min-phase IIR only). M8b = +21.3 ms (dedicated WOLA, cannot ride on M4/M6's already-consumed transform). Clarity's honest minimum lookahead (>1 s once its modulation window is corrected to resolve 0.5 Hz) is far too large to pad into any session PDC, so it is demoted to **offline/two-pass only**, contributing 0 ms to realtime PDC — exactly like WPE. Corrected Mix total: **112.8 ms** (5416 samples @48k). |
| 2 | Major | M12's "−90 dBFS at 1 kHz/0 dBFS comfortably met at 8x" alias claim holds only at low-to-moderate drive | At Drive=24 dB a heavily-driven tanh approaches a square wave whose harmonics decay as 1/n, not exponentially — no realistic oversampling ratio recovers −90 dBFS from that (a physical limit, not a bug). Now publishes a **three-axis** alias surface (level × frequency × DRIVE), states the honest degraded numbers (−50 to −60 dBFS at Drive=24 dB pre-switchover, −70 to −75 dB after a drive-triggered ADAA-2/16x switchover above 12 dB Drive), and notes the Chebyshev curve alone is alias-safe at any drive by construction (harmonic content past h5 is exactly zero). |
| 3 | Major | No denormal policy stated anywhere despite the whole chain running recursive filter state | Stage contract now requires: (1) Chain sets FTZ/DAZ once per `process()` call on the audio thread, documented as process-wide and NOT numerically transparent; (2) every `@kernel` holding recursive state adds a fixed 1e-20 anti-denormal bias to its feedback register, immune to the Python↔C++ boundary not preserving CPU flags; (3) new CI test `assert_no_denormal_stall`, run once with FTZ/DAZ forced OFF to isolate the bias mechanism. |
| 4 | Major | S3's dynamics bisection referenced an undefined "post-stage analysis tap" for its 200k-sample statistic | Replaced with a fully specified RT feature: **F13**, a 96-bin, 768-byte, O(1)-per-frame decaying level histogram in `vox.analysis`, published on the AnalysisBus like every other feature. Offline mode is proven a special case of the same bisection code (tau=infinity) via `assert_solver_offline_rt_agree`. New bounded-time test `assert_solver_rt_tick_bounded` (<2.0 ms on reference core). |
| 5 | Major | S1/S2/Policy constants (hpf.corner_factor, gate.offset_db, etc.) were unlabeled "magic constants" | Every constant now carries an explicit provenance tag. Since the reference corpus needed for corpus-derivation doesn't exist yet, every constant ships as "tunable default, stated safe range" with a new per-constant CI test, `assert_solver_constant_sensitivity(name, pct=0.20)`, asserting the solver's measured OUTPUT (not the constant) doesn't move more than a stated bound under a ±20% perturbation. This proves non-brittleness, not correctness — that distinction is stated explicitly. |
| 6 | Minor | DynamicEQ/TonalEQ structural capacity was specified as 8/4 nodes, contradicting BAR item 9's 24-band requirement | Corrected to **24 always-instantiated nodes each (48 total)**, matching the BAR exactly. The assistant solver writes only a small assist-writable subset (default ≤4 nodes); the rest is manual/host-automatable capacity via existing assist_min/assist_max=None mechanism. Raises the accepted CPU floor substantially — flagged as more urgent, not less, in open questions. |

---

## Modules

### M0 — Input conditioning + robust calibration
DC servo (2nd-order Butterworth HP + 1-pole servo) corner **lowered to 5 Hz** (round-2's
12 Hz claimed "flat within 0.02 dB above 20 Hz," which is actually −0.53 dB — a real
arithmetic error, corrected in closed form: −0.045 dB @20 Hz / −0.02 dB @30 Hz at the
new corner). All recursive states float64 (float32 misses the −120 dB null gate by
~80 dB at this corner). Calibration offset computed from LUFS-S (K-weighted, voiced-
gated, ≥30 s accumulated) — NOT LUFS-I over 3 s — persisted, overridable, proposed-not-
applied on re-analysis. Gate: 20 different start offsets must agree within ±1 LU.

### M1 — Analysis front-end (multi-tap, 3 taps)
One shared feature bus instead of every module re-detecting the same sibilant. Taps:
A = post-input-conditioning, B = post-cleanup, C = post-chain pre-limiter — no control
signal may be derived downstream of the module it controls. F0 via clean-room pYIN
(FFT difference function, Beta-distributed thresholds, HMM Viterbi decode) with
CREPE-tiny octave arbitration only on the <8% of frames where pYIN posterior <0.6.
Formants via order-18 LPC (corrected from round-2's ill-conditioned order-50). Spectral
envelope via True Envelope (Roebel & Rodet), not plain cepstral liftering. Noise floor
via MCRA/IMCRA. Reverb via two cross-checked estimators (EDC backward integration +
MTF). Canonical control rate 100 Hz; CPU genuinely flat 44.1–192 kHz via decimation, not
a fixed hop (which would NOT be flat).

### M2 — De-click / de-crackle
AR(32) via Burg's method, robust-scale outlier flagging, LSAR (Godsill & Rayner)
Cholesky-banded repair. De-clip is the same machinery with an inequality constraint,
projected conjugate gradient. Latency: 10.7 ms lookahead (Mix), 0 offline two-pass.

### M3 — De-hum
Fundamental via maximized harmonic-sum objective + phase-vocoder refinement, FLL
tracking. Default mode: least-squares sinusoidal subtraction (phase-linear, no notch);
notch-comb mode available. Handles drifting mains / switching-supply hum a fixed
50/60 Hz comb cannot.

### M4 — Unified cleanup engine (denoise + de-reverb + de-bleed + spectral gate, ONE gain field, ONE ISTFT)
OM-LSA denoise × Lebart/WPE de-reverb × coherence-Wiener/NMF de-bleed × adaptive
soft-logistic spectral gate, composed as ONE gain field in the gain domain (phase-
coherent by construction) before a single minimum-phase ISTFT — so artefacts never
compound across four separate transforms. WPE de-reverb is offline-only (iterative);
RT uses RLS-WPE. Latency: Mix 32.0 ms, Tracking 13.4 ms, Live 5.3 ms.

### M5 — Adaptive rumble HPF + de-plosive
HPF corner = 0.72×F0_p5, clamped [40, 200] Hz (upper clamp corrected from round-2's 140
Hz), set once per analysis, smoothed 200 ms, never swept per-event. De-plosive: static
LR4 crossover at 160 Hz, gain envelope on the LOW band only — zipper-free, alias-free,
nulls at Depth=0.

### M6 — Resonance suppressor (the Soothe2 killer)
Two engines: Engine A (spectral, ≥500 Hz, True Envelope detection, ERB-Gaussian
reference, ISO 226:2023 level-dependent masking weight, bin-aware harmonic protection,
minimum-phase reconstruction with a pre-echo gate — the round-2 8x-decimated LF path
that pre-echoed ±170 ms is retired); Engine B (tracked TPT peaking filters, <500 Hz and
all of Live tier, no window, no pre-echo). Latency: Engine A 21.3 ms, Engine B ~0
(group delay <2 ms).

### M7 — Gate / expander / breath control
Feedforward downward expander, dual detector max(level, SPP), asymmetric dual-branch
ballistics. Breath mode: fixed attenuation (default −9 dB) with 20 ms ramps, not a gate.
Latency: 3 ms Mix/Tracking, 1 ms Live.

### M8 — Dynamic EQ + Unmask (psychoacoustic sidechain masking curve)
6-band dynamic EQ, per-band detector on the band's own BP output, soft-knee piecewise-
quadratic gain law. Unmask: excitation-pattern masking threshold, harmonic-selective
weighting by the vocal's own harmonicity (typically 3–4 dB less total energy removed
for equal intelligibility gain vs. a flat duck), applied as min-phase spectral gain to
the vocal or limited inverse boost.

### M8b — Order-tracked harmonic dynamic EQ (prior art acknowledged, not marketed as novel)
Resamples the log-magnitude spectrum onto an F0-locked harmonic-index axis, applies a
dynamics law on that axis, warps back, crossfades against flat gain by F0 confidence.
Explicitly cited as order tracking (rotating-machinery diagnostics, 1980s–90s) / pitch-
synchronous vocoder processing (1970s–80s) — NOT claimed as novel. Fixes vibrato
amplitude-modulation artefact: measured −18 dB residual AM for a fixed notch vs. below
−45 dB on the harmonic-index axis. Latency: 21.3 ms, Mix tier only.

### M9 — Compressor A (slow feedback leveler)
Feedback (return-path) log-domain topology, detector taps POST-COMPRESSION PRE-MAKEUP.
The round-2 ">12 dB gain margin" claim is retracted (gain margin is a phase-domain
quantity a bare loop-gain magnitude can't establish) and replaced with what IS
derivable (loop cannot diverge under first-order analysis for the exposed ratio range)
plus a measured, verifiable gate: step-response overshoot ≤0.5 dB, settling ≤150 ms,
swept across ratio/threshold/knee. RMS tau 30 ms, sidechain HPF + sibilance de-emphasis
(−6 dB shelf 5–9 kHz keyed by S_hat). Latency: 0.

### M10 — Compressor B (fast feedforward peak)
Smooth-decoupled peak detector, running-min + Hann-convolved lookahead gain
construction (guaranteed ≤ required gain at every sample, C1-continuous), tanh gain
slew (0.35 dB/sample, design target −80 dBFS IMD), adaptive release keyed to voicing/
onset-flux. Latency: 3 ms (1.5–5 ms range).

### M11 — De-esser (two-point, texture-adaptive, frequency-tracking)
Detector: median-subtracted sibilance ratio (texture-independent), duration + onset-
flux + voicing-consistency gating, 25% duty-cycle limiter. Adaptive centre-frequency
tracking 4–12 kHz. Two-point strategy (M9's sidechain de-emphasis ≤6 dB + this stage
≤4 dB) beats one stage at 8 dB. Latency: 3 ms (spectral mode 21.3 ms, Mix only).

### M12 — Saturation (3-band, 8x oversampled, ADAA)
Curves with exact ADAA antiderivatives: Soft/Tube/Chebyshev (exact harmonic control via
T1–T5)/Tape (Jiles-Atherton hysteresis)/Diode. 8x oversampling all bands. Alias
reporting is a THREE-axis surface (level × frequency × drive) — see objection 2 above.
Latency: 1.0 ms (48 samples @48 kHz).

### M13 — Tonal EQ (static, matched-Z, deliberately under-fitted auto-match)
8 bands, TPT SVF, Matched-Z/magnitude-matched biquads (Vicanek) for shelves/bells above
~5 kHz — fixes the bilinear-transform warp toward Nyquist present in essentially every
shipping plugin. Auto-EQ: constrained NNLS, deliberately under-fitted (≤6 bands,
0.5-octave min separation) so it never chases noise. Latency: 0.

### M14 — Transient shaper (voicing-gated)
Differential-envelope design (fast-slow, slow-very-slow envelope pairs), no threshold.
Voicing gate: attack emphasis only on unvoiced→voiced transitions and plosive/fricative
onsets — prevents emphasizing vibrato peaks. Latency: 0 (feedforward) or 2 ms.

### M15 — Gain riding, split in two (input normaliser + output fader)
(a) Input normaliser gated by an OPEN-LOOP, level-invariant voicing detector at tap A
(never a downstream, level-sensitive SPP). (b) Output fader targets LUFS-S at tap C
(post-chain, pre-limiter). Phrase-aware: hold within a segment (≤0.5 dB/s), fast move
at boundaries (≤12 dB/s, 60 ms raised cosine). Latency: 0.

### M16 — True-peak limiter + ISP clipper + BS.1770-4 metering
Exact BS.1770-4 K-weighting, correctly-gated LRA per EBU Tech 3342. True-peak
oversampling corrected (4x@44.1/48k, 2x@88.2/96k, 1x@176.4/192k — round-2 had this
inverted). Lookahead 5 ms default, running-min+Hann trajectory, dual-branch release,
S-curve shape. Aliasing bound published (design target −85 dBFS), not claimed zero.
Latency: 5.2 ms.

### M17 — Latency budget and PDC policy
See objection 1. Corrected Mix total 112.8 ms / 5416 samples @48k. Tracking 23.9 ms.
Live 10.05 ms. Clarity is offline-only in every tier. PDC is a session-level,
transport-stopped setting; default is fixed-maximum-latency padded to Mix PDC.

---

## Novel effects

### Clarity — MTF-targeted modulation-domain de-reverb (offline/two-pass only)
Reverb is a low-pass filter on the modulation spectrum, not a spectral defect (Houtgast
& Steeneken 1973 / STI). Fixes the round-2 window-length bug (512 ms window couldn't
resolve its own advertised 0.5 Hz modulation floor); lengthened to 2.048 s. Offline-only
because a correct implementation needs ≥1 s of context per band — contributes 0 ms to
any realtime PDC tier. UI reads out STI directly.

### Partial-Loudness Rider — ride the vocal to masked loudness, not LUFS
Moore-Glasberg (1997) partial specific loudness of the vocal in the presence of the
instrumental, in sones. Rides gain so partial loudness tracks a target trajectory
(absolute or ratio-to-instrumental) instead of a solo, unmasked level metric that
doesn't describe what a vocal in a mix actually sounds like.

### Effort Compression — dynamics in the H1-H2 / spectral-tilt domain
Compressors change how loud a note is; they cannot change how HARD it sounds like it
was sung. Measures vocal effort via Iseli-Alwan-corrected H1*-H2* (open-quotient proxy),
spectral tilt, and formant bandwidth (Klatt & Klatt 1990, Hanson 1997), compresses THAT
via a loudness-neutralised tilt filter. Latency: 0 ms (control-rate + min-phase IIR).

### Dissonance Duck — partial-precision, roughness-driven instrumental ducking
Masking (Unmask) and roughness (Plomp & Levelt 1965, Vassilakis 2001) are different
perceptual phenomena — a tone can be fully unmasked and still clash. Ducks only the
specific instrumental partial beating against the vocal's harmonics, at partial (not
ERB-band) resolution — a narrower, less-destructive cut than a band-level masking duck.

---

## Final signal chain (engineer's ordering, as originally specified)

0. InputConditioner · 0.5 Input normaliser · 1. Analysis tap A · 2. De-click/de-crackle
· 3. De-hum · 4. Unified cleanup WOLA (denoise×dereverb×debleed×gate) · 5. Analysis tap
B · 6. Adaptive rumble HPF + de-plosive · 7. Gate/expander/breath · 8. Resonance
suppressor (Engine A+B) · 9. Dynamic EQ + Unmask · 9b. Dissonance Duck · 10. Compressor
A · 11. Effort Compression · 12. Compressor B · 13. De-esser · 14. Order-tracked
harmonic dynamic EQ (Mix only) · 15. Saturation · 16. Tonal EQ · 17. Transient shaper ·
18. Clarity (offline/Max quality only) · 19. Analysis tap C · 20. Output rider · 21.
True-peak limiter · 22. Metering (off-path).

*(Note: the master spec resolves this against the producer's ordering requirement that
all threshold-triggered dynamic EQ/resonance work sits AFTER compression — see
01_MASTER_SPEC.md §1 for the reconciled order.)*

---

## Open questions for human (engineer's list)

- Realtime-first or offline-first? Decides Engine A/B split, Clarity, and the
  drive-triggered 16x saturation switchover's tier placement.
- M12's alias gate at maximum drive is unmeetable by physics for non-Chebyshev curves —
  re-scope the bar, cap max drive, or disclose the honest surface: a product call.
- Mix-tier total latency grew 91.5 ms → 112.8 ms once M8b was correctly counted — is
  +21.3 ms acceptable given the latency story used competitively against Nectar?
- Clarity repositioned offline-only — confirm that's acceptable, or drop it.
- Ship any neural component at all? Spec remains deliberately 100% classical DSP;
  decide classical-only v1 (recommended) or fund a corpus acquisition programme.
- Scope: corrective chain only, or a full Nectar replacement (Reverb/Delay/Dimension/
  Voices/Backer)?
- Partial-Loudness Rider AND Dissonance Duck both need an instrumental sidechain, on top
  of Unmask — three best features now share Nectar's most-complained-about limitation.
- Effort Compression's Phi→tilt calibration needs a small graded-effort corpus — do we
  have studio access?
- Regression corpus ownership and timeline, now with two new required cases (drive
  sweep for the alias surface, compressor step-response sweep).
