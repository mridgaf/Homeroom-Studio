# Chapter 09: Reason 12 manual digest and studio workflow
## Part 98 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 89 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 99 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 89 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

       Using Automap
       The automap function can be used as a quick way of creating a key map, or as a good starting point for further ad-
       justments of a key map.
       Automap works under the assumption that you intend to create a key map for a complete instrument, for example a
       number of samples of a piano, all at different pitches.
       1. Load the samples you want to Automap.
           Now you have three options:
       D   Trust that the root note information in the files is already correct.
       D   Manually adjust the root notes (and tuning) for all the samples.
       D   Use “Set Root Notes from Pitch Detection” to automatically set up the root notes.
       2. Select all zones you want to automap.
       3. Select Automap Zones from the Edit menu or the NN-XT context menu.
       All the selected zones will now be arranged automatically in the following way:
       D   The zones will be sorted in the display (from top to bottom - lowest key first) according to the root keys.
       D   The zones will be assigned key ranges according to the root keys.
           The key ranges are set up so that the split between two zones is exactly in the middle between the zones’ root
           notes. If two zones have the same root key they will be assigned the same key range.

       Automapping zones chromatically
       D   This Edit menu item will give each zone a key range of one semitone (i.e. one key), starting from C2 and up-
           wards.
           The function does not take root key into account. It simply places each selected sample on successive keys ac-
           cording the position in the sample list (from the top down).

       Layered, crossfaded and velocity switched sounds
       Creating layered sounds
       You can set things up so that two or more zones have overlapping key ranges - either completely or partially. This way
       you can create layered sounds, i.e. different samples that are played simultaneously when you press a key on your
       keyboard.

       In the picture above, you can see a set of piano samples at the top, mapped across the key range.
       Below these are a set of string samples that also span the entire key range.
       Whenever you play a key within this keyboard range, the sound produced will be a combination of the piano and the
       string sample.
       In addition, in the example above, the user has arranged the piano samples into one group and the string samples in
       another. This is convenient since it allows for quick selection of the entire piano map, for example for balancing its
       level against the strings.

       About velocity ranges
       When zones are set up so that their key ranges overlap – completely or partially – you can use velocity switching and
       crossfading to determine which zones should be played back depending on how hard or soft you play on your MIDI
       keyboard.
       This is done by setting up velocity ranges, with or without crossfading.
       Each time you press a key on your MIDI keyboard, a velocity value between 1-127 is sent to Reason. If you press the
       key softly, a low velocity value is sent and if you press it hard, a high velocity value is sent.
       This velocity value determines which samples will be played and which will not.
       Let’s say for example that you’ve mapped three different zones across the same key range:
       • Zone 1 has a velocity range from 1-40.
         This means that the sample in it will be triggered by velocity values between 1-40.
       • Zone 2 has a velocity range of 41-80.
         The sample in this zone will be played back by velocity values between 41-80.

       • Zone 3 has a velocity range of 81-127.
         The sample in this zone will be triggered by all velocity values above 80.

                127

                100

                 80

                 60

                 40
                                                             Zone 3
                    20
                                                             Zone 2
          Velocity 0                                         Zone 1

       Overlapping velocity ranges
       Let’s change the values above slightly:
       • Zone 1 has a velocity range from 1-60.
       • Zone 2 has a velocity range of 41-100.
       • Zone 3 has a velocity range of 81-127.

              127

              100

               80

               60

               40
                                                          Zone 3
               20
                                                          Zone 2
       Velocity 0                                         Zone 1
       Now, velocity values between 41 and 60 will trigger samples from both Zone 1 and Zone 2. Likewise, velocity values
       between 81 and 100 will trigger sounds from Zone 2 and Zone 3.

       About full and partial velocity ranges
       You can see which zones have modified velocity ranges in the key map display:
       • Zones with a full velocity range (0 - 127) are only shown with an outline.
       • Zones with any other velocity range are shown as striped.

       The top zone has a full velocity range (1-127), and the lower zone has a partial velocity range (any other range), which is indicated by
       stripes

       Sorting Zones by velocity values
       The Edit menu and the NN-XT context menu contain an item called “Sort Zones by Velocity”. This option lets you au-
       tomatically sort the selected zones in the display in descending order according to their set low or high velocity val-
       ues.
       When you invoke this option, the selected zones will be sorted from top to bottom starting with the one with the high-
       est “Lo Vel “value.
       Note however, that the sorting is done strictly on a group basis. That is, only zones that belong to the same group can
       be sorted in relation to each other.
       If two zones have the same velocity range, they are sorted by key range.

       Setting velocity range for a Zone
       To set up a velocity range for a zone, proceed as follows:
       1. Select one or more zones that you want to adjust.
       2. Use the knobs marked “Lo Vel” and “High Vel” in the sample parameter area to set the desired low- and high
          velocity values.

          Adjusting the “Lo Vel” value for a zone.
       “Lo vel” is the lowest velocity value that should trigger the sample in the zone - i.e. if a key is pressed so softly that the
       velocity is lower than this value, the sample will not be played.
       “Hi vel” is the highest velocity value that should trigger the sample, which means that if a key is pressed so hard that
       the velocity is higher than this value, the sample will not be played.

       About Crossfading Between Zones
       At the bottom right in the sample parameter area are two knobs marked “Fade In” and “Fade Out”. These are primarily
       used for setting up velocity crossfades for smooth transitions between overlapping zones. In order to set up cross-
       fades you adjust the fade out and fade in values for the overlapping zones.

       Crossfading Between two Sounds
       An example:
       • Two zones are both set to play in the full velocity range of 1-127.
       • Zone 1 has a fade out value of 40.
         This means that this zone will play at full level with velocity values below 40, With higher velocity values, it will grad-
         ually fade out.
       • Zone 2 has a fade in value of 80.
         This has the effect that as you play velocity values up to 80, this zone will gradually fade in. With velocity values
         above 80, it will play at full level.

              127

              100

               80

               60

               40

               20
                                                             Zone 2
       Velocity 0                                            Zone 1
       Another example:
       Crossfading can be used to only fade in or fade out a certain sound. One common example is to set things up so that
       one sound plays the entire velocity range and another is faded in only at high velocity values.
       • Zone 1 is set to play the entire velocity range with no crossfade.
       • Zone 2 is set to play the velocity range 80 to 127, with a fade in value of 110.
         This means that this zone will start fading in from velocity values 80 and will play at full level in the velocity range
         110 to 127.

              127

              100

               80

               60

               40

               20
                                                             Zone 2
       Velocity 0                                            Zone 1
       This can be used for example to add a rimshot to a regular snare sound or a harder attack to a softer violin sample.

       Setting crossfading for a Zone
       Manually
       To set up a crossfade for a zone, proceed as follows:
       1. Select one or more zones that you want to adjust.
       2. Use the knobs marked “Fade In” and “Fade Out” in the sample parameter area, to set the desired values.

       q   You can change the values with finer precision by pressing [Shift] while turning the knobs, and you can reset
           the standard values by pressing [Command] (Mac)/[Ctrl] (Windows) and clicking on the knobs.

       Automatically
       If you find it tedious to manually set up crossfades between zones, NN-XT can do it for you! The Edit menu and the
       NN-XT context menu contain an item called “Create Velocity Crossfades”.
       1. Set up the zones so that their velocity ranges overlap, as desired.
       2. Select the zones.
           You can select as many zones as you wish, not just one pair of overlapping zones.
       3. Select “Create Velocity Crossfades” from the Edit menu.
           NN-XT will analyze the overlapping zones and automatically set up what it deems to be appropriate fade in and
           fade out values for the zones.
       D   This operation will not work if both zones have full velocity ranges.
           At least one of the zones must have a partial velocity range (see “About full and partial velocity ranges”).
       D   This operation will not work if the zones are completely overlapping.

       Using Alternate
       About the Alternate function

       At the bottom right in the sample parameters area is a knob marked “Alt”. It only has two states - On and Off. This is
       used for semi-randomly alternating between zones during playback.
       There are several practical uses for this. Here follows two examples:
       • Layering several recordings of the same snare drum. By alternating between them you get a more natural rep-
         etition.
       • Layering string up- and down strokes. By alternating you get the realistic effect of switching between the two
         directions of the stroke.

       You can layer as many sounds as you will and the algorithm switches between them in a way that provides as little
       repetition as possible.
       To set up an alternating set of zones, proceed as follows:
       1. Set up the zones so that they overlap completely or partially.
       2. Select them all.
       3. Set “Alt” to On for all the zones.
           Now, the program will automatically detect how to alternate between the zones, depending on their overlap.

       Sample parameters

       The Sample parameter area is found below the screen. They allow you to adjust parameters for one or several se-
       lected zones. Adjusting a parameter with multiple zones selected, will set the parameter to the same value for all se-
       lected zones. Below follows a run-down of the various parameters:

       Root Note and Tune
       These parameters are described in “Setting Root Notes and Tuning”.

       Sample Start and End
       By turning the knobs you offset the start and end positions, so that they will play back more or less of a sample’s
       waveform. Typical examples of use for this would be:
       • Removing unwanted portions from samples.
           This could be anything from noise to “dead air” at the beginning or end of a sample.
       • To create variations out of a single sample.
           These controls can be used to pick out any section of a recording for use as a sample.
       • Together with velocity sample start control.
           You can for example increase Sample Start and then apply negative velocity modulation to Sample Start. Then, the
           harder you play the more you will hear of the attack portion of the sound.
       q   If you hold down [Shift] when adjusting these parameters, the adjustment is in single frames (samples).

       Loop Start and End
       A sample, unlike the cycles of an oscillator for example, is a finite quantity. There is a sample start and end. To get
       samples to play for as long as you press down the keys on your keyboard, they need to be looped. For this to work
       properly, you have to first set up two loop points which determine the part of the sample that will be looped.
       The instrument samples in the sound banks included with Reason are already looped. The same will be true for most
       commercial sample libraries. However, if you need to, you can use these controls to adjust the looping.
       • The size and position of the loop – in the sample – is determined by two parameters, Loop Start (the beginning
         of the loop) and Loop End (the end point of the loop).
       • The NN-XT then keeps repeating the section between the Loop Start and Loop end until the sound has de-
         cayed to silence.

       Play Mode
       By using this knob you can select one of the following loop modes for each zone:
       • FW
           The sample in the zone will play only once, without looping.
       • FW-LOOP
           The sample will play from the sample start point to the loop end point, jump back to the loop start point and then
           loop infinitely between the start and end loop points. This is the most common loop mode.
       • FW - BW
           The sample will play from the sample start point to the loop end point, then from the loop end point to the loop start
           point (backwards), and then loop infinitely forwards-backwards between the start and end loop points.
       • FW-SUS
           This works like FW-LOOP with the exception that it will only loop as long as the key is held down. As you release
           the key, the sample will play to the absolute end of the sample, that is beyond the boundaries of the loop.
           This means that the sound may have a short natural release even if the release parameter is raised to a high value
           (which is not true for “FW-LOOP”, where the release parameter always controls the length of the sound after the
           key is released).
       • BW
           The sample will play only once - from the end to the beginning - without looping.

       Lo Key and Hi Key
       These parameters are described in “Setting up Key Ranges”.

       Lo Vel and Hi Vel
       These parameters are described in “About velocity ranges”.

       Fade In and Fade Out
       These parameters are described in “About Crossfading Between Zones”.

       Alt
       This parameter is described in “About the Alternate function”.

       Out
       The NN-XT features eight separate stereo output pairs (see “Audio Output”). For each zone, you can decide which of
       these output pairs to use. Thus, if you have created a key map consisting of eight zones, each of these can have a
       separate stereo output from NN-XT, and can then be routed to a separate mixer channel if you so wish.
       D   To select which output a selected zone should be directed to, use the knob marked “Out” in the sample param-
           eter area.
           The output pairs are indicated above the button.
       !   Note that you still have to route the outputs the way you want them on NN-XT’s back panel. If you assign a
           zone to an output pair other than 1-2 (which is the default) no connections or auto routing are made. You have
           to do that manually.

       A Stereo example
       One possible way of utilizing this would be to create a drum kit. In this case you could load up to eight different stereo
       drum samples, assign them to separate outputs, route each to a separate mixer channel and then use the mixer to set
       levels and pan, add send effects etc.

       Using a stereo output as two mono outputs
       If, on the other hand, you are using mono samples, you can use one stereo pair as a two separate outputs, effectively
       giving you a total of 16 separate outputs.
       1. Assign two zones to the same output.
       2. Us the Pan control to pan one of the zones hard left and the other hard right.
       3. Connect each of the two outputs in the stereo pair to a separate mixer channel.

       Group parameters

       The group parameters are located at the top left on the remote editor panel. These are parameters that in various
       ways are directly related to playing style.
       Group parameters apply to a group, that is they are settings that are shared by all zones in a group.
       D   To make adjustments to one group, select one or more zones that belong to the group, and adjust the param-
           eter on the front panel.
       D   To set several groups to the same value, select at least one zone in each group you want to adjust, and adjust
           the parameter on the front panel.

       Key Poly
       This setting determines the number of keys that you can play simultaneously (the polyphony). The maximum number
       is 99 and the minimum is 1, in which case the group will be monophonic.
       Users of other samplers may want to note that the polyphony often means setting the number of voices that should
       be able to play. The NN-XT is different in this aspect, since the polyphony setting instead determines the number of
       keys, regardless of how many voices each key plays.

       The Group Mono button
       The Group Mono button beside the Key Poly section can be used to quickly set a group to play monophonically re-
       gardless of the polyphony setting. E.g. if you have a group with open and closed hi hats, you can switch this on so that
       an open hi hat is automatically muted when you play a closed hi hat.
       Group Mono overrides the Key Poly setting - except when playing the same note.

       So you can play your open hi-hat repeatedly without the sound cutting itself off. When you play the closed hi-hat, this
       cuts off the open hi-hat.
       Note that activating this button is not the same as setting polyphony to 1. E.g., it can not be used for Legato or mono
       Retrig (see “Legato and Retrig”).

       Legato and Retrig
       Legato
       Legato works best with monophonic sounds. Set Key Poly (see above) to 1 and try the following:
       D   Hold down a key and then press another key without releasing the previous.
           Notice that the pitch changes, but the envelopes do not start over. That is, there will be no new “attack”.
       D   If Key Poly is set to more voices than 1, Legato will only be applied when all the assigned keys are “used up”.
           For example, if you had a polyphony setting of “4” and you held down a 4 note chord, the next note you played
           would be Legato. Note, however, that this Legato key will “steal” one of the keys in the 4 note chord, as all the as-
           signed keys were already used up!

       Retrig
       Retrig is the “normal” setting for playing polyphonic patches. That is, when you press a key without releasing the pre-
       vious, the envelopes are triggered, like when you release all keys and then press a new one. In monophonic mode,
       Retrig has an additional function; if you press a key, hold it, press a new key and then release that, the first note is
       also retriggered.

       LFO 1 Rate
       This is used for controlling the rate of LFO 1 if it is used in “Group Rate” mode. In that case, this knob will take pre-
       cedence over the rate parameter in the LFO 1 section. See “The LFOs” for detailed information about this.

       Portamento
       This is used for controlling portamento - a parameter that makes the pitch glide between the notes you play, rather
       than changing the pitch instantly as soon as you hit a key on your keyboard. By turning this knob you set how long it
       should take for the pitch to glide from one note to the next as you play them.
       In legato mode, there will only be any portamento when actually playing legato (tied) notes.
       With the knob turned all the way to the left, portamento is disabled.

       Synth parameters
       The Modulation controls

       As previously described, the Modulation wheel (and the External Control wheel) can be used for controlling various
       parameters. These controls allow you to define which parameters the wheels should modulate and to what extent.
       D   Below each of the knobs are the letters “W” and “X”.
           These are used for selecting the source that should control the parameter, and represent the “Modulation Wheel”
           and the “External Control wheel” respectively.
       D   By clicking on any of the letters, you decide which source should control the parameter.
           You can select either, both or none. When a letter is “lit”, the corresponding source is set to control the parameter.
       D   By turning the knobs, you decide how much the modulation and/or external control wheel should modulate
           the corresponding parameter.
       Note that all of the control knobs are bi-polar, which means that they can be set to both positive and negative values.
       Positive values are set by turning the knobs to the right, and negative values are thus set by turning the knobs to the
       left:
       • Setting them to positive values means that the value of the controlled parameter will be raised if the source
         wheel is pushed forward.
       • Setting them to negative values means that the value will be lowered when a wheel is pushed forward.
       • Keeping the knobs in the center position means that no modulation control is applied.
       There is one exception to these rules, and that is the LFO 1 Amt control, which works in a slightly different way. See
       below for more information about this.
       The following parameters can be modulated:

       F.Freq
       This sets modulation control of the Filter’s cutoff frequency (see “The Filter section”).


=== END OF PART ===
