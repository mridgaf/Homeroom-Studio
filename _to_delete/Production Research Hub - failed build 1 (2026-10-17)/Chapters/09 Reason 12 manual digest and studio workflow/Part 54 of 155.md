# Chapter 09: Reason 12 manual digest and studio workflow
## Part 54 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 45 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 55 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 45 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 20: Importing and Exporting Audio

Importing and
Exporting Audio

      About this chapter
      This chapter describes the various techniques you can use to import and export audio to and from Reason.

      Importing audio
      Audio formats, sample rates and tempo matching
      The Reason sequencer supports import of mono and stereo audio files of various formats, sample rates and resolu-
      tions. Reason also supports import of REX (ReCycle rcy, rex and rx2) files. You can import several audio files at the
      same time, with each audio file ending up on a separate Audio Track in the sequencer - or on separate Comp Rows
      in a selected Audio Clip. You can import files of different formats on the same Audio Track - or even in the same Au-
      dio Clip. One audio file could be an 8-bit mono file sampled at 22.05 kHz, the next a 24-bit stereo file sampled at 192
      kHz, etc. Reason automatically converts sample rates and resolution with preserved audio quality. If the imported au-
      dio file includes tempo data that Reason supports, Reason automatically matches (stretches) the audio file to fit the
      current Song Tempo, without affecting the pitch.
      • if the imported audio files’ sample rates differ from the current audio hardware sample rate, Reason will auto-
        matically sample rate convert.
        This will first be done with a real-time algorithm, allowing for immediate playback. In the background, a high-quality
        sample rate conversion is performed. This is indicated by the CALC indicator on the transport panel. When done,
        Reason will automatically switch to playing back the high-quality version and the CALC indicator will go out.

        The CALC indicator indicates when Reason performs high-quality stretching of audio.

      About tempo matching imported audio
      When you import an audio file, which has tempo data that Reason can read, the audio will be automatically stretched
      to fit the current tempo in the song. However, if the tempo in the imported audio is unknown, you could manually
      tempo match (stretch) the imported audio in a couple of ways:
      • By using the Scale Tempo “tool” to manually stretch the audio clips, see “Tempo scaling Clips”.
      • By using the Scale Tempo function in the Tool Window, see “Scale Tempo”.
      • If the imported audio has a steady - but unknown - tempo, you can adjust the imported audio to the song
        tempo as described in “Matching imported audio to the song tempo”.

      Importing audio to the sequencer
      !   To minimize the song saving time, we strongly recommend to save the song before you import many or large
          audio files.
      To import one or several audio files to tracks in the sequencer, proceed as follows:
      1. Select “Import Audio File...” from the File menu, or hold down [Ctrl]+[Shift](Win) or [Cmd]+[Option](Mac) and
         press [I].
          The “Import Audio File” function gets browser focus:

      2. Browse and select the audio file(s) you want to import.
          When you select a single audio file, information about length, format, size and tempo (if included in the file) is
          shown in the information section, below the Browse list. If you like, you can also preview selected audio file by
          clicking the “Play” button in the “Audition” section. If you select several audio files, the total number of files and
          their total size are displayed in the Details section. You will not be able to preview the audio files when several files
          are selected.
      D   You can also import samples from the Song Samples location in the Browser.

      !   If you select a REX file, this will be rendered to audio when imported and all information about slice positions
          etc. will be lost. The Song Tempo and any Tempo Automation starting at the Song Position Pointer will be
          taken into account during the import. After the import, the REX file will behave just like any imported audio
          file.
      !   If you are going to edit the imported REX file inline, and work with slices, audio quantizing, stretching etc. Rea-
          son will automatically detect the transients in the audio and generate new slice markers that might not corre-
          spond to the original slice distribution of the imported REX file, see “Editing audio in Slice Edit mode”.
      3. Click “Import” to import the audio file(s).
          Depending on the where the edit focus was when you selected “Import Audio File” from the Edit menu, the audio
          file(s) will be placed a little differently. In all scenarios, the imported audio file(s) will be placed at the current song
          position:
      • If an audio track has edit focus in the sequencer track list and you have selected only a single audio file, the
        imported audio file will be placed in a new clip on this audio track.
      • If you selected several audio files when using the Import Audio File command, each audio file will be imported
        to new audio tracks in the sequencer - in the order the files were selected in the Browser.
      • If you selected only a single audio file and the edit focus is elsewhere in the application, a new audio track will
        be created for the imported audio file.
      D   You can also drag one or several audio files from the Browser and drop in the sequencer track list.
          The audio files will then be imported to separate audio tracks in the sequencer:

          A + sign and a divider indicate where in the track list the imported audio file(s) will be placed.
      D   You can also drag one or several audio files from the Browser and drop on an audio track on the Arrange Pane.
          The audio files will then be imported as separate audio clips, after one another, on the corresponding audio track.
          If Snap is active in the sequencer, this will be taken into consideration:

          A waveform sign and an insertion point divider indicate where on the audio track the imported audio file(s) will be placed.

      Import audio file(s) to an open Audio Clip
      It’s also possible to import audio files to open Audio Clips in the Comp Editor in the sequencer. Proceed as follows:
      1. Open the Audio Clip you wish to import the audio file(s) to in the Comp Editor.
      2. Select “Import Audio File...” from the File menu, or hold down [Ctrl]+[Shift](Win) or [Cmd]+[Option](Mac) and
         press [I].
          The “Import Audio File” function gets browser focus.
      3. Browse and select the audio file(s) you want to import.
      D   You can also import samples from the Song Samples location in the Browser.
      !   If you select REX files, these will be rendered to audio when importing. The Song Tempo and any Tempo Auto-
          mation starting at the Clip position will also be taken into account.
      4. Click “Import” to import the selected audio file(s).
          The audio file(s) will be imported as new recordings on new Comp Rows. The Comp Row(s) for the imported audio
          file(s) will be named “<filename.extension> (Imported)” where <filename.extension> is the name of the imported
          audio file with the appropriate extension.
          Depending on if you selected one or several audio files, the following will happen:
      • If you selected a single audio file, it will end up on the topmost Comp Row in the audio clip.
      • If you selected several audio files, the first selected file will end up on the topmost Comp Row.
      D   You can also drag one or several audio files from the Browser and drop it/them in the Comp Row area in the
          Comp Editor.
          The audio files will then be imported to new separate Comp Rows in the Comp Editor. The horizontal divider indi-
          cates where the new Comp Row(s) will be inserted and the vertical divider indicates where the audio will begin. If
          Snap is active in the sequencer, this will be taken into consideration:

          A + sign and a horizontal and a vertical divider indicate where in the Comp Row area the imported audio file(s) will be placed.
      q   If you like, you could now edit the Audio Clip and comp the recordings on the different Comp Rows according
          to the description in “Creating a comped audio clip”.

      Exporting audio
      You can export audio from Reason in some different ways. Besides exporting songs or parts of songs, it’s also pos-
      sible to export (bounce) audio from separate Mixer Channels, with or without the mixer settings. It’s also possible to
      export (bounce) individual Audio Clips. You can choose a variety of sample rates for the exported/bounced audio,
      and also various audio file formats and resolutions.

      Exporting Songs or parts of Songs
      There are two ways of exporting the mix of all active sequencer tracks in a song:
      • The “Export Song as Audio File...” on the File menu allows you to save the mix from the start of the song to the
        End Position Marker.
      • The “Export Loop as Audio File...” on the File menu allows you to save the mix from the Left Locator to the
        Right Locator.
      !   When you export a song or a Loop, the signals for the exported audio file are taken from Outputs 1 and 2 of the
          Hardware Interface device. Any other used outputs on the Hardware Interface will be disregarded.
      Proceed as follows to export the mix of an entire song, or a loop section of a song:
      1. Make sure the End Position Marker is placed where you want the song to end or, if you want to export a Loop,
         make sure the Left and Right Locators are placed around the Loop you want to export.
      !   Make sure you place the End Marker (when exporting a Song) or Right Locator (when exporting a Loop) so that
          any sustaining sounds are allowed to decay to silence. Otherwise, there will be an abrupt “cut” in the end of
          the exported audio file. This is probably not what you want.
      2. Select “Export Song as Audio File...” or “Export Loop as Audio File...” from the File menu.
          The “Export Song as Audio File” or “Export Loop as Audio File” dialog appears.
      3. Choose location, File Name and File Format (AIFF, WAV or MP3) for the exported audio file at the bottom of
         the dialog and click “Save”:

          Choose a file name and select file format.
      4. Select “Sample Rate”, “Bit Depth” (resolution) and “Dither” in the “Export Audio Settings” dialog and click
         “OK”:
          If you are exporting at 16-bit Bit Depth you will have the option of applying Dither. Dither means that a type of
          noise is added to the digital signal to improve low level sound quality when exporting high resolution audio at a
          lower bit depth. Reason features a new, and very sophisticated, dithering algorithm with noise shaping.
      D   Tick the “Dither” check box to improve the audio quality of exported audio at 16-bit resolution.

          Select Sample Rate, Bit Depth and Dithering of the audio to be exported.

      About Tempo data in exported audio files
      In addition to the audio data, tempo data is automatically included in the exported audio file. The tempo data contains
      information about the song Tempo and any Tempo Automation used in the song/loop. If you import such an audio file
      into another Reason song, it will automatically stretch to fit the current song tempo.
      If the section to be exported contains audio for which high-quality stretching hasn't already been done, this will be
      calculated before the actual export happens. When Reason performs high-quality stretching, the CALC indicator on
      the Transport Panel shows a progress bar:

        The CALC indicator indicates when Reason performs high-quality stretching of audio.
      • If high-quality stretching is still in progress when you export your audio file, the Export dialog will show a prog-
        ress bar as well.
        As soon as the high-quality stretching is finished, the dialog will be closed.

      Bouncing Mixer Channels
      Bouncing Mixer Channels basically means “recording” the audio outputs from Audio Track Channels and/or Mix
      Channels and then automatically creating separate audio files. The audio files can then be saved to disk or placed on
      new Audio Tracks in your song. If you choose to bounce to disk, the audio files will be automatically saved to disk as
      separate audio files. If you instead choose to bounce to new tracks, the bounced audio files will be automatically
      placed on new Audio Tracks in the sequencer.
      The “bounce to disk” option is ideal if you want to export your sequencer tracks separately for further processing in
      external applications. The “bounce to track” option is great if you, for example, have instrument tracks with lots of re-
      source consuming Insert FX etc. and therefore want to render them into audio to free up DSP resources in your song.
      You can choose to bounce the Mixer Channels, either throughout the entire song, or only between the Left and Right
      Locators. You can also choose to bounce with or without mixer settings.
      !   It’s also possible to bounce individual clips to new audio clips on new audio tracks in the sequencer. If this is
          what you want to do, please refer to the “Bounce in Place” function.
      To bounce Mixer Channels proceed as follows:
      1. Select “Bounce Mixer Channels...” from the File menu.
          The “Bounce Mixer Channels” dialog appears:

          The “Bounce Mixer Channels” dialog.

          When you open the “Bounce Mixer Channels” dialog, some channels in the Mixer Channels list might already be
          checked. This depends on what Mixer Channels (or their corresponding tracks or rack devices) were selected
          when you opened the dialog. The Master Section and FX Returns are never automatically checked when you open
          the dialog; you have to do that manually.
      2. Tick the check boxes for the Mixer Channels you want to bounce. Note that you can also bounce the Mixer
         Master Section and any FX Returns at the same time if you like.
          The Mixer Channels in the list appear in the order they are placed in the Main Mixer, i.e. not necessarily in numer-
          ical or chronological order. The color tags in the list correspond to the Channel Strip colors in the Main Mixer. The
          Master Section is always listed as “Master Section” in the list and the eight FX Returns are listed as "FX 1 Return
          (<name>)", where <name> is the FX name shown on the label in the Main Mixer. Selecting FX Returns makes it
          possible to bounce reverbs and other Send FX you might be using in your song. The FX signal is tapped after FX
          Return Level/Pan/Mute if “Apply Mixer Settings = All” (see below). Otherwise, the signals will be taken at the FX
          Return inputs.
      D   Click the “Check All” or “Uncheck All” buttons to activate or deactivate all checkboxes in one go.
      3. Select what channel settings you want to use (or not use) by clicking one of the radio buttons in the “Apply
         Mixer Settings” section.
      D   Select “All” to bounce the selected Mixer Channels with all its settings, including any Insert FX, Level and Pan.
          Since the Pan parameter is included, mono Mixer Channels will be bounced as stereo audio files.
      D   Select “All except fader section” to bounce the selected Mixer Channels with all Mixer Channel settings, in-
          cluding any Insert FX, but excluding the Level, Pan, Stereo Width and Mute parameters of the Channel Strip.
          Stereo Mixer Channels will be bounced as stereo audio files whereas mono Mixer Channels will be bounced as
          mono audio files. For the Master Section, this option means including Insert FX and the Master Compressor, but
          not the master fader.
      D   Select “None” to bounce the selected Mixer Channels before the Mixer Channel Strips, without applying any
          Mixer Channel parameters or Insert FX.
          Bounced files will be in stereo if there's any stereo material on the Audio Track (or, for a Mix Channel, if it's con-
          nected in stereo). Otherwise, the bounced audio files will be in mono.
      4. Tick the “Normalize” check box to adjust all bounced audio files so the maximum level is 0 dB.
          Normalizing is useful to get good levels when you proceed to use the bounced audio files in another application, or
          to avoid clipping.
      5. Select what range to bounce in the “Range to Bounce” section.
      D   Select “Song” to bounce the entire song (from the beginning of the song to the End Marker).
      D   Select “Loop” to bounce the section between the Left and Right Locators.
      !   Make sure you place the End Marker (when bouncing a Song) or Right Locator (when bouncing a Loop) so that
          any sustaining sounds are allowed to decay to silence. Otherwise, there will be an abrupt “cut” in the end of
          the bounced audio files.
      6. Select destination for the bounced Mixer Channel(s) in the “Bounce to:” section.

      D   Select “New Tracks in Song” to bounce the Mixer Channels to new Audio Tracks in the song.
          When “New Tracks in Song” is selected, the File Format settings in the dialog are disabled (as is the "Export
          Tempo Track (.MID)" setting). The audio will be rendered at the current song’s sample rate (i.e. what you have pre-
          viously set up in the hardware audio interface), at full 32-bit float resolution.
          Clicking OK will create a new Audio Track for each selected Mixer Channel, create an Audio Clip on each of these
          Tracks and render the Mixer Channel audio as a recording on a Comp Row in the Audio Clip.
          The new Audio Tracks will get the names and colors of their corresponding (bounced) Mixer Channels. The Audio
          Clips will get the same color but will not be labeled (named).
          The new recordings (on the Comp Rows) will get the name of their source Mixer Channels + "(Bounced)", e.g.
          "Picked Guitar (Bounced)" if the bounced Mixer Channel’s name is “Picked Guitar”.
          Selecting "Mute Original Channels" will mute all bounced Mixer Channels (those selected in the Mixer Channels
          list) after the bouncing. If there are automation lanes for their Mute buttons, their ON buttons will be turned off.
          If you selected “None” in the “Apply mixer settings” section, you will be given the option to copy the original mixer
          channel settings to the destination channels. To do this, tick the “Copy original channel settings” box.
      !   The “Mute Original Channels” setting does not affect the Master Section or the FX Returns.
      D   Select “Audio Files on Disk” to bounce the Mixer Channels to audio files on disk.
          When “Audio Files on Disk” is selected, the "Mute Original Channels" option in the dialog is automatically disabled.
          Choose File Type, Sample Rate, Bit Depth and any Dither in the “File Format” section.
          Clicking OK will bring up a Save dialog which allows you to select a folder, or create a new folder. Clicking Save
          will then create one audio file per selected Mixer Channel and place in a sub-folder named “Bounced <song
          name>”. All audio files will have the file type, sample rate and bit depth as defined in the “File Format” section.
          The audio files will get the name of the bounced Mixer Channels, plus the File Type extension. If several selected
          Mixer Channels have the same name, an incremental number (starting with "-01") will be automatically added be-
          fore the file extension.
          The Song Tempo, and any Tempo Automation, is also included in the exported audio files. This means that if you
          import the audio files into another Reason Song document, they will automatically be stretched to the Song Tempo
          of that song.
          If "Export Tempo Track (.MID)" is activated, the bounce function will also export a separate MIDI file containing the
          Song Tempo, and any Tempo Automation data. The MIDI file will have the name of the song, with the extension
          ".MID". This MIDI file can then be imported to the tempo automation lane in another Reason Song document, or to
          the tempo track in another DAW, to automatically set the song tempo and control any tempo automation in the se-
          quencer.
      !   Note that the “Export Tempo Track” option is available only if you have selected “Audio Files on Disk" in the
          “Bounce to:” section and “Song” in the “Range to Bounce:” section.

      Bouncing Audio Clips
      The “Bounce Clip to Disk” function
      The “Bounce Clip to Disk” function becomes available when a single Audio Clip is selected (in Arrange Mode or Edit
      Mode). The function allows you to bounce single Audio Clips, after the Clip Level and Fades but without the Mixer
      Channel settings, to disk for further processing in an external application, for example. Do like this to bounce an audio
      clip to disk:
      1. Select an Audio Clip and choose “Bounce Clip to Disk...” from the Edit menu or context menu.
          The “Bounce Clip As Audio File” dialog appears. It looks the same, and has the same functionality, as the “Export
          Song as Audio File” and “Export Loop as Audio File” dialogs.

      2. Choose location, File Name and File Format (AIFF or WAV) for the bounced audio clip at the bottom of the di-
         alog and click “Save”.
          (The default name in the dialog is the Clip name + extension, or (if there's no name label on the clip) the track
          name + extension.)

          Choose a file name and select file format.
      3. Select “Sample Rate”, “Bit Depth” (resolution) and “Dither” in the “Export Audio Settings” dialog and click
         “OK”:
          If you are exporting at 16-bit Bit Depth you will have the option of applying Dither. Dither means that a type of
          noise is added to the digital signal to improve low level sound quality when exporting high resolution audio at a
          lower bit depth. Reason features a new, and very sophisticated, dithering algorithm with noise shaping.
      D   Tick the “Dither” check box to improve the audio quality of exported audio at 16-bit resolution.

          Select Sample Rate, Bit Depth and Dithering of the audio clip to be bounced.
          The exported audio file will also contain tempo data as described in “About Tempo data in exported audio files”.

      About the “Bounce Clip to New Sample” function
      You can bounce an Audio Clip to a new Song Sample if you like. You could then edit the sample and load into a sam-
      pler device for playback.
      See “Bounce Clip(s) to New Sample(s)” in the “Audio Editing in the Sequencer” chapter for more details.

      About the “Bounce Clip to New Recording” function
      You can also bounce an Audio Clip to a new recording on an additional Comp Row in the Audio Clip. This is like a
      non-destructive “Flatten” operation. It will create a new recording from the clip output - ignoring Clip Level and Clip
      Fade In/Out settings. The recording will be placed on a new Comp Row at the top of the Comp Row list in the clip.
      The Audio Clip will then automatically switch to Single Mode.
      See “Bounce Clip(s) to New Recording(s)” in the “Audio Editing in the Sequencer” chapter for more details.

      About the “Bounce Clip to REX Loop” function
      A Single Take clip, which is open for inline editing, features the function “Bounce Clip to REX Loop” on the Edit and
      context menu. This allows you to generate a REX loop out of the Single Take audio clip. The REX loop can then be
      used in a Dr Octo Rex device in Reason and/or be exported to disk.
      See “Bounce Clip to REX Loop” in the “Audio Editing in the Sequencer” chapter for more details.

540   IMPORTING AND EXPORTING AUDIO


---

<a id="sampling-21"></a>

=== END OF PART ===
