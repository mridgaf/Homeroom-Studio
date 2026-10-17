# Chapter 09: Reason 12 manual digest and studio workflow
## Part 37 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 28 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 38 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 28 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      1. Select a track in the sequencer Track List rack and choose “Select All” from the Edit menu or track context
         menu.
          Tracks are marked with darker colors to indicate they’ve been selected.
      2. Select “Sort Selected Device Groups” from the Edit menu or track context menu.
          Now all Device Groups and channel strips in the Main Mixer will be automatically re-ordered according to the cur-
          rent track configuration in the sequencer. The topmost sequencer track will have its associated Device Group
          moved to the top in the rack. The remaining Device Groups will be re-ordered according to the remaining track or-
          der in the Track List. The Main Mixer channel strips will also be re-ordered according to the sequencer track order.
      • If you have devices in several rack columns, the sorting will begin in the leftmost rack column and continue to
        the right through the rest of the rack columns. The number of devices in each rack column will not be changed.
      • If you select several Device Groups in the rack and choose “Sort Selected Device Groups” from the Edit menu
        or device context menu, the tracks in the sequencer and the Main Mixer channel strips will be re-ordered ac-
        cording to the current Device Group order in the rack.
      • If you select several channel strips in the Main Mixer and choose “Sort Selected Device Groups” from the Edit
        menu or channel strip context menu, the Device Groups in the rack and the tracks in the sequencer will be re-
        ordered according to the current channel strip order in the Main Mixer.

      Replacing devices
      If you want to replace an Instrument, Effect or Player device in the rack with another device of the same category,
      proceed as follows:
      1. Bring up the Device Palette in the Browser for the desired device type (Instruments, Effects or Players).
      !   Utility devices cannot be replaced using these methods!
      2. Drag the desired device from the Device Palette to the rack and place on top of the device you want to replace.
          The device to be replaced is dimmed in orange and gets a “replace” symbol in the center:

          Replacing a Subtractor with a PX7 FM Synthesizer device.
      3. Release the mouse button to replace the device in the rack.
          The new device is automatically routed like the previous device. The Mix Channel now also gets the name of the
          current patch in the new device. The new device also gets “browse focus” in the Browser, see “Loading patches”.
      D   You can also drag and drop devices on existing device icons in the Sequencer Track List. The result is exactly
          the same as dropping devices on existing devices in the rack.

      D   You can also drag other device patches from the Browser, Windows Explorer or Finder (Mac) and drop on a de-
          vice in the rack or Sequencer Track List to replace existing devices, see “Loading patches”.
      !   Note that Instrument devices can only be replaced by other Instrument devices. The same goes for Effect de-
          vices.

      Duplicating devices
      Duplicating devices will have different results depending on the “Auto-group Devices and Tracks” setting on the Op-
      tions menu (see “About Device Groups”):
      D   To duplicate a device or a Device Group in the rack, hold down [Ctrl](Win) or [Option](Mac) and drag the device
          to a new position.
      • If “Auto-group Devices and Tracks” is not selected, a copy of the selected device will be created without any
        connections.
      • If “Auto-group Devices and Tracks” is selected, a copy of the entire Device Group will be created with all con-
        nections preserved. A new track will also be created in the sequencer.
      D   Select the device(s) and select “Duplicate Devices and Tracks” from the Edit menu or context menu.
          A duplicate (copy) of the device(s) or Device Group(s) will be created. New tracks for the device(s) or Device
          Groups will also be created in the sequencer.
      D   If you hold down [Shift] when you duplicate devices, Reason will attempt to automatically route them, just as
          when you move devices.
          See “Automatic routing”.

      Cut, Copy and Paste devices
      Selected devices or Device Groups can be moved or duplicated using the Cut, Copy and Paste Device functions on
      the Edit menu or device context menu. This allows you to copy one or several devices (such as an instrument device
      and all its “insert” effects) from one Reason Song document to another. Cutting/Copying and Pasting will have differ-
      ent results depending on the “Auto-group Devices and Tracks” setting on the Options menu (see “About Device
      Groups”):
      • Cut and Copy affects all selected devices or Device Groups, and works according to the standard procedures.
          That is, Cut moves the devices/Device Groups to the clipboard (removing them from the rack) while Copy creates
          copies of the devices/Device Groups and puts these in the clipboard memory, without affecting the rack.
      D   To Cut, Copy and Paste a Device Group, make sure the “Auto-group Devices and Tracks” is selected on the Op-
          tions menu. Then, select a device in the Device Group and proceed with the Cut/Copy and Paste procedure.
          All devices in the Device Group will be cut/copied and pasted with preserved connections (in the same Song or in
          another Song document).
      • When you Paste devices or Device Groups, these are inserted into the rack below the currently selected device.
          If no device is selected, the pasted devices/Device Groups will appear at the bottom of the rack column.
      !   As when creating devices, you cannot paste a Source device into an existing Device Group if “Auto-group De-
          vices and Tracks” is on. It will be inserted below the Device Group.
      • If you Copy and Paste several devices, any connections between these are preserved.
      • If you hold down [Shift] when you Paste a device, Reason will attempt to automatically route it.
          The rules are the same as when moving or duplicating devices by dragging and dropping. See “Routing Audio and
          CV” for more information about automatic and manual routing.

      Naming devices
      Each device has a “tape strip” which shows the name of the device. When you create a new device it is automatically
      named according to the current patch in the device. Devices that don’t use patches are automatically named accord-
      ing to the device type, with an index number (so that the first ID8 device r you create is called “ID8 1”, the next “ID8
      2” and so on). If you like, you can rename a device by clicking on its tape strip and typing a new name (up to 16 char-
      acters).

      For instrument devices connected to Mix Channel devices, the device names are automatically copied to the tape
      strips for the corresponding Mix Channel devices and their channel strips in the Main Mixer, as well as on their corre-
      sponding sequencer tracks. Similarly, the names of the FX Returns in the Main Mixer show the names of the effect
      devices connected to the corresponding FX Return inputs.
      • When you create a device for which an associated sequencer track is created, the track in the sequencer will be
        assigned the same name as the device. Renaming the device will also rename the corresponding sequencer
        track, and vice versa.
      • Note that the mixer channel tape strips always show the patch name (or device name) of the source device
        connected to the Mix Channel device! This means that if you have an instrument device routed through one or
        several effect devices, the Mix Channel tape strip will show the name of the instrument device (as this is the
        Source device).
      • You can rename Mix Channels manually, for example, if you use multiple outputs from a sampler device going
        to separate Mix Channels. If you later delete the custom name, the Mix Channel will default to showing the
        Source device's name. For audio tracks, the Audio Track device is always the Source device and will never
        change name unless you manually rename it.
      • If you delete your custom device name, the name reverts back to the default name, i.e. the patch name or de-
        vice name (for non patch devices).

      Folding and unfolding devices
      If you don’t need to edit the parameters for a device, you can fold the device to make the rack more manageable and
      to avoid having to scroll a lot.
      D   Click the “Fold/Unfold” button to the left on the device panel to fold the device.

          The “Fold/Unfold” button on an RV7000 device.
      D   To unfold the device, click the “Fold/Unfold” button again.
      • In rack rows containing devices of smaller width, the “Fold/Unfold” button is placed to the left of the leftmost
        device and affects all devices in the row:

          The “Fold/Unfold” buttons for devices of smaller width.
      D   Hold down [Alt](Win) or [Option](Mac) and click the “Fold/Unfold” button of an unfolded device to fold all de-
          vices in the current rack column.
          Conversely, hold down [Alt](Win) or [Option](Mac) and click the “Fold/Unfold” button of a folded device to unfold
          all devices in the current rack column.
      • For folded devices, no parameters are shown and you cannot reroute any cables on the rear of the rack as long
        as the devices are folded.
          However, if you want to make a connection to a folded device, you can drag a cable to it and hold it there for a mo-
          ment. This will cause the folded device to automatically unfold and let you make the connection.
      • Folded devices can be renamed, moved, duplicated and deleted just like unfolded devices.
      • For devices that use patches, you can select patches in folded mode as well.
      • Playback is not affected by folding.


---

<a id="working-with-players-12"></a>

=== END OF PART ===
