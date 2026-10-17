# Chapter 09: Reason 12 manual digest and studio workflow
## Part 53 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 44 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 54 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 44 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 19: Song File Handling

Song File Handling

      About this chapter
      This chapter describes how to open, create and save songs in various ways. It also describes how to save a song as
      a Template and how to import and export songs as Standard MIDI files.

      Opening Songs
      Opening a Reason or Record Song
      !   To be able to open a Reason Song (or a Reason Essentials/Reason Intro/Reason Lite/Record Song), you need
          to run Reason in Authorized mode. If you’re using Reason in Demo Mode (unauthorized), the “Open” item on
          the File menu is removed and replaced by “Open Demo Song”. This allows you to open only the factory made
          Reason Demo Songs (see “Opening a Reason Demo Song”). See “Authorizing Reason” for details on how to
          authorize Reason.
      To open a Reason Song:
      D   Double click the Song file in Windows Explorer (Win) or in Finder (Mac).
      Or, if you want to open a Song file from within the program:
      1. Hold down [Ctrl](Win) or [Cmd](Mac) and press [O], or select “Open” from the File menu.
          The Browser appears (if it was hidden) in the Song window.
      !   If no Song document was open on the macOS version of Reason, Reason temporarily opens an empty Song
          document to be able to show the Browser. When a Song has been loaded, the empty document closes.
      2. Navigate in the Browser to the desired folder on disk or within a ReFill.
          See “Using the Browser” in the “Sounds and Patches” chapter.
      3. When you have located the Reason (.reason, .rsndemo, .ree, .reedemo, .rei, .reidemo, .relt, .reltdemo, .rltd, .rns,
         .rps or .rsb), or Record Song file (.record or .recdemo), select it and click “Open” (or double click the file).
          The song opens in a new document window.
      q   You can have several Songs open at the same time if you like. This allows you to drag and drop (and copy and
          paste) patterns, clips and patches between songs. However, all open songs consume some memory and pro-
          cessing power, so you might want to close songs you don’t need for the moment.
      q   It’s also possible to have Reason open the last song you worked on as soon as you launch the program. See
          “Opening the last Song at program launch” for more information.

      If the “Missing Sounds” window appears
      If the song includes samples or REX files, and these have been moved or renamed since the song was saved, the
      program will inform you that it cannot find all files. You can then choose to either manually locate the missing files, to
      have the program search for them or to proceed without the missing sounds. For details, see “Handling Missing
      Sounds” in the “Sounds and Patches” chapter.

      If “Missing Device” panels appear in the rack
      When you open a Reason song made by another user, it may have been created with Rack Extension devices that
      you don't have. All such missing devices in a song will be replaced by generic “Missing Device” placeholder devices.
      See “About missing Rack Extensions” for more information.

      About opening Reason Version 5 (or earlier) Songs in Reason Version 12
      If you run Reason in Authorized mode, it’s also possible to open older Reason (.rns, .rps and .rsb) songs. A Reason
      Song created in Reason Version 5 or earlier will end up in a separate Song document, just like an ordinary Reason
      Version 12 Song. All Rack device and sequencer track configuration will be preserved as well as all cable connec-
      tions. The only things that will be changed are these:
      • The Main Mixer Master Section will be connected to Outputs 1 and 2 of the Reason Hardware Interface.
      • The Rack device that was connected to outputs 1 and 2 on the Reason Hardware Interface in the old song will
        now be connected to a new Mix Channel device, below the Master Section device in the Rack.
      • If there were any more connections to the Reason Hardware Interface in the song, these will now be connected
        to new mono Mix Channels.
      • Below the Mix Channel devices in the Rack, the devices from the Reason song will appear in a single rack col-
        umn, just like they did in the earlier version of Reason.
      !   If you open a Reason Published Song (.rps), you cannot save etc., and the “Export Audio” and “Bounce Mixer
          Channels” functions will only work if you haven't manually changed anything in the Song document.
      q   If you want to re-route the instrument devices from the 14:2 Mixer in the old Reason Song to separate Mix
          Channels in the Reason Version 12 Song, there is kind of a semi-workaround for this, see “About re-routing
          devices in songs created in Reason Version 5 or earlier”.

      Opening a Reason Demo Song
      Reason Demo Songs are factory made songs that demonstrate how Reason can be used in various musical projects.
      If you run Reason in “Demo Mode” (unauthorized), you will only be able to open Demo Songs - but not regular Songs.
      If you run Reason in authorized mode, the Open Demo Song item is available in addition to the regular Open item.
      D   Select “Open Demo Song” from the File menu and select a Demo Song from the sub-menu.
          You could also select “Download more Demo Songs” from the sub-menu. This will open your default web browser
          and direct you to the Reason Demo Songs page on the Reason Studios web site. On this page you can download
          additional Reason Demo Songs to your computer. You will then have to use the “Open Demo Song” command
          from the File menu to open the downloaded Demo Songs.
      q   You can also download more Reason Demo Songs by selecting “Download more Demo Songs” from the Help
          menu.
      q   You can have several Demo Songs open at the same time if you like. This allows you to drag and drop (and
          copy and paste) patterns, clips and patches between songs. However, all open songs consume some memory
          and processing power, so you might want to close songs you don’t need for the moment.

      Opening the last Song at program launch
      It’s possible to instruct Reason to automatically open the last Song you worked on each time you launch Reason. You
      select this on the “General” tab in the “Preferences” dialog.
      1. Select “Preferences” from the Edit menu (Win) or “Reason” menu (Mac) and then click the “General” tab.

      2. Tick in the “Load last song on startup” checkbox.
          When you launch Reason the next time, the last saved Song will automatically open in a document window.

      Closing Songs
      Closing a Song
      D   To close a Song, hold down [Ctrl](Win) or [Cmd](Mac) and press [W], or select “Close” from the File menu. Al-
          ternatively, click the close button in the upper corner of the Song document window.
          If you have unsaved changes, you will be asked if you want to save the song before closing.
      !   Note that when you’re closing the last open Song document in the Windows version of Reason, the Reason ap-
          plication will quit.

      Creating Songs
      Creating a new Song
      D   To create a new song, hold down [Ctrl](Win) or [Cmd](Mac) and press [N], or select “New” from the File menu.
          A new Song document window appears. By default, the new Song contains the following:
      • The Reason Hardware Interface.
      • The Main Mixer Master Section with its Master Section device in the Rack.
          The Master Section device’s Master Out L & R are connected to the Reason Hardware Interface Audio Out 1 & 2.
      • The Transport Track at the top of the Sequencer.
      q   Instead of creating an empty song each time you select “New”, it’s possible to automatically load an existing
          song to use as template for your new songs. For example, if you want to start with your own unique selection
          of devices, you can create and save a song and then instruct Reason to use this song each time you create a
          new song. See “Setting up a Default Song”.
      q   An alternative to creating a new song is to use the “Create New from Template” command to open one of the
          factory made Template Songs. See “Creating a new Song from a template”.

      Setting up a Default Song
      It’s possible to specify a certain Song document which will automatically open as a “template” each time you select
      “New” from the File menu. The Default Song could be any Song you have created earlier, or a factory made Template
      Song. You can select this Default Song on the “General” tab in the “Preferences” dialog.
      1. Select “Preferences” from the Edit menu (Win) or “Reason” menu (Mac) and then click the “General” tab.

      2. Click the “Template” radio button in the “Default Song” section.
      3. Click the folder icon to the right and select the Song you want to use as a template when creating new Songs.
          Each time you create a new Song (by selecting “New” from the File menu), the selected Song will be loaded and
          used as a template for your new Song. On Windows platforms, the Song document will be named “Document n”
          where “n” is an incremental number. On macOS platforms, the document will be named “untitled n” where “n” is an
          incremental number. You can then save your Song with a new name.
      !   Make sure the “Load last song on start-up” checkbox is not ticked, otherwise the last song will be opened in-
          stead of the Template song you selected.

      Creating a new Song from a template
      D   To create a new song from a Template, select “New from Template” from the File menu and then select one of
          the Template Songs that appear in the sub-menu.
          The selected Template Song appears in a new document window. On Windows platforms, the document will be
          named “Document n” where “n” is an incremental number. On macOS platforms, the document will be named “un-
          titled n” where “n” is an incremental number. You can then save your Song with a new name.
      q   You could also create your own Template Songs and make them appear in the sub-menu. See “Making a Song
          appear as a Template Song”.
      q   You can also download more Reason Template Songs by selecting “Download more Template Songs” from
          the Help menu.

      Saving Songs
      Saving a Song
      You will always be able to save your Songs in Reason. It doesn’t matter if you’re running in authorized or unauthorized
      (Demo) mode.

      The “Save” function
      To save a Song, proceed as follows:
      1. Hold down [Ctrl](Win) or [Cmd](Mac) and press [S], or select “Save” from the File menu.
          If this is the first time you’re saving the song, a file dialog will appear where you can specify a name and destina-
          tion.
      2. Specify a name and destination for the Song and click “Save”.
          Once you have saved a song, selecting “Save” will simply save it under the same name and in the same location,
          without showing a dialog.
      q   It’s also possible to automatically include all samples used by the Reason devices and make the Song “self-
          contained”. Refer to “About Self-Contained Songs” for details about how to include your own samples in your
          songs.
      q   To reduce the file size of your song, you can use the “Save and Optimize” command described in “Saving and
          optimizing a Song”.
      q   It’s also possible to include detailed information about your song. Refer to “Including Song Information” for
          more details.

      The “Save As...” function
      To save an existing Song under another name and/or in another location:
      1. Hold down [Ctrl]+[Shift](Win) or [Cmd]+[Shift](Mac) and press [S], or select “Save As...” from the File menu.
          The “Save As” dialog appears.
      2. Specify a new name and/or new destination for the Song and click “Save”.
      q   Using the “Save As...” function will automatically optimize the Song (see “Saving and optimizing a Song”).

      Saving and optimizing a Song
      When you record audio in the Sequencer, the recordings are stored in your Song document. If you remove recordings
      in your song while editing, there might be “empty” areas left in the document, similar to a fragmented hard disk. To
      “defragment” the Song document, and thus reduce the file size, you can use the “Save and Optimize” command on
      the File menu. Note that the “Save and Optimize” command can only be used on previously saved Song documents.
      D   Select “Save and Optimize” from the File menu.
          The Song will be optimized and saved at the original location.
      !   Note that saving and optimizing a Song could take a couple of minutes if you have lots of audio recordings in
          it. Therefore, the best alternative would probably be to use the “Save” command while you’re still working with
          your Song, and then use the “Save and Optimize” command as a final step when you’ve finished editing.
      q   Using the “Save As...” function automatically optimizes the Song.
      q   In some situations, it’s possible to reduce the file size even further by deleting any recordings you haven’t used
          in your Song. See “Delete Unused Recordings”.

      Including Song Information
      Selecting “Song Information” on the File menu opens a dialog in which you can add information about your song. For
      example, if you plan to send the song to other Reason users, this dialog allows you to add contact information, com-
      ments about the song, etc.
      D   Select “Song Information...” from the File menu.
          The Song Information dialog opens.

          The Song Information dialog contains the following items:
      • Text in window title:
          The text you add here will be displayed directly after the file name in the song window’s title bar.
      • More information:
          This is where you could add notes and comments about your song.

      • Song splash:
          This allows you to add a picture to the song. The picture will be displayed when the song is opened.
      D   To add a splash picture, click the folder button at the upper right corner, locate and open the picture file in the
          file dialog that appears.
      !   Splash pictures must be JPEG files (Windows extension “.jpg”) with a size of 256 x 256 pixels.
      D   To remove the splash picture from the song, click the “cross” button at the upper right corner.
      D   Tick the “Show splash on song open” check box to make the splash appear every time the song is opened.
      • Author’s web page:
          Here, you can type in your web site URL. When a user opens your song, he/she can go directly to your web site
          by clicking the Browse button that appears in the splash (provided there’s an Internet connection available).
      • Author’s e-mail address:
          Here, you can specify your e-mail address if you want other Reason users to e-mail you their comments, etc.

      About Self-Contained Songs
      The Song is the main file format in Reason. A Song contains the device setup and all settings and connections in the
      Rack, all Main Mixer Channel settings as well as everything you have recorded in the Sequencer. However, this is not
      always sufficient. If you want to open your song on another computer, or send it to another Reason user, you will also
      need to include all samples and REX files used by the Reason devices in the Song. To make this easier, Reason al-
      lows you to create “self-contained” songs. A self-contained song contains not only the references to the used sam-
      ples and REX files, but also the files themselves. You can choose exactly what files should be included in the self-
      contained song.
      q   An alternative to self-containing samples and/or REX files could be to bounce Mixer Channels to Audio
          Tracks. This way, you could “convert” ReFill samples to audio so that your song would always sound the same,
          no matter on which computer you play it back. See “Bouncing Mixer Channels” for details.
      To specify what files should be included in the self-contained song, proceed as follows:
      1. Select “Song Self-Contain Settings...” from the File menu.
          The “Song Self-Contain Settings” dialog appears, listing all samples and REX files used in the song:

      2. Tick the checkboxes to the left of the “Name” column for the files you want to contain in the song.
          Note that samples and REX files from ReFills can also be self-contained (but not un-self-contained, see below).
      D   You can use the “Check All” button to tick all checkboxes in one go.
          Similarly, the “Uncheck All” button unchecks all checkboxes.
      3. When you have marked the desired sounds, click “OK” to exit the dialog.
          The next time you save your Song, the specified sounds will be automatically included in the Song file.
      !   Note that a self-contained song file will be larger than the original song file. However, samples included in a
          self-contained song are automatically compressed by approximately 50% of their original size. Since the com-
          pression is lossless, this does not in any way affect the sound quality.

      “Un-self-containing” a Song
      If you have a self-contained song which contains one or several sounds embedded in the song file, you may want to
      extract these sounds and make the song refer to them on disk as usual. This is done in the following way:
      1. Select “Song Self-Contain Settings...” from the File menu.
          The “Song Self-Contain Settings” dialog appears.
      2. Locate the sounds you want to extract from the song file, and deactivate their checkboxes (or click the “Un-
         check All” button).
      3. Click “OK” to close the dialog.
          Now, Reason will check for each “extracted” sound file whether it is available (at its original, stored location) or not.
      • If the program finds the sound file at the location stored in the song, it is simply removed from the song file,
        and the original file reference path is used.
          This would be the case if you made the song self-contained yourself, and un-self-contain it on your own computer
          (provided that you haven’t removed the original sound files from disk since you made the song self-contained).
      • If the program doesn’t find the sound file, a file dialog appears, allowing you to select a folder and name for
        the sound file.
          The extracted file will be saved in the specified folder, and the path in the song will be adjusted. This would be the
          case if you were given the self-contained song by another user, for example.
      !   Note that it is not possible to un-self-contain samples that originate from ReFills!
      !   If you un-self-contain samples that were modified in the Edit Sample Window and feature Start and End Mark-
          ers and/or loop crossfades, the Lossy Sample Export dialog appears. The available options are described fur-
          ther down in the “Exporting samples” section in the Sampling chapter. Note that the option you select in the
          Lossy Sample Export applies to all samples you have deselected in the Song Self-contain Settings dialog!

      Making a Song appear as a Template Song
      If you want Songs you have created to appear on the “New from Template” sub-menu, and be available for selection
      when you use the “New from Template” command (see “Creating a new Song from a template”), you need only move
      or copy the Song(s) to the Template Songs folder in the Music folder on your hard drive. The easiest way to get to this
      folder is by selecting File > New from Template > Show Template Folder. This brings up the Template folder in Win-
      dows Explorer or Finder on Mac.

      A note about saving Songs as audio files
      It’s also possible to export your Songs as audio files in WAV or AIFF format. Refer to “Exporting Songs or parts of
      Songs” for more information.

      Audio data and Scratch Disk settings
      About audio data in Song files
      If you record or import audio into an unsaved Song document, the audio is written to the “Scratch Disk folder” on your
      computer. As soon as you save (and name) the Song document, the audio is moved from the Scratch Disk folder to
      the Song document. From here on, all new recorded and/or imported audio is stored in the Song document.

      Changing Scratch Disk folder location
      The Scratch Disk is where Reason stores new, unsaved songs, plus analysis data (waveform data and high-quality
      time stretch/transposed audio/sample rate conversion data).
      By default, Reason places the Scratch Disk folder in the system temp folder in your home directory. You can change
      the Scratch Disk folder location if you like:
      1. Select “Preferences” from the Edit menu (Win) or Reason menu (Mac) and then click the “Folders” tab.

      2. Click the “Change” button in the Scratch Disk Folder section.
          A system folder browser opens where you can select - or create - a new folder.
      3. Select the folder where you want to locate the Scratch Disk Folder and click “OK”.
      4. Restart the computer and relaunch Reason.
      D   If you later want to revert to the default setting, click the “Reset” button on the “Advanced” tab.
          The custom Scratch Disk Folder setting is removed and is replaced by the default setting. You will then have to re-
          start the computer for the change to take effect.

      About unavailable Scratch Disk Folder
      If a custom assigned Scratch Disk Folder isn't available when you launch Reason, an alert saying: "The selected
      Scratch Disk folder isn't available. Reason will use the default scratch disk for this session." is shown. This could hap-
      pen if you have assigned the Scratch Disk folder to a removable disk and that disk is currently unavailable.
      D   Click “OK” to use the default Scratch Disk Folder.
      The next time you launch Reason, it will look for the custom assigned Scratch Disk Folder again, and will do so every
      time you launch Reason, until you reset the custom assignment by clicking the “Reset” button.

      About “Orphan Audio Streams”
      If your computer should malfunction (due to power loss etc.) during recording into a previously saved Song document,
      there is a good chance that your last unsaved audio recordings can be (at least partly) recovered:
      1. Restart your computer and launch Reason.
      2. Open one of the Song documents that was open during the computer malfunction.
          If the Song contained unsaved audio recordings, Reason will find these and show an alert saying that the Song
          contains “orphan audio streams”. You will be given the choice of deleting them or having them appear in new clips
          on a new audio track, for salvaging.
      !   Note that it’s only audio recordings that it’s possible to recover. Any new Instrument Tracks in an unsaved
          Song will be lost in the case of computer malfunction.

      Importing and exporting Standard MIDI Files
      Reason can import and export Standard MIDI Files (SMF). This allows you to transfer MIDI data between Reason and
      other applications.

      Importing Standard MIDI Files
      To import a Standard MIDI File to the Reason sequencer, follow these steps:
      1. Create a new, empty Song document.
      2. Select “Import MIDI File...” from the File menu.
          The Browser appears (if it was hidden).
      3. Select a Standard MIDI File (.mid) in the Browser and click “Import”.
          A number of new tracks are created in the Reason sequencer. The tracks will have their original name, with their
          original MIDI channel added. Each track will be assigned an ID8 device, loaded with a sound that resembles the
          original sound. These assignments will only serve as a starting point to be able to play back the imported MIDI file.
          You may want to change sound, or replace the ID8 with another device if you have Reason installed.
      • The Note events in the MIDI file will be imported into one or several Note Clips on a Note Lane on each Track.
      • If the imported MIDI file is a Type 1 MIDI file, there will be one sequencer track for each track in the MIDI file.
      • If the imported MIDI file is a Type 0 MIDI file (that is, it contains one track with MIDI events on multiple chan-
        nels), there will be one sequencer track for each used MIDI channel.
      • The Tempo setting, any Tempo Automation and any Time Signature automation in the MIDI file will be recog-
        nized.
      • All controller data in the MIDI file is included.
          This means that standard performance controllers (Pitch Bend, Mod Wheel etc.) are preserved properly and will be
          included in the note clip, just as when recording in Reason. If there are separate MIDI Controllers in the imported
          MIDI file, these will be imported to separate Automation Lanes on the Instrument Tracks. There is a chance that
          some controller data may be imported to alien clips, due to different interpretations of a controller by a device in
          the rack and the MIDI instrument used to create the MIDI file (see “About alien clips”).

          Green frames will appear for automated parameters on the ID8 device panels. This helps you locate any unwanted controller
          automation.

      Exporting Standard MIDI Files
      To export all Instrument Tracks and Automation Tracks from the Reason sequencer as a Standard MIDI File (SMF),
      do like this:
      1. Set the End Marker in the sequencer to where you want your song to end.
          The MIDI file will contain all MIDI events on all tracks from the start of the song to the End marker.
      2. Select “Export MIDI FIle...” from the File menu.
          The standard file browser appears.
      3. Type in a new file name (if desired) and select location for the file to be exported. Then, click “Save”.
          The default name for the MIDI File will be the Song’s name followed by the “.mid” extension.
          MIDI files exported by Reason will have the following properties:
      • The MIDI file will be of Type 1, with one MIDI track for each track in the Reason sequencer.
          The tracks will have the same names as in the Reason sequencer.
      • Since the Reason sequencer doesn’t use MIDI channels as such, all tracks will be set to MIDI channel 1.
      • The sequencer Tempo, and any Tempo Automation and/or Time Signature Automation, is included in the MIDI
        file.
      !   Since an Instrument Track in Reason could consist of different types of devices (plus FX etc.), there is no infor-
          mation about the actual sound in the exported MIDI File. The exported MIDI File only contains information
          about each instrument track and its MIDI Notes and/or MIDI Controller data laid out on the track. You will have
          to manually assign appropriate sounds to each track in the importing application.

528   SONG FILE HANDLING


---

<a id="importing-and-exporting-audio-20"></a>

=== END OF PART ===
