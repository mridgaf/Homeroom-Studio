# Chapter 09: Reason 12 manual digest and studio workflow
## Part 88 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 79 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 89 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 79 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Routing
      The Malström puts you in total control of how the signal should be routed from the oscillators, through the filters and
      on to the outputs. Below is first a general description of the routing options, followed by examples of how to route the
      signal in order to achieve a certain result.
      D   Click on a button so that it is lit, to route the signal correspondingly.
          See below for descriptions.
      If this button is lit, the signal from osc:A is routed to filter:A via the shaper. If neither this nor the other routing
      button from osc:A (to filter:B) is lit, the signal will go straight to the outputs.

      If this button is lit, the signal from osc:A is routed
      to filter:B. If neither this nor the other routing
      button from osc:A (to filter:A/shaper) is lit, the
      signal from osc:A will go straight to the outputs.

      If this button is lit, the signal from osc:B is
      routed to filter:B. If this is not lit, the signal from
      osc:B will go straight to the outputs.

                         If this button is lit, the signal from filter:B is routed to filter:A via the shaper. The signal from
                         filter:B can originate from either osc:A, osc:B or both. If this is not lit, the signal from filter:B
                         will go straight to the outputs.

      !   Note that the result depends both on the routing buttons and on whether the filters and shaper are activated or
          not!

897        MALSTRÖM SYNTHESIZER

      Routing examples
      One or both oscillators without filters

      With this configuration, the signals from the oscillators will bypass the filters and the shaper and go directly to the re-
      spective output. Using both oscillators allows you to use the Spread parameter to create a true stereo sound.

      One or both oscillators to one filter only

      Both oscillators routed to filter:B only.                Both oscillators routed to filter:A only.
      With these configurations, the signal from osc:A and/or osc:B will go to either filter:A or filter:B and then to the out-
      puts. This is essentially a mono configuration and hence Spread should probably be set to “0”.

898        MALSTRÖM SYNTHESIZER

      Both oscillators to one filter each

      With this configuration, the signals from osc:A and osc:B will go to filter:A and filter:B respectively, and then to the
      outputs.
      Again, this configuration allows you to work in true stereo.

      Oscillator A to both filters in parallel

      With this configuration, the signal from osc:A will go to both filter:A and filter:B, with the filters in parallel.
      !   This configuration is only possible with osc:A. Osc:B can be routed to both filters as well, but only in series
          (see below).

899        MALSTRÖM SYNTHESIZER

      One or both oscillators with both filters in series

      Osc:A routed through both filters in series.                        Osc:B routed through both filters in series.
      With these configurations, the signal from osc:A and/or osc:B will go to both filter:A and filter:B, with the filters in se-
      ries (one after the other).

      Adding the shaper
      The signal from one or both oscillators can also be routed to the shaper. The signal will then pass through the shaper
      to the outputs, with or without also passing through the filters.

      In the left figure, the signal from osc:A is routed to the shaper and then directly to the outputs. In the right figure, the signal from osc:B is
      routed to filter:B, then to the shaper and then to filter:A.

900        MALSTRÖM SYNTHESIZER

      The output controls

      These two parameters control the output from the Malström in the following way:

      Volume
      This knob controls the master volume out from the Malström.

      Spread
      This controls the stereo pan-width of the outputs from Osc:A/B and Filter:A/B respectively. The farther to the right
      you turn the knob, the wider the stereo image will be. In other words, the signals will be panned further apart to the
      left and right.
      !   If you are only using one output (A or B), it is strongly recommended that you set Spread to “0”.

      The play controls

      To the far left on the Malström’s “control panel” are various parameters that are affected by how you play, and lets you
      apply modulation by MIDI controls. The following is a description of these controls.

901        MALSTRÖM SYNTHESIZER

      Polyphony - setting the number of voices

      This lets you set the polyphony for the Malström. Polyphony is the number of voices it can play simultaneously. The
      maximum number is 16 and the minimum is 1, in which case the Malström will be monophonic.
      !   The number of voices you can play depends of course on the capacity of your computer. Even though the max-
          imum number is 16 it doesn’t necessarily mean that your system is capable of using that many voices. Also
          note that voices do not consume CPU capacity unless they are really “used”. That is, if you are using a patch
          that plays two voices but have polyphony set to four, the two “unused” voices do not consume any of your sys-
          tem resources.

      Porta (portamento)

      This is used for controlling portamento. This is a parameter that makes the pitch glide between the notes you play,
      rather than changing the pitch instantly as soon as you hit a key on your keyboard. By turning this knob you set how
      long it should take for the pitch to glide from one note to the next as you play them.
      With the knob turned all the way to the left, portamento is disabled.

      Legato

      By clicking this button you activate/deactivate Legato. Legato in Malström is unique in that it allows you to control
      whether the sound is monophonic or polyphonic by using your playing style:
      D   If you play legato (hold down a key and then press another key without releasing the previous), the sound is
          monophonic.
          Also note that the pitch changes, but the envelopes do not start over. That is, there will be no new “attack”.
      D   If you play non-legato (separated notes), with polyphony set to more voices than 1, each note will decay sepa-
          rately (polyphonic).
          This will be most apparent with longer release times.

