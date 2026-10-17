# Chapter 09: Reason 12 manual digest and studio workflow
## Part 27 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 18 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 28 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 18 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

                             Note Level handle
                                                                                                               Vertical
                                                                                                               Zoom
                                                                           Note handle                         buttons

                             Pitch Correct button
                             Pitch Reset button                                                Note Lines
                                                                           Drift handle
                             Transpose mode
                             buttons
                             Selected note

                                                                           Transition handle

                                                   note with no detectable pitch

                        Reference keyboard
                 Monitor button

      A clip with a lead vocal stereo recording open in Pitch Edit mode.
      The Pitch Editor contains the following elements:
      • Close button
          Click this button to close the audio clip and exit to the Arrange View.
      • Clip Overview
          The Clip Overview area at the top shows the clips on the selected audio track. In the Clip Overview area, selected
          audio clips are displayed in the same fashion as in the Arrange View, i.e. with Clip Resize handles. However, in
          Pitch Edit mode the Level handle and Fade handles are not available. You can select one or several audio clips in
          the Clip Overview and perform clip-based editing (e.g. moving and resizing) - just like in the Arrange View.
      • Note Level handle
          With the Note Level handle you can adjust the level(s) of the selected note(s).
      • Note handle
          Hold this and move sideways to move the note back or forth in time. The range is limited by the adjacent notes,
          which are indicated by the Note Lines, see “Moving notes and changing note lengths”.

      • Note Lines
          These indicate where the notes start and end. You can adjust the start/end positions by click-holding a Note Line
          and dragging it sideways. Changing the position(s) and/or length(s) will also automatically stretch the note(s). See
          “Moving notes and changing note lengths”.
      • Drift handle
          The Drift handle appears when you select the note(s). Drag the Drift handle downwards to reduce the amount of
          any natural pitch drift/vibrato present in the selected note(s), see “Attenuating pitch drift/vibrato”.
      • Transition handle
          The Transition handle(s) control the pitch transition times between the selected note(s) and the previous adjacent
          note(s), see “Editing transition times”.
      • Pitch Correct button
          The Correct button transposes all selected notes to their nearest exact semitone. If no note is selected, the Cor-
          rect function corrects all notes in the open audio clip.
      • Pitch Reset button
          The Reset button removes any transposition/pitch correction changes you have made for all selected notes. If no
          note is selected the Reset function resets the pitches of all notes in the audio clip.
      • Transpose mode buttons
          This is a three-way switch that determines what happens when you drag notes up/down on the note pane:
          Snap = the notes snap to absolute semitones.
          Jump (default) = the notes snap relative to their original pitches, i.e. moves in semitone steps but preserves any
          fine tuning.
          Fine = the notes can be transposed freely, in cents.
          See “Changing transposition” for more details about transposing notes.
      • Monitor button
          With the Monitor button on, you will hear the pitch of a note as a continuous reference tone, when you click the
          note and hold the mouse button depressed. The reference tone changes pitch when you drag the note up/down
          on the note pane. The reference tone reflects the pitch+fine-tune setting of the note. It doesn't matter where in
          the note you click.
      • Reference Keyboard
          The Reference Keyboard is there as a visual guide for the notes on the note pane.

      Selecting notes
      Selecting notes in Pitch Edit mode can be done as follows:
      D   Click a note on the note pane, or on the note’s corresponding section in the clip overview.
      D   You can also select one or several notes by dragging a selection rectangle on the note pane,
      D   Select all notes on the note pane by selecting “Select All” from the Edit menu or context menu.
      D   Click anywhere on the note pane background to deselect the note(s).

      Auditioning notes
      It’s possible to audition individual notes without needing to start playback of the sequencer:
      D   Select the Speaker Tool in the Toolbar and click on the desired note, or its corresponding section in the clip
          overview.
          Each time you click, the note is played back once in its entirety.
      q   With the Selection Tool (Arrow) selected, pressing [Alt](Win) or [Cmd](Mac) will momentarily switch to the
          Speaker Tool.
      !   Note that auditioning notes plays back the unprocessed audio - bypassing the Main Mixer settings.

      Correcting pitches
      1. Select the note(s) you want to pitch-correct. If no note is selected, all notes will be affected by the pitch correc-
         tion.
      2. Click the Correct button to the left of the note pane.
          The Correct function moves all selected notes to their nearest exact note pitch.
      D   Alternatively, hold down [Shift]+[Ctrl](Win) or [Shift]+[Cmd](Mac) and press [C].
      D   To undo the pitch correction and revert to the original pitch(es), click the Reset button.
          If no note is selected, the Reset function will reset the pitches of all corrected (and transposed) notes in the clip!

      Changing transposition
      1. Select the note(s) you want to transpose.
      2. Click and drag the note(s) up/down on the note pane to transpose.
          The Transpose buttons to the left of the note pane determine how the notes will be transposed:
          Snap = the notes will snap to absolute semitones.
          Jump (default) = the notes will snap relative to their original pitches, i.e. move in semitone steps but preserves any
          fine tuning.
          Fine = the notes will be transposed freely, in cents.
      D   You can also fine-tune by holding down [Alt]+[Shift](Win) or [Cmd]+[Shift](Mac) while dragging the notes up/
          down on the note pane.
      • If the Monitor button is on a reference tone, with the pitch of the held note, will play continuously.
      D   To undo the transposition and revert to the original pitch(es), click the Reset button.
          If no note is selected, the Revert function will reset the pitches of all transposed (and pitch-corrected) notes in the
          clip!
      D   Alternatively, you can edit the transposition numerically in the Inspector, see “Note” and “Fine-tune”.

      Resetting pitches
      D   Click the Reset button to reset any transposition and/or pitch correction and revert to the original pitch(es) of
          the selected note(s).
          If no note is selected, the Reset function will reset the pitches of all transposed and pitch-corrected notes in the
          open audio clip!

      Splitting the clip at notes
      It’s possible to split an audio clip at the edges of selected notes in Pitch Edit mode (similar to splitting at slices in
      Slice Edit mode):
      D   Select the note(s) where you want to split the clip and then select “Split at Notes” from the Edit menu or con-
          text menu.

      Reverting all notes
      It’s possible to “undo” all edits you have made in Pitch Edit mode (similar to the “Revert Slices” function in Slice Edit
      mode):
      D   Select “Revert All Notes” from the Edit menu or context menu.
          The clip will be completely re-analyzed and any pitch, timing and timbre edits will revert to the original.

      Attenuating pitch drift/vibrato
      You can attenuate the pitch drift or vibrato for each note individually:
      1. Select the note(s) you want to change the pitch drift/vibrato for.
      2. Lower the Drift handle to “straighten out” the pitch curve in the note, removing large scale pitch drift.
          The default setting is always 100%, which means you can only attenuate the pitch drift/vibrato - not increase it.

      D   Alternatively, you can edit the Drift numerically in the Inspector, see “Drift”.
      q   If you want to preserve small pitch fluctuations in the note, you can use the Preserve Expression parameter in
          the Inspector, see “Preserve”.

      Editing transition times
      When you have recorded your audio and haven’t (yet) made any pitch changes (transpositions) of notes, editing the
      transition times won’t have any effect at all.
      !   It’s only after you have edited note pitches (moved notes up/down on the note pane) that editing transition
          times will have any effect.
      You can edit the pitch transition times between transposed notes as follows:
      1. Select the note(s) you want to change the transition time(s) for.
      2. Drag the Transition handle(s) up/down to control the pitch transition between the selected note(s) and the
         previous adjacent note(s).
          The important thing here is to get a smooth pitch curve (the line) from the preceding note to the following note.
          Adjust the Transition handle until the pitch curve is a smooth line between the notes. The dark blue colored tran-
          sition zones in the notes themselves indicate the transition times. The Transition times can be max 200 ms - or
          half of the note length (if the note length is less than 400 ms).

      D   Alternatively, you can edit the Transition times numerically in the Inspector, see “Transition”.
      q   To get the best result when editing transition times you might also have to change the actual note positions
          without moving/stretching the audio, see “Changing note start positions (without affecting the audio)”.

      Moving notes and changing note lengths
      Moving notes
      To move a note back or forth in time, proceed as follows:
      1. Select the note(s) you want to move.
      2. Click and hold the Note handle in the Clip Overview and drag sideways.
          The closest adjacent notes will then be stretched.
          You may want to deactivate the Snap function if you want to fine-adjust the note position(s).

      D   Alternatively, you can move the note(s) numerically in the Inspector, see “Position”.
      q   If you want to change the note start position(s) and/or note lengths, see “Changing note start positions and
          lengths”.

      Changing note start positions and lengths
      To change note lengths, and thus stretch the note(s), proceed as follows:
      1. Select the note(s) you want to adjust.
      2. Click and hold the desired Note line, on the note pane or in the Clip Overview, and drag sideways.
          Adjusting the length of a note automatically changes the start position of the consecutive note - and vice versa.
          You may want to deactivate the Snap function if you want to fine-adjust the note(s).

      Changing note start positions (without affecting the audio)
      Similar to when editing in Slice Edit mode it’s possible to “decouple” the notes from the actual audio in the note. This
      can be useful if the automatic note placement wasn’t perfect and you have a hard time adjusting the transition times
      between transposed notes (see “Editing transition times”).
      D   Hold down [Ctrl](Win) or [Option](Mac) and drag the note line sideways to change the note start/length with-
          out affecting the audio.

          You may want to deactivate the Snap function if you want to adjust the note start position with greater precision.
          As you can see in the picture above, the pitch curve is left unaffected (unstretched) and only the note start/length
          is affected.

      Proportional stretching of multiple notes
      Like in Slice Edit mode it’s possible stretch a range of notes, proportionally, in an “accordion style” fashion:
      1. Select the desired consecutive range of Notes on the Note pane.
      D   If you drag the start or end Note line in the range, the whole range will be stretched as if it were a single note:

      D   If you drag a Note line within the selected range, all selected notes will be stretched proportionally against the
          start and end Note lines of the selected range.

      Quantizing notes
      Quantizing notes in Pitch Edit mode works just like when quantizing in Slice Edit mode, see “Quantizing audio”.
      !   Note, though, that the quantization is made on the pitch transitions (where the notes start) and not on the level
          transients as in Slice Edit mode.

      Splitting and joining notes
      Splitting notes
      To split a note, proceed as follows:
      1. Select the Razor tool from the Toolbar.
      2. Click on a note where you want to split it, or click in the Clip Overview at the desired split position.
          You may want to deactivate the Snap function if you want to split the note with more precision.

          The two halves of the note are now re-analyzed and placed in suitable pitch positions of the note range. This could
          mean that the new notes are placed differently than the original note.

      Joining notes
      To join notes, proceed as follows:
      1. Select the Eraser tool from the Toolbar.
      2. Click on a note that you want to join with the preceding note, or click in the corresponding section in the Clip
         Overview.

          The new “joint” note is now re-analyzed and placed on the suitable pitch position in the note range. This could
          mean that the new note is placed differently than the original notes.
      D   To join several notes in one go, draw a selection rectangle with the Eraser tool and then release the mouse
          button.
          The result will be one long note, re-analyzed and placed on the most suitable pitch position in the note range.

      About switching from Pitch Edit mode to Slice Edit mode
      !   When you have edited an audio clip in Pitch Edit mode and then switch to Slice Edit mode (with the “Vocal”
          Stretch and Transpose Type still selected), the slices are now based on the note transitions from Pitch Edit
          mode, and not on the level transients.

      Audio pitch editing in the Inspector
      In Pitch Edit mode a series of additional audio pitch editing boxes appear in the Inspector. These are unique to the
      Pitch Edit mode and apply to selected notes on the note pane:

      The Inspector elements for a selected note in Pitch Edit mode.

      Position
      Here you can edit the start position of the note in Bars, Beats, 1/16th notes and Ticks.

      Note
      Here you can set the note value to transpose to, in semitone steps. If the note has a Fine-tune setting, this will be pre-
      served also after the semitone Note transposition.

      Fine-tune
      Here you can detune the note up/down in steps of 1 cent. If you fine-tune more than +/- 50 cents, the Note value
      will change and the fine-tuning will now be based on the new Note value instead. This way you will be able to use the
      Fine-tune function throughout the entire MIDI note range.

      Drift
      Here you can attenuate the pitch drift/vibrato of the audio in the note. The default 100% keeps the pitch drift/vibrato
      unaffected, and at 0% the audio in the note doesn’t contain any pitch drift/vibrato at all.

      Preserve
      The Preserve Expression function works in tandem with the Drift function. If you raise the Preserve Expression value,
      small pitch fluctuations (vibrato and other expressions) are maintained even when you “straighten out” the note by
      lowering the Drift value.

      Transition
      This controls the pitch transition time between the selected note and the preceding note.
      There are dark blue colored transition zones in the notes themselves, which changes according to your edits. The
      Transition times can be max 200 ms - or half the note length (if the note length is less than 400 ms).

      Formant
      Here you can edit the formant “position” of the selected note(s). Changing the Formant downwards creates a deeper
      tone and changing it upwards generates a brighter tone to the vocals.
      Range +/-1 octave, in steps of 0.01 semitones.
      For more information about formants, please have a look at “What are formants?” in the Neptune Pitch Adjuster and
      Voice Synth chapter.

      Level
      Here you can change the level of the selected note(s). The range is -inf to +18 dB.

      Editing audio in the Comp Editor
      In this section we will describe audio editing procedures that are common for Single Take clips and Comp clips when
      edited in the Comp Editor. Comp clip specific procedures are described in “Comping audio”.

      Audio clip elements in the Comp Editor
      When an audio clip is open for editing in Comp Edit mode, its contents are shown on the Edit Pane below the Clip
      Overview area. An open audio clip can have one or several Comp Rows on which the audio recordings reside. The
      number of Comp Rows depends on how you recorded your audio clip. If you only recorded once in the clip, there will
      only be one single Comp Row. If you have recorded several times in the same clip, or several cycles in Loop Mode,
      there will be one Comp Row for each take, or cycle.
      There are vertical zoom controls for resizing the Clip Overview area and the Comp Row area. You can also scroll in
      the Comp Row area by using the scroll bars on the right hand side of the Edit Pane.

      Single Take clips in the Comp Editor
      For Single Take clips, only the recording on the selected Comp Row is played back. If there is only one single Take
      (Comp Row) in the clip, this will play back by default. This is how an open Single Take clip with only one recording on
      one Comp Row could look like when opened in Comp Edit mode:

                 Close button
                                                                                                  Clip Resize handles
                                                       Clip Level handle

                           Fade In                                      Fade Out
                           handle                                       handle

                                                                                                       Vertical Zoom
                                                                                                       buttons

                                                                     Clip Overview

                                                                                                       Vertical Zoom
                                                                                                       buttons

                     Comp Row handle                                           Comp Row with
                    Comp Row Level fader                                       recording
                   Single Take Mode button

      A Single Take clip open in the Comp Editor.
      • Clip Overview
         The Clip Overview area at the top shows the clips on the selected audio track. In the Clip Overview area, selected
         audio clips are displayed in the same fashion as in the Arrange View, i.e. with Clip Resize handles, Level handle and
         Fade handles. You can select one or several audio clips in the Clip Overview and perform clip-based editing (e.g.
         moving and resizing) - just like in the Arrange View.
      • Clip Resize handles
         By clicking and dragging either of the handles, you can change the position and length of the clip.

      • Fade In and Fade Out handles
          Click and drag these handles horizontally to introduce a fade in and/or fade out of the audio in the clip. The fading
          is non-destructive and can be changed at any time. If Snap is activated (see “Snap”), the set (Arrange Mode) Snap
          value is taken into account when moving the Fade Handles.
      • Close button
          Click this button to close the audio clip and exit to the Arrange View.
      • Clip Level handle
          Click and drag this handle vertically to adjust the audio level of the recordings in the clip. The level adjustment is
          non-destructive and can be changed at any time.
      • Comp Row
          Depending on how you recorded the audio clip, there can be one or several Comp Rows, containing one audio re-
          cording each. Comp Rows can be described as “virtual tracks” in the sense that you can have many parallel Comp
          Rows in an audio clip but only play back from one Comp Row at a time (see “Creating a comped audio clip”). In
          Single Take clips, only the audio recording on the currently selected Comp Row will play back.
      • Comp Row handle
          If there are several Comp Rows in the audio clip, it’s possible to rearrange the order of the Comp Rows by clicking
          and dragging the Comp Row handles vertically.
      • Comp Row Level fader
          Use the Comp Row Level fader to adjust the volume of the recording on the corresponding Comp Row. This is es-
          pecially useful in Comp Mode, when you want to trim and balance the levels of the recordings on several Comp
          Rows.
      • Single Take Mode button
          Click this to manually select the desired Comp Row for playback - and thus set the clip to Single Take Mode.
      !   If the clip only has one single Comp Row, this is automatically selected “in the background” by default - i.e. its
          Single Take Mode button is not depressed.

      Comp clips in the Comp Editor
      A Comp clip consists of several Comp Rows, with one recording on each Comp Row. If you have recorded several
      takes in an audio clip and want to cut out sections of the various takes and comp into a final clip, this can be done in
      the Comp Editor (see “Creating a comped audio clip”). This is how an already comped audio clip could look like in
      Comp Edit mode:
             Bounce button                   Segment Focus Indicator

                                                                                             Cut Crossfade Zones

                     Cut Row                                                                 Cut Handles
                                                                                             Silence Row
                                                                                              Comp Rows

                                                                                             Cut Lines

      A Comp clip open in the Comp Editor.
      From the top down in the preceding picture, the Edit Pane contains the following elements:
      • Bounce button
         Clicking this button will bounce the recordings of the comped clip to a new recording, automatically select the
         bounced recording’s Comp Row - and thus set the clip type to Single Take. The same thing happens automatically
         if you click the Slice Edit or Pitch Edit buttons in the Toolbar.
      • Cut Row
         The area between the Clip Overview and the topmost Comp Row is called the Cut Row. This is where the Cut Han-
         dles are placed.
      • Segment Focus Indicator
         The gray Segment Focus Indicator appears if you click on the Cut Row, or if you double-click on a Comp Row. A
         Segment is the area between two Cuts. The Segment Focus Indicator shows which segment currently has edit fo-
         cus. Edit focus is required for editing using keyboard short-cuts (see the “Keyboard Commands” pdf document).
      • Cut Crossfade Zones
         When you have comped an audio clip by creating cuts and assigning different Comp Rows to the resulting seg-
         ments, it’s possible to set individual crossfades between the segments. This makes it possible to get smooth tran-
         sitions between the audio recordings in the different segments. Any crossfades are indicated by boxes. The widths
         of the boxes indicate the crossfade times.


=== END OF PART ===
