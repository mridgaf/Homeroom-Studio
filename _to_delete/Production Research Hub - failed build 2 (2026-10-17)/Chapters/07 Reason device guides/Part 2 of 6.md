# Chapter 07: Reason device guides
## Part 2 of 6

_Plain-language guide for each Reason device (compressors, EQs, reverbs, delays, synths, drums...)._

**In this part:**
- ddl-1.md — DDL-1 Digital Delay Line
- dr-octo-rex.md — Dr. Octo Rex Loop Player
- ecf-42.md — ECF-42 Envelope Controlled Filter
- europa.md — Europa
- grain.md — Grain
- guitar-amps.md — Your guitar amps (Crate, Epiphone Electar, and the red one)
- humana.md — Humana Vocal Ensemble
- id8.md — ID8 Instrument Device
- klang.md — Klang Tuned Percussion

(Next: Part 3 of 6)


=====================================================
SOURCE FILE: ddl-1.md
ORIGINAL LOCATION: HS:device_refs/ddl-1.md
=====================================================

# DDL-1 Digital Delay Line

Plain mono delay (output pannable) with tempo steps. Clean, no colour.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Unit**: Steps (tempo-locked) or MS (free time, max 2000 ms).
- **DelayTime (steps)**: 1–16 steps. Tip: set it in Steps, then flip to MS to nudge it off-grid.
- **DelayTime (ms)**: delay in milliseconds when Unit = MS.
- **Step Length**: each step is a 1/16 or a 1/8 triplet.
- **Feedback**: number of repeats.
- **Pan**: where the echo sits left/right.
- **Dry/Wet Balance**: full Wet as a send.
- **Enabled**: bypass/on/off.

Back panel: CV in for Pan (LFO = moving echo) and Feedback (dub throws on certain hits).

## Where it shines / falls short
Shines: tight rhythmic slap/echo that stays out of the way. Falls short: no
filtering or stereo ping-pong — The Echo does that.

=====================================================
SOURCE FILE: dr-octo-rex.md
ORIGINAL LOCATION: HS:device_refs/dr-octo-rex.md
=====================================================

# Dr. Octo Rex Loop Player

A loop player that holds **eight** REX loops at once, one per slot, and plays
one at a time. A REX loop is a loop that has already been cut into slices at
every hit, so it follows your song tempo without changing pitch — and the
slices can be treated as separate sounds.

Reason calls this device `Dr.REX Loop Player` when it talks to a control
surface. Same device, older name.

## When you'd use it

When the loop IS the song — boom-bap flips, breakbeats, anything built on a
sampled bar. Load eight variations (main, fill, drop, half-time) in the eight
slots and switch between them instead of programming a drum part.

It is also the one device here that reads your sealed ReFills natively, so the
whole factory loop library is available without anything being indexed first.

## Key controls

- **Select Loop**: the eight slots. "Go to loop 3" switches which loop plays. Say the slot NUMBER.
- **Selected Loop Slot**: the same choice as one dial instead of eight buttons.
- **Trigger Next Setting**: WHEN a slot switch lands — next bar, next beat, or next 1/16. Bar is musical, 1/16 is snappy.
- **Run**: starts and stops the loop without the transport.
- **Enable Loop Playback**: turn this OFF and the device stops looping and becomes a slice sampler — the keyboard plays one slice per key from C1 up. The single biggest thing this device does that is not obvious.
- **Follow Loop Playback**: keeps the slice display tracking what is playing.
- **Notes to Slot**: which of the eight slots your keyboard is playing.
- **Selected Loop in Editor**: which slot the loop knobs below are pointed at.
- **Transpose**: pitches every loop in the device. On drums this is a varispeed effect, not a key change.
- **Loop Transpose**: pitches only the loop in the selected slot.
- **Loop Level**: the volume of the loop in the selected slot.
- **Osc Env Amount**: sends the FILTER envelope to slice PITCH. This is the vinyl-scratch and warped-pop knob — nothing else in Reason does it. Small amounts warble, large amounts scratch.
- **Osc Octave / Osc Fine Tune**: coarse and fine tuning over the whole device.
- **Amp Env**: an attack/decay/sustain/release shape applied to EVERY slice. Decay down with sustain at zero gives a hard gated stutter; attack up past a fifth of the way gives a slow, backwards-sounding swell.
- **Amp Vel Amount**: how much harder playing makes slices louder.
- **Filter Env**: the same envelope idea on the filter, re-triggered on every slice. With the filter frequency low, resonance high and this amount high, you get a 303-style swoop on each hit.
- **Filter**: frequency, resonance, mode (notch, high pass, band pass, low pass 12, low pass 24) and an on/off. Note that the envelope is usually driving the frequency, so moving Freq alone may do less than expected.
- **LFO Sync**: locks the LFO's rate to the song tempo instead of free-running.
- **LFO1**: rate, amount, waveform and destination — a slow wobble over the whole loop. What Amount means depends on where Dest is pointed.

