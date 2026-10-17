# Chapter 09: Reason 12 manual digest and studio workflow
## Part 82 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 73 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 83 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 73 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 33: Thor Polysonic Synthesizer

Thor Polysonic
Synthesizer

      Introduction

      Thor is an advanced synthesizer with many unique features.
      The design could be described as semi-modular, in that the oscillator and filter sections are open slots that allow the
      user to select between various different oscillator and filter types, each with a distinct character. Some of these de-
      signs were inspired by selected vintage equipment.
      As a result, Thor is capable of producing an astounding array of sounds.
      While it offers a lot of scope for serious sound modeling, it still has a basically simple and user-friendly interface.
      In the extensive Modulation bus routing section both audio and control signals (CV) co-exist, and more or less any
      routing combination can be assigned. Use audio to modulate a CV signal or vice versa - Thor’s modulation capabilities
      are virtually limitless.
      Thor also features an advanced step sequencer which can be used for creating melody lines or purely as a modula-
      tion source.
      There are also audio inputs on the back panel. By connecting the output of another device to these inputs, you can
      use Thor’s filters, envelopes etc. to process the sound, or you can use the external audio source to modulate a Thor
      parameter.

      About basic synthesizer terminology
      This chapter assumes familiarity with common synth terminology like oscillators, waveforms, filters and envelopes. If
      you are new to Reason (or these terms), you may want to read the “Subtractor Synthesizer” chapter first, where these
      elements and how they interact are described from a more basic point of view.

      Loading and Saving Patches
      Loading and saving patches is done in the same way as with any other Reason device - see “Loading patches” and
      “Saving patches”.

      Thor elements
      In the picture below an unfolded Thor device is shown.

      Thor’s user interface consists of the following elements (from the top down):
      • The Controller panel, which is always shown if Thor is unfolded.
        See “The Controller panel”.
      • The main Programmer panel contains all the synth parameters.
        The Programmer can be shown/hidden by clicking the “Show Programmer” button on the Controller panel. See
        “Using the Programmer”.
      • The Modulation bus routing section.
        See “Modulation bus routing section”.
      • The Step Sequencer section, where you can program up to 16 steps to produce short melody lines/grooves or
        use it as a modulation source.
        See “Step Sequencer”.

      The Controller panel

      The Controller panel contains standard Master Volume and Pitch and Mod controls, Keyboard Mode/Note Triggering
      sections and four virtual (freely assignable) controls. The panel also has a patch display and standard Select/
      Browse/Save patch buttons (these are always shown even if Thor is folded).

      The Keyboard Mode section
      In this section you make basic keyboard related settings for a patch. It has the following options:

      | Function               | Description
      Polyphony                 This setting determines the number of voices that you can play simultaneously when Polyphonic mode
                                is selected. The maximum number of voices is 32.
      Release                   This governs the number of voices that are allowed to naturally decay/ring out (in the release phase of
      Polyphony                 the envelope) when new notes are triggered and Polyphonic mode is selected. E.g. if you set this to “0”,
                                any new note(s) will cut off the release of any previously triggered notes.
      Mono Legato               Mono Legato mode is monophonic regardless of the Polyphony setting. It works as follows:
                               D   Hold down a key and then press another key without releasing the previous.
                                   Notice that the pitch changes, but the envelopes do not start over. That is, there
                                   will be no new “attack”.
      Mono Retrig               Mono Retrig is also monophonic and this mode means that when you press a key the envelopes are al-
                                ways retriggered.
      Polyphonic                This is the standard polyphonic play mode - you can play the number of voices set with the Polyphony
                                parameter.
      Portamento On/Off/Auto The knob is used for controlling portamento - a parameter that makes the pitch glide between the
                             notes you play, rather than changing the pitch instantly as soon as you hit a key on your keyboard. By
                             turning this knob you set how long it should take for the pitch to glide from one note to the next as you
                             play them. There are three basic portamento modes:
                               • In Auto mode, there will only be any portamento when playing more than one
                                 note. If any of the Mono modes is selected, portamento will only affect the
                                 legato notes.
                               • When set to On, portamento is applied to all notes.
                               • Off means no portamento.

      Note Triggering section
      Using the buttons in this section you can select in what way Thor will respond:
      • Via note input only.
      • Via the Step Sequencer only (see “Step Sequencer”).
      • Or both.
      The section also has a standard Note On indicator.

      About the assignable controls
      • The rotary knobs and buttons in the Controller panel are assignable controls that can be assigned to multiple
        parameters and functions in Thor.
      • You assign parameters to the knobs and buttons in the Modulation Routing panel (these are located on the
        “Modifiers” sub-menu - see “Modulation bus routing section”).
      • Movements of the assignable controls can be recorded as automation.
      • Each control can be assigned to any number of parameters.
      • Clicking on the label for a Rotary or Button lets you type in an appropriate name for it.
      About the button key note function
      To the right of the two assignable buttons there are corresponding spin controls and displays. These can be used to
      assign a key for turning the button on momentarily, as long as the key is held down.
      D   Use the spin controls (or click in the display and move the mouse up or down) to assign a key for the button
          status.
          The assigned key will now turn the function(s) assigned to the button on for as long the key is held down.
      D   Note that the key note function can only switch from off to on, not the other way around, so make sure the but-
          ton is deactivated if you wish to use this function.
          An assigned key will not trigger a note, only the button status. Also note that the button will not light up when you
          press the assigned key.

      The Pitch Bend and Modulation wheels
      • The Pitch and Mod wheels on the Controller panel will mirror the corresponding actions on your master key-
        board.
      • The Range parameter (like for all instrument devices) sets the range of the Pitch Bend action.
      • Pitch Bend is pre-wired to the pitch parameter of the three oscillators, but you can of course use it to control
        any parameter you like. If you don’t want Pitch Bend to affect oscillator pitch, simply set the Range parameter
        to “0”.

      Master volume
      This is the main volume control for outputs 1 & 2.

      Using the Programmer
      The Programmer contains the main synth parameters.
      D   To show the Programmer panel, click the “Show Programmer” button on the Controller panel.
          The Programmer appears below the Controller panel.

      D   The Programmer panel is divided into two sections; the Voice section to the left and the Global section to the
          right. The Global section has a separate brown panel to differentiate it from the Voice section.
          The Voice section contains the basic synth parameters and the parameters are “per-voice”, i.e. all envelope and
          LFO cycles are triggered individually for each voice. The Global section to the right contains global parameters that
          affect all voices.
      D   There are three open Oscillator slots, a Mixer, two open Filter slots, a Shaper, three Envelope generators, an
          LFO and an Amplifier in the Voice section.
          The open Oscillator and Filter slots allow you to select between different types of oscillators and filters.
      D   The Global section contains a second LFO, a Global Envelope, a third open Filter slot and Chorus and Delay ef-
          fects.

      Basic connections - a tutorial
      There are certain pre-defined connections available between the Oscillator 1-3 slots and the Mixer, Filter 1/Shaper,
      Filter 2 and Amp sections. On the panel itself, lines with arrows are shown to indicate the standard signal paths.
      q   Note that you can also connect sections using the Modulation bus section (see “Modulation bus routing sec-
          tion”). You are not in any way limited to the pre-defined routings, but they do provide a quick and convenient
          way to connect the basic synth “building blocks” together.
      In the following tutorial we will create a standard setup using two oscillators and two filters to demonstrate Thor ba-
      sics and the (standard) signal path:
      1. Select “Reset Device” from the context menu or from the Edit menu.
          The “Init patch” is a basic setup with an Analog oscillator in Oscillator slot 1 and a Ladder LP filter in Filter slot 1
          loaded. A connection between Oscillator 1, Filter 1 and the Amp section is already activated, so you get a sound
          when you play.
      Below the Oscillator 1 slot in the upper left corner are two more slots, currently empty. These are the Oscillator 2 and
      3 slots, respectively. The three Oscillator slots are basically identical in that they can each be loaded with one of 6 os-
      cillator types.
      2. Click the arrow pop-up in the upper left corner of the Oscillator 2 slot, and select a second oscillator from the
         pop-up that appears.
          The following oscillator types are available; Analog, Wavetable, Phase Modulation, FM Pair, Multi and Noise. For a
          description of the various oscillator types, see “The Oscillator section”.

          Selecting oscillator type.

      With a basic connection setup, the Oscillator outputs are internally connected to the “Mix” section. To pass the output
      signal onwards in the signal chain, you first have to activate a connection. This is done using the two vertical rows of
      routing buttons labelled 1, 2 and 3 to the right of the Oscillator section.

      • The upper row of routing buttons determine which of the Oscillators 1 to 3 are routed to Filter 1, and the lower
        row which of the Oscillators 1 to 3 are routed to Filter 2.
        All three oscillators can be simultaneously routed to both filters, serially or in parallel (or any combination of these
        variations). This is explained later in this tutorial.
      By activating one or more of these buttons means that the oscillator (1 to 3) is routed to the corresponding Filter.
      Currently, Oscillator 1 is connected to Filter 1 slot (which is pre-loaded with a Ladder LP filter).
      This is indicated by the “1” routing button being lit. The Filter 2 slot is currently not active, which is indicated by a
      blank panel.
      3. Click the “2” button to the left of the Filter 1 section so that it lights up to activate a connection for Oscillator 2.
        Now if you play a few notes you should hear both Oscillator 1 and Oscillator 2, via the Filter 1 section.

      • The Filter 1 output passes via the Shaper (currently not activated), on to the Amp section, and finally to the
        Main Outputs.
        Actually, the Amp section output is routed via the Global section before being sent to the Main Outputs, but as cur-
        rently nothing is activated in the Global section the signal passes through unprocessed.

      4. Next, click the arrow pop-up in the upper left corner of the Filter 2 slot.
        A pop-up menu with the four available Filter types appears. For a description of the filter types, see “Filter slots”.

      5. Select a type of filter, e.g. a Comb filter for the Filter 2 slot.
        Now that the Filter 2 slot in the Voice section is active, you can connect the oscillators to it by using the lower row
        of routing buttons.
      6. Click the routing buttons “1” and “2” to the left of the Filter 2 slot so that the buttons are lit.
        Now the two oscillators are connected to Filter 2.
      7. Make sure the arrow routing button that points to the Amp section just above the Filter 2 section is activated.
        Now if you play a few notes, both oscillators are routed via both filter sections in parallel. You could of course se-
        lect to pass only one of the oscillators via one filter and both oscillators via the other - any combination is possible.

      You can also connect the Filter 1 and 2 sections serially, meaning that the output of Filter 1 is passed through Filter
      2 before reaching the Amp section. This is done as follows:
      8. Switch off the routing buttons “1” and “2” to the left of the Filter 2 slot.
        If you leave them on the oscillators will pass through Filter 2 twice; both via Filter 1 and directly. This is also per-
        fectly “allowable”, but to make things clearer in this tutorial we will use a standard serial filter setup.
      9. Click the Arrow “left” button below the Shaper.
        Now the filters are connected serially, with the output of Filter 1 (via the for now inactive Shaper) being connected
        to the Filter 2 input. Both oscillators are processed by both filters connected in series.

      That concludes this tutorial on how the pre-wired connections in the Voice section can be used, but note that you can
      also use the Modulation bus to make connections - see “Modulation bus routing section”.

      Other pre-defined routing assignments
      There are other sections in Thor which are pre-defined and can be used without having to make any prior assign-
      ments:
      D   The Amp Envelope and the Filter Envelope control the volume level and frequency of the Filters (1 & 2), respec-
          tively.
          The amount of filter envelope control is controllable by using the “Env” parameter in each Filter section.
      D   The effects (Delay/Chorus) in the Global section are part of the signal chain and can simply be switched on and
          used.

      The Oscillator section

      Oscillators generate the basic raw sound (pitch and waveform) that can in turn be processed by the other parame-
      ters. The Oscillator section contains three open slots which can each be loaded with one of six oscillator types. The
      three Oscillator slots are numbered 1-3, with the top slot housing Oscillator 1, the middle slot Oscillator 2 and the
      bottom slot Oscillator 3.
      D   The Arrow button in the top left corner of each slot opens a pop-up menu where an oscillator type can be se-
          lected for the corresponding slot.

      There are six Oscillator types available:
      • Analog
      • Wavetable

      • Phase Modulation
      • FM Pair
      • Multi Oscillator
      • Noise
      You can also select Off mode (no oscillator).

      Common parameters
      The specific parameters of the various oscillator types are described separately, but there are also common parame-
      ters that apply to all oscillator types. These are:
      D   Octave (OCT) knob - this changes the pitch of the oscillator in octave steps.
          The range is ten octaves.
      D   The Semi knob changes the pitch of the oscillator in semi-tone steps.
          The range is 12 semitone steps (1 octave).
      D   The Tune knob fine tunes the pitch of the oscillator in cent steps.
          The range is +/- 50 cents (down or up half a semitone).
      D   Keyboard Track (KBD) - this knob sets how much the oscillator pitch tracks incoming note data.
          Turned fully clockwise the pitch tracks the keyboard normally, i.e. a semitone per key.
      D   All oscillators also have waveform selectors and a modifier parameter. How the waveform selection works,
          and what parameter is the modifier varies according to the selected oscillator type.

      D   Important to note is that if you have made a modulation routing to an oscillator parameter e.g. the modifier,
          and then change the oscillator type, the modulation will be transferred to the corresponding parameter in the
          new oscillator.
          The same goes for all common parameters (tuning and tracking). If you switch oscillator type, all common param-
          eters are left unchanged.
      D   Oscillators can be synced - see “About Oscillator Sync”.

      D   Any oscillator type loaded into the Oscillator 1 slot can also be amplitude modulated by Oscillator 2 - see
          “About Amplitude Modulation (AM)”.

      Analog oscillator

      This is a classic analog oscillator with 4 standard waveforms. The waveform selector button is in the lower left corner
      of the oscillator panel, but you can also click directly on the waveform symbols to switch waveform. The four available
      waveforms are from the top down (as displayed on the panel): Sawtooth, Pulse, Triangle and Sine.
      • The Mod parameter (PW) controls pulse width and only affects the pulse waveform.
          By modulating the PW parameter the width of the pulse wave changes, allowing for PWM (Pulse Width Modula-
          tion) which is a standard feature in most vintage analog synths.
      q   For a perfect square wave, set pulse width (PW) to 64.

      Wavetable oscillator

      Wavetable oscillators has been the basis of several vintage synths (PPG, Korg Wavestation and many others).
      • With the Wavetable oscillator, you select between 32 wavetables, where each wavetable contains several (up
        to 64) different waveforms. By using an envelope or a LFO you can sweep through a wavetable to produce tim-
        bre variations.
      The parameters are as follows:
      D   Position is the modifier (Mod) parameter and controls the position within the selected wavetable, i.e. which
          waveform is active at a given time.
          By modulating the Position you can sweep through the waveforms in the selected wavetable. You can of course
          also use a single static waveform in a wavetable if you so wish, by not applying any modulation to this parameter.
      D   The X-Fade button determines whether the change between waveforms in a wavetable should be abrupt (X-
          Fade off), or smooth (X-Fade on).
          If set to on, the waveform transitions are cross-faded.
      D   There are 32 wavetables that can be selected using the up/down buttons or by clicking in the Wavetable dis-
          play.
      Some of the wavetables have waveforms that sequentially follow the harmonic series, i.e. each following waveform
      adds a harmonic. Others have waveform series that produce a sound similar to oscillator sync when swept, and other
      wavetables are simply mixed waveforms. The last 11 wavetables are based on wavetables used in the original PPG
      2.3 synthesizer.

      Phase Modulation oscillator

      The Phase Modulation oscillator is inspired by the Casio CZ series of synthesizers. Phase modulation is based on
      modulating the phase of digital waveforms to emulate common filter characteristics.
      D   You have a First and Second waveform which can be combined. Instead of mixing the two waveforms they are
          played in series, one after the other.
          This adds a fundamental one octave below the pitch of the original sound.
      D   The PD parameter (Mod) changes the shape of the wave, much like a filter does.
      The following waveforms (sequentially from the first) are available as the First waveform:
      • Sawtooth
      • Square

      • Pulse
      • Pulse and Sine
      • Sine and flat (half sine)
      • Saw x Sine
      • Sine x Sine
      • Sine x Pulse
      The last three waveforms could be described “resonant”, as these originally were meant to simulate filter resonance.
      They didn’t really do this very accurately, but nevertheless constituted an important part of the sound.
      The Second waveform has the same available waveforms except the last three, and it can also be bypassed alto-
      gether. You can combine waveforms freely, except it is not possible to combine two “resonant” waveforms.

      FM Pair oscillator

      As the name implies, this oscillator generates FM, where one oscillator (Carrier) is frequency modulated by a second
      oscillator (Modulator). Although very simple to use (unlike most hardware FM synths), this oscillator can produce a
      very wide range of FM sounds.
      D   The Carrier and Modulator selector buttons set the frequency ratio between these two oscillators (the range is
          1-32).
          The frequency ratio is what determines the basic frequency content, and thus, the timbre of the sound.
      D   The FM knob sets the amount of frequency modulation.
          This is also the Modifier parameter. If FM amount is set to zero, there is no FM and the output will be a pure sine
          wave.
      • If you set FM Amount to zero and step through the values of the Carrier oscillator, you can hear that the pitch
        is changed according to the harmonic series.
      • Stepping through the Mod oscillator values will change the pitch in the same way, although FM Amount has to
        be set to a value other than zero to be able to hear it.
      Thus, 2:2 is the same wave shape as 1:1 but one octave higher in pitch, 3:3 is the same wave shape as 2:2 but a fifth
      higher in pitch and so on.

      Multi oscillator

      This versatile oscillator can simultaneously generate multiple detuned waveforms (of a set type) per voice. It is great
      for producing complex timbres e.g. to simulate cymbal or bell sounds, but can also generate a wide range of harmonic
      sounds.
      D   The following basic waveforms are available: Sawtooth, Square, Soft Sawtooth, Soft Square, Pulse.
          You switch waveforms using the button in the lower left corner, or by clicking directly on the waveform symbol.
      D   The Amount (AMT) parameter governs the amount of detune.
          Turn clockwise for more detune. This is also the modifier (Mod) parameter. Using low Amount settings can pro-
          duce subtle detune variations that makes the sound shift and move endlessly, like an advanced chorus effect,
          whereas higher Amount settings can produce wild, detuned timbres.
      D   The Detune Mode parameter sets the basic operational mode of the detuning.
          If Amount is set to 0, only the “Octave” and “Fifth” Detune modes actually change the sound, as these modes start
          off with dual waveforms tuned one octave and a fifth apart, respectively. The “Fifth Up” and “Oct UpDn” modes de-
          tune waveforms as the names imply between zero to full Amount settings. “Linear” will change the amount of de-
          tune according to where on the keyboard you play; in lower keyboard ranges the amount of detune is stronger
          than in higher keyboard ranges and vice versa. The other modes (Interval and Random) basically add multiple
          waveforms and detune them in various ways that will produce different results.

      Noise oscillator

      The Noise oscillator can not only produce white and colored noise, but can also be used either as a pitched oscillator
      or as a modulation source.
      It has the following basic parameters:
      D   There is a single Noise parameter (apart from the standard tuning and kbd track knobs).
          This is the Noise modifier parameter, that controls different parameters depending on the selected Oscillator
          mode, see below.

      D   The Waveform selector button in the bottom left corner is used to set the Oscillator mode.
          The following modes are available:’

      | Mode         | Description
      Band            In this mode, the Oscillator knob controls bandwidth. Turned fully clockwise, the oscillator produces pure noise.
                      Turning the knob counter-clockwise gradually narrows the bandwidth until a pitch is produced. The pitch will
                      track the keyboard normally if the keyboard (KBD) knob is set fully clockwise.
      S/H             S/H stands for “sample and hold”, which is a type of random generator. The Oscillator knob controls the rate of
                      the sample and hold. With high Oscillator knob settings, it produces colored noise with a slightly “phased” sound
                      quality. With lower rate settings you can use the oscillator as a modulation source like a LFO with random values.
                      For example, if you modulate the pitch of another oscillator using S/H with a low Rate setting as the source, you
                      will get stepped random modulation of the pitch.
      Static          As the name implies, this can generate the sound of static interference if you use low Oscillator settings. The
                      Oscillator parameter controls Density, i.e. the amount of static. High Density settings generates noise.
      Color           This produces colored noise, which is basically noise where certain frequency areas are filtered, i.e. cutting or
                      boosting certain frequency areas in the noise. The Oscillator knob controls Color. With a maximum Color setting
                      you get white noise, and lower settings produces noise emphasizing lower frequencies.
      White           This produces pure white noise, where all frequencies have equal energy. There is no associated Oscillator pa-
                      rameter for White noise.

      About Oscillator Sync
      Oscillator sync is when one oscillator will restart the period of another oscillator, so that they will have the same base
      frequency. If you change or modulate the frequency of the synced oscillator you get the characteristic sound associ-
      ated with oscillator sync.

                                                                     Syncing oscillator

                                                                     Synced oscillator


=== END OF PART ===
