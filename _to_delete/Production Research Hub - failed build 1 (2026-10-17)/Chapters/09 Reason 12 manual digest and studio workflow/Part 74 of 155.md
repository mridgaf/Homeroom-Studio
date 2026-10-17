# Chapter 09: Reason 12 manual digest and studio workflow
## Part 74 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 65 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 75 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 65 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Velo
      D   If you want the Gain level to be controlled from keyboard velocity, turn up the Velo knob.

      The Envelopes section

      The Envelopes section features four separate polyphonic (one per voice) general purpose envelope generators, that
      can be assigned to control selectable parameter(s) in the Modulation Bus section.
      The Envelopes are extremely flexible, and you can draw your own custom modulation shapes by clicking and drawing
      in the display area. There are also a number of preset shapes that you can use as starting points (or use as is). If you
      use Loop mode, you could turn the envelope into a kind of LFO.
      See “The Modulation Bus section” for details on how to assign the Envelopes to the desired destination(s).

      Envelope 1, 2, 3 and 4
      D   Click one of the Envelope 1, 2, 3 or 4 buttons to select which envelope to edit:

      Preset
      1. Click the Preset button to bring up a palette of envelope preset curves:

      2. Click the desired envelope preset curve to place it on the display.
          Let’s select a standard ADSR style of envelope curve:

      Adding a Sustain stage
      D   Click the Sustain button to add a sustain stage to the envelope:

          The vertical red marker that appears indicates at what level (and where) the envelope will stay sustained until you
          release the key.
      D   Drag the sustain marker sideways to move the sustain stage to the desired position:

      D   To remove the sustain stage, click the Sustain button.

      Adding and removing envelope points
      D   Double click, or hold down [Ctrl](win) or [Cmd](Mac) and click in the envelope display to add points to the
          envelope curve:

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
      In the Edit Y-Pos mode, you can also draw “free form” curves:
      D   To continuously add new consecutive points, hold down [Ctrl](win) or [Cmd](Mac) and drag in the envelope
          display:

      D   To erase points, hold down [Shift] and [Ctrl](win) or [Cmd](Mac) and drag in the envelope display.

      Using the Envelope 3 and Envelope 4 curves as Sound Engine waveforms
      As a special feature you can use the Envelope 3 and Envelope 4 curves as waveforms for the Sound Engines:
      1. Select Envelope 3 and create/modify a curve in the envelope display:

      2. Select Envelope 4 and create/modify another curve:

      3. In the Waveform selector for a Sound Engine, select the “Envelope 3-4” waveform:

      4. Turn the Shape knob to crossfade between the curves/waveforms of Envelopes 3 and 4:

      Using the Envelope 4 curve as a Spectral Filter curve
      Another special feature is that you could use the Envelope 4 curve as a filter curve in the Spectral Filter:
      1. Select Envelope 4 and create/modify a curve in the envelope display:

      2. In the Filter selector in the Spectral Filter section, select “Envelope 4”:

      3. Turn the Freq knob to change the curve’s “cutoff” frequency and the Reso knob to change the curve’s “reso-
         nance”.
          At Reso=0% the curve is completely flat (no gain or attenuation) and at Reso=100% the resonance corresponds
          exactly to the Envelope 4 curve.

      The LFO section

      An LFO (Low Frequency Oscillator) is used for generating cyclic modulation. A typical example is to have an LFO
      modulate the pitch of a signal to produce vibrato, but there are countless other applications for LFOs.
      The LFO section features three separate general purpose LFOs, that can be assigned to control selectable parame-
      ter(s) in the Modulation Bus section, see “The Modulation Bus section”.
      1. Select which of the three LFOs you want to edit by clicking one of the LFO 1, LFO 2 and LFO 3 buttons.
      2. Select an LFO waveform by clicking the spin controls to the right of the waveform display, or by click-holding
         in the display and dragging up or down.
          Besides the standard waveforms (sine, triangle, pulse, etc.) there are random, slope and stepped waveforms. The
          shape of the waveforms are shown in the display.
      3. Set the LFO frequency with the Rate knob.
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
      D   To define the order of the effects in the serial chain, click and hold on the desired Effect button and drag side-
          ways to the desired position:

          Moving the Reverb effect to another position in the effects chain.
          You can reorder the effects at any time.

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

      EQ

      The EQ effect is a single band parametric equalizer with adjustable Q-value and Gain.
      • Freq
          Sets the center frequency of the EQ band.
      • Q
          Sets the bandwidth of the EQ band, from wide to narrow.
      • Gain
          Sets the gain/attenuation of the EQ band, from -18dB to +18dB.

      The Modulation Bus section

      The Modulation Bus section is used for routing a modulation Source to one or two modulation Destinations each.
      This creates a very flexible routing system that complements the “pre-wired” routing in Europa.
      The Modulation Bus section in Europa is derived from the one in the Reason Thor Polysonic Synthesizer device, so if
      you are familiar with Thor, you will quickly find your way around in Europa’s modulation bus.
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

      | Parameter                           | Description
          MW Latched                         This allows you to modulate parameters based on the current Mod Wheel value at a given Note On.
          Pitch Wheel                        This allows you to modulate parameters from the Pitch Bend control.
          Breath                             This allows you to modulate parameters from the Breath performance controller
          Expression                         This allows you to modulate parameters from the Expression performance controller
          Aftertouch                         This allows you to modulate parameters from Keyboard Aftertouch (channel aftertouch)
          Sustain                            This allows you to modulate parameters from a connected sustain pedal. Note that continuous sustain
                                             data (0-127) is supported - not just on/off.
          Key                                This is keyboard tracking. If a positive Amount value is used and the destination is filter frequency, the
                                             filter frequency will track the keyboard, i.e. increase with higher notes.
          Random                             This sends out a random value each time a new note is played.
          Key In Octave                      This allows you to modulate parameters based on 12 separate note values (within each octave).
          Noise                              This allows you to modulate parameters from white noise.
          Polyphony                          This allows you to modulate parameters based on the number of playing voices at a given time.
          Last Velocity                      This applies modulation according to the latest Keyboard Velocity value (how hard or soft you hit the
                                             latest MIDI keyboard key).
          CV Input 1/2/3/4                   This takes the current value on the CV 1/CV 2/CV 3/CV 4 inputs on the rear panel and sends to the
                                             desired destination.
          CV Input 1/2/3/4 Latched           This allows you to modulate parameters based on the current CV 1/CV 2/CV 3/CV 4 value at a given
                                             Note On.

      Modulation Bus Source parameters.
      2. Set the Amount for the first Destination by turning the corresponding Amount knob, or by clicking and drag-
         ging vertically in the corresponding Amount box.
      !     Note that the Amount range is +/-100. This means that the Amount value can exceed the modulated parame-
            ter’s range. When this happens, the modulated parameter simply stays at its extreme value until the Amount
            value gets within the parameter’s range again.
      3. Select the first Destination parameter by click-holding the red arrow symbol to the right of the corresponding
         Destination box.
      4. While click-holding, drag to the desired destination parameter on the panel:

            Assigning LFO 1 Rate as a Destination for Envelope 1.
            As you hover over a valid destination control on the panel, the parameter name is automatically displayed in the
            Destination box in the Modulation Bus.
      5. To assign the currently selected Destination control, release the mouse button.
      D     Alternatively, click the desired Destination box and select the Destination parameter from the list.

      The following parameters can be used as modulation Destinations:

      | Parameter                        | Description
      Engine: Pitch                      This affects the (full range) pitch of the Oscillator.
      Engine: Shape                      This affects the Shape parameter in the Oscillator section.
      Engine: Mod 1 Amount               This affects the Modifier 1 Amount parameter in the Sound Engine.
      Engine: Mod 2 Amount               This affects the Modifier 2 Amount parameter in the Sound Engine.
      Engine: Filter Freq                This affects the Spectral Filter Frequency parameter in the Sound Engine.
      Engine: Filter Res                 This affects the Spectral Filter Resonance parameter in the Sound Engine.
      Engine: Harmonics Pos              This affects the Harmonics Pos parameter in the Sound Engine.
      Engine: Harmonics Amount           This affects the Harmonics Amount parameter in the Sound Engine.
      Engine: Unison Count               This affects the Unison Count parameter in the Sound Engine.
      Engine: Unison Detune              This affects the Unison Detune parameter in the Sound Engine.
      Engine: Unison Blend               This affects the Unison Blend parameter in the Sound Engine.
      Engine: Unison Spread              This affects the Unison Spread parameter in the Sound Engine.
      Mixer: Level                       This affects the Sound Engine Level in the Mixer section.
      Mixer: Pan                         This affects the Sound Engine Pan in the Mixer section
      Filter: Drive                      This affects the Drive parameter in the Filter section.
      Filter: Freq                       This affects the Frequency parameter in the Filter section.
      Filter: Reso                       This affects the Resonance parameter in the Filter section.
      Amplifier: Gain                    This affects the Gain parameter of the Amplifier section.
      Amplifier: Pan                     This affects the Pan parameter of the Amplifier section.
      Amp Envelope: Attack               This affects the Attack time of the Envelope in the Amplifier section.
      Amp Envelope: Decay                This affects the Decay time of the Envelope in the Amplifier section.
      Amp Envelope: Sustain              This affects the Sustain level of the Envelope in the Amplifier section.
      Amp Envelope: Release              This affects the Release time of the Envelope in the Amplifier section.
      LFOs: Delay                        This affects the LFO Delay parameters.
      LFOs: LFO Rate                     This affects the LFO Rate parameters.
      Envelopes: Env Rate                This affects the Envelope Rate parameters.
      Portamento                         This affects the Portamento Time parameter.
      CV Outputs: CV1/2/3/4 Out          This sends out the source modulation value(s) on the CV1/2/3/4 Output on the rear panel.
      Reverb: Decay                      This affects the Decay parameter in the Reverb effect.
      Reverb: Amount                     This affects the Amount parameter in the Reverb effect.
      Delay: Time                        This affects the Time parameter in the Delay effect.
      Delay: Feedback                    This affects the FB parameter in the Delay effect.
      Delay: Amount                      This affects the Amount parameter in the Delay effect.
      Delay: Pan                         This affects the Pan parameter in the Delay effect.
      Dist: Drive                        This affects the Drive parameter in the Dist effect.
      Dist: Tone                         This affects the Tone parameter in the Dist effect.
      Dist: Amount                       This affects the Amount parameter in the Dist effect.
      Compressor: Release                This affects the Release parameter in the Compressor effect.
      Compressor: Ratio                  This affects the Ratio parameter in the Compressor effect.
      Chorus/Flanger/Phaser: Frequency   This affects the center frequency of the Chorus/Flanger/Phaser effects.
      Chorus/Flanger/Phaser: Amount      This affects the Amount parameter of the Chorus/Flanger/Phaser effects.
      Par EQ: Frequency                  This affects the Freq parameter in the EQ effect.
      Par EQ: Gain                       This affects the Gain parameter in the EQ effect.

      Modulation Bus Destination parameters.

      6. Set the Amount for the second Destination (if desired) by turning the corresponding Amount knob, or by click-
         ing and dragging vertically in the Amount box for the second destination.
      7. If desired, select a second Destination parameter by click-holding the blue arrow symbol to the right of the
         corresponding Destination box, and dragging to the desired control on the panel.
      8. If desired, click the Scale box and select a Scale parameter.
          The available Scale parameters are the same as the Source parameters, see “Modulation Bus Source parame-
          ters.”.
      9. Turn the Scale Amount knob, or click the Amount box to the left of the Scale box and move the mouse pointer
         up or down to set a Scale Amount value.
          Both positive and negative Scale Amount values can be set (+/- 100%). If you, for example, are using the Mod
          Wheel as Scale parameter and don’t want any modulation when the Mod Wheel is set to zero, set the Scale
          Amount parameter to 100%. Then, there will be no effect when the Mod wheel is set to zero, and full modulation
          when the Mod Wheel is all the way up.
      • How much modulation will be applied when the Scale parameter is set to maximum is governed by the to Des-
        tination Amount parameter(s).
      • How much the Scale parameter controls the modulation is set with the Scale Amount parameter.
      D   To clear an assigned Source, Destination or Scale parameter, hold down [Ctrl](Win) or [Cmd](Mac) and click
          the Source/Destination/Scale box. Alternatively, click the Source/Destination/Scale box and select “Off” from
          the list.
      D   To reset an Amount value to 0, hold down [Ctrl](Win) or [Cmd](Mac) and click the desired Amount box or knob.
      D   To clear an entire modulation assignment (a whole row), click the circular X button to the right of the corre-
          sponding Scale box.

      Connections

      !   Remember that CV connections are NOT stored in the Europa patches! If you want to store CV connections
          between devices, put them in a Combinator device and save the Combi patch.

      Sequencer Control inputs
      The Sequencer Control CV and Gate inputs allow you to play Europa from another CV/Gate device (typically a Matrix
      or an RPG-8). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note on/
      off along with velocity. There are also inputs for modulating the Pitch Bend and Mod Wheel parameters.

      CV Modulation inputs and outputs
      These assignable control voltage (CV) inputs and outputs can be used for modulation of and from assigned Source
      and Destination parameters in the Modulation Bus section, see “The Modulation Bus section”.

      Audio Output
      These are the main audio outputs. When you create a new Europa device, these outputs are auto-routed to the first
      available Mix Channel in the main mixer. If there is no Mix Channel available, a new one will be automatically created.


=== END OF PART ===
