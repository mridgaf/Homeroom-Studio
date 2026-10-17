# Chapter 09: Reason 12 manual digest and studio workflow
## Part 65 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 56 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 66 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 56 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      The Drum and FX section in Kong is built up of the Drum Control Panel and the Drum and FX section.
      D   Click the Show Drum and FX button below the Drum Control Panel to unfold the Drum and FX section.
          The Drum and FX section consists of five slots:
      • The Drum Module Slot.
      • The FX1 Slot.
      • The FX2 Slot.
      • The Bus FX Slot.
      • The Master FX Slot.
      The Drum, FX1 and FX2 slots are unique to each of the 16 Drum channels in Kong. The Bus FX and Master FX slots
      are shared between all Drum channels in the Kong device. You can activate/deactivate any of the slots by clicking
      the On button at the upper left of each slot.

      Signal flow
      The output signal from a Drum module is sent via the FX1 and FX2 Slots to the Bus FX, Master FX or to a pair of the
      individual outputs on the back of the Kong panel. There is also an internal Bus FX Send that can be used to send an
      audio signal from the Drum via the FX1 and FX2 Slots to the Bus FX. The Bus FX Slot can the hold e.g. a reverb
      module which can be used a send effect for all the Drum channels. As an extra bonus, you can also hook up an ex-
      ternal effect device between the Bus FX and Master FX Slots, see “Using external effects with Kong”.
      The signal routing in the Drum and FX section depends on the Drum Output selector setting at the bottom of the
      Drum and FX section:

      The different signals flows are described in the following paragraphs:

      Master FX Drum Output
      When the Drum Output is set to “Master FX”, the signal flow is according to the picture below. If you are using a Bus
      FX, this is treated as a Send effect with the Bus FX level controlled by the Bus FX knob on the Drum Control Panel.
                                                                                                     Bus FX

                 Drum Module                      FX1       FX2
                                                                                                     Master FX

                                                                                                          Main Out L & R

      Signal flow when Drum Output is set to “Master FX”.

      Bus FX Drum Output
      When the Drum Output is set to “Bus FX”, the signal flow is according to the picture below. Note that the Bus FX is
      now routed both as an Insert effect and as a Send effect at the same time. Therefore, it might be a good idea to set
      the Bus FX Send knob on the Drum Control Panel to zero in this configuration.
                                                                                                     Bus FX

                 Drum Module                       FX1    FX2
                                                                                                     Master FX

                                                                                                          Main Out L & R

      Signal flow when Drum Output is set to “Bus FX”.

      Separate Out Drum Output
      When the Drum Output is set to any of the separate output pairs “3-4” to “15-16”, the signal flow is according to the
      picture below. The signals to the selected separate output pair are taken directly after the FX2 via the Master Level
      knob. Note that the signal via the Bus FX and Master FX is still available on the Main Out L & R and can be controlled
      with the Bus FX Send knob on the Drum Control Panel.
                                                                                                       Bus FX

                Drum Module                       FX1            FX2
                                                                                                       Master FX

                                                                                                            Main Out L & R

                                                                                                            Output 3 & 4

      Signal flow when Drum Output is set to any of the separate output pairs “3-4” to “15-16”.

      The Drum Control Panel

      The Drum Control Panel features a set of “macro controls” that affect parameters in each Drum. These controls scale
      the parameters in the Drum module and FX modules in the Drum and FX section. There are also some standard pa-
      rameters that are identical for each Drum: Pan, Tone and Level.
      • The Pitch Offset knob affects the Pitch parameters in all Drum modules.
         No FX modules are affected, even if they feature a Pitch parameter.

      • The Decay Offset knob affects the amplitude Decay or Release parameters in all Drum modules plus any FX
        modules that feature a Decay parameter.
        For example, the reverb decay time in the Room Reverb FX module is affected by the Decay Offset parameter.
      • The Bus FX Send knob affects the signal level sent to the Bus FX Slot.
        Depending on current Drum Output setting, the effect will be a little different - see the examples in “Signal flow”.
      • The Aux 1 and Aux 2 Send knobs controls the level to any devices connected to the Aux 1 and Aux 2 Send Out-
        puts on the back of the panel, see “Aux Send Out”.
        The signals to the Aux Send is tapped after the FX1 and FX2 Slots but before the Bus FX and Master FX Slots.
      • The Pan parameter controls the panning of the signal in the stereo panorama.
        The Pan parameter affects the signal after the FX1 and FX2 Slots but before it is sent to the Bus FX and Master
        FX Slots.
      • The Tone parameter is a built-in filter (similar to the filter in Redrum).
        The Tone parameter affects the signal after the FX1 and FX2 Slots but before it is sent to the Bus FX and Master
        FX Slots.

      Editing the Drum Control Panel parameters using the Quick Edit function
      A quicker way of editing the Drum Control Panel parameters for several Drum channels at once is by using the Quick
      Edit function. The Drum Control Panel features four Quick Edit buttons.
      1. Click the Quick Edit button below the Pitch and Decay Offset section.

        Each Pad now shows the current Pitch and Decay Offset settings for each assigned Drum channel.
      2. Edit the Pitch and Decay Offsets by clicking and dragging the “crosshair” on the desired Pads.

        The Decay Offset is on the horizontal X-axis and the Pitch Offset is on the vertical Y-axis, as shown in plain text
        on the big red frame around the Pad section. As you move the crosshair, the corresponding knobs on the Drum
        Control Panel move as well - and vice versa.
      3. When you are done, click the Quick Edit button or press [Esc] to exit - or click another Quick Edit button to
         change other sets of parameters.

      Loading and Saving Drum Patches

      Loading and Saving Kong Drum patches (“.drum”) are done in the same way as with any other Reason device - see
      “Creating a new Kit Patch”, “Loading patches” and “Saving patches”.
      A Kong Drum patch contains all parameter settings on the Drum Control Panel, including modules and parameter
      settings in the Drums and FX section - with references to any used samples.
      It’s also possible to load samples and REX loops in the Drum Control Panel section. Loading a sample will automati-
      cally open it in an NN-Nano Sampler module (see “NN-Nano Sampler”) and loading a REX file will automatically open
      it in a Nurse Rex Loop Player module (see “Nurse Rex Loop Player”).

      Sampling in Kong
      The sampling procedure is the same for all devices that can sample (Kong, NN-19, NN-XT and Redrum). The sam-
      pling and sample editing procedures are described in detail in the “Sampling” chapter.
      D   To sample your own sound and automatically load it into an NN-Nano Sampler module in the Drum and FX
          section, click the Sample button for the desired Drum channel.

          Refer to the “Sampling” chapter for details on how to set up and use the sampling feature.

      The Drum Module slot

      Each Drum channel in Kong has a main module slot - the Drum Module slot - to which you can load one of 9 different
      types of drum sound modules for designing drum sounds.

      D   Select Drum Module type by clicking the button to the right of the On button and selecting the module from the
          pop-up.
          the following Drum Module types can be selected: NN-Nano Sampler, Nurse Rex Loop Player, Physical Bass
          Drum, Physical Snare Drum, Physical Tom Tom, Synth Bass Drum, Synth Snare Drum, Synth Tom Tom and Synth
          Hi-Hat. See “The Drum modules” for details about each Drum module.
      !   Note that only four pre-defined parameters per Drum Module can be automated!
          At the bottom below the Drum Slot is the Pitch Bend Range parameter which controls the Pitch Bend Range for
          the Drum Slot. This parameter is global for all types of Drum Modules but is unique to each of the 16 Drum chan-
          nels.

          The Pitch Bend Range knob for each of the 16 Drum channels

      The FX slots

      Each Drum channel also has 2 insert effect slots - the FX 1 and FX 2 Slots - to which you can load one of two dif-
      ferent types of support sound generators or one of 9 different effect modules.
      D   Select Module type by clicking the button to the right of the On button and selecting module from the pop-up.
          the following module types can be selected for the FX 1 and FX 2 Slots: Noise generator, Tone generator, Room
          Reverb, Transient Shaper, Compressor, Filter, Parametric EQ, Ring Modulator, Rattler, Tape Echo and Overdrive/
          Resonator. See “The Support Generator modules” and “The FX modules” for details about each module type.
      !   Note that only two pre-defined parameters per FX/Support Generator Module can be automated!
      • For the Bus FX and Master FX slots, all module types except the Noise and Tone generators can be selected.

      The Drum modules
      !   Note that only four pre-defined parameters per Drum Module can be automated!

      NN-Nano Sampler

      The NN-Nano Sampler is based on the NN-XT Sampler and was designed to be ideal for drums and percussion
      sounds.
      The NN-Nano can handle samples or sets of samples for each of the four different Hit Types described in “Assigning
      Hit Type to Pads”. Each Hit Type can contain one or several samples which can be layered and/or altered and con-
      trolled individually via velocity.

      Loading samples
      1. Select the Hit you want to load the sample(s) into by clicking in the display.

      2. Click the Browse Samples (folder) button and select one or several WAV, AIFF or SoundFont Samples or REX
         slice files.
      3. Click the Load button in the Browser.
          The sample(s) are loaded in the selected Hit.

      D   Alternatively, drag a sample, a REX slice or a SoundFont file from the Browser and drop on the NN-Nano panel.
          The NN-Nano panel is dimmed in blue and a Sample Replace symbol appears in the center.
      If you selected several samples in the Browser, these will be loaded as separate Layers in the selected Hit.
      If you like you can load additional samples, either into another Hit or into a new Layer in the same Hit. To load a new
      sample in a new Layer in the same Hit, proceed as follows:

      1. Select the Hit and then click the Add Layer button.

          An additional space is created in the Hit.
      2. Select the empty Layer in the display and load a new sample according to the description in “Loading samples”
         above.
      The NN-Nano Sampler module in Kong can read and play back sample files of the following formats:
      • In Windows:
          .wav, .aif, .mp3, .aac, .m4a and .wma.
      • In macOS:
          .wav, .aiff, .3g2, .3gp, .mp1, .mp2, .mp3, .mpeg, .mpa, .snd, .au, .sd2, .ac3, .aac, .adts, .amr, .caf, .m4a .m4r and .mp4.
      • SoundFonts (.sf2)
          SoundFonts are an open standard for wavetable synthesized audio, developed by E-mu systems and Creative
          Technologies.
      • REX file slices (.rx2, .rex, .rcy)
          REX files are music loops created in the ReCycle program or when editing audio clips inline in Reason (see
          “Bounce Clip to REX Loop”). The NN-Nano lets load separate slices from REX files as individual samples.
      • Any sample rate and practically any bit depth.

      Replacing samples
      D   To replace one or several samples, select the sample(s) in the display and then load new samples according to
          the description in “Loading samples”.
          This way it is possible to e.g. replace three selected samples with three new samples in one go.

      Adding and Removing Layers
      D   To add a new Layer to a Hit, select the Hit and click the Add Layer button.

          An additional space is created in the Hit for the created Layer.
      D   To remove a Layer from a Hit, select the Layer and click the Remove Layer button.

          The Layer is removed together with its sample (if any).

      Sampling into the NN-Nano
      The sampling procedure is generic for all devices that can sample (Kong, NN-19, NN-XT and Redrum). The sampling
      and sample editing procedures are described in detail in the “Sampling” chapter.

      D   To sample your own sound and automatically load it into the NN-Nano, click the Sample button.

          Refer to the “Sampling” chapter for details on how to set up and use the sampling feature.

      The Edit Sample button

      If you click the Edit Sample button with a sample selected in the display, the sample will open in the generic Edit
      Sample window. In this window you can edit the sample and save as a self-contained Song Sample. See “The Edit
      Sample window” in the Sampling chapter for details about editing samples.

      Sample parameters
      There are a number of parameters that are unique to each individual sample and Hit in the NN-Nano. These param-
      eters are visible in the display for the selected (highlighted) sample:

      • Velocity
          The Velocity range can be set, either by clicking and dragging the Velocity bar sideways to the right of the sample,
          or by clicking and dragging the Vel Lo and Hi values vertically at the bottom of the display.
      • Level
          Set the sample level by clicking and dragging the Level value up or down in the display.
      • Pitch
          Set the sample pitch by clicking and dragging the Pitch value up or down in the display.
      • Alt
          Click the Alt box for several samples in the same Hit to make them play back alternating.
      • Hit Name
          Edit the Hit Name if you like by clicking in the Hit Name box, typing in a new name and then pressing [Enter]. The
          name will appear in the Hit Type display on the main panel (see “Assigning Hit Type to Pads”).
      !   It’s also possible to select multiple samples and edit them together. If the selected samples have different
          Level, Velocity, Range and/or Pitch values this is indicated by an “M” (for multiple) symbol next to the param-
          eter:

          If you change the values of any of the “M” parameters, all selected samples will get the exact same value.

      Global parameters
      The parameters located on the panel, outside the display, are global and affect all samples in all Hit groups equally.

      • Polyphony
        “Full” is, as the word implies, full polyphony. This means that all Hits can sound with full polyphony. Several Hits can
        also sound together if controlled from separate Pads that are assigned to different Hit Types.
        “Exclusive Hits” means that when one Hit plays it will automatically mute any other sounding Hits. The polyphony
        is still full within each Hit, though.
        “Monophonic” is... well, monophonic.
      • Mod Wheel
        If you want the Mod Wheel to affect the pitch and/or decay of the sound, you can set this with the Mod Wheel ->
        Pitch and/or the Mod Wheel -> Decay knobs. Both parameters are bipolar (+/-).
      • Velocity
        In the Velocity section you can control how the velocity should affect a number of parameters. The parameters are:
        Pitch, Decay, Level, Bend and Sample Start. All parameters are bipolar (+/-).
      • Pitch
        Here you can set the global Pitch, Pitch Bend Amount and Pitch Bend Time for all samples. The Pitch and Pitch
        Bend Amount parameters are bipolar (+/-).
      • Osc
        In the Osc section you can set the global Sample Start and Reverse parameters for all samples in the NN-Nano.
      • Amp Env
        The Amp Env section contains an Attack-Decay Envelope and the global Level parameter for all samples. There is
        also an envelope trigger mode selector for choosing between Gate and Trig mode. In Gate mode (the square sym-
        bol), the Decay time defines the minimum gate time. If you hold down a key or pad on your MIDI keyboard/control
        surface, the Decay stage will set in after you released the key/pad.

      Nurse Rex Loop Player

      The Nurse Rex Loop Player is based on the Dr. OctoRex Loop Player but has been modified to be ideal for playing
      and triggering drum and percussion sounds.
      The Nurse Rex can load standard REX files and play back the loops and/or slices in a variety of ways depending on
      the selected Hit Type (see “Assigning Hit Type to Pads”).

      Loading REX files
      1. Click the Browse Samples (folder) button.

      2. Select a REX file and click the Load button in the Browser.
      D   Alternatively, drag a REX file from the Browser and drop on the Nurse Rex panel.
          The Nurse Rex panel is dimmed in orange and a Patch Replace symbol appears in the center.
      The REX file is loaded in Nurse Rex with the loop shown in the display.

      Hit Types (playback modes)
      Depending on selected Hit Type, the REX loop will play back differently. The editing possibilities also differs depend-
      ing on selected Hit Type for the assigned pad.
      • Loop Trig
          In Loop Trig mode, you trigger the REX loop to play one single cycle every time you hit the assigned pad. Loop Trig
          can also be used together with the “Stop” mode on another pad to immediately stop the loop playback, see “Stop”
          below.
                                                                Loop range (Start and End)

          A REX loop with “Loop Trig” as Hit Type.

      D   Set Start and End slice, either by clicking and dragging the S and E numerical values up/down in the boxes, or
          by clicking and dragging the handles sideways in the “ruler” above the REX loop in the display.

          Different ways of editing the Start and End Slice values.
      • Chunk Trig
          In Chunk Trig mode, you can assign several pads to play back shorter sections - chunks - of the REX loop. The
          number of chunks is determined by the number of pads you have assigned to the REX loop using the Chunk Trig
          Hit Type. The chunks are distributed in equal sections across the REX loop. Chunk Trig can also be used together
          with the “Stop” mode on another pad to immediately stop the chunk playback, see “Stop” below.
          In the picture below, we have assigned four pads to the same REX loop and we have selected “Chunk Trig” as Hit
          Type on all four pads:

                   Four Chunks distributed
                   equally across the REX loop

                                                                      Pad 1-4 assigned to the same
                                                                      Nurse Rex module

          Four pads assigned to the same REX loop and Hit Type set to “Chunk Trig”.
      D   Set the size of the chunks by clicking and dragging the right edges of the “tabs” above the REX loop in the dis-
          play.
          Doing so will automatically move the start position of the subsequent chunk so that the chunks will always be ad-
          jacent to each other.

          Editing the sizes of the chunks.

      D   Change the Start position of the first chunk and the End position of the last chunk by changing the REX loop
          Start and End values.
          In effect, this is the same as setting the overall REX loop start and end position.

          Editing the start position of the first chunk and end position of the last chunk.
      • Slice Trig
          In Slice Trig mode, you can assign a pad to play back one single slice of the REX loop - or several slices alternat-
          ingly. By default, Slice 1 of any REX loop loaded into the Nurse Rex is set to play back when you have selected
          “Slice Trig” as Hit Type.

                                                                            Slice 1 plays back by default
                                                                            in Slice Trig mode

          A REX loop with “Slice Trig” as Hit Type.
      D   Change the slice to play back by first removing the tick in the Trig checkbox and then clicking on another slice
          in the display and ticking the Trig checkbox for that slice.

                                                                            Slice 3 plays back instead

          Slice 3 selected for playback in Slice Trig mode.
      Another way of assigning a slice for playback, or to assign several slices to play back alternating, is by using the
      mouse in combination with the [Ctrl](Win)/[Cmd](Mac) key.
      D   Hold down [Ctrl](Win)/[Cmd](Mac) and click on the slice(s) in the display you want to assign or deassign.

                                                                            Slices 3, 5, 8 and 11 selected and will now play
                                                                            back alternating in Slice Trig mode

          Slices 3, 5, 8 and 11 selected for playback in Slice Trig mode, forcing them to play back alternating.
          Selected slices are displayed with a red background. The currently “focused” slice is displayed with an orange
          background. Selected slices also get their corresponding Trig checkbox ticked automatically.

      • Stop
         The fourth Hit Type is named “Stop”. The Stop mode can be used if you want to use a pad for immediately stop-
         ping the currently playing REX loop or Chunk. The Stop mode should be used in combination with any of the Hit
         Types “Loop Trig” or “Chunk Trig”, otherwise it won’t be useful.

         “Stop” selected as Hit Type for a pad assigned to a Nurse Rex module.
      1. Assign one pad to a REX loop in Nurse Rex and select any of the Hit Types “Loop Trig” or “Chunk Trig”.
      2. Assign another pad to the same Nurse Rex module and select “Stop” as Hit Type.
         Now, when you play the first pad, the loop or chunk will play. Once you hit the second pad, the loop/chunk play-
         back will immediately stop.

      Combining Hit Types
      By combining the different Hit Types for the Nurse Rex module you can create really interesting setups. For example,
      you could load a REX loop and assign a couple of pads to the “Chunk Trig” Hit Type, one pad to Loop Trig, another
      one to Slice Trig and another pad to Stop. Playing the different pads can now generate really inspiring results. The
      picture below shows an example of this type of setup:

      Eight pads assigned to the same Nurse Rex module, with the pads set to different Hit Types (in Quick Edit mode).
      If we click the Hit Type Quick Edit button, we can see that Pad 1 is set to Loop Trig, Pads 2-6 are set to Chunk Trig,
      Pad 7 is set to Slice Trig and has four slices set to Trig in the REX loop display for alternate playback. Finally Pad 8
      is set to Stop so we could stop the loop and chunks playback whenever we like.

      Editing Slice Parameters
      In the REX loop display you can edit parameters that are unique to each separate slice:

                                                                  Slice parameters


=== END OF PART ===
