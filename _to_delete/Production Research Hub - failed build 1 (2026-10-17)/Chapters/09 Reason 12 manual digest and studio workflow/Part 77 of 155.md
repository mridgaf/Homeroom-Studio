# Chapter 09: Reason 12 manual digest and studio workflow
## Part 77 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 68 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 78 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 68 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Oct
      D   Turn the OCT knob to change the pitch in octave steps.
          Range: 5 octaves.

      Waveform and Mod
      D   Select the desired waveform by dragging up/down in the waveform display, or by clicking the up/down but-
          tons.
          The waveforms are:
      • Sine
          A pure sinewave at Mod=0%, gradually transformed towards a sawtooth type signal at Mod=100%.
      • Triangle
          A triangle wave at Mod=0%, gradually transformed towards a sawtooth type signal at Mod=100%.
      • Sawtooth
          A lowpass-filtered sawtooth wave at Mod=0%, gradually transformed to a pure sawtooth signal at Mod=100%.
      • Square/Pulse
          A 50% duty cycle square wave at Mod=0%, gradually pulsewidth-modulated to a 0% duty cycle pulse wave
          (silence) at Mod=100%.
      q   Modulate the Mod parameter from an LFO (using the Modulation Bus) to achieve PWM.
      • Noise
          A level-compensated lowpass-filtered noise at Mod=0%, gradually transformed to white noise at Mod=100%.
      • Band Noise
          A noise-modulated sinewave. The Mod knob controls noise bandwidth. At Mod=100%, the oscillator produces
          pure noise. Turning the knob counter-clockwise towards 0% gradually narrows the noise bandwidth until a slightly
          modulated sinewave is produced.

      The Filter section

      The signals from the Playback Algorithms section and the Oscillator section can be individually mixed and routed
      through the Filter section. The Filter section features four different filter types.

      Routing buttons
      D   Click the red buttons with a triangle pointing to the right, to route the desired signal to the Filter section.
          To bypass the signals from the Filter section, click the buttons with the triangle pointing upwards or downwards.

      Filter type
      D   Click the Filter type selector to choose any of the following filter types:
      • HP 12dB
          A highpass filter with a 12dB/octave slope.
      • BP 12dB
          A bandpass filter with 12dB/octave slopes.
      • LP 12dB
          A lowpass filter with a 12dB/octave slope.
      • LP Ladder 24dB
          A ladder-type lowpass filter with a 24dB/octave slope.

      Freq
      D   Set the cutoff frequency (for the HP and LP filter types) or the center frequency (for the BP filter type).

      Reso
      D   Set the resonance amount.

      Env 2
      D   Set the cutoff/center frequency modulation amount from the Envelope 2.
          Since this is a “hardwired” connection from Envelope 2 you don’t need to use the Modulation Bus for envelope
          modulating the cutoff/center frequency.

      Vel
      D   If you want the Envelope 2 amount to be controlled from keyboard velocity, turn up the Vel knob.

      Kbd
      D   Set how much you want the filter cutoff/center frequency to track the keyboard.
          At 0%, the filter frequency is static regardless where on the keyboard you play. At 100% the filter tracks the key-
          board 1:1, i.e. one semitone per note.

      The Amplifier section

      The Amplifier section contains a standard ADSR envelope which controls the amplitude of the signals from the Play-
      back Algorithms and Oscillator sections equally. The picture below shows the various stages of the ADSR envelope:

           Level

       Gain
      (level)
                                             Sustain
                                             (level)
                                                                       Time
                           Attack   Decay                Release
                           (time)   (time)                (time)

                Key Down                                Key Up

      The ADSR envelope stages.

      A(ttack)
      When you play a note on your keyboard, the envelope is triggered. This means it starts rising from zero to the value
      set with the Gain knob (see below). How long this should take, depends on the Attack setting. If the Attack is set to
      “0”, the Gain level is reached instantly. If the Attack value is raised, it will take longer time before the Gain level is
      reached.

      D(ecay)
      After the Gain level has been reached, the level starts to drop. How long this should take is governed by the Decay
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

      But often a combination of Decay and Sustain is used to generate envelopes that rise up to the Gain level, then grad-
      ually decreases to finally land to rest on a level somewhere in-between zero and the Gain level. Note that Sustain rep-
      resents a level, whereas the other envelope parameters represent times.

      R(elease)
      The Release parameter works just like the Decay parameter, except it determines the time it takes for the volume to
      drop back to zero after you release the key.

      Gain
      D   Set the desired maximum level for the Amplifier with the Gain knob.
          This is the maximum level the envelope will reach after the Attack stage is completed (see above).
      q   If you want to create a tremolo effect, assign “Gain” as Destination and an LFO as Source in the Modulation
          Bus section, see “The Modulation Bus section”.

      Vel
      D   If you want the Gain level to be controlled from keyboard velocity, turn up the Vel knob.

      Pan
      D   Set the panning of the output signal from the Amplifier in the stereo panorama.
      q   Since Pan works individually per voice, you can assign e.g. Keyboard Velocity or an Envelope in the Modula-
          tion Bus to control the Pan effect, see “The Modulation Bus section”.

      The Envelopes section

      The Envelopes section features four separate polyphonic (one per voice) general purpose envelope generators, that
      can be assigned to control selectable parameter(s) in the Modulation Bus section. The first two envelopes (Envelope
      1 and Envelope 2) are also hardwired to the Motion and Filter Frequency destinations respectively.
      The Envelopes are extremely flexible, and you can draw your own custom modulation shapes by clicking and drawing
      in the display area. There are also a number of preset shapes that you can use as starting points (or use as is). If you
      use Loop mode, you could turn the envelope into a kind of LFO.
      See “The Modulation Bus section” for details on how to assign the Envelopes to the desired destination(s).

      Envelope 1, 2, 3 and 4
      D   Click one of the Envelope 1, 2, 3 or 4 buttons to select which envelope to edit:

          Envelope 1 and Envelope 2 are also hardwired to the Motion and Filter Frequency destinations respectively.

      Preset
      1. Click the Preset button to bring up a palette of envelope preset curves:

      2. Click the desired envelope preset curve to place it on the display.
          Let’s select a standard ADSR style of envelope curve:

      Adding a Sustain stage
      D   Click the Sustain button to add a sustain stage to the envelope:

          The vertical blue marker that appears indicates where the envelope will stay sustained until you release the key.
      D   Drag the sustain marker sideways to move the sustain stage to the desired position:

      D   To remove the sustain stage, click the Sustain button.

      Adding and removing envelope points
      D   Double click, or hold down [Ctrl](win) or [Cmd](Mac) and click, in the envelope display to add points to the en-
          velope curve:

      D   To remove a point, double click, or hold down [Ctrl](win) or [Cmd](Mac) and click, on an existing point on the
          envelope curve.

      Changing the envelope curve shape
      D   Click a line segment (between two points) and drag up/down to change the curve shape:

      Looping the envelope
      D   Click the Loop button to turn the envelope into a kind of LFO.
          If there was previously a sustain stage in the envelope, this will automatically be disabled when you click the Loop
          button.

          Here we have edited a stepped curve from the Presets. We have also enabled Beat Sync and set the length/rate
          to 4/4. This means that each step in the curve now represents an 1/8th note.
      • Key Trig means the envelope restarts when you play a note.
      • You can choose whether the envelope should send out a bipolar value or unipolar one (0-100%).
      • If Global is on, the envelope will be common for all voices.
      Another useful application for looped envelopes is to sync the sample playback to the Reason sequencer when using
      the Envelope 1 Motion mode (see “Envelope 1”):
      1. Select Envelope 1 (since it is hardwired to the sample playback Motion parameter).
      2. Select the “Ramp Up” Preset, enable Loop and set the Beat Sync to the desired value:

          Playing back Reason’s sequencer now plays back the sample synced to the sequencer Tempo.

      Editing levels only
      D   To restrict the editing to levels only, without affecting the time positions, click the Edit Y-Pos button:

          In this mode you cannot change the time positions of the envelope points, only their levels (height). This is extra
          useful with a stepped Preset curve, because dragging up or down will change the value of an entire segment, turn-
          ing the Envelope into a pseudo-sequencer.
      !   To be able to adjust the level of a segment, the two points on either side of the segment have to be on the ex-
          act same time positions. Otherwise, only the closest point will be changed. Also, any inclining/declining seg-
          ment will automatically turn horizontal when edited:

          Adjusting the level of a segment.

      Creating “free form” envelope curves
      As a special feature in the Edit Y-Pos mode, you can also draw “free form” curves:
      D   To continuously add new consecutive points, hold down [Ctrl](win) or [Cmd](Mac) and drag in the envelope
          display:

      D   To erase points, hold down [Shift] and [Ctrl](win) or [Cmd](Mac) and drag in the envelope display.

      The LFO section

      An LFO (Low Frequency Oscillator) is used for generating cyclic modulation. A typical example is to have an LFO
      modulate the pitch of a signal to produce vibrato, but there are countless other applications for LFOs.
      The LFO section features three separate general purpose LFOs, that can be assigned to control selectable parame-
      ter(s) in the Modulation Bus section.
      D   Select which of the three LFOs you want to edit by clicking one of the LFO 1, LFO 2 and LFO 3 buttons.
      D   Select an LFO waveform by clicking the spin controls to the right of the waveform display, or by click-holding
          in the display and dragging up or down.
          Besides the standard waveforms (sine, triangle, pulse, etc.) there are random, slope and stepped waveforms. The
          shape of the waveforms are shown in the display.
      D   Set the LFO frequency with the Rate knob.
      D   Click the Beat Sync button to sync the LFO to the main sequencer Tempo in Reason.
          The Rate parameter now controls the time divisions.
      D   Click the Key Sync button to restart the LFO at every new Note On.
      D   Click the Global button to make the LFO common for all voices (monophonic).
      D   Turn the Delay knob to introduce a delay before the LFO modulation kicks in after a note is played.
          Turn clockwise for longer delay times.

      The Effects section

      The Effects section features six different effect modules that can be freely reordered by dragging & dropping. Most
      of the effect parameters are also available as destinations in the Modulation Bus, see “The Modulation Bus section”.
      At the top of the Effects section are six Effect buttons. Click any of these to bring up the control panel for the corre-
      sponding effect. Below the Effect buttons are the On/Off buttons for the individual effects. Click these to activate the
      effects.

      Reordering the effects
      D   To define the order of the effects in the serial connection, click and hold on the desired Effect button and drag
          to the desired position:

          Moving the Chorus effect to another position in the effects chain.
          You can reorder the effects at any time.

      Phaser/Flanger/Chorus

      This is a stereo Phaser/Flanger/Chorus.
      D   Select effect type with the Phaser/Flanger/Chorus switch.
          The selected effect type is displayed on the Effect button.
      • Depth
          Sets the depth of the selected effect. To get a static sound, set Depth to zero.
      • Rate
          Sets the rate/speed of the modulation.
      • Spread
          Sets the stereo width of the effect.
      • Amount
          Sets the Dry/Wet amount of the effect.
      q   It’s also possible to modulate the start/center frequency of the Phaser/Flanger/Chorus using the “Chorus/
          Flanger/Phaser > Frequency” destination in the Modulation Bus, see “The Modulation Bus section”.

      Distortion

      The Distortion effect features six different types of distortion.
      D   Select distortion type with the switch.
          “Dist” produces a dense, rich analog type of distortion.
          “Scream” produces a less bright type of distortion.
          “Tube” emulates a tube type of distortion.
          “Sine” is a sine shaping distortion.
          “S/H” gives the effect of sample rate reduction.
          “Ring” is a ring modulator effect.
      • Drive
          Sets the overdrive/feedback level of the selected distortion.
      • Tone
          This is a lowpass filter and sets the tone of the selected distortion.
      • Amount
          Sets the Dry/Wet amount of the distortion.

      EQ

      The EQ effect is a single band parametric equalizer with adjustable Q-value and Gain.
      • Freq
          Sets the center frequency of the EQ band.
      • Q
          Sets the bandwidth of the EQ band, from wide to narrow.
      • Gain
          Sets the gain/attenuation of the EQ band, from -18dB to +18dB.

      Delay

      This is a stereo delay, routed as a send effect.
      • Sync
          Activate Sync to sync the delay time to the main sequencer Tempo.
      • Time
          This sets the time between the delay repeats. If Sync is active (see above), the Time parameter now controls the
          time divisions.
      • Ping Pong
          Activate Ping Pong to have the delay repeats alternating between left and right in the stereo panorama. The effect
          is also dependent on the Pan parameter (see below).
      • Pan
          Sets the panning of the delay repeats in the stereo panorama. If Ping Pong is active (see above) the Pan knob
          controls the panning of the initial delay repeat as well as the total stereo spread of the remaining repeats.
      • FB
          The FB (feedback) parameter determines the number of delay repeats.
      • Amount
          Use this parameter to adjust the send level to the Delay effect.
      q   If you play a note, have a long delay feedback and turn down Amount, the echoes will continue. This allows for
          automated “triggered delay” fx.

      Compressor

      This is a stereo compressor.
      • Attack
        This governs how quickly the compressor will apply its effect when signals rise above the set threshold. If you raise
        this value, the response will be slower, allowing more of the signal to pass through the compressor unaffected.
        Typically, this is used for preserving the attacks of the sounds.
      • Release
        When the signal level drops below the set threshold, this determines how long it takes before the compressor lets
        the sound through unaffected. Set this to short values for intense, “pumping” compressor effects, or to longer val-
        ues for a smoother change of the dynamics.
      • Thres
        This is the threshold level above which the compression sets in. Signals with levels above the threshold will be af-
        fected, signals below it will not. In practice, this means that the lower the Threshold setting, the more the compres-
        sion effect.
      • Ratio
        This specifies the amount of gain reduction applied to the signals above the set threshold.

      Reverb

      This is a stereo reverb, routed as a send effect.
      • Decay
        This governs the length of the reverb effect.
      • Size
        Sets the emulated room size, from small room to large hall. Middle position is the default room size.
        Lowering this parameter results in a closer and gradually more “canned” sound. Raising the parameter results in a
        more spacey sound, with longer pre-delay.
      • Damp
        Raising the Damp value cuts off the high frequencies of the reverb, thereby creating a smoother, warmer effect.
      • Amount
        Use this parameter to adjust the send level to the Reverb effect.
        If you play a note, have a long delay Decay time and turn down Amount, the reverberation will continue.

      The Modulation Bus section

      The Modulation Bus section is used for routing a modulation Source to one or two modulation Destinations each.
      This creates a very flexible routing system that complements the pre-wired routing in Grain.
      The Modulation Bus section in Grain is derived from the one in the Reason Thor Polysonic Synthesizer device, so if
      you are familiar with Thor, you will quickly find your way around in Grain’s modulation bus.
      There are eight “Source –> Destination 1 –> Destination 2 –> Scale” busses, of which the first four have pre-as-
      signed sources. However, these four pre-assigned sources can be easily changed if you like.
      A Source parameter can modulate two different Destination parameters per bus (with variable Amount settings).
      Each bus also has a Scale parameter that affects the relative modulation Amount for both Destinations.
      q   Note that it is possible to assign the same source parameter as Source in several busses. This allows you to
          control more than two Destination parameters from the same Source.

      1. Select the desired Source parameter by clicking in the corresponding Source box and selecting from the list.
      The following parameters can be used as modulation Sources:

      | Parameter                          | Description
      Velocity                             This applies modulation according to the Keyboard Velocity values (how hard or soft you strike the MIDI
                                           keyboard keys).
      LFOs (LFO 1, LFO 2 and LFO 3)        This allows you to modulate parameters from LFO 1, LFO 2 and LFO 3 respectively.
      Envelopes (Amp Envelope, Envelope 1, This allows you to modulate parameters from any of the Envelopes.
      Envelope 2, Envelope 3, Envelope 4, As a special feature you can also modulate parameters from the multiplied signal of Envelope 3 and
      Envelope 3 * Envelope 4, Envelope 3 * Envelope 4, as well as from the multiplied signal of Envelope 3 and LFO 3.
      LFO 3)
      Mod Wheel                            This allows you to modulate parameters from the Mod Wheel.
      MW Latched                           This allows you to modulate parameters based on the current Mod Wheel value at a given Note On.
      Pitch Wheel                          This allows you to modulate parameters from the Pitch Bend control.
      Breath                               This allows you to modulate parameters from the Breath performance controller
      Expression                           This allows you to modulate parameters from the Expression performance controller
      Aftertouch                           This allows you to modulate parameters from Keyboard Aftertouch (channel aftertouch)
      Sustain                              This allows you to modulate parameters from a connected sustain pedal. Note that continuous sustain
                                           data (0-127) is supported - not just on/off.
      Key                                  This is keyboard tracking. If a positive Amount value is used and the destination is filter frequency, the
                                           filter frequency will track the keyboard, i.e. increase with higher notes.
      Random                               This sends out a random value each time a new note is played.
      Key In Octave                        This allows you to modulate parameters based on 12 separate note values (within each octave).
      Noise                                This allows you to modulate parameters from white noise.
      Polyphony                            This allows you to modulate parameters based on the number of playing voices at a given time.
      Last Velocity                        This applies modulation according to the latest Keyboard Velocity value (how hard or soft you hit the
                                           latest MIDI keyboard key).
      Sample Pitch Curve                   As soon as you load a sample in Grain the pitches throughout the entire sample is automatically analyzed
                                           and saved as a “Pitch Curve”. This allows you to modulate parameters based on the analyzed pitch value
                                           at the Position marker’s current position in the original sample.


=== END OF PART ===
