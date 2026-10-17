# Chapter 09: Reason 12 manual digest and studio workflow
## Part 71 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 62 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 72 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 62 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Global Transpose

      Set the global transposition of the loops in all Loop Slots by using the Global Transpose spin control. You can raise
      or lower the pitch in 12 semitone steps (+/– 1 octave).
      • The Global Transpose value can also be controlled via MIDI Notes, by pressing a key between C-2 and C0 (with
        C-1 resetting the transpose value to zero).
          This way you can also record transposition changes in the sequencer.

      Dr. Octo Rex synth parameters
      The Dr. Octo Rex synth parameters are used for shaping and modulating the sound of the REX loops. These param-
      eters are familiar synth parameters, similar to the ones in the synthesizers; The Subtractor and the Malström, and in
      the samplers; the NN-19 and the NN-XT. It is important to remember that these parameters do not alter the REX
      files in any way, only the way they will play back.
      !   Most of the synth parameters are global, in the sense that they will affect all slices in the REX files as well as
          all REX loops in all eight Loop Slots.
      !   All Dr. Octo Rex synth panel settings are stored in the Song (and in the Dr. Octo Rex patch file if you choose to
          save the settings as a patch).

      Select Loop & Load Slot

      D   Click any of the eight Select Loop & Load Slot buttons to select a loaded REX loop for editing, or to load a new
          REX file to.
          If no loop is already present in the selected Loop Slot, the Waveform Display will be blank. Otherwise, the display
          shows a graphical readout of the REX loop and info (name, original loop tempo, number of bars and signature).
      D   Click the Follow Loop Playback button to “synchronize” the Select Loop & Load Slot buttons to the Loop Slot
          buttons on the front panel.
          This way, the currently playing loop will always be displayed in the Waveform Display. If you’re using Pattern Auto-
          mation in the sequencer, where the Slots are switched during playback, you might want to deactivate the Follow
          Loop Playback function to make it easier to edit a specific loop.
      Refer to “Adding Loops” for info on how to load REX files and to “Editing in the Waveform Display” for info about ed-
      iting the REX loop.

      Loop Transpose

      D   Set the transposition of individual loops in the Dr. Octo Rex by using the Loop Transpose knob to the bottom
          left on the panel, or by clicking on the keyboard display below the knob.
          You can raise or lower the pitch in 12 semitone steps (+/–1 octave).
      q   It’s also possible to set a global transpose value that affects all REX loops equally, see “Global Transpose”.

      Loop Level
      D     Set the individual levels for the loops in the Loop Slots with the Loop Level knob.
            This lets you match the levels of the loops in the 8 Loop Slots.

      Oscillator section

      For a REX file, the audio contained in the slices are what oscillators are for a synthesizer, the main sound source. The
      following settings can be made in the Osc Pitch section of the Dr. Octo Rex:

      Env. A
      This parameter determines to what degree the overall pitch of all the REX files will be affected by the Filter Envelope
      (see “Filter Envelope”). You can set negative or positive values here, which determines whether the envelope curve
      should raise or lower the pitch.

      Oct and Fine - Setting the overall Pitch
      You can change the overall pitch of all REX files in the 8 Loop Slots in three ways:
      D     In octave steps.
            This is done using the Oct knob. The range is 0 - 8, with “4” as default.
      D     In semitone steps.
            This is done by using Global Transpose controls, see “Global Transpose”.
      D     In cents (hundredths of a semitone).
            The range is -50 to 50 (down or up half a semitone).
      q     To transpose individual REX loops, use the Loop Transpose parameter, see “Loop Transpose”.
      !     To tune an individual slice in a REX loop, select it and use the Pitch parameter below the waveform display,
            see “Editing in the Waveform Display”.

      Mod. Wheel

      The Modulation wheel can be set to simultaneously control a number of parameters. You can set positive or negative
      values, just like in the Velocity Control section. The following parameters can be affected by the modulation wheel:

      | Parameter              | Description
          F. Freq              This sets modulation wheel control of the filter frequency parameter. A positive value will raise the fre-
                               quency if the wheel is pushed forward. Negative values invert this relationship.

      | Parameter         | Description
      F. Res               This sets modulation wheel control of the filter resonance parameter. A positive value will increase the
                           resonance if the wheel is pushed forward. Negative values invert this relationship.
      F. Decay             This sets modulation wheel control for the Filter Envelope Decay parameter. A positive value will increase
                           the decay if the wheel is pushed forward. Negative values invert this relationship.

      Velocity section

      Velocity is usually used to control various parameters according to how hard or soft you play notes on your keyboard.
      A REX file does not contain velocity values on its own. And when you create sequencer track data by applying the
      “Copy Loop To Track” function, all velocities are set to a default value of “64”. As velocity information is meant to re-
      flect variation, having them all set to the same value is not meaningful if you wish to velocity control Dr. Octo Rex pa-
      rameters.
      There are basically two ways you can apply “meaningful” velocity values to REX files:
      • After creating track data, you can edit velocity values in the Velocity Lane in the sequencer.
      • You can play slices in real time on your keyboard. The resulting data will have velocity values reflecting how
        the notes were struck when you played.
      When velocity values have been adjusted, you can control how much the various parameters will be affected by ve-
      locity. The velocity sensitivity amount can be set to either positive or negative values, with the center position repre-
      senting no velocity control.
      The following parameters can be velocity controlled:

      | Parameter          | Description
      F. Env                This sets velocity control for the Filter Envelope Amount parameter. A positive value will increase the en-
                            velope amount with higher velocity values. Negative values invert this relationship.
      F. Decay              This sets velocity control for the Filter Envelope Decay parameter. A positive value will increase the De-
                            cay time with higher velocity values. Negative values invert this relationship.
      Amp                   This let’s you velocity control the overall volume of the file. If a positive value is set, the volume will in-
                            crease with higher velocity values.

      The Filter Section

      Filters are used for shaping the overall timbre of all REX files in all 8 Loop Slots. The filter in Dr. Octo Rex is a multi-
      mode filter with five filter modes.

      D   Activate or deactivate the filter completely by clicking the Filter On button.
          The filter is active when the button is lit.

      Mode
      With this selector you can set the filter to operate as one of five different types of filter. These are as follows:
      • Notch
          A notch filter (or band reject filter) could be described as the opposite of a bandpass filter. It cuts off frequencies
          in a narrow midrange band, letting the frequencies below and above through.
      • High-Pass (HP12)
          A highpass filter is the opposite of a lowpass filter, cutting out lower frequencies and letting high frequencies pass.
          The HP filter slope has a 12 dB/Octave roll-off.
      • Bandpass (BP 12)
          A bandpass filter cuts both high and low frequencies, while midrange frequencies are not affected. Each slope in
          this filter type has a 12 dB/Octave roll-off.
      • 12 dB Lowpass (LP 12)
          This type of lowpass filter is also widely used in classic analog synthesizers (Oberheim, early Korg synths, etc.). It
          has a gentler slope (12 dB/Octave), leaving more of the harmonics in the filtered sound compared to the LP 24 fil-
          ter.
      • 24 dB Lowpass (LP 24)
          Lowpass filters lets low frequencies pass and cuts out the high frequencies. This filter type has a fairly steep roll-
          off curve (24dB/Octave). Many classic synthesizers (Minimoog/Prophet 5 etc.) used this filter type.

      Filter Frequency
      The Filter Frequency parameter (often referred to as “cutoff”) determines which area of the frequency spectrum the
      filter will operate in. For a lowpass filter, the frequency parameter could be described as governing the “opening” and
      “closing” of the filter. If the Filter Freq is set to zero, none or only the very lowest frequencies are heard, if set to max-
      imum, all frequencies in the waveform are heard. Gradually changing the Filter Frequency produces the classic syn-
      thesizer filter “sweep” sound.
      !   Note that the Filter Frequency parameter is usually controlled by the Filter Envelope (see “Filter Envelope”) as
          well. Changing the Filter Frequency with the Freq slider may therefore not produce the expected result.

      Resonance
      The filter resonance parameter affects the character of the filter sound. For lowpass filters, raising the resonance will
      emphasize the frequencies around the set filter frequency. This produces a generally thinner sound, but with a
      sharper, more pronounced filter frequency “sweep”. The higher the resonance value, the more resonant the sound be-
      comes until it produces a whistling or ringing sound. If you set a high value for the resonance parameter and then vary
      the filter frequency, this will produce a very distinct sweep, with the ringing sound being very evident at certain fre-
      quencies.
      • For the highpass filter, the resonance parameter operates just like for the lowpass filters.
      • When you use the Bandpass or Notch filter, the resonance setting adjusts the width of the band.
          When you raise the resonance, the band where frequencies are let through (Bandpass), or cut (Notch) will become
          narrower. Generally, the Notch filter produces more musical results using low resonance settings.

      Envelope section
      Envelope generators are used to control several important sound parameters in analog synthesizers, such as pitch,
      volume, filter frequency etc. In a conventional synthesizer, envelopes govern how these parameters should respond
      over time - from the moment a note is struck to the moment it is released. In the Dr. Octo Rex device however, the en-
      velopes are triggered each time a slice is played back.
      There are two envelope generators in the Dr. Octo Rex, one for volume, and one for the filter frequency (and/or
      pitch). Both have the standard four parameters; Attack, Decay, Sustain and Release
      !   Please refer to “Envelopes - General” in the Subtractor chapter for a description of the basic envelope param-
          eters.

      Amplitude Envelope

      The Amp Envelope governs how the volume of each slice should change over time, from the time it is triggered (the
      slice note starts) until the slice note ends. This can be used to make a loop more distinct (by having a snappy attack
      and a short decay time) or more spaced-out (by raising the attack time).

      Filter Envelope

      The Filter Envelope can be used to control two parameters for all REX loops in the 8 Loop Slots; filter frequency and
      overall loop pitch. By setting up a filter envelope you control how the filter frequency and/or the pitch should change
      over time for each slice.
      The Amount parameter determines to what degree the filter frequency will be affected by the Filter Envelope. The
      higher the Amount setting, the more pronounced the effect of the envelope on the filter.
      q   Try lowering the Frequency slider and raising Resonance and Envelope Amount to get the most effect of the
          filter envelope!

      LFO section

      LFO stands for Low Frequency Oscillator. LFOs are oscillators in the sense that they generate a waveform and a fre-
      quency. However, there are two significant differences compared to normal sound generating oscillators:
      • LFOs only generate waveforms with low frequencies.
      • The output of the two LFOs are never actually heard. Instead they are used for modulating various parameters.
      The most typical application of an LFO is to modulate the pitch of a (sound generating) oscillator or sample, to pro-
      duce vibrato. In the Dr. Octo Rex device, you can also use the LFO to modulate the filter frequency or panning.

      Waveform
      LFO 1 allows you to select different waveforms for modulating parameters. These are, from top to bottom:

      | Waveform         | Description
      Triangle            This is a smooth waveform, suitable for normal vibrato.
      Inverted            This produces a “ramp up” cycle. If set to control pitch (frequency), the pitch would sweep up to a set point (governed by
      Sawtooth            the Amount setting), after which the cycle immediately starts over.
      Sawtooth            This produces a “ramp down” cycle, the same as above but inverted.
      Square              This produces cycles that abruptly changes between two values, usable for trills etc.
      Random              Produces random stepped modulation to the destination. Some vintage analog synths called this feature “sample & hold”.
      Soft Random         The same as above, but with smooth modulation.

      Destination
      The available LFO Destinations are as follows:

      | Destination       | Description
      Osc                  Selecting this makes LFO control the pitch (frequency) of the REX file.
      Filter               Selecting this makes the LFO control the filter frequency.
      Pan                  Selecting this makes the LFO modulate the pan position of the REX file, i.e. it will move the sound from
                           left to right in the stereo field.

      Sync
      By clicking the SYNC button you activate/deactivate LFO sync. The frequency of the LFO will then be synchronized
      to the song tempo, in one of 16 possible time divisions. When sync is activated, the Rate knob (see below) is used for
      setting the desired time division.

      Turn the knob and check the tooltip for an indication of the time division.

      Rate
      The Rate knob controls the LFO’s frequency. Turn clockwise for a faster modulation rate.

      Amount
      This parameter determines to what degree the selected parameter destination will be affected by the LFO 1, i.e. the
      amount of vibrato, filter wah or auto-panning.

      Pitch Bend Range

      The Pitch Bend Range parameter sets the amount of pitch bend when the wheel is turned fully up or down. The max-
      imum range is 24 semitones (=up/down 2 Octaves).

      Setting number of voices - polyphony

      This determines the polyphony, i.e. the number of voices, or slices, Dr. Octo Rex can play simultaneously. For normal
      loop playback, it is worth noting that slices sometimes “overlap”. Therefore, it is recommended that you use a polyph-
      ony setting of about 3-4 voices when playing REX files. If you are “playing” slices via MIDI, the polyphony setting
      should be set according to how many overlapping slices you want to have.
      !   Note that the Polyphony setting does not “hog” voices. For example, if you are playing a file that has a polyph-
          ony setting of ten voices, but the file only uses four voices, this doesn’t mean that you are “wasting” six voices.
          In other words, the polyphony setting is not something you need to consider if you want to conserve CPU
          power - it is only the number of voices actually used that counts.

      Audio Quality settings
      Dr. Octo Rex features two parameters that provide ways of balancing audio quality vs. conservation of computer
      power. The parameters are called “High Quality Interpolation” and “Low Bandwidth” and are located to the right on
      the rear panel:

      High Quality Interpolation
      When High Quality Interpolation is active, the loop file playback is calculated using a more advanced interpolation al-
      gorithm. This results in better audio quality, especially for loops with a lot of high frequency content.
      • High Quality Interpolation uses more computer power - if you don’t need it, it’s a good idea to turn it off.
          Listen to the loop in a context and determine whether you think this setting makes any difference.

      Low Bandwidth
      This will remove some high frequency content from the sound, but often this is not noticeable (this is especially true
      if you have “filtered down” your loop). Activating this mode will save you some extra computer power, if needed.

      Connections

      On the rear panel of Dr. Octo Rex you will find the connectors. The left part of the panel houses a number of CV/Gate
      inputs and outputs. Using CV/Gate is described in “Routing Audio and CV”.

      Modulation Inputs
      These control voltage (CV) inputs (with trim pots), allow you to modulate various Dr. Octo Rex parameters from other
      devices (or from the modulation outputs of the Dr. Octo Rex device itself). The following CV inputs are available:
      • Master Volume
      • Mod Wheel
      • Pitch Wheel
      • Filter Cutoff
      • Filter Resonance
      • Osc Pitch

      Modulation Outputs
      The Modulation outputs can be used to voltage control other devices, or other parameters in the Dr. Octo Rex device
      itself. The Modulation Outputs are:
      • Filter Envelope
        The Filter Envelopes in Dr. Octo Rex are polyphonic (one per voice). Only the filter envelope of voice 1 is output
        here.
      • LFO

      Gate Inputs
      These inputs can receive a CV/gate signal to trigger the two envelopes. Note that connecting to these inputs will
      override the “normal” triggering of the envelopes. For example, if you connected an LFO CV output on another device
      to the Gate Amp input on the Dr. Octo Rex, the amplitude envelope would not be triggered by the incoming MIDI
      notes to the Dr. Octo Rex device, but by the LFO CV signal. In addition you would only hear the LFO triggering the en-
      velope for the slices that were playing at the moment of the trigger.
      • Amp Envelope
      • Filter Envelope

      Gate Output
      This outputs a gate signal for each triggered slice in the loop.

      Slice Outputs
      To the right of the modulation inputs and outputs are the eight individual slice audio outputs. You can assign individ-
      ual slices to any of these outputs as described in “Editing in the Waveform Display”.

      Main Outputs
      To the right are the main left and right audio outputs. When you create a new Dr. Octo Rex device, these are auto-
      routed to the first available channel on the audio mixer.


---

<a id="europa-shapeshifting-synthesizer-30"></a>

=== END OF PART ===
