# Chapter 09: Reason 12 manual digest and studio workflow
## Part 55 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 46 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 56 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 46 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 21: Sampling

Sampling

      About this chapter
      This chapter describes how you can sample, edit samples and manage your samples in your songs. For more infor-
      mation about the specific devices that can sample and play back samples, please refer to the “NN-XT Sampler”, “NN-
      19 Sampler”, “Redrum Drum Computer”, “Kong Drum Designer”, “RV7000 Mk II Advanced Reverb”, “Europa Shape-
      shifting Synthesizer”, “Grain Sample Manipulator” and “Mimic Creative Sampler” chapters.

      Overview
      The sampling feature allows you to sample external audio (or internally from the outputs of any device) and use in any
      of the Reason devices that support sample files.

      One-click sampling
      The sampling workflow has been designed to be as quick and easy as possible, so you don’t lose any inspiration. Re-
      gardless which device you use when sampling - NN-XT, NN-19, Redrum, Kong, Europa, Grain, Mimic or RV7000 Mk
      II - sampling can be instantly accessed by simply clicking, or by clicking and holding the Sampling button(s) on these
      devices:

      Sampling buttons on NN-XT, NN19, Redrum and Kong respectively.
      See “Sampling procedure” for more details on how to sample.

      The Edit Sample window
      All sampling parameters and functions are controlled from one single window - the Edit Sample window. This window
      is used when you’re editing samples in any of the devices described above, See “Editing samples” for more details.

      The Edit Sample window with a sample.

      About sample format, rate and resolution
      Whenever you sample in Reason, the resulting audio files are stored in WAV format. The sample rate is determined
      by the settings on the Audio tab in Preferences (see “Audio settings”). The resolution (bit depth) is fixed at 16 bits.
      Reason is totally agnostic about what sample rate you use. If you like, you can change the sample rate at any time
      without affecting the pitch, playback speed etc. of your samples. What you have once sampled will always sound the
      same, regardless of the current audio settings.

      General sampling functions
      Setting up for sampling
      If you want to sample external audio, e.g. from a mic or an instrument connected to the audio hardware on your com-
      puter, make sure you have set up the desired audio input(s) on the Audio tab in Preferences, see “Active input and
      output channels”. Available audio inputs are indicated with yellow or green LEDs on the Hardware Interface in the
      rack:

      Selecting audio input source(s)
      To set up for sampling, you first need to make some connections on the Hardware Interface:
      1. Navigate to the Hardware Interface and press [Tab] to flip the rack around.
      2. Patch cables to the Sampling Inputs as follows:
      D   To sample external audio, connect the desired Audio Input connector(s) to the Sampling Input connector(s) to
          the left on the rear of the Hardware Interface.
      D   To sample the audio of a device in the rack, connect cables from the audio output(s) of the device to the Sam-
          pling Input connector(s) on the Hardware Interface.
      • To sample in stereo, connect to both the Left and Right Sampling Input connectors.
      • To sample in mono, connect only to the Left or Right Sampling Input connector.

          Audio Inputs 1&2 connected to Sampling Inputs L&R for sampling in stereo.

      Setting audio input level
      Once you have made the desired connections to the Sampling Input(s) on the Hardware Interface, it’s important to
      check the audio input level to avoid clipping. If you are going to sample external audio via the audio hardware of your
      computer, you have to adjust the level at the source, i.e. on the pre-amp of the audio hardware (or connected instru-
      ment). A good suggestion is to use the Big Meter on the Hardware Interface to be able to monitor the input level(s)
      more easily.
      D   Adjust the level at the source and make sure the level doesn’t exceed 0 dB to avoid clipping.

      D   If you sample internally, from the output(s) of a device in the rack, adjust the Output Level on the source device
          and check the levels with the Sampling Inputs selected on the Big Meter:

      Monitoring and Monitor Level
      To the left on the Hardware Interface are two buttons and one knob for monitoring the signals on the Sampling In-
      puts:

      D   Click the Monitor button to activate monitoring of the signals present at the Sampling Inputs.
          Monitoring will always be active, regardless of if you sample or not.
      D   Click the Auto button to activate monitoring only during sampling.
          Monitoring will only be active during the actual sampling. When you don’t sample, monitoring will be off.
      D   Turn the Monitor knob to adjust the monitor signal level.
      !   The Monitor Level knob does not affect the level of the audio to be sampled - only the monitored signal.

      Sampling
      The Sample buttons
      The NN-XT, NN19, Redrum, Kong, Grain and RV7000 Mk II devices feature one or several Sample buttons. The
      Sample buttons are located on the devices as follows:

      Sampling buttons on NN-XT, NN19, Redrum and Kong respectively.

      Sampling procedure
      1. Make sure you have made the necessary connections and set the levels according to the descriptions in “Set-
         ting up for sampling”.
      2. Click the Sample button on the device you want to sample to.
      D   Alternatively, click and hold the Sample button depressed for as long as you want to sample.
          When you use the “click and hold” method, sampling will be automatically terminated as soon as you release the
          mouse button. The sample will then end up in the device and in the Song Samples location in the Browser.
      !   If you’re sampling into a Redrum, make sure you click/hold the Sample button for the desired drum channel.
          A waveform display shows up with a moving “play head”:

                       Play head

      3. Start playing or singing what you want to sample.
          As soon as any audio is present on the Sampling Inputs on the Hardware Interface, the waveform display will indi-
          cate this by drawing a wave.
      !   The buffer size for sampled audio is 30 seconds. After 30 seconds, the play head will start over again from the
          beginning and start erasing any previously sampled audio.

      D   If you want to restart the sampling manually, click the Restart Sampling button:

          The “Restart Sampling” button.
          This will erase any sampled audio and force the play head to restart from the beginning.
      !   Note that you cannot restart sampling this way if you use the “click and hold” sampling method.
      4. When you’re satisfied with your recording, click the Stop Sampling button in the waveform display.

          The “Stop Sampling” button.
      The waveform display closes and the sample automatically ends up in the device, where you can play it back instantly:

      By default, the sample is named “Sample ‘n’” where ‘n’ is a serial number. As you will notice, any silence preceding the
      actual audio in the sample will be automatically disregarded. The entire sample is preserved, but this is done so you
      won’t have to edit the sample start before playback.

      Besides ending up in the device, the sample is also placed under the corresponding device icon in the Assigned
      Samples folder in the Song Samples location in the Browser:

      Here, all samples you use in your song are listed (see “The Song Samples location”). Here is also where you can open
      samples for editing (see “Editing samples”).

      The Song Samples location
      The Song Samples location in the Browser is where all samples in your song are listed and can be accessed for pre-
      view and editing purposes. Besides your own samples, all Factory samples and any ReFills samples used in the song
      are also accessible for previewing and editing!

      The Song Samples location in the Browser.

      The Song Samples location in the Browser contains the following items:
      • Assigned Samples folder
        Here, all samples that are assigned to devices in the song are listed. All devices that contain assigned samples are
        listed as “sub-folders”. Each device “sub-folder” shows the samples currently assigned to it. See “Assigned Sam-
        ples” for more details.
      • Unassigned Samples folder
        If you remove a sound you have sampled from a device, the sound is automatically moved from the Assigned Sam-
        ples folder to the Unassigned Samples folder. From here you can load the sample into other devices if you like.
        See “Unassigned Samples” for more details.
      • All Self-contained Samples folder
        All sounds you have sampled yourself, plus any duplicated samples from the Factory Soundbank and/or ReFills,
        automatically becomes self-contained and are always stored with the song. These samples are listed in the All
        Self-contained Samples folder. See “About self-contained samples” for more details.
      • Edit button
        Click the Edit button to open the selected sample for editing in the Edit Sample window (see “The Edit Sample
        window”).
      • Import button
        Click this button to import the selected sample(s) to audio tracks in the sequencer.
      • Play and Auto buttons
        To audition a sample, select it in the Browser list and click the Play button. If you click the Auto button, simply se-
        lecting a sample in the list will automatically play it back.
      • Volume slider
        Adjust the preview volume of the sample with the slider. This does not affect the samples original volume.
      The context menu of a selected sample contains the following functions:
      • Edit Sample
        Select this to open the sample for editing in the Edit Sample window (see “The Edit Sample window”). If several
        samples are selected, this item is grayed out.
      • Duplicate Sample(s)
        Select this to create a duplicate of the selected sample. The duplicated sample is placed in the All Self-contained
        Samples and Unassigned Samples folders. Several selected samples can be duplicated in one go. See “Duplicat-
        ing samples” for more details.
      • Export Sample(s)
        Select this to export the selected sample to disk. A dialog appears where you can select file format. Note that it is
        not possible to export samples from the Factory Soundbank or from ReFills. Several selected samples can be ex-
        ported in one go. See “Exporting samples” for more details.
      • Delete Sample(s)
        Select this to permanently delete the selected sample(s) from the song. Note that samples from the Factory
        Soundbank and from ReFills will not be deleted from their original locations - only from the song document. Sev-
        eral selected samples can be deleted in one go. See “Deleting samples from a song” for more details. Any samples
        you have recorded yourself will be permanently erased unless you have previously exported them to disk (see “Ex-
        port Sample(s)” below).

      Editing samples
      The Edit Sample window
      Any sample present in the All Self-contained Samples folder in the Song Samples location in the Browser can be ed-
      ited.

      D   Select a sample in the Browser list and click the Edit button to open the sample in the Edit Sample window:

          The Edit Sample window with an open sample.

      The Edit Sample window can be resized in all directions by clicking and dragging the window frame. If you resize the
      window vertically, the displayed waveform will be resized vertically as well.
      • Undo and Redo buttons
        The Undo and Redo buttons work like the regular undo and redo functions in the main window menu, but these
        are used locally only for the Sample Edit window. The number of Undo and Redo steps in the Sample Edit window
        are limited to 10. Once you have clicked the Save button, you can still undo the entire sample editing procedure by
        using the Undo function in the main window.
      • Crop button
        Click the Crop button to crop the sample so that only the content between the Start (S) and End (E) locators is
        preserved. The rest of the sample will be permanently deleted. See “Cropping samples” for more info.
      • Normalize button
        Click the Normalize button to amplify the entire sample so that the loudest peak touches 0 dB. Note that the entire
        sample is normalized, regardless of any locator settings. See “Normalizing samples” for more info.
      • Reverse button
        Click the Reverse button to reverse (play backward) the entire sample. Note that the entire sample is reversed, re-
        gardless of any locator settings. See “Reversing samples” for more info.
      • Fade In and Fade Out buttons
        The Fade In and Fade Out buttons can be used to apply a fade in or fade out of the sample volume. See “Fading
        in/out samples” for more info.
      • Loop Mode buttons
        Click one of the Loop Mode buttons to select loop type. The default (leftmost) setting is “no loop”. Then follow
        “Loop Forward” and “Loop Forward + Backward”. See “Looping samples” for more info.
      • Waveform pane
        Here, the currently open sample is displayed as one (mono) or two (stereo) waveforms. The Start (S) and End (E)
        locators are also displayed. By default the Start locator is placed where the audio begins in the sample. This means
        that if you have started sampling before there were any audio present, the playback will automatically start where
        the audio begins. This way you won’t have to manually move the Start locator in most situations.
      • Waveform Navigator
        Below the waveform pane is the horizontal Waveform Navigator. This can be operated in the same way as the
        Song Navigator in the sequencer (see “Scrolling with the Navigators and scrollbars”, “Zooming horizontally in the
        Sequencer” and “Scrolling and zooming using a wheel mouse”).
      • Set Sample Start/End button
        Set the desired sample playback region by clicking and dragging on the waveform pane. Then, click the Set Sam-
        ple Start/End button to automatically place the Start and End locators at the beginning and end of the sample re-
        gion. See “The Set Start/End function” for more info.
      • Snap Sample Start/End To Transients button
        Click the Snap Sample Start/End To Transients button to make the Start and End locators snap to suitable tran-
        sients in the sample as you move the locators. This makes it easier to find appropriate start and end locations for
        the sample playback.
      • Crossfade Loop checkbox
        Tick the Crossfade Loop box to introduce a crossfade in the loop. Crossfade is useful to even out any clicks in the
        loop points, especially for sounds with fairly even volume throughout the loop region. See “The Crossfade Loop
        function” for more info.
      • Set Loop button
        Set the desired loop region by clicking and dragging on the waveform pane. Then, click the Set Loop button to au-
        tomatically place the Left and Right Loop locators at the beginning and end of the loop region. See “The Set Loop
        function” for more info.

      • Play button, Solo checkbox and Volume slider
        Click the Play button to play back the sample from the current position of the play head until the end of the sample.
        As soon as playback is started the button switches to display Stop instead, giving you the option of stopping play-
        back. This is especially useful if your sample is looped. As an alternative to clicking the Play/Stop button you can
        press [Spacebar] to toggle between Play and Stop.
        Tick the Solo checkbox to solo sample playback. This is useful if your song is playing in the background and you
        only want to listen to the sample.
        Adjust the sample playback volume with the Volume slider to the right.
      • Root Key
        Set the sample Root Key (pitch) by clicking the spin controls, or by entering the desired note value in the display.
        If you know what note your sample is, select that note here. When you open the sample in a sampler device, the
        device will automatically transpose the sample correctly across the keyboard.
      • Name
        Type in desired name for your sample. Note that this will overwrite the original name of the sample in the Song
        Samples list in the Tool Window once you click Save. See “Renaming samples” for more info.
      • Save and Cancel buttons
        Click Save to save your sample. The sample will appear in the Song Samples location in the Browser. See “Saving
        edited samples” for more info.
        Click Cancel to exit the Edit Sample window and discard from any edits you’ve made in the current sample.

      Setting Sample Start and End
      1. Open the sample by selecting it in the Browser list and clicking the Edit button - or select “Edit Sample” from
         the context menu.
        The sample opens in the Edit Sample window.

        If you have recorded the sample yourself in Reason, the Start (S) locator has been automatically placed at the first
        significant transient in the sound. The play head is also automatically placed at the Start locator.

      2. If necessary, adjust the Start locator by clicking and dragging it back or forth in the Edit Sample window ruler.
          Play back the sample by clicking the Play button, or by pressing the [Spacebar].
      q   To make it easier to fine adjust the locators, it could be wise to magnify the waveform pane horizontally using
          the Waveform Navigator. The Waveform Navigator works exactly as the Song Navigator in the Sequencer - see
          “Zooming horizontally in the Sequencer” and “Scrolling and zooming using a wheel mouse”.
      D   Tick the “Snap Sample Start/End To Transients” check box if you want the locators to snap to significant tran-
          sients in the sample.
      3. Adjust the End locator by clicking and dragging it back or forth in the Edit Sample window ruler.

      The Set Start/End function
      Another way of defining a sample’s start and end positions is by using the Set Start/End function:
      1. Set the desired sample playback zone by clicking and dragging on the waveform pane.

          The defined zone is highlighted in blue color.
      2. Click the Set Sample Start/End button.

          The Start and End locators are automatically placed at the beginning and end of the defined playback zone.
      3. Click anywhere on the Waveform pane to remove the highlight.

      Cropping samples
      Cropping a sample means deleting parts you don’t want to keep, e.g. any silence in the beginning and/or in the end
      of a sample. The Crop function in the Edit Sample window deletes everything except what’s in between the Start and
      End locators, or everything outside any highlighted part of the sample. To crop a sample, proceed as follows:
      1. Set the Start and End locators where you want them - see “Setting Sample Start and End”.
          Alternatively, click and drag in the Edit Sample window to highlight the section you want to keep.
      2. Click the Crop button in the Edit Sample window.

      • If you highlighted a section by clicking and dragging in the Edit Sample window, everything except the high-
        lighted part gets permanently deleted.
      • If you didn’t highlight a section of the sample, everything before the Start locator and after the End locator
        gets permanently deleted.

      Normalizing samples
      Normalizing means amplifying the volume of the sample so that the loudest peak in the sound touches 0 dB. The
      Normalize function normalizes either the entire sample, or the highlighted part of the sample.
      1. Click and drag in the Edit Sample window to highlight the part of the sample you want to normalize.
          To normalize the entire sample, you don’t have to do anything.
      2. Click the Normalize button in the Edit Sample window.

      • If you highlighted a section of the sample, the highlighted part gets normalized.
      • If you didn’t highlight a section of the sample, the entire sample gets normalized regardless of any Locator set-
        tings.
          Since the entire sample is normalized, this means that any noise present in the sound will also be amplified.
          After the Normalize operation, the waveform is redrawn with the new volume values.
      !   Note that normalizing a sample that already use the full headroom (touches 0 dB) won’t have any effect.

      Reversing samples
      Reversing a sample means playing it backwards, from the end to the start. The Reverse function reverses either the
      entire sample, or the highlighted part of the sample.
      1. Click and drag in the Edit Sample window to highlight the part of the sample you want to reverse.
          To reverse the entire sample, you don’t have to do anything.
      2. Click the Reverse button in the Edit Sample window.

      • If you highlighted a section of the sample, the highlighted part gets reversed.
      • If you didn’t highlight a section of the sample, the entire sample gets reversed regardless of any Locator set-
        tings.
        After the Reverse operation, the waveform is redrawn with the reversed shape.

      Fading in/out samples
      Using short fades is useful if you want to remove clicks or pops in the beginning and/or end of the sample. You can
      also create longer fades to make a sound fade in and/or out nice and smoothly.
      1. Set the desired Fade In (or Fade Out) zone by clicking and dragging on the waveform pane.

        The defined zone is highlighted in blue color.
      2. Click the Fade In (or Fade Out) button.

        Clicking the Fade In button creates a fade in from complete silence at the beginning of the highlighted zone to the
        current volume at the end of the highlighted zone:

        Clicking the Fade Out button creates a fade out from the current volume at the beginning of the highlighted zone
        to complete silence at the end of the zone.
        After the Fade operation, the waveform is redrawn with the new volume values.
      3. Click anywhere on the Waveform pane to remove the highlight.

      Looping samples
      Looping a sample means playing back the sample from the start and then playing back a defined zone in the sample
      over and over again (usually for as long as a key is depressed on the MIDI master keyboard). In practice, looping sam-
      ples can be used to create “longer” sounds out of shorter ones. For example, if you have a flute sample you may want
      to loop the middle part of it so that you could make the sound sustain as for long as you like.
      There are two different loop modes available in the Edit Sample window (besides the default non-loop mode):
      • Loop Forward
          In Loop Forward mode the sample is played back from the Start locator to the Right Loop locator, then playback
          starts over from the Left Loop locator and continues to the Right Loop locator over and over again.
      • Loop Forward + Backward
          In Loop Forward + Backward mode the sample is played back from the Start locator to the Right Loop locator,
          then the playback is reversed from the Right Loop locator to the Left Loop locator and then forward again to the
          Right Loop locator over and over again.

      Adjusting the Loop locators
      1. Click the Loop Forward or Loop Forward + Backward button.

          The Left (L) and Right (R) Loop locators appear on the Waveform pane.
      2. Play back the sample and adjust the Loop locators to your liking.
          If necessary, zoom in horizontally to more easily find suitable loop positions.

      D   To make loops sound smoother, try using crossfades as described in “The Crossfade Loop function”.

      The Set Loop function
      Another way of defining a sample’s loop positions is by using the Set Loop function:
      1. Set the desired loop zone by clicking and dragging on the waveform pane.

          The defined zone is highlighted in blue color.
      2. Click the Set Loop button.
          The Left and Right Loop locators are automatically placed at the beginning and end of the defined zone.

      3. Click anywhere on the Waveform pane to remove the highlight.
      D   To make loops sound smoother, try using crossfades as described in “The Crossfade Loop function”.

      The Crossfade Loop function
      Crossfades are useful for evening out clicks or transients at the loop points, especially in sounds with fairly constant
      volume throughout the loop zone. The Crossfade Loop function creates smooth volume crossfade around the Loop
      Locators.
      D   Tick the Crossfade Loop box to automatically introduce a crossfade in the loop.

      • When the Crossfade Loop function is active, moving the Left and/or Right Loop Locators will force them to au-
        tomatically “snap” to suitable loop positions. If you move the Left Loop Locator, the Right Loop Locator will
        automatically self-adjust to a suitable loop position.
          This way you will quickly reach a good result.
      q   Experiment by alternating the Loop Modes between Loop Forward and Loop Forward + Backward. Just chang-
          ing Loop Mode can make the loop transitions much smoother in many situations.
      q   A general tip when trying to create a smooth loop is to locate the loop zone where the volume and timbre is
          fairly constant over time. Big changes in volume and/or timbre in the loop zone will often result in quite pro-
          nounced or strange “pulsating” loops. Also, very short loop zones often tend to sound unnatural and “static”.


=== END OF PART ===
