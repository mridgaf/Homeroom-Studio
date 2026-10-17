# Chapter 09: Reason 12 manual digest and studio workflow
## Part 21 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 12 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 22 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 12 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 6: Recording in the Sequencer

Recording in
the Sequencer

      About this chapter
      This chapter describes the different recording techniques that you can use in Reason. The chapter covers both audio,
      notes and parameter automation recording. Before you read this chapter, it’s recommended that you are familiar with
      the basic sequencer functions and definitions described in the “Sequencer Functions” chapter. A lot of functions are
      common for all types of recording methods. These will be described first in this chapter. Later in the chapter we will
      go into functions specific to audio, notes and parameter automation recording.

      General recording functions
      Record enabling
      Before you can start recording on a track in the sequencer, the track needs to be record enabled. There are two types
      of buttons for record enabling: the Record Enable button, which is used when recording audio clips and note clips,
      and the Record Enable Parameter Automation button, which is used when recording device/channel strip parameter
      automation and tempo automation:

                                                                     Record Enable buttons

                                                                     Record Enable Parameter
                                                                     Automation buttons
      Five tracks with their Record Enable and Record Enable Parameter Automation buttons.
      Activated Enable Record and Enable Record Parameter Automation buttons are indicated with a red color. Recording
      can be simultaneously enabled on an unlimited number of audio tracks (limited only by the computer’s processing
      and hard disk performance) - plus one note lane on an instrument track. However, if you have locked several MIDI
      keyboard controllers to specific instrument devices in the rack - using Remote (see “Locking a surface”) - you can re-
      cord MIDI on these instrument tracks simultaneously. Recording of parameter automation can be simultaneously en-
      abled on as many tracks as you like.

      Record enabling an audio track

                                                                          Record Enable button (On)

      D   To record enable an audio track, click on the Record Enable button on the audio track.
          The Record Enable button goes red.
          Selecting an audio track will automatically record enable the track if you have selected “Standard” mode in the
          “Master Keyboard Input” section on the “MIDI” page in the Preferences dialog (see “The Master Keyboard Input
          setting”) - and if the Manual Rec button in the Track List is Off, see “About the Manual Rec function”.
          Also, depending on the setting in the “Monitoring” section on the “Audio” page in Preferences, monitoring of the in-
          put signal to the audio track may, or may not, be automatically activated - see “Monitoring”.

      Record enabling multiple audio tracks
      D   If you want to record audio from separate audio inputs on several tracks at once, click the Record Enable but-
          tons on all desired audio tracks in the Track List.
          Each record enabled audio track will automatically unfold to show the Tuner button, the Select Audio Input drop-
          down list and the Input Meter. When recording audio on several tracks simultaneously, it doesn’t matter which au-
          dio track has Master Keyboard Input.

                                                                             Record Enable buttons (On)

          Multiple audio tracks record enabled, for recording audio on several tracks at once.

      Record enabling an instrument track
                                                                Record Enable Parameter
                                                                Automation button

                                                               Record Enable buttons

      D   To record enable an instrument track, click on the Record Enable button on a note lane on the instrument
          track.
          The Record Enable button lights up red and the track has Master Keyboard Input.
          If you have selected “Standard” mode in the “Master Keyboard Input” section on the “MIDI” page in the Prefer-
          ences dialog (see “The Master Keyboard Input setting”), selecting an instrument track will automatically set Master
          Keyboard Input to that track - if the Manual Rec button in the Track List is Off, see “About the Manual Rec func-
          tion”. An instrument track that has Master Keyboard Input will automatically be record enabled, and will also be en-
          abled for parameter automation recording, indicated by the red Record Enable Parameter Automation button.
      D   If you want to record on another note lane on the instrument track, just click the corresponding Record Enable
          button on the note lane.
      !   Only one note lane on one instrument track can have Record Enable active at a time, unless you have locked
          additional MIDI keyboard controllers to specific instrument devices in the rack (see “Locking a surface” in the
          Remote chapter). If you only have one MIDI keyboard controller (assigned as Master Keyboard), you can only
          record notes on one note lane at a time (see “Setting Master Keyboard Input”).

      Record enabling several instrument tracks
      If you have locked additional MIDI keyboard controllers to specific instrument devices in the rack (see “Locking a sur-
      face” in the Remote chapter), the corresponding tracks for all these locked devices are automatically record enabled
      - if the Manual Rec button in the Track List is Off, see “About the Manual Rec function”. These additional record en-
      abled tracks are all displayed with the gray “Master Keyboard Input” symbol to the left of the device icon in the track
      list, and their Record Enable buttons are also automatically switched on. The track with “normal” Master Keyboard In-
      put is also indicated with the gray Master Keyboard Input symbol to the left of its device icon.

                                                                   Record Enable buttons (On)

      The “Combinator 3” track with Master Keyboard Input and the “Combinator 1” and “Combinator 2” tracks controlled from additional
      MIDI keyboards locked to the corresponding devices in the rack.
      D   To manually enable/disable any additional record enabled instrument tracks that are locked to specific MIDI
          keyboard controllers, click the Record Enable buttons on a note lane on any of these tracks.

      About the Manual Rec function

                                                                     The Manual Rec button

      The Manual Rec button in the Track List.
      The Manual Rec function in the Track List can be used if you don’t want automatic record enabling of a selected
      track. For example, when you are finished recording your audio tracks and want to proceed with recording channel
      strip parameter automation, you probably don’t want the audio tracks to be record enabled for audio.
      D   Click the manual Rec button to disable automatic record enabling of selected tracks.

                                                                    The selected track is not automatically
                                                                    record enabled anymore

          The Manual Rec function activated.
          If you change your mind and want to record audio on an audio track, you have to manually record enable it by click-
          ing its Record Enable button as described in “Record enabling an audio track”. Alternatively, switch off the Manual
          Rec button to enable the automatic record enabling again.
      !   The Manual Rec function affects both audio tracks and instrument tracks.

      Record enabling parameter automation
      Parameter automation can be recorded on all track types, on one track at a time or on multiple tracks simultaneously.
                                                                 Record Enable Parameter
                                                                 Automation button

      D   Click on the Record Enable Parameter Automation button(s) on the desired track(s) in the Track List to enable
          parameter automation recording.
          All tracks enabled for parameter automation recording will be indicated by red Record Enable Parameter Automa-
          tion buttons.
      D   Setting Master Keyboard Input to a track will automatically enable parameter automation recording, as indi-
          cated by the red Record Enable Parameter Automation button.

      Record enabling pattern automation
      Pattern automation can be recorded on tracks associated with pattern based devices such as the Redrum Drum
      Module, Dr. Octo Rex Loop Player or Matrix Analog Pattern Sequencer. Enabling pattern automation works in the
      same way as enabling regular parameter automation (see “Record enabling parameter automation”).
      !   Note that enabling the Record Enable Parameter button on a track featuring a pattern based device will also
          allow automation recording of other device parameters besides the Bank and Pattern select buttons. Any ad-
          ditional device parameters will be recorded on separate parameter automation lanes just like with non-pattern
          devices.

      Click and Pre-count
      During recording and playback it’s possible to have a metronome-style click sound to indicate the tempo of the song.
      In recording mode it’s also possible to have the metronome click sound appear a selectable number of bars before
      the start of the actual recording, a so called pre-count. Activation of click and pre-count are managed on the Trans-
      port Panel:

      The Click and Pre-count controls on the Transport Panel.

      Click
      D   Click the Click button to get an audible metronome click as the sequencer plays. Alternatively, press [C].
          The click will sound on every beat, with the first beat in every bar accented (higher pitched).

      Pre-count
      D   Click the Pre button to get a pre-count (count-in) click sound before the recording starts. Alternatively, press
          [Ctrl](Win)/[Cmd](Mac)+[P]
          Pre-count will only be present before you record - not when you start regular playback.
      !   Note that Pre-count does not have any effect if you are using Ableton Link for synchronization, see “Synchro-
          nization using Ableton Link”.

      D   Select the number of pre-count bars by choosing “Number of Precount Bars” in the Options menu.
          You can choose between 1 to 4 bars.

          Selecting number of pre-count bars.
      q   Feel free to experiment with different pre-count settings. For up-tempo (faster) songs it’s generally more con-
          venient to have a little longer pre-count (3 or 4 bars) whereas for slower songs it’s often sufficient with 1-2
          bars.

      Click Level

      Click Level slider.
      D   Adjust the audio level of the metronome click (and pre-count click) with the slider.
      !   Note that since the click sound is also routed via the selected audio card/interface on your computer - but not
          through the Reason mixer, the click sound will be summed to the rest of the sounds playing in your song. A
          high Click Level setting could therefore cause the Audio Output Meter on the Transport Panel, and the “Big
          Meter” in the Reason Hardware Interface, to indicate clipping. If this should occur, either lower the Click Level
          or deactivate Click to determine if it’s the click sound or the recorded sounds that cause clipping.

      Loop mode
      In loop mode, the song is automatically looped between the Left and Right Loop Locators on the Edit/Arrangement
      Pane during playback and/or recording:

      Loop mode activated by clicking the Loop button on the Transport Panel.
      The behavior when recording in loop mode differs depending on what you’re recording - audio, MIDI or parameter au-
      tomation. Refer to “Recording audio in Loop mode”, “Recording notes in Loop mode” and “Recording parameter au-
      tomation in Loop mode”.

      General recording procedure
      The following description applies to all types of recording: audio, MIDI and parameter automation. For specific details
      of audio, MIDI and parameter automation recording, refer to “Recording audio”, “Recording notes”, “Recording perfor-
      mance controller automation” and “Recording parameter automation”.
      1. If desired, select Click and/or Pre-count according to the descriptions in “Click and Pre-count”.
      2. Move the Song Position Pointer to the position in the Ruler where you want to start your recording (see “Ruler
         details”).
      3. Click the Record button on the Transport Panel. Alternatively, press [*] on the numeric keypad, or hold down
         [Ctrl](Win) or [Cmd](Mac) and press [Return].
          The Record button turns red. If Pre-count is enabled, wait for the set number of pre-count bars before starting to
          record audio, MIDI or parameter automation. During pre-count, nothing will be recorded.

          During pre-count, only the Record button is active (red) and nothing will be recorded.
      4. Start recording on the track.
          As the recording begins, the Play button on the Transport Panel goes dark while the Record button remains red.

          During recording, both the Play and Record buttons are active and any input data will be recorded.
          If the lane is currently empty, a new clip is automatically created on the record enabled lane on the track. As the re-
          cording progresses, the clip expands following the Song Position Pointer. The clips are shaded in red during re-
          cording according to the picture below:

                                                                                              A note clip being recorded

                                                                                              An audio clip being recorded

      5. When you’re done recording, click the Stop button on the Transport Panel. Alternatively, press [Spacebar], [0]
         on the numeric keypad, or hold down [Shift] and press [Return].
          The Record and Play buttons turn gray, the Song Position Pointer stops and the red shading of the clip(s) disap-
          pears. The clip(s) show the recorded events as different types of graphical objects, depending on clip type.
      !   If nothing was recorded in a note clip, clicking Stop will automatically remove the empty note clip.

      Undoing a recording
      D   If you’re not satisfied with the finished recording, you can select “Undo Record Track” from the Edit menu or
          select the clip on the Edit/Arrangement Pane and press [Delete] or [Backspace].
          This will delete the clip and its contents.

      Undoing while recording a note clip
      D   If you’re not satisfied with your ongoing recording of a note clip, press [Delete] or [Backspace].
          This will delete the current note clip and all its contents and at the same time create a new clip starting at the cur-
          rent song position. The sequencer will continue recording during the entire process.
      !   Note that this only works when recording note clips.

      Recording tips
      Lowering the Tempo during recording
      If you are going to record complex/difficult takes, a good suggestion is to lower the song tempo during recording and
      then speed up the song to normal tempo again during playback. For audio tracks, Reason features very sophisticated
      functions for audio stretching. Audio stretch enables you to alter the song tempo up or down without changing the
      pitch of the recorded audio. See “About tempo changes and tempo automation of audio tracks” for more details.
      When recording MIDI, just lower the tempo when recording the difficult parts and speed up to normal tempo during
      playback.

      Audio recording details
      Setting up the audio track
      Selecting audio input(s) and defining mono or stereo
      D   Select audio input(s) for the track from the Audio Input drop-down list.

          Selecting audio inputs for the Audio Track.
          At the top of the drop-down list you can select whether you want to use mono or stereo inputs. Depending on your
          selection, the LED meter switches to a stereo or mono display. Further down in the drop-down list you can select
          the audio interface input(s) you want to use for the track.
      • If you are using the Propellerhead Balance audio interface, selecting any of its input channels in the drop-
        down list will automatically switch on the corresponding Ready LEDs on the Balance front panel. Also, if you
        have selected “Mono Input” in the Audio Input drop-down list, the Audio Track will show a CS (Clip Safe) sym-
        bol to the right of the LED meter.

      Setting input level(s)
      Before you start recording audio on the track it’s very important to set correct input level(s). The input signal should
      be loud enough to minimize noise and provide high quality, but not so loud that it causes clipping and distortion.
      If you’re using a 24-bit audio interface (recommended), aim at having the level of the input signal around -12dB on
      the track Input Meter according to the picture below. For 16-bit audio interfaces you may want to raise the level an-
      other couple of dB’s.
                                                                                 “Safe” input level ~ -12dB
                                                                                 (first yellow LEDs lit)

      q   To get a better view of the input levels, use the separate Recording Meter Window, see “The Recording Meter
          Window”.
      !   If you are using the Propellerhead Balance audio interface you can use the special Clip Safe function to protect
          your recordings from accidental audio input clipping, see “Recording using the Clip Safe function in Propeller-
          head Balance”.
      !   Always adjust the input level at the source (e.g. the preamp connected to, or built-in to the audio interface).
      !   If the input signal level should exceed 0dB (red clipping LEDs to the right) on the track Input Meter at any time
          during recording, there could be audible distortion in the recording:

                                                                                 Audio clipping LED = distortion
                                                                                 (Clipping LED lit)

      If the input level should clip, at any time, the red clipping LED(s) in the Input Meter will be constantly lit until you click
      on the Input Meter. This is to notify that there is, or has been, too loud an input signal present on the track.
      !   The input level cannot be adjusted using the Channel strip controls in the Main Mixer. The Channel strip con-
          trols are used only for adjusting the level and characteristics of the monitored signal and/or the playback sig-
          nal of an existing recording on the track.

      Using the Clip Safe function with Propellerhead Balance
      !   Note that the Clip Safe function only works together with the Propellerhead Balance audio interface.
      If you use the Propellerhead Balance audio interface together with Reason, you will have access to the Clip Safe
      function. The Clip Safe function lets you record a mono signal with an additional “invisible” headroom. This is done by
      using both AD converters in Propellerhead Balance for the same mono signal, with the second AD converter dedi-
      cated to the additional headroom.
      When recording with the Clip Safe function, Reason records the mono signal in parallel using both AD converters.
      The original AD converter records the signal at normal level and the second AD converter records the same signal
      “padded” at a lower level.
      In practice this means that if the input signal should exceed the normal 0dB clipping level during recording, the pro-
      gram will allow you to use the “padded” signal from the second AD converter and replace the clipped/distorted audio.
      The padded signal will be amplified in Reason so that its level accurately reflects the original recording level. In other
      words, the resulting signal will be just as loud as the original signal - but without any clipping or distortion.

      Proceed as follows to activate the Clip Safe function:
      1. Select “Mono Input” in the Audio Input drop-down list on the Audio Track and then select either “Balance 1/L”
         or “Balance 2/R”.

          The CS (Clip Safe) symbol appears to the right of the level meter on the Audio Track.
      2. Press the Clip Safe button on the Propellerhead Balance front panel.

          The Clip Safe button on the Propellerhead Balance audio interface.
          A Clip Safe request signal is sent from the Balance interface to Reason. Depending on what audio inputs are se-
          lected on the record enabled Audio Track(s), the following happens:
      • If the Balance 1/L or 2/R input is selected as audio input (Mono) on one single record enabled Audio Track, the
        Clip Safe LED on the Balance interface turns green and the CS symbol on the Audio Track is lit.
          When the Clip Safe LED on the Propellerhead Balance audio interface is green, the Clip Safe function is enabled.
          If the 1/L input is selected as audio input (Mono), the Right channel on the Balance interface is used for the ad-
          ditional headroom, and vice versa.
      • If the Balance 1/L and 2/R inputs are selected as Stereo Input, the Clip Safe function is disabled and the Clip
        Safe LED on the Balance interface turns red. The CS symbol on the Audio Track also disappears.
          The Clip Safe function requires both inputs to be available. Also, if the Balance 1/L (mono) and 2/R (mono) inputs
          are selected as audio inputs on other record enabled Audio Tracks, the Clip Safe function is disabled.
      See “Recording using the Clip Safe function in Propellerhead Balance” for more information about using the Clip
      Safe function.

      Monitoring
      Monitoring means listening to the input signal of an audio track. Monitoring works according to the following princi-
      ples:
      • By default, monitoring is automatically enabled as soon as an audio track is record enabled.
          This makes it possible to hear what you will be recording - before and during recording to disk.
      • During playback of an audio track, monitoring is automatically disabled.
          During playback, you will only hear the recorded signal - not any input signal.
      q   Note that you can manually activate or deactivate monitoring for a track by clicking the Monitor button.
      The input signal is monitored after the Channel strip and Master Section in the Main Mixer which means that all mixer
      parameters, including any Insert Effects, Dynamics etc., will also be applied to the monitored signal.
      !   Note that the Main Mixer parameters will only affect the monitored (and/or played back) signal - they will not
          affect the signal being recorded to disk.

      Depending on the technical specifications and/or settings in your hardware audio interface, the latency of the moni-
      tored input could become a problem. If this is the case, it’s probably better to monitor the input signal before it
      reaches the Reason program, i.e. directly on the external audio interface/mixer/preamp. If you don't want to monitor
      through the Reason program you should select "External" or “Manual” in the Monitoring section on the Audio tab in
      the Preferences dialog:

                                                             The “Monitoring” section
                                                             on the Audio tab in the
                                                             Preferences dialog

      D   Select “Automatic” to select automatic monitoring of the Audio Track in Reason.
          Each time you select and/or record enable an Audio Track in the Track List, monitoring in Reason will be automat-
          ically enabled. It’s possible to manually disable monitoring in this mode if you like.
      D   Select “Manual” to manually select if monitoring should be on or off.
          This mode should be selected if you prefer to have manual control over monitoring, or when you are monitoring
          through external mixer or audio interface. In the latter case, you would select "Manual" mode and just don't click
          any monitor buttons.
      D   Select “External” to deselect automatic monitoring of the Audio Track in Reason.
          When you select and/or record enable an Audio Track in the Track List, monitoring in Reason will be automatically
          disabled. It’s not possible to manually enable monitoring in this mode.

      Using the Tuner
      An audio track also features a built-in tuner function. The Tuner detects and displays the input pitch of a connected
      instrument - an electric guitar, for example.
      1. Click the “Enable Tuner” button below the device icon to switch to Tuner mode.
          The Input Meter switches to a Tuner.

          An audio track in Tuner mode.
      2. Play a note on the connected instrument and watch the Tuner.
          When the input pitch is detected, the Tuner lights up and indicates how far the pitch is from the displayed note
          value to the right of the Tuner. The center LED on the Tuner Meter indicates a perfectly tuned note pitch. The
          green arrow LEDs on either side of the Tuner Meter indicate how the connected instrument should be tuned. The
          left arrow LED means raise the pitch and the right means lower the pitch.
      !   Note that the input note needs to sustain for a little while before the pitch can be detected.

      The Recording Meter Window

      The main purpose of the Recording Meter floating window is to provide a good overview of recording levels and/or
      tuner values when you are located some distance away from the computer screen. The Recording Meter mirrors the
      information from the input level meter and Tuner of the currently selected record enabled Audio Track.
      D   Toggle the Recording Meter window on and off by selecting “Show/Hide Recording Meter” from the Windows
          menu.
      D   If you are using the Propellerhead Balance audio interface you can also press the Meter/Tuner button on the
          front panel to toggle the Recording Meter window on and off:

          The Meter/Tuner button on the Propellerhead Balance audio interface.
      D   Move the Recording Meter window by clicking on the window background and then dragging.
      D   If you have manually record enabled several Audio Tracks in the sequencer, you can choose which track to dis-
          play in the Recording Meter window by clicking the right/left arrows on either side of the Audio Track name.
          By default, the first record enabled Audio Track in the sequencer is displayed in the Recording Meter window.
      D   Click the pitchfork symbol in the Recording Meter window to bring up the Tuner for the selected Audio Track.
          A large Tuner display is shown at the bottom of the Recording Meter window.

          See “Using the Tuner” for more information about the Tuner.

      Recording audio
      !   To minimize the song saving time, we strongly recommend saving the song before recording many or large au-
          dio recordings.
      1. Set up the audio track according to the descriptions in “Setting up the audio track”.
      2. Record the track according to the descriptions in “General recording procedure”.
      3. When the recording is finished, the audio clip on the track shows the recorded audio as one or two continuous
         waves inside the clip, depending on whether the input was in mono or stereo:


=== END OF PART ===
