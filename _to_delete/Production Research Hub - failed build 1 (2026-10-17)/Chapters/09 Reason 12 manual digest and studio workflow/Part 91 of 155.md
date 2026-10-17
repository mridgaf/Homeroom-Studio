# Chapter 09: Reason 12 manual digest and studio workflow
## Part 91 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 82 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 92 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 82 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 38: Rytmik Drum Machine

Rytmik Drum Machine

      Introduction

      The Rytmik Drum Machine device is an eight-channel drum sample player, designed for seamless integration of
      Reason Compact projects. Rytmik features a Distortion effect and a Low Cut + Hi Cut filter per drum channel. There
      are also two send effects - Reverb and Delay - that are shared among the eight drum channels, plus a master section
      with a Master Compressor, Master Pitch and a Master Filter.

      Panel overview
      The Rytmik front panel contains the following sections:

                                          1
           2                                                                 3

                   4            4        4          4           4       4          4           4      5

      The Rytmik front panel sections.
      • 1. Patch selector (for browsing, loading and saving patches).
      • 2. Sample playback and editing section (for the currently selected Drum Channel).
      • 3. Distortion and Low Cut + Hi Cut Filter (for the currently selected Drum Channel).
      • 4. Drum Channel sections (for playing back samples and for selecting Drum Channel to edit).
      • 5. Send Effects and Compressor section (global for all eight Drum Channels).

      Signal flow
      The picture below shows the basic signal flow in Rytmik:

                                                                                               Reverb
                                                                                   Send (x8)            Lvl (x1)

           Sample Playback (x8)   Distortion (x8)    Filter (x8)
                                                                                               Delay
                                                                        Pan (x8)   Send (x8)
                                                                                               Clean

                                                                   Vol (x8)

                                                                                                           Compressor

                                                                                                             EQ/Filter

                                                                                                                         Volume

                                                                                                                   Out

      Rytmik signal flowchart.
      • Rytmik features eight Sample Playback engines (one per Drum Channel).
         Each Sample Playback engine features a Sample section, where you can select any of the built-in samples. Here,
         you can also set the Sample Start, Sample End, Pan, Pitch, Fade In and Fade Out parameters.
      • The audio from the Sample Playback engines are then routed to a Distortion insert effect (one per Drum Chan-
        nel).
      • The signal is then routed to a Filter section (one per Drum Channel).
         The signal can then be processed with a Low Cut and Hi Cut filter.
      • The signal from each Drum Channel can then be panned in stereo - and have its own individual volume.
      • Each Drum Channel can also use the two global Send Effects (Reverb and Delay).
         The signal levels to each of these send effects can be set individually for each Drum Channel.
      • Finally, the signals of all eight Drum Channels, plus the Send Effects are mixed and output as a stereo signal
        via a Master Compressor and a Master Filter.
         It’s also possible to output the desired Drum Channel signals individually via separate audio outputs - if you want
         to process the signals outside of the Rytmik device. If you do that, the signal will be output after the Filter section
         of the Drum Channel, bypassing the Send Effects and the Master FX.

      Global controls
      Loading and saving patches

      Loading and saving patches is done in the same way as with any other internal Reason device, see “Loading patches”
      and “Saving patches” for details.

      The Drum Channel sections

      Auditioning samples
      D   Click a Drum Channel button to play back the sample of the corresponding Drum Channel.
          By clicking the Drum Channel button you also automatically select the Drum Channel (see below).

      • If you are using a MIDI Keyboard/On-screen Piano Keys you can play back the samples of the Drum Channels
        from Key C0 to G0.

      Selecting a Drum Channel
      D   Click a Drum Channel button to select the desired Drum Channel:

      Muting and soloing Drum Channels
      D   Click the M(ute) or S(olo) button in a Drum Channel to mute or solo the desired Drum Channel:

      Setting the Drum Channel volumes
      D   Drag the Volume slider up/down - or just click - to set the volume of a Drum Channel:

      Setting the Send Effect levels
      D   Turn the Delay and Reverb knobs to set the send levels from the Drum Channel to the respective Send Effect:
          See “The Master FX section” for more information about the Send Effects.

      The Sample Playback section

      The Sample Playback section contains all sample related controls and parameters for the currently selected Drum
      Channel. The currently selected Drum Channel is indicated by the lit Drum Channel selection button (see “Selecting a
      Drum Channel”).
      The Sample Playback section features the following parameters and controls:

      Selecting Samples

      D   Select and load a sample either by clicking the triangular arrow buttons on either side of the sample name - or
          by clicking the sample name and selecting from the pop-up menu.
          The pop-up menu features eight sub-groups with different types of samples.
      !   All samples in Rytmik are embedded in the device itself, so when you save a Rytmik patch the samples are al-
          ways included (as opposed to other sampler devices in Reason).

      Setting the Sample Start and End

      D   Click and drag the Sample Start handle sideways to change the where in the sample playback should begin.
      D   Click and drag the Sample End handle sideways to change the where in the sample playback should stop.

      Setting the Panning

      D   Click and drag up/down in the Pan box to place the sample in the stereo panorama.
          Range: 100L to 100R.

      Setting the Pitch

      D   Click and drag up/down in the Pitch box to set the pitch of the sample.
          Range: +/- 1200 cents.

      Setting Fade In and Fade Out

      D   Click and drag up/down in the Fade In and/or Fade Out boxes to apply a fade in/out of the sample.
          Any fade in/out is shown graphically in the sample display.

      The Insert Effects section

      The Insert Effects section consists of a Distortion effect and a Low Cut and Hi Cut Filter.

      Distortion

      The Distortion effect is a transistor type of distortion.
      D   Click and drag up/down in the Distortion box to adjust the input gain to the distortion effect.
          A high value will overdrive the pre-amp and generate more distortion.
          Range: 0-100%, where “0” is completely dry/off.

      Low Cut and Hi Cut Filter

      The Filter features a Low Cut (Highpass) and a Hi Cut (Lowpass) filter. Perfect for removing any rumble (Lo Cut)
      and/or hiss (Hi Cut), for example.
      D   Click and drag up/down in the Low Cut box to set the cutoff frequency for the highpass filter.
          Alternatively click the left part of the filter curve in the display and drag sideways.
          Range: 20 Hz to 25 kHz.
      D   Click and drag up/down in the Hi Cut box to set the cutoff frequency for the lowpass filter.
          Alternatively click the right part of the filter curve in the display and drag sideways.
          Range: 20 Hz to 25 kHz.
      !   Note that the Low Cut and Hi Cut cutoff frequencies can also be on opposite sides of each other, which means
          that the level of the sample could eventually drop to zero with extreme settings.

      The Master FX section

      The Master FX section features controls for the Delay and Reverb send effects, as well as for the master bus Com-
      pressor. The Send Effects can be used by all Drum Channels simultaneously, and the effects are active simultane-
      ously.

      Delay

      This is a delay with two different modes - Stereo and Ping Pong. The delay repeats are tempo synced and you can
      select the desired time division.

      Mode

      D   Click the Mode box and select the desired mode from the pop-up.
          “Stereo” repeats the delay in stereo in a fixed centered position.
          “Ping Pong” repeats the delays, alternating between the left and right channels.

      Time

      D   Click and drag the Time box up/down to set the time division of the tempo-synced delay repeats.
          The tempo is hard-wired to the main sequencer tempo.
          Time divisions: 1/1, 1/2D, 1/1T, 1/2, 1/4D, 1/2T, 1/4, 1/8D, 1/4T, 1/8, 1/16D, 1/8T and 1/16

      Feedback

      D   Click and drag the Feedback box up/down to set the number of delay repeats.
          Alternatively, click and drag in the display to set the Feedback amount.
          Range: 0-100%, where “0” is one single delay repeat.

      Reverb

      This is a stereo reverb with six different Modes (reverb algorithms).

      Mode

      D   Click the Mode box and select the desired reverb algorithm from the pop-up.
      The following reverb types can be selected:
      • Room
      • Large Room
      • Culvert
      • Plate
      • Gated
      • Hall

      Decay

      D   Click and drag the Decay box up/down to set the length of the reverb effect.
          Alternatively, click and drag in the display to set the decay length.
          The Decay amount is also shown graphically in the display.

      Low Cut and Hi Cut

      This is essentially a combination of a highpass and a lowpass filter.
      D   Raise the Low Cut value to cut the low frequencies of the reverb signal and make the reverb effect less
          “muddy”.
          Range: 20 Hz to 25 kHz.
      D   Lower the Hi Cut value to cut off the high frequencies of the reverb, thereby creating a smoother, warmer ef-
          fect.
          Range: 20 Hz to 25 kHz.
      !   Note that the Low Cut and Hi Cut cutoff frequencies can also be on opposite sides of each other, which means
          that the reverb level could eventually drop to zero with extreme settings.

      Compressor

      This is a stereo compressor, which acts on the total mix of all Drum Channels. It is always active, but if you don’t want
      any compression effect you can set the controls so that no compression is produced. The gain reduction is shown by
      the meter.

      Threshold

      This is the threshold level above which the compression sets in. Signals with levels above the threshold will be af-
      fected, signals below it will not. In practice, this means that the lower the Threshold setting, the more the compression
      effect.
      D   Click and drag the Threshold box up/down to set the threshold level.
          Range: -60 dB to 0 dB
      q   For no compression effect at all, set the Threshold to “0 dB”.

      Ratio

      This specifies the amount of gain reduction applied to the signal above the set threshold. A high Ratio value makes
      the sound less dynamic and more “even” in level.
      D   Click and drag the Ratio box up/down to set the compression ratio.
          Range: 1:1 to 20:1
      q   For no compression effect at all, set the Ratio to “1.00”.

      Attack
      This governs how quickly the compressor applies the gain reduction when signals rise above the set Threshold (see
      above). If you raise the Attack value, the response will be slower, allowing more of the signal to pass through the
      compressor unaffected. Typically, this is used for preserving the attacks of the sounds.

      D   Click and drag the Attack box up/down to set the compressor attack time.
          Range: 0-200 ms

      Release
      When the signal level drops below the set Threshold (see above), this determines how long it takes before the com-
      pressor lets the sound through unaffected. Set this to short values for intense, “pumping” compressor effects, or to
      longer values for a smoother change of the dynamics.

      D   Click and drag the Release box up/down to set the compressor release time.
          Range: 0-200 ms

      Master Pitch

      D   Turn the Master Pitch knob to adjust the pitches of all Drum Channels equally.
          Range: +/-1200 cents.

      Master Reverb

      D   Turn the Master Reverb knob to adjust the Reverb return level.
          Range: +/-100%.
      !   Note that this control is bipolar, i.e. you could attenuate or amplify the reverb return level. This means that if
          any of the Reverb Amount knobs for the Drum Channels are < 0 dB, raising the Master Reverb knob to a posi-
          tive value will increase the Reverb level for these Drum Channels. The level can never exceed 0 dB, though.

      Master Filter

      The Master Filter is a combined highpass and lowpass filter, which can be used for cutting out low or high frequen-
      cies in the total mix signal. At the default 0% setting the output signal is completely unaffected (not filtered at all).
      D   Turn the Master Filter knob to adjust the Low Cut and Hi Cut effect.
          Range: +/-100%.

      Master Volume

      D   Drag the Master Volume slider up/down - or just click - to set the output volume of the total mix.
          Range: -inf to 6.00 dB

      Connections

      !   Remember that CV connections are NOT stored in the Rytmik patches! If you want to store CV connections be-
          tween devices, put them in a Combinator device and save the Combi patch.

      Drum Gate In/Out
      The Drum Gate inputs allow you to play Rytmik from another CV/Gate device. The Drum Gate inputs respond to
      “Note On/Off” along with Velocity.
      The Drum Gate outputs allow you to control other CV/Gate equipped devices from Rytmik. The Drum Gate outputs
      send out “Note On/Off” along with Velocity.

      Separate Outputs
      The separate outputs can be used for routing individual Drum Channels to external destinations, for further process-
      ing.
      !   Note that Drum Channels routed via separate outputs are automatically disconnected from the Master FX sec-
          tion. Note, though, that the signal could still be sent to (and heard via) the Send Effects (Delay and Reverb) on
          the Main Outputs.

      Main Output L & R
      These are the main audio outputs. When you create a new Rytmik device, these outputs are auto-routed to the first
      available Mix Channel in the Reason main mixer. If there is no Mix Channel available, a new one will be automatically
      created.


---

<a id="radical-piano-39"></a>

=== END OF PART ===
