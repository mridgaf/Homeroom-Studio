# Chapter 07: Reason device guides
## Part 1 of 6

_Plain-language guide for each Reason device (compressors, EQs, reverbs, delays, synths, drums...)._

**In this part:**
- alligator.md — Alligator
- audiobox-96.md — PreSonus AudioBox USB 96 (your audio interface)
- audiomatic.md — Audiomatic Retro Transformer
- bv512.md — BV512 Vocoder
- cf-101.md — CF-101 Chorus/Flanger
- channel-dynamics.md — Channel Dynamics (Compressor & Gate)
- channel-eq.md — Channel EQ
- combinator.md — Combinator
- comp-01.md — COMP-01 Compressor
- d-11.md — D-11 Foldback Distortion

(Next: Part 2 of 6)


=====================================================
SOURCE FILE: alligator.md
ORIGINAL LOCATION: HS:device_refs/alligator.md
=====================================================

# Alligator

A triple filtered gate. One sound goes in, and Alligator splits it into three
parallel copies — a low pass, a band pass and a high pass. Each copy has its
own gate that chops it on and off in a rhythm, its own filter, and its own
drive and volume. What comes out is a rhythmic pattern made out of a sound
that had no rhythm in it.

## When you'd use it

Point it at something sustained and boring — a held pad, a long chord, a
drone, a loop that's just sitting there — and it comes back as a pattern.
It is the fastest way in Reason to turn a flat sound into a groove without
playing anything.

## Key controls

- **Low Pass Filter On/Band Pass Filter On/High Pass Filter On**: switches that whole band on or off. Off means that copy of the sound disappears.
- **Low Pass Frequency/Band Pass Frequency/High Pass Frequency**: where that band's filter sits. On the low pass, down is darker and thicker; on the high pass, up is thinner and more brittle.
- **Low Pass Resonance/Band Pass Resonance/High Pass Resonance**: how much that band rings and whistles at its own frequency. High resonance is the squelchy, vocal sound.
- **Low Pass Env Amount/Band Pass Env Amount/High Pass Env Amount**: how far the filter envelope sweeps that band's frequency every time its gate opens. This is what makes each hit move instead of sitting still.
- **Low Pass LFO Amount/Band Pass LFO Amount/High Pass LFO Amount**: how much the LFO wobbles that band's filter. Slow and small is a drift; fast and large is a warble.
- **Low Pass Drive Amount/Band Pass Drive Amount/High Pass Drive Amount**: distortion on that band alone. Driving just the band pass is how you get grit in the middle without dirtying the bass.
- **Low Pass Pan/Band Pass Pan/High Pass Pan**: where that band sits left to right. Spreading the three bands apart is the stereo trick Alligator is known for.
- **Low Pass Volume/Band Pass Volume/High Pass Volume**: how loud that band is in the mix of the three.
- **Gate 1 Open/Gate 2 Open/Gate 3 Open**: holds that gate open by hand, ignoring the rhythm. Gate 1 is the low pass, 2 the band pass, 3 the high pass.
- **Gate 1 Trig/Gate 2 Trig/Gate 3 Trig**: fires that gate once, like hitting it.
- **Amp Env Attack**: how fast each gated hit comes in. Slow softens the chop into a swell.
- **Amp Env Decay**: how long each hit lasts before it falls away.
- **Amp Env Release**: how long the tail hangs on after the gate shuts.
- **Filter Env Attack**: how fast the filter sweep starts on each hit.
- **Filter Env Decay**: how fast the filter sweep falls back. Short decay with high Env Amount is the classic pluck.
- **Filter Env Release**: how long the filter takes to settle after the gate shuts.
- **LFO Freq**: how fast the wobble is.
- **LFO Waveform**: the shape of the wobble — smooth, stepped, ramping.
- **LFOSync**: locks the wobble to the song tempo instead of free running.
- **Pattern**: which built-in gate rhythm plays. This is the single biggest change to how it sounds.
- **Pattern Enable**: whether the built-in rhythm runs at all. Off, the gates only open when you play notes or hold one open by hand.
- **Resolution**: how fast the pattern steps go by. Faster is a stutter, slower is a groove.
- **Shift**: slides the whole pattern earlier or later against the beat. A small shift is the difference between stiff and human.
- **Shuffle**: swings the pattern.
- **Ducking**: how far the untreated signal drops out of the way when the gates fire.
- **Dry Volume**: how much of the original untreated sound comes through underneath.
- **Master Volume**: the whole device at once.
- **Enabled**: bypass — on or off for the whole thing.

