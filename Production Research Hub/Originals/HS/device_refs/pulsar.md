# Pulsar Dual LFO

Two LFOs plus an attack/release envelope, as a rack utility. Its CV outputs
modulate any other device's CV inputs. Rates reach audio range; can sync to tempo
and be "played" from the keyboard.
Source: Reason 12.7 Operation Manual, ch. 64, pp. 1333–1342.

## When you'd use it
- Tempo-synced wobble, tremolo, filter pumping on devices that lack their own LFO.
- Complex modulation: LFO 2 speeding up/scaling LFO 1.
- Gated/pumping effects triggered by notes or its own envelope.

## Key controls
Named exactly as Reason's Remote layer names them.

- **LFO1 Waveform** / **LFO2 Waveform**: nine shapes incl. random, slope, stepped.
- **LFO1 Rate Free** / **LFO1 Rate Synced** / **LFO1 Tempo Sync**: speed (free Hz or note values).
- **LFO1 Level**: output amount.
- **LFO1 Phase**: start point in the cycle (0–360°).
- **LFO1 Shuffle**: swings pairs of cycles (stays in time when synced).
- **LFO1 Lag**: smooths sharp shapes.
- **LFO1 Env Sync**: envelope trigger restarts LFO 1.
- **LFO2 Enabled** + the same LFO2 set (**LFO2 Rate Free**, **LFO2 Rate Synced**, **LFO2 Tempo Sync**, **LFO2 Level**, **LFO2 Phase**, **LFO2 Shuffle**, **LFO2 Lag**).
- **LFO2 to LFO1 Rate** / **LFO2 to LFO1 Level**: LFO 2 FM/AM-modulates LFO 1.
- **Sync LFO1 to LFO2**: each LFO 2 cycle restarts LFO 1.
- **Attack** / **Release** / **Trig**: the AR envelope; Trig is a hold-to-open gate. Also fired by MIDI notes, the rear gate input, or LFO 2.
- **LFO2 Triggers Envelope**: every LFO 2 cycle fires the envelope.
- **LFO1 Env Rate** / **LFO1 Env Level** / **LFO2 Env Rate** / **LFO2 Env Level**: envelope moves each LFO's speed/level (bipolar).
- **Keyboard Track**: MIDI notes change LFO speed (100 = chromatic, centred on C3). Needs its own track.

## Where it shines / falls short
Shines: adds movement to anything with a CV input. Falls short: CV cables are not
saved in device patches — save the setup inside a Combinator.
