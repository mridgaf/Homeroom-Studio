# Chapter 09: Reason 12 manual digest and studio workflow
## Part 13 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Reference.md (piece 4 of 10) — Reason 12.7 Operation Manual — Compiled Reference

(Next: Part 14 of 25)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Reference.md (piece 4 of 10)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Reference.md
=====================================================

## 9. Note and Automation Editing


This chapter describes how to edit note and parameter automation events after they have been recorded in the sequencer. It also describes how to manually create note and automation events in clips. General sequencer functions, recording, editing audio, arranging in the sequencer and working with Blocks are described in detail in the chapters “Sequencer Functions”, “Recording in the Sequencer”, “Audio Editing in the Sequencer”, “Arranging in the Sequencer” and “Working with Blocks in the Sequencer”.

The Edit Mode shows the contents of a single lane at a time on the Edit Pane - unless you use the Multi Lanes function, described in “Multi Lanes editing”, where you can see the contents of multiple note lanes in a “ghosted” fashion underneath the currently open clip. On instrument tracks, only one note lane can have edit focus at a time.

Also, all parameter automation lanes will be shown at the bottom of the Edit Pane. If a single clip was selected on the note lane with edit focus when you switched to Edit Mode, it will automatically be opened. If no clip was selected, the events will be grayed out. To be able to edit or draw notes and/or automation events, you need to open the clip, for example by double-clicking it (see “Opening note and automation clips for editing”).

Note clips can contain both note events - with velocity values - and performance controller events. By default, performance controllers include Mod Wheel, Pitch Bend, Sustain Pedal, Aftertouch, Expression and Breath Controller. However, the controller configuration can easily be changed (see “Creating new performance controller automation lanes” and “Deleting performance controller automation lanes”).

See “Editing parameter automation in the Song/Block View” for information on how to edit parameter automation events in the Song/Block View.

See “Editing parameter automation in Edit Mode” for information on how to edit parameter automation events in Edit Mode.

To the right of the Note Edit Lane, below the Vertical Zoom tools, is the Note Edit Mode Selector. Click to choose between Key Edit, Drum Edit or REX Edit Mode. Depending on selected mode, the Note Edit Lane will display differently. See more about the different modes in “Note Edit Modes”.

Each performance controller you used when recording the note clip has its own separate Performance Controller Edit Lane. You can add or delete performance controller edit lanes from the clip using this selector. See the “Creating new performance controller automation lanes” and “Deleting performance controller automation lanes” for more details.

Here you can edit the notes of one open clip at a time. Note events are displayed as orange horizontal “boxes” in a piano roll fashion on the Note Edit Lane. The left side of each box indicates Note On (key down) and the right side Note Off (key up). The color intensity of each box indicates the velocity for the corresponding note. Depending on selected Note Edit Mode (see “Note Edit Modes”), the contents of the Note Edit Lane will display differently.

The Velocity Edit Lane shows the velocity values for each of the recorded notes. Velocity values are automatically recorded together with notes. See more about editing velocity values in “Editing note velocity”.

On the Performance Controller Edit Lanes are the performance controller events for Mod Wheel, Pitch Bend, Sustain Pedal etc. Performance controller events are automatically distributed on separate lanes for each recognized controller during recording. Even though performance controllers belong to separate note clips, they will affect all active parallel note lanes on a track. See “Automation editing” for details on how to edit performance controller events.

Any recorded parameter automation will be shown in separate clips, on separate Parameter Automation Lanes. Parameter automation clips don’t “belong” to the note lane or to any note clips, and will not be opened together with note clips. Double-clicking on a parameter automation clip will open it for editing. See “Automation editing”.

The Static Value Handles to the left of the Performance Controller Edit Lanes and Parameter Automation Lanes indicate to what value the automated controller/parameter will default to where there are no clips on the lane. Basically, this value reflects the parameter’s initial value, before it was automated. You can easily change a parameter’s Static Value by dragging the Static Value Handle up or down. See “Automation editing” for more details.











•

Notes can be edited using the mouse in Edit Mode. It’s also possible to edit notes by using the functions on the Tools tab in the Tool Window. Notes can also be numerically edited in the Inspector, as described in “Note and automation editing in the Inspector”.

