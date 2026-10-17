# Chapter 09: Reason 12 manual digest and studio workflow
## Part 96 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 87 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 97 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 87 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 43: NN-XT Sampler

NN-XT Sampler

       Introduction
       The basic functions of the NN-XT are very similar to those of its sampler companion in the Reason rack - the NN-19
       (see “NN-19 Sampler”). Just like the NN-19, NN-XT lets you load samples and create multi-sample patches by map-
       ping samples across the keyboard. The sound can then be modified by a comprehensive set of synth-type parame-
       ters. There are however some major differences between the two. The NN-XT has:
       D   Support for SoundFonts.
           Presets and samples from SoundFont banks can be loaded and used in the NN-XT (see “Loading SoundFonts”).
       D   8 stereo output pairs.
           This makes it possible to route different samples to different mixer channels for individual effect processing (see
           “Out”).
       D   The possibility to create layered sounds.
           This is done by mapping several samples across the same keyboard range (see “Creating layered sounds”).
       D   The possibility to create sounds that only play over certain velocity ranges, velocity switched key maps and ve-
           locity crossfading.
           See “Setting velocity range for a Zone”.
       D   Key maps with individual synth parameter settings for each sample.
           See “Synth parameters”.
       Even though the NN-XT is a more advanced sample player than NN-19, it should not be considered as a successor
       to the NN-19, but rather as a complement to it. The NN-19 will for example probably still be the sampler of choice for
       those of you who want to be able to quickly load a couple of samples and start playing, since that particular aspect
       takes a little more doing with the NN-XT.

       Sampling in NN-XT
       The sampling procedure is generic for all devices that can sample (NN-19, NN-XT, Redrum and Kong). The sampling
       and sample editing procedures are described in detail in the “Sampling” chapter.
       D   To sample your own sound and automatically load it into the NN-XT device, click the Sample button.

           Refer to the “Sampling” chapter for details on how to set up and use the sampling feature.

       Panel overview
       The main panel
       When the NN-XT is added to the rack, you will initially only see the main panel.

       The NN-XT main panel.
       The main panel is where you load complete sample patches. It also contains the “global controls”. These are controls
       that affect and modify the sound of entire patches rather than the individual key zones.

       The Remote Editor panel
       To show/hide the remote editor panel, use the fold/unfold arrow at the bottom left.

           Remote
           Editor
           Fold/Unfold
           button

       The remote editor panel is where you load individual samples, create key maps, modify the sound of the samples with
       synth parameters etc.
       !    The main panel of the NN-XT can be folded like any other Reason device. Note that folding the main panel will
            also fold the remote editor regardless of its current state.

       Loading complete Patches and REX files
       As previously alluded, you can load complete sample patches as well as individual samples into the NN-XT.
       • A patch is a complete “sound package”. It contains information about all the samples used, assigned key
         zones, associated panel settings etc. Loading a sample patch is done by using the patch browser on the main
         panel, and works in the same way as with any other Reason device.

           The Browse Patch button on the main panel.
       For general instructions on how to load and save patches, please see “Loading patches” and “Saving patches”.
       • Loading separate samples is done in a similar way, but via the sample browser on the remote editor panel. If
         you load samples, map them across keyboard ranges and set up the sound the way you want it, you can save
         your settings as a Patch for easy access later.

           The Browse Sample button on the remote editor.
       More about loading samples later in this chapter.

       Loading NN-XT Patches
       NN-XT Patches are patches made specifically for the NN-XT. Reason ships with a large number of NN-XT Patches,
       some in the Factory Sound Bank but most in the Orkester Sound Bank. NN-XT Patches have the extension “.sxt”.
       1. Click the Browse Patch button on the front panel to set browse focus to the NN-XT device.
       2. Navigate to the folder that contains the NN-XT patch you wish to load, select it and click Load in the Browser.
       D   Alternatively, drag an NN-XT patch from the Browser and drop it on the NN-XT device in the rack.
           The panel is dimmed in orange and the Patch Replace symbol appears in the center.

       Loading NN-19 Patches
       NN-19 Patches have the extension “.smp”. Note that when loading NN-19 patches into the NN-XT, some parameters
       will not be applicable since the NN-19 and the NN-XT to some extent differ from each other in terms of controls. In
       these cases, the concerned parameters will either be ignored by the NN-XT or mapped to the most equivalent con-
       trol.
       1. Click the Browse Patch button on the front panel to set browse focus to the NN-XT device.
       2. Navigate to the folder that contains the NN-19 patch you wish to load, select it and click Load in the Browser.
       D   Alternatively, drag an NN-19 patch from the Browser and drop it on the NN-XT device in the rack.
           The panel is dimmed in orange and the Patch Replace symbol appears in the center.

       Loading SoundFonts
       The SoundFont format was developed by E-mu systems in collaboration with Creative Technologies. It is a standard-
       ized data format containing wavetable synthesized audio and information on how it should be played back in wavet-
       able synthesizers - typically on audio cards. The SoundFont format is an open standard so there is a vast amount of
       SoundFont banks and SoundFont compatible banks developed by third parties.
       Loading SoundFonts is no different from loading NN-XT Patches. As with NN-19 Patches, the NN-XT does its best
       to map all the SoundFont settings to NN-XT parameters.
       You can load SoundFont presets by using the patch browser, and single SoundFont samples by using the sample
       browser.

       Loading complete REX files as Patches
       REX files are music loops created in the ReCycle program or when editing audio clips inline in Reason (see “Bounce
       Clip to REX Loop”). In Reason, REX files are primarily used in the Dr. Octo Rex loop player, but they can be used in
       the NN-XT as well. Possible extensions are “.rx2”, “.rcy” and “.rex”.
       1. Click the Browse Patch button on the front panel to set browse focus to the NN-XT device.
       2. Navigate to the folder that contains the REX loop you wish to load, select it and click Load in the Browser.
       D   Alternatively, drag a REX loop from the Browser and drop it on the NN-XT device in the rack.
           The panel is dimmed in orange and the Patch Replace symbol appears in the center.
           When loading a REX file, each slice in the file is assigned to one key, chromatically, starting from C1. All parame-
           ters are set to their default settings.
       When using REX files in the Dr. Octo Rex loop player, it is possible to make a track play the slices in order to recreate
       the original loop. To do the same in the NN-XT requires a few extra steps.
       1. Use the Browser to load the REX file into an NN-XT sampler.
       2. Create a Dr. Octo Rex loop player and load the same REX file into a Loop Slot of this device.
       3. Use the Copy Loop To Track feature on the Dr. Octo Rex to create playback data (a group) on the track as-
          signed to the Dr. Octo Rex.
       4. Move that group to the track that plays the NN-XT and play it back from there.
       5. Delete the Dr. Octo Rex loop player.

       Using the main panel
       All of the controls on the main panel are used for globally modifying certain parameters for all of the samples in a
       patch, by the same amount.
       !   Movements of the parameters on the main panel can be recorded as automation. However, controls on the re-
           mote editor panel (described later) can not!
       The following is a description of the controls and parameters on the main panel.

       The Pitch and Modulation wheels

       Most MIDI keyboards come equipped with Pitch Bend and Modulation wheels. The NN-XT features settings for how
       incoming MIDI Pitch Bend and Modulation wheel messages should affect the sound. The wheels on the NN-XT will
       also mirror the movements of the wheels on your MIDI keyboard.
       If you don’t have Pitch Bend or Modulation controls on your keyboard, or if you aren’t using a keyboard at all, you can
       use the two fully functional wheels on the NN-XT to apply real time modulation and pitch bend.
       • The Pitch Bend wheel is used for “bending” the played notes up and down to change their pitch - much like
         bending the strings on a guitar or other string instrument. The Pitch Bend Range is set on the remote editor
         panel (see “Pitch Bend Range”).
       • The Modulation wheel can be used for applying modulation to the sound while you’re playing. It can also be
         used for controlling a number of other parameters, as described in “The Modulation controls”.

       The External Control wheel

       This section can be used in three ways:

       Receiving MIDI controller messages from external sources
       NN-XT can receive common MIDI controller messages, and route these to various parameters. You use the “Source”
       selector switch to determine which type of message should be received:
       • Aftertouch (Channel Pressure)

       • Expression Pedal
       • Breath Control
       If your MIDI keyboard is capable of sending aftertouch messages, and/or if you have connected an expression pedal
       or a breath controller to it, you can use these to modulate NN-XT parameters. Which parameters should be modu-
       lated is set in the remote editor panel (see “The Modulation controls”).

       Recording MIDI controller messages with the wheel
       The wheel in the external control section can be used for recording any or all of the three MIDI controller message
       types into the Reason sequencer. If your MIDI keyboard isn’t capable of sending aftertouch messages or you don’t
       have access to an expression pedal or a breath controller, you can use the wheel instead.
       This is done just as with any other automation recording, see “Recording performance controller automation”.

       High Quality Interpolation

       This switch turns High Quality Interpolation on and off. When it is activated, the sample pitch is calculated using a
       more advanced interpolation algorithm. This results in better audio quality, especially for samples with a lot of high
       frequency content.
       • High Quality Interpolation uses more computer power - so if you don’t need it, it’s a good idea to turn it off! Lis-
         ten to the sounds in a context and determine whether you think this setting makes any difference.

       Global Controls

       All of these knobs change the values of various parameters in the remote editor panel and affect all loaded samples.
       Thus they can be used for quickly adjusting the overall sound.
       The knobs are bi-polar, which means that when they are centered, no parameter change is applied. By turning them
       to the right you increase the corresponding value, and by turning them to the left, you decrease the value.
       Again, the movements of these parameters can be recorded as automation. This is done just as with any other auto-
       mation recording, see “Recording parameter automation”.
       The controls are, from left to right:

       Filter
       These two knobs each control a parameter of the filter (see “The Filter section”). Note that the filter must be on for
       these to have any effect.
       • Frequency
         This changes the cutoff frequency of the filter.
       • Resonance
         This changes the resonance parameter of the filter, meaning - the filter characteristic, or quality.

       Amp Envelope
       These three knobs control the Amplitude Envelope (see “The Amplitude Envelope”) in the following way:
       • Attack
         This changes the Attack value of the Amplitude Envelope. That is, how long it should take for the sound to reach
         full level after you press a key on your keyboard.
       • Decay
         This changes the Decay value of the Amplitude Envelope. Decay determines how long it should take for the sound
         to go back to the sustain level after it has reached full value (see “The Amplitude Envelope”) and the key that trig-
         gered the sound is still being pressed.
       • Release
         This changes the Release value of the Amplitude Envelope. Release works just like Decay with the exception that
         it determines how long it should take for the sound to become silent after the key has been released.

       Mod Envelope
         This knob controls the Decay value of the Modulation Envelope (see “The Modulation Envelope”). Also see above
         for a brief description of Decay.

       Master Volume
       This controls the main volume out from the NN-XT. Turn the knob to the right to increase the volume.

       Overview of the Remote Editor panel
       It is in the Remote Editor Panel that the main NN-XT action is going on, especially if you’re creating your own
       patches. The remote editor is dominated by the key map display, and this is also the part on which we will concentrate
       to begin with.

       The Key Map display
       The key map display consists of a number of separate areas that let you do different things. To help you navigate the
       key map display, these areas are described below.
                                        The Keyboard area               The Tab Bar area
       The Info
       area                                                                                               The Scrollbars

       The Sample
       area

       The Group
       area

                                                                   The Key Range area

       The Info area
       This displays the following information about the currently selected sample: Sample rate, mono/stereo information,
       bit resolution and file size.

       The Sample area
       This area displays the names of the samples in each zone. It also allows you to change the order of the zones by
       clicking and dragging them up and down.

       The Group area
       This area does not show any information. However, by clicking in it, you can instantly select all the zones that belong
       to a certain group. See “Working with Grouping” for information on how to create groups.

       The Keyboard area
       Aside from the fact that is a guideline for setting up key ranges, it is also used for setting the root keys of, and audi-
       tioning loaded samples. See “About the Root Key” and “Auditioning samples” respectively for more information.

       The Tab Bar area
       This area gives you a visual indication of the key range of a selected zone. By clicking and dragging the “handles” at
       the key range boundaries, you can resize the key ranges, and by clicking in between the handles, you can move the
       key ranges without changing their length.

       The Key Range area
       This area in the middle of the key map display is where you keep track of all the zones and the relationship between
       them. You can also move and resize the zones just like in the Tab Bar area, as described above.

       The Scrollbars
       There are both horizontal and vertical scrollbars that work just like regular scrollbars. Whenever there is more infor-
       mation in the key map display than what fits on a “single screen”, you can use the scrollbars to reveal it. Either click
       on the arrows or click and drag the scrollbar handles.

       Sample parameters

       This area shows the current values of basic parameters you can set for zones, such as root key, play mode, output
       etc. The parameters are changed by using the knobs directly below the key map display.

       Group parameters

       These parameters are adjusted on a per group basis (see “Group parameters” for more information on groups). Most
       of them relate to performance or playing style.

       Synth Parameters

       The bulk of the parameters on the remote editor are used for adjusting the sound of the samples by applying filtering,
       envelope shaping, modulation (like vibrato and tremolo) and so on. We call these the synth parameters, since they are
       to a large extent identical to those on a regular synthesizer.

       About Samples and Zones
       For a clear understanding of the terminology used when describing the various operations that can be performed in
       the key map display, it is important to clarify the distinction between a sample and a zone:
       • A Sample is a piece of audio that can be loaded into the NN-XT and played back.
       • A Zone could be viewed as a “container” for a loaded sample.
       All loaded samples are placed in “Zones” in the key map display. You can then organize the zones as you please, and
       make various settings such as key- and velocity ranges separately for each zone.
       In other words, the settings you make are actually performed on the zones, but affect the samples in them. Hence,
       when we talk about making settings for a zone, it is synonymous with making settings for a sample - the sample that
       the zone contains.
       • Two or more zones can play the same sample, but with different parameter settings, making them sound com-
         pletely different.
       • A zone can be empty, playing no sample at all.

       Selections and Edit Focus
       Almost all operations in the remote editor are performed on one or more selected zones or on the zone with edit fo-
       cus. Several zones can be selected at once, but only one zone at a time can have edit focus.
       This is important since:
       • Editing operations that can be performed on several zones (like deleting), always apply to the selected zones.
       • Editing operations that can be performed on one zone only, always apply to the zone with edit focus.
       • The front panel always shows the settings for the zone with edit focus.

       Here no zone is selected.

       Here the middle zone is selected but does not have edit focus.

       Here the middle zone has edit focus but is not selected. Notice the thicker border and the additional handles in the key range area.

       Here the middle zone is selected and has edit focus.

       Here, all three zones are selected, but the middle one has edit focus.

       Selecting Zones
       D   To select a zone, click on it.
           Clicking on a zone will also automatically give it edit focus.
       You can also select multiple zones in several ways:
       D   By holding down [Shift], or [Ctrl](Win) or [Cmd](Mac) and clicking on the zones you wish to select.
           This way you can select several non-contiguous zones. You can also deselect a selected zone by clicking on it
           again.
       D   By holding down [Ctrl](Win) or [Cmd](Mac) and pressing [A].
           This will select all of the zones in the key map display. To deselect all zones, click in an unoccupied area in the
           Sample column or the key map area.
       D   By clicking and dragging a selection box in the key map area.
       Making a selection box like this....

       ...will select these zones:

       Note that the zones don’t have to be completely encompassed by the selection box. The selection box only have to
       intersect parts of the zones to include them in the selection.

       Selecting zones via MIDI
       You can also select zones via your MIDI keyboard. By clicking the button marked “Select zones via MIDI” above the
       key map display so that it lights up, you enable selection via MIDI.

       This way, you can select a zone and give it edit focus by pressing a key that lies within the zone’s key range (see later
       in this chapter for information about setting up key ranges).

       In this case, this zone can be selected by pressing any key between C2 - C3 on your MIDI keyboard.
       Note also, that selection via MIDI is velocity sensitive. Zones may have specific velocity ranges. This means that they
       won’t be played unless the key that triggers the zone is played with a certain velocity. The same rules apply when se-
       lecting via MIDI, only zones that meet the velocity criteria will be selected. Read more about setting up velocity ranges
       on “Setting velocity range for a Zone”.

       Selecting All Zones in a Group
       The concept of zone groups is fully introduced on “Working with Grouping”. For now we will only describe how to se-
       lect all samples that belong to the same group:
       Clicking in the
       Group column...

       ...selects all zones in
       the group

       Moving Edit Focus
       Moving Edit Focus
       A zone can be given edit focus independently of selection:
       D   When you click on an unselected zone, it both gets selected and gets edit focus.
       D   When you select several zones using [Shift], or [Ctrl](Win) or [Cmd](Mac), the one you select last always gets
           edit focus.
       D   To set edit focus to a zone when several zones are already selected, click on it without holding down any mod-
           ifier keys.
           This way, you can move edit focus between the selected zones freely without deselecting any of them.

       Adjusting parameters
       Adjusting Synth parameters
       The synth parameters are the ones that occupy the bulk of the remote editor panel (see “Synth Parameters”).
       Changes you make to synth parameters always apply to all selected zones.
       D   The panel always shows the settings for the zone with edit focus.
           More about this below.
       D   To make adjustments to one zone, select it (which also gives it edit focus) and adjust the parameter on the
           front panel.
       D   To set several zones to the same value, select them and adjust the parameter.
           All zones will be set to the same value for the parameter you adjusted.

       Adjusting Group parameters
       Group parameters apply to a group. That is, they are settings that are shared by all zones in a group.
       D   To make adjustments to one group, select one or more zones that belong to the group, and adjust the param-
           eter on the front panel.
       D   To set several groups to the same value, select at least one zone in each group you want to adjust, and adjust
           the parameter.
           All groups will be set to the same value. More about this below.

       About “Conflicting” parameters
       Often you will find yourself in a situation where you select multiple zones and parameter settings differ between
       them. This is quite normal. For example, you will often find yourself making adjustments to for example level and fil-
       tering to balance the sound between several samples across the keyboard. However, if you have multiple selections
       this can sometimes lead to confusion: Enter the NN-XT’s “conflicting parameters” indication:

       Whenever two or more selected zones have conflicting parameter settings, NN-XT will notify you about this by show-
       ing a small “M” (for multiple) symbol, next to the parameter.


=== END OF PART ===
