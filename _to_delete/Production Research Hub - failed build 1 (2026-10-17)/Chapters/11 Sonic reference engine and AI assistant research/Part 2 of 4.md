# Chapter 11: Sonic reference engine and AI assistant research
## Part 2 of 4

_Research on analyzing reference tracks, REAPER control, and AI production assistants; plus the equipment list._

**In this part:**
- HANDOFF.md — Sonic Reference Engine — handoff brief
- README.md — Sonic Reference Engine
- START-HERE.md — How to start this in Claude Code

(Next: Part 3 of 4)


=====================================================
SOURCE FILE: HANDOFF.md
ORIGINAL LOCATION: HS:sonic/HANDOFF.md
=====================================================

# Sonic Reference Engine — handoff brief

Read this first, then `DECISIONS.md`. Everything marked UNVERIFIED must be tested,
not assumed. Last revised 2026-08-24.

---

## What we're building

A production assistant that:

1. Takes a **reference track** the owner likes.
2. Isolates the part he cares about (usually the bassline).
3. Measures it, measures **his** attempt at the same part, and describes the gap
   in plain language with a **named mechanism** — "that's saturation, not EQ."
4. Suggests settings **on plugins he actually owns** (see `EQUIPMENT.md` and
   `plugin_inventory.json` — both are real, generated, and current).
5. Applies them in REAPER, **re-renders, re-measures, and corrects itself**.

Step 5 is what separates this from every advice-only tool. The loop must close.

**Explicitly out of scope:** push-button "make mine sound like that." Not achievable.
The owner stays in the loop making calls. Do not build toward autonomy.

---

## The owner

- Non-technical explanations only. Short answers. No hedging, no flattery, no
  rose-tinted framing. Push back when he's wrong.
- Analogies help. Pictures and links help.
- Produces in **Reason 12**, doesn't use many factory sounds — he likes the rack
  and the routing, not the library.
- Mac: **MacBook Pro 14" 2023, `Mac14,9`, Apple M2 Pro, 10 cores, 16 GB, arm64,
  macOS Tahoe 26.5.2 (build 25F84)** — measured, not guessed. This is a fast,
  current machine; nothing gets ruled out "because the hardware is old." Demucs
  runs on MPS, under a minute a song.
- **Disk is the binding constraint, not the CPU: 86 GB free of 494 GB (17%).**
  This project makes audio at every step — stems, batch renders, model
  downloads. Check free space before a batch, delete intermediates after, keep
  anything bulky on `/Volumes/TBOTC 3`. `.gitignore` keeps rendered audio out of
  the repo; it does not keep it off the disk.
- Hardware-first studio: Korg Kronos, Roland HandSonic HPD-15, Yamaha DTX400K,
  three real amps, two-input AudioBox. Full detail and — more importantly — the
  **limits** are in `EQUIPMENT.md`. Read it before giving any performance advice.
- He has abandoned several previous attempts because results were unsatisfying.
  Ship something that produces a real, checkable result early.

---

## Decisions made

**DAW: REAPER** (~$60, bought and installed). Chosen for one reason: ReaScript can
both read/write every plugin parameter *and* render audio back to disk. That second
half is what lets the system grade its own work.

**Do not buy plugins.** Nothing is missing. The owned set is already larger than the
system can master well. Ten tools known completely beat thirty half-known.

**Stack:** Python, numpy/scipy/soundfile, Demucs for stem separation. No GPU needed.

**Design around where the audio lives, not around CPU.** Measurement runs ~147 MB/s
single-threaded and parallelises 2.77x — but on the sibling beat-machine corpus,
compute was ~1% of wall time and disk reads were the rest. `bench_parallel.py`
re-checks this; run it cold once stems exist.

---

## VERIFIED — actually run, with results

### The REAPER bet is confirmed. 19 of 19 plugins writable by script.
`reaper/setup_and_inventory.lua` ran on the owner's Mac. It wrote a parameter, read
it back, confirmed the change stuck, and restored it — on every plugin. Named,
meaningful parameters throughout: Obliterate exposes 25 including `Obliterate`,
`Algorithm`, `Frequency`, `Resonance` (the grime engine is fully addressable);
Gateway/NAM 16; ReaXcomp 51; ReaEQ 19; ReaComp 24; ReaSamplOmatic5000 33.
Output: `plugin_inventory.json` (1.1 MB) — every parameter name, value, range and
formatted display. **Build-order step 3 is done, and generated rather than
hand-written.** Re-run the script after any plugin change.

### The Reason Rack Plugin is a dead end for automation. Confirmed negative.
It reports 2,570 parameters, but **2,560 are literally named `Param 1000` …
`Param 3559`** — a fixed bank of empty slots requiring hand-assignment inside the
rack. Only ten are real, and they're MIDI globals (Pitch Bend, Mod Wheel, Breath,
Expression, Damper, Channel Pressure, Bypass Rack). The pessimistic reading flagged
on 08-21 was correct. Reason can be automated only for parameters he maps by hand,
one at a time. Plan accordingly — do not design a feature that depends on this.