If you want to restrict note input to certain note values (e.g. 1/16th notes), activate Snap (see “Snap”) and set the snap value accordingly.

A note will be inserted at the closest Snap value position. By default, the note will be given the Velocity value ‘100’. (This can be edited afterwards according to the descriptions in “Editing note velocity”). If an open or closed clip is already present on the Note Lane, at the position where you draw the note, the note will be placed in that clip. If no clip is available, refer to “About drawing notes outside an open clip” and “About drawing notes outside a closed clip” below.

If Snap is off, the note will get the length of the shortest possible Snap value, i.e. 1/128th note.



Multiple notes of the currently selected Snap value length are now added after one another (at the same pitch) in the note clip. By default, the notes will be given the Velocity value ‘100’. (This can be edited afterwards according to the descriptions in “Editing note velocity”).

•



If Snap is on (see “Snap”), the beginning and/or end of the note will be magnetic to the (absolute) Snap value positions.

You can also edit the length of notes numerically in the inspector. See “Note and automation editing in the Inspector”.

If several notes are selected, all will be moved. If Snap is on (see “Snap”), the moved events will keep their relative distance to the Snap value positions - or will be moved to new positions on an absolute grid - depending on whether you have selected “Absolute” or “Relative” in the Snap value list.

If you nudge notes outside the boundaries of an open clip, the notes will belong to the open clip, but become masked since they are nudged outside the clip boundaries. The “Keep Events in Clip While Editing” setting has no effect when nudging notes. If you want to move notes between clips, or to a new clip, you have to do that using the Selection Tool as described in “About moving notes outside or between clips”.

It’s possible to move defined notes in a clip to new clips on new, additional lanes. See “Extract Notes to Lanes”.

You can also edit the note positions and pitches numerically in the inspector. See “Note and automation editing in the Inspector”.



It’s possible to duplicate defined notes in a clip and automatically place them on new, additional lanes. See “Extract Notes to Lanes”.

The “Quantize” function on the Transport Panel and on the Sequencer Tools tab in the Tool Window is normally used for applying quantization to notes - but can also be used for quantizing recorded audio. Clicking the Quantize or Apply button will automatically align the start positions of the selected notes or audio slices to a pre-defined, absolute grid. You can also choose to automatically quantize MIDI notes as they are being recorded - see “Quantizing notes during recording”.

A more flexible way of doing this for notes and note clips is to use the ReGroove mixer - see “The ReGroove Mixer” chapter for details.

Any notes recorded after having activated this function will be automatically quantized to the current settings on the “Quantize” pane in the Tool Window, see “Quantize”.







The “Extract Notes to Lanes” function on the Sequencer Tools tab in the Tool Window is used for moving or duplicating user-defined notes of a certain pitch, or notes within a defined pitch range, to a new note clip on a new, additional note lane. This function is very useful if you, for example, have recorded a drum track, with all notes in the same clip, and then want to extract individual drum sounds (note pitches in this case) to separate lanes to be able to edit them more easily - or to apply ReGroove channels (see “The ReGroove Mixer”).

Since the Extract Notes to Lanes function applies to selected clips and not to selected notes, you have to click in the Clip Overview to enable the function. (In the Song/Block View, you just select the clip by clicking on it).



You can also edit velocity values numerically in the Inspector. See “Note and automation editing in the Inspector”.

This is done in the Song/Block View. If the clips are on the same lane, it can also be done in the Comp Editor. See “Reversing audio clips” for more details about reversing audio clips.

The easiest ways of selecting what note lanes should be available for Multi Lanes editing are these:

With the Multi Lanes editing feature, the functions “Move/Duplicate Selected Notes to New Lane” and “Extract Notes to Lanes” are very useful, especially when working with drum tracks.

•

•



Here you can edit the parameter’s Static Value (see “Static Value Handles”) with the up/down arrow buttons to the left of the open clip. Alternatively, double-click and type in a new Static Value in the box.

In the open parameter automation clip, it’s possible to move, add and delete automation events in the same way as in Edit Mode using the Selection (Arrow), Pencil and Eraser tools - see “Editing parameter automation in Edit Mode”.

