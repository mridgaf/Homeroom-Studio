# Chapter 11: Sonic reference engine and AI assistant research
## Part 1 of 4

_Research on analyzing reference tracks, REAPER control, and AI production assistants; plus the equipment list._

**In this part:**
- DECISIONS.md — Decision Ledger — Sonic Reference Engine
- EQUIPMENT.md — Equipment — what this studio can and cannot make

(Next: Part 2 of 4)


=====================================================
SOURCE FILE: DECISIONS.md
ORIGINAL LOCATION: HS:sonic/DECISIONS.md
=====================================================

# Decision Ledger — Sonic Reference Engine

Read this at the start of a session. Append to it at the end. Update `status`
on old entries when you learn what actually happened — don't just pile on new
entries.

Scope: this project only. The Beat Machine and vocal-processing decisions live in
`../DECISIONS.md`. Cross-project standing rules live in
`~/Documents/ClaudeMemory/PREFERENCES.md`.

## Entry format

```
### [YYYY-MM-DD] Short title
- Context: what was going on / what problem this addressed
- Decision/change: what was actually done
- Reasoning: why this over the alternatives
- Verify by: how to check if this held up (test, re-check, "ask user next time")
- Status: open | confirmed | failed
- Outcome: (filled in later, when known)
```

---

## Log

(new entries go below this line, most recent first)

### [2026-08-24] Comparator built — and the centroid fix in the ledger was wrong
- Context: build-order step 1, the only unbuilt piece of the product. Also asked
  to fix the `open` spectral-centroid bug while in `analyzer.py`.
- Decision/change: `comparator.py` + `prove_comparator.py` added. `brightness()`
  and `hf_above_ladder_db` added to `analyzer.py`; `centroid_hz` kept but
  documented as unusable on bass.
- **The ledger's proposed centroid fix does not work, and I measured it before
  writing it.** "Measure centroid on the sustain portion" assumed the whole-file
  Welch average was being reweighted by the decay tail. Gated the spectrum to
  frames within 20 dB of the loudest and compared: **identical to three
  significant figures on all ten test files.** A 3-second note at a 32768-sample
  window is only 7 frames and the loudest already dominates. The real cause is
  simpler — on a 55 Hz note the fundamental holds so much energy that the
  centroid barely moves however much dirt you add (clean saw 107 Hz, hard-clipped
  91 Hz). It is the wrong shape of measurement for bass, not a windowing problem.
  The ledger's *second* option (band-energy ratios) was the right one.
- Replaced with `brightness_db` = energy above 4*f0 vs below, pitch-relative so
  it means the same on a 55 Hz bass as a 220 Hz one. `prove.py` sine control
  6/7 -> **7/7**.
- **But absolute brightness still cannot see dirt on realistic material**, and
  that failure is now locked in as an expectation rather than papered over. On
  the sawtooth every treatment reads DARKER than clean, because saturation
  compresses and the upper partials fall relative to the fundamental. Same wall
  THD hit. The realistic-bass run is 3/7 -> 4/7 and the three remaining failures
  are the documented finding, not regressions.
- **Comparator rules, and what they were measured on.** Scores are
  evidence/just-noticeable so dimensions rank on one scale; no hard gates,
  the ranking decides:
    * digital grit — inharmonic energy. CATEGORICAL precedence over drive: no
      analog drive produces inharmonic content.
    * drive — high-frequency content and crest factor moving in OPPOSITE
      directions (geometric mean). EQ does the first without the second, a
      compressor the second without the first. This is the load-bearing rule.
    * EQ — ladder tilt, requires a usable ladder.
    * compression — dynamic range MINUS whatever drive/grit already explains,
      since both compress as a side effect and charging the same dB twice let
      "compression" win on a plainly saturated sound.
- **Two artifacts had to be killed first, both from the synthetic source.** The
  test sawtooth is band-limited to 11 partials, so comparing partials 12-16
  compared two noise floors and read as a +26 dB "ladder shift" that was
  nothing. Gating the ladder to partials above -60 dB in BOTH files fixed it and
  turned the realistic table from unusable into 6/6. Thresholds were NOT tuned
  to make tests pass — see the JND table's comment.
- Verify by: `../.venv/bin/python prove_comparator.py` — 13/13, including all
  six known treatments named correctly on the realistic bass.
