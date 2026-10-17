# Chapter 09: Reason 12 manual digest and studio workflow
## Part 22 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 13 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 23 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 13 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

                                                                                 Audio clip with stereo
                                                                                 audio events
          An audio clip with a stereo audio recording.

      Recording using the Clip Safe function in Propellerhead Balance
      If you are recording using the (discontinued) Propellerhead Balance audio interface, you can utilize the Clip Safe
      function to protect your recordings from any accidental input signal clipping. The program can then take care of and
      heal any input signals that accidentally exceed 0dB.
      See “Using the Clip Safe function with Propellerhead Balance” for more details.
      !   Note that the Clip Safe function can only be used when recording in mono (single audio input) and only on one
          record enabled Audio Track at a time.
      Proceed as follows to set up and activate the Clip Safe function:
      1. Select the desired Audio Track for recording.
      2. Select audio input in the drop-down list.
      !   Note that you can only select the Balance In L or R (Mono Input) for the Clip Safe function to be available.
      3. Press the Clip Safe button on the Balance front panel.
          The Clip Safe LED on the Propellerhead Balance audio interface turns green. The CS indicator to the right of the
          input level meter on the Audio track is lit:

                                                   Clip Safe LED on
                                                                     CS indicator on

          The Clip Safe LED on the Propellerhead Balance interface and the CS indicator on the Audio Track.
      4. Record the track according to the descriptions in “General recording procedure”.

      !   We recommend that you aim at -12dB maximum recording level, even if you are using the Clip Safe function.
          Recording high input levels will result in very loud audio on the track, which could be problematic to mix with
          the rest of the instrument tracks in your song.
          When the Clip Safe function is active, the Input Meter on the Audio Track, as well as the level meter in the Record-
          ing Meter window get their red LEDs replaced by yellow ones. The Recording Window also gets a Clip Safe sym-
          bol to the upper right:

          The Input Meter on the Audio track and the Recording Meter gets yellow LEDs instead of red ones.
      5. When the recording is finished, the audio clip on the track shows the recorded audio as a continuous wave in-
         side the clip.
          The red vertical line(s) at the top of the audio clip indicate that Clip Safe was activated since the input level ex-
          ceeded 0dB. The selected audio clip also gets an additional Heal (CS) button on its upper right hand side:

                        Clip Safe applied when input signal exceeds -0dB

                                                                                                               Heal button

          Audio recorded with the Clip Safe function active.
      6. Play back the track and hear where the signal clips.
          You should hear this when the playhead passes over the red vertical line(s) in the audio clip. Sometimes, though,
          if the clipping is moderate it might not be audible.
      7. To permanently heal the audio clip and use the Clip Safe audio, click the Heal (CS) button to the upper right-
         hand side of the audio clip. Alternatively, select “Heal Clip Safe Clips” from the Edit menu or audio clip context
         menu.
          Now, the clipped/distorted audio has been replaced by the “padded” Clip Safe audio and the recording should not
          clip or distort anymore. The area above the audio clip disappears, as does the Heal (CS) button.
      q   If you like, you can zoom out using the Waveform Zoom Level buttons to view the resulting waveform in its en-
          tirety in the Audio Clip (see “Waveform Zoom Mode”).
      D   The healing operation can also be performed on several selected audio clips in one go. Just select the desired
          clips and click a Heal (CS) button on one of the clips.
      D   If you want to remove the Clip Safe parts and keep the clipped/distorted parts, just undo the healing operation
          using the standard [Cmd](Mac)/[Ctrl](Win)+[Z] command.
      D   If you want to permanently delete the Clip Safe audio and keep the clipped/distorted audio, select “Delete Clip
          Safe Audio” from the Edit menu or audio clip context menu.
      • In Edit Mode, the audio clip will have the same graphical appearance (the clipped/distorted parts indicated by
        red vertical lines, plus the Heal (CS) button to the right in the Clip Overview).

      Recording audio in Loop mode
      Recording audio in Loop mode is very useful if you want to record alternative takes of the same part of the song. For
      example, let’s say you want to sing a couple of takes of the chorus part of your song to later create the perfect chorus
      by selecting the best parts of the different takes.
      !   To minimize the song saving time, we strongly recommend saving the song before recording many or large au-
          dio recordings.
      Proceed as follows to record audio in Loop mode:
      1. Set up the audio track according to the descriptions in “Setting up the audio track”.
      2. Set the Left and Right Locators to span the chorus part of your song.
      3. Enable the Loop function by pressing [L] or by clicking the Loop On/Off button on the Transport Panel:

          Loop mode activated on the Transport Panel.
      4. Click the L button on the Transport Panel to move the Song Position Pointer (play head) to the Left Locator.

      5. Record the track according to the descriptions in “General recording procedure”.
      6. Start singing to record audio on the track.
          When the Song Position Pointer has reached the Right Locator, the recording starts over from the Left locator
          again and you can now record a second take. The audio recorded in the previous take won’t be heard but is saved
          in the “background” on a Comp Row.
          Continue recording for as many loop cycles as you like.
      7. When the recording is finished, the audio clip on the track shows the last recorded audio take as one or two
         continuous waves inside the clip (depending on whether the input was in mono or stereo).
      !   If you recorded the last loop cycle throughout the entire clip length, the audio clip will be a Single Take clip. If
          you stopped recording the last loop cycle somewhere in the middle of the clip, the clip will be a Comp Clip.
      8. Double-click the clip to open it for editing.

      • If the last loop cycle was recorded throughout the entire clip length, the clip opens in Slice Edit mode.
          If so, open the clip in the Comp Editor by clicking the “Comp Edit” button in the Toolbar.
          Otherwise, it opens in the Comp Editor right away. In the Comp Editor, you can see that there is one Comp Row for
          each of the recorded loop cycles (Takes):

                                                                                                 Audio clip (latest take)
                                                                                                 with stereo recording

                                                                                                Audio Comp Rows with
                                                                                                stereo recordings

          Audio recorded in Loop mode with 5 loop cycles (Takes) recorded.
          From here, it’s easy to assign the best parts from the different takes and comp them into a final clip. See “Creating
          a comped audio clip” for details.
      !   If you have recorded using the Clip Safe function with the Propellerhead Balance audio interface, any clipped
          parts are displayed with vertical red lines above each Comp Row. If you decide to heal the audio clip using the
          Heal (CS) button or “Heal Clip Safe Clips” from the Edit menu or context menu of the selected audio clip, the
          recordings on all Comp Rows are healed in one go.

      Overdubbing audio using the “Dub” function
      Back in the tape recorder days, overdubbing was used to record additional takes on additional tracks on the same
      section of the tape, to create a complete arrangement. For example, recording a vocal chorus part could be done by
      overdubbing the singer three or four times on additional tracks. Overdubbing in Reason works in a similar way, but
      with much better control, and much better editing possibilities afterwards.
      D   After you have recorded the first take on an audio track, click the “Dub” button on the Transport Panel.
          This will create a new audio track with a duplicate of the original audio track settings, including the channel strip
          settings (with insert effects etc.). Now, you can continue recording on the new audio track as described in “Re-
          cording audio” and “Recording audio in Loop mode”. Afterwards, you can edit the new track completely inde-
          pendently of the original track.
      q   The “Dub” function can also be used on-the-fly while recording.

      Duplicating audio tracks using the “Alt” function
      Closely related to the “Dub” function, described in “Overdubbing audio using the “Dub” function”, is the “Alt” function.
      This function can be used to create a new audio track with an identical copy of the selected audio track’s settings.
      The only difference between the “Alt” and “Dub” functions is that the Alt function will automatically mute the original
      audio track.

      D   Select the audio track you want to duplicate and then click the “New Alt” button on the Transport Panel.
          This will create a new audio track with a duplicate of the original audio track settings, including the channel strip
          settings (with insert etc.). Now, you can continue recording on the new audio track as described in “Recording au-
          dio” and “Recording audio in Loop mode”. Afterwards, you can edit the new track completely independently of the
          original track.
      q   The “Alt” function can also be used on-the-fly while recording.

      Recording over or into an existing audio clip
      If you start recording over an existing clip on an audio track, the new recording will incorporate (replace, but not
      erase) the previous recording in the clip. When you open the audio clip in the Comp Editor afterwards, there will be
      one Comp Row for each of the takes, the same result as when recording audio in Loop mode (see “Recording audio
      in Loop mode”).
      Let’s have a look at the following example:
      In the picture below, we have the original audio clip spanning bars 1-8 on the track:

      An audio track with an existing clip.
      Now, we want to redo (re-record) the part that spans bars 5-6. We place the Song Position Pointer at bar 5 and re-
      cord 2 bars:

                                         New recording
      A new recording made on bars 5-6 on the audio track.
      The new recording is made over the original clip. The recording in the original clip has therefore been incorporated
      into the start of bar 5 to the end of bar 6.
      You can also see that the clip has become a Comp Clip, as indicated by the symbol (gray dots) at the lower right cor-
      ner of the clip.

      Now, let’s double-click the clip to open it in the Comp Editor:

                                                              New recording

                                                    Incorporated part of the original recording
      The new and original recordings (takes) in Edit Mode.
      The new recording has incorporated bars 5-6 of the original recording. However, the original recording in bars 5-6
      has been left totally unaffected. The entire original audio recording now resides on the “Take 1” Comp Row and the
      latest recording resides on the “Take 2” Comp Row. The resulting clip will now play back the “Take 1” recording in
      bars 1-4 and 7-8. Bars 5-6 will play back the “Take 2” recording.
      See “Creating a comped audio clip” for details on how to extract parts from individual takes and comp into a final clip.

      Recording audio from Mix Channel outputs
      Besides recording external audio from the inputs of your audio interface, it’s also possible to record audio internally
      from the outputs of Mix Channel or Audio Track devices. Typical applications for this could be:
      • Recording the audio from an Output Bus (sub mixer) Mix Channel.
          You might have the individual drums of your drum kit on separate tracks and these tracks are routed to a Mix
          Channel which is set to work as an Output Bus (see “Output Busses”). You then want to record the audio from
          the Output Bus onto a new Audio Track.
          In this situation, all you need to do is create a new Audio Track, activate the Rec Source button on the Output Bus
          Mix Channel device, and then select the Output Bus in the Select Audio Input drop-down list on the Audio Track
          in the Track List. Then, record the audio from the Output Bus as described in “Recording audio”.
      • Re-recording of an audio track with effects applied.
      • Recording when playing back an instrument or audio track while making live manipulations of effects or pa-
        rameters.
      q   If you want to record the audio from an Instrument track onto an audio track, without making any live manipu-
          lations, you can also use the “Bounce Mixer Channels” function - see “Bouncing Mixer Channels”.
      The example below describes how to capture and record the audio from an ID8 device, but the general method can
      be used for other recording scenarios as well:
      1. Create an instrument track for the instrument device you want to record according to the descriptions in “Cre-
         ating an instrument track”.
          You won’t actually be recording on the instrument track in this situation. However, you will need the instrument
          track to be able to play the instrument device from your connected master keyboard.
      2. Create an audio track according to the description in “Creating an audio track”.

      3. In the rack, locate the Mix Channel device connected to the ID8 instrument device and click its “Rec Source”
         button.
          The “Rec Source” button on Mix Channel devices is used for real-time audio recording of devices connected to the
          Mix Channel device.
          The “Rec Source” button on Audio Track devices are used for real-time re-recording of audio tracks.

          Enabling the Rec Source button on the Mix Channel device in the rack.
      4. Locate the audio track and select “Stereo Input” and “ID8 1” as input source in the “Select Audio Input” drop-
         down list.
          All Mix Channel and Audio Track devices that have their “Rec Source” button enabled will appear in the list. In this
          example, we only have the Rec Source button active on the “ID8 1” Mix Channel.

          “Stereo Input” and “ID8 1” selected in the “Select Audio Input” drop-down list.
      5. Select the instrument track, in this example the ID8 1, so that it has Master Keyboard Input (red frame around
         the device icon) and disable the “Record Enable” button.

          Select the ID8 1 track and disable the Record Enable button.
      6. Locate the audio track and record enable it by clicking the Record Enable button.

          Engage Record Enable on the Disk Channel track.
      !   Don’t set Master Keyboard Input to the audio track - only click the “Record Enable” button on the audio track!
          This way, the ID8 1 instrument track will still have Master Keyboard Input.

      7. Play the master keyboard and set the input level to the audio track by adjusting the Level Fader on the ID8 1
         Mix Channel strip in the mixer.

          Adjusting the instrument’s level to the audio track.
      !   A Volume setting of -0.0 dB on the instrument device and a Level Fader setting of -0.0 dB on its corresponding
          Mix Channel strip in the mixer is often the optimal setting to avoid audio signal clipping. As when recording ex-
          ternal audio, it’s the track’s Input Meter that should be observed for any clipping.
      8. Start recording audio on the audio track according to the description in “Recording audio”.
      q   By using the recording method described above, it’s also possible to record the audio from previously re-
          corded note clips on instrument tracks.

      Recording a mixdown of several audio tracks
      Another useful feature is to record a real-time mixdown of several previously recorded audio tracks onto a new, ad-
      ditional audio track. This is sometimes also referred to as recording stems or sub-mixes. Let’s say we have four back-
      ing vocal tracks that we want to mix down and record on a new audio track. We can do this as follows:
      1. Create a new audio track according to the description in “Creating an audio track”.
          This is the track we’re going to use for recording the mixdown. We name the track “Mixdown” to make it easier to
          distinguish.
      2. Locate the Master Section device in the rack and click its “Rec Source” button.

          The “Rec Source” button on the Master Section device.
          This will allow you to record the output from the Master Section onto the new audio track.

      3. Locate the four backing vocal Audio Track devices in the rack, or their corresponding channel strips in the
         mixer, and click their “Solo” buttons.

          The four backing vocal Audio Track devices soloed.
          Since we’re going to record the four backing vocal tracks through the outputs of the Master Section, we only want
          the backing vocal tracks to sound. All other tracks in the song should therefore be muted.
      4. Select the “Mixdown” track in the sequencer and select “Stereo” and “Master Section” from the “Select Audio
         Input” drop-down list.

          “Stereo” and “Master Section” selected as Audio Input source.
          Selecting “Stereo” makes it possible to pan the backing vocal tracks in stereo before recording on the mixdown
          audio track.
      5. Adjust the parameters of each of the backing vocal track channel strips as desired.
      q   Don’t forget to set the panning of each of the tracks to spread them in the stereo panorama.

      6. Select the “Mixdown” track in the sequencer and click the “Rec” button on the Transport Panel to start record-
         ing the mixdown.

          Recording the mixdown of the four backing vocal tracks to the “Mixdown” track.
      q   During recording, you might want to perform real-time adjustments of the backing vocal tracks’ channel strip
          parameters to create a “live” mix.
      7. When you have recorded the mixdown, click “Stop” on the Transport Panel.

      8. Before you play back the song with the mixdown track, remember to un-solo the four backing vocal Audio
         Track devices/channel strips. Also, mute the four original backing vocal tracks in the sequencer to avoid “dou-
         ble” sounds.

          Playing back the Mixdown track with the original backing vocal tracks muted in the sequencer.
      q   Another alternative, if you want to record several Audio Tracks or Mix Channels onto a single audio track, is to
          create a sub-mixer setup - see “Output Busses”.

      Note recording details
      Note events can be recorded for instrument devices and are contained in note clips. Performance controller events,
      such as Mod Wheel, Pitch Bend and Aftertouch events, can also be recorded for instrument devices, and be con-
      tained in note clips, but they are described separately in “Parameter automation recording details”.

      Setting up the instrument track
      To record notes for an instrument device - or for an external MIDI instrument - on a track in the sequencer, you need
      only create an instrument track as described in “Creating an instrument track”. The instrument track will automatically
      have Master Keyboard Input and the note lane will automatically be record enabled. Since you will only be recording
      MIDI events on the instrument track - and no audio - there is no need to adjust audio levels etc. These can always be
      adjusted afterwards.
      If you want to control an external MIDI instrument, simply create a MIDI Out Device and select the appropriate MIDI
      port and channel on the device panel. See “MIDI Out Device” for more details.

      About “Quantize During Recording”

      The Q Record (Quantize During Recording) button on the Transport Panel.
      It’s possible to quantize MIDI notes as they are being recorded. This will automatically align the start positions of the
      recorded notes to a pre-defined grid. Refer to “Quantize” for more details.

      Recording notes
      1. Set up the instrument track according to the description in “Setting up the instrument track”.
      2. Record the track according to the description in “General recording procedure”.
      3. When the recording is finished, the note clip on the lane shows the recorded note events in a piano-roll fashion
         inside the clip:

                                                                            Note clip with note events

          A note clip with note events.
          The note clip’s start and end boundaries will automatically snap to the closest bar to make it easier to arrange
          (move etc.) later on.
      !   If no MIDI events (notes and/or performance controllers) were recorded, the empty note clip will be automati-
          cally removed from the lane after you have clicked Stop.
      q   It’s also possible to manually insert notes by drawing them with the Pencil tool. Refer to “Drawing notes”.
      q   You can also use Player devices to automatically generate various types of MIDI Note sequences, patterns and
          chords when you record your instrument, see “Working with Players”.

      Recording notes in Loop mode
      Recording on a note lane in Loop mode allows you to continuously add new notes in a defined section of your song:
      1. Set up the instrument track according to the description in “Setting up the instrument track”.
      2. Set the Left and Right Locators to span the desired part of your song.

      3. Enable the Loop function by pressing [L] or by clicking the Loop On/Off button on the Transport Panel:

          Loop mode activated on the Transport Panel.
      4. Click the L button on the Transport Panel to move the Song Position Pointer (play head) to the Left Locator.

      5. Record the track according to the description in “General recording procedure”.
          When the Song Position Pointer has reached the Right Locator, the recording starts over from the Left Locator
          again and you can record additional notes. Any new recorded notes will be added to the previously recorded ones
          and all notes will be heard during the recording.
          Continue recording for as many loop cycles you like.

      Recording over or into an existing note clip
      Recording over or into an existing note clip will simply add new note events to the previously recorded events in the
      note clip as described in “Recording notes in Loop mode”. However, If the new recording should start before the orig-
      inal clip, and expand into the original clip, a new clip will be created and will engulf the original clip. Let’s have a look
      at the following example:
      In the picture below, we have the original note clip spanning bars 4-13 on the track:

      A note lane with an existing clip.
      Now, we’re going to record an intro which is going to span the first four bars:

      A new note clip recorded on bars 1-4 on the same note lane.
      The new clip is partly recorded over the original clip. The part of the original clip that has been recorded over is incor-
      porated in the new clip; the events from the original clip are now contained in the new clip, and the start of the original
      clip has been moved to bar 5, where the new clip ends.
      !   If you’re recording over or into a masked clip and the new clip engulfs masked events, the masked events will
          be permanently deleted! See more about masked events in “About masked recordings and events”.
      q   Another, perhaps more convenient, way of overdubbing on an instrument track is to create additional note
          lanes and record new clips on these using the New Dub or New Alt functions described in “Recording notes us-
          ing the “Dub” and “Alt” functions”. This way, you will get a better overview of exactly what you added in each
          of your recordings.

      Recording notes using the “Dub” and “Alt” functions
      A practical way of recording additional MIDI events on an instrument track is to use the “Dub” and “Alt” functions.

      The “Dub” function
      The “Dub” function creates additional record enabled note lanes on which you can record “overdubs”. This is the func-
      tion to use when you want to add new notes in the same section of the instrument track but want the notes to end
      up in new clips on additional note lanes instead of in the original clip. All note lanes will play back together.

      The “Dub” function used for creating two additional lanes for overdub purposes. Loop mode is Off.

      The “Dub” function used for creating two additional lanes for overdub purposes in Loop mode.
      q   Creating a new note lane using the “Dub” button can also be done on-the-fly while recording.

      The “New Alt” function
      The “Alt” function creates additional record enabled note lanes on which you can record alternative takes. At the
      same time, the previous note lane will be muted. Only the most recently added note lane will play back.
      !   Note that if Loop is activated and the Song Position Pointer is between the Locators, the clips between the Lo-
          cators will be muted (instead of the lanes).
      Here are two examples where the “Alt” function has been used:

                                                                                Muted note lanes

      The “Alt” function used for creating two additional lanes for alternative takes. Loop mode is Off.
      When using the “Alt” function with Loop mode off, the previous note lane will be automatically muted.

                                                                             Muted note clip
                                                                             Split and muted note clip

      The “Alt” function used for creating two additional lanes for alternative takes in Loop mode.
      When using the “Alt” function in Loop mode, the clips between the locators will be muted - not the entire note lane. If
      the locators are placed over an existing clip, as in the example above, clicking the “Alt” button in Loop mode will split
      the clip and mute the clip between the locators.
      q   Creating a new note lane using the “Alt” button can also be done on-the-fly while recording.

      Parameter automation recording details
      In Reason, you can automate virtually any device and channel strip parameters and create completely automated
      mixes if you like. This is done by recording parameter events in the sequencer. It’s also possible to record sequencer
      Tempo automation (see “Tempo automation recording”).


=== END OF PART ===