## What the app can and can't do here

All three bands are reachable in full — filter on/off, frequency, resonance,
envelope amount, LFO amount, drive, pan and volume, on every band. So are both
envelopes, the LFO, all the pattern controls and the three gates. That is 48
controls, which is every slot the surface has.

**Say the band by name.** "Open up the low pass", "more resonance on the band
pass", "drive the high pass harder". The bands are named, not numbered, so
this reads naturally.

**Say the gate NUMBER.** "Open gate 2", not "open the gate" — there are three
and the app refuses to pick one for you.

**Alligator's built-in delay and phaser are not mapped.** That is the one cut:
the per-band delay and phaser sends, Delay Time, Feedback, Pan and Sync, and
Phaser Rate and Feedback — 13 controls, dropped because 61 will not fit in 48.
They still work; you reach them with the mouse. Nothing else about the device
is out of reach.

**Pattern Enable off makes four knobs do nothing.** Pattern, Resolution, Shift
and Shuffle only matter while the internal rhythm is running. The app will
still move them, and you will hear no difference — check that switch first if
a pattern change does nothing.

## Where it shines / falls short

Shines: turning anything sustained into a rhythm in seconds, three-way stereo
splits, and gated filter sweeps that would take three separate devices
otherwise.
Falls short: it is a rhythm generator, not a mix tool — nothing here is
transparent. And the pattern is chosen from a built-in list, so it is a menu,
not something you draw.

## Pairs well with

Anything that holds a note: Subtractor or Thor on a pad, or a Dr. Octo Rex
loop. The RV7000 after it puts one room around all three bands. Scream 4 in
front of it gives the gates something dirty to chop.

## Reference

Reason 12.7 Operation Manual, the Alligator chapter, for the three gates, the
pattern section and the per-band controls. Parameter spellings were taken from
Reason's own Remote vocabulary (`docs/reason/remote-vocab.json`), not from the
panel.

=====================================================
SOURCE FILE: audiobox-96.md
ORIGINAL LOCATION: HS:device_refs/audiobox-96.md
=====================================================

# PreSonus AudioBox USB 96 (your audio interface)

The blue metal box. It's the middleman between microphones/guitars and the
Mac: mics plug into the front, sound comes out the back to your speakers or
headphones. "96" just means it can record at up to 96 kHz quality.

## Make Reason use it — once per machine

1. Reason menu → **Settings/Preferences → Audio**.
2. Set **Audio Output** (and Input) to **AudioBox USB 96**.
3. If the sound crackles, raise the **Buffer Size** one notch and try again.
   Bigger buffer = safer sound but more delay when you play keys.

## The front knobs, in plain words
- The two knobs by the inputs are **gain** — how loud the mic or guitar
  comes IN. Turn up until the light flickers green while you play or sing;
  if it ever goes red, turn it back down — red means distortion is being
  recorded and no knob can fix it later.
- **Mixer** knob: blends "what's going in RIGHT now" (turn toward Inputs —
  no delay, good for singing) with "what the Mac plays back" (turn toward
  Playback).
- **48V button**: phantom power. ON for condenser mics (the sensitive
  studio kind). OFF for guitars and most stage mics.
- **Main** knob: speaker volume. **Phones** knob: headphone volume.

## Recording a take into Reason
Create an audio track, click its little input picker, choose AudioBox
input 1 (or 2), arm the track (red dot), check the meter moves when you
make noise, press record. If the meter doesn't move: wrong input picked or
gain knob all the way down — it's always one of those two.

=====================================================
SOURCE FILE: audiomatic.md
ORIGINAL LOCATION: HS:device_refs/audiomatic.md
=====================================================

# Audiomatic Retro Transformer

"Instagram filters for audio": 16 one-click character presets with one morph knob.
Source: Reason 12.7 Operation Manual, ch. 56, pp. 1229–1234.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Preset**: 16 looks, subtle (top row) to extreme (bottom row): Tape, Hi-Fi (loudness curve), Bright (adds top, cuts bass), Bottom (tighter lows), Spread (wider), Radio, VHS, Vinyl (crackle), MP3 (bad encode), Psyche, Cracked (blown speaker), Gadget (robotic), Circuit (circuit-bend + bitcrush), Wash, PVC (sci-fi), Eerie (waterphone).
- **Transform**: a morph, not just an amount — moves several hidden settings per preset.
- **Input Gain**: drive in (−∞ to +12 dB). Pushing it adds distortion; easy to overdo on a full mix (Tape especially).
- **Dry Wet**: blend. Towards Dry for subtle.
- **Volume**: output, to balance after raising Input Gain.
- **Enabled**: bypass/on/off.

