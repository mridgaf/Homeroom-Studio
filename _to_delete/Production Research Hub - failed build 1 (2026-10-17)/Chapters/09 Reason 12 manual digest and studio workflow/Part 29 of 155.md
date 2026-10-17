# Chapter 09: Reason 12 manual digest and studio workflow
## Part 29 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 20 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 30 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 20 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Bounce Clip(s) to New Recording(s)
      !   The function described below is exactly the same as clicking the “Bounce” button to the left in the Clip Over-
          view, see “Bounce button”.
      A very nice way to “clean up” among the recordings in a comped audio clip is to bounce the clip to a new recording.
      Bouncing to a new recording is also a prerequisite to be able to edit the clip in Slice Edit mode and stretch and quan-
      tize the audio.
      What happens is that the audio recordings in all segments of the comped clip, including any Cut Crossfades and in-
      dividual Comp Row Levels, are combined into a single recording on an additional Comp Row. After the clip has been
      bounced to a new recording, you can delete the unused recordings to reduce the file size. Bouncing clips to new re-
      cordings can be made for one or several selected audio clips:
      D   Select the clip(s) in the Clip Overview area in the Comp Editor, or select the clip(s) in the Arrange View, and
          then select “Bounce > Bounce Clip(s) to New Recording(s)” from the Edit menu or context menu.
          A new “combined” recording is created on a new Comp Row, which is created above the other Comp Rows on the
          Edit Pane. The new Comp Row is assigned the suffix “(bounced)”.

                   Select the clip in the Clip Overview.

                                                                       Select “Bounce Clip to New Recording” to create a new
                                                                       “combined” recording on an additional Comp Row.

          As the clip is bounced, the clip automatically switches from a Comp clip to a Single Take clip. If you play back the
          clip now, you will only hear the bounced recording on the automatically selected (topmost) Comp Row. However,
          the clip will sound exactly the same as before the bounce.
          If you’re happy with the result and don’t plan to edit the clip any further, you can use the “Delete Unused Record-
          ings” function to delete the recordings on the original Comp Rows and reduce the file size (see “Delete Unused
          Recordings”). If file size is not an issue, you can keep the original takes in the clip. This way you can switch to
          Comp Mode at any time if you need to edit the comp.
      q   The “Bounce Clip to New Recording” function is very useful if you have imported a large audio file and only
          want to use a part of it. You can bounce the part of the clip you want use to a new recording and then delete
          the remaining unused part on the Comp Row to reduce the file size.
      q   It’s also possible to bounce Audio Clips to disk and to a Sample - see “Bouncing Audio Clips” and “Bounce
          Clip(s) to New Sample(s)”.

      Creating a comped audio clip
      If you have recorded more than one loop cycle of audio in Loop Mode (see “Recording audio in Loop mode”), or re-
      corded over or into an existing audio clip (see “Recording over or into an existing audio clip”), each recording has
      been placed on a separate Comp Row. If you like, you can now select the best parts (segments) of the recordings on
      the various Comp Rows and create a final “comped” audio clip. All editing described below is non-destructive and can
      be changed at any time:
      1. Open the audio clip in Comp Edit mode.
          Each take has generated a separate Comp Row, each with a separate recording on it. The latest take, on the top-
          most Comp Row, is the one that will play back.

                                                                                                Audio clip (latest take)

                                                                                                Comp Rows with audio
                                                                                                recordings

          An audio clip (in Single Take Mode) with four separate takes recorded in Loop Mode.
      !   If the clip is in Single Take Mode, because a Single Take Mode button is depressed (as in the picture above),
          you will have to click that Single Take Mode button to deselect the Comp Row before you can start adding
          Cuts!
      2. Locate the best parts of the recordings in the different Comp Rows.
          Audition the recordings on the Comp Rows to decide which recordings to use at what position in the comped clip.
          Select the Speaker Tool and click-hold at desired positions on the different Comp Rows (see “Speaker Tool” for
          details).
      q   If you’re using the Selection Tool, you can temporarily switch to the Speaker Tool by holding down
          [Alt]+[Shift](Win) or [Cmd]+[Shift](Mac).

      3. Double-click with the Selection Tool on the Comp Row you want to use first in the clip.
        In this example, we decide to use the recording on the “Take 2” Comp Row:

        Double-click on the “Take 2” Comp Row to assign it to the first segment of the clip.
      4. Select the Razor Tool in the Sequencer Toolbar - or, with the Selection Tool still selected, hold down [Alt](Win)
         or [Cmd](Mac).
        We want the recording on the “Take 2” Comp Row to play until beat 3 of Bar 7. After beat 3 of bar 7 we want the
        clip to be silent to get rid of some background noise that could be heard when we recorded without playing any-
        thing. Therefore, place the Razor Tool on the Silence Row at Beat 3 of bar 7 and click:

         Place the Razor Tool on the Silence Row at                              ...and click to assign the Silence Row to the
         beat 3 of bar 7...                                                      second segment of the clip.

        Now, you have assigned the recording on the “Take 2” Comp Row from the beginning of the clip to beat 3 of bar
        7. At the same time you have assigned the Silence Row to a second segment of the clip.
      5. Use the Audition Tool to find a suitable recording to assign to a new segment in the clip.
        We found a good recording that we want to use on the “Take 4” Comp Row between beat 3 and 4 of bar 8 until
        beat 1 of bar 11.

      6. Assign a complete segment by swiping with the Razor Tool.
        Swipe with the Razor Tool on the “Take 4” Comp Row from beat 3 and 4 of bar 8 until beat 1 of bar 11:

         Place the Razor Tool between beat 3 and 4 of bar 8 on the                  ...and release at beat 1 of bar 11.
         “Take 4” Comp Row and swipe...

        Now the recording on the “Take 4” Comp Row is assigned to a third segment in the clip. Two new Cut Handles
        have been added: one at the beginning of the swiped segment and one at the end.
      7. Assign a recording to the last segment of the clip.
        We used the Audition Tool and found that the recording on the “Take 1” Comp Row was just what we were looking
        for to play through to the end of the clip. Since a fourth segment was already created when you swiped in the pre-
        vious step, you just need to double-click with the Selection Tool on the “Take 1” Comp Row, to the right of the last
        Cut Line, to assign the recording to the fourth segment:

        Double-click on the “Take 1” Comp Row, to the right of the last Cut Line,
        to assign it to the last segment in the clip.

      8. To eliminate any clicks that might occur between the recordings in the different segments of our clip, let’s in-
         troduce some crossfades.
          Crossfades can be applied by first selecting a Cut Handle and then clicking with the Selection Tool and dragging
          the Cut Crossfade Handles that appear above the selected Cut Handle:

            Click and drag the Cut Crossfade Handle...                ...to introduce a crossfade between the segments.

          The crossfade slopes are indicated by curves on the assigned Segments. The longer the crossfade time, the flatter
          the curves.
          Repeat the procedure for the other Cut Crossfade Handles in the clip if needed.
      q   If you want to set the same crossfade time for several Cuts, select the Cut Handles and use the “Match Value”
          function in the Inspector (see “Matching Cut Crossfades”).
      9. Finally, you might want to trim the audio levels of the different recordings on the Comp Rows in the clip.
          Click with the Selection Tool and drag the Comp Row Level Faders on the respective Comp Row to achieve a bal-
          anced audio level throughout the clip. The Comp Row level adjustments can be made anytime during the creation
          of the comped audio clip.

          Adjusting the individual Comp Row audio levels.
      q   If you want to set the same level for several Comp Rows, select the Comp Rows and use the “Match Value”
          function in the Inspector (see “Matching Comp Row Levels”).
      D   When you’re satisfied with your comped clip, you might want to click the “Bounce” button to generate a single
          recording that plays back your comped audio.
          The clip is then also automatically set to Single Take mode, which makes it possible to edit the clip in Slice Edit
          mode, where you can stretch and quantize the audio etc. (see “Editing audio in Slice Edit mode”), or in Pitch Edit
          mode, where you can correct and edit the pitches of monophonic audio recordings (see “Editing audio in Pitch Edit
          mode”).
          Bouncing also helps you keep things organized and can be a way to create a “snapshot” of your current comp, for
          comparison while you continue to fine-tune the edits.
      q   If you're finished with a comp and want to keep the file size down, you can use the “Bounce” function together
          with the “Delete Unused Recordings” function to permanently remove all original takes (see “Delete Unused
          Recordings”).

      Common audio editing functions
      The functions below apply to all audio clip types.

      Delete Unused Recordings
      After you have edited your audio clips in the Comp Editor, there might be unused recordings left on Comp Rows that
      you don’t plan to use. To reduce the file size of your song, you can choose to delete all unused recordings in one or
      several audio clips.
      D   Select the clip(s) in the Clip Overview area in the Comp Editor, or select the clip(s) in the Arrange View, and
          then select “Delete Unused Recordings” from the Edit menu or context menu.
          All recordings that are not used in the clip(s) will be permanently deleted.
      • If a clip is in Single Take Mode, only the selected Comp Row will be played back - all other Comp Rows are per
        definition “unused”. However, there may still be Cuts and assigned Segments among these Comp Rows, visi-
        ble and audible if you switch the clip to Comp Mode.
          As a safety measure, if you use the “Delete Unused Recordings” function on such a clip, you will be asked to con-
          firm that you really want to remove all Comp Rows other than the selected one.
      • After deleting audio recordings, you will have to use the “Save and Optimize” function on the File menu to
        minimize the Song file size - see “Saving and optimizing a Song”.

      Bounce Clip(s) to New Sample(s)
      You can bounce one or several Audio Clips to new Song Samples. You could then edit the samples in the Edit Sam-
      ple window and then load into a sampler device for playback. Proceed as follows:
      D   Select the clips in the Clip Overview area in the Comp Editor, or select them in the Arrange View, and then se-
          lect “Bounce > Bounce Clip(s) to New Sample(s)” from the Edit menu or context menu.
          The Audio Clips are bounced to new Song Samples and named according to the Audio Clip name (if the clip was
          named) or according to the Audio Track name with serial numbers. The bounced Audio Clips then end up as sam-
          ple files in the Song Samples location in the Browser. Refer to “Sampling” for more details about sampling and
          sample editing.

      About the “Bounce Clip to Disk” function
      The “Bounce > Bounce Clip to Disk” function on the Edit menu and clip context menu allows you to export the audio
      of a selected clip to disk as a single WAV or AIFF file. This might be useful if you want to process an audio clip in an
      external application and then re-import the clip to the track again. See “Bouncing Audio Clips” for more details.

      Bouncing audio to MIDI notes
      It’s possible to convert Single Take audio clips to note clips. This is especially useful for monophonic audio that can
      be edited in Pitch Edit mode. But if you like to experiment you could try it on polyphonic audio as well. The result in
      any situation will be a monophonic note clip on a default Subtractor instrument track.
      D   Select one or several Single Take audio clips in the Arrange View and select “Bounce > Bounce Audio Clips To
          MIDI” from the Edit menu or context menu.
          A Subtractor instrument track is automatically created for each of the audio tracks. On the Subtractor track(s) a
          note clip for each of the selected audio clips are created.
      D   Alternatively, drag one or several Single Take audio clips and drop onto an Instrument track.
          The audio clips are automatically converted into note clips as you drop them on the Instrument track. Once
          dropped, you could play back the note clips using the present Instrument sound.

      • Clips that have “Vocal” Stretch and Transpose Type selected will generate Note clips with different MIDI notes
        in them.
      • Clips that have “Allround” or “Melody” Stretch and Transpose Type selected will generate Note clips with only
        MIDI note C3 in them. In other words, you will basically only get a “rhythm” played by note C3.
          This can be very useful if you, for example, want to bounce drums to MIDI notes. You may then have to move the
          MIDI notes to the correct notes in the generated Note clip afterwards.
      !   If you drag Single Take audio clips from several audio tracks, you will need the same number of Instrument
          tracks to be able to drop all clips. As a rule of thumb, always create the instrument tracks right below the re-
          spective audio track.

      Normalizing audio clips
      Normalizing means increasing the overall audio level so that the loudest peak in the sound touches 0 dB. Normalizing
      can be made on any audio clip, regardless of if they are Single Take clips or Comp clips.
      1. Select the Audio Clip(s) in the Arrange View, or in the Clip Overview in the Comp Editor.

          A comped audio clip selected in the Clip Overview in the Comp Editor.
      2. Select “Normalize Clips” from the Edit menu or context menu.

          A new Comp Row is automatically created at the top and named after the Audio Track, with the extension “(nor-
          malized)”. The new Comp Row contains the “bounced” normalized audio and the Audio Clip has also automatically
          switched to Single Take Mode. The original audio is preserved on their original Comp Rows.
      !   Only the audio within the Audio Clip boundaries will be normalized. Any masked audio will be disregarded.
      !   Note that normalizing a clip that contains audio that already reaches the full headroom (touches 0 dB) won’t
          have any effect.
      !   When you normalize a Single Take clip, Reason automatically re-analyzes the audio and distributes new Slice
          Markers at the detected transients.

      Reversing audio clips
      Reversing an audio clip means playing it backwards, from the end to the start. Reversing can be made on any Audio
      Clips, regardless of whether they are Single Take clips or Comp clips.
      1. Select the Audio Clip(s) in the Arrange View, or in the Clip Overview in the Comp Editor.

          A comped audio clip selected in the Clip Overview in the Comp Editor.
      2. Select “Reverse” from the Edit menu or context menu.

          A new Comp Row is automatically created at the top and named after the Audio Track, with the extension “(re-
          versed)”. The new Comp Row contains the “bounced” reversed audio and the Audio Clip has also switched to Sin-
          gle Take Mode. The original audio is preserved on their original Comp Rows.
      !   Only the audio within the Audio Clip boundaries will be reversed. Any masked audio will be disregarded.
      !   When you reverse a Single Take clip, Reason automatically re-analyzes the audio and distributes new Slice
          Markers at the detected transients.
      q   You can also reverse Note and Automation Clips (and individual events in these), see “Reverse”.

      Changing the tempo and transposition of the audio
      Tempo scaling Clips
      Besides the automatic time stretching function applied when you change the Tempo in the main sequencer, there is
      a Scale Tempo function which can be applied to scale the tempo of one or several clips. The Scale Tempo function
      works in the same way for audio clips, note clips and parameter automation clips. However, it might be interesting to
      see what happens when you tempo scale an audio clip.
      1. Open an audio clip in the Comp Editor.
        In this example we use a Comp clip with four Comp Rows and a number of Cuts. The tempo scaling works exactly
        the same way, regardless if the clip is a Single Take clip or Comp clip.
      2. With the Arrow Tool selected, hold down [Ctrl](Win) or [Option](Mac) and place the mouse cursor over one of
         the Clip Resize handles (in the Clip Overview).
        When you reach any of the Clip Resize handles, the arrow symbol switches to a “scale tempo” arrow.

      3. Hold down [Ctrl](Win)/[Option](Mac) and click and drag the cursor sideways in either direction to scale the
         tempo of the clip.
        In this example, we make the clip one bar longer by dragging the right clip handle one bar to the right.

        Now, the audio clip has been tempo scaled and the audio recordings have been stretched to match the new clip
        length. Note that the distance between the Cuts, as well as the lengths of the recordings on all Comp Rows have
        been expanded proportionally.

      !   When you use the Scale Tempo function on Single Take clips (in the Arrange View), the Slice Markers will fol-
          low proportionally.
      The Scale Tempo function can also be applied to clips numerically in the Tool Window, see “Scale Tempo”.
      !   When you scale the tempo of large clips, it could take a while before the high quality stretch is finished, see
          “Preview vs. High Quality Stretching”.

      Transposing Audio Clips
      Audio clips can be transposed. That is, all the audio recordings in a selected audio clip can be transposed up or down
      12 semitones, in steps of 1 Cent, relative to their original pitch. The transposition can be applied to all types of audio
      - including polyphonic material.
      !   The transposition is non-destructive, i.e. the original audio is always preserved and left unaffected.
      !   To get the best sound quality when you are transposing audio it’s important that you have selected the correct
          Stretch and Transpose Type for the audio track, see “Opening audio clips for editing”.
      1. Select one or several audio clips.
          The Transpose display shows up to the right in the Inspector:

          Three audio clips selected on the arrangement pane in the Song View.
      2. Click the up/down arrow button next to the Transpose display to change the transposition in Semitones and
         Cents.
          The audio in the selected clips are now transposed relative to their original pitch.
      D   You can also edit the transposition value by clicking and dragging the respective display segment up/down or
          entering numeric values according to standard procedures.
      • It’s also possible to transpose individual Comp Rows in a Comp clip - see “Transposing Comp Rows” below.
      • Audio Clips and MIDI notes in Note Clips can be transposed in whole semitone steps in the Transpose section
        in the Tool Window - see “Pitch (Transpose)”.
      q   If you want to edit and/or correct the pitches of individual notes in monophonic audio recordings (e.g. vocal re-
          cordings), you can open the audio clip in Pitch Edit mode, see “Editing audio in Pitch Edit mode”.

      Transposing Comp Rows
      Besides the Audio Clip Transpose function described above, individual Comp Rows in a Comp clip can be individually
      transposed:
      1. Open a comped audio clip in the Comp Editor and select a Comp Row to be transposed.

        The selected Comp Row is shown in a darker color.
      2. Change the Transpose value in the Inspector as desired.

      3. Select another Comp Row and change its Transpose value in the Inspector as desired.
        Now the Comp Rows will have individual transposition values.
      • If you decide to change the Transpose value for the entire audio clip - by selecting the clip in the Clip Overview
        - the relative transpositions of the Comp Rows will be preserved.

      Audio and tempo matching
      Matching imported audio to the song tempo
      Audio files created by the Export or Bounce functions in Reason include information about their original tempo. When
      you import such an audio file, it will automatically be stretched to fit the tempo in the new song.
      However, if you have imported audio which has a steady, but unknown, tempo, you can adjust the imported clip to the
      song tempo. You can either use the Clip Tempo Scaling function to manually “stretch” the audio clip as described in
      “Tempo scaling Clips”.
      Another way is to disable the automatic stretch for the audio clip and then adjust the sequencer tempo to match the
      clip. This is done in two steps: first you adjust the song tempo to the imported audio clip without Stretch enabled and
      then adjust the song tempo back to original - with Stretch enabled on the audio clip:
      1. Select the clip containing the imported audio file and choose “Disable Stretch” from the Edit menu or context
         menu.
        Disabling Stretch makes the audio recording in the clip play back at the same tempo regardless of song tempo in
        the sequencer.

        Disabling Stretch on a clip containing an imported audio recording.
      2. Start the sequencer and adjust the sequencer Tempo, up or down, to match the tempo of the audio recording
         in the clip.
        If necessary, enable the metronome click in the sequencer to get an audible tempo reference. Continue adjusting
        the tempo of the song until it matches the tempo of the audio recording.
      3. Adjust the length of the clip so that it plays the entire audio file (or as much as you want).
      4. Select the clip and select "Bounce > Bounce Clip to New Recording" from the Edit menu or context menu.
        The new recording will sound the same, but include information about the tempo you set in step 2.
      5. With the audio clip still selected, choose “Enable Stretch” from the Edit menu or context menu.
      6. Adjust the song tempo back to the original BPM.
        As you adjust the song tempo, the tempo of the audio recording will follow along accordingly - without affecting
        the original pitch of the recording. This is done by stretching the audio. Reason does this automatically in two par-
        allel steps: a real-time “preview” stretch so that you can instantly hear the result of your tempo changes, then a
        high quality stretch “in the background” to further improve the sonic results. As soon as high quality stretch is in
        progress, the “Calc” indicator on the Transport Panel shows a progress meter:

        The CALC progress meter appears when Reason performs high quality stretching of audio.
        Since the high quality stretch is performed in the background, you can still continue to work with your song without
        any interruption. When the high quality stretch data has been calculated, the Calc indicator goes out and the high
        quality audio data will be heard on playback.

      Editing audio using the Inspector
      The Inspector can be used for editing audio recordings numerically.
      !   For Inspector editing specific to Pitch Edit mode, please refer to “Audio pitch editing in the Inspector”.

      Editing recordings and cuts in the Inspector
      If you select a Comp Row, the three displays change to show the Recording Offset, Comp Row Level and Comp Row
      Transpose value:

      If you select a Cut Handle in Comp Mode, two displays appear, showing the Cut Handle’s Position and Crossfade
      time:

      D   Edit the values by clicking on a segment in a display and then dragging up/down, using the up/down spin con-
          trols, or typing in new values. Snap is not taken into account.
          See “Inspector segment displays” for details on how to edit in the Inspector displays.

      Editing multiple recordings or multiple cuts in the Inspector
      When you edit values for several selected Comp Rows or objects (Cut Handles etc.), the changes will always be rel-
      ative. For example, if you change the Recording Offset, Level or Transpose values when several Comp Rows are se-
      lected, the recordings will all be changed by the same amount; their relative values will be retained.
      • If several Comp Rows are selected, the displays will show the values for the topmost selected Comp Row.
      • If several Cut Handles are selected, the displays will show the Position and Crossfade values for earliest Cut
        Handle in the clip.
      • If several Comp Rows, or several Cut Handles, are selected and any of their values differ, Match Value buttons
        appear next to the corresponding display.
          For Cut Handles, only Crossfade values can be matched - not the Positions. See “Matching audio values using the
          "Match Values" function”.
      • If Comp Rows and Cut Handles are selected in combination (e.g. for moving Cuts and recordings together as a
        group), no displays are shown in the Inspector.

      Matching audio values using the "Match Values" function

      The Match Values buttons appear as ‘=’ signs.
      The “Match Values” function in the Inspector can be used for matching Recording Offsets, Comp Row Levels and
      Transpose values of several selected Comp Rows to the offset/level/value of the topmost selected Comp Row. It can
      also be used for matching Cut Crossfade values of several selected Cut Handles to the Crossfade value of the Cut
      Handle with the earliest start position in the clip.

      The “Match Values” function can also be used for matching the following parameters of several selected notes in
      Pitch Edit mode: Note, Fine-tune, Drift, Preserve Expression, Transition, Formant and Level. See “Audio pitch editing
      in the Inspector” for more info.

      Matching Recording Offsets
      Matching Recording Offsets is useful if you want to make sure that the Recordings on multiple Comp Rows start at
      the exact same position.
      1. Select more than one Comp Row and then place the Selection Tool on the Recording Offset Match Value but-
         ton.

        Three selected Comp Rows (the three topmost).
        The topmost Comp Row has the Recording Offset set to 2 beats.
      2. Click the Match Value button to the right of the “Recording Offset” display.
        The Recording Offsets on all selected Comp Rows have now been moved to 2 beats.

        The Recording Offsets of the recordings on the three topmost Comp Rows have been moved to 2 beats.

      Matching Comp Row Levels
      Here’s an example showing how to match Comp Row Levels:
      D   Select several Comp Rows and then click the Level Match Value button.

          The Levels on the three selected Comp Rows are matched and adjusted to -19.90 dB.

      Matching Comp Row Transpose values
      D   Select several Comp Rows and then click the Transpose Match Value button.
          The transposition is matched to the Transpose value of the topmost selected Comp Row.


=== END OF PART ===
