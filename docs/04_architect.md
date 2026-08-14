# ARCHITECT SPEC — Round 4 (hardened after 8 objections)

**Role:** Staff software architect — owner of the module contract, parameter/state
model, assistant solver, and the Python→JUCE port path. Deliverable is the architecture
that Phase 1 (offline Python stem processor, runs today) and Phase 2 (VST3/AU) both
live inside without a rewrite. Every objection from round-3 adversarial review is
correct and closed below by a concrete, testable fix — nothing here disputes the
adversary's findings.

---

## Adversary objections and how each was resolved

| # | Severity | Objection | Resolution |
|---|---|---|---|
| 1 | Fatal | BreathControl's "gain relative to the FOLLOWING phrase" was an offline, whole-file-shaped algorithm placed as an always-on real-time stage with undeclared, unbounded lookahead — and missing from the document's own degradation table every other offline module honestly appears in | Split exactly as demanded: the always-on RT chain now runs a strictly causal surrogate (running K-weighted median of the PRECEDING 3 voiced phrases, zero forward lookahead beyond the stage's declared `max_lookahead_samples`); the follow-phrase mode is reclassified `OFFLINE_ONLY`, added to `vox.core.rt`'s degradation table, and only runs behind the transport-stopped Analyze pass — identical treatment to Rider, LUFS-I, and RT60. |
| 2 | Major | The executive summary's "runs today on numpy/scipy/soundfile, zero pretrained weights" claim was false given the `lfilter` ban and an undecided kernel-runtime question — a 15-stage chain of biquads/compressors/resonance suppression/multiband saturation as pure-CPython scalar loops isn't usable | **Decided**, not left open: Phase 1 hard-depends on **numba** (`njit(cache=True, fastmath=False)`) for the `@kernel` path. Numba is a JIT-compiler dependency, not a model or weight file — claim corrected to "zero pretrained weights; numba is a build/runtime compiler dependency, not a model," which is now true. |
| 3 | Major | No denormal policy in the Stage contract | Same fix as Engineer objection 3: Chain-level FTZ/DAZ once per `process()`, documented as non-numerically-transparent, plus a per-`@kernel` 1e-20 anti-denormal bias immune to the Python/C++ boundary. New CI test `assert_no_denormal_stall`, forced-off FTZ/DAZ run included. |
| 4 | Major | S3's bisection referenced an undefined RT statistic | Same fix as Engineer objection 4: F13, a 96-bin/768-byte/O(1)-per-frame decaying histogram, now a published AnalysisBus feature, not a hidden solver detail. |
| 5 | Major | Solver constants in S1/S2/Policy were unlabeled | Every constant gets an explicit CONSTANT PROVENANCE tag — "tunable default, range R, sensitivity-tested" — with a per-constant CI test bounding solver OUTPUT stability under a ±20% perturbation. Explicitly NOT a correctness claim; that's deferred to the (not-yet-existing) corpus. |
| 6 | Minor | DynamicEQ/TonalEQ structural capacity understated at 8/4 nodes vs. BAR item 9's 24 | Corrected to 24 nodes each (48 total). Raises the accepted CPU floor substantially — flagged more urgent, not less. |
| 7 | Major | Per-stage internal Wet/Dry reintroduces comb filtering if the dry tap isn't delay-matched to the stage's own latency | Stage contract rule: any stage with `HAS_INTERNAL_MIX=True` must route its dry tap through the SAME shared `DelayLine` primitive `ParallelSplit` uses, sized to `latency_samples()`. New CI test `assert_wet_dry_nulls`, parameterized over every stage declaring internal mix (9+ stages — Compressor A/B, both EQs, De-Esser, Saturation, Delay, Dimension, Reverb). |
| 8 | Minor | Preset format's "no variable-length arrays anywhere" claim contradicted itself (programs and profile.events ARE variable-length) | Invariant restated precisely: it applies ONLY to the flat, fixed-cardinality `params` map. `programs` and `profile.events` are separately, explicitly capped (64 programs/20,000 points each; 64/128/128 events by salience rank; 8 MB total blob) and enforced by a new CI test, `test_preset_size_caps` — no cap violation is ever silently accepted into a written blob. |

---

## Modules

### vox.core.stage — the Stage contract
Every processing element (including the chain itself) is a pure function of
`(state, params, input)`. Denormal policy (see objection 3) and the internal-mix
DelayLine rule (objection 7) are now part of the base contract, not left to each
stage's discretion. Float64 throughout; per-sample recursion lives only in `@kernel`
functions, policed by an AST test.

### vox.core.params — declare-once parameter registry + codegen
One declaration drives the offline CLI, preset schema, assistant's legal move set, and
the future JUCE UI. `assist_min`/`assist_max = None` on a param makes the AI
structurally incapable of touching it — codegen now renders this as a visible
"manual-only" badge, not a hidden implementation detail.

### vox.core.chain — Chain, ParallelSplit, Oversampled, PDC, automation slicer
Latency composition (`Chain L = sum(child L)`), bit-accurate bypass
(`assert_bypass_nulls` at −120 dB), and now internal-mix null-testing
(`assert_wet_dry_nulls`) at every stage boundary. Structural EQ node counts corrected
to 24×2 = 48 (objection 6), which is now the accepted CPU-cost floor.

### vox.analysis — feature front-end, AnalysisBus, VocalProfile
F1–F12 as before, plus new **F13 RT level histogram**: 96 log-spaced bins over
[−70, +12] dBFS, decaying update (tau tier-configurable: Live 2.0 s / Tracking 4.0 s /
Mix 8.0 s), O(1) per frame, 768 bytes/instance — feeds the compressor bisection solve
and is itself a testable, published bus feature.

### vox.assistant.target — the Target document
Targets as diffable, human-editable data (LTAS curves, scalar targets, vetoes, solver
policy) — unchanged from round 2, survived round-3 review without objection.

### vox.assistant.solve — the deterministic staged solver (this IS the AI Assistant)
Staged solve (S0 integrity → S1 HPF/gate → S2 subtractive EQ → S3 dynamics → S4 tonal →
S5 character/space/output), Huber-loss objective, hard cages, named vetoes, full audit
trail. S3 now reads the F13 histogram instead of an undefined tap (objection 4); every
S1/S2/Policy constant carries a CONSTANT PROVENANCE label (objection 5); S4's ≤4-node
closed-form solve is now explicitly the assistant's default WRITE PATTERN over
TonalEQ's actual 24-node structural capacity (objection 6).

### vox.io.preset — preset/state format and migration
One serialization for CLI config, plugin state blob, and regression harness input.
Fixed-cardinality invariant restated precisely and scoped correctly (objection 8);
`programs`/`profile.events`/total blob size all explicitly capped and enforced in CI.

### tests/ — the verification harness
Framework-level tests parameterized over every Stage (`assert_bypass_nulls`,
`assert_latency_matches_impulse`, `assert_no_alloc_in_process`, `assert_param_cage`,
etc.), plus five new tests demanded by round-3 review: `assert_no_denormal_stall`,
`assert_wet_dry_nulls`, `assert_solver_rt_tick_bounded`,
`assert_solver_constant_sensitivity`, `test_preset_size_caps`.

### vox.core.rt — the real-time / offline duality layer
Draws the MUST-BE-REAL-TIME-SAFE / MAY-BE-OFFLINE-ONLY line. Numba dependency now
decided (objection 2). Degradation table gains the breath-event row (objection 1):
follow-phrase mode → offline-only Analyze pass; always-on RT surrogate → causal
preceding-3-phrase median, same treatment LUFS-I's rolling-window surrogate already
gets in the same table.

---

## Novel effects

### CONVEX RIDE — the provably optimal fader
Global optimum of `min ||L + g − T||_1 + λ·TV(g)` via Condat's taut-string TV1D
algorithm — O(n), 7.2 ms measured on a 3000-point envelope, no iteration/convergence
risk. Correctly declared `OFFLINE_ONLY` with a stated, bounded receding-horizon RT
surrogate (warm-started, still O(n)).

### MOVING TARGET — a target that follows the arrangement
Morph between target curves (keyframed, re-solved at each tick) or drive the target
from the instrumental bed in real time (Bark-spreading masking model → target LTAS),
bounded by the same trust region and cages as every other solver write. Morphing in
MEASUREMENT space, not parameter space, is only cheap because `solve()` is pure,
deterministic, and bounded-time.

### RESIDUAL — audition and edit the error, not the settings
Solo what the chain is still failing to fix, hear it, then drag that curve — you are
editing the Target document itself, and the chain re-solves around your edit. Requires
the residual to be a first-class persisted object, which only exists because the
assistant is a solver against an explicit target rather than a preset lookup.

### EVENT PROGRAMS — per-breath, per-plosive, per-sibilant parameter programs (revised)
Plosive/sibilant modes need only a short, declared, bounded lookahead (30 ms / 150 ms,
folded into the stage's existing budget) — never the objection's target. Breath's
follow-phrase mode is now correctly offline-only (see objection 1); the always-on path
is the causal preceding-phrase-median surrogate.

### SEAMLESS COMP WELD — invisible comp-take splices via change-point matching
The effect chosen specifically to dodge the killed breath effect's prior art by making
**no real-time claim anywhere in its design** — comp-take welding is definitionally a
whole-file problem (you cannot match a segment to segments you haven't identified yet,
in either direction, without seeing the whole composite). CUSUM change-point detection
on LUFS-S + spectral centroid; closed-form gain + 2-band tilt match per segment, written
as a timestamped parameter program.

---

## Final signal chain (architect's ordering, as originally specified)

0. InputConditioner · 0.5 Input normaliser · 1. RumbleHPF+PlosiveTamer · 2. Repair
(denoise/dereverb) · 3. Gate/Expander/BreathControl (causal surrogate) · 4. Analysis tap
A · 5. ResonanceSuppressor · 6. DynamicEQ (24 nodes) · 7. CompressorA · 8. CompressorB ·
9. DeEsser · 10. Saturation · 11. TonalEQ (24 nodes) · 12. TransientShaper · 13. Rider
(Convex Ride) · 14. TruePeakLimiter · 15. OutputStage · Parallel: Doubler/Reverb/Delay/
Dimension, ducked from the dry vocal envelope.

*(Note: the master spec reconciles this against the producer's requirement that
threshold-triggered dynamic EQ/resonance work sit AFTER compression — see
01_MASTER_SPEC.md §1.)*

---

## Open questions for human (architect's list)

- float64 everywhere in C++, or float64 filter state / float32 buffers? Real SIMD-width
  cost either way; needs sign-off.
- The corrected CPU number: EQ structural capacity is now 48 nodes, not the round-1
  documents' 4x-disagreeing estimates — needs a per-tier number before the
  system-requirements page is written.
- numba packaging/platform/CI matrix — which Python versions/platforms get wheels, and
  what's the fallback story on a platform numba doesn't support (currently none).
- Latency tier switching stays transport-stopped-only — acceptable, or does Live need to
  pad to Mix's latency?
- Does the offline Analyze pass survive contact with the plugin UX? Now load-bearing for
  THREE features (Convex Ride, breath refinement, Comp Weld) — if users won't press the
  button, all three ship reduced.
- Where do the target curves come from, legally and practically? Blocks Target
  derivation AND the solver's own constant provenance table.
- How much of Nectar's module list is v1 scope, now with the corrected 48-node EQ cost?
- Detector strategy once learned weights exist — version forever, or version presets and
  accept audible drift on plugin update?
- Preset size caps (8 MB / 64-128-128 / 20,000 points) are proposed defaults, not
  measured against real sessions — need sign-off or a measurement pass.