- Status: confirmed
- Outcome: build-order step 1 DONE. Review pass found three real bugs, all now
  regression-tested: white noise was named "digital grit, clear, 196x" (guard
  only fired when BOTH files were unpitched); a mono-vs-stereo pair scored
  stereo width at infinity and buried every real finding (`analyzer.stereo()`
  returns -inf for mono and `_finite` only screened NaN); and the drive and
  compression rules only fired when the REFERENCE was the dirtier file, so a
  too-driven bounce of his own would have reported nothing.

### [2026-08-22] PROVEN: ReaScript can drive every plugin — and the Reason caveat was right
- Context: the entire REAPER decision rested on one untested assumption — that a
  script can read AND write plugin parameters on this machine. `reaper/
  setup_and_inventory.lua` ran on the owner's Mac and settled it.
- Decision/change: the REAPER bet is confirmed. Build the parameter-control layer
  on ReaScript as planned. Separately, close the Reason-Rack-Plugin question as
  NEGATIVE.
- Reasoning: **19 of 19 plugins writable.** The script wrote a parameter, read it
  back, and confirmed the change stuck on every one, then restored it. Named,
  meaningful parameters on everything that matters:
    * Gateway (NAM), 16 params: Input, Threshold, Bass, Middle, Treble, Output,
      NoiseGateActive, ToneStack, IRToggle, OutputMode, Wet, Delta
    * Obliterate, 25 params: Input/Output Level, Mix, **Obliterate**, Frequency,
      Resonance, Algorithm, Filter Amount 1/2, Filter Shape 1/2, Wet, Delta —
      the grime engine is fully addressable
    * Addictive Trigger: Trig Threshold/Sensitivity/Hold/Blend, per-drum
      Level/Pan/Width — real drum-replacement control
    * Ultra Analog: VCO PW/Sync/Rate, Filter Resonance/Frequency/Envelope,
      Amp ADSR
    * ReaEQ 19, ReaComp 24, ReaXcomp 51, ReaSamplOmatic5000 33 — all real
- **Reason Rack Plugin: the pessimistic reading was correct.** It reports 2,570
  parameters, but **2,560 of them are literally named `Param 1000` … `Param 3559`**
  — a fixed bank of empty slots that must be hand-assigned inside the rack. Only
  ten are real, and they are MIDI globals (Pitch Bend, Mod Wheel, Breath,
  Expression, Damper, Channel Pressure, Bypass Rack). This is exactly the failure
  mode flagged as UNVERIFIED on 08-21: "if it is a small fixed bank requiring
  manual assignment, the Reason-inside-REAPER plan gets materially worse." It is.
  Reason can be automated only for parameters he maps by hand, one at a time.
- Verify by: `sonic/plugin_inventory.json` (1.1 MB) holds every parameter name,
  value, range and formatted display. Re-run the script after any plugin change.
- Status: confirmed
- Outcome: build-order step 3 (plugin inventory) is DONE, and generated rather
  than hand-written. Three plugins were not found — `fast-balancer`, `Massive`,
  `Absynth 4`. Massive and Absynth ship as VST2/AU only with no .vst3, so this is
  a REAPER scan-path setting, not a missing plugin. Re-run after enabling AU.


### [2026-08-22] Fast measurement is a disk problem, not a CPU problem
- Context: this project's whole design is measure -> compare -> correct in a
  loop, so how cheap a measurement pass is decides whether the loop is worth
  having. Benchmarked that assumption against the sibling beat-machine corpus
  before building anything on it. `bench_parallel.py` added here.
- Decision/change: do not design around multi-core measurement. Design around
  where the audio LIVES.
- Reasoning: the per-file numpy measurement runs at ~147 MB/s single-threaded
  and parallelises 2.77x across 4 cores — but at that speed a ~1.8 GB corpus
  is ~12 seconds of arithmetic. The equivalent pass on the beat machine took
  20 minutes, reading from an external drive. Compute was ~1% of it. The same
  trap is waiting here: Demucs stems, batch renders and reference libraries
  are all bulk audio, and reading them from the wrong place will dominate
  every timing in this project.
- Verify by: run `bench_parallel.py` cold against whatever corpus this project
  ends up reading; it reports read-time vs compute-time and names the
  bottleneck. Re-check after the Demucs stage exists, since stems change the
  file-size profile.
