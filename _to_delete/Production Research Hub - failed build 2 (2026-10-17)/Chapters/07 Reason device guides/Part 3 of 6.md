# Chapter 07: Reason device guides
## Part 3 of 6

_Plain-language guide for each Reason device (compressors, EQs, reverbs, delays, synths, drums...)._

**In this part:**
- kong.md — Kong Drum Designer
- launchkey-mk3.md — Launchkey MK3 49 (your MIDI controller)
- malstrom.md — Malström
- master-bus-compressor.md — Master Bus Compressor
- matrix.md — Matrix Pattern Sequencer
- mclass-compressor.md — MClass Compressor
- mclass-equalizer.md — MClass Equalizer
- mclass-maximizer.md — MClass Maximizer
- mclass-stereo-imager.md — MClass Stereo Imager
- mimic.md — Mimic

(Next: Part 4 of 6)


=====================================================
SOURCE FILE: kong.md
ORIGINAL LOCATION: HS:device_refs/kong.md
=====================================================

# Kong Drum Designer

A 16-pad drum instrument. Each pad is its own little drum machine: a drum
module that makes the sound, two effect slots on top of it, and a set of macro
knobs that shape whatever is in there.

## When you'd use it

When you want to build a kit pad by pad and shape each drum on its own —
rather than Redrum, which is faster for a pattern but shallower per sound.

## Key controls

- **Level**: how loud that pad is. The first thing to reach for when a drum sits wrong against the others.
- **Pitch Offset**: tunes the whole pad up or down. On a kick this is the difference between a thud and a boom.
- **Tone**: a built-in filter, same idea as Redrum's tone. Up is brighter, down is duller.
- **Decay Offset**: how long the sound rings. Short for tight and modern, long for a room-y tail.
- **Pan**: where it sits left to right. Leave kick and snare centred.
- **Bus FX Send**: how much of the pad goes to Kong's shared effect. One reverb or delay for the whole kit lives here.
- **DM Pitch / DM Decay / DM Level**: the drum module's OWN pitch, decay and level, underneath the macro knobs above. What they do depends on which module is loaded.
- **FX1 / FX2**: two effect slots per pad, each with an on/off and two controls whose job depends on which effect is loaded.

## What the app can and can't do here

All 16 pads are reachable, three controls each: **Level, Pitch Offset and
Decay Offset**. Those three mean the same thing no matter which drum module is
loaded, so real values and percentages both work on every pad.

**Say the pad NUMBER.** "Turn up pad 5", "tune drum 9 down". Reason never tells
a control surface what is loaded on a pad, so the app cannot know which pad
holds the snare — asking for "the snare" by name is a guess, and it refuses to
guess.

The Tone, Pan, Bus FX Send, drum-module and per-pad effect controls are not
mapped. There are 48 knob slots and 16 pads; reaching every pad cost the depth.
The module and effect knobs were the cheapest half to give up — they scale
whatever is loaded in the slot, which Reason never reports, so they could only
ever take percentages anyway.

## Where it shines / falls short

Shines: deep per-drum control, two effects per pad, a shared bus effect.
Falls short: every parameter names its pad number and there is no "the
selected pad" to talk to, so a control surface has to spend a slot per pad per
control — 16 pads x 6 macro knobs would need 96 slots and only 48 exist.

## Pairs well with

Redrum for quick patterns; the RV7000 on Kong's Bus FX for one room around the
whole kit.

## Reference

Reason 12.7 Operation Manual, chapter 27 "Kong Drum Designer" — the Drum
Control Panel section for the macro knobs, and "Physical Modelling Drums" for
the bass-drum module's own head, shell and beater parameters.

=====================================================
SOURCE FILE: launchkey-mk3.md
ORIGINAL LOCATION: HS:device_refs/launchkey-mk3.md
=====================================================

# Launchkey MK3 49 (your MIDI controller)

Your keyboard with 16 square rubber pads on top. The keys play whatever
instrument is selected in Reason. The pads are for finger-drumming.