## What the app can and can't do here

**Say the slot NUMBER.** "Go to loop 3", "switch to loop 7". Reason never tells
a control surface which loop is loaded in which slot, so "play the drum loop"
has no answer and the app refuses to guess.

**Loop Transpose and Loop Level move whichever slot is selected in the editor**,
not the one playing. If they seem to do nothing, that is why — check
Selected Loop in Editor first.

**Nothing slice-level is reachable.** Slice pitch, pan, level, decay, reverse,
alt group and slice output are not parameters Reason exposes to a control
surface at all. So the famous Octo Rex tricks that live down there — alt-group
randomising, sending just the snare slices to a reverb through the eight back
outputs, drawing modulation in Slice Edit Mode — can only be done with the
mouse. The app will not pretend otherwise. Same limit as Kong's drum-module
knobs.

**The settings can be said by name now, not just as percentages.** Rex reports
every picker to the app as a bare number — "3" where the panel says LP 12 — so
until 2026-09-12 a phrase like "stop the loop" was heard, understood, and then
did nothing at all. The panel's own words are now filled in from the manual:

| Control | Say one of |
|---|---|
| Filter Mode | Notch, HP 12, BP 12, LP 12, LP 24 |
| LFO1 Wave | Triangle, Inverted Sawtooth, Sawtooth, Square, Random, Soft Random |
| LFO1 Dest | Osc, Filter, Pan |
| Trig Next | Bar, Beat, 1/16 |
| Run, Enable Loop Playback, Follow Loop Playback, Filter, LFO Sync | Off, On |

**Transpose takes real semitones.** "Pitch the loop down two semitones" lands on
−2, not near it. Same for Loop Transpose, and Osc Fine Tune takes cents.

**Osc Octave still takes percentages only.** It reads 0 to 8 and nothing outside
Reason knows which of those is neutral — calling 4 "4 octaves" when it means no
change would be worse than leaving it a bare number.

**The eight Select Loop buttons take percentages only.** They report "1" at
every position no matter what is written to them, so there is nothing to look a
number up in. "Go to loop 3" still works — it moves the knob, it just can't
read back where it landed.

**Master Level is not mapped.** It is spelled the same on Scream 4, which
would leave the app unable to tell the two apart. Loop Level does the job and
is per-slot anyway.

## Where it shines / falls short

Shines: instant tempo-following loops, eight variations under one hand, and a
full synth filter and envelope section wrapped around a sample.
Falls short: everything interesting about individual slices is mouse-only, and
it only plays one slot at a time — for two loops at once you need two devices.

## Pairs well with

Scream 4 and the MClass EQ for the lo-fi flip; Kong for one-shots under the
loop. Kong's pads can also be cabled to a Rex device's volume to turn loops
into an Ableton-style clip launcher — that is a cable job, not a voice one.

## Reference

Reason 12.7 Operation Manual, chapter 29 "Dr. Octo Rex Loop Player"
(pp. 695-718) for the parameters — the filter modes, LFO waveforms, LFO
destinations and Trig Next settings above are that chapter's own lists, in its
order. The slice-sampler mode, the Osc Env pitch trick and the envelope
gating are covered in Sound On Sound, "Introducing Dr OctoRex" (January 2011)
and ModeAudio, "The Art Of Loop Mangling" (January 2015) — the manual lists
those controls but never says what they are for.

=====================================================
SOURCE FILE: ecf-42.md
ORIGINAL LOCATION: HS:device_refs/ecf-42.md
=====================================================

# ECF-42 Envelope Controlled Filter

