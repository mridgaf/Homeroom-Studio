# Chapter 09: Reason 12 manual digest and studio workflow
## Part 43 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 34 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 44 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 34 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 15: Sounds, Patches and the Browser

Sounds, Patches and
the Browser

      About this chapter
      This chapter deals with the following topics:
      • Handling Patches.
          See “About patches”.
      • Using the Patch Browser.
          See “Using the Browser”.
      • ReFills and Reason file formats.
          See “About ReFills”.

      About patches
      A patch contains settings for a specific device. Patches can be either separate files on your hard disk or files embed-
      ded in a ReFill (see “About ReFills” for info about ReFills). The devices that use patches are described below. The Mix
      Channel, Master Section and Audio Track devices can use Insert FX patches saved as Combinator devices. All other
      Reason devices use either Presets or can only be programmed using the device panel parameters.

      Reason devices that use patches
      • Subtractor, Thor, Malström and Europa synth patches contain all settings on the device panel.
          Loading a patch brings up a new sound, just like when loading programs or patches on a hardware synthesizer.
      • Dr. Octo Rex patches contain information about what REX files are loaded in each slot, their settings as well as
        the parameter settings on the device panel.
          It is important to note that the Dr. Octo Rex patch doesn’t contain the actual REX files - only information about
          which REX files are used.
      • Mimic, NN19, NN-XT and Grain patches contain information regarding which samples are used, their settings
        (key mapping, tuning, etc.) and the parameter settings on the device panel.
          It is important to note that the patch doesn’t contain the actual samples - only information about which sample files
          are used.
      • Redrum Drum Computer and Kong Kit Patches patches contain a complete “drum kit”, that is, information
        about which drum samples are used, together with the parameter settings for each drum sound.
          Again, the actual samples are not included in the patch, only references to files. Also note that Redrum patches are
          separated from Redrum patterns - loading a new patch will not affect the patterns in the device.
      • Softube Amp and Softube Bass Amp patches contain information about the parameter settings on the device
        panel, as well as information about used Amp and Cabinet models.
          Loading a patch brings up a new sound, just like when selecting programs or patches on a hardware effect device.
      • RV7000 MkII, Pulveriser, The Echo, Alligator and Scream 4 effect patches contain all settings on their respec-
        tive device panels.
          Loading a patch brings up a new sound, just like when selecting programs or patches on a hardware effect device.
      • The MIDI devices on the Players palette use patches that contain panel settings.
      • The Combinator (Combi) patch format saves all settings and file references for each device in the Combi,
        along with the Combinator’s own settings; key/velocity zones, modulation routing etc.
          Any audio or CV routing from/to devices that are part of the Combi is also saved.
      !   Note that patches for devices included in a Combi are not saved individually - e.g. if a Combi includes a Sub-
          tractor, and you have tweaked its settings, these settings will be saved with the Combi, but will not be saved as
          a separate Subtractor patch unless you do so from within the Combi - see “Saving patches”.
      !   Patches other than Combi patches do not include any cable routing information.

      About the “Load Default Sound in New Devices” preference
      On the “General” page in Preferences, there is an option (on by default) to load a default patch when creating a de-
      vice. For some devices, there are a number of patches that exist outside category folders in the main Sound Bank
      folder for the device. These will be available on the browse list (see “About browse lists”) directly after creating the
      device, which allows you check out a few sounds for a device without opening the browser.

      Loading patches
      Immediately after you have created a new device, the device automatically gets “browse focus”. This means that the
      Browser is temporarily “locked” to the device and displays patches for the device you just created. Browse focus for
      a device is indicated by orange side bars in the rack and on the sequencer track - and that the patch section on the
      device is colored in orange. In the Browser the orange Browse Focus field at the top now shows patches only for the
      highlighted device in the rack:

      To load a patch for a device, use one of the following methods:
      !   For all the patch load methods described below, you can automatically revert back to the original patch, see
          “The Revert function”.
      D   Double click a patch in the Browser to automatically load it in the device that has browse focus.
      D   Use the up/down arrow keys, or click the Load Previous/Load Next triangle buttons at the bottom of the
          Browser, to select a patch in the Browser and automatically load it in the device that has browse focus.
      D   Click a patch in the Browser to select it, then click the Load button at the bottom of the Browser, or press [En-
          ter] (not on the numeric key pad).
      D   Drag a patch from the Browser - or from the Windows Explorer (Win) or Finder (Mac) - and drop it on the device
          panel (or drop it on the device icon in the Sequencer Track List).
      !   Automatic browse focus can be turned off on the General page in Preferences, see “New devices get browse
          focus”.
      !   If you drop patches for other devices (of the same device type (Instruments or Effects)), the existing device will
          be replaced by the new device. You can also drag and drop patches onto devices that don’t support patches. In
          these situations, the new device replaces the current one and the dropped patch is automatically loaded in the
          new device.
      !   Note that Instrument devices can only be replaced by other Instrument devices. The same goes for Effect de-
          vices. Utility devices cannot be replaced using the “drag and drop” method!

      D   Click the Select Patch buttons on the device panel:

                                                                  Save Patch button

                                                        Browse Patch button
               Patch Name display                   Select Patch buttons
          The Patch section of the Subtractor device.
      D   Click on the Patch Name display on the device panel to bring up a a pop-up menu which lists all patches in the
          currently selected folder.
      D   Click the Browse Patch button on the device panel.
          This is useful mainly if a device doesn’t already have browse focus. Clicking the Browse Patch button sets browse
          focus to the device. Then, you can select and load patches as described above.
      !   On the panels of the Redrum, NN19, NN-XT, Kong, Grain and Dr. Octo Rex devices, there are also other Patch
          buttons, used for loading samples or REX files. Make sure you click on the button in the Patch section (next to
          the patch name display)!
      D   Select “Browse Patches...” from the Edit menu or device context menu.
          This is useful mainly if a device doesn’t already have browse focus. Selecting Browse Patches sets browse focus
          to the device. Then, you can select and load patches as described above.
          Note that the Edit menu reflects which device is selected - in other words, you must select the device for the cor-
          responding Browse Patches item to appear on the Edit menu.
      q   Once you have loaded a patch, you can step between all the patches in the same folder by using the “Select
          Patch” buttons on the device panel:

      D   If you click on the Patch Name display on the device panel, a pop-up menu will appear, listing all patches in the
          currently selected folder.
          This allows you to quickly load another patch, without having to step through the patches one by one. You can also
          choose to set browse focus to the device by selecting “Open Browser...” from this pop-up menu.

      When you load a patch in any of the ways described above, the device’s parameters will be set according to the val-
      ues stored in the patch, and the name of the patch will be shown in the Patch Name display.
      !   Any parameter adjustments you make on the device panel after loading a patch will not affect the actual patch
          file. For this to happen, you need to save the patch - see “Saving patches”.
      !   You can also load patches from a MIDI Master Keyboard or Control Surface - see “Remote - Playing and Con-
          trolling Devices”.

      The Revert function
      A soon as you have loaded a new patch into a device that has browse focus, the Revert button becomes available at
      the bottom of the browser list:

      The Revert button appears as soon as you load new patches into a device that has browse focus.
      The Revert function makes it possible to get back to the patch which was originally in the device - before you started
      loading new patches. This is very handy if you should change your mind and want your original patch back in your de-
      vice. The Revert function also works if you have loaded patches for other device types, so called cross-browsing (see
      “Cross-browsing patch files”).

      If referenced samples are missing
      As described above, patches for the Redrum, NN19, NN-XT, Kong, Grain and Dr. Octo Rex contain references to
      samples or REX files. Just like patches, samples can be independent files on the hard disk or elements within a Re-
      Fill. However, if sample files have been moved or renamed after a patch was saved, the sample file references in the
      patch will not be accurate.
      If this is the case when you select a patch, the program will tell you so. You can then choose to either manually locate
      the missing files, to have the program search for them, or to proceed without the missing sounds. For details, see
      “Handling Missing Sounds”.
      !   Proceeding without locating or replacing the missing samples will result in silent drum channels, key zones or
          loop slots (for the Redrum, NN19/NN-XT, Kong and Dr. Octo Rex respectively).

      Clearing browse focus
      To clear browse focus for a device, use one of the following methods:
      D   Click anywhere in the rack background.
      D   Click the X symbol to the right on the orange browse focus label at the top in the Browser.
      D   Select another sequencer track (if the rack is not detached).

      Setting browse focus
      Apart from when creating and loading patches into a device, browse focus can be set anytime you like. This is very
      useful if you're working in the sequencer where there are no browse buttons. Or if you want to set browse focus to a
      non-patch device and replace it with something else.
      1. Select a device in the rack, or a track in the sequencer.
          In this example we select a Redrum track in the sequencer. As soon as the track (or device) is selected, the
          Browser shows the track/device name on a gray background in the Browse Focus field:

      2. Now, click the folder button in the Browse Focus field:

          Browse focus is now set to the Redrum device:

      3. Now, you can browse and load new patches into the Redrum device.
      4. When you are done, clear the browse focus by clicking the X button in the browse focus field.
      !   If you are using two Browsers, the one in the Song window and the other in the detached rack window, browse
          focus can only be set in one of the Browsers at a time.

      Saving patches
      Saving device settings in a song
      When you save a Reason song, all settings for all devices are automatically included in the song file - there is no need
      to save the patches separately.
      !   It’s important to realize that it’s the actual settings that are saved in the Song - not references to patches on
          disk. The next time you open the song, all devices will be set as they were when you saved it (regardless of
          whether you have removed or edited any patches on disk).
      !   Note that device samples are not stored with the Song by default. This means that if you edit any Redrum,
          Kong, Grain or NN19/NN-XT samples in an external application and then open a Song containing devices that
          use these samples, the sound will be different. It’s possible, however, to store actual device samples together
          with the Song using the “Self-Contain” feature. See “About Self-Contained Songs”.

      Saving device settings as patches on disk
      Even though the device settings are stored with the song, you may want to save any settings you have made for a de-
      vice as a separate patch file. This allows you to use the patch in other songs, and lets you try out other patches in your
      song without the risk of losing your original sound. A patch is saved as follows:
      1. Click the “Save Patch” button on the device panel:

      2. In the file dialog that appears, specify a location and name for the patch file and click Save.
      • Under Windows, the different types of patch files have different file extensions.
          File extensions are automatically added by Reason when you save. Under macOS, file extensions are not needed
          but it may be a good idea to keep them if you want the saved files to be usable under Windows.
      • If you have selected a patch, modified it and want to save it with the modifications, you could either save a sep-
        arate, modified version of the patch (with a new name) or simply overwrite the old patch file on disk.
          As usual, you will be asked whether you really want to replace the existing patch file.
      !   Note that you can save a patch under the same name and location without having the save dialog appear by
          holding down [Alt](Win) or [Option](Mac) and clicking the “Save Patch” button on the device panel. Be aware
          that this overwrites the original patch!
      !   Note also that you cannot save into a ReFill! This means that if you have opened a patch from within a ReFill,
          modified it and want to save it, you need to save it as a separate file in a new location (outside the ReFill). Pref-
          erably, you should also rename the modified patch file, to avoid confusion.

      Copying and pasting patches between devices
      A quick way to copy device parameter settings between devices of the same type is to use the “Copy Patch” and
      “Paste Patch” functions. The result is exactly the same as if you had saved a patch from one device and opened it on
      another device of the same type - this is just a quicker method.
      !   Copying and Pasting settings is possible with all device types that can use patches.
      Proceed as follows:
      1. Select a patch, and/or make the desired settings on the source device.
          Make sure the device remains selected.
      2. Select “Copy Patch” from the Edit menu or from the device context menu.
      3. Select the destination device of the same type (in the same song or another song).
      4. Select “Paste Patch” from the Edit menu or from the device context menu.
          The settings of the source device (including Redrum, NN19, NN-XT, Grain and Kong sample references and Dr.
          Octo Rex REX loop references) are applied to the destination device.
      !   Note that this operation simply copies the settings from one device to another. Adjusting the settings on one
          of the devices will not affect the other; neither will the settings affect any patch file on disk.

      Copying Main Mixer Insert FX settings and paste as Combinator patches
      You can copy Insert FX settings from Main Mixer channels and paste these as Combinator effect patches - or vice
      versa. To copy a Main Mixer channel Insert FX setting and paste into a Combinator device, follow the steps below:
      1. Select the desired Mix Channel/Audio Track device in the rack, or the desired Mixer Channel in the Main Mixer.
      2. Select “Copy Channel Settings -> Insert FX” from the Edit menu or device/Mix Channel context menu.
          The Insert FX devices with their settings and connections are placed on the computer’s clipboard memory.
      3. Select the desired empty Combinator device in the rack - or create a new Combinator device and select it.
      4. Select “Paste Patch” from the Edit menu or the device context menu.
          The Insert FX devices with their settings and connections are pasted into the Combinator device.
      To copy an effect patch in a Combinator device and paste it as an Insert FX in a channel strip in the Main Mixer, pro-
      ceed as follows:
      1. Select the Combinator device which contains the effects you want to copy.
      2. Select “Copy Patch” from the Edit menu or the device context menu.
          The Combinator effect devices with their settings and connections are placed in the computer’s clipboard memory.
      3. Select the desired Mix Channel/Audio Track device in the rack, or the desired channel strip in the Main Mixer.
      4. Select “Paste Channel Settings: Insert FX” from the Edit menu or the device context menu.
          The Combinator devices with their settings and connections are pasted into the Insert FX section of the selected
          Mix Channel/Audio Track device.

      Initializing patches and resetting device parameters
      Sometimes it is useful to start with a “clean slate” when creating a synth sound, a drum kit or a sampler patch. This is
      achieved by selecting “Reset Device” from the Edit menu or from the device context menu. This resets all parameters
      to “default” values. Initializing Mimic, NN19, NN-XT, Dr. Octo Rex, Kong, Grain or Redrum devices will also remove all
      sample/REX file references, allowing you to start from scratch.

      About ReFills
      A ReFill is a kind of component package for Reason, which can contain sounds and effects patches, samples, REX
      files, SoundFonts and demo songs. If you like, you can compare ReFills to ROM cards for a hardware synthesizer. On
      your computer, ReFills appear as large files with the extension “.rfl”.
      All sounds included with Reason are embedded in three ReFills named “Reason Sounds”, “Orkester Sounds” and
      “Factory Sounds”, which were (downloaded and) copied to the hard disk during installation.
      Additional Reason Studios ReFills are available for purchase. You can also download ReFills from other Reason us-
      ers on the Internet, purchase them from other sample manufacturers, etc.
      • Samples (Wave and AIFF files) are compressed to about half their original file size when stored in ReFills,
        without loss of quality.
      In Reason, you can use the browser to list and access the embedded sounds and other components within the Re-
      Fills, just as if the ReFills were folders on your hard disk.
      Furthermore, if a song makes use of components from ReFills, Reason will tell you which ReFills are required.

      Using the Browser

      The Browser when using the File|Open... command.
      The Browser is used when you open songs or load patches, samples, audio files, MIDI files and REX files, from reg-
      ular file folders or from a ReFill.
      D   Open and close the Browser by pressing [F3] or by selecting Show/Hide Browser from the Windows menu.
      !   If you have the rack detached in a separate window, you can have a second Browser in the rack window, see
          “About using the Browser in the detached rack”.
      The Browser can also be resized by dragging the edges of the browser list sideways, as shown in the picture above.
      Each column in the browse list can also be resized. You can also scroll horizontally and vertically (when applicable)
      using the scrollbars to the right and at the bottom of the browse list (yellow arrows in the picture above).

      Besides standard file folder browsing, the Browser offers several useful functions:
      • Search for files by name and/or type - see “Using the “Search” function”.
      • Use “cross-browsing” to search for patches belonging to any type of device.
          For example, set browse focus from a Subtractor device by clicking its Browse Patch button. Instead of limiting the
          Browser to show only Subtractor patches, you can choose to browse for any type of instrument patch. If you select
          a patch with a different format than the device you are browsing from, the original device will be replaced by the
          new device. See “Cross-browsing patch files”.
      • Create Favorite Lists containing shortcuts to your favorite files for instant access.
          See “Favorites Lists”.
      • Audition audio samples and loops on the fly.
      • Save shortcuts to various locations on your local drive(s).
          See “Using Locations and Favorites”.

      Opening the browser
      Besides pressing [F3] you can use any of the following commands to open the Browser (what file types you can
      browse for depends on which method you used to open the Browser):
      • By selecting “Open” from the File menu.
          This opens the Browser where you can select to open a Song (.reason, .rsndemo, .ree, .reedemo, .rltd, .record, .rec-
          demo, .rns, .rps and .rsb).
      !   If no Song document is open on the macOS version of Reason, Reason temporarily opens an empty Song doc-
          ument to be able to show the Browser. When a Song has been loaded, the empty document closes.
      • By selecting “Browse Patches” on the Edit menu with a patch based device selected (or by clicking the
        “Browse Patches” button on the device panel).
          This opens the Browser allowing you to browse for and load patches for the selected device, or use “cross-brows-
          ing” (see “Cross-browsing patch files”) to select patches for other device types.
      • By selecting “Browse Insert FX Patches” on the Edit menu with a Main Mixer Channel or Mix Channel/Audio
        Track device selected.
          This opens the Browser, where you can browse for and load Combinator Effect patches.
      • By selecting “Browse Samples” on the Edit menu with a sample based device selected (or by clicking the
        “Browse Samples” button on the device panel).
          This opens the Browser, where you can browse for, preview and load samples in the supported audio formats.
      • By selecting “Browse ReCycle/REX Files” on the Edit menu with a Dr. Octo Rex Loop Player selected (or by
        clicking the “Browse Loops” button on the device panel).
          This opens the Browser, allowing you to browse for, preview and load REX loops into the Dr. Octo Rex device.
      • By selecting “Browse Drum Patches” on the Edit menu with a Kong Drum Designer device selected (or by click-
        ing the “Browse Drum Patch” button on the Drum Control Panel on the device).
          This opens the Browser, allowing you to browse for Kong Drum Patches and supported audio files to load into a
          slot in the Kong Drum Designer device.
      • By selecting “Import Audio File” from the File menu.
          This opens the Browser, allowing you to browse for, preview and load files in the supported audio formats to an au-
          dio track in the sequencer. See “Importing audio to the sequencer”.
      • By selecting “Import MIDI File” from the File menu.
          This opens the Browser, allowing you to browse for MIDI files to import to instrument tracks in the sequencer. See
          “Importing Standard MIDI Files”.
      • By selecting “Create Instrument...” or “Create Effect...” from the Create menu.
          This allows you to browse for and load patches for any device. See “Create Instrument/Create Effect”.

      Browser elements

      The Browser when using the Browse Patch button/function on a Subtractor device.
      Regardless of what command you used for opening the Browser (Open/Browse Patch/Import Audio etc.), the
      Browser basically contains the same main elements:

      Browse focus field

      This field shows the name of the currently selected device in the rack - or the currently selected sequencer track. The
      Browse Focus field is orange when a device or track has browse focus - and gray when no focus is set. See “Setting
      browse focus” and “Clearing browse focus” for more information.

      Root Folder drop-down list

      This field displays the name of the currently selected root folder.
      D   Click in the name field to bring up a drop-down list where you can move up in the folder hierarchy.
          Search results and Favorites lists, however, are shown as “flat” lists - with no folder hierarchy.
      D   Click on the (arrow) button to the right of the root folder list to move up in the hierarchy one level at a time:

      Back/Forward buttons

      These arrow buttons allow you to move between the browser locations opened while browsing, much like pages in a
      web browser.

      Locations and Favorites list

      This list contains shortcuts to various locations. You can manually add any locations (on any drive) to the bottom sec-
      tion of the list. The locations in the upper part of the list are default and cannot be changed. Selecting an item in the
      “Locations and Favorites” list will open the corresponding folder/ReFill as the root in the main files and folder list -
      see “Navigating in the Browser”.
      In the “Locations and Favorites” list you could also create your own “Favorites Lists”. The “Favorite Lists” can contain
      shortcuts to your favorite patches, samples or song files - see “Favorites Lists”.

      Search text field

      Here you can enter a text string and click Search to search for Song files, patches, audio files and samples. The
      Search function is described in “Using the “Search” function”.

      Browser list

      This is the Browser list, showing the contents of a selected folder - see “Navigating in the Browser”.

      Patch Load section
      At the bottom of the Browser list are a buttons for selecting and loading patches:

      D   Click a patch in the Browser list and then click the Load button to load the patch in the device.
      D   Click the triangular Load Previous/Load Next buttons to automatically load the previous/next patch in the de-
          vice.
          Alternatively, press the up/down arrow keys on the computer keyboard.
      D   Click the Revert button to revert to the patch that was originally in the device, before you loaded new patches.
          See “The Revert function” for more details.

      Info and Details

      The info pertaining to a selected Song file.

      The “Info” section at the bottom of the Browser can show Song/ReFill splash images and also information about the
      item currently selected in the “Files and Folders” list. Exactly what information is shown here depends on the selected
      file type. For example, samples or REX files contain information about the file format and length of the selected file,
      while a selected song file can display comments from the author (see “Including Song Information”) etc. If the se-
      lected file is part of a ReFill, this will be indicated regardless of the file type.
      D   Click the triangular fold/unfold button at the top left to show/hide the Info and Details section.
          Folding the Info and Details section automatically expands the Browse list/device palette downwards.

      Audition section (for audio files, samples and REX files)

      This section contains controls for auditioning audio files, samples and REX files - see “Selecting and auditioning sam-
      ples and REX loops”. For other file types, the “Audition” section is not present.

      Navigating in the Browser


=== END OF PART ===
