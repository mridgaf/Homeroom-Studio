# HANDOFF — AAA AI Vocal Processor ("vox")

Written 2026-08-13 for whoever (human or Claude session) picks this up next.
Read this top to bottom before touching code — it'll save you from re-finding
bugs that are already found, documented, and regression-tested.

## What this is

A vocal-stem cleanup + processing chain meant to match-or-beat iZotope
Nectar 4 Advanced, built by a producer/DSP-engineer/architect design process
with adversarial review at every stage (each proposer's spec had to survive
a hostile industry-expert critique before being accepted). Phase 1 (current)
is a Python/numpy/scipy offline processor, proving the DSP is correct and
the product is good, before Phase 2 ports it to a JUCE VST3/AU plugin.

**Run this first:**
```bash
cd vox
PYTHONPATH=src python3 -m pytest tests/ -v
```
Expect **174 passed, 1 xfailed** (as of 2026-08-19). The xfail is
load-bearing — it's a regression guard on a known, documented, unfixed bug
(see below). If it starts passing unexpectedly (XPASS), something changed —
investigate before removing the marker, don't just delete it.

Note the suite takes ~95 s, up from ~40 s. That is the true-peak meter and
limiter running at 16x oversampling instead of 4x/8x, which is what it costs
for the ±0.1 dBTP bar to be met rather than asserted. See
`docs/05_FINDINGS.md`, "True-peak accuracy re-measured".

## Read these in order

1. **`docs/00_BAR.md`** — the quality gate. Nectar 4's actual verified
   feature list, plus our non-negotiable engineering requirements (null
   test < −120 dB, aliasing < −90 dBFS, true-peak accurate to ±0.1 dBTP,
   BS.1770-4 loudness). Every module is judged against this.
2. **`docs/05_FINDINGS.md`** — everything measured on the synthetic test
   bench (`vox.testsignal`, a source-filter voice model with known ground
   truth). Meter validated against EBU Tech 3341. Aliasing floors for every
   saturation config. The two limiter bugs found and fixed, with numbers.
3. **`docs/06_REAL_STEM_FINDINGS.md`** — what happened on the first REAL
   vocal file. This is the important one: the synthetic bench did **not**
   catch the two worst bugs in the project. Real material did, in about
   ten minutes of listening. Read this before trusting any synthetic-bench
   result as sufficient.
4. **`docs/design_process/`** — round1/round2 markdown from the producer,
   DSP engineer, and architect design agents, plus their adversarial
   reviews. `round1_engineer.md` in particular has a full alternative
   signal-chain spec (dual-rail architecture, per-stage algorithm choices,
   latency/CPU budgets) that **has not yet been reconciled** with what's
   actually built in `chain_demo.py` — see "Outstanding work" below.

## Current state — what's real and verified

