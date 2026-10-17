# Chapter 09: Reason 12 manual digest and studio workflow
## Part 60 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 51 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 61 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 51 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Removing Remote Overrides
      This can be done for a selected parameter in the following way:
      1. In Remote Override Edit Mode, select the parameter you wish to remove Remote Override for.
          The lightning bolt changes to orange, indicating it is selected.
      2. Select “Clear Remote Override Mapping...” from the Edit menu.
          You can also right-click (Win) or [Ctrl]-click (Mac) on the parameter to select the same item from the context
          menu. This is always available, regardless whether Remote Override Edit mode is selected or not.
      Or you can remove all Remote Overrides for a device in one go:
      1. Select the device you wish to remove Remote Override for.
      2. Select “Clear All Remote Override Mappings for Device” from the Edit menu.
          You can also right-click (Win) or [Ctrl]-click (Mac) on the device panel to select the same item from the context
          menu.

      Copying/Pasting Remote Overrides
      You can copy Remote Override mappings for a device and paste them into a device of the same type. This works as
      follows:
      1. With Remote Override Edit mode activated, select the device you want copy Remote Override mappings from,
         and the select “Copy Remote Override Mappings” from the Edit menu.
          You can also right-click (Win) or [Ctrl]-click (Mac) on the device panel to select the same item from the context
          menu.
      2. Select the device you wish to paste the copied mappings to.
          It has to be the same type of device you copied from. In case you copied Remote Override mappings from the
          Transport panel you can thus only paste the mappings into another song document.
      3. Select “Paste Remote Override Mappings” from the Edit menu.
      Now the following happens:
      D   If you are pasting in the mappings into a device in the same song document, a dialog appears informing that
          the overrides are already used.
          You then have the choice of canceling the operation, or to move the existing overrides to the new device.
      D   If you are pasting into a device in another song, the copied Remote Override mappings are simply pasted.
          In this case, the original Remote Override mappings are not affected.

      Additional Remote Overrides...

      On the Options menu there is an item named “Additional Remote Overrides...”. Selecting this opens a dialog with re-
      mote functions that cannot be assigned using Remote Override Edit mode, such as switching target tracks, Undo/
      Redo etc. Although most of the items in this dialog are self-explanatory, some need to be described. These are as fol-
      lows:

      Target Track Delta and Target Previous/Next Track
      D   Target track is the track with Master Keyboard Input.
          Assigning Target Previous/Next Track to two Button controls on a control surface allows you to move the Master
          Keyboard Input symbol up or down in the Track list.
      D   Target Track Delta is meant to be used with Delta wheel controllers (a special control with no min/max range)
          to switch target track.
          A Mackie Jog wheel is an example of this type of controller.
      D   Select Previous/Next Track can be assigned to standard button controls.

      Select Patch for Target Device and Select Previous/Next Patch for Target Device
      The target device is the device connected to the target track.
      D   Patch selection is usually standard-mapped to buttons on a control surface.
          If you wish to override this standard patch selection mapping for devices globally to select patches for any patch
          device that currently has Master Keyboard Input, you can assign this here.
          For example, you may always want to use the same buttons on a specific control surface for selecting patches.
      D   Select Patch for Target Device is also meant to be assigned to a Delta-type control (see above).
          This allows you to select patches for a device connected to the target track by spinning the wheel clockwise or
          anti-clockwise.
      D   Select Previous/Next Patch can be assigned to standard button controls.

      Select Keyboard Shortcut Variation (Delta)/Select Previous/Next Keyboard Shortcut
      Variation
      By mapping controls to these, you can use your control surface to change which keyboard shortcut variation is se-
      lected in Reason.
      • The "Select Previous/Next” functions are typically mapped to buttons, allowing you to step between keyboard
        shortcut variations.
      • The Delta function must be mapped to a delta-type control to work.
      • The keyboard shortcut variation selection is a global setting in Reason. It affects all added control surfaces (if
        they make use of keyboard shortcut variations and aren't locked to a specific device and variation in the Sur-
        face Locking dialog).

      Undo/Redo
      You can assign Undo/Redo to controls. This works just like the corresponding items on the Edit menu.

      Document Name
      This allows you show the name of the song in the display of the control surface. This only works for control surfaces
      that support this feature.

      Assigning Additional Overrides
      Assigning overrides in this dialog is similar to assigning standard Remote Overrides:
      1. Select a function/parameter in the list that you wish to assign to a control and click “Edit”.
        This opens the Edit Remote Override Mapping dialog, where you can assign a control to the selected function/pa-
        rameter. You can also simply double click the item in the list to open this dialog.
      2. Click OK to close the dialog.

      Clearing Additional Overrides
      1. Select “Additional Remote Overrides” from the Options menu.
        In the Mapping column you can see which parameters/functions use overrides.
      2. Select the item currently assigned override mapping, and click “Clear”.

      Keyboard Control
      Assigning computer keyboard remote commands does not involve MIDI, so there is no special setting up required.
      Keyboard commands can be assigned to parameters just as when using Remote Override mapping, but the function-
      ality differs in one central aspect:
      • Keyboard Control commands can only be used to toggle on/off or min/max values for an assigned parameter.
      Hence, if you assign a computer keyboard remote command for a knob, slider or spin control, it will only switch be-
      tween the minimum and maximum values for that parameter. The only exception to this are the multi-selector buttons
      used for various parameters such as envelope destination, for example. These will cycle through the available options
      when using keyboard control.
      !   Note that Keyboard Control cannot be used for the ReGroove Mixer parameters.

      Enabling Keyboard Control
      To enable Keyboard Control, select “Enable Keyboard Control” from the Options menu.

      Editing Keyboard Control
      D   To get an overview of which parameters are remote controllable select “Keyboard Control Edit Mode” from the
          Options menu.
          When done, each device you select in the rack will show a yellow arrow symbol beside every parameter that can be
          assigned a keyboard control.

          A section of a Redrum drum machine with Keyboard Control Edit Mode enabled.
      !   The Main Mixer channel strip parameters can also be controlled using the Keyboard Control function, but there
          is no Edit Mode for this. Instead, you have to right-click (Win) or [Ctrl]-click (Mac) on individual channel strip
          parameters and select “Edit Keyboard Control Mapping” from the context menu.

      D   If you click on an assignable parameter to select it, you can then select “Edit Keyboard Control Mapping” from
          the Edit menu.
          This opens a dialog allowing you to select a key command for that parameter.
          You may use any key except the [Space bar], [Tab], [Enter], the Numeric keypad keys (which is reserved for Trans-
          port functions) and the function keys (except [F2] and [F3]) - or a combination of [Shift] + any key (with the same
          aforementioned exceptions).

          The Keyboard Control dialog.
      D   Simply press the key (or Shift-key combination) you wish to use to remote control the parameter.
          The “Key Received” field momentarily indicates that it is “learning” the keystroke(s), and then the dialog displays
          the name of the key you have pressed. If [Shift] was used, the box beside the word Shift in the dialog is ticked.
      You can also double-click on the arrow for an assignable parameter to set up keyboard control:
      D   A rotating yellow rectangle appears, indicating Learn mode. Press the key (or key combination) you wish to
          use to control the parameter.
          The rotating stops and the rectangle will now display the key or key combination you used.

      About the two Edit Keyboard Control Modes
      If Keyboard Control Edit Mode is enabled (ticked) on the Options menu, assigned parameters in the rack are
      “tagged”, showing the remote key for that parameter. In this mode, however, you cannot operate Reason normally.
      This mode is primarily for overview of available parameters and the current assignments.
      D   Another way to assign keyboard remote commands is to have “Keyboard Control Edit Mode” deselected on
          the Options menu, and to simply right-click (Win) or [Ctrl]-click (Mac) the parameter you wish to remote con-
          trol.
          This opens a pop-up menu, where one of the options will be “Edit Keyboard Control Mapping”. Selecting this opens
          the Keyboard Control dialog. Thus, you do not have to enable/disable Edit mode from the Options menu if you
          know that a parameter is assignable.
      !   This is the only way Main Mixer channel strip parameters can be assigned to Keyboard Control.

      Saving Remote Setups
      There’s no need to save MIDI Remote mapping as the Standard Remote mapping for each Reason device to sup-
      ported control surfaces is built-in, and is always available. You may, however, wish to save specific Remote Override
      mappings or Keyboard Control setups as a template:
      D   This could be done by saving a song document containing all the devices that are affected by the related Key
          or Remote Override mappings, but without any sequencer data.
          This song document could then be used as a starting point for any new song, by simply loading it, and immediately
          using “Save As” to save it under a new name.
      q   A good idea could be to save these types of “Remote Template” songs in the Template Songs folder. See
          “Making a Song appear as a Template Song” for info on how to do this.


---

<a id="synchronization-and-advanced-midi-24"></a>

=== END OF PART ===