- Status: open
- Outcome: shapes a decision already logged elsewhere — 86 GB free of 494 GB.
  Working audio wants to be on the internal SSD for speed and cannot all fit.
  That tension is a real design constraint, not an afterthought.


### 2026-08-21 Reason cannot be the engine — REAPER chosen
- Context: owner produces in Reason 12 and asked whether to force it to work
  with an AI control layer, or buy a different DAW.
- Decision/change: buy REAPER (~$60) as the engine. Keep creating in Reason via
  the Reason Rack Plugin on a REAPER track.
- Reasoning: Reason's Remote codecs can address parameters on the *targeted*
  device and send value feedback, so dial control is not literally impossible —
  but only one device is addressable at a time, every device type needs
  hand-mapping, and **no audio comes back**. A system that cannot hear its own
  output can never grade its work. REAPER's ReaScript can both set every plugin
  parameter and render audio to disk, which closes that loop.
- Verify by: confirm ReaScript render + `TrackFX_GetParam` round-trip on the
  owner's machine.
- Status: open

### 2026-08-21 The comparator is the product, not the analyzer — PROVEN
- Context: built `analyzer.py` to measure sound character, and `prove.py` to
  test whether "griminess" is measurable at all.
- Decision/change: never score a sound in isolation. Always diff two harmonic
  ladders. Referencing is not a feature of this system — it is the only thing
  that functions.
- Reasoning: ran the test twice. On a **pure sine**, 6/7 checks passed — hard
  clipping read +85 dB odd-dominant, asymmetric saturation read +0.6 dB (even
  harmonics, the "warm" signature), bitcrush was the only inharmonic one. On a
  **realistic sawtooth bass, 3/7 passed and every distortion metric failed** —
  hard clipping measured *lower* THD than clean. A real bass already carries
  ~82% harmonic content, so saturation adds no measurable harmonics on top; it
  compresses, and relative harmonic levels go down. Absolute distortion metrics
  are meaningless on real music.
- Verify by: `python3 prove.py` reproduces both runs.
- Status: confirmed

### 2026-08-21 Spectral centroid is a bad brightness proxy for decaying notes
- Context: the "dirt raises brightness" check failed in both test runs.
- Decision/change: measure centroid on the sustain portion, or replace it with
  band-energy ratios. Not yet fixed in `analyzer.py`.
- Reasoning: saturation acts as compression on a decaying note, sustaining the
  low fundamental and pulling the centroid *down* even as the sound gets
  audibly brighter.
- Verify by: re-run `prove.py` after the fix; the check should pass on both
  signal types.
- Status: confirmed (bug real), but the PROPOSED FIX WAS WRONG — see the
  2026-08-24 entry. Measuring on the sustain portion changes nothing; the
  band-energy ratio was the fix that worked.

### 2026-08-21 Claims made to the owner that were NOT verified
- Context: owner asked to be told where the assistant had been overconfident.
- Decision/change: logged here so the next session tests rather than inherits.
  1. Reason Rack Plugin exposes device parameters to host automation — sourced
     from a third-party blog, not Reason's docs. Slot count unknown. If it is a
     small fixed bank requiring manual assignment, the Reason-inside-REAPER
     plan gets materially worse.
  2. `bonfire-systems/reaper-mcp` recommended off its README (~123 stars, 11
     commits). Never run. A thin hand-written ReaScript bridge may be cleaner.
  3. "Griminess = odd harmonics through 2–3 kHz" was one hypothesis stated as
     fact. Could equally be bitcrushing, layered noise, amp/cab colour, tape,
     or a dirty DI.
  4. "~95% of the reason_voice codebase is portable" — invented figure, never
     measured.
- Verify by: each item is falsifiable by a direct test. Do them before relying
  on any of it.
- Status: open

### 2026-08-21 Plugin inventory is the missing piece in every prior attempt
- Context: owner has abandoned several previous builds as unsatisfying. His
  `reason_voice` project indexes patches and samples but has no record of what
  plugins exist or what their knobs do.
- Decision/change: build a plugin inventory (scan REAPER's FX list via
  ReaScript, annotate each parameter with what it does sonically) as step 3,
  before the DAW bridge.
- Reasoning: "using the tools at my disposal" is undefined without it — the
  system cannot recommend a setting on a plugin it doesn't know exists.