The event’s position and value can be edited numerically in the displays - see “Note and automation editing in the Inspector”.



When moving automation events with the Selection (Arrow) Tool, Snap (see “Snap”) is taken into account if enabled. You can also resize the clip by dragging the clip handles.



These values can be edited numerically in the Inspector displays. See “Note and automation editing in the Inspector”.

If you move parameter automation events outside the boundaries of an open clip, the same rules apply as when moving note events outside an open clip. See “About moving notes outside or between clips”.

When dragging, the resulting curve (i.e. the number of points) depends on two factors; the selected “Automation Cleanup” setting in the Preferences menu (see “About Automation Cleanup”), and the snap value if Snap is activated (see “Snap”).

Note that if the automation line is curved (see “Creating curves between automation points”), the line will become straight (not curved) to the right of the added point.

If you draw parameter automation events outside the boundaries of an open clip, the same rules apply as when drawing note events outside an open clip. See “About drawing notes outside an open clip”.



It’s possible to reverse the order of selected automation events in an open note or automation clip, see “Reverse”.



4.

Afterwards, you can edit the performance controller events the same way as with regular parameter automation events (see “Editing parameter automation in Edit Mode”).

This automatically removes superfluous automation events next time you record or draw events and simplifies the curves. Note that Snap (see “Snap”) also governs the number of events when drawing events.

1.

However, it is recommended that Snap is activated (and in most cases set to “Bar”) when you do this (see “Snap”).

Tempo automation is edited in the same way as regular parameter automation. See “Editing parameter automation”.

Drawing tempo automation events is done in the same way as drawing regular parameter automation events. See “Drawing parameter automation events”.



It is generally a good idea to activate Snap (see “Snap”) and have the Snap value set to “Bar” when drawing clips.

The available signatures are: 1/2-16/2, 1/4-16/4, 1/8-16/8 and 1/16-16/16. The Time Signature display in the dialog can be edited according to the descriptions in “Transport Panel segment displays”.

5.

There is no need to switch to Edit Mode unless you wish to change the time signature’s Static Value.

However, it is recommended that Snap is activated (and in most cases set to “Bar”) when you do this.

See “Inspector segment displays” for details on how to edit in the Inspector displays.

•
---

<a id="working-with-blocks-in-the-sequencer-10"></a>
## 10. Working with Blocks in the Sequencer


This chapter describes how to work with Blocks and Block Automation Clips in the main sequencer. Basic sequencer functions, recording, editing clips and events and arranging in the sequencer are described in detail in the chapters “Sequencer Functions”, “Recording in the Sequencer”, “Audio Editing in the Sequencer”, “Note and Automation Editing” and “Arranging in the Sequencer”.

A colored area appears on the arrangement pane with the Block name at the top on the Blocks Track. By default, the Blocks are named “Block n” where “n” is a number between 1 and 32. If you like, you can rename your Blocks to more suitable names (see “Renaming Blocks”). The Block View is where you record the clips you want to include in a specific Block. The clips present in the colored Block area in the Block View are unique only to that specific Block.

Refer to “Recording in the Sequencer” for details about recording.

Refer to “Note and Automation Editing” and “Audio Editing in the Sequencer” for details about editing clips.

The following section describes functions and routines that are specific to Block Automation Clips. General clip handling procedures (e.g. naming, coloring etc.) are described in the general “Clip handling” section.

The contents (clips and events) of Block 1 are displayed on the respective sequencer tracks in a ghosted fashion on a colored background. This way you will see what events and/or recordings the Block will play back. This also allows for muting of individual lanes in the Block (see “Muting lanes in Block Automation Clips”).
---

<a id="working-with-the-rack-11"></a>
## 11. Working with the Rack


This will place the rack in a separate window. (See "The Rack" for more info.)

See also "Creating new rack columns" for information on how to create several rack columns.

By default, when you create an Instrument device, a new (or currently unused) Mix Channel device will be automatically connected to the Instrument device, as described in "Creating devices". In this situation, the Instrument device and the connected Mix Channel device will now be considered a Device Group - with the Instrument device as the Source device.

Devices can be created in a number of different ways. These first methods apply to any device types:

