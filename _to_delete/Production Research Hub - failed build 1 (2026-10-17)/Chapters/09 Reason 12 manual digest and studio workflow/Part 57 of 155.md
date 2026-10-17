# Chapter 09: Reason 12 manual digest and studio workflow
## Part 57 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 48 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 58 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 48 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 22: The ReGroove Mixer

The ReGroove Mixer

      Introduction

      The ReGroove Mixer combines all the benefits of quantization, shuffle, and groove templates into a single integrated
      environment, giving you real-time creative control over the feel and timing of individual note lanes. The ReGroove
      Mixer, which extends from the top of the Transport Panel puts 32 channels of interactive groove control at your fin-
      gertips.
      If you're familiar with mixing, you're already well on your way toward understanding the ReGroove Mixer. Think of it as
      a mixer with 32 busses but, instead of these busses modifying the volume of the input tracks, they modify the feel (or
      groove) of the input tracks. You can route any note lane to one of ReGroove's 32 channels, and that lane's feel and
      timing are modified, in real-time, by the channel's settings. Each ReGroove channel can use its own groove template
      or shuffle amount. In addition, each channel can slide notes forward or backward in time, allowing you to put certain
      tracks slightly ahead or behind the beat, which greatly alters the feel of your music.
      !   Note that ReGroove only works for notes on note lanes.
      q   It’s also possible to lock a control surface to control the ReGroove Mixer parameters via Remote - see “Lock-
          ing a surface”.

      ReGroove basics
      When working with grooves, you'll make use of three interacting sections within Reason's interface:
      • First, in the Sequencer, each note lane can be assigned to any of ReGroove's 32 channels.
          You assign a note lane to a groove channel by selecting it with the Select Groove pop-up in each note lane.

      • Second is the ReGroove Mixer, which contains both global groove settings and channel-specific ones.
          This is described on the following pages.

      • Finally, there's the Groove Settings section of the Tool Window, which is accessed by clicking a ReGroove
        channel's Edit button.
          Groove Settings allow you to set the intensity of various groove patch parameters. This is also where you save your
          own ReGroove patches. See “Groove Settings”.

      The ReGroove Mixer
      D   Open the ReGroove Mixer by clicking the Groove button to the left on the Transport Panel.

      The ReGroove mixer is divided into two sections. On the left are the Global parameters, and on the right are the
      Channel parameters.

                 Global parameters

                                                               Channel parameters

      Global parameters

      These parameters operate globally, rather than channel-by-channel.

      Channel Banks
      The ReGroove mixer consists of 32 channels, grouped into 4 banks (labeled A through D). Click a Channel Bank but-
      ton to see and edit its corresponding bank of 8 channels.

      Anchor Point
      Normally, all groove patterns start at Bar 1 and repeat themselves throughout a song. For example, a 4-bar groove
      pattern will begin at Bar 1 and repeat its pattern every four bars. Many times, however, songs begin with blank mea-
      sures, pickup measure or, perhaps, a short introduction. In these cases, you probably don't want the groove pattern to
      begin at Bar 1, but at some later bar. This is the purpose of the anchor point - it tells Reason at which measure it
      should begin applying the groove settings.
      For example, assume you have a song with a 1-bar pickup. Because the song really begins on bar 2, that's where you
      want your groove to begin. Setting the anchor point to 2 insures that the groove patterns all begin at measure 2.
      D   Note: There is one exception to the rule that grooves start playing at their anchor point and repeat indefinitely
          throughout the song-and that's when they encounter a time-signature change. Grooves always restart at any
          measure containing a time signature change.
          You can use this knowledge if, for example, you have a song section with an odd number of bars-inserting a time
          signature change will force all your grooves to restart at that measure.

      Global Shuffle
      This knob adjusts Reason's global shuffle amount, and is used by any devices that employ patterns, such as the Dual
      Arpeggiator Player device, Redrum's internal sequencer, the Matrix pattern sequencer, and the RPG-8 arpeggiator. It
      also defines the shuffle value for any ReGroove channel for which the Global Shuffle option is activated.
      Setting the Global Shuffle to a value of 50% results in a “straight” beat, with no swing applied. Setting the Global
      Shuffle to a value of 66% results in a perfect sixteenth-note triplet shuffle. Values between 50% and 66% have a
      less pronounced swing feel, and values greater than 66% are more exaggerated.
      • If you are quantizing notes and/or audio Slices to “Shuffle” in the “Quantize” section in the Tool Window,
        these are quantized to the current Global Shuffle value.

      Channel parameters
                  On button
                      Edit button

                               Channel number

                               Groove patch name
                               Groove patch browser button

                                Slide knob

                                Groove Amount slider
                                Shuffle knob

                                Pre-align button

                                Global Shuffle button

      These parameters operate on a per-channel basis. Each of ReGroove's 32 channels (arranged in 4 banks of eight)
      contains an identical set of parameters.

      On Button
      This is an On/Bypass button for the channel. When the button is lit, the groove channel is active and any note lane
      assigned to this groove channel will be affected. When the button is not lit, the channel is disabled and any note lanes
      assigned to this groove channel will play back straight, without being “grooved.”
      q   This can be used for comparing the groove with the original, ungrooved beat. You can also do this for individ-
          ual note lanes, by turning off the “Enabled” item on the Groove Select pop-up menu in the track list - see “Ap-
          plying grooves to your music”.

      Edit Button
      Click this button to open Reason's floating Tool Window, and show the Groove tab, where you can view and edit ad-
      ditional “Groove Settings” for each channel.
      Each ReGroove channel has its own groove settings, so clicking the Edit button in different channels will fill the Tool
      Window with groove settings specific to that channel.

      Channel Number
      This is a non-editable channel number label. Channels are numbered 1-8 and are grouped into 4 banks (A-D). Chan-
      nel numbers are named accordingly. For example, A2 is the second channel in Bank A, and B5 is the fifth channel in
      Bank B.

      Groove Patch Name
      This shows the name of the groove patch currently loaded into the channel. If no groove patch is loaded, then no
      name appears. Click this area to bring up a list of the patches in the current folder, just as with patch displays on de-
      vices in the Reason rack.

      D   To remove a groove patch assignment and reset the channel to its default values, right-click (Win) or [Ctrl]-
          click (Mac) the Groove Patch name, or anywhere on the ReGroove panel background, and select “Initialize
          Channel” from the context menu.

      Groove Patch Browser
      This allows you to load groove patches and to step between them, just like device patches in the Reason rack. Re-
      Groove patches have a .grov extension. See “ReGroove patches in the Factory Sounds bank”, later in this chapter, to
      learn more about the types of groove patches included with Reason.

      Slide
      Use this knob to slide notes forward or backward in time. Musicians will frequently add energy and urgency to a track
      by “rushing” a particular beat or instrument a little. Similarly, they may “drag” a note a little in order to create a more
      laid back, shuffle-like feel. The Slide knob has a range of ±120 ticks, which allows you to slide notes up to a thirty-
      second note in either direction. Setting negative values makes notes play earlier in time (rushing the feel). Setting
      positive values makes notes play later in time (lagging the feel).

                                       With Slide set to +20 ticks, notes play
                                       back later in time.

                                      With Slide set to 0 ticks, notes are not
                                      shifted in time.

                                     With Slide set to –20 ticks, notes play
                                     back earlier in time.

      For example, if you wanted to create a slightly “in the pocket” groove, you could create a snare lane and assign it to
      a ReGroove channel with a small amount of positive slide. This would delay the snare track slightly, giving your music
      a relaxed, laid back feel.
      q   If you have a track that you want to rush (set to a negative slide value), you should put an empty bar at the be-
          ginning of your sequence, making sure to set the Anchor Point to “2” (see “Anchor Point”). This insures that
          any notes assigned to Bar 1/Beat 1 will indeed play ahead of the beat (since you created an empty measure
          into which the early note can shift).

      Shuffle
      At its most basic level, this knob adds a sixteenth note “swing” feel to the ReGroove channel. A value of 50% results
      in a straight (no shuffle) feel, and a value of 66% creates a perfect triplet feel.

                                                                        Shuffle works by changing the start
                                                                        time of every other sixteenth note.

                                                                         A shuffle value of 66% delays every
                                                                         other sixteenth note to create a perfect
                                                                         triplet feel.

      You can also use this knob to “de-shuffle” a beat by dialing in values below 50%. For example, if you had a recording
      that was played with a perfect triplet feel, setting the Shuffle value to 34% will make the beat straight again!

      Groove Amount
      Use this fader to adjust how intensely the selected groove patch will modify your notes. At 0%, the groove patch will
      have no effect. At 100%, the groove patch will have its maximum effect. Obviously, values between these extremes
      will produce some amount of groove effect, but less than maximum.
      As discussed in “Groove Settings”, later in this chapter, several additional parameters are associated with groove
      patches and how they modify your notes. Specifically, the Groove Settings section of the Tool Window contains four
      “impact” settings (timing, velocity, note length, and randomness), and the Groove Amount fader acts like a “master”
      fader that scales these four parameters proportionally.

                                                                           A Groove Amount of 100%
                                                                           modifies notes using all
                                                                           groove settings at their
                                                                           specified amounts.

                                                                           A Groove Amount of 50%
                                                                           modifies notes using all groove
                                                                           settings at only half their
                                                                           specified amounts.

      Pre-Align
      Enabling this button causes any incoming notes to be quantized to a rigid, sixteenth note grid prior to having any ad-
      ditional groove modifications applied to them. This quantization, which occurs in real time and is non-destructive, is an
      easy way to align all incoming notes to a “straight” grid, so that any shuffle, slide, or groove modifications have the ex-
      pected effect on the notes.

      Global Shuffle
      Enabling this button causes the ReGroove channel to use the “Global Shuffle” setting, rather than the channel's own
      shuffle setting. The channel's Shuffle knob will have no effect when a channel uses global shuffle. Using global shuf-
      fle is a good way to synchronize notes in a particular channel with those in pattern-based devices, such as Redrum’s
      internal sequencer, the Matrix pattern sequencer, and the RPG-8 arpeggiator, all of which get their shuffle values
      from the Global Shuffle value.

      Copy, Paste and Initialize ReGroove channels
      To copy one ReGroove channel configuration into another:
      1. Decide which ReGroove channel you want to copy from, then right-click (Win) or [Ctrl]-click (Mac) on the
         Groove Patch Name (or anywhere else in that channel, except directly on a parameter).
        A context menu appears.

      2. Select “Copy Channel” from the context menu.
      3. Right-click (Win) or [Ctrl]-click (Mac) on the destination channel's Groove Patch Name, then select “Paste
         Channel” from the context menu.
        Reason copies all the ReGroove channel settings to this channel.
      To initialize a ReGroove channel:
      1. Right-click (Win) or [Ctrl]-click (Mac) on the Groove Patch Name (or anywhere else in that channel, except di-
         rectly on a parameter) to open a context menu.
      2. Select “Initialize Channel” from the context menu.
        Reason resets all channel parameters to their default values.

      Groove Settings

      A groove patch consists of a groove template, which contains timing and dynamics information extracted from a per-
      formance, plus a collection of Impact parameters, which determine how strongly the groove patch applies the tem-
      plate settings. This section discusses the settings on the Groove tab in the Tool window, which is where all the
      Groove Patch settings are viewed and edited.

      Groove channel
      The Groove Settings display one mixer channel at a time. To select which ReGroove channel is currently displayed,
      select it from this pop-up (or click the Edit button for the channel in the ReGroove Mixer).

      Groove patch name
      This shows the name of the groove patch currently loaded into the channel. If no groove patch is loaded, then no
      name appears. Click this area to bring up a list of the patches in the current folder, just as with device patches in the
      Reason rack. This area duplicates the functionality of the Groove Patch Name area in each channel of the ReGroove
      Mixer.

      Groove patch Load/Save
      These buttons allow you to load and/or save groove patches, just like device patches in the Reason rack. ReGroove
      patches have a .grov extension. To learn more about the types of groove patches included with Reason, see “Re-
      Groove patches in the Factory Sounds bank”.

      Groove patch Length
      This displays the groove's length, which is import for determining how often the groove repeats.
      D   In general, if you apply different groove patches to different note lanes, you'll want their lengths to be multi-
          ples of one another.
          For example, if one ReGroove channel uses a 4-bar groove, you might want to use 4-bar grooves on other chan-
          nels or, perhaps, a multiple (such as 1-bar, 2-bar, or 8-bar grooves).
          You can, of course, mix and match grooves with non-standard lengths, but you need to be aware of how these
          grooves will interact. For example, if one channel used a 3-bar groove and another used a 4-bar groove, the groove
          pattern would actually repeat every 12 bars (3-bars times 4-bars).

      Groove patch Time signature
      This displays the groove's time signature and should, in most cases, match the time signature of your sequence.
      D   In general, if you apply different groove patches to different note lanes, you'll want them to share a common
          time signature.
          You can, of course, mix and match time signatures to create polyrhythmic grooves, but you need to be aware of
          how these grooves interact. For example a 6/8 groove will shift notes in a radically different way than a 4/4
          groove, so applying them simultaneously may or may not sound the way you expect.

      Timing impact
      This determines the extent to which timing information embedded in the groove template affects the position of your
      notes. A 50% setting means that notes are moved halfway to the positions defined in the groove template. 100%
      means they are moved exactly to the positions in the groove, and 200% means they are moved just as far past the
      groove template positions.

                                                             These are the original notes in your sequence.

                                                             These are note locations stored in a groove template. A
                                                             Timing Impact = 100% moves your original notes to
                                                             this location.
                                                             A Timing Impact = 50% moves your original notes
                                                             only halfway to the template's note location.

      D   This parameter works in conjunction with the ReGroove Mixer's Groove Amount fader, which can scale back
          the groove's timing impact.
          For example, if the Groove Amount fader is set to 100%, then notes are moved by the indicated Timing Impact
          amount, but if the Groove Amount fader is set to 50%, then notes are moved by only half the Timing Impact
          amount.

      Velocity impact
      This determines the extent to which velocity information embedded in the groove template affects the velocity of your
      notes. Grooves modify only the relative differences between note velocities, not their absolute values. This way, soft
      passages remain soft and loud passages remain loud-the groove simply accents the notes differently. A 100% set-
      ting means that the feel is more or less exactly transferred from the template to your music. Values below this mean
      that less of the groove's dynamics affect your notes, and values above 100% dramatically increase the dynamic ef-
      fect of the groove patch.
      D   This parameter works in conjunction with the ReGroove Mixer's Groove Amount fader, which can scale back
          the groove's velocity impact.
          For example, if the Groove Amount fader is set to 100%, then velocities are modified by the indicated Velocity Im-
          pact amount, but if the Groove Amount fader is set to 50%, then velocities are modified by only half the Velocity
          Impact amount.

      Note length impact
      This determines the extent to which note length information embedded in the groove template affects the length of
      your notes. This setting is not always relevant (such as with drum samples, which always play at their full length) and,
      consequently, most grooves in the Factory Sounds bank do not contain any length information (with the exception of
      the “Bass-Comp” category).
      That said, when working with sustaining instruments, note length can have a dramatic impact on the performance's
      feel. Grooves modify only the relative differences between note lengths, not their absolute values. This way, legato or
      staccato passages retain some of their original intent when modified with a groove patch.
      D   This parameter works in conjunction with the ReGroove Mixer's Groove Amount fader, which can scale back
          the groove's note length impact.
          For example, if the Groove Amount fader is set to 100%, then note lengths are modified by the indicated Note
          Length Impact amount, but if the Groove Amount fader is set to 50%, then note lengths are modified by only half
          the Note Length Impact amount.

      Random timing
      This determines the extent to which note positions are randomized. This value defines the maximum distance that a
      note can be randomly shifted (in either a positive or negative direction). You may set an amount between 0 ticks (no
      randomization occurs) and 120 ticks, which allows notes to shift as much as a thirty-second note in either direction.
      The effect is “polyphonic,” meaning that any notes originally beginning at the same position will still be moved by dif-
      ferent amounts. It is also “semi-deterministic,” meaning that if you play a clip several times, without editing anything,
      all notes will play back at exactly the same positions each time. However, as soon as you edit the clip in any way, all
      random positions are recalculated.
      D   This parameter works in conjunction with the ReGroove Mixer's Groove Amount fader, which can scale back
          the randomization.
          For example, if the Groove Amount fader is set to 100%, then notes are randomized by the indicated Random Tim-
          ing amount, but if the Groove Amount fader is set to 50%, then notes are randomized by only half the Random
          Timing amount.

      Get from clip
      This button converts the notes in a selected clip into a groove patch. The patch can then be used right away in the ac-
      tive ReGroove Mixer Channel or saved to disk as a new groove patch. Clicking this button has the same effect as se-
      lecting a clip and choosing “Get Groove From Clip” from the Edit (or context) menu. See “Creating your own
      ReGroove patches”.

      Working with grooves
      Applying grooves to your music
      Follow this example to learn basic ReGroove mixing techniques and hear the effect that various groove parameters
      have on your music.
      1. If it's not already visible in either the Sequencer or Rack, open the ReGroove Mixer by clicking the Groove but-
         ton to the left on the Transport Panel in the Sequencer.

      2. Decide which note lane you are going to apply the groove to.
          For the most obvious effect the track should contain a drumbeat based on straight (as opposed to shuffled) six-
          teenth notes. A hi-hat lane, for example, might be a good source for experimentation.
      3. Use the Groove Select pop-up on the chosen note lane to route those notes to a specific ReGroove mixer chan-
         nel.
                                                          Groove Select pop-up

      D   The “Enabled” item at the top of the pop-up menu allows you to turn ReGroove off for individual note lanes.
          This is useful for comparing with the original, ungrooved beat. If you want to do this for several note lanes set to a
          particular ReGroove channel, use the “On” button for the channel in the ReGroove mixer instead (see “On Button”).
      D   To turn ReGroove off for a note lane, select “No Channel”.
      4. In the ReGroove Mixer, make sure the channel you are using is activated - the On button should be lit.

      5. To hear some of the different possibilities, start by turning up the channel's Shuffle knob while you play the se-
         quence.

          The music on that note lane (and any other note lane assigned to the same ReGroove channel) will start playing
          with a shuffle feel.
      6. Turn down Shuffle to its middle position (50%), and turn up the channel's Slide knob to hear its effect.

      D   Note that, because slide shifts all notes by the same amount, you won't hear the results unless you play the
          track in conjunction with another track whose notes are not being slid (or with Click activated in the se-
          quencer).

      7. Turn the Slide knob back to its middle position (0 Ticks), then click the channel's Browse button to set Browse
         focus to the ReGroove Patches folder in the Factory Sounds bank.

      8. Open the Vinyl folder, select the first groove patch in the list and click Load to load the groove patch.
      9. Pull up the Groove Amount fader on the channel, to about 80%.

      10.Click the Next Patch button to step through the groove patches in the folder and hear what they do to your mu-
         sic.
      11.On the ReGroove Mixer channel, click the Edit button to open that channel's groove settings in the floating
         Tool Window.
      12.Move the various horizontal faders and listen for their effect.
          Note that none of the patches in the Vinyl folder make use of Note Length, so the Note Length Impact will have
          no effect.
      q   There are all sorts of creative and useful ways to apply grooves to your music. See “Groovy tips & tricks”, later
          in this chapter, for some suggested techniques.

      Commit to Groove - making the grooves “permanent”
      When you assign a ReGroove channel to a note lane, this will only affect how the notes play back. The notes will still
      be shown with their original, ungrooved positions if you open the note clip.
      If you want to edit grooved notes (e.g. adjust timing and velocity manually), it’s useful to first actually move the notes
      to the grooved positions, permanently. This is done with the “Commit to Groove” function:
      1. Select the track with the grooved note lane(s).
      2. Select “Commit to Groove” from the Edit menu or the track context menu.
        All notes on all lanes on the track will be moved to their grooved positions, and the Groove Select pop-up will be
        reset to “No Channel”.
      If you play back the track, it will sound exactly the same as before. If you look at the notes in Edit mode, their posi-
      tions, length and velocity will now match what you hear.


=== END OF PART ===
