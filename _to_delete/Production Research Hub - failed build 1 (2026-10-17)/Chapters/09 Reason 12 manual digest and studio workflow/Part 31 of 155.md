# Chapter 09: Reason 12 manual digest and studio workflow
## Part 31 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 22 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 32 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 22 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 9: Note and Automation Editing

Note and Automation
Editing

      About this chapter
      This chapter describes how to edit note and parameter automation events after they have been recorded in the se-
      quencer. It also describes how to manually create note and automation events in clips. General sequencer functions,
      recording, editing audio, arranging in the sequencer and working with Blocks are described in detail in the chapters
      “Sequencer Functions”, “Recording in the Sequencer”, “Audio Editing in the Sequencer”, “Arranging in the Sequencer”
      and “Working with Blocks in the Sequencer”.

      The Edit Mode
      After you have recorded in note clips or parameter automation clips, you might want to edit and correct any mistakes
      you made during the recording. For example, if you accidentally hit the wrong notes or used the Mod Wheel too ex-
      tensively when you recorded a note clip, there is no need to redo the recording. Individual notes and parameter auto-
      mation events can easily be edited and corrected in a number of different ways.
      Edit Mode in the sequencer is where you can perform detailed editing of note and automation events.
      D   To enter Edit Mode, either double-click a note clip in the Song/Block View, or select the note clip and press
          [Return] - or click the Edit button in the Toolbar, or right click a note clip and select Edit from the context menu.
          Alternatively, hold down [Ctrl](Win) or [Cmd](Mac) and press [E].

          Double-clicking a note clip in the Song/Block View opens it for editing in Edit Mode.
      D   Exit Edit Mode by pressing [Esc], or by clicking the Close or Edit button, or by holding [Ctrl](Win) or
          [Cmd](Mac) and pressing [E].

          Click the Close button to close the clip and revert to the Song/Blocks View.
      D   Toggle between the Song/Block View and Edit Mode by pressing [Shift]+[Tab] or by holding [Ctrl](Win) or
          [Cmd](Mac) and pressing [E].

      Selecting what to edit
      The Edit Mode shows the contents of a single lane at a time on the Edit Pane - unless you use the Multi Lanes func-
      tion, described in “Multi Lanes editing”, where you can see the contents of multiple note lanes in a “ghosted” fashion
      underneath the currently open clip. On instrument tracks, only one note lane can have edit focus at a time.
      • If a track is selected when you enter Edit Mode, the contents of the note lane with edit focus will be shown.
        Also, all parameter automation lanes will be shown at the bottom of the Edit Pane. If a single clip was selected on
        the note lane with edit focus when you switched to Edit Mode, it will automatically be opened. If no clip was se-
        lected, the events will be grayed out. To be able to edit or draw notes and/or automation events, you need to open
        the clip, for example by double-clicking it (see “Opening note and automation clips for editing”).
      • If the selected track has multiple note lanes, the contents of the currently selected note lane will be shown.
        To switch edit focus between note lanes, click on the note lane handle in the Track List.

        A note lane handle.
      • You can change track and note lane edit focus at any time, by clicking in the Track List.
        This way you can stay in Edit Mode and change edit focus between different tracks and note lanes, without having
        to go back to the Song/Block View.

      Opening note and automation clips for editing
      Open a note clip for editing
      Note clips can contain both note events - with velocity values - and performance controller events. By default, perfor-
      mance controllers include Mod Wheel, Pitch Bend, Sustain Pedal, Aftertouch, Expression and Breath Controller.
      However, the controller configuration can easily be changed (see “Creating new performance controller automation
      lanes” and “Deleting performance controller automation lanes”).
      In the Song/Block View, note events are displayed in a “piano roll” fashion whereas performance controllers are dis-
      played as curves or lines in the clip. In the Song/Block View, it’s not possible to distinguish one performance control-
      ler from another since all controllers are displayed together in the clip. The note clip in the picture below contains
      note events and Mod Wheel and Pitch Bend performance controller events:

      D   To edit the events in a note clip, open the clip by double-clicking it, or select it and press [Return].
          Opening a note clip in the Song/Block View automatically switches the sequencer to Edit Mode.

          Double-clicking a note clip in the Song/Block View...

          ...opens it for editing in Edit Mode. An open clip in Edit Mode is highlighted.
      D   Double-click on a closed (grayed out events) note clip in Edit Mode to open it for editing in Edit Mode.
          You can double-click in the Clip Overview, Note Edit Lane or any of the Performance Controller Edit Lanes (if any).
      D   To close a clip, press [Esc], click outside the open clip in the Clip Overview, or click the Close button.
          If you opened the clip from the Song/Block View, pressing [Esc] will automatically switch the sequencer back to
          the Song/Block View.

      Open a parameter automation clip for editing
      A parameter automation clip contains automation events for a single parameter.
      D   Double-click a parameter automation clip in the Song/Block View to open it for editing in the Song/Block
          View. Alternatively, select the clip and click the Edit Inline button in the Toolbar.
          The parameter automation lane expands in height to make it easier to edit the automation events. Now you can
          edit the parameter automation events without needing to switch to Edit Mode. This is very practical if you want to
          perform quick editing of automation events.

          A parameter automation clip before and after opening it in the Song/Block View.
      D   To close an open parameter automation clip in the Song/Block View, press [Esc] or click on another lane.
      See “Editing parameter automation in the Song/Block View” for information on how to edit parameter automation
      events in the Song/Block View.
      D   To open a parameter automation clip in the Song/Block View for editing in Edit Mode, double-click the clip
          and then click the Open In Edit Mode button. Alternatively, select the clip and click the Edit Mode button in the
          Toolbar.

      D   Double-click on a parameter automation clip in Edit Mode to open it for editing in Edit Mode.

          A parameter automation clip before and after opening it in Edit Mode.
      D   To close an open parameter automation clip in Edit Mode, press [Esc] or click anywhere on another lane.
      See “Editing parameter automation in Edit Mode” for information on how to edit parameter automation events in Edit
      Mode.

      Edit Mode elements
      In Edit Mode, a note clip is divided into various Edit Lanes which are used for editing different types of events and val-
      ues (i.e. note events, velocity values and performance controller automation events). At the bottom, any parameter au-
      tomation lanes on the track will also be shown. The different Edit Lanes can be resized by adjusting the horizontal
      dividers between the lanes. You can also scroll and zoom on each Edit Lane by using the scroll bars and Vertical
      Zoom tools on the right hand side of the Edit Pane.
                Interactive Keyboard
                   Close button                                                                             Clip Resize Handles
                                                                                                           Clip Overview

                                                                                                            Vertical Zoom tools

                                                                                                            Note Edit Mode Selector

                                                                                                            Performance Controller
                                                                                                            Automation Selector
                                                                                                            Note Edit Lane

                                                                                                            Velocity Edit Lane

                                                                                                            Vertical Zoom tools
                                                                                                            Performance Controller
                                                                                                            Edit Lanes

                                                                                                            Vertical Zoom tools

                                                                                                            Parameter Automation
                                                                                                            Lanes

                Static Value Handles

      The picture shows three note clips in Edit Mode. The center clip is open for editing and therefore highlighted. Adjacent (closed) clips on
      the same lane are visible but the events are grayed out.

      From the top down in the picture above, the Edit Pane contains the following elements:
      • Interactive Keyboard
        The interactive Keyboard highlights the notes you play on your MIDI keyboard, as well as notes you edit on the Edit
        Pane. You can also play (and record) notes by clicking on the Interactive Keyboard.
      • Close button
        Click the Close button to exit Edit Mode and return to the Song/Block View.
      • Clip Resize Handles
        By clicking and dragging either of the handles, you can change the position and length of the clip.
      • Clip Overview
        The Clip Overview shows the note clips of the note lane which has edit focus. You can select one or several clips
        in the Clip Overview and perform clip-based editing (e.g. moving and resizing) - just like in Arrange Mode.
      • Note Edit Mode Selector
        To the right of the Note Edit Lane, below the Vertical Zoom tools, is the Note Edit Mode Selector. Click to choose
        between Key Edit, Drum Edit or REX Edit Mode. Depending on selected mode, the Note Edit Lane will display dif-
        ferently. See more about the different modes in “Note Edit Modes”.
      • Performance Controller Automation Selector
        Each performance controller you used when recording the note clip has its own separate Performance Controller
        Edit Lane. You can add or delete performance controller edit lanes from the clip using this selector. See the “Cre-
        ating new performance controller automation lanes” and “Deleting performance controller automation lanes” for
        more details.
      • Note Edit Lane
        Here you can edit the notes of one open clip at a time. Note events are displayed as orange horizontal “boxes” in
        a piano roll fashion on the Note Edit Lane. The left side of each box indicates Note On (key down) and the right
        side Note Off (key up). The color intensity of each box indicates the velocity for the corresponding note. Depend-
        ing on selected Note Edit Mode (see “Note Edit Modes”), the contents of the Note Edit Lane will display differently.
      • Velocity Edit Lane
        The Velocity Edit Lane shows the velocity values for each of the recorded notes. Velocity values are automatically
        recorded together with notes. See more about editing velocity values in “Editing note velocity”.
      • Performance Controller Edit Lanes
        On the Performance Controller Edit Lanes are the performance controller events for Mod Wheel, Pitch Bend, Sus-
        tain Pedal etc. Performance controller events are automatically distributed on separate lanes for each recognized
        controller during recording. Even though performance controllers belong to separate note clips, they will affect all
        active parallel note lanes on a track. See “Automation editing” for details on how to edit performance controller
        events.
      • Parameter Automation Lanes
        Any recorded parameter automation will be shown in separate clips, on separate Parameter Automation Lanes.
        Parameter automation clips don’t “belong” to the note lane or to any note clips, and will not be opened together
        with note clips. Double-clicking on a parameter automation clip will open it for editing. See “Automation editing”.
      • Static Value Handles
        The Static Value Handles to the left of the Performance Controller Edit Lanes and Parameter Automation Lanes
        indicate to what value the automated controller/parameter will default to where there are no clips on the lane. Ba-
        sically, this value reflects the parameter’s initial value, before it was automated. You can easily change a parame-
        ter’s Static Value by dragging the Static Value Handle up or down. See “Automation editing” for more details.

      Edit Mode window handling
      Resizing, zooming and scrolling
      D   You can resize or hide Edit Lanes by dragging the dividers between them.

          Where applicable, individual zoom controls and scrollbars are available to the right of each Edit Lane.
      D   The Magnifying Glass tool can be used for zooming in and out (see “Magnifying Glass Tool”).
      D   The Hand tool can be used for scrolling the view in any direction (see “Hand Tool”).
      D   Use the Song Navigator to scroll and zoom horizontally (see “Areas, windows and basic navigation”).
      D   Click on a Song Navigator Handle and drag horizontally to zoom in and out horizontally (see “Areas, windows
          and basic navigation”).
      D   Shift-click on a Song Navigator Handle and drag horizontally to zoom in and out horizontally, symmetrically
          (see “Areas, windows and basic navigation”).
      D   Shift-click or Right-click (Win) or Ctrl-click (Mac) inside the Song Navigator and drag up or down to zoom in
          and out horizontally, symmetrically (see “Areas, windows and basic navigation”).
      D   Use the Scrollbars to scroll vertically in the respective Edit Lanes.
      D   Click the Zoom buttons to the right to zoom in and out vertically in the respective Edit Lanes.
      • For extensive editing, you may want to maximize the sequencer and/or have it in a separate window covering
        the entire computer screen. Refer to “Areas, windows and basic navigation”.

      Note Edit Modes
      When you switch to Edit Mode, the device used on the selected instrument track determines which Note Edit Mode
      is selected. For instrument tracks associated with synth devices such as the ID 8 device, for example, Key Edit Mode
      is automatically selected. For Redrum tracks Drum Edit Mode is selected and for Dr. Octo Rex tracks the REX Edit
      Mode is automatically selected.
      In all three Note Edit Modes, the note events are shown as “boxes”, with the note length indicated by the width of the
      box and the velocity values indicated by the color intensity of the box (the darker the color, the higher the velocity).
      The basic note editing procedures are the same for all three Note Edit Modes.

      D   You can manually change Note Edit Mode by clicking the Note Edit Mode button in the upper right corner of
          the Note Edit Lane and selecting another mode from the pop-up menu.

          Selecting Note Edit Mode.
          The selected Note Edit Mode is automatically remembered for each note lane on a track. The next time you switch
          to Edit Mode, the correct Note Edit Mode will be recalled for that note lane.

      Key Edit Mode

      Key Edit Mode.
      Key Edit Mode is best suited for viewing and editing notes recorded for instrument devices, such as the ID 8. The pi-
      ano keyboard to the left indicates the notes values, covering the entire MIDI note range (C-2 to G8). By clicking on
      any of the keys, you can audition the notes. As soon as the mouse pointer reaches the keyboard section, the cursor
      changes to a speaker symbol.
      q   Note that the black and white keys are reflected in the background colors of the Note Edit Lane grid, making it
          easier to locate the desired note when drawing and moving note events.

      Drum Edit Mode

      Drum Edit Mode.

      Drum Edit Mode is best suited for viewing and editing notes recorded for a Redrum device. In Drum Edit Mode the
      keyboard has been replaced by a list showing the corresponding Redrum drum sound channel names. If the track is
      associated with another type of instrument device, the list shows MIDI note numbers (0-127) instead. By clicking on
      any of the names (or note numbers) in the list, you can audition the sounds.

      REX Edit Mode

      REX Edit Mode.
      REX Edit Mode is designed for viewing and editing Dr. Octo Rex Loop Player slices. In REX Edit Mode the keyboard
      has been replaced by a list showing the corresponding loop slice numbers in a Dr. Octo Rex device. Slice #1 in the
      list corresponds to the note C3. By clicking on any of the slice numbers in the list, you can audition the corresponding
      sound of the Rex loop.

      Creating empty clips
      When you record in the sequencer, clips are automatically created on the record enabled lane when necessary. How-
      ever, there might be situations when you want to manually draw empty clips in the Song/Block View to record or edit
      in later on:
      D   To create an empty clip, double click with the Selection (Arrow) Tool on a track.
          This will create an empty clip with the length of the current Snap value setting (e.g. 1 bar). To create longer clips,
          double click, keep the mouse button pressed and drag to the right.
      Alternatively, do as follows:
      1. Select the Pencil Tool from the sequencer Toolbar.

      2. Place the Pencil on the lane where you want the clip to begin.
          If you want to create a note clip, draw it on a note lane. If you want to create a parameter automation clip, draw it
          on a parameter automation lane. If Snap is activated, the clip start and end boundaries will snap to the set Snap
          value (see “Snap”).
      3. Click and drag the Pencil to the right where you want the clip to end.

          An empty note clip in the Song View created using the Pencil Tool.
      D   You can also draw empty clips in Edit Mode. A note clip should then be drawn in the Clip Overview and a pa-
          rameter automation clip on the corresponding Parameter Automation Lane.
          If you draw on the Edit Pane in Edit Mode, a note will be created instead. If necessary, a new clip will be automat-
          ically created to surround the note.
      q   See also “Drawing notes” and “Drawing parameter automation events”.

      Tool Window editing tools
      The Sequencer Tools tab in the Tool Window is very useful when you want to perform various note and parameter au-
      tomation editing tasks. Here is how you access the Tool Window and the contents of the Sequencer Tools tab:
      1. Open the Tool Window by selecting “Show Tool Window” from the Window menu. Alternatively, press [F8].
          The [F8] key can be used for toggling between showing and hiding the Tool Window.
      2. Click the Sequencer Tools tab.

                                                              Fold/unfold buttons

          The Sequencer Tools page has a number of panes, each with separate functions.
      D   Click on the arrow buttons to the right of the function name to fold/unfold the corresponding pane.
      D   Hold down [Alt](Win) or [Option](Mac) and click an arrow button to fold/unfold all panes simultaneously.
      The values in the displays on the various panes can be edited in similar ways as in the Inspector. For single-segment
      displays, you can either use the spin controls or click in the display and select a value from a list, or drag up or down
      to change the value. For multi-segment displays, click on a specific segment (e.g. bars, beats, 1/16ths or ticks) and
      then use the spin controls to set the value. Alternatively, click on a segment and drag up or down.

      Note editing
      Notes can be edited using the mouse in Edit Mode. It’s also possible to edit notes by using the functions on the Tools
      tab in the Tool Window. Notes can also be numerically edited in the Inspector, as described in “Note and automation
      editing in the Inspector”.

      Selecting notes
      To select notes in an open clip in Edit Mode, use one of the following methods:
      D   Click on a note event with the Selection (Arrow) Tool.

          The Selection tool.

      • Selected notes are distinguished by a darker color and by the handles at both edges.
          The selected notes are also highlighted in the interactive keyboard to the left.
      D   To select several notes, hold down [Ctrl](Win) or [Shift](Mac) and click on the desired notes, one after the
          other. You can deselect individual notes by [Ctrl](Win)-clicking or [Shift](Mac)-clicking them again. In Win-
          dows it’s also possible to select a range of notes by [Shift]-clicking the first and last note in the range.
      D   You can also click and drag a selection rectangle around the notes you want to select.
      D   You can select the next or previous note on the lane by pressing the right or left arrow key on the computer
          keyboard.
          Holding down [Shift] and using the arrow keys allows you to make multiple selections.
      D   To select all notes of the same pitch (note value) in a clip, double-click the corresponding key in the keyboard
          display to the left in Key Edit Mode.
      D   To select notes of the same pitch(es) of one or several notes, first select the note(s) in the open clip and then
          use the function "Select Notes of Same Pitch" on the Edit menu or context menu.
      D   To select all notes in the open clip, use the “Select All” function on the Edit menu. Alternatively, hold down
          [Ctrl](Win) or [Cmd](Mac) and press [A].
      D   To deselect all notes, click somewhere in an empty area in the clip (where there are no events).

      Drawing notes
      Notes are usually drawn and edited in Key Edit Mode on the Note Edit Lane, but the actions described below also ap-
      ply to the Drum Edit Mode and the REX Edit Mode.
      !   If you want to restrict note input to certain note values (e.g. 1/16th notes), activate Snap (see “Snap”) and set
          the snap value accordingly.

      Drawing single notes
      D   Double click with the Selection (Arrow) tool in the open clip to insert a note with a length of the current Snap
          value.
          This will create a note with the length of the current Snap value setting (e.g. 1/16th note). To create longer notes,
          double click, keep the mouse button pressed and drag to the right.
      Alternatively, do as follows:
      1. Select the Pencil tool.

      q   With the Selection (Arrow) tool selected, you can toggle temporarily between the Selection tool and the Pencil
          tool by holding down [Alt](Win) or [Cmd](Mac). To switch between the Pencil and “Multiple notes” tools (see
          “Drawing multiple notes of the same length”), hold down [Alt]+[Ctrl](Win) or [Cmd]+[Option](Mac).
      2. Click at the desired position on the Note Edit Lane.
          A note will be inserted at the closest Snap value position. By default, the note will be given the Velocity value ‘100’.
          (This can be edited afterwards according to the descriptions in “Editing note velocity”). If an open or closed clip is
          already present on the Note Lane, at the position where you draw the note, the note will be placed in that clip. If no
          clip is available, refer to “About drawing notes outside an open clip” and “About drawing notes outside a closed
          clip” below.
      • If you just click, and Snap is activated, the note will get the length of the set Snap value.
          If Snap is off, the note will get the length of the shortest possible Snap value, i.e. 1/128th note.
      • If you click and keep the mouse button depressed, you can drag to the right to set the length of the note.
          If Snap is on, the length will be a multiple of the Snap value.
      !   If you are drawing drum notes for a Redrum device, refer to the info about drum note lengths in “About resiz-
          ing drum notes”.

      Drawing multiple notes of the same length
      1. Click the Pencil tool (twice) and select “Draw multiple notes”.

      q   With the Selection (Arrow) tool selected, you can toggle temporarily between the Selection tool and the Pencil
          tool by holding down [Alt](Win) or [Cmd](Mac). To switch between the “Multiple notes” and “single notes”
          tools, hold down [Alt]+[Ctrl](Win) or [Cmd]+[Option](Mac).

      2. Select the desired note length from the Snap value selector:

      3. Click at the desired position on the Note Edit Lane, click and draw sideways to the right:

        Multiple notes of the currently selected Snap value length are now added after one another (at the same pitch) in
        the note clip. By default, the notes will be given the Velocity value ‘100’. (This can be edited afterwards according
        to the descriptions in “Editing note velocity”).

      About drawing notes outside an open clip
      If you draw notes outside the boundaries of an open clip, the result depends on the setting "Keep Events in Clip
      While Editing" on the Options menu:
      • If the “Keep Events in Clip While Editing” option is active, the notes will belong to the open clip after they have
        been drawn, but become masked since they are drawn outside the clip boundaries.
          The clip position and length will remain unchanged.
      • If "Keep Events in Clip While Editing" is deactivated and you draw notes outside the clip, the notes will be
        placed in an existing clip - or in another new clip on the lane, depending on where you draw.
          The picture below shows three scenarios when drawing a note outside an open clip with the “Keep Events in Clip
          While Editing” option off:

          Here, we’re going to draw a note in beat 3 of bar 5...          The open clip expands by the set Arrange Mode Snap
                                                                          value (1 bar) to fit in the new note.

          Here, we’re going to draw a note in beat 3 of bar 8...         The note is placed in the existing clip at beat 3 of bar 8.

          Here, we’re going to draw a note in beat 1 of bar 12...        A new clip is created at bar 12 with a length of the set Snap
                                                                         value (1 bar) and the new note is placed in beat 1.

      About drawing notes outside a closed clip
      If you draw notes outside the boundaries of a closed clip in Edit Mode, i.e. where there are no clips available on the
      lane, a new clip will be automatically created and opened. The clip length is determined by the Song/Block View
      Snap value, if Snap is activated.
      q   This works best with "Keep Events in Clip while Editing" turned OFF because then you can continue drawing
          notes - the clip will be resized to fit the new notes.

      Deleting notes
      You can delete notes by doing any of the following:
      D   To delete individual notes, double click the note with the Selection (Arrow) tool.
      D   Select one or several notes with the Selection (Arrow) tool and press [Backspace] or [Delete], or select “De-
          lete” from the Edit or context menu.
      D   Select the Eraser tool and click on the notes you want to delete.


=== END OF PART ===
