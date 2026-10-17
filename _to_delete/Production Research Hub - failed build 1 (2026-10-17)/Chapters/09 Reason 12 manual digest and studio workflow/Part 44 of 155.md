# Chapter 09: Reason 12 manual digest and studio workflow
## Part 44 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 35 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 45 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 35 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      The Browser with browse focus set to a Subtractor device, allowing you to browse for and load Subtractor patches.
      When navigating in the Browser, items are shown as a hierarchical list in a selected root folder, just like in your com-
      puter’s file browser (Finder on Mac and Explorer on Windows).
      All folders and sub-folders within a root folder are shown, but only files of the relevant type (i.e. songs/samples/
      patches etc.) can be viewed/selected in the Browser. For example, if you have selected to browse samples for a NN-
      XT device, only audio samples and REX files will be shown in the Browser.

      D   Click on the triangular symbol next to a closed folder to expand it. If the folder contains files of the relevant
          type, these will be shown.
      D   Double-clicking a folder in the list opens it as the root folder in the Browser.
      • The “Name”, “Type”, “Modified” and “Size” columns show the name of the folder or file, the file/folder type,
        the modification date and the size (files only), respectively.
      • Clicking on a column header sorts the files accordingly (i.e. alphabetically, by file type, by modification date or
        by file size).
          Click the same column again to toggle between ascending or descending display order.
      D   You can use the “Back/Forward” buttons to move between the different locations you have opened in the
          Browser.
          When you hide the Browser the “location list” is cleared.
      D   Use the up/down arrow buttons on the computer keyboard to step between files in the current Browser list
          and automatically load them into the device.
          Only files will be stepped through, while folders are skipped.
      • The Root Folder drop-down list to the right of the “Back/Forward” buttons allows you to move up in the folder
        hierarchy when the Browser points to a specific folder location (see “About hierarchic and flat lists” below).
      D   If you want to browse for patches for other devices, click the X button on the orange field to clear the Browse
          focus from the existing device type.
          If you select and load a patch for another device type, the new device will replace the device that previously had
          Browse focus.

      About hierarchic and flat lists
      In certain circumstances the Browser will display a flat list without any folder hierarchy. In such cases there will be an
      extra “Parent” column displaying the parent folder location for all files. The “Root Folder” drop-down list will then also
      contain a shortcut to the selected file’s parent folder - the “Go To Parent Folder” item.

                                                                  The “Parent” column

      The Browser display for flat lists.
      Flat lists are shown in the following cases:
      • When the Browser is showing a search result - see “Using the “Search” function”.
      • When the Browser is showing a Favorites folder list - see “Favorites Lists”.
      • When the Browser is showing a browse list stored for a device in a saved song - see “About browse lists”.

      Using Locations and Favorites
      To help you to find your files quickly, you can add shortcuts to the folders where you store your samples and patch
      files etc. By default, the Locations list contains eight fixed locations; the Reason Sounds location, the Reason
      Orkester Sounds location, the Reason Factory Sounds location, the Rack Extensions location, This PC folder, the
      Desktop folder and the Song Samples location. You can easily add your own locations below this list if you like.
      • Selecting a Location or Favorite List in the list opens it as the root folder in the Browser.
      D   To add a new Location, select a file, folder or ReFill in the main browser list and drag and drop it in the “Loca-
          tions and Favorites” list.
          Any new Locations will be added below the list of fixed locations. An insertion line is shown to indicate where in
          the list the new location will placed. Manually added locations can later be reordered by dragging and dropping.

          Adding a new Location.
      !   Even though it is possible to add individual ReFills as separate Locations, we strongly recommend that you
          create a ReFill folder in which you put all your ReFills; then add the ReFill folder as a Location:

          The reason for this is that some ReFills (such as the Reason Electric Bass) consist of several ReFill files: one
          which contains patches and another that contains the samples. If you should add only the patch ReFill as a Loca-
          tion and not the samples ReFill, Reason won’t find the samples that correspond to the patches.
      q   If you don’t want to put all your ReFills in one folder, you can create shortcuts (alias) to the ReFills and put all
          the shortcuts in a single folder which you then add as a Location.
      D   To remove a Location (or Favorite List), select it in the “Locations and Favorites” list and press [Backspace] or
          [Delete] - or click the “Remove Favorite” button.
          Alternatively, select “Delete” from the context menu.
      !   The default locations cannot be removed.
      • Manually added locations are stored in the Preferences file in the Reason application folder.
      !   If a stored location has been removed or is unavailable, a warning triangle with an exclamation mark is shown
          before the location name in the “Locations and Favorites” list.
      !   If you have un-synced cloud folders (e.g. in Dropbox) in the Locations and Favorites list you might want to ex-
          clude these folders from the Browser indexing, to avoid very long indexing times. See “Do not index these fold-
          ers” for more information.

      Favorites Lists
      “Favorites Lists” provide a way to group and order files that may be physically located at different places on your local
      drives. Any file that can be loaded in Reason (songs, patches, samples etc.) can be added to a “Favorites List”. Only
      shortcuts to the files are added - the original files aren’t moved. You can also add devices to the list.
      This is particularly useful for handling patches. By adding the patches you need for a given situation to a Favorite List,
      you can determine exactly which patches will be selectable for a device, and in what order. You can then sequentially
      step through these patches using patch select buttons on your MIDI keyboard or control surface device. See “Using
      Favorites - a practical example”.
      !   We strongly recommend not to put ReFills in Favorite Lists. Instead, use Locations for ReFills, see “Using Lo-
          cations and Favorites”.
      D   To add a New Favorite List, click the “Create New Favorite Lists” button.

          The “Create New Favorites Lists” button
          An empty “folder” is created, named “New Favorite List n”. Favorite Lists are always indicated by a star icon. The
          Browser list remains unchanged.
      D   To rename the “New Favorite List” folder, double-click it and type in a new name.
          Alternatively, select “Rename” from the context menu.
      D   To add a file to the “Favorite List” folder, select it in the Browser and drag it to the desired “Favorite List”
          folder.
          You can also select multiple files using standard selection techniques - [Shift] and/or [Ctrl](Win) or [Command]
          (Mac) - and drag these into the folder in the same way.
      D   Select the “Favorite List” folder to view the currently added files in the Browser list.
          The Browser displays all files you have previously dragged to the Favorite List, regardless of file type:

      • When a “Favorites List” folder is selected in the Browser, an additional “Parent column” is shown (just like for
        Search results), listing the name of the original folder for each file in the list.
      • Files in a “Favorites List” folder cannot be sorted by clicking the column headers. However, they can be reor-
        dered by using drag and drop in the Browser list.

      D   To remove files from a “Favorites List” folder, select the folder and then select the files in the Browser list and
          press [Delete], or select “Delete Favorite(s)...” from the context menu.
          This removes the shortcut only - the original file isn’t affected.
      D   To remove a “Favorites List” folder, select it and press [Backspace] or [Delete] - or select “Delete Favorites
          List...” from the context menu.

      Using Favorites - a practical example
      Here follows a practical example of how you can use Favorites for patch files:
      You are preparing for a live gig as a keyboard player. You know the songs, and you have chosen suitable patches (in
      various device formats) for each song.
      You want to use Reason, but you want to be able to switch to the correct patch for each song using your MIDI key-
      board, and not have to worry about fiddling with the computer during your performance.
      Here is how this can be done by using Favorites:
      1. Create a new Reason song.
      2. Create a device, for example a Combinator.
          It doesn’t matter which instrument device you choose at this point.
      3. Click the “Create New Favorites Lists” button.
          A new folder appears in the list. Double-click it and type in an appropriate name (e.g. “The Band”).
      4. Click the Reason Factory Sound Bank and then expand the “All Instrument Patches” folder in the Browser list.
          Now you can start locating the instrument patches you need by navigating in the Browser.
      5. When you have located a patch that you need for the gig, drag it from the Browser list into the Favorites List
         folder.
          If this was a patch in a different format than the instrument you created, a device of this type will replace the orig-
          inal device (see “Cross-browsing patch files”).

      6. Continue to add new instrument patches in the same way until you have all the patches you need.
      7. When you’re done, select the (The Band) Favorites List folder.
          All the patches you added are now listed in the Browser list.
      8. Use drag and drop to order the patch files in the Browser list according to the set list.
      9. Double click the first patch file in the (The Band) Favorites List.
          The the patch is loaded in the appropriate device.
      D   If you have a MIDI keyboard or control surface with programmable buttons, you can assign a button to “Select
          next patch” on the device.
          Many MIDI keyboards and control surfaces have buttons assigned to patch selection - check the Control Surface
          Details document for information about your controllers. Alternatively, you can manually assign buttons for select-
          ing patches - see the “Remote - Playing and Controlling Devices” chapter.
      10.Save the Song.
      11.At the gig, open the song, and the first patch will be loaded.
      12.When the first song is finished, use the “next patch” button on the device or on your MIDI keyboard and the
         next patch in the (The Band) Favorites List will be loaded!

      Selecting and auditioning samples and REX loops
      For audio files, samples and REX loops you can use the Audition controls in the Browser to preview the audio. This
      is done in the following way:
      D   Select the audio or REX file in the Browser list and click the triangular Play button.
          The file is played back. During playback, the Play button in the Audition section switches to a square “Stop” button
          - click this to stop playback.

      D   Alternatively, you can click the Auto button to automatically audition the file as soon as you select it in the
          Browser list.
          The selected file is automatically played back. Again, click the Stop button to stop playback.

      D   Adjust the playback level with the slider to the right of the Auto button.

      Selecting multiple files
      It is possible to select multiple files in the Browser, by using standard [Shift] or [Ctrl](Win) or [Cmd](Mac) selection
      techniques. This, however, doesn’t necessarily mean that the selected files can be loaded. There are a number of in-
      stances where selecting several files in the Browser file list is relevant:
      • It is possible to load several drum patches (on consecutive pads) simultaneously into the Kong device.
          See the “Kong Drum Designer” chapter for details.
      • It is possible to load several samples simultaneously into the NN-XT, NN19 and Kong NN-Nano sampler de-
        vices.
          See “NN-19 Sampler”, “NN-XT Sampler” and “NN-Nano Sampler” for details.
      • It is possible to load several REX files simultaneously into the Dr. Octo Rex device.
          See the “Dr. Octo Rex Loop Player” chapter for details.
      • It is possible to simultaneously import multiple audio files to the sequencer.
          See “Importing audio to the sequencer” for more info.
      • You can select several files to add them to a Favorites List in one go - see “Favorites Lists”. Note that this is
        only possible if a device does not have browse focus!
      !   In situations where several selected files (e.g. patches or songs) cannot be loaded, the Create/Load button in
          the Browser is grayed out.

      Cross-browsing patch files
      Cross-browsing patches is a powerful feature of the Browser. It allows you to browse for any type of instrument
      patches or effect patches, regardless of which instrument or effect device you opened the Browser from.

      About instrument and effect patches
      Patches are internally divided into two patch categories in the Browser; instrument patches and effect patches (the
      Browser “knows” what type of patch it is). This is because instrument patches and effect patches are fundamentally
      different - instruments are played, and effects are used to process sound - and you would logically browse for one or
      the other, but not both.
      • When browsing patches from an existing instrument device, including instrument Combinators, no effects
        patches are shown in the Browser list.
      • When browsing patches from an existing effect device, including effect Combinators, no instrument patches
        are shown in the Browser list.
      !   When browsing Insert FX patches for an audio track, Mix Channel or the Master Section, cross-browsing is not
          possible (you can only load effect Combinator patches).

      Cross-browsing - an example:
      1. You are playing a Subtractor device but feel that the sound isn’t quite what you had in mind, so you click the
         Browse Patch button on the Subtractor to set Browse focus and check out some other patches.
      2. After browsing Subtractor patches for a while, you still haven’t found the type of sound you wanted, so you
         click the Root Folder drop-down list and select “Reason Factory Sound Bank” from the list:

          From here you can select instrument patches for any device. You decide to browse a folder containing Malström
          patches.
      3. As soon as you load a Malström patch from the Browser, a Malström device replaces the Subtractor device in
         the rack.
          The sequencer track which was previously assigned to the Subtractor is now assigned to a Malström with the se-
          lected patch loaded.
      • The name of the sequencer track and the Mix Channel device (and channel strip in the main mixer) are auto-
        matically changed to the Malström patch name.
      !   Note that is only true if you haven’t manually renamed the sequencer track earlier. If you renamed the se-
          quencer track earlier, it will keep this name regardless of what device or patch you load. However, if you delete
          the custom name, the sequencer track and Mix Channel device will show the patch name again.

      D   You can continue to browse and load patches and play your keyboard to try them out.
          Each time you load a patch that belongs to a different device, this device automatically replaces the previous de-
          vice in the rack.
      • Cross-browsing for an effect patch it works in the same way - loading an effect patch of a different format will
        replace the current effect device in the rack.

      Special instances of cross-browsing
      There are a few instances when replacing an existing device by loading other device patches might lead to lost cable
      connections in the rack:
      • When a device is replaced by another device type, audio connections may be lost.
          An example is replacing an NN-XT, which can use up to 16 audio outputs, with a Subtractor which only has one
          audio output.
      • When a device is replaced by another device type, CV connections on the back panel may be lost.
          The only connections that are retained between device types are Sequencer Control CV/Gate in.
      !   If you encounter such situations and you want to restore the original connections, use the “Undo” function.
          Browsing back to the original device patch will not restore lost connections.

      Create Instrument/Create Effect
      These functions allow you to browse for any kind of instrument or effect patches. This is essentially the same as
      cross-browsing, except that you do not start with an existing device. The “Create Instrument/Effect” functions are
      very useful if you’re looking for a specific type of sound or effect but don’t know, or don’t care, what devices are used.
      For example, you might be looking for a “pad” sound or a “delay effect”. Once you’ve found what you’re looking for,
      you can just load the sound or effect in the required device(s).
      1. Select “Create Instrument...” or “Create Effect...” from the Create menu.
          The Browser opens. Depending on your selection, only Instrument Patches or Effect Patches are shown.
      2. When you load a patch, a corresponding device is created automatically.
          If you load an instrument device patch, a corresponding sequencer track will also be automatically be created. If an
          “empty” Mix Channel device isn’t available in the rack, a new one will be automatically created - with its channel
          strip in the Main Mixer. The instrument device will be automatically connected to the Mix Channel device. Master
          Keyboard input will be set to the new track so that you can play the patch from your master keyboard. The se-
          quencer track, Mix Channel and channel strip in the Main Mixer automatically gets the name of the loaded patch.

      About patch formats and sampler devices
      As both the NN-XT and NN19 sampler devices can load patches in the NN19 (.smp) and REX (.rx2/.rcy/.rex) for-
      mats, there must be certain rules regarding cross-browsing.
      • The basic rule is that the Browser will load such patches into the original device type (the device you opened
        the browser from), whenever possible.
          Thus, when the patch format is NN19 (.smp) or REX (.rx2/.rcy/.rex) and the NN19 device has browse focus, the
          patch will be loaded into this device.
      • If you are browsing from any other type of device, these patch types will be loaded into an NN-XT device.
      • If you are using the “Create Instrument” function, an NN19 (.smp) patch will create a NN19 device and a REX
        patch will create a Dr. Octo Rex device.

      Using the “Search” function

      The Search function allows you to search for patches, songs, audio files etc. The Search field is always available at
      the top of the Browser.
      D   Press [Command]/[Ctrl]+[F] to set the Browser focus to the Search field at any time.
      D   Type in a search text and the search results will automatically begin to display in real-time as you type.
      • The search happens in the currently shown folder/location (shown above the Search field) - and in all its sub
        folders (if any).
          The Root folder popup above the Search field shows "Searching <location>" where location is the current search
          folder. The search looks for items (including folders and ReFills) with matching names. We don't show the con-
          tents of a folder with matching name - we show the folder itself.
      • If you like you can change the search location/folder and redo the search in the new location/folder.

      The search result view in the Browser list

      • The search result is shown in alphabetical order, in separate groups. If you search in the Factory Sound Bank
        the result is divided into “Instrument Patches”, “Effect Patches”, “Other Patches”, “Samples” and “Folders”,
        with files and folders whose names match the search string.
          If there are no search hits, the Browser list is empty.
      • A new “Parent” column also appears, listing the name of the parent folder for each file in the Browser list.
          If you select a file in the Browser list, you can pull down the “Root Folder” drop-down list and select “Go to Parent
          folder” - this opens the parent folder for the selected file:

          In this example, selecting the Go to Parent Folder takes you to the “Synth FX” folder
          To go back to the search result Browser list, click the Back button:

      • When searching in the Instruments/Effects/Utilities palette, the search result view shows matching devices
        only, not the manufacturer headings.

      Loading files
      When you have navigated to the desired folder (on your hard disk or within a ReFill) and located the desired file, you
      load it by double clicking it in the Browser list, or by selecting it and clicking the Open/Load/Create/Import button.
      The name of the button differs depending on what command you used for locating the file.
      q   Once you have loaded a patch into a device (that now has browse focus), you can select and automatically load
          new patches by pressing the up/down arrow keys on your computer keyboard.

      About browse lists
      When you click the Open/Load/Create/Import button to open a file from the Browser, the file and folder list shown
      at that time is memorized for that device. This is called a “browse list”.
      For patches (and to a certain extent samples) this list provides a specific functionality:
      • The browse list is what applies when changing patches using the Next/Previous Patch buttons on the front
        panel of a device (or from patch selectors on a control surface).
      • The browse list is shown as the patch list when you click in the patch name field for a device.
      • For samples, the browse list applies when changing samples using the Next/Previous Sample buttons on the
        front panel of a sampler device.

      What can a browse list contain?
      • When you load a patch or sample by clicking Load/Create/Import in the Browser, the resulting browse list will
        include the files contained in all currently open folders in the Browser.
          If you open the Browser (set Browse focus) again from the same device, the same file and folder structure is
          shown.
      • If you save the current song and reopen it, the items in the browse list will be shown as a “flat” list, and the
        “Root Folder” field will show “Document Browse List”.
          In these situations, the Browser will show the “Parent” column, listing the names of the source folders. The “Root
          Folder” drop-down list will also contain the item “Go to parent folder” for a selected file.
      • A browse list could also be a Search result, or a Favorites List.
          Favorites Lists provide a way of controlling/filtering which patches or samples will be available on a browse list for
          a device - see “Using Favorites - a practical example”!
      !   Note that if you opened a patch after having used cross-browsing (see “Cross-browsing patch files”) or used
          the Search function (see “Using the “Search” function”), the active browse list could contain patches of differ-
          ent formats, and loading patches from the device panel could change the device type.

      Handling Missing Sounds
      Sampler patches, drum machine patches, Dr. Octo Rex patches, and SoundFonts contain references to samples -
      files on your hard disk. The same is true for songs that contain samples (in sampler or drum machine devices) or REX
      files. If any of these files have been moved, renamed or removed when you try to open the patch or song, Reason will
      alert you that files are missing by showing the “Missing Sounds” window. The “Missing Sounds” window also appears
      if patches in the song are part of a ReFill which has been moved, removed or is not installed on your computer:

      The “Missing Sounds” window.

      The main display in the Missing Sounds window lists all missing files. The three columns show the following proper-
      ties:

      | Column                                 | Description
          Device                               Shows the name of the device in which the missing sound is used, along with a device
                                               type icon.
          Sound                                Shows the name of the missing file, along with a file type icon.
          Part of ReFill/R.E.                  If the missing file is part of a ReFill (or a SoundFont within a ReFill) or a Rack Extension
                                               device, this column shows the name of the ReFill/SoundFont/Rack Extension.

      Below the main display are four buttons:
      D     Select a file in the list and click the “Download ReFill/R.E.” button to open your web browser and download
            (and purchase, if necessary) the ReFill/R.E from the Reason Studios website.
      D     Click the “Search Folder” button to automatically search for and find the missing files in the currently selected
            folder in the Browser.
      D     Click the “Search Locations” button to automatically search for and find the missing files in any of the Loca-
            tions present in the Browser.
      !     If you have a lot of ReFills and folders in your Locations, the search could take a while.
            If you want to abort the search, click the Cancel button in the “Searching...” window:

            When you have found the sound you want to replace the missing sound with, double click it or select it and click
            the Replace button in the Browser:

            Replacing a missing sound.
            The selected missing sound in the Missing Sounds window now disappears from the window and you can select
            the a new missing sound to replace.
      D     If you want to replace a missing sound without searching for it, select the missing sound in the list and click
            the “Replace” button. Then use the Browser to select and replace the sample.
            If you like, you could replace missing sounds with new sounds - it doesn’t have to be the original ones. When you
            save the Patch or Song later on, the new sounds will permanently replace the previous (missing) sounds.

      D   Alternatively, close the Missing Sounds window.
          The song or patch will still work, but with sounds missing. This means that sampler patches, drum machine patches
          and/or loop players will not play back correctly.
          On the panels of the concerned devices, missing samples are indicated with an asterisk (*) before the file names:

                                     This sample is missing

          A Redrum device with a missing sample in one of its slots.
      D   If you want to continue searching for and replacing missing sounds later on, you can open the Missing Sounds
          window again by selecting “Show Missing Sounds Window” from the Windows menu.

      Reason file formats
      The following table lists the file formats that you can browse and open using Reason’s browser:


=== END OF PART ===
