# Chapter 09: Reason 12 manual digest and studio workflow
## Part 97 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 88 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 98 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 88 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

       In this example, Level and Spread have conflicting settings.
       D   The controls on the panel always show the setting for the zone with edit focus.
       D   By clicking your way through the zones within the selection, you can see the settings for each zone.
       D   If you adjust a parameter, all selected zones will be set to the same value for this parameter.
       You can put this functionality to good use when checking how a patch has been created and when checking that
       your own settings are consistent through the various zones.

       Sample parameters
       The Sample parameters allow you to specify various properties for one or several selected zones, such as tuning, key
       and velocity ranges.

       D   To set several zones to the same value, select them and adjust the parameter.
           All zones will be set to the same value for the parameter you adjusted.

       Copying parameters between zones
       You can easily copy parameter settings from one zone to any number of other zones. Proceed as follows:
       1. Select all the zones you want to involve in the operation.
           By this we mean the zone with the settings you wish to copy, and the zone(s) to which you want to copy the set-
           tings.
       2. Make sure the zone that contains the settings you want to copy has edit focus.
       3. Pull down the Edit menu or the NN-XT context menu and select “Copy Parameters to Selected Zones”.
           All the selected zones will now get the exact same parameter settings.
       !   Observe that this only applies to the synth parameters (see “Synth parameters”). Sample parameters (root
           key, velocity range etc.) can not be copied.

       Managing Zones and Samples
       Creating a Key Map
       When you add an NN-XT sampler to the rack and select “Reset Device” from the context menu or Edit menu, its key
       map display becomes empty. That is, it contains no samples.
       To create a new key map, proceed as follows:
       1. Either click the Browse Samples button, select Browse Samples from the Edit menu or select Browse Samples
          from the NN-XT’s context menu.
           The NN-XT device gets browse focus.

           The Browse Samples button.
       2. Select the sample or samples that you want to load in the browser and click the “Load” button in the Browser.
           The selected sample(s) are loaded into the NN-XT.
       D   Alternatively, drag one or several sample files from the Browser and drop it on the NN-XT device in the rack.
           The panel is dimmed in blue and a Sample Replace symbol appears in the center.
       When new samples are loaded into the NN-XT they have the following properties:
       • Each sample is placed in its own zone.
       • Each zone spans a key range of five octaves on the keyboard - C1 to C6.
       • All the newly added sample(s)/zones are automatically selected.
       • The first added zone gets edit focus.

       A key map with four newly added samples.

       Setting Root Notes and Key Ranges
       The next step after loading the samples is most likely to adjust the key range, root note and tuning of the samples, so
       that they play sensibly across the key range. There are many ways of doing this, described in “Working with Key
       Ranges” and onwards. However, we will here briefly describe a procedure for quickly creating a complete key map
       out of a set of loaded samples.
       This example assumes that the samples you load is a set of multisamples for a pitched instrument (like guitar, piano,
       flute etc.).
       1. Load the samples.
       2. Use “Select All” on the Edit menu to select all the loaded samples.
       3. Use “Set Root Notes from Pitch Detection” to automatically set up the root notes (pitches) for the samples.

       4. Select “Automap Zones” from the Edit menu.
       All selected zones are automatically arranged into a basic key map. You can now proceed with adjusting the synth
       parameters on the front panel to shape the sound!

       About file formats and REX slices
       The audio file format support differs depending on which computer OS you are using.
       The NN-XT can read audio files in the following formats:
       • In Windows:
           .wav, .aif, .mp3, .aac, .m4a and .wma.
       • In macOS:
           .wav, .aiff, .3g2, .3gp, .mp1, .mp2, .mp3, .mpeg, .mpa, .snd, .au, .sd2, .ac3, .aac, .adts, .amr, .caf, .m4a .m4r and .mp4.
       • SoundFont samples
           This is a standardized data format containing wavetable synthesized audio and information on how it should be
           played back in wavetable synthesizers - typically on audio cards. SoundFont banks are hierarchically organized into
           different categories: User Samples, Instruments, Presets etc. The NN-XT lets you load single samples from within
           a Soundfont bank.
       • REX file slices
           A slice is a snippet of sound in a REX File (see “Loading complete REX files as Patches”). To import a REX slice,
           browse to a REX file and open it as if it was a folder. The browser will then display the slices as files inside that
           “folder”. In the rest of this manual, when we refer to importing samples, all that is said applies to REX slices as well.
       • Any sample rate and practically any bit depth.

       Adding more samples to the Key Map
       You can add additional samples to an existing key map way described above.
       1. Make sure that no already loaded sample has edit focus.
           If you don’t, there’s a risk that the selected sample will be replaced, see below. To remove the edit focus, click in an
           unoccupied area in the Sample column or the key map area.
       2. Open the Sample Browser.
       3. Select the sample(s) you want to load in the browser and click the “Load” button in the Browser.
       D   Alternatively, drag one or several sample files from the Browser and drop it on the NN-XT device in the rack.
           The panel is dimmed in blue and a Sample Replace symbol appears in the center.
       The new sample(s) are added to the key map.

       Replacing a sample
       To replace the sample in a zone, proceed as follows:
       1. Make sure the zone has edit focus and do one of the following:
       D   Click the Browse Samples button.
       D   Select Browse Samples from the Edit menu or the NN-XT context menu.
       D   Double click in the zone.
           Any of these methods will set browse focus and open the standard file browser in which you can select new sam-
           ples for the zone.

       2. Select one and only one sample in the Sample Browser.
           If you select more than one sample in the browser the samples you load will not replace the one with edit focus.
           They will instead be added below it.
       3. Click the Load button in the Browser.
       D   Alternatively, drag a sample file from the Browser and drop it on the NN-XT device in the rack.
           The panel is dimmed in blue and a Sample Replace symbol appears in the center.

       Quick browsing through samples
       If you want to quickly browse through a number of samples, for example to see which one of them would fit best in a
       certain context, proceed as follows:
       1. Set up the zone as desired and make sure it has edit focus:
       2. Use the arrow buttons in the Browse Samples section to select the next/previous sample in the directory.

       Removing samples
       D   To remove a sample from a zone, select it by clicking on it and then select “Remove Samples” from the Edit
           menu or the NN-XT context menu.
           This will remove the sample from the zone, leaving it empty. Note that you can remove the samples from several
           selected zones at the same time.

       Auditioning samples
       You can audition the loaded samples in two ways:
       D   By pressing [Alt](Win) or [Option](Mac) and clicking a sample in the sample column.
           The mouse pointer will take on the shape of a speaker symbol when you move it over the sample column.
           Clicking a sample will play it back at its root pitch (see “About the Root Key”). Furthermore, the sample will play
           back in its unprocessed state. That is, without any synth-parameters applied (see “Synth parameters”).
       D   By pressing [Alt](Win) or [Option](Mac) and clicking a sample in the keyboard column.
           The difference here is that you will hear the sample at the pitch corresponding to the key you clicked and with any
           and all processing applied. The click mimics a key played with velocity 100. Also note that this may trigger several
           samples, depending on whether they are mapped across the same or overlapping key ranges, and the velocity
           range settings (see “Setting up Key Ranges” and “Setting velocity range for a Zone” respectively).

       Adding empty Zones
       You can add empty zones to a key map. Empty zones are treated just like zones containing samples, in that they are
       automatically selected, gets edit focus and are assigned a five octave key range when they are first created. How-
       ever, you can only add one zone at a time. It is also possible to resize, move and edit empty zones in the same way as
       zones containing samples.
       D   To add an empty zone, pull down the Edit menu or the NN-XT context menu and select “Add Zone”.
           An empty zone is added below any existing zones in the key map. An empty zone is indicated with the text “**No
           Sample**”.
       After you have added an empty zone, you can assign a sample to it, just as when Replacing a Sample, or when Quick
       Browsing, as described above.

       Duplicating Zones
       You can duplicate any number of already existing zones (containing samples or empty).
       1. Select the zone(s) you want to copy.
       2. Pull down the edit menu or the NN-XT context menu and select “Duplicate Zones”.
           The selected zones will now be copied and automatically inserted below the last one in the key map display.
       The duplicated zones will contain references to the same samples as the original zones. They will also have the exact
       same key ranges and parameter settings.

       Using Copy and Paste
       The Copy Zones function on the Edit menu allows you to copy all selected zones to the clipboard. Selecting Paste
       Zones from the Edit menu will paste the zones into the selected NN-XT device, below the existing zones.
       This is a handy way to transfer zones (complete with all settings) from one NN-XT device to another.

       Removing Zones
       To remove one or several zones, select them and do one of the following:
       D   Press [Delete] or [Backspace] on the computer keyboard.
       D   Select “Delete Zones” from the Edit menu or the NN-XT context menu.
       When removing zones, you will remove any samples in them as well.

       Rearranging Zones in the List
       D   To move a zone to another position in the list, click on it in the samples column and drag up or down.
           An outline shows you where the zone will appear when you release the mouse button.

       Working with Grouping
       About Groups
       Grouping has two purposes:
       D   To allow you to quickly select a number of zones that “belong together.”
           For example if you have created a layered sound consisting of piano and strings, you could put all string samples
           in one group and all piano samples in one group. Then you can quickly select all piano samples and make an ad-
           justment to them by trimming a parameter.
       D   To group zones that need to share group settings together.
           For example, you may want to set a group to legato and monophonic mode and add some portamento so that you
           can play a part where you slide between notes.
       Note that there is always at least one group, since the zones you create are always grouped together by default.

       Creating a Group
       1. Select the zones you want to group together.
           The zones don’t have to be contiguous in order to be grouped. Regardless of their original positions in the samples
           column, they will all be put together in succession.

       2. Select “Group Selected Zones” from the Edit menu or the NN-XT context menu.
           The zones are grouped.
           Selecting these zones and grouping them...

           ...will create these two groups instead of the original one large group.

       Moving a Group to another position in the List
       D   Click on the group in the Groups column and drag up or down with the mouse button pressed.
           An outline of the group you move is superimposed upon the display to help you navigate to the desired position.

           Dragging a group to a new position.
       3. Release the mouse button at the desired position.
           The group and all its zones appear at the new position.

       Moving a Zone from one Group to another
       This is done just as when rearranging samples in the list, as described on the previous page. The only difference is
       that you drag the zone from one group to another.

       Selecting a Group and/or Zones in a Group
       D   Clicking on a group in the groups column selects the group and all the zones in the group.

       D   Clicking on a zone in the samples column selects the group (and that zone).

       The Group Parameters
       There are a few parameters on the front panel that apply specifically to groups. see “Group parameters” for details.

       Working with Key Ranges
       About Key Ranges
       Each zone can have its own separate key range, the lowest and the highest key that will trigger the sample.
       A good example of use for this is when sampling a certain instrument. Sampling of a piano for example is usually per-
       formed by making several recordings of different notes at close intervals, and then mapping these samples to sepa-
       rate, contiguous, fairly narrow key ranges. This concept is called multi-sampling.
       The reason for this is that if one single sample is played across the entire keyboard, it will most likely sound very un-
       natural when played too far from its original pitch, since the amount you can transpose a sound without negatively af-
       fecting its timbre is very limited.

       Setting up Key Ranges
       You can adjust the key range of zones in a number of ways:

       By Dragging the Zone Boundary Handles
       1. Select the zone in the Key Range area.
       2. Point and click on one of the handles that appear at each end.

       3. Drag the handle left/right.
         Dotted lines extend from the edges of the zones up to the keyboard area. These lines give you a visual indication
         of which keys the key range will encompass. There is also an alphanumerical indication at the bottom left of the
         display.
       Clicking and dragging the high key boundary handle of a zone with the default key range of C1 - C6...

       ...to change the key range to C1 - C2.

       4. Repeat the procedure with as many zones as you wish, to create a complete key map.

       By using the Lo Key and Hi Key controls
       Directly below the key map area you will find the sample parameters. These are used for changing various parame-
       ters that affect how the zones are played back. They can affect single or multiple selected zones. In the middle of the
       sample parameters area are two knobs called “Lo Key” and Hi Key”.

       These can be used for setting the low key and the high key of a zone’s key range.
       1. Make sure the zone which you want to set the key range for is selected.
       2. Use the Lo Key/Hi Key knobs to change the key range.
         Check the display right above the knobs for an indication of the key. You can also keep an eye on the lines extend-
         ing from the zone edges to the keyboard area.
       Setting key ranges for multiple zones
       You can set key ranges for multiple selected zones simultaneously. This can only be done by using the Lo and Hi Key
       controls. It works as follows:

       D   If you have three selected zones that each have different high keys and then turn the Hi Key knob, they will all
           automatically get the same High Key value as the zone with edit focus.
           In other words, if the selected zone with edit focus has the high key set to C4, and you change this to D4 by turn-
           ing the Hi Key knob, all other selected zones will also be extended to D4 as the High Key.

       D   If any selected zone’s low key setting is higher than the edit focused zone’s high key before turning the Hi Key
           knob, the zone range will be scaled down to one semitone, starting from the low key setting.
           The high key can naturally never be set to a value lower than one semitone above its low key setting - the zone
           would otherwise disappear!
       D   The inverse is also true - i.e. turning the Lo Key knob for several selected zones will apply the edit focused low
           key setting to all selected zones.
           A low key can never be set higher than one semitone below the high key in a zone, so if the edit focused zone has
           a low key above the high key of another zone, the other zone will be scaled to the minimum semitone range.

       By Dragging the Zone Boundary Handles on the Tab Bar
       As previously described, the area directly below the keyboard area is called the tab bar. This shows the key range for
       the currently selected zone, and also contains boundary handles.

       Dragging a boundary handle on the tab bar.
       These handles can be used much to the same effect as when dragging the boundary handles in the key map display.
       However, the handles on the tab bar can change the key range of multiple zones at the same time.
       The following applies:
       • The tab bar shows the key range for the zone with edit focus.

       • Dragging the boundary handles for that zone will also simultaneously change the key range for a number of
         surrounding zones if:
       D   The high key or low key (depending on which handle you drag) of the other zones are the same as the zone
           with edit focus.
       D   The other zones are adjacent to the zone with edit focus.
       !   Note that it doesn’t matter whether the other zones are selected or not. They will be affected anyway.

       In the example in the picture above, the zone in the middle has edit focus. Its left handle (the low key) is placed dif-
       ferently from any of the other zones, but all of the zones have the same high key setting. This means that...
       • Dragging the left handle will only move the low key position of the zone with edit focus (the pictures show be-
         fore and after dragging).

       • Dragging the right handle will move the high key position for all of the zones at the same time, since they all
         have the same high key position (again, the picture shows before and after dragging).

       Moving Zones by Dragging the Zone Boxes
       You can also move entire zones horizontally, thereby changing their key ranges.
       1. Select all the zones you want to move.
         You can move several zones simultaneously.
       2. Point on any of the selected zones, and press the mouse button.
       3. Drag left/right and release the mouse button.

         Dragging multiple zones.

       Moving Zones by Dragging in the Tab Bar
       You can also move a zone by dragging anywhere between the zone boundary handles on the tab bar. When you do,
       the surrounding zones will be affected just as when dragging the boundary handles in the tab bar (see above).
       This can be used to “slide” a zone in relation to its surrounding zones, as the picture example below shows (before
       and after dragging).

       About the Lock Root Keys function

       Normally, when you move zones (as described above), the root note of the zone(s) you move will change accordingly.
       In other words, the zone(s) will be transposed. If this is not desired, you can activate the Lock Root Keys function prior
       to moving the zone(s) by clicking on the button above the key map display.
       Moving zones without changing their root notes can be used for some interesting effects, since it will completely
       change the timbre of the sample(s) as they are played back.

       About the Solo Sample function

       The Solo Sample function lets you play a selected sample over the entire keyboard and disregarding any velocity
       range assigned to the sample. All other loaded samples are temporarily muted.
       This is useful if you for example want to check how far up and down from its root key a sample can be played on the
       keyboard before starting to sound “unnatural”. The solo sample function can therefore be useful as a guide for setting
       up key ranges, as described in “Setting up Key Ranges”.
       1. Select one and only one zone, or - if you have a selection of multiple zones - make sure the one you want to
          hear has edit focus.
       2. Activate Solo Sample by clicking on the button so that it lights up.
       3. Play the MIDI keyboard

       Sorting Zones by Note
       The Edit menu and the NN-XT context menu contains an item called “Sort Zones by Note”. This option lets you auto-
       matically sort the selected zones in descending order according to their key ranges.
       When you invoke this option, the selected zones will be sorted from top to bottom in the display starting with the one
       with the lowest range.
       Note however, that the sorting is done strictly on a group basis. That is, only zones that belong to the same group can
       be sorted in relation to each other.

       Before sorting and after.
       If two zones have the same key range, they are sorted by velocity range.

       Setting Root Notes and Tuning
       About the Root Key
       All instrument sounds have an inherent pitch. When playing a sample of such a sound on the keyboard, the keys you
       play must correspond to that pitch. For example, you may have recorded a piano playing the key “C3”. When you map
       this onto the NN-XT key map, you must set things up so that the sampler plays back the sample at original pitch
       when you press the key C3.
       This is done by adjusting the root note.
       D   Many samples files from different sources already have a set root key in the file. If they do, the root key will be
           correctly set automatically when you load the sample into a zone.
       D   However if the sample doesn’t have a root note stored in the file, (if you for example have recorded it yourself)
           you will need to adjust it

       Setting the Root Note manually
       To set the root key for a zone, proceed as follows:
       D   Make sure the zone has edit focus (for example by clicking on it), and do one of the following:
       D   Use the knob marked “Root” in the sample parameter area below the display.
           Turning it to the right will raise the pitch of the root key. The selected key is displayed alphanumerically directly
           above the knob, and you can also look at the keyboard area for a visual indication (see below).

       D   Press [Ctrl](Win) or [Cmd](Mac) and click on the desired root key in the keyboard area.
           The set root key is shaded so you can easily distinguish it.

       Tuning samples manually
       In addition to setting the root note, you may need to fine tune your samples, in order for them to match other instru-
       ments and/or each other:
       D   Make sure the zone has edit focus (for example by clicking on it).
       D   Use the knob marked “Tune” in the sample parameter area.
           This allows you to tune each sample in a key map by +/– half a semitone (-50 – 0 – 50).

       Setting the Root Note and Tuning using pitch detection
       The NN-XT features a pitch detection function to help you set the root keys. This is useful if you for example load a
       sample that you haven’t recorded yourself, and you don’t have any information about its original pitch.
       Proceed as follows:
       1. Select all the zones you want to be subject to pitch detection.
       2. Pull down the Edit menu or the NN-XT context menu and select “Set Root Notes from Pitch Detection”.
           The samples in all the selected zones will now be analyzed, and the detected root keys will automatically be set for
           you.
       !   Note that for this to work properly, the samples must have some form of perceivable pitch. If it is sampled
           speech, or a snare drum for example, it probably doesn’t have any discernible pitch.

       About changing the pitch of samples
       The procedures above should be used to make sure the samples are consistently pitched across the keyboard, and
       that they all match an absolute reference (for example A 440 tuning).
       If you need to tune the samples to match other material, or to get a certain effect (for example detuning two sounds
       against each other for a chorus effect) you should use the Pitch section among the synth parameters, not the sample
       tuning parameters.


=== END OF PART ===