Resonant filter with its own envelope. The envelope does NOT follow the audio —
it fires only from a gate (Matrix, Redrum gate outs) or MIDI notes on its own
sequencer track. With audio only, it's a static filter.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Mode**: 24 dB lowpass, 12 dB lowpass, 12 dB bandpass.
- **Frequency**: cutoff; also where the envelope sweep starts and ends.
- **Resonance**: emphasis at the cutoff — more "synthy".
- **Env Amount**: how far the envelope opens the filter. If Frequency is already high this does little — lower Frequency.
- **Velocity**: how much the gate/note velocity scales Env Amount.
- **Attack** / **Decay** / **Sustain** / **Release**: the filter envelope.
- **Trigger**: fires the envelope, same as a gate arriving (remote-controllable).
- **Enabled**: bypass/on/off.

Back panel: CV in for Freq, Decay, Res; Env Gate in.

## Tricks from the manual
- Right-click > "Create Track for …", draw notes: note length + velocity (not pitch) shape the filter.
- Matrix Gate → Env Gate and Matrix Curve → Freq CV = pattern-controlled filter.
- Redrum gate outs → Spider CV → Env Gate = filter pumping in time with the drums.

## Where it shines / falls short
Shines: rhythmic filter chops on pads and loops. Falls short: needs a gate or
track to be more than a static filter.

=====================================================
SOURCE FILE: europa.md
ORIGINAL LOCATION: HS:device_refs/europa.md
=====================================================

# Europa

Reason's widest-sounding synth. Three identical sound engines, each with an
oscillator (analog shapes, wavetables, FM, e-piano, vocal, plucked string,
noise, or your own sample), two waveform Modifiers, a Spectral Filter, a
Harmonics processor and Unison. Then one shared filter, amp, six reorderable
effects, and a Mod Bus.
Source: Reason 12.7 Operation Manual, ch. 30, pp. 719–754.

## When you'd use it
- Big modern pads, supersaws, wide plucks and leads (Unison + Harmonics).
- Evolving textures from your own sample as a wavetable ("User Wave").
- Vocal/formant tones (Vocal waveform + Vocal Formant spectral filter).
- Metallic/bell tones (Karplus-Strong waveform + Harmonics Stretch).

## Key controls
Named exactly as Reason's Remote layer names them. Osc1 shown; Osc2 and Osc3 are the same.

- **Osc1 On** / **Osc1 Level**: engine on and its level.
- **Osc1 Wave**: the waveform family.
- **Osc1 Shape** / **Osc1 Shape Amt** / **Osc1 Shape Vel**: morphs the wave (saw→square, table position, FM depth, pluck damping…); its modulation amount and velocity.
- **Osc1 Semi** / **Osc1 Detune**: tuning.
- **Osc1 Mod1 On** / **Osc1 Mod1** / **Osc1 Mod1 Amt** / **Osc1 Mod2 On** / **Osc1 Mod2 Amt**: the two Modifiers — sync, bit/rate crush, wrap/fold/clip, octave/fifth/harmonic blends, ring mod, FM, "Detune 2/6/Multi", formant.
- **Osc1 Filter On** / **Osc1 Filter** / **Osc1 Filter Freq** / **Osc1 Filter Reso** / **Osc1 Filter Mod**: the per-engine Spectral Filter — LP/HP/BP, notch, comb, vocal formant, resonators, or a filter made from your sample.
- **Osc1 Harm On** / **Osc1 Harm Pos** / **Osc1 Harm Amt**: Harmonics — Ensemble (dense pads), Stretch (inharmonic/metal), odd/even, air noise.
- **Osc1 Unison On** / **Osc1 Unison Mode** / **Osc1 Spread** / **Osc1 Blend**: unison voices, detune/width, mix.
- **Osc1 To Filter**: send this engine through the shared filter.
- **Filter Type** / **Filter Freq** / **Filter Reso** / **Filter Drive** / **Filter Kbd** / **Filter Mod**: the shared filter after the engines.
- **Amp Attack** / **Amp Decay** / **Amp Sustain** / **Amp Release** / **Amp Gain** / **Amp Velocity**: volume envelope for all engines.
- **Pan**: output pan.
- **LFO 1 Rate** / **Env 1 Rate**: first LFO speed, first envelope speed.
- **Dist On** / **Dist Amount**: distortion (Dist, Scream, Tube, Sine, S/H crush, Ring).
- **Delay On** / **Delay Time** / **Delay Sync** / **Delay Synced Time** / **Delay FB** / **Delay PingPong** / **Delay Pan** / **Delay Amount**: send-style delay. Turn Amount down on a held note and the echoes keep going.
- **Reverb On** / **Reverb Size** / **Reverb Damp** / **Reverb Amount**: send-style reverb.
- **Comp On** / **Comp Ratio**: compressor.
- **Phaser On** / **Mod Effect Amount**: phaser/flanger/chorus and its depth.
- **EQ On** / **EQ Freq** / **EQ Gain** / **EQ Q**: one parametric band.
- **Key Mode**: Poly (up to 16 voices), Mono Retrig, Mono Legato.
- **Portamento** / **Portamento Mode**: glide.
- **Master Volume**, **Mod Wheel**, **Pitch Bend** (range ±24 semitones).

