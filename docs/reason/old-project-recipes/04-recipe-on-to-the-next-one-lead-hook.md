> Copied 2026-10-11 from the claude.ai "Reason 12" chat "Reason 12 production guide project" (2026-05-14).
> Status: THEORETICAL (as originally tagged). Original text below, unchanged except this note.
> CHECK BEFORE TRUSTING: Thor parameter names/values (use docs/reason/remote-vocab.json for exact spellings), "Reason Studios Algoritm" (not confirmed as a Reason device), and RE names/prices (Softube Heartbeat, GForce ImpOSCar 3) were not verified. "Europa is factory" is true; the rest needs checking.

# On to the Next One — Lead Hook (Justice Sample Recreation)

**Sounds like:** Jay-Z & Swizz Beatz — "On to the Next One" (2009) — the chopped Justice "D.A.N.C.E." (Live Version) hook
**Genre tag:** Hip-Hop / Electro
**Accuracy:** C (55–65%) overall
**Status:** Theoretical — test and report back
**Source assumed:** Building from scratch in Reason 12; no external samples required

---

## What this recipe actually is

Part 1: a Thor patch that approximates Justice's lead synth tone (Juno-style poly synth, narrow pulse, distortion, bit-crush).
Part 2: the Swizz Beatz mangling chain that turns clean source material into the grimy lead heard on the record — chopping, filtering, distortion, pitch tricks.

Build Part 1 for your source, then process it through Part 2. The Part 2 chain works on any source audio.

---

## PART 1 — The Justice-Style Source Synth

### The chain
**Thor** → channel strip

### Settings — Thor

**Oscillator 1**
- Mode: Analog
- Waveform: Square/Pulse
- Pulse Width: 25
- Octave: 4
- Semi: 0
- Detune: 0

**Oscillator 2**
- Mode: Analog
- Waveform: Square/Pulse
- Pulse Width: 30
- Octave: 4
- Semi: 0
- Detune: +7 cents

**Oscillator 3:** OFF

**Filter 1 (Slot 1)**
- Type: Low Pass Ladder
- Frequency: 78
- Resonance: 35
- Drive: 40
- Env: +50

**Amp Envelope**
- Attack: 0
- Decay: 30
- Sustain: 75
- Release: 25

**Filter Envelope (to Filter 1 Frequency)**
- Attack: 0
- Decay: 35 (quick decay — the Justice "pluck")
- Sustain: 20
- Release: 30
- Amount: Filter 1 Freq, +50

**Global**
- Polyphony: 6
- Portamento: 0
- Velocity to Amp: 30
- Velocity to Filter Env: 40

**Chorus:** ON, subtle (default settings, mix 25%)

### Channel strip on Thor's mix channel
- HP filter: 80 Hz
- EQ: +3 dB at 1.5 kHz
- Drive: 25%

---

## PART 2 — The Swizz Mangling Chain

### The chain
Source → **Scream 4** → **MClass Equalizer** → **The Echo** → **MClass Stereo Imager** → **MClass Compressor** → channel strip

### Settings

**Scream 4 (destruction stage)**
- Damage Control: 55
- Damage Type: DIGITAL
- P1 (Bit Depth): 35
- P2 (Sample Rate): 60
- Cut Lo: 30
- Cut Mid: 60
- Cut Hi: 35
- Master: -2

**MClass Equalizer (post-distortion)**
- Low Shelf: cut -8 dB at 150 Hz
- LO Mid: cut -4 dB at 350 Hz
- HI Mid: boost +6 dB at 3 kHz, Q 1.5
- High Shelf: cut -4 dB at 8 kHz

**The Echo**
- Mode: Synced
- Time: 1/8 dotted
- Feedback: 25
- Ducking: ON, amount 40
- Drive: 30
- Color/Filter: 50
- Wobble: 15
- Mix: 25%

**MClass Stereo Imager**
- Lo Width: 0
- Hi Width: 130
- Crossover: 600 Hz

