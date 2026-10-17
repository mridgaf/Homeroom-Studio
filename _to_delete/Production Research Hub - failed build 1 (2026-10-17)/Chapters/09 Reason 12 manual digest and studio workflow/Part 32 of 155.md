# Chapter 09: Reason 12 manual digest and studio workflow
## Part 32 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 23 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 33 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 23 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

          The Eraser tool.
      D   You can also draw a selection rectangle with the Eraser tool to delete several notes in one go.

      Resizing notes
      Resizing notes manually
      When you select a note on the Edit Pane, a handle appears on either edge of the note. You can click any of these
      handles and drag sideways to make the note shorter or longer.

      • If Snap is on (see “Snap”), the beginning and/or end of the note will be magnetic to the (absolute) Snap value
        positions.
      • If several notes are selected, the note you resize with the mouse will be magnetic to absolute Snap value po-
        sitions. The other selected notes will be resized by the current Snap value relative to their original positions or
        lengths.
      • When resizing notes, the event may extend outside the clip boundaries.
          As long as the start position of events is inside the clip, the note will play for the whole duration, i.e. it won’t be cut
          off when the clip ends.
      !   If a note is resized to the left, outside the clip start position, the note will no longer belong to that clip and will
          thus be masked (silent). to unmask the note, resize the clip to the left so that the note’s start position gets in-
          side the clip.

      About resizing drum notes
      Redrum drum notes can be resized, just like any other notes. However, the audible result of this depends on the set-
      tings of the Decay/Gate switch and the Length knob for the drum sound on the Redrum device panel:
      • If Decay mode is selected, the drum sound will play to its end, regardless of the note length in the sequencer.
          Or rather, it will fade out according to the Length parameter setting on the Redrum device panel.
      • If Gate mode is selected, the note lengths in the sequencer affect the resulting sound.
          However, the maximum length of the sound is determined by the Length knob setting - the sound will be cut off
          after this length, regardless of the note length in the sequencer. Also, even if the Length knob is set to its maxi-
          mum value, the sound will not play longer than the length of the drum sample.

      Resizing notes with the “Note Lengths” function

      The Note Lengths pane in the Tool Window.
      The “Note Lengths” function on the Sequencer Tools tab in the Tool Window allows you to add or subtract length val-
      ues to the selected notes.
      Note length resizing can be applied to:
      • Individual (selected) note events in a note clip.
          This has to be done in Edit Mode.
      • All note events in one or several selected note clips.
          This is done in Arrange Mode. If the clips are on the same lane, it can also be done in Edit Mode.
      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All note events in all note clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.
      D   Click the “Add” or “Sub” radio button and select the length value to add or subtract in the corresponding dis-
          play. Then, click “Apply”.
      D   Click the “Fixed” radio button to set all notes to the length defined in the display. Then, click “Apply”.

      Resizing notes with the “Legato Adjustments” function

      The Legato Adjustments pane in the Tool Window.
      The “Legato Adjustments” function can be used to extend each selected note so that it reaches the start position of
      the next selected note. You can also shorten the note length for the first of two selected overlapping notes and set a
      gap between them. You specify the desired gap or overlap in the displays. Only the note length is affected by Legato
      Adjustments - note start positions are never changed.
      Legato adjustments can be applied to:
      • Individual (selected) note events in a note clip.
          This has to be done in Edit Mode.

      • All note events in one or several selected note clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All note events in all note clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.
      • “Side By Side (Abut)” extends the selected note(s) to the start of the next selected note(s):

          A group of notes before and after applying the “Side By Side (Abut)” legato function.
      • “Overlap” extends the selected note(s) to overlap the next selected note(s) by a set amount.

          A group of notes before and after applying the “Overlap” legato function with an overlap of 1/16th note.
      D   “Gap by” introduces a gap between selected notes, which you specify in the “Gap by:” display.

          A group of notes before and after applying the “Gap” legato function with a gap value of 1/16th note.

      Resizing notes in the Inspector
      You can also edit the length of notes numerically in the inspector. See “Note and automation editing in the Inspector”.

      Muting notes
      You can mute individual notes in an open note clip:
      1. Select the Mute tool.

      2. Click the notes you want to mute.
          Muted notes are highlighted in blue in the open clip:

      D   To mute multiple notes in one go, select the desired notes with the Selection (Arrow) tool and press [M].
          Press [M] again to unmute the selected notes.

      Splitting notes
      You can split (slice) one or several notes in an open note clip by using the Razor tool:
      1. Select the Razor tool.

          The Razor tool.
      2. Place the Razor where you want to split the note, and then click:

          A note before and after splitting it.
      D   You can also split several notes by selecting the Razor tool and drawing a selection rectangle that intersects
          the desired split points:

          Splitting two notes by drawing a selection rectangle with the Razor tool.
          The split notes get the same velocity values as their “parent” notes.

      Moving notes
      Moving notes manually
      D   To move a note, click and drag it to a new position, or new pitch (note number), using the Selection Tool.
          If several notes are selected, all will be moved. If Snap is on (see “Snap”), the moved events will keep their relative
          distance to the Snap value positions - or will be moved to new positions on an absolute grid - depending on
          whether you have selected “Absolute” or “Relative” in the Snap value list.

      • By default, when manually moving notes to new pitches (note numbers), the notes will trigger and sound. This
        makes it easier to move (transpose) the notes to where you want them.
          If you don’t want notes to sound during editing, it’s possible to disable the function in the Preferences dialog by de-
          selecting the “Trigger Notes While Editing” box:

          The “Trigger notes while editing” function in the Preferences dialog.
      D   If you hold down [Shift] when you drag, the movement is restricted to horizontal or vertical direction.
          This helps you move notes without accidentally transposing them, or transpose notes without accidentally chang-
          ing their position.
      D   You can also edit the note pitches numerically using the “Pitch (Transpose)” function in the Tool Window.
          See “Pitch (Transpose)”.
      D   You can also move selected notes to a new note clip, on a new additional note lane, by right-clicking (Win) or
          [Ctrl]-clicking (Mac) and selecting “Move Selected Notes to New Lane” from the context menu.
          A new note clip and note lane will be automatically created.

      About moving notes outside or between clips
      If you want to move notes outside the boundaries of an open clip, the result depends on the setting "Keep Events in
      Clip While Editing" on the Options menu:
      • If the “Keep Events in Clip While Editing” option is active, the notes will belong to the open clip after they have
        been moved, but become masked since they are moved outside the clip boundaries.
          The clip position and length will remain unchanged.
      • If "Keep Events in Clip While Editing" is deactivated and you move notes outside the clip, the notes will be
        placed in an existing clip - or in a new clip on the lane, depending on to where you move them to.
          The picture below shows three scenarios when moving three notes outside a clip with the “Keep Events in Clip
          While Editing” option off:

          We’re going to move the last three notes in the clip to beat    The open clip expands by the set Song/Block View Snap
          3 in bar 5.                                                     value (1 bar) to fit in the moved notes.

          Here, we’re going to move the last three notes in the clip to   The notes are placed in the other existing clip at beat 4 in
          beat 4 in bar 10.                                               bar 10.

          Here, we’re going to move the last three notes in the clip to   A new clip is created at bar 12 with a length of the set Snap
          beat 1 in bar 12.                                               value (1 bar) and the notes are placed in beat 1.

      Changing note pitches (transpose) with the arrow keys
      You can use the up/down arrow keys to change the pitches of selected notes by moving them up or down:
      D   Hold [Ctrl](Win) or [Cmd](Mac) and use the up or down arrow key to move the selected notes in semi-tone
          steps.
      You can also move/transpose notes in whole octave steps:
      D   To move the selected notes up/down in octave steps, hold [Shift]+[Ctrl](Win) or [Shift]+[Cmd](Mac) and use
          the up or down arrow key.

      Nudging note positions with the arrow keys
      You can use the left or right arrow keys to “nudge” the positions of selected note events:
      D   Hold [Ctrl](Win) or [Cmd](Mac) and use the left or right arrow key to move the position back or forward by the
          set Snap value.
      D   Hold [Ctrl]+[Alt](Win) or [Cmd]+[Option](Mac) and use the left or right arrow key to move the position back or
          forward in Tick increments.
          There are 240 ticks per 1/16 note so this allows for very fine editing. Check the Tick value in the Inspector when
          you nudge because typically you won’t see the position changes on the Edit Pane, unless you have zoomed in a lot.
      D   Hold [Ctrl]+[Shift](Win) or [Cmd]+[Shift](Mac) and use the left or right arrow key to move the position back or
          forward in Beat increments.

      About nudging notes outside an open clip
      If you nudge notes outside the boundaries of an open clip, the notes will belong to the open clip, but become masked
      since they are nudged outside the clip boundaries. The “Keep Events in Clip While Editing” setting has no effect
      when nudging notes. If you want to move notes between clips, or to a new clip, you have to do that using the Selec-
      tion Tool as described in “About moving notes outside or between clips”.

      Moving notes with the “Alter Notes” function

      The Alter Notes pane in the Tool Window.
      The “Alter Notes” function on the Sequencer Tools tab in the Tool Window alters the positions between the selected
      notes, in a random fashion.
      The “Alter Notes” function can be applied to:
      • Individual (selected) note events in a note clip.
          This has to be done in Edit Mode.
      • All note events in one or several selected note clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All note events in all note clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.
      • The Alter Notes function will only use the note positions that already exist among the selected notes.
      D   Adjust the alteration amount in with the Amount display.
      q   This function is especially useful for experimenting with rearranging Dr. Octo Rex loop slices. Select some
          slices on a Dr. Octo Rex track and use Alter Notes to rearrange the slices and create instant variations, without
          losing the timing and rhythmic feel of the loop.

      Moving notes with the “Extract Notes to Lanes” and “Explode” functions
      It’s possible to move defined notes in a clip to new clips on new, additional lanes. See “Extract Notes to Lanes”.

      Moving notes in the Inspector
      You can also edit the note positions and pitches numerically in the inspector. See “Note and automation editing in the
      Inspector”.

      Duplicating notes
      Duplicating notes manually
      D   To duplicate selected notes, hold down [Ctrl](Win) or [Cmd](Mac) and press [D].
          This will duplicate the selection and place it after the selection, at the closest Snap value after the last note in the
          selection. Repeat the command to continue the duplication for as many times as you like.
      D   To duplicate selected notes, hold down [Ctrl](Win) or [Option](Mac) and click and drag a copy of the selection,
          similar to when moving notes manually (see “Moving notes”).
      D   You can also duplicate selected notes to a new note clip by right-clicking (Win) or [Ctrl]-clicking (Mac) and se-
          lecting “Duplicate Selected Notes to New Lane” from the context menu.
          This will automatically copy the selection and paste it in a new note clip on a new, additional note lane.

      Duplicating notes with the “Extract Notes to Lanes” function
      It’s possible to duplicate defined notes in a clip and automatically place them on new, additional lanes. See “Extract
      Notes to Lanes”.

      Using Cut, Copy and Paste
      You can move or duplicate events using the Cut, Copy and Paste commands on the Edit menu or context menu.
      • When you use Cut or Copy, the Song Position Pointer is automatically moved to the end of the selection.
        This is very useful for repeating events, i.e. pasting the selection several times one after another in the song.

      Pasting events outside an open clip
      When you use the Paste command, the events will appear at the Song Position Pointer, on the original lane. Depend-
      ing on the “Keep Events in Clip While Editing” setting in the Preferences dialog, the following rules apply:
      • If the “Keep Events in Clip While Editing” option is active, the notes will belong to the open clip after they have
        been pasted, but become masked since they are pasted outside the clip boundaries.
        The clip position and length will remain unchanged.
      • If "Keep Events in Clip While Editing" is deactivated and you paste notes outside the clip, the notes will be
        placed in an existing clip - or in another new clip on the lane, depending on where you paste them.
        The picture below shows three scenarios where three notes are being cut and pasted at different positions outside
        the open clip with the “Keep Events in Clip While Editing” option off. We determine the paste positions by moving
        the Song Position Pointer:

        We’re going to cut the last three notes in the open clip and      The open clip expands by the set Song/Block View Snap
        paste at beat 3 in bar 5.                                         value (1 bar) to fit in the pasted notes.

        Here, we’re going to cut the last three notes in the open         The notes are pasted in the other existing clip at beat 4 in
        clip and paste at beat 4 in bar 10.                               bar 10.

        Here, we’re going to cut the last three notes in the open         A new clip is created at bar 12, with a length of the set Snap
        clip and paste at beat 1 in bar 12.                               value (1 bar), and the notes are pasted in beat 1.

      Quantize
      The “Quantize” function on the Transport Panel and on the Sequencer Tools tab in the Tool Window is normally used
      for applying quantization to notes - but can also be used for quantizing recorded audio. Clicking the Quantize or Apply
      button will automatically align the start positions of the selected notes or audio slices to a pre-defined, absolute grid.
      You can also choose to automatically quantize MIDI notes as they are being recorded - see “Quantizing notes during
      recording”.
      Quantization can be applied to:
      • Individual (selected) notes in a note clip or in an audio clip in Pitch Edit mode.
          This has to be done in Edit Mode/Pitch Edit mode.
      • Individual (selected) audio slices in a Single Take audio clip.
          This has to be done in Slice Edit mode.
      • All notes in one or several selected note clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      • All audio recordings in one or several selected Single Take audio clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in the Comp Editor.
      !   In Edit mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All notes in all note clips and/or all audio slices in all Single Take audio clips on one or several selected tracks.
          This has to be done in the Song/Block View.
      The quantization grid is selected in the Quantize Value drop-down list on the Transport Panel and/or in the Quantize
      pane on the Tools tab in the Tool Window:

      The Quantize Value drop-down list on the Transport Panel.

      The Quantize pane in the Tool Window.
      In most situations the Quantize functions on the Transport Panel are probably sufficient. However, if you want more
      in-depth quantization functionality, perform the quantization in the Tool Window instead.
      q   You could also use the ReGroove functions for groove quantizing of notes. See “The ReGroove Mixer”

      Quantizing after recording
      1. Select the note(s)/audio slices, note clip(s)/Single Take audio clips or instrument and audio track(s) you want
         to quantize.
          Only the notes/audio slices in the clip(s) will be affected - not any parameter automation events.
      2. Select a quantize value from the Quantize Value drop-down list on the Transport Panel, or from the Value
         drop-down list in the Tool Window.
          This determines to which note value grid the notes/audio slices will be moved when you quantize. For example, if
          you select 1/16, the notes/audio slices will be moved to (or closer to) the closest sixteenth note position.
      !   Since several audio slices cannot be quantized to the same position, only the slices closest to the quantize
          grid will be moved - the other slices will be ignored.

          The Quantize Value drop-down list in the Tool Window.
          A ‘T’ letter next to some quantization value means Triplets. The effect of using triplets is that three notes are
          equally distributed over the same time period as two “regular” (non-triplet) notes of the same note value.
      3. Select a value from the Quantize Amount drop-down list.
          This is a percentage, governing how much each note or audio slice should be moved. If you select 100%, the
          notes/audio slices will be moved all the way to the closest Quantize value positions; if you select 50%, the notes/
          audio slices will be moved half-way, etc.

          The Quantize Amount drop-down list in the Tool Window.

      4. Click the Quantize button on the Transport Panel or the Apply button in the Tool Window.
          The selected notes are quantized.

          A sloppily recorded hi-hat pattern is quantized to straight 1/4 notes (Quantize Value 1/4, Amount 100%).
      D   Quantization can also be applied to note(s), audio slice(s), clip(s) and track(s) by right-clicking(Win) or [Ctrl]-
          clicking(Mac) and selecting “Quantize” from the context menu.
          The current settings on the “Quantize” pane in the Tool Window will apply when performing this operation.

      Random
      You can offset the quantized notes/audio slices using the Random function. The notes/audio slices will be quantized
      according to the Value and Amount settings, but the note/slice positions will be randomly offset by the set tick value.
      E.g. if you set Random to 10 ticks, the notes/slice positions will randomly vary within a +/- 10 tick range after apply-
      ing quantization.

      Quantize to Shuffle
      In the Value drop-down list, you will also find an option called “Shuffle”. If this is selected when you quantize, the
      notes/audio slices are moved towards sixteenth note positions, but with Shuffle applied.
      Shuffle creates a “swing feel” by delaying the even-numbered sixteenth notes (the sixteenth notes that fall in be-
      tween the eighth notes). The amount of Shuffle is set with the Global Shuffle control in the ReGroove Mixer. Quan-
      tizing to Shuffle is useful if you want to match the timing with pattern devices in the song (if Shuffle is activated in
      their patterns).
      A more flexible way of doing this for notes and note clips is to use the ReGroove mixer - see “The ReGroove Mixer”
      chapter for details.
      !   The Amount setting applies as when quantizing to “regular” note values.

      Quantizing notes during recording
      It’s also possible to quantize input notes directly during recording. Activation of this function can be made in the Tool
      Window and/or on the Transport Panel:
      D   Enable note quantization by ticking the “Quantize Notes During Recording” check box.

          The Quantize Notes During Recording check box on the Sequencer Tools tab.
      D   Alternatively, click the Q Rec button on the Transport Panel.

          The Q Record (Quantize Notes During Recording) button on the Transport Panel.
          It doesn’t matter where you activate or deactivate this function - the current state is automatically mirrored at the
          other location.
          Any notes recorded after having activated this function will be automatically quantized to the current settings on
          the “Quantize” pane in the Tool Window, see “Quantize”.
      !   Audio cannot be quantized during recording!

      Pitch (Transpose)

      The Pitch pane in the Tool Window.
      The “Pitch” function in the Tool Window transposes selected MIDI notes, or all notes in selected note clips, or the au-
      dio recordings in selected audio clips, up or down in whole semitone steps.
      There is also a Randomize function which randomly transposes the pitch of selected MIDI notes in a note clip.
      The “Pitch” function can be applied to:
      • Individual (selected) note events in a note clip.
          This has to be done in Edit Mode.
      • Individual (selected) comp rows in a Comp audio clip.
          This has to be done in Edit Mode (see “Transposing Comp Rows”).
      • All note events in one or several selected note clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in Edit Mode.
      • All audio recordings in one or several selected audio clips.
          This is done in the Song/Block View. If the clips are on the same lane, it can also be done in the Comp Editor.

      !   In Edit Mode, select clip(s) by clicking on it/them in the Clip Overview.
      • All note events in all note clips on one or several selected instrument tracks.
          This has to be done in the Song/Block View.
      • All audio recordings in all audio clips on one or several selected audio tracks.
          This has to be done in the Song/Block View.
      !   In Song/Block View you can transpose a combination of selected note clips/tracks and audio clips/tracks in
          one go!

      Transpose (Semitones)
      D   Click the “Transpose (Semitones)” radio button and then select the number of semi-tones to transpose the se-
          lected notes, note clips and/or audio clips up or down. Click “Apply” to transpose.
      !   For MIDI notes and note clips the transposition is “absolute”, i.e. the notes are permanently moved to new
          note positions in the clip.
      !   For audio clips the transposition is non-destructive, i.e. the audio is transposed relative to their original pitch/
          key without affecting the original audio. For audio clips the relative Transpose amount is also displayed in the
          Transpose display in the Inspector for the selected audio clip(s). See “Transposing Audio Clips” for more de-
          tails about transposing audio clips.
      q   You can also transpose notes by manually moving them using the mouse or arrow keys, as described in “Mov-
          ing notes manually” and “Changing note pitches (transpose) with the arrow keys”.
      q   You can also transpose notes numerically in the inspector. See “Note and automation editing in the Inspec-
          tor”.

      Randomize Notes
      D   Click the “Randomize Notes” radio button and then select the note range to which to transpose the selected
          MIDI notes. Click “Apply” to transpose.
          The selected notes will be randomly transposed within the set note range.

      Extract Notes to Lanes

      The Extract Notes to Lanes pane in the Tool Window.
      The “Extract Notes to Lanes” function on the Sequencer Tools tab in the Tool Window is used for moving or duplicat-
      ing user-defined notes of a certain pitch, or notes within a defined pitch range, to a new note clip on a new, additional
      note lane. This function is very useful if you, for example, have recorded a drum track, with all notes in the same clip,
      and then want to extract individual drum sounds (note pitches in this case) to separate lanes to be able to edit them
      more easily - or to apply ReGroove channels (see “The ReGroove Mixer”).


=== END OF PART ===
