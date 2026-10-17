# Chapter 06: Vocal processing research
## Part 3 of 3

_The AI vocal processor research: spec, findings from real stems, reference vocals, handoff._

**In this part:**
- 07_REFERENCE_VOCALS.md — Reference vocals — Jay-Z, Tupac, Eminem
- HANDOFF.md — HANDOFF — AAA AI Vocal Processor ("vox")

(Next: end of chapter)


=====================================================
SOURCE FILE: 07_REFERENCE_VOCALS.md
ORIGINAL LOCATION: WT:vox/docs/07_REFERENCE_VOCALS.md
=====================================================

# Reference vocals — Jay-Z, Tupac, Eminem

Research pass, 2026-08-14. Sourced from engineer interviews (Sound On Sound,
Waves, Gearspace, Equipboard), not from tutorial-blog paraphrase where
avoidable. Nothing here is built yet. This document exists so the build starts
from evidence instead of vibes.

Provenance tags: `[verified]` = stated by the engineer who did the work.
`[recalled]` = widely reported, weaker sourcing. `[inferred]` = my reasoning.

---

## 0. The finding that reorganises everything

The three sounds are **not three mix chains**. They are three different KINDS
of thing, and only one of them is mostly mixing.

| | What actually makes the sound | Reachable by processing one take? |
|---|---|---|
| Jay-Z | **Mix identity.** One engineer, consistent chain. | **Yes — mostly.** |
| Eminem | **Arrangement identity.** 3–6 separate real overdubs, panned. | **Partly.** Needs takes from him. |
| Tupac | **Performance + tracking identity.** One take, sung hot, minimal processing. | **Partly.** Some is the performance. |

This is why "apply a look to my lyrics" works cleanly for one of the three and
needs his participation for the other two. That's not a limitation of the tool —
it's what those records actually are.

---

## 1. Jay-Z

The owner's note is correct and it is the key to this entry: **Jay-Z has used
many producers** — Ski, DJ Premier, Just Blaze, Kanye, Timbaland, Pharrell,
No I.D., Mike Dean. The beats have nothing in common.

The vocal still sounds like Jay-Z on all of them.

**Because the constant is not the producer — it's Young Guru.** Guru has mixed
10 of Jay-Z's 12 albums `[verified]`. The producer changes; the vocal engineer
doesn't. That is the entire reason a "Jay-Z look" is a coherent thing to build,
and it means the target is Guru's chain, not any producer's.

### Tracking `[verified]`
- Neumann U87 or U67 → **Avalon VT-737** (using its preamp *and* its compressor)
- 24-bit / 44.1 kHz into Pro Tools. Guru is explicitly not a high-sample-rate guy.

### Mix `[verified]`
- **Fairchild 660** (Waves) on *every* vocal track — lead and ad-libs alike.
  Guru's words: it "glues them together without having this super compressor sound."
  Read: gentle, slow, colouring — not a level-control compressor.
- **ADL 1500** in series after it — "presence that the plug-in can't do."
  So: **two compressors in series, each doing a little**, not one doing a lot.
- **Two Focusrite 110 EQs** after compression. EQ AFTER compression, not before.
- **Lexicon 480** reverb.
- **TC Electronic D-Two, quarter-note delay.** Note: 1/4, not the dotted-eighth
  that's fashionable now.
- Lead, doubles and ad-libs all get the **same** processing `[verified]`.

### The philosophy `[verified]`
Guru's teaching is built around **subtractive EQ**: he makes room for the vocal
by carving the *beat*, not by boosting the voice. He also stresses clip-gaining
before any processing.

**What this means for us:** the Jay-Z look is a *restraint* profile. Two gentle
compressors, EQ after them, cuts not boosts, a plate and a 1/4-note delay.
Nothing extreme anywhere. That is very buildable.

---

## 2. Eminem

### Tracking `[verified]`
- **Sony C800G** → **Avalon VT-737**. Same mic Dre uses; Em has always used it.
- 44.1/24 into Pro Tools, tracked in a large live room with gobos.

### Mix `[verified — Mike Strange, SOS]`
- Compression: **Alta Moda Unicomp**, plus a **Requisite L2M** tube mastering
  compressor — "on every song I've recorded for Em."
- **Massenburg EQ** on the rap vocals. SSL console EQ + compression.
- Delay: **TC 2290**. Reverbs: Bricasti, Eventide 2016, Lexicon 480 & PCM70, SPX90.
- **Distortion**: made by driving the vocal hard from the Alta Moda back into
  the SSL returns. Not a plugin — a deliberate overdrive stage.

### The part that is NOT mixing `[verified]`
- Rap vocals **double-tracked throughout**.
- Hooks recorded **five times**. Bridges **six times**. Real overdubs, not copies.
- **"I have never done vocal comps for him."** No comping. Every take is a take.

`[recalled]` Em has described four dubs: one screamed, one whispered, two normal;
dubs panned to different places rather than stacked in one spot, with different
dynamics per dub.

`[recalled]` Common reconstruction: 3 tracks, two panned ~65% L/R and dropped in
level under a centre lead, the group bus-compressed in parallel.

**What this means for us:** the crispness people hear as "Eminem" is largely
**many real takes, panned wide, at different intensities**, plus a hard-driven
distortion stage. Fabricating that from one take is exactly the STACK problem
already documented in `01_MASTER_SPEC.md`. Confirms the earlier decision: STACK
should align and glue **real takes he records**, not synthesise fake ones.

