# Chapter 09: Reason 12 manual digest and studio workflow
## Part 28 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 19 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 29 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 19 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      • Cut Handles and Cut Lines
        Each cut in a comped audio clip is indicated by a Cut Handle and a Cut Line. The Cuts indicate where the playback
        changes from one segment to another (in most situations from one Comp Row to another). You can edit the Cut
        positions by clicking and dragging any of the Cut Handles or Cut Lines sideways.
      • Silence Row
        The Silence Row can be used for inserting silent segments in the comped audio clip, e.g. for removing breath noise
        between vocal phrases.
      • Comp Rows
        All of your audio recordings reside on Comp Rows. Depending on how you recorded the audio clip, there might be
        one or several Comp Rows, each containing one audio recording. The most recent take is on the topmost Comp
        Row. In a Comp clip, the colored part(s) of each Comp Row (or Silence Row) will play back. All Comp Rows used
        in the clip have colored Comp Row Handles. Any unused Comp Rows in the clip are indicated by gray Comp Row
        Handles.

      The relationship between Clips, Comp Rows and Recordings
      In the Comp Editor, the contents of an open clip are displayed on the Comp Row(s) on the Edit Pane:

                                                                                                    Audio Clip in the
                                                                                                    Clip Overview area

                                                                                                    Comp Rows with one
                                                                                                    Recording each

      A Single Take clip with four Comp Rows, with the topmost Comp Row manually selected for playback.

                                                                                                  Audio Clip in the
                                                                                                  Clip Overview area

                                                                                                  Silence Row

                                                                                                  Comp Rows with one
                                                                                                  Recording each

      A Comp clip with alternating playback from four Comp Rows.
      • A recorded audio clip, or an audio clip containing imported audio, can consist of one or several Comp Rows.
         The number of Comp Rows and their position can be unique for each individual audio clip. Any edits you make in
         an audio clip will never interfere with other clips in the Song.
      • On each Comp Row there is one single Recording, i.e. the audio that you have recorded or imported.
         If the clip was recorded in one single take, it will have a single Comp Row. If the clip was recorded in several takes
         one after another, or recorded in Loop Mode, it will contain one Comp Row for each take or loop. Also, if you im-
         ported audio files to a clip, each audio file will end up on a separate Comp Row.

      • Only one Comp Row can play back at a time.
        In a Single Take clip with more than one Comp Row, only the Comp Row you have selected by clicking the Single
        Take Mode button will play back. In a Comp clip, you can alternate the playback between the Comp Rows by as-
        signing regions of the different Comp Rows to different Segments in the Clip. What you hear when you play back
        an audio clip is displayed in the Clip Overview area at the top on the Edit Pane. (The Clip Overview area displays
        the same content as the clip in the Arrange View.)

                                                                                                      Audio Clip in the
                                                                                                      Clip Overview area

                                                                                                      Played back Comp Row

                                                                                                      Unused (silent)
                                                                                                      Comp Rows

        A Single Take clip with four Comp Rows, with the topmost Comp Row manually selected for playback.

                                                                                                      Audio Clip in the
                                                                                                      Clip Overview area

                                                                                                      Played back Segments
                                                                                                      of assigned Comp Rows

                                Unused (silent) Comp Row

        A Comp clip with alternating playback from three Comp Rows plus the Silence Row.
      • The Comp Row configuration, and the Recordings on the Comp Rows, are unique to each individual audio clip.
        This means that you could move Comp Rows up or down on the Edit Pane, change Comp Row Levels and Cross-
        fades, or move Recordings back and forth on the Comp Rows, without affecting any neighboring audio clips.
      • If you duplicate a Clip, or a Comp Row with its Recording, you can freely edit the duplicated Clip, Comp Row or
        Recording without affecting the original.
        However, the actual audio data is not duplicated. Reason features a very sophisticated internal audio management
        system which re-uses Recordings throughout the entire Song whenever necessary. This means that the Song file
        size won’t increase when you duplicate audio clips or Comp Rows.

      Comp Editor window handling
      Resizing, zooming and scrolling
      D   The Magnifying Glass tool can be used for zooming in and out (see “Magnifying Glass Tool”).
      D   The Hand tool can be used for scrolling the view in any direction (see “Hand Tool”).
      D   Use the Song Navigator to scroll and zoom horizontally (see “Areas, windows and basic navigation”).
      D   Click on a Song Navigator Handle and drag horizontally to zoom in and out horizontally (see “Areas, windows
          and basic navigation”).
      D   Shift-click on a Song Navigator Handle and drag horizontally to zoom in and out horizontally, symmetrically
          (see “Areas, windows and basic navigation”).
      D   Right-click (Win) or Ctrl-click (Mac) inside the Song Navigator frame and drag up or down to zoom in and out
          and scroll at the same time (see “Areas, windows and basic navigation”).
      D   Use the Track Navigator to scroll vertically in the Track List (see “Areas, windows and basic navigation”).
      D   Click the Zoom buttons below the Track Navigator to zoom in and out vertically (see “Areas, windows and ba-
          sic navigation”).
      • For extensive editing, you may want to maximize the Sequencer and/or detach the Main Mixer and Rack so
        that the sequencer covers the entire computer screen. Refer to “Areas, windows and basic navigation”.

      Comp Editor audio editing tools
      When editing audio in the Comp Editor, some of the Toolbar tools have different functionality as when editing note
      and automation clips. There are also some additional tools that are unique to audio editing.

      Razor (Cut) Tool
      When editing audio in the Comp Editor, the Razor Tool on the sequencer Toolbar is used for creating Cuts. When you
      place the Razor Tool over the Comp Rows, Silence Row or Cut Row, it changes into a “Cut Tool”.
      q   With the Selection Tool selected, hold down [Alt](Win) or [Cmd](Mac) to temporarily switch to the Cut Tool.
      D   Click with the Razor Tool on a Comp Row to assign the recording to the right of the cursor to a new Segment.

          Assigning the recording on the “Take4” Comp Row to a new segment.
          See “Adding Cuts” for more details on how to use the Cut Tool.
      The Razor Tool can also be used for assigning a complete Segment, with a start and end Cut, by clicking and drag-
      ging (swiping) the Razor Tool horizontally on the desired Comp Row. See “Adding Segments” for more details on how
      to swipe with the Cut Tool.

      Speaker Tool
      It’s possible to audition individual recordings on Comp Rows, without needing to start playback of the sequencer. This
      is very useful when you’re going to select what Comp Rows to use in the clip:

      1. Make sure the Speaker Tool is selected and place the cursor at the position on the Comp Row you would like
         to audition.
          The cursor switches to a speaker symbol with crosshairs next to it.

          Auditioning a recording on a Comp Row.
      2. Click and hold the mouse button depressed for as long as you want to listen.
          The playback starts at the current crosshairs position and proceeds for as long as you keep the mouse button de-
          pressed. The playback position is indicated by a vertical moving line on the auditioned Comp Row.
      q   With the Selection Tool (Arrow) selected, holding down [Alt]+[Shift](Win) or [Cmd]+[Shift](Mac) will switch to
          the Speaker Tool.
      !   Note that auditioning recordings on Comp Rows will play back the unprocessed sound of the recording -
          bypassing any settings in the Main Mixer.
      q   Using the Speaker Tool, it’s possible to audition recordings anywhere on any Comp Rows. The Comp Row
          doesn’t have to be selected - it’s even possible to audition recordings on masked Comp Row segments.

      Selecting a Comp Row for playback in a Single Take clip
      In a Single Take clip, only the selected Comp Row will play back throughout the entire clip length. It’s also possible to
      change Comp Row Levels and Recording Offsets in a Single Take clip. The picture below shows an open Single
      Take clip in the Comp Editor. The clip consists of four separate takes, each on a separate Comp Row. When played
      back, the recording on the selected “Take 4” Comp Row will play back:

      A Single Take clip open in the Comp Editor with four recorded takes.

      If you want to change which Comp Row should play back in a Single Take clip:
      D   Click the Single Take Mode button for the Comp Row you want to play back.

          The “Take 2” Comp Row is now manually selected for playback throughout the clip.
          Now, the “Take 2” Comp Row will play back instead when the sequencer is started.

      Selecting Comp Rows
      D   To select a Comp Row, e.g. for moving, cutting, copying, duplication or deletion, click (don’t double-click!) with
          the Selection Tool anywhere on the Comp Row, or on the Comp Row Handle.
          The selected Comp Row is shown in a darker color:

          The selected Comp Row is shown in a darker color.
      D   Select multiple Comp Rows by holding down [Ctrl](Win) or [Cmd](Mac) and clicking with the Selection Tool.
      D   Select a range of Comp Rows by holding down [Shift] and clicking with the Selection Tool on the first and last
          Comp Row in the desired range.
      !   Don’t double-click on a Comp Row to select it. Double-clicking on a Comp Row will automatically assign the
          recording on it to the segment at the current click position.

      Deleting Comp Rows
      D   Select one or several Comp Rows (see “Selecting Comp Rows”) and then press [Backspace] or [Delete], or se-
          lect “Delete” from the Edit menu or context menu.
      D   Alternatively, select the Eraser Tool and click anywhere on the Comp Row you wish to delete.

      Moving Comp Rows
      Moving Comp Rows up or down on the Edit Pane can be useful to make it faster and easier and to access the de-
      sired Comp Rows when editing a comped clip. Let’s say you have recorded six takes but you’re only going to edit
      takes 1, 3 and 5. In this case, it would be more practical to have these Comp Rows right below one another at the top
      of the Edit Pane.
      D   To move a single Comp Row up or down, click and hold the Comp Row Handle and drag vertically.
          A red insertion line is shown, indicating where the Comp Row will be placed after you release the mouse button.

          Moving a Comp Row.
      D   To move several Comp Rows in one go, select them and then click and hold one of the selected Comp Row
          Handles and drag to the new destination.
          A red insertion line is shown, indicating where the Comp Rows will be placed after you release the mouse button.
          Note that if you move non-adjacent Comp Rows, they will be placed as a group (adjacent) on the Edit Pane.
      D   To move Comp Rows between clips, use the cut/copy and paste functions described in “Cutting, copying and
          pasting Comp Rows”.
      D   Moving Comp Rows sideways is the same as changing the Recording Offsets - see “Adjusting the Recording
          Offset” for more details.

      Duplicating Comp Rows
      Duplicating Comp Rows can be useful if you want to re-use the same part of a take several times in a comped clip.
      Duplicate the Comp Row and then adjust the Recording Offset (see “Adjusting the Recording Offset”) in the dupli-
      cated Comp Row to access the same part of the recording in another segment of the comped clip. Duplicating Comp
      Rows will not use up any more space on your hard disk, so you can do this as many times as you like.
      D   To duplicate one or several Comp Rows, select them and hold [Ctrl](Win) or [Cmd](Mac) and press [D], or se-
          lect “Duplicate Comp Rows” from the Edit menu or context menu.
          The duplicated Comp Rows will be placed below the lowest selected Comp Row. Note that if you duplicate non-
          adjacent Comp Rows, they will be placed as a group (adjacent) below the lowest selected Comp Row.
      D   You can also duplicate a Comp Row and assign the duplicated Comp Row to a new segment in one go. With
          the Razor (Cut) Tool selected, hold down [Ctrl](Win) or [Option](Mac) and click, or swipe, on a Comp Row to
          assign a new segment to a duplicate of the recording on a new, additional Comp Row.

      Cutting, copying and pasting Comp Rows
      To move recordings between clips, you can cut or copy and paste Comp Rows as follows:
      1. Select one or several Comp Rows and then hold [Ctrl](Win) or [Cmd](Mac) and press [X] to cut or [C] to copy
         the Comp Rows to the clipboard memory.
          Alternatively, select “Cut” or “Copy” from the Edit menu or context menu.
      2. Open the audio clip into which you want to paste the Comp Row(s).
          This can be in the same song or a different one.
      3. To paste the cut or copied Comp Rows, hold down [Ctrl](Win) or [Cmd](Mac) and press [V] - or select “Paste”
         from the Edit menu or context menu.
          The pasted Comp Rows will be placed at the top of the Edit Pane. Note that if you paste non-adjacent Comp
          Rows, they will be placed below each other, starting at the top of the Edit Pane.
      !   If you paste Comp Rows into another song, the actual audio recordings will be added to that song as well and
          consequently increase the file size.

      Adjusting the Comp Row Level
      If you are comping different Takes where the levels differ a bit, you might want to adjust the levels individually for the
      Takes:
      1. Click on a Comp Row to select it.
          The Comp Row is displayed in a darker color to indicate it’s selected.
      2. Adjust the level, either by clicking and dragging the Comp Row Level Fader, or by adjusting it in the Level (dB)
         display in the Inspector.
          The Level (dB) display is divided into dB and 1/100th of a dB.

          Adjusting the audio level of a recording on a Comp Row.
      3. Repeat the procedure for the other Comp Rows, if necessary.
      D   It’s also possible to edit the entire Clip Level in the Comp Editor by clicking and dragging the Clip Level Handle
          in the Clip Overview.
          Any level adjustments you make on the Comp Row and in the Clip Overview are summed.

      Adjusting the Recording Offset
      In some situations you might want to move, or nudge, the entire recording on a Comp Row to make it play back ex-
      actly when you want. Maybe you just need to fine tune the position by a couple of Ticks:
      1. Click on the Comp Row to select it.
      2. Either click and drag the recording horizontally, or adjust the position in the Recording Offset display in the In-
         spector.
          The Recording Offset display is divided into Bars, Beats, 1/16th notes, Ticks and Subticks. There are 240 Ticks
          for each 1/16th note and 16 Subticks for each Tick.

                                                                          The “Recording Offset” display shows the offset of the
                                                                          recording on the selected Comp Row relative to the Clip
                                                                          Position.
                                                                          If you move the recording on the selected Comp Row back or
                                                                          forth, the Offset Display will update. Similarly, if you resize the
                                                                          Clip by changing its start position (left Clip Handle), the Offset
                                                                          Display will also update.
                                                                          However, If you resize the clip using its right Clip Handle, or
                                                                          move the entire clip, all recordings on all Comp Rows will follow
                                                                          along and the Recording Offset will remain unaffected.

          Adjusting the offset (position) of a recording on a Comp Row.
      You can also nudge the Recording Offset of the selected recording by using the arrow keys on the keyboard.
      D   To nudge the recording in Snap value steps, hold [Ctrl](Win) or [Cmd](Mac) and press the left/right arrow keys.
          Note that Snap doesn’t have to be activated for this to work.
      D   To nudge the recording in steps of Ticks, hold [Ctrl]+[Alt](Win) or [Cmd]+[Opt](Mac) and press the left/right ar-
          row keys.
      D   To nudge the recording in steps of Beats, hold [Ctrl]+[Shift](Win) or [Cmd]+[Shift](Mac) and press the left/
          right arrow keys.
      q   To make it easier to find the exact positions in the recording, you can audition the recording at desired posi-
          tions (see “Speaker Tool”).

      Comping audio
      In this section we will describe procedures that are specific to audio editing in Comp clips. At the end of this section
      is a detailed example on how to use the various procedures to create a complete comped audio clip - see “Creating
      a comped audio clip”. General audio editing procedures are described in “Editing audio in the Comp Editor”.

      Adding Cuts
      !   If the clip is in Single Take mode, because a Single Take Mode button is depressed, you will have to click that
          Single Take Mode button to deselect the Comp Row before you can start adding Cuts!
      !   If the clip only contains one single (not manually selected) Comp Row, and thus is a Single Take clip, adding a
          Cut on the Silence Row will automatically turn the clip into a Comp clip.
      D   Place the Razor Tool on the Comp Row which contains the recording you want to assign, and click.
          A new Cut Handle is added on the Cut Row. The recording to the right of the Cut Line on the Comp Row is as-
          signed to a new Segment:

          Assigning the recording on the “Take4” Comp Row to a new Segment.
      D   Click with the Razor Tool on the Silence Row to assign silence to a new Segment to the right of the cursor.
      D   Click with the Razor Tool on the Cut Row to create a new Cut without changing the currently assigned record-
          ing.
          A new Cut Handle is added on the Cut Row. The previous recording assignment is retained throughout the new
          segment.
      • If you hold down [Ctrl](Win) or [Option](Mac) and click with the Razor tool on a Comp Row, this will first create
        a duplicate of the Comp Row. Then, the duplicated Comp Row will be assigned to the new Segment.
          You can then adjust the timing (Recording Offset) or level of the duplicated Comp Row as needed, without affect-
          ing any segments playing the original Comp Row.
      !   Note that Snap is taken into account (if activated).
      q   A quick way to toggle Snap on or off is to press [S].
      q   For a practical example on how to add Cuts, see “Creating a comped audio clip”.
      q   It’s also possible to assign a complete Segment, with a start and end Cut, by swiping with the Cut Tool on the
          Comp Rows - see “Adding Segments”.

      Adding Segments
      The Razor Tool can be used for assigning a complete Segment, with a start and end Cut, by clicking and dragging
      (swiping) the Razor Tool horizontally on the desired Comp Row.
      D   Swipe (click-hold and drag) with the Razor Tool to assign a part of a Comp Row to a new segment.

          Place the Razor Tool on the desired start position on a               ...and release where you want the segment to end.
          Comp Row and swipe...

      D   To insert a new Segment in an existing Segment, swipe with the Razor Tool on a Comp Row or on the Cut Row.
          Swiping on a Comp Row will automatically assign the recording on that Comp Row to the new segment. Swiping
          on the Cut Row will insert a new segment but won’t change the recording assignment. The result after inserting a
          new segment in an existing segment is three separate segments. Swiping over an existing Cut will remove that
          Cut.
      • If you hold down [Ctrl](Win) or [Option](Mac) and click or swipe with the Razor tool on a Comp Row, this will
        first create a duplicate of the Comp Row. Then, this duplicated Comp Row will be assigned to the new Seg-
        ment.
          You can then adjust the timing (Recording Offset) or level of the duplicated Comp Row as needed, without affect-
          ing any segments playing the original Comp Row.
      !   Note that Snap is taken into account (if activated).
      q   A quick way to toggle Snap on or off is to press [S].
      q   For a practical example on how to add a Segment, see “Creating a comped audio clip”.

      Adding Crossfades to Cuts
      To add a crossfade zone to a Cut (between two Segments), proceed as follows:
      D   Select a Cut Handle and then drag the Cut Crossfade Handle to the right.

            Click and drag the Cut Crossfade Handle...              ...to introduce a crossfade between the segments.

          The crossfade slopes are indicated by curves on the assigned Segments. The longer the crossfade time, the flatter
          the curves.
      D   To remove a crossfade, simply drag the Cut Crossfade Handle all the way to the left.

      Deleting Cuts
      D   To delete a Cut, click on the left Cut Handle and press [Backspace] or [Delete], or select “Delete” from the Edit
          menu or context menu.
          The segment to the right of the deleted Cut will be deleted. The segment to the left of the deleted Cut will expand
          and replace the deleted segment:

           Click on a Cut Handle to select it.                           Press [Backspace] or [Delete] to delete the
                                                                         segment to the right of the Cut Handle.

      D   Alternatively, select the Eraser Tool and click on the Cut Handle.

      Moving Cuts
      Moving Cuts has a similar effect to resizing a clip, i.e. you select what part of the recording on the Comp Row should
      be active for playback. Recordings outside the active segment on the Comp Row will be masked (silent) but not af-
      fected in any other way.
      D   To move a Cut, click and hold its right Cut Handle, or Cut Line, and drag it horizontally in either direction.
          The segment to the left of the Cut Line will be resized. The segment to the right of the resized segment will now
          have a new start position:

           Click on a Cut Handle to select it.                           Drag the Cut Handle to horizontally to move it.

      !   Recordings in the segments will not be moved back or forth - only masked according to the current positions
          of the Cut Handles/Lines. Any Cut Crossfades will also move along with the Cut Handles/Lines.
      !   Two Cuts can never exist on the same position. If you drag a Cut to the position of another Cut and release the
          mouse button, the moved Cut will disappear. If you do this by mistake, you can always use the Undo function.
      D   To move a Cut and have the recording on the Comp Row move along with the Cut, select the Comp Row and
          the Cut Handle using the standard [Ctrl]-click (Win) or [Shift]-click method. Then, click and drag the Cut to the
          desired position.
      !   Note that Snap is taken into account (if activated).
      • It’s also possible to use the Inspector to move Cuts numerically - see “Editing recordings and cuts in the In-
        spector”.

      Changing Comp Row assignments
      When you have created a comped audio clip, you might later want to change which Comp Rows are assigned to play:
      D   Choose the Selection Tool and double-click on the Comp Row that contains the recording you want to assign
          to the Segment.
          Make sure you double-click in the area between the desired Segment’s Cut Lines.

            Double-click on the Comp Row you want to                         The segment will now play back this recording
            assign to the segment.                                           instead.

      You can also use keyboard commands to change comp row assignments and segment focus as follows:
      D   Hold down [Ctrl](Win) or [Cmd](Mac) and press the up/down arrow keys to select which Comp Row that
          should be assigned.
      D   To change Segment focus, hold down [Ctrl]+[Alt]+[Shift](Win) or [Cmd]+[Option]+[Shift](Mac) and press the
          left/right arrow keys.
          This will move the Segment Focus Indicator between the segments. Note that you can still change comp row as-
          signments using this keyboard command together with the up/down arrow keys.

                     Cut Row

                                                           Segment Focus Indicator

          The Segment Focus Indicator shows which segment has currently focus.


=== END OF PART ===
