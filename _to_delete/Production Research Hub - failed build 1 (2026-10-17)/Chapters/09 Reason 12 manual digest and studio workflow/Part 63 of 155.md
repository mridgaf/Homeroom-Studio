# Chapter 09: Reason 12 manual digest and studio workflow
## Part 63 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 54 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 64 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 54 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 26: Hardware Interface

Hardware Interface

      Introduction

      The Hardware Interface device is where you connect Reason to the “outside world”. This is where MIDI is received,
      and where audio signals are routed from physical inputs and to physical outputs of your audio hardware. The Hard-
      ware Interface is always present at the top of the rack, and cannot be deleted. This chapter is meant to serve as a
      panel reference, describing the various sections of the device. How to set up your audio hardware is described in the
      “Audio Basics” chapter.
      The Hardware Interface is normally unfolded, showing a panel with 2 Sampling Inputs, 16 Audio Inputs and 16 Audio
      Outputs and a couple of buttons.
      • On the right hand side at the top of the panel are the Input Focus and Play Focus buttons - these are described
        in “Input Focus and Play Focus”.
      • The Sampling Input, Audio Input and Audio Output sections feature a LED meter for each input and output
        channel.
      !   Remember that the Hardware Interface is where any possible audio clipping will occur in Reason. Keep an eye
          on the clipping indicator on the Transport Panel, and also on the individual meters on the Hardware Interface
          panel. If a channel pushes the meter into the red, the level should be reduced at the source - see “About audio
          levels” in the “Audio Basics” chapter.
      • The multi-color LEDs below each channel indicate the following:
          Green LED: Available and used channel (cable connected to the channel jack on the rear panel).
          Yellow LED: Available but unused channel (no cable connected to the channel jack on the rear panel).
          Red LED: Unavailable channel but with a connected cable on the rear panel. No audio will be present on channels
          with red LEDs.
          Unlit LED: Unavailable and unconnected channel (no cable connected to the channel jack on the rear panel).
      • By clicking the “ADVANCED MIDI” button at the top on the panel, the Advanced MIDI Device panel is shown:

      Refer to “Advanced MIDI Device” for more information.
      • By clicking the “MORE AUDIO” button at the top on the panel, an additional Audio In and Out panel is shown
        for a total of 64 inputs and outputs.

      Refer to “More Audio” for more information.

      • By clicking the “BIG METER” button at the top on the panel, a panel with bigger audio level meters is shown:

      Refer to “The Big Meter” for more information.

      Sampling Input section

      The Sampling section features two audio inputs (L & R) to which you should route the audio signals you want to sam-
      ple. There is also a Level knob and two Monitor buttons. See “Setting up for sampling” for details on how to sample.

      Advanced MIDI Device

      !   Do NOT use the Advanced MIDI Device if you are only going to use Reason’s internal sequencer for recording
          and playback!
      This is opened by clicking the “ADVANCED MIDI” button on the Hardware Interface panel. The Advanced MIDI de-
      vice is only used if you are controlling Reason from an external sequencer, using the External Control Bus inputs.
      Normally, you send MIDI to a track via the sequencer, by selecting the sequencer track.
      You can select MIDI ports for up to four External Control Busses (on the Sync page in Preferences). Each bus can
      host 16 MIDI channels, for a total of up to 64 MIDI input channels. The Advanced MIDI Device is where you can route
      each MIDI channel to a specific device in the Reason rack:
      1. Select one of the External Control Busses by clicking the corresponding Bus Select button at the top of the Ad-
         vanced MIDI device.
      2. Pull down the device pop-up menu for a MIDI channel and select a device.
          The menu lists all devices in the current song.
      Now, incoming MIDI data on the selected bus and MIDI channel is sent directly to the selected device, bypassing the
      Reason sequencer. The name of the device is shown in the name field for that MIDI particular channel.
      3. Try sending MIDI notes from the external sequencer, on the selected bus and MIDI channel.
          The indicator below the channel's name field should light up.
      See also “Advanced MIDI - The External Control Bus inputs” in the Advanced MIDI and Synchronization chapter.

      More Audio
      Reason supports up to 64 audio input and 64 audio output channels. The additional 48 inputs and 48 outputs can be
      found on the “More Audio” panel.
      D   To view inputs 17-64 and outputs 17-64, click the “More Audio” button.

      Each additional input and output features a meter and a multi-color LED indicator which will be lit in different colors
      depending on current state - see “Introduction”.

      The Big Meter
                                      The “Show Big Meter” button                           Channel Selection buttons
                                                                                            for the “Big Meter”

               Meter Mode                     Channel Selection knob                                                   Reset
               button                         for the “Big Meter”                         Clip indicators              button
      To get a better overview of the levels of a particular channel pair you can bring up the Big Meter on the Hardware
      Interface.
      1. Click the “BIG METER” button on the front panel.
          The “Big Meter” panel shows up.
      2. Select the Input or Output pairs to view in the Big Meter by clicking on the corresponding Channel Selection
         button below each Input or Output pairs.
          Alternatively, select channel by turning the Channel Selection knob.
      D   It’s also possible to select various Meter Modes, or combinations of Meter Modes, by clicking the Meter Mode
          button to the far left.
          The available Meter Modes are:
      • VU
          The VU Mode simulates the behavior of analog meters and shows the RMS (Root Mean Square) value of the sig-
          nal. Since the RMS value is an "average" of the signal level over time it's not suited for detecting fast transients in
          the sound. Rather, VU meters are useful for monitoring the overall loudness of the signal.
          In VU Mode, the meter response is 300 ms/20 dB for both attack and release. There is no peak segment in the
          meter.
      D   The VU Offset can be set in 2 dB steps between -20 and 0 dB, by turning the VU Offset knob.
          This setting determines how the VU dB scale relates to the Peak dB scale. If you have no specific preference in
          this matter, you don't need to change the VU Offset.
      !   The VU Offset setting will affect the readout of all Meters on the Main Mixer channel strips and on their corre-
          sponding Rack devices.
      • PPM
          In PPM (Peak Program Meter) Mode, the meter response is 0 ms rise and 2.8 s/24 dB fall. The PPM Mode is per-
          fect for detecting transients in the sound. There is no peak segment in the meter.
      • PEAK
          In PEAK Mode, the meter response is 0 ms for both rise and fall, which means that this mode provides the most
          accurate representation of the signal level over time. Since the fall time is 0 ms, it could be quite distracting to the
          eyes to watch the meters in PEAK mode. If so, the PPM Mode might be more convenient since it's equally fast at
          responding to transients, but falls more slowly.
          The peak segment (the rightmost LED segment, indicating the highest level) has a fall time according to the Peak
          Hold parameter setting (5 seconds or infinite). This allows you to more easily spot very brief level peaks.

      • VU+PEAK
        In VU+PEAK Mode, the meter response is according to the VU Mode, plus a peak segment.
      • PPM+PEAK
        In PPM+PEAK Mode, the meter response is according to the PPM Mode, plus a peak segment.
      If the audio level for the selected is, or have been, too high, the Clip indicators on the Big Meter will stay lit until you
      click the “Reset” button, or select new audio channels for the Big Meter. See “About audio levels” for more informa-
      tion on how to use and work with the Big Meter.


---

<a id="kong-drum-designer-27"></a>

=== END OF PART ===
