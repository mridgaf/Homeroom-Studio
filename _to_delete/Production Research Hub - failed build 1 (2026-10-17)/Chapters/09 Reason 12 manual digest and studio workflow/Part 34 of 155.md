# Chapter 09: Reason 12 manual digest and studio workflow
## Part 34 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 25 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 35 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 25 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Deleting automation events
      D   Deleting automation events is done in the same way as when deleting note events. I.e. click on events to select
          them or draw selection rectangles and then press [Backspace] or [Delete] - or use the Eraser tool (see “Delet-
          ing notes”).
      D   To clear all automation events in a clip, hold down [Ctrl](Win) or [Cmd](Mac) and press [A] to select all events,
          then press [Backspace] or [Delete]. Alternatively, delete the clip (or remove the whole lane to clear all automa-
          tion for that parameter).
      D   If you want to delete single parameter automation events, you can double click on an event with the Selection
          (Arrow) tool in the clip.

      Reversing automation events
      It’s possible to reverse the order of selected automation events in an open note or automation clip, see “Reverse”.

      Editing performance controller automation
      D   To edit, draw or delete performance controller events, open the note clip in Edit Mode.

                                                                                              Performance Controller
                                                                                              Edit Lanes

          Performance controllers (Mod Wheel and Pitch Bend in the example above) are shown on separate Performance
          Controller Edit Lanes at the bottom of the open note clip. The performance controller curves are also indicated in
          the Clip Overview (top), and in the clip in the Song/Block View.
      D   You can edit performance controller events using the Selection (Arrow), Pencil and Eraser tools, just like when
          editing parameter automation events in Edit Mode (see “Editing parameter automation in Edit Mode”).

      Creating new performance controller automation lanes
      If you want to manually draw performance controller automation events for a controller which hasn’t already been
      automated, you have to create a new Performance Controller Edit Lane for that parameter. Proceed as follows:
      1. Open the note clip in Edit Mode.
      2. Select the new performance controller to be automated by clicking on the Performance Controller Automation
         Selector and selecting it from the pop-up list that appears:

                                                                                                 Performance Controller
                                                                                                 Automation Selector

          In this example, we select Aftertouch.
      3. A new Performance Controller Edit lane is created for the Aftertouch controller:

                                                                                                 Aftertouch Edit lane

      4. Now, you can draw Aftertouch performance controller events in the clip using the Pencil Tool as described in
         “Drawing parameter automation events”.
          Afterwards, you can edit the performance controller events the same way as with regular parameter automation
          events (see “Editing parameter automation in Edit Mode”).
      D   It’s also possible to add any of the available device panel parameters as a performance controller.
          Just select the desired parameter from any of the sub-menus at the bottom of the Performance Controller Auto-
          mation Selector pop-up menu.

      Deleting performance controller automation lanes
      D   To delete a performance controller automation lane, deselect it from the Performance Controller Automation
          Selector list.
          This brings up a confirmation alert if there is data on the lane (in any clip). You can delete without the alert by
          pressing [Ctrl](Win) or [Cmd](Mac) when you deselect the parameter from the list.

      About Automation Cleanup
      Automation Cleanup is a function for controlling the amount of parameter automation events that should be created
      during recording and/or manual drawing. The Automation Cleanup function applies to parameter automation events
      as well as to performance controller automation events. The Automation Cleanup level can be set in the Preferences
      menu and will apply to all new recorded automation events. You can also use the function on previously recorded pa-
      rameter automation events. This is done on the Tools tab in the Tool Window.

      Automation Cleanup in the “Preferences” menu
      D   If you feel you get too many automation events when recording or drawing events, you can adjust the “Auto-
          mation Cleanup” setting in the Preferences dialog - General page to “Heavy” or “Maximum”:

          This automatically removes superfluous automation events next time you record or draw events and simplifies the
          curves. Note that Snap (see “Snap”) also governs the number of events when drawing events.

          Drawing automation with “Normal” Cleanup (left), and with “Maximum” Cleanup (right).

      The “Automation Cleanup” function in the Tool Window
      You can also apply Automation Cleanup to already recorded/drawn events. This is done on the Sequencer Tools tab
      in the Tool Window:

      The Automation Cleanup pane in the Tool Window.
      The “Automation Cleanup” function can be applied to:
      • Individual (selected) parameter automation events in an open clip.
          This has to be done in Edit Mode for performance controllers. For parameter automation, it can be done in both
          Edit Mode and the Song/Block View.
      • All parameter automation events in one or several selected clips.
          This is done in the Song/Block View. If the clips are on the same track, it can also be done in Edit Mode.
      • All parameter automation events in all clips on one or several selected tracks.
          This has to be done in the Song/Block View.

      Editing pattern automation
      Pattern automation clips are viewed and edited in the Pattern Select lane, which is available on Dr. Octo Rex, Redrum
      and Matrix tracks:

                                                        Pattern (group and number)

                                                        Pattern Selector

                                                        Clip Resize handles

      Pattern changes are shown as clips with a Pattern Selector at the top (when the clip is selected). A single pattern au-
      tomation clip can only contain data for a single pattern. In practice this means that each pattern automation clip only
      contains one pattern automation “event”. All pattern changes in the song will therefore require unique clips.
      • Pattern (group and number)
          The Pattern (group and number) indicate which pattern in the source device is playing in this clip. For Dr. Octo Rex
          devices, the Bank is of no importance.
      • Pattern Selector

          Click the Pattern Selector triangle, or double-click anywhere in the clip, to bring up a pop-up list featuring all avail-
          able patterns (groups and numbers) of the source device. Select another pattern from the list if you wish to change
          pattern in the selected clip. If several pattern clips are selected, selecting a pattern for one of them will set them all
          to play that pattern.
      • Clip Resize handles
          Click and drag any of the Clip Resize handles horizontally to resize the clip and thus change the pattern playback
          start position and/or duration.
      !   If there is pattern automation for a device, it will only play patterns where there are pattern clips.

      Drawing pattern automation
      You can draw pattern automation clips on a Pattern Select lane as follows:
      1. Activate Snap and set the Snap value to the note position where you want to insert the pattern change clip
         (see “Snap”).
          It is probably a good idea to set the Snap value to “Bar”, at least if you are working with patterns of a length corre-
          sponding to the time signature (e.g. 16 or 32 step patterns and 4/4 time signature). However, if you are working
          with patterns of another length, it can make sense to use other Snap values when drawing pattern automation
          clips.
      2. Select the Pencil Tool.
          A Pattern/Loop drop-down list appears in the Inspector. Use this to select the pattern you wish the clip to play. For
          Dr. Octo Rex devices, the Bank is of no importance.

      3. Draw a clip for length you want the selected pattern to play.

      4. Continue using the same method to draw clips for all the patterns you wish to use.
      q   Don’t draw pattern change clips with Snap turned off, unless you want chaotic pattern changes!
      D   If you want to add single pattern change clips, you can also double click with the Selection (Arrow) tool on the
          Pattern Select lane.
          This will create an empty pattern change clip with the length of the current Snap value setting (e.g. 1 bar). To cre-
          ate longer clips, double click, keep the mouse button pressed and drag to the right.

      Moving, resizing and duplicating pattern automation clips
      • You can move, resize and duplicate pattern automation clips in the same way as with note or automation clips.
          However, it is recommended that Snap is activated (and in most cases set to “Bar”) when you do this (see “Snap”).
      !   If you resize a pattern automation clip by clicking and dragging the left resize handle, and thus change the
          start position, the clip will be masked (just like a note clip). This means the pattern won’t necessarily begin on
          beat 1. A selected pattern automation clip that has a masked start position will indicate this in the Pattern Off-
          set display in the Inspector.

          A pattern automation clip drawn between bar 1 and 5.
          Now, if we resize the clip by dragging the left resize handle two beats to the right, the Pattern Offset will change
          but the pattern will play back as expected:

          The same pattern automation clip “resized” to begin at beat 2.
      • You can also move or duplicate pattern automation clips using the Cut, Copy and Paste commands on the Edit
        menu or context menu.
          Again, the same rules apply as for note and parameter automation clips.

      Deleting pattern automation clips
      D   Deleting pattern automation clips is done in the same way as deleting note clips. I.e. you can select or draw se-
          lection rectangles and then press [Backspace] or use the Eraser tool etc.
      D   To clear all automation in a clip, simply delete the clip (or remove the whole lane to clear all pattern change au-
          tomation on the track).

      The “Convert Pattern Automation to Notes” function
      If you have recorded or drawn pattern automation on a Redrum or Matrix track, you can automatically convert the
      whole pattern automation lane into note events on an additional note lane. Proceed as follows:
      1. Select the track with the pattern automation.
      2. Select “Convert Pattern Automation to Notes” from the Edit menu or the track’s context menu.
        For each pattern automation clip, the corresponding device pattern is converted to note clips on an additional note
        lane on the track. The generated note lane will play back just the same as when you played the pattern device with
        the pattern changes.
      • The pattern automation lane is automatically disabled (turned off) after this operation.
        You can later go back to pattern automation if you wish, by turning on the pattern lane again.

      Redrum specifics:
      • The “Enable Pattern Section” switch on the Redrum device is automatically turned off when you use the “Con-
        vert Pattern Track to Notes” function.

      Matrix specifics:
      • Make sure that the correct track is selected (normally the track for the device that the Matrix is connected to)!
        Creating notes for the Matrix itself is pointless, as the Matrix cannot produce any sound.
      • You may want to disconnect or even remove the Matrix device after performing this function.
        This is because you probably don’t want both the Matrix and the sequencer notes to play the device at the same
        time.

      Editing tempo automation
      Tempo automation is edited in the same way as regular parameter automation. See “Editing parameter automation”.

      Drawing tempo automation events
      Drawing tempo automation events is done in the same way as drawing regular parameter automation events. See
      “Drawing parameter automation events”.
      • Even though Reason supports a very wide tempo range (1.0 BPM to 999.999 BPM), the initial displayed editing
        range is 60-250 BPM in the left column in Edit Mode. This is only to make it easier to work with small tempo
        changes.

        If you want higher tempi than 250 BPM, or lower than 60 BPM, you can easily expand the range, either by select-
        ing and moving a tempo automation event above, or below, the clip border, by double-clicking the max or min val-
        ues (“250” or “60” in the left column in the picture above) and typing in a new value, or by selecting an event and
        changing its value in the Value display in the Inspector.

      About tempo changes and tempo automation of audio tracks
      The built-in Stretch function allows you to change the tempo of the song without affecting the pitch of the recordings
      on the audio tracks. This is great if you want to adjust the tempo after you have recorded your audio tracks. In Rea-
      son, the Stretch is enabled by default for all audio clips.
      !   The Stretch function also affects the sonic result when transposing audio clips using the Transpose function
          (see “Transposing Audio Clips”).
      There are three selectable Stretch and Transpose Type algorithms which are suitable for playing back different types
      of audio material:
      • The “Allround” Stretch and Transpose Type is suited for most types of polyphonic audio material.
      • The “Melody” Stretch and Transpose Type is best suited for sources sounding one note at a time e.g. solo in-
        struments.
      • The “Vocal” Stretch and Transpose Type is best suited for stretched and/or transposed vocal material.
          In the “Vocal” Stretch and Transpose Type the formants of the original vocal are preserved, which prevents the vo-
          cal from sounding artificial when transposed and/or stretched.
      D   Select “Stretch and Transpose Type” from the Audio Track context menu or from the Edit menu.

      Stretch preview vs. high quality stretch
      Stretch and transposition of audio are always made in two parallel steps: a real-time “preview” so that you can in-
      stantly hear the result of your tempo changes or transpositions, and a high quality stretch “in the background” to fur-
      ther improve the sonic results. As soon as high quality stretch is in progress, the “Calc” indicator on the Transport
      Panel shows a progress indicator:

      The CALC indicator appears when Reason performs high quality stretching of audio.
      Since the high quality stretch is performed in the background, you can still continue to work with your song without
      any interruption. When the high quality stretch is finished, the “Calc” indicator goes out and the high quality audio au-
      tomatically replaces the “preview” audio.

      About disabling Stretch for audio clips
      In some situations, you might want to exclude audio clips from tempo automation. For example, if you have recorded
      dialogue or sound effects that shouldn't adapt to tempo changes. In such situations, you can select the audio clip(s)
      you want to exclude from the tempo changes and select “Disable Stretch” from the Edit menu or clip context menu.
      !   Note that disabling stretch does not affect the Transpose function for audio clips!

      Automating time signature
      Time signature automation events can only be manually drawn with the Pencil tool - not recorded like tempo automa-
      tion, parameter automation or performance controller automation. A single time signature automation clip can only
      contain a single time signature value. In practice this means that each time signature automation clip can only contain
      one time signature automation “event”. All time signature changes in the song will require a unique clip.
      1. Set the desired time signature in the Signature display on the Transport Panel.
          This will be the Static Value, i.e. the time signature of the song wherever there is no clip present on the time sig-
          nature automation lane.
      2. Hold down [Alt](Win) or [Option](Mac) and click in the Signature display on the Transport Panel.
          This will select the Transport track and create a time signature automation lane in one go. The Signature display
          will also be displayed with a green border, indicating that the time signature has been automated.
      q   It is generally a good idea to activate Snap (see “Snap”) and have the Snap value set to “Bar” when drawing
          clips.
      3. Select the Pencil Tool.
          When the Pencil tool is selected, a Time Signature drop-down list appears in the Inspector. Select the desired time
          signature from the drop-down list.

      D   If you select “Other” the Edit Time Signature dialog appears where you can specify another time signature.

          The available signatures are: 1/2-16/2, 1/4-16/4, 1/8-16/8 and 1/16-16/16. The Time Signature display in the
          dialog can be edited according to the descriptions in “Transport Panel segment displays”.
      4. Draw a clip over the area on the Time Signature lane in the Transport track where you want the time signature
         to change.
          The time signature will change for the duration of the clip.

      5. Continue using the same general method wherever you want the time signature to change in your song.

      D   If you want to add single time signature clips, you can also double click with the Selection (Arrow) tool on the
          Time Signature lane.
          The clip gets the length of the currently selected Snap value.
      D   You can change the time signature for the automation clip at any time by simply double-clicking the clip with
          the Selection (Arrow) Tool and changing the value on the pop-up that appears. Alternatively, select the clip and
          then click the small triangle in the clip to bring up the time signature pop-up.
          There is no need to switch to Edit Mode unless you wish to change the time signature’s Static Value.

      Moving, resizing and duplicating time signature automation
      clips
      D   You can move, resize and duplicate time signature automation clips in the same way as with note or automa-
          tion clips.
          However, it is recommended that Snap is activated (and in most cases set to “Bar”) when you do this.
      D   You can also move or duplicate clips using the Cut, Copy and Paste commands on the Edit menu or context
          menu.
          Again, the same rules apply as for cutting, copying and pasting note and parameter automation clips.

      Deleting time signature automation clips
      D   Deleting time signature automation clips is done in the same way as deleting note clips. I.e. you can select or
          draw selection rectangles and then press [Backspace] or [Delete], or use the Eraser Tool.
      D   To clear the time signature automation in a clip, simply delete the clip (or remove the whole Time Signature
          Lane to clear all time signature automation on the track).

      Note and automation editing in the Inspector
      In the Inspector you can edit note and automation events numerically using the displays.

      Editing notes and events in the Inspector
      If you select a note, four displays appear in the Inspector, showing the event (start) Position, Length, Note
      number and Velocity value:

      If you select a parameter automation event, two displays appear, showing the event’s Position and Value:

      If you select a pattern automation clip, three displays appear, showing the clip’s Position, Length and Pattern Offset:

      D   Edit the values by clicking on a segment in a display and then drag up/down, use the up/down spin controls, or
          type in new values. Snap is not taken into account.
          See “Inspector segment displays” for details on how to edit in the Inspector displays.
      !   Note that when moving the position of events, these may end up outside the clip and be masked (not played).
          There will be no warning or indication if this should happen. However, since the clip is open in Edit Mode, you
          will be able to see if events are masked.
      • If the Tick segment in the Position and/or Length displays shows an asterisk (*), it means that the value is a
        fraction of a Tick - a subtick. See “About subticks in the Position and Length displays” for more info.

      Editing values for multiple notes or events in the Inspector
      When you edit values for several selected events, the changes will always be relative. For example, if you change the
      position, length, pitch or velocity when several notes are selected, they will all be changed by the same amount, re-
      taining their relative values.
      • If several events are selected, the displays will show the values for the event with the earliest start position in
        the song.
          If several selected events have the same start position, the displays will show the values for the event with the low-
          est Note value (for note events) or lowest Value (for automation events).
      • If several events are selected and any of their values differ, Match Value buttons appear next to the corre-
        sponding display.
          See “Matching notes or events using the “Match Values” function”.

      Matching notes or events using the “Match Values” function

      The Match Values buttons appear as ‘=’ signs.

      The “Match Values” function in the Inspector can be used for matching the positions, lengths and velocities of several
      selected note events to the position/length/velocity of the selected event with the earliest start position in the song.
      It’s always the values of the earliest event that are shown in the displays. Similarly, automation events can be matched
      to the position and/or value of the earliest selected automation event in the song.
      If several selected events have the same start position, the matching will be to the values for the event with the low-
      est Note value (for note events) or lowest Value (for automation events).

      Matching notes
      Here’s an example on how to match note values:
      1. In Edit Mode, select several notes.

        Four selected notes in Edit Mode.
      2. Click the respective Match Values button to achieve the following results:

                                        or                                or

           Position values                        Length values                        Velocity values
           matched                                matched                              matched

      Matching parameter automation events
      Matching parameter automation event values is useful if you want an automated device parameter to be modulated
      to the same value throughout the clip.
      • Let’s say you want to modulate a parameter to a maximum value of 80 several times throughout the clip. Then,
        just select all “max value” events, click the “Match Values” button and then adjust the Value to 80 for the se-
        lected events.

      Matching automation events positions can be useful under the following circumstances:
      • If you want to match the positions of single performance controller events on several Performance Controller
        Automation lanes.

      • If you want to match the position of two adjacent automation events in a clip to create an instant “jump” be-
        tween the two values.

        Matching the positions of several automation events in a single clip is not really useful. It will only place them in a
        “pile” on the same position. The effect during playback would be an instant jump between the extreme values. In
        practice, all events in between the extreme values will be disregarded.


---

<a id="working-with-blocks-in-the-sequencer-10"></a>

=== END OF PART ===
