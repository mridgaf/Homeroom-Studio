# Chapter 09: Reason 12 manual digest and studio workflow
## Part 89 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 80 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 90 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 80 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 36: Monotone Bass Synthesizer

Monotone
Bass Synthesizer

      Introduction

      The Monotone Bass Synthesizer is a great little monophonic bass synthesizer, designed for seamless integration of
      Reason Compact projects. Despite its fairly small size, it’s very versatile can produce really fat and punchy bass synth
      sounds.
      Monotone features two oscillators, a 24 dB lowpass ladder filter, amp envelope and chorus and delay effects. It also
      has an LFO and an additional envelope for modulation purposes.

      Panel overview
      The Monotone front panel contains the following sections:

                                           1                            2           3
          4                  5                    6                     7   8   9

                                                  10

      The Monotone front panel sections.
      • 1. MIDI Note On LED.
      • 2. Patch Selector (for browsing, loading and saving patches).
      • 3. Master Volume.
      • 4. Voicing section and global controls.
      • 5. Oscillator section.
      • 6. Filter section.
      • 7. Amplitude Envelope.
      • 8. Chorus section.
      • 9. Delay section.
      • 10. Modulation section.

      Signal flow
      The picture below shows the basic signal flow in Monotone:
                  OCT      Wave

                                                                   Drive    Freq       Res       A     D     S     R     Amount          Amount
                        Oscillator 1                   Noise

                        FM Env          Detune                              Filter                     Amplifier         Chorus           Delay
                                                 OSC
                                                 MIX                                                                                                    Master
                                                                                                                                                        Volume
                        Oscillator 2                           ENV
                                                               (Freq)        KEY        LFO                VEL         Rate   Spread   Time   Feedb.
                                                                                        (Freq)

       LFO
       (pitch)    OCT      Wave        Semi
                                                                                                                              Shape
                                                                           Envelope                              LFO
                                                                                                                              Rate
                                                                                                 VEL

                                                                    A      D       S    R                                                         : audio signal
                                                                                                                                                  : control signal

      Monotone signal flowchart.
      • The “heart” of Monotone is the Oscillator section, which generates the basic audio signal.
         There are two oscillators in Monotone, that can produce a number of traditional “analog” waveforms - plus a Noise
         generator, which produces white noise. The two oscillators can be detuned, to create a fatter sound. Oscillator 2
         can also frequency modulate Oscillator 1, for metallic/bell type sounds.
      • The signal from the Oscillator section is routed to the Filter.
         The Filter in Monotone is a classic 24 dB/octave lowpass ladder filter, with overdrive control.
      • The signal from the Filter is routed to the Amplifier.
         The Amplifier is controlled by a standard ADSR (Attack-Decay-Sustain-Release) envelope.
      • The signal from the Amplifier is then routed to the Chorus module.
         This module generates a chorus effects, to make the sound fat and wide.
      • The signal from the Chorus is then routed to the Delay module.
         Here you can add audio delay effects.
      • The remaining section in Monotone (Envelopes and LFO) can be used for modulating some Oscillator and
        Filter parameters.

      Playing and using Monotone
      Loading and saving patches

      Loading and saving patches is done in the same way as with any other internal Reason device, see “Loading patches”
      and “Saving patches” for details.

      Global output controls

      Master Volume
      This is the main stereo output volume control.

      Global performance and “play” controls

      Portamento
      Portamento makes the note pitch glide from the previous note to the new one, at the time set with the Portamento
      knob.
      • When On, the pitch will always glide between consecutive notes.
      • In Auto mode, the pitch will glide between consecutive notes only when you play legato.
          If you release the previous key before hitting the new key, there will be no portamento effect.

      Retrig
      D   Click the Retrig button if you want to play Monotone and always retrigger the envelopes as soon as you play a
          new note.
          When Off, the envelopes will retrigger only if you have released the previous note before playing the new note.

      Range
      D   Set the desired Pitch Bend range for the “Pitch” wheel with the up/down buttons, or by click-holding on the
          display and dragging up/down.
          Range: +/-24 semitones (+/-2 octaves) in steps of +/-1 semitone.

      Pitch
      The Pitch bend wheel can be used for bending note pitches up and down. Monotone also responds to Pitch Bend
      MIDI data from a connected MIDI master keyboard. You set the desired Pitch bend Range with the “Range” control
      above the Pitch bend wheel.

      Mod
      The Mod wheel can be used for controlling the Filter Frequency and LFO intensity in Monotone.
      D   Raise the FILT knob above the Mod wheel to set the Filter Frequency modulation amount.
      D   Raise the LFO knob above the Mod wheel to set the LFO intensity modulation amount.
          Note that for the LFO modulation to work you need to already have some LFO modulation set in the Oscillator
          (see “LFO”) and/or Filter (see “LFO”) sections.

      Panel reference
      The Oscillator section

      Here is where you choose oscillator waveforms and set the pitches for the two oscillators. You can also add noise
      and frequency modulate Oscillator 1 from Oscillator 2.

      Waveform selector
      D   Turn the Wave knob to select one of four wave shapes.
      The wave shapes are:
      • Ramp
          Also known as sawtooth. Generates a rich tone with both even and odd harmonics (overtones).
      • Square (Pulse in Oscillator 2)
          The square wave has a symmetric square shape and contains only even harmonics. The Pulse wave is basically a
          square wave with non-symmetrical shape, i.e. a duty cycle that is not 50%. The Pulse wave generally sounds a little
          thinner than a perfect square wave.

      • Triangle
          The Triangle wave only contains odd harmonics, and at lower intensities than the square wave overtones. This
          makes it sound a little “rounder” and with less bite than the square wave.
      • Sine
          The Sine wave doesn’t contain any overtones - only the fundamental. This makes it sound dull and makes it perfect
          as a sub bass an octave or two below another waveform in the other oscillator.

      Oct
      D   Set the pitch in octave steps.
          Range: 5 octaves.

      Osc Mix
      D   Set the mix of the Oscillator 1 and 2 signals.

      Noise
      D   Turn up the Noise knob to introduce white noise to the oscillator signal mix.

      Detune
      D   Change the pitch in steps of 1 cent (in opposite directions for the two oscillators).
          Range: +/- 50 cents (down or up half a semitone).

      LFO
      D   Turn the LFO knob to introduce pitch modulation to both oscillators from the current setting of the LFO section
          (see “The LFO section”).

      FM Env
      D   Turn the knob to have the oscillator 2 signal frequency modulate the oscillator 1 signal according to the cur-
          rent Envelope settings (see “The Envelope section”).
          Range: 0% (no tracking (constant pitch)) to 100% (1 semitone per note).

      Osc 2 Semi
      D   Set the pitch of Oscillator 2 in semitone steps.
          Range: +/-12 semitones (two octaves).

      The Filter section

      The Filter in Monotone is a classic 24 dB/octave lowpass ladder filter. If you raise the Resonance high enough, the
      filter will start to self-oscillate.

      The picture below shows the lowpass filter’s basic characteristics at four different resonance levels:
      Amplitude

                                           RESONANCE

                                                         Frequency
                                FREQ

      Drive
      D   Turn the Drive knob to amplify and introduce an overdrive type of distortion to the signal fed into the filter.

      Freq
      D   Set the cutoff frequency for the filter.
          The cutoff frequency is where the filter starts to cut out/dampen the higher frequencies of the signal.

      Resonance
      D   Set the resonance amount.
          This controls the resonance peak level at the currently set cutoff frequency (see “Freq” above).
          The picture below shows a ramp oscillator signal lowpass-filtered at three different Resonance levels:

                                                           Amplitude

          Amplitude                                                                                     Amplitude

                                         Time                                                                          Time
                                                     RESONANCE

                                                                                            Frequency
                                                                       FREQ
                                                                       (Cutoff Frequency)

                                                           Amplitude

          Amplitude                                                                                     Amplitude

                                         Time                                                                          Time
                                                     RESONANCE

                                                                                            Frequency
                                                                       FREQ
                                                                       (Cutoff Frequency)

                                                           Amplitude

          Amplitude                                                                                     Amplitude

                                         Time                                                                          Time
                                                     RESONANCE

                                                                                            Frequency
                                                                       FREQ
                                                                       (Cutoff Frequency)

      !   Be careful when using high Resonance values as this could generate quite loud audio levels!

      Env
      D   Turn the Env knob to set the frequency modulation amount from the current settings of the Envelope (see “The
          Envelope section”).

      Key
      D   Turn the Kbd knob to set the keyboard tracking amount.
          At 0% the filter cutoff frequency is static and doesn’t track the keyboard at all.
          At 100% the filter cutoff frequency tracks the keyboard 1 semitone per note.

      LFO
      D   Turn the LFO knob to set the frequency modulation amount from the current settings of the LFO (see “The LFO
          section”).

      The Amplifier section

      The Amplifier section contains a standard ADSR envelope, which controls the amplitude of the audio signal.
      The picture below shows the various stages of the ADSR envelope:

            Level

      Volume
       (level)
                                               Sustain
                                               (level)
                                                                         Time
                            Attack   Decay                 Release
                            (time)   (time)                 (time)

                 Key Down                                 Key Up

      The ADSR envelope stages.

      A(ttack)
      When you play a note on your keyboard, the envelope is triggered. This means it starts rising from zero to max level.
      How long this should take, depends on the Attack setting. If the Attack is set to “0”, maximum level is reached in-
      stantly. If the Attack value is raised, it will take longer time before the maximum level is reached.

      D(ecay)
      After maximum level has been reached, the level starts to drop. How long this should take is governed by the Decay
      parameter.

      If you want to emulate the volume envelope of a note played on a piano for example, the Attack should be set to “0”,
      the Decay parameter should be set to a medium value and the Sustain level should be set to “0”, so that the volume
      gradually decreases down to silence, even if you keep holding the key down. Should you want the decay to drop to
      some other value than zero, you raise the Sustain parameter.

      S(ustain)
      The Sustain parameter determines the level the envelope should rest at, after the Decay stage. If you set Sustain to
      full level, the Decay setting is of no importance since the volume of the sound is never lowered.
      If you want to emulate the volume envelope of an organ, you theoretically only really need to use the Sustain param-
      eter set to full level, as a basic organ volume envelope instantly goes to the maximum level (Attack “0”) and stays
      there (Decay “0”), until the key is released and the sound instantly stops (Release “0”).
      But often a combination of Decay and Sustain is used to generate envelopes that rise up to max level, then gradually
      decreases to finally land to rest on a level somewhere in-between zero and maximum level. Note that Sustain
      represents a level, whereas the other envelope parameters represent times.

      R(elease)
      The Release parameter works just like the Decay parameter, except it determines the time it takes for the volume to
      drop back to zero after you release the key.

      Vel
      D   Turn up the Vel knob if you want the maximum level to be controlled from Keyboard Velocity.
          The harder you play, the louder the maximum volume.

      Chorus

      This is a stereo Chorus effect, which can be used for generating a fatter and wider sound.

      Amount
      D   Set the Dry/Wet amount of the chorus effect.
          Set to 0% for a completely dry (unprocessed) signal.

      Rate
      D   Set the rate/speed of the chorus modulation.

      Spread
      D   Set the stereo width of the chorus effect.
          Set to 0% for a if you want the signal to be in mono.

      Delay

      This is a stereo delay, which generates delayed copies of the original signal.

      Amount
      D   Use this parameter to adjust the send level to the Delay effect.
          Set to 0% for a completely dry (unprocessed) signal.

      Time
      The delay time is synced to the main sequencer tempo.
      D   Set the sync division to the main sequencer tempo with the Time knob.
          Range: 1/16, 1/8T, 1/8, 2/8T, 3/16, 1/4, 5/16, 4/8T, 7/16 and 2/4.

      Feedback
      D   Set the number of delay repeats.

      Ping Pong
      D   Activate Ping Pong to have the delay repeats alternate between left and right in the stereo panorama.

      The LFO section

      An LFO (Low Frequency Oscillator) is used for generating cyclic modulation. A typical example is to have an LFO
      modulate the pitch of a signal to produce vibrato, but there are also other applications for LFOs. The LFO section fea-
      tures an LFO which can be set to control Oscillator pitch (see “LFO”) and/or Filter frequency (see “LFO”).

      Rate
      D   Set the LFO rate/speed.
          Range: 0.06-94.0 Hz

      Shape
      D   Turn the Shape knob to select one of three LFO wave shapes.
          The wave shapes are: Sine, Triangle and Square.

      The Envelope section

      The Envelope section features a standard ADSR envelope, which can be used for controlling Oscillator Frequency
      Modulation (see “FM Env”) and/or Filter Frequency (see “Env”).
      The various envelope stages work exactly like those of the Amplifier, see “The Amplifier section”.

            Level

      Volume
       (level)
                                              Sustain
                                              (level)
                                                                      Time
                            Attack   Decay              Release
                            (time)   (time)              (time)

                 Key Down                               Key Up

      The ADSR envelope stages.

      A(ttack)
      D   Set the time it should take to reach from zero to maximum level.

      D(ecay)
      D   Set the time it should take to go from maximum level to the Sustain level (see below).

      S(ustain)
      D   Set the level the envelope should rest at, after the Decay stage (see above).

      R(elease)
      D   Set the time it should take to go from the Sustain level back to zero, after you have released the note.

      Vel
      D   Turn up the Vel knob if you want the maximum level to be controlled from Keyboard Velocity.
          The harder you play, the higher the maximum level.

      Connections

      !   Remember that CV connections are NOT stored in the Monotone patches! If you want to store CV connections
          between devices, put them in a Combinator device and save the Combi patch.


=== END OF PART ===