## Tricks from the manual
- **Vocoder-ish**: load speech as User Wave, Spectral Filter = User Wave filter, Freq 50%, Reso 0%, Kbd 0%, an envelope ramp sweeping Reso 100%.
- **Metal**: Karplus-Strong waveform + Harmonics "Stretch".
- **White noise**: Noise S&H waveform, Shape max, Oct −1, Kbd 0.

## Where it shines / falls short
Shines: wide, modern, evolving sounds fast. Falls short: CPU on big unison
patches; classic warm analog bass is simpler in Thor (Ladder) or Subtractor.

## Pairs well with
MClass Stereo Imager (narrow the lows of wide patches), Combinator, RV7000.

=====================================================
SOURCE FILE: grain.md
ORIGINAL LOCATION: HS:device_refs/grain.md
=====================================================

# Grain

Granular sampler: it plays your sample as tiny overlapping snippets ("grains"),
so you can stretch, freeze, scrub and re-pitch it independently — or play it
straight like a normal sampler. Plus an oscillator, filter, envelopes, LFOs,
Mod Bus and a multi-effect.
Source: Reason 12.7 Operation Manual, ch. 31, pp. 755–786.

Samples are referenced, not saved in the patch — keep the file (or save the song self-contained).

## When you'd use it
- Turning one of YOUR samples (a vocal, a chord, a loop) into a pad or texture.
- Freezing a moment of a sample and playing it as an instrument.
- Tape-stop and scrub effects (Tape algorithm, Speed to 0).
- Playing a loop in time with the song (Motion = Envelope 1, Beat Sync on a ramp).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Algorithm**: how the sample is played — Spectral Grains (FFT; can force it harmonic), Grain Oscillator (tiny grains, pitch from the keyboard, sample only colours the tone), Long Grains (keeps the sample's own pitch), Tape (speed and pitch linked).
- **Motion**: Freeze (stay at Start), One Shot, FW Loop, FW-BW Loop, End Freeze, Envelope 1 (Envelope 1 draws the path through the sample).
- **Position** / **End Pos**: sample start and end. Start after End = plays backwards.
- **Speed**: how fast the playhead moves (0% = stopped; in Tape it's also pitch).
- **Jitter**: random wobble of the play position — makes it alive/chorus-y.
- **Global Position**: new notes carry on from where the playhead is instead of restarting.
- **Grain Length** / **Rate-Spacing** / **XFade**: grain size, spacing/rate, and crossfade between grains (low XFade = gritty/poppy).
- **Pan Spread**: alternate grains left/right (Grain Oscillator: also adds a sub an octave down).
- **Pitch Jitter**: random pitch per grain.
- **Formant** / **Formant Tune**: tone colour (or pitch in Spectral Grains when Snap and Filter are 0).
- **Harm Snap** / **Harm Filter**: Spectral Grains — pull partials onto harmonics / remove the inharmonic ones.
- **FFT Size**: Spectral analysis accuracy (0 fast, 3 catches lows).
- **Curve On** / **Curve Amt**: your drawn formant curve.
- **Oct** / **Semi** / **Tune** / **Pitch Kbd**: pitch; Kbd 100% = normal keyboard.
- **Sample Level** / **Sample To Filter**: sample level and routing to the filter.
- **Osc On** / **Osc Wave** / **Osc Mod** / **Osc Oct** / **Osc Level** / **Osc To Filter**: extra oscillator (sine, triangle, saw, pulse, noise…), handy as a pitch reference under a smeared sample.
- **Filter Type** / **Filter Freq** / **Filter Reso** / **Filter Env2** / **Filter Vel** / **Filter Kbd**: HP12, BP12, LP12, LP24 ladder; Envelope 2 hard-wired to cutoff.
- **Amp Attack** / **Amp Decay** / **Amp Sustain** / **Amp Release** / **Amp Gain**: volume envelope.
- **LFO 1 Rate** / **LFO 1 TempoSync** / **LFO 1 KeySync** / **LFO 1 Global**: LFOs (also 2 and 3).
- **Env 1 Rate** / **Env 2 Rate**: envelope speeds.
- **Effect Select** / **Effect On**: pick/enable an effect in the multi-effect.
- **Dist On** / **Dist Drive** / **Dist Tone** / **Dist Amount**, **Comp On** / **Comp Threshold** / **Comp Ratio** / **Comp Attack** / **Comp Release**, **Delay On** / **Delay Time** / **Delay Sync** / **Delay FB** / **Delay PingPong** / **Delay Amount**, **Reverb On** / **Reverb Size** / **Reverb Decay** / **Reverb Damp** / **Reverb Amount**, **EQ On** / **EQ Freq** / **EQ Gain** / **EQ Q**, **Mod Effect Type** / **Mod Effect Rate** / **Mod Effect Depth**: the effects.
- **Key Mode** (Poly up to 12 / Mono Retrig / Mono Legato), **Portamento** / **Portamento Mode**, **Master Volume**, **Mod Wheel**, **Pitch Bend**.

## Where it shines / falls short
Shines: making something new and musical out of samples he already owns — fits
the no-synthesized-sounds house rule. Falls short: tight, punchy one-shot drum
playback — NN-XT or Kong for that.

## Pairs well with
The Echo, RV7000, MClass Stereo Imager.

=====================================================
SOURCE FILE: guitar-amps.md
ORIGINAL LOCATION: HS:device_refs/guitar-amps.md
=====================================================

# Your guitar amps (Crate, Epiphone Electar, and the red one)

Three combo amps — each one is a flavor, not just a volume box. The Crate
leans modern and gritty, the old Epiphone Electar is a vintage voice
(warm, boxy, breaks up sweetly when pushed), and the red-panel one is a
third color. Different amp = different song, so pick by mood before
reaching for pedals or plugins.

## Getting an amp INTO Reason (two honest ways)

1. **Mic the amp (the real-deal way).** Dynamic mic (SM57-type) an inch
   from the grille, pointed just off the speaker's center. Mic → AudioBox
   input, gain until green flickers, never red. Dead-center = brighter;
   toward the edge = warmer. Move the mic before touching EQ — one inch
   does more than any knob.
2. **Skip the amp (the quiet-apartment way).** Guitar straight into the
   AudioBox (it has instrument-friendly inputs), then use Reason's own
   distortion (Scream 4) and cab-flavored EQ for the dirt. Cleaner,
   quieter, endlessly re-editable — but it's Reason's grit, not the
   Crate's.

## The shoegaze cheat
The Shoegaze Guitar Wall recipe in the book pairs perfectly with the
Electar: its natural vintage fuzz stacked with Reason reverbs gets you
most of the wall before any plugin. Record it mic'd (way 1) and double
the take twice, panned hard left and right.

## One safety note
Tube-style amps hate being powered on with no speaker connected, and all
amps hate drinks on top. That's the whole lecture.

=====================================================
SOURCE FILE: humana.md
ORIGINAL LOCATION: HS:device_refs/humana.md
=====================================================

# Humana Vocal Ensemble

Multisampled choir and solo voices: "Mars", "Venus", "Mercury" ensembles
(ah / oo, sustained and staccato), Female Soprano/Alto, Male Tenor/Bass, and
solo Female/Male "ah". Same layout as Klang.
Source: Reason 12.7 Operation Manual, ch. 42, pp. 987–1004.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Instrument**, **Octave** / **Semitune** / **Finetune**, **SampleStart**.
- **Filter_On** / **Filter_Type** (LP, HP, BP, Comb) / **Filter_Cutoff** / **Filter_Reso** / **Filter_Env** / **Filter_Velocity** / **Filter_KeyFollow** / **Filter_Attack** / **Filter_Decay** / **Filter_Sustain** / **Filter_Release**.
- **Amp_Attack** / **Amp_Decay** / **Amp_Sustain** / **Amp_Release**.
- **Delay_On** / **Delay_Time** / **Delay_Sync** / **Synced_Delay_Time** / **Delay_Feedback** / **Delay_Damp** / **Delay_PingPong** / **Delay_Amount**.
- **Reverb_On** / **Reverb_Time** / **Reverb_PreDelay** / **Reverb_LowDamp** / **Reverb_HighDamp** / **Reverb_Amount**.
- **ModWheel_to_Amp_Level**, **Master_Volume**, **Mod Wheel**, **Pitch Bend**.

Reason's factory maps also list "Filter 1/2" and "Osc 1–3 Filter Select" names for
Humana that the manual never explains — unverified, so not described here.

## Where it shines / falls short
Shines: choir pads, "ooh" beds, staccato vocal stabs. Falls short: words — it only sings vowels.

=====================================================
SOURCE FILE: id8.md
ORIGINAL LOCATION: HS:device_refs/id8.md
=====================================================

# ID8 Instrument Device

Preset sound module: 36 ready sounds in 9 categories (piano, e-piano, organ,
guitar, bass, strings, brass/wind, synth, 4 drum kits of 53–65 sounds). Reason
puts one on every track when you import a MIDI file.
Source: Reason 12.7 Operation Manual, ch. 37, pp. 923–926.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Category** / **Sound**: pick the family and the sound (**Sound A**–**Sound D** = the four in a category).
- **Parameter 1** / **Parameter 2**: two preset tweak knobs; what they do changes per sound (shown on the panel).
- **Volume**.
- **Mod Wheel**: usually vibrato; on Electronic Drums a low-pass cutoff; nothing on other kits.
- **Pitch Bend**: fixed ±2 semitones.

## Notes
- Top velocity layer can be a different articulation: slides on the basses and jazz guitar, pizzicato on Arco Strings.
- Edits save with the song only (no patch saving) — or wrap it in a Combinator.
- It has no knob for incoming CCs it doesn't know — an imported MIDI CC lane lands as an "alien" clip (confirmed in the 2026-09-25 automation test).

## Where it shines / falls short
Shines: instant sketch sounds, MIDI import. Falls short: shaping — swap it for a real instrument once the part is right.

=====================================================
SOURCE FILE: klang.md
ORIGINAL LOCATION: HS:device_refs/klang.md
=====================================================

# Klang Tuned Percussion

Multisampled tuned percussion: Alto Glockenspiel, Bamblong, Circle Bells Mallet,
Cylindrum, Imbibaphones, Kalimba, Music Box, Noah Bells, Steel Tones, Whale Drum.
Filter, amp envelope, delay and reverb built in. (Same layout as Pangea and Humana.)
Source: Reason 12.7 Operation Manual, ch. 40, pp. 955–970.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Instrument**: which sound.
- **Octave** / **Semitune** / **Finetune**: pitch.
- **SampleStart**: skip into the sample (0–150 ms) — softens or removes the attack.
- **Filter_On** / **Filter_Type** / **Filter_Cutoff** / **Filter_Reso**: LP, HP, BP or Comb.
- **Filter_Env** / **Filter_Velocity** / **Filter_KeyFollow** / **Filter_Attack** / **Filter_Decay** / **Filter_Sustain** / **Filter_Release**: filter envelope and what drives it.
- **Amp_Attack** / **Amp_Decay** / **Amp_Sustain** / **Amp_Release**: volume envelope.
- **Delay_On** / **Delay_Time** / **Delay_Sync** / **Synced_Delay_Time** / **Delay_Feedback** / **Delay_Damp** / **Delay_PingPong** / **Delay Amount**: delay.
- **Reverb_On** / **Reverb_Time** / **Reverb_PreDelay** / **Reverb_LowDamp** / **Reverb_HighDamp** / **Reverb Amount**: reverb.
- **Mod Wheel to Amp Level**, **Master_Volume**, **Mod Wheel**, **Pitch Bend**. The wheel can also move sample start and filter.

Instruments play beyond their natural range on purpose — odd effects at the extremes.

## Where it shines / falls short
Shines: kalimba/music-box/bell melodies and textures for lo-fi and trap tops. Falls short: only these ten sounds.

=== END OF PART ===
