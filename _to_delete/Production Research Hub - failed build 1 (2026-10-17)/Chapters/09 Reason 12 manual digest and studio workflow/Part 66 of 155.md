# Chapter 09: Reason 12 manual digest and studio workflow
## Part 66 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 57 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 67 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 57 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Slices parameters for a loaded REX loop.
      D   To select a slice for editing, click on the desired slice in the REX loop display.
          Alternatively, click and drag up/down in the Slice number box or use the Slice Select knob below the Slice item.
      The Slice Parameters are:
      • Trig
          Click the Trig check box for the slices you want to alternate between using the Slice Trig Hit Type.
      • Pitch
          Set the pitch for each individual slice in the REX loop by clicking and dragging the Pitch value up/down.
      • Level
          Set the level for each individual slice in the REX loop by clicking and dragging the Level value up/down.
      • Reverse
          Click the Reverse box for the slices you want to play back backwards.

      The Nurse Rex panel parameters
      On the Nurse Rex panel you can edit parameters that are common to all slices in the loaded REX loop:

      • Env Type
          Sets the amplitude envelope type to “Gate” or “ADSR” (Attack, Decay, Sustain, Release). In Gate mode, the gate
          time is set with the Decay parameter.
      • Attack with Velocity control
          Sets the attack time for the amplitude envelope when ADSR is selected as Env Type. The attack time can also be
          velocity controlled according to the sensitivity set with the Vel knob.
      • Decay with Velocity and Modulation controls
          Sets the decay time for the amplitude envelope when ADSR is selected as Env Type. When Gate is selected as
          Env Type, the Decay parameter sets the gate time. The decay/gate time can also be velocity controlled according
          to the sensitivity set with the Vel knob. You can also control the decay/gate time from the Mod Wheel with the
          amount set with the Mod knob.
      • Sustain
          Sets the sustain level of the amplitude envelope when ADSR is selected as Env Type. In Gate mode, the Sustain
          parameter has no effect.

      • Release with Velocity and Modulation controls
        Sets the release time for the amplitude envelope when ADSR is selected as Env Type. The release time can also
        be velocity controlled according to the sensitivity set with the Vel knob. You can also control the release time from
        the Mod Wheel with the amount set with the Mod knob. In Gate mode, the Release parameter has no effect.
      • Pitch with Velocity control
        Sets the overall pitch of all slices in the REX loop. The pitch can be velocity controlled according to the Vel knob
        setting. A negative Vel setting will lower the pitch with increasing velocity and a positive setting will raise the pitch
        with increasing velocity.
      • Level with Velocity control
        Sets the overall level of all slices in the REX loop. The level can be velocity controlled according to the Vel knob
        setting. A negative Vel setting will lower the level with increasing velocity and a positive setting will raise the level
        with increasing velocity.
      At the top of the Nurse Rex panel is a button for setting the polyphony:

      • Polyphonic means full polyphony
        Retriggering the same slice/chunk will keep on adding more voices without muting any sustaining sounds.
      • Monophonic will make any new triggered loop/slice/chunk mute any currently playing/sustaining sound.

      Physical Bass Drum, Snare Drum and Tom Tom

      The Physical Bass Drum, Snare Drum and Tom Tom use very faithful mathematical models for generating acoustic
      drum sounds. The sounds of the PM drums are generated using physical modelling; mathematical real-time calcula-
      tions of physical acoustic phenomena. The physical modelling technique allows for a lot more creative freedom, and
      much wider sonic ranges, compared to sample playback.

      General parameters
      • Level
        This controls the overall output level of the Drum module to the FX1 and FX2 Slots (see “Signal flow”). The Level
        is also affected by velocity.

      Drum head and shell parameters
      The Physical Modelling Drums feature the following drum head and shell parameters:
      • Pitch
        Sets the overall pitch of the drum. The Pitch parameter can be considered the total size of the drum and affects all
        other head and shell parameters.
      • Tune 1 and Tune 2 (PM Bass Drum and PM Tom Tom)
        The Tune 1 and Tune 2 parameters set the drum’s harmonic character, similar to the effect of individually adjusting
        the rim tension screws of the top drum head.
      • Tune (PM Snare Drum)
        This controls the top drum head tension and thus affects the harmonic character of the sound.
      • Bend Amount (PM Bass Drum and PM Tom Tom)
        This sets the dynamic “pitch bend” effect you get when hitting a drum head.
      • Damp
        This controls the damping of the drum head.
      • Decay
        The Decay parameter doesn’t have any actual counterpart in real life. It simply controls the decay time of the drum
        sound.
      • Shell Level (PM Bass Drum and PM Tom Tom)
        This controls how much of the drum shell sound should be present in the sound.
      • Shell Size (PM Tom Tom)
        This controls the depth (“length”) of the shell.
      • Edge Tune (PM Snare Drum)
        This controls the head tuning when Hit Type 4 (Edge Hit) is selected for the pad (see “Assigning Hit Type to
        Pads”).
      • Snare Tension (PM Snare Drum)
        This controls the tension of the snare and the distance between the snare and bottom drum head.
      • Bottom Pitch (PM Snare Drum)
        This controls the pitch of the bottom drum head.
      • Bottom Mix (PM Snare Drum)
        This controls how much of the bottom head sound should be present in the drum sound.

      Beater and Stick parameters
      • Density (PM Bass Drum)
        This controls the “hardness” of the bass drum pedal beater.
      • Tone (PM Bass Drum and PM Tom Tom)
        This is a filter which controls the tone of the hit.
      • Beater Level (PM Bass Drum)
        This controls how much of the beater hit sound should be present in the drum sound.
      • Stick Level (PM Tom Tom)
        This controls how much of the drum stick hit sound should be present in the drum sound.

      Synth Bass Drum, Snare Drum and Tom Tom

      The Synth Bass Drum, Snare Drum and Tom Tom use analog modelling to generate classic synth drum sounds. The
      Synth Tom Tom was faithfully modelled after a famous hexagonal shaped analog drum system from the 80’s.

      General parameters
      • Level
        This controls the overall output level of the Drum module to the FX1 and FX2 Slots (see “Signal flow”). The Level
        is also affected by velocity.

      Drum parameters
      The Synth Drums feature the following parameters:
      • Pitch
        This sets the overall pitch of the drum. The Noise pitch is not affected by this parameter.
      • Tone (Synth Bass Drum)
        This is a filter similar to the one used in Redrum and affects the tone of the drum. The Noise is not affected by this
        parameter.
      • Attack (Synth Bass Drum)
        Sets the attack time of the drum sound. This also affects the Noise.
      • Decay
        Sets the Decay time of the drum sound. This also affects the Noise decay on the Synth Bass Drum and is added
        to the Noise Decay parameter on the Synth Snare and Synth Tom Tom drums. It is also added to the Harmonic
        Decay value on the Synth Snare Drum. The Decay time is also affected by velocity.
      • Harmonic Balance (Synth Snare Drum)
        Sets the level balance between the fundamental tone and the harmonic tone.
      • Harmonic Frequency (Synth Snare Drum)
        Sets the frequency of the harmonic tone.
      • Harmonic Decay (Synth Snare Drum)
        Sets the decay time of the harmonic tone. This is also affected by the Decay parameter.
      • Click Frequency (Synth Bass Drum)
        Sets the frequency of the click sound in the attack.
      • Click Resonance (Synth Bass Drum)
        Sets the resonance amount of the click sound in the attack.
      • Click Level (Synth Bass Drum and Synth Tom Tom)
        Sets the level of the click sound in the attack.

      • Bend Time (Synth Bass Drum and Synth Tom Tom)
        Sets the time it should take to change the pitch from the Bend Amount value (se below) back to the original pitch.
      • Bend Amount (Synth Bass Drum and Synth Tom Tom)
        Sets the upper pitch to bend from. The Bend Amount is also affected by velocity.
      • Noise Tone (Synth Snare Drum and Synth Tom Tom)
        This is a filter which sets the frequency content of the noise.
      • Noise Decay (Synth Snare Drum and Synth Tom Tom)
        This sets the decay of the noise in the sound. The Noise Decay is also affected by the regular Decay parameter.
      • Noise Mix (Synth Snare Drum and Synth Tom Tom)
        Sets the noise level in the drum sound.

      Synth Hi-hat

      The Synth Hi-hat uses analog modelling to generate sounds. The Synth Hi-hat can be used for generating the typical
      hi-hat sounds of the early analog drum machines.

      Parameters
      • Pitch
        This sets the overall pitch of the hi-hat sound.
      • Decay
        This sets the decay time of the hi-hat sound.
      • Level
        This controls the overall output level of the Synth Hi-hat module to the FX1 and FX2 Slots (see “Signal flow”). The
        Level is also affected by velocity.
      • Click
        This controls the click level in the attack of the hi-hat sound.
      • Tone
        This is a filter similar to the one used in Redrum and affects the frequency content of the hi-hat sound.
      • Ring
        Sets the level of the resonance peaks in the sound. The higher the value, the more “metallic” the sound.

      The Support Generator modules
      There are two types of Support Generator modules in Kong, one for generating noise and another one for generating
      a tone. The Support Generator modules can be used as companions to any of the Drum modules, or stand-alone. The
      Support Generators can be loaded into the FX1 and/or FX2 slots.
      !   Note that only two pre-defined parameters per Support Generator module can be automated!

      Noise Generator

      • Hit Type buttons
          These buttons allow you to choose for which Hit Type(s) the Noise generator should be active. By default, the
          Noise generator is active for all Hit Types (see “Assigning Hit Type to Pads”).
      • Pitch
          This sets the center pitch of the noise.
      • Attack
          This sets the attack time of the noise.
      • Decay
          This sets the decay time of the noise.
      • Reso
          This sets the resonance amount of the noise around the center pitch.
      • Sweep
          This sets the upper start pitch of the sweep range. The Sweep range is also affected by velocity.
      • Click
          This sets the level of the click in the attack of the noise.
      • Level
          This sets the overall level of the Noise generator. The level is also affected by velocity.

      Tone Generator

      • Hit Type buttons
        These buttons allow you to choose for which Hit Type(s) the Tone generator should be active. By default, the Tone
        generator is active for all Hit Types (see “Assigning Hit Type to Pads”).
      • Pitch
        This sets the pitch of the oscillator.
      • Attack
        This sets the attack time of the tone.
      • Decay
        This sets the decay time of the tone.
      • Bend Decay
        This sets the decay time for the Bend.
      • Bend
        This sets the upper start pitch of the bend range. The Bend range is also affected by velocity.
      • Shape
        This sets the tonal character of the sound, from less to more harmonics.
      • Level
        This sets the overall level of the Tone generator. The level is also affected by velocity.

      The FX modules
      The FX modules can be used in any of the FX1, FX2, Bus FX and Master FX slots.
      !   Note that only two pre-defined parameters per FX Module can be automated!

      Using CV modulation of Bus FX and Master FX parameters
      When the FX modules are used in the Bus FX and/or Master FX slots, it is possible to route external CV signals to
      the first two Effect module parameters for modulation. If you hover with the mouse over the first or second parameter
      of an FX module loaded in the Bus FX or Master FX slot, a tool tip appears:

      The tool tip shows which CV modulation input on the back of the unfolded Kong panel will control that parameter. For
      FX modules loaded in the Bus FX slot, the tool tip displays “Bus FX P1: nn” for the first FX module parameter and
      “Bus FX P2: nn” for the second one. For FX modules loaded in the Master FX slot, the tool tip instead reads “Master
      FX P1: nn” for the first FX module parameter and “Master FX P2: nn” for the second one. The “nn” in the tool tip in-
      dicates the current parameter value.
      By connecting cables to the CV modulation inputs on the back of the Kong panel, you can modulate the correspond-
      ing FX module parameters in the Bus FX and/or Master FX slots.

      D   Control the FX parameter modulation amounts with the corresponding attenuation knobs.
      If you decide to replace the FX modules in the Bus FX and/or Master FX slots, the modulation routing will be pre-
      served - but the CV signals will now control the first two parameters of the replacement module(s).

      Drum Room Reverb

      The Drum Room Reverb is a reverb with a room-type reverb algorithm. It’s perfect for adding ambience to single drum
      sounds or to the entire mix of all 16 drum channels. The parameters are as follows:
      • Size
        This sets the “size” of the room, from small to large.
      • Decay
        This sets the reverb decay time.
      • Damp
        This sets the high frequency damping amount of the reverb effect, from none to heavy.
      • Width
        This sets the stereo effect of the reverb, from mono to wide stereo.
      • Dry/Wet
        This sets the mix between Dry (no effect) and Wet (reverb) signal.

      Transient Shaper

      The Transient Shaper is a type of dynamics processor which produces a result that could be compared to that of a
      compressor. As opposed to a “normal” compressor, the Transient Shaper mainly affects the signal’s attack, or tran-
      sients in the signal, making the signal transients cut through in the mix. The parameters are as follows:
      • Attack
        A positive Attack value will produce an amplified attack/transient whereas a negative value will reduce the attack/
        transient volume.

      • Decay
        This sets the decay time from amplification/attenuation back to normal amplitude level.
      • Amount
        This controls the amplification amount. A high Amount in combination with a positive Attack value will produce a
        very pronounced attack/transient in the sound.

      Compressor

      The Compressor levels out the audio, by making loud sounds softer. To compensate for the volume loss, the Com-
      pressor has a make-up gain control for raising the overall level by a suitable amount. The result is that the audio levels
      become more even and the sounds can get more “power” and longer sustain. The parameters are as follows:
      • Amount
        This sets the sensitivity of the compressor. A high amount will make the compressor more sensitive and react to
        weak input signals.
      • Attack
        This sets how fast the compression should be applied to the incoming signal. A low value will make the compres-
        sion set in immediately whereas a high value will let the attack/transients through before compression sets in.
      • Release
        This sets how long it should take before the compressor lets the sound through unaffected again. Set this to short
        values for more intense, “pumping” compressor effects, or to longer values for a smoother change of the dynamics.
      • Make up gain
        This sets the overall level compensation. A low value will produce a softer output signal whereas a high value will
        amplify the output signal.

      Filter

      The Filter is a state variable filter with a switch for selecting Lowpass, Bandpass or Highpass state. It has controls for
      cutoff/center frequency and resonance amount and can also be controlled from a built-in MIDI controlled envelope
      generator for sweeping the frequency. When used in the Bus FX Slot, MIDI Note E2 (#52) trigs the envelope. When
      used in the Master FX Slot, MIDI Note F2 (#53) trigs the envelope. The parameters are as follows:
      • Frequency
        Sets the cutoff frequency in the LP and HP states and center frequency in the BP state.
      • Resonance
        This sets the amplification amount of the frequencies around the cutoff/center frequency.
      • LP/BP/HP
        Sets the state of the filter to either Lowpass, Bandpass or Highpass.
      • MIDI Trig EG Amount
        This sets the amount of the MIDI controlled filter envelope. The Amount value is bipolar (+/-). Set to a positive
        value, the envelope will sweep the filter frequency from a high value down to the set Frequency value. Set to a neg-
        ative Amount, the envelope will sweep the filter frequency from a low value up to the set Frequency value. The
        Amount is also affected by velocity.
      • MIDI Trig EG Decay
        This sets the MIDI controlled envelope decay time.

      Parametric EQ

      The Parametric EQ is a single-band parametric equalizer with controls for center frequency, gain and bandwidth (Q-
      value). The parameters are as follows:

      • Frequency
        Sets the center frequency of the equalizer.
      • Gain
        Sets the amplification (positive Gain value) or attenuation (negative Gain value) around the center Frequency.
      • Q
        Sets the bandwidth around the center Frequency, from wide to a narrow peak.

      Ring Modulator

      The Ring Modulator takes the input signal and multiplies it with an internal sinewave signal. The result is often a syn-
      thetic metallic sound. The Ring Modulator also features a MIDI controlled envelope generator for sweeping the inter-
      nal sinewave frequency. When used in the Bus FX Slot, MIDI Note E2 (#52) trigs the envelope. When used in the
      Master FX Slot, MIDI Note F2 (#53) trigs the envelope. The parameters are as follows:
      • Frequency
        Sets the frequency of the internal sinewave oscillator. The higher the frequency, the higher the resulting output
        signal pitch.
      • Amount
        Sets the level of the internal sinewave oscillator. The higher the level, the more the ring modulation effect.
      • MIDI Trig EG Amount
        This sets the amount of the MIDI controlled envelope. The Amount value is bipolar (+/-). Set to a positive value, the
        envelope will sweep the internal sinewave oscillator frequency from a high value down to the set Frequency value.
        Set to a negative Amount, the envelope will sweep the oscillator frequency from a low value up to the set Fre-
        quency value. The Amount is not affected by velocity.
      • MIDI Trig EG Decay
        This sets the MIDI controlled envelope decay time.

      Rattler

      The Rattler adds the effect of a snare “attached” to whatever sound is fed through it. Using the Rattler in combination
      with other types of sounds than “usual” snare drum sounds can produce really interesting results! Ever played a snare
      bass drum, or a snare hi-hat, for example? The parameters are as follows:
      • Snare Tension
        This sets the tension of the snare. Note that when the Snare Tension is increased, the effect will actually be less
        pronounced since the snare will have “less contact” with the sound source.
      • Tone
        This is a filter similar to the one used in Redrum and affects the frequency content of the output signal.
      • Decay
        This sets how long the snare will “ring”.
      • Tune
        This sets the snare tuning, from low to high, and affects the frequency content of the signal.
      • Level
        This sets the overall level of the Rattler. The level is also affected by velocity.

      Tape Echo

      The Tape Echo is based on the principles of classic tape echo effects. The original tape echo effects were electro-
      mechanical devices that used an endless magnetic tape in combination with recording and playback heads inside the
      box. Depending on the speed of the tape, and on which playback heads were used, the echo repetition and echo pat-
      terns could be controlled. Later on, a lot of tape echo effects were replaced by digital delay effects. The Tape Echo
      in Kong simulates the classic tape echo effect and features the following parameters:

      • Time
        This sets the time between the delays, from short to long.
      • Feedback
        This sets the number of delay repetitions, from one to... many.
      • Wobble
        This sets the tape speed wobbling effect. Since it emulates a magnetic tape, a wobbling speed also automatically
        produces a wobbling pitch of the signal.
      • Frequency
        This sets the change in frequency of the delay repetitions. For every delay, the frequency content will shift accord-
        ing to the Frequency setting. A low value will make each repetition sound muddier than the previous one, whereas
        a high value will make each delay sound brighter.
      • Resonance
        This sets the resonance amount of the delay repetitions. Depending on the Frequency parameter setting above,
        different frequencies will be amplified.
      • Dry/Wet
        This is a traditional dry/wet parameter for controlling the relationship between unprocessed and processed signal.

      Overdrive/Resonator


=== END OF PART ===
