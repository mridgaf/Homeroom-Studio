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
Expect **43 passed, 2 xfailed**. The 2 xfails are load-bearing — they're
regression guards on known, documented, unfixed bugs (see below). If either
one starts passing unexpectedly (XPASS), something changed — investigate
before removing the xfail marker, don't just delete it.

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
| Gate, DeEsser, ParametricEQ, Compressor, Saturation | `vox/dsp/modules.py` | Hand-rolled, null-tested at bypass settings, Saturation passes the −90 dB alias bar at 8× oversampling (4× measurably fails — kept as a documented regression test). |
| Limiter | `vox/dsp/modules.py` | Hand-rolled, true-peak (not sample-peak) detection. **Two real bugs found and fixed during this project** — sample-peak-only detection (up to 2.3 dB overshoot), then rectify-before-interpolate (up to 2.3 dB *more*, root cause). Now 0 dB worst-case overshoot on a 12-freq/4-phase sweep, matches an independent reference to 0.003 dB. See `test_limiter_detector_matches_reference_meter`. |
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
