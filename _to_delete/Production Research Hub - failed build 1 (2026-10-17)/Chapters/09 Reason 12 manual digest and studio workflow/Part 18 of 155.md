# Chapter 09: Reason 12 manual digest and studio workflow
## Part 18 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 9 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 19 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 9 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Creating a parameter automation track for a non-instrument device
      For non-instrument devices, such as effects devices and Mix Channel devices, you need to manually create a track if
      you want to record parameter automation. You can do that either by following the description below or by following
      either of the two last descriptions in “Creating/adding parameter automation lanes”.
      The track creation procedure described below also applies if you have manually deleted a track for an instrument de-
      vice or an Audio Track device and want to create a new track for the device:
      1. Select the device by clicking on it in the rack.

                                      RV7000 device

          A border around a device in the Rack indicates that it has been selected.
      2. Select ”Create Track for ((patch) name of device)” from the Edit menu or the device context menu.
      !   Note that if a track already exists for the device, this menu item will not be available - a device can only have
          one track.
      • The new track will be automatically associated with the device and will get the same name as the device.

                                    RV7000 device

                                           TheRV7000 Automation Track

      D   Another way of creating a parameter automation track is by holding [Alt](Win) or [Option](Mac) and clicking
          on a parameter on the device panel. Alternatively, select “Edit Automation” from the parameter context menu.
      q   If you press [Alt](Win) or [Option](Mac) when you create a non-instrument device, this will automatically create
          an associated automation track for the device.

      Short-cut for creating a Mix Channel track or Audio track
      A faster way of creating a track for a Mix Channel device, or to create a new audio track (if you deleted the original
      one), is to go via the corresponding mixer channel strips in the Main Mixer:
      1. Scroll to the Main Mixer and locate the channel strip you want to create a track for.

      2. [Shift]-click the SEQ (Goto Sequencer Track) button at the bottom of the channel strip.
          A new track will be automatically created in the sequencer for the selected channel strip.
      !   If a track should already exist for the selected channel strip, [Shift]-clicking the SEQ (Goto Sequencer Track)
          button will only scroll the corresponding sequencer track into view, not create any new track.

      Selecting tracks
      D   Select a track by clicking on it in the Track List.
          A selected track gets a darker gray background color.

      q   Selecting a track in the sequencer will automatically scroll the corresponding device into view in the rack.
      D   Double click a device icon in the Track List to automatically reveal the associated device in the rack.
      • Selecting an audio track will set Edit Focus to its channel strip in the Main Mixer.
      • Selecting another type of track (e.g. an instrument track) will set Edit Focus to the Mix Channel belonging to
        that device group.
          See “About Device Groups” for information about device groups.
      D   You can also select the next or previous track in the Track List list by using the up and down arrow keys on the
          computer keyboard.
      !   By default, selecting a track will automatically set Master Keyboard Input to that track. If you’d rather select
          tracks independent of the Master Keyboard Input selection, select “Separated” mode in the Preferences menu
          (“MIDI” page). In “Separated” mode, you can select another track without automatically changing Master Key-
          board Input. To change Master Keyboard Input, click the device icon on the desired track in the Track List.
      • It is possible to select several tracks by using the standard [Shift], or [Ctrl](Win) or [Cmd](Mac), selection tech-
        niques.
          This allows you to e.g. move or delete several tracks in one go.
      • It is also possible to select several instrument tracks (by using standard [Shift], or [Ctrl](Win) or [Cmd](Mac),
        selection techniques) and then edit the Note Clips using the Multi Lanes function, see “Multi Lanes editing”.

      Resizing tracks
      If you like you can resize tracks vertically, for a more detailed overview:
      D   Click the bottom edge of the track in the Track List and drag down/up to resize the track height.
          The cursor switches to a vertical “double arrow” as you hover over the bottom edge of a track in the Track List.

      D   To resize multiple tracks in one go, select the desired tracks and drag the bottom edge of one of the selected
          tracks.
          If the selected tracks have different heights to begin with, they will be scaled proportionally.
      D   To scale multiple tracks to the same heights, hold [Alt](Win) or [Option](Mac) and drag one of the track bottom
          edges.
      D   To scale all track heights proportionally, click the -/+ Track Height buttons:

      D   To set all track to the same height, hold [Alt](Win) or [Option](Mac) and click the -/+ Track Height buttons:
      !   Note that folded tracks (see “Folding tracks”) cannot be resized.

      Moving tracks
      D   To move a track to another position in the Track List, click on the track handle (the leftmost area of the track)
          and drag the track up or down.
          A red insertion line is shown, indicating where the track will be placed after releasing the mouse button. All clips on
          all lanes of the track will be moved along with the track.

          You can use the same technique to move several selected tracks at once. Use standard [Shift]-select or use
          [Ctrl](Win) or [Cmd](Mac) to select non-adjacent tracks.

      About sorting devices and channel strips according to the track order
      Note that the order of the tracks in the sequencer Track List is totally independent from the device order in the rack
      - and from the channel strip order in the Main Mixer. However, it’s possible to re-order devices and channel strips ac-
      cording to the track order in the Track List:
      1. Select the tracks in the Track List you want to re-order devices and channel strips after.
      2. Select “Sort Selected Device Groups” from the Edit menu or from the track’s context menu.
          The associated devices and channel strips are now re-ordered, in the rack and Main Mixer respectively, according
          to the order of the selected tracks in the Track List.
      !   Note that the re-ordering only affects the devices and channel strips of the selected tracks - all other devices
          and channel strips will remain unaffected.

      Deleting tracks
      The most common scenario would probably be to delete a track together with its associated device(s). However, it’s
      also possible to delete only the track while keeping the associated device(s) in the rack.

      Deleting tracks together with their associated devices
      D   To delete one or several tracks together with their associated devices in the Rack, select the tracks and then
          select “Delete Track(s) and Device(s)” from the Edit menu or from the track’s context menu. Alternatively,
          press [Delete] or [Backspace].
          An alert appears which prompts you to confirm or cancel the deletion of the track(s) and device(s).
      !   If you're deleting the track for the Source Device or Mix Channel, and “Auto-group Devices and Tracks” on the
          Options menu is on, you will be asked if you want to delete the whole device group. If you hold down
          [Ctrl](Win) or [Cmd](Mac) while deleting, the whole device group will be deleted without the alert.
          See “About Device Groups” for more information about device groups.

      Deleting tracks only
      D   To delete one or several tracks, select them and then select “Delete Track(s)” from the Edit menu or from the
          track’s context menu.
          The tracks will be deleted without an alert but you can always use the Undo function. See “Undo and Redo”.
      !   If you delete an audio track, all recordings on that track will be removed!
      If you have deleted a track for a device and want to create a new track for the device, follow the descriptions in “Cre-
      ating a parameter automation track for a non-instrument device” or “Short-cut for creating a Mix Channel track or Au-
      dio track”.

      Duplicating/copying tracks and devices
      As it is not possible for a specific instance of a device to have more than one track, you cannot copy or duplicate only
      a track. These operations will instead duplicate/copy both the track (including all clips on the track) and its associ-
      ated device(s) (with all settings). The duplicated/copied devices are really just like separate devices but with the
      same name and settings as the original devices, although their names will have the extension “Copy” to differentiate
      them from the original.
      To make copies of tracks and their associated devices, complete with all lanes and recorded clips, use any of the fol-
      lowing methods:

      !   Note that if “Auto-group Devices and Tracks” on the Options menu is on, the entire device group(s) associated
          with the track(s) will be copied/duplicated when you perform the procedures described below.
          See “About Device Groups” for more information about device groups.
      D   Hold down [Ctrl](Win) or [Option](Mac), click on the track handle and drag the selected track(s) to a new posi-
          tion in the track list.
      D   Select the track in the Track List, hold down [Ctrl](Win) or [Cmd](Mac) and press [D].
          The duplicated track(s) will be inserted below the original track.
      D   Select “Duplicate Device(s) and Track(s)” from the Edit menu or from the track’s context menu.
          To bring up the context menu, right-click (Win) or [Ctrl]-click (Mac) on the track in the Track List. The duplicated
          track(s) will be inserted below the original track.
      D   Select “Copy Device(s) and Track(s)” from the Edit menu or from the track’s context menu.
          This allows you to insert the copied track(s) and device(s) by selecting “Paste” from the Edit menu or from the
          track’s context menu. The copied track(s) will be pasted below the currently selected track.
      !   Note that if “Auto-group Devices and Tracks” on the Options menu is off, duplicated/copied devices will not
          have auto-routed audio connections. To hear the duplicated devices, select the device and choose “Auto-route
          Device” on the Edit menu or context menu. Alternatively, flip the rack around and connect the audio outputs to
          available (or new) Mix Channel devices. You might also want to mute the original track to avoid double notes.
      D   To duplicate a selected audio track, with all recordings and mixer channel strip parameter settings, including
          any Insert FX, click the “Alt” or Dub” buttons on the Transport Panel - see “Duplicating audio tracks using the
          “Alt” function” and “Overdubbing audio using the “Dub” function”.
      q   If you hold down [Shift] and select Paste from the Edit menu or context menu, the copied device(s) will be
          auto-routed to an available mixer channel. If necessary, an additional Mix Channel will be automatically cre-
          ated.

      Coloring tracks
      A track can be assigned a color in the sequencer as follows:
      D   To assign a new color to a selected track, select “Track Color” from the Edit menu or from the track’s context
          menu and then select color from the palette.
          The track color is shown in the track background in the Track List. The associated Audio Track device or Mix
          Channel device in the rack and its corresponding channel strip in the Main Mixer will also be assigned the new
          color. The selected track color will be reflected in all new clips you record or draw on this track.
      !   If existing clips have the function “Use Track Color” active on the Clip context menu, these clips will also
          change color - otherwise they won’t. To manually change color of previously recorded clips, refer to “Coloring
          clips”.
      D   To automatically set a new color for new tracks, make sure the “Auto-color New Sequencer Tracks” box in the
          Options menu is ticked.
          The track color will be automatically selected from the palette when you create a new track.

      Naming tracks
      Devices (and tracks) get the name of their loaded patch by default, but you can override this by manually renaming:
      D   Name, or rename, a track by double-clicking its name tag in the Track List, typing in a name and pressing [Re-
          turn].
          Note that naming/renaming a track also changes the name of the associated Source Device in the rack (and vice
          versa). Furthermore, renaming an audio track also changes the name of the associated Audio Track device in the
          rack as well as its corresponding channel strip in the Main Mixer. If you rename the track of a source device in a
          device group, its Mix Channel will get the same name. If you want a separate name for the Mix Channel, double-
          click in the Mix Channel name tag, in the rack or Main Mixer, type in a new name and press [Return].
          See “About Device Groups” for more information about device groups.

      Folding tracks
      To minimize the visible height of the track, and thus allow for a better overview of the tracks in the sequencer, it’s pos-
      sible to fold tracks.
      D   To fold/unfold a track, click on the small triangle on the track handle.

          An unfolded track.

          The same track folded.
          A folded track will not show the individual lanes in the Track List, and on the Edit/Arrangement Pane the clips are
          shown as horizontal strips. If the folded track has several lanes, all the clips on the lanes will be shown as vertically
          stacked strips on the Arrangement Pane. No events in the clips are shown.
      D   Basic clip operations (selecting, moving, copying etc.) are available also for folded tracks, although it is gener-
          ally better to unfold a track if you want to edit its contents, as this gives you a better overview.
      D   To fold/unfold all tracks in the sequencer in one go, press [Alt](Win) or [Option](Mac) and click on a track han-
          dle triangle.
      q   It’s also possible to fold/unfold only the parameter automation lanes on a track by clicking the triangle on the
          parameter automation tab. See “Parameter automation lane elements” for more details.

      Muting tracks
      To mute a track means to silence it, so that no data is sent from the track during playback. This can be useful when
      you are trying out different versions of an arrangement, for bringing elements in and out of the mix during playback.
      !   Note that muting a sequencer track is NOT the same as muting a mixer channel (see “MUTE/SOLO buttons”).
      D   To mute a track, click the corresponding Mute (M) button in the Track List.
          Everything present on the track will be muted.

          A red “M” button in the Track List indicates that the track is muted.
      D   To unmute the track, click the “M” button again.
      D   Several tracks can have Mute active at the same time, in which case you can unmute them all by clicking the
          master “M” button at the top of the Track List.

      q   It’s also possible to mute individual lanes and individual clips on a track. Refer to “Muting lanes” and “Muting
          clips”.

      Soloing tracks
      To solo a track means that all tracks in the sequencer, except for the soloed track, are muted.
      !   Note that soloing a sequencer track is NOT the same as soloing a mixer channel (see “MUTE/SOLO buttons”).
      D   To solo a track, click the corresponding Solo (S) button in the Track List.
          This mutes all other (un-soloed) tracks. Soloed tracks have green S buttons.

          Here, the “Filmscore Pad” track is soloed (indicated by the green “S” button).
          All other tracks are automatically muted (indicated by red “M” buttons).
      D   To turn solo off, click the green “S” button again.
      D   Several tracks can have Solo active at the same time, in which case you can turn off Solo for all of them by
          clicking the master “S” button at the top of the Track List.

      Lane details
      A track consists of one (default) or several parallel lanes. Depending on track type, the clips on the lanes can contain
      various types of events. A lane can also contain clips with performance controller and parameter automation events -
      or pattern selection for pattern based devices.

      Audio lane

                                                        Audio Lane

      The audio lane is not distinguished by a separate lane tab in the Track List like the other lane types. This is simply be-
      cause an audio track can only have a single audio lane. Consequently, all audio lane elements reside in the audio
      track section instead.

      Audio lane elements

      • Record Enable button
          To the right of the Record Enable Parameter Automation button is the Record Enable button. Make sure this but-
          ton is on (red) before recording audio on the track. By default, this is activated when you select an audio track. If
          you want to record several audio tracks at the same time you need to click their Record Enable buttons first.
      • Monitor button
          To the right of the Record Enable button is the Monitor button. Click this button to monitor the input signal of the
          track. The signal is monitored after the audio track channel strip which means that all channel strip parameters, in-
          cluding any Insert FX, Dynamics etc., will be monitored.
      !   The Monitor button activation/deactivation depends on the setting in the “Monitoring” section on the “Audio”
          page in Preferences. If “Manual” is selected, you will have to manually activate the Monitor button. If “Auto-
          matic” is selected, the Monitor button is automatically activated when the Record Enable button is on.
      • Enable Tuner button
          To the left below the Device icon is the Enable Tuner button. Click the button to switch to Tuner mode. The Input
          Meter to the right will switch to a Tuner.

          Audio track in Tuner mode.
          In Tuner mode, you can tune a connected instrument - an electric guitar, for example. See “Using the Tuner” for
          more info.

      • Select Audio Input drop-down list
          To the right of the Tuner button is the Select Audio Input drop-down list. Here, you select which audio input(s) to
          use for the track. See “Selecting audio input(s) and defining mono or stereo” for more info.

      • Input Meter
          The Input Meter shows the level(s) of the input signal(s). If the selected audio input is mono, the Input Meter dis-
          plays a single LED bar. If the audio input is in stereo, the Input Meter displays two parallel LED bars. See “Setting
          input level(s)” for details about setting input levels.

      Note lane
                                                        Note Lane

      As the name implies, the note lane can contain clips that feature note events. Clips on a note lane can also contain
      performance controller events. One or several note lanes can be present on an instrument track.

      Note lane elements

      • Name
          At the top to the left is the name of the lane. As soon as you create a note lane it will automatically be named
          “Lane n” where “n” is the number of the lane - in chronological order. You can change the name of the lane by dou-
          ble-clicking in the name field, typing in a new name and then pressing [Return] on the computer keyboard.
      !   Note that depending on the current magnification of the Edit/Arrangement Pane, the note lane names could
          sometimes be hidden. To make the note lane names visible, increase the vertical magnification of the Edit/Ar-
          rangement Pane, for example, by clicking the + magnification button below the sequencer Track Navigator.

          Increase the vertical magnification by clicking the + magnification button below the Track List.

      • Record Enable button
          Below the note lane name is the “Record Enable” button. Make sure this button is on (red) before recording on the
          lane. By default, the “Record Enable” button on the latest created/added note lane is automatically activated when
          you select an instrument track.
      • Groove Select drop-down list
          To the right of the “Record Enable” button is the “Groove Select” drop-down list. Here you can select a ReGroove
          channel for all clips on the lane. See more about ReGroove in “The ReGroove Mixer”.
      • M (Mute) button
          Clicking the “M” button will mute the playback from the lane.
      • Delete (X) button
          To the far right is the “Delete Note Lane” (X) button. Clicking this button will delete the lane (and all clips on it). If
          there are clips on the lane, a dialog appears prompting you to confirm deletion.

      Parameter automation lane

                                                                                                     Parameter Automation
                                                                                                     Lanes

      An instrument track with two parameter automation lanes.
      Parameter automation is used for controlling changes of device parameter values in a song. You could, for example,
      automate a filter cutoff parameter and record filter sweeps at various positions in your song. These kind of parameter
      value changes are recorded on parameter automation lanes.
      Parameter automation lanes can exist in all track types and can contain clips with device and/or channel strip param-
      eter automation. A track can have as many automation lanes as its device has automatable parameters. For Mix
      Channel and Audio Track devices, parameter automation could be used for any of their corresponding channel strip
      controls.

      Parameter automation lane elements

      • Fold/Unfold button
          Parameter automation lanes in a track can be folded/unfolded, as a group, by clicking the small triangle on the
          handle to the far left on the parameter automation lane tab.
      D   To fold/unfold all parameter automation lanes on all tracks in the sequencer, hold down [Alt](Win) or
          [Option](Mac) and click on the triangle on a parameter automation lane tab.
      • Name
          The name of the automated parameter is displayed on the parameter automation lane tab. Since the name reflects
          the original device/channel strip parameter name, this cannot be changed.

      • M (Mute) button
         Clicking the “M” button will mute the parameter automation playback from the lane. Muting a parameter automa-
         tion lane will freeze whatever value the parameter had when you muted the lane. Deactivating the Mute button re-
         activates the automation.
      • Delete Automation Lane (X) button
         To the far right is the “Delete Automation Lane” (X) button. Clicking this button will delete the lane (and all clips on
         it). If there are clips on the lane, a dialog appears prompting you to confirm deletion. See “Deleting parameter au-
         tomation lanes” for alternative ways of deleting parameter automation lanes.

      Pattern lane

                                                                                                    Pattern Lane

      A Redrum track featuring a pattern lane.
      A pattern lane can only exist in a track featuring a pattern based device, such as the Redrum Drum Module or the
      Matrix Analog Pattern Sequencer. A pattern lane can only contain clips with pattern Bank and pattern Number auto-
      mation data. There can only be a single pattern lane per track.

      Pattern lane elements

      • Name
         The name of the automated parameter is displayed on the pattern automation lane tab. Since the name reflects
         the original device parameter name, this cannot be changed.
      • M (Mute) button
         Clicking the “M” button will mute the pattern automation playback from the lane. Muting a pattern automation lane
         will freeze whatever value the parameter had when you muted the lane. Deactivating the Mute button reactivates
         the pattern automation.
      • Delete Pattern Lane (X) button
         To the far right is the “Delete Pattern Lane” (X) button. Clicking this button will delete the lane (and all clips on it).
         If there are clips on the lane, a dialog appears prompting you to confirm deletion. See “Deleting pattern lanes” for
         alternative ways of deleting pattern lanes.

      Creating/adding lanes
      Adding note lanes
      You can add additional note lanes on an instrument track. This can be useful under the following circumstances:
      • If you want to overdub notes or performance automation but don’t want to record in existing clips.
      • If you want to record a series of takes on separate note lanes, to later decide which take is the “best” (or to
        edit together a composite).
      • If you want to apply different ReGroove grooves to different parts of a track, or want different grooves on sep-
        arate drums on a drum track.
      You can create new note lanes for selected instrument tracks in the following ways:
      D   Select “New Note Lane” from the Edit menu or from the context menu.
          A new note lane will be created and automatically record enabled.
      D   Click on the “New Note Lane” (Lanes +) button at the top of the Track List.

          A new Note Lane will be created and automatically record enabled.
      D   Click on the “Dub” button on the Transport Panel.

          A new note lane will be created and automatically record enabled. See “Recording notes using the “Dub” and “Alt”
          functions” for more details.
      D   Click on the “Alt” button on the Transport Panel.

          A new note lane will be created and automatically record enabled. At the same time, the previous note lane, or (if
          loop is activated and the Song Position Pointer is between the Left and Right Locators) the clips between the Left
          and Right Locators, will be muted. See “Recording notes using the “Dub” and “Alt” functions” for more details.
      q   Note that the “Dub” and “Alt” functions can also be used on-the-fly during recording without stopping the se-
          quencer.


=== END OF PART ===
