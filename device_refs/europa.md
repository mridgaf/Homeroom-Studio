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
