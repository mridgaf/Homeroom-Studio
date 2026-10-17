# Chapter 09: Reason 12 manual digest and studio workflow
## Part 72 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 63 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 73 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 63 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 30: Europa Shapeshifting Synthesizer

Europa
Shapeshifting
Synthesizer

      Introduction

      The Europa Shapeshifting Synthesizer is the most advanced and sonically “wide” synthesizer in Reason. Despite
      being a very advanced synthesizer, it’s really easy to create great sounds from scratch. Just a few mouse clicks and
      knob twists in a Sound Engine section will generate truly impressive and inspiring sounds!
      The three powerful and flexible sound engines offer a unique combination of analog/wavetable/spectral/physical
      modeling/FM synthesis techniques. If you like, you could also draw your own waveforms and filter curves to design
      your own completely unique sounds. In addition to this you can also load your own sample into Europa and use as a
      wavetable and/or filter! Each sound engine also has its own Unison module for generating really wide multi-voice
      stereo chorus effects.
      The extensive Envelopes section and Modulation Bus section allow for very detailed and flexible modulation and con-
      trol. Europa also features a top-notch semi-modular multi-effect section so you could put that final touch on your
      sounds.
      Don’t forget to check out the Europa videos here!

      Panel overview
      The Europa front panel contains the following sections:

                               1         2
       3

        4                                    5                          6         7

        8          9                                                         10

                  11                                                    12

      The Europa front panel sections.
      • 1. MIDI Note On LED.
      • 2. Patch Selector (for browsing, loading and saving patches).
      • 3. Sound Engines section.
      • 4. User Wave and Mixer section.
      • 5. Filter section.
      • 6. Amplifier section.
      • 7. Global output controls.
      • 8. Global performance and “play” controls.
      • 9. Envelopes section.
      • 10. LFO section.
      • 11. Modulation Bus section.
      • 12. Effects section.

      Signal flow
      The picture below shows the basic signal flow in Europa:
                                                                 Engine III
                                                               Engine II
         Amt     Mod    Amt    Mod                           Engine I

                                      KBD      Mod     Vel                          Count Blend
         Modifier 1     Modifier 2
                                                                                                        Pan

                 Oscillator             Spectral Filter                Harmonics       Unison
                                                                                                       Level

         Pitch        KBD     Shape     Freq         Reso           Modify    Amt   Detune Width

                                                                                        KBD     Mod    Vel        Pan

                                                                                                                Amp
                                                                                              Filter                          Multi FX
                                                                                                                Envelope                      Out
                                                                                                                                         Volume

                                                                                                                                         : audio signal
                                                      Per Voice                        Drive Freq Reso         Gain     Vel              : control signal

      Europa signal flowchart.
      • The “hearts” of Europa are the three Sound Engines I, II and III.
      • First in each Sound Engine is an Oscillator, which generates the basic audio signal.
         The oscillators in Europa are extremely powerful and flexible. Besides all the basic “analog” waveforms, the oscil-
         lators can also generate a vast variety of wavetable waveforms, physical modeling signals and other types of
         unique signals - and also your own samples! The signals can also be continuously transformed into various shapes.
      • The Oscillator signal can be modified by the two Modifiers.
         The Modifiers feature a huge amount of algorithms that can modify the Oscillator signal in various ways.
      • The signal from the Oscillator is routed to the Spectral Filter.
         The Spectral Filter affects the partials of the signal. The algorithms could be various types of filters - or special
         purpose signal processors.
      • The signal from the Spectral Filter can then be routed to the Harmonics processor.
         The Harmonics processor modulates the harmonics in the signal, for example introducing ensemble or stretch ef-
         fects.
      • The signal from the Harmonics processor can then be routed to the Unison module.
         This module can generate various types of unison chorus effects, to make the sound really fat and wide.
      • The signals from the Sound Engines are then routed to the Mixer, where you can set the mix between the three
        Sound Engine output signals and also pan the signals individually.
      • The mixed signal is then routed to the Filter, Amp Envelope and then, via the Multi FX section, to the stereo
        outputs.
      • The remaining sections in Europa (Envelopes 1-4 and LFOs 1-3) can be freely assigned to modulate destina-
        tion parameters via the Modulation Bus section.

      Playing and using Europa
      Loading and saving patches

      Loading and saving patches is done in the same way as with any other internal Reason device, see “Loading patches”
      and “Saving patches” for details.

      Global output controls

      Master Volume
      This is the main stereo output volume control.

      Voices
      Here you set the desired maximum polyphony of your patch, from 1 to 16 voices. This control is mainly intended for
      deliberately restricting the polyphony of a sound. If you just want to play a patch polyphonically you can leave the
      Voices setting at 16 at all times. The DSP Load won’t increase with higher voice number settings - only if you play a
      lot of notes simultaneously.
      q   If you want monophonic playback you could use the “Retrig” and “Legato” modes instead of lowering the
          Voices parameter to 1.

      Global performance and “play” controls

      Key Mode
      Here you choose how Europa should respond to MIDI Note data:
      • Poly
          Select this if you want to play Europa polyphonically. The maximum number of voices is 16. The number of voices
          is set in the Voices control at the center right of the Europa panel, see “Voices”.
      • Retrig
          Select this if you want to play Europa in monophonic mode and always retrigger the envelopes as soon as you play
          a new note.
      • Legato
          The Mono Legato mode is also monophonic. However, if you play a new note without having released the previous
          one, the envelopes won’t start over.

      Porta
      Portamento makes note pitches glide from previous notes to new ones, at the time set with the Time knob. Porta-
      mento can be used in all Key modes (see above).
      • When On in Poly Key Mode (see above), the pitches will glide from any of the available voices.
          The results will be unpredictable since there is no way of controlling from which note(s) the glide(s) will com-
          mence. The effect is very nice, though.
      • When On in Retrig or Legato Key Mode (see above), the pitch will glide between consecutive notes.
      • In Auto mode, the pitch will glide between consecutive monophonic notes only when you play legato. If you
        have selected Poly Key Mode (see above), Auto will have no effect at all.
          If you release the previous key before hitting the new key, there will be no portamento effect.

      P.Range
      D   Set the desired Pitch Bend range for the “Pitch” wheel with the up/down buttons, or by click-holding on the
          display and dragging up/down.
          Range: +/-24 semitones (+/-2 octaves) in steps of +/-1 semitone.

      Pitch
      The Pitch bend wheel can be used for bending note pitches up and down. Europa also responds to Pitch Bend MIDI
      data from a connected MIDI master keyboard. You set the desired Pitch bend Range with the “P.Range” control
      above the Pitch bend wheel.

      Mod
      The Mod wheel can be used for controlling almost any parameter in Europa. Use the Mod wheel as a Source param-
      eter in any of the Modulation Source boxes in the different sections. Or use it as Source parameter in the Modulation
      Bus section and then route to the desired Destination parameter(s), see “The Modulation Bus section”.

      Panel reference
      Sound Engines On/Off and Edit Focus section

      Engine Select
      D   Click the On LED buttons to activate the corresponding Sound Engine.
      D   Click the I, II or III LED radio buttons to select the corresponding Sound Engine for editing.

      The Oscillator section

      Here is where you choose oscillator waveform and set the wave shape and pitch for the selected Sound Engine.

      On
      D   Click the red rectangular LED button to switch the selected Sound Engine on/off.

      Oct
      D   Set the pitch in octave steps.
          Range: 5 octaves.

      Semi
      D   Set the pitch in semitone steps.
          Range: 12 semitones (one octave).

      Tune
      D   Change the pitch in steps of 1 cent.
          Range: +/- 50 cents (down or up half a semitone).

      Kbd
      D   Set how much the pitch should track incoming MIDI Notes.
          Range: 0% (no tracking (constant pitch)) to 100% (1 semitone per note).

      Waveform display
      The interactive Waveform display shows the waveform shape in real-time.
      • Clicking and dragging vertically in the display changes the Shape parameter, see “Shape”.
      • Clicking and dragging horizontally in the display changes the Modifier 1 Amount parameter, see “Amount”.
      q   See “Recording display movements in the sequencer” for tips about automating display movements.

      Waveform selector
      D   Click the Waveform name box to bring up a menu of the available waveforms.
          The wave shapes are shown in the display above and are updated in real-time according to the current settings
          and modulations. A great way to understand how the sound actually “looks”.
          The waveforms are:
      • Basic Analog
          A pure sinewave at Shape=0%, gradually transformed via triangle and square towards a sawtooth wave at
          Shape=100%.
      • Square-Ramp
          A square wave at Shape=0%, gradually transformed towards a sawtooth wave at Shape=100%.
      • Saw-Triangle
          A negative ramp sawtooth wave at Shape=0%, gradually transformed via triangle towards a positive ramp saw-
          tooth wave at Shape=100%.
      • Pulse Width
          A 0% duty cycle pulse wave (silence) at Shape=0 gradually transformed via a 50% duty cycle square wave to-
          wards a 100% duty cycle pule wave (silence) at Shape=100%.
      q   Modulate the Shape parameter from an LFO to achieve PWM, see “Shape Modulation” below.
      • Game
          A lo-fi “early computer game” type of signal. Turn the Shape knob to change the overtone contents and the octave
          transposition.
      • Synced Sine
          A pure sinewave at Shape=0%. As the Shape is increased, the pitch of the synced sinewave oscillator is raised.
      • Formant Sweep
          A cosine window modulated by a sinewave. Turn the Shape knob to change the sinewave frequency and thus
          sweep through the generated formants.
      • Electro Mechanical
          This is a simulation of an electric piano. A soft/mellow tone at Shape=0% gradually transformed towards an
          agitated signal at Shape=100%, with natural sound at the 12 o’clock position (50%).
      • Vocal Cord
          A simulation of a vocal cord with a bit of noise modulation. Change the overtone content with the Shape knob.
      q   Try this together with the Vocal Formants algorithm in the Spectral Filter section to generate “vocal” sounds,
          see “Vocal Formant”.
      • Karplus-Strong
          A physical model of a “string”, generated by sending a short pulse through pitched delay lines. At Shape=0% there
          is no damping and at Shape=100% there is full damping, which results in just a short clicking sound.
      q   Try this together with the “Stretch” algorithm in the Harmonics section to create realistic metallic sounds.

      • Envelope 3-4
          This is a special mode where you can manually draw your waveforms in the Envelope 3 and Envelope 4 windows
          and then gradually crossfade between the drawn waveforms using the Shape knob. See “Using the Envelope 3
          and Envelope 4 curves as Sound Engine waveforms” for information on how to draw your own waveforms.
      • FM > FM Ratio (1:1, 1:2, 1:8, 2:1)
          These are frequency modulated sine waves with different frequency ratios between the carrier (C: ) and modulator
          ( :M) signals. Set the frequency modulation amount with the Shape knob.
      • FM > FM Feedback
          A pure sinewave signal at Shape=0% gradually fed back internally at an 1:1 ratio. The feedback signal is filtered
          before fed back to the carrier signal. If you modulate the Shape parameter from e.g. an LFO you will get a similar
          result as when using the FM FB Noise waveform without Shape modulation, see “Noise > FM FB Noise” below.
      • Noise > S/H Noise
          A sample & hold modulated noise. Change the sample & hold rate with the Shape knob. If you play high up on the
          keyboard at high Shape values, you get a kind of “pitched noise” sound.
      q   To get white noise, set Shape to max, set Oct to -1 and turn Kbd to 0.
      • Noise > Perlin Noise
          A pure sinewave signal modulated by low frequency noise. At Shape=0% the noise has its lowest frequency and
          at Shape=100% the noise frequency is higher (but still low-frequent). The character of the signal is similar to the
          Band Noise in the Thor synthesizer.
      • Noise > Bit Noise
          This generates a random lo-fi “digital” bit noise. At Shape=0% the signal is completely silent and with increasing
          Shape values the signal is modulated faster and in a wider frequency range.
      • Noise > FM FB Noise
          A pure sinewave signal at Shape=0% gradually fed back internally at an 1:1 ratio. The feedback signal unfiltered
          before fed back to the carrier signal which gives the signal a noisy character.
      q   To get a cleaner FM signal, use the FM Feedback waveform, see “FM > FM Feedback” above.
      • Noise > Freeze Noise
          This signal produces a range of noises, from tonal noise up to almost white noise, by amplitude modulating the sig-
          nal’s partials with noise.
      • Wave Tables >
          The Wave Tables sub-menu contains a selection of very useful wave tables. Each wave table features eight wave-
          forms that you could crossfade between with the Shape knob.
      • User Wave/User Wave Smooth
          The User Wave options let you use the external sample you have loaded in the User Wave section (see “The User
          Wave and Mixer section”). The oscillator then generates and plays back wavetables (grains) of that sample. The
          “User Wave Smooth” algorithm uses a crossfaded loop within each grain, which produces a smoother character to
          the sound. Set the playback position in the sample with the Shape knob. Modulate the Shape parameter, for exam-
          ple from a negative Envelope ramp, for continuous movement in the sample.

      Shape
      D   Turn the Shape knob to change the shape of the currently selected waveform.
          The wave shapes are shown in the display above and are updated in real-time according to the current Shape set-
          tings.

      Shape Modulation
      D   Click the Shape Modulation Source box to bring up a menu of the available modulation sources.
          The “Inverted” sub-menu contains inverted variations of all modulation sources.
      D   Set the modulation amount with the Shape Modulation Amount knob.

      D   Turn the Velo knob to control the Shape Modulation Amount from Keyboard Velocity.
      q   If you want other modulation sources or scaling options, use the Mod Bus, see “The Modulation Bus section”.

      Phase Sync
      D   Click the Phase Sync button to force the waveform cycle to always start at the same phase (0 degrees).
          When active, the sound character will be the same each time you play the same note. When inactive, the sound
          character will vary more or less each time you play the same note.

      The Modifiers section

      The two Modifiers can be used for modifying the currently selected waveform in various ways. The two Modifiers are
      identical in functionality and can be used alone or together (or not at all).

      Modifier On/Off
      D   Click the On/Off LED buttons to activate/deactivate the corresponding Modifier.

      Modifier selector
      D   Click the Modifier name box to bring up a menu of the available Modifier types.
          The available Modifier types are:
      • Faded Sync
          This is oscillator sync but with a crossfade at the sync positions. This makes the effect a little smoother (less
          bright) than with regular hard sync, see below.
      • Hard Sync
          Oscillator hard sync is when one oscillator restarts the period of another oscillator, so that they will have the same
          base frequency. If you change or modulate the frequency of the synced oscillator you get the characteristic sound
          associated with oscillator sync. Control the frequency of the synced oscillator (and thereby the overtone spectrum)
          with the Amount knob.
      • Invert
          This inverts the waveform phase at a variable position within the waveform cycle. Set the phase angle with the
          Amount knob.
      • Mirror
          This mirrors the waveform cycle (in the time line) at a variable position in the waveform cycle. Set the mirroring
          position in the waveform cycle with the Amount knob. At Amount=50% the waveform is completely symmetric.
      • DownSample
          This lets you quantize the waveform in time, i.e. reduce the sample rate. Set the sample rate reduction amount with
          the Amount knob.
      • Quantize
          This lets you truncate the signal’s bit depth, thus making it possible to achieve that noisy, characteristic “8-bit
          sound” for example. Set the bit-reduction amount with the Amount knob.

      • Phase Distort
        This distorts the waveform by modulating the start phase of the waveform cycle. This generally creates a brighter
        tone towards the extremes of the Amount range (0% and 100%). At Amount=50% the signal is unaffected.
      • Self Multiply
        This multiplies a copy of the waveform with the original waveform. Set the phase angle of the copied waveform
        with the Amount knob.
      • Noise Mod
        This modulates the waveform with low frequency noise. Perfect for adding e.g. “breath noise” to a signal. Set the
        noise modulation amount with the Amount knob.
      • Shaping > Wrap
        This amplifies the signal above the available headroom and then wraps the peaks down into the available head-
        room. This adds quite an aggressive distortion to the sound.
      • Shaping > Fold
        This amplifies the signal above the available headroom and then “mirrors” the peaks down into the available head-
        room. Fold is similar to the Wrap shaping but is generally less “aggressive”.
      • Shaping > Hard Clip
        This amplifies the signal above the available headroom and then clips the peaks that are above the headroom.
        Generally, a signal that is clipped to the maximum would result in a pulse/square shaped waveform.
      • Shaping > Soft Clip
        Soft clip is similar to hard clip described above, but has a smoother shape at the clipping points and thus generates
        less overtones.
      • Shaping > Sine Shape
        This generates sine shaping distortion to the signal.
      • Shaping > Glitch 1
        This distorts the waveform by introducing a short low-frequency noise glitch in the waveform cycle, but only in
        parts of the waveform that go from zero to positive level.
      • Shaping > Glitch 2
        This is similar to Glitch 1 described above, but introduces a more high-frequent noise glitch in the waveform cycle.
      • Harmonics > Octave
        This makes it possible to gradually crossfade between the original signal and a copy of the signal one octave
        above. Set the crossfade amount with the Amount knob.
      • Harmonics > Fifth
        This makes it possible to gradually crossfade between “one octave up” and “one octave+one fifth up”. As soon as
        you turn on the Fifth modifier you automatically raise the pitch by one octave. The reason for this is that this is
        done by multiplying frequencies, i.e. you crossfade between the double and triple of the original frequency. Set the
        crossfade amount with the Amount knob.
      • Harmonics > 16 Harmonics
        This makes it possible to gradually crossfade between the original signal and copies of the signal at the 16 first
        harmonics above the original frequency. Set the position in the harmonic spectrum with the Amount knob.
      • Harmonics > Fund. + 16 Harm.
        This is the same as “16 Harmonics” described above, except this always keeps the original signal mixed in with the
        selected harmonic.
      • Harmonics > All 16 Harm.
        This gradually adds copies of the original signal at the first 16 harmonics. Turning up the Amount knob will add on
        the harmonics one by one until all 16 harmonics are present in the signal.
      • Harmonics > Ring Harm.
        This multiplies the waveform with a sinewave signal to generate a ring modulator effect. Set the modulator fre-
        quency with the Amount knob.


=== END OF PART ===