### Absolute distortion metrics are meaningless on real music.
`prove.py` synthesizes one bass note through five treatments and checks whether the
measurements separate them. **Pure sine input: 6/7 passed.** Hard clipping read
+85 dB odd-dominant; asymmetric saturation read +0.6 dB (even harmonics — the "warm"
signature); bitcrush was the only inharmonic one. **Realistic sawtooth bass: 3/7
passed, every distortion metric failed** — hard clipping measured *lower* THD than
clean.

Why: a real bass already carries ~82% harmonic content before you touch it.
Saturation adds no measurable harmonics on top — it compresses, so *relative*
harmonic levels go down. The source's own timbre drowns the effect.

**Consequence, and this is the central design constraint:** never score a sound in
isolation. Always diff two harmonic ladders. The *tilt* of the difference is the
signal, not the numbers. Referencing isn't a feature of this system — it's the only
thing that functions.

### The old reason_voice project had no LLM in it at all.
`intents.py` is regex keyword matching; no Anthropic or OpenAI call anywhere.
"Learning" was the owner hand-editing markdown recipes and flipping a `status`
field. The brief's *fine-tunes, suggests, learns* was never implemented — which
likely explains why the results were unsatisfying. Do not repeat this.

---

## Known open bugs

- ~~Spectral centroid is a bad brightness proxy.~~ **FIXED 2026-08-24**, but not
  the way this brief said. "Measure on the sustain portion" was measured and
  changes nothing (7 Welch frames; the loudest already dominates). The real
  cause: on a 55 Hz note the fundamental holds so much energy the centroid
  barely moves whatever you do to it. Replaced by `analyzer.brightness()` —
  energy above 4*f0 vs below. Sine control 6/7 -> 7/7. Note that absolute
  brightness *still* cannot see dirt on realistic material, for the same reason
  THD cannot; that is now an asserted expectation in `prove.py`, not a bug.
- **Three plugins missing from the scan** — `fast-balancer`, `Massive`, `Absynth 4`.
  Massive and Absynth ship VST2/AU-only with no .vst3, so this is a REAPER scan-path
  setting, not a missing plugin. Enable AU scanning and re-run the Lua script.

---

## UNVERIFIED — test before building on these

- **`bonfire-systems/reaper-mcp`** (~123 stars, 11 commits) was recommended off its
  README. Never run. Given that the hand-written Lua script worked first time,
  writing a thin ReaScript bridge directly is probably cleaner. Treat as a lead.
- **"Griminess = odd harmonics through 2–3 kHz"** was one hypothesis stated too
  confidently. Could equally be bitcrushing, layered noise, amp/cab coloration, tape,
  or a dirty DI. Let the measurements decide, per-case.
- **Stem separation damages the evidence.** A Demucs bass stem carries bleed and
  artifacts, and mastering already reshaped it. Quantify how much this distorts the
  measurements before trusting them. Testable without the owner: mix a known bass
  with known drums, separate, measure the error against the original.
- **Soloed ≠ in the mix.** The reference bass sounds grimy *against those drums*.
  Matching it soloed can produce something wrong in his mix.
- **"~95% of the reason_voice codebase is portable"** — invented figure, never
  measured. Don't cite it.

---

## Build order — current state

1. **Comparator** — ✅ **DONE 2026-08-24.** `comparator.py`, proved by
   `prove_comparator.py` (13/13). Names drive vs EQ vs compression vs digital
   grit on a realistic bass — the case where every absolute metric failed —
   and refuses unpitched, silent or pure-tone input rather than guessing.
   Ranked findings, plain language, `--json` for the step-5 brain.
   **Still unproven on real audio: every number so far is synthetic.** The
   owner's reference/attempt pair is the next real test.
2. **Stem pipeline** — Demucs wrapper, MPS on M2. Measure the artifact cost. NOT BUILT.
3. **Plugin inventory** — ✅ **DONE.** `plugin_inventory.json`, generated by
   `reaper/setup_and_inventory.lua`.
4. **REAPER bridge** — parameter read/write ✅ **PROVEN**. Render-to-disk and
   re-analyze NOT BUILT. This half is what closes the loop.
5. **Brain** — Claude with the above as tools; recipe files as memory. NOT BUILT.

---

## Reusable from the old `reason_voice` project

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
| `reason_control.py` | 10 MIDI CCs + `open -a Reason`. Dead end — and the Reason automation finding above confirms it. |
| `intents.py` | Regex keyword matching. Replace with an LLM tool-call loop. |
| `midi_ptt.py`, `templates.py` | Reason-specific |

Also present: `../vox/tools/ab_reference.py` already contains a
`saturation_vs_obliterate` comparison — prior art for A/B'ing his own DSP against
Obliterate. Worth reading before writing the comparator.

---

## Open questions for the owner

1. **One real case** — a reference track, the bassline, what he tried, why it failed.
   Still the top blocker, and now the sharpest one: the comparator is built and
   every number in it came from synthesized audio.
