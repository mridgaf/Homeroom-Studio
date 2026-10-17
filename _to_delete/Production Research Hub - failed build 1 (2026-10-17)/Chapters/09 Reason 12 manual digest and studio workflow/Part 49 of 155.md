# Chapter 09: Reason 12 manual digest and studio workflow
## Part 49 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 40 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 50 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 40 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Working with effects
      Insert FX
      By definition, insert effects are inserted in the signal chain and process the whole channel signal, as opposed to Send
      effects (see “Send FX”) where the effect is shared among all channels and the balance is individually adjustable for
      each channel. Typical insert effects are dynamics, distortion, chorus etc., plus mastering effects for the Master Sec-
      tion.

      As mentioned earlier in this chapter, the channel strips and Master Section strip have a “slot” dedicated to insert ef-
      fects - the Insert FX section. In the Insert FX section, you can create effect devices and use as insert effects.
      q   A very flexible way of using Insert FX is to have the effects in separate mixer channels and utilize parallel pro-
          cessing, see “Parallel Channels”.

      Adding Insert effects
      To add an effect device as an insert effect, proceed as follows:
      1. Select a channel strip in the Main Mixer, a Mix Channel or Audio Track device in the rack, or an audio track or
         Mix Channel track in the sequencer.
      2. Select the desired effect device from the Create menu or from the context menu.
          The effect device is created and automatically routed in the Insert FX container in the channel's rack device.

          A Scream 4 device created as Insert FX in an Audio Track device.
      3. If you need to re-route any connections, press [Tab] to flip the rack around.

          The “To Device” and “From Device” connections in the Insert FX slot in the Audio Track device.
      !   Note that the Mix Channel/Audio Track device must be unfolded to show the connections.
      D   If desired, re-route the connections according to the standard routing procedures (see “Manual routing”).
          The signals always travel from the “To Devices” outputs, via the desired effect devices, to the “From Devices” in-
          puts on the Mix Channel/Audio Track device.
      • When the Show Insert FX button is on, you can add devices directly in the insert FX container area, drag de-
        vices in or out, etc. - just like with a Combinator (see “The Combinator”).
      !   Note that if you add, load or route insert effects in stereo, and the Mix Channel/Audio Track device (and chan-
          nel strip) is in mono, the channel will automatically switch to stereo.

      Using Effect Combi patches as insert effects
      It’s possible to load Effect Combi patches as Insert FX as well. First you either need to create a Combinator device in
      the Insert FX container of the channel - or drag an Effect Combi patch from the Browser and drop in the Insert FX
      container.
      You could also add several Combinators/Effect Combi patches to the same Insert FX container, e.g. by dragging and
      dropping. This makes it possible to have multiple Combinators in series, for even more complex effects processing:

      Three Effects Combinators serially connected in the Insert FX container.

      Bypassing Insert effects
      D   Click the “Bypass” button at the top of the Insert FX section on the channel strip, or on the device in the rack,
          to bypass the insert effects for the channel.

          The “Bypass” buttons on the channel strip and on the device.

      Deleting Insert effects
      Deletion of insert effects can be done either in the rack or with a mixer channel selected in the Main Mixer:
      1. Select a Mix Channel or Audio Track device in the rack or a mixer channel in the Main Mixer.
      2. Select “Clear Insert FX” from the Edit menu or context menu.
          This will disconnect and delete all Insert FX devices of the selected channel. The deleted devices will be replaced
          by an internal straight-through connection.
      Another way of deleting Insert FX is by manually removing them from the Insert FX container in the Mix Channel or
      Audio Track device in the rack:

      1. Unfold the Mix Channel/Audio Track device and click the “Show Insert FX” button.
      2. In the Insert FX container, select the device(s) you want to remove.
      3. Press [Backspace] or [Delete], or select “Delete Devices and Tracks” from the Edit or context menu.
        An alert appears asking you to confirm the deletion. (See “Deleting devices” for more details).

      Copying and Pasting Insert effects between mixer channels
      To copy the insert effect(s) from one mixer channel and paste to another mixer channel, proceed as follows:
      1. Select the mixer channel which contains the Insert effect(s) you want to copy.
      2. Select “Copy Channel Settings” from the Edit or context menu and then select “Insert FX” from the sub-menu.
        If you select the Master Section, the “Copy Insert FX” item will appear directly on the Edit menu or context menu.
      3. Select the mixer channel to which you want to paste the Insert effects and choose “Paste Channel Settings: In-
         sert FX” from the Edit menu or context menu.
        If you select the Master Section, the “Paste Insert FX” item will appear directly on the Edit menu or context menu.

      Send FX
      Send effects are routed in parallel with the signal chain, and the effect balance can be adjusted - as opposed to In-
      sert effects, which are inserted in the signal chain and process the whole channel signal (see “Insert FX”). Typical
      Send effects include reverbs and delays.
      The Main Mixer can hold up to eight separate Send effects per Song. These eight Send effects can be used simulta-
      neously by any or all mixer channels in the Song, at individually adjustable levels per mixer channel. The main Send
      FX controls, which include the FX Send and FX Return sub-sections, are located in the Master Section strip in the
      mixer. In these sections, you can control the FX Send and FX Return levels to and from all mixer channels, as well as
      panning for each of the Send effects.
      In addition to the “global” Send FX controls in the Master Section, each mixer channel features a Send FX section,
      where you can control the levels to each of the Send effects for the specific mixer channel.
      Mixer Channel                       Master Section                                Master Section
      FX Send section                     FX Send section                               FX Return section

      Creating Send effects
      Send effects can be added as follows:
      1. In the Main Mixer, select a channel strip or the Master Section strip.
      2. Select “Create Send FX...” from the context menu.
          The Browser appears (if it was hidden) and the Send FX section gets browse focus. Now, you can now browse for
          and load effect devices. You can also browse for Effects patches and load these into their corresponding devices,
          e.g. Effect Combinators.
      !   If all eight Send effect busses are already in use, the “Create Send FX...” item on the context menu is grayed
          out.

      • Each FX Send and FX Return in the Master Section strip has a display that shows the name of the last effect
        in that send's signal path:

          The names of three added Send effects are displayed in the Master Section strip.
      3. If you need to re-route any connections, press [Tab] to flip the rack around.

          The Send FX connections on the Master Section device.
      !   Note that the Master Section device must be unfolded to show the connections.
          As you can see, all Send effects are placed outside the Master Section device - as opposed to Insert effects, which
          are placed in the Insert FX container of the Master Section device.
      • It’s also possible to manually connect devices to the FX Send and FX Return connectors according to the stan-
        dard routing procedures (see “Manual routing”).
          The signals always travel from the “FX Send” outputs, via the desired effect device(s), to the “FX Return” inputs on
          the Master Section device.

      Editing and saving Send effects
      D   Click the “Edit” buttons in the FX Send or FX Return sections to get to the corresponding Send effect device(s)
          in the rack.

          The Edit buttons for the Send effects in the FX Send and FX Return sections.
          The corresponding Send effect devices are scrolled into view in the rack.
      • Send effects can be edited from their device panels according to standard editing procedures.
          Any edits you make will be automatically stored when you save the Song document. If you edit Effect Combi
          patches, these can also be saved separately as Combinator patches as usual.

      Muting Send effects
      D   Click one of the “M” buttons in the FX Return section to mute the FX Return for the corresponding Send effect.
          All channels that currently use the muted send effect will be affected.

          The Mute buttons for the Send effects in the FX Return section.
      !   The Mute buttons only mute the FX Return signals. If you should choose to route an FX Send output of the
          Master Section device to an effect, and then route the effect to a regular Mix Channel instead of an FX Return
          input, the Mute button will of course not have any effect.

      Deleting Send effects
      Deletion of Send effects is done in the rack according to the standard device deletion procedures:
      D   Select the device(s) you want to delete and press [Backspace] or [Delete] - or select “Delete Devices and
          Tracks” from the Edit or context menu.
          An alert appears asking you to confirm the deletion. (See “Deleting devices” for more details).
      • When a Send effect has been deleted, the name will automatically be removed from the displays in the FX
        Send and FX Return sections in the Master Section strip.

      Output Busses
      Output Busses allow you to create sub-mixers. Sub-mixers can be very useful for pre-mixing a multi-mic’ed drum kit,
      or a horn section, for example. You can also use a sub-mixer configuration to route several external input signals
      (from separate microphones, for example) for recording onto a single audio track (see “Recording a sub-mix onto an
      audio track”). You can have as many mix busses as you like in a Reason song.
      q   For multiple levels of sub-mixing, it’s also possible to create an Output Bus that is fed by an existing Output
          Bus.

      Creating an Output Bus
      The fastest and easiest way of creating an Output Bus for several mixer channels is this:
      1. Select all mixer channel strips that you want to route to the same Output Bus.
      2. Press [Ctrl]+[G](Win) or [Cmd]+[G](Mac) - or select “Route to > New Output Bus” from the Edit menu or con-
         text menu of one of the selected channels.

          A new Output Bus channel, named “Bus 1”, is created to the right and the selected channels are automatically
          routed to it as indicated on the channels’ Output labels.
      The step-by-step instructions below show how you can assign individual channels to an Output Bus - one channel at
      a time. The picture shows a number of Audio Tracks in a song with individual recordings of the drums of a drum kit:

      Audio Tracks with separate drum recordings routed to the Master Section.
      Now, we want to create a sub-mixer which mixes only the individual drum channels. The advantage of doing this is
      that we can then control the sound and volume of the entire drum kit using only one single Mix Channel:
      1. Click the Output selector (the gray name tag) on the Kick channel and select “New Output Bus”.

      D   Alternatively, select the Kick channel strip and press [Ctrl]+[G](Win) or [Cmd]+[G](Mac).
          A new Mix Channel is created in the Main Mixer and its corresponding Mix Channel device is created in the Rack.
          The Kick channel is now routed to the new Mix Channel via the internal P-Lan network.
          The Output selector area on the Kick channel is colored and the name “Bus 1” is displayed to indicate the name
          of the Output Bus it is routed to:

          The Fader section of the new Output Bus channel gets a colored background and a red Fader knob to indicate it
          is an Output Bus.
      2. Click the Output selector on the Snare channel and select “Bus 1”.

          The Output selector area on the Snare channel is now colored in the same color as the Bus 1 channel and the
          Output Bus name is displayed:

      3. Repeat the procedure for the remaining drum channels in the Main Mixer.

      4. If you like you could now rename the Output Bus channel, e.g. to Drum Mix, and drag the channel strip to the
         right of the individual drum channels for better overview:

          The changed Output Bus name is automatically displayed in the colored Output area on all channels routed to that
          Output Bus channel.
      If you look in the rack, you can see that the Audio Output display on the Audio Track devices for the individual drum
      channel now show “Drum Mix” instead of the default “Master Section”.

      Output Bus destinations on the Audio Track devices in the rack (front and rear).

      Rerouting channels
      D   If you like you can change the Audio Output destinations - or create new Output Busses - by clicking the Audio
          Output selector on the device front panel, or in the Audio Output display on the rear panel, or in the Output se-
          lector area on the channel strip in the mixer.
      !   If you manually deassign all channels from the Drum Mix Output Bus channel, the Output Bus channel auto-
          matically becomes a regular Mix Channel. If you want to assign channels to this Mix Channel, and thus make it
          become an Output Bus channel again, click the Audio Output selector on the front panel, or in the Audio Out-
          put display on the rear panel, and select “All Channels > Drum Mix”. These routings can also be made in the
          Output selector area on the channel strip in the mixer.

      Deleting an Output Bus
      D   To delete an Output Bus channel, select the Output Bus channel strip in the Main Mixer - or the device in the
          rack - and press [Delete] or [Backspace].
          When you delete an Output Bus channel which has other mixer channels already routed to it, the source channels
          will be automatically re-routed to the default Master Section again via P-Lan.
          On the Mix Channel/Audio Track devices in the rack, “Master Section” is now shown in the Audio Output displays
          to indicate that the channels have been re-routed to the Master Section device.

      Recording a sub-mix onto an audio track
      The example below shows an Output Bus (sub-mixer) configuration with four microphones connected to one input
      each on the audio interface and then routed from the Reason Hardware Interface to the Direct Inputs on four Mix
      Channel devices. The four Mix Channel devices are routed to the “Drums SubMix” Output Bus for sub-mixing:

      Direct routing of individual Audio Inputs to Mix Channels which, in turn, are routed to an Output Bus for sub-mixing.
      D   To record the sub-mixed signals from the “Drums SubMix” Mix Channel onto Audio Track 1, click the Rec
          Source button on the “Drums SubMix” Mix Channel device, and then select “Stereo Input” and “Drums Sub-
          Mix” as Audio Input source on the “Audio Track 1” device:

          The Rec Source button on the Drums SubMix device activated and “Drums SubMix” selected as Audio Input on the Audio Track 1
          device.
          See “Recording audio from Mix Channel outputs” for more details.
      q   In the sub-mixer setups above, each source Mix Channel could also house individual Insert FX. See “Creating
          an input channel for recording with effects” for tips on how to record with FX.

      Parallel Channels
      A very flexible way of working with insert effects is to use parallel channels that host the effects, while keeping the
      dry signal of the source channel intact. This way you can freely control the levels of the dry signal and the separate
      effects - and also control the sound of each effect individually from each of the parallel channels.
      You could, for example, have one parallel channel with a compressed distortion effect, another parallel channel with
      a Delay, and so on. Then, you can freely EQ the effects in each of the parallel channels, as well as control their levels
      individually from each Fader.

      Creating Parallel Channels
      Parallel channels can be created as follows:
      1. Select the source Mix/Audio Track channel strip in the Main Mixer, or its device in the rack.

      2. Select “Create Parallel Channel” from the Edit menu or context menu.
        A new Mix Channel is created and placed to the right of your original channel in the Main Mixer:

        A Parallel Channel created for Audio Track 1.
        The parallel Mix Channel is automatically named “P1: <source channel name>” and its channel header is colored
        according to the source mixer channel header. Both the source channel and the parallel channel also get shorter
        channel headers to indicate they are routed in a parallel configuration.

      D   If you want to add more parallel channels to your source channel, select the last created parallel channel and
          select “Create Parallel Channel” from the Edit menu or context menu.
          This adds another parallel channel to your source channel:

          Another Parallel Channel created for Audio Track 1.
          In the rack, the Parallel out jack(s) of the source Mix Channel/Audio Track device are automatically connected to
          the Direct Input jack(s) of the first parallel Mix Channel. The second parallel Mix Channel is then connected to the
          first parallel Mix Channel, and so on:

                                                                                                            Source device

                                                                                                            Parallel channel 1

                                                                                                            Parallel channel 2

          Parallel Channels 1 and 2 for the Audio Track 1 source channel in the rack.
      !   Since the Audio Track/Mix Channel device only has one pair of Parallel out jacks, any additional parallel chan-
          nels have to be created from the last created parallel channel.
          If your original channel is in mono, only the left parallel output is connected to the left input of the parallel channel.
      3. Now, you can create Insert FX in each of the parallel channels and process the signal of your source channel
         separately, in parallel.
      q   It might also be a good idea to create a separate Output Bus for the source channel and all parallel channels,
          see “Creating an Output Bus”.

      Creating a Parallel Output Bus
      Parallel channels can also be created for Output Bus channels, for parallel processing of the entire Bus signal. The
      following example shows a drum kit, with a channel for each drum, that we want to assign to an Output Bus and apply
      parallel compression to:

      1. [Shift]-select all drum channels in the mixer.
      2. Press [Ctrl]+[G](Win) or [Cmd]+[G](Mac) to create a new Output Bus to automatically route the drum channels
         to.

        A new Output Bus channel, named “Bus 1”, is created to the right and the selected channels are automatically
        routed to it as indicated on the channels’ Output labels.
      3. Select the “Bus 1” channel in the mixer and select “Create Parallel Channel” from the Edit menu or context
         menu.

        A parallel channel, the “P1: Bus 1” is created and the “Bus 1” Output Bus channel is automatically connected to it.

      4. Activate the Compressor in the “P1: Bus 1” parallel channel and raise the Compression Ratio up high.

      5. Raise the Level fader on the “P1: Bus 1” channel to gradually introduce the heavily compressed sound (in par-
         allel with the dry signal of the “Bus 1” channel).

      Deleting Parallel Channels
      D   To delete a Parallel Channel, select its mixer channel strip - or its device in the rack - and press [Delete] or
          [Backspace].
          Confirm the deletion in the alert that appears.

      Naming Parallel Channels
      When you create a Parallel Channel it is automatically named after its source channel according to: “P1: <source
      channel name>”, where “P” stands for Parallel and “1” for the first parallel channel. If you add on more parallel chan-
      nels, the following channels are named “P2: <source channel name>” and so on.
      If you change the name of the source channel, all the parallel channel are automatically renamed accordingly. You
      can then manually rename each parallel channel afterwards if you like.
      D   To revert to the automatically generated name, double-click the parallel channel’s name, press [Delete] or
          [Backspace] and then [Enter].

      Solo, Mute and Send FX logic
      The Solo, Mute and Send FX functions in the channel strips are very straight-forward when you work with mixer
      channels that are routed straight to the Master Section. However, when you are using Output Busses for sub-mixing
      and/or Parallel Channels for parallel processing, the Solo, Mute and Send FX functions need to work intelligently to
      provide the desired result. This has been carefully taken care of in the Main Mixer in Reason.

      Solo and Mute logic
      The Solo and Mute functions are designed to work intelligently in the following special scenarios:
      • When several mixer channels are routed to an Output Bus.
      • When a mixer channel has one or more Parallel Channels.
      • When Output Busses are routed to other Output Busses.
      • When Output Busses have Parallel Channels.

      Solo and Mute examples
      There are two ways a mixer channel can be soloed or muted:
      • Manually, by clicking the corresponding Solo or Mute buttons.
        In these situations, the buttons light up in green (Solo) or red (Mute).
      • Automatically, according to the state(s) of the other mixer channels.
        This happens when another mixer channel is affected by a manual Solo/Mute in another mixer channel. Automat-
        ically soloed/muted buttons light up in dimmed green (Solo) or dimmed red (Mute) color.

      The examples in the figure below show how Solo and Mute work in different mixer channel configurations:

      The Snare channel has been manually
                                                                                                  Parallel
      soloed.
                                                                   The Snare channel has been manually soloed.
      Since the Snare channel is routed to the
      Drums SubMix Output Bus, the Drums                           Since the Snare channel is routed to the Drums Clean Output
      SubMix bus is automatically soloed to let                    Bus, the Drums Clean Output Bus is automatically soloed to let
      the Snare signal through to the Master                       the Snare signal through.
      Section.                                                     The Drums Clean Output Bus is routed to the Drums SubMix
      All other mixer channels are automatically                   Output Bus. The Drums Clean channel also has a parallel
      muted.                                                       channel; the Drums Dist, which is also routed to the Drums
                                                                   SubMix Output Bus.
                                                                   This means that the Drums Clean, Drums Dist and Drums SubMix
                                                                   channels are automatically soloed to let the Snare signal through
                                                                   to the Master Section.
                                                                   All other mixer channels are automatically muted.

                                   Parallel                                                      Parallel
      Now, if we manually mute the Drums Clean Output Bus          If we start from scratch again and click the Solo button in the
      channel from the previous example, its automatic solo is     Drums SubMix channel, all channels routed to the Drums
      disabled, allowing you to hear the sound of the Drums Dist   SubMix Output Bus are automatically soloed.
      bus only.                                                    All other mixer channels are automatically muted.

      Below is another example of the Solo and Mute logic:

                                    Parallel
      The Drums Dist parallel channel is manually soloed.
      Its output bus, the Drums SubMix, is automatically soloed, as
      are the Kick, Snare and Overhead channels that are routed to
      the Drums Dist channel via the parallel connection from the
      Drums Clean channel.
      The Drums Clean channel is automatically muted, as are the
      other remaining channels in the mixer.

      Send FX level and mute logic
      If you are using Send FX in your mixer channels, these need to behave intelligently when you are using Output Bus
      channels and/or Parallel Channels.

      Send FX level examples
      Since the eight Send FX busses in the Main Mixer are shared between all mixer channels, including Output Bus
      channels, there has to be a way to compensate the Send FX levels for changes in Output Bus levels. Therefore:
      • If a channel is routed to an Output Bus, its Send FX levels will follow the Output Bus level.
          One example would be if you have a number of drum channels routed to a “Drums” Output Bus, and add a reverb
          to the Snare channel using an FX Send. Now, if you raise or lower the Drums Output Bus level fader, the individual
          Snare reverb Send level will automatically adjust, so that the effect balance is maintained.
      !   Note that the automatic Send FX level adjustment is disabled if the Send FX PRE button is on.
      !   Note that the individual FX Send level knobs will not move to reflect the automatic level compensations.

      Send FX mute examples
      The example in the figure below shows how the Send FX behave when an Output Bus channel is muted:

      The Send FX outputs of all channels that are
      routed to the Drums SubMix Output Bus are
      automatically muted if you manually mute the
      Drums SubMix Output Bus channel.

      The examples in the figure below show how the Send FX behave when you mute a Parallel Channel as well as a Par-
      allel Channel plus an Output Bus:


=== END OF PART ===
