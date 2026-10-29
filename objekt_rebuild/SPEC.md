# Published Objekt Architecture

This is a source-grounded architecture map from the official 2023 operation manual. It replaces the earlier speculative notes.

## Voice signal flow

```text
Impact + Noise + External In
            |
       per-voice Exciter EQ
            |
      +-----+-----------------------+
      |                             |
    Modal --------> Object 1 ------> Object 2
      |                |                |
      +----------------+----------------+
                       |
                 per-voice Mixer
                       |
            reorderable global effects
                       |
                  stereo output
```

The manual states that Modal can feed Object 1, and Object 1 can feed Object 2. Every resonator does not have to be audible in the mixer to be used as an intermediate filter/exciter stage.

## Exciter

### Impact

The impact generator models a strike, pluck, or pick. Published controls include Level and velocity response, Impact Frequency (pulse length/brightness), Click level, Hardness and velocity response, and a Diffuse section with Shape and Time.

### Noise

The noise generator has Level and velocity response, Rate, and a delay/ADSR envelope. Published noise types are Off, White, Color, Static, Noise Pulse, Random Pulse, Pulse, and low-pass noise. Pulse can enter the audio range; the manual recommends Key -> Noise Rate at amount 80 for 1:1 tracking.

### External input and EQ

Stereo external input can excite the model. In polyphonic modes notes create model voices; Mono/Legato can process external audio without note triggering. A per-voice parametric EQ processes the combined Impact, Noise, and External signals before the nonlinear resonators.

## Modal section

- Up to eight tuned resonant filters
- Frequency expressed as a factor of the fundamental (`1.00`, `2.00`, etc.)
- Consecutive active-stage count and consecutive keyboard-tracking count
- Per-stage decay scale and gain
- Overall pitch, decay, and release mute
- Nonlinear pickup model with Drive and Symmetry

## Object 1 and Object 2

Each Object has up to eight tuned feedback-delay stages. The documented controls include:

- Input Mix: Exciter/Modal for Object 1; Exciter/Object 1 for Object 2
- Strike position and per-note random strike-position variation
- Pitch, tuning, low cut, active-stage count, and keyboard-tracking count
- Per-stage frequency factor, polarity, and gain
- Coupling modes: Off, On, and high-pass X-Over
- Collision Amount/Bounce
- Signal-driven Pitch Mod Amount/Filter
- Dispersion Frequency/Mod/Filter
- Feedback-loop damping: low, mid frequency/gain, high cutoff, and high slope
- Decay and release mute

## Mixer

Exciter, Modal, Object 1, and Object 2 have per-voice levels and pan. Object 1 and 2 also have stereo Width controls that distribute delay-line components across the stereo field.

## Effects

Five freely reorderable effects:

1. EQ: low shelf, parametric mid, high shelf
2. Distortion: Dist, Scream, Tube, Sine, sample-and-hold reduction, Ring
3. Stereo compressor
4. Send delay with sync, ping-pong, pan, feedback, and amount
5. Send reverb with type, decay, damping, early-reflection level, and send level

The manual describes selectable reverb algorithms; it does not say convolution. Earlier project notes calling it convolution were wrong.

## Modulation

- Two LFOs
- One 1-16 step/curve generator
- Two named macros
- Eight matrix buses
- Each bus: one source, two destinations, and one scale source
- Amounts are bipolar and can exceed a destination's normal range before clamping

## Performance and utility

- Mono, Legato, Auto Legato, and Poly 1-16 key modes
- Portamento Off/On/Auto
- Pitch bend up to +/-12 semitones
- Built-in analyzer/fix tuner
- Section-selective randomizer
- Rear-panel external audio, CV/Gate, modulation CV inputs, modulation CV outputs, and stereo audio output

## Reconstruction strategy

The rebuild treats the published architecture as a behavioral specification, not as evidence of the proprietary implementation. Modal modes use stable second-order resonators. Object stages use fractional feedback delays. Nonlinear behaviors are bounded with saturation and conservative feedback gains.
