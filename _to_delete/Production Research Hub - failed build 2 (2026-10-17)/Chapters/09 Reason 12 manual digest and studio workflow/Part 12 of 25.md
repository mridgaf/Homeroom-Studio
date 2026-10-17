# Chapter 09: Reason 12 manual digest and studio workflow
## Part 12 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Reference.md (piece 3 of 10) — Reason 12.7 Operation Manual — Compiled Reference

(Next: Part 13 of 25)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Reference.md (piece 3 of 10)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Reference.md
=====================================================

## 7. Arranging in the Sequencer


The clip Position display shows at what position in the song the clip begins. The display readout is divided into Bar, Beat, 1/16 Note and Ticks (1/16th note=240 Ticks). The position can be edited according to the descriptions in “Moving clips using the Inspector”.

The clip Length display shows the length of the clip. The display readout is divided into (from left to right) Bar, Beat, 1/16 Note and Ticks. The length can be edited according to the descriptions in “Resizing clips using the Inspector”.

The Fade In and Fade Out displays for selected audio clips show the Fade In and Fade Out times for the audio in the clip. The readout is divided into 1/16 Note and Ticks. The Fade times can be edited as described in “Inspector segment displays”.

The Level display for selected audio clips shows the level of the audio in the clip. The readout is divided into dB and 1/100 dB. The level can be edited as described in “Inspector segment displays”.

The Transpose display shows the transposition of the audio recordings in the selected Audio Clip(s) - relative to the original pitch. The display readout is divided into (from left to right) Semitones and Cents, See “Transposing Audio Clips”.

In Song View, several clips can be selected, e.g. for cutting, copying, pasting, deleting, moving and resizing purposes. If you select multiple note clips, these can be opened for Multi Lanes editing, see “Multi Lanes editing”.

Besides the Clip Resize handles, a selected audio clip also has Fade In and Fade Out handles plus a Clip Level handle. These can be edited at any time, either by using the handles as described below, or using the Inspector as described in “Fade In and Fade Out displays (audio clips only)” and “Level display (audio clips only)”:

The Fade settings can be set individually for each audio clip in the song. The fading is non-destructive and can be changed at any time. If Snap is activated (see “Snap”), the set Snap value is taken into account when setting the fade time(s).

You can also draw selection rectangles with the Selection tool, encompassing several clips and delete them all at once. The same rules apply as when selecting clips (see “Selecting clips”).

If you resize a clip and make it smaller, any recordings or events that now lie outside the clip boundaries will not sound, or have any effect, when played back. However, they are not deleted - just masked. If you make the clip larger again, the recordings or events that were masked will become visible and will play back again. See “About masked recordings and events”.

See “Inspector segment displays” for more details on how to edit in the Inspector displays.

•

Masked performance controller events, parameter automation events and pattern automation events will be inactive - but could still affect the masked clip (see “About masked performance controllers and automation events” below). Outside a masked clip, the controller/parameter/pattern values will default to their Static Values in the masked area (see “Static Value Handles”).



Below, we will describe how to use the “scale tempo” tool to manually stretch clips. Numerical tempo scaling in the Tool Window is explained in “Scale Tempo” in the “Note and Automation Editing” chapter.

For more details about tempo scaling audio clips, refer to “Tempo scaling Clips” in the “Audio Editing in the Sequencer” chapter.

It’s also possible to select and move several clips by dragging and dropping them at the desired destination. If the Snap function is selected (see “Snap”), you will only be able to move the clip(s) in steps of the selected Snap value - or to absolute positions on the grid, depending on the Snap settings.







•

The set Snap value is taken in to account if the function is activated (see “Snap”). It’s also possible to move several selected clips in one go.



•



If you have recorded non-standard controller parameters for a device in the note clip using the “Record Automation into Note Clip” option (see “Recording parameter automation into Note Clips”) some automated parameters may not have an equivalent parameter in the target device.

Any lane can only play back a single clip at a time - if you want to mix two clips, put them on separate lanes (note clips) or on separate tracks (audio clips). See “Adding note lanes” and “Duplicating/copying tracks and devices”.



•

2.



Activate Snap (see “Snap”) and set the Snap value to “Bar” (or to the length of the section you want to repeat).

On the Razor Tool’s left edge is a cross-hair which indicates where the split will take place. If activated, the Snap setting is taken into account (see “Snap”).



4.

It’s also possible to reverse clips, i.e. play the content of the clip “backwards” (from the end to the start). This works a little differently for audio clips and note clips. Please refer to “Reverse” for information about reversing note and automation clips, and to “Reversing audio clips” for information about reversing audio clips.



•



for creating audio clips that you could use as samples in any sample player device (see “Bounce Clip(s) to New Sample(s)”) or as REX loops in the Dr Octo Rex (see “Bounce Clip to REX Loop”).



•
---

<a id="audio-editing-in-the-sequencer-8"></a>
## 8. Audio Editing in the Sequencer


