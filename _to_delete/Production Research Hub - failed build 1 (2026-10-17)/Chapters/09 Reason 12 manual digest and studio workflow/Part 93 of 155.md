# Chapter 09: Reason 12 manual digest and studio workflow
## Part 93 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 84 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 94 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 84 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 40: Klang Tuned Percussion

Klang
Tuned Percussion

      Introduction

      The Klang Tuned Percussion instrument features an assortment of high-quality multi-sampled tuned percussion in-
      struments - perfect for any music style. Each of the multi-sampled instruments can also be tailored and processed in
      the high-quality filter, amp, delay and reverb sections.

      Panel overview
      The Klang front panel contains the following sections:

                                             1                                                2

                            3               4                   5               6             7             8

      The Klang front panel sections.
      • 1. Patch Selector (for browsing, loading and saving patches).
      • 2. Master Volume.
      • 3. Global performance and “play” controls.
      • 4. Instruments section.
      • 5. Filter section.
      • 6. Amp Envelope section.
      • 7. Delay effect section.
      • 8. Reverb effect section.

      Using Klang
      Loading and saving patches

      Loading and saving patches is done in the same way as with any other internal Reason device, see “Loading patches”
      and “Saving patches” for details.

      Global performance and “play” controls

      Note
      The Note LED lights up each time Klang receives a MIDI Note On.

      Range
      D   Set the desired Pitch Bend range for the “Pitch” wheel with the up/down buttons, or by click-holding on the
          display and dragging up/down.
          Range: +/-12 semitones (+/-1 octave) in steps of +/-1 semitone.

      Pitch
      The Pitch bend wheel can be used for bending note pitches up and down. Klang also responds to Pitch Bend MIDI
      data from a connected MIDI master keyboard. You set the desired Pitch bend Range with the “Range” control to the
      right of the Mod wheel.

      Mod
      The Mod wheel can be used for controlling the three predefined parameters to the right of the Mod wheel:
      • S. Start
          Here you set how/if the Mod wheel should affect the Sample Start position of the currently selected instrument.
          The parameter is bi-polar, with zero modulation at the 12 o’clock position. A negative value moves the sample start
          back and a positive value moves it forward.
      !   Note that if the S.Start parameter in the Instruments section (see “S. Start (Sample Start)”) is at 0 ms, the sam-
          ple start cannot be moved back any further. Similarly, if the S.Start parameter in the Instruments section is at
          150 ms, the sample start cannot be moved forward any further.
      • F. Freq
          Here you set how/if the Mod wheel should affect the Filter Cutoff parameter. The parameter is bi-polar, with zero
          modulation at the 12 o’clock position.

      !   Note that if the Cutoff parameter in the Filter section (see “Cutoff”) is at 20 Hz, the frequency cannot be low-
          ered any further. Similarly, if the Cutoff parameter in the Filter section is at 25 kHz, the frequency cannot be
          raised any further.
      • Level
          Here you set how/if the Mod wheel should affect the Master Volume parameter. The parameter is bi-polar, with
          zero modulation at the 12 o’clock position.
      !   The volume can never be modulated louder than the maximum +12 dB limit of the Master Volume control.

      Panel controls
      The Instruments section

      Instrument selector

      D   Click the Instrument name selector to bring up a menu of the available instruments - and then select the de-
          sired instrument from the menu.
          Alternatively, click and drag up/down in the display above the selector to scroll through the instruments.
      !   Depending on the instrument size (in MB), it could take a short moment before the entire instrument is loaded
          into RAM.
      !   Also note that the note ranges of the instruments extend outside their “natural” ranges, which could produce
          nice artificial effects.
      The available instruments are:

      • Alto Glockenspiel

        The Alto Glockenspiel was played with hard mallets and was recorded with close mics (stereo) in a large hall,
        slightly wet. The samples were taken from Soundiron's Alto Glockenspiel library.
      • Bamblong

        This instrument is also known as a bamboo log drum, from Indonesia. It was played with rubber mallets and was re-
        corded with close mics (stereo) in a studio, dry. The samples were taken from Soundiron's Bamblong library.
      • Circle Bells Mallet

        This instruments is also known as Blossom Bells. It was played with rubber mallets and was recorded with close
        mics (stereo) in a studio, dry. The samples were taken from Soundiron's Circle Bells library.

      • Cylindrum

        This is an experimental instrument built from large diameter plastic piping, also known as a tubulum. It was played
        with rubber paddle mallets and was recorded with close mics (stereo) in a studio, dry. The samples were taken
        from Soundiron's Cylindrum library.
      • Imbibaphones

        These are wine glasses played with rubber mallets. They were recorded with close mics (stereo) in a studio, dry.
        The samples were taken from Soundiron's "Imbibaphones" library.
      • Kalimba

        The Kalimba is also known as an mbira or thumb piano, from Africa. It was recorded with close mics (stereo) in a
        studio, dry. The samples were taken from Soundiron's Kalimba library.

      • Music Box

        This is a music box recorded with close mics (stereo) in a studio, dry. The samples were taken from Soundiron's
        Musique Box library.
      • Noah Bells

        The Noah Bells from India are played with the fingertips and were recorded with close mics (stereo) in a large hall,
        slightly wet. The samples were taken from Soundiron's Noah Bells library.
      • Steel Tones

        This instrument is also known as a hank drum or propane drum. It was played with felt mallets and was recorded
        with close mics (stereo) in a room, dry. The samples were taken from Soundiron's Steel Tones library.

      • Whale Drum

          The whale drum is a wooden box slit drum from Africa. It was played with rubber mallets and was recorded with
          close mics (stereo) in a studio, dry. The samples were taken from Soundiron's Whale Drum library.

      S. Start (Sample Start)

      D   Turn the S.Start knob to set where in the sample the playback should start.
          Note that the effect could be different depending on the selected instrument.

      Oct

      D   Set the octave transposition for the instrument.
          Range: 5 (+/-2) octaves.
      !   Note that the note ranges of the instruments can be transposed far outside their “natural” ranges, which could
          produce nice artificial effects.

      Semi

      D   Set the pitch in semitone steps.
          Range: +/-12 semitones (two octaves).

      Fine

      D   Set the pitch in steps of 1 cent.
          Range: +/- 50 cents (down or up half a semitone).

      The Filter section

      Filter On/Off

      D   Click the On/Off LED button to switch on/off the Filter section.

      Filter Type selector

      D   Click and drag up/down on the Filter Type selector to select one of the available filter types - or step through
          the filter types by clicking the Up/Down arrow buttons.
          The available filter types are:
      • LP
          This is a lowpass filter with 12db/octave slope.
      • HP
          This is a highpass filter with 12db/octave slope.
      • BP
          This is a bandpass filter with 6db/octave slopes.
      • Comb
          This is a comb filter for phaser/flanger type of effects.

      Cutoff

      D   Set the cutoff/center frequency with the Cutoff knob.
          The cutoff parameter sets where in the frequency range you want the resonance and attenuation to appear.
          Range: 20 Hz to 25 kHz.

      Reso

      D   Set the resonance amount with the Reso knob.
          The resonance parameter amplifies the frequencies at, and around the cutoff/center frequency.

      Env

      D   With the Env knob you set how much you want the Filter Envelope (see below) to affect the Cutoff frequency.
          Range: 0% to 100%.

      Filter Envelope

      The standard ADSR type envelope controls the filter cutoff frequency modulation over time. The ADSR envelope
      characteristics are described in detail in “Amp Envelope”.

      Vel

      D   Turn the Vel knob to set how much the cutoff/center frequency should be modulated by Keyboard Velocity.
          Range: 0% to 100%.

      Kbd

      D   Turn the KBD (Keyboard Track) knob to set how much the cutoff/center frequency should track incoming MIDI
          Notes.
          Range: 0% (no tracking (constant frequency)) to 100% (1 semitone per key).

      The Amp section

      Vel

      D   Turn the Vel knob to set how much the amplitude should be modulated by Keyboard Velocity.
          Range: 0% to 100%.

      Amp Envelope

      The Amp Envelope is a standard ADSR envelope which controls the amplitude of the signal over time. The picture
      below shows the various stages of the ADSR envelope:

      The ADSR envelope stages.
      • A(ttack)
          When you play a note on your keyboard, the envelope is triggered. This means it starts rising from zero to the value
          set with the Master Volume knob. How long this should take, depends on the Attack setting. If the Attack is set to
          “0”, the Volume value is reached instantly. If the Attack value is raised, it will take longer time before the Master
          Volume value is reached.

      • D(ecay)
          After the Master Volume value has been reached, the level starts to drop. How long this should take is governed
          by the Decay parameter.
          If you want to emulate the volume envelope of a note played on a piano for example, the Attack should be set to
          “0”, the Decay parameter should be set to a medium value and the Sustain level should be set to “0”, so that the
          volume gradually decreases down to silence, even if you keep holding the key down. Should you want the decay to
          drop to some other value than zero, you raise the Sustain parameter.
      • S(ustain)
          The Sustain parameter determines the level the envelope should rest at, after the Decay stage. If you set Sustain
          to full level, the Decay setting is of no importance since the volume of the sound is never lowered.
          If you want to emulate the volume envelope of an organ, you theoretically only really need to use the Sustain pa-
          rameter set to full level, as a basic organ volume envelope instantly goes to the maximum level (Attack “0”) and
          stays there (Decay “0”), until the key is released and the sound instantly stops (Release “0”).
          But often a combination of Decay and Sustain is used to generate envelopes that rise up to the Volume value, then
          gradually decreases to finally land to rest on a level somewhere in-between zero and the Master Volume value.
          Note that Sustain represents a level, whereas the other envelope parameters represent times.
      • R(elease)
          The Release parameter works just like the Decay parameter, except it determines the time it takes for the volume
          to drop back to zero after you release the key.

      The Delay section

      This is a stereo delay which affects all voices globally.

      Delay On/Off

      D   Click the On/Off LED button to switch on/off the Delay section.

      Time

      D   Set the time between the delay repeats.
          If Sync is active (see below), the Time parameter controls the time divisions.

      Feedback

      D   Set the number of delay repeats with the Feedback knob.

      Sync

      D   Click the Sync button to sync the delay time to the main sequencer Tempo.
          When active, the Time knob (see above) controls the time divisions.

      Ping Pong

      D   Activate this to get the delay repeats alternating between the left and right channels.
          Note that this also doubles the delay tempo.

      Damp

      D   Raise the Damp value to gradually cut off the high frequencies of the delay repeats.

      Amount

      D   Set the delay amount with the Amount knob.
          Note that the Delay effect is routed as a “send effect”, with the Amount knob working as an “effect return” control.
          This means that if you play a short note with the Amount knob set to zero, you might still get a delay effect if you
          turn up the Amount afterwards (depending on the Feedback setting, see “Feedback”).

      The Reverb section

      This is a stereo reverb which affects all voices globally.

      Reverb On/Off

      D   Click the On/Off LED button to switch on/off the Reverb section.

      Time

      D   Set the reverberation duration time.
          In practice this sets the “size” of the reverberation “chamber/room/hall”.

      Pre-Delay

      D   Set the pre-delay time of the reverb.
          Range: 0-200 ms.

      Hi Damp

      D   Raise the Hi Damp value to cut off the high frequencies of the reverb and thereby create a smoother, warmer
          effect.

      Lo Damp

      D   Raise the Lo Damp value to cut off the low frequencies of the reverb signal, to make the reverb effect less
          “muddy”.

      Amount

      D   Set the reverb amount with the Amount knob.
          Note that the Reverb effect is routed as a “send effect”, with the Amount knob working as an “effect return” con-
          trol. This means that if you play a short note with the Amount knob set to zero, you might still get a reverb effect if
          you turn up the Amount afterwards (depending on the Time setting, see “Time”).

      Connections

      !   Remember that CV connections are NOT stored in the Klang patches! If you want to store CV connections be-
          tween devices, put them in a Combinator device and save the Combi patch.

      Sequencer Control inputs
      The Sequencer Control CV and Gate inputs allow you to play Klang from another CV/Gate device (typically a Matrix
      or an RPG-8). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note on/
      off along with velocity. There are also inputs for modulating the Pitch Bend and Mod Wheel parameters.

      Modulation Inputs
      These control voltage (CV) inputs can be used for modulating the Filter Cutoff and Resonance parameters, as well as
      the Master Volume level.

      Audio Out
      These are the main audio outputs. When you create a new Klang device, these outputs are auto-routed to the first
      available Mix Channel in the Reason main mixer. If there is no Mix Channel available, a new one will be automatically
      created.

970   KLANG TUNED PERCUSSION


---

<a id="pangea-world-instruments-41"></a>

=== END OF PART ===
