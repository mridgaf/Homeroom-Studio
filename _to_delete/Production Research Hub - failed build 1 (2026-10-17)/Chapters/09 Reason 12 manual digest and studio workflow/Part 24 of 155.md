# Chapter 09: Reason 12 manual digest and studio workflow
## Part 24 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 15 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 25 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 15 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 7: Arranging in the Sequencer

Arranging in
the Sequencer

      About this chapter
      This chapter describes how you can arrange and work with the clips in your song. The chapter covers both audio,
      note and parameter automation clip arrangement. Special arrangement techniques pertaining to the Blocks View are
      described in the separate chapter “Working with Blocks in the Sequencer”.
      Before reading this chapter, it’s recommended that you are familiar with the sequencer functions and definitions de-
      scribed in the “Sequencer Functions” and “Recording in the Sequencer” chapters.

      Clip handling
      Clip arrangement in the sequencer is done mainly in the Song View - but could also be done in Edit Mode, if the clips
      you’re arranging are on the same lane. The descriptions in this chapter refer to arrangement in the Song View, unless
      otherwise stated.

      Creating Clips
      Clips are created automatically when you record, but you can also create empty clips and add notes and other events
      in them by drawing with the Pencil Tool.
      D   To create a clip, double click with the Selection (Arrow) Tool on a track.
          This will create an empty clip with the length of the current Snap value setting (e.g. 1 bar). To create longer clips,
          double click, keep the mouse button pressed and drag to the right.
      D   You can also create clips by selecting the Pencil Tool and drawing on a Lane in the sequencer.

      Selecting clips
      D   To select any type of clip in the Song View, just click on it.
          A selected clip is indicated with a thick black border with Clip Resize handles on either side. In Edit Mode, the Clip
          Resize handles appear in the Clip Overview area.

                          Audio clip
                                                      Clip Resize handles

                  Note clip                          Parameter automation clip
                                                                                                        Pattern clip

          Selected clips in Song View.
      D   To de-select clips, just click anywhere on the Arrange Pane background.

      Inspector displays for selected clips
      In the sequencer Inspector, the Position and Length displays shows the start position and length of the selected clip.
      For selected audio clips, four additional displays are shown: Fade In, Fade Out, Level and Transpose. If several clips
      are selected, the displays show the values for the earliest (or topmost) selected clip in the song.

      The Inspector displays for selected Audio Clips.
      • Clip Position display
          The clip Position display shows at what position in the song the clip begins. The display readout is divided into Bar,
          Beat, 1/16 Note and Ticks (1/16th note=240 Ticks). The position can be edited according to the descriptions in
          “Moving clips using the Inspector”.
      • Clip Length display
          The clip Length display shows the length of the clip. The display readout is divided into (from left to right) Bar,
          Beat, 1/16 Note and Ticks. The length can be edited according to the descriptions in “Resizing clips using the In-
          spector”.
      • Fade In and Fade Out displays (audio clips only)
          The Fade In and Fade Out displays for selected audio clips show the Fade In and Fade Out times for the audio in
          the clip. The readout is divided into 1/16 Note and Ticks. The Fade times can be edited as described in “Inspector
          segment displays”.
      • Level display (audio clips only)
          The Level display for selected audio clips shows the level of the audio in the clip. The readout is divided into dB
          and 1/100 dB. The level can be edited as described in “Inspector segment displays”.
      • Transpose display
          The Transpose display shows the transposition of the audio recordings in the selected Audio Clip(s) - relative to
          the original pitch. The display readout is divided into (from left to right) Semitones and Cents, See “Transposing
          Audio Clips”.

      Selecting multiple clips
      In Song View, several clips can be selected, e.g. for cutting, copying, pasting, deleting, moving and resizing purposes.
      If you select multiple note clips, these can be opened for Multi Lanes editing, see “Multi Lanes editing”.
      D   Press [Ctrl](Win) or [Shift](Mac) and select the clips.
          Under Windows, you can also press [Shift] and click to select a range of clips on the same lane.

      D   Draw a selection rectangle with the Selection Tool (arrow) on the Arrange Pane background.

          Click, hold and draw a rectangle with the Selection Tool to select multiple clips.
          All clips that are touched by the selection rectangle will be automatically selected when the mouse button is re-
          leased.
      D   If you hold down [Shift] when you select clips with the selection rectangle technique, any previously selected
          clips will remain selected.
          This allows you to make multiple, non-contiguous selections: first select some clips, then hold [Shift] and select
          some more clips, and so on.
      D   Use the “Select All” function on the Edit menu or on the clip context menu to select all clips in the song.
          Alternatively, hold down [Ctrl](Win) or [Cmd](Mac) and press [A].
      • You can also select multiple clips in the Clip Overview area in Edit Mode - if the clips are on the same lane.

          Two selected clips in the Clip Overview area in Edit Mode.

      Selecting clips with the arrow keys
      Another way of selecting clips on the Arrange Pane is to use the arrow keys on the computer keyboard.
      D   Press the [Left] or [Right] arrow keys to select the previous or next clip on the lane.
      D   Press the [Up] or [Down] arrow key to select the closest clip on the lane above or below.
      D   Hold down [Shift] and use the [Left]/[Right] arrow keys to make multiple selections on the same lane.

      Setting audio clip Level and Fades
      Besides the Clip Resize handles, a selected audio clip also has Fade In and Fade Out handles plus a Clip Level han-
      dle. These can be edited at any time, either by using the handles as described below, or using the Inspector as de-
      scribed in “Fade In and Fade Out displays (audio clips only)” and “Level display (audio clips only)”:
                                        Clip Level handle

                                                        Clip Fade handles

          A selected audio clip in Arrange Mode.

      Fade In and Fade Out Handles
      D   Click and drag these handles horizontally to introduce a fade in and/or fade out of the audio in the clip.
          The Fade settings can be set individually for each audio clip in the song. The fading is non-destructive and can be
          changed at any time. If Snap is activated (see “Snap”), the set Snap value is taken into account when setting the
          fade time(s).

      Clip Level Handle
      D   Click and drag this handle vertically to adjust the audio level in the audio clip.
          The Level can be set individually for each audio clip in the song. The Level setting is non-destructive and can be
          changed at any time.

      Deleting clips
      D   To delete a clip, select it and press [Delete] or [Backspace] or select “Delete” from the Edit or context menu.
          You can also draw selection rectangles with the Selection tool, encompassing several clips and delete them all at
          once. The same rules apply as when selecting clips (see “Selecting clips”).
      !   If you delete an audio clip which contains recordings that are not used elsewhere in the song, those audio re-
          cordings will be permanently deleted! However, if you accidentally erase an audio clip, you can always use the
          “Undo” function.

      Deleting clips with the Eraser tool
      You can also use the Eraser tool to delete clips on the Arrange Pane. The Eraser tool can be used in two ways: you
      can click on single clips or you can make a selection rectangle encompassing several clips:
      D   Select the Eraser Tool and click on the clip you want to delete.

          Select the Eraser Tool and click on the clip you want to delete.
      Alternatively, if you want to delete multiple clips:
      D   Select the Eraser Tool, click and hold the mouse button and draw a selection rectangle on the Edit/Arrange
          Pane background.

          Click, hold and draw a rectangle with the Eraser Tool to erase multiple clips.
          All clips that are touched by the selection rectangle will be deleted once you release the mouse button.

      Resizing (masking) clips
      All clip types can be resized by clicking and dragging either of the Clip Resize handles on the selected clip(s). This
      can be done both in the Song View and in Edit Mode. In Edit Mode, the Clip Resize handles appear in the Clip Over-
      view area.

                                   Clip Resize handles
      A selected note clip.
      If you resize a clip and make it smaller, any recordings or events that now lie outside the clip boundaries will not
      sound, or have any effect, when played back. However, they are not deleted - just masked. If you make the clip larger
      again, the recordings or events that were masked will become visible and will play back again. See “About masked re-
      cordings and events”.
      If you enlarge an unmasked clip, nothing special will happen except that the clip “window” becomes larger.
      • If you resize an audio clip which uses Fade In and/or Fade Out, the fade slopes will follow along, unaffected,
        with the clip boundaries.

      Resizing multiple clips
      It’s possible to resize several clips by first selecting the clips, and then dragging a Clip Resize handle on one of the
      selected clips. All selected clips will be resized by the same amount.

      Resizing clips using the Inspector
      Another way of resizing clips is to change the clip length(s) in the Inspector. This can be done in the following way:
      D   Select one or several clips on the Arrange Pane and then change the Length value in the Inspector by clicking
          on the up/down arrow buttons.
          In the example below, we expand the clip lengths by 2 bars by clicking the up arrow button twice.

          All selected clips become 2 bars longer.
      q   See “Inspector segment displays” for more details on how to edit in the Inspector displays.
      • If the Tick segment in the Length display shows an asterisk (*), it means that the value is a fraction of a Tick - a
        subtick. See “About subticks in the Position and Length displays” for more info.

      About masked recordings and events
      A note or parameter automation clip which contains masked events is indicated by white corners on the left, right or
      both clip boundaries:

      The position of the white corners indicate on which side of the clip boundary the masked events exist:

                                                                     Masked events to the right of the clip

                                                                     Masked events to the left of the clip

                                                                     Masked events on both sides of the clip

      !   Audio clips don’t have any indication if they contain masked recordings.

      Masked recordings in audio clips
      If you resize an audio clip and make it smaller, the masked part of the recording will be silent during playback. If you
      open a masked audio clip in the Comp Editor, the part of the recording that will actually play back is shown in the Clip
      Overview area. The masked part of the recording will appear grayed out on a Comp Row:
                 Clip start              Clip end                                    Clip start         Clip end

                                                                        Masked part of the recording

      An open audio clip before and after masking.

      Masked events in note and parameter automation clips
      In the picture below is an open note clip in Edit Mode with notes and performance controller events, before and after
      resizing the clip:
               Clip start                 Clip end                               Clip start              Clip end

                                                                                                            Masked
                                                                                                            events

               An 8-bar note clip with notes and                                  The same note clip resized to 4 bars
               performance controller events.

      After resizing the clip from 8 to 4 bars, all events that begin in bars 5-8 are now masked and won’t play back. All
      masked events will still be there - and follow along with the clip if the clip should be moved, cut or copied.
      Masked events will be a blue color on the Note Edit Lane, to indicate that they won’t play back. The first three-note
      chord in the masked area is still an orange color. That’s because the notes begin in bar 4 (just before the downbeat)
      and thus will play back in their entirety, also after resizing the clip.
      Masked performance controller events, parameter automation events and pattern automation events will be inactive
      - but could still affect the masked clip (see “About masked performance controllers and automation events” below).
      Outside a masked clip, the controller/parameter/pattern values will default to their Static Values in the masked area
      (see “Static Value Handles”).
      !   Note that just switching to Edit Mode won’t show masked events. A clip has to be opened before you can view
          these events. You can remove all masked note and parameter automation events using the “Crop Events to
          Clips” function on the Edit menu (see “The “Crop Events to Clips” function”).

      About masked performance controllers and automation events
      Masked performance controller and parameter automation events just outside a clip can still affect the clip, since
      they affect the curve shape. The example below shows a masked note clip with Mod Wheel performance controller.

                                                 Masked event which still affects the clip

      The first Mod Wheel automation event to the right of the masked part of the clip determines the direction of the au-
      tomation curve from the last event in the unmasked area. These types of automation events are not blue, but black
      and white, just like unmasked events.
      The result in this example is that the Mod Wheel value will continue to rise all the way to the end of the masked clip,
      at which point the value will drop down to the Static Value - in this case “0”.

      The “Crop Events to Clips” function
      There may be situations when you want to delete all masked events, i.e. events located outside the left and/or right
      clip boundaries. This function only works for note and parameter automation clips and will delete all masked notes
      that begin in the masked clip section, plus any performance controller or parameter automation events:
      1. Reduce the size of the clips to your liking.
      2. Select one or several clips and choose “Crop Events To Clips” from the Edit menu or from the context menu.
      3. After the cropping operation, all events outside the clip have been deleted.

      Tempo scaling clips
      It is possible to tempo scale the content of clips, i.e. make the clip play back at faster or slower tempos. This can be
      achieved in two different ways:
      • By manually stretching selected clip(s).
      • By editing the tempo scaling numerically in the Tool Window.
      !   Tempo scaling can be applied to all clip types, except for Time Signature automation clips.
      !   Note that Pattern Automation Clips will only be resized - the pattern tempo in the source device will NOT be
          scaled but will still be synced to the main sequencer tempo!

      Below, we will describe how to use the “scale tempo” tool to manually stretch clips. Numerical tempo scaling in the
      Tool Window is explained in “Scale Tempo” in the “Note and Automation Editing” chapter.
      1. Select one or several clips, either on the arrangement pane in Song/Blocks View, or in the Clip Overview in
         Edit Mode.
      2. With the Arrow Tool selected, hold down [Ctrl](Win) or [Option](Mac) and place the mouse cursor over one of
         the Clip Resize handles.
        When you reach any of the Clip Resize handles, the arrow symbol switches to a “scale tempo” arrow.

      3. Hold down [Ctrl](Win)/[Option](Mac) and click and drag the cursor sideways in either direction to scale the
         tempo of the clip contents.
        In this example, we make the “stretched” clip four bars longer by dragging the right clip handle one bar to the right.

        Now, all clips have been tempo scaled and the clip content have been stretched to match the new clip length. Note
        that the content of all selected clips have been scaled proportionally. The Pattern Clip has only been resized,
        though. The pattern tempo in the source device has NOT been scaled.
        For more details about tempo scaling audio clips, refer to “Tempo scaling Clips” in the “Audio Editing in the Se-
        quencer” chapter.

      Moving clips
      Moving clips on the same lane
      D   To move a clip, drag and drop it to the desired destination on the lane.
          It’s also possible to select and move several clips by dragging and dropping them at the desired destination. If the
          Snap function is selected (see “Snap”), you will only be able to move the clip(s) in steps of the selected Snap value
          - or to absolute positions on the grid, depending on the Snap settings.
      D   You can also use the “Cut” and “Paste” functions on the Edit menu or context menu to cut the selected clip(s)
          and then paste them at the current Song Position Pointer position (see “Cutting, Copying and Pasting clips”).

      Nudging clip positions
      You can use the left and right arrow keys on the computer keyboard to “nudge” the positions of selected clips in a
      couple of different ways:
      1. Select the Snap value by which you want to nudge the clip(s).
      2. Press [Ctrl](Win) or [Cmd](Mac) and use the Left and Right arrow keys to move the clip position back or for-
         ward by the set Snap value.
          It doesn’t matter if Snap is on or off - the clip will always be moved in steps of the set Snap value.
      D   Press [Ctrl]+[Alt](Win) or [Cmd]+[Option](Mac) and use the left and right arrow keys to move the clip position
          back or forward in Tick increments.
          There are 240 ticks per 1/16 note so this is very fine editing - check the tick positions in the inspector when you
          nudge because typically you won’t “see” the position changes unless you’re working at a high zoom level.
      D   Press [Ctrl]+[Shift](Win) or [Cmd]+[Shift](Mac) and use the left and right arrow keys to move the clip position
          back or forward in Beat increments.

      Moving clips using the Inspector
      Another way of moving clips is to change the clip position in the Inspector. This can be done in the following way:
      D   Select one or several clips on the Arrange Pane. Then, change the Position value in the Inspector, either by
          clicking on the Up/Down spin controls, or by using any of the methods described in “Inspector segment dis-
          plays”.
          In this example, we move the clips position 2 bars forward by clicking the “Up” spin control twice.

          All selected clips are moved forward by 2 bars.
      • If the Tick segment in the Position display shows an asterisk (*), it means that the value is a fraction of a Tick -
        a subtick. See “About subticks in the Position and Length displays” for more info.

      Moving clips between lanes
      You can move clips between lanes, either on the same track or between lanes on different tracks:
      D   Click and drag the clip(s) to the desired position on the new lane.
          The set Snap value is taken in to account if the function is activated (see “Snap”). It’s also possible to move several
          selected clips in one go.
      D   Hold down [Shift] when you drag the clip(s), to restrict the clips to vertical movement.
      !   If you want to move several clips in the Windows version of Reason, press the [Shift] key after you have
          pressed the mouse button, otherwise pressing [Shift] will select or deselect clips, and that’s not what we want
          here.
      !   For a successful result, it’s important that the source and destination lanes are of the same, or similar, type
          (see “About alien clips” below).

      About alien clips
      An alien clip is a clip containing types of event, or different parameter range/resolution, other than that the lane is in-
      tended for. For example, if we move a note clip from a note lane to a parameter automation lane, the note clip would
      become alien and won’t play back on the automation lane:

      If a note clip is moved from a note lane to a parameter automation lane, for example, the clip becomes alien.
      An alien clip can be distinguished by its red stripes, which indicate that the clip is currently inactive. If you place the
      cursor over an alien clip, a tool tip appears with detailed information:

      Tool tip for an alien note clip.
      • A parameter automation clip can also become alien if it is moved to a parameter automation lane for a param-
        eter with a different range or resolution.
          In most cases, you can resolve this by first selecting the clip and then selecting “Adjust Alien Clips to Lane” from
          the Edit menu or from the context menu.
          For example, if a parameter automation clip for a parameter that has a bipolar (-64 to 63) value range is moved to
          a parameter automation lane with a unipolar (0 to 127) value range, it will become alien. Selecting “Adjust Alien
          Clips to Lane” from the Edit menu or context menu will adjust the parameter automation events of the clip to fit the
          range of the parameter on the destination lane.

      Moving clips with performance controller automation to another track
      If you move note clips that contain performance controller automation events to another track (for a different type of
      instrument device), there are a few things to note:

      • If you have only recorded standard performance controllers (Pitch Bend, Mod Wheel and Sustain pedal) in the
        note clip, these will usually translate without any problems when moved to another device track.
          Be aware that all devices do not respond to all performance controllers - the Malström device, for example, does
          not respond to Aftertouch, Expression or Breath performance controller data.
      • If you have recorded non-standard controller parameters for a device in the note clip using the “Record Auto-
        mation into Note Clip” option (see “Recording parameter automation into Note Clips”) some automated pa-
        rameters may not have an equivalent parameter in the target device.
          In such cases the automation data for an incompatible controller will simply be ignored.
      • Parameters common to most instrument devices (filters, envelopes etc.) will be transferred to the target device
        whenever applicable.

      About overlapping clips
      If you move or resize clips so that the clips overlap each other, the following rules apply:
      • Clips or sections of clips that are hidden (overlapped) will not play back.
          Any lane can only play back a single clip at a time - if you want to mix two clips, put them on separate lanes (note
          clips) or on separate tracks (audio clips). See “Adding note lanes” and “Duplicating/copying tracks and devices”.
      • The clip with the latest start position have priority (and will be played back).
          This means if a shorter clip is placed “in the middle” of a longer clip, as in the picture below, the sequencer will play
          the beginning of the long clip, then the shorter overlapping clip and then the end of the long clip.

      !   If both clips start at the same position and have the same length, the clip which was moved last will sound.
          Consequently, the “hidden” clip won’t play back at all.
      !   Note that it’s possible to cross-fade adjacent audio clips, for smooth overlaps. See “Crossfading audio clips”.

      Duplicating clips
      D   To duplicate selected clips, hold down [Ctrl](Win) or [Option](Mac), then click with the Selection Tool and drag
          a copy of the clip(s) to the desired destination.
          As you begin dragging, the cursor displays a “+” sign next to it to indicate duplication.
      • You can use the Duplicate function ([Ctrl]/[Cmd]-[D]) to quickly make copies of clips, lined up after each other
        and spaced according to the Snap value.
      • It’s also possible to duplicate only a part of one or several clips by using the Razor Tool as described in “Dupli-
        cating a part of one or several clips”

      Cutting, Copying and Pasting clips
      You can move or duplicate clips using the “Cut”, “Copy” and “Paste” commands on the Edit menu or the context
      menu. When you paste, the clips will end up at the current song position, on their original lane(s).
      If you paste a clip into another Reason song document, the pasted clip will be placed on the track with edit focus, if
      possible. Typically, you can just select a track in the other document, place the song position pointer where you want,
      and paste the clip(s) onto the selected track.
      New tracks will be created when necessary. Since all tracks must have a device associated with them, the new tracks
      will be associated with empty Combinator devices. You can then use the Patch browser on the Combinator to select
      a suitable patch and device type. The above rules also apply when pasting alien clips and parameter automation clips.


=== END OF PART ===