2. ~~How will we know it's working?~~ **Partly answered.** `prove_comparator.py`
   is a ground-truth set: six treatments applied by us, so the right answer is
   known, and the comparator must name each one. It caught three real bugs
   already. It does NOT cover real recorded material — bleed, noise floor, room,
   a mastering chain — so it is a floor, not a ceiling.

=====================================================
SOURCE FILE: README.md
ORIGINAL LOCATION: HS:sonic/README.md
=====================================================

# Sonic Reference Engine

Reference a track, measure the gap to your own, name the mechanism, set the
parameters, re-render, check. A production assistant with ears and a memory —
not an autopilot.

## Start here

- **`HANDOFF.md`** — the design brief. Read it first. Everything marked
  UNVERIFIED must be tested, not assumed.
- **`DECISIONS.md`** — the decision ledger. Read the `open` entries before
  starting work; append at the end of a session.

## What's here now

| File | What it is |
|---|---|
| `analyzer.py` | Measures a sound's character: fundamental, harmonic ladder, odd/even ratio, THD, inharmonic share, band energy, crest, envelope, stereo |
| `prove.py` | The go/no-go test. Synthesizes one bass note through five kinds of dirt and checks the metrics separate them |
| `comparator.py` | **The product.** Diffs two sounds and names the mechanism behind the gap in plain language |
| `prove_comparator.py` | The comparator's answer key: six treatments with known causes, plus the refusal cases |

## The finding that shapes everything

Run `python3 prove.py`. It runs twice:

- **Pure sine — 6/7 checks pass.** The distortion metrics work. Hard clipping
  reads odd-dominant, asymmetric saturation reads even-dominant, bitcrush is
  the only inharmonic one.
- **Realistic bass — 3/7 pass.** Every distortion metric fails. Hard clipping
  measures *lower* THD than clean.

A real bass already carries ~82% harmonic content before you touch it.
Saturation adds nothing measurable on top — it compresses, so relative
harmonic levels go *down*.

**So: never score a sound in isolation.** Diff two harmonic ladders and read
the tilt. The comparator is the product; the analyzer is a component of it.

## Using it

```bash
../.venv/bin/python comparator.py reference.wav mine.wav
```

Two sounds in; a ranked list of what differs and the mechanism behind each,
in plain words. It compares one pitched instrument against another and will
refuse a full mix, a drum stem, silence or a pure tone rather than guess.
Pitch and level are normalised away, so a quiet D1 against a loud A1 still
reads true.

Prove it: `../.venv/bin/python prove_comparator.py` — 13/13.

**Every number in it is synthetic so far.** Real recorded audio is the next test.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy soundfile
python3 prove.py
```

Stem separation (Demucs) comes later — runs on MPS, under a minute a song on
an M2.

## Build order

1. ~~**Comparator**~~ — ✅ done, `comparator.py`
2. **Stem pipeline** — Demucs wrapper; measure how much separation artifacts
   distort the numbers
3. **Plugin inventory** — scan REAPER's FX list, record what each knob does
   sonically. This is the piece missing from every previous attempt
4. **REAPER bridge** — set parameters, render, re-analyze. Closes the loop
5. **Brain** — Claude with the above as tools, the ledger as memory

=====================================================
SOURCE FILE: START-HERE.md
ORIGINAL LOCATION: HS:sonic/START-HERE.md
=====================================================

# How to start this in Claude Code

Four steps. Takes about ten minutes.

---

## 1. Make a folder for the project

Open **Terminal** (press Cmd+Space, type "Terminal", hit Enter). Paste this and press Enter:

```
mkdir -p ~/Desktop/"Homeroom Studio"/sonic && cd ~/Desktop/"Homeroom Studio"/sonic
```

That makes a new folder called `sonic` and moves you into it.

---

## 2. Put the three files in it

Drag `HANDOFF.md`, `analyzer.py`, and `prove.py` from your Downloads into that
new `sonic` folder in Finder.

---

## 3. Install Claude Code

Back in Terminal, paste this and press Enter:

```
curl -fsSL https://claude.ai/install.sh | bash
```

When it finishes, close Terminal and open it again. Then check it worked:

```
claude --version
```

You should see a version number. If you'd rather not use Terminal at all, there's a
desktop app instead — download it from claude.ai and open the `sonic` folder in it.
Same thing, with buttons.

---

## 4. Start it

```
cd ~/Desktop/"Homeroom Studio"/sonic
claude
```

It'll ask you to log in through your browser the first time. Then paste this as your
first message:

> Read HANDOFF.md. It's a brief from a design session about a sound-matching tool
> I'm building. Start with the comparator — step 1 in the build order. Before you
> write anything, ask me for my plugin list and a real example to work from.

That's it. From there just talk to it normally.

---

## What to expect

It will ask you for your plugin list first. Have that ready — it's the thing that
blocks everything else.

It can install Python packages, run the analyzer on real audio, and eventually drive
REAPER for you. You don't need to know any of that. Tell it what you want and tell it
when the result is wrong.

**One habit worth having:** when it says something works, ask it to prove it by running
something. That's how the last session caught a test that was passing for the wrong
reason.

=== END OF PART ===
