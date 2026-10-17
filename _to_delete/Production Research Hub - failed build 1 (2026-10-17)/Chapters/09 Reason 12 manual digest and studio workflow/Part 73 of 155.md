# Chapter 09: Reason 12 manual digest and studio workflow
## Part 73 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 64 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 74 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 64 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      • FM > FM Ratio (1:1, 1:2, 1:8, 2:1)
          These modifiers let you frequency modulate the currently selected Waveform at various ratios. The carrier signal is
          the currently selected Waveform (C: ) and the modulator ( :M) is the modifier signal. Set the frequency modulation
          amount with the Amount knob.
      • FM > FM Feedback
          Here, an internally fed back sinewave signal at an 1:1 ratio modulates the waveform (same signal type as in the
          “FM > FM Feedback” Waveform).
      • Detuning > Unison3
          This simulates 2 copies of the original signal. The Amount knob controls the detuning amount and rate.
      • Detuning > Unison7
          This simulates 6 copies of the original signal. The Amount knob controls the detuning amount and rate.
      • Detuning > Ensemble
          This simulates a variable number of copies of the original signal. The Amount knob controls the number of copies,
          the detuning amount and rate.
      • Detuning > Unison 3Oct
          This simulates 2 copies of the original signal at +1 and +2 octaves relative to the original signal. The Amount knob
          controls the detuning amount and rate.
      • Formant
          This simulates a formant (body) filter, which produces multiple peaks and notches in the frequency spectrum of
          the signal. The Amount knob controls the formant transposition in the frequency spectrum. At Amount=50% the
          signal is unaffected. Below 50% the formant is transposed down and above 50% it’s transposed up.
          To make the formant static in the frequency spectrum, regardless of which note you play, modulate the Amount
          parameter using the “-KEY” (inverted) modulation source with a fairly high value (see “Amount Modulation” below).
          This is especially useful if you are using an acoustic instrument sample as User Wave in the Oscillator section.

      Amount
      D   Turn the Amount knob to change the modification amount of the currently selected Modifier.
          The wave shapes are updated in real-time and shown in the Waveform display.

      Amount Modulation
      D   Click the Modulation Source box to bring up a menu of the available modulation sources.
          The “Inverted” sub-menu contains inverted variations of all modulation sources.
      D   Set the modulation amount with the Amount Modulation knob.
      q   If you want other modulation sources or scaling options, use the Mod Bus, see “The Modulation Bus section”.

      The Spectral Filter

      The signal from the Oscillator section can then be processed by the Spectral Filter. The Spectral Filter features a
      wide variety of algorithms that affect the partials of the signal.

      Spectral Filter On/Off
      D   Click the On/Off LED button to activate/deactivate the Spectral Filter.

      Spectral Filter display
      The interactive Spectral Filter display shows the filter shape in real-time.
      • Clicking and dragging vertically in the display changes the Freq parameter, see “Freq”.
      • Clicking and dragging horizontally in the display changes the Resonance parameter, see “Reso”.
      q   See “Recording display movements in the sequencer” for tips about automating display movements.

      Spectral Filter selector
      D   Click the Spectral Filter name box to bring up a menu of the available filter types.
          The available filter types are:
      • LP 12
          This simulates a standard 12dB/octave lowpass filter. Set the cutoff frequency with the Freq knob and the
          resonance amount with the Reso knob.
      • LP 24
          This simulates a standard 24dB/octave lowpass filter. Set the cutoff frequency with the Freq knob and the
          resonance amount with the Reso knob.
      • HP 24
          This simulates a standard 24dB/octave highpass filter. Set the cutoff frequency with the Freq knob and the
          resonance amount with the Reso knob.
      • BP 12
          This simulates a standard 12dB/octave bandpass filter. Set the center frequency with the Freq knob and the
          resonance amount with the Reso knob.
      • Par EQ
          This simulates a standard single band parametric equalizer with a fixed bandwidth. Set the center frequency with
          the Freq knob and the gain/attenuation with the Reso knob.
      • Dual Peak
          This simulates two 12dB/octave bandpass filter routed in parallel. Set the center frequency of the first bandpass
          filter with the Freq knob and the peak separation with the Reso knob.
      • Vocal Formant
          This simulates the formants of the vocal tract by using multi-peak+notch filters. Change the formant with the Freq
          and Reso knobs.
      • LP Variable Slope
          This simulates a non-resonant lowpass filter with a variable attenuation slope. Set the cutoff frequency with the
          Freq knob and the attenuation slope with the Reso knob.
      • HP Variable Slope
          This simulates a non-resonant highpass filter with a variable attenuation slope. Set the cutoff frequency with the
          Freq knob and the attenuation slope with the Reso knob.
      • Comb +
          This simulates a multi notch filter, great for phaser types of effects. Set the cutoff frequency of the first notch with
          the Freq knob and the attenuation amount - and consequently the bandwidth - of the notches with the Reso knob.
          The difference between “Comb +” and “Comb –” (see below) is in the position of the peaks in the spectrum. The
          main audible difference is that the “Comb –” version causes a bass cut.

      • Comb -
          This simulates a comb filter with a positive feedback loop - but without feed forward - ideal for flanger and phaser
          types of effects. Set the cutoff frequency of the second peak with the Freq knob and the resonance amount with
          the Reso knob. The difference between “Comb +” (see above) and “Comb –” is in the position of the peaks in the
          spectrum. The main audible difference is that the “Comb –” version causes a bass cut.
      • Resonator 1,2 and 3
          The three Resonator algorithms contain formant filter tables that simulate various body resonances (multi-
          peak+notch filters). Set the position in the formant tables with the Freq knob and the resonance with the Reso
          knob.
      • Envelope 4
          This is a special mode where you can manually draw your own filter curve in the Envelope 4 window. You then con-
          trol the cutoff/center frequency with the Freq knob and the resonance with the Reso knob. See “Using the Enve-
          lope 4 curve as a Spectral Filter curve” for information on how to draw your own filter curves.
      • User Wave
          This utilizes a filter generated from FFT analyses of the external sample you have loaded in the User Wave section
          (see “The User Wave and Mixer section”). Transpose the formant up/down in the frequency spectrum with the
          Freq knob and change the filter’s position in the sample with the Reso knob.
      q   To create a classic “vocoder” effect, load a vocal/speech sample in the User Wave section. Then, set the Freq
          knob to 50%, the Reso knob to 0% and the KBD knob to 0%. Then, have one of the Envelopes modulate the
          Reso parameter using the Modulation Bus (see “The Modulation Bus section”). Create a positive ramp (in-
          verted sawtooth) envelope and set the Reso modulation amount to 100%.

      Freq
      D   Set the cutoff/center frequency of the currently selected Spectral Filter type.

      Reso
      D   Set the resonance amount of the currently selected Spectral Filter type.

      Frequency Modulation
      D   Turn the Kbd knob to set the keyboard tracking amount.
          At 0% the filter is static and doesn’t track the keyboard at all. At 100% the filter tracks the keyboard 1 semitone
          per note. At values above 0% you can also see the filter curve move sideways in the Spectral Filter Display
          depending on where on the keyboard you play.
      D   Click the Frequency Modulation Source box to bring up a menu of the available modulation sources.
          The “Inverted” sub-menu contains inverted variations of all modulation sources.
      D   Set the modulation amount with the Frequency Modulation Amount knob.
      D   Turn the Velo knob to control the Frequency Modulation Amount from Keyboard Velocity.
      q   If you want other modulation sources or scaling options, use the Mod Bus, see “The Modulation Bus section”.

      The Harmonics section

      The Harmonics section offers extensive modulation possibilities of the partials of the signal. For most algorithms the
      partials’ characteristics is displayed in the Spectral Filter display, see “Spectral Filter display”.

      Harmonics On/Off
      D   Click the On/Off LED buttons to activate/deactivate the Harmonics section.

      Harmonics selector
      D   Click the Harmonics name box to bring up a menu of the available harmonic algorithms.
          The available Harmonics types are:
      • Random Gain
          This alters the gain for each of the partials in the signal in a random fashion. Turn the Pos knob to change the
          randomization “pattern” and the Amount knob to change the partial gain levels in the “pattern”.
      • Harmonic 1-8 Mix
          This alters the gain/attenuation for the first eight partials in the signal. Turn the Pos knob to crossfade between
          the partials and the Amount knob to change the partial gain/attenuation level. Amount levels below 50% attenu-
          ate all partials but the one selected with the Pos knob. Amount levels above 50% attenuate the partial selected
          with the Pos knob.
      • Odd-Even
          This alters the gain/attenuation of the partials in the signal. At Pos=0% the Amount knob controls the mix strictly
          between the odd and even partials in the signal. At other Pos values, the gain/attenuation is not strictly on odd and
          even partials. At Amount=50% the Pos value has no effect.
      • Stretch
          This stretches or squeezes all partials (overtones) - except for the fundamental - in the signal, up or down in the
          frequency range. Perfect for turning a harmonic signal into a more inharmonic one. Change the stretch amount
          with the Amount knob. The Pos knob controls the start phase of all the overtones. At Pos=0% all partials start at
          the same phase. When Amount is set fairly high the Pos parameter have little or no influence on the sound.
      q   Try this with the Karplus-Strong waveform to create really realistic metallic sounds, see “Karplus-Strong”!
      • Ensemble
          This is the perfect algorithm for really dense pad sounds. The Ensemble algorithm simulates a type of chorus
          effect by utilizing noise modulation of the partials. Set the noise frequency with the Pos knob and the mix level with
          the Amount knob.
      • Ensemble Sparse
          The Ensemble Sparse algorithm also utilizes noise modulation of the partials, but here a lot of noise frequency
          bands are cut out. This makes Ensemble Sparse sound more animated and less smooth than the Ensemble algo-
          rithm described above. Set the noise frequency with the Pos knob and the mix level with the Amount knob.
      • HF Noise
          This amplitude modulates the high frequencies in the signal with (high-frequency) noise, perfect for adding “breath
          noise” to the signal, for example. Set the noise frequency with the Pos knob and the noise mix level with the
          Amount knob.
      • Harmonic Lag A-R
          The Harmonic Lag A-R algorithm is designed especially for use with the User Wave algorithm in the Spectral Filter
          (see “User Wave”) to create vocoder effects. The Harmonic Lag A-R algorithm controls the Spectral Filter - so the
          Spectral Filter has to be on for this to work!
          Note that the Harmonic Lag A-R algorithm works on the filter partials - not the oscillator’s signal partials. Set the
          Attack time of the filter partials with the Pos knob and the Release time with the Amount knob. These controls
          work similarly to the Attack and Decay parameters on the BV512 Vocoder device.

      Pos
      D   Turn the Pos knob to change the frequency of the currently selected Harmonics algorithm.
          The frequency spectrum is updated in real-time and shown in the Spectral Filter display.

      Amount
      D   Turn the Amount knob to change the intensity of the currently selected Harmonics algorithm.
          The frequency spectrum is updated in real-time and shown in the Spectral Filter display.

      The Unison section

      The Unison function generates detuned duplicates of the signal in pairs on either side of the original signal’s pitch.

      Unison On/Off
      D   Click the On/Off LED button to activate/deactivate the Unison section.

      Unison display
      The Unison display shows the unison characteristics, as set with the controls in the Unison section. Note, though, that
      this display is not interactive like the Waveform and Spectral Filter displays.

      Unison Type selector
      D   Click the Unison name box to bring up a menu of the available Unison types.
          The available Unison types are:
      • Normal
          This generates duplicates of the signal on either side of the original signal’s pitch.
      • Fourth
          This generates duplicates of the signal on either side of the fourth above the original signal’s pitch.
      • Fifth
          This generates duplicates of the signal on either side of the fifth above the original signal’s pitch.
      • Octave Down
          This generates duplicates of the signal on either side of the original signal’s pitch - one octave down.
      • Phase Only
          This generates duplicates of the signal on either side of the original signal’s pitch. The Detune parameter (see be-
          low) now controls the phases of the signal copies, instead of the detuning. This is great for creating wide stereo
          sounds without lots of detuning.
          If Phase Sync is active in the Oscillator (see “Phase Sync”), all signals in the Unison function get the same relative
          start phases each time you play the same note. The original signal always has the phase 0 degrees.

      Count
      D   Set the number of desired signals in the unison effect.
          Range: 1-7.
          Note that for even numbers, the original signal is represented by two duplicates.

      Blend
      D   Set the mix between the original signal and the duplicates.
          For even “Count” numbers (see above), one of the duplicates represents the original signal in the mix.

      Detune
      D   Set the pitch detuning of the signal duplicates.
          If the “Phase Only” Unison type is selected (see above), the Detune knob controls the phases of the signal dupli-
          cates instead of the pitch detuning.
      q   In the “Phase Only” scenario it could also be a good idea to modulate the Detune parameter from an LFO
          using the Modulation Bus (see “The Modulation Bus section”), to create nice phasing effects.

      Spread
      D   Set the stereo spread amount of the signal duplicates.

      The User Wave and Mixer section

      The User Wave and Mixer section is where you can sample (or load an external sample) to use in the Oscillators (see
      “User Wave/User Wave Smooth”) and/or in the Spectral Filter (see “User Wave”). In the Mixer you can mix and pan
      the signals from the three Sound Engines before sending them to the Filter, Amp and Multi FX sections.

      Sample Select/Load/Sampling/Edit buttons
      D   Load a sample using drag & and drop, or by clicking the Browse sample button, or by using the Up/Down but-
          tons to scroll and load a sample from the currently selected folder.
      D   Alternatively, sample straight into Europa by clicking the Start sampling button.
          See the “Sampling” chapter for more information about setting up and using Reason for sampling.
      D   Click the Edit Sample button to open up the existing sample in the Sample Edit window.
          See “Editing samples” for more information about editing samples in Reason.
      • It’s possible to load/sample stereo signals. However, the sample will be automatically converted to mono in
        Europa.
      !   Like with the other sampler devices in Reason, the Europa patch does not include the actual sample - only a
          reference to it. Therefore, the sample has to be stored separately (self-contained with the song, or already on
          disk or in a ReFill on your computer).
      !   If the sample length is a multiple of 2048 samples (“Serum compatible”), no pitch detection is being made.
          Then, Europa automatically assumes that 2048 samples is one complete waveform cycle (period). If the sample
          is not an exact multiple of 2048 samples, a pitch detection is being performed by Europa to determine the
          pitch. Longer samples (with a stable pitch) will render better pitch detection results, so don’t use very short
          samples.

      Level
      D   Set the volume of the corresponding Sound Engine signal with the Level slider.
          Range: -Inf to +6.0dB.

      Pan
      D   Set the panning of the corresponding Sound Engine signal in the stereo panorama.

      The Filter section

      Routing buttons
      D   Click the red LED buttons to route the corresponding Sound Engine signals to the Filter section.
          If deactivated, the signal bypasses the Filter and goes straight to the Amp section, see “The Amplifier section”.

      Drive
      D   Turn the Drive knob to amplify and introduce an overdrive type of distortion to the Sound Engine signal(s)
          in the filter.

      Filter Type selector
      D   Click the Filter Type name box to select one of the following filter types:
      • SVF HP 12dB
          A state variable (SVF) highpass filter with a 12dB/octave slope. This filter is similar to the State Variable Filter in
          the Thor synthesizer.
      • SVF BP 12dB
          A state variable (SVF) bandpass filter with 12dB/octave slopes. This filter is similar to the State Variable Filter in
          the Thor synthesizer.
      • SVF LP 12dB
          A state variable (SVF) lowpass filter with a 12dB/octave slope. This filter is similar to the State Variable Filter in
          the Thor synthesizer.
      • SVF Notch
          A state variable (SVF) notch filter. This filter is similar to the State Variable Filter in the Thor synthesizer.
      • Ladder LP 24dB
          A ladder-type lowpass filter with a 24dB/octave slope. The resonance peak more narrow in this filter type than in
          the MFB LP 24dB filter (see below). The filter can be driven to self-oscillate.
      !   Be careful when using this filter type as high Resonance values could generate quite extreme audio levels!
      • MFB LP 12dB
          A multiple feedback (MFB) lowpass filter with a 12dB/octave slope.
      • MFB LP 24dB
          A multiple feedback (MFB) lowpass filter with a 24dB/octave slope. The resonance peak is wider in this filter type
          that in the Ladder filter (see above). The filter can be driven to self-oscillate.
      !   Be careful when using this filter type as high Resonance values could generate quite extreme audio levels!

      • MFB HP 24dB
          A multiple feedback (MFB) highpass filter with a 24dB/octave slope.
      !   Be careful when using this filter type as high Resonance values could generate quite extreme audio levels!
      • K35 LP 12dB
          An “early MS-20 type” of lowpass filter with a 12dB/octave slope. The filter can be driven to self-oscillate.
      !   Be careful when using this filter type as high Resonance values could generate quite extreme audio levels!

      Reso
      D   Set the resonance amount.
          In the SVF Notch filter, the Reso knob controls the width of the notch - from wide to narrow.

      Freq
      D   Set the cutoff frequency (for the HP and LP filter types) or the center frequency (for the BP filter type).

      Frequency Modulation
      D   Turn the Kbd knob to set the keyboard tracking amount.
          At 0% the filter is static and doesn’t track the keyboard at all. At 100% the filter tracks the keyboard 1 semitone
          per note.
      D   Click the Frequency Modulation Source box to bring up a menu of the available modulation sources.
          The “Inverted” sub-menu contains inverted variations of all modulation sources.
      q   Use one of the Envelopes (see “The Envelopes section”) as modulation source to create a Filter envelope.
      D   Set the modulation amount with the Frequency Modulation Amount knob.
      D   Turn the Velo knob to control the Frequency Modulation Amount from Keyboard Velocity.
      q   If you want other modulation sources or scaling options, use the Mod Bus, see “The Modulation Bus section”.

      The Amplifier section

      The Amplifier section contains a standard ADSR envelope, which controls the amplitude of the signals from all three
      Sound Engines equally.
      q   To create an “amp envelope” for a separate Sound Engine, have a look at “Creating an individual “pre amp en-
          velope” for a Sound Engine”.
      The picture below shows the various stages of the ADSR envelope:

            Level

        Gain
       (level)
                                              Sustain
                                              (level)
                                                                        Time
                            Attack   Decay               Release
                            (time)   (time)               (time)

                 Key Down                                Key Up

      The ADSR envelope stages.

      A(ttack)
      When you play a note on your keyboard, the envelope is triggered. This means it starts rising from zero to the value
      set with the Gain knob (see below). How long this should take, depends on the Attack setting. If the Attack is set to
      “0”, the Gain level is reached instantly. If the Attack value is raised, it will take longer time before the Gain level is
      reached.

      D(ecay)
      After the Gain level has been reached, the level starts to drop. How long this should take is governed by the Decay
      parameter.
      If you want to emulate the volume envelope of a note played on a piano for example, the Attack should be set to “0”,
      the Decay parameter should be set to a medium value and the Sustain level should be set to “0”, so that the volume
      gradually decreases down to silence, even if you keep holding the key down. Should you want the decay to drop to
      some other value than zero, you raise the Sustain parameter.

      S(ustain)
      The Sustain parameter determines the level the envelope should rest at, after the Decay stage. If you set Sustain to
      full level, the Decay setting is of no importance since the volume of the sound is never lowered.
      If you want to emulate the volume envelope of an organ, you theoretically only really need to use the Sustain param-
      eter set to full level, as a basic organ volume envelope instantly goes to the maximum level (Attack “0”) and stays
      there (Decay “0”), until the key is released and the sound instantly stops (Release “0”).

      But often a combination of Decay and Sustain is used to generate envelopes that rise up to the Gain level, then grad-
      ually decreases to finally land to rest on a level somewhere in-between zero and the Gain level. Note that Sustain
      represents a level, whereas the other envelope parameters represent times.

      R(elease)
      The Release parameter works just like the Decay parameter, except it determines the time it takes for the volume to
      drop back to zero after you release the key.

      Pan
      D   Set the panning of the output signal from the Amplifier in the stereo panorama.
      q   Since Pan works individually per voice, you can assign e.g. Keyboard Velocity or an Envelope in the Modula-
          tion Bus to control the Pan effect, see “The Modulation Bus section”.

      Gain
      D   Set the desired maximum level for the Amplifier with the Gain knob.
          This is the maximum level the envelope will reach after the Attack stage is completed (see above).
      q   If you want to create a tremolo effect, assign “Gain” as Destination and an LFO as Source in the Modulation
          Bus section, see “The Modulation Bus section”.


=== END OF PART ===