| Module | File | Status |
|---|---|---|
| Loudness/true-peak/null/alias meter | `vox/meter.py` | Validated against EBU Tech 3341, BS.1770-4 Annex 2. Trust this — everything else is graded against it. |
| Synthetic test vocal w/ ground truth | `vox/testsignal.py` | Source-filter voice model + known room IR + known noise. Useful for DSP correctness, **not sufficient alone** for judging cleanup-stage quality — see finding above. |
| Gate, DeEsser, ParametricEQ, Compressor, Saturation | `vox/dsp/modules.py` | Hand-rolled, null-tested at bypass settings, Saturation passes the −90 dB alias bar at 8× oversampling (4× measurably fails — kept as a documented regression test). **Four real bugs fixed 2026-08-19** — see "The 2026-08-19 adversarial pass" below. |
| Limiter | `vox/dsp/modules.py` | Hand-rolled, true-peak (not sample-peak) detection, **16× oversampled since 2026-08-19** (8× did not meet the ±0.1 dBTP bar). **Two real bugs found and fixed during this project** — sample-peak-only detection (up to 2.3 dB overshoot), then rectify-before-interpolate (up to 2.3 dB *more*, root cause). Now 0 dB worst-case overshoot on a 12-freq/4-phase sweep, matches an independent reference to 0.003 dB. See `test_limiter_detector_matches_reference_meter`. |
| De-reverb | `vox/dsp/dereverb.py` | **Broken, OFF by default.** Habets/statistical late-reverb suppression. Cannot distinguish a sustained held note from a reverb tail — confirmed on real material and now regression-tested (`test_dry_sustained_tone_is_not_treated_as_reverb`, xfail). Needs a redesign (onset-gating or externally-supplied RT60), not a parameter tweak. See `06_REAL_STEM_FINDINGS.md` for the specific fix options considered. |
| ML denoise | `vox/engines/denoise_dfn.py` | Real pretrained model (DeepFilterNet3, MIT/Apache-2.0, weights cached at `~/.cache/DeepFilterNet`). Good at noise floor (~25 dB reduction, verified). **OFF by default** — it's speech-trained, not singing-trained, and measurably suppresses sustained non-speech-like content (~59 dB at full wet on a pure tone). Regression-tested (xfail). |
| ReverbSend, Dimension (chorus/phaser) | `vox/dsp/pedalboard_modules.py` | Phase-1-only, built on `pedalboard` (Spotify's JUCE-adjacent library). Wired into the default chain but **mix=0 (inert) by default**. `pedalboard.Limiter` and `pedalboard.Distortion` are explicitly NOT used anywhere — both measured worse than our own modules (see `06_REAL_STEM_FINDINGS.md`). Cannot ship in the eventual JUCE plugin (Python-only lib) — Phase 2 needs a native reimplementation. |
| Full chain scaffold | `vox/chain_demo.py` | `build_chain()` / `run_dsp_chain()` / `run_full_pipeline()`. This is a **scaffold to prove interop**, not the final product chain — the real chain comes out of reconciling `docs/design_process/round1_engineer.md`'s spec with what's built. |

## Outstanding work, roughly in priority order

1. **Reconcile `chain_demo.py` with `docs/design_process/round1_engineer.md`.**
   The engineer's spec describes a more sophisticated architecture (dual-rail,
   two-stage compression, a dedicated resonance-suppression "crown jewel"
   stage, split fast/slow gain riding) than what's actually wired up. Read
   that doc, decide what to adopt, build it, verify it the same way
   everything else here was verified (bypass null, then working null,
   then real-material listening test — don't skip the last one).
2. **Fix or replace de-reverb.** See the "What would actually fix this"
   section in `06_REAL_STEM_FINDINGS.md` for three concrete approaches.
   Whatever you build, keep `test_dry_sustained_tone_is_not_treated_as_reverb`
   and make it pass for real — don't loosen the threshold to cheat it.
3. **Decide the denoise strategy.** VAD-gated blend (only denoise between
   phrases, where there's no vocal to damage) is probably the highest-value,
   lowest-risk fix — it sidesteps the "not trained on singing" problem
   entirely rather than trying to solve it.
4. **The adversarial design workflow's effect shortlist was never delivered
   to the user.** A background Workflow run (producer/engineer/architect
   agents + adversaries) was designing the 3 novel vocal effects the user
   asked for. It hit a session token limit mid-run, was resumed, and its
   final status was not confirmed complete before this session's context
   moved on to real-stem debugging. **Check `docs/01_MASTER_SPEC.md` — if
   it doesn't exist, the synthesis never finished; re-run or re-do it
   before the user can pick their 3 effects.**
5. **Validate ReverbSend/Dimension on real material.** They're verified for
   bypass-cleanliness and basic sanity, but never A/B'd on an actual vocal
   the way the core chain was. Do that before recommending non-zero mix
   defaults.
6. **Process the full "delo mirror" file**, not just the 20 s test segment
   (2:56–3:16), once the chain is in a state worth spending the ~6 minutes
   of render time on. Staged at
   `/mnt/user-data/uploads/Desktop/delo mirror 18 13 26.wav` this session;
   re-stage via `device_stage_files` if it's gone.
7. **JUCE/C++ port planning.** Nothing has been ported yet. `vox/core.py`'s
   `Module` interface was designed to transliterate cleanly (block-based,
   explicit state, no whole-file tricks in real-time-legal modules) — but
   this has not been tested against actual JUCE code, only designed for it.

## Ground rules this project has been operating under

- **Never trust a claim without a measurement.** Every number in the docs
  has a reproducible test behind it. If you add a capability, add the test
  that proves it, in the same commit/session, not later.
- **The synthetic test bench is necessary but not sufficient.** It catches
  DSP-correctness bugs (aliasing, true-peak overshoot, null-test failures)
  well. It did NOT catch the de-reverb/denoise content-destruction bugs —
  those only showed up on a real vocal take. Test on real material before
  trusting a cleanup-stage default.
- **Quality bar is `docs/00_BAR.md`**, not vibes, not "sounds cool." Every
  module gets judged against Nectar 4's actual feature list and our
  measurable engineering requirements.
- **Be honest about tool provenance.** `ReverbSend`/`Dimension` are clearly
  marked Phase-1-only in their own docstrings because they depend on a
  Python library that can't ship in the final plugin. Don't let a
  convenient prototype quietly become an assumed permanent dependency.


## The 2026-08-19 adversarial pass — read this before adding a module

A hostile reviewer that did not write this code was pointed at all of
`src/vox`. Six real bugs came out, four of them shipping in all three artist
presets. Every one of them lived in one of **two blind spots**, and both are
now guarded by `tests/test_latency_and_mix.py`, parametrized over the module
list so the next module added is checked for free:

1. **Partial mix.** Every test in the project used `mix=0` (a null test) or
   `mix=1` (no dry path at all). The product ships partial mix everywhere, so
   the one region that mattered was the one region nothing exercised.
2. **Latency.** Nothing ever compared a module's reported `latency_samples()`
   to its measured impulse delay.

What that combination hid:

- **`Saturation` was a comb filter at every mix value the presets use.** The
  wet path is delayed 32 samples by the oversampling FIRs; the dry path
  wasn't. Notches every fs/32 (≈1370 Hz at 44.1 k). Re-rendering after the
  fix restored **up to +7 dB of high end** on the Tupac and Eminem presets.
  If you are looking for the cause of the "muffled" complaint in
  `06_REAL_STEM_FINDINGS.md`, start here.
- **`Chain` had the identical bug**, in a class whose docstring advertised
  "dry-path delay compensation" it did not implement.
- **`Gate` amplified the room tone it exists to remove**, up to +2.95 dB
  inside its hysteresis window, because the expander shortfall was measured
  against the wrong threshold. The only gate test held the gate permanently
  open.
- **`Gate` silently discarded its own `attack_s`/`release_s`.**
- **`Limiter` spliced audio out of the stream** when `lookahead_ms` changed
  mid-stream.
- **`DeEsser.mix` was a −70 dB notch generator** (allpass wet blended against
  dry).

And one non-bug worth more than some of the bugs: **the limiter's true-peak
accuracy claim was never tested.** Its "independent reference" was the same
algorithm as its detector. When actually graded against a different one, the
4× meter missed the project's own ±0.1 dBTP bar by 0.464 dB.

The lesson to carry forward is the same one `06_REAL_STEM_FINDINGS.md` already
recorded, one level up: **a test that only exercises the settings the product
doesn't ship is not evidence.** Before trusting a module, ask which of its
parameter space is actually covered.

Also note, still open: every test in this project runs at **48 kHz**, while
both reference acapellas are **44.1 kHz**. The presets run and stay finite at
44.1/96 k, but nothing is graded there.
