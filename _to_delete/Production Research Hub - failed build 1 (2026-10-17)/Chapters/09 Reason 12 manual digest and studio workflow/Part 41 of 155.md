# Chapter 09: Reason 12 manual digest and studio workflow
## Part 41 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 32 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 42 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 32 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 14: Working with VST Plugins

Working with VST
Plugins

      About this chapter
      This chapter describes the procedures and techniques for working with VST plugins in the Reason application.

      About VST plugins
      VST (Virtual Studio Technology) is a software instruments and effects plug-in format designed by Steinberg. Reason
      12.5 and later supports 64-bit VST3 and VST2 (2.4) plugins. VST plugins integrate nicely with the Reason rack:
      • A VST Plugin is represented by a Plugin Rack Device in the Reason rack.
      • Cables can be connected on the rear panels of the Plugin Rack Devices, just like on the internal rack devices.
      • CV signals can be routed like on the internal rack devices.
      • Plugin Rack Devices are combinable with other Plugin Rack Devices, Rack Extensions and internal devices
        (see “The Combinator” chapter).
      • Panel parameters are automatable and remotable.

      VST compatibility in Reason
      • Reason 12.5 and later supports 64-bit VST3 and 64-bit VST2 (2.4) plugins.
      • Both Windows and Mac VSTs are supported.
      !   Multitimbrality in VSTs is currently not supported - only one channel per VST can be played back at a time. If
          you are using a multitimbral VST it will only receive on MIDI Channel 1.
      !   Reason does not support VSTs that output MIDI.
      !   VSTs are NOT supported in Reason Rack Plugin!

      Installing and enabling VST plugins
      VST plugins are downloaded and installed individually for each VST, as designed by the plugin manufacturer. No spe-
      cial Reason Studios app or functions are required for installing VSTs.

      About VST licenses
      VST licenses and authorizations are handled by the individual VST manufacturers. VSTs cannot be authorized using
      the Reason Studios authorization system used for Reason and Rack Extensions.

      Installing VST plugins under Windows
      At each launch, Reason automatically scans for installed VST plugins in the following folders:
      C:\Program Files\VSTplugins\ (VST2 plugins)
      C:\Program Files\Steinberg\VSTplugins\ (VST2 plugins)
      C:\Program Files\Common Files\Steinberg\VST2\ (VST2 plugins)
      C:\Program Files\Common Files\VST3\ (VST3 plugins)
      D   If you don’t have any VST plugins installed on your Windows computer you might have to manually create a
          folder according to one of the paths listed above.
          When you then install VST plugins later on, instruct the VST Installation program to install the dll files in the appro-
          priate folder. If there is no installation program for the VST, manually place the VST dll files in this folder.
      • It’s also possible to define your own custom VST folders on the Folders tab in Preferences, see “Defining cus-
        tom VST folders”.

      Installing VST plugins under Mac
      On a Mac OS computer Reason automatically scans for installed VST plugins in the following folders at each launch:
      Library/Audio/Plug-ins/VST (VST2 plugins)
      ~/Library/Audio/Plug-ins/VST (VST2 plugins)
      Library/Audio/Plug-Ins/VST3 (VST3 plugins)
      D   If you don’t have any VST plugins installed on your Mac you might have to manually create a folder according
          to one of the paths listed above.
          When you then install VST plugins later on, instruct the VST Installation program to install the files in the appropri-
          ate folder. If there is no installation program for the VST, manually place the VST files in this folder.
      • It’s also possible to define your own custom VST folders on the Folders tab in Preferences, see “Defining cus-
        tom VST folders”.

      Enabling VST plugins in Reason
      D   To make newly installed VST plugins s available in Reason, simply (re)launch Reason.
          The available VST plugins are displayed on the corresponding palettes in the Reason Browser; VST instruments
          on the “Instruments” palette and VST effects on the “Effects” palette. VSTs that are internally tagged with “Analy-
          sis” are placed on the “Utilities” palette.
      • The VST plugins appear in the corresponding manufacturer sections, the same way as Rack Extensions are
        presented:

          VST instruments on the Instruments palette in the Browser.
      • VST3 plugins have a small golden VST3 label at the top left of the device thumbnail - and VST2 plugins have a
        small blue VST2 label. This is to distinguish them from Rack Extension devices, which don’t have any label.
      D   Click the Show/hide button(s) to choose what devices should be shown in the browser.
          If both the VST2 and VST3 buttons are on, you can choose to hide any VST2 “duplicates” of the same device by
          deactivating the Duplicates button:

      • Some VST plugins might be represented by a generic device “panel” in the Browser. If this is the case, you can
        have Reason take a screenshot of the VST plugin panel and automatically replace the generic panel, see
        “Screenshot”.

      Using VST plugins in Reason
      VST plugins are listed together with Rack Extensions and Reason devices in the Create menu subgroups and on the
      Device Palettes in the Browser:

      The Arturia ARP 2600 V3 VST2 and VST3 instruments are available from the Create menu and on the Instruments device palette in the
      Browser.
      The VST plugins are sorted in the appropriate subgroups and are listed, per manufacturer, in alphabetical order. Note
      though, that devices from Reason Studios are always placed first in the list, below the internal Reason devices.

      Adding VSTs to the rack
      Adding VSTs to the rack is done in exactly the same way as when you add native devices and Rack Extensions.
      1. To create a VST, either select it in the appropriate subgroup in the Create menu, double click or drag and drop
         from the Device Palette in the Browser, or select “Create Instrument...” or “Create Effect...” from the Create
         menu.
         The Plugin Rack Device is placed in the rack and is auto-routed according to the standard rules. See “About auto-
         routing of VSTs in the rack” for more details about auto-routing of VSTs.
         Like with other devices, Instrument VST plugins automatically get a sequencer track, whereas effect and utility
         VSTs don’t, by default.
      2. To edit the VST plugin, click the Open button on the Plugin Rack Device (see “The Plugin Rack Device” below).
         A Plugin Window opens up and displays the VST panel.

      The Plugin Rack Device
      When you create a VST in Reason it’s automatically housed in a Plugin Rack Device. The Plugin Rack Device is a
      “container” for the VST plugin and represents the VST in the Reason rack. The Plugin Rack Device much resembles
      a Combinator device and features audio inputs and outputs as well as CV connectors and a CV Programmer section.
      If the VST is detected as an instrument the Plugin Rack Device is automatically connected to a Mix Channel device,
      just like any other instrument device in Reason.

      Front panel

      A Plugin Rack Device representing an Arturia ARP 2600 V3 VST3 instrument.

      A Plugin Rack Device representing a Sonic Charge Permut8 VST2 effect.
      A Plugin Rack Device for a VST instrument has Pitch and Mod Wheel controls, whereas a Plugin Rack Device for a
      VST effect has the standard “Bypass/On/Off” switch (like any other Effect device in the rack).
      !   Note that setting the VST effect device in “Off” or “Bypass” will not disable the VST. This means the VST will
          still affect the CPU/DSP Load.
      • The center and right sections of the Plugin Rack Device are identical, regardless of if it represents a VST instru-
        ment or VST effect.
      • The Patch Load/Save section works in the same way as for the other device types in Reason (see “Loading
        patches” and “Saving patches”).
          There are also Next/Previous VST Program buttons to the right of the patch display, where you can step through
          the programs loaded in the VST plugin itself, see “Selecting VST presets/programs”.
      • Above the Patch Load/Save section is the name of the corresponding VST, as well as the manufacturer’s
        name.
      • Below the Patch Load/Save section is a button for unfolding the CV Programmer (see “The CV Programmer”).
      • The display shows a screenshot of the corresponding VST (or a default logo).
          At the top left of the display it’s also stated if it’s a VST2 or VST3 plugin.
      • At the bottom of the display is the Open button. Clicking this (or the image of the VST) brings up the VST in its
        Plugin Window (see “The Plugin Window”).
      • To the far right are audio input and output level meters, as well as indicators for Note On, Automation data and
        CV input.
      • Below the indicators is an On/Off button for enabling/disabling the VST plugin completely.
          Disabling a VST plugin will also reduce the CPU/DSP Load.

      The CV Programmer

      The CV Programmer of the Plugin Rack Device.
      On the CV Programmer panel you can route CV signals from other (modulation) devices in the rack to parameters of
      the VST plugin. Each of the eight CV slots can receive a CV signal connected to the corresponding Modulation CV In
      connector on the rear panel of the Plugin Rack Device (see “Rear panel” below).
      Refer to “CV modulation of VST parameters” for information on how to route CV signals to VST parameters.

      Rear panel

      The rear panel of a Plugin Rack Device representing a VST Instrument, with the CV Programmer unfolded.
      The rear panel features Sequencer Control connectors for controlling VSTs from e.g. step sequencers and arpeggia-
      tor devices. This section is available only if the Plugin Rack Device represents a VST Instrument. To the right are au-
      dio inputs and outputs.
      If the Plugin Rack Device represents a VST Effect, Audio Inputs 3-4 (Sidechain) are available at the top right on the
      upper section of the rear panel, together with the other main inputs and outputs.
      On the unfolded CV Programmer/Optional Inputs & Outputs panel are eight CV modulation inputs, for controlling
      VST parameters from connected CV modulation sources.
      To the right on the unfolded panel are optional audio inputs and outputs. If the VST supports the use of multiple audio
      inputs and/or outputs, the available jacks are indicated by green numbers.
      For more details about CV controlling VSTs, see “CV modulation of VST parameters”.

      About auto-routing of VSTs in the rack
      Auto-routing of VST instruments
      The auto-routing rules for VST instruments are very straight forward:
      • VST instruments that output a stereo signal are automatically connected from Audio Out 1 (L) and 2 (R) of the
        Plugin Rack Device to the L and R inputs of a Mix Channel device.
      • VST instruments that output a mono signal are automatically connected from Audio Out 1 (L) of the Plugin
        Rack Device to the L input of a Mix Channel device.

      Auto-routing of VST effects
      Unlike with native Reason effects and Rack Extension effects, there can be mono VSTs, with mono in/mono out.
      Also, Reason doesn't know whether a stereo VST effect device is "dual mono" or generates stereo from a mono sig-
      nal.
      There are two cases to be aware of:
      • If you insert a Mono In-Mono Out VST effect in a stereo signal path, only the left output will be connected (re-
        sulting in a mono signal path):

            L
                           Mono Plugin         mono
            R                                  (to L input of next device)

      • If you insert a Stereo VST effect in a mono signal path, Reason will route it as mono in-stereo out (changing
        the signal path to stereo):

             mono                              L
                          Stereo Plugin
                                               R

      The Plugin Window
      The VST plugin panel is shown in a separate floating window - the Plugin Window - that is kept on top of the song
      window(s). Several Plugin Windows can be open at the same time.

      Opening the Plugin Window
      D   Open the Plugin Window by clicking the Open button - or the VST image - on the Plugin Rack Device panel:

      The Plugin Window opens up and shows the VST panel:

      The MicroTonic VST in its Plugin Window.

      General functions in the Plugin Window
      • The title bar of the VST Plugin Window shows the name of the device instance (same as tape strip).
         This is for helping you finding the correct Plugin Window, especially if there are several instances of the same
         plugin.
      At the top of the Plugin Window are a number of icons:
      • Keep open
         If you activate the “Keep open” function, the Plugin Window(s) will not be automatically closed when you select an-
         other device in the rack. Having the “Keep open” selected on several Plugin Windows makes it possible to have
         several VST panels open at the same time.
      • Automate
         Click this button when you want to assign a VST parameter for automation in the Reason sequencer, see “Auto-
         mating VST parameters”.
      • Remote
         Click this button and then select a VST parameter you want to remote control from your MIDI keyboard/control
         surface, see “Remote controlling VST parameters”.

      • Screenshot
          Click the camera symbol to take a screenshot of the VST front panel:

          The screenshot is then automatically scaled down and placed on the corresponding Palette in the Browser, and in
          the Plugin Rack Device display:

          The screenshot of the MicroTonic VST is scaled down and displayed in the Browser and in the Plugin Rack Device.

      Closing the Plugin Window
      The Plugin Window can be closed in a number of different ways:
      • By clicking the Open button on the Plugin Rack Device panel (the same as for opening the Plugin Window).
          This works regardless of whether the “Keep open” function in the Plugin Window is on or off.
      • By clicking the standard “window close” button in the upper corner of the Plugin Window.
          This works regardless of whether the “Keep open” function in the Plugin Window is on or off.
      • By selecting another device in the rack.
          If the “Keep open” function in the Plugin Window is active, selecting another device in the rack will NOT close the
          Plugin Window (see “Keep open” above).

      Editing the VST parameters
      Editing a VST is done in the same way as when editing a native device or a Rack Extension device, only VSTs are ed-
      ited in their Plugin Windows - not in the rack.
      !   Note that the standard “Reason” functions, such as holding [Shift] while turning a knob/moving a slider to im-
          prove the precision - or holding [Ctrl](Win) or [Cmd](Mac) to reset parameters to their default position/value -
          won’t work for most VSTs. This is because the VST manufacturers define this type of functionality themselves.
      !   If the VST plugin has a built-in on-screen keyboard (etc), this can be used for auditioning sounds but you can-
          not use it for recording into Reason’s sequencer!

      About Undo and Redo
      The Undo/Redo functions in Reason also work in most situations when editing VST parameters in the Plugin Win-
      dow(s).

      Automating VST parameters
      Automating VST parameters in the Reason sequencer works in a similar way as for native devices and Rack Exten-
      sion devices. Basically, there are three (or four) ways of automating VST parameters in the Reason sequencer:
      D   Start recording in the Reason sequencer and then edit the desired VST parameters while recording.
          Each of the edited VST parameters automatically gets their own automation lane on the sequencer track, with
          clips and automation points recorded. Make sure the Parameter Automation is record-enabled on the track first.

      Another alternative is this:
      1. Click the Automate button in the Plugin Window.

      2. Then, click the parameter you want to automate on the VST panel.

        The automated VST parameter gets an automation lane in the Reason sequencer:

      3. Then, you can draw automation clips and automation points, the same way you would for a native device or a
         Rack Extension device.
      • A third alternative is to select the parameter from the Track Parameter Automation popup above the track list
        in the sequencer, see “Creating/adding parameter automation lanes”:

      • As a fourth alternative, some VSTs let you right click a parameter on the VST panel and select Automate from
        the context menu.

      CV modulation of VST parameters
      There are eight CV inputs on the rear panel of the Plugin Rack Device. These CV inputs can be assigned on the CV
      Programmer panel of the Plugin Rack Device.
      D   Click the CV Programmer button on the VST Rack Device panel to unfold the CV Programmer:

          The CV Programmer of the Plugin Rack Device.
      For each slot on the CV Programmer panel you can:
      • Select a CV input.
          Several slots can use the same CV input.
      • Set a bipolar modulation Amount.
          The range is -100 to 100.
      • Select a VST destination parameter from a drop-down list.
          This can also be done with Learn function (see below).
      • Set a Base Value.
          The Base Value is the value the parameter has the time you select it on the VST panel. This is similar to the “Static
          Value” used when automating parameters on native Reason devices and Rack Extension devices. The exact Base
          Value is shown in the corresponding value slider.
      • Clear the CV assignment.

      CV controlling VST parameters using the Learn function
      1. Press [Tab] to flip the rack around.
      2. Connect a CV cable from the device you want to use as control source, to the CV IN 1 input of the Plugin Rack
         Device.

      3. Press [Tab] to flip the rack back to the front again.
      4. Click the topmost Learn button.

        The Learn button lights up and the Plugin Window is opened and brought to front. In the Plugin Window, the text
        display tells you to move a parameter.

      5. Click a parameter in the VST Plugin Window.

          In this example we click the Fine Tune slider of Oscillator 1 to assign it.
          The Fine Tune Osc1 parameter is now assigned in the Parameter column for CV slot 1:

      6. If desired, change the CV (bipolar) modulation amount by clicking the Amount bar and dragging up/down:

      7. Repeat the procedure for the other CV slots you want to assign.
      D   You can also change the VST parameter’s “start” value by clicking the Base Value bar and dragging up/down.
      D   If you want to reassign a VST parameter, just click the Parameter drop-down and select the desired VST pa-
          rameter from the list:

      Remote controlling VST parameters
      It’s possible to assign Remote Overrides to VST parameters, to be able to control VST parameters from your con-
      nected MIDI Control Keyboard/Surface.

      Adding a Remote Override to a parameter
      1. Click the Remote button at the top of the Plugin Window.

        The button is highlighted and a text display tells you to click a parameter.
      2. Click a parameter on the VST panel in the Plugin Window.

      • In some VSTs you could right click a parameter on the VST panel and select Remote from the context menu.
        The Remote Override Edit dialog appears for this parameter:

      3. Use the “Learn from control surface input” function and turn a knob on your MIDI Control Keyboard/Surface to
         assign a physical knob/slider to the VST parameter.

        Knob 8 on the MIDI keyboard assigned to control the DistAmt1 parameter on the MicroTonic VST.
      4. Click OK to close the dialog.

      Removing a Remote Override from a parameter
      1. Click the Remote button at the top of the Plugin Window.
          The button is highlighted and a text display tells you to click a parameter.
      2. Click the parameter you want to remove from the Remote Override.
          A context menu appears where you can select “Edit Remote Override Mapping...” (to reassign an override), or
          “Clear Remote Override Mapping” to remove the override.

      Selecting VST presets/programs
      VST3 plugins can support “vstpreset” files. Vstpreset files can be browsed by clicking the Browse Patch button on
      the Plugin Rack Device:

      You then select and load the desired vstpreset from the Reason browser, like you would any other patch files.
      Programs for VST2 plugins can be selected from the Plugin Rack Device (if the VST2 supports programs). For ex-
      ample, if you load a bank (fxb) using Reason’s Browser, the fxb bank may contain a number of different programs,
      which are then loaded into the VST.
      1. Click the patch name display on the Plugin Rack Device to show the list of programs loaded in the VST plugin.

      2. Select the desired VST2 program/patch from the list.
      D   Alternatively, click the VST Prog up/down selectors to step between and load the VST programs:

      These methods also work if the VST2 has presets that are automatically loaded when you create the device.
      !   Note that the VST Prog selector buttons only appear if the plugin has a bank of programs or presets loaded.

      About saving songs that contain VSTs
      When you save a Reason song document, all VST preset/patch/program data is automatically embedded in the song
      document. This means that you can load VST presets/patches/programs, edit them and then save the Reason song
      without needing to save the edited VST presets/patches/programs separately. This works exactly the same way as
      for patches in native Reason devices and Rack Extension devices.

      Combining VST plugins in Combinator devices
      A Plugin Rack Device can be Combined just like any other device types. In the Combi Programmer, all VST parame-
      ters are listed. See “The Combinator” for more information.

      About missing VST plugins
      When you open a Reason song from another user, it might have been created using VST plugins that you don't have.
      When you open such a song, any missing VSTs are replaced by empty Plugin Rack Devices in the rack:

      An empty Plugin Rack Device representing a VST which is currently unavailable on your computer.
      • The empty VST device itself will be silent.
         If it's an effect, it will bypass the audio (or be silent, if connected as a send effect).
      • If you're collaborating with a friend you can safely save the song and send it back.
         When your friend opens the song, the missing VST will be restored with all settings intact.

      Managing VST plugins
      To get an overview of the VST plugins currently installed on your computer - and to be able to disable any malfunc-
      tioning VSTs - there is the Manage Plugins window.
      D   Select “Manage Plugins” from the Window menu.


=== END OF PART ===