- Verify by: ask the owner for his plugin list; the inventory should match.
- Status: open

### 2026-08-21 No LLM was ever in the reason_voice loop
- Context: audited `~/Desktop/Homeroom Studio/reason_voice`.
- Decision/change: recorded as a finding. The new build must not repeat it.
- Reasoning: `intents.py` is regex keyword matching. There is no Anthropic or
  OpenAI call anywhere in the codebase. "Learning" was the owner hand-editing
  markdown recipes and flipping a `status` field. The brief's *fine-tunes,
  suggests, learns* was never implemented — which likely explains why the
  results were unsatisfying.
- Verify by: `grep -ri "anthropic\|openai" reason_voice/` returns nothing.
- Status: confirmed

=====================================================
SOURCE FILE: EQUIPMENT.md
ORIGINAL LOCATION: HS:sonic/EQUIPMENT.md
=====================================================

# Equipment — what this studio can and cannot make

The system's job is to say **what to play, on what, and what to run it through.**
That only works if it knows the real limits. Every entry below lists what the box
can produce AND what it cannot — the second half is what keeps the advice honest.
Recommending a half-open hi-hat swell on a switch pedal is worse than useless.

**Shape of this studio: hardware-first.** Most sound sources make their own noise
and arrive as recorded audio. Only guitar and bass DI pass through plugins. That
keeps the plugin list small — which is what the system wants.

---

## Sound sources

### Korg Kronos — the keyboard rig
Nine engines: **SGX-2** (grand piano), **EP-1** (six electric pianos),
**CX-3** (tonewheel organ), **HD-1** (PCM), **AL-1 / MS-20EX / PolysixEX**
(analogue modelling), **MOD-7** (FM), **STR-1** (plucked-string physical modelling).

- **Can:** essentially any keyboard part — acoustic piano, Rhodes/Wurli, organ,
  analogue-style synth, FM, plucked strings. Sound design happens on the box.
- **Cannot:** be adjusted by the computer. It is an audio source, not a plugin.
  The system directs the *performance and patch choice*; it cannot turn its knobs.
- **Instructions should look like:** "EP-1, a Rhodes with the tremolo slow and
  the bark dialled back — play it in the low-mid, let notes ring."
- **Do not recommend buying piano/keys libraries.** This outclasses them.

### Roland HandSonic HPD-15 — hand percussion
10-inch pad, 15 zones, 572 percussion sounds (Latin, African, Indian, Asian,
orchestral, FX), two ribbon controllers, D-Beam, pedal inputs for kick and hi-hat,
MIDI In and Out/Thru, stereo audio out.

- **Can:** hand percussion of almost any tradition, played with real dynamics;
  live timbre-shaping via ribbons and D-Beam; drive external gear over MIDI.
- **Cannot:** replace a kit. It is a percussion layer, not drums.
- **Underused asset.** Most producers do not have this. Reach for it when a part
  needs texture and human motion rather than a sampled loop.

### Yamaha DTX400K — the drum kit
Five-piece electronic kit. **USB MIDI only** (no MIDI ports).

- **Can:** timing and velocity for kick, snare, toms, cymbals. Good enough to
  perform a part and drive a sampler.
- **Cannot — and this constrains what the system may ask for:**
  - **Single-zone rubber pads** — no rim shots, no edge-vs-centre, no cross-stick
  - **Switch hi-hat** — open or closed only. No half-open, no swells, no foot splash
  - **No positional sensing**
  - Beaterless kick pedal; feel differs from an acoustic pedal
- **Never recommend:** articulation that depends on zone, position, or continuous
  hi-hat. Ask for patterns, dynamics and feel instead.
- **The upgrade that matters is the CONTROLLER, not software.** A continuous
  hi-hat or mesh pads raises what can be played. No sample library fixes a switch.

### Guitars and basses — real instruments
Played directly. The main thing plugins exist for in this studio.

### Novation Launchkey 49 MK3
MIDI controller — keys, pads, faders, knobs. Drives software; makes no sound.

---

## Amps — three different voices

| Amp | Character | Best use |
|---|---|---|
| **Crate** | modern, gritty | aggressive parts |
| **Epiphone Electar** | vintage, warm, boxy, breaks up sweetly | character, small-amp sounds |
| **Line 6 Spider** | modelling combo | practice; a third colour when reamped |

