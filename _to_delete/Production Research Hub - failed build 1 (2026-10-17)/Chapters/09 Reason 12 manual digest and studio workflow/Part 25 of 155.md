# Chapter 09: Reason 12 manual digest and studio workflow
## Part 25 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 16 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 26 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 16 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Using Cut/Copy and Paste to repeat clips
      When you cut or copy clips, the song position will automatically move to the end of the selection (or, if Snap is acti-
      vated, to the closest Snap value position after the end of the longest clip). This allows you to quickly repeat a section
      of clips in the following way:
      1. Make sure the sequencer is stopped.
      2. Activate Snap (see “Snap”) and set the Snap value to “Bar” (or to the length of the section you want to repeat).
      3. Select the clips you want to repeat.
          Since you can select clips on several tracks , this is a quick way to copy entire song sections.
      4. Select “Copy” from the Edit menu or context menu, or hold down [Ctrl](Win) or [Cmd](Mac) and press [C].
          The song position is moved to the closest snap value after the end of the longest clip in the selection (provided
          that the sequencer is stopped).
      5. Select “Paste” from the Edit menu, or hold down [Ctrl](Win) or [Cmd](Mac) and press [V].
          The copied section is pasted in, and the song position is moved to the end of pasted selection.
      6. Paste again, as many times as you want to repeat the selection.

      Naming clips
      1. You can name an individual clip by selecting it and then selecting “Add Labels to Clips” from the Edit menu or
         context menu.
          A text field is opened.
      2. Type in a name for the clip and then press [Return].
      When adding labels to several selected clips in one go, they will all receive generic names according to the clip type
      (e.g. “untitled note clip”). Double-clicking on a label in a clip opens the text field where you can type in the label text.

      Renaming clips
      D   To rename a clip, double-click on the label, type in a new name and press [Return].

      Removing labels from clips
      D   To remove labels from clips, select them and choose “Remove Labels From Clips” from the Edit menu or con-
          text menu.
          Alternatively, double-click on the clip label, press [Backspace] or [Delete] and then press [Return].

      Coloring clips
      By default Clips are set to "Use Track Color", and will have the same color as their tracks. You can override this by
      selecting individual colors from the Clip Color submenu.
      D   Select “Clip Color” from the Edit menu or the context menu and then choose a color from the palette on the
          sub-menu.
          All selected clips will be colored according to the selected color. If you record new clips on the lane, they will be
          colored according to the set track color.

      Splitting clips
      You can split clips using the Razor Tool in Arrange Mode. To split a single clip, proceed as follows:
      1. Select the Razor Tool and place it where you want to split the clip.
          On the Razor Tool’s left edge is a cross-hair which indicates where the split will take place. If activated, the Snap
          setting is taken into account (see “Snap”).

      2. Click with the Razor Tool to split the clip at the cross-hair’s position.
          The clip is now split into two separate clips.

          A vertical line appears where the clip is split.
      !   Recordings and events in a split clip will always remain intact, e.g. notes in a note clip will not be split even if
          they span over the split point.
      It’s also possible to split clips on all tracks in a song:
      1. Place the Razor Tool’s cross-hair on the Ruler where you want to split the clips on all tracks and lanes of the
         song.
      2. Click in the Ruler to split the clips on all tracks and lanes at the current position.
          Clips on tracks and lanes - including tracks and lanes that might not be visible - on the Arrange Pane will also be
          split.
      You can also cut out a section of one or several clips in one go to:
      1. Place the Razor Tool on the Arrange Pane background close to where you want to split the clips.
      2. Click and drag with the Razor Tool to select the split section - on one or several lanes.

      3. Release the mouse button to split the clips.

      If you want to “cut” out a section of all clips on all tracks in the song, this can be done as follows:
      1. Place the Razor Tool’s cross-hair on the Ruler where you want to split the clips on all tracks of the song.

      2. Click and drag the Razor Tool in either direction on the Ruler to make a range selection.
      3. Release the mouse button to split the clips on all tracks and lanes in the song.
      !   Clips on tracks and lanes that might be scrolled out of view on the Arrange Pane will also be split.

      Duplicating a part of one or several clips
      By using either of the methods described above, it’s also possible to duplicate the “split” section of the clip(s) and
      then move them to a new destination. Here’s how:
      D   With the Razor Tool selected, hold down [Ctrl](Win) or [Cmd](Mac) and drag to create a duplicate of the “cut
          out” section of the clip(s). Then, use the Selection Tool to move the duplicated clip(s) to a new destination.
          The original clips will remain uncut, just as they were before the operation.

      Crossfading audio clips
      When two audio clips have overlapping edges, it’s possible to add a crossfade in the overlap area. By “crossfade” we
      mean “crossfade to previous clip”.
      1. Drag one of the audio clips so that it overlaps the edge of the other audio clip:

          Moving the last (orange) clip....

          ...so that it partly overlaps the first (green) clip.
      2. Press [X] or right click the last (orange) clip and select "Crossfade" from the bottom of the context menu.
          The overlap area is now crossfaded, as shown by the white crossfade curves:

      3. You can adjust the crossfade zone by clicking on either edge of the crossfade zone and drag sideways:
          This actually resizes the clips; adjusting the left edge changes the start of the orange clip and adjusting the right
          edge changes the end of the green clip.

          Adjusting the right edge of the crossfade zone.
      4. You can also change the crossfade symmetry by clicking the crossfade curve and dragging sideways:

          Adjusting the crossfade symmetry.
      D   To remove a crossfade, select the last (orange) clip and press [X] - or deselect Crossfade from the context
          menu:

      Joining clips
      Separate clips on the same lane can be joined into one clip. You can also join clips that aren’t directly adjacent on the
      lane, or clips that overlap each other.
      1. Select the clips you wish to join.

      2. Select “Join Clips” from the Edit menu or from the clip context menu. Alternatively, hold down [Ctrl](Win) or
         [Cmd](Mac) and press [J].

          A single clip is created. If there was a gap between the clips before the operation, this area will be empty - the
          original positions of all events in the original clips will be preserved in the joined clip.
      • Only clips on the same lane can be joined.
          It’s possible to select several clips on several lanes, but only selected clips on the same lanes will be joined.
      • You can also join selected clips that have other non-selected clips in-between them.
          The non-selected clips in-between will then overlap and mask the joined clip at their current positions.
      !   If you join note or parameter automation clips that contain masked events in the area(s) between the clips, the
          masked events will be permanently deleted! This is to make the resulting clip play back the same as the origi-
          nal clips did before joining. (See “Masked events in note and parameter automation clips”).

      !     If you join overlapping note or parameter automation clips, the events in the clip which lies on top will replace
            and permanently delete the events in the overlapped region of the “hidden” clip.

      About joining audio clips
      Joining audio clips basically works in the same way as joining note and parameter automation clips - except when it
      comes to joining overlapping audio clips. What happens if you join overlapping audio clips is that the clips will be
      placed on separate Comp Rows - and be automatically comped to a “final” clip. No recording will be deleted. Let’s
      have a look at the example in the picture below:

          The original audio clip (blue) with an overlapping            The two audio clips joined into a single
          audio clip (yellow) selected in Arrange Mode.                 audio clip in Arrange Mode.

                                            The “joined” clip
                        Masked part of the original clip

                                             The original clip
                                       The overlapping clip

                                                                 The “joined” audio clip open in the Comp Editor.

      As you can see, the entire audio recording in the original clip is preserved - only masked where the overlapping clip
      is located. If you change your mind afterwards, you will still be able to access the entire original recording.
      • If overlapping clips have different Clip Levels, the Comp Row Levels will change to these levels after joining.
            The Clip Level in the joined clip will be set to -0 dB.
      • If overlapping clips use Fade In and/or Fade Out and the clips overlap in the Fade In/Out area(s), the Fade(s)
        will be removed after joining.
            Also, if you join audio clips that aren’t directly adjacent, any Fade Out in the first clip and Fade In in the second clip
            will be removed.
      • Any Cut Crossfades used in comped audio clips will be preserved after the joining.

      About joining crossfaded audio clips
      If audio clips you are joining have a crossfade between them, this is what happens:
      1. Select the two crossfaded clips:

      2. Select “Join Clips” from the Edit menu or from the clip context menu. Alternatively, hold down [Ctrl](Win) or
         [Cmd](Mac) and press [J].
            The “joined” clip shows up on the track:

      3. Double click the clip to open it in Comp Edit Mode:

                                                                                       The “joined” clip

                                                                                       Masked part of the
                                                                                       first (green) clip
                                                                                        The crossfade zone

                                                                                       Masked part of the
                                                                                       last (orange) clip

          As you can see, the crossfade zone has been automatically bounced to a new recording on a separate Comp Row.
      !   Note that even though we joined two mono audio clips, the resulting audio clip automatically becomes stereo
          (with two identical mono audio “channels”). This happens by default when crossfaded audio clips are
          bounced, but does not affect the audible result.

      Reversing clips
      It’s also possible to reverse clips, i.e. play the content of the clip “backwards” (from the end to the start). This works a
      little differently for audio clips and note clips. Please refer to “Reverse” for information about reversing note and au-
      tomation clips, and to “Reversing audio clips” for information about reversing audio clips.

      Muting clips
      Clips can be muted as follows:
      D   Select the Mute Tool from the Toolbar and click on the clips you want to mute.

          Muted clips are indicated with gray stripes, borders and events:

          Muted clips.
      D   Select the clips and then select “Mute Clips” from the Edit menu or from the clip context menu. Alternatively,
          select the clips and press [M] on the computer keyboard to mute them.

      Unmuting clips
      Muted clips can be unmuted as follows:
      D   Click on muted clips with the Mute Tool.
      D   Select muted clips with the Arrow Tool and select “Unmute Clips” from the Edit menu or context menu - or
          press [M].
      !   Muted clips cannot be joined with other clips.
      !   Muted note clips will not be included when using the “Merge Note Lanes on Tracks” function described in the
          “Merging clips on note lanes” section.

      Merging clips on note lanes
      Several note lanes on a track can be merged into a single note lane:
      1. Select the track with the note lanes you wish to merge.

          A selected instrument track with separate note lanes.
      2. Select “Merge Note Lanes on Tracks” from the Edit menu or from the context menu.
          The clips on all note lanes will be merged on the topmost note lane.

          The same instrument track after merging.
      • If there are time gaps between the clips on the lanes, several clips will be created on the merged note lane.
      • Muted note lanes or muted clips on the track will not be included in the merge.
      • It’s also possible to select several tracks and merge the note lanes on each individual track, all in one go.

      Bounce in Place
      The Bounce in Place function lets you bounce the sound generated from playing back note or audio clips, with any in-
      sert effects and channel strip coloration - but without Send FX and Master Section settings - to a new audio clip on
      a new audio track. The Bounce in Place function is mainly intended for creative audio work, for example:
      • creating audio clips out of note clips, that you could then manipulate the slices in - or cut up.
      • creating audio clips out of note (or audio) clips - with the sound from any effects included.
      • creating audio clips out of note clips that you could then reverse (see “Reversing clips”).
          This is great for reverberated drum hits or vocals etc. that you could then play backwards for interesting effects.
      • for creating audio clips that you could use as samples in any sample player device (see “Bounce Clip(s) to New
        Sample(s)”) or as REX loops in the Dr Octo Rex (see “Bounce Clip to REX Loop”).
      q   If you want to bounce entire tracks to audio, use the Bounce Mixer Channels function instead. See “Bouncing
          Mixer Channels”.
      !   Note that if you bounce audio clips that are in mono, the bounced clip will be in stereo because the bounce is
          post-pan on the channel strip. Thus, if a mono channel is panned left or right, the two channels will not be iden-
          tical. Also, even though the audio clip is in mono, there may be insert fx turning the channel to stereo.

      Here is an example of how you can use the Bounce in Place function:
      1. Select the clip you want to bounce.
          In this example we choose a note clip on an ID8 instrument track:

      2. Select “Bounce in Place” from the context menu (or Edit menu). (If you bounce an audio clip, select “Bounce >
         Bounce in Place” instead).
          A new audio clip is created on a new audio track, colored and named according to the original track - with the ad-
          dition of the word “Bounced” in the destination track name. The destination track inherits the settings from the
          source track, i.e. mixer settings and any Output Bus routing.

          The bounced audio clip always has the same position and length as the original source clip.
          Note also that the source clip is automatically muted.
      3. If the source clip generated any sustaining (or reverberating) audio, this might be masked in the bounced au-
         dio clip. To reveal any audio tail, just resize (expand) the bounced clip:

          Expand the bounced audio clip to reveal any sustaining audio tail.
      • Similarly, if a note clip should contain any notes that extend to the right outside the clip boundary, the audio
        from the notes will be bounced to the new audio clip in its entirety.
          The audio from the extended note(s) will be masked in the audio clip, so you will have to expand the bounced au-
          dio clip to hear the complete rendering.
      !   The maximum length of any sustaining/reverberating “tail” in the bounced clip is automatically limited to 5
          seconds after the last “note off” in the original note clip - or 5 seconds after the end of an audio clip.
      • Completely masked notes in a source clip will not be rendered to audio - only the notes you can hear.
      • Any parameter automation of the source device that affects the audio are also taken into account when bounc-
        ing.
          This means that what you heard when you played back the source track is exactly what you will hear when you
          play back the bounced clip on the destination track.

      Bouncing multiple clips
      If you have selected multiple clips to “Bounce in Place”, this is what happens:
      • Clips that are on the same source track will result in bounced clips on the same destination track.
      • If the clips are on different source tracks, the bounced clips will be on separate, new destination tracks.

      Bouncing overlapping clips
      If you have selected multiple overlapping clips to “Bounce in Place”, this is what happens:
      • The separate ranges for each of the source clips are bounced. The bounced clips are then placed overlapping
        in the same way on the destination track.

      Bouncing clips on instrument tracks that use several Mix Channels
      • If you want to bounce a note clip for an instrument that uses separate Mix Channels (e.g. individual outputs of
        an instrument device connected to separate Mix Channels), a separate audio track will be created for each
        used Mix Channel.
        On each of these audio tracks there will be a separate audio clip rendered from each of the Mix Channels.

      About tracks with no Mix Channel of their own
      • If a track's device is not connected to its own separate Mix Channel, the Bounce in Place function will be dis-
        abled.
        For example, if an instrument device is connected to a Mixer 14:2, which has other instrument devices connected
        to it, and then routed to a single Mix Channel device, there's no obvious way to isolate the audio from a single in-
        strument device (since other devices connected to the Mixer 14:2 might be playing as well). Thus, the Bounce in
        Place function will be disabled.

      Matching clips using the “Match Values” function

      The “Match Value” function in the Inspector can be used for matching the positions or lengths of several selected
      clips to the position and/or length of the topmost selected clip (or leftmost if the clips are on the same lane).

      Matching clip positions
      To match clip positions:
      1. Select a couple of clips on the Arrange Pane.
      2. Click the “Match Values” button to the right of the Position display to move all selected clips to the start posi-
         tion of the topmost clip - or leftmost clip, if the clips are on the same lane.

          All selected clips are moved to the start position of the topmost selected clip.
      !   Note: If you match the position of several clips on the same lane, they will all start at the same position, and
          thus overlap.

      Matching clip lengths
      Another Match Value function in the Inspector can be used to match the lengths of several selected clips to the
      length of the topmost (or leftmost if on the same lane) selected clip:
      1. Select a couple of clips on the Arrange Pane.
      2. Click the “Match Values” button to the right of the Length display to resize all selected clips to the length of
         the topmost clip - or leftmost clip, if the clips are on the same lane.

        All selected clips are resized to a length of 6 bars - the same as the topmost selected clip.

      Matching audio clip levels, fades and transposition
      In addition to Position and Length matching, audio clips can have their Fades, Levels and Transpose values matched:
      1. In Arrange Mode, select a couple of audio clips.
      2. Click the “Match Values” buttons to the right of the respective displays to match to the values of the topmost
         clip - or leftmost clip if the clips are on the same lane.

        After having clicked the Match Values buttons, all selected audio clips get the same values as the topmost se-
        lected audio clip.

      Inserting bars
      The “Insert Bars Between Locators” function on the Edit menu, or context menu, can be used for inserting empty bars
      between the Left and Right Locators. All clips that intersect the locator positions on all tracks after the Left Locator
      are split and moved to the Right Locator to make room for the inserted bars.

      Different tracks with lanes before and after insertion of 4 extra bars between bars 13-17.

      Removing bars
      The “Remove Bars Between Locators” function on the Edit menu, or context menu, removes all events between the
      Left and Right Locators. All clips that intersect the locator positions will be cut (when necessary), and the cut section
      (between the locators) will be removed. All clips that originally were located to the right of the Right Locator will then
      be moved to the Left Locator, closing the gap.

      Different tracks with lanes before and after removal of 4 bars starting at bar 13.
      !   Any removed note and parameter automation events between the Left and Right Locators will be deleted!

      About removing bars that contain audio recordings
      As opposed to note and parameter automation events, audio recordings in removed bars will not be deleted. Instead,
      they will be placed on a Comp Row and masked. If we open the second audio clip in the previous example in Edit
      Mode, we can see that the audio recording in the removed bars has been moved forward and masked:

                                                                         The audio clip in the Comp Editor after
                                                                         removal of four bars.

                                                                     “Removed” recording moved forward
      The audio clip in Song View before and after removal of four   on the Comp Row and masked
      bars (yellow frame) between the locators.

202   ARRANGING IN THE SEQUENCER


---

<a id="audio-editing-in-the-sequencer-8"></a>

=== END OF PART ===
