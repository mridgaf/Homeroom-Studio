# Chapter 09: Reason 12 manual digest and studio workflow
## Part 68 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 59 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 69 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 59 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 28: Redrum Drum Computer

Redrum Drum
Computer

      Introduction

      At first glance, Redrum looks styled after pattern-based drum machines, like the legendary Roland 808/909 units. In-
      deed, it does have a row of 16 step buttons that are used for step programming patterns, just like the aforementioned
      classics. There are significant differences, however. Redrum features ten drum “channels” that can each be loaded
      with an audio file, allowing for completely open-ended sound possibilities. Don’t like the snare - just change it. Com-
      plete drum kits can be saved as Redrum Patches, allowing you to mix and match drum sounds and make up custom
      kits with ease.
      In addition, Redrum also has sampling capability. This means that you can sample your own sounds straight into each
      of the ten drum channels with just a click of a button!

      Sampling in Redrum
      The sampling procedure is generic for all devices that can sample (NN-19, NN-XT, Redrum and Kong). The sampling
      and sample editing procedures are described in detail in the “Sampling” chapter.
      D   To sample your own sound and automatically load it into a drum channel in the Redrum device, click the Sam-
          ple button for the desired drum channel.

          Refer to the “Sampling” chapter for details on how to set up and use the sampling feature.

      About file formats
      Redrum reads two basic types of files:

      Redrum Patches
      A Redrum patch (Windows extension “.drp”) contains all settings for all ten drum sound channels, including file refer-
      ences to the used drum samples (but not the actual drum samples themselves). Switching patches is the same as se-
      lecting a new drum kit.

      Drum Samples
      The audio file format support differs depending on which computer OS you are using.
      Redrum can read audio files in the following formats:
      • In Windows:
        .wav, .aif, .mp3, .aac, .m4a and .wma.
      • In macOS:
        .wav, .aiff, .3g2, .3gp, .mp1, .mp2, .mp3, .mpeg, .mpa, .snd, .au, .sd2, .ac3, .aac, .adts, .amr, .caf, .m4a .m4r and .mp4.
      • SoundFonts (.sf2)
        SoundFonts are an open standard for wavetable synthesized audio, developed by E-mu systems and Creative
        Technologies.
      • REX file slices (.rx2, .rex, .rcy)
        REX files are music loops created in the ReCycle program or when editing audio clips inline in Reason (see
        “Bounce Clip to REX Loop”). Redrum lets you load separate slices from REX files as individual samples.
      • Any sample rate and practically any bit depth.

      Using patches
      When you create a new Redrum device it is loaded with a default kit. If you like you can program a pattern and play
      back using the default kit - or you can load another Redrum patch (or create one from scratch, by loading individual
      drum samples). A Redrum patch contains settings for the ten drum sound channels, complete with file references to
      the drum samples used.
      !   Redrum patterns are not part of the patch! If you want to save Redrum patches complete with patterns, create
          a Combinator containing the Redrum and save the Combi patch.

      Loading a patch
      To load a patch, use one of the following methods:
      D   Use the Browser to locate and load the desired patch.
          To open the browser and set browse focus to the Redrum device, select “Browse Redrum Patches” from the Edit
          menu or device context menu, or click the folder button in the patch section on the device panel.

      D   Once you have selected a patch, you can step between all the patches in the same folder by using the arrow
          buttons next to the patch name display.
      D   If you click on the patch name display on the device panel, a pop-up menu will appear, listing all patches in the
          current folder.
          This allows you to quickly select another patch in the same folder, without having to step through each one in turn.
      D   Drag a Redrum (.drp) patch from the Browser and drop on the device panel.
          The panel is dimmed in orange and a Patch Replace symbol appears in the center.

      Checking the sounds in a patch
      There are two ways you can listen to the sounds in a patch without programming a pattern:
      D   By clicking the Trigger (arrow) button at the top of each drum sound channel.

      D   By playing the keys C1 to A1 on your MIDI keyboard.
          C1 plays drum sound channel 1 and so on. See also “Using Redrum as a sound module”.
      Both these methods play back the drum sample for the corresponding drum sound channel, with all settings for the
      sound applied.

      Creating a new patch
      To create a patch of your own (or modify an existing patch), you use the following basic steps:
      1. Click the folder button for a drum sound channel.
          The Redrum sample browser opens.

      2. Locate and load a drum sample.
          You will find a large number of drum samples in the Factory Sound Bank (in the folder Redrum Drum Kits/xclusive
          drums-sorted). You can also load other samples in any supported format.
      D   Alternatively, drag a sample file from the Browser and drop on the desired sound channel section.
          The sound channel is dimmed in blue and a Sample Replace symbol appears in the center.
      3. Make the desired settings for the drum sound channel.
          The parameters are described in “Redrum parameters”.
      4. Repeat steps 1 and 3 for the other drum sound channels.
      5. When you’re satisfied with the drum kit, you can save the patch by clicking the Floppy Disk button in the patch
         section on the device panel.
          Note however, that you don’t necessarily need to save the patch - all settings are included when you save the
          song.

      Loading REX file slices
      Loading slices from within a REX file is done much in the same way as loading “regular” samples:
      1. Open the Browser as described above.
      2. Browse to a REX file.
          Possible extensions are “.rx2”, “.rex” and “.rcy”.
      3. Unfold the REX file.
          The browser will now display a list of all the separate slices within the REX file.
      4. Select the desired slice and click the Load button in the Browser.
          The slice is loaded into the Redrum.
      D   Alternatively, drag a REX slice file from the Browser and drop on the desired sound channel section.
          The sound channel is dimmed in blue and a Sample Replace symbol appears in the center.

      Creating an empty patch
      To “initialize” the settings in the Redrum, select “Reset Device” from the Edit menu or the device context menu. This
      removes all samples for all drum sound channels, and sets all parameters to their default values.

      Programming patterns
      Pattern basics
      Redrum contains a built-in pattern sequencer. Unlike the main sequencer in Reason, the Redrum sequencer repeat-
      edly plays back a pattern of a specified length. The typical analogy in the “real world” is a drum machine which plays
      drum patterns, usually one or two bars in length.
      Having the same pattern repeat throughout a whole song may be fine in some cases, but most often you want some
      variations. The solution is to create several different patterns and program pattern changes (automatic switching from
      one pattern to another) at the desired positions in the song.

      How the Redrum pattern sequencer integrates with the main sequencer
      The built-in pattern sequencer in the Redrum interacts with the main Reason sequencer in the following ways:
      D   The tempo set on the transport panel is used for all playback.
          If the Tempo track (see “Recording tempo automation”) is used, Redrum will follow this.
      D   If you start playback for the main sequencer (on the transport panel), the Redrum will automatically start as
          well (provided the pattern sequencer hasn’t been disabled - see below).
      D   You can mute and solo Redrum tracks in the sequencer.
          If the Redrum has a track in the sequencer and you mute this track, Redrum will automatically be muted as well.
          This is indicated by a Mute indicator on the device panel. If there are several note lanes on the Redrum track, their
          respective mute status will not be indicated on the device panel.

          This Redrum device is muted.
      D   You can also run Redrum separately (without starting the main sequencer) by clicking the Run button on the
          device panel.
          This starts the built-in pattern sequencer in the device. To stop playback, click the Run button again or click the
          Stop button on the Transport panel.

          The Run button on the Redrum.
      D   If you are running Redrum separately and start playback of the main sequencer, the pattern device will auto-
          matically restart in sync with the sequencer.

      D   Pattern changes can be controlled by pattern change events in the main sequencer.
          In other words, you can record or create pattern changes in the main sequencer, and have them occur at the cor-
          rect position on playback.
      D   The sound sources can also be played by the main sequencer, or via MIDI.
          You can combine the built-in pattern playback with playback from the main sequencer or via MIDI. For example,
          this allows you to add variations or fills to a basic pattern.
          It is also possible to disable the pattern sequencer totally, converting the device to a pure sound module. This is
          done by deactivating the Enable Pattern Section switch.

      Selecting patterns
      The Redrum has 32 pattern memories, divided into four banks (A, B, C, D).

      The Bank and Pattern buttons for the Redrum pattern sequencer.
      D   To select a pattern in the current bank, click on the desired Pattern button (1-8).
          If you like, you can assign computer key commands and/or MIDI messages to pattern selection.
      D   To select a pattern in another bank, first click the desired Bank button (A, B, C, D) and then click the Pattern
          button.
          Nothing happens until you click the Pattern button.
      D   If you select a new pattern during playback, the change will take effect on the next downbeat (according to the
          time signature set in the transport panel).
          If you automate pattern changes in the main sequencer, you can make them happen at any position - see “Record-
          ing pattern automation”.
      D   Note that you cannot load or save patterns - they are only stored as part of a song.
          However, you can move patterns from one location to another (even between songs) by using the Cut, Copy and
          Paste Pattern commands.

      Pattern tutorial
      If you are unfamiliar with step programming patterns, the basic principle is very intuitive and easy to learn. Proceed as
      follows:

      1. Load a Redrum patch, if one isn’t already loaded.
      2. Make sure an empty pattern is selected.
        If you like, use the Clear Pattern command on the Edit menu or device context menu to make sure.
      3. Make sure that the “Enable Pattern Section” and the “Pattern” buttons are activated (lit).

      4. Press the “Run” button.
        There will be no sound, as no pattern steps have been recorded yet. But as you can see, the LEDs over the Step
        button light up consecutively, moving from left to right, and then starts over. Each Step button represents one
        “step” in the Pattern.
      5. Select a Redrum channel, by clicking the “Select” button at the bottom of the channel.
        The button lights up, indicating that this channel and the drum sound it contains is selected.

      6. While in Run mode, press Step button 1, so that it lights up.
        The selected sound will now play every time Step 1 is “passed over”.
      7. Clicking other Step buttons so they light up will play back the selected sound as the sequencer passes those
         steps.
        Clicking on a selected (lit) step button a second time removes the sound from that step and the button goes dark
        again. You can click and drag to add or remove steps quickly.
      8. Select another Redrum channel to program steps for that sound.
        Selecting a new sound or channel also removes the visual indications (static lit buttons) of step entries for the pre-
        viously selected sound. The step buttons always show step entries for the currently selected sound.
      9. Continue switching between sounds, and programming steps to build your pattern.
        Note that you can erase or add step entries even if Run mode isn’t activated.

      Setting pattern length
      You may want to make settings for Pattern length, i.e the number of steps the pattern should play before repeating:

      D   Use the “Steps” spin controls to set the number of steps you wish the pattern to play.
          The range is 1 to 64. You can always extend the number of steps at a later stage, as this will merely add empty
          steps at the end of the original pattern. You could also make it shorter, but that would (obviously) mean that the
          steps “outside” the new length won’t be heard. These steps aren’t erased though; if you raise the Steps value
          again, the steps will be played back again.

      About the “Edit Steps” Switch
      If you set the pattern length to more than 16 steps, the pattern steps following after the 16th won’t be visible, al-
      though they will play back. To view and be able to edit the next 16 steps, you have to set the Edit Steps switch to 17-
      32. To see and edit steps beyond 32 you set the switch to 33-48, and so on.

      Setting pattern resolution

      Redrum always follows the tempo setting on the transport panel, but you can also make Redrum play in different
      “resolutions” in relation to the tempo setting. Changing the Resolution setting changes the length of each step, and
      thereby the “speed” of the pattern.

      Step dynamics
      When you enter step notes for a drum sound, you can set the velocity value for each step to one of three values:
      Hard, Medium or Soft. This is done by setting the Dynamic switch before entering the note.

      The color of the step buttons reflect the dynamics for each step. Soft notes are light yellow, Medium notes are orange and Hard are red.
      D   When the Medium value is selected, you can enter Hard notes by holding down [Shift] and clicking.
          In the same way, you can enter Soft notes by holding down [Option] (Mac) or [Alt] (Windows) and clicking. Note
          that this doesn’t change the Dynamic setting on the device panel - it only affects the notes you enter.
      D   When you use different dynamics, the resulting difference in the sound (loudness, pitch, etc.), is governed by
          the “VEL” knob settings for each drum channel (see “Redrum parameters”).
          If no velocity amount is set for a drum channel, it will play back the same, regardless of the Dynamic setting.
      D   To change the dynamics for an already programmed step, set the switch to the dynamic value you wish to
          change it to and click on the step.
      !   Note that if you are triggering Redrum via MIDI or from the main sequencer, the sounds will react to velocity
          like any other audio device. The Dynamic values are there to offer velocity control when using the built-in pat-
          tern sequencer.

      Pattern Shuffle
      Shuffle is a rhythmic feature, that gives the music a more or less pronounced swing feel. It works by delaying all six-
      teenth notes that fall in between the eighth notes. You can activate or deactivate shuffle individually for each Redrum
      pattern by clicking the Shuffle button on the device panel.

      The amount of shuffle is set globally with the Global Shuffle control in the ReGroove Mixer - see “The ReGroove
      Mixer”.

      Flam

      A flam is when you double-strike a drum, to create a rhythmic or dynamic effect. Applying flam to a step entry will add
      a second “hit” to a drum sound. The flam amount knob determines the delay between the two hits.
      To add a flam drum note, proceed as follows:
      1. Activate flam by clicking the Flam button.
      2. Click on a step to add a note (taking the Dynamic setting into account as usual).
          A red LED is lit above the step to indicate that flam will be applied to that step.
      3. Use the Flam knob to set the desired amount of flam.
          The flam amount is global for all patterns in the device.
      D   To add or remove flam to or from an existing step note, click directly on the corresponding flam LED.
          You can also click and drag on the LEDs to add or remove several flam steps quickly.
      D   Applying flam to several consecutive step entries is a quick way to produce drum rolls.
          By adjusting the Flam knob you can create 1/32 notes even if the step resolution is 1/16, for example.

      The Pattern Enable switch

      If you deactivate the “Pattern” button the pattern playback will be muted, starting at the next downbeat (exactly as if
      you had selected an empty (silent) pattern). For example, this can be used for bringing different pattern devices in
      and out of the mix during playback.
      q   You can also mute Redrum devices in the sequencer using the Mute button for the track connected to the
          Redrum. If you do so, this will mute the Redrum output instantly, and the Mute indicator on the Redrum panel
          lights up. Note that all tracks connected to this Redrum device must be muted for this to work.

      The Mute indicator

      The Enable Pattern Section switch

      If this is off, Redrum will function as a pure “sound module”, i.e. the internal Pattern sequencer is disengaged. Use this
      mode if you wish to control Redrum exclusively from the main sequencer or via MIDI (see “Using Redrum as a sound
      module”).

      Pattern functions
      When a Redrum device is selected, you will find some specific pattern functions on the Edit menu (and on the device
      context menu):

      | Function                       | Description
      Shift Pattern Left/Right         These functions move all notes in the pattern one step to the left or right.
      Shift Drum Left/Right            The Shift Drum functions move all notes for the selected drum channel (the channel for
                                       which the Select button is lit) one step to the left or right.
      Randomize Pattern                Creates a random pattern. Random patterns can be great starting points and help you get
                                       new ideas.
      Randomize Drum                   Creates a random pattern for the selected drum sound only - the notes for the other
                                       drum sound channels are unaffected.
      Alter Pattern                    The Alter Pattern function modifies the selected pattern by “shuffling” the current pattern
                                       notes and redistributing them among the drum sounds at random. This creates a less
                                       chaotic pattern than the “Randomize Pattern” function.
                                       Note that there must be something in the pattern for the function to work on - using an
                                       Alter function on an empty pattern will not do anything.
      Alter Drum                       Works like the “Alter Pattern” function, but affects the selected drum sound only.

      Chaining patterns
      When you have created several patterns that belong together, you most probably want to make these play back in a
      certain order. This is done by recording or inserting pattern changes into the main sequencer. See “Recording pattern
      automation”.

      Converting Pattern data to notes in the main sequencer
      You can convert Redrum Patterns to notes in the main sequencer. This allows you to edit the notes freely, create vari-
      ations or use Groove quantizing.

      The “Copy Pattern to Track” function
      This function is useful when you have created a single pattern in the Redrum device and want to render individual
      note events on the sequencer track. You could also use this if you e.g. have created a drum pattern and want to have
      the pattern play back some other type of device.
      Proceed as follows:
      1. Set the Left and Right Locators to encompass the section you want to “fill” with the notes in the pattern.
          You may want to make sure that the space between the locators is a multiple of the pattern length, to avoid “cut-
          ting off” the pattern.
      2. Select the device in the rack and select “Copy Pattern to Track” from the Edit menu or the device context menu.
          The pattern is converted to a single note clip on the track (see the notes below). If the space between the locators
          is greater than the pattern length, the pattern will be repeated in the clip to fill up the space.

          An internal Redrum drum pattern converted to note events on the track
      When you use the “Copy Pattern to Track” function with the Redrum, you should note the following:
      • The notes will have the pitch of the corresponding drum sound (see “Using Redrum as a sound module”) and
        the velocity depending on the “Dynamic” parameter value in the device.
          “Soft” notes get velocity 30, “Medium” notes get velocity 80 and “Hard” notes get velocity 127.
      • You probably want to turn off the “Enable Pattern Section” switch on the Redrum device panel.
          Otherwise, the drum sounds will be double-triggered during playback (by the pattern section itself, and by the ren-
          dered notes on the sequencer track).

      The “Convert Pattern Automation to Notes” function
      If you have recorded or drawn pattern changes on a Redrum track, you can have the whole track converted to notes,
      in the following way:
      1. Select the track with the pattern automation.
      2. Select “Convert Pattern Automation to Notes” from the Edit menu or the context menu for the track.
          For each pattern clip, the corresponding pattern is converted to note clips on the track (following the same rules as
          for the “Copy Pattern to Track” function). The track will play back just the same as when you played the pattern de-
          vice with the pattern changes.
      D   After the operation, the Pattern Select lane is switched off.
          The “Enable Pattern Section” button on the device is automatically turned off.

      Redrum parameters
      Drum sound settings
      Redrum features ten drum sound channels that can each be loaded with a Wave or AIFF sample or a sample from a
      SoundFont bank. Although they are basically similar, there are three “types” of drum sound channels, with slightly dif-
      ferent features. This makes some channels more suitable for certain types of drum sounds, but you are of course free
      to configure your drum kits as you like.
      On the following pages, all parameters will be listed. If a parameter is available for certain drum sound channels only,
      this will be stated.

      Mute & Solo

      At the top of each drum sound channel, you will find a Mute (M) and a Solo (S) button. Muting a channel silences its
      output, while Soloing a channel mutes all other channels. Several channels can be muted or soloed at the same time.
      You can also use keys on your MIDI keyboard to mute or solo individual drum sounds in real time.
      D   The keys C2 to E3 (white keys only) will mute individual drum channels starting with channel 1.
          The sounds are muted for as long as you hold the key(s) down.
      D   The keys C4 to E5 (white keys only) will solo individual drum channel, starting with channel 1.
          The sounds are soloed for as long as you hold the key(s) down.
          C2                  C3                    C4                     C5

           1   2 3 4 5 6 7 8 9 10                     1 2 3 4 5 6 7 8 9 10

                     Mute                                        Solo

      This is a great way to bring drum sounds in and out of the mix when playing Reason live. You can also record the
      drum channel Mutes in the main sequencer, just like any other controller (see “Recording parameter automation”).

      The Effect Sends (S1 & S2)

      On the back panel of Redrum you will note two audio connections labeled “Send Out” 1 and 2. When you create a
      Redrum device, these will by default be auto-routed to the first two “Chaining Aux” inputs on the Mixer device (pro-
      vided that these inputs aren’t already in use).
      This feature allows you to add effects to independent drum sounds in the Redrum.

      D   Raising the S1 knob for a drum sound channel will send the sound to the first send effect connected to the
          mixer.
          Similarly, the S2 knob governs the send level to the second send effect in the mixer.
      D   Note that there must be send effects connected to the AUX Sends and Returns in the mixer for this to work.

      D   Also note that if Redrum is soloed in the Mixer the effect sends will be muted.

      D   Another way to add independent effects to drum sounds is to use the independent drum outputs.
          See “Connections”.

      Pan


=== END OF PART ===
