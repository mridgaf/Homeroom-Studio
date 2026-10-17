# Chapter 09: Reason 12 manual digest and studio workflow
## Part 23 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 14 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 24 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 14 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Performance controllers vs. track parameter automation
      Recording parameter automation can be done in two different ways; either as performance controller automation or
      as track parameter automation.
      • Performance controller automation is automatically recorded together with note events in note clips on note
        lanes.
        Any standard MIDI performance controllers that you apply when playing (Pitch Bend, Mod Wheel etc.) will be re-
        corded as performance controller automation in the note clip. A clip on a note lane can contain any combination of
        note events and performance controller automation events.
      • Track parameter automation creates separate parameter automation lanes on a track, one for each automated
        parameter.
      Which method you should use depends on how you prefer to work. The main differences to take into account are the
      following:
      • Performance controller automation allows you to contain the automation data in a note clip together with note
        events.
        The key feature with performance controller automation is that it’s contained together with the notes in the note
        clip. Moving the note clip moves the performance controller automation as well. Therefore, if your controller
        changes are part of your "note performance" (e.g. Pitch Bend and Sustain Pedal), then you want them as perfor-
        mance controllers (see “Recording performance controller automation”).
        Filter sweeps played together with the notes etc. can also be recorded as performance controllers (see “Recording
        parameter automation into Note Clips”).
      • If your parameter changes are for sound design or mixing purposes (e.g. a slow opening of a filter, a gradual
        change in level), they would probably work better as track parameter automation.
        Track parameter automation is recorded on separate lanes on the track (one lane for each automatable parame-
        ter). Track parameter automation clips can be moved individually, independent from any note clips. See “Recording
        parameter automation”.

      Recording performance controller automation
      If you use any MIDI performance controllers when recording on a note lane, these are automatically added to the re-
      corded clip. This makes sense as performance controllers are usually recorded at the same time you record notes, as
      a part of the performance. Standard MIDI performance controllers are Pitch Bend, Modulation Wheel, Sustain Pedal,
      Aftertouch, Breath Control and Expression.
      D   To record standard performance controller automation, just follow the descriptions in “Recording notes”.
          When you have recorded performance controllers in the note clip, the clip will have automation curves visible in it
          along with the recorded note data.

          Performance controllers are shown as curves in the note clip. In this picture, Mod Wheel, Pitch Bend and Sustain Pedal controllers
          have been used.
          Green borders will appear around the automated device parameters to indicate that they are automated.

          The Pitch Bend and Mod Wheel parameters have been automated, indicated by the green borders.
      !   After you stop recording, you need to click Stop again, or click the “Automation Override” indicator to the right
          on the Transport Panel, for the green automation borders to appear on the device panel.

          The Automation Override indicator on the Transport Panel.
          The performance controller automation is shown differently in the clip depending on the type of controller used.
          Controllers with bipolar range (such as Pitch Bend) are shown as lines in the middle when at zero (no pitch bend)
          with curves travelling up or down from the zero value. Controllers with only positive values (such as Mod Wheel)
          have zero at the bottom of the clip with applied modulation shown as curves travelling up from the zero value. Con-
          trollers with off/on values (such as Sustain Pedal) are shown as rectangular curves (on - duration- off).
      • If you open a note clip in Edit Mode (by double-clicking on the clip), the recorded performance data will show
        up on separate Performance Controller Edit Lanes on the Edit Pane.

                                                                                                            Performance Controller
                                                                                                            Edit Lanes

          Performance controller automation on separate Edit lanes in Edit Mode.

      q   Note that you can record notes and performance controllers separately. I.e. you can first record notes on one
          note lane and then record performance controllers on another note lane on the same instrument track. The au-
          tomation will be contained in note clips placed on a separate lane and can also be moved or muted separately.
      !   If several note lanes contain performance controller automation, the topmost lane has priority (see “About
          performance controller automation on multiple lanes”).
      q   It’s also possible to manually insert performance controller events by drawing events with the Pencil tool. Re-
          fer to “Drawing parameter automation events”.

      Recording parameter automation into Note Clips
      Besides the standard performance controllers (Pitch Bend, Mod Wheel etc.), you can choose to record automation of
      any type of instrument device parameter into a note clip:
      1. Select “Record Automation into Note Clip” from the Options menu.

      2. While recording on a note lane according to the description in “Recording notes”, tweak the parameter(s) you
         want to automate on the instrument device panel in the rack - or use a Remote MIDI controller (see “Remote -
         Playing and Controlling Devices”).
          Any parameter you tweak on the device will be recorded as automation inside the note clip - just like Performance
          Controller automation.
          Green borders will appear around the automated device parameters to indicate that they are automated.
      !   After you stop recording, you need to click Stop again, or click the “Automation Override” indicator above the
          audio meters on the Transport Panel, for the green automation borders to appear on the device panel.
      q   While this method is perfect for making a note clip self-contained, there are some trade-offs. If you use this
          method to record device parameters, you won’t have the same overview as with track parameter automation.
          You also won’t be able to later mute a separate parameter automation lane, or move to parameter lanes inde-
          pendently.
      !   It is possible to have overlapping track parameter automation and automation inside a note clip for the same
          parameter. In such a case, the track parameter automation overrides the note clip automation. As soon as the
          track parameter automation clip ends, any automation inside the remaining part of the note clip takes over.

      Recording performance controller automation over or into an
      existing clip
      • If you record over a note clip with performance automation data and you adjust any of the performance con-
        trollers used in the clip, the automation will be replaced with new performance events from this point onward
        until you stop recording.
          However, if the new recording should start before the original clip’s start position, a new clip will be created which
          will incorporate the original clip. The new automation data will replace the existing one, but any existing note
          events will not be affected (see “Recording parameter automation over or into an existing clip” and “Recording
          over or into an existing note clip”).

      About performance controller automation on multiple lanes
      If you have several active (un-muted) note clips with performance controller automation on different lanes of the
      same track, and these note clips overlap position-wise, the following rule applies:
      • Performance controllers in clips on the topmost lane override performance controllers of the same type in
        other overlapping clips on lanes below:

          The clip on Lane 2 has Mod Wheel automation, and the clip on Lane 1 also has Mod Wheel automation - plus
          Pitch Bend and Sustain Pedal automation and note events. The Mod Wheel automation affecting the notes will fol-
          low the automation curve of the clip on Lane 2 for its duration. As soon as the clip on Lane 2 ends, the notes will
          be affected by the Mod Wheel automation in the clip on Lane 1.

      Recording parameter automation
      Parameter automation is the standard way to automate device and channel strip parameters. Each automated de-
      vice/channel strip parameter will generate a separate automation lane on the track. It’s also possible to record auto-
      mation of the Tempo on the Transport Panel. This is described in detail in “Tempo automation recording”.

      Before you start recording parameter automation
      Before you start recording automation of a device/channel strip parameter, you may want to set it to a suitable start
      value, what we call its “static value”. By static value we mean the value the parameter should have whenever it is not
      automated in the song. Here is why:
      Let’s say you want to create a fade-out by recording a fader movement in a mixer channel strip. It’s a good idea to
      first set the fader to the correct static value (i.e. the value the fader should have before you start the fade-out). The
      same thing is true if you want to create a filter sweep somewhere in the song: first set the filter frequency to the value
      it should have elsewhere in the song, then record the filter sweep. This makes it possible to set up a static mix first,
      and then add some automated parameter changes anywhere in the song while maintaining the static values else-
      where in the song.
      You can think of the static value as a “default” or “fall-back” position for the duration of the song.
      q   You can change the static value at any time, by opening the automation clip in Edit Mode. See “Editing param-
          eter automation in Edit Mode”.

      Parameter automation recording procedure
      1. Make sure there is a sequencer track for the device you’re going to record parameter automation for.
          For audio track devices and for instrument devices, a sequencer track is automatically created together with the
          device. For mix channel and effect devices, that might not necessarily have a sequencer track, the easiest way to
          create a track for parameter automation is by right-clicking (Win) or [Ctrl]-clicking (Mac) on the device/channel
          strip parameter and selecting “Edit parameter Automation” from the pop-up.
      2. Set up the track for parameter automation recording according to the description in “Record enabling param-
         eter automation”.
          If the track has note lanes you may want turn off the “Record Enable” button for the active note lane (unless you
          plan to record notes and parameter automation simultaneously of course).
      !   Note that it is not necessary for the track to be selected, or for the track to have Master Keyboard Input, to be
          able to record parameter automation. The “Automation Record Enable” button is completely independent
          from Master Keyboard Input. However, if you want to adjust the parameters from a control surface or MIDI
          Controller keyboard, this is most easily done by setting Master Keyboard Input to the track - see “Setting Mas-
          ter Keyboard Input”.
      3. Record the track according to the description in “General recording procedure”.
      4. Record the parameter automation by changing device/channel strip parameter(s) in the rack or in the mixer.
          During recording, adjust the desired parameter(s), from the device panel or from a MIDI control surface. You can
          automate any parameter for the device - each parameter you tweak will automatically generate a separate param-
          eter automation lane and a clip will be recorded on the corresponding lane from the point you changed the param-
          eter.
      q   It is also possible to record automation of the channel strip EQ and Filter parameters from the Spectrum EQ
          window, see “The Spectrum EQ Window”.
      5. When you’re done, click the “Stop” button on the Transport Panel to stop recording.
          In the Song View or Blocks View, the parameter automation clip(s) on the lane(s) show the recorded parameter
          automation events as curves or lines inside the clip.

                                                                           Parameter automation clip
                                                                           with parameter events
          If you click the “Stop” button again, or click the “Automation Override” indicator on the Transport Panel, the auto-
          mated parameters on the device(s) will be marked with green borders, indicating that they have been automated.
          If you play back the recorded section again, the automated parameters will change automatically. Outside the clip
          boundaries, the parameters will have their original settings (the static values they had before you started record-
          ing).
      q   It’s also possible to manually insert parameter automation events by drawing events with the Pencil tool. Re-
          fer to “Drawing parameter automation events”.

      Recording parameter automation in Loop mode
      Recording parameter automation events in Loop mode works similar to “non-looped” recording (see “Recording pa-
      rameter automation”), except that for every new loop cycle any changed parameter value will replace the previously
      recorded value for the corresponding parameter.

      Recording parameter automation over or into an existing clip
      Recording parameter automation events over or into an existing automation clip will simply replace the previously re-
      corded automation events. However, If the new recording should start before the start position of the original auto-
      mation clip, and expand into the original clip, the new clip will merge with the original clip. After the new clip ends, the
      parameter automation in the original clip will “take over”.
      If you need to redo a section of the recorded automation in an existing clip, or simply record more automation for a
      parameter, proceed as follows:
      1. Set up and start recording in the same way as described in “Parameter automation recording procedure”.
          As long as you don’t change the parameter value, its automation data will be played back normally, and nothing will
          be changed.
      2. At the desired position, adjust the parameter.
          As soon as you start changing the parameter value, the Automation Override indicator will light up on the transport
          panel.

          The Automation Override indicator on the Transport Panel.
          From this point on, the previously recorded automation values will be replaced with the new automation values. Au-
          tomation recording is different from recording note events where nothing is erased when you record over previ-
          ously recorded clips. A parameter automation “overdub” will replace any previous automation values at the same
          position for the duration of the recording. Automation clips logically cannot be “overdubbed” as a parameter cannot
          have more than one specific value at a given point in time.
      3. When you’re done, click the “Stop” button on the Transport Panel to stop recording.
          You have now replaced the automation values from where you started recording to where you stopped recording.
          The Automation Override indicator will still be lit but it will go off if you click Stop or Play on the Transport Panel.
      D   You can also click the “Automation Override” indicator during recording.

          This “resets” the parameter to the previously recorded value and the automation recording will stop (making the
          previously recorded automation active again, from that position). You are still in record mode, so as soon as you ad-
          just the parameter again, the Automation Override indicator will light up.

      Adjusting automated parameters during playback - “Live
      mode”
      Even if you have automated a device/channel strip parameter, you can still “grab it” and adjust it during playback,
      overriding the recorded automation:
      1. During playback, adjust an automated parameter.
          The Automation Override indicator lights up on the Transport Panel.

          From this point onward, the recorded automation for the parameter is temporarily disabled.
      2. To activate the previously recorded automation again, click the “Automation Override” indicator.
          This returns the control of the parameter to the parameter automation lane in the sequencer.
      q   Note that you can also temporarily turn off automation for a parameter by clicking the “On” button (so that it
          goes dark) on the parameter automation lane in the sequencer (see “Muting a parameter automation lane”).

      Recording parameter automation on multiple tracks
      Although only one track can have Master Keyboard Input, it is possible to record enable any number of tracks for au-
      tomation recording.
      D   Activate the Record Enable Parameter Automation button for all the tracks you wish to record automation for.
          When recording is activated, all automation record enabled tracks will record track parameter changes from their
          respective devices in the rack. This is especially useful if you have assigned parameters on several devices to a
          single control on a MIDI control surface, or have multiple control surfaces controlling different devices in the rack
          while you’re recording. See “Remote - Playing and Controlling Devices” for details.

      Pattern automation recording details
      If your song contains pattern based devices such as the Redrum Drum Computer, Matrix Analog Pattern Sequencer
      or Dr. Octo Rex, you probably want to use more than a single pattern throughout the song. To facilitate this you can
      record pattern changes in the sequencer.

      Recording pattern automation
      1. Before you start recording on the track, make sure the “Record Enable Parameter Automation” button is on
         (red).
        You can disable the “Record Enable” button for the note lane for now as it won’t be needed.
      2. Make sure that the “Enable Pattern”/”Enable Loop Playback” button is activated on the device in the rack.

        The “Enable Pattern” buttons on the Redrum (top) and Matrix (bottom) devices.
      3. Set the desired start pattern on the pattern device.
      4. Start recording on the track from the desired position.
        When recording starts, the pattern device will automatically start. Although no clip will be created until you change
        pattern on the device for the first time, the start pattern is still being recorded.
      5. During recording, change patterns with the “Bank” and “Pattern” buttons on the device panel.
        As soon as a Pattern or Bank value is changed on the device, a pattern lane is automatically created on the track.
        On the lane, a pattern clip is automatically created and the pattern selection is recorded in the clip. Make sure you
        change the patterns slightly in advance - the actual pattern change will be recorded (and happen) on the next
        downbeat according to the sequencer time signature setting.
      6. When you are done, click “Stop” on the Transport Panel to stop recording.
        The automated pattern selection buttons on the device in the rack will marked with a green border, indicating that
        they have been automated. A pattern automation lane with pattern clips has also been created on the Edit/Ar-
        rangement Pane.

        Pattern automation clips on the pattern automation lane.
      • Pattern automation has no “static value”. Patterns will only be played back where there are pattern clips on
        the lane. Where the pattern lane has no clips, the device will stop and no pattern will be played back.

      • Each pattern change will be recorded on a downbeat (at the start of a new bar in the sequencer).
          You can move pattern changes to other positions by moving or resizing the pattern clips, see “Editing pattern au-
          tomation”.
      • You can “punch in” on recorded pattern changes, to replace a section of the pattern lane with new pattern au-
        tomation events. This can be done the same way as described in “Recording parameter automation over or
        into an existing clip”.
      • After recording the pattern changes, you can use the function “Convert Pattern Track to Notes”, to transfer the
        notes in the patterns to regular notes in the main sequencer.
          This allows you to create unlimited variations by later editing the notes in Edit mode. See “The “Convert Pattern
          Automation to Notes” function”.
      • On the Redrum, Matrix and Dr. Octo Rex devices, you could also use the “Copy Pattern/Loop to Track” func-
        tion.
          This function lets you convert a defined range of pattern clips into notes in a new note clip. See “Copy Pattern to
          Track”.
      q   You can also manually draw automation clips on the Pattern automation lane - see “Drawing pattern automa-
          tion”

      Tempo automation recording
      In Reason it’s possible to record automation of the sequencer’s tempo. This means that a song can automatically
      change tempo whenever you like. You can record tempo automation events on the parameter automation lanes on
      the Transport track.

      Recording tempo automation
      Automating tempo is done much in the same way as with other parameter automation. You record the tempo
      changes by changing the Tempo value on the Transport Panel. When you later play back, audio clips will automati-
      cally be stretched to follow the tempo changes (unless you have disabled stretch for the clips - see “About disabling
      Stretch for audio clips”). Note clips and automation clips will always follow tempo changes.
      To record tempo automation, do as follows:
      1. Set the desired song tempo in the Tempo display on the Transport Panel.
          This will be your static value, i.e. the tempo of the song wherever there is no clip present on the tempo automation
          lane.
      2. Press [Alt](Win) or [Option](Mac) and click in the Tempo display on the Transport Panel.
          This will both select the Transport track and create a Tempo automation lane at the same time. The Tempo display
          will also be marked with a border, indicating that the Tempo parameter has been automated.

      3. Start recording in the sequencer and record the tempo changes by changing the value in the Tempo display.
          Click and drag up/down in either of the display segments to change tempo in BPM steps or 1/1000 BPM steps.

                      or

      q   You can also manually draw Tempo automation events in the parameter automation clip, using the Pencil tool
          - see “Drawing tempo automation events”.

174   RECORDING IN THE SEQUENCER


---

<a id="arranging-in-the-sequencer-7"></a>

=== END OF PART ===