**MClass Compressor**
- Threshold: -14 dB
- Ratio: 4:1
- Attack: 8 ms
- Release: 60 ms
- Output: +3 dB
- Gain reduction target: 4–6 dB on hits

**Channel strip**
- Drive: 10%
- HP filter: 100 Hz

---

## How to use this (the chopping step)

The lead is a rhythmic 3-note stab pattern repeated, not a melodic line.

1. Build the Thor patch from Part 1.
2. Play short stabbed notes — eighth-note triplets or sixteenth-note bursts in groups of 3.
3. Suggested pattern (A minor): A3 → C4 → E4, rhythmically displaced: stab-stab-(rest)-stab on each beat.
4. Render to audio (right-click track → Bounce in Place).
5. Load the bounced audio into Dr. Octo Rex or NN-XT.
6. In Dr. Octo Rex: chop into slices, trigger them out of order from the matrix step sequencer, occasionally reverse a slice, occasionally pitch one down a fifth.
7. Run the chopped audio through the Part 2 chain.

---

## Why this works
Justice's lead is a narrow-pulse-wave Juno-style poly synth pushed into distortion. The Thor patch reproduces the oscillator and filter behavior. The Swizz treatment bit-crushes for the broken digital character, boosts mids so it cuts through a dense beat, uses ducked echo for movement, and mono's the low end so it doesn't fight the 808.

## Order of operations note
Distortion (Scream 4) before EQ so we shape after harmonics are generated. Echo after EQ so delays are already filtered. Stereo Imager before the compressor so the comp glues the widened signal as one. Compressor last so final levels are consistent.

## Reason-specific tricks
1. Combinator the whole thing: Thor + the Part 2 chain in one Combinator 2. Macros: 1 Scream 4 Damage Control, 2 Thor Filter Envelope Decay, 3 The Echo Feedback, 4 MClass Compressor Threshold. Save as "Justice-Style Lead — Mangled."
2. CV automation for the chop: Thor's built-in Step Sequencer (Programmer section) can generate the stab pattern, keeping the patch MIDI-editable.
3. Dr. Octo Rex over NN-XT for chopping: slice-based playback and matrix sequencer suit this.

## RE upgrade path
Stock Reason gets the analog pulse fine; the FM-bell harmonics are weak.
- Europa (factory in Reason 12) — layer a second voice with an FM-style waveform.
- "Reason Studios Algoritm" (the original called it a factory FM synth) — a simple 2-operator FM patch in parallel with Thor. [unverified]
- Softube Heartbeat ($149) — drum-machine transient shaping. [unverified]
- GForce ImpOSCar 3 ($199) — closer to real Juno character. [unverified]

## Technique you just learned
Sample-mangling sound design. Four techniques:
1. A Juno/analog-style poly lead in Thor.
2. The "destroy then shape" order — Scream → EQ → modulation.
3. Bit-crushing for lo-fi character without losing presence — DIGITAL mode + 3 kHz boost + 8 kHz cut.
4. Mono lows + wide highs with the MClass Stereo Imager crossover.

## Reference track
- "Jay-Z On to the Next One official audio"
- "Justice D.A.N.C.E. live version" — the source Swizz sampled (around 1:52)
A/B both. Listen for what Swizz removed (most of Justice's bass and beat) and what he kept and exaggerated (the chopped stab).

---

## Honest flags
1. This is the hardest stock Reason recipe in the book so far. C-grade is realistic. B-grade would be better than most.
2. The chopping step matters as much as the synth. A sustained melodic line will sound nothing like the record.
3. If you have an FM synth, build the source there instead; Justice's bell character is FM. Thor was used because it ships with every Reason 12.
4. The original used real hardware (Juno + distortion pedal + outboard compressors). The patch gets the family right but sounds like a cousin in solo; much closer in a mix.
5. Tagged Theoretical: built from production analysis, not session verification.