Back panel: CV in for Transform (LFO + PVC = sweep) and Dry/Wet.

## Where it shines / falls short
Shines: instant vibe on a loop, drum bus or the whole beat (Tape, Vinyl, VHS).
Falls short: control — no way to fine-tune what each preset does. Note it adds
its own noise/crackle; check against the "clean open renders" rule before
using it on anything that gets rendered.

## Pairs well with
Parallel mixer channel + channel EQ/compressor to shape the effect.

=====================================================
SOURCE FILE: bv512.md
ORIGINAL LOCATION: HS:device_refs/bv512.md
=====================================================

# BV512 Vocoder

Classic vocoder: a "modulator" (voice, drums) shapes a "carrier" (a bright synth)
so the synth talks. 4/8/16/32 bands or a 512-band FFT mode. Also works as a
graphic EQ.
Source: Reason 12.7 Operation Manual, ch. 52, pp. 1165–1182.

## When you'd use it
- Talking/singing synth (voice into Modulator, sustained saw pad as Carrier).
- Drums "playing" a pad rhythmically (drums as Modulator).
- Freezing a vowel into a pad (Hold).
- Coloured or clean graphic EQ (Equalizer mode; FFT for clean).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Vocoder/Equalizer**: vocoder, or EQ mode (modulator ignored, bars = EQ).
- **Band Count**: 4, 8, 16, 32 bands or FFT (512). More = clearer speech; fewer = more musical/robotic. FFT: best for speech, ~20 ms delay, soft on transients.
- **Band Level 1** … **Band Level 32**: level per band (the lower display).
- **Attack**: how fast bands open — keep near 0; raise to smear into pads.
- **Decay**: how fast bands fall.
- **Shift**: moves the carrier filters up/down — big character change; CV-able for sweeps.
- **HF Emphasis**: boosts the carrier's highs — raise when it sounds muddy.
- **Hold**: freeze the current filter shape (resets when the sequencer stops).
- **Dry/Wet**: dry = modulator. Fully Wet for the pure vocoder sound.
- **Enabled**: bypass/on/off.