## Play drums on the pads — every time, 3 steps

1. **Pick the drum track.** In Reason, click the Kong (or Redrum) track in
   the sequencer so it's highlighted. The little keyboard-with-an-arrow icon
   on that track means "the Launchkey talks to THIS device now."
2. **Put the pads in Drum mode.** On the Launchkey, hold **Shift** and press
   the **Pad Mode** button, then pick **Drum**. The pads light up.
3. **Hit the pads.** Each of the 16 pads is one of Kong's 16 drum squares.
   Bottom-left pad = Kong pad 1 (usually the kick). Hit harder = louder.

That's it. If it works once, it works every time — the only thing that
"breaks" it is step 1: some other track being selected. When drums stop
making sound, look at which track is highlighted first.

## If the pads make the WRONG sounds
- Pads playing melodies instead of drums → you're in **Session** or
  **Custom** pad mode. Redo step 2.
- Pads trigger drums but the wrong ones → the pad bank got shifted. Press
  the little **up/down arrow** buttons next to the pads until the kick is
  back at bottom-left.

## The knobs and faders
The 8 knobs above the keys twist whatever Reason maps them to on the
selected device (on Kong: pad level and tone controls). You don't have to
set anything up — Reason recognizes the Launchkey by itself when it's
plugged in before Reason starts.

## Bonus: talk to Reason Voice with your foot
A sustain pedal plugged into the Launchkey's **Sustain** jack is also the
push-to-talk pedal for this app — hold it, speak, let go.

=====================================================
SOURCE FILE: malstrom.md
ORIGINAL LOCATION: HS:device_refs/malstrom.md
=====================================================

# Malström

"Graintable" synth: two oscillators play chopped-up sampled sounds that it can
scan through, freeze, or speed up without changing pitch. Two filters (incl.
comb and ring-mod), a waveshaper, and flexible A/B routing. Made for moving,
swirling, metallic, broken textures — not for a clean analog bass.
Source: Reason 12.7 Operation Manual, ch. 35, pp. 883–908.

## When you'd use it
- Evolving pads and drones that keep moving on a held note.
- Metallic bells, comb-filtered plucks, ring-mod weirdness.
- Lo-fi 8-bit crunch (Shaper in Quant mode).
- As an **effect**: its back-panel audio inputs run any rack signal through its filters and Shaper.

## Key controls
Named exactly as Reason's Remote layer names them. Every A control has a B twin.

- **Oscillator A On/Off**: oscillator on.
- **Oscillator A Octave** / **Oscillator A Semi** / **Oscillator A Cent**: tuning. Octave −4…+4, Semi 0…+12, Cent ±50.
- **Oscillator A Index**: where in the graintable the note starts.
- **Oscillator A Motion**: how fast it moves through the graintable. Centre = normal, hard left = frozen (one static wave).
- **Oscillator A Shift**: formant / tone colour without changing pitch.
- **Oscillator A Attack** / **Oscillator A Decay** / **Oscillator A Sustain** / **Oscillator A Release**: per-oscillator volume envelope (comes BEFORE the filters).
- **Oscillator A Gain**: oscillator level.
- **Modulator A Curve** / **Modulator A Rate** / **Modulator A Sync** / **Modulator A One Shot**: LFO shape, speed, tempo lock; One Shot turns it into an envelope.
- **Modulator A To Pitch** / **Modulator A To Index** / **Modulator A To Shift**: what Mod A moves (centre = none, left = inverted).
- **Modulator B To Motion** / **Modulator B To Level** / **Modulator B To Filter** / **Modulator B To Modulator A**: what Mod B moves.
- **Modulator A Target** / **Modulator B Target**: A, B or both oscillators/filters.
- **Filter A On/Off** / **Filter A Mode**: LP 12, BP 12, Comb +, Comb − (bass cut), AM (ring mod).
- **Filter A Freq** / **Filter A Resonance**: cutoff and resonance (in AM mode: ring-mod pitch and wet/dry).
- **Filter A Env** / **Filter A Kbd Track**: let the filter envelope / keyboard move the cutoff.
- **Filter Env Attack** / **Filter Env Decay** / **Filter Env Sustain** / **Filter Env Release** / **Filter Env Amount** / **Filter Env Invert**: one envelope shared by both filters.
- **Shaper On/Off** / **Shaper Mode** / **Shaper Amount**: waveshaper before Filter A — Sine (round), Saturate (rich), Clip (digital), Quant (bit-crush), Noise.
- **Route Oscillator A To Shaper** / **Route Oscillator A To Filter B** / **Route Oscillator B To Filter B** / **Route Filter B To Shaper**: the routing buttons. Nothing lit = oscillator goes straight out.
- **Spread Amount**: stereo width between the A and B paths. Set to 0 if only one path is used.
- **Master Level**: output.
- **Polyphony** (1–16), **Portamento**, **Legato On/Off**: play style. Legato = mono only while you play overlapping notes.
- **Velocity To Level A** / **Velocity To Filter Env** / **Velocity To Shift** / **Velocity To Attack** / **Velocity To Modulator**: how hard you play changes these.
- **Mod Wheel To Index** / **Mod Wheel To Shift** / **Mod Wheel To Filter** / **Mod Wheel To Modulator**: what the mod wheel moves.
- **Pitch Bend Range**: up to 24 semitones.