902        MALSTRÖM SYNTHESIZER

      The Pitch Bend and Modulation wheels

      • The Pitch Bend wheel is used for bending the pitch of notes, much like bending the strings on a guitar or other
        string instrument.
      • The Modulation wheel can be used for applying modulation while you are playing.
      Virtually all MIDI keyboards have Pitch Bend and Modulation controls. The Malström does not only feature the set-
      tings for how incoming MIDI Pitch Bend and Modulation wheel messages should affect the sound, but also two func-
      tional wheels that can be used for applying real time modulation and pitch bend if you don’t have these controllers on
      your keyboard, or if you aren’t using a keyboard at all. The wheels on the Malström also mirror the movements of the
      wheels on your MIDI keyboard.

      Pitch Bend Range
      The Range parameter sets the maximum amount of pitch bend, i.e. how much it is possible to change the pitch by
      turning the wheel fully up or down. The maximum range is 24 semitones (2 Octaves). You change the value by click-
      ing the spin controls to the right of the display.

      The Velocity controls

      Velocity is used for controlling various parameters according to how hard or soft you play notes on your keyboard. A
      typical use of velocity control is to make sounds brighter and louder if you strike a key harder. By using the knobs in
      this section, you can control how much the various parameters will be affected by velocity.
      !   All of the velocity control knobs are bi-polar, which means that the amount can be set to either positive or neg-
          ative values, while keeping the knobs in the center position means that no velocity control is applied.
      The following parameters can be velocity controlled:
      • Lvl:A
          This lets you velocity control the output level of osc:A.
      • Lvl:B
          This lets you velocity control the output level of osc:B.

903        MALSTRÖM SYNTHESIZER

      • F.env
          This sets velocity control for the Filter Envelope Amount parameter. Positive values will increase the envelope
          amount the harder you play, and negative values will decrease the amount.
      • Atk (attack)
          This sets velocity control for the Amp Envelope Attack parameter of osc:A and/or osc:B. Positive values will in-
          crease the Attack time the harder you play, and negative values will decrease it.
      • Shift
          This lets you velocity control the Shift parameter of osc:A and/or osc:B.
      • Mod
          This lets you velocity control all modulation amounts of mod:A and/or mod:B.
      !   Note that you can set the last three parameters (Atk, Shift and Mod) to be velocity controlled for either or both
          of oscillator/modulator A and B. This is done with the A/B selector switch.

      The Modulation wheel controls

      The Modulation wheel can be set to control a number of parameters. You can set positive or negative values, just like
      in the Velocity Control section (see above).
      The following parameters can be affected by the modulation wheel:
      • Index
          This sets modulation wheel control of the currently active graintable’s index (see “Controlling playback of the
          graintable”) for osc:A and/or osc:B. Positive values will move the index position forwards if the modulation wheel
          is pushed forward. Negative values will move it backwards.
      • Shift
          This sets modulation wheel control of the Shift parameter of osc:A and/or osc:B (see “Controlling playback of the
          graintable”).
      • Filter
          This sets modulation wheel control of the Filter Frequency
          parameter (see “Filter controls”). Positive values will raise the frequency if the
          wheel is pushed forward and negative values will lower the frequency.
      • Mod
          This sets modulation wheel control of the total amount of modulation from mod:A and/or mod:B. Positive values
          will increase the settings if the wheel is pushed forward and negative values will decrease the settings.
      !   You can set whether these parameters on either or both oscillator/modulator/filter A and B will be affected by
          the modulation wheel. This is done with the A/B selector switch.

