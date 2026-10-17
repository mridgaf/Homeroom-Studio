# Chapter 03: Mixing, routing and buses
## Part 3 of 4

_How to wire effects, buses and sends in Reason, plus the Reason 12 template and technique library (by genre and by type)._

**In this part:**
- 00-index.md — Reason 12 Templates & Techniques — Reference Index
- combinator-workflow.md — Combinator & Workflow — Unique & Surprising Techniques
- cv-routing.md — CV & Routing — Unique & Surprising Techniques
- drums.md — Drums — Unique & Surprising Techniques
- instruments-synths.md — Instruments & Synths — Unique & Surprising Techniques
- mixing-mastering-creative.md — Mixing & Mastering — Unique & Surprising Techniques
- original-ideas.md — Original Ideas — 🧪 My Own Proposals, Not Sourced, Not Tested
- sampling-vocal.md — Sampling & Vocal — Unique & Surprising Techniques
- edm-future-bass.md — EDM / Future Bass / Electronic — Producer Templates
- hip-hop-trap.md — Hip-Hop / Trap — Producer Templates

(Next: Part 4 of 4)


=====================================================
SOURCE FILE: 00-index.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/00-index.md
=====================================================

# Reason 12 Templates & Techniques — Reference Index

A standalone research document, separate from the Hip-Hop Recipe Book system. Built from a deep-dive search of Reason Studios' own documentation, Sound on Sound's Reason column, the ReasonTalk forum, Reddit's r/reason and r/reasoners, Audeobox's Reason learning library, reason101.net's device-hacking archive, and a few other producer-facing sources — plus a handful of original ideas of my own.

## How this is organized

Three folders, three different jobs:

- **`templates-by-genre/`** — how professional producers structure a Reason 12 project (rack setup, instrument choices, signal chain) for a given genre. One file per genre. This is the write-up.
- **`techniques-by-type/`** — unusual, surprising, or advanced Reason techniques that aren't genre-specific, grouped by what part of the rack they touch (drums, synths, CV routing, Combinator/workflow, sampling/vocal, mixing/mastering). Also a write-up.
- **`built-patches/`** — the actual Reason files. Real `.cmb` Combinator patches and `.rns` song files, sorted into genre folders (matching `templates-by-genre/`'s genre list), ready to drop into your rack. This is a living library, not a one-time snapshot: as we build our own templates together, they get added here too, genre by genre.

## Sourcing key

Every entry is tagged so you can weigh it correctly:

- **[Sourced]** — pulled from a specific article, forum post, or official tutorial, with a link in that file's Sources section.
- **[Adapted]** — general production knowledge (not Reason-specific in the source) that I've mapped onto specific Reason 12 stock devices.
- **[🧪 Original]** — my own proposal. Not pulled from anywhere, not tested in a session. Treat these as hypotheses worth trying, not verified fact.

I did not skim — several of these came from fetching full articles and forum threads, not just search snippets. Two sources (a ReasonTalk guitar-Combinator thread and a MacProVideo mastering article) blocked automated fetching after two attempts each; I've noted what I could still glean from their search snippets and moved on rather than working around the block.

## Files

**Templates by genre:**
1. `templates-by-genre/hip-hop-trap.md`
2. `templates-by-genre/rock.md`
3. `templates-by-genre/pop-vocal.md`
4. `templates-by-genre/edm-future-bass.md`
5. `templates-by-genre/lofi-hiphop.md`
6. `templates-by-genre/techno-house.md`
7. `templates-by-genre/mastering-universal.md`

**Techniques by type:**
1. `techniques-by-type/drums.md`
2. `techniques-by-type/instruments-synths.md`
3. `techniques-by-type/cv-routing.md`
4. `techniques-by-type/combinator-workflow.md`
5. `techniques-by-type/sampling-vocal.md`
6. `techniques-by-type/mixing-mastering-creative.md`
7. `techniques-by-type/original-ideas.md` — my own proposals, clearly marked 🧪, not sourced or tested

**Built patches (real files, by genre):**
- `built-patches/README.md` — what's here and why
- `built-patches/pop-vocal/` — SlapGuruVOX5.cmb (Yana Mahal's official vocal chain Combinator)
- `built-patches/hip-hop-trap/` — 2× Granular Drum Machine Combinators (Reason Studios)
- `built-patches/edm-future-bass/` — Wonderland.rns (reason101.net hybrid rhythm/synth patch)
- `built-patches/techno-house/` — 2× Audiomatic Kong Switcher Combinators + 2× Granular Drum Machine Combinators
- `built-patches/rock/`, `built-patches/lofi-hiphop/`, `built-patches/mastering-universal/` — empty for now, each with a README explaining why and what belongs there next

An HTML version with folder-style navigation was also published as an Artifact for browsing.

=====================================================
SOURCE FILE: combinator-workflow.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/combinator-workflow.md
=====================================================

# Combinator & Workflow — Unique & Surprising Techniques

## The 8-way instant preset switcher [Sourced — detailed]
The most elaborate Combinator build documented in this research. What it does: lets you instantly switch between 8 different Audiomatic Retro Transformer presets — even automate or randomize the switching — with zero audible glitch, plus a clean dry/wet bypass so silence isn't the default state.

**Structure:**
1. A 14:2 Mixer with channels 1–8 faders held at 0 — volume on every channel is controlled *entirely* by CV, never the physical fader.
2. A **Directre Audio Router** splits the incoming audio into 8 identical parallel paths.
3. **8 separate Audiomatic Retro Transformer units**, each loaded with a different preset, all processing the same input simultaneously and continuously (this is what makes switching instant — nothing has to load or spin up, you're just choosing which already-processed signal to let through).
4. A **Kong** with its 16 pads relabeled per-preset, used purely as a trigger surface — not a drum machine here.
5. A dedicated "Sequencer" Thor (all synthesis disabled) used purely as a MIDI step sequencer — Run Mode set to Repeat/Random, gate length 100%, a front-panel Button wired via MBRS (`Button1: 100 > S.Trig`) to start/stop it — whose Note/Gate output drives Kong's pad triggers directly.
6. Kong's per-pad Gate Out CV cross-routes into the Mixer's Level CV inputs (with a deliberate offset — pads 1–4 → channels 5–8, pads 5–8 → channels 1–4) so each pad hit gates that channel's volume open instantly. (Full CV mechanism detail in `cv-routing.md`.)
7. **The bypass problem and its fix**: since audio only comes through when a pad is actively held/triggered, a second Thor ("Bypass Gate," all synthesis disabled) is used purely as an audio-through gate: MBRS lines `Audio In1: 100 > Audio Out1 : -100 > MIDI Gate` (and the mirrored line for channel 2). The **negative** MBRS amount on MIDI Gate is the key detail — it means unprocessed audio passes through *only when no gate is active*, and cuts the instant a gate fires. A Spider CV Merger taps the Sequencer Thor's own Gate/Velocity CV and feeds it into the Combinator's CV Input 1 (Unipolar), mapped in the Programmer to mute the bypass Line Mixer's channel exactly when a wet pad is active — preventing the dry signal from doubling up with the wet one.

Source's own framing of why this works: *"Since the audio is always going through all 8 Audiomatic devices, the switch from Pad to Pad is instantaneous... However, when no pad is pressed, you won't hear anything. So let's set up our Combinator so that if the Pads are not pressed, the original audio still passes through."* [Source: reason101.net]

**Why it's worth knowing even if you never build this exact patch**: the underlying pattern — run N parallel processing chains continuously, gate which one's audible via CV instead of switching/reloading — generalizes to any "instantly switchable" effect or instrument bank you want to build, at the cost of N times the CPU load of a single chain.

## Combinator 2's "Source Range" macro trick — a DJ-style performance filter from a plain EQ [Sourced]
Documented directly by Sound on Sound as a showcase of a genuinely new Reason 12 Combinator feature. Route audio through the stock **Channel EQ**, and use a single macro knob to control the cutoff frequency of *both* the low-pass and high-pass filter stages — but instead of one knob doing both at once across its whole travel, use **Source Range** to make the knob only adjust the low-pass frequency when turned anti-clockwise from center, and only the high-pass frequency when turned clockwise, with a neutral dead zone left in the middle to return easily to a clean signal. A companion button switches both filters on/off together. This is the same underlying mechanic as a Novation Circuit's hardware performance filter, built entirely from a stock EQ and macro mapping — no RE required. [Source: Sound on Sound, "Reason: Exploring The New Combinator"]

## Building instruments by combining and cross-fading, not layering [Sourced]
- **Key zone + velocity switching combined**: a single Combinator can hold a bass synth in the low register, a clean pad in the mid register, and a lead with velocity-sensitive filtering in the high register — three different instruments, three different behaviors, one MIDI track. [Source: Audeobox]
- **Parallel effects inside a Combinator**: a Spider Audio splitter inside the Combinator sends audio to multiple effects chains at once (e.g. one path through distortion, one through chorus), recombined via an internal mixer — richer than any single serial chain, and it saves/loads as one device. [Source: Audeobox]
- **Nesting**: Combinators can be nested inside Combinators for complex multi-layered instruments, but is explicitly flagged as hard to manage and CPU-heavy past about two levels deep — a real practical ceiling, not just theoretical. [Source: Audeobox]

## Reusing pieces of a rack without a formal Song Template [Sourced]
Song Templates are the obvious tool, but Reason has a second, less-used path for reusing *parts* of a project rather than a whole starting rack:
- **Combine + Edit → Combine** packages a selected group of devices into a single portable Combinator patch file — the standard way to save an effects chain, a modular sound construction, or an instrument combination for reuse elsewhere. But Combinators specifically **cannot** include mixer channels — they're device-only.
- For mixer channels and their associated sequencer tracks, the actual mechanism is **Copy Devices and Tracks / Copy Channels and Tracks** (the Edit menu's actual command names, not just "Copy") — Reason allows multiple Song files open simultaneously, so you literally copy a chunk of one project's mixer+rack+tracks and paste it into another open project. This is how a producer can maintain a "library" Song file full of pre-built building blocks (vocal chains, drum groups) without needing them to be formal Templates at all. [Source: Sound on Sound, "Reason: Boost Productivity With Templates"]

## A real producer's actual daily template, described in detail [Sourced]
Worth reading as a model of restraint rather than maximalism: Sound on Sound's own Simon Sherbourne describes moving *away* from a more elaborate input-channel setup (found monitoring fiddly) toward going straight into audio tracks with Input Monitoring enabled — his template got simpler over time, not more complex. His current template: a few hardware synths + guitar wired to a USB mixer's physical inputs, Kong loaded, Komplete Kontrol host present for NI integration, and one favorite RE instrument of the moment loaded and ready. The lesson generalizes: a template is allowed to change as your workflow simplifies, and "what's my current favorite device" is a legitimate thing to keep swapping in a personal template rather than something to over-fix. [Source: Sound on Sound]

## Sources
- reason101.net, "Creative Reason Projects" archive — http://www.reason101.net/category/creative-reason-projects/
- Sound on Sound, "Reason: Exploring The New Combinator" — https://www.soundonsound.com/techniques/reason-exploring-new-combinator
- Audeobox, "Reason Combinator Guide" — https://www.audeobox.com/learn/reason/combinator-guide/
- Sound on Sound, "Reason: Boost Productivity With Templates" — https://www.soundonsound.com/techniques/reason-boost-productivity-templates

=====================================================
SOURCE FILE: cv-routing.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/cv-routing.md
=====================================================

# CV & Routing — Unique & Surprising Techniques

## Freezing/holding any CV value in place [Sourced — detailed]
Reason's CV system has no native "sample and hold a fader position" function. This technique builds one, using a vocoder as an unlikely CV-freeze utility.

**Core insight**: the BV512 Vocoder's Modulation input can be "held" (frozen mid-value) — something raw CV signals can't do on their own. So the trick converts CV → Audio → back to CV specifically to pass it through that hold-capable stage.

**The chain**: Fader CV output → **Thor** (converts CV to Audio internally; Thor's Modulation Bus Routing scales this conversion — a routing amount of **39** is the specific value cited as correctly scaling it) → **BV512 Vocoder**'s Modulation input → BV512 Band 1 output (now converted back to CV) → your actual destination (e.g. SubTractor's Amp or Pitch parameter). A toggle button, mapped through a Combinator, drives BV512's Hold function — while held, the CV value at that instant stays locked regardless of what the Fader does afterward.

**Practical use beyond a single fader**: the same chain freezes *any* CV signal at an arbitrary moment — e.g., freezing an LFO's value at whatever point it happened to be at when you hit the button, turning a moving modulation into a static one on demand.

**Refinement**: a community contributor (credited as "Eric Kloeckner" in the source) simplified the original two-Thor / two-toggle-button version down to 2 Thors and a single toggle button. **Multi-function fader**: using two parallel BV512 chains (each independently held via its own toggle) lets one physical Fader control two completely different destination parameters, switched by which toggle is active — effectively doubling your physical control surface without more hardware. [Source: reason101.net]

## Kong pads used as a CV/gate crossbar switch [Sourced — detailed]
This is really a Combinator-building technique that lives on CV routing — see `combinator-workflow.md` for the full macro-wiring context. The CV mechanism itself: Kong's per-pad **Gate Out CV** was cross-routed directly into a Mixer's **Level CV inputs**, so a pad hit gates that mixer channel's volume open *instantly* — no crossfade ramp, no audible click — because the audio path itself never stops, only the gate opens/closes. This is the mechanism that made an 8-way instant preset-switcher (built from 8 parallel Audiomatic Retro Transformer units) actually feel instant rather than crossfaded. [Source: reason101.net]

## Shelob (4×20 audio splitter RE) repurposed as a crossfader and a group-mute bank [Sourced]
- **Song-level crossfades**: a Combinator button flips Channel A off / Channel B on simultaneously, with a Combinator rotary mapped to Shelob's global 0–20 second **Fade** knob to set crossfade length — turns a plain splitter into a full fade-in/fade-out utility, suggested specifically for use on Master Outs or pre-dithering.
- **Grouped independent mute banks from one input**: feed a signal into Channel 1, enable **Stripe** (auto-broadcasts that signal to channels 2–4 with no extra cabling), then use each channel's own Pass-Through switch to toggle that channel's *entire output group* independently. The global Stripe switch can also kill/restore channels 2–4 all at once as a master group toggle. In the device developer's own words (quoted in the source): *"Put your input into Channel 1, and turn on Stripe... Now you can turn each Channel off/on either as a Channel group with its Pass Switch... and you can turn all Channels 2, 3 and 4 on and off simultaneously via the Stripe switch!"* [Source: reason101.net]

## Kong-as-keyboard's octave-shift CV fan-out [Sourced — cross-reference]
The full technique lives in `drums.md` (it's fundamentally a Kong/drum-controller idea), but the CV mechanism is worth knowing on its own: a Thor used purely as a 1-step "step transposer" converts a pad-hit into a transpose CV value, which is then fanned out to 13 separate NN-XT instruments' Oscillator Pitch CV inputs via three daisy-chained Spider CV Merger/Splitters. The general pattern — "one trigger becomes a transpose signal, fanned out via Spiders to many devices at once" — generalizes well beyond that specific 13-NN-XT build. [Source: reason101.net]

## Official CV/Gate documentation baseline [Sourced]
Reason's own operation manual frames CV/Gate routing plainly, as the foundation the tricks above all build on: connecting multiple outputs from instruments together, sidechaining, and using CV to modulate or control a parameter on one device *from* another device entirely. Worth reading if the above techniques feel unfamiliar — they're all extensions of this base capability, not exotic hacks requiring anything beyond stock Reason. [Source: Reason Studios operation manual]

## Sources
- reason101.net, "Creative Reason Projects" archive — http://www.reason101.net/category/creative-reason-projects/
- Reason Studios, "Routing Audio and CV" (Rack Plugin 12 Operation Manual) — https://docs.reasonstudios.com/rackplugin12/routing-audio-and-cv

=====================================================
SOURCE FILE: drums.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/drums.md
=====================================================

# Drums — Unique & Surprising Techniques

## Turning Kong into a played keyboard/piano-roll controller [Sourced — detailed]
The single most elaborate documented drum-adjacent technique found in this research. Origin: reason101.net, inspired by Native Instruments Maschine's "Pad Mode – Keyboard" feature, rebuilt from scratch in Reason using CV routing.

**What it does:** lets you play full chromatic melodic lines (not just fixed drum hits) from a 16-pad controller mapped to Kong, with two pads dedicated to octave-up/octave-down shifting.

**How it's built:**
1. Combinator containing: a 14:2 Mixer, a Kong (the trigger surface), two empty Thors (one labeled "Octave Up," one "Octave Down"), three CV Spider Merger/Splitters, and 13 NN-XT devices (one per semitone across a full octave, C to C).
2. Load the same melodic sample/patch (example used: a Wurlitzer piano) into all 13 NN-XTs. Set Pitch Semitone to 0 on the first, then increment by exactly 1 semitone on each subsequent NN-XT (1, 2, 3 … up to 12) — this gives you a full chromatic octave spread across 13 identical-sounding instruments instead of relying on a single sampler's own keyboard tracking.
3. Route Kong's Gate CV output from pad 1 into NN-XT #1's Gate CV input (and Osc Pitch CV input trim set to 127), then the same pattern for pads 2–13 into NN-XTs 2–13.
4. **Octave Up (pad 15)** and **Octave Down (pad 16)**: each drives a dedicated Thor used purely as a step-transposer (not as a synth voice) — Step Sequencer set to Run Mode "Step," 1 step only, that step's note set to C2 (Octave Up) or C4 (Octave Down). The Thor's own MBRS lines (`Seq.Note: 100 > S.Transp` and `Seq.Note: 100 > CV Out1`) convert a pad-hit into a CV transpose signal.
5. That transpose CV is fanned out to all 13 NN-XTs' Osc Pitch CV inputs via the three Spider CV Merger/Splitters, daisy-chained.
6. In the Combinator Programmer, "Receive Notes" is unchecked for every device except Kong — otherwise playing the Combinator's own sequencer track would trigger every NN-XT simultaneously instead of routing through Kong's pads.

**The one non-obvious "magic number":** the Spider trim knob on the octave-transpose CV path is set to **84** specifically — noted in the source as the value that makes the octave switching land correctly (not derived from first principles in the writeup, just stated as the working value).

**Why this belongs in your drums file rather than a synth file:** the whole point is repurposing Kong — a drum device — as the *playing surface* for melodic material, which is the surprising/creative part. The underlying "borrow CV to transpose a bank of samplers" idea generalizes to any Reason device with an Oscillator Pitch CV input (i.e., nearly all of them), per the original author's own closing note. [Source: reason101.net]

## Kong layering discipline (less exotic, still underused) [Sourced]
- Each Kong pad supports **two module slots**. A documented pattern for a thicker kick: a Synth Bass Drum in slot 1 for the sub/body, an NN-Nano loaded with a short transient/click sample in slot 2 — both trigger simultaneously on one pad hit, giving you sub weight and attack definition from a single hit without manually layering two separate tracks.
- **Mute groups**: assigning closed-hat and open-hat pads to the same mute group makes hitting the closed hat choke the open hat's ring, mimicking how a real hi-hat physically works. Commonly skipped by producers who program hats as two unrelated one-shots.
- **Hit type variation**: each pad can store up to 4 alternate hits that cycle or randomize per trigger — this is Kong's built-in answer to the "same snare sample every single hit sounds robotic" problem, without needing a separate randomization MIDI effect.
- **Bus FX vs per-pad FX vs Master section**: Kong has three distinct processing tiers (per-pad insert effects, two shared Bus FX sends for grouping e.g. all pads into one compressor, and a master section for the whole kit) — worth deliberately deciding which tier a given process belongs on rather than defaulting to per-pad inserts for everything. [Source: Audeobox, "Reason Kong Drum Designer"]

## Grain as a granular drum machine [Sourced — description level]
Reason Studios published a dedicated "Quick Tip" specifically repurposing **Grain** (built for melodic/textural granular synthesis) as a drum sampler instead — i.e., using granular playback modes on drum hits rather than melodic samples, for drum sounds with built-in micro-variation and texture that a standard one-shot sampler can't produce. The official Combinator patch demonstrating this was distributed alongside the tutorial video. [Source: Reason Studios]

## Sources
- reason101.net, "Kong Drum Creation A to Z" / NN-XT tag archive (Kong-as-keyboard writeup) — http://www.reason101.net/tag/nn-xt/
- Audeobox, "Reason Kong Drum Designer" — https://www.audeobox.com/learn/reason/kong-drum-designer/
- Reason Studios, "Build your own granular drum machine in Reason 11" — https://www.reasonstudios.com/news/post/build-your-own-granular-drum-machine-reason-11

=====================================================
SOURCE FILE: instruments-synths.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/instruments-synths.md
=====================================================

# Instruments & Synths — Unique & Surprising Techniques

Most of this file comes from a single, unusually dense source: an archive of "creative Reason projects" articles on reason101.net, specifically because it documents devices being used for jobs they weren't designed for. Where a routing is given as exact MBRS (Modulation Bus Routing Section — Thor's back-panel modulation matrix) lines, I've kept the exact syntax so it's directly typeable.

## Turning an LFO device into a full synth voice (Pulsar as oscillator) [Sourced]
Pulsar is a dual-LFO Rack Extension — not a synth. This technique uses its raw waveform output as if it were an oscillator:
- Both LFOs: unsynced, rate maxed, waveform = Sawtooth, Shuffle ~70%, Level rotaries at 0%, envelope Release 0 ms, Envelope Rate 100% / Level ~60%.
- **The unlock**: MIDI KBD Follow turned to 100% on both. Without this, the "oscillator" ignores keyboard pitch entirely and plays one fixed note regardless of what you play.
- LFO1 Audio Output → Combinator Left input, LFO2 Audio Output → Right, for stereo width from two independently-shuffled LFOs.
- **Advanced version**: pipe both LFO audio outputs into a Thor via MBRS (`Audio In1: 100 > Filt1 In` and `Audio In2: 100 > Filt1 In`), so Thor's filters/envelopes/effects process the LFO signal exactly as if it were a normal oscillator — you're using Thor purely as a processing chassis around someone else's raw waveform.
- **Variant**: route into Thor's **Filter 3** instead, bypassing Filter 1/2, Shaper, and the Amp Envelope entirely — gains Thor's 4-stage envelope explicitly through the MBRS routing, at the cost of losing Thor's own Amp section for level control (level then has to be controlled from the Pulsar LFO Level knobs directly).
- Documented result: "a raw aliased sound that some like and some don't, but nevertheless, it's a unique sound." [Source: reason101.net]

## Etch Red (filter RE) misused as six different effect types [Sourced]
Etch Red is a dual-filter device with a 10-source modulation matrix. None of the following are its advertised function:
- **Distortion**: unsynced LFO1 at 100–600 Hz as mod source, output level −14 dB, Drive Mod rotary turned up — using an LFO at audio rate to drive distortion instead of a slow sweep.
- **Tremolo**: LFO1 bipolar, small amount into the Level Mod rotary.
- **External wavetable modulation**: Malstrom's "Mod A" output patched into Etch Red's rear CV 1 input — repurposing Malstrom's 31 wavetables as an external LFO shape source for a completely different device.
- **Rhythmic gate effect from a filter, not a VCA**: Drive and Filter 2 off; both LFOs set to Square wave, synced but at different rates (e.g. 1/4 and 1/16), both modulating Filter 1 frequency at 100% — produces an on/off gating rhythm from the filter itself.
- **Auto-panner**: LFO1 bipolar into the Pan Mod rotary.
- **FM/ring-mod audio input**: external audio (a loop, a synth, a raw oscillator) fed directly into the Filter FM input jacks, FM rotary up — turns the filter's FM input into an audio-rate ring-modulator stage, with an LFO further modulating FM depth for movement.
- **Envelope triggering from a programmed rhythm, not a keyboard**: Etch Red's onboard envelope has no built-in trigger source, so a Matrix pattern's Gate CV or Curve CV output is routed into Etch Red's rear Gate CV input, letting a programmed step pattern drive the envelope instead of playing notes.
- **"Stolen" key tracking**: create a Sequencer track for Etch Red, copy MIDI note data from an *unrelated* track into it, then use Key Track so the filter frequency follows that borrowed melodic line rather than whatever's actually playing through the filter.
- **Wobble bass from the filter's own LFO** (not the oscillator): LFO1 CV → Etch Red rear Pitch CV input, Key Track engaged, Fatty LP filter, Freq ~185 Hz, Rez 70%, LFO1 rate ~34 Hz free-running, Mph ~77%. [Source: reason101.net]

## Thor MBRS tricks (the modulation matrix, used past its obvious purpose)
- **Button as manual step-advance** — turns a front-panel Button into a physical "next step" control for the built-in Step Sequencer: turn off the Sequencer's global Trigger light and the Global Envelope's Gate Trig; Global Envelope Sustain to full, everything else to zero. MBRS: `Button1: 100 > G.Env Gate` and `Global Env: -100 > S.Trig`, plus a second row `Button1: 100 > S.Trig : 100 > S.Trig`. Step Sequencer Run Mode = "Step." Result: both pressing *and releasing* the button each advance one step — because both the on- and off-transitions trigger S.Trig — letting one button manually cycle through all 16 steps (e.g. to browse 16 stored patch variations). Costs you the Global Envelope for anything else. [Source: reason101.net]
- **Chiptune tone via stepped-LFO FM**: modulate the Wavetable Oscillator's Frequency (FM) parameter with a *stepped* LFO shape (not a smooth wave) for authentic chiptune-style stepped pitch changes. Combine with the button-step trick above to pack 4 distinct chiptune voices into one Thor patch, browsed via the same button. [Source: reason101.net]
- **Inverting a modulation's direction with a button**: write the same modulation twice at opposite polarity, each gated by the same button — `Mod Envelope: 30 > Osc1 Pitch : -100 > Button1` and `Mod Envelope: -30 > Osc1 Pitch : 100 > Button1`. Button off → envelope bends pitch up 30; button on → same envelope bends pitch down 30. A general pattern for flipping the *direction* of an existing modulation rather than switching it on/off. [Source: reason101.net]
- **Blending two different modulation types on one Rotary, gated by a Button**: chain a source through two scaling stages in one MBRS row so a single Rotary continuously blends Vibrato and Tremolo — `LFO2: 25 > Osc1 Pitch : -100 > Rotary1` and `LFO2: 66 > Amp Gain : 100 > Rotary1` — using the less-common "double destination/double scaler" MBRS row slots to stack a continuous blend and a discrete on/off in one control. [Source: reason101.net]
- **Negative key tracking (inverted pitch response)**: `KeyNote: -100 > Osc1 Pitch` — a negative full-range key-tracking amount inverts normal keyboard response, so lower notes produce *higher* pitch and vice versa. Not reachable from the front-panel KBD knob (positive-only) — MBRS only. The source itself flags this as bizarre with no obvious musical purpose, but technically available. [Source: reason101.net]
- **"Note 2 (Octave Range)" key tracking for a modulation that repeats every octave**: using Thor's "Voice Key > Note 2 (Octave Range)" MBRS source instead of full-range Note tracking makes a key-scaled modulation reset and repeat every octave — e.g. an LFO rate sweeping slow→fast within one octave, then resetting — a way to make a patch that only sounds good over 1–2 octaves usable across the full keyboard by tiling the "good" curve rather than stretching it thin. [Source: reason101.net]
- **Pushing modulation past 100%**: stacking the *same* MBRS line on multiple separate rows sums their amounts — three identical 100% rows plus the knob's own 100% yields roughly 400% total, for destinations that need more range than one row's cap allows. [Source: reason101.net]
- **One Thor, two instrument personalities**: a single Button switches between two completely different characters within one patch (a synth/pad hybrid via one MBRS row modulating Attack+Release together, or a bass/bass-drum hybrid), with a specific MIDI key assigned as a momentary trigger for that button — lets a performer hold one key to morph the whole patch live while playing other notes normally. [Source: reason101.net]
- **Clean bypass via a zeroed Dry/Wet knob**: dial in an effect (e.g. Chorus) normally, then turn its Dry/Wet knob physically to 0, and drive Dry/Wet *entirely* from the MBRS (`Button1: [amount] > Chorus Dry/Wet`) — makes the button a true on/off bypass instead of a modulation layered on top of a nonzero baseline. [Source: reason101.net]

## Grain's less-obvious playback modes [Sourced]
Grain has four fundamentally different ways of interpreting a loaded sample, and two of them behave more like synthesis than sampling:
- **Grain Oscillator mode**: plays grains at the speed of each note's own pitch, effectively turning any sample into a raw analog-style oscillator waveform.
- **Spectral Grains mode**: analyzes each grain's frequency content and *resynthesizes* it using additive synthesis — producing a deliberately artificial-sounding version of the source sample, shapeable via Snap, Filter, and Formant controls. This is closer to a vocoder/resynthesis effect than to sampling at all.
- Grain's Motion envelope can control playback position itself — not just amplitude — letting you make a sample skip around in time or change where it starts/stops as a modulation destination, not just a static setting. [Source: Reason Studios]

## Mimic's "Fixed Pitch" vocal trick [Sourced]
From a hands-on reviewer's own workflow, not an official tutorial — flagged as a personal discovery: load an entire vocal *phrase* (not a single word) into Mimic, set **Start position to Global** (keeps sample playback continuous across retriggered notes instead of restarting each time), and select **Vocal mode with Fixed Pitch**. In Fixed Pitch mode the sample is forced, Auto-Tune-style, to whatever MIDI note you play — so you can replay the original phrase with a completely different melody, or play the original melody back for an unusual, modern take on the Auto-Tune sound. Reviewer's own words: *"I've got slightly obsessed with a trick where..."* — genuinely a producer finding a use the device wasn't explicitly built to demonstrate. [Source: Sound on Sound, Reason 12 review]

## Sources
- reason101.net, "Creative Reason Projects" archive — http://www.reason101.net/category/creative-reason-projects/
- Reason Studios, "Tutorial: Granular Synthesis Sound Design" — https://www.reasonstudios.com/news/post/tutorial-granular-synthesis-sound-design-2
- Sound on Sound, "Reason Studios Reason 12" (review) — https://www.soundonsound.com/reviews/reason-studios-reason-12

=====================================================
SOURCE FILE: mixing-mastering-creative.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/mixing-mastering-creative.md
=====================================================

# Mixing & Mastering — Unique & Surprising Techniques

## Sidechain Tool's three distinct modes — most producers only use one [Sourced]
Reason's dedicated Sidechain Tool device is built around three genuinely different behaviors, and it's easy to only ever touch the first one:
- **Auto Pump**: quick classic four-on-the-floor ducking, curve adjustable to fit your kick, rate adjustable for other rhythmic effects (including half-speed).
- **Band Mode**: ducks only a selected low or high frequency band rather than the full signal — useful when you want the pump feel without also thinning out unrelated frequency content.
- **Trigger mode**: the curve is triggered by *any* audio signal, MIDI note, or CV — not necessarily the actual kick drum you're ducking against. This is what makes the "ghost kick" and "unconventional trigger source" techniques below possible. [Source: Reason Studios, Sidechain Tool product page]

## The "ghost kick" trigger [Sourced — technique name only, video not transcribed]
A dedicated YouTube walkthrough on sidechaining in Reason includes a chapter specifically on creating a **silent, CV-only "ghost" kick drum** purely to drive sidechain ducking — i.e., a kick pattern that never makes sound itself, existing only to trigger the pump/duck effect on other elements. Useful when the audible kick pattern and the ducking rhythm you actually want don't match (e.g. a sparse audible kick but a denser ducking pulse for groove). The same video's chapter list also references **using Pulsar's own waveform to trigger sidechain compression** — i.e., an LFO device's output pattern (not a drum hit at all) driving the ducking rhythm, for a pump that isn't tied to any drum hit whatsoever. Both are named/scoped from the video's chapter markers, not independently verified by a full transcript — worth testing rather than assuming exact settings. [Source: YouTube, "How to Sidechain in Reason 10 Complete Guide"]

## Serial (not single-stage) compression as a general mixing principle [Sourced — detailed in pop-vocal.md]
The Yana Mahal vocal chain technique (full detail in `templates-by-genre/pop-vocal.md`) generalizes past vocals: two compressors each doing light work (2:1 ratio, ~2 dB reduction each) reads as more natural and more "glued" than one compressor doing the equivalent total reduction in a single stage. Worth trying on any bus that's sounding "squashed" under a single heavier compressor — split the same total gain reduction across two lighter stages instead of reaching for a gentler ratio on one.

## Width without smear: offset stereo delay instead of a stereo widener [Sourced]
Also from the vocal chain research, but a general mixing principle: rather than reaching for a dedicated stereo-widener plugin/device, sending a signal to **Ripley (Space Delay) on an Aux Send** and using its **Offset** knob to create a timing difference between left and right channels produces stereo spread described as beyond what "a standard delay can't touch" — while keeping the dry signal itself centered and upfront (because it's a send, not an insert). Applicable to any mono source that needs width without losing center focus — not just vocals.

## The DJ-style dual-range filter knob (cross-reference) [Sourced]
Full build in `combinator-workflow.md`: using Combinator 2's **Source Range** macro feature to make one rotary control low-pass frequency on one half of its travel and high-pass frequency on the other half (with a dead zone at center) — built from nothing but the stock Channel EQ. Filed here as a mixing/mastering-adjacent technique because it's genuinely useful as a creative transition tool (drops, breakdowns, DJ-style build-ups) beyond its original sound-design framing.

## Sources
- Reason Studios, "Sidechain Tool" product page — https://www.reasonstudios.com/devices/sidechain-tool
- YouTube, "How to Sidechain in Reason 10 Complete Guide" — https://www.youtube.com/watch?v=9_LlSd3xCW4
- Reason Studios, "How to Build a Vocal Chain in Reason 13" (serial compression, Ripley Offset) — https://www.reasonstudios.com/news/post/build-an-epic-vocal-chain-in-reason-13

=====================================================
SOURCE FILE: original-ideas.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/original-ideas.md
=====================================================

# Original Ideas — 🧪 My Own Proposals, Not Sourced, Not Tested

You asked me to be creative and propose my own templates/techniques, not just report what's documented. Everything in this file is my own idea, built by extrapolating from the patterns found during research — none of it is pulled from a source, and none of it has been verified in an actual Reason session. Treat these as hypotheses worth 20 minutes of testing, not established technique. If one doesn't work as described, that's expected — write down what actually happened and it becomes real documentation for your recipe book system.

## 🧪 Simplified octave-shift keyboard using Note 2 (Octave Range) key tracking
The Kong-as-keyboard technique (`drums.md`) builds full chromatic playability from 13 separate NN-XT instruments plus CV-driven octave transposition through Spider mergers — powerful, but heavy to build and CPU-expensive. My proposal: since Thor's **"Note 2 (Octave Range)" key tracking source** (documented in `instruments-synths.md`) causes a modulation to repeat identically every octave, you could potentially get a similar "one melodic voice, multi-octave, pad-triggered" result with a single Thor patch and Kong's own note-range mapping, instead of 13 duplicated NN-XTs. Untested reasoning: if Kong's pads are mapped across a wide enough note range and the instrument being triggered uses Note 2 key tracking for its own pitch-relevant modulation (not the base pitch itself, which would need normal full-range tracking), you might get usable octave-consistent behavior with far less rack real estate. Worth trying specifically because it would cut the original technique's complexity roughly in half.

## 🧪 Ghost-hat sidechain pump, independent of the audible drum pattern
Building on the documented "ghost kick" trigger (`mixing-mastering-creative.md`), which uses a silent kick purely to drive ducking: my proposal extends this to a **silent hi-hat pattern** feeding Sidechain Tool's Trigger mode on a pad or lead, at a much faster, denser rate than the kick — producing a subtle rhythmic filter-pump texture on a sustained element that has nothing to do with the actual kick/bass ducking relationship. Use case: a pad that needs to feel "alive" and rhythmically locked to the groove without literally pumping in time with the kick (which would compete with an 808 or bass that's already ducking against the kick). This is a straightforward extension of a documented technique into an unexplored trigger source, not a wild leap — reasonably likely to work as described.

## 🧪 Genre-blend Combinator using Source Range crossfading
The documented DJ-filter Source Range trick (`combinator-workflow.md`) uses one knob's travel range to switch which parameter it affects. My proposal: apply the same Source Range mechanic to **crossfade between two completely different patches** rather than two filter types — e.g., a Thor 808 patch and a Thor rock-synth-bass patch, both loaded in one Combinator, with a single Rotary's Source Range split so the left half of its travel controls the 808 patch's level/character and the right half controls the rock patch's. Since your project already spans a Hip-Hop and a planned Rock Recipe Book, this could be a genuinely useful "genre-morph" bass instrument for a track that wants to reference both — turn the knob to blend rather than manually swapping instruments mid-arrangement. Higher uncertainty than the other two ideas here — worth a real test session before trusting it in a mix.

## 🧪 Mastering A/B reference Combinator
Building two complete, differently-tuned MClass mastering chains (e.g. one tuned for a louder streaming-target master, one more conservative/dynamic) inside a single Combinator, with one macro button instantly flipping which chain is active on the master bus — using the same "run both chains in parallel, gate which one's audible" pattern documented in the 8-way Audiomatic switcher (`combinator-workflow.md`), just with 2 chains instead of 8 and MClass Maximizer/Compressor instead of Audiomatic Retro Transformers. Purpose: instant A/B reference switching between two mastering approaches without the CPU/complexity of the full 8-way switcher build, and without the click/level-jump of manually bypassing one chain and enabling another mid-listen.

## What I'd actually do with these four
Test the sidechain one first — it's the smallest change from documented technique and most likely to just work. The Note 2 octave-shift simplification is the most likely to reveal something genuinely useful about Kong-keyboard-style patches if it works, but also the most likely to fail in a way that teaches you why the original 13-NN-XT approach exists. The genre-blend and mastering A/B ideas are both worth a session each, but I'd log them as experiments in your recipe book format (accuracy rating, verified/unverified) rather than trust them until you've actually heard the result.

=====================================================
SOURCE FILE: sampling-vocal.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/techniques-by-type/sampling-vocal.md
=====================================================

# Sampling & Vocal — Unique & Surprising Techniques

## Mimic's Fixed Pitch vocal trick [Sourced — full detail also in instruments-synths.md]
Cross-referenced here because it's fundamentally a sampling/vocal technique even though it lives on a synth-style device: load a full vocal *phrase* into Mimic, set Start position to **Global** so playback position stays continuous across retriggered notes instead of restarting, select **Vocal mode with Fixed Pitch**. The sample is then forced, Auto-Tune-style, to whatever note you play — letting you replay an entire recorded phrase with a new melody, or play the original melody back through an unusual modern-Auto-Tune-style texture. A hands-on reviewer's own discovered use, not something the official tutorial demonstrates. [Source: Sound on Sound, Reason 12 review]

## NN-XT for arbitrary-location chopping, not just multisampling [Sourced]
Community consensus (Reddit r/reasoners, "What is the best sampler in reason?") specifically calls out NN-XT as useful for **sample chopping at arbitrary locations** — think glitchy vocal fragments in EDM, or grabbing an unconventional slice point rather than a clean transient-aligned chop. This is a different use case from NN-XT's usual job (mapping a clean multisample across the keyboard) and worth remembering when a sample needs deliberately "wrong" slice points for a glitch effect. [Source: Reddit r/reasoners]

## NN-XT split-key patches for CPU savings on stage/live rigs [Sourced — snippet level, source article itself blocked]
A MacProVideo tutorial (title/description only — full article blocked on two fetch attempts, per the "move on after two tries" approach) covers building custom NN-XT split-key patches specifically to reduce CPU load in a streamlined laptop performance setup — i.e., deliberately limiting which samples/patches are "live" across the keyboard at once rather than loading a full multisample, to keep a live rig lighter. Worth knowing the technique exists even without the full article; the concept (split by key range for real-time layer control, not just up-front CPU savings) recurs elsewhere in this research too — see the Combinator key-zone technique in `combinator-workflow.md`. [Source: MacProVideo, title/description]

## The "Wonderland" hybrid Combinator — a rhythm generator built from a synth + a Rex loop [Sourced — detailed]
A shared, downloadable Combinator from reason101.net, worth studying as a complete example of a hybrid instrument rather than a single isolated trick:
- **Structure**: an NN-XT synth layer (in the example, a Wurlitzer piano patch) layered against a Dr.Rex-played rhythm loop, both inside one Combinator, with 4 rotaries and 4 buttons mapped to blend and shape them together as one instrument rather than two separate tracks.
- **The genuinely clever routing detail**: Scream's Auto CV output is used to convert the Dr.Rex loop's *audio* into a CV signal, which is then routed into Thor's modulation bus to affect the NN-XT synth layer — i.e., **the rhythm loop's own amplitude is driving modulation on the melodic layer**, an envelope-follower-style trick built entirely from a distortion device's side output rather than a dedicated envelope follower.
- Explicit invitation from the author to treat this as a template: swap the NN-XT patch for any other synth sound, swap the Dr.Rex loop for a different rhythm, and the macro mapping (pitch bend on the synth layer only; mod wheel affecting several parameters at once; a "Crudge" sine-shaper rotary; a Rex-layer-only distortion button; a Rex-layer-only octave-shift button; a "Underwater" chorus button on the synth layer only) still applies as a reusable performance-instrument skeleton. [Source: reason101.net]

## Sources
- Sound on Sound, "Reason Studios Reason 12" (review — Mimic Fixed Pitch trick) — https://www.soundonsound.com/reviews/reason-studios-reason-12
- Reddit r/reasoners, "What is the best sampler in reason?" — https://www.reddit.com/r/reasoners/comments/8dm7mc/what_is_the_best_sampler_in_reason/
- MacProVideo, "Using the NN-XT for Split Key Patches in Reason to Save CPU" — https://macprovideo.com/article/propellerhead-reason/using-the-nnxt-for-split-key-patches-in-reason-to-save-cpu (fetch blocked after two attempts; title/description only)
- reason101.net, "Wonderland" Combinator / Creative Reason Projects archive — http://www.reason101.net/category/creative-reason-projects/

=====================================================
SOURCE FILE: edm-future-bass.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/edm-future-bass.md
=====================================================

# EDM / Future Bass / Electronic — Producer Templates

## Full genre breakdown: Future Bass in Reason 12 [Sourced]
An official Reason Studios tutorial (featuring producer/artist Protostar) walks through a complete future-bass production template — genre pioneered by Flume, Louis The Child, Marshmello, The Chainsmokers. Reproduced with device-level specificity:

**1. Groove/drums** — two documented starting points:
- Load up to **8 percussion loops into Dr. Octo Rex** (loop-player approach), or
- Program from scratch with **Redrum**, or
- For a more experimental drum sound specifically, **Kong Drum Designer** sculpting a hybrid of samples and synthesis to get sounds that don't exist in any sample pack.

**2. Chords — the genre's signature "supersaw" pulse:**
- Choose from hundreds of presets, or build a supersaw patch from scratch in **Europa**, **Thor**, or **Maelstrom**.
- For complex, layered chord sounds specifically, **blend multiple instruments/effects together inside a Combinator** rather than relying on one synth.
- Harmonic guidance given directly: future bass chords lean on suspensions, 7ths, 9ths, 11ths, and other extended/inverted voicings — not plain triads. If theory isn't second nature, Reason's **Chords and Scales Player** is called out specifically as a way to get sophisticated voicings without knowing the theory behind them.
- Once the chord bed exists, use the sequencer's automation to add pitch bends, filter envelope moves, volume swells, and LFO wobbles — this is what produces the genre's signature "pulse."

**3. The vocal hook — chopped/pitched vocal sample:**
- The trademark future-bass earworm is a pitch- and timing-edited vocal sample, chipmunk-like.
- Workflow: use **Pitch Edit** to quantize, stretch, and re-pitch the vocal sample to your song's key/timing, then load it into **NN-XT** and map snippets across the keyboard so the chopped vocal becomes a playable melodic instrument.

[Source: Reason Studios, official tutorial, "How to Make Future Bass Tracks in Reason 12"]

## Community template pattern (dance-genre specific, from the Reddit thread) [Sourced]
Same source cited in the hip-hop file, but the poster (umbringer) frames it explicitly as their dance-music template: one Kong per principal drum sound (kick/snare/clap/shaker/hi-hat/cymbal), each in its own Combinator with EQ/processing already dialed in and favorite timbres saved, plus a mastering Combinator sitting at the end of the chain by default. [Source: Reddit r/reason]

## Deep house / tech house workflow notes [Sourced — light detail]
A more recent (Reason 14-era, applicable to 12) walkthrough covers deep house specifically: warm Rhodes-style chords, a "dusty," low-slung beat, jazzy plucked bass, late-night atmosphere. A separate Facebook thread names specific stock-adjacent devices used in a real deep house production: **Antidote** (pad + bass arpeggio) and **Revival** (a second bass + pad layer) — note these are Rack Extension synths, not devices in the base Reason 12 install, so treat them as "if you own these REs" rather than stock-only guidance. [Sources: YouTube, Facebook Reason Users group]

## Sources
- Reason Studios, "How to Make Future Bass Tracks in Reason 12" — https://www.reasonstudios.com/news/post/how-make-future-bass-tracks-in-reason-12
- Reddit r/reason, "Song / Rack Starter Templates" — https://www.reddit.com/r/reason/comments/1cecm1m/song_rack_starter_templates/
- YouTube, "Deep House Production Workflow in Reason 14" — https://www.youtube.com/watch?v=E7y4Pzl7IyE
- Facebook, Reason Users group, "Reason stock devices in deep house production" — https://www.facebook.com/groups/361165013897141/posts/2866302826716668/

=====================================================
SOURCE FILE: hip-hop-trap.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/hip-hop-trap.md
=====================================================

# Hip-Hop / Trap — Producer Templates

## Full project templates

### The "battle-ready" starter rack [Sourced]
A pattern used by competitive/timed beat producers, but it's the same logic any hip-hop producer uses to avoid rebuilding a rack every session: pre-load your go-to instruments, save as a `.reason` template, and load it instead of starting from an empty Rack.

- **Kong Drum Designer** loaded with your own kit ("battle kit") — not a factory preset kit, a kit you've built once and reuse.
- **Thor** pre-configured as a bass/808 starting patch.
- **Europa** pre-loaded with a melody patch.
- Mixer channels for each with basic EQ/compression already inserted, so you're mixing as you go instead of bolting it on at the end.

Time-boxed workflow the same source lays out (useful as a sanity-check pace even outside a battle context): drums ~4 min, bass ~3 min, melody ~4 min, arrangement ~2 min, mix/export ~1 min, after a ~1 min template load. [Source: Audeobox]

### The 808 patch (Thor), specifically [Sourced]
- Sine wave oscillator.
- Long amp envelope decay (2–5 seconds).
- A **fast pitch envelope routed to oscillator pitch** — this is what gives the classic 808 pitch-down "slide" on the attack, not a manually-drawn pitch bend.
- Light **Scream 4** distortion for harmonic content/grit.
- Programmed as a melodic (keygroup-style) instrument playing different notes to follow the chord progression, not a single fixed pitch.
[Source: Audeobox — "Beat Making in Reason"]

### Community rack templates (Reddit r/reason, "Song / Rack Starter Templates" thread) [Sourced]
Several working producers described their actual daily templates in this thread — worth treating as a small sample of real-world setups rather than one "correct" answer:

- **two_chalfonts**: a base template with two RV7000 reverbs (hall + room) wired to the mixer's sends/returns, an NN-XT with 4 of its outputs wired to 4 separate mix channels, plus master group channels for drums, bass, and music.
- **umbringer** (dance-leaning, but directly applicable to hip-hop/trap drum programming): one Kong per principal drum sound — kick, snare, clap, shaker, hi-hat, cymbals — each wrapped in its own Combinator with EQ/processing dialed in and saved with favorite drum timbres, plus a mastering Combinator already sitting at the end of the chain. Explicit caution from the same poster: leaning on templates too hard can flatten your own expression — build new synths/patches regularly, don't just recall the same rack forever.
- **m8k**: default drum kit + drum players mapped to the two Umpfs (Reason's user-remappable controller buttons), plus audio-in channels pre-wired to match a specific hardware interface's patchbay.
- **will_sherman**: pushes back on using *other people's* templates specifically — argues a template only pays off when you understand why each piece is wired the way it is, and that in Reason (unlike Cubase/DP-era workflows) a lean master-bus-insert template plus liberal use of the Favorites/preset system may be enough.

Takeaway: there's no single "pro hip-hop template" file being traded around — the pattern is: wrap each drum voice in its own tuned Combinator, keep a reusable reverb send pair, and put a mastering chain at the end by default. [Source: Reddit r/reason]

### Harald Austad's real workflow (platinum producer — Karpe Diem, Madcon, Jaa9 & OnklP) [Sourced]
Not a file template, but a documented step order from a working hip-hop-adjacent producer who does "90% of all the work" in Reason:
1. Start with drums (kick, snare, hats) to set tempo/feel.
2. Browse sounds/loops until something sparks a groove.
3. Add a melody — Austad favors electric bass and piano sounds, reaches for 808s specifically on hip-hop beats.
4. Build layer by layer, listening after each addition.
5. Arrange into intro/verse/drop structure.
6. Process every sound individually (EQ, compression, reverb, saturation) — he treats this as part of *writing*, not a cleanup pass at the end.

His stated production identity comes from *how* he processes sounds (saturation/warmth, Thor as a go-to synth) more than which devices he picks. [Source: Reason Studios artist interview]

## Mix/master-stage notes specific to this genre
- ReGroove Mixer with **MPC-style groove templates** applied to the drum track is called out specifically as effective for hip-hop — it reintroduces human-feeling shuffle/timing/velocity variance to programmed drums. [Sourced — Audeobox]
- High-pass the melodic/chord elements around 150 Hz to keep the low end clear for kick + 808/bass. [Sourced — Audeobox]
- Trap-specific: intricate hi-hat rolls are typically programmed at 1/32 resolution in the sequencer; Reason handles this natively. [Sourced — Audeobox]

## Sources
- Audeobox, "Beat Making in Reason: Complete Workflow from Drums to Export" — https://www.audeobox.com/learn/reason/beat-making-in-reason/
- Reason Studios, "How To Make Beats In Reason: A Producer's Step-By-Step Guide" (Harald Austad) — https://www.reasonstudios.com/news/post/harald-austad
- Reddit r/reason, "Song / Rack Starter Templates" — https://www.reddit.com/r/reason/comments/1cecm1m/song_rack_starter_templates/

=== END OF PART ===
