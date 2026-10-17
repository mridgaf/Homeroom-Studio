# Chapter 09: Reason 12 manual digest and studio workflow
## Part 59 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 50 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 60 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 50 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 23: Remote - Playing and Controlling Devices

Remote - Playing and
Controlling Devices

      About the various MIDI inputs
      This chapter describes how you can use Remote and the Easy MIDI Input function to set up your master keyboard
      and control surfaces, allowing you to play Reason devices, adjust parameters and control various Reason functions.
      This is the main way of sending MIDI to Reason, but there are also some additional methods:
      • Using the External Control Bus inputs.
        The External Control Bus inputs (set up on the Preferences - Sync page and in the MIDI In device in the hardware
        interface) let you send MIDI directly to the individual devices in the rack. This is mainly used if you control Reason
        from an external sequencer, etc. See “About the External Control Bus inputs”.
      • Sending MIDI Clock to Reason.
        This allows you to synchronize Reason’s tempo to other devices. See “Synchronization to MIDI Clock”.

      About Remote
      MIDI from control surfaces (keyboards, remote control units etc.) is handled by a protocol called Remote. The Remote
      protocol allows for seamless integration between Reason and control surface devices. It is basically a mapping sys-
      tem that provides direct hands-on control of parameters for each Reason device - including transport and sequencer
      track selection!
      At the time of this writing, Reason supports a large number of control surfaces and keyboards - the knobs, faders and
      buttons on the devices are automatically mapped to parameters on each Reason device.
      Remote drivers for more control surfaces will be added continuously. Check the Reason Studios web page in case
      your model isn’t listed on the Preferences - MIDI page.
      Remote controlling Reason devices couldn’t be made any simpler. Let Reason automatically look for all available MIDI
      Input ports on your computer and automatically connect your master keyboard. Or, manually set up your control sur-
      face for use with Reason - the program handles the rest!

      Setting up
      Automatic set-up using the Easy MIDI Inputs function
      By default Reason automatically scans and detects all available MIDI In port(s) on your computer. If you have a MIDI
      keyboard or MIDI control surface connected to your computer, Reason automatically connects and lets you use it for
      controlling Reason. This way you don’t have to do any manual set-up but can start controlling Reason right away.
      At the bottom of the MIDI tab in Preferences all currently available MIDI In Ports are listed:

      All available MIDI In Ports on your computer are listed in the Easy MIDI Inputs list.
      • The Easy MIDI Inputs function supports input of MIDI Note On/Off (with Velocity) as well as standard perfor-
        mance controllers, such as Mod Wheel, Pitch Bend and Sustain Pedal.
          You can also do manual Remote Overrides to assign Reason parameters to knobs/sliders/buttons on your control
          keyboard/surface, see “Remote Override”.
      D   Deselect the Enabled box(es) to disable MIDI Ports you don’t want to be available for Reason.
          For example, if you have a drum machine connected via USB to your computer, you might not want it to start send-
          ing MIDI Note data to Reason, especially if it’s synced to MIDI Clock to Reason’s sequencer.

      Adding a specific control surface or keyboard
      If your specific MIDI keyboard/control surface model is featured in the list of supported surfaces in Reason you will
      get even more functionality if you add it in the “Remote keyboards and control surfaces” section at the top - with
      knobs/sliders/buttons already pre-assigned to parameters in Reason.
      This is how you add your specific control surfaces - including the master keyboard.
      1. Open the Preferences dialog and click the MIDI tab.
      2. If your control surface is connected via USB (or if you have made a two-way MIDI connection), try clicking the
         Auto-detect Surfaces button.
          Reason sends an ID request to all MIDI ports and checks for answers from any connected control surfaces. Note
          that not all control surfaces support auto-detection.

      !   If a MIDI Port of your connected control surface/keyboard is already used by the Easy MIDI Inputs function
          (see “Automatic set-up using the Easy MIDI Inputs function”), this detection will override this and automati-
          cally remove the MIDI In Port from the Easy MIDI Inputs list.

      3. To add a control surface manually, click the “Add manually” button.
          This brings up a new dialog.
      4. Select the manufacturer of your control surface from the Manufacturer pop-up menu.
          If you can’t find it on the menu, see below.
      5. Select the model of your control surface from the Model pop-up menu.
          If you can’t find it on the menu, see below.

      6. An image of the selected control surface model is shown, often along with some information text - read this
         carefully.
          For some control surfaces, you need to select a specific preset to use the surface with Reason - this is noted here.

      7. Use the MIDI Input pop-up to select the input port to which you have connected the surface.
          If in doubt, you can click the Find button and then tweak a control or play a key on the control surface to have Rea-
          son find the correct input port for you.
      • Some control surfaces may have more than one MIDI Input pop-up menu.
          You need to select ports on all MIDI Input pop-up menus.
      • Some control surfaces will have a MIDI Output pop-up menu.
          In some cases this labeled “Optional” - then you don’t have to make a selection. In other cases, a MIDI Output is re-
          quired. This is the case if the control surface uses MIDI feedback - motor fader, displays, etc.
      • Reason only “grabs” the MIDI inputs you are actually using.
          MIDI inputs not selected here or on the Sync page (see “Advanced MIDI - The External Control Bus inputs”) are
          available to other programs.
      !   Note that other MIDI programs may “grab” all MIDI ports in your system when you launch them!
      8. If you like, you can rename your control surface in the Name field.
      9. Click OK to add the surface.
      • Depending on the surface model, alerts may appear, reminding you to select a specific preset etc.
          In some cases, Reason can restore a preset in the control surface to factory settings for you. In such cases you will
          be informed about this.
      Finally you return to the MIDI tab in Preferences, where your added surface is now listed.

      If your control surface model isn’t listed
      If you can’t find your control surface listed on the Manufacturer or Model pop-up menus when you try to add it, this
      means that there’s no native support for that model. However, the program supports generic keyboards and control-
      lers. These alternatives might be more useful than the Easy MIDI Input alternative described earlier - if you have a
      control surface (or keyboard with knobs/buttons/sliders) that you want predefined parameter destinations for. Here’s
      what to do:
      D   Select “Other” on the Manufacturer pop-up menu and then one of the three options on the Model pop-up
          menu.
      or, if the Manufacturer is listed but not your specific model:
      D   Select one of the three “Other” options on the Model pop-up menu:
      In both cases, the options are:
      • MIDI Control Keyboard
          Select this is you have a MIDI keyboard with programmable knobs, buttons or faders. You need to set up your con-
          trol keyboard so that the controls send the correct MIDI CC messages, depending on which Reason device you
          want to control - check out the MIDI Implementation Chart. If your control keyboard has templates or presets for
          Reason devices, these can be used if you run Reason.
      • MIDI Control Surface
          Select this if you have a MIDI controller with programmable knobs, buttons or faders (but without keyboard).
          You need to set up your control surface so that the controllers send the correct MIDI CC messages, depending on
          which Reason device you want to control - check out the MIDI Implementation Chart. If your control surface has
          templates or presets for Reason devices, these can be used if you run Reason.
      • MIDI Keyboard (No Controls)
          Select this is you have a MIDI keyboard without programmable knobs, buttons or faders. This is used for playing
          only (including performance controllers such as pitch bend, mod wheel, etc.) - you cannot adjust Reason device
          parameters with this type of control surface.
      • MIDI Multichannel Control Keyboard
          Select this is you have a MIDI keyboard with programmable controls that use multiple MIDI channels (different
          controls send the same MIDI CC but on different MIDI channels). With this model there is no automatic mapping
          to device parameters - you need to use Remote Overrides to map each control to a parameter on a device.
      • MIDI Multichannel Control Surface
          Select this is you have a MIDI control surface with programmable controls that use multiple MIDI channels (differ-
          ent controls send the same MIDI CC but on different MIDI channels). With this model there is no automatic map-
          ping to device parameters - you need to use Remote Overrides to map each control to a parameter on a device.
      After selecting a model, proceed with selecting MIDI input port as described above.

      About the Master Keyboard
      One of the control surfaces can be the Master Keyboard. This is like any other control surface, but it must have a key-
      board and it cannot be locked to a specific Reason device (in other words, it always follows the MIDI input to the se-
      quencer). This is the surface you use to play the instrument devices in Reason.
      D   The first surface with a keyboard that is added (manually or auto-detect) is automatically selected to be the
          master keyboard.
          This is shown in the “Remote keyboards and control surfaces” list on the Preferences page.
      D   If you want to use another surface as master keyboard, select it in the list and click the “Make Master Key-
          board” button.
          You can only have one surface as master keyboard at a time.
      D   If you don’t want to use any master keyboard at all, select the current master keyboard surface and click the
          same button (which is now labeled “Use No Master Keyboard”).

      Other functions
      D   To edit a surface, double click it in the list (or select it and click Edit).
          This lets you change its name and MIDI port settings, if needed.
      D   To delete a surface, select it in the list and click Delete.
      D   You can turn off a surface by deactivating its “Use with Reason” checkbox.
          This could be useful if the surface is connected to your system but you only want to use it with another program.
      There is also the Sync tab in the Preferences. This is only used for External Control MIDI buses and for MIDI Clock
      Sync settings. All hands-on MIDI control is set up on the MIDI tab.

      Example Setups
      There are several possible variables when it comes to what type of setup you are using. Please read on.

      A single MIDI keyboard with controls
      With this setup, the keyboard is your master keyboard, which means it is always routed via the sequencer (it controls
      the device connected to the sequencer track with Master Keyboard Input). To control another device, you move the
      Master Keyboard Input (the keyboard symbol in the In column in the track list) to another sequencer track.
      You can, however, use Remote Override to control parameters on other Reason devices (or global Reason functions
      such as transport).

      A basic MIDI keyboard and an additional control surface
      The keyboard and the control surface should be connected to separate MIDI ports (or use separate USB connec-
      tions). Here, the basic MIDI keyboard is your master keyboard - it is used for playing and recording via the sequencer.
      You can have the control surface follow the master keyboard - this lets you tweak the parameters of the device you
      are playing (just like in the example above).
      You can also lock the control surface to another device in the rack - this lets you play one device while adjusting the
      parameters of another.

      A MIDI keyboard with controls plus one or more control surfaces
      This is the ideal setup! Again, all keyboards and control surfaces should be connected to separate MIDI ports (or use
      separate USB connections). The master keyboard is routed via the sequencer track and you can use its controls to
      tweak the parameters of the device you are playing. The additional control surfaces could be locked to the Main
      Mixer or to different devices in the rack.
      If you have additional MIDI keyboards locked to devices in the rack, you can also play and record on their correspond-
      ing sequencer tracks simultaneously. This is perfect if your band has several keyboard players who want to play and
      record their tracks simultaneously into Reason!
      For example, if you lock a control surface to the Main Mixer, you will always have control over levels, pans and addi-
      tional channel strip parameters - see “Remote controlling the Main Mixer” and “Remote controlling multiple mixer
      channels”. You could also have dedicated controls for transport, Undo/Redo, sequencer track MIDI focus selection,
      etc.

      Remote basics
      Parameters and functions for each Reason device are mapped to controls on supported control surface devices. As
      soon as you have added your control surface(s) in the Preferences, you can start tweaking parameters!
      • By default, all connected control surfaces follow the sequencer’s current Master Keyboard Input.
          This means that you set Master Keyboard Input to a track in the sequencer to route the control surface(s) to the
          track’s device in the rack. You can bypass this functionality by locking a control surface to a specific device - see
          “Locking a surface to a device”. Or you can simply use Remote Override mapping (see “Remote Override” for spe-
          cific parameters - these will then be mapped to the selected controls regardless of Master Keyboard Input.
      • The Reason device associated with the track with Master Keyboard Input will have its parameters standard
        mapped to logical controls (faders, buttons etc.) on the control surface device.
          E.g. if a Subtractor has Master Keyboard Input, your control surface will control the most important Subtractor pa-
          rameters. If you set Master Keyboard Input to a track connected to an NN-XT, the control surface will now control
          parameters on the NN-XT device, and so on for each device. There are standard mapping variations for most de-
          vices as well - see “About mapping variations”.
      • Supported control surfaces with dedicated transport controls will be standard mapped to the equivalent trans-
        port controls in Reason.
          If you do not have transport controls on your control surface you can still map transport controls to controllers us-
          ing Remote Override mapping - see “Remote Override mapping”.
      • Other important functions such as switching target track in the sequencer, selecting patches, Undo/Redo can
        also be remote controlled.
          See “Additional Remote Overrides...”.

      About Standard vs Remote Override mapping
      Reason parameters are “standard-mapped” to supported control surface devices. There is nothing the user needs to
      set up to remote control any Reason device. You can, however, use Remote Override mapping to map a specific pa-
      rameter to a specific control if you should want to.
      D   By using standard mapping, the remote mapping for each device will be the same for any new song created in
          Reason, given you have the same set of control surfaces connected.
          If you use Remote Override mapping (see “Remote Override”), the overrides will be saved with the current song,
          but won’t be there if you create a new song.
      D   Which parameters and functions that are standard mapped for each Reason device depends on the control
          surface(s).
      The “Control Surface Details” document contains some information about the standard mappings of the different
      control surface models. But you can also activate Remote Override Edit mode to see which parameters for each de-
      vice are mapped to your control surface(s) - see “Remote Override”.
      D   Note that if you have several control surfaces connected, some parameters could be mapped to controls on
          more than one control surface.
          This is not a conflict of any kind, but simply a consequence that stems from the fact that all control surfaces by de-
          fault follow Master Keyboard Input. By using Surface Locking (see below) or Remote Override (see “Remote Over-
          ride”) you have full control over your control surfaces.

      About mapping variations
      Since there are often more parameters on a device than there are controls on the control surface, there are standard
      mapping variations available for most devices. When selecting a standard mapping variation, a new set of parameters
      will be mapped to the controls on your control surface for a selected Reason device.

      For example, if you have a control surface with 8 rotary knobs routed to a Subtractor, the knobs may control filter pa-
      rameters by default. Selecting variation 2 may make the knobs control the oscillator settings, variation 3 may control
      LFOs and so on.
      D   For devices that support keyboard shortcuts, you switch between mapping variations by holding down [Ctrl]+
          [Alt](Win) or [Cmd]+[Option](Mac) and press the numerical keys [1] to [10] (not the numerical keypad), where
          [1] selects the default standard mapping.
          How many mapping variations are available depends on the control surface and the Reason device selected. The
          variation selected will stay active until you switch MIDI input to another device (or select another variation). If you
          switch back to the same device it will have its default standard mapping (variation [1]).
      D   For control surfaces that have dedicated controls for selecting mapping variations these are used instead of
          keyboard shortcuts.
      D   Locked devices (see “Locking a surface to a device”) can also be locked to a specific mapping variation.

      Locking a surface to a device
      You can lock a control surface or an additional MIDI keyboard/controller to a specific device so that it is always
      “tweakable” and record enabled, regardless of which track has Master Keyboard input in the sequencer. This enables
      you to play and record notes for several devices simultaneously from multiple control surfaces/keyboards.
      For example, you could lock a control surface to control the Main Mixer, so you can always control overall levels while
      playing/tweaking other devices. See “Remote controlling the Main Mixer” for an example.
      • The master keyboard device cannot be locked!
          If you select the master keyboard in the Preferences, you can click the “Use No Master Keyboard” button. You can
          then lock this control surface to a device and use its controllers to tweak parameters, but you will not be able to
          play the device.
      • You can lock several control surfaces to the same device.
          However, each control surface can only be locked to one device at a time.
      • Info about which devices are locked (and to which control surfaces) is saved with the song.
      !   Control surfaces/keyboards that use the Easy MIDI Inputs function (see “Automatic set-up using the Easy
          MIDI Inputs function”) cannot be locked to devices.

      Locking a surface
      There are basically two methods you can use to lock a Surface:

      Using the Surface Locking dialog
      1. Select “Surface Locking...” from the Options menu.
          The Surface Locking dialog opens.

          In this picture, the dialog has the master keyboard as the selected control surface - this cannot be locked.

      2. Pull down the Surface pop-up from at the top of the dialog and select the control surface you wish to lock to a
         device.

      3. Next, open the “Lock to device” pop-up menu.
          On this pop-up, all devices in the current song are listed. The “Follow Master Keyboard” item which is selected by
          default, means that the control surface isn’t locked (it instead follows the Master Keyboard Input in the sequencer).

      4. Select the device you wish to lock to the selected control surface from the list.
      D   If the selected control surface supports keyboard shortcuts for selecting mapping variations (see “About map-
          ping variations”) an additional “Always use Mapping” pop-up appears.
          On this pop-up you can set whether you wish to lock a specific standard mapping variation or whether the device
          should switch mapping variations according to keyboard shortcuts. If the former is the case, select the mapping
          variation from the list. If the latter is the case, select “Follow Keyboard Shortcut”.

      5. Close the dialog when you are done.
          The device is now locked to the selected control surface. In Remote Override Edit mode (see “Activating Remote
          Override Edit mode”) a locked device is shown with a lock symbol in the upper left corner of the device panel.

      q   It’s also possible to lock a control surface to the ReGroove Mixer (see “The ReGroove Mixer”) to control its pa-
          rameters via Remote!

      Using the context menu
      D   A quick way to lock devices is by right-clicking (Win) or [Ctrl]-clicking (Mac) on a device panel to bring up the
          context menu.
          On the context menu, all installed control surfaces (apart from the master keyboard) are listed with the text “Lock
          to” plus the name of the control surface. Selecting one will lock the device to the control surface. On the context
          menu the control surface that is currently locked to this device will be ticked.

      Unlocking a surface
      D   To unlock a locked device, bring up the context menu for the locked device, and untick the “Lock to” item.’
          This unlocks the device and the control surface will now follow master keyboard input.
      D   Another way to unlock a surface is to open the Surface Locking dialog and selecting “Follow Master Key-
          board” on the Lock to device pop-up.

      Remote Override
      Remote Override allows you to map parameters and functions to controls on your control surface device, overriding
      the standard mapping. It also allows you to control device parameters from Easy MIDI Inputs (that has no standard
      mapping).

      Activating Remote Override Edit mode
      1. Select “Remote Override Edit Mode” from the Options menu.
        All unselected devices in the rack are grayed out, indicating Edit mode. Each selected device (including the Trans-
        port panel) will show a blue arrow symbol on every parameter that can be mapped to a control on a control surface.

        Remote Override Edit mode enabled with the mixer device selected.
      To be able to see which parameters are currently mapped for a device, you have to direct Master Keyboard input to
      the sequencer track it is connected to:
      2. Select a device in the rack and enable Master Keyboard input for its sequencer track.
        Standard-mapped parameters are tagged with yellow knob symbols.

        A Subtractor with standard-mapped parameters.

      D   Note that you can select the Transport Panel as well!
          Most items on the Transport panel can be mapped to controls. Note that by selecting the Transport panel any
          standard mapping will be shown automatically, unlike other devices where you have to first direct Master Keyboard
          input to the device from the sequencer.
      D   If you point on a standard mapped parameter, a tooltip appears showing which control on the control surface
          device the parameter is mapped to.

      Remote Override mapping
      If Remote Override Edit Mode is enabled you can use the following methods to map a parameter to a control:

      Method 1:
      1. Select the parameter you wish to map.
          The arrow (or knob) changes to orange, indicating it is selected.
      2. Select “Edit Remote Override Mapping...” from the Edit menu.
          You can also right-click (Win) or [Ctrl]-click (Mac) on the parameter to select the same item from the context
          menu.
          The “Edit Remote Override Mapping” dialog opens. From here you have two ways to proceed:

      D   Either manually select the control surface and the control you wish to map the parameter to from the two cor-
          responding pop-ups.
          The Control Surface pop-up lists all installed control surface devices, and the Controls pop-up lists all the mappa-
          ble controls for the selected control surface.
      D   Or you can activate “Learn From Control Surface Input” and simply move (or press) the control you want to
          map the parameter to.
          The “Control Surface Activity” field momentarily flickers as you turn the knob, and then the dialog shows the con-
          trol surface and control it is mapped to.
      D   If the control surface has a keyboard, you can also select keys as controls.
          Keys work just like on/off buttons. If “Keyboard” is selected from the Controls pop-up, a Note Number field ap-
          pears in the dialog.

      3. Click OK to exit the dialog.
          The mapped parameter now shows a lightning bolt icon, indicating it uses Remote Override mapping. Any over-
          rides are always shown in Remote Override Edit mode. The device does not have to be selected or have Master
          Keyboard Input in the sequencer.

      4. To exit Remote Override Edit Mode, deselect it from the Options menu.
          You can also leave this mode by pressing [Esc].

      Method 2:
      1. Double-click the parameter you wish to map.
          A rotating lightning bolt appears for the parameter - this indicates that “Learn From Control Surface” mode is ac-
          tive. You can leave this mode by pressing [Esc].
      2. Now move (or press) the control you want to map the parameter to.
          The parameter is now mapped to the control.
      You do not always have to edit override mapping when Remote Override Edit mode is activated - see below.

      Override mapping with Remote Override Edit mode deactivated
      If Remote Override Edit Mode is enabled on the Options menu, mapped parameters are “tagged”, and the arrow indi-
      cators show the assignable parameters. In this mode, however, you cannot operate Reason normally. Remote Over-
      ride Edit mode is primarily for overview of available parameters and the current assignments.
      D   Another way to map parameters is to have “Remote Override Edit Mode” deactivated on the Options menu,
          and to simply right-click (PC) or [Ctrl]-click (Mac) on the parameter you wish to remote control.
          This opens a pop-up menu, where one of the options will be “Edit Remote Override Mapping”. Selecting this will
          open the Edit Remote Override Mapping dialog. Thus, you do not have to select Edit mode from the Options menu
          if you already know that a parameter is free and assignable.


=== END OF PART ===