## Where it shines / falls short
Shines: motion, texture, sounds nothing else in the rack makes. Falls short:
precise, predictable subtractive tones — Subtractor/Thor are easier for that.

## Pairs well with
The Echo (Motion + delay = huge movement), RV7000, Scream 4 (after the Shaper for more grit).

=====================================================
SOURCE FILE: master-bus-compressor.md
ORIGINAL LOCATION: HS:device_refs/master-bus-compressor.md
=====================================================

# Master Bus Compressor

The main mixer's bus compressor (SSL-style "glue") as a rack device, with
Input Gain and a dry/wet Mix added.
Source: Reason 12.7 Operation Manual, ch. 59, pp. 1247–1252.

## When you'd use it
- Glue on a drum bus or the whole beat: 2:1, 1–3 dB of reduction.
- Parallel drum smash with Mix around 30–50%.
- Kick-keyed pumping via the sidechain.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Input Gain**: ±18 dB into the compressor.
- **Threshold**: −30…0 dB. Lower = more compression.
- **Ratio**: 2:1, 4:1 or 10:1 only.
- **Attack**: 0.1, 0.3, 1, 3, 10 or 30 ms. 10–30 ms lets drum hits punch through.
- **Release**: 0.1, 0.3, 0.6, 1.2 s or Auto (adapts to the music).
- **Make-Up Gain**: −5…+15 dB to win back lost level.
- **Mix**: dry/wet for parallel compression.
- **Sidechain**: trigger from the rear sidechain input instead of the signal itself.
- **Enabled**: bypass/on/off.

## Back panel
Sidechain in L/R; CV out of gain reduction.

## Where it shines / falls short
Shines: musical glue with very few choices to get wrong. Falls short: fixed steps
only, no soft-knee control, not a limiter.

## Pairs well with
MClass Maximizer after it on the master; Channel EQ before it.

=====================================================
SOURCE FILE: matrix.md
ORIGINAL LOCATION: HS:device_refs/matrix.md
=====================================================

# Matrix Pattern Sequencer

Classic step sequencer. Up to 32 steps, 32 pattern memories (4 banks × 8).
Sends Note CV + Gate CV (plays one voice of an instrument) and a separate Curve
CV lane that can move any parameter with a CV input.
Source: Reason 12.7 Operation Manual, ch. 66, pp. 1359–1372.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Run**: start/stop (also starts with the transport).
- **Pattern Enable**: mute/unmute the pattern.
- **Bank A** / **Bank B** / **Bank C** / **Bank D**, **Pattern 1** … **Pattern 8**: pick the pattern (automatable for song arrangements).
- **Resolution**: step length (e.g. 1/16).
- **Pattern Shuffle**: swing on/off (amount from ReGroove global shuffle).