904        MALSTRÖM SYNTHESIZER

      Connections

      Flipping the Malström around reveals a wide array of connection possibilities. Most of these are CV/Gate related. Us-
      ing CV/Gate is described in the chapter “Routing Audio and CV”.

      Audio Output
      These are the Malström’s audio outputs. When you create a new Malström device, they are auto-routed to the first
      available channel on the audio mixer:
      • Shaper/Filter:A (left) & Filter:B (right)
          These are the main stereo outputs. Each of the two filters are connected to a separate output, and by connecting
          both, you can have stereo output. Whether the output really will be in stereo however, is determined by the routing
          and the Spread parameter. See “Routing” for details about this.
      • Osc:A & osc:B
          These make it possible to output the sound directly after the Amp Envelope of each oscillator, bypassing the filter
          section. Connecting one or both of these to a channel on the audio mixer will break the Malström’s internal signal
          chain. That is, it is not possible to process the sound by using the filters and the shaper of the Malström. the sound
          instead goes directly to the mixer.
      q   Note also that you can connect the outputs Osc:A & Osc:B to the Audio Inputs on the Malström for some inter-
          esting effects - see “Routing external audio to the filters”.

      Audio Input
      • Shaper/Filter:A
      • Filter:B
      These inputs let you connect either other audio sources, or the Malström’s own internal signal directly to the filters
      and the shaper - see “Routing external audio to the filters”.

      Sequencer Control
      The Sequencer Control CV and Gate inputs allow you to play the Malström from another CV/Gate device (typically a
      Matrix or a Redrum). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note
      on/off along with velocity.
      !   For best results, you should use the Sequencer Control inputs with monophonic sounds.

905        MALSTRÖM SYNTHESIZER

      Gate Input
      These inputs can receive a CV signal to trigger the following envelopes:
      • Amp Envelope
      • Filter Envelope
      !   Note that connecting to these inputs will override the normal triggering of the envelopes. For example, if you
          connected a Modulation output to the Gate Amp in-put, you would not trigger the amp envelope by playing
          notes, as this is now controlled by the Modulator. In addition you would only hear the Modulator triggering the
          envelope for the notes that you hold down.

      Modulation Input
      These control voltage (CV) inputs (with associated voltage trim pots and A/B selector switches), can modulate vari-
      ous Malström parameters from other devices, or from the modulation outputs of the same Malström device. These in-
      puts can control the following parameters:
      • Oscillator Pitch
      • Filter Frequency
      • Oscillator Index offset
      • Oscillator Shift
      • Amp Level
      • Mod Amount
      • Mod Wheel

      Modulation Output
      The Modulation outputs can be used to voltage control other devices, or other parameters in the same Malström de-
      vice.
      The Modulation Outputs are:
      • Mod:A
      • Mod:B
      • Filter Envelope

906        MALSTRÖM SYNTHESIZER

      Routing external audio to the filters

      The audio inputs on the back of the Malström allows you to connect any audio signal to the filters and Shaper.
      To use this feature, it’s important to understand the following background:
      Normally the Malström behaves like any regular polyphonic synthesizer, in that each voice has its own filter. The filter
      settings are the same, but each filter envelope is triggered individually when you play a note.
      However, when you connect a signal to the audio inputs, it is routed to an “extra” filter. The envelope for this filter is
      triggered each time any of the other filter envelopes is triggered. In other words, the “extra” filter envelope is triggered
      each time you play a note on the Malström.
      There are two different uses for the audio inputs:

      Connecting an external signal source
      Connecting an audio signal from another device in the rack to the audio input allows you to process the signal
      through the filters and/or Shaper of the Malström. The processed signal will then be mixed with the Malström’s “own”
      voices (if activated) and sent to the outputs.
      The result depends on the following:
      • To which jack you connect the signal.
      • Whether the filters and/or Shaper are activated on the front panel.
      • The routing button for filter:B.
        If this is activated and you connect a signal to the Filter:B input, the signal will be processed in filter:B and then
        sent to the Shaper and filter:A (just as when routing Malström’s own oscillators on the front panel).
      Note again that the filter envelope is triggered by all voices. To make use of the filter envelope, you either need to
      play the Malström or use gate signals to trigger it or the filter envelope, separately.

907       MALSTRÖM SYNTHESIZER

      Connecting the signals from the Malström itself

      If you connect one or both oscillator outputs to the audio input(s), the internal signal path from the oscillators to the
      filters is broken. In other words, no signals will pass internally from the oscillators to the filters, and the three routing
      buttons for the oscillators are ignored.
      This may seem pointless at first, but there are several uses for this:
      D   When you play the Malström in this mode, the filter envelope will be triggered for each note you play, affecting
          all sounding notes.
          This is due to the monophonic “extra” filter described above. On older synthesizers, this feature is called “Multiple
          triggering”.
      D   Since all notes you play are mixed before being sent into the filter, the result of using the Shaper will be totally
          different (if you play more than one note at a time).
          This is similar to playing a guitar chord through a distortion effect, for example.
      D   You can patch in external effects between the oscillators and the filters.
          Just connect an oscillator output to the input of the effect device, and the effect output to the Malströms’s audio
          input.
      q   You can use combinations of connections and routing. You could for instance connect an external audio signal
          to one of the inputs, one of the Malström’s oscillators to the other input and then use the routing options on
          the front panel for the other oscillator. All of these signals will then be mixed and sent to the Malström’s main
          outputs.

908        MALSTRÖM SYNTHESIZER


---

<a id="monotone-bass-synthesizer-36"></a>

=== END OF PART ===