## Setup
1. Select the carrier synth, create the BV512 — it's auto-wired as the synth's insert.
2. Patch the voice (Hardware Interface input, or an audio track's Insert FX "To Device") into **Modulator Input** on the back.
3. Dry/Wet fully Wet, hold chords on the carrier.
Carrier tip: sustaining, bright, lots of harmonics (open saw).

## Where it shines / falls short
Shines: the classic robot voice and rhythmic pad chopping. Falls short: natural
harmonies — Neptune's Voice Synth sounds human, this sounds like a machine.

=====================================================
SOURCE FILE: cf-101.md
ORIGINAL LOCATION: HS:device_refs/cf-101.md
=====================================================

# CF-101 Chorus/Flanger

Short modulated delay: gentle chorus to jet-plane flanger.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Delay**: short = flanger, medium = chorus.
- **Feedback**: centre = gentle chorus; hard left or right = resonant, "tonal" flanging (two different flavours).
- **Rate**: LFO speed.
- **LFO Sync Enable**: lock the LFO to tempo; Rate then picks the note value.
- **Modulation Amount**: depth. At 0 it "freezes" (nice with Feedback up). At 0 it's also mono.
- **Send/Insert Mode**: Send = outputs only the wet signal. On an insert that gives a vibrato effect.
- **Enabled**: bypass/on/off.

Back panel: CV in for Delay (Matrix = stepped flanger; higher delay = lower pitch) and Rate.

## Where it shines / falls short
Shines: classic chorus/flange on keys, guitars, hats. Falls short: lush wide
ensemble — Quartet or UN-16 go further. Mono in + stereo out is needed for movement.

=====================================================
SOURCE FILE: channel-dynamics.md
ORIGINAL LOCATION: HS:device_refs/channel-dynamics.md
=====================================================

# Channel Dynamics (Compressor & Gate)

The mixer channel's compressor + gate as a rack device, with Input Gain and a
dry/wet Mix added (so it does parallel compression on its own).
Source: Reason 12.7 Operation Manual, ch. 57, pp. 1235–1240.

## When you'd use it
- Evening out a vocal, bass or loop; punchy drums (Peak mode).
- Parallel compression with Mix under 100%.
- Gating noise or bleed; rhythmic "chopped pad" by keying the gate from a drum loop.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Input Gain**: ±18 dB, works even with both sections off.
- **Mix**: dry/wet. Below 100% = parallel compression.
- **Comp On**: compressor on.
- **Comp Threshold**: −52…0 dB. Lower = more squash. Make-up gain is automatic.
- **Comp Ratio**: 1:1 to ∞:1.
- **Comp Release**: 100–1000 ms. Short = pumping, long = smooth.
- **Comp Peak On**: peak mode — better for sharp drum hits.
- **Comp Fast On**: faster attack.
- **Gate On**: gate/expander on.
- **Gate Exp On**: expander instead of hard gate — turns quiet parts down rather than muting.
- **Gate Threshold**: −52…0 dB. Under this, the gate closes.
- **Gate Range**: 0 to −40 dB, how far it turns down when closed.
- **Gate Hold**: 0–4000 ms held open before release starts.
- **Gate Release**: 100–1000 ms fade when closing.
- **Gate Fast On**: faster opening for steep percussive hits.
- **Sidechain**: use the rear sidechain input as the trigger.
- **Enabled**: bypass/on/off.

## Back panel
Sidechain in L/R; CV out for compressor gain reduction and gate state (gate CV is high while open).

## Where it shines / falls short
Shines: quick, clean, automatic make-up gain. Falls short: no attack knob (only
Fast on/off) — use MClass Compressor when attack time is the point.

## Pairs well with
Channel EQ, MClass Compressor as a second stage, a kick into Sidechain for pumping.

=====================================================
SOURCE FILE: channel-eq.md
ORIGINAL LOCATION: HS:device_refs/channel-eq.md
=====================================================

# Channel EQ

The mixer channel's EQ as a rack device: high-pass and low-pass filters plus a
4-band EQ (two shelves that can become bells, two sweepable mids).
Source: Reason 12.7 Operation Manual, ch. 58, pp. 1241–1246.

## When you'd use it
- Inside a Combinator, or anywhere you want the channel-strip EQ as a separate, saveable device.
- Steep low cut on everything that isn't kick/bass (HPF 18 dB/oct).
- Darkening a sample or loop (LPF).

## Key controls
Named exactly as Reason's Remote layer names them.

- **HPF On** / **HPF Frequency**: removes lows, 20 Hz–4 kHz, 18 dB/oct.
- **LPF On** / **LPF Frequency**: removes highs, 100 Hz–20 kHz, 12 dB/oct.
- **LF Gain** / **LF Frequency**: low shelf, ±20 dB, 40–600 Hz.
- **LF Bell On**: turns the low shelf into a bell (fixed width).
- **LMF Gain** / **LMF Frequency** / **LMF Q**: low-mid bell, ±20 dB, 200 Hz–2 kHz, Q 0.7–2.5.
- **HMF Gain** / **HMF Frequency** / **HMF Q**: high-mid bell, ±20 dB, 600 Hz–7 kHz, Q 0.7–2.5.
- **HF Gain** / **HF Frequency**: high shelf, ±20 dB, 1.5–22 kHz.
- **HF Bell On**: turns the high shelf into a bell.
- **E Mode On**: normal mode = bigger boosts get narrower (musical). E Mode = width stays fixed (surgical).
- **Gain**: output level ±18 dB, to match level after big moves.
- **Enabled**: bypass/on/off.

## Back panel
CV inputs (with trims): HPF Freq, LPF Freq, LMF Gain/Freq, HMF Gain/Freq — e.g. an LFO on LPF for a filter sweep.

## Where it shines / falls short
Shines: fast, familiar channel-strip tone shaping with real filters. Falls short:
only two fully parametric bands; for mastering precision use MClass Equalizer.

## Pairs well with
Channel Dynamics (the other half of the channel strip), Scream 4 (EQ before to choose what distorts).

=====================================================
SOURCE FILE: combinator.md
ORIGINAL LOCATION: HS:device_refs/combinator.md
=====================================================

# Combinator

A container that saves a whole chain — instruments, effects, mixers, and the
cables between them — as one patch (a "Combi", `.cmb`). Its front-panel knobs
and buttons are "virtual": each one can be wired to any number of parameters on
the devices inside.
Source: Reason 12.7 Operation Manual, ch. 63, pp. 1305–1332.

## When you'd use it
- Saving a finished recipe chain (e.g. bass + Scream 4 + EQ) as one patch you can reload.
- Layers and splits: several instruments played together, by key or velocity zone.
- Multi-effects: an effect chain saved as an Effect Combi, droppable into a mixer insert.
- One-knob macros: one Rotary moves several parameters at once, in different directions.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Rotary 1** … **Rotary 16**: the virtual knobs. Do nothing until mapped in the Editor's Modulation Routing. Their moves record as automation.
- **Button 1** / **Button 2** / **Button 3** / **Button 4**: virtual switches, same idea.
- **Mod Wheel** / **Pitch Bend**: passed to every instrument inside; each device decides what its wheel does.
- **Run Pattern Devices**: starts/stops Matrix/Redrum-style pattern devices inside. Pressing Play does this automatically.
- **Bypass All FX**: bypasses every insert effect inside, turns off send effects.
- **Select Next Patch** / **Select Previous Patch**: browse Combis.
- **Enabled**: bypass/on/off.

## How mapping works (Editor → Modulation Routing)
- Pick a device on the left, then per row: **Source** (a panel control) → **Target** (any parameter of that device) → **Min/Max**.
- Min above Max = reversed: turning the knob up turns the target down.
- **Source Range**: make a knob act only over part of its travel (e.g. 50–100%).
- Same knob can hit several devices — select another device and map it again.
- Quick way: right-click any parameter on an inner device → assign to a Combinator control.

## Rules worth knowing
- **Keep cables inside.** Anything wired straight to a device outside the Combi is "External Routing" and is NOT saved with the patch. Go through the To/From Devices jacks.
- 8 stereo "From Devices" inputs on the built-in mixer; out of room → add a Line Mixer 6:2.
- Devices you add inside a Combi get no sequencer track (hold Option when creating to get one).
- Combine existing devices: select them (Shift-click) → Edit > Combine. Edit > Uncombine undoes it.
- Panel can be 1U–6U, up to 32 knobs/faders + 32 buttons; custom backdrop images (3770 px wide).

## For the voice bridge
The bridge can only turn knobs Reason exposes for a device. A Combinator's
Rotary 1–16 can be pointed at ANY parameter inside it, so wrapping a device in a
Combi is the way to automate controls the bridge has no direct map for.
(Today the bridge maps only patch next/prev on the Combinator — not its knobs.)

## Where it shines / falls short
Shines: turning a recipe into a one-click, tweakable instrument. Falls short:
nothing inside is scriptable from outside except through those virtual controls.

## Pairs well with
Everything. Spider Audio for parallel chains inside, Line Mixer 6:2 for more inputs.

=====================================================
SOURCE FILE: comp-01.md
ORIGINAL LOCATION: HS:device_refs/comp-01.md
=====================================================

# COMP-01 Compressor

Basic compressor with automatic make-up gain. No sidechain, no CV.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Ratio**: 1:1 to 16:1.
- **Threshold**: lower = more compression.
- **Attack**: slower lets the front of each hit through.
- **Release**: short = pumping, long = smooth.
- **Gain**: the meter (net reduction + automatic make-up).
- **Enabled**: bypass/on/off.

## Where it shines / falls short
Shines: quick levelling with almost no CPU. Falls short: no sidechain, no knee, no
manual make-up — MClass Compressor or Channel Dynamics for real work.

=====================================================
SOURCE FILE: d-11.md
ORIGINAL LOCATION: HS:device_refs/d-11.md
=====================================================

# D-11 Foldback Distortion

Two-knob distortion, from a hint of edge to total wreck.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Amount**: how much distortion.
- **Foldback**: character. Centre = normal flat clipping; lower = rounder, gentler; higher = sharper, nastier.
- **Enabled**: bypass/on/off.

Back panel: CV in for Amount.

## Where it shines / falls short
Shines: fast grit with almost no CPU. Falls short: tone control — Scream 4 has far more flavours and a post-EQ.

=== END OF PART ===