The devices are sorted in four different groups: Instruments, Effects, Utilities and Players. The Utilities group contains device types such as mixers, modulation devices, etc. In each device type group the devices are listed in the following sections: Reason Devices, and then by Rack Extension and/or VST manufacturer in alphabetical order. The Players group is a little special; it contains a number of MIDI "generators" that can be used when recording Instrument tracks in the sequencer, see "Working with Players".

Automatic browse focus can be switched off if you like. This is done on the General tab in Preferences, see "New devices get browse focus".

This will show the Instruments palette in the Browser. Here you can choose the Instrument device you want to create - see "Create Instrument/Create Effect".

The track, the Mix Channel device and its channel strip will be given the same name as the created Instrument device. Master Keyboard Input will also automatically be set to the new track, allowing you to immediately play the created Instrument device via MIDI (see "Master Keyboard Input"). By default, the Instrument device and Mix Channel device will be treated as a "Device Group" from here on (see "About Device Groups").

This will show the Effects palette in the Browser. Here you can choose the Effect device you want to create - see "Create Instrument/Create Effect".

Some operations, e.g. cutting, copying, moving and deleting devices (see "Cut, Copy and Paste devices" and "Deleting devices"), require that you select one or several devices in the rack. This is done according to the following:

If you want to move an instrument device to another position in the rack, you probably also want its Mix Channel device and connected effects to move along with it. If the "Auto-group Devices and Tracks" on the "Options" menu is selected, all devices in the Device Group will follow along when you drag and drop a device included in a Device Group. However, it's still possible to re-order devices within each Device Group. See "About Device Groups" for more details. See also "About the "Sort Selected Device Groups" function" for information about automatic sorting of several Device Groups.

This allows you to e.g. change the order of effect devices in a signal chain by Shift-dragging them.

When you are working with Device Groups (see "About Device Groups"), there is a very nice feature which allows you to visually organize and re-order the Device Groups, Main Mixer channel strips and sequencer tracks. With the "Sort Selected Device Groups" function on the Edit menu, it's possible to sort Device Groups and Main Mixer channel strips according to the current sequencer track order - or vice versa, depending on what's currently selected. To sort the Device Groups in the rack, and the channel strips in the Main Mixer, according to the current sequencer track order, proceed as follows:

The new device is automatically routed like the previous device. The Mix Channel now also gets the name of the current patch in the new device. The new device also gets "browse focus" in the Browser, see "Loading patches".

Duplicating devices will have different results depending on the "Auto-group Devices and Tracks" setting on the Options menu (see "About Device Groups"):

Selected devices or Device Groups can be moved or duplicated using the Cut, Copy and Paste Device functions on the Edit menu or device context menu. This allows you to copy one or several devices (such as an instrument device and all its "insert" effects) from one Reason Song document to another. Cutting/Copying and Pasting will have different results depending on the "Auto-group Devices and Tracks" setting on the Options menu (see "About Device Groups"):

The rules are the same as when moving or duplicating devices by dragging and dropping. See "Routing Audio and CV" for more information about automatic and manual routing.

---

<a id="working-with-players-12"></a>
## 12. Working with Players


If you like, you can attach several Player devices to a single Instrument device in the rack. Just follow the instructions in "Creating Players" above and make sure you insert the additional Player(s) somewhere in between the Instrument device and the top section of the topmost Player device.

See "Tips & Tricks" for some interesting combinations!

Replacing a Player device with another Player device can be done in exactly the same way as when replacing other device types, see "Replacing devices".

Deleting Players is done in exactly the same way as when deleting other device types, see "Deleting devices".

Naming Players is done in exactly the same way as when naming other device types, see "Naming devices".

See "General recording methods" for more information.

#Rate

* The Shuffle amount is set with the Global Shuffle knob in the ReGroove Mixer, see "Global Shuffle".

Provided the Pattern function (see "Pattern") is not active, this is what will be played back:

Provided the Pattern function (see "Pattern") is not active, this is how it works:

| Mode

If the Pattern function is active (see "Pattern"), the Direction setting only determines in which direction the steps should advance - regardless of the pitches of the notes in the pattern.

#Hold

Set the Direction to "Up" (see "Direction"), to make the examples below work as described.