---

## 3. Tupac

### Tracking `[verified]`
- Death Row: **Neumann U87** → Neve or SSL 4000 preamp → **Studer A800** tape.
- Other rooms `[verified — engineer Paul Arnold]`: U87 through an SSL E preamp
  and its onboard compressor (Quad, NYC); later an **AKG 414** through an SSL G
  preamp with the console compressor or a **dbx 160**.

### The defining fact `[verified]`
**"One-Take Tupac."** *All Eyez on Me* was recorded in about two weeks. Speed
and performance, not production, are the sound.

**What this means for us:** the Tupac profile is the *least* processed of the
three. Console compressor, tape, room, done. Two things carry it:

1. **Tape.** The Studer A800 is doing real work — soft saturation, gentle
   high-end loss, transient rounding. That is `Saturation` + a tilt, and it's
   buildable.
2. **Analogue console compression**, which behaves differently from a modern
   digital compressor — softer knee, program-dependent release.

`[inferred]` The risk with this profile is faking rawness by *adding* dirt.
Correct move is the opposite: take processing away, then add tape.

---

## 4. Common ground across all three

Worth noting how much overlaps — this is the "studio quality baseline" the
owner asked for, and all three sit on top of it:

- **Large-diaphragm condenser → Avalon 737 or an SSL/Neve channel.** Every one.
- **Compression in stages**, each doing a few dB. Never one compressor doing 10.
  `[recalled]` Dre's *In Da Club* chain: ~7:1, medium attack, fast release,
  3–4 dB typical, up to 7 dB on peaks.
- **Vocals mixed deliberately loud.** `[recalled]` Dre mixes them a little hot
  on purpose so mastering's bass doesn't bury them.
- **Doubles are recorded, never generated.** All three.
- Hardware reverb + a tempo-synced delay. Delay time is the main dialect
  difference (Jay 1/4, modern rap 1/8D).

`[recalled]` Measurable targets from mix-analysis literature: lead vocal
integrated loudness ≈ **4.5 LUFS below** the full mix (range 3–6); for rap,
momentary vocal **4–6 dB above** the instrumental.

---

## 5. How we get past "clearly in the lane"

The owner asked for as close as possible, not just the right neighbourhood.
The honest engineering path:

**We cannot copy the gear.** No Fairchild, no Studer, no C800G, no SSL.
Modelling each box by ear is how you land at "in the lane" and stop.

**We can copy the RESULT, measured.** Take actual reference records, measure
what the vocal is doing, and make our output hit the same numbers:

| Measure | What it captures |
|---|---|
| Long-term spectrum of the vocal | tone — the single biggest identity cue |
| Crest factor / short-term dynamics | how hard it's compressed, and how fast |
| Vocal-to-beat loudness ratio | how forward the voice sits |
| Stereo width vs. frequency | how the doubles are spread |
| Harmonic distortion vs. level | how much tape/drive is on it |
| Reverb decay + pre-delay, delay time | the space |

Six numbers per artist. Then it's a closed loop: measure the target, measure our
render, correct the difference. Same method already proven on THROW's ducking,
where an open-loop control delivered 4.3 dB for a requested 6 and the closed
loop delivered 5.93.

That is the difference between imitating settings and matching an outcome, and
it is the only route to "as comparable as possible" that doesn't depend on
owning the rack.

**Requirement:** this needs real reference audio. Isolated vocal stems would be
ideal; full mixes are workable for some measures and useless for others.

---

## 6. Open questions

**BLOCKING — reference audio.** Section 5 is the whole plan and it can't start
without files. What can the owner supply?

**BLOCKING — the Eminem profile.** Its core is 3–6 real takes. Is he willing to
record doubles, or does the Eminem look have to work from a single take?
The answer changes what gets built, not just how well it works.

## Sources

- [Secrets Of The Mix Engineers: Young Guru — Sound On Sound](https://www.soundonsound.com/techniques/secrets-mix-engineers-young-guru)
- [Mike Strange Jr: Eminem *Recovery* — Sound On Sound](https://www.soundonsound.com/techniques/mike-strange-jr-eminem-recovery)
- [Young Guru: The Art of Vocal Mixing and Subtractive EQ — Waves](https://www.waves.com/waves-premium-masterclasses-young-guru)
- [2Pac — Equipboard](https://equipboard.com/pros/2pac)
- [Eminem — Equipboard](https://equipboard.com/pros/eminem)
- [What gear was used to record Pac vocals — Gearspace](https://gearspace.com/board/rap-hip-hop-engineering-and-production/380555-what-gear-used-record-pac-vocals.html)
- [Eminem vocal stacks — Gearspace](https://gearspace.com/board/rap-hip-hop-engineering-and-production/178467-eminem-vocal-stacks.html)
- [Secrets to Mixing Rap Vocals — Produce Like A Pro](https://producelikepro.com/blog/mixing-rap-vocals/)
- [The Perfect Vocal Loudness (Backed by Data) — Mastering The Mix](https://www.masteringthemix.com/blogs/learn/the-perfect-vocal-loudness-with-data)

=====================================================
SOURCE FILE: HANDOFF.md
ORIGINAL LOCATION: WT:vox/HANDOFF.md
=====================================================

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

=== END OF PART ===
