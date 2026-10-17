# Chapter 09: Reason 12 manual digest and studio workflow
## Part 78 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 69 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 79 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 69 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      | Parameter                            | Description
          Display Y Position                  This allows you to modulate parameters based on the mouse pointer’s Y position in the sample window.
                                              See “Automating sample playback parameters from the sequencer” for an example.
          Display Mouse Gate                  This allows you to modulate parameters based on the clicking/holding the mouse in the sample window.
                                              See “Automating sample playback parameters from the sequencer” for an example.
          CV Input 1/2/3/4                    This takes the current value on the CV 1/CV 2/CV 3/CV 4 inputs on the rear panel and sends to the
                                              desired destination.
          CV Input 1/2/3/4 Latched            This allows you to modulate parameters based on the current CV 1/CV 2/CV 3/CV 4 value at a given
                                              Note On.

      Modulation Bus Source parameters.
      2. Set the Amount for the first Destination by turning the corresponding Amount knob, or by clicking and drag-
         ging vertically in the corresponding Amount box.
      !      Note that the Amount range is +/-100. This means that the Amount value can exceed the modulated parame-
             ter’s range. When this happens, the modulated parameter simply stays at its extreme value until the Amount
             value gets within the parameter’s range again.
      3. Select the first Destination parameter by click-holding the grey arrow symbol to the right of the corresponding
         Destination box.
             The arrow symbol turns blue.
      4. While click-holding, drag to the desired destination parameter on the panel:

             Assigning LFO 1 Rate as a Destination for Envelope 1.
             As you hover over a valid destination control on the panel, the parameter name is automatically displayed in the
             Destination box in the Modulation Bus.
      5. To assign the currently selected Destination control, release the mouse button.
      !      Dragging to the Waveform Display (see “The Sample section”) will always assign the playback Position
             parameter. To assign the sample Start Position or End Position, select the parameter from the list (see below).
      D      Alternatively, click the desired Destination box and select the Destination parameter from the list.
      The following parameters can be used as modulation Destinations:

      | Parameter                             | Description
          Position                             This affects the sample “playhead” position in the original sample.
          Speed                                This affects the Speed control in the sample window.
          Jitter                               This affects the Jitter control in the sample window.
          Start Position                       This affects the Sample Start marker position in the original sample.
          End Position                         This affects the Sample End marker position in the original sample.
          Pitch                                This affects the pitch of the original sample.
          Octave                               This affects the Oct control in the Playback Algorithm section.
          Formant                              This affects the Formant Form control in the Playback Algorithm section (if applicable).

      | Parameter                        | Description
      Sample Level                       This affects the Sample Level control of the Playback Algorithm section.
      Grain: Length                      This affects the Grain Length parameter on the Grain Oscillator and Long Grains playback algorithms.
      Grain: Rate/Spacing                This affects the Grain Spacing parameter on the Grain Oscillator and the Rate parameter on the Long
                                         Grains playback algorithms.
      Grain: X-Fade                      This affects the X-Fade parameter on the Long Grains playback algorithm.
      Grain: Pan Spread                  This affects the Pan Spread parameter on the Grain Oscillator and Long Grains playback algorithms
      Grain: Pitch Jitter                This affects the Pitch Jitter parameter on the Grain Oscillator and Long Grains playback algorithms
      Spectral Grain: Harm Snap          This affects the Snap parameter on the Spectral Grains playback algorithm.
      Spectral Grain: Harm Filter        This affects the Filter parameter on the Spectral Grains playback algorithm.
      Spectral Grain: Curve Amount       This affects the Amount parameter on the Spectral Grains playback algorithm.
      Oscillator: Modulation             This affects the Mod parameter on the Oscillator.
      Oscillator: Octave                 This affects the Oct parameter on the Oscillator.
      Oscillator: Pitch                  This affects the (full range) pitch of the Oscillator.
      Oscillator: Level                  This affects the Osc Level parameter of the Oscillator section.
      Filter: Freq                       This affects the Frequency parameter in the Filter section.
      Filter: Reso                       This affects the Resonance parameter in the Filter section.
      Amplifier: Gain                    This affects the Gain parameter of the Amplifier section.
      Amplifier: Pan                     This affects the Pan parameter of the Amplifier section.
      Amp Envelope: Attack               This affects the Attack time of the Envelope in the Amplifier section.
      Amp Envelope: Decay                This affects the Decay time of the Envelope in the Amplifier section.
      Amp Envelope: Sustain              This affects the Sustain level of the Envelope in the Amplifier section.
      Amp Envelope: Release              This affects the Release time of the Envelope in the Amplifier section.
      LFO’s: LFO1/2/3 Delay              This affects the LFO1/2/3 Delay parameter.
      LFO’s: LFO1/2/3 Rate               This affects the LFO1/2/3 Rate parameter.
      Envelopes: Env1/2/3/4 Rate         This affects the Envelope 1/2/3/4 Rate parameter.
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
      Note Trig                          This is mainly intended for use with the Display > Mouse Gate or Display > Y-Position source parame-
                                         ters, e.g. with the Freeze motion mode, to trig/gate the sample without having to play the keyboard. This
                                         way you can play back the Root Key of the sample by just clicking/dragging in the Waveform display.

      Modulation Bus Destination parameters.

      6. Set the Amount for the second Destination (if desired) by turning the corresponding Amount knob, or by click-
         ing and dragging vertically in the Amount box for the second destination.
      7. If desired, select a second Destination parameter by click-holding the blue arrow symbol to the right of the cor-
         responding Destination box, and dragging to the desired control on the panel.
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

      Modulation example patches
      The factory patches for Grain features a folder named “Templates”. In this folder you will find a number of patches
      that show typical modulation examples, to make it easier to get the hang of how to create your own patches.

      Connections

      !   Remember that CV connections are NOT stored in the Grain patches! If you want to store CV connections
          between devices, put them in a Combinator device and save the Combi patch.

      Sequencer Control inputs
      The Sequencer Control CV and Gate inputs allow you to play Grain from another CV/Gate device (typically a Matrix
      or an RPG-8). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note on/
      off along with velocity. There are also inputs for modulating the Pitch Bend and Mod Wheel parameters.

      CV Modulation inputs and outputs
      These assignable control voltage (CV) inputs and outputs can be used for modulation of and from assigned Source
      and Destination parameters in the Modulation Bus section, see “The Modulation Bus section”.

      Audio Output
      These are the main audio outputs. When you create a new Grain device, these outputs are auto-routed to the first
      available Mix Channel in the main mixer. If there is no Mix Channel available, a new one will be automatically created.

      Tips and Tricks
      Automating sample playback parameters from the sequencer
      Besides the extensive modulation capabilities of the Modulation Bus, the sample playback parameters can also be
      automated in the Reason sequencer. For example, you could automate the Sample Start and/or Sample End markers
      in the Sample section to have the markers reposition in real-time during playback of the Reason sequencer. Below is
      a basic example of how you could automate various sample playback parameters:
      1. Record some notes on the Grain sequencer track in the Reason sequencer and then hit Stop twice.
      2. Hit Record again in the Reason sequencer and drag the Sample Start and Sample End markers during record-
         ing:

      3. Hit Stop in the sequencer twice when you are done recording.
        If you moved both the Sample Start marker and the Sample End marker you will now have four Parameter Auto-
        mation lanes with clips on them on the Grain sequencer track. A green Parameter Automation frame is also visible
        around the Sample section display:

        The first two Parameter Automation lanes - the Display Y lane and the Display Gate lane - always appear as soon
        as you have recorded any marker movements in the Sample section display.

      • The clip on the Display Y lane represents the vertical movements you made with the mouse during the record-
        ing.
          This automation doesn’t affect the sample playback in any way but can instead be used as a modulation source in
          the Modulation Bus, for modulating the desired destination parameter(s).
      • The clip on the Display Gate lane reflects when you clicked (and held) the mouse button during the recording.
          This automation doesn’t affect the sample playback either but can be used as a modulation source in the Modula-
          tion Bus, for modulating/gating the desired destination parameter(s).
      • The clips on the Position and End Pos lanes represent the movements of the Sample Start and Sample End
        markers respectively.
      D   If you like you could also record automation of the Sample Range Zoom and Scroll parameters by dragging the
          markers in the Sample Overview area:

          After recording the movements of the Sample Range markers, two new Parameter Automation lanes appear on
          the sequencer track:

      • The clip on the Scroll lane represents the movement of the leftmost Sample Range marker, and thus the move-
        ment of the entire sample range.
      • The clip on the Zoom lane represents the movement of the rightmost Sample Range marker, and thus the
        zooming (in or/and out) of the sample range.
      q   It’s also possible to automate the Motion, Speed, Jitter and Global Position parameters.
      q   Also, don’t forget to check out the modulation example patches, see “Modulation example patches”.

786   GRAIN SAMPLE MANIPULATOR


---

<a id="mimic-creative-sampler-32"></a>

=== END OF PART ===
