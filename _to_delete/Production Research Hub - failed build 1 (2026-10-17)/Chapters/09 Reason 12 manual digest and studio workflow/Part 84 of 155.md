# Chapter 09: Reason 12 manual digest and studio workflow
## Part 84 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 75 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 85 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 75 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      D   Lastly, there are two “Source –> Destination –> Scale 1 –> Scale 2” busses.
          This means that a modulation Amount can use two Scale parameters.
          An example: You have the Mod Envelope as Source and Oscillator Pitch as the Destination (Amount set whatever
          you like). As the first Scale parameter we use the Mod Wheel (Amount set to 100 so that no modulation is applied
          when the Mod wheel is at zero), and LFO 1 as the second Scale parameter (Amount set to whatever you like).
          When you move the Mod wheel, the pitch modulation amount will be modulated by both the Mod Envelope and
          LFO 1 simultaneously.

      Modulation Sources - Voice section
      The following parameters can be used as Voice section modulation Sources:

      | Parameter            | Description
      Voice Key               Voice Key lets you assign modulation according to notes. There are 4 modes selectable from the
                              sub-menus:
                             • Note - this is keyboard tracking. If a positive Amount value is used and the
                               destination is filter frequency, the filter frequency will track the keyboard,
                               i.e. increase with higher notes.
                             • Note2 - this works similarly to Note but within a repeated octave range.
                               E.g. if Note2 modulates Amp Pan the pan position will move from left to
                               right within an octave range then start over. If you play chords normally
                               over the keyboard the effect will be that notes are randomly spread across
                               the stereo field.
                             • Velocity - this applies modulation according to velocity (how hard or soft
                               you strike the keys).
                             • Gate - this is Gate on/off. E.g. if applied to oscillator pitch you will get one
                               pitch value (set by Amount) when a key is pressed, and another value (the
                               unmodulated pitch) when the key is released.
      Osc 1/2/3               This allows you to route the audio output from the oscillators to a destination.
      Filter 1/2              This is the audio output of the filters. All filter parameters affect the destination.
      Shaper                  This is the audio output of the Shaper module. Note that anything connected to the Shaper, e.g.
                              Filter 1, affects the Shaper output, and thus the resulting modulation.
      Amp                     This is the audio output of the Amp Gain section.
      LFO 1                   This allows you to modulate parameters with LFO 1.
      Filter Envelope         This allows you to modulate parameters with the Filter Envelope.
      Amp Envelope            This allows you to modulate parameters with the Amp Envelope.
      Mod Envelope            This allows you to modulate parameters with the Mod Envelope.

      Modulation Sources - Global
      The following parameters can be used as Global section modulation Sources:

      | Parameter                | Description
      Global Envelope             This allows you to modulate parameters using the Global Envelope.
      Voice Mixer                 This allows you to modulate parameters using the Left and Right Mixer inputs.
      Last Key                    This will apply modulation according to the last note played (monophonic), either via MIDI, or
                                  from the Step Sequencer. For example, you can use Last Key to make a filter’s frequency
                                  track notes played by the Step Sequencer.
      MIDI Key                    This applies modulation according to notes globally, not per-voice so in other words it is
                                  monophonic. E.g. if you use MIDI Note as Source and a self-oscillating filter’s frequency as
                                  the destination, the filter will track but you will only be able to play one voice at a time. MIDI
                                  Note is handy for transposing Step patterns in real time.
                                  There are 3 modes selectable from the sub-menus:
                                 • Note - this is keyboard tracking. If a positive Amount value is used and
                                   the destination is filter frequency, the filter frequency will track the
                                   keyboard, i.e. increase with higher notes.
                                 • Velocity - this applies modulation according to velocity (how hard or
                                   soft you strike the keys).
                                 • Gate - this is Gate on/off. E.g. if applied to oscillator pitch you will get
                                   one pitch value (set by Amount) when a key is pressed, and another
                                   value (the unmodulated pitch) when the key is released.
      LFO 2                       This allows you to modulate parameters with LFO 2.
      Performance parameters      On this sub-menu you can assign the one of the standard Performance controllers to modu-
                                  late/scale parameters; Mod Wheel/Pitch Bend/Breath/AfterTouch/Expression.
      Modifiers                   This is where you assign parameters and functions to be controlled with the virtual 2 Rotary
                                  and 2 Button controls on the Controller panel.
      Sustain Pedal               This allows you to assign the Sustain Pedal as a modulation source.
      Polyphony                   This allows you to apply modulation according to how many notes you play. E.g. you could
                                  have a short envelope attack when you play single notes, and a long attack when you play
                                  chords.
      Step Sequencer              This allows you to apply modulation according to the settings for each step in the Step Se-
                                  quencer.
                                  On the sub-menu you can chose to apply modulation according to Gate/Note/Curve 1 and
                                  2/Gate Length/Step Duration settings for each step.
                                  In addition you have Start and End Trig, which sends a gate trigger at the start and end of the
                                  Step sequence, respectively.
      CV Inputs 1-4               These are CV inputs on the back panel which facilitates the use of external modulation
                                  sources, (e.g. the Matrix) in Thor. If connected you can freely assign the external CV to any
                                  modulation destination in Thor.
      Audio Inputs 1-4            These are Audio inputs on the back panel which allows you to connect external audio signals
                                  and process these using Thor parameters, or use them as modulation sources. See “About
                                  using the Audio inputs”.

      Modulation Destinations - Voice section
      The following parameters can be used as Voice section modulation Destinations:

      | Parameter                 | Description
      Osc 1                       There are four modulation destinations available on the Osc 1 sub-menu:
                                  • Pitch - this will affect oscillator pitch (frequency).
                                  • FM - this will frequency modulate the oscillator.
                                  The difference between Pitch and FM is that if a high frequency audio signal (i.e. an oscillator
                                  or an external audio signal) is the source, FM will not alter the basic pitch of the source, only
                                  the timbre. If Pitch is used both the pitch and the timbre will be affected.
                                  • There is also a modifier parameter, which differs depending on what
                                    oscillator type is selected. See “The Oscillator section” for details.
                                  • Osc 2 AM Amount - this will control AM modulation amount from Osc
                                    2. See “About Amplitude Modulation (AM)”.
      Osc 2/ Osc 3                Oscillator slots 2 and 3 have the same Destination parameters as Osc 1, except that there is
                                  no AM.
      Filter 1/ Filter 2          The following destinations are available on the Filter 1 and 2 sub-menus:
                                  • Audio In - this allows you to connect an audio source (e.g. an oscilla-
                                    tor or an external audio signal) to the filter input.
                                  • Frequency - this controls the filter frequency.
                                  • Frequency (FM) - this will apply filter frequency modulation.
                                  The difference between Frequency and FM is that if a high frequency audio signal (i.e. an os-
                                  cillator or an external audio signal) is the source, FM will not alter the basic frequency of the
                                  source, only the timbre. If Frequency is used both the pitch and the timbre will be affected.
                                  • Resonance - this controls filter resonance.
                                  • Drive - this controls the filter’s Drive parameter.
                                  • Gender - this controls the Gender parameter (Formant filter only).
                                  • LPHPMix - this controls the LP/HP parameter (State Variable filter
                                    only).
      Shaper Drive                This will control the Shaper Drive parameter.
      Amp                         The Amp section has three destinations on the sub-menu:
                                  • Input - this allows you to connect a source (e.g. an oscillator or an ex-
                                    ternal audio signal) to the Amp input.
                                  • Gain - this controls the Amp Gain.
                                  • Pan - this controls the Pan for each voice. Modulating this parameter
                                    with for example LFO 1 means that the Pan position will modulate dif-
                                    ferently for each voice you play.
      Mix                         The Mixer has three destinations on the sub-menu:
                                  • Osc 1+2 Level - this controls the level of both oscillator 1 and 2.
                                  • Osc 1:2 Balance - you can modulate the level balance between oscilla-
                                    tor 1 and 2, e.g. to sweep from one oscillator to the other.
                                  • Osc 3 Level - this controls the level of oscillator 3.

      | Parameter                  | Description
      Filter Envelope               The Filter Envelope mod destinations are as follows:
                                   • Gate - this is the gate input of the envelope. A gate signal applied to
                                     this input will trigger the envelope.
                                   • Attack - this controls the Attack of the envelope.
                                   • Decay - this controls the Decay of the envelope.
                                   • Release - this controls the Release parameter.
      Amp Envelope                  This has the same destination parameters as the Filter Envelope.
      Mod Envelope                  This has the same destination parameters as the Filter Envelope.
      LFO 1 Rate                    This allows you to control the LFO 1 Rate parameter.

      Modulation Destinations - Global
      The following Global modulation destinations are available:

      | Parameter                  | Description
      Portamento                    This allows you to control the Portamento time parameter.
      LFO 2 Rate                    This allows you to control the LFO 2 Rate parameter.
      Global Envelope               The Global Envelope mod destinations are as follows:
                                   • Gate - this is the gate input of the envelope. A gate signal applied to
                                     this input will trigger the envelope.
                                   • Attack - this controls the attack time of the envelope.
                                   • Decay - this controls the decay time of the envelope.
                                   • Release - this controls the release time of the envelope.
      Filter 3                      The following destinations are available on the Filter 3 sub-menu:
                                   • Left/Right In - this allows you to connect a source to the filter input.
                                   • Frequency - this controls the filter frequency.
                                   • Frequency (FM) - this will apply filter frequency modulation.
                                   • Resonance - this controls filter resonance.
                                   • Drive - this controls the filter’s Drive parameter.
                                   • Gender - this controls the Gender parameter (Formant filter only).
                                   • LPHPMix - this controls the LP/HP parameter (State Variable filter
                                     only).
      Chorus                        The Chorus effect has the following destinations:
                                   • DryWet balance
                                   • Delay (time)
                                   • ModRate
                                   • ModAmount
                                   • Feedback

      | Parameter                   | Description
      Delay                         The Delay effect has the following destinations:
                                    • DryWet balance
                                    • Time
                                    • ModRate
                                    • ModAmount
                                    • Feedback
      Step Sequencer                This allows you to control various parameters belonging to the Step Sequencer.
                                    • Trig - this enables control over the Step Sequencer Run on/off status.
                                    • Rate - this enables control over the Step Sequencer Rate.
                                    • Transpose - this enables control over the Step Sequencer base pitch.
                                      E.g. if you apply MIDI Note as a source to this parameter you can
                                      transpose the sequence by playing notes.
                                    • Velocity - this enables control over the Step Sequencer Velocity re-
                                      sponse.
                                    • Gate Length - this enables control over the Step Sequencer Gate
                                      Length response.
      CV Output 1-4                 This will allow you to send signals to the CV outputs on the back of the device. Note that you
                                    can send CV signals to audio outputs and vice versa.
      Audio Output 1-4              This will allow you to send signals to the audio outputs on the back of the device. Note that
                                    you can send CV signals to audio outputs and vice versa.

      Scale parameters
      The available scale parameters are the same as the Source parameters.

      About using the Audio inputs
      The 4 Audio inputs on the back panel can be used to connect external audio sources and process them with Thor’s
      parameters.
      Note that when routing audio to the Voice section, the following things apply:
      • There are only mono inputs in the Voice section.
      • You need to send a gate trigger for the audio signal to be heard. This can be done in three ways; by playing
        notes, via notes played by the Step sequencer or from CV gate signals.
      D   Routing audio to Global destinations does not require a gate trigger and stereo inputs are provided.
      D   The external audio sources can also be used purely for modulation, e.g. you can modulate an oscillators pitch
          with an audio signal.
          This way you can use the audio input source to modulate any available destinations.

      Step Sequencer

      Thor’s Step Sequencer is a further development of the step sequencers which were often present in vintage analog
      modular systems. It can be used for programming arpeggios or short melody sequences. Alternatively, it can be used
      purely as a modulation source.
      You can have up to 16 steps, and each step can be programmed with various values such as Note pitch, Velocity,
      Step Duration etc.

      Basic operation
      The main parameters and functions are as follows:
      D   The row of 16 buttons are used to program each step’s on or off status.
          A lit button means that the step is active, and a dark button means that the step will be a rest (silent).
      D   Each step button has a knob above it, which is used to set values for the corresponding step.
      D   The Edit knob determines what value you set with the step knobs.
          The available Edit values are Note (pitch), Velocity, Gate length, Step duration and Curve 1 and 2.
      D   The Run button starts/stops the step sequencer.
      What exactly happens when you press Run depends on the Run mode - see below.

      Setting the Run mode

      The Run mode is set with the lever beside the Run button. The set mode governs how the step sequencer is played
      back when you press Run. The options are as follows:
      D   Repeat mode - this will repeat the sequence continuously.
          Click the Run button again or use the Transport to stop.
      D   1 Shot mode - this will play the sequence once then stop.
      D   Step mode - the Run button steps the sequencer forward one step at a time.
      D   Off - the step sequencer is inactive.

      Setting the direction

      The Direction parameter is used to set the direction of the step sequence. The following options are available:
      D   Forward - plays the sequence from the first step to the last.
      D   Reverse - plays the sequence from the last step to the first.
      D   Pendulum 1 - plays the sequence from the first step to the last, then from the last step to the first.
          I.e. the last and first step is played twice when the sequencer reverses direction.
      D   Pendulum 2 - plays the sequence from the first step to the last, then from the second last step to the first, i.e.
          without repeating the last/first step when reversing direction.
      D   Random - plays the steps in a random order.

      Programming step note pitch
      To program step note pitch, you proceed as follows:
      1. Make sure that the Step Seq Trigger button is activated in the Controller panel.

      2. Set the Run mode to “Repeat”.
          You don’t have to use Repeat mode but it makes it easier to follow the following steps.
      3. Start the step sequencer by pressing the Run button.
          You should now hear a sequence of repeated notes, each with the same pitch (C3). The current step is indicated
          by a yellow LED above the step buttons.
      4. Make sure that the Edit knob is set to Note.

      5. Turn one of the step knobs above one of the steps.
          A tooltip shows you what current note pitch the knob is set to, and when the sequencer repeats you should be able
          to hear the change in pitch for that step. Turn clockwise to raise the pitch in semitone increments. Turn counter-
          clockwise to lower the pitch.

      D   You can set the knob’s note range by using the Octave lever to the left of the step buttons.
          Available note ranges are 2 Octaves (i.e. one octave up and down from the middle knob position (C3), 4 Octaves
          (i.e. two octaves up and down from the middle position (C3), or Full (-C2 to G8).
      q   Note that the octave range can be set independently for each step. Each step memorizes the current octave
          range when the pitch is set for that step, and will keep this octave range until you change the pitch for the step
          with a different octave range setting.
      D   You can either program steps “on the fly” (with the Step sequencer running) or step by step (Step mode).
          In Step mode, you press Run to forward the step number one position so you can set step parameters for one step
          at a time.
      By using this general method you can continue to enter note pitch for other steps.

      Inserting rests
      To make step sequences more rhythmically interesting, you can program rests for steps.
      D   This is simply done by pressing one or several step buttons so they go dark.
          Dark steps will be rests.
      D   Note that the Step Duration value still “counts” for rests.

      Setting the number of steps
      D   You can set how many steps a sequence should have before starting over using the Steps knob at the far right
          on the panel.
          Up to 16 steps can be used. The lit LEDs above each step button show the number of steps currently used. You
          can also change number of steps by clicking on a LED directly - the sequencer will then stop/start over at the se-
          lected step.

      Setting Rate
      The Rate knob determines the rate of the step sequence.
      • You can either use “free running” rates (i.e. not synced to main sequencer tempo) or synced tempo.
          This is set with the Sync button on/off status. If Sync is active you can set the tempo in various beat resolutions.

      Setting other values for steps
      For each step you can also program other parameters with the step value knobs apart from note pitch. You use the
      Edit knob to set one the following:
      D   Velocity - if this is selected as the Edit mode you can set a velocity value for each step.
          Default value is 100, range is 0-127.
      D   Gate Length - if this is selected as the Edit mode you can set a Gate Length value for each step.
          Default is 75%. Gate Length determines the length of the note played for that step.
      D   Step Duration - if this is selected as the Edit mode you can set a Step duration value for each step.
          This parameter determines the total length of the step, which is a factor related to the sequencer rate. Range is 1/
          4 to 4. E.g. if Rate is 1/16, “1” means a 1/16-note will be played, a “4” means a 1/4-note will be played, and so on.
      D   The Curves 1 and 2 allow you to set values for each step that can be sent to control parameters of your choice.
          This is done in the Modulation bus routing section, where these two independent Curves are selectable as Source
          controllers.
      q   You can compare these curves to the Curve CV output of the Matrix - they simply represent a series of values
          which can be applied to anything.

      Step Pattern functions
      You will find some specific Step pattern functions on the Edit menu (and on the device context menu). These are as
      follows:

      | Function                    | Description
      Randomize Sequencer Pattern   The Randomize Pattern function creates random patterns. The function only randomizes the se-
                                    lected Edit value (e.g. if set to Note, only the note pitch values are randomized, not velocity, gate
                                    length etc.).
      Shift Pattern L/R             The Shift Pattern functions move the pattern one step to the left or right. All parameters (rests,
                                    note pitch, velocity etc.) are shifted one step.

      Connections
      The following Audio and CV connectors can be found at the back of Thor:

      Sequencer Control Inputs
      The Sequencer Control CV and Gate inputs allow you to play Thor from another CV/Gate device (e.g. a Matrix or the
      RPG-8). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note on/off
      along with velocity.

      Modulation Inputs
      D   The Rotary control voltage (CV) inputs (with associated voltage trim pots), can modulate the two virtual Rotary
          controls.
          Thus, any parameter(s) assigned to a Rotary control can be modulated by CV.
      D   The Filter 1x allows for CV control of the Filter 1 frequency.
          If the Formant filter is used this is the “X” parameter - see “Formant filter”.
      D   The four CV Inputs can receive CV from external sources that will be available as Sources in the Modulation
          bus.

      Modulation Outputs
      Here you can find CV outputs from the Global Envelope and LFO 2, as well as the 4 user assignable CV outputs.

      Audio Inputs
      The Audio inputs can be used to connect audio outputs from other Reason devices. When connected, you can route
      the Audio inputs as a Modulation source to for example one of the filters and process the external signal. See “About
      using the Audio inputs”.

      Audio Outputs
      Thor has 4 outputs:
      • 1 Left (Mono)/2 Right - these are the main stereo outputs.
      • 2 additional outputs (3 and 4), which can be assigned in the Modulation section.

856   THOR POLYSONIC SYNTHESIZER


---

<a id="subtractor-synthesizer-34"></a>

=== END OF PART ===
