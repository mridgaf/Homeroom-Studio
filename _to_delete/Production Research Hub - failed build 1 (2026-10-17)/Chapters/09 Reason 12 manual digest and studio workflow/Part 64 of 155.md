# Chapter 09: Reason 12 manual digest and studio workflow
## Part 64 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 55 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 65 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 55 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 27: Kong Drum Designer

Kong Drum Designer

      Introduction
      The Kong Drum Designer gives the visual impression of a pattern-based drum machine, like the legendary MPC
      units. Indeed, it does have a matrix of 4 x 4 pads that are used for playing the sounds, just like the aforementioned
      classics. There are significant differences, however.
      Kong features 16 drum “sound channels” that can host one drum sound each. Each drum sound can consist of a
      sound module routed through various types of FX and processing modules, allowing for completely open-ended
      sound design possibilities. Individual drum sounds can be saved as Drum Patches and complete drum kits can be
      saved as Kit Patches, allowing you to mix and match drum sounds and make up custom kits with ease.
      In addition, Kong also has sampling capability. This means that you can sample your own sounds straight into any of
      the 16 drum channels with just a click of a button!

      Overview

      The Kong front panel.
      Kong is an advanced drum sound synthesizer, sampler/sample player and REX loop/slice player with many unique
      features. The design could be described as semi-modular, in that the sound, FX and audio processing modules are
      open slots that allows you to select between an array of different sound generators, FXs and audio processor types.
      As a result, Kong is capable of producing an astounding array of drum and percussion sounds - or any type of sound,
      for that matter. While it offers a lot of scope for serious sound design, it still has a straight-forward and user-friendly
      interface.
      Kong also features audio inputs on the back panel. By connecting the output of another device to these inputs, you
      can use Kong’s audio processing modules to process external sound. You can also route drum sounds for audio pro-
      cessing in external devices.

      The Pad Section
      The pad section features 16 pads. Each of these pads can be assigned to a separate Drum sound. You can also
      choose to assign several pads to one and the same Drum sound - or to link pads so that one pad will trigger several
      other pads as well. To the right of the pads is the Pad Settings area where you can control the pad assignments and
      behavior. See “Pad Settings”.

      The Drum Control Panel
      The Drum Control Panel at the bottom left of the panel shows the name and “macro parameter” settings for the se-
      lected pad in the pad section. From the Drum Control Panel you can also load and save Drum Patches as well as ini-
      tiate sampling. See “The Drum Control Panel”.

      The Drum and FX Section
      By clicking the Programmer button below at the bottom of the Drum Control Panel you can bring up the Drum and
      FX Section. Here is where you can edit your drum sounds and combine with various types of sound processors and
      FX. See “The Drum and FX section”.

      About using custom backdrops
      As with the Combinator device, it is possible to customize the Kong front panel graphics with a user-designed skin. In
      the Reason Download section at the Reason Studios website is the “Combi and Kong Backdrop Templates” zip file,
      which can be used as starting point for designing your own Kong panel graphics. See the “Read Me.txt” file in the
      Backdrops folder for more details. Note that you should use separate backdrops for folded vs. unfolded states.

      About file formats
      Kong can read the following file types:

      Kit Patches
      A Kong Kit Patch (Windows extension “.kong”) contains all settings for all 16 Drum sound channels, including file ref-
      erences to any used drum samples (but not the actual samples themselves). Switching patches is the same as se-
      lecting a new drum kit.

      Drum Patches
      A Kong Drum Patch (Windows extension “.drum”) contains all settings for the selected Drum sound channel, includ-
      ing file references to any used drum samples (but not the actual samples themselves). Switching Drum Patches is
      the same as selecting a new drum sound.

      Drum Samples
      The audio file format support differs depending on which computer OS you are using.
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
        “Bounce Clip to REX Loop”). The NN-Nano lets you load separate slices from REX files as individual samples.

      • Any sample rate and practically any bit depth.
      See “NN-Nano Sampler” for details.

      REX Files
      The Nurse Rex Loop Player module in Kong can read and play back files of the following formats:
      • REX files (.rx2, .rex, .rcy)
          REX files are music loops created in the ReCycle program or when editing audio clips inline in Reason (see
          “Bounce Clip to REX Loop”).
      See “Nurse Rex Loop Player” for details.

      Using patches
      When you create a new Kong device it is loaded with a default kit. If you like you can use the default kit - or you can
      load another Kong Kit patch (or create one from scratch, by loading individual Drum patches). A Kong Kit patch con-
      tains settings for the 16 Drum channels, complete with parameter settings and file references to any samples used.

      Loading a Kit Patch
      To load a patch, use one of the following methods:
      D   Use the browser to locate and open the desired patch.
          To open the browser, select “Browse Kong Patches” from the Edit menu or device context menu, or click the folder
          button in the patch section on the device panel.

      D   Once you have selected a patch, you can step between all the patches in the same folder by using the arrow
          buttons next to the patch name display.
      D   If you click and hold on the patch name display on the device panel, a pop-up menu will appear, listing all Kong
          Kit patches in all currently expanded folders in the Patch Browser.
          This allows you to quickly select another patch without having to step through each one in turn.
      D   Use the drag and drop method to drag Kong Kit Patch files from the Browser and drop on the Kong panel.
          The Kong panel is dimmed in orange and a Patch Replace symbol appears in the center.

      Checking the sounds in a Kit Patch
      There are three ways you can listen to the sounds in a patch without using the main sequencer:
      D   By clicking the Pad buttons on the front panel.

      !   Note that the vertical click position on the pad determines the Velocity value. If you click towards the bottom of
          a pad, the velocity is low and at the top of each pad the velocity value is high.

                                                                                                                          Velocity = 127

                                                                                                                          Velocity = 4

          This will give you a good idea about the dynamics behavior of each drum sound. This also allows you to record in
          the main sequencer using the full dynamic range of each drum sound, even without a connected MIDI keyboard/
          control surface.
      D   By playing the keys C1 to D#2 or C3 to B6 on your MIDI keyboard or on the On-screen Piano Keyboard.
                                                                            Pad 11

                                                                                                   Pad 14
                                                                                                                 Pad 16

                                                                                                                                                                                                                                                                                                              Pad 10

                                                                                                                                                                                                                                                                                                                                     Pad 11
                                                                                                                                                                                                                                                                                                                                                   Pad 11
                                                                                                                                                                                                                                                                                                                                                                 Pad 12

                                                                                                                                                                                                                                                                                                                                                                                        Pad 13
                                                                                                                                                                                                                                                                                                                                                                                                      Pad 14

                                                                                                                                                                                                                                                                                                                                                                                                                             Pad 15
                                                                                                                                                                                                                                                                                                                                                                                                                                           Pad 15
                                                                                                                                                                                                                                                                                                                                                                                                                                                         Pad 16
                   Pad 2
                               Pad 4

                                                   Pad 7
                                                               Pad 9

                                                                                                                                          Pad 1
                                                                                                                                                      Pad 2

                                                                                                                                                                          Pad 3
                                                                                                                                                                                      Pad 3
                                                                                                                                                                                                  Pad 4

                                                                                                                                                                                                                      Pad 5
                                                                                                                                                                                                                                  Pad 6

                                                                                                                                                                                                                                                      Pad 7
                                                                                                                                                                                                                                                                  Pad 7
                                                                                                                                                                                                                                                                              Pad 8

                                                                                                                                                                                                                                                                                                  Pad 9
                                                                   Pad 10
                                                                                 Pad 12
                                                                                          Pad 13
                                                                                                        Pad 15

                                                                                                                                                                                                                                                                                                                   Pad 10
                                                                                                                                                                                                                                                                                                                            Pad 10
                                                                                                                                                                                                                                                                                                                                          Pad 11
                                                                                                                                                                                                                                                                                                                                                        Pad 12
                                                                                                                                                                                                                                                                                                                                                                      Pad 12
                                                                                                                                                                                                                                                                                                                                                                               Pad 13
                                                                                                                                                                                                                                                                                                                                                                                             Pad 13
                                                                                                                                                                                                                                                                                                                                                                                                           Pad 14
                                                                                                                                                                                                                                                                                                                                                                                                                    Pad 14
                                                                                                                                                                                                                                                                                                                                                                                                                                  Pad 15
                                                                                                                                                                                                                                                                                                                                                                                                                                                Pad 16
                                                                                                                                                                                                                                                                                                                                                                                                                                                              Pad 16
           Pad 1
                       Pad 3
                                   Pad 5
                                           Pad 6
                                                       Pad 8

                                                                                                                                  Pad 1
                                                                                                                                              Pad 1
                                                                                                                                                          Pad 2
                                                                                                                                                                  Pad 2
                                                                                                                                                                              Pad 3
                                                                                                                                                                                          Pad 4
                                                                                                                                                                                                      Pad 4
                                                                                                                                                                                                              Pad 5
                                                                                                                                                                                                                          Pad 5
                                                                                                                                                                                                                                      Pad 6
                                                                                                                                                                                                                                              Pad 6
                                                                                                                                                                                                                                                          Pad 7
                                                                                                                                                                                                                                                                      Pad 8
                                                                                                                                                                                                                                                                                  Pad 8
                                                                                                                                                                                                                                                                                          Pad 9
                                                                                                                                                                                                                                                                                                      Pad 9

          C1                                                                              C2                                      C3                                                                          C4                                                                          C5                                                                                   C6

          In the C1-D#2 range, each MIDI note will trigger one pad each, from Pad 1 to Pad 16. In the C3-B6 MIDI note
          range each pad can be triggered from three adjacent keys on your MIDI keyboard. C3-D3 trigs Pad 1, D#3-F3
          trigs Pad 2 and so on. The C3-B6 note range is perfect if you want to play fast passages by triggering the same
          pad from several keys on your MIDI keyboard.

      Creating a new Kit Patch
      To create a patch of your own (or modify an existing patch), use the following basic steps:
      1. Click on the pad for the drum sound you want to load or replace.
          A blue frame surrounds the selected pad.

      2. Click the folder button on the Drum Control Panel.

      D   Alternatively, right-click (Win) or [Ctrl]-click (Mac) on the Pad and select “Browse Drum Patches...” from the
          context menu.
          The Patch Browser opens.
      3. Locate and open a Kong Drum Patch (extension ‘.drum’) or a sample or REX file.
          You will find a selection of Kong Drum Patches in the Factory Sound Bank (in the Kong Drum Patches folder).
          Loading a sample will automatically open it in an NN-Nano Sampler module (see “NN-Nano Sampler”) and loading
          a REX file will automatically open it in a Nurse Rex Loop Player module (see “Nurse Rex Loop Player”).
          You can also sample your own sound into a Drum, see “Sampling in Kong”.
      D   Alternatively, drag a Kong Drum Patch file, a REX file, a sample or a REX slice from the Browser and drop on
          the Drum Control Panel - or on any desired drum pad.
          Depending on if you drop a Drum Patch file, a REX file or a sample/REX slice, the Drum Control Panel or pad is
          dimmed in orange or blue and a Patch/Sample Replace symbol appears in the center.
      !   It is important that you drop REX files either on the Drum Control Panel or on a pad. Dropping it elsewhere will
          replace the entire Kong device with a Dr. Octo Rex device and load the REX file in this device instead!
      4. Change some parameter settings for the drum sound channel using the knobs on the Drum Control Panel.
          These parameters are described in “The Drum Control Panel”. Note that the Drum Control Panel parameters are
          “global” for each Drum channel. Each drum sound can consist of a number of different sound and FX modules,
          each with their separate set of parameters. Refer to “The Drum modules”, “The Support Generator modules” and
          “The FX modules” for details about all the modules that can be used to build up a complete Drum sound.
      5. Repeat steps 1 and 4 for the other drum sound channels.
      6. When you’re satisfied with the drum kit, you can save the patch by clicking the Floppy Disk button in the patch
         section on the Drum panel.
          Note however, that you don’t necessarily need to save the Drum patch - all settings are included when you save a
          Kong Kit Patch (see “Saving Kit Patches”) and/or your song.

      Creating an empty Kit Patch
      To “initialize” the settings in the Kong, select “Reset Device” from the Edit menu or the device context menu. This re-
      moves all samples for all drum sound channels, and sets all parameters to their default values.

      Saving Kit Patches
      Saving patches is done in the same way as with any other Reason device - see “Loading patches” and “Saving
      patches”.
      !   Note that you don't have to save any of the 16 individual Drum patches first if you don’t want to - all settings for
          each individual Drum patch are included in the Kong Kit patch.

      Pad Settings
      In the Pad Settings section to the right of the Pad section you can perform various assignments and tricks pertaining
      to how the Drum channels should be controlled from the Pads.

      Assigning Drums to Pads
      Kong features 16 pads and 16 Drum channels, as described earlier. Each pad can control a separate Drum sound
      channel. You can also assign several pads to control a single Drum sound channel. This is especially useful if you
      want to apply different settings, like Hit Types (see “Assigning Hit Type to Pads”), for each pad so that the controlled
      Drum sound channel responds differently. By default the 16 pads are assigned to their corresponding Drum sound
      channel; Pad 1 to Drum 1 and so on. If you want to change this assignment, proceed as follows:
      1. Select the desired Drum sound channel by clicking on its corresponding pad - or on the Pad name below the
         pad if you don’t want the pad to trigger the sound.
        A blue frame surrounds the selected pad and the corresponding Drum is displayed in the Drum section to the left.

      2. Select the other pad you want to control Drum 1 from.
        In this example, we select Pad 2.

      3. Click on button 1 in the Drum Assignment section to assign Pad 2 to Drum 1.

        Now, Pad 2 is also assigned to play Drum 1. Below Pad 2 it now says “Drum 1” to indicate the current assignment.

      Assigning Drums to Pads using the Quick Edit function
      If you want to assign several Drums to several pads quickly, you can do this by using the Quick Edit function.
      1. Click the Quick Edit button in the Drum Assign section.

          Each Pad now shows the current Drum assignment.
      2. Change the Drum assignment clicking on the desired Drum channel number on each Pad.
      3. When you are done, click the Quick Edit button or press [Esc] to exit to normal mode.

      Renaming Pads
      D   Double click on the Pad name below the corresponding Pad, enter a new name and press [Enter].

      Copying & Pasting Drums between Pads
      It’s possible to copy a Pad with an assigned Drum and paste into another Pad location:
      1. Select the source Pad.
      2. Press [Ctrl](Win)/[Cmd](Mac)+[C].
          Alternatively, select “Copy Drum Patch” from the Edit menu or context menu.
      3. Select the destination Pad.
      4. Press [Ctrl](Win)/[Cmd](Mac)+[V].
          Alternatively, select “Paste Drum Patch” from the Edit menu or context menu.
      Now, the complete Drum patch has been duplicated to the destination Pad and you can begin editing it as a separate
      patch.

      Assigning Hit Type to Pads
      If you have assigned several pads to the same Drum sound channel, you can choose a different Hit Type for each of
      the pads (where applicable). Depending on Drum sound type, some of the sounds can have up to four pre-defined Hit
      Types. These Hit Types are shown in the Hit Type display.

      For example, a Synth Hi-Hat Drum sound has four Hit Types by default: “Closed”, “Semi-Closed”, “Semi-Open” and
      “Open”. By selecting a different Hit Type for each of the pads assigned to the same Drum, you can create a very nice
      and “live” sound.

      D   To assign a Hit Type to a pad, select the pad and then select Hit Type by clicking the Hit Type button (or on the
          name in the display).
          The Hit Type assignment is saved when you save your Kong Kit Patch and/or song.

      Assigning Hit Type to Pads using the Quick Edit function
      A quicker way of assigning Hit Type to several pads is by using the Quick Edit function.
      1. Click the Quick Edit button in the Hit Type section.

          Each Pad now shows the current Hit Type assignment.
      2. Change the Hit Type assignment clicking on the desired Hit Type number on each Pad.
      3. When you are done, click the Quick Edit button or press [Esc] to exit.

      Muting and Soloing Pads

      D   Click the Mute button to mute the assigned Drum for the selected Pad.
          This will also mute MIDI control of the assigned Drum. Muted pads are displayed in red color.
      D   Click the Solo button to solo the assigned Drum for the selected Pad.
          Soloed pads are displayed in green color. All other pads are automatically muted. This also affects MIDI control of
          the Drum channels.
      D   Click the CLR button to remove all Mute and Solo assignments.

      Muting and Soloing Pads using the Quick Edit function
      A quicker way muting and soloing several pads is by using the Quick Edit function.
      1. Click the Quick Edit button at the top of the Pad Settings section.

          Each Pad will now show a Mute and Solo button.
      2. Click the Mute and/or Solo buttons on the desired Pads.
      3. When you are done, click the Quick Edit button to exit.

      Working with Pad Groups

      Kong features 9 Pad Groups, divided into 3 Mute Groups, 3 Link Groups and 3 Alt Groups. Each Pad can be as-
      signed to one or more of these 9 Pad Groups independently. Pad Groups are useful if you, for example, want to trig-
      ger several pads from a single pad, have one pad mute another, or randomly trigger other pads from one pad.

      Mute Groups
      Mute Groups can be used if you want one pad to automatically mute another sound in the same Mute Group. For ex-
      ample, if you assign an open hi-hat and a closed hi-hat sound to the same Mute Group, playing on one pad will auto-
      matically mute the sound assigned to the other pad.

      Link Groups
      Pads assigned to the same Link Group will play together when you trigger any of the pads in that group.

      Alt Groups
      If you play pads assigned to the same Alt Group, the pads will be triggered in a random fashion, one by one. It doesn’t
      matter which pad you play in the group, the pad triggering is always random.

      Assigning Pads to Pads Groups using the Quick Edit function
      A quicker way of assigning several pads to Pad Groups is by using the Quick Edit function.
      1. Click the Quick Edit button in the Pad Group section.

        Each Pad now shows the current Pad Group assignment.
      2. Edit the Pad Group assignment by clicking on the desired Pad Group letter on each Pad.

        In the picture above, Pads 9 and 10 are assigned to Alt Group “G”, which means they will trigger alternating when
        you play any of these Pads.
        Pads 11 and 12 are assigned to Mute Group “B”, which means that playing Pad 11 will mute Pad 12 and vice
        versa.
      3. When you are done, click the Quick Edit button or press [Esc] to exit.

      The Drum and FX section

                                                    Drum Control Panel

                                                        Drum Module Slot

                                                            FX1 Slot              Bus FX Slot

                                                                       FX2 Slot              Master FX Slot


=== END OF PART ===