Note that if the Steps function is not active (see "Steps"), note 5 and up will add additional silent steps in the pattern, making the pattern longer.

This knob sets the number of repeats, from 1-16. The number of repeats is also shown in the display.

#Key

You can easily switch between your Custom Scale and any of the preset Scales whenever you want, by clicking the "Scale" display and selecting the desired scale from the list that appears.

When the Filter Notes switch is off (default), incoming notes outside the set Scale (see "Scales") are transposed to fit the scale.

When you play a note, you will get a chord that fits the set Scale (see "Scales"), and contains the number of notes set with the "Notes" knob. The generated notes are shown in real-time in the keyboard display at the bottom of the Chords section.

Note that the Inversion function is only relevant if the Inversion number is less than the selected "Notes" value. So, if the Notes value is 4, only a maximum Inversion value of 3 is useful.

When the Open Chords function is active, some notes in the generated chords are transposed in octave steps, so that the notes are not so close to each other. The transposition is different depending on the "Inversion" and the "Notes" settings.

#Add

The Scales & Chords Player is great for generating chords that stay within a set scale, but sometimes you may want chords that keep their form when you play different notes. For example, you might want a minor 9th chord that is transposed with the notes you play, but stays a minor 9th chord (like with the Chord Memory function of some synthesizers, for example). This can be called "parallel chords", and is actually best done with the Note Echo device.

The "Creating parallel chords" example monitored in a Scales & Chords device when playing the note C.

---

<a id="working-with-rack-extensions-13"></a>
## 13. Working with Rack Extensions


Rack Extensions are additional rack devices that can be purchased in the Reason Studios web shop at www.reasonstudios.com/shop and used together with the internal devices in the rack. Rack Extensions can be instruments, effects or utility devices, such as mixers and CV processors. Rack Extension devices are developed by Reason Studios as well as by 3rd party companies.

You can try out a Rack Extension by going to the Reason Studios web shop at www.reasonstudios.com/shop and using the "Try" function. This gives you a trial license which will last for 30 days (counted from when you clicked the "Try" button). During this time, the Rack Extension is fully operational, with no limitations.

---

<a id="working-with-vst-plugins-14"></a>
## 14. Working with VST Plugins


The Plugin Rack Device is placed in the rack and is auto-routed according to the standard rules. See "About auto-routing of VSTs in the rack" for more details about auto-routing of VSTs.

There are also Next/Previous VST Program buttons to the right of the patch display, where you can step through the programs loaded in the VST plugin itself, see "Selecting VST presets/programs".

On the CV Programmer panel you can route CV signals from other (modulation) devices in the rack to parameters of the VST plugin. Each of the eight CV slots can receive a CV signal connected to the corresponding Modulation CV In connector on the rear panel of the Plugin Rack Device (see "Rear panel" below).

Refer to "CV modulation of VST parameters" for information on how to route CV signals to VST parameters.

Click this button when you want to assign a VST parameter for automation in the Reason sequencer, see "Automating VST parameters".

Click this button and then select a VST parameter you want to remote control from your MIDI keyboard/control surface, see "Remote controlling VST parameters".

If the "Keep open" function in the Plugin Window is active, selecting another device in the rack will NOT close the Plugin Window (see "Keep open" above).

---

<a id="sounds-patches-and-the-browser-15"></a>
## 15. Sounds, Patches and the Browser


A patch contains settings for a specific device. Patches can be either separate files on your hard disk or files embedded in a ReFill (see "About ReFills" for info about ReFills). The devices that use patches are described below. The Mix Channel, Master Section and Audio Track devices can use Insert FX patches saved as Combinator devices. All other Reason devices use either Presets or can only be programmed using the device panel parameters.

Again, the actual samples are not included in the patch, only references to files. Also note that Redrum patches are separated from Redrum patterns - loading a new patch will not affect the patterns in the device.

On the "General" page in Preferences, there is an option (on by default) to load a default patch when creating a device. For some devices, there are a number of patches that exist outside category folders in the main Sound Bank folder for the device. These will be available on the browse list (see "About browse lists") directly after creating the device, which allows you check out a few sounds for a device without opening the browser.

