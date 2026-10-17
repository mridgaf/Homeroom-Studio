# Chapter 09: Reason 12 manual digest and studio workflow
## Part 36 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 27 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 37 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 27 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 11: Working with the Rack

Working with the Rack

      About this chapter
      This chapter describes the procedures and techniques for managing devices and Device Groups in the rack.

      Rack device procedures
      The rack is where you create and configure your devices, and make parameter settings. This section describes all the
      procedures for managing the rack, that is, procedures and techniques common to all devices.

      Navigating in the rack

                                                                                                                Rack
                                                                                                                Navigator

          Rack Column 3                                 Rack Column 2                          Rack Column 1

      The rack, here with three rack columns visible.
      The rack houses all the devices you use in your song. To make it easier to overview the devices, the rack can contain
      several rack columns next to each other. To navigate in the rack, use one of the following methods:
      D   Click and drag the blue frame in the Rack Navigator to scroll continuously in the rack, both vertically and hori-
          zontally.
          Just clicking in the Rack Navigator will directly scroll to the corresponding position in the rack.
      D   If you’re using a mouse equipped with a scroll wheel, you can use it to scroll up or down in the rack.
          Hold down [Shift] and use the scroll wheel to scroll horizontally in the rack.
      D   Press the [Page Up] and [Page Down] buttons on the computer keyboard to move the view one “full screen” up
          or down in the rack column currently in view.
          Note that the rack area must have Edit Focus, i.e. there must be a frame surrounding the rack area. Set Edit Focus
          by clicking anywhere in the rack area.
      D   Press the [Home] and [End] buttons on the computer keyboard to scroll the top or bottom of the rack column
          currently in view.
          Note that the rack area must have Edit Focus.
      q   When you select a track in the sequencer, or click the “Rack” button below a channel strip in the Main Mixer,
          the rack will automatically scroll to bring the associated device into view.

      Resizing and detaching the rack

      D   Resize the rack area by clicking and dragging either of the gray horizontal headers above or below the rack
          area, or by dragging the vertical Browser divider.
          This will shrink the Main Mixer and/or sequencer areas and make more of the rack visible.
      D   You can also resize the Rack Navigator area by clicking and dragging the vertical divider to the left of the Rack
          Navigator.
          Dragging the divider to the left will expand the Rack Navigator area and enlarge the devices, making it easier to
          get a good overview of all devices in your rack.
      D   To make the rack fill the entire song document window, press [F6] or double click the gray Rack header:

          The rack header.
      D   To toggle between show and hide rack, click the Show/Hide icon to the left on the gray rack header:

          The Show/Hide icon on the rack header.
      D   You can detach the rack area from the other areas altogether by holding [Ctrl](Win) or [Cmd](Mac) and press-
          ing [F6], or by clicking the “Detach” icon in the gray rack header.
          This will place the rack in a separate window. (See “The Rack” for more info.)

                                                                                                          Detach button

          The rack Detach icon.
      q   See also “Creating new rack columns” for information on how to create several rack columns.

      About using the Browser in the detached rack
      When the rack is detached, it also features a second instance of the Browser. The Browser is available to the left in
      the detached rack.
      D   Click the Show/Hide icon, or press [F3] to bring up the Browser (or to hide it):

          The Show/Hide icon on the Browser header in the detached rack.
      • The Browser in the detached rack can be navigated independently from the Browser in the Song window, ex-
        cept only one can have browse focus at a time (see “Setting browse focus”).
          This means you can be in two completely different locations (or palettes) in the two Browsers.

      About Device Groups
      A Device Group is a series of interconnected devices that “belong together”. A Device Group could be, for example,
      an instrument device connected to an effect device and then to a Mix Channel device.
      A Device Group consists of the following:
      • One (and only one) Source device (e.g. an instrument).
      • The devices to which the Source device feeds its audio signals (e.g. and effect device).
      • Any CV-only devices (a Matrix Sequencer, for example) that are CV-connected to devices in this group only.
      • All sequencer tracks and Main Mixer channel strips for the devices in the group.
      !   A Device Group is only defined by the connections between the devices - it has nothing to do with the physical
          location of the devices in the rack.
      By default, when you create an Instrument device, a new (or currently unused) Mix Channel device will be automati-
      cally connected to the Instrument device, as described in “Creating devices”. In this situation, the Instrument device
      and the connected Mix Channel device will now be considered a Device Group - with the Instrument device as the
      Source device.

      If you want to keep all devices in a Device Group physically together in the rack (e.g. if you want to move all devices
      in the group), there is an option “Auto-group Devices and Tracks” on the Options menu.

      The “Auto-group Devices and Tracks” option.
      The advantage of using the “Auto -group Devices and Tracks” option is that it’s much easier to get a good visual over-
      view over what devices are connected to each other and associated with specific sequencer tracks and with a spe-
      cific channel strip in the Main Mixer. It’s also easier to rearrange devices in the rack since all devices in the Device
      Group will move together if one device in the Device Group is moved.
      The example below shows two ID8 devices connected to one Mix Channel device each. Let’s say you want to move
      the ID8 1 device to another position in the rack. This is what will happen:
      1. Make sure “Auto-group Devices and Tracks” is selected on the Options menu - if not, select it from the menu
         or hold down [Ctrl]+[Shift](Win) or [Cmd]+[Shift](Mac) and press [G].
      2. Click on the ID8 1 device panel (but not on a parameter or display) and drag and drop below the ID8 2 device in
         the rack.
          As you can see, both the ID8 1 device and its connected Mix Channel device are moved together, as a group, to
          the new destination.

                                                                                                              ID8 1
                                                                                                              Device
                                                                                                              Group

                                                                                                              ID8 2
                                                                                                              Device
                                                                                                              Group

                                                                                                              Moved ID8 1
                                                                                                              Device
                                                                                                              Group

      q   If you want to view what devices belong to a specific Device Group, select a device and then select “Select All
          in Device Group” from the Edit menu or context menu.

      Creating devices
      Devices can be created in a number of different ways. These first methods apply to any device types:
      D   Use drag and drop, or double-click a device in any of the device palettes in the Browser.
          The devices are sorted in four different groups: Instruments, Effects, Utilities and Players. The Utilities group con-
          tains device types such as mixers, modulation devices, etc. In each device type group the devices are listed in the
          following sections: Reason Devices, and then by Rack Extension and/or VST manufacturer in alphabetical order.
          The Players group is a little special; it contains a number of MIDI “generators” that can be used when recording In-
          strument tracks in the sequencer, see “Working with Players”.
          A device can be dropped in the rack or in the Track List in the Sequencer. As you drag a device to the rack or Se-
          quencer Track List, a +-sign is shown together with an orange divider to indicate where the device will be placed:

          Adding a PX7 FM Synthesizer device by dragging from the Instruments device palette and dropping in the rack.
      D   Use drag and drop from the Browser, Windows Explorer (Win), Finder (Mac), or double click a patch in the
          Browser.
          When you drop a patch in the rack or in the Track List in the Sequencer the corresponding device is automatically
          created in the rack.
      D   Click the Add Device icon in the rack background and select the desired device from the menu:

      D   Select desired device from the “Create” menu.
          Any device type can be created. The “Create” menu is available both on the main menu and on the rack and device
          context menus and is divided into the three groups Instruments, Effects and Utilities. At the top of each group (In-
          struments/Effects/Utilities) are the devices you create most often. Below are all available devices, on sub-menus
          per manufacturer.
      • When you have created an Instrument or Effect device that can load patches, it automatically gets “browse fo-
        cus” (orange indicators). This means that the Browser automatically displays patches for the device you just
        created. See “Loading patches” for more information.
          Automatic browse focus can be switched off if you like. This is done on the General tab in Preferences, see “New
          devices get browse focus”.
      • When you add a new device, Reason attempts to automatically route it in a logical way.
          For more information about the auto-routing features, see “Automatic routing”.

      Depending on what type of device you’ve created, and also the “Auto-Group Devices and Tracks” setting, the results
      will differ:
      • If “Auto-Group Devices and Tracks” on the Options menu is not selected, the new device is added directly be-
        low the currently selected device in the rack.
          If no device is selected, the new device is added at the bottom of the rack.
      • If “Auto-Group Devices and Tracks” on the Options menu is selected, devices will not be created in the middle
        of existing Device Groups (except if they are effect devices - see “Effect devices specifics”).
          This means a device might not end up below the selected device in the rack, but below that device's Device Group.
      !   See below for information specific to certain device types.

      Instrument device specifics
      The following additional methods can be used for creating Instrument devices:
      D   Select “Create Instrument...” from the Create menu.
          This will show the Instruments palette in the Browser. Here you can choose the Instrument device you want to cre-
          ate - see “Create Instrument/Create Effect”.
      • If you have created an Instrument device, a new sequencer track will be automatically created. Also, a new (or
        unused) Mix Channel device will be connected to the Instrument device. The Mix Channel device’s channel
        strip will appear in the Main Mixer.
          The track, the Mix Channel device and its channel strip will be given the same name as the created Instrument de-
          vice. Master Keyboard Input will also automatically be set to the new track, allowing you to immediately play the
          created Instrument device via MIDI (see “Master Keyboard Input”). By default, the Instrument device and Mix Chan-
          nel device will be treated as a “Device Group” from here on (see “About Device Groups”).
      !   By default, the automatic creation of a sequencer track and Mix Channel device only applies to instrument de-
          vices, not to mixers or effect devices.
      • If you hold down [Alt](Win) or [Option](Mac) when you create an Instrument device (except when you drag and
        drop from the Browser), a sequencer track will not be created.
      • If you hold down [Shift] when you create an Instrument device, there will be no automatic routing or connec-
        tions made.

      Audio Track device specifics
      The following additional methods can be used for creating Audio Track devices:
      D   Select “Create Audio Track” from the Create menu.
          This will create an Audio Track device (with its corresponding channel strip in the Main Mixer) and a sequencer
          track.

      Mix Channel device specifics
      • If you hold down [Alt](Win) or [Option](Mac) when you create a Mix Channel device (from the Create menu or
        Browser), a sequencer track will be created for the device.

      Effect devices specifics
      The following additional method can be used for creating Effects devices:
      D   Select “Create Effect...” from the Create menu.
          This will show the Effects palette in the Browser. Here you can choose the Effect device you want to create - see
          “Create Instrument/Create Effect”.

      The results when creating Effect devices depend on the following criteria:
      • If an Audio Track (device or channel strip), or a Mix Channel (device or channel strip), was selected in the rack
        when you created an effect, the effect device will be added and connected as an insert effect, inside the Insert
        FX container for that Audio Track or Mix Channel device.
      • If an Instrument device was selected in the rack when you created an effect device, the effect device will be
        added and connected as an “insert effect”, between the Instrument device and the Mix Channel device.
      • If a Mixer 14:2 or Line Mixer 6:2 was selected in the rack when you created an effect, the effect device will be
        added and connected as a Send Effect, on the first available Send FX connectors of the mixer device.
      • If you hold down [Alt](Win) or [Option](Mac) when you create an effect device, a sequencer track will be cre-
        ated for the device.
      • If you hold down [Shift] when you create an effect device, the effect device will not be connected.

      Mixer device specifics
      • If you hold down [Alt](Win) or [Option](Mac) when you create a mixer device, a sequencer track will be created
        for the mixer device.
      • If you hold down [Shift] when you create a mixer device, it will not be connected to a Mix Channel device.

      Selecting devices
      Some operations, e.g. cutting, copying, moving and deleting devices (see “Cut, Copy and Paste devices” and “Deleting
      devices”), require that you select one or several devices in the rack. This is done according to the following:
      D   To select a single device, click on it in the rack.
          The selected device is displayed with a colored border (based on the color scheme selected for your operating
          system).

      D   To select several devices, hold down [Shift] and click on the desired devices.
          In other words, [Shift]-clicking a device selects it without de-selecting any other selected devices.
      D   To de-select all devices, click in the empty area at the bottom of, or next to, the rack.
      D   To de-select a device in a multiple selection, hold down [Shift] and click on it.
          All other selected devices remain selected.
      D   You can also use the arrow keys on the computer keyboard to select the device directly above, below or next
          to the currently selected one.
          When you use this method, Reason will automatically scroll the rack so that the selected device is fully visible. This
          is a quick way of “stepping through” the rack. Narrow devices (e.g. half-width devices such as some effects) are or-
          dered left-to-right, i.e. pressing the down arrow key will step through the devices from left to right before moving
          on the next device row.
      D   If you hold down [Shift] when using the up or down arrow keys, the currently selected device will remain se-
          lected.
          This allows you to select a range of devices.
      D   Adjusting a parameter in a device will automatically select the device.
          In other words, you don’t have to select a device as a separate operation before editing its parameters.

      Playing devices from the rack
      When you create an instrument device it automatically gets a corresponding sequencer track, and Master Keyboard
      Input is set to that track so you can play the instrument device from your MIDI keyboard. You can change Master
      Keyboard Input by selecting another sequencer track, but you can also change Master Keyboard Input from the rack.
      This is useful if you, for example, have the rack detached and maximized, so you can’t see the sequencer area.
      When you select a device in the rack it is surrounded by a colored border. At the top left of the border is a Master
      Keyboard Input tab:

      The Master Keyboard Input tab on a selected ID8 device in the rack.
      D   Click the Master Keyboard Input tab to automatically set Master Keyboard Input to the device.
          Master Keyboard input is automatically switched in the sequencer as well and you can now play the device from
          your MIDI keyboard:

          Master Keyboard Input set from the ID8 1 device in the rack.
          When you play the device, incoming MIDI is indicated by the Master Keyboard Input symbols on the device in the
          rack as well as on the sequencer track.
      • If a selected device doesn't have a sequencer track (e.g. effect devices), one will be automatically created if you
        click the Master Keyboard Input tab.

      About selecting all devices in a Device Group
      To select all devices in a Device Group, do as follows:
      1. Select any device in the desired Device Group.
      2. Select “Select All in Device Group” from the Edit menu or context menu.
          All devices in the Device Group will be selected as indicated by the colored borders around the devices.

      Deleting devices
      To delete one or several devices, select them in the rack and use one of the following methods:
      D   Press [Backspace] or [Delete].
          An alert appears asking you to confirm the deletion. Any cable connections to the device will also be deleted (or
          re-routed).
      !   If you have selected a Source device or a Mix Channel device and the “Auto-Group Devices and Tracks” on the
          Options menu is selected, an alert appears asking if you want to delete the device or the whole Device Group,
          including sequencer tracks and channel strips. (See “About Device Groups”).
      D   To delete devices or Device Groups without alerts, hold down [Ctrl](Win) or [Cmd](Mac) and press [Backspace]
          or [Delete].
      D   Select “Delete Devices and Tracks” from the Edit menu or the device context menu.
          An alert appears asking you to confirm the deletion. This will delete the devices together with the associated se-
          quencer track(s) also if the “Auto-group Devices and Tracks” option isn’t selected. (It’s possible to have devices
          without associated tracks but it is not possible to have a sequencer track without an associated device.)
      D   To delete devices and tracks without alerts, hold down [Ctrl](Win) or [Cmd](Mac) before selecting “Delete De-
          vices and Tracks” from the Edit menu or the device context menu.
      !   If you delete a device connected between two other devices, the connection between the two other devices is
          automatically preserved.
      !   The Reason Hardware Interface and the Master Section device at the top of the rack cannot be deleted.

      Re-ordering devices
      If you want to move an instrument device to another position in the rack, you probably also want its Mix Channel de-
      vice and connected effects to move along with it. If the “Auto-group Devices and Tracks” on the “Options” menu is se-
      lected, all devices in the Device Group will follow along when you drag and drop a device included in a Device Group.
      However, it’s still possible to re-order devices within each Device Group. See “About Device Groups” for more details.
      See also “About the “Sort Selected Device Groups” function” for information about automatic sorting of several De-
      vice Groups.
      If the “Auto-group Devices and Tracks” on the “Options” menu is not selected, you can re-order and move devices in-
      dividually in the rack - even outside the Device Groups:
      1. If you want to move more than one device at the same time, [Shift]-click the devices to select them.
      2. Click on the panel of one of the devices (but not on a control or display).
      3. With the mouse button pressed, drag the device(s) to the new destination in the rack.
          An orange line indicates where the device(s) will be positioned. Note that when re-ordering devices with smaller
          width, the line can be to the left of a device (indicating that the moved device will be placed before the other de-
          vice) or to the right of a device (indicating that the moved device will be placed after the other device).

      q   It’s also possible to move devices to a new rack column to the left or right of the original rack (see “Creating
          new rack columns”).
          In this example an RV-7 reverb device is moved to two different destinations:

          In this case, the line
          indicates that the RV-7
          reverb device will be
          placed to the left of the
          phaser.

          This is the result. Note
          that the filter device is
          moved to the left, to fill
          out the gap.

          In this case, the line
          indicates that the reverb
          device will be placed to
          the right of the chorus/
          flanger.

          This is the result. All three
          devices are moved to the
          left, to fill out the gap.

      4. Release the mouse button.
          The device(s) are moved to the new position and the other devices in the rack are adjusted to fill up the gap(s).
      !   Note that if you start to move a device but change your mind, you can abort the operation by pressing [Esc]
          while keeping the mouse button depressed.
      !   Moving devices in the rack does not affect the order of the sequencer tracks or channel strips and vice versa. If
          you want the sequencer tracks and channel strips to be re-ordered as well, see “About the “Sort Selected De-
          vice Groups” function”.

      Re-routing devices
      D   If you hold [Shift] and drag a device to a new position in the rack, it will be re-routed (as if you deleted it and
          created it in its new position).
          This allows you to e.g. change the order of effect devices in a signal chain by Shift-dragging them.
          See “Automatic routing” for more info on auto-routing.

      Creating new rack columns
      It’s possible to move devices, or Device Groups, to new rack columns. This is very useful if your rack starts to get
      crowded, or if you want to arrange your devices in separate rack columns to get a better overview.
      By default, when you create a new empty Song document, the rack consists of a single rack column featuring the
      Reason Hardware Device and the Master Section device. When you create new devices from the “Create” menu,
      these will automatically be placed in that rack column.
      By dragging and dropping devices to either side (left or right) of the original rack, you can move the devices and at
      the same time create a new rack column. You can create as many rack columns as you like - the only condition is that
      at least one device must be present in a neighboring rack column. In other words, you can’t create empty rack col-
      umns.
      In the example below, we drag and drop an RV7000 reverb device to the right of the original rack:

      Click on the RV7000
      device panel and drag to
      the right...

      ... Release the mouse
      button and the RV7000
      device is automatically
      placed in a new rack
      column to the right.

      A large white arrow symbol appears on the right wooden rack side of the original rack column to indicate that the de-
      vice is about to be moved to a new rack column.

      About the “Sort Selected Device Groups” function
      When you are working with Device Groups (see “About Device Groups”), there is a very nice feature which allows you
      to visually organize and re-order the Device Groups, Main Mixer channel strips and sequencer tracks. With the “Sort
      Selected Device Groups” function on the Edit menu, it’s possible to sort Device Groups and Main Mixer channel strips
      according to the current sequencer track order - or vice versa, depending on what’s currently selected. To sort the
      Device Groups in the rack, and the channel strips in the Main Mixer, according to the current sequencer track order,
      proceed as follows:


=== END OF PART ===
