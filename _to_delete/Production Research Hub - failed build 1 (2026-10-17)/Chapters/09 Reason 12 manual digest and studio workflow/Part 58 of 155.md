# Chapter 09: Reason 12 manual digest and studio workflow
## Part 58 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 49 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 59 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 49 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Using Commit to Groove on some lanes only
      “Commit to Groove” affects entire tracks, including all note lanes if there are several. If you only want to make the
      groove permanent for one of the lanes, here’s a workaround:
      1. Click the Groove Select pop-up for the note lanes that should remain ReGrooved, and turn off “Enabled”.
        This bypasses the ReGroove channel for those note lanes, but retains the channel selection.

      2. Select “Commit to Groove”.
        Only the note lanes with ReGroove Enabled will be affected.
      3. Select “Enabled” again for the note lanes that should remain ReGrooved.

      Creating your own ReGroove patches
      To create your own ReGroove Patch, proceed as follows.
      1. Create a clip containing notes with the desired timing and dynamics (velocity).
          Alternatively, you could import a MIDI File with the desired effect, or use the “Copy Loop To Track” function on a
          Dr. Octo Rex device to extract the notes from a REX loop.
      D   Note that some MIDI clips will make better grooves than others.
          To learn some of the characteristics of a good groove-making clip, see “Tips for selecting the best Groove-Making
          Clips” below.
      2. Select the clip.
      3. In the Tool Window's Groove section, select an unused Groove Channel.
      4. Click the “Get from clip” button at the bottom of the Tool Window's Groove Settings tab.
          Alternatively, you could select “Get Groove From Clip” from the clip's context menu.
      5. Set the various impact parameters as desired.
          For a good starting point, you can simply leave them at their default settings.
      6. Click the Save Patch button in the Tool Window's Groove section and specify a name and location.
      Your ReGroove patch is now ready to use. As discussed in “Applying grooves to your music”, simply route one or
      more note lanes to the ReGroove channel assigned to your new groove, and pull up the Groove Amount fader on that
      channel.

      Tips for selecting the best Groove-Making Clips
      The following tips will help insure that your custom grooves work their best:
      D   Include as many sixteenths notes as possible in the source clip.
          If there are any sixteenth note gaps in your source material, there will be corresponding gaps in your groove patch.
          This means, when you apply the groove to a note lane, some notes will be grooved and some (those that fall in the
          gaps) will not.
      D   Grooves use the relative differences between note velocities, not their absolute values.
          If you don't want dramatic shifts in dynamics, avoid having widely varying velocities in your source clip.
      D   Groove patches are always an exact number of bars, so if your source clip has an uneven length, the groove
          will be extended to the next bar.
          We recommend that you adjust your source clip to an exact number of bars before creating a groove patch.
      D   In general, you should use source clips whose length is an even multiple of 2 (for example, 1-bar, 2-bars, 4-
          bars, etc.)
          You can create and use grooves that are an odd number in length (3, 7, 13, etc.), but unless you're well organized
          and plan to use these grooves in specific polyrhythmic pieces, their general effect on most tracks will be some-
          what unpredictable.

      Groovy tips & tricks
      • Because you can route each note lane to any of the 32 ReGroove channels, the key to creating really dynamic
        grooves is to spread your instrumentation across multiple note lanes.
          For instance, where you might normally create a Redrum sequence with kick, snare, and hi-hat all on the same
          track, putting these elements into different lanes will let you apply different grooves to them. For example, you
          might have a kick lane routed to a ReGroove channel with a slight shuffle feel, and you might send the snare to a
          ReGroove channel that slides the notes earlier in time to “push” the backbeat a little. Breaking things into lanes will
          definitely enable you to create beats that are more loaded with feel and personality than if you simply apply one
          groove setting to everything.
      q   See “Extract Notes to Lanes” for tips on how to automatically distribute notes from one note lane to several
          additional note lanes.
      • When building a groove, start simple. Experiment with adjusting the slide parameter to move just the snare or
        hi-hat forward or backward in time.
          Try applying slightly different amounts of shuffle to different percussion instruments. Small changes can some-
          times have a big visceral effect, so use your ears (and not your eyes) when adjusting the various groove settings.
      • Try applying the same groove patch to multiple lanes, but by varying amounts.
          You are, of course, free to apply different groove patches to different lanes. Though, more often than not, your re-
          sults might result in something that sounds more clumsy than groovy. The hottest grooves often have the most
          subtle of humanization.
      • Don't forget to try sending sequenced REX files through the ReGroove mixer.
          Depending on the material in the file and how it's sliced up, this can create all types of results-ranging from unus-
          able to downright inspiring.
      • If you're doubling instruments - that is two instruments play the exact same part - try sending one of the instru-
        ments to a ReGroove channel that has a small amount of random timing applied.
          Random timing (which is accessible in the Groove Settings section of the Tools Window) will put some separation
          between the two instruments, making their performance sound more human. For example, if you have a clap dou-
          bling a snare, apply a little bit of random timing to the clap track, and it'll stand out more clearly in the mix.
      • As described under the “Anchor Point” heading above, grooves restart whenever a new time signature ap-
        pears.
          You can use this knowledge to force a groove to restart, which might be required if your music contains sections
          of odd lengths. Simply add in a time signature event, with the same type of time signature as you already have in
          the song. The groove will restart where the event starts.
      • Remember that groove patches have separate timing and velocity impacts and, as such, you can apply them in-
        dependently.
          For example, if you already have a track that has just the right groove timing, but you want to experiment with dif-
          ferent dynamic feels, you can apply just the velocity portion of a groove by setting its Timing Impact parameter to
          0. A groove's timing and velocity impact parameters can be accessed by clicking a ReGroove channel's Edit but-
          ton, which opens the Groove Settings section of the Tools Window.

      ReGroove patches in the Factory Sounds bank
      Reason ships with a ready-made assortment of groove patches, arranged in a number of different folders:

      Bass-Comp, Drummer, and Percussion
      Grooves in these categories were created by session musicians. Their performances were captured and analyzed,
      and the timing and velocity information was then extracted from the performances. The Bass-Comp patches also
      contain note length information, though the other categories do not.

      MPC-60
      These grooves were created by analyzing the audio output of an Akai MPC-60. Use these patches to get the same
      shuffle feeling as an original MPC-60. Note that these patches do not contain any velocity or note length information.
      There are some additional patches that use the Random Timing feature, which emulates the original MPC-60's be-
      havior when loaded with a lot of information.

      Programmed
      These grooves were created by a session drum groove programmer. They were hand-crafted to emulate the feel of
      certain styles, and are divided into two genres: Hiphop and Pop-Rock. These grooves do not contain any note length
      information.

      Vinyl
      These grooves were created by sampling snippets from classic groove records, analyzing them with a special signal
      processing tool, then extracting both timing and velocity information from the samples. These grooves do not contain
      any note length information.

586   THE REGROOVE MIXER


---

<a id="remote-playing-and-controlling-devices-23"></a>

=== END OF PART ===