The Revert function makes it possible to get back to the patch which was originally in the device - before you started loading new patches. This is very handy if you should change your mind and want your original patch back in your device. The Revert function also works if you have loaded patches for other device types, so called cross-browsing (see "Cross-browsing patch files").

If this is the case when you select a patch, the program will tell you so. You can then choose to either manually locate the missing files, to have the program search for them, or to proceed without the missing sounds. For details, see "Handling Missing Sounds".

For example, set browse focus from a Subtractor device by clicking its Browse Patch button. Instead of limiting the Browser to show only Subtractor patches, you can choose to browse for any type of instrument patch. If you select a patch with a different format than the device you are browsing from, the original device will be replaced by the new device. See "Cross-browsing patch files".

This opens the Browser allowing you to browse for and load patches for the selected device, or use "cross-browsing" (see "Cross-browsing patch files") to select patches for other device types.

This opens the Browser, allowing you to browse for, preview and load files in the supported audio formats to an audio track in the sequencer. See "Importing audio to the sequencer".

This opens the Browser, allowing you to browse for MIDI files to import to instrument tracks in the sequencer. See "Importing Standard MIDI Files".

This allows you to browse for and load patches for any device. See "Create Instrument/Create Effect".

This field shows the name of the currently selected device in the rack - or the currently selected sequencer track. The Browse Focus field is orange when a device or track has browse focus - and gray when no focus is set. See "Setting browse focus" and "Clearing browse focus" for more information.

This list contains shortcuts to various locations. You can manually add any locations (on any drive) to the bottom section of the list. The locations in the upper part of the list are default and cannot be changed. Selecting an item in the "Locations and Favorites" list will open the corresponding folder/ReFill as the root in the main files and folder list - see "Navigating in the Browser".

In the "Locations and Favorites" list you could also create your own "Favorites Lists". The "Favorite Lists" can contain shortcuts to your favorite patches, samples or song files - see "Favorites Lists".

Here you can enter a text string and click Search to search for Song files, patches, audio files and samples. The Search function is described in "Using the "Search" function".

This is the Browser list, showing the contents of a selected folder - see "Navigating in the Browser".

The "Info" section at the bottom of the Browser can show Song/ReFill splash images and also information about the item currently selected in the "Files and Folders" list. Exactly what information is shown here depends on the selected file type. For example, samples or REX files contain information about the file format and length of the selected file, while a selected song file can display comments from the author (see "Including Song Information") etc. If the selected file is part of a ReFill, this will be indicated regardless of the file type.

Folding the Info and Details section automatically expands the Browse list/device palette downwards.

This section contains controls for auditioning audio files, samples and REX files - see "Selecting and auditioning samples and REX loops". For other file types, the "Audition" section is not present.

This is particularly useful for handling patches. By adding the patches you need for a given situation to a Favorite List, you can determine exactly which patches will be selectable for a device, and in what order. You can then sequentially step through these patches using patch select buttons on your MIDI keyboard or control surface device. See "Using Favorites - a practical example".

A new folder appears in the list. Double-click it and type in an appropriate name (e.g. "The Band").

If this was a patch in a different format than the instrument you created, a device of this type will replace the original device (see "Cross-browsing patch files").

Many MIDI keyboards and control surfaces have buttons assigned to patch selection - check the Control Surface Details document for information about your controllers. Alternatively, you can manually assign buttons for selecting patches - see the "Remote - Playing and Controlling Devices" chapter.

See the "Kong Drum Designer" chapter for details.

See the "Dr. Octo Rex Loop Player" chapter for details.

See "Importing audio to the sequencer" for more info.

You can select several files to add them to a Favorites List in one go - see "Favorites Lists". Note that this is only possible if a device does not have browse focus!

The Browser opens. Depending on your selection, only Instrument Patches or Effect Patches are shown.

Favorites Lists provide a way of controlling/filtering which patches or samples will be available on a browse list for a device - see "Using Favorites - a practical example"!

Note that if you opened a patch after having used cross-browsing (see "Cross-browsing patch files") or used the Search function (see "Using the "Search" function"), the active browse list could contain patches of different formats, and loading patches from the device panel could change the device type.

---

<a id="routing-audio-and-cv-16"></a>

=== END OF PART ===
