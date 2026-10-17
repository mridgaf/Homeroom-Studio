# Chapter 09: Reason 12 manual digest and studio workflow
## Part 35 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 26 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 36 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 26 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 10: Working with Blocks in the Sequencer

Working with Blocks
in the Sequencer

      About this chapter
      This chapter describes how to work with Blocks and Block Automation Clips in the main sequencer. Basic sequencer
      functions, recording, editing clips and events and arranging in the sequencer are described in detail in the chapters
      “Sequencer Functions”, “Recording in the Sequencer”, “Audio Editing in the Sequencer”, “Note and Automation Edit-
      ing” and “Arranging in the Sequencer”.

      Introduction
      The arrangement in the sequencer has two basic views: the Song View, which is exactly the same as the “Arrange
      Mode” in previous versions of the program, and the Blocks view. The Block View is designed for creating shorter
      multi-track “sections” that can be repeated anywhere in the song arrangement. In most situations a Block would
      probably consist of 4-8 bars.
      An analogy to a Block would be a traditional drum machine pattern where you would record several (drum) instru-
      ment tracks and save as a complete “pattern”. Then, you would build up your song arrangement by arranging your
      patterns, one after another, with repetitions etc.
      The Song and Block Views share the same Track List but use separate clips and recordings. Any track and clip types
      can be used when working with Blocks, e.g. instrument tracks with note clips, audio tracks with audio clips, automa-
      tion tracks with parameter automation clips and pattern tracks with pattern automation clips.
      32 different Blocks are available in the program and each Block can be reused and repeated in the song arrange-
      ment as many times as you like. By working with Blocks you can create complete verse and chorus blocks and ar-
      range and reuse them as desired in the song. When you arrange your Blocks in the song - using Block Automation
      Clips - you can also choose to temporarily mute desired lanes for the duration of each Block Automation Clip to cre-
      ate variations.

      The idea behind Blocks
      Working with the sequencer in a “pattern based” fashion appeals to many users. It is the way traditional hardware se-
      quencers worked when they were first introduced on the market. The linear working method of most software se-
      quencers also have many advantages. So, why not combine these two basic working methods to get the best of both
      worlds!
      A very neat way of working with Blocks is by combining Block data with regular linear song data. In the picture below,
      Block data is being used as base for the song. Then, a number of shorter linear clips are used to override parts of the
      Block data to introduce nice variations in the song:

                                                   Blocks Data (shaded)
                                                                                             Linear clips override
                                                                                             Block data to introduce
                                                                                             nice variations

      Linear clips override Block data to create nice variations in the final arrangement.

      Arrangement Views
      Song View (with Blocks disabled)

      The sequencer in the Song View.
      This is the Song View, which is the same as “Arrange Mode” in older versions of the program. Here you work with
      your song in a linear fashion, by recording and arranging your clips from the start of the song to the end. Songs cre-
      ated in previous versions of the program will automatically open up in the Song View, so it will all look very familiar.

      Song View (with Blocks enabled)
      When you create a new song, or a song from a template, the sequencer will automatically have the Blocks function
      activated. However, if you open a song that was previously saved with the Blocks function off, you will have to manu-
      ally activate Blocks:
      D   Select “Enable Blocks” on the Options menu to enable the Blocks function.
                      Block View button
                          Song View button

                                                  Blocks Track

          The sequencer in Song View with “Enable Blocks” activated
          With Enable Blocks activated on the Options menu, an additional track - the Blocks Track - becomes available
          above the Transport Track. On the Blocks Track you can arrange your Block Automation Clips once you have re-
          corded your Blocks. There are also two buttons to the left on the Blocks Track in the Track List: the Block and
          Song View buttons.

      Block View
      D   Click the Block button on the Blocks Track to switch to the Block View.
          A colored area appears on the arrangement pane with the Block name at the top on the Blocks Track. By default,
          the Blocks are named “Block n” where “n” is a number between 1 and 32. If you like, you can rename your Blocks
          to more suitable names (see “Renaming Blocks”). The Block View is where you record the clips you want to in-
          clude in a specific Block. The clips present in the colored Block area in the Block View are unique only to that spe-
          cific Block.

                                            Block Area

          The sequencer in Block View
      !   The Song View and Block View share the Track List. However, the clips on the lanes are unique to the respec-
          tive views. This means you can have clips in the Song View “on top” of clips in Blocks. See “Combining Block
          Automation Clips with Song Clips” for more details.

      Editing Blocks in the Block View
      Selecting a Block for editing
      Selecting a Block for editing is done in the Block View. Select the Block you want to work with as follows:
      1. Make sure “Enable Blocks” is activated on the Options menu.
      2. Click the Block button on the Blocks Track to switch to Block View.
          Block 1 appears by default on the arrangement pane:

      3. Select a Block (1-32) from the Blocks drop-down list in the Track List if desired.
          In this example, we will stick to Block 1. The Block name is shown on the Blocks Track.

      Renaming Blocks
      If you don’t want to use the default Block names you can easily rename them:
      D   Double-click the Block name on the Blocks Track in the Block View, type in a new name and press [Return].

      Defining the Block length
      The length of a Block is defined using the End Marker in the Blocks view:
      1. Select desired Block in the Block View as described in “Selecting a Block for editing”.
      2. Adjust the End Marker to the desired position by clicking and dragging it in the Ruler.

      • The Block length is always defined from the beginning of the Ruler to the End Marker.
          The Left and Right Loop Locators have no influence on the Block length.
      • When the sequencer is running in Block View, it will automatically loop at the End Marker.
          The Loop Locators can also be used in Block View to loop at other positions, if Loop On/Off is activated on the
          Transport Panel. However, in Song View the Loop Locator settings used in the Block View will be ignored.
      • The Block length can be set individually for each of the 32 Blocks.
      • The Block length can be changed at anytime by adjusting the End Marker in the Blocks view.

      Changing Block color
      Selecting separate colors for your blocks can be useful when you arrange your blocks in the Song View later on. All
      32 Blocks already have default colors but these can easily be changed:
      D   Select a color from the Block Color palette on the Blocks Track context menu or from the Edit menu.
          This applies the selected color to the Block. The sequencer tracks and any clips in the Block will maintain their
          original colors.

      Recording in the Block View
      Recording on tracks in the Block View is done in the same ways as when recording in the regular Song View.
      !   Any events or recordings to the right of the End Marker in the Block View will be ignored when the Block is
          played back in the Song View.
      Refer to “Recording in the Sequencer” for details about recording.

      Editing clips in the Block View
      Editing events in clips in the Block View is done in the same way as when editing clips in the Song View.
      D   Double-click desired clip to open it for editing in Edit Mode, or click the Edit Mode button in the Toolbar.
          Refer to “Note and Automation Editing” and “Audio Editing in the Sequencer” for details about editing clips.

      Arranging clips in the Block View
      Arranging clips in the Block View is done in the same ways as when arranging clips in the Song View.
      !   Any clips, or parts of clips, to the right of the End Marker in the Block View will be ignored when the Block is
          played back in the Song View.
      Refer to “Arranging in the Sequencer”.

      Arranging Blocks in the Song View
      Once you are finished with your clips on the tracks and lanes in the Block View, it is time to arrange the Blocks to
      build up your song in the Song View. Setting up the Blocks and their playing order is done by creating Block Automa-
      tion Clips on the Blocks Track in the Song Arrange view.
      The following section describes functions and routines that are specific to Block Automation Clips. General clip han-
      dling procedures (e.g. naming, coloring etc.) are described in the general “Clip handling” section.

      Creating Block Automation Clips
      A Block Automation Clip is very similar to a Pattern Clip (for a Redrum device, for example). A Block Automation Clip
      defines which Block should play back, and for how long. To create Block Automation Clips, proceed as follows:
      1. Click the Song button to switch to the Song View.

                                                  Blocks Track

      2. Select the Pencil tool.
          The Block selector appears in the Inspector:

                                                                 Block Selector

      3. Select desired Block (1-32) from the Block Selector List.
          In this example, we will use Block 1.

      4. Draw a clip on the Blocks Track.
          This creates a Block Automation Clip which instructs the sequencer to play back the events you have previously
          recorded in Block 1:

                                                                       Block Automation Clip

                                                Block contents

          A Block Automation Clip drawn on the Blocks Track in the Song View.
          The contents (clips and events) of Block 1 are displayed on the respective sequencer tracks in a ghosted fashion
          on a colored background. This way you will see what events and/or recordings the Block will play back. This also
          allows for muting of individual lanes in the Block (see “Muting lanes in Block Automation Clips”).
          The following rules apply to Block Automation Clips:
      • If the Block Automation Clip is longer than the actual Block length (defined by the End Marker in the Block
        View), the Block is repeated over and over for as many times as necessary.
          In the picture above, the Block length is 8 bars and the Block Automation Clip is 20 bars. This means that Block 1
          is repeated at bars 9 and 17. The repetitions are indicated with thin vertical lines in the Block Automation Clip and
          on the sequencer tracks (similar to a Pattern Automation clip).
      • If the Block Automation Clip is shorter than an even multiple of the Block length, the remaining content of the
        Block is masked out (muted) in the Song View arrangement.
          In the picture above, the last 4 bars of the third repetition are masked out.
      D   If you want to add single Block Automation Clips, you can also double click with the Selection (Arrow) tool on
          the Blocks Track.
          The clip gets the length of the currently selected Snap value. To create longer clips, double click, hold and drag to
          the right.

      Resizing Block Automation Clips
      As with other clip types Block Automation Clips can be resized by clicking and dragging the clip handle(s) with the
      Selection (Arrow) tool or by editing the Position and Length values in the Inspector.
      • If you resize a Block Automation Clip by clicking and dragging its left clip handle, and thus changing its start
        position, the Block Offset will change.
          This means that the Block Automation Clip could start playing in the middle of the Block, i.e. not from the begin-
          ning. The picture below shows a Block Automation Clip before and after resizing the start position:

                                                                            Block Offset = 0

                                                                            Block Offset =
                                                                            -6 Bars

          Changing the start position by resizing a Block Automation Clip
          In the example above, the Block Automation Clip will begin playing at Bar 7, and will start playing back the events
          that begin at Bar 7 in the Block.
      • If a Block contains sequencer tracks that use Pattern Automation (a Redrum track, for example), a Block Offset
        will make the pattern start playing back from the correct position within the pattern and sound just as you
        would expect.

      Reassigning Blocks in Block Automation Clips
      D   To assign another Block to an existing Block Automation Clip, click the small triangle button on the Block Au-
          tomation Clip and select another Block from the drop-down list:

          The Block Automation Clip color changes to the color of the new Block and the ghosted clips on the tracks switch
          to show the contents of the new Block.

      Muting lanes in Block Automation Clips
      When you have arranged your Block Automation Clips as desired on the Blocks Track, it is possible to mute individual
      lanes contained in any Block. These lanes will remain muted until the end of the Block Automation Clip.
      This way you can use the same Block to create a song intro, by gradually introducing more and more sequencer
      tracks/lanes. The example below shows how to mute lanes in individual Block Automation Clips to create a song in-
      tro.
      We are going to use one single Block - Block 1 - to create a song intro. The Block is 8 bars long and uses four se-
      quencer tracks. In the Block View we have recorded on all four sequencer tracks:

                                                                  Clips recorded in
                                                                  the Block View

      Block 1 in the Block View with four sequencer tracks.
      Now, we want to arrange our song so we switch to the Song View and draw an 8 bar Block Automation Clip on the
      Blocks Track:

                                                              Block Automation Clip

                                                              The Block contents
                                                              in the Song View

      An 8 bar Block Automation Clip assigned to Block 1.
      In our intro we want the Piano and Bass track to play the first eight bars. In the next eight bars we want to have the
      drums playing as well. Then, we want the song to continue for another 16 bars with all tracks playing except the Pi-
      ano track.
      To achieve this, we need to create several Block Automation Clips that play back the same Block. This is because
      when we’re going to mute lanes later on, we need to define for how many bars we want the mutes to be active. The
      duration of the mutes are defined solely by the lengths of the Block Automation Clips.

      We begin by copying and pasting the Block Automation Clip twice. Then we resize (expand) the last Block Automa-
      tion Clip to 16 bars:

      The Block Automation Clip assigned to Block 1 copied and pasted twice, with the last Block Automation Clip resized to 16 bars.
      Now, we want to mute individual lanes for the duration of each Block Automation Clip to create our intro. We select
      the Mute tool from the Toolbar and click on the lanes we want to mute in each Block Automation Clip:

                                                                                               Muted lanes in each
                                                                                               Block Automation Clip

      Muted lanes throughout the length of each Block Automation Clip.
      Now, we have our intro with the Piano and Bass playing the first 8 bars. Then, the song continues for another 8 bars
      with Piano, Bass and Drums. Finally the song plays another 16 bars with Drums, Bass and Synth Pad. All we needed
      for this intro was one single 8 bar Block.
      !   Note that the lanes will be muted for the duration of each Block Automation Clip. If the Block contents are re-
          peated in the Block Automation Clip, as in the last clip above, the lane will be muted throughout the entire
          Block Automation Clip length. If you resize a Block Automation Clip, any muted lanes will be resized accord-
          ingly.

      Converting Block Automation Clips to Song Clips
      After you have arranged your Block Automation Clips in the Song View, you might want to convert the content of the
      Block(s) to “regular” clips on the sequencer tracks and lanes. There are a few ways of doing this:

      Converting single Block Automation Clips to clips in the Song View
      1. Choose the Block Automation Clip(s) you want to convert by selecting it on the Blocks Track.
      2. Select “Convert Block Automation to Song Clips” from the Edit menu or Block Clip context menu.
        All unmuted clips in the Block(s) are automatically converted to regular clips on the tracks. The Block Automation
        Clip and its contents are preserved and left unchanged:

                                                                                              Selected Block
                                                                                              Automation Clip

                                                                                              Converted Clips

        Before and after the “Convert Block Automation To Song Clips” command used on the first Block Automation Clip.

      Converting all Block Automation Clips to clips in the Song View
      D   Select “Convert Block Automation to Song Clips” from the Track List context menu.
          All unmuted clips in all Block Automation Clips are automatically converted to regular clips on the tracks. The
          Block Automation Clips and their referenced Block contents still are preserved but the Blocks Track is automati-
          cally muted. This is made to reduce the clutter on the arrangement pane:

                                                                                               Blocks Track automatically
                                                                                               muted

                                                                                                Converted Clips

          Before and after the “Convert Block Automation To Song Clips” command on the Track List context menu.
      D   If you want to activate the Blocks Track again, click the “M” button on the Blocks Track.

      Using Cut/Copy and Paste for individual clips
      You can of course also use the standard Cut/Copy & Paste functions to copy clips from the Block View to the Song
      View, and vice versa.
      1. Select the clip(s) on the arrangement pane (in Blocks or Song View).
      2. Use the standard Cut or Copy command.
      3. Switch to the other View (Song or Blocks)
      4. Use the Paste command.

      Combining Block Automation Clips with Song Clips
      It’s possible to combine Block Automation Clips with regular clips in the Song View. The general rule is that clips in
      the Song View have priority over Block data. This means that if a clip in the Song View overlaps a (ghosted) clip on
      the same lane in a Block, the Song Clip will play back and the clip in the Block “underneath” will be silent (masked):

                                                                                     Song Clips

      Song clips and Block Automation Clips in combination in the Song View.
      If we play back the song in the picture above, this is what we will hear:
      • In Bars 1-8 the song clips on the Piano and Bass tracks will play. Any Block data “underneath” these clips will
        be silent.
      • In Bars 9-16 the Block data for the Piano, Drums and Bass tracks will play back since there are no overlapping
        Song Clips.
      • In Bars 17-32 the Block data for the Drums, Bass and Synth Pad tracks will play back since there are no over-
        lapping Song Clips.

      Practical tips on combining Blocks and Song Clips
      A nice way of working with Block Automation Clips and Song Clips is to first create a couple of Blocks in the Block
      View and then arrange Block Automation Clips in the Song View. When you have arranged your Block Automation
      Clips, you could record a couple of shorter Song Clips with variations in the Song View. Then, place these short clips
      at desired positions in the arrangement to create nice variations in the song, according to the example below:

                                                                                           Basic arrangement with only
                                                                                           Block Automation Clips

                                                                                               Song Clips overlap to
                                                                                               create variations in
                                                                                               the arrangement

      Short Song Clips combined with Block Automation Clips in the Song View to create nice variations.
      q   Since Song Clips automatically mute (mask) the “underlying” Block data, short Song Clips are perfect for in-
          troducing temporary variations in a Block based song.

      About Performance Controllers and Parameter Automation
      Since the sequencer tracks and lanes are shared between the Blocks and the Song arrangement, the following rules
      apply regarding Performance Controller and Parameter Automation:
      • Performance Controller and Parameter Automation data in the Song View arrangement always overrides auto-
        mation in Blocks.
      • If a sequencer track uses Parameter Automation in the Block, the automation will also affect all clips on the
        corresponding lanes in the Song View.
        The picture below shows a piece of an arrangement with an instrument track which has one note lane and one pa-
        rameter automation lane. The arrangement is built up by Blocks (the ghosted data) and one short Song Clip for
        variation in bars 28 through 29 (the blue clip on the note lane). The Block uses Mod Wheel Performance Control-
        ler automation (the gray line inside the note clips in the Block) and automation of the Rotary 4 parameter (the gray
        line in the parameter automation clips in the Block):

      • The song only plays Block data from the start to bar 28.
        During this time, the Rotary 4 automation is active. (However, no notes are played back in bars 1 through 16 since
        the note lane in the Block is muted.)
      • At bar 17 the note lane is played back together with the Mod Wheel Performance Controller data in the Block.
        The Rotary 4 automation is still active.
      • At bar 28 the (blue) Song Clip takes over the note playback and Mod Wheel Performance Controller automa-
        tion.
        Since the Mod Wheel isn’t touched at all in the Song Clip, its value is set to zero. However, note that the Song Clip
        is still affected by the Rotary 4 automation in the Block!
      • At bar 30 the note clip in the Block takes over again and controls note playback and Mod Wheel Performance
        Controller automation.
        The Rotary 4 automation is still active.

326   WORKING WITH BLOCKS IN THE SEQUENCER


---

<a id="working-with-the-rack-11"></a>

=== END OF PART ===
