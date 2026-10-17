# Chapter 09: Reason 12 manual digest and studio workflow
## Part 33 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 24 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 34 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 24 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      The “Extract Notes to Lanes” function can be applied to:
      • Notes of defined pitches in one or several selected note clips.
          If the clips are on the same lane, this can be done in Edit Mode. If the clips are on separate lanes, this has to be
          done in the Song/Block View.
      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • Notes of defined pitches in all note clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.

      Extract Notes to Lanes example
      We have recorded a 4-bar drum beat, consisting of kick, snare and open+closed hi-hat, in a single clip on a note lane.
      Now, we want to extract the open and closed hi-hat sounds to a new separate note lane. Normally, this could be done
      in the Song/Block View, but to better show what happens with the individual note events, we will show this in Edit
      Mode:
      1. Open the note clip in Edit Mode.
      2. Click in the Clip Overview to enable the ”Extract Notes to Lanes” function.
          Since the Extract Notes to Lanes function applies to selected clips and not to selected notes, you have to click in
          the Clip Overview to enable the function. (In the Song/Block View, you just select the clip by clicking on it).

          Click in the Clip Overview to enable the Extract Notes to Lanes function.
      3. Define which notes you want to move on the “Extract Notes to Lanes” pane in the Tool Window.
          We want to move the open and closed hi-hat notes, i.e. the note range from G#1 to B1. We therefore click the
          “Note Range” radio button and then select the note range in the “From:” and “To:” displays.

          Select the notes to be moved.

      4. Click the “Move” button on the “Extract Notes to Lanes” pane.
          The open and closed hi-hat notes are now moved to a new clip on a new note lane. If we click in the Note Edit lane
          and scroll, we can see the moved hi-hat notes in the new clip:

                                         New note lane

             Original note lane

          The moved notes in a new clip on a new note lane.
          If we exit to the Song/Block View, we can see both the original clip and the new clip:

                                                           New note clip with
                                                           the hi-hat sounds

                                                           Original note clip

          The original clip and the new clip in the Song/Block View.
      D   If you want to move or duplicate notes of a certain note number only, click the “Single Note” radio button and
          select the note pitch in the display. Then click, the “Move” or “Duplicate” button.
          Only the notes of the selected note number will be moved or duplicated to a new clip on a new note lane.
      • The “Extract Notes to Lanes” function is available both in Edit Mode and the Song/Block View, since it’s ap-
        plied to defined notes in clips and not to manually selected notes.
      !   Any recorded performance controller automation will remain on the original note lane.

      The “Explode” function
      D   Click the “Explode” radio button to move or duplicate notes of the same note numbers to new clips on sepa-
          rate note lanes.
          Notes of the same note number will be moved or duplicated to new separate clips on separate note lanes. A new
          lane will be created for each of the used note numbers in the original clip
      q   The “Explode” function is perfect if you have recorded a drum track and want to move, or duplicate, each indi-
          vidual drum sound to a separate note lane for further editing. Applying different ReGroove channels to each of
          the generated note lanes could provide extremely nice grooves to the rhythm! See “The ReGroove Mixer” for
          more details.

      Scale Tempo

      The Scale Tempo pane in the Tool Window.
      The “Scale Tempo” function in the Tool Window can be applied to selected notes and/or automation events. It can
      also be applied to selected note, audio and automation clips. The Scale Tempo function will make the selection play
      back faster (Scale factor above 100%) or slower (Scale factor below 100%). For notes and automation events, this
      is achieved by changing the position of the events (starting from the earliest selected event) and adjusting the length
      of the notes accordingly. For audio clips, high-quality stretching is applied to all audio recordings in the clip.
      Tempo scaling can be applied to:
      • Individual (selected) note and/or parameter automation events in a clip.
          This has to be done in Edit Mode.
      • All note and/or parameter automation events and/or audio recordings in one or several selected clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      !   In Edit Mode, select the clip(s) by clicking on it/them in the Clip Overview.
      • All note and/or parameter automation events and/or audio recordings in all clips on one or several selected
        tracks.
          This has to be done in the Song/Block View.
      • The “Double” and “Half” buttons are “shortcuts” to Scale factors 200% and 50%, respectively.
          These are probably the most common values used, simulating double tempo and half tempo scaling.

          The result of applying Scale Tempo on note events with the Scale factor 200% (double speed).
      • The “Scale to” function can be used for scaling selected clips, or selected events in an open clip, to a fix length.
        The segments in the “Scale to” box are divided into, bars, beats, 1/16th notes and tics.
      !   The Scale Tempo function affects note, performance controller, parameter automation, pattern change, tempo
          automation events and audio clips! It does NOT affect time signature automation.
      !   When you are tempo scaling audio clips, make sure you have selected the appropriate Stretch Type, otherwise
          the sonic result might not be what you’d expect, see “Opening audio clips for editing”.
      !   Note that Pattern Automation Clips will only be resized - the pattern tempo in the source device will NOT be
          scaled but will still be synced to the main sequencer tempo!

      Editing note velocity
      Editing note velocity manually
      The velocity values of notes can be edited manually on the Velocity Edit Lane:

      The velocity values are shown as bars, with taller bars indicating higher velocity.
      Note also that the color intensity of the notes and velocity bars reflect the velocity values.
      D   To change the velocity of a note, click on its velocity bar with the Pencil tool and drag the bar up or down. Click-
          ing above or below a bar immediately adjusts the velocity to the level at which you click.
          You can also edit the velocity of several notes at once by clicking and dragging with the Pencil tool.
      D   When the Pencil Tool is selected and you press [Ctrl](Win) or [Option](Mac) on the Velocity Edit Lane, the pen-
          cil will change to a cross.
          This is the Line Tool which is a special tool only available on the Velocity Edit Lane. By dragging across the velocity
          “bars”, at the desired height, you can quickly draw velocity ramps.

          Drawing a velocity ramp with the Line Tool.
          The Line Tool is probably the preferred method for creating regular, smooth ramps, or for giving all the notes the
          same velocity (by drawing a straight line), while the Pencil tool can be used for creating more irregular curves.

      D   If you hold down [Shift] when you edit velocity values, only selected notes will be affected.
          This can be very useful, especially in “crowded” sections with lots of notes.
          Consider for example if you have a busy drum beat, and want to adjust the velocity of the hi-hat notes only. Simply
          dragging with the Line- or Pencil tool would change the velocity of all other drum notes in the area too, but if you
          first select the hi-hat notes on the Drum Edit lane and press [Shift] as you draw, you can edit their velocity without
          affecting any other notes.

      Editing note velocity with the “Note Velocity” function

      The Note Velocity pane in the Tool Window.
      The “Note Velocity” function in the Tool Window can be used for adjusting the velocity of selected notes in a number
      of different ways.
      Note velocity can be applied to:
      • Individual (selected) notes in a note clip.
          This has to be done in Edit Mode.
      • All notes in one or several selected note clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All notes in all note clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.
      D   The “Add” function lets you add a fixed value to the existing velocity values.
          To subtract, choose a negative value. Note that the allowed range is 1-127.
      D   “Fixed” allows you to set a fixed velocity value for all selected notes.
      D   The “Scale” function allows you to scale velocities by a percentage factor.
          Scaling by a factor of more than 100% will increase the velocity values, but also make the difference between soft
          and hard notes bigger.
          Scaling by a factor of less than 100% will decrease the velocity values, but also make the difference between soft
          and hard notes smaller.
      D   “Random” will randomize the velocity values by a set percentage value.
      q   By combining the “Add” and “Scale” functions, you can adjust the “dynamics” of the notes in various ways. For
          example, by using a Scale factor below 100% and adding a suitable value in the “Add” display, you can “com-
          press” the velocity (decreasing the difference between the velocity values without lowering the average veloc-
          ity level).

      Editing note velocity in the Inspector
      You can also edit velocity values numerically in the Inspector. See “Note and automation editing in the Inspector”.

      Reverse

      The Reverse pane in the Tool Window.
      It’s possible to reverse note (and automation) clips and events, i.e. play the events of the clip “backwards” (from the
      end to the start). The main difference between reversing note (and automation) clips compared to audio clips is that
      in note clips the notes and automation points are reversed (mirrored) - not the actual audio that the notes generate.
      With audio clips, however, the actual audio is reversed (played backwards).
      The Reverse function can be applied to:
      • Individual (selected) note events in a note clip.
          This has to be done in Edit Mode.
      • Individual (selected) automation points in a note clip or in an automation clip.
          For note clips this has to be done in Edit Mode.
      • All note and automation events in one or several selected note and automation clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      • All audio recordings in one or several selected audio clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in the Comp Editor. See
          “Reversing audio clips” for more details about reversing audio clips.
      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All note and automation events in all note and automation clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.
      • All audio recordings in all audio clips (and all automation clips, if any) on one or several selected audio tracks.
          This has to be done in the Song/Block View.
      !   In Song/Block View you can reverse a combination of selected note clips/tracks and audio clips/tracks in one
          go!
      There are two different types of Reverse functions for note clips: the “Reverse notes graphically” and the “musical re-
      verse”. The “Reverse notes graphically” function considers the note lengths when the new start positions are calcu-
      lated, whereas the “musical reverse” function only considers the notes’ start positions.
      Here is an example of a masked note clip in Edit mode, with automation points before and after using the “Reverse
      notes graphically” function:

      As you can see, all end positions (Note Offs) of the notes become the new start positions (Note Ons) after the re-
      verse procedure. Also, any masked notes and automation points are also “flipped around”.
      Here are examples of using the Reverse functions on a selected note clip and on selected notes in a note clip:

      A note clip selected before reversing.   The note clip reversed using the        The note clip reversed using the
                                               “Reverse notes graphically” function.   “musical” Reverse function. Here, only
                                                                                       the notes’ start positions are mirrored.

      Selected notes in a note clip before     The selected notes reversed using the   The notes reversed using the “musical”
      reversing.                               “Reverse notes graphically” function.   Reverse function. Here, only the notes’
                                                                                       start positions are mirrored.

      Multi Lanes editing
      Overview
      Multi Lanes editing lets you have note clips of multiple lanes visible at the same time on the Edit pane, in a layered
      fashion. This makes it a lot easier to edit notes in relation to other notes in other clips:

      Four clips on four different lanes in Multi Lanes edit mode, with the note lane on the EuroBass tack currently selected.

      Selecting multiple lanes for editing
      The easiest ways of selecting what note lanes should be available for Multi Lanes editing are these:
      • By selecting multiple instrument tracks in the track list and then entering Edit mode in the Sequencer.
      • By selecting multiple note clips on the Arrange pane and pressing [Return], or right clicking one of the
        selected clips and then selecting “Edit” from the context menu.
      D   In Edit mode, make sure the Multi Lanes button is on:

          The Edit pane now shows all (un-muted) clips on all selected lanes in a layered fashion, with the notes of the cur-
          rently selected note lane in red and the notes of the other lanes in grey:

      • If a single sequencer track contains multiple lanes, selecting the track will automatically display all clips on all
        un-muted lanes:

          The RnB Kit 03 track, which contains six lanes, selected for Multi Lanes editing.
      q   With the Multi Lanes editing feature, the functions “Move/Duplicate Selected Notes to New Lane” and “Extract
          Notes to Lanes” are very useful, especially when working with drum tracks.

      Editing notes in Multi Lanes mode
      Editing notes in Multi Lanes editing mode is done in the same way as when editing one clip on one lane at a time, as
      described earlier in this chapter. The only important thing to bear in mind is which lane you want to edit:
      D   Select the lane you want to edit, either by clicking the desired Lane selector in the track list...

          The lane on the EuroBass track is currently selected.
      D   ... or by clicking a note on the Edit pane:

          The notes of the currently selected EuroBass lane shown in red on the Edit pane and the notes of the other lanes are shown in grey.
      • If you click any of the grey notes on the Edit pane, the lane that this note belongs to is automatically selected
        in the track list.
          Now, all notes of the newly selected lane become red, and the notes of the other lanes become grey.
      !   It’s not possible to edit multiple notes on multiple lanes together - only notes of the currently selected lane can
          be edited together (e.g. moved, transposed, etc.).
      !   If the tracks selected for Multi Lanes editing has different Note Edit Modes (e.g. REX Edit Mode or Drum Edit
          Mode), you might want to switch to regular Key Edit Mode for the entire note range to become visible and
          accessible on the Edit pane. See “Note Edit Modes” for more details.

      Automation editing
      Overview
      Parameter automation is stored in clips as automation events (points), connected by lines. When recorded or drawn,
      the automation lines are straight. However, if you wish you could edit the lines into curves afterwards.

      Automation lanes for a Mixer 14:2 Level slider (top), Mute button (middle) and Aux Send slider (bottom) in Edit Mode. The Aux Send
      automation clip at the bottom is open for editing.
      • Parameter automation is contained in automation clips on Parameter Automation Lanes (see “Edit Mode ele-
        ments”).
          Each automated parameter has its own Parameter Automation Lane.
      • Performance controller automation is stored on Performance Controller Edit Lanes in note clips (see “Edit
        Mode elements”).

      Editing parameter automation
      Parameter automation events can be edited both in the Song/Block View and Edit Mode. In the Song/Block View
      the parameter automation clip can be opened in sort of a “semi edit mode”, which shows the automation events of the
      selected clip. You can also edit the parameter’s Static Value. Editing automation events works in the same way,
      whether in the Song/Block View or in Edit mode.

      Editing parameter automation in the Song/Block View
      D   In the Song/Block View, double-click the parameter automation clip on the parameter automation lane.
          The parameter automation clip is now opened in the Song/Block View:

                                                                                 Static Value controls
                                                                                    Parameter automation events

          A parameter automation clip before and after opening it in the Song/Block View.
      Here you can edit the parameter’s Static Value (see “Static Value Handles”) with the up/down arrow buttons to the
      left of the open clip. Alternatively, double-click and type in a new Static Value in the box.
      In the open parameter automation clip, it’s possible to move, add and delete automation events in the same way as in
      Edit Mode using the Selection (Arrow), Pencil and Eraser tools - see “Editing parameter automation in Edit Mode”.

      • A selected automation event’s position and value is also shown in the Inspector.

                                                                           Position and Value of
                                                                           the selected parameter
                                                                           automation event

                                                                           Selected parameter
                                                                           automation event

          The event’s position and value can be edited numerically in the displays - see “Note and automation editing in the
          Inspector”.
      D   To close an open parameter automation clip in the Song/Block View, press [Esc] or click on another lane on
          the Arrangement Pane.
      D   If you resize the automation clip and make it longer, the first and/or last automation value will be extended all
          the way to the clip boundary.

          In the picture above, a Mixer 14:2 Mute button is automated. The clip only contains a single automation point, but
          as we extend the clip in both directions, the value is automatically extended to the start and end of the clip. This
          means you can adjust the Mute automation time by moving and resizing the clip, without having to open the clip.

      Editing parameter automation in Edit Mode
      1. Open the parameter automation clip in Edit Mode.
      D   If the parameter automation clip is on an Instrument Track, just double-click a Note clip to enter Edit Mode.
      D   If the parameter automation clip is not on an Instrument Track, first double-click the automation clip and then
          click the “Open In Edit Mode” button.
          Use the dividers if necessary to locate the automation clip to edit - these are located at the bottom of the Edit/Ar-
          range Pane (not in the note clip). Parameter automation clips are distinguished by a “cut off” upper right corner.

                                                                                            Parameter automation
                                                                                            clips in Edit Mode

          An instrument track in Edit Mode with parameter automation clips at the bottom.
      2. Open the parameter automation clip for editing by double-clicking it or by selecting it and pressing [Return].
          The parameter automation clip is now open for editing.

                                                                                            Parameter automation
                                                                                            clip open for editing

          The “Parameter 1” automation clip open for editing in Edit Mode.
          In Edit Mode, the parameter’s Static Value is shown to the left in the automation lane. In this example, the Static
          Value is set to 20 - this means that the “Parameter 1” value will be set to 20 everywhere in the song except where
          there are automation clips for the parameter.
      D   To change the Static Value, click and drag the handle up or down, or double-click and type in a new value.
          To fine adjust the Static Value, hold down [Shift] when you click and drag.

                    Static Value handle
      q   The Static Value can also be edited in the Song/Block view, see “Editing parameter automation in the Song/
          Block View”.

      3. When a parameter automation clip is open, you can select, move, copy or delete automation events, using the
         Selection (Arrow) Tool.
          When moving automation events with the Selection (Arrow) Tool, Snap (see “Snap”) is taken into account if en-
          abled. You can also resize the clip by dragging the clip handles.
      D   If you resize the automation clip and make it longer, the duration of the first or last automation event will be
          extended all the way to the clip boundaries (see the last example in “Editing parameter automation in the
          Song/Block View”).
      • A selected automation event’s position and value is also shown in the Inspector.
          These values can be edited numerically in the Inspector displays. See “Note and automation editing in the Inspec-
          tor”.

      About moving parameter automation events outside an open clip
      If you move parameter automation events outside the boundaries of an open clip, the same rules apply as when mov-
      ing note events outside an open clip. See “About moving notes outside or between clips”.

      Drawing parameter automation events
      To add new parameter automation events, do any of the following:
      D   Double click with the Selection (Arrow) Tool in the open automation clip to insert an automation point.
          Double click, hold, and then drag to draw a series of automation points in the clip.
      D   Click or drag with the Pencil Tool in the open automation clip.
          When dragging, the resulting curve (i.e. the number of points) depends on two factors; the selected “Automation
          Cleanup” setting in the Preferences menu (see “About Automation Cleanup”), and the snap value if Snap is acti-
          vated (see “Snap”).
      D   To add an additional automation point onto an automation line, hold down [Shift] and click with the Pencil tool
          at the position you want the point to be added.
          This is also useful if the automation clip doesn’t yet contain any automation points, and you want to add the first
          automation point with the same value as the Static Value.
          Note that if the automation line is curved (see “Creating curves between automation points”), the line will become
          straight (not curved) to the right of the added point.

          Three examples of Shift-clicking automation points with the Pencil tool: adding the first point in an empty clip, adding a point on a
          straight line and adding a point on a curved line.
      • Holding down [Ctrl](Win) or [Option](Mac) and clicking or dragging with the Pencil tool will insert an automa-
        tion range (the same parameter value over a period of time).
          The length of the range is set with the Snap value.

          Drawing an automation range.

      • When the automated parameter is “stepped” rather than continuous, there will be abrupt steps between the
        automation events instead of linear ramps.
          Examples of stepped parameters could be device buttons and multi-mode selectors, and the Sustain Pedal perfor-
          mance controller.

          Stepped automation.

      About drawing parameter automation events outside an open clip
      If you draw parameter automation events outside the boundaries of an open clip, the same rules apply as when draw-
      ing note events outside an open clip. See “About drawing notes outside an open clip”.

      Creating curves between automation points
      When you record or draw automation, the lines between the automation points are always straight (vectors). This
      works perfectly fine in most situations. However, if you like you could change the straight lines into curves, to create
      different character to your parameter automation.
      Creating curved automation works both in the Song/Blocks View and in Edit Mode.
      1. Open an automation clip (in the Song/Block View or in Edit Mode).
      2. With the Selection (Arrow) tool selected, click and drag an automation line to make it curved:
          The arrow switches to a “curve tool” as you hover over an automation line.

          Creating curved automation in an automation clip open in Song View.

          Creating curved automation in an automation clip open in Edit Mode.
      D   To edit the curve shape, repeat the procedure above and drag in the desired direction.
      D   To make a curve straight again, hold down [Shift] and click the automation line.
      D   Double click an automation curve/line to add an automation point on the line.
      !   Note that it’s not possible to create a curve from a straight horizontal automation line (which has automation
          points with the same value).


=== END OF PART ===
