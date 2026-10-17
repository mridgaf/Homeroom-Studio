# Chapter 09: Reason 12 manual digest and studio workflow
## Part 81 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 72 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 82 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 72 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      The Send section

      The Send knobs can be used for tapping the output signal of the Slot to the corresponding FX Send Out jacks on the
      rear panel (see “FX Send Out”). You could then route the signals to external effect devices and then further to a sep-
      arate mixer/audio channel.
      D   Control the Send output levels with the corresponding Send knobs.

      Connections

      !   Remember that CV connections are NOT stored in the Mimic patches! If you want to store CV connections
          between devices, put them in a Combinator device and save the Combi patch.

      Sequencer Control inputs
      The Sequencer Control CV and Gate inputs allow you to play Mimic from another CV/Gate device (typically a Matrix
      or an RPG-8). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note on/
      off along with velocity. There are also inputs for modulating the Pitch Bend and Mod Wheel parameters.

      CV In 1-4
      These four assignable control voltage (CV) inputs can be used for modulating parameters on the Mimic front panel,
      by selecting “CV In” in the Mod drop-down selector for the desired parameter.

      Slot Out 1-8
      These outputs are breakout jacks for each individual Slot. Connect these to have the audio from the desired Slot(s)
      routed to its own stereo output pair.
      !   Connecting any of the Slot Outs will automatically remove the corresponding Slot from the Master Audio Outs.

      FX Send Out
      Here you can route the audio from all eight Slots to external effect devices for further processing. Since there are no
      FX Return jacks on Mimic, route the processed signal to a separate mixer/audio channel. You can control the Send
      level of each Slot with the respective Send knobs (see “The Send section”).

      Audio Output
      These are the main audio outputs. When you create a new Mimic device, these outputs are auto-routed to the first
      available Mix Channel in the main mixer. If there is no Mix Channel available, a new one will be automatically created.

      Tips and Tricks
      Optimizing performance/DSP Load
      Under some circumstances Mimic could be quite DSP demanding. If you experience any excessive DSP Load or
      playback problems, please check the following:
      D   Try another Stretch Type (see “Stretch”).
          Especially the “Advanced” Stretch Type can be quite DSP consuming.
      • If you are playing high-pitched notes using a low-pitched sample, the stretch function has to calculate a lot. To
        reduce the workload, try loading a higher pitched sample (which has a higher Root Key) and use that instead.
      D   Try to avoid having a lot of notes decaying at the same time. Try shortening the Release time of the Amp Enve-
          lope (see “The Filter Envelope and Amp Envelope sections”) and/or deactivating Play Thru in Slice Mode (see
          “Play Thru”).

      Creating a “velocity layered” instrument
      A neat way to simulate a velocity layered instrument is to sample the same note repeatedly, of let’s say a bass or pi-
      ano, and then modulate which of the recorded notes should play back. This will give you a more “live” and organic
      sound when you play. In this example we have sampled the same note of a bass guitar eight times in a single record-
      ing, played with a little different nuances between the eight picks:

      1. Make sure Pitch Mode is selected.
      2. Click the “Snap to Slices” LED in the Start Position section.
          Do this to ensure that the playback will start from a slice marker (and not from in between slice markers).
      3. Select “Velocity” in the Start Position Mod drop-down list and turn up the Start Position Mod amount.
          We are now controlling which “slice” should play back from Keyboard Velocity. You can of course choose another
          modulation source (e.g. Mod Wheel) if you want to control the start position using the Mod Wheel instead.
      q   Make sure you set the Amp Envelope “Release” time so that the consecutive “slice” doesn’t play back.

      Extending the sample “tail” (without looping)
      Sometimes it could be useful to extend the tail of a sample (a drum sample, for example), to have it decay longer than
      the original sample length. An easy way of doing this is by modulating the “Speed” parameter as follows:

      1. Turn down the “Speed” knob close to minimum.
      2. Turn up the “Speed Mod” knob and select “Filt Env” as Speed Mod source.
      3. Select the “Advanced” stretch type in the Stretch section.
      4. Raise the Filter Envelope (D)ecay slider to the desired value.
        When you play and hold a key down, the Speed will quickly raise and then slow down in the sample tail, making the
        playback time extend.

      Automating the sample Start and End markers
      Besides the regular modulation capabilities in Mimic, you could also automate and modulate the sample Start and
      End markers from the main sequencer, to have them reposition in real-time during sequencer playback. This could be
      useful if you have a longer recording/sample that you want to alter the playback position in:
      1. Record some notes on the Mimic sequencer track in the sequencer and then hit Stop twice.
      2. Hit Record again in the sequencer and drag the Sample Start and Sample End markers during recording:

      q   If you like, drag and move the Start/End marker up into the Slice Marker area above the waveform, to have the
          Start/End marker snap to the closest slices. This works in all modes, not just in Slice Mode.
      3. Hit Stop in the sequencer twice when you are done recording.
          If you moved both the Sample Start marker and the Sample End marker you will now have two Parameter Auto-
          mation lanes with clips on them on the Mimic sequencer track:

      • The clips on the Start Pos and End Pos lanes represent the movements of the Sample Start and Sample End
        markers respectively.


---

<a id="thor-polysonic-synthesizer-33"></a>

=== END OF PART ===
