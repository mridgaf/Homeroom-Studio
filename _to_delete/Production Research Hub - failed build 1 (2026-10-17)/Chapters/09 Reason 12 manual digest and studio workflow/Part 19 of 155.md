# Chapter 09: Reason 12 manual digest and studio workflow
## Part 19 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 10 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 20 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 10 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Creating/adding parameter automation lanes
      Parameter automation lanes can be created for all track types.
      • During recording of a track, changing any parameter values on the device/channels strip will automatically cre-
        ate a new parameter automation lane for each unique parameter. See “Recording parameter automation” for
        more details.
      Do as follows to manually create a parameter automation lane on a selected track:
      D   Hold down [Alt](Win) or [Option](Mac) and click on a device parameter in the rack, or on a channel strip param-
          eter in the Main Mixer. Alternatively, select “Edit Automation” from the parameter’s context menu.
          A new parameter automation lane will be automatically created in the track for the corresponding device or chan-
          nel strip. The automated parameter on the device in the rack or channel strip in the Main Mixer will get a green
          border, indicating that it has been automated.
      !   Note that if a track hasn’t already been created for the device/channel strip, it will be automatically created
          during this operation.
      Other ways of creating/adding a parameter automation lane are as follows:
      1. Click on the “Track Parameter Automation” drop-down list at the top of the Track List.

      2. Select the parameter you want to automate from the list.
          A new parameter automation lane is automatically created on the selected track.
          If you click the Track Parameter Automation drop-down list again, any selected parameters will have a symbol to
          the left of the parameter name, indicating that an automation lane already exists for the parameter.
          The automated parameters on the device in the rack or channel strip in the Main Mixer will get green borders, in-
          dicating that they have been automated.

      Creating a pattern lane
      For pattern based devices such as the Redrum Drum Module and Matrix Analog Pattern Sequencer, a single pattern
      lane can be created on a selected track. Do either of the following:
      D   Click the “Create Pattern Lane” button at the top right of the Track List.

      D   Select “Create Pattern Lane” from the Edit menu or from the context menu.
      D   Hold down [Alt](Win) or [Option](Mac) and click on the “Pattern” button section of the device in the rack.
      D   Right-click (Win) or [Ctrl]-click (Mac) on the “Pattern” button section of the device in the rack and select “Edit
          Automation” from the context menu.
      When you create a pattern lane, the bank buttons on the device in the rack get a green border to indicate that they
      have been automated.
      D   Clicking the Pattern and/or Bank buttons on the device during recording will automatically create a pattern
          lane. See “Recording pattern automation” for more details.

      Deleting lanes
      Deleting note lanes
      A note lane can be deleted as follows:
      D   Click the “Delete Note Lane” (X) button on the lane tab in the Track List.
          This will delete the lane (and all clips on it). If there are clips on the lane, a dialog appears prompting you to confirm
          deletion.

      D   To delete the lane without the dialog, hold down [Ctrl](Win) or [Cmd](Mac) and click the Delete Note Lane but-
          ton.

      Deleting parameter automation lanes
      There are a number of different ways of deleting a parameter automation lane:
      D   Click the “Delete Automation Lane” (X) button on the lane tab in the Track List.
          This will delete the lane (and all clips on it). If there are clips on the lane, a dialog appears prompting you to confirm
          deletion.

      D   To delete the lane without the dialog, hold down [Ctrl](Win) or [Cmd](Mac) and click the Delete Automation
          Lane button.
      Another way is this:
      D   Right-click (Win) or [Ctrl]-click (Mac) on the automated device parameter in the rack and select “Clear Automa-
          tion” from the context menu.
          The green border around the device parameter disappears and the corresponding parameter automation lane is
          deleted from the track.
      Alternatively, do the following:
      1. Select a track by clicking on it.
      2. Click on the “Track Parameter Automation” drop-down list at the top of the Track List.

      3. De-select the parameter you want to delete from the list.
          All selected parameters will have a symbol to the left of the parameter name in the list indicating that it has been
          selected. Selecting a parameter with a symbol in the list will automatically delete the corresponding lane, with its
          clips, from the track. If there are clips on the lane, a dialog appears prompting you to confirm deletion.
          The green borders that surrounded the automated parameters on the device/channels strip will also be removed.

      Deleting pattern lanes
      There are two ways of deleting a pattern lane:
      D   Click the “Delete Pattern Lane” (X) button on the lane tab in the Track List.
          This will delete the lane (and all clips on it). If there are clips on the lane, a dialog appears prompting you to confirm
          deletion.

      D   To delete the lane without the dialog, hold down [Ctrl](Win) or [Cmd](Mac) and click the Delete Pattern Lane
          button.
      Alternatively:
      D   Right-click (Win) or [Ctrl]-click (Mac) on the automated pattern section on the device in the rack and select
          “Clear Automation” from the context menu.
          The green border around the device pattern section disappears and the corresponding pattern lane is deleted from
          the track.

      Moving note lanes
      A note lane has a “handle” and can be moved vertically together with all clips on the lane. Move a note lane to another
      position on the same track like this:
      1. Click on the lane handle (the leftmost area of the lane).

      2. Drag the note lane up or down and release at the desired destination.
          Just as when moving tracks, a red insertion line is shown indicating where the note lane will be placed after you re-
          lease the mouse button.
      • It is also possible to move note lanes, with their clips, between tracks.
      !   Parameter automation lanes and pattern lanes cannot be moved since they are tightly connected with their as-
          sociated devices However, you can move or copy clips from one lane to another.

      Copying (duplicating) note lanes
      You can copy (duplicate) one note lane at a time, together with its clips, by doing the following:
      1. While pressing [Ctrl](Win) or [Option](Mac), click and drag a copy of the note lane to the desired destination.
          The cursor gets a + sign next to it to indicate duplication. The destination of the duplicated note lane could be the
          same track or another track.
      2. Release the mouse button.
      !   Parameter automation lanes and pattern lanes cannot be duplicated.

      Muting lanes
      Muting a note lane
      D   To mute a note lane, click its “M” (Mute) button.

          The note lane’s “M” (Mute) button.

      Muting a parameter automation lane
      D   To mute a parameter automation lane, click its “M” (Mute) button.

          The parameter automation lane’s “M” (Mute) button.

      Clip basics
      Only the basic properties and functions pertaining to clips are described here. See “Arranging in the Sequencer” for
      in-depth details about what you can do with clips.

      Clip types
      Here are the different clip types:

                                                                        Block automation clip

                                                                        Note clip with note and per-
                                                                        formance controller events
                                                                        Parameter automation clip
                                                                        with automation events
                                                                        Audio clip with audio
                                                                        recording (stereo or mono)
                                                                        Pattern automation clips

      • Block automation clips (only if Blocks are on) that contain information of which Block should play back.
      • Note clips contain note events with velocity values. Note clips can also contain performance controller events.
      • Parameter automation clips contain events for an automated device/channel strip parameter.
          A parameter automation clip can easily be distinguished by the shape of its frame: the top right corner is “cut off”.
      • Audio clips contain mono or stereo audio recordings.
          If the audio clip is a Comp clip, or a Single Take clip which contains several takes, there is a small symbol in the
          lower right corner of the clip.
      • Pattern automation clips contain device bank+pattern number.

      Toolbar details

      The Sequencer Toolbar can be found to the top left in the Sequencer Area. From the Sequencer Toolbar you can se-
      lect various sequencer editing tools.

      Toolbar tools
      Selection Tool

      The Selection (arrow) Tool is the main tool for selecting and moving tracks, note lanes, clips and events and record-
      ings in clips. It’s also used for resizing clips and events in clips. It is selected by default when a song is opened.
      D   You can also select the Selection Tool by pressing [Q] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Selection Tool to the Pencil Tool - or to the
          Speaker Tool when editing an open audio clip inline - or to the Cut (Razor) Tool when editing an open audio
          clip in the Comp Editor.

      Pencil Tool

      The Pencil Tool is used for manually drawing clips and events in clips. It can also be used to edit the velocity values
      of notes in open note clips.
      D   You can also select the Pencil Tool by pressing [W] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Pencil Tool to the Selection Tool.
      !   When a note clip is open in Edit Mode, there two different Pencil Tools are available - one for drawing single
          notes with varying lengths and one for drawing repetitive notes of the same length, see “Drawing notes”.

      Eraser Tool

      The Eraser Tool is used for deleting clips and events. In audio Pitch Edit mode you can also join notes with the Eraser.
      D   You can also select the Eraser Tool by pressing [E] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Eraser Tool to the Pencil Tool.

      Razor Tool

      The Razor Tool is used for splitting clips and notes - and for creating cuts when comping audio clips in Edit Mode.
      D   You can also select the Razor Tool by pressing [R] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Razor Tool to the Pencil Tool - or to the Selec-
          tion Tool when editing an open audio clip on the Edit Pane.

      Mute Tool

      The Mute Tool is used for muting clips in the arrangement - or lanes in Block automation clips (see “Muting lanes in
      Block Automation Clips”).
      D   You can also select the Mute Tool by pressing [T] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Mute Tool to the Razor Tool.

      Magnifying Glass Tool

      The Magnifying Glass Tool lets you zoom in and out both horizontally and vertically on the Arrangement Pane. The
      Magnifying Glass Tool offers a couple of possibilities:
      D   To zoom in with the Magnifying Glass Tool, click in the Arrangement Pane where you want the origin of mag-
          nification.

          Place the Magnifying Glass Tool in   After three clicks, the Arrangement Pane
          the Arrangement Pane and click.      looks like this. The magnification is equal in
                                               vertical and horizontal directions.

      D   To zoom out with the Magnifying Glass Tool, hold down [Ctrl](Win) or [Option](Mac) and click.
          You’ll notice that the “+” sign in the Magnifying Glass Tool changes to a “-” sign.

      D   You can also click and drag with the Magnifying Glass Tool to create a selection rectangle.
          The view will then be zoomed in so that the selected area fills the entire Arrangement Pane.

          Place the Magnifying Glass Tool   After releasing the mouse button, the zoomed selection fills up the
          on the Arrangement Pane, click    Arrangement Pane. The magnification can be different in vertical and
          and drag to create a selection.   horizontal directions depending on the shape of the selection rectangle.

      D   You can also select the Magnifying Glass Tool by pressing [Y] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Magnifying Glass Tool to the Hand Tool.
      q   It’s also possible to zoom in the Arrangement Pane by using the Sequencer Area Navigators and Zoom To Se-
          lection function as described in “Zooming in the Sequencer” and “Zooming to selection”.

      Hand Tool

      The Hand Tool is used for scrolling in the Edit/Arrangement Pane.
      D   Select the Hand Tool and click anywhere in the Edit/Arrangement Pane, keep the mouse button depressed
          and drag to desired view.

      D   You can also select the Hand tool by pressing [U] on the computer keyboard.
      D   Press [Alt](Win) or [Cmd](Mac) to momentarily switch from the Hand Tool to the + Magnifying Glass Tool.
      D   Press [Ctrl]+[Alt](Win) or [Cmd]+[Option](Mac) to momentarily switch from the Hand Tool to the - Magnifying
          Glass Tool.
      q   It’s also possible to scroll in the Edit/Arrangement Pane by using the Sequencer Area Navigators as described
          in “Scrolling with the Navigators and scrollbars”.

      Speaker Tool

      The Speaker Tool is used for auditioning slices or notes in Single Take audio clips, and for auditioning individual re-
      cordings on Comp Rows in Comp Clips. See “Slice Edit mode tools”, “Auditioning notes” and “Comp Editor audio ed-
      iting tools” for details.

      Alternate tools
      For every tool mode described earlier, there is a so called alternate tool that can be momentarily selected by holding
      down [Alt](Win) or [Cmd](Mac) on the computer keyboard. Below is a summary of the alternate tools:

      | Selected tool                   | Alternate tool
          Selection tool                Pencil tool (Speaker tool in inline editing of Audio Track or Cut (Razor) tool
                                        when editing audio clip in Comp Editor)
          Pencil tool                   Selection tool
          Eraser tool                   Pencil tool
          Razor tool                    Pencil tool (Selection tool when editing open audio clip on the Edit Pane)
          Mute tool                     Razor tool
          Magnifying Glass tool         Hand tool
          Hand tool                     + Magnifying Glass tool
          Hand tool                     - Magnifying Glass tool by pressing [Alt]-[Ctrl](Win) or [Option]-[Cmd](Mac)

      Edit Mode buttons

      D     Click the Edit button (or Slice Edit/Pitch Edit/Comp Edit button for selected audio clips) to switch to Edit
            Mode.

      Snap

      The Snap function in the sequencer toolbar is used for “restricting” editing of clips and events to a user-selectable
      note value grid.
      D     Activate the Snap function by pressing [S], or by clicking the Snap button:

      !     When moving clips or events, the Snap function can work either absolute (to the closest absolute position in
            the grid) - or relative to the clip(s)/event(s) original position(s), in steps of the set Snap value:

                                                                                                               Absolute Snap

                                                                                                                         Relative Snap

            Absolute Snap set to “Bar” (top) and Relative Snap set to “Bar” (bottom).

      1. Select the grid you wish to snap to by selecting the note grid value from the drop-down list:

      2. Click the drop-down list again and select if you want the Snap to be “Relative” or “Absolute” from the bottom
         of the drop-down menu.
      !   Note that you can select different Snap values for selected clips in the Arrange/Block View and for open clips
          in Edit Mode (see “About separate Snap values for selected clips and for open clips”).
      The Snap function affects the following operations:
      • Moving the Song Position Pointer, Loop Locators and Song End Marker.
          When you adjust the Locators with Snap activated, they will always snap to the selected Snap value on an absolute
          grid, regardless of the setting on the Snap drop-down menu.
      • Moving clips and events, recordings and Comp Row cuts.
          When you move objects with Snap activated, they will move relative or absolute to the Snap value, depending on
          what you selected on the Snap drop-down menu.
      • Drawing clips.
          When you create clips with the Pencil tool, their start and end positions will snap to the selected note value posi-
          tions on an absolute grid.
      • Drawing events in open clips.
          The Snap value determines the absolute grid points on which you can draw a note or an automation point. The
          Snap value also determines the shortest possible note length that you can draw.
      • Splitting clips with the Razor tool.
          The Snap value determines the absolute grid to which a clip can be split.
      • Nudging clips, events and recording.
          When you nudge clips, events or recordings with Snap activated, they will move relative or absolute to the Snap
          value, depending on what you selected on the Snap drop-down menu.
      • Creating Comp Row cuts
          The Snap value determines the absolute grid to which you could add cuts in open Comp audio clips.
      • Moving Comp Row cuts
          The Snap value determines the relative or absolute grid to which you could move cuts in open Comp audio clips.
      • Adding and moving Slice Markers
          The Snap value determines the absolute grid to which you could add and move Slice Markers in open Single Take
          audio clips.

      About the “Grid” Snap value
      The “Grid” value at the top in the list is dynamic and automatically changes the snap value, from “Bar” to “1/128”,
      depending on the current horizontal zoom level on the Arrange/Edit pane.
      The picture below shows the same clips in the Arrange pane at two different horizontal zoom levels:

      About separate Snap values for selected clips and for open clips
      There are two different Snap settings, one for when a clip is open for editing in Edit Mode, and one for when no clip
      is open (e.g. in Song/Block View). Typically, you would set a fine Snap value (e.g. 1/16) for open clips in Edit Mode
      and have the other Snap value set to “Bar” for convenient clip arranging in the Song/Block View. You can also
      choose to turn Snap off in either of these modes, independently of the other setting.
      • The Snap value for editing is used whenever a note clip or automation clip is open (including when an automa-
        tion clip is opened in Arrange Mode).
         However, there’s one exception: If a note clip is open in Edit Mode and you click in the Clip Overview (see “Edit
         Mode elements”), the clip will remain open but the Snap value for arranging will be selected. This allows you to e.g.
         move or resize the clip in the Clip Overview just like in the Song/Blocks View, without closing it first.

      Sequencer Toolbar keyboard shortcuts
      Below is a complete list of the computer keyboard shortcuts for selecting tools on the sequencer Toolbar:

      | Function                        | Key command
      Selection tool select              [Q]
      Pencil tool select                 [W]
      Eraser tool select                 [E]
      Razor tool select                  [R]
      Mute tool select                   [T]
      Magnifying Glass tool select       [Y]
      Hand tool select                   [U]
      Snap On/Off                        [S]

      Ruler details
      The Ruler is the song’s time line. In the Ruler, the Song Position Pointer indicates the current position in the song, i.e.
      in which bar the song is, or will start, playing. The Ruler also shows the Left (L) and Right (R) Loop Locators as well
      as the Song End Marker (E).

            Left (Loop) Locator                                     Right (Loop) Locator
                             Song Position Pointer                                 Song End Marker

      You can change the positions of the Song Position Pointer, Locators and Marker in the Ruler by clicking and drag-
      ging them to desired positions in the Ruler. Note that you have to click and drag the “flags” in the Ruler - not the lines.
      The Song Position Pointer and Loop Locators can also be moved by typing in new positions in the respective Position
      displays in the Sequencer Transport Panel (see “Song Position” and “Left and Right Locator Positions”). Another way
      of moving the Song Position Pointer is by using the Rewind and Fast Forward controls on the sequencer Transport
      Panel (see “Rewind and Fast Forward”).

      Transport Panel details
      At the bottom of the Reason window is the sequencer’s Transport Panel. From here you control the sequencer trans-
      port functions. You can also set tempo, time signature and various other parameters.

      On-screen Keyboard              Click On/Off      Fast Forward Record   Go to Left Locator
       Quantize during rec.                        Tempo           Play New
                  Sync Mode                            Rewind   Stop    Overdub   Left Locator Pos
                            Song Position

         Quantize                Time Position                        Signature                 Loop   Right Locator Pos
       Quantize value               Pre-count On/Off              New Alternative take          On/Off
      ReGroove Mixer                      Click Level          Tap Tempo                               Go to Right Locator

      Keys
      D   Click this button to bring up the On-screen Piano Keyboard floating window.
          See the “On-screen Piano Keys” chapter for more information.

      Groove
      D   Click the Groove button to bring up the ReGroove Mixer.
          Refer to “The ReGroove Mixer” chapter for more information.

      Q Record
      D   Click the Q Record (Quantize during recording) button to quantize notes as they are being recorded.
          When the Q Record button is on, all recorded MIDI notes will be quantized to the currently selected quantization
          grid. Refer to “Quantize” for more information on quantization.

      Quantize value
      D   Select the desired quantization value from the drop down list.
          Refer to “Quantize” for more information on quantization.

      Quantize
      D   Click the Quantize button to quantize the notes in the selected clips to the selected Quantize value - after they
          have been recorded.
          Refer to “Quantize” for more information on quantization.


=== END OF PART ===
