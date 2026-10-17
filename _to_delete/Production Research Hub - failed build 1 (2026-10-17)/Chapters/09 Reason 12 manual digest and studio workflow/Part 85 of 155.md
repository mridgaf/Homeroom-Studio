# Chapter 09: Reason 12 manual digest and studio workflow
## Part 85 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 76 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 86 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 76 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 34: Subtractor Synthesizer

Subtractor Synthesizer

      Introduction
      Subtractor is an analog-type polyphonic synthesizer based on subtractive synthesis, the method used in analog syn-
      thesizers. This chapter will go through all parameters of each section of Subtractor. In addition to the parameter de-
      scriptions, the chapter also includes a few tips and tricks to help you get the most out of the Subtractor synthesizer.
      !   It is recommended that you start with default settings (an “Init Patch”) if you intend to follow the examples in
          this chapter, unless otherwise is stated. An Init Patch is created by selecting “Reset Device” from the device’s
          context menu, or from the Edit menu. If you wish to keep the current settings, save them before initializing.
      The Subtractor has the following basic features:
      D   Up to 99 Voice Polyphony.
          You can set the number of voices for each Patch.
      D   Dual Filters.
          A combination of a multimode filter and a second, linkable, lowpass filter allows for complex filtering effects. See
          “The Filter Section”.
      D   Two Oscillators, each with 32 waveforms.
          See “The Oscillator Section”.
      D   Frequency Modulation (FM).
          See “Frequency Modulation (FM)”.
      D   Oscillator Phase Offset Modulation.
          This is an unique Subtractor feature that generates waveform variations. See “Phase Offset Modulation”.
      D   Two Low Frequency Oscillators (LFO’s)
          See “LFO Section”.
      D   Three Envelope Generators.
          See “Envelopes - General”.
      D   Extensive Velocity Control.
          See “Velocity Control”.
      D   Extensive CV/Gate Modulation possibilities.
          See “Connections”.

      Loading and Saving Patches
      Loading and saving patches is done in the same way as with any other Reason device - see “Loading patches” and
      “Saving patches”.

      The Oscillator Section

      Subtractor provides two oscillators. Oscillators are the main sound generators in Subtractor, the other features are
      used to shape the sound of the oscillators. Oscillators generate two basic properties, waveform and pitch (frequency).
      The type of waveform the oscillator produces determines the harmonic content of the sound, which in turn affects the
      resultant sound quality (timbre). Selecting a oscillator waveform is usually the starting point when creating a new
      Subtractor Patch from scratch.

      Oscillator 1 Waveform

      Oscillator 1 provides 32 waveforms. The first four are standard waveforms, and the rest are “special” waveforms,
      some of which are suitable for emulating various musical instrument sounds.
      q   It is worth noting here that all waveforms can be radically transformed using Phase offset modulation (see
          “Phase Offset Modulation”).
      D   To select a waveform, click the spin controls to the right of the “Waveform” LED display.
          The first 4 basic waveforms are shown as standard symbols, and the special waveforms are numbered 5 - 32.

      Here follows a brief description of the Subtractor waveforms:
      !       Please note that the descriptions of the waveforms sound or timbre is merely meant to provide a basic guide-
              line, and shouldn’t be taken too literally. Given the myriad ways you can modulate and distort a waveform in
              Subtractor, you can produce extremely different results from any given waveform.

      | Waveform             | Description
          Sawtooth           This waveform contains all harmonics and produces a bright and rich sound. The Sawtooth is perhaps the
                             most “general purpose” of all the available waveforms.

          Square             A square wave only contains odd number harmonics, which produces a distinct, hollow sound.

          Triangle           The Triangle waveform generates only a few harmonics, spaced at odd harmonic numbers. This produces
                             a flute-like sound, with a slightly hollow character.

          Sine               The sine wave is the simplest possible waveform, with no harmonics (overtones). The sine wave produces
                             a neutral, soft timbre.

          5                  This waveform emphasizes the higher harmonics, a bit like a sawtooth wave, only slightly less bright-sound-
                             ing.
          6                  This waveform features a rich, complex harmonic structure, suitable for emulating the sound of an acoustic
                             piano.
          7                  This waveform generates a glassy, smooth timbre. Good for electric piano-type sounds.
          8                  This waveform is suitable for keyboard-type sounds such as harpsichord or clavinet.
          9                  This waveform is suitable for electric bass-type sounds.
          10                 This is a good waveform for deep, sub-bass sounds.
          11                 This produces a waveform with strong formants, suitable for voice-like sounds.
          12                 This waveform produces a metallic timbre, suitable for a variety of sounds.
          13                 This produces a waveform suitable for organ-type sounds.
          14                 This waveform is also good for organ-type sounds. Has a brighter sound compared to waveform 13.
          15                 This waveform is suitable for bowed string sounds, like violin or cello.
          16                 Similar to 15, but with a slightly different character.
          17                 Another waveform suitable for string-type sounds.
          18                 This waveform is rich in harmonics and suitable for steel string guitar-type sounds.
          19                 This waveform is suitable for brass-type sounds.
          20                 This waveform is suitable for muted brass-type sounds.
          21                 This waveform is suitable for saxophone-like sounds.
          22                 A waveform suitable for brass and trumpet-type sounds.
          23                 This waveform is good for emulating mallet instruments such as marimba.
          24                 Similar to 23, but with a slightly different character.
          25                 This waveform is suitable for guitar-type sounds.
          26                 This is a good waveform for plucked string sounds, like harp.
          27                 Another waveform suitable for mallet-type sounds (see 23-24), but has a brighter quality, good for vibra-
                             phone-type sounds.

      | Waveform         | Description
      28                    Similar to 27, but with a slightly different character.
      29                    This waveform has complex, enharmonic overtones, suitable for metallic bell-type sounds.
      30                    Similar to 29, but with a slightly different character. By using FM and setting the Osc Mix to Osc 1, this and
                            the following two waveforms can produce noise.
      31                    Similar to 30, but with a slightly different character.
      32                    Similar to 30, but with a slightly different character.

      Setting Oscillator 1 Frequency - Octave/Semitone/Cent

      By clicking the corresponding up/down buttons you can tune, i.e. change the frequency of Oscillator 1 in three ways:
      D   In Octave steps
          The range is 0 - 9. The default setting is 4 (where “A” above middle “C” on your keyboard generates 440 Hz).
      D   In Semitone steps
          Allows you to raise the frequency in 12 semitone steps (1 octave).
      D   In Cent steps (100th of a semitone)
          The range is -50 to 50 (down or up half a semitone).

      Oscillator Keyboard Tracking

      Oscillator 1 has a button named “Kbd. Track”. If this is switched off, the oscillator pitch will remain constant, regard-
      less of any incoming note pitch messages, although the oscillator still reacts to note on/off messages. This can be
      useful for certain applications:
      D   When Frequency Modulation (FM - see “Frequency Modulation (FM)”) or Ring Modulation (see “Ring Modula-
          tion”) is used.
          This produces enharmonic sounds with very varying timbre across the keyboard.
      D   For special effects and non-pitched sounds (like drums or percussion) that should sound the same across the
          keyboard.

      Using Oscillator 2

      You activate Osc 2 by clicking the button next to the text “Osc 2“. Setting oscillator frequency and keyboard tracking
      is identical to Oscillator 1.

      Adding a second oscillator enables many new modulation possibilities which can produce richer timbres. A basic ex-
      ample is to slightly detune (+/– a few cents) one of the oscillators. This slight frequency offset causes the oscillators
      to “beat” against each other, producing a wider and richer sound. Also, by combining two different waveforms, and
      adding frequency or ring modulation, many new timbres can be created.

      Oscillator Mix

      The Osc Mix knob determines the output balance between Osc 1 and Osc 2. To be able to clearly hear both oscilla-
      tors, the “Osc Mix” knob should be set somewhere around the center position. If you turn the Mix knob fully to the left,
      only Osc 1 will be heard, and vice versa. [Command]/[Ctrl]-clicking the knob sets the Mix parameter to center posi-
      tion.

      Oscillator 2 Waveform
      The waveform alternatives for Oscillator 2 are identical to those of Oscillator 1.
      However, the Noise Generator provides a third sound generating source (in addition to the two oscillators) in Sub-
      tractor, and could be regarded as an “extra” waveform for Oscillator 2, as it is internally routed to the Oscillator 2 out-
      put. See below for a description of the Noise Generator.

      Noise Generator

      The Noise Generator could be viewed as an oscillator that produces noise instead of a pitched waveform. Noise can
      be used to produce a variety of sounds, the classic example being “wind” or “rolling wave” sounds, where noise is
      passed through a filter while modulating the filter frequency. Other common applications include non-pitched sounds
      like drums and percussion, or simulating breath noises for wind instruments. To use the Noise Generator, select an
      Init Patch and proceed as follows:
      1. Turn Osc 2 off.
      2. Click the button (in the Noise Generator section) to activate the Noise Generator.
          If you play a few notes on your MIDI instrument you should now hear Osc1 mixed with the sound of the Noise
          Generator.
      3. Turn the Mix knob fully to the right, and play a few more notes.
          Now just the Noise Generator will be heard.
      D   Thus, the output of the Noise Generator is internally routed to Osc 2.
          If you switch Osc 2 on, the noise will be mixed with the Osc 2 waveform.

      There are three Noise Generator parameters. These are as follows:

      | Parameter            | Description
      Noise Decay             This controls how long it takes for the noise to fade out when you play a note. Note that this is inde-
                              pendent from the Amp Envelope Decay parameter, allowing you to mix a short “burst” of noise at the
                              very beginning of a sound, i.e. a pitched sound that uses oscillators together with noise.
      Noise Color             This parameter allows you to vary the character of the noise. If the knob is turned fully clockwise, pure
                              or “white” noise (where all frequencies are represented with equal energy) is generated. Turning the
                              knob anti-clockwise produces a gradually less bright sounding noise. Fully anti-clockwise the noise
                              produced is an earthquake-like low frequency rumble.
      Level                   Controls the level of the Noise Generator.

      Phase Offset Modulation
      A unique feature of the Subtractor oscillators is the ability to create an extra waveform within one oscillator, to offset
      the phase of that extra waveform, and to modulate this phase offset. By subtracting or multiplying a waveform with a
      phase offset copy of itself, very complex waveforms can be created. Sounds complicated? Well, the theory behind it
      might be, but from a user perspective it is just a method of generating new waveforms from existing waveforms.
      A seasoned synth programmer using Subtractor for the first time may wonder why the Subtractor oscillators (seem-
      ingly) cannot provide the commonly used pulse waveform and the associated pulse width modulation (PWM). Or os-
      cillator sync, another common feature in analog synthesizers. The simple answer is that Subtractor can easily create
      pulse waveforms (with PWM) and oscillator sync-sounds, and a lot more besides, partly by the use of phase offset
      modulation.

      Each oscillator has it's own Phase knob and a selector button. The Phase knob is used to set the amount of phase
      offset, and the selector switches between three modes:
      • Waveform multiplication (x)
      • Waveform subtraction (–)
      • No phase offset modulation (o).

      When phase offset modulation is activated, the oscillator creates a second waveform of the same shape and offsets
      it by the amount set with the Phase knob. Depending on the selected mode, Subtractor then either subtracts or mul-
      tiplies the two waveforms with each other. The resulting waveforms can be seen in the illustration below.
      1. The two offset             Ampl.
      waveforms:

                                                                             t.

      2. The result of              Ampl.
      subtraction:

                                                                             t.

      3. The result of              Ampl.
      multiplication:

                                                                             t.

      • In example 1, we see two sawtooth waves with a slight offset.
      • Example 2 shows that subtracting one slightly offset sawtooth wave from the other, produces a pulse wave. If
        you modulate the Phase offset parameter (with for example an LFO), the result will be pulse width modulation
        (PWM).
      • Example 3 shows the resulting waveform when multiplying the offset waves with each other. As you can see
        (and hear if you try it), multiplying waveforms can produce very dramatic and sometimes unexpected results.
      Using phase offset modulation can create very rich and varied timbres, especially when used along with LFO or En-
      velopes to modulate the phase offset.
      q   To get a “feel” for this concept, you could study Patches that use phase offset modulation, and maybe tweak
          some of the Phase Offset parameters to find out what happens. Try “SyncedUp” in the Polysynth category in
          the Factory Soundbank for an example of osc sync or “Sweeping Strings” (in the Pads category) for an exam-
          ple of PWM.
      !   Note that if you activate waveform subtraction with a Phase offset set to “0” for an oscillator, the second wave-
          form will cancel out the original waveform completely, and the oscillator output will be silent. If you set the
          Phase Offset knob to any other value than zero, the sound returns.

      Frequency Modulation (FM)

      In synthesizer-speak, Frequency Modulation, or FM, is when the frequency of one oscillator (called the “carrier”) is
      modulated by the frequency of another oscillator (called the “modulator”). Using FM can produce a wide range of har-
      monic and non harmonic sounds. In Subtractor, Osc 1 is the carrier and Osc 2 the modulator. To try out some of the
      effects FM can produce, proceed as follows:
      1. Select an Init Patch by selecting “Initialize Patch” from the Edit menu.
      2. Activate Osc 2.
          As you need both a carrier and a modulator to produce FM, turning the FM knob will not produce any effect unless
          you first activate Osc 2. For classic FM sounds, use sine wave on oscillator 1 and triangle wave on oscillator 2.
      3. Use the FM knob to set the FM amount to a value of about 50.
          As you can hear, the timbre changes, but the effect isn’t very pronounced yet.
      4. Turn the Osc Mix knob fully to the left, so that only the sound of Osc 1 is heard.
          The modulator (Osc 2) still affects Osc 1, even though the Osc 2 output is muted.
      5. Now, hold down a note on your MIDI keyboard and tune Osc 2 a fifth up from the original pitch by setting the
         Osc 2 frequency “Semi” parameter to a value of 7.
          As you can hear, for each semitone step you vary the Osc 2 frequency, the timbre changes dramatically. Setting
          Osc 2 frequency to certain musical intervals (i.e. fourth, fifth or octave semitone steps) produces harmonic, rich
          timbres, almost like tube distortion. Setting Osc 2 to non-musical intervals usually results in complex, enharmonic
          timbres.
      q   Experiment with different oscillator parameters such as phase offset modulation, changing the waveforms etc.
          and listen to how they affect the sound of frequency modulation.

      Using the Noise Generator as the Modulator source
      As explained earlier, the Noise Generator is internally routed to the Osc 2 output. Hence, if you deactivate Osc 2, and
      activate the Noise Generator while using FM, the noise will be used to frequency modulate Osc 1.
      q   With the Noise Generators default settings, this will sound much like colored noise. But by changing (lower-
          ing) the Noise Generator Decay parameter, so that the noise modulates only the attack portion of the sound
          can produce more interesting results. You could also use a combination of noise and Osc 2.

      Ring Modulation

      Ring Modulators basically multiply two audio signals together. The ring modulated output contains added frequencies
      generated by the sum of, and the difference between, the frequencies of the two signals. In the Subtractor Ring Mod-
      ulator, Osc 1 is multiplied with Osc 2 to produce sum and difference frequencies. Ring modulation can be used to
      create complex and enharmonic, bell-like sounds.
      1. Select an Init Patch by selecting “Initialize Patch” from the Edit menu.
        Save any current settings you wish to keep before initializing.
      2. Activate Ring Modulation with the button in the lower right corner of the oscillator section.
      3. Activate Osc 2.
        You need to activate Osc 2 before any ring modulation can happen.
      4. Turn the Osc Mix knob fully to the right, so that only the sound of Osc 2 is heard.
        Osc 2 provides the ring modulated output.
      5. If you play a few notes while varying the frequency of either oscillator, by using the Semitone spin controls,
         you can hear that the timbre changes dramatically.
        If the oscillators are tuned to the same frequency, and no modulation is applied to either the Osc 1 or 2 frequency,
        the Ring Modulator won’t do much. It is when the frequencies of Osc 1 and Osc 2 differ, that you get the “true”
        sound of ring modulation.

      The Filter Section

      In subtractive synthesis, a filter is the most important tool for shaping the overall timbre of the sound. The filter sec-
      tion in Subtractor contains two filters, the first being a multimode filter with five filter types, and the second being a
      low-pass filter. The combination of a multimode filter and a lowpass filter can be used to create very complex filter ef-
      fects.

      Filter 1 Type
      With this multi-selector you can set Filter 1 to operate as one of five different types of filter. The five types are illus-
      trated and explained on the following pages:
      • 24 dB Lowpass (LP 24)
        Lowpass filters lets low frequencies pass and cuts out the high frequencies. This filter type has a fairly steep roll-
        off curve (24dB/Octave). Many classic synthesizers (Minimoog/Prophet 5 etc.) use this filter type.

        The darker curve illustrates the roll-off curve of the 24dB Lowpass Filter. The lighter curve in the middle represents the filter
        characteristic when the Resonance parameter is raised.

      • 12 dB Lowpass (LP 12)
        This type of lowpass filter is also widely used in analog synthesizers (Oberheim, early Korg synths etc.). It has a
        gentler slope (12 dB/Octave), leaving more of the harmonics in the filtered sound compared to the LP 24 filter.

        The darker curve illustrates the roll-off curve of the 12dB Lowpass Filter. The lighter curve in the middle represents the filter
        characteristic when the Resonance parameter is raised.
      • Bandpass (BP 12)
        A bandpass filter cuts both high and low frequencies, while midrange frequencies are not affected. Each slope in
        this filter type has a 12 dB/Octave roll-off.

        The darker curve illustrates the roll-off curve of the Bandpass Filter. The lighter curve in the middle represents the filter characteristic
        when the Resonance parameter is raised.

      • Highpass (HP12)
        A highpass filter is the opposite of a lowpass filter, cutting out lower frequencies and letting high frequencies pass.
        The HP filter slope has a 12 dB/Octave roll-off.

        The darker curve illustrates the roll-off curve of the Highpass Filter. The lighter curve in the middle represents the filter characteristic
        when the Resonance parameter is raised.
      • Notch
        A notch filter (or band reject filter) could be described as the opposite of a bandpass filter. It cuts off frequencies
        in a narrow midrange band, letting the frequencies below and above through. On its own, a notch filter doesn’t re-
        ally alter the timbre in any dramatic way, simply because most frequencies are let through. However, by combining
        a notch filter with a lowpass filter (using Filter 2 - see “Filter 2”), more musically useful filter characteristics can be
        created. Such a filter combination can produce soft timbres that still sound “clear”. The effect is especially notice-
        able with low resonance (see “Resonance”) settings.

        The darker curve illustrates the roll-off curve of the Notch Filter. The lighter curve in the middle represents the filter characteristic
        when the Resonance parameter is raised.

      Filter 1 Frequency
      The Filter Frequency parameter (often referred to as “cutoff”) determines which area of the frequency spectrum the
      filter will operate in. For a lowpass filter, the frequency parameter could be described as governing the “opening” and
      “closing” of the filter. If the Filter Freq is set to zero, none or only the very lowest frequencies are heard, if set to max-
      imum, all frequencies in the waveform are heard. Gradually changing the Filter Frequency produces the classic syn-
      thesizer filter “sweep” sound.
      !   Note that the Filter Frequency parameter is usually controlled by the Filter Envelope (see “Filter Envelope”) as
          well. Changing the Filter Frequency with the Freq slider may therefore not produce the expected result.

      Resonance
      The filter resonance parameter is used to set the Filter characteristic, or quality. For lowpass filters, raising the filter
      Res value will emphasize the frequencies around the set filter frequency. This produces a generally thinner sound, but
      with a sharper, more pronounced filter frequency “sweep”. The higher the filter Res value, the more resonant the
      sound becomes until it produces a whistling or ringing sound. If you set a high value for the Res parameter and then
      vary the filter frequency, this will produce a very distinct sweep, with the ringing sound being very evident at certain
      frequencies.
      • For the highpass filter, the Res parameter operates just like for the lowpass filters.
      • When you use the Bandpass or Notch filter, the Resonance setting adjusts the width of the band. When you
        raise the Resonance, the band where frequencies are let through (Bandpass), or cut (Notch) will become nar-
        rower. Generally, the Notch filter produces more musical results using low resonance settings.

      Filter Keyboard Track (Kbd)
      If Filter Keyboard Track is activated, the filter frequency will increase the further up on the keyboard you play. If a low-
      pass filter frequency is constant (a Kbd setting of “0”) this can introduce a certain loss of “sparkle” in a sound the
      higher up the keyboard you play, because the harmonics in the sound are progressively being cut. By using a degree
      of Filter Keyboard Tracking, this can be compensated for.

      Filter 2
      A very useful and unusual feature of the Subtractor Synthesizer is the presence of an additional 12dB/Oct lowpass
      filter. Using two filters together can produce many interesting filter characteristics, that would be impossible to create
      using a single filter, for example formant effects.
      The parameters are identical to Filter 1, except in that the filter type is fixed, and it does not have filter keyboard
      tracking.
      D   To activate Filter 2, click the button at the top of the Filter 2 section.
          Filter 1 and Filter 2 are connected in series. This means that the output of Filter 1 is routed to Filter 2, but both fil-
          ters function independently. For example, if Filter 1 was filtering out most of the frequencies, this would leave Filter
          2 very little to “work with”. Similarly, if Filter 2 had a filter frequency setting of “0”, all frequencies would be filtered
          out regardless of the settings of Filter 1.

      q   Try the “Singing Synth” patch (in the Monosynth category of the Factory Sound Bank) for an example of how
          dual filters can be used.

      Filter Link

      When Link (and Filter 2) is activated, the Filter 1 frequency controls the frequency offset of Filter 2. That is, if you
      have set different filter frequency values for Filter 1 and 2, changing the Filter 1 frequency will also change the fre-
      quency for Filter 2, but keeping the relative offset.
      q   Try the “Fozzy Fonk” patch (in the Polysynth category of the Factory Sound Bank) for an example how linked
          filters can be used.
      !   Caution! If no filter modulation is used, and the filters are linked, pulling down the frequency of Filter 2 to zero
          will cause both filters to be set to the same frequency. If combined with high Res settings, this can produce
          very loud volume levels that cause distortion!


=== END OF PART ===