## Panel (not Remote)
- Keys/Curve switch: draw notes (upper) and gate velocities (lower), or the Curve lane.
- Steps (1–32), Tie per step, Octave switch.
- Back: Unipolar/Bipolar curve switch; Curve CV out to e.g. a filter's CV input = stepped filter pattern.

## Handy tricks from the manual
- Matrix Gate → ECF-42 Env Gate and Curve → Freq CV = pattern-controlled filter.
- Curve CV steps after a zero step also fire gates — use it to trigger samples.

## Where it shines / falls short
Shines: quick mono riffs and stepped modulation. Falls short: mono; the main sequencer is easier for real parts.

=====================================================
SOURCE FILE: mclass-compressor.md
ORIGINAL LOCATION: HS:device_refs/mclass-compressor.md
=====================================================

# MClass Compressor

Single-band compressor from the MClass mastering suite. Clean, program-friendly, with a sidechain input on the back. The default choice when the channel strip's compressor isn't enough or you need a second serial stage.

## When you'd use it
- Bus glue (2:1, slow attack, 1–2 dB), vocal stage-two compression, 808 leveling, sidechain ducking via the rear input.

## Key controls
- **Threshold**: where compression starts. Watch the gain-reduction meter, not the knob position.
- **Ratio**: 2:1 gentle glue → 4:1 workhorse → higher = effect territory.
- **Attack**: THE character control. Slow (30 ms+) lets transients punch through = punchy. Fast clamps them = dense, controlled.
- **Release**: fast = energetic but risks pumping; **Adapt** button auto-adjusts and is usually right for busses.
- **Soft-knee**: smoother onset — leave on for vocals/busses.
- **Output gain**: make up what you compressed away; match bypassed level for honest A/B.
- **Sidechain input (rear)**: feed a kick here to duck whatever this compresses — classic pump.

## Where it shines / falls short
Shines: transparent utility compression anywhere in the rack. Falls short: character — it adds no color ever (that's Scream's job in this rack), and there's no lookahead or true-peak awareness, so don't rely on it for limiting (Maximizer or a modern VST does that).

## Pairs well with
Scream 4 before it (saturate, then control), channel strip comp as stage one, kick channel → its sidechain for ducking.

=====================================================
SOURCE FILE: mclass-equalizer.md
ORIGINAL LOCATION: HS:device_refs/mclass-equalizer.md
=====================================================

# MClass Equalizer

Clean mastering-grade EQ: a 30 Hz rumble cut, low and high shelves, and two
fully parametric bands. No bands are on by default — switch each one on first.
Source: Reason 12.7 Operation Manual, ch. 61, pp. 1273–1280.

## When you'd use it
- Cleaning low rumble before a compressor or maximizer.
- Broad tone shaping on a bus or the master (shelves).
- Surgical cuts/boosts on one instrument (parametrics).
- Feeding a compressor's sidechain with a boosted "S" band = de-esser.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Low Cut Enable**: cuts everything under 30 Hz (12 dB/oct). Turn on before any compressor/limiter so sub rumble doesn't trigger it.
- **Low Shelf Enable** / **Low Shelf Frequency** / **Low Shelf Gain** / **Low Shelf Q**: boost/cut below 30–600 Hz, ±18 dB. High Q = steeper, with a small bump the other way.
- **Parametric 1 Enable** / **Parametric 1 Frequency** / **Parametric 1 Gain** / **Parametric 1 Q**: bell band, 39 Hz–20 kHz, ±18 dB. Higher Q = narrower.
- **Parametric 2 Enable** / **Parametric 2 Frequency** / **Parametric 2 Gain** / **Parametric 2 Q**: second bell, same ranges.
- **Hi Shelf Enable** / **Hi Shelf Frequency** / **Hi Shelf Gain** / **Hi Shelf Q**: boost/cut above 3–12 kHz, ±18 dB.
- **Enabled**: bypass/on/off.

