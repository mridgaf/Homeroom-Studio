# Chapter 09: Reason 12 manual digest and studio workflow
## Part 99 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 90 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 100 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 90 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

       Mod Dec
       This sets modulation control of the Decay parameter in the Modulation Envelope (see “The Modulation Envelope”).

       LFO 1 Amt
       This determines how much the amount of modulation from LFO 1 is affected by the Modulation wheel and/or the Ex-
       ternal Controller wheel. It does this by “scaling” the amounts set with the three destination knobs in the LFO 1 section
       (Pitch, Filter and Level, see “The LFOs”). We’ll explain this with an example:
       To use the Modulation Wheel to increase pitch modulation (vibrato), proceed as follows:
       1. Turn the Mod Wheel all the way down, so that no modulation is applied.
       2. Activate the “W” button for LFO 1 Amt in the Modulation section.
       3. Set the corresponding knob to “12 o’clock” (zero).
       4. Set up LFO 1 so that as much vibrato is applied as you want it to be when the Modulation wheel is turned all
          the way up.
       5. Increase LFO 1 Amt until you hear as much vibrato as you want it to be when the wheel is turned all the way
          down.
         If you turn LFO 1 Amt all the way up, there will be no vibrato at all when the wheel is all the way down.
       To instead use the Modulation wheel to decrease vibrato, process as follows:
       1. Turn the Mod Wheel all the way down, so that no modulation is applied.
       2. Activate the “W” button for LFO 1 Amt in the Modulation section.
       3. Set the corresponding knob to “12 o’clock” (zero).
       4. Set up LFO 1 so that as much vibrato is applied as you want it to be when the Modulation wheel is turned all
          the way down.
       5. Turn the Modulation wheel all the way up.
       6. Decrease LFO 1 Amt until you hear as much vibrato as you want it to be when the wheel is turned all the way
          up.
         If you turn LFO 1 Amt all the way down, there will be no vibrato at all when the wheel is all the way up.

       F.Res
       This sets modulation control of the Resonance parameter in the Filter (see “The Filter section”).

       Level
       This sets the amount of amplitude envelope modulation of each zone’s level. The level set here will be the level of the
       highest point of the Amp Envelope.

       LFO 1 Rate
       This sets modulation control of the Rate parameter in LFO 1 (see “The LFOs”).

       The Velocity controls

       Velocity is used for controlling various parameters according to how hard or soft you play notes on your keyboard. A
       typical use of velocity control is to make sounds brighter and louder if you strike a key harder. By using the knobs in
       this section, you can control if and how much the various parameters will be affected by velocity.
       Just like the modulation controls, all of the velocity control knobs are bi-polar, and can be set to both positive and
       negative values.
       • Setting them to positive values means that the value of the controlled parameter will be raised the harder you
         play.
       • Setting them to negative values means that the value will be lowered the harder you play.
       • Keeping the knobs in the center position means that no velocity control is applied.
       The following parameters can be velocity controlled:

       F.Freq
       This sets velocity control of the Filter’s cutoff frequency (see “The Filter section”).

       Mod Dec
       This sets velocity control of the Decay parameter in the Modulation Envelope (see “The Modulation Envelope”).

       Level
       This sets velocity control of the Amp Envelope.

       Amp Env Attack
       This sets velocity control of the Attack parameter in the Amplitude Envelope (see “The Amplitude Envelope”).

       Sample Start
       This sets velocity control of the Sample Start parameter (see “Sample Start and End”), so that it will be offset for-
       wards or backwards, according to how hard or soft you play.
       This allows you to control how much of the attack portion of the sample you hear when playing harder or softer.
       To be able to make use of negative values for this parameter, you must increase the sample parameter Sample Start.

       The Pitch section

       This section contains various parameters related to controlling the pitch, or frequency, of the zones.

       Pitch Bend Range
       This lets you set the amount of pitch bend, i.e. how much the pitch changes when your turn the pitch bend wheel fully
       up or down. The maximum range is +/- 24 semitones (2 Octaves).

       Setting the pitch
       Use the three knobs marked “Octave”, “Semi” and “Fine” to change the pitch of the sample(s):
       • Octave
         This changes the pitch in steps of one full octave. The range is -5 – 0 – 5.
       • Semi
         This lets you change the pitch in semitone steps. The range is -12 – 0 – 12 (2 octaves).
       • Fine
         This changes the pitch in cents (hundredths of a semitone). The range is -50 – 0 – 50 (down or up half a semi-
         tone).

       K. Track
       This knob controls Keyboard Tracking of the pitch.
       • In the center position, each key represents a semitone This is the normal setting.
       • When turned all the way down, all keys play the same pitch. This can be useful for percussion like timpani
         where you might want to play the same pitch from a range of keys.
       • When turned all the way up, each key on the keyboard shifts the pitch one octave.

       The Filter section

       Filters can be used for shaping the character of the sound. The filter in NN-XT is a multimode filter with six different
       filter types.
       D   To activate/deactivate the filter, click the On/Off button in the top right corner.
           When the filter is activated, the button is lit.

       Filter mode
       To select a filter mode, either click the Mode button in the bottom right corner or click directly on the desired filter
       name so that it lights up:
       • Notch
           The notch filter is used for cutting off frequencies in a narrow frequency range around the set cutoff frequency,
           while letting the frequencies below and above through.
       • HP 12
           This is a highpass filter with a 12 dB/Octave roll-off slope. A highpass filter cuts off low frequencies and lets high
           frequencies pass. That is, frequencies below the cutoff frequency are cut off and frequencies above it pass
           through.
       • BP 12
           This is a bandpass filter with a 12 dB/Octave roll-off slope. A bandpass filter could be viewed as the opposite of
           a notch filter. It cuts off both the high and the low frequencies, while frequencies in the band range pass through.
       • LP 6
           This is a lowpass filter with a gentle, 6 dB/Octave slope. A lowpass filter is the opposite of a highpass filter. It lets
           the low frequencies through and filters out the high frequencies. This filter has no Resonance.
       • LP 12
           This is a lowpass filter with a 12 dB/Octave roll-off slope.
       • LP 24
           This is a lowpass filter with a fairly steep roll-off slope of 24 dB/Octave.

       Filter controls
       The following filter controls are available:
       • Freq
           This is used for setting the filter cutoff frequency. The cutoff frequency determines the limit above or below which
           frequencies will be cut off depending on the selected filter type. In the case of a lowpass filter for example, fre-
           quencies below the cutoff frequency will be allowed to pass through, while frequencies above it will be cut off. The
           farther to the right you turn the knob, the higher the cutoff frequency will be.
       q   It is very common to modulate filter frequency with the modulation envelope, as described in “The Modulation
           Envelope”.
       • Res
           Technically, this knob controls feedback of the output signal from the filter, back to its input. Acoustically it empha-
           sizes frequencies around the cutoff frequency. For a lowpass filter for example, increasing Res will make the
           sound increasingly more hollow until the sound starts “ringing”. If you set a high value for the Res parameter and
           then vary the filter frequency, this will produce a classic synthesizer filter sweep.
           For the notch and bandpass filter types, the Resonance setting instead adjusts the width of the band. That is, the
           higher the resonance setting, the narrower the band will be where frequencies are cut off (notch) or let through
           (Bandpass).
       • K. Track
           This lets you activate and control keyboard tracking of the filter frequency. If keyboard tracking is activated, the set
           cutoff frequency of the filter will change according to the notes you play on your keyboard. That is, if you play notes
           higher up on the keyboard, the filter frequency will be raised and vice versa.
           When the knob is set to its center position, filter frequency is adjusted so that the harmonic content remains con-
           stant across the keyboard.
           Keyboard tracking is deactivated by default (the knob all the way to the left). This means that the filter frequency
           will remain unchanged regardless of where on the keyboard you play.

       The Modulation Envelope

       The Modulation Envelope parameters let you control how certain parameters, or destinations, should change over
       time - from the moment a note is struck to the moment it is released again.
       The destinations you can use are:
       • Pitch
       • Filter frequency

       Parameters
       The following are the available controlling parameters:
       • Attack
         When you press a key on your keyboard, the envelope is triggered. The attack parameter then controls how long
         it should take before the controlled parameter (pitch or filter) reaches the maximum value, when you press a key.
         By setting attack to a value of “0”, the destination parameter would reach the maximum value instantly. By raising
         the attack parameter, the value will instead slowly “slide” up to its maximum.
       • Hold
         This is used for deciding how long the controlled parameter should stay at its maximum value before starting to
         decrease again. This can be used in combination with the Attack and Decay parameters to make a value reach its
         maximum level, stay there for a while (hold) and then start dropping gradually down to the sustain level.
       • Decay
         After the maximum value for a destination has been reached and the Hold time has expired, the controlled param-
         eter will start to gradually drop down to the sustain level. How long it should take before it reaches the sustain level
         is controlled with the Decay parameter. If Decay is set to “0”, the value will immediately drop down to the sustain
         level.
       • Sustain
         The Sustain parameter determines the value the envelope should drop back to after the Decay. If you set Sustain
         to full level however, the Decay setting doesn’t matter since the value will never decrease.
         A combination of Decay and Sustain can be used for creating envelopes that rise up to the maximum value, then
         gradually decrease to, and stay on a level somewhere in-between zero and maximum.
       • Release
         This works just like the Decay parameter, with the exception that it determines the time it takes for the value to fall
         back to zero after the key is released.
       • Delay
         This is used for setting a delay between when a note is played and when the effect of the envelope starts. That is,
         the sound will start unmodulated, and the envelope will kick in after you have kept the key(s) pressed down for a
         while. Turn the knob to the right to increase the delay time. If the knob is set all the way to the left, there will be no
         delay.
       • Key To Decay
         By using this, you can cause the value of the Decay parameter (see above) to be offset depending on where on
         your keyboard you play. If you turn the knob to the right the decay value will be raised the higher up you play, and
         turning the knob to the left will lower the decay value the higher up you play. With the knob in the center position,
         this parameter is deactivated.

       Destinations
       The following are the available Mod Envelope destinations:
       • Pitch
         This will make the envelope modulate the pitch, as set in the Pitch section (see “The Pitch section”). Turn the knob
         to the right to raise the pitch and to the left to lower the pitch. In the middle position, pitch will not be affected by
         the envelope.
       • Filter
         This will make the envelope modulate the cutoff frequency of the Filter (see “The Filter section”). Turn the knob to
         the right to increase the frequency and to the left to lower the frequency. In the middle position, the envelope will
         have no effect on the cutoff frequency.

       The Amplitude Envelope

       The Amplitude Envelope parameters let you control how the volume of a sound should change over time - from the
       moment a note is struck to the moment it is released again.

       Parameters
       Most of the Amplitude Envelope parameters are identical to those of the Modulation Envelope. So for a detailed de-
       scription of the following parameters, please refer to the modulation envelope section in “The Modulation Envelope”:
       • Attack
       • Hold
       • Decay
       • Sustain
       • Release
       • Delay
       • Key To Decay
       The following are the parameters that are unique for the Amp Envelope section:
       • Level
         This knob sets the level of the zone. Turn it to the right to raise the level.
       • Spread and Pan modes
         These two parameters are used for controlling the stereo (pan) position of the sound. The Spread knob deter-
         mines the sound’s width in the stereo image (how far left – right the notes will be spread out). If this is set to “0”,
         no spread will take place. The Mode selector switch is used for choosing which type of spread you want to apply:

       | Mode        | Description
       Key            This will make the pan position shift gradually from left to right, the higher up on the keyboard you play.
       Key 2          This will make the pan position shift from left to right and then back again from right to left in a sequence of eight keys.
                      Playing 4 adjacent semitones thus makes the pan position gradually go from left to right. The next 4 higher semitone notes
                      will then change the pan position from right to left in the same way, and this cycle will then be repeated.
       Jump           This will make the pan position jump between left and right each time a note is played.

       • Pan
         This controls the stereo balance of the output pair to which a zone is routed. In the middle position, the signal ap-
         pears equally strong on the left and right channel in a stereo pair. By turning the knob to the left or right, you can
         change the stereo balance.
       Note that if you for instance turn the Pan knob all the way to the left, you cause the signal to be output from the left
       channel of the stereo pair only.
       You can use this to treat a stereo output as two independent mono outputs, if required.
       See “Out” for information on routing zones to output pairs.

       The LFOs

       NN-XT features two Low Frequency Oscillators - LFO 1 and LFO 2. “Normal” oscillators generate a waveform and a
       frequency, and produce sound. Low frequency Oscillators on the other hand, also generate a waveform and a fre-
       quency, but there are two major differences:
       • LFOs only generate sounds of a low frequency.
       • LFOs don’t produce sound, but are instead used for modulating various parameters.
       The most typical use of an LFO is to modulate the pitch of a sound (generated by an oscillator or - in the case of NN-
       XT - a sample), to produce vibrato.

       About the Difference between LFO 1 and LFO 2
       There are two fundamental differences between LFO 1 and LFO 2:
       • LFO 2 is always key synced, that is, each time you press a key, the LFO waveform starts over from scratch. LFO
         1 can be switched between key synced and non-key synced modes.
       • LFO 2 only has one waveform, triangle.
       The following parameters are available for the LFOs:

       Rate (LFO 1 and 2)
       This knob controls the frequency of the LFO. For a faster modulation rate, turn the knob to the right. The Rate knob
       of LFO 1 is also used for setting the timedivision when synchronizing the LFO to the song tempo (see below).

       Delay (LFO 1 and 2)
       This can be used for setting a delay between when a note is played and when the LFO modulation starts kicking in
       (gradually). This way, you can make the sound start unmodulated, and then have the LFO modulation start after you
       have kept the key(s) pressed down for a while.
       Turn the knob to the right to increase the delay time.

       Mode (LFO 1 only)
       This lets you set the “operation mode” for the LFO. Click the button to switch between the available modes:
       • Group Rate
             In this mode, the LFO will run at the rate set for its group in the group section, rather than at the rate set here (see
             “Group parameters”). This way, all zones in the group will have the exact same modulation rate.
       • Tempo Sync
             In this mode, the LFO will be synchronized to the song tempo, in one of 16 possible time divisions.
       !     When tempo sync is activated, the Rate knob is used for selecting the desired timedivision. Turn the Rate knob
             and observe the tool tip for an indication of the timedivision.
       • Free Run
             In free run mode, the LFO simply runs at the rate set with the Rate parameter. Furthermore, if Key Sync is deacti-
             vated, the modulation cycle will not be retriggered each time you press a key - it will run continuously.

       Waveform (LFO 1 only)
       Here, you select which type of waveform should be used for modulating the destination parameters.
       Click the button to switch between the following waveforms:

       | Waveform                    | Description
           Triangle                   This is a smooth waveform, suitable for normal vibrato.

           Inverted Sawtooth          This produces a “ramp up” cycle. If applied to an oscillator’s frequency, the pitch would sweep up,
                                      after which the cycle immediately starts over.
           Sawtooth                   This produces a “ramp down” cycle, the same as above but inverted.

           Square                     This produces cycles that abruptly change between two values, usable for trills etc.

           Random                     Produces random stepped modulation to the destination. Some vintage analog synths called this
                                      feature “sample & hold”.
           Soft Random                The same as above, but with smooth modulation.

       !     LFO 2 always uses a triangle waveform.

       Key Sync (LFO 1 only)
       By activating key sync, you “force” the LFO to restart its modulation cycle each time a key is pressed.
       !     Note that LFO 2 always uses Key Sync.

       Destinations for LFO 1
       The following parameters can be modulated by LFO 1:
       • Pitch
         This will make the LFO modulate the pitch, for vibrato, trills, etc. It can be set to -2400 – 0 – 2400 cents which
         equals 4 octaves. The set pitch will change up and down by this amount, with each modulation cycle. Turning the
         knob to the right will make the modulation cycle start above the set pitch, while turning it to the left will invert the
         cycle. Keeping this in the middle position means that the pitch will not be affected by the LFO.
       • Filter
         This will make the LFO modulate the cutoff frequency of the Filter, for auto-wah effects, etc. The positive/negative
         effect is the same as for pitch.
       • Level
         This will make the LFO modulate NN-XT’s output level, for tremolo effects, etc. The positive/negative effect is the
         same as for pitch.

       Destinations for LFO 2
       The following parameters can be modulated by LFO 2:
       • Pan
         This makes the LFO modulate the pan position of a zone. The sound will move back and forth in the stereo field.
         Turning the knob to the left makes the sound move from left to right, and turning it to the right thus makes it move
         from right to left. The middle position provides no modulation at all.
       • Pitch
         Just like for LFO 1 (see above), this makes LFO 2 modulate the pitch. The range is also the same as for LFO 1.

       Connections
       On the back panel of NN-XT are a number of connectors. Many of these are CV/Gate related. Using CV/Gate is de-
       scribed in the chapter “Routing Audio and CV”.

       Sequencer Control
       The Sequencer Control CV and Gate inputs allow you to play the NN-XT from another CV/Gate device (typically a
       Matrix or a Redrum). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note
       on/off along with velocity.

       Modulation Input
       These control voltage (CV) inputs (with associated voltage trim pots), can modulate various NN-XT parameters from
       other devices. These inputs can control the following parameters:
       • Oscillator Pitch
       • Filter Cutoff Frequency
       • Filter Resonance
       • LFO 1 Rate
       • Master Volume
       • Pan
       • Modulation Wheel
       • Pitch Wheel

       Gate Input
       These inputs can receive a CV signal to trigger the following envelopes:
       • Amplitude Envelope
       • Modulation Envelope
       Note that connecting to these inputs will override the normal triggering of the envelopes. For example, if you connect
       a Matrix Gate Out to the Gate In Amp Envelope, you would not trigger the amp envelope by playing notes, as this is
       now controlled by the Matrix Gate Out. In addition you would only hear the Gate Out triggering the envelope for the
       notes that you hold down.

       Audio Output
       There are 16 audio output jacks on the NN-XT’s back panel - eight separate stereo pairs. When you create a new
       NN-XT device, the first output pair (1L & 2R) is auto-routed to the first available channel on the audio mixer.

       The other output pairs are never automatically routed. If you wish to use any of the other output pairs, you have to
       manually connect them to the desired device - typically a Mix Channel device. The basics on Routing is described in
       “Routing Audio and CV”.
       !   Note that when you use any other output pair than the first, you also have to route one or more zones to it if
           you want it to actually output sound, since all zones by default are routed to outputs 1 & 2. How to route zones
           to other outputs is described in the “Out” section.


---

<a id="nn-19-sampler-44"></a>

=== END OF PART ===