This chapter describes how to edit audio clips after you have recorded them in the sequencer. General sequencer functions, recording, note and automation editing, and arranging in the sequencer are described in detail in the chapters “Sequencer Functions”, “Recording in the Sequencer”, “Note and Automation Editing” and “Arranging in the Sequencer”.

Slice editing can be made on Single Take clips (see “Clip Types” below). Single Take clips can be opened for editing in Slice Edit mode in the Arrange View, similar to when editing parameter automation clips. Slice editing allows you to adjust the positions (timing) of the automatically detected and distributed transient slice markers that appear in the audio clip. The timing can be adjusted by moving and stretching (warping) the audio slices. See “Editing audio in Slice Edit mode”.

In Pitch Edit mode you can graphically correct and edit the pitches of monophonic audio in Single Take clips -   
perfect for vocal pitch correction/manipulation. See “Editing audio in Pitch Edit mode” for more information.

perfect for vocal pitch correction/manipulation. See “Editing audio in Pitch Edit mode” for more information.

In Comp Edit mode you can cut out segments of several Takes (recordings) and compile into a final clip. Here you can also insert silence segments to e.g. remove noise from silent parts in your audio clips. See “Editing audio in the Comp Editor”.

The Stretch and Transpose Type, together with the Clip Type, also determines the default Edit Mode in which the clip will open when you double-click it, see “Opening audio clips for editing”. However, you can always change the Edit Mode for a clip manually, if you like.

The formants are preserved and are not transposed along with the audio. This will keep the original character of the vocal and will only affect the pitch. “Vocal” is also the default Stretch and Transpose Type for editing audio in Pitch Edit mode, see “Editing audio in Pitch Edit mode”.

When the audio clip is in Slice Edit mode you can stretch, move and quantize audio slices etc., see “Editing audio in Slice Edit mode”. When the clip is open in Pitch Edit mode you can pitch-correct and transpose individual notes (pitches) in monophonic audio recordings, see “Editing audio in Pitch Edit mode”. When the clip is open in Comp Edit mode you can alternate the playback between several recordings and compile into a single recording, see “Editing audio in the Comp Editor”.







•

If more than one Slice Marker has been selected, a Slice Group Handle appears below the waveform. You could then click and drag the Slice Group Handle sideways to move all selected Slice Markers as a group, see “Moving several Slice Markers”.

The range of Slice Markers can then be moved as a group by clicking and dragging the Slice Group Handle sideways. You can also stretch the range in an “accordion style” fashion by clicking and dragging any of the selected Slice Marker Handles in the range, see “Stretching a range of Slices”.

Now, you can move all Slice Markers as a group by dragging the Slice Group Handle sideways (see “Moving several Slice Markers”), or stretch the entire range of Slices (see “Stretching a range of Slices”).



If you are not satisfied with the position of the Slice Marker, you can reposition it afterwards, see “Repositioning Slice Markers”.











•



It’s also possible to move a range of Slices by selecting a range of Slice Markers as described in “Selecting Slices and Slice Markers” and then dragging the Slice Group Handle sideways.











If you like, you can now select the desired clip(s) and move, reverse (see “Reversing audio clips”) or choose to bounce the clip(s) to samples (see “Bounce Clip(s) to New Sample(s)”).



Refer to the “Dr. Octo Rex Loop Player” chapter for information on how to work with REX Loops in the Dr Octo Rex device.

If you want to load your REX Loop in another sampler device, you first have to un-self-contain the REX file, see ““Un-self-containing” a Song”. Then, create the sampler device and load the un-self-contained REX file from disk.

3.

Hold this and move sideways to move the note back or forth in time. The range is limited by the adjacent notes, which are indicated by the Note Lines, see “Moving notes and changing note lengths”.

These indicate where the notes start and end. You can adjust the start/end positions by click-holding a Note Line and dragging it sideways. Changing the position(s) and/or length(s) will also automatically stretch the note(s). See “Moving notes and changing note lengths”.

The Drift handle appears when you select the note(s). Drag the Drift handle downwards to reduce the amount of any natural pitch drift/vibrato present in the selected note(s), see “Attenuating pitch drift/vibrato”.

The Transition handle(s) control the pitch transition times between the selected note(s) and the previous adjacent note(s), see “Editing transition times”.

This is a three-way switch that determines what happens when you drag notes up/down on the note pane:   
Snap = the notes snap to absolute semitones.  
Jump (default) = the notes snap relative to their original pitches, i.e. moves in semitone steps but preserves any fine tuning.  
Fine = the notes can be transposed freely, in cents.  
See “Changing transposition” for more details about transposing notes.

Snap = the notes snap to absolute semitones.

Jump (default) = the notes snap relative to their original pitches, i.e. moves in semitone steps but preserves any fine tuning.

Fine = the notes can be transposed freely, in cents.

