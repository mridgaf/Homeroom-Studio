# Sonic Reference Engine — handoff brief

Read this first. It carries decisions, verified results, and known-unverified claims
from the design session. Everything marked UNVERIFIED must be tested, not assumed.

---

## What we're building

A production assistant that:

1. Takes a **reference track** the user likes.
2. Isolates the part he cares about (usually the bassline).
3. Measures it, measures **his** attempt at the same part, and describes the gap
   in plain language with a **named mechanism** — "that's saturation, not EQ."
4. Suggests settings **on plugins he actually owns**.
5. Applies them in the DAW, **re-renders, re-measures, and corrects itself**.

Step 5 is what separates this from every advice-only tool. The loop must close.

**Explicitly out of scope:** push-button "make mine sound like that." Not achievable.
The user stays in the loop making calls. Do not build toward autonomy.

---

## The user

- Non-technical explanations only. Short answers. No hedging, no flattery.
- Produces in **Reason 12**, does not use many factory sounds — he likes the rack
  and the routing, not the library.
- Mac: **Apple Silicon M2**. Demucs runs on MPS.
- Hardware: PreSonus AudioBox 96, Novation Launchkey MK3, Yamaha DTX400K,
  Yamaha EMX66M, Samson Servo 300, assorted guitar amps.
- **Plugin inventory is UNKNOWN.** Ask for it. Nothing downstream works without it.
- He has abandoned several previous attempts because results were unsatisfying.
  Ship something that produces a real, checkable result early.

---

## Decisions made

**DAW: REAPER** (~$60). Chosen for one reason: ReaScript can both read/write every
plugin parameter *and* render audio back to disk. That second half is what lets the
system grade its own work. Reason cannot hand audio back, which is why it can't be
the engine — though he can keep creating in Reason via the Reason Rack Plugin on a
REAPER track.

**Do not buy plugins yet.** REAPER's stock set (ReaEQ, ReaComp, ReaXcomp, etc.) is
free, documented, and cleanly addressable. Prove the loop, then buy for real gaps.

**Stack:** Python, numpy/scipy/soundfile, Demucs for stem separation. No GPU needed.

---

## VERIFIED result — read this before writing any analysis code

`analyzer.py` and `prove.py` are included. `prove.py` synthesizes one bass note through
five treatments (clean, soft saturation, asymmetric saturation, hard clipping, bitcrush)
and checks whether the measurements separate them.

**Run A — pure sine input: 6/7 checks passed.**
The distortion metrics work. Hard clipping read +85 dB odd-dominant. Asymmetric
saturation read +0.6 dB (even harmonics present — the "warm" signature). Bitcrush was
the only treatment flagged inharmonic. THD ranked correctly.

**Run B — realistic sawtooth bass: 3/7 checks passed. Every distortion metric failed.**
Hard clipping measured *lower* THD than the clean signal.

**Why, and this is the central design constraint:**
A real bass already carries ~82% harmonic content before you touch it. Saturation adds
no measurable harmonics on top of that — it compresses, so *relative* harmonic levels
go down. The source's own timbre drowns the effect.

**Consequences:**

- **Never score a sound in isolation.** "This bass is 24% THD, therefore it's clipped"
  is meaningless on real music. Absolute distortion metrics are noise.
- **The comparator is the product, not the analyzer.** Always diff two harmonic
  ladders. The *tilt* of the difference is the signal, not the numbers.
- Referencing isn't a feature of this system. It's the only thing that functions.

**Known bug in the current analyzer:** spectral centroid is used as a brightness proxy,
but saturation sustains the low fundamental on a decaying note and pulls centroid
*down*. Failed in both runs. Measure centroid on the sustain portion, or replace with
band-energy ratios.

---

## UNVERIFIED — test before building on these

- **Reason Rack Plugin parameter exposure.** Claimed from a third-party blog, not
  Reason's docs. Unknown how parameters are exposed to a host, or how many. If it's a
  small fixed bank requiring manual assignment, the Reason-inside-REAPER plan gets
  materially worse. Test early.
- **`bonfire-systems/reaper-mcp`** (~123 stars, 11 commits) was recommended off its
  README. Never run. Treat as a lead, not a dependency. Writing a thin ReaScript
  bridge directly may be cleaner.
- **"Griminess = odd harmonics through 2–3kHz"** was one hypothesis stated too
  confidently. Could equally be bitcrushing, layered noise, amp/cab coloration, tape,
  or a dirty DI. Let the measurements decide, per-case.
- **Stem separation damages the evidence.** A Demucs bass stem carries bleed and
  artifacts, and mastering already reshaped it. Quantify how much this distorts the
  measurements before trusting them.
- **Soloed ≠ in the mix.** The reference bass sounds grimy *against those drums*.
  Matching it soloed can produce something wrong in his mix.

---

## Build order

1. **Comparator** — diff two analyses, output plain-language gap + named mechanism.
   This is the product. Build it before anything else.
2. **Stem pipeline** — Demucs wrapper, MPS on M2. Measure the artifact cost.
3. **Plugin inventory** — scan REAPER's FX list via ReaScript, build JSON of every
   plugin with parameter names and what each knob does sonically. This is the piece
   missing from all his previous attempts, and it's what makes "using the tools at my
   disposal" mean anything.
4. **REAPER bridge** — set parameters, render, re-analyze. Closes the loop.
5. **Brain** — Claude with the above as tools; recipe files as memory.

---

## Reusable from his old `reason_voice` project

Located at `~/Desktop/Homeroom Studio/reason_voice`.

| Keep | Why |
|---|---|
| `recipes.py` | Markdown+YAML recipe format with `accuracy`, `status`, `technique`, `sounds_like`. Correct schema for a knowledge base. Keep the format even if the code is rewritten. |
| `search.py` | Fuzzy + synonym-expanded search |
| `indexer.py` | Drive scanning, tokenizing |
| `crates.py` | Saved collections |
| `static/` | Working web UI |

| Discard | Why |
|---|---|
| `reason_control.py` | 10 MIDI CCs + `open -a Reason`. Dead end. |
| `intents.py` | Regex keyword matching. Replace with an LLM tool-call loop. |
| `midi_ptt.py`, `templates.py` | Reason-specific |

Note: that project had **no LLM in it at all** and no evaluation of whether its advice
was good. Both gaps must be closed here.

---

## Open questions for the user

1. **What plugins do you own?** Blocking everything.
2. **One real case** — a track, the bassline, what you tried, why it failed.
3. **How will you know it's working?** There is currently no ground truth. His old
   recipes had an `accuracy` field he filled in by ear after the fact, which means
   there's no way to tell whether a change improves the system or degrades it.
   Establish a small test set early.