Three real amps in a real room is a genuine advantage. **Reamping** — sending a
recorded DI back out through an amp and micing it — produces air and speaker
movement that captures cannot fake. Use it when a part needs to sound like it
happened somewhere.

For straight recording, **Neural Amp Modeler** (free, open source) with captures
from TONE3000 will generally beat micing the Spider. The Crate and the Electar are
worth micing on their own terms.

---

## The signal path — and the one real ceiling

**PreSonus AudioBox USB 96 — two inputs.** This is the hard limit of the studio.

- One stereo source (Kronos, HandSonic) uses **both** inputs.
- So: **one thing at a time.** No two sources recorded together in stereo, and
  no multi-mic drum kit ever.
- For a one-person overdub workflow this is fine. The cost is re-plugging between
  sources, not lost capability.
- **This is the only place money would buy real capability** — and only if the
  workflow ever needs more than one source at once. It currently does not.

Also present: Yamaha EMX66M powered mixer, Samson Servo 300 power amp — PA gear,
not recording gear.

---

## Software — the plugins actually installed

Corrected 2026-08-22 by reading `/Library/Audio/Plug-Ins` directly. The owner said
he had "not many plugins" and that what he had was irrelevant. **Both were wrong**,
and taking it on trust nearly cost him $179 on a drum library he already owns.
Read the disk, not the summary.

### Instruments
| Plugin | What it is | Note |
|---|---|---|
| **Addictive Drums 2** | full drum library + mixer | **Already owned.** One of the three $179 options previously recommended. Do not buy a drum library. |
| **Addictive Trigger** | drum replacement / triggering | Turns DTX400K hits or recorded drums into better samples. Directly answers the kit's weak pads. |
| **Addictive Keys** | acoustic + electric keyboards | |
| **Lounge Lizard Session 4** (AAS) | modelled electric pianos | Rhodes / Wurli, physically modelled |
| **Strum Session 2** (AAS) | strummed guitar | |
| **Ultra Analog Session 2** (AAS) | analogue-modelling synth | |
| **Massive** (NI) | wavetable synth | |
| **Absynth 4** (NI) | semi-modular synth / atmospheres | |
| **Reason Rack Plugin** | the whole Reason rack, as a plugin | **The Reason-inside-REAPER path is already installed.** Test how many parameters it exposes to a host before designing around it. |

### Effects
| Plugin | What it is | Note |
|---|---|---|
| **Obliterate** (Newfangled Audio) | distortion / destruction | **The grime tool.** `vox/tools/ab_reference.py` already contains `saturation_vs_obliterate` — this was being A/B'd against his own DSP. Start here for "griminess". |
| **DS-10 Drum Shaper** | transient shaper | punch and body on drums |
| **AIR Multiband Filterbank** | multiband filtering | |
| **T-De-Esser** | de-esser | |
| **Clear** | his own build, July 2026 | from the `vox` project |
| **fast-balancer** | tone balancing | |

### Free, and still worth adding
| | |
|---|---|
| **REAPER** | bought and installed |
| **ReaPlugs** (stock) | ReaEQ, ReaComp, ReaXcomp, ReaDelay, ReaGate, ReaSamplOmatic5000 — documented and fully scriptable, so the system can master them completely |
| **Neural Amp Modeler** (free) | the one real gap: captures of specific amps for guitar and bass DI. Plugin ("Gateway") from neuralampmodeler.com/users, models from TONE3000 |
| **Own sample library** | 5,287 samples indexed, 2,943 of them drums |

**Total still to spend: nothing.** REAPER is bought; NAM is free; everything else is
already on the machine.

**Do not recommend buying more plugins.** The set above is already larger than the
system can master well. Ten tools known completely beat thirty half-known.

## What this means for the advice the system gives

1. **Most answers are performance instructions, not knob positions.** "Play this,
   on that, with that patch" — then a short chain in REAPER.
2. **Check the instruction against the limits above before giving it.** If the kit
   cannot play it, it is not advice.
3. **Reach for hardware first.** The Kronos and HandSonic will beat a plugin
   substitute nearly every time, and they are already owned.
4. **Reamping is available and rare.** Three amps and a room is a real option most
   in-the-box setups do not have.

=== END OF PART ===