See “Changing transposition” for more details about transposing notes.















2.

Similar to when editing in Slice Edit mode it’s possible to “decouple” the notes from the actual audio in the note. This can be useful if the automatic note placement wasn’t perfect and you have a hard time adjusting the transition times between transposed notes (see “Editing transition times”).

Quantizing notes in Pitch Edit mode works just like when quantizing in Slice Edit mode, see “Quantizing audio”.

#Note

For more information about formants, please have a look at “What are formants?” in the Neptune Pitch Adjuster and Voice Synth chapter.

In this section we will describe audio editing procedures that are common for Single Take clips and Comp clips when edited in the Comp Editor. Comp clip specific procedures are described in “Comping audio”.

Click and drag these handles horizontally to introduce a fade in and/or fade out of the audio in the clip. The fading is non-destructive and can be changed at any time. If Snap is activated (see “Snap”), the set (Arrange Mode) Snap value is taken into account when moving the Fade Handles.

•

Depending on how you recorded the audio clip, there can be one or several Comp Rows, containing one audio recording each. Comp Rows can be described as “virtual tracks” in the sense that you can have many parallel Comp Rows in an audio clip but only play back from one Comp Row at a time (see “Creating a comped audio clip”). In Single Take clips, only the audio recording on the currently selected Comp Row will play back.

A Comp clip consists of several Comp Rows, with one recording on each Comp Row. If you have recorded several takes in an audio clip and want to cut out sections of the various takes and comp into a final clip, this can be done in the Comp Editor (see “Creating a comped audio clip”). This is how an already comped audio clip could look like in Comp Edit mode:

•

•



















•

See “Adding Cuts” for more details on how to use the Cut Tool.

The Razor Tool can also be used for assigning a complete Segment, with a start and end Cut, by clicking and dragging (swiping) the Razor Tool horizontally on the desired Comp Row. See “Adding Segments” for more details on how to swipe with the Cut Tool.

Select one or several Comp Rows (see “Selecting Comp Rows”) and then press [Backspace] or [Delete], or select “Delete” from the Edit menu or context menu.







Duplicating Comp Rows can be useful if you want to re-use the same part of a take several times in a comped clip. Duplicate the Comp Row and then adjust the Recording Offset (see “Adjusting the Recording Offset”) in the duplicated Comp Row to access the same part of the recording in another segment of the comped clip. Duplicating Comp Rows will not use up any more space on your hard disk, so you can do this as many times as you like.

In this section we will describe procedures that are specific to audio editing in Comp clips. At the end of this section is a detailed example on how to use the various procedures to create a complete comped audio clip - see “Creating a comped audio clip”. General audio editing procedures are described in “Editing audio in the Comp Editor”.



•



If you’re happy with the result and don’t plan to edit the clip any further, you can use the “Delete Unused Recordings” function to delete the recordings on the original Comp Rows and reduce the file size (see “Delete Unused Recordings”). If file size is not an issue, you can keep the original takes in the clip. This way you can switch to Comp Mode at any time if you need to edit the comp.



If you have recorded more than one loop cycle of audio in Loop Mode (see “Recording audio in Loop mode”), or recorded over or into an existing audio clip (see “Recording over or into an existing audio clip”), each recording has been placed on a separate Comp Row. If you like, you can now select the best parts (segments) of the recordings on the various Comp Rows and create a final “comped” audio clip. All editing described below is non-destructive and can be changed at any time:

Audition the recordings on the Comp Rows to decide which recordings to use at what position in the comped clip. Select the Speaker Tool and click-hold at desired positions on the different Comp Rows (see “Speaker Tool” for details).







The clip is then also automatically set to Single Take mode, which makes it possible to edit the clip in Slice Edit mode, where you can stretch and quantize the audio etc. (see “Editing audio in Slice Edit mode”), or in Pitch Edit mode, where you can correct and edit the pitches of monophonic audio recordings (see “Editing audio in Pitch Edit mode”).

•

The Audio Clips are bounced to new Song Samples and named according to the Audio Clip name (if the clip was named) or according to the Audio Track name with serial numbers. The bounced Audio Clips then end up as sample files in the Song Samples location in the Browser. Refer to “Sampling” for more details about sampling and sample editing.

The “Bounce > Bounce Clip to Disk” function on the Edit menu and clip context menu allows you to export the audio of a selected clip to disk as a single WAV or AIFF file. This might be useful if you want to process an audio clip in an external application and then re-import the clip to the track again. See “Bouncing Audio Clips” for more details.

The Scale Tempo function can also be applied to clips numerically in the Tool Window, see “Scale Tempo”.







•

•







See “Inspector segment displays” for details on how to edit in the Inspector displays.

For Cut Handles, only Crossfade values can be matched - not the Positions. See “Matching audio values using the "Match Values" function”.
---

<a id="note-and-automation-editing-9"></a>

=== END OF PART ===