## Where it shines / falls short
Shines: transparent, precise, visual curve display. Falls short: no color and
no low-pass/high-pass beyond the fixed 30 Hz cut — use Channel EQ's HPF/LPF for
steeper filtering.

## Pairs well with
MClass Compressor after it; Spider Audio + MClass Compressor sidechain for de-essing (manual's own recipe).

=====================================================
SOURCE FILE: mclass-maximizer.md
ORIGINAL LOCATION: HS:device_refs/mclass-maximizer.md
=====================================================

# MClass Maximizer

Loudness limiter for the end of the chain. 4 ms look-ahead for true brick-wall
limiting, plus a Soft Clip stage that adds warm saturation.
Source: Reason 12.7 Operation Manual, ch. 61, pp. 1273–1280.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Input Gain**: pushes the mix into the limiter (±12 dB). This is the "louder" knob.
- **Limiter Enable**: the limiter section on/off.
- **Look Ahead Enable**: 4 ms preview of peaks. On + Attack Fast + Output 0 dB = nothing gets over 0 dB.
- **Attack Speed**: Fast / Mid / Slow. Slower keeps more punch but lets peaks through.
- **Release Speed**: Fast / Slow / Auto. Auto adapts to the music — a safe default.
- **Output Gain**: leave at 0 dB normally.
- **Soft Clip Enable** / **Soft Clip Amount**: warm clipping at 0 dB. With Amount at zero it's harsh hard-clip, so give it some Amount.
- **Output Level Meter Mode**: Peak (fast) or VU (average loudness).
- **Enabled**: bypass/on/off.

## Where it shines / falls short
Shines: quick safe loudness on a beat or demo; Soft Clip adds pleasant grit on
drums. Falls short: no LUFS or true-peak metering, so check loudness elsewhere.

## Pairs well with
MClass Equalizer (Low Cut on) → MClass Compressor → MClass Stereo Imager → this. That is exactly Reason's factory "Mastering Combi" layout.

=====================================================
SOURCE FILE: mclass-stereo-imager.md
ORIGINAL LOCATION: HS:device_refs/mclass-stereo-imager.md
=====================================================

# MClass Stereo Imager

Splits a stereo signal into a low and a high band and sets the width of each.
Classic move: low band narrower (tight bass), high band wider (open top).
Source: Reason 12.7 Operation Manual, ch. 61, pp. 1273–1280.

**It cannot make stereo from mono.** Wire it stereo in / stereo out with a real stereo signal.

## Key controls
Named exactly as Reason's Remote layer names them.

- **X-Over Frequency**: split point between the bands, 100 Hz–6 kHz.
- **Low Width**: centre = unchanged, left = narrower (towards mono), right = wider. Usually narrow the lows.
- **High Width**: same, for the high band. Usually widen a bit.
- **Low Band Active** / **High Band Active**: the "Active" lights for each band.
- **Solo Mode**: hear Lo or Hi band alone to check them ("Normal" = both).
- **Separate Out Mode**: which band goes to the rear "Separate" outputs (Lo or Hi).
- **Enabled**: bypass/on/off.

## Trick from the manual
Solo = Lo and Separate out = Hi turns it into a crossover: lows from the main
out, highs from the Separate out — process each band differently.

## Where it shines / falls short
Shines: mono-ing the low end of a wide pad or loop, final width polish. Falls
short: on mono sources (does nothing), and heavy widening can collapse badly on
phone speakers.

## Pairs well with
Last in a mastering chain before the MClass Maximizer.

=====================================================
SOURCE FILE: mimic.md
ORIGINAL LOCATION: HS:device_refs/mimic.md
=====================================================

# Mimic

Fast "creative sampler" with eight slots. Each slot holds one sample and has
its own pitch, stretch, filter, envelopes, LFO and a lo-fi effect. Best for
chopping: drop a loop in, it slices it on the hits, each slice lands on a key.
Source: Reason 12.7 Operation Manual, ch. 32, pp. 787–816.

Samples are referenced, not saved in the patch.

## When you'd use it
- Chopping a loop or break into slices and replaying them (Slice mode).
- Eight one-shots on pads, drum-machine style (Multi Slot mode).
- Re-pitching a vocal or melody and keeping its speed (Vocal / Melody stretch).
- Tape-stop and lo-fi texture.

## Slot modes (Play Mode)
- **Pitch**: one slot played chromatically.
- **Slice**: one slot's slices across the keys from C1 (up to 92 slices).
- **Multi Slot**: keys C–G in every octave fire slots 1–8, unpitched.
- **Multi Pitch**: up to 8 slots layered/split across the keyboard, pitched.

## Key controls
Named exactly as Reason's Remote layer names them. The number is the slot
(1 shown; every one exists for slots 1–8).

- **Play Mode**: the four modes above (whole device).
- **Start Pos 1** / **End Pos 1**: play region.
- **Reverse 1**: play backwards.
- **Loop On 1** / **Loop Length 1** / **Loop Xfade 1**: loop at the end of the sample/slice.
- **Global Pos 1**: new notes continue from the playhead — keeps polyphonic chops in time.
- **Start Mod 1**: move the start earlier/later by modulation.
- **Snap Slices 1**: start points snap to slice markers.
- **Slice Sens 1**: auto-slicing sensitivity (more = more slices).
- **Play Thru 1**: on = a slice keeps playing past the next marker while held.
- **Stretch Mode 1**: Tape (speed = pitch), Advanced (full mixes), Melody (mono lines, clean loops), Vocal, Granular.
- **Stretch Speed 1** / **Speed Mod 1** / **Speed ModAmt 1**: playhead speed (0% = stopped/tape stop) and its modulation.
- **Transients On 1**: Preserve Transients (Advanced/Melody).
- **Voice Formant 1**: Vocal stretch — smaller/bigger "body" (child ↔ adult).
- **Voice Fixed 1**: Vocal stretch "Fixed Pitch" — auto-tunes the sample to the key you play.
- **Grain Len 1**: Granular stretch grain size.
- **Pitch Semi 1** / **Tune 1** / **Pitch Kbd 1** / **Pitch Mod 1**: pitch ±24 semitones, keyboard tracking, modulation.
- **Filter Type 1** / **Filter Freq 1** / **Filter Reso 1** / **Filter Drive 1** / **Filter Env 1**: 8 filter types incl. comb; drive and envelope depth.
- **Filter Attack 1** / **Filter Decay 1** / **Filter Sustain 1** / **Filter Release 1**: filter envelope.
- **Hi Cut 1** / **Lo Cut 1**: quick band limiting.
- **Amp Attack 1** / **Amp Decay 1** / **Amp Sustain 1** / **Amp Release 1** / **Amp Gain 1** / **Amp Velocity 1**: volume envelope.
- **Pan 1** / **Pan Mod 1**: pan and its modulation.
- **LFO Rate 1** / **LFO Wave 1** / **LFO Beat Sync 1** / **LFO Synced Rate 1** / **LFO Key Sync 1** / **LFO Delay 1**: per-slot LFO.
- **Effect Type 1** / **Effect Mix 1** / **Effect Mod 1**: per-slot lo-fi effect and amount.
- **Send1 1**: send to the Send 1 output (back panel).
- **Key Mode 1**, **Portamento Mode 1** / **Portamento Rate 1**, **Pitchbend Range 1**, **Master Volume**.

## Back panel
Separate out per slot, two send outputs — each chop can go to its own mixer channel.

## Where it shines / falls short
Shines: fastest way to chop and flip his own loops — directly useful for the
beat workflow. Falls short: huge multisampled instruments — NN-XT.

## Pairs well with
Channel Dynamics / Pulveriser on the output, The Echo in Roll mode for fills.

=== END OF PART ===
