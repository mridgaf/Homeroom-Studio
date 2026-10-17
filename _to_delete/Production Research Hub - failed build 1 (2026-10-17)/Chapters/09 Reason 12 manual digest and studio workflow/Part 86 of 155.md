# Chapter 09: Reason 12 manual digest and studio workflow
## Part 86 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 77 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 87 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 77 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Envelopes - General
      Envelope generators are used to control several important sound parameters in analog synthesizers, such as pitch,
      volume, filter frequency etc. Envelopes govern how these parameters should respond over time - from the moment a
      note is struck to the moment it is released.
      Standard synthesizer envelope generators have four parameters; Attack, Decay, Sustain and Release (ADSR).
      There are three envelope generators in the Subtractor, one for volume, one for the Filter 1 frequency, and one mod-
      ulation envelope which has selectable modulation destinations.
         Level

                                                                 Sustain
                                                                 (level)

                                                                                               Time
                      Attack             Decay                                 Release
                      (time)             (time)                                (time)

      Key Down                                                                  Key Up
      The ADSR envelope parameters.

      Attack
      When you play a note on your keyboard, the envelope is triggered. This means it starts rising from zero to the maxi-
      mum value. How long this should take, depends on the Attack setting. If the Attack is set to “0”, the maximum value
      is reached instantly. If this value is raised, it will take time before the maximum value is reached.
      For example, if the Attack value is raised and the envelope is controlling the filter frequency, the filter frequency will
      gradually rise up to a point each time a key is pressed, like an “auto-wha” effect.

      Decay
      After the maximum value has been reached, the value starts to drop. How long this should take is governed by the
      Decay parameter.
      If you wanted to emulate the volume envelope of a note played on a piano for example, the Attack should be set to
      “0” and the Decay parameter should be set to a medium value, so that the volume gradually decreases down to si-
      lence, even if you keep holding the key down. Should you want the decay to drop to some other value than zero, you
      use the Sustain parameter.

      Sustain
      The Sustain parameter determines the level the envelope should rest at, after the Decay. If you set Sustain to full
      level, the Decay setting is of no importance since the volume of the sound is never lowered.

      If you wanted to emulate the volume envelope of an organ, you theoretically only really need to use the Sustain pa-
      rameter set to full level, as a basic organ volume envelope instantly goes to the maximum level (Attack “0”) and stays
      there (Decay “0”), until the key is released and the sound instantly stops (Release “0”).
      But often a combination of Decay and Sustain is used to generate envelopes that rise up to the maximum value, then
      gradually decreases to finally land to rest on a level somewhere in-between zero and maximum. Note that Sustain
      represents a level, whereas the other envelope parameters represent times.

      Release
      Finally, we have the Release parameter. This works just like the Decay parameter, except it determines the time it
      takes for the value to fall back to zero after releasing the key.

      Amplitude Envelope

      The Amplitude Envelope is used to adjust how the volume of the sound should change from the time you press a key
      until the key is released. By setting up a volume envelope you sculpt the sound’s basic shape with the four Amplitude
      Envelope parameters, Attack, Decay, Sustain and Release. This determines the basic character of the sound (soft,
      long, short etc.).

      Filter Envelope

      The Filter Envelope affects the Filter 1 Frequency parameter. By setting up a filter envelope you control the how the
      filter frequency should change over time with the four Filter Envelope parameters, Attack, Decay, Sustain and Re-
      lease.

      Filter Envelope Amount
      This parameter determines to what degree the filter will be affected by the Filter Envelope. Raising this knob’s value
      creates more drastic results. The Envelope Amount parameter and the set Filter Frequency are related. If the Filter
      Freq slider is set to around the middle, this means that the moment you press a key the filter is already halfway open.
      The set Filter Envelope will then open the filter further from this point. The Filter Envelope Amount setting affects
      how much further the filter will open.

      Filter Envelope Invert

      If this button is activated, the envelope will be inverted. For example, normally the Decay parameter lowers the filter
      frequency, but after activating Invert it will instead raise it, by the same amount.

      Mod Envelope

      The Mod Envelope allows you to select one of a number of parameters, or Destinations, to control with the envelope.
      By setting up a modulation envelope you control the how the selected Destination parameter should change over
      time with the four Mod Envelope parameters, Attack, Decay, Sustain and Release.
      The available Mod Envelope Destinations are as follows:

      | Destination      | Description
      Osc 1               Selecting this makes the Mod Envelope control the pitch (frequency) of Osc 1.
      Osc 2               Same as above, but for Osc 2.
      Osc Mix             Selecting this makes the Mod Envelope control the oscillator Mix parameter. Both oscillators must be acti-
                          vated for this to have any effect.
      FM                  Selecting this makes the Mod Envelope control the FM Amount parameter. Both oscillators must be acti-
                          vated for this to have any effect.
      Phase               Selecting this makes the Mod Envelope control the Phase Offset parameter for both Osc 1 and 2. Note
                          that Phase Offset Modulation (Subtraction or Multiplication) must be activated for this to have any effect.
      Freq 2              Selecting this makes the Mod Envelope control the Frequency parameter for Filter 2.

      LFO Section

      LFO stands for Low Frequency Oscillator. LFO’s are oscillators, just like Osc 1 & 2, in that they also generate a wave-
      form and a frequency. However, there are two significant differences:
      • LFOs only generate waveforms with low frequencies.
      • The output of the two LFO’s are never actually heard. Instead they are used for modulating various parameters.
      The most typical application of an LFO is to modulate the pitch of a (sound generating) oscillator, to produce vibrato.
      Subtractor is equipped with two LFO’s. The parameters and the possible modulation destinations vary somewhat be-
      tween LFO 1 and LFO 2.

      LFO 1 Parameters
      Waveform
      LFO 1 allows you to select different waveforms for modulating parameters. These are (from top to bottom):

      | Waveform           | Description
      Triangle             This is a smooth waveform, suitable for normal vibrato.
      Inverted Sawtooth    This produces a “ramp up” cycle. If applied to an oscillator’s frequency, the pitch would sweep up to a set point
                           (governed by the Amount setting), after which the cycle immediately starts over.
      Sawtooth              This produces a “ramp down” cycle, the same as above but inverted.
      Square               This produces cycles that abruptly changes between two values, usable for trills etc.
      Random                Produces random stepped modulation to the destination. On some vintage synths, this is called “sample & hold”.
      Soft Random          The same as above, but with smooth modulation.

      Destination
      The available LFO 1 Destinations are as follows:

      | Destination       | Description
      Osc 1&2              Selecting this makes LFO 1 control the pitch (frequency) of Osc 1 and Osc 2.
      Osc 2                Same as above, but for Osc 2.
      Filter Freq          Selecting this makes the LFO 1 control the filter frequency for Filter 1 (and Filter 2 if linked).
      FM                   Selecting this makes the LFO 1 control the FM Amount parameter. Both oscillators must be activated for this to
                           have any effect.
      Phase                Selecting this makes the LFO 1 control the Phase Offset parameter for both Osc 1 and 2. Note that Phase Off-
                           set Modulation (Subtraction or Multiplication) must be activated for this to have any effect.
      Osc Mix              Selecting this makes the LFO 1 control the oscillator Mix parameter.

      Sync
      By clicking this button you activate/deactivate LFO sync. The frequency of the LFO will then be synchronized to the
      song tempo, in one of 16 possible time divisions. When sync is activated, the Rate knob (see below) is used for set-
      ting the desired time division.
      Turn the knob and check the tooltip for an indication of the time division.

      Rate
      The Rate knob controls the LFO’s frequency. Turn clockwise for a faster modulation rate.

      Amount
      This parameter determines to what degree the selected parameter destination will be affected by LFO 1. Raising this
      knob’s value creates more drastic results.

      LFO 2 Parameters
      LFO 2 is polyphonic. This means that for every note you play, an independent LFO cycle is generated, whereas LFO
      1 always modulates the destination parameter using the same “cycle”. This can be used to produce subtle cross-
      modulation effects, with several LFO cycles that “beat” against each other. This also enables LFO 2 to produce mod-
      ulation rates that vary across the keyboard (see the “Keyboard Tracking” parameter below).

      Destination
      The available LFO 2 Destinations are as follows:

      | Destination       | Description
      Osc 1&2              Selecting this makes LFO 2 modulate the pitch (frequency) of Osc 1 and Osc 2.
      Phase                Selecting this makes the LFO 2 modulate the Phase Offset parameter for both Osc 1 and 2. Note that
                           Phase Offset Modulation (Subtraction or Multiplication) must be activated for this to have any effect.
      Filter Freq 2        Selecting this makes the LFO 2 modulate the filter frequency for Filter 2.
      Amp                  Selecting this makes the LFO 2 modulate the overall volume., to create tremolo-effects.

      LFO 2 Delay
      This parameter is used to set a delay between when a note is played and when the LFO modulation “kicks in”. For ex-
      ample, if Osc 1 & 2 is selected as the destination parameter and Delay was set to a moderate value, the sound would
      start out unmodulated, with the vibrato only setting in if you hold the note(s) long enough. Delayed LFO modulation
      can be very useful, especially if you are playing musical instrument-like sounds like violin or flute. Naturally it could
      also be used to control more extreme modulation effects and still retain the “playability” of the sound.

      LFO 2 Keyboard Tracking
      If LFO keyboard tracking is activated, the LFO rate will progressively increase the higher up on the keyboard you play.
      Raising this value creates more drastic results.

      q   If the LFO is set to modulate the phase offset, LFO keyboard tracking can produce good results. For example,
          synth string pads and other sounds that use PWM (see “Phase Offset Modulation”) can benefit from this.

      Rate
      The Rate knob controls the LFO’s frequency. Turn clockwise for a faster modulation rate.

      Amount
      This parameter determines to what degree the selected parameter destination will be affected by LFO 2. Raising this
      knob’s value creates more drastic results.

      Play Parameters
      This section deals with two things: Parameters that are affected by how you play, and modulation that can be applied
      manually with standard MIDI keyboard controls.
      These are:
      • Velocity Control
      • Pitch Bend and Modulation Wheel
      • Legato
      • Portamento
      • Polyphony

      Velocity Control

      Velocity is used to control various parameters according to how hard or soft you play notes on your keyboard. A com-
      mon application of velocity is to make sounds brighter and louder if you strike the key harder. Subtractor features
      very comprehensive velocity modulation capabilities. By using the knobs in this section, you can control how much the
      various parameters will be affected by velocity. The velocity sensitivity amount can be set to either positive or negative
      values, with the center position representing no velocity control.

      The following parameters can be velocity controlled:

      | Destination      | Description
      Amp                 This let’s you velocity control the overall volume of the sound. If a positive value is set, the volume will in-
                          crease the harder you strike a key. A negative value inverts this relationship, so that the volume decreases
                          if you play harder, and increases if you play softer. If set to zero, the sound will play at a constant volume,
                          regardless of how hard or soft you play.
      FM                  This sets velocity control for the FM Amount parameter. A positive value will increase the FM amount the
                          harder you play. Negative values invert this relationship.
      M. Env              This sets velocity control for the Mod Envelope Amount parameter. A positive value will increase the enve-
                          lope amount the harder you play. Negative values invert this relationship.
      Phase               This sets velocity control for the Phase Offset parameter. This applies to both Osc 1 & 2, but the relative
                          offset values are retained. A positive value will increase the phase offset the harder you play. Negative val-
                          ues invert this relationship.
      Freq 2              This sets velocity control for the Filter 2 Frequency parameter. A positive value will increase the filter fre-
                          quency the harder you play. Negative values invert this relationship.
      F. Env              This sets velocity control for the Filter Envelope Amount parameter. A positive value will increase the en-
                          velope amount the harder you play. Negative values invert this relationship.
      F. Dec              This sets velocity control for the Filter Envelope Decay parameter. A positive value will increase the Decay
                          time the harder you play. Negative values invert this relationship.
      Osc Mix             This sets velocity control for the Osc Mix parameter. A positive value will increase the Osc 2 Mix amount
                          the harder you play. Negative values invert this relationship.
      A. Attack           This sets velocity control for the Amp Envelope Attack parameter. A positive value will increase the Attack
                          time the harder you play. Negative values invert this relationship.

      Pitch Bend and Modulation Wheels

      The Pitch Bend wheel is used for “bending” notes, like bending the strings on a guitar. The Modulation wheel can be
      used to apply various modulation while you are playing. Virtually all MIDI keyboards have Pitch Bend and Modulation
      controls. Subtractor features not only the settings for how incoming MIDI Pitch Bend and Modulation wheel mes-
      sages should affect the sound. Subtractor also has two functional wheels that could be used to apply real time mod-
      ulation and pitch bend should you not have these controllers on your keyboard, or if you aren’t using a keyboard at all.
      The Subtractor wheels mirror the movements of the MIDI keyboard controllers.

      Pitch Bend Range
      The Range parameter sets the amount of pitch bend when the wheel is turned fully up or down. The maximum range
      is “24” (=up/down 2 Octaves).

      Modulation Wheel
      The Modulation wheel can be set to simultaneously control a number of parameters. You can set positive or negative
      values, just like in the Velocity Control section. The following parameters can be affected by the modulation wheel:

      | Parameter           | Description
      F. Freq               This sets modulation wheel control of the Filter 1 Frequency parameter. A positive value will increase the
                            frequency if the wheel is pushed forward. Negative values invert this relationship.
      F. Res                This sets modulation wheel control of the Filter 1 Resonance parameter. A positive value will increase the
                            resonance if the wheel is pushed forward. Negative values invert this relationship.
      LFO 1                 This sets modulation wheel control of the LFO 1 Amount parameter. A positive value will increase the
                            Amount if the wheel is pushed forward. Negative values invert this relationship.
      Phase                 This sets modulation wheel control of the Phase Offset parameter for both Osc 1 and 2. Note that Phase
                            Offset Modulation (Subtraction or Multiplication) must be activated for this to have any effect.
      FM                    This sets modulation wheel control of the FM Amount parameter. A positive value will increase the FM
                            amount if the wheel is pushed forward. Negative values invert this relationship. Both oscillators must be
                            activated for this to have any effect.

      Legato
      Legato works best with monophonic sounds. Set Polyphony (see below) to 1 and try the following:
      D   Hold down a key and press another key without releasing the previous.
          Notice that the pitch changes, but the envelopes do not start over. That is, there will be no new “attack”.
      D   If polyphony is set to more voices than 1, Legato will only be applied when all the assigned voices are “used
          up”.
          For example, if you had a polyphony setting of “4” and you held down a 4 note chord, the next note you played
          would be Legato. Note, however, that this Legato voice will “steal” one of the voices in the 4 note chord, since all
          the assigned voices were already used up!

      Retrig
      This is the “normal” setting for playing polyphonic patches. That is, when you press a key without releasing the previ-
      ous, the envelopes are retriggered, like when you release all keys and then press a new one. In monophonic mode,
      Retrig has an additional function; if you press a key, hold it, press a new key and then release that, the first note is
      also retriggered.

      Portamento (Time)
      Portamento is when the pitch “glides” between the notes you play, instead of instantly changing the pitch. The Porta-
      mento knob is used to set how long it takes for the pitch to glide from one pitch to the next. If you don’t want any Por-
      tamento at all, set this knob to zero.

      Setting Number of Voices - Polyphony

      This determines the polyphony, i.e. the number of voices a Subtractor Patch can play simultaneously. This can be
      used to make a patch monophonic (=a setting of “1”), or to extend the number of voices available for a patch. The
      maximum number of voices you can set a Subtractor Patch to use is 99. In the (unlikely) event you should need more
      voices, you can always create another Subtractor!
      !     Note that the Polyphony setting does not “hog” voices. For example, if you have a patch that has a polyphony
            setting of ten voices, but the part the patch plays only uses four voices, this won’t mean that you are “wasting”
            six voices. In other words, the polyphony setting is not something you need to consider much if you want to
            conserve CPU power - it is the number of voices actually used that counts.

      About the Low Bandwidth button
      This can be used to conserve CPU power. When activated, this function will remove some high frequency content
      from the sound of this particular device, but often this is not noticeable (this is especially true for bass sounds).

      External Modulation

      Subtractor can receive common MIDI controller messages, and route these to various parameters. The following MIDI
      messages can be received:
      • Aftertouch (Channel Pressure)
      • Expression Pedal
      • Breath Control
      If your MIDI keyboard is capable of sending Aftertouch messages, or if you have access to an Expression Pedal or a
      Breath controller, you can use these to modulate parameters. The “Ext. Mod” selector switch sets which of these
      message-types should be received.
      These messages can then be assigned to control the following parameters:

      | Destination          | Description
          F. Freq             This sets External modulation control of the Filter 1 Frequency parameter. A positive value will increase
                              the frequency with higher external modulation values. Negative values invert this relationship.
          LFO 1               This sets External modulation control of the LFO 1 Amount parameter. A positive value will increase the
                              LFO 1 amount with higher external modulation values. Negative values invert this relationship.

      | Destination         | Description
          Amp               This let’s you control the overall volume of the sound with external modulation. If a positive value is set,
                            the volume will increase with higher external modulation values. A negative value inverts this relation-
                            ship.
          FM                This sets External modulation control of the FM Amount parameter. If a positive value is set, the FM
                            amount will increase with higher external modulation values. A negative value inverts this relationship.
                            Both oscillators must be activated for this to have any effect.

      Connections

      Flipping the Subtractor around reveals a plethora of connection possibilities, most of which are CV/Gate related. Us-
      ing CV/Gate is described in the chapter “Routing Audio and CV”.

      Audio Output
      This is Subtractor’s main audio output. When you create a new Subtractor device, this is auto-routed to the first avail-
      able channel on the audio mixer.

      Sequencer Control
      The Sequencer Control CV and Gate inputs allow you to play the Subtractor from another CV/Gate device (typically
      a Matrix or a Redrum). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers
      note on/off along with velocity.
      !    For best results, you should use the Sequencer Control inputs with monophonic sounds.

      Modulation Inputs
      !   Remember that CV connections will not be stored in the Subtractor patch, even if the connections are to/from
          the same Subtractor device!
      These control voltage (CV) inputs (with associated voltage trim pots), can modulate various Subtractor parameters
      from other devices, or from the modulation outputs of the same Subtractor device. These inputs can control the fol-
      lowing parameters:
      • Oscillator Pitch (both Osc 1 & 2).
      • Oscillator Phase Offset (both Osc 1 & 2).
      • FM Amount
      • Filter 1 Cutoff
      • Filter 1 Res
      • Filter 2 Cutoff
      • Amp Level
      • Mod Wheel

      Modulation Outputs
      The Modulation outputs can be used to voltage control other devices, or other parameters in the same Subtractor de-
      vice. The Modulation Outputs are:
      • Mod Envelope
      • Filter Envelope
      • LFO 1

      Gate Inputs
      These inputs can receive a CV signal to trigger the following envelopes. Note that connecting to these inputs will
      override the normal triggering of the envelopes. For example, if you connected an LFO output to the Gate Amp input,
      you would not trigger the amp envelope by playing notes, as this is now controlled by the LFO. In addition you would
      only hear the LFO triggering the envelope for the notes that you hold down. The following Gate Inputs can be se-
      lected:
      • Amp Envelope
      • Filter Envelope
      • Mod Envelope


---

<a id="malstr-m-synthesizer-35"></a>

=== END OF PART ===
