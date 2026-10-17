# Chapter 09: Reason 12 manual digest and studio workflow
## Part 26 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 17 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 27 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 17 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 8: Audio Editing in the Sequencer

Audio Editing in
the Sequencer

      About this chapter
      This chapter describes how to edit audio clips after you have recorded them in the sequencer. General sequencer
      functions, recording, note and automation editing, and arranging in the sequencer are described in detail in the chap-
      ters “Sequencer Functions”, “Recording in the Sequencer”, “Note and Automation Editing” and “Arranging in the Se-
      quencer”.

      Edit Modes, Stretch & Transpose Types and Clip Types
      After you have recorded your audio clips, you might want to adjust levels, trim starts and ends, add fades etc. If you
      have recorded several takes in your audio clips, or several cycles in Loop Mode, you can also cut out segments of the
      various takes and compile (comp) them into a final “perfect” audio clip.
      You can also quantize audio clips, manually change the timing of individual notes or beats in the clips and even export
      audio clips as REX files.
      In addition to this you can also edit and correct the pitches of monophonic audio recordings, in the Pitch Edit mode.

      Edit Modes
      There are three main ways you can edit your audio clips:
      • In Slice Edit mode.
          Slice editing can be made on Single Take clips (see “Clip Types” below). Single Take clips can be opened for ed-
          iting in Slice Edit mode in the Arrange View, similar to when editing parameter automation clips. Slice editing al-
          lows you to adjust the positions (timing) of the automatically detected and distributed transient slice markers that
          appear in the audio clip. The timing can be adjusted by moving and stretching (warping) the audio slices. See “Ed-
          iting audio in Slice Edit mode”.
      • In Pitch Edit mode.
          In Pitch Edit mode you can graphically correct and edit the pitches of monophonic audio in Single Take clips -
          perfect for vocal pitch correction/manipulation. See “Editing audio in Pitch Edit mode” for more information.
      • In Comp Edit mode, to create compiled clips out of multiple recordings in the clip.
          In Comp Edit mode you can cut out segments of several Takes (recordings) and compile into a final clip. Here you
          can also insert silence segments to e.g. remove noise from silent parts in your audio clips. See “Editing audio in the
          Comp Editor”.

      Selecting Stretch and Transpose Type
      When you are stretching, transposing and/or changing the tempo of the audio it’s important that the Stretch and
      Transpose Type for the corresponding audio clip - or Comp Rows in Comp clips - is set according to the type of audio
      that’s in the clip. Otherwise, the sonic result might not be what you’d expect.
      The Stretch and Transpose Type, together with the Clip Type, also determines the default Edit Mode in which the clip
      will open when you double-click it, see “Opening audio clips for editing”. However, you can always change the Edit
      Mode for a clip manually, if you like.
      Stretch and Transpose Type can be selected as follows:
      D   In Arrange View select all the desired audio clip(s), then select the desired Stretch and Transpose Type from
          the Edit menu or clip context menu.
      !   For Comp Clips, the active Stretch and Transpose Type for all active Comp Rows are shown in the menu - if the
          Stretch and Transpose Type is the same. If there are active Comp Rows with different Stretch and Transpose
          Types, none of the options on the menu are shown as selected.

          Selecting a Stretch and Transpose Type from the sub-menu for a Comp Clip will change the stretch and trans-
          pose type for all active Comp Rows in the clip.

          If there are Slice/Pitch Edits done to any of these Comp Rows (and these edits cannot be preserved in the new
          Stretch Type), there will be an alert asking if you want to bounce the clip to a new recording.
      • For polyphonic material, select “Allround”.
          The formants are transposed along with the audio.
      • For monophonic material select “Melody”.
          The formants are transposed along with the audio.
      • For vocal material select “Vocal”.
          The formants are preserved and are not transposed along with the audio. This will keep the original character of
          the vocal and will only affect the pitch. “Vocal” is also the default Stretch and Transpose Type for editing audio in
          Pitch Edit mode, see “Editing audio in Pitch Edit mode”.
      !   For the Stretch and Transpose function to be active, make sure that you have selected Enable Stretch from the
          clip context menu!

      Clip Types
      An audio clip can be either a Single Take clip or a Comp clip:
      • A Single Take clip is set to play back only a single Take (Comp Row) throughout the audio clip.
          If you have recorded only once in an audio clip, or recorded several complete Takes, the clip is automatically set to
          Single Take mode. A Single Take clip could also contain several Comp Rows, where one Comp Row has been
          manually selected for playback. The symbol in the lower right corner of a Single Take clip depends on the selected
          Stretch and Transpose Type and also determines what Edit Mode the clip will open in:
      • A Single Take clip, which has the “Allround” or “Melody” Stretch and Transpose Type looks as follows:

          A single Take clip with “Allround” or “Melody” Stretch and Transpose Type.
          When you double-click these types of clips, they will automatically open in Slice Edit mode.
      • A Single Take clip, which has the “Vocal” Stretch and Transpose Type looks as follows:

          A single Take clip with “Vocal” Stretch and Transpose Type.
          When you double-click these types of clips, they will automatically open in Pitch Edit mode.
      • A Comp clip is built up by segments from several recordings on multiple Comp Rows in the clip.
          If you have recorded (or imported) several takes (recordings) in the same audio clip - or recorded several loops in
          Loop Mode - and then compiled segments of the various Comp Rows in the Comp Editor, the clip becomes a
          Comp clip.
      • Comp clips are distinguished by the following symbol in the lower right corner:

          A Comp clip, regardless of selected Stretch and Transpose Type.
          When you double-click these types of clips, they will automatically open in Comp Edit mode.

      Opening audio clips for editing
      In the Arrange View, audio recordings are displayed as one or two (mono or stereo) waves in the audio clips. The se-
      lected audio clip in the pictures below contain mono recordings.
      D   Open an audio clip by double-clicking it, or by selecting it and pressing [Return].
          The audio clip opens in its default Edit Mode, as indicated by the symbol at the bottom right of the clip.

          Double-click an audio clip in the arrangement...

          ...to open it for editing in its default Edit Mode. Here, Slice Edit mode is the default Edit Mode.
      • The clip opens in its default Edit Mode (Slice Edit, Pitch Edit or Comp Edit).
          When the audio clip is in Slice Edit mode you can stretch, move and quantize audio slices etc., see “Editing audio
          in Slice Edit mode”. When the clip is open in Pitch Edit mode you can pitch-correct and transpose individual notes
          (pitches) in monophonic audio recordings, see “Editing audio in Pitch Edit mode”. When the clip is open in Comp
          Edit mode you can alternate the playback between several recordings and compile into a single recording, see
          “Editing audio in the Comp Editor”.
      D   Alternatively, select the clip and click any of the Edit buttons in the Toolbar (Slice Edit/Pitch Edit/Comp Edit)
          to open the clip for editing in the desired Edit Mode.
      • If Reason detects monophonic, melodic audio when you import an audio file, the clip will be automatically set
        to Vocal stretch type. If you then open the clip for editing, it will default to Pitch Edit mode.
      It is also possible to open a clip for editing as follows:
      D   Select the Single Take clip, hold down [Ctrl](Win) or [Cmd](Mac) and press [E].
          The clip opens in its default Edit Mode (Slice Edit, Pitch Edit or Comp Edit).

      Closing a clip
      D   To close a Single Take clip and return to the Arrange View, press [Esc].
          Alternatively, to close a Single Take clip in Slice Edit mode, click outside the open clip on the Arrange Pane, but
          not on the same track.
      D   To close a Comp Clip, press [Esc] or click the “Close” button in the Comp Editor.

      Editing audio in Slice Edit mode
      !   If you plan to comp the audio in your clips in Comp Edit mode, always do that before you start to work with
          slice stretching etc. in Slice Edit mode. It will save you a lot of work if all the comping has been done before-
          hand!
      !   To get the best sound quality when you are stretching and quantizing audio it’s important that you have se-
          lected the correct Stretch Type for the audio clip, see “Opening audio clips for editing”.

      Audio clip elements in Slice Edit mode
      When a clip is open for editing in Slice Edit mode, it could look like this:

                                                                              Slice Marker Handles

                                                    a Slice Marker                   a Slice

      A Single Take clip open in Slice Edit mode.
      q   You might have to zoom in quite a bit on the clip to get a good view of the Slices, see “Zooming in the Se-
          quencer”.
      • Slice Markers with handles
          When a Single Take audio clip is opened in Slice Edit mode, Reason automatically detects the transients in the
          sound and marks these with vertical white lines - Slice Markers. By moving Slice Markers left or right you stretch
          (warp) the audio between the nearest Slice Markers on either side, i.e. you change the timing without affecting the
          pitch. You can manually add and remove Slice Markers. It is also possible to “decouple” and move the Slice Mark-
          ers without stretching the audio.
      • Slices
          Slices are the areas between two adjacent Slice Markers. Each slice represents a part of the audio in the clip.

      Slice Edit mode tools
      When editing audio in Slice Edit mode, some of the Toolbar tools have different functionality than when editing note
      and automation clips. There are also some additional tools that are unique to slice editing of audio.

      Speaker Tool
      It’s possible to audition individual Slices without needing to start playback of the sequencer:
      D   Select the Speaker Tool in the Toolbar and click in the waveform area on the Slice you want to audition.

          The Slice is played back once in its entirety, from the start Slice Marker to the end Slice Marker of the desired
          Slice, each time you click.
      q   With the Selection Tool (Arrow) selected, pressing [Alt](Win) or [Cmd](Mac) will momentarily switch to the
          Speaker Tool.
      !   Note that auditioning Slices will play back the unprocessed sound - bypassing the Main Mixer settings.

      Selecting Slices and Slice Markers
      A Slice is the portion of audio between two adjacent Slice Markers. A Slice Marker indicates the beginning of a Slice
      - and consequently the end of the preceding Slice (if it’s not the first Slice in the clip).
      D   To select a Slice Marker, click the Slice Marker or its handle:

          As you hover over a Slice Marker or a Slice Marker Handle, the arrow switches to a double-arrow. A selected Slice
          Marker is indicated by a black Slice Marker Handle.
      D   To select several individual Slice Markers, hold down [Ctrl](Win)/[Shift](Mac) and click the desired Slice Mark-
          ers or their handles.

                                                                                  a Slice Group Handle
          If more than one Slice Marker has been selected, a Slice Group Handle appears below the waveform. You could
          then click and drag the Slice Group Handle sideways to move all selected Slice Markers as a group, see “Moving
          several Slice Markers”.

      D   To select a range of Slice Markers, draw a rectangle with the Selection Tool (Arrow), in the Slice Marker Han-
          dles area or in the waveform area, that touches the desired Slice Markers:

          Draw a rectangle over the desired Slice Markers to select a complete range.

          As you release the mouse button all touched Slice Markers are selected.
          The range of Slice Markers can then be moved as a group by clicking and dragging the Slice Group Handle side-
          ways. You can also stretch the range in an “accordion style” fashion by clicking and dragging any of the selected
          Slice Marker Handles in the range, see “Stretching a range of Slices”.
      D   Under Windows it’s also possible to select a range of Slice Markers by clicking a Slice Marker and then hold-
          ing down [Shift] and clicking the first or last Slice Marker in the desired range.
      D   You can expand a Slice/Slice Marker selection range by holding [Shift] and pressing the left/right arrow keys.
      D   To select all Slices/Slice Markers in the clip, select “Select All” from the clip’s context menu or from the Edit
          Menu.
          Now, you can move all Slice Markers as a group by dragging the Slice Group Handle sideways (see “Moving sev-
          eral Slice Markers”), or stretch the entire range of Slices (see “Stretching a range of Slices”).

      Adding Slice Markers
      When you open a Single Take clip in Slice Edit mode, there will be a Slice Marker at each transient, plus one at the
      start and one at the end of the clip. If you are not satisfied with Reason’s automatic Slice Marker assignments you
      can add Slice Markers manually:
      !   You might want to turn off Snap to be able to position the Slice Markers more precisely (see “Snap”).
      1. Open the Single Take clip for editing in Slice Edit mode.
      2. Select the Pencil Tool from the Toolbar.
      3. Click in the open clip to add new Slice Markers.
          If you are not satisfied with the position of the Slice Marker, you can reposition it afterwards, see “Repositioning
          Slice Markers”.
      !   You cannot add Slice Markers before the first Slice Marker or after the end Slice Marker in the clip.

      Deleting Slice Markers
      To delete Slice Markers, proceed as follows:
      1. Select the desired Slice Marker(s) as described in “Selecting Slices and Slice Markers”.
      2. Press [Delete] or [Backspace] to delete the marked Slice Makers.
          This deletes the Slice Markers but not the audio that’s in the clip.
      !   If you delete Slice Markers that were previously moved, the stretched audio will revert to the original timing.
      !   You cannot delete the first Slice Marker or the end Slice Marker in the clip.

      Repositioning Slice Markers
      To reposition a Slice Marker without stretching the audio, proceed as follows:
      !   You might want to turn off Snap to be able to position the Slice Marker more precisely (see “Snap”).
      1. Place the Selection Tool (Arrow) on a Slice Marker or Slice Marker Handle.
          The arrow switches to a double-arrow symbol.
      2. Hold down [Ctrl](Win] or [Option](Mac) and click and move the Slice Marker sideways.
      !   You cannot move Slice Markers past their closest adjacent Slice Markers.

      Moving/stretching Slices
      Stretching can be used for adjusting the timing of the transients in the audio clip. You can also use stretching to cre-
      ate special effects such as increasing or decreasing the lengths of the Slices. Stretching can be applied on single
      Slices as well as on a selection of Slices.
      !   To get the best sound quality when you are stretching audio it’s important that you have selected the correct
          Stretch and Transpose Type for the audio track, see “Opening audio clips for editing”.
      !   You might want to turn off Snap to be able to position the Slice Marker more precisely (see “Snap”).
      !   You cannot move Slice Markers past their closest adjacent Slice Markers.

      Preview vs. High Quality Stretching
      Reason features very sophisticated audio stretch and transpose algorithms for pristine results. Reason always per-
      forms audio stretching in two parallel steps:
      • A real-time “preview” stretch so that you can instantly hear the result of your changes.
      • A high quality stretch “in the background” to further improve the sonic results.
          As soon as high quality stretch is in progress, the “Calc” indicator on the Transport Panel shows a progress meter:

          The CALC progress meter appears when Reason performs high quality stretching of audio.
      Since the high quality stretch is performed in the background, you can still continue to work with your song without
      any interruption. When the high quality stretch data has been calculated, the Calc indicator goes out and the high
      quality audio data will be heard on playback.

      Moving a Slice Marker
      D   To adjust the timing of a single note or beat, just click and drag its Slice Marker to the desired position.
          If Snap is on, the Slice Marker will snap to the grid as set with the Snap value. When you move a Slice Marker, the
          slices on either side of it will be stretched accordingly.

      Moving several Slice Markers
      If you need to adjust the timing of several notes or beats (e.g. move all snare hits a little later in the beat), proceed as
      follows:
      1. Select the desired Slice Markers as described in “Selecting Slices and Slice Markers”.
      2. Click and drag the Slice Group Handle to move all selected Slice Markers.
          As you hover over the Slice Group Handle, the arrow switches to a double-arrow

                                               Slice Group Handle
          All selected Slice Markers will be moved as a group. The Slices between the selected Slice Markers and their clos-
          est unselected Slice Markers will be stretched.
      • It’s also possible to move a range of Slices by selecting a range of Slice Markers as described in “Selecting
        Slices and Slice Markers” and then dragging the Slice Group Handle sideways.
          This is useful if you want to move a whole phrase (e.g. a vocal phrase) later or earlier in the clip.
      !   You cannot move the selection past any unselected Slice Markers.

      Stretching a range of Slices
      It is also possible to stretch a range of Slices, proportionally, in an “accordion style” fashion:
      1. Select the desired range of Slice Markers as described in “Selecting Slices and Slice Markers”.
          The range is indicated by a light gray Stretch Range Marker above the waveform.
      D   If you drag the start or end Slice Marker in the range, the whole range will be stretched as if it were a single
          slice:
                                                                                     Stretch Range Marker

      D   If you drag a Slice Marker within the selected range, all selected Slices will be stretched proportionally against
          the start and end Slice Markers of the selected range:

      Nudging Slices
      You can nudge the Slice Marker(s) by using the following standard key commands:
      D   Hold down [Ctrl](Win) or [Cmd](Mac) and press the left/right arrow keys to nudge in Snap value steps.
      D   Hold down [Ctrl]+[Shift](Win) or [Cmd]+[Shift](Mac) to nudge in Beat steps.
      D   Hold down [Ctrl]+[Alt](Win) or [Cmd]+[Option](Mac) to nudge in Ticks steps.

      Quantizing audio
      Audio quantizing can be made in the Quantize section on the Transport Panel, in the Tool Window or from the context
      menu or Edit menu.
      !   Audio can only be quantized after recording, not during recording.
      !   Quantize requires that the clips have Stretch enabled (see “Enable/Disable Stretch (Audio Clips)”).
      !   To get the best sound quality when you are quantizing audio it’s important that you have selected the correct
          Stretch Type for the audio clip, see “Opening audio clips for editing”.
      !   Note that quantization of audio clips that have “Vocal” Stretch and Transpose Type is made on the pitch tran-
          sitions (where the “notes” start) and not on the level transients as in Slice Edit mode, see “Editing audio in
          Pitch Edit mode”.
      !   The difference between quantizing audio and MIDI notes is that several Slice Markers cannot be quantized to
          the same position. Instead, only the Slice Markers closest to the quantization grid will be moved - the remain-
          ing Slice Markers will be left unaffected.
      It’s possible to use the quantize audio function in the following ways:

      Quantizing selected Slice Marker(s) in Slice Edit mode
      Quantizing Slice Markers has the same effect as moving the Slice Markers to a quantization grid:
      1. Select the Slice Markers you want to quantize:

          A range of Slice Markers selected for quantization.
      2. Select Quantize Value (and Amount and/or Random values) in the Tool Window and click Apply:

          The selected Slice Markers that are closest to the quantization grid are automatically moved to the quantization grid.

      q   Note that you can quantize to “Shuffle” in the Value list - this will use the Global Shuffle setting made in the
          ReGroove Mixer, see “Global Shuffle”.
      D   Alternatively, select Quantize Value and click the Quantize button on the Transport Panel.
          This alternative is very handy if you only want to quantize to a set quantization value, and don’t need the extra op-
          tions featured in the Tool Window.

      Quantizing one or several selected Single Take audio clips in the Arrange View
      This will quantize all Slice Markers that are closest to the quantization grid in the selected clip(s).

      Split at Slices
      The Split at Slices function allows you to create separate audio clips out of a Single Take clip. Splitting can be useful
      if you, for example, want to reverse parts of the original clip or if you want to export single or multiple Slices as sepa-
      rate samples for use in any of Reason’s sampler devices. The split point(s) will be located at the selected Slice Mark-
      ers in the clip.
      The following example shows how the “Split at Slices” function can be used:
      1. Select the split points for the new clips by selecting the desired Slice Markers in the open Single Take clip:

          The selected Slice Markers define the split points for the new clips.
      2. Select “Split at Slices” from the context menu or Edit menu.

          The original Single Take clip is now split into four separate audio clips and the clips are automatically closed.
          If you like, you can now select the desired clip(s) and move, reverse (see “Reversing audio clips”) or choose to
          bounce the clip(s) to samples (see “Bounce Clip(s) to New Sample(s)”).

      Bounce Clip to REX Loop
      A great feature with Single Take clips is that you can bounce them to REX Loops. You could then load your bounced
      REX file for further processing in a Dr Octo Rex device, for example! Here is how:
      1. Open a Single Take clip in Slice Edit mode.
      2. Make sure the Slice Markers are located exactly where you want them in the clip.
          This is where the slices in the REX Loop will appear after bouncing.
      D   You might have to remove some Slice Markers in the clip to reduce the number of slices in the final REX Loop,
          see “Deleting Slice Markers”.
      3. Adjust the audio clip length to the closest full Beat.
          This way you make sure that the REX Loop will sound the same as the original audio clip.
      !   If the clip is not adjusted to a full Beat, Reason will automatically expand the clip end to the closest full Beat
          during the bounce operation.

      4. Select “Bounce > Bounce Clip to REX Loop” from the context menu or Edit menu.
          The bounced REX file ends up in the “All Self-contained Samples” folder in the Song Samples location in the
          Browser, and is named after the original clip name:

      5. To load the bounced REX file in a new Dr Octo Rex device, either double click the REX file or select the REX
         file and click the “Create” button at the bottom of the Browser.
          This is a shortcut for creating a Dr Octo Rex device and loading the selected REX Loop in Slot 1 of the Dr Octo
          Rex device in one go.
      q   Refer to the “Dr. Octo Rex Loop Player” chapter for information on how to work with REX Loops in the Dr Octo
          Rex device.
      !   If you want to load your REX Loop in another sampler device, you first have to un-self-contain the REX file, see
          ““Un-self-containing” a Song”. Then, create the sampler device and load the un-self-contained REX file from
          disk.

      About exporting bounced REX Loops to disk
      You can also export your bounced REX Loops to disk if you like:
      1. Select the REX Loop in the Song Samples location in the Browser and select Export Sample(s) from the con-
         text menu or Edit menu.
      2. Choose a location for the REX Loop (and change the file name, if desired).
      3. Click Save.
          The REX Loop is exported and saved in .rx2 format.

      Revert All Slices
      If you get lost in the Slice Edit mode editing, there is a handy command for reverting the Slice Markers back to where
      they were before you started editing the clip:
      1. Open the Single Take clip in Slice Edit mode.
      2. Select “Revert All Slices” from the context menu or Edit menu.
          This will revert all slice edits and the clip will play back with its original timing. Any manually removed Slice Markers
          will reappear, and any manually added Slice Markers will be removed.

      Editing audio in Pitch Edit mode
      In Pitch Edit mode you can correct and/or transpose the pitches of individual detected notes in monophonic record-
      ings. Pitch Edit mode is developed especially for editing and correcting the pitches of vocal recordings. The audio
      pitch editing is made graphically in a way similar to other pitch correction/editing software on the market.
      !   As soon as you open an audio clip in Pitch Edit mode, the Stretch and Transpose Type will be automatically set
          to “Vocal”.

      Pitch Editor elements
                             Close button                                          Clip Overview


=== END OF PART ===
