# Reason 12.7 Operation Manual — Compiled Reference

Compiled from the official free Reason Studios documentation site (docs.reasonstudios.com/reason12), the same content Reason Studios publishes as the free HTML manual and the free downloadable PDF (no login, no paywall — unlike the Scribd copy). Source: https://docs.reasonstudios.com/reason12/introduction

**Read this before relying on it:** the source site renders device parameter tables, knob labels, and panel diagrams as interactive graphics rather than plain text, so a chunk of the reference material that would normally be in these chapters (individual knob ranges, some panel-callout labels) didn't survive text extraction and is not reproduced here. What *did* come through cleanly is the prose: how each device works, signal flow, procedures, tips, and cross-references. Two chapters — Menu and Dialog Reference and Key Commands — came through in much fuller detail, key command tables included (the key-command table pairing is mostly but not 100% reliable due to how the source table was structured).

For the complete, exact reference — every knob, every parameter table, every diagram — get the actual official PDF directly from Reason Studios, free, one click, no account needed:

**Reason 12.7 Operation Manual (PDF):** https://a.phcdn.se/Reason12/Manuals/Reason_127_Operation_Manual.pdf
**Reason 12.7 Installation Manual (PDF):** https://a.phcdn.se/Reason12/Manuals/Reason_127_Installation_Manual.pdf
**Key Commands (PDF):** https://a.phcdn.se/Reason12/Manuals/Reason_122_Key_Commands.pdf
**MIDI Implementation Chart (PDF):** https://a.phcdn.se/Reason12/Manuals/Reason_126_MIDI_Implementation.pdf
**Full documentation index (all versions):** https://help.reasonstudios.com/hc/en-us/articles/360002216673-Reason-Documentation-and-Help-Files

(The full Operation Manual PDF is roughly 30-40MB with illustrations — too large for me to download directly in this session or pull the raw text out of, which is why this compiled version exists as a fast-reference companion. It's also available inside Reason itself via Help menu.)

---

## Table of Contents

1. [Introduction](#introduction-1)
2. [Common Operations and Concepts](#common-operations-and-concepts-2)
3. [On-screen Piano Keys](#on-screen-piano-keys-3)
4. [Audio Basics](#audio-basics-4)
5. [Sequencer Functions](#sequencer-functions-5)
6. [Recording in the Sequencer](#recording-in-the-sequencer-6)
7. [Arranging in the Sequencer](#arranging-in-the-sequencer-7)
8. [Audio Editing in the Sequencer](#audio-editing-in-the-sequencer-8)
9. [Note and Automation Editing](#note-and-automation-editing-9)
10. [Working with Blocks in the Sequencer](#working-with-blocks-in-the-sequencer-10)
11. [Working with the Rack](#working-with-the-rack-11)
12. [Working with Players](#working-with-players-12)
13. [Working with Rack Extensions](#working-with-rack-extensions-13)
14. [Working with VST Plugins](#working-with-vst-plugins-14)
15. [Sounds, Patches and the Browser](#sounds-patches-and-the-browser-15)
16. [Routing Audio and CV](#routing-audio-and-cv-16)
17. [The Main Mixer](#the-main-mixer-17)
18. [Delay Compensation](#delay-compensation-18)
19. [Song File Handling](#song-file-handling-19)
20. [Importing and Exporting Audio](#importing-and-exporting-audio-20)
21. [Sampling](#sampling-21)
22. [The ReGroove Mixer](#the-regroove-mixer-22)
23. [Remote - Playing and Controlling Devices](#remote---playing-and-controlling-devices-23)
24. [Synchronization and Advanced MIDI](#synchronization-and-advanced-midi-24)
25. [Optimizing Performance](#optimizing-performance-25)
26. [Hardware Interface](#hardware-interface-26)
27. [Kong Drum Designer](#kong-drum-designer-27)
28. [Redrum Drum Computer](#redrum-drum-computer-28)
29. [Dr. Octo Rex Loop Player](#dr-octo-rex-loop-player-29)
30. [Europa Shapeshifting Synthesizer](#europa-shapeshifting-synthesizer-30)
31. [Grain Sample Manipulator](#grain-sample-manipulator-31)
32. [Mimic Creative Sampler](#mimic-creative-sampler-32)
33. [Thor Polysonic Synthesizer](#thor-polysonic-synthesizer-33)
34. [Subtractor Synthesizer](#subtractor-synthesizer-34)
35. [Malström Synthesizer](#malstrm-synthesizer-35)
36. [Monotone Bass Synthesizer](#monotone-bass-synthesizer-36)
37. [ID8 Instrument Device](#id8-instrument-device-37)
38. [Rytmik Drum Machine](#rytmik-drum-machine-38)
39. [Radical Piano](#radical-piano-39)
40. [Klang Tuned Percussion](#klang-tuned-percussion-40)
41. [Pangea World Instruments](#pangea-world-instruments-41)
42. [Humana Vocal Ensemble](#humana-vocal-ensemble-42)
43. [NN-XT Sampler](#nn-xt-sampler-43)
44. [NN-19 Sampler](#nn-19-sampler-44)
45. [MIDI Out Device](#midi-out-device-45)
46. [Quartet Chorus Ensemble](#quartet-chorus-ensemble-46)
47. [Sweeper Modulation Effect](#sweeper-modulation-effect-47)
48. [Alligator Triple Filtered Gate](#alligator-triple-filtered-gate-48)
49. [Pulveriser](#pulveriser-49)
50. [The Echo](#the-echo-50)
51. [Scream 4 Sound Destruction Unit](#scream-4-sound-destruction-unit-51)
52. [BV512 Vocoder](#bv512-vocoder-52)
53. [RV7000 Mk II Advanced Reverb](#rv7000-mk-ii-advanced-reverb-53)
54. [Neptune Pitch Adjuster and Voice Synth](#neptune-pitch-adjuster-and-voice-synth-54)
55. [Softube Amps](#softube-amps-55)
56. [Audiomatic Retro Transformer](#audiomatic-retro-transformer-56)
57. [Channel Dynamics Compressor & Gate](#channel-dynamics-compressor--gate-57)
58. [Channel EQ Equalizer](#channel-eq-equalizer-58)
59. [Master Bus Compressor](#master-bus-compressor-59)
60. [Synchronous Timed Effect Modulator](#synchronous-timed-effect-modulator-60)
61. [The MClass Effects](#the-mclass-effects-61)
62. [Half-Rack Effects](#half-rack-effects-62)
63. [The Combinator](#the-combinator-63)
64. [Pulsar Dual LFO](#pulsar-dual-lfo-64)
65. [RPG-8 Arpeggiator](#rpg-8-arpeggiator-65)
66. [Matrix Pattern Sequencer](#matrix-pattern-sequencer-66)
67. [Mixer 14:2](#mixer-142-67)
68. [The Line Mixer 6:2](#the-line-mixer-62-68)
69. [Menu and Dialog Reference](#menu-and-dialog-reference-69)
70. [Key Commands](#key-commands-70)

---

<a id="introduction-1"></a>
## 1. Introduction


This is the HTML Help for Reason Version 12 music production software from Reason Studios. The information in this HTML Help is also available as a PDF file - the Reason Operation Manual - which can be downloaded here.

If you haven't already, don't forget to check out the Video Tutorials web site, which can be accessed from the Help menu in Reason. Also, be sure to regularly check out www.reasonstudios.com for the latest news!

Whenever the manual instructs you to select an item from the “context menu”, it means that you should right-click (or [Ctrl]-click if you’re using a Mac with single-button mouse) on the specific area, section or device, and then select the item from the pop-up menu that appears - the context menu. The item list in context menus varies depending on where in the application you click. See “Context menus” for an overview of the context menus in Reason.

•

•

When you work with Reason, you will do a lot of navigating between the three main areas - the main mixer, the rack and the sequencer. The quickest way to switch between these areas is to use the function keys F5, F6 and F7 (see “Navigating between the areas” for details). Also, the F2, F3, F4 and F8 keys are shortcuts for showing and hiding the Spectrum EQ window, Browser, On-screen Piano Keys window and the Tool Window, respectively.
---

<a id="common-operations-and-concepts-2"></a>
## 2. Common Operations and Concepts


•

The areas can be viewed together, as in the picture above, in pairs or separately - see “Navigating between the areas”. The areas can also be resized - see “Resizing”.

•



See “About using the Browser in the detached rack” and “Creating devices” for information on how to use the “Device” functions.

•



See “Using the Browser” for information on how to browse for patches and songs.

•



See the “Sampling” chapter for information on how to use the “Song Samples” functions.

You can scroll in the Sequencer by using the Track scrollbar to the right and the Song Navigator at the bottom of the Sequencer - see “Scrolling” and “Zooming in the Sequencer”.

•



See the “Note and Automation Editing” chapter for information on how to use the various functions of the “Sequencer Tools” tab.

•



See “The ReGroove Mixer” chapter for information on how to use the functions of the “Groove Settings” tab.

See “On-screen Piano Keys” for more information.

In the Sequencer you have to manually switch to the Hand Tool by selecting it from the sequencer Toolbar. With the Hand Tool selected, you can scroll in any direction on the Edit/Arrangement Pane. Refer to “Hand Tool” for more information.

In the Sequencer it’s possible to zoom in and out horizontally using the Song Navigator. You can also use the Magnifying Glass Tool on the Sequencer Toolbar to zoom vertically - see “Magnifying Glass Tool”. In addition to this, it’s also possible to set a zoom level for the audio recordings inside the Audio Clips.

Using the Small Waveform Zoom Mode is especially useful if you have recorded with the Clip Safe function (see “Recording using the Clip Safe function in Propellerhead Balance”) where the dynamic range can be quite wide.

•
---

<a id="on-screen-piano-keys-3"></a>
## 3. On-screen Piano Keys


The Computer Keys keyboard range is fixed to 18 notes (from C to F), although the octave range will give you access to any notes within the ten octaves shown in the navigator. You can also click on the keys with your mouse to trigger notes. The numerical keys in the top row are not used to enter notes but to set velocity, see “Velocity”.

The first (leftmost) key represents C and so on up to F an octave above. By default, the [A]-key will play the first C, the [W]-key a C# and so on, according to piano keyboard standards. If you wish, you can customize the note to key assignment in the Preferences - Advanced page (see “Preferences – Advanced”).

See “Setting Octave range” for more ways of changing the Octave range.

| Item
---

<a id="audio-basics-4"></a>
## 4. Audio Basics


However, the number of available inputs and outputs depends on the number of inputs and outputs on your hardware audio interface. For example, if you are using a standard sound card with stereo inputs and outputs, only the first two inputs and outputs will be available. In the Hardware Interface, the indicators are lit green for all currently active and connected inputs and outputs. Activation of inputs and outputs on your hardware audio interface is done on the Audio page in the Preferences dialog (see “Active input and output channels”).

In most cases, you will want to have the Main Mixer Master Section device connected to outputs 1 and 2 of the Hardware Interface. This connection is made automatically as soon as you create a new Song document. However, there might be situations where you want to manually route audio to other outputs of the Hardware Interface. For example if you want to use the Control Room Outputs of the Main Mixer (see “Control Room output section”).

To send the sound of a device in the Rack to a specific output, you route the device output to the corresponding Output jack on the Hardware Interface. This is done by using the patch cables on the back of the rack, as described in “Manual routing”. If we flip the rack around, by pressing the [Tab] key, the Hardware Interface looks like this:

| Comment:

See “About latency” for more information about buffer size and latency. Also see “About audio rendering using the audio card buffer size setting” below for information on how to improve the DSP performance.

See “Max audio threads” for more details.

The “Render audio using audio card buffer size setting” function should be selected (checked) for best plugin performance. When selected, the audio batches are rendered internally according to the set Buffer size (see “Buffer Size settings” above). For example, if you have a Buffer size of 512 Samples, each audio batch will be 512 samples internally. Raising the Buffer size will let Reason process larger audio batches in one go, which is often more efficient. Many plugins are also more efficient when doing larger audio batches. if you are using DSP-heavy VSTs (mastering effects, for example), these will run a lot smoother with this function selected.

You could also use the MClass Maximizer as an insert effect on the Master Section in the Main Mixer to ensure that clipping never occurs - see “The MClass Maximizer”.

In some situations, the Audio Out Clip indicator on the Transport Panel and the Output Clip indicators on the Reason Hardware Interface might light up if the metronome Click is active in the sequencer during playback (see “Click and Pre-count”). This is nothing to worry about and won’t cause any distortion in your song. To determine if the metronome is causing the clipping indication, just disable Click and see if the clipping stops.
---

<a id="sequencer-functions-5"></a>
## 5. Sequencer Functions


This chapter describes the layout and general functions of the main sequencer. Recording, editing clips and events, arranging and working with Blocks in the sequencer are described in detail in the chapters “Recording in the Sequencer”, “Audio Editing in the Sequencer”, “Note and Automation Editing”, “Arranging in the Sequencer” and “Working with Blocks in the Sequencer”.

The sequencer is where you record your songs. The sequencer can be used to record audio tracks as well as instrument tracks, performance controllers, parameter automation and pattern automation. You can also arrange your songs, or parts of your songs, in Blocks. In Blocks mode you can build complete “sections” - consisting of a desired number of bars and tracks - that can be reused throughout the song. This chapter mainly describes the Song View and Edit Mode. Functions specific to Blocks and the Blocks View are described in the separate chapter “Working with Blocks in the Sequencer”.

On the Blocks track you arrange the Block automation clips that control which Block should play back (see “Working with Blocks in the Sequencer”).

In Edit Mode the Edit Pane shows detailed information about the content of one track (see “Tracks overview”), or lane (see “Lanes overview”) at a time and you can edit the events in individual clips (see “Clips overview”).

The sequencer Toolbar features various sequencer editing tools as well as the Snap function. The tools can be used in both Edit Mode and the Song/Block Views, with slightly different purposes in the respective modes. See “Toolbar details” for details about each tool.

To the left in the sequencer, all tracks are listed in the Track List. Each track in the sequencer is associated with a specific device in the rack. By clicking on a device icon in the Track List you automatically set Master Keyboard Input (see “Setting Master Keyboard Input”) to the corresponding device in the rack for playing and/or recording.

Most rack devices in a song automatically get their own dedicated track in the sequencer when you create the device. Each track can feature one or several lanes on which audio, note, performance controller, pattern and parameter automation events can be recorded - in clips. See “Track details” for more details about tracks.

Each track consists of one (default) or several parallel lanes. The lanes can contain clips that feature note events or audio recordings, depending on track type. A track can also feature automation lanes that contain clips with parameter automation events - or pattern automation for pattern based devices. See “Lane details” for more details about lanes.

Note, audio, performance controller, pattern and parameter automation events are always contained in clips. A clip is basically a “container” for recorded data. Audio clips are displayed in the Edit/Arrange Pane as a rectangular box with one or two graphical audio waves inside (mono or stereo). Note events are displayed in a “piano roll” fashion in the clip. Performance controllers and parameter automation events are displayed as continuous lines, and pattern events are displayed as repeated rectangles in the clips. See “Clip basics” for information about the different clip types.

The context sensitive Inspector shows the properties of whatever is currently selected in the sequencer: clips, notes, automation events, audio comp rows and cuts etc. The properties of the selected item can be edited by changing the values in the various displays. See “About the Inspector” for more info.

The Ruler is the song’s “time line”, measured in bars. In the Ruler, the Song Position Pointer indicates the current position in the song, i.e. in which bar the song is, or will begin, playing. The Ruler also shows the Left and Right Loop Locators as well as the Song End Marker. See “Ruler details” for more details.

To the far right in the sequencer is the Track scrollbar. With the Track scrollbar you can scroll vertically on the Edit/Arrange Pane. See “Scrolling” and “Zooming in the Sequencer” for more details.

Below the Edit/Arrangement Pane is the Song Navigator. With the Song Navigator you can scroll and zoom horizontally on the Edit/Arrangement Pane. The Song Navigator also features indicators for the Ruler’s Loop Locators, Song Position Pointer and Song End Marker. In the Song Navigator, all clips on all lanes are displayed as colored lines, indicating their positions in the song. See “Scrolling” and “Zooming in the Sequencer” for more details.

Note that when you create an instrument, the connected Mix Channel device doesn’t automatically get a track in the sequencer. If you want to record Mixer Channel automation, you have to first create a separate sequencer track for the Mix Channel device. See “Automation (non-instrument) track relationships”.

If you want to control an external MIDI instrument from the Reason sequencer you have to use the MIDI Out Device (see “MIDI Out Device”). The device works as a MIDI router in which you can define which MIDI Out Port and MIDI Channel you want the MIDI signals to be sent to from Reason. Since there is no internal audio involved in this setup, there is no Audio Track device or Mix Channel device present in the configuration.

A pure automation track is always associated with a “non-instrument” device, i.e. a device which can’t receive MIDI Note information. Consequently, an automation track can only consist of parameter automation lanes. Examples of non-instrument devices are Mix Channel devices with their corresponding Mix Channel strips, effect devices, mixer devices and Spider Merger & Splitter devices. The picture below shows an example with an automated Mix Channel:

The standard way of routing MIDI from a connected MIDI master keyboard or control surface to a device in the rack is to set the Master Keyboard Input in the sequencer. When MIDI is routed to a selected track in the sequencer, the notes and controller data are automatically echoed to the associated device in the rack. However, it is also possible to set Master Keyboard Input from the rack, see “Playing devices from the rack”.

By locking additional MIDI keyboards to separate devices in the rack, you will be able to play and record on several sequencer tracks simultaneously, see “Locking a surface”.

Besides the standard routing described above, it’s also possible to lock certain rack devices to specific control surfaces. See “Locking a surface” for more details.

It’s also possible to set Master Keyboard Input and track selection independently from each other by selecting “Separated” on the “MIDI” page in Preferences - see “Preferences – MIDI”.

•



Only one track at a time can have Master Keyboard Input. However, if you have locked additional MIDI keyboards to specific devices in the rack via Remote (see “Locking a surface”), you will be able to play and record these together with the track that has Master Keyboard Input.

The Blocks track is present at the top of the Track List only when the Enable Blocks function on the Options menu is on. On the Blocks track you can create Block Automation clips to decide which Blocks should play back. Refer to “Working with Blocks in the Sequencer” for more information about the Blocks feature.

The Transport track is always present at the top of the Track List and cannot be moved or deleted. The Transport Track can have a maximum of two lanes: one containing time signature automation, and the other containing tempo automation. See “Automating time signature” and “Editing tempo automation” for more details.

An audio track can only have a single audio lane containing clips with mono or stereo audio recordings. However, each audio clip can contain several recordings, i.e. different "takes". You can view and comp these takes in the Comp Editor. See “Audio Editing in the Sequencer” for more details. An audio track can also have parameter automation lanes containing automation for the Audio Track Channel strip parameters in the Main Mixer.

By default, the audio track is set up in mono. You can easily change to stereo by selecting “Stereo Input” in the “Audio Input” drop-down list - see “Selecting audio input(s) and defining mono or stereo”. If you select “Stereo Input”, the Audio Track channel strip in the Main Mixer automatically switches to a stereo channel.



A MIDI Out Device is created in the rack and the associated track is automatically created in the sequencer. See “MIDI Out Device” for more details on how to configure the MIDI Out Device for controlling external MIDI instruments.

For non-instrument devices, such as effects devices and Mix Channel devices, you need to manually create a track if you want to record parameter automation. You can do that either by following the description below or by following either of the two last descriptions in “Creating/adding parameter automation lanes”.

2.

See “About Device Groups” for information about device groups.

•

Note that folded tracks (see “Folding tracks”) cannot be resized.

See “About Device Groups” for more information about device groups.

The tracks will be deleted without an alert but you can always use the Undo function. See “Undo and Redo”.

If you have deleted a track for a device and want to create a new track for the device, follow the descriptions in “Creating a parameter automation track for a non-instrument device” or “Short-cut for creating a Mix Channel track or Audio track”.

See “About Device Groups” for more information about device groups.



The track color is shown in the track background in the Track List. The associated Audio Track device or Mix Channel device in the rack and its corresponding channel strip in the Main Mixer will also be assigned the new color. The selected track color will be reflected in all new clips you record or draw on this track.



See “About Device Groups” for more information about device groups.















In Tuner mode, you can tune a connected instrument - an electric guitar, for example. See “Using the Tuner” for more info.

To the right of the Tuner button is the Select Audio Input drop-down list. Here, you select which audio input(s) to use for the track. See “Selecting audio input(s) and defining mono or stereo” for more info.

The Input Meter shows the level(s) of the input signal(s). If the selected audio input is mono, the Input Meter displays a single LED bar. If the audio input is in stereo, the Input Meter displays two parallel LED bars. See “Setting input level(s)” for details about setting input levels.

•

To the right of the “Record Enable” button is the “Groove Select” drop-down list. Here you can select a ReGroove channel for all clips on the lane. See more about ReGroove in “The ReGroove Mixer”.

•

To the far right is the “Delete Automation Lane” (X) button. Clicking this button will delete the lane (and all clips on it). If there are clips on the lane, a dialog appears prompting you to confirm deletion. See “Deleting parameter automation lanes” for alternative ways of deleting parameter automation lanes.

•

To the far right is the “Delete Pattern Lane” (X) button. Clicking this button will delete the lane (and all clips on it). If there are clips on the lane, a dialog appears prompting you to confirm deletion. See “Deleting pattern lanes” for alternative ways of deleting pattern lanes.

•

A new note lane will be created and automatically record enabled. See “Recording notes using the “Dub” and “Alt” functions” for more details.

A new note lane will be created and automatically record enabled. At the same time, the previous note lane, or (if loop is activated and the Song Position Pointer is between the Left and Right Locators) the clips between the Left and Right Locators, will be muted. See “Recording notes using the “Dub” and “Alt” functions” for more details.

•



Only the basic properties and functions pertaining to clips are described here. See “Arranging in the Sequencer” for in-depth details about what you can do with clips.



The Mute Tool is used for muting clips in the arrangement - or lanes in Block automation clips (see “Muting lanes in Block Automation Clips”).







The Speaker Tool is used for auditioning slices or notes in Single Take audio clips, and for auditioning individual recordings on Comp Rows in Comp Clips. See “Slice Edit mode tools”, “Auditioning notes” and “Comp Editor audio editing tools” for details.

#Snap



However, there’s one exception: If a note clip is open in Edit Mode and you click in the Clip Overview (see “Edit Mode elements”), the clip will remain open but the Snap value for arranging will be selected. This allows you to e.g. move or resize the clip in the Clip Overview just like in the Song/Blocks View, without closing it first.

| Function

You can change the positions of the Song Position Pointer, Locators and Marker in the Ruler by clicking and dragging them to desired positions in the Ruler. Note that you have to click and drag the “flags” in the Ruler - not the lines. The Song Position Pointer and Loop Locators can also be moved by typing in new positions in the respective Position displays in the Sequencer Transport Panel (see “Song Position” and “Left and Right Locator Positions”). Another way of moving the Song Position Pointer is by using the Rewind and Fast Forward controls on the sequencer Transport Panel (see “Rewind and Fast Forward”).

#Keys

See the “On-screen Piano Keys” chapter for more information.

Refer to “The ReGroove Mixer” chapter for more information.

When the Q Record button is on, all recorded MIDI notes will be quantized to the currently selected quantization grid. Refer to “Quantize” for more information on quantization.

Refer to “Quantize” for more information on quantization.

Refer to “Quantize” for more information on quantization.

Here you can set the desired synchronization mode for the Reason sequencer: Internal, MIDI Clock (if applicable) or Ableton Link (if applicable). You can also choose “Send MIDI Clock” to sync other applications/instruments from Reason (if applicable). See the chapter “Synchronization and Advanced MIDI” for more information about synchronization.

The current song position is shown in the display. The song position is where the Song Position Pointer in the Ruler (see Ruler details) is at the moment. The display is divided into Bars, Beats, 1/16th Note and Ticks (there are 240 Ticks for each 16th note) segments. You can edit the position of the Song Position Pointer, and thus change the song playback position, according to the descriptions in “Transport Panel segment displays”.

The current position of the Song Position Pointer in the Ruler (see Ruler details) is shown in time format (hours, minutes, seconds and milliseconds) in the display. You can change the position in time of the Song Position Pointer, and thus change the song playback time position, according to the descriptions in “Transport Panel segment displays”.

The click will sound on every beat, with the first beat in every bar accented (higher pitched). See “Click and Pre-count” for more details.

Pre-count will only be present before recording - not before regular playback. See “Click and Pre-count” for details about selecting number of pre-count bars etc.

See “Click and Pre-count” for more details.

The current song tempo is shown in the display in BPM (Beats Per Minute) and 1/1000 of a BPM. You can edit the tempo according to the descriptions in “Transport Panel segment displays”. The Tempo range is 1.000-999.999 BPM.

The current song time signature is shown in the display. You can edit the time signature according to the descriptions in “Transport Panel segment displays”.

•

•

Alternatively, press [\*] on the numeric keypad or hold down [Ctrl](Win) or [Cmd](Mac) and press [Return] on the computer keyboard. If Pre-count has been activated (see Pre(-count) On/Off above), the recording will begin after the set number of pre-count bars.

Clicking on any of these buttons will add additional audio tracks or note lanes for overdub purposes. Refer to “Overdubbing audio using the “Dub” function” and “Recording notes using the “Dub” and “Alt” functions” for more details about these functions.

The current positions of the Left and Right Locators in the Ruler (see Ruler details) are shown in the displays. The display is divided into Bar, Beat, 1/16th Note and Ticks (there are 240 Ticks for each 1/16th Note). You can change the positions of the Locators, and thus change the loop playback region, according to the descriptions in “Transport Panel segment displays”.

| Function

The Inspector, located above the Edit/Arrangement Pane, can be used for a number of different editing purposes pertaining to clips, events and recordings. The Inspector is context sensitive, meaning it will have different content and functionality depending on what is currently selected. How to edit using the Inspector is described in detail in the sections “Resizing clips using the Inspector”, “Moving clips using the Inspector”, “Editing recordings and cuts in the Inspector” and “Editing notes and events in the Inspector”.

The “Match Values” function in the Inspector can be used to match the positions, lengths and/or values of several selected clips, notes, events or recordings to the position, length and/or value of the topmost (or leftmost) selected clip, note, event or recording. Refer to “Matching clips using the “Match Values” function”, “Matching audio values using the "Match Values" function” and “Matching notes or events using the “Match Values” function”.
---

<a id="recording-in-the-sequencer-6"></a>
## 6. Recording in the Sequencer


This chapter describes the different recording techniques that you can use in Reason. The chapter covers both audio, notes and parameter automation recording. Before you read this chapter, it’s recommended that you are familiar with the basic sequencer functions and definitions described in the “Sequencer Functions” chapter. A lot of functions are common for all types of recording methods. These will be described first in this chapter. Later in the chapter we will go into functions specific to audio, notes and parameter automation recording.

Activated Enable Record and Enable Record Parameter Automation buttons are indicated with a red color. Recording can be simultaneously enabled on an unlimited number of audio tracks (limited only by the computer’s processing and hard disk performance) - plus one note lane on an instrument track. However, if you have locked several MIDI keyboard controllers to specific instrument devices in the rack - using Remote (see “Locking a surface”) - you can record MIDI on these instrument tracks simultaneously. Recording of parameter automation can be simultaneously enabled on as many tracks as you like.

Selecting an audio track will automatically record enable the track if you have selected “Standard” mode in the “Master Keyboard Input” section on the “MIDI” page in the Preferences dialog (see “The Master Keyboard Input setting”) - and if the Manual Rec button in the Track List is Off, see “About the Manual Rec function”.

Also, depending on the setting in the “Monitoring” section on the “Audio” page in Preferences, monitoring of the input signal to the audio track may, or may not, be automatically activated - see “Monitoring”.

If you have selected “Standard” mode in the “Master Keyboard Input” section on the “MIDI” page in the Preferences dialog (see “The Master Keyboard Input setting”), selecting an instrument track will automatically set Master Keyboard Input to that track - if the Manual Rec button in the Track List is Off, see “About the Manual Rec function”. An instrument track that has Master Keyboard Input will automatically be record enabled, and will also be enabled for parameter automation recording, indicated by the red Record Enable Parameter Automation button.

Only one note lane on one instrument track can have Record Enable active at a time, unless you have locked additional MIDI keyboard controllers to specific instrument devices in the rack (see “Locking a surface” in the Remote chapter). If you only have one MIDI keyboard controller (assigned as Master Keyboard), you can only record notes on one note lane at a time (see “Setting Master Keyboard Input”).

If you have locked additional MIDI keyboard controllers to specific instrument devices in the rack (see “Locking a surface” in the Remote chapter), the corresponding tracks for all these locked devices are automatically record enabled - if the Manual Rec button in the Track List is Off, see “About the Manual Rec function”. These additional record enabled tracks are all displayed with the gray “Master Keyboard Input” symbol to the left of the device icon in the track list, and their Record Enable buttons are also automatically switched on. The track with “normal” Master Keyboard Input is also indicated with the gray Master Keyboard Input symbol to the left of its device icon.

If you change your mind and want to record audio on an audio track, you have to manually record enable it by clicking its Record Enable button as described in “Record enabling an audio track”. Alternatively, switch off the Manual Rec button to enable the automatic record enabling again.

Pattern automation can be recorded on tracks associated with pattern based devices such as the Redrum Drum Module, Dr. Octo Rex Loop Player or Matrix Analog Pattern Sequencer. Enabling pattern automation works in the same way as enabling regular parameter automation (see “Record enabling parameter automation”).



The behavior when recording in loop mode differs depending on what you’re recording - audio, MIDI or parameter automation. Refer to “Recording audio in Loop mode”, “Recording notes in Loop mode” and “Recording parameter automation in Loop mode”.

The following description applies to all types of recording: audio, MIDI and parameter automation. For specific details of audio, MIDI and parameter automation recording, refer to “Recording audio”, “Recording notes”, “Recording performance controller automation” and “Recording parameter automation”.

1.

2.



If you are going to record complex/difficult takes, a good suggestion is to lower the song tempo during recording and then speed up the song to normal tempo again during playback. For audio tracks, Reason features very sophisticated functions for audio stretching. Audio stretch enables you to alter the song tempo up or down without changing the pitch of the recorded audio. See “About tempo changes and tempo automation of audio tracks” for more details.











See “Recording using the Clip Safe function in Propellerhead Balance” for more information about using the Clip Safe function.

See “Using the Tuner” for more information about the Tuner.

See “Using the Clip Safe function with Propellerhead Balance” for more details.



From here, it’s easy to assign the best parts from the different takes and comp them into a final clip. See “Creating a comped audio clip” for details.

This will create a new audio track with a duplicate of the original audio track settings, including the channel strip settings (with insert effects etc.). Now, you can continue recording on the new audio track as described in “Recording audio” and “Recording audio in Loop mode”. Afterwards, you can edit the new track completely independently of the original track.

Closely related to the “Dub” function, described in “Overdubbing audio using the “Dub” function”, is the “Alt” function. This function can be used to create a new audio track with an identical copy of the selected audio track’s settings. The only difference between the “Alt” and “Dub” functions is that the Alt function will automatically mute the original audio track.

This will create a new audio track with a duplicate of the original audio track settings, including the channel strip settings (with insert etc.). Now, you can continue recording on the new audio track as described in “Recording audio” and “Recording audio in Loop mode”. Afterwards, you can edit the new track completely independently of the original track.

If you start recording over an existing clip on an audio track, the new recording will incorporate (replace, but not erase) the previous recording in the clip. When you open the audio clip in the Comp Editor afterwards, there will be one Comp Row for each of the takes, the same result as when recording audio in Loop mode (see “Recording audio in Loop mode”).

See “Creating a comped audio clip” for details on how to extract parts from individual takes and comp into a final clip.

You might have the individual drums of your drum kit on separate tracks and these tracks are routed to a Mix Channel which is set to work as an Output Bus (see “Output Busses”). You then want to record the audio from the Output Bus onto a new Audio Track.

In this situation, all you need to do is create a new Audio Track, activate the Rec Source button on the Output Bus Mix Channel device, and then select the Output Bus in the Select Audio Input drop-down list on the Audio Track in the Track List. Then, record the audio from the Output Bus as described in “Recording audio”.



1.

Note events can be recorded for instrument devices and are contained in note clips. Performance controller events, such as Mod Wheel, Pitch Bend and Aftertouch events, can also be recorded for instrument devices, and be contained in note clips, but they are described separately in “Parameter automation recording details”.

To record notes for an instrument device - or for an external MIDI instrument - on a track in the sequencer, you need only create an instrument track as described in “Creating an instrument track”. The instrument track will automatically have Master Keyboard Input and the note lane will automatically be record enabled. Since you will only be recording MIDI events on the instrument track - and no audio - there is no need to adjust audio levels etc. These can always be adjusted afterwards.

If you want to control an external MIDI instrument, simply create a MIDI Out Device and select the appropriate MIDI port and channel on the device panel. See “MIDI Out Device” for more details.

It’s possible to quantize MIDI notes as they are being recorded. This will automatically align the start positions of the recorded notes to a pre-defined grid. Refer to “Quantize” for more details.







Recording over or into an existing note clip will simply add new note events to the previously recorded events in the note clip as described in “Recording notes in Loop mode”. However, If the new recording should start before the original clip, and expand into the original clip, a new clip will be created and will engulf the original clip. Let’s have a look at the following example:



Another, perhaps more convenient, way of overdubbing on an instrument track is to create additional note lanes and record new clips on these using the New Dub or New Alt functions described in “Recording notes using the “Dub” and “Alt” functions”. This way, you will get a better overview of exactly what you added in each of your recordings.

When using the “Alt” function in Loop mode, the clips between the locators will be muted - not the entire note lane. If the locators are placed over an existing clip, as in the example above, clicking the “Alt” button in Loop mode will split the clip and mute the clip between the locators.

In Reason, you can automate virtually any device and channel strip parameters and create completely automated mixes if you like. This is done by recording parameter events in the sequencer. It’s also possible to record sequencer Tempo automation (see “Tempo automation recording”).

The key feature with performance controller automation is that it’s contained together with the notes in the note clip. Moving the note clip moves the performance controller automation as well. Therefore, if your controller changes are part of your "note performance" (e.g. Pitch Bend and Sustain Pedal), then you want them as performance controllers (see “Recording performance controller automation”).

Filter sweeps played together with the notes etc. can also be recorded as performance controllers (see “Recording parameter automation into Note Clips”).

Track parameter automation is recorded on separate lanes on the track (one lane for each automatable parameter). Track parameter automation clips can be moved individually, independent from any note clips. See “Recording parameter automation”.











2.



While recording on a note lane according to the description in “Recording notes”, tweak the parameter(s) you want to automate on the instrument device panel in the rack - or use a Remote MIDI controller (see “Remote - Playing and Controlling Devices”).

However, if the new recording should start before the original clip’s start position, a new clip will be created which will incorporate the original clip. The new automation data will replace the existing one, but any existing note events will not be affected (see “Recording parameter automation over or into an existing clip” and “Recording over or into an existing note clip”).

Parameter automation is the standard way to automate device and channel strip parameters. Each automated device/channel strip parameter will generate a separate automation lane on the track. It’s also possible to record automation of the Tempo on the Transport Panel. This is described in detail in “Tempo automation recording”.



1.

2.







Recording parameter automation events in Loop mode works similar to “non-looped” recording (see “Recording parameter automation”), except that for every new loop cycle any changed parameter value will replace the previously recorded value for the corresponding parameter.

1.



When recording is activated, all automation record enabled tracks will record track parameter changes from their respective devices in the rack. This is especially useful if you have assigned parameters on several devices to a single control on a MIDI control surface, or have multiple control surfaces controlling different devices in the rack while you’re recording. See “Remote - Playing and Controlling Devices” for details.

You can move pattern changes to other positions by moving or resizing the pattern clips, see “Editing pattern automation”.

•

This allows you to create unlimited variations by later editing the notes in Edit mode. See “The “Convert Pattern Automation to Notes” function”.

Automating tempo is done much in the same way as with other parameter automation. You record the tempo changes by changing the Tempo value on the Transport Panel. When you later play back, audio clips will automatically be stretched to follow the tempo changes (unless you have disabled stretch for the clips - see “About disabling Stretch for audio clips”). Note clips and automation clips will always follow tempo changes.
---

<a id="arranging-in-the-sequencer-7"></a>
## 7. Arranging in the Sequencer


The clip Position display shows at what position in the song the clip begins. The display readout is divided into Bar, Beat, 1/16 Note and Ticks (1/16th note=240 Ticks). The position can be edited according to the descriptions in “Moving clips using the Inspector”.

The clip Length display shows the length of the clip. The display readout is divided into (from left to right) Bar, Beat, 1/16 Note and Ticks. The length can be edited according to the descriptions in “Resizing clips using the Inspector”.

The Fade In and Fade Out displays for selected audio clips show the Fade In and Fade Out times for the audio in the clip. The readout is divided into 1/16 Note and Ticks. The Fade times can be edited as described in “Inspector segment displays”.

The Level display for selected audio clips shows the level of the audio in the clip. The readout is divided into dB and 1/100 dB. The level can be edited as described in “Inspector segment displays”.

The Transpose display shows the transposition of the audio recordings in the selected Audio Clip(s) - relative to the original pitch. The display readout is divided into (from left to right) Semitones and Cents, See “Transposing Audio Clips”.

In Song View, several clips can be selected, e.g. for cutting, copying, pasting, deleting, moving and resizing purposes. If you select multiple note clips, these can be opened for Multi Lanes editing, see “Multi Lanes editing”.

Besides the Clip Resize handles, a selected audio clip also has Fade In and Fade Out handles plus a Clip Level handle. These can be edited at any time, either by using the handles as described below, or using the Inspector as described in “Fade In and Fade Out displays (audio clips only)” and “Level display (audio clips only)”:

The Fade settings can be set individually for each audio clip in the song. The fading is non-destructive and can be changed at any time. If Snap is activated (see “Snap”), the set Snap value is taken into account when setting the fade time(s).

You can also draw selection rectangles with the Selection tool, encompassing several clips and delete them all at once. The same rules apply as when selecting clips (see “Selecting clips”).

If you resize a clip and make it smaller, any recordings or events that now lie outside the clip boundaries will not sound, or have any effect, when played back. However, they are not deleted - just masked. If you make the clip larger again, the recordings or events that were masked will become visible and will play back again. See “About masked recordings and events”.

See “Inspector segment displays” for more details on how to edit in the Inspector displays.

•

Masked performance controller events, parameter automation events and pattern automation events will be inactive - but could still affect the masked clip (see “About masked performance controllers and automation events” below). Outside a masked clip, the controller/parameter/pattern values will default to their Static Values in the masked area (see “Static Value Handles”).



Below, we will describe how to use the “scale tempo” tool to manually stretch clips. Numerical tempo scaling in the Tool Window is explained in “Scale Tempo” in the “Note and Automation Editing” chapter.

For more details about tempo scaling audio clips, refer to “Tempo scaling Clips” in the “Audio Editing in the Sequencer” chapter.

It’s also possible to select and move several clips by dragging and dropping them at the desired destination. If the Snap function is selected (see “Snap”), you will only be able to move the clip(s) in steps of the selected Snap value - or to absolute positions on the grid, depending on the Snap settings.







•

The set Snap value is taken in to account if the function is activated (see “Snap”). It’s also possible to move several selected clips in one go.



•



If you have recorded non-standard controller parameters for a device in the note clip using the “Record Automation into Note Clip” option (see “Recording parameter automation into Note Clips”) some automated parameters may not have an equivalent parameter in the target device.

Any lane can only play back a single clip at a time - if you want to mix two clips, put them on separate lanes (note clips) or on separate tracks (audio clips). See “Adding note lanes” and “Duplicating/copying tracks and devices”.



•

2.



Activate Snap (see “Snap”) and set the Snap value to “Bar” (or to the length of the section you want to repeat).

On the Razor Tool’s left edge is a cross-hair which indicates where the split will take place. If activated, the Snap setting is taken into account (see “Snap”).



4.

It’s also possible to reverse clips, i.e. play the content of the clip “backwards” (from the end to the start). This works a little differently for audio clips and note clips. Please refer to “Reverse” for information about reversing note and automation clips, and to “Reversing audio clips” for information about reversing audio clips.



•



for creating audio clips that you could use as samples in any sample player device (see “Bounce Clip(s) to New Sample(s)”) or as REX loops in the Dr Octo Rex (see “Bounce Clip to REX Loop”).



•
---

<a id="audio-editing-in-the-sequencer-8"></a>
## 8. Audio Editing in the Sequencer


This chapter describes how to edit audio clips after you have recorded them in the sequencer. General sequencer functions, recording, note and automation editing, and arranging in the sequencer are described in detail in the chapters “Sequencer Functions”, “Recording in the Sequencer”, “Note and Automation Editing” and “Arranging in the Sequencer”.

Slice editing can be made on Single Take clips (see “Clip Types” below). Single Take clips can be opened for editing in Slice Edit mode in the Arrange View, similar to when editing parameter automation clips. Slice editing allows you to adjust the positions (timing) of the automatically detected and distributed transient slice markers that appear in the audio clip. The timing can be adjusted by moving and stretching (warping) the audio slices. See “Editing audio in Slice Edit mode”.

In Pitch Edit mode you can graphically correct and edit the pitches of monophonic audio in Single Take clips -   
perfect for vocal pitch correction/manipulation. See “Editing audio in Pitch Edit mode” for more information.

perfect for vocal pitch correction/manipulation. See “Editing audio in Pitch Edit mode” for more information.

In Comp Edit mode you can cut out segments of several Takes (recordings) and compile into a final clip. Here you can also insert silence segments to e.g. remove noise from silent parts in your audio clips. See “Editing audio in the Comp Editor”.

The Stretch and Transpose Type, together with the Clip Type, also determines the default Edit Mode in which the clip will open when you double-click it, see “Opening audio clips for editing”. However, you can always change the Edit Mode for a clip manually, if you like.

The formants are preserved and are not transposed along with the audio. This will keep the original character of the vocal and will only affect the pitch. “Vocal” is also the default Stretch and Transpose Type for editing audio in Pitch Edit mode, see “Editing audio in Pitch Edit mode”.

When the audio clip is in Slice Edit mode you can stretch, move and quantize audio slices etc., see “Editing audio in Slice Edit mode”. When the clip is open in Pitch Edit mode you can pitch-correct and transpose individual notes (pitches) in monophonic audio recordings, see “Editing audio in Pitch Edit mode”. When the clip is open in Comp Edit mode you can alternate the playback between several recordings and compile into a single recording, see “Editing audio in the Comp Editor”.







•

If more than one Slice Marker has been selected, a Slice Group Handle appears below the waveform. You could then click and drag the Slice Group Handle sideways to move all selected Slice Markers as a group, see “Moving several Slice Markers”.

The range of Slice Markers can then be moved as a group by clicking and dragging the Slice Group Handle sideways. You can also stretch the range in an “accordion style” fashion by clicking and dragging any of the selected Slice Marker Handles in the range, see “Stretching a range of Slices”.

Now, you can move all Slice Markers as a group by dragging the Slice Group Handle sideways (see “Moving several Slice Markers”), or stretch the entire range of Slices (see “Stretching a range of Slices”).



If you are not satisfied with the position of the Slice Marker, you can reposition it afterwards, see “Repositioning Slice Markers”.











•



It’s also possible to move a range of Slices by selecting a range of Slice Markers as described in “Selecting Slices and Slice Markers” and then dragging the Slice Group Handle sideways.











If you like, you can now select the desired clip(s) and move, reverse (see “Reversing audio clips”) or choose to bounce the clip(s) to samples (see “Bounce Clip(s) to New Sample(s)”).



Refer to the “Dr. Octo Rex Loop Player” chapter for information on how to work with REX Loops in the Dr Octo Rex device.

If you want to load your REX Loop in another sampler device, you first have to un-self-contain the REX file, see ““Un-self-containing” a Song”. Then, create the sampler device and load the un-self-contained REX file from disk.

3.

Hold this and move sideways to move the note back or forth in time. The range is limited by the adjacent notes, which are indicated by the Note Lines, see “Moving notes and changing note lengths”.

These indicate where the notes start and end. You can adjust the start/end positions by click-holding a Note Line and dragging it sideways. Changing the position(s) and/or length(s) will also automatically stretch the note(s). See “Moving notes and changing note lengths”.

The Drift handle appears when you select the note(s). Drag the Drift handle downwards to reduce the amount of any natural pitch drift/vibrato present in the selected note(s), see “Attenuating pitch drift/vibrato”.

The Transition handle(s) control the pitch transition times between the selected note(s) and the previous adjacent note(s), see “Editing transition times”.

This is a three-way switch that determines what happens when you drag notes up/down on the note pane:   
Snap = the notes snap to absolute semitones.  
Jump (default) = the notes snap relative to their original pitches, i.e. moves in semitone steps but preserves any fine tuning.  
Fine = the notes can be transposed freely, in cents.  
See “Changing transposition” for more details about transposing notes.

Snap = the notes snap to absolute semitones.

Jump (default) = the notes snap relative to their original pitches, i.e. moves in semitone steps but preserves any fine tuning.

Fine = the notes can be transposed freely, in cents.

See “Changing transposition” for more details about transposing notes.















2.

Similar to when editing in Slice Edit mode it’s possible to “decouple” the notes from the actual audio in the note. This can be useful if the automatic note placement wasn’t perfect and you have a hard time adjusting the transition times between transposed notes (see “Editing transition times”).

Quantizing notes in Pitch Edit mode works just like when quantizing in Slice Edit mode, see “Quantizing audio”.

#Note

For more information about formants, please have a look at “What are formants?” in the Neptune Pitch Adjuster and Voice Synth chapter.

In this section we will describe audio editing procedures that are common for Single Take clips and Comp clips when edited in the Comp Editor. Comp clip specific procedures are described in “Comping audio”.

Click and drag these handles horizontally to introduce a fade in and/or fade out of the audio in the clip. The fading is non-destructive and can be changed at any time. If Snap is activated (see “Snap”), the set (Arrange Mode) Snap value is taken into account when moving the Fade Handles.

•

Depending on how you recorded the audio clip, there can be one or several Comp Rows, containing one audio recording each. Comp Rows can be described as “virtual tracks” in the sense that you can have many parallel Comp Rows in an audio clip but only play back from one Comp Row at a time (see “Creating a comped audio clip”). In Single Take clips, only the audio recording on the currently selected Comp Row will play back.

A Comp clip consists of several Comp Rows, with one recording on each Comp Row. If you have recorded several takes in an audio clip and want to cut out sections of the various takes and comp into a final clip, this can be done in the Comp Editor (see “Creating a comped audio clip”). This is how an already comped audio clip could look like in Comp Edit mode:

•

•



















•

See “Adding Cuts” for more details on how to use the Cut Tool.

The Razor Tool can also be used for assigning a complete Segment, with a start and end Cut, by clicking and dragging (swiping) the Razor Tool horizontally on the desired Comp Row. See “Adding Segments” for more details on how to swipe with the Cut Tool.

Select one or several Comp Rows (see “Selecting Comp Rows”) and then press [Backspace] or [Delete], or select “Delete” from the Edit menu or context menu.







Duplicating Comp Rows can be useful if you want to re-use the same part of a take several times in a comped clip. Duplicate the Comp Row and then adjust the Recording Offset (see “Adjusting the Recording Offset”) in the duplicated Comp Row to access the same part of the recording in another segment of the comped clip. Duplicating Comp Rows will not use up any more space on your hard disk, so you can do this as many times as you like.

In this section we will describe procedures that are specific to audio editing in Comp clips. At the end of this section is a detailed example on how to use the various procedures to create a complete comped audio clip - see “Creating a comped audio clip”. General audio editing procedures are described in “Editing audio in the Comp Editor”.



•



If you’re happy with the result and don’t plan to edit the clip any further, you can use the “Delete Unused Recordings” function to delete the recordings on the original Comp Rows and reduce the file size (see “Delete Unused Recordings”). If file size is not an issue, you can keep the original takes in the clip. This way you can switch to Comp Mode at any time if you need to edit the comp.



If you have recorded more than one loop cycle of audio in Loop Mode (see “Recording audio in Loop mode”), or recorded over or into an existing audio clip (see “Recording over or into an existing audio clip”), each recording has been placed on a separate Comp Row. If you like, you can now select the best parts (segments) of the recordings on the various Comp Rows and create a final “comped” audio clip. All editing described below is non-destructive and can be changed at any time:

Audition the recordings on the Comp Rows to decide which recordings to use at what position in the comped clip. Select the Speaker Tool and click-hold at desired positions on the different Comp Rows (see “Speaker Tool” for details).







The clip is then also automatically set to Single Take mode, which makes it possible to edit the clip in Slice Edit mode, where you can stretch and quantize the audio etc. (see “Editing audio in Slice Edit mode”), or in Pitch Edit mode, where you can correct and edit the pitches of monophonic audio recordings (see “Editing audio in Pitch Edit mode”).

•

The Audio Clips are bounced to new Song Samples and named according to the Audio Clip name (if the clip was named) or according to the Audio Track name with serial numbers. The bounced Audio Clips then end up as sample files in the Song Samples location in the Browser. Refer to “Sampling” for more details about sampling and sample editing.

The “Bounce > Bounce Clip to Disk” function on the Edit menu and clip context menu allows you to export the audio of a selected clip to disk as a single WAV or AIFF file. This might be useful if you want to process an audio clip in an external application and then re-import the clip to the track again. See “Bouncing Audio Clips” for more details.

The Scale Tempo function can also be applied to clips numerically in the Tool Window, see “Scale Tempo”.







•

•







See “Inspector segment displays” for details on how to edit in the Inspector displays.

For Cut Handles, only Crossfade values can be matched - not the Positions. See “Matching audio values using the "Match Values" function”.
---

<a id="note-and-automation-editing-9"></a>
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
## 16. Routing Audio and CV


Gate outputs/inputs are typically used to trigger events, such as note on/off values, envelopes etc.

See "Manual routing" for a description of routing methods.

This allows you to e.g. change the order of effect devices in a signal chain by Shift-dragging them.

If you are duplicating a complete Device Group (see "Duplicating devices"), this will often include a Mix Channel. In this case, the Mix Channel will also be duplicated, with no need for further auto-routing.

Note that routing cables can be done regardless of the "Reduce Cable Clutter" setting on the Options menu. This means that you can connect cables even though they are hidden (see "Cable appearance").

On the back of each device you will find connectors of two different types: audio and CV (Control Voltage, used for controlling parameters - see "Using CV and Gate"). Audio inputs and outputs are shown as large quarter inch jacks, while CV input and output jacks are smaller. For now, we'll stick to the audio connections.

Conversely, if you would like to apply Gate or CV modulation to more than one voice, you should not use the Sequencer Control inputs, as these only function monophonically.

See the chapter "Matrix Pattern Sequencer" for more tips about using CV.

---

<a id="the-main-mixer-17"></a>
## 17. The Main Mixer


A Mix Channel device acts as a host to a source device (e.g. an instrument device). When you create an instrument, a Mix Channel device is added automatically to the rack and a corresponding Mix Channel strip is added to the Main Mixer. You can also create Mix Channels manually from the Devices tab in the Tool Window or from the Create menu. This is useful if you need to make manual mixer routings - see "Advanced routing tips and tricks" at the end of this chapter.

The Mix Channel device has inputs to which the source (instrument) device is connected. The Mix Channel device and channel strip will automatically be assigned the name of the connected source device, but this can be changed - see "Naming mixer channels".

A Mix Channel device will not automatically have a corresponding track created in the sequencer (but the connected source device will). Mix Channel tracks are created manually and used for automating channel strip parameters - see "Automating mixer parameters".

The Master Section device is always present and is fixed in the rack, just below the Reason Hardware Interface. This is where all your Audio Track and Mix channels are summed and mixed to stereo, and where you set up your Send effects and Master Insert effects. For descriptions of how to set up and use effects, see "Insert FX" and "Send FX".

Each section has a section name header in the channel strip. The sections are as follows (from the top down): Input, Dynamics, EQ, Inserts, FX Sends and Fader. (See "The channel strip" for descriptions of each section.)

The channel will get Edit Focus (see "Channel Header section") and be scrolled into view in the Main Mixer. If you have both the sequencer and Main Mixer in view, or the rack and Main Mixer, clicking a track in the Track List, or on a Mix Channel/Audio Track device in the rack, will flash the corresponding channel strip in the Main Mixer.

Mixer channel strips are automatically created when you create Audio Track and Mix Channel devices. In most situations, a Mix Channel device (with its channel strip) is also automatically created when you create an instrument device (see "Creating devices").

If there are devices connected to the Mix Channel device you delete, and "Auto-group Devices and Tracks" is selected on the Options menu, the alert will ask if you want to delete only the selected device, or all devices in the Device Group (see "About Device Groups" for more information).

This allows you to e.g. change the Fader levels of all selected channels simultaneously (see "Changing Fader section parameters on multiple channels simultaneously"), or move or delete several channels in one go. The last selected channel will be given edit focus which is indicated by a red strip in the channel header (see "Channel Header section").

Resetting channel settings initializes all channel strip parameters to default values and removes any insert effects (see "Insert FX section") from the channel.

See "Using compression sidechaining" for a description of further uses of sidechaining.

The Insert effects can be placed ahead of the Dynamics and EQ sections in the signal path, see "Signal Path section".

See "Insert FX" for descriptions of how to create and work with Insert effects.

Send effects, which are global for all channels in the Main Mixer, are connected to the Master Section rack device. Up to 8 Send effects can be used simultaneously. For a description of how to use Send effects, see "Send FX".

The Remote Base Channel indicator - To the left in the same horizontal strip area a small yellow arrow symbol can be shown. This is the Remote Base Channel indicator, which shows which channel is considered the first or base channel when using Remote Control - see "Setting the Remote Base Channel".

The Master Compressor can be applied pre or post Master Insert section - see "Master Inserts section".

This section controls the master levels of the FX Returns. Send effect devices are connected to the Master Section via the eight FX Send and eight FX Return connectors on the Master Section device. See "Send FX" for a description of Send FX.

The Control Room outputs are located on the back of the Master Section device. To use the Control Room output section, the outputs have to be connected to your monitor system. This can be done by manually patching cables from the "Ctrl Room Out" connectors to a separate output pair on the Reason Hardware Device - see "Manual audio routing".

The total delay of the Main Mixer signal (at the Master Out) is displayed below the display. See the "Delay Compensation" chapter for more information about delay compensation in Reason.

By definition, insert effects are inserted in the signal chain and process the whole channel signal, as opposed to Send effects (see "Send FX") where the effect is shared among all channels and the balance is individually adjustable for each channel. Typical insert effects are dynamics, distortion, chorus etc., plus mastering effects for the Master Section.

An alert appears asking you to confirm the deletion. (See "Deleting devices" for more details).

Send effects are routed in parallel with the signal chain, and the effect balance can be adjusted - as opposed to Insert effects, which are inserted in the signal chain and process the whole channel signal (see "Insert FX"). Typical Send effects include reverbs and delays.

Output Busses allow you to create sub-mixers. Sub-mixers can be very useful for pre-mixing a multi-mic'ed drum kit, or a horn section, for example. You can also use a sub-mixer configuration to route several external input signals (from separate microphones, for example) for recording onto a single audio track (see "Recording a sub-mix onto an audio track"). You can have as many mix busses as you like in a Reason song.

See "Recording audio from Mix Channel outputs" for more details.

Functions for changing the Remote Base Channel may already be mapped to buttons on your control surface - see the "Control Surface Details" pdf document. If not, you can set this up manually in the Additional Remote Overrides dialog on the Options menu - see "Additional Remote Overrides...".

If your control surface doesn't have buttons already assigned for controlling Remote Base Channel selection, you can manually assign controllers for this by using the Remote Override function described in "Remote Override mapping". Alternatively, select a channel strip and select "Set Remote Base Channel" from the Edit menu or context menu.

See "Remote - Playing and Controlling Devices" for more details about remote controlling Reason. See also the "Control Surface Details" pdf document for information about parameter assignments on various common control surfaces.

Use a "Spider Audio Merger & Splitter" device to split the sidechain signal from the Parallel outputs and/or Insert FX "To Device" output into several signals.

See "Output Busses" for information.

Another typical application for compression sidechaining is to use the internal signal of the channel, filter it, and then feed to the compressor via "internal" sidechaining. This type of internal sidechaining can be used for de-essing, for example. No additional patching is required for this; you only have to activate the "Filters to Dynamics Sidechain" button in the Filter or EQ sections. See "About the Filters To Dynamics Sidechain button".

Direct routing of individual channel outputs to individual outputs on the Reason Hardware Interface.

Now, you can begin recording on the Audio Track according to the standard recording procedures described in "General recording procedure". The signal will be processed by the Insert FX of the Mix Channel device before being recorded on the track.

---

<a id="delay-compensation-18"></a>
## 18. Delay Compensation


When on, the delay compensation affects all configurations described in "Delay Compensation rules" below.

In other words, Reason doesn't measure any latency of the effect devices. However, you can manually adjust the delay compensation if needed (if things sound wrong due to plugins reporting wrong latencies etc.). See "Manually adjusting the latency values" for more details.

What Reason then does to compensate for the inherent latencies in effect devices is to automatically add "invisible delays" to the signals of the other mixer channels. The goal for the delay compensation is to have all mixer channel signals arriving at exactly the same time to the Master Section of the main mixer.

---

<a id="song-file-handling-19"></a>
## 19. Song File Handling


See "Using the Browser" in the "Sounds and Patches" chapter.

If the song includes samples or REX files, and these have been moved or renamed since the song was saved, the program will inform you that it cannot find all files. You can then choose to either manually locate the missing files, to have the program search for them or to proceed without the missing sounds. For details, see "Handling Missing Sounds" in the "Sounds and Patches" chapter.

When you open a Reason song made by another user, it may have been created with Rack Extension devices that you don't have. All such missing devices in a song will be replaced by generic "Missing Device" placeholder devices. See "About missing Rack Extensions" for more information.

It's also possible to automatically include all samples used by the Reason devices and make the Song "self-contained". Refer to "About Self-Contained Songs" for details about how to include your own samples in your songs.

The text you add here will be displayed directly after the file name in the song window's title bar.

This allows you to add a picture to the song. The picture will be displayed when the song is opened.

The "Song Self-Contain Settings" dialog appears, listing all samples and REX files used in the song.

If you un-self-contain samples that were modified in the Edit Sample Window and feature Start and End Markers and/or loop crossfades, the Lossy Sample Export dialog appears. The available options are described further down in the "Exporting samples" section in the Sampling chapter. Note that the option you select in the Lossy Sample Export applies to all samples you have deselected in the Song Self-contain Settings dialog!

If you want Songs you have created to appear on the "New from Template" sub-menu, and be available for selection when you use the "New from Template" command (see "Creating a new Song from a template"), you need only move or copy the Song(s) to the Template Songs folder in the Music folder on your hard drive. The easiest way to get to this folder is by selecting File > New from Template > Show Template Folder. This brings up the Template folder in Windows Explorer or Finder on Mac.

This means that standard performance controllers (Pitch Bend, Mod Wheel etc.) are preserved properly and will be included in the note clip, just as when recording in Reason. If there are separate MIDI Controllers in the imported MIDI file, these will be imported to separate Automation Lanes on the Instrument Tracks. There is a chance that some controller data may be imported to alien clips, due to different interpretations of a controller by a device in the rack and the MIDI instrument used to create the MIDI file (see "About alien clips").

---

<a id="importing-and-exporting-audio-20"></a>
## 20. Importing and Exporting Audio


The exported audio file will also contain tempo data as described in "About Tempo data in exported audio files".

See "Bounce Clip(s) to New Sample(s)" in the "Audio Editing in the Sequencer" chapter for more details.

See "Bounce Clip(s) to New Recording(s)" in the "Audio Editing in the Sequencer" chapter for more details.

See "Bounce Clip to REX Loop" in the "Audio Editing in the Sequencer" chapter for more details.

---

<a id="sampling-21"></a>
## 21. Sampling


Here, all samples you use in your song are listed (see "The Song Samples location"). Here is also where you can open samples for editing (see "Editing samples").

Here, all samples that are assigned to devices in the song are listed. All devices that contain assigned samples are listed as "sub-folders". Each device "sub-folder" shows the samples currently assigned to it. See "Assigned Samples" for more details.

If you remove a sound you have sampled from a device, the sound is automatically moved from the Assigned Samples folder to the Unassigned Samples folder. From here you can load the sample into other devices if you like. See "Unassigned Samples" for more details.

All sounds you have sampled yourself, plus any duplicated samples from the Factory Soundbank and/or ReFills, automatically becomes self-contained and are always stored with the song. These samples are listed in the All Self-contained Samples folder. See "About self-contained samples" for more details.

Click the Edit button to open the selected sample for editing in the Edit Sample window (see "The Edit Sample window").

Select this to open the sample for editing in the Edit Sample window. If several samples are selected, this item is grayed out.

Select this to create a duplicate of the selected sample. The duplicated sample is placed in the All Self-contained Samples and Unassigned Samples folders. Several selected samples can be duplicated in one go. See "Duplicating samples".

Select this to export the selected sample to disk. A dialog appears where you can select file format. Note that it is not possible to export samples from the Factory Soundbank or from ReFills. Several selected samples can be exported in one go. See "Exporting samples".

Select this to permanently delete the selected sample(s) from the song. Samples from the Factory Soundbank and from ReFills will not be deleted from their original locations - only from the song document. Any samples you have recorded yourself will be permanently erased unless you have previously exported them to disk.

All sampling parameters and functions are controlled from one single window - the Edit Sample window, used when editing samples in any of the sampling devices.

Whenever you sample in Reason, the resulting audio files are stored in WAV format. The sample rate is determined by the settings on the Audio tab in Preferences. The resolution (bit depth) is fixed at 16 bits.

If you want to sample external audio, e.g. from a mic or an instrument connected to the audio hardware on your computer, make sure you have set up the desired audio input(s) on the Audio tab in Preferences. Available audio inputs are indicated with yellow or green LEDs on the Hardware Interface in the rack.

Click the Crop button to crop the sample so that only the content between the Start (S) and End (E) locators is preserved. The rest of the sample will be permanently deleted.

Click the Normalize button to amplify the entire sample so that the loudest peak touches 0 dB. The entire sample is normalized, regardless of any locator settings.

Click the Reverse button to reverse (play backward) the entire sample, regardless of any locator settings.

The Fade In and Fade Out buttons apply a fade in or fade out of the sample volume.

Click one of the Loop Mode buttons to select loop type: the default (leftmost) setting is "no loop", then "Loop Forward" and "Loop Forward + Backward".

Below the waveform pane is the horizontal Waveform Navigator, operated the same way as the Song Navigator in the sequencer.

Set the desired sample playback region by clicking and dragging on the waveform pane, then click Set Sample Start/End to place the Start/End locators at the beginning and end of the region.

Tick the Crossfade Loop box to introduce a crossfade in the loop, useful to even out clicks in the loop points.

Set the desired loop region by dragging on the waveform pane, then click Set Loop to place the Left/Right Loop locators.

Type in a desired name for your sample - this overwrites the original name in the Song Samples list once you click Save.

Click Save to save your sample; it appears in the Song Samples location in the Browser.

Unassigned samples can be assigned to any sampler device by simply loading them into it.

Self-contained samples can also be loaded into any sampler device from the Browser.

You can "un-self-contain" your own samples - export them to disk as separate files and remove them from the song document - via "Song Self-Contain Settings..." on the File menu.

---

<a id="the-regroove-mixer-22"></a>
## 22. The ReGroove Mixer


Click the button to open Reason's floating Tool Window and show the Groove tab, where you can view and edit additional "Groove Settings" for each channel.

Groove patches can be loaded and stepped between just like device patches in the Reason rack. ReGroove patches have a .grov extension.

If you have a track you want to rush (negative slide value), put an empty bar at the beginning of your sequence and set the Anchor Point to "2" - this ensures notes assigned to Bar 1/Beat 1 play ahead of the beat.

The Groove Settings section of the Tool Window contains four "impact" settings (timing, velocity, note length, randomness); the Groove Amount fader acts like a master fader scaling these four proportionally.

These buttons load/save groove patches (.grov), just like device patches.

The "Get Groove From Clip" button converts the notes in a selected clip into a groove patch, usable immediately in the active ReGroove Mixer channel or saved to disk. Same as selecting a clip and choosing "Get Groove From Clip" from the Edit/context menu.

Useful for comparing with the original, ungrooved beat. For several note lanes on one ReGroove channel, use the channel's "On" button instead.

There are creative ways to apply grooves to music - see "Groovy tips & tricks".

For characteristics of a good groove-making clip, see "Tips for selecting the best Groove-Making Clips".

Once your ReGroove patch is ready, route one or more note lanes to the assigned ReGroove channel and raise the Groove Amount fader on that channel.

Grooves restart whenever a new time signature appears.

---

<a id="remote---playing-and-controlling-devices-23"></a>
## 23. Remote - Playing and Controlling Devices


The External Control Bus inputs (set up on the Preferences Sync page and in the MIDI In device in the hardware interface) let you send MIDI directly to individual devices in the rack - mainly used when controlling Reason from an external sequencer.

You can also do manual Remote Overrides to assign Reason parameters to knobs/sliders/buttons on your control keyboard/surface.

If a MIDI Port of your connected control surface/keyboard is already used by Easy MIDI Inputs, detecting it will override this and remove the MIDI In Port from the Easy MIDI Inputs list.

MIDI inputs not selected on this page or the Sync page are available to other programs.

Locking a control surface to the Main Mixer gives permanent control over levels, pans, and channel strip parameters regardless of what else is selected. You could also have dedicated controls for transport, Undo/Redo, sequencer track MIDI focus selection, etc.

Master Keyboard Input routes control surface(s) to the selected track's device in the rack. You can bypass this by locking a control surface to a specific device, or by using Remote Override mapping for specific parameters (mapped regardless of Master Keyboard Input).

E.g. a Subtractor with Master Keyboard Input gives your control surface control over the most important Subtractor parameters; switching Master Keyboard Input to an NN-XT track switches control to NN-XT parameters, and so on. There are standard mapping variations for most devices - see "About mapping variations".

Without dedicated transport controls, you can map transport controls via Remote Override mapping.

Remote Override mappings are saved with the current song but won't carry over to a new song.

The "Control Surface Details" document has standard mapping info for common control surface models; you can also activate Remote Override Edit mode to see live parameter mappings for your control surface(s).

This isn't a conflict - it's simply a consequence of all control surfaces following Master Keyboard Input by default. Surface Locking or Remote Override give you full control.

Locked devices can also be locked to a specific mapping variation.

Example: lock a control surface to control the Main Mixer so you always have overall level control while tweaking other devices.

Control surfaces/keyboards using Easy MIDI Inputs cannot be locked to devices.

If the selected control surface supports keyboard shortcuts for mapping variations, an "Always use Mapping" pop-up appears.

The device shows a lock symbol in the upper left corner of the panel when locked, visible in Remote Override Edit mode.

A control surface can also be locked to the ReGroove Mixer to control its parameters remotely.

Another way to map parameters: with "Remote Override Edit Mode" off in the Options menu, right-click (PC) or [Ctrl]-click (Mac) the parameter you want to remote control, or right-click the device panel for the same option via context menu.

Similarly, with "Keyboard Control Edit Mode" deselected, right-click (Win) or [Ctrl]-click (Mac) a parameter to assign a keyboard remote command.

---

<a id="synchronization-and-advanced-midi-24"></a>
## 24. Synchronization and Advanced MIDI


Due to latency, Reason needs time to correct its playback speed when it first receives the Start command - this can appear as a small glitch in audio playback when the program starts. If problematic, insert a couple of empty measures at the beginning of the Song.

If your song has tempo automation, see "About Tempo Automation when using Ableton Link" for additional info.

This could be an external hardware sequencer or a sequencer application running on another computer.

See "Recording pattern automation", "Editing pattern automation" and "Drawing pattern automation" for recording and editing pattern changes.

---

<a id="optimizing-performance-25"></a>
## 25. Optimizing Performance


You generally want the lowest possible latency for the best response when recording/playing in real time. However, too low a latency risks playback problems (clicks, pops, dropouts) because smaller buffers put higher average strain on the CPU - the more CPU-intensive your song (more devices/audio tracks), the higher the minimum latency needed.

"Render audio using audio card buffer size setting" should be selected for best plugin performance. When selected, audio batches render internally according to the set Buffer size (e.g. 512 samples = 512-sample internal batches). Raising Buffer size lets Reason process larger batches more efficiently; many plugins (especially DSP-heavy mastering VSTs) run smoother with this enabled.

Deleting unused recordings won't affect processing power but reduces Song file size.

After recording/editing, use "Save and Optimize" on the File menu to remove empty disk areas and shrink the file.

If an instrument track uses lots of devices, bounce it to an Audio Track, then delete the instrument track to reduce processing power (see "Bouncing Mixer Channels").

Polyphonic Devices affecting CPU load: Subtractor, Thor, Malström, NN19, NNXT, Grain, Europa, Dr. Octo Rex and Redrum.

---

<a id="hardware-interface-26"></a>
## 26. Hardware Interface


The Hardware Interface device is where you connect Reason to the "outside world" - MIDI is received here, and audio signals route from physical inputs to physical outputs of your audio hardware. It's always present at the top of the rack and cannot be deleted. This chapter serves as a panel reference; see "Audio Basics" for how to set up your audio hardware.

Yellow LED: available but unused channel (no cable connected to the channel jack on the rear panel).

See "Advanced MIDI Device", "More Audio", and "The Big Meter" for details on those sections, and "Advanced MIDI - The External Control Bus inputs" in the Synchronization and Advanced MIDI chapter.

If the audio level for a selected channel has been too high, the Clip indicators on the Big Meter stay lit until you click Reset or select new audio channels for the Big Meter.

---

<a id="kong-drum-designer-27"></a>
## 27. Kong Drum Designer


The pad section features 16 pads, each assignable to a separate Drum sound. You can assign several pads to one Drum sound, or link pads so one pad triggers several others. The Pad Settings area to the right controls pad assignments and behavior.

The Drum Control Panel at bottom left shows the name and "macro parameter" settings for the selected pad, and lets you load/save Drum Patches and initiate sampling.

Clicking the Programmer button below the Drum Control Panel brings up the Drum and FX Section, where you edit drum sounds and combine them with sound processors and FX.

As with the Combinator, Kong's front panel graphics can be customized with a user-designed skin using the "Combi and Kong Backdrop Templates" zip from the Reason Studios download section (use separate backdrops for folded vs. unfolded states).

REX files are music loops created in ReCycle or by bouncing audio clips in Reason. The NN-Nano Sampler lets you load separate REX slices as individual samples; a loaded REX file automatically opens in a Nurse Rex Loop Player module.

Drum Control Panel parameters are "global" per Drum channel; each drum sound can consist of several sound and FX modules with their own parameters (see "The Drum modules", "The Support Generator modules", "The FX modules"). You don't need to save the Drum patch separately - settings are included when you save a Kong Kit Patch or your song.

Kong has 16 pads and 16 Drum channels. By default pad N maps to Drum channel N; you can reassign pads, e.g. to apply different Hit Types per pad so the same Drum channel responds differently depending on which pad triggered it.

Signal flow: a Drum module's output goes via FX1 and FX2 Slots to Bus FX, Master FX, or a pair of individual outputs on the back panel. An internal Bus FX Send can carry the signal via FX1/FX2 to Bus FX (e.g., a shared reverb send for all Drum channels); an external effect device can also be inserted between Bus FX and Master FX.

Loading/saving Kong Drum patches (.drum) works like any other Reason device patch.

Selectable Drum Module types: NN-Nano Sampler, Nurse Rex Loop Player, Physical Bass Drum, Physical Snare Drum, Physical Tom Tom, Synth Bass Drum, Synth Snare Drum, Synth Tom Tom, Synth Hi-Hat.

Selectable FX1/FX2 Slot module types: Noise generator, Tone generator, Room Reverb, Transient Shaper, Compressor, Filter, Parametric EQ, Ring Modulator, Rattler, Tape Echo, Overdrive/Resonator.

The NN-Nano handles samples/sample sets for each of four Hit Types, each of which can be layered/altered/controlled individually via velocity, and can also load REX slices as individual samples.

The sampling procedure is the same across Kong, NN-19, NN-XT and Redrum - see the "Sampling" chapter.

The Nurse Rex loads standard REX files and plays back loops/slices in several ways depending on Hit Type: Loop Trig triggers one full loop cycle per pad hit (stoppable via a "Stop" mode pad); Chunk Trig splits the loop into equal chunks across as many pads as assigned (also stoppable); Slice Trig lets you check boxes for which slices to alternate between.

Kong's back panel has numerous CV/Gate-related connectors (see "Routing Audio and CV"), two stereo Aux Send Outputs (levels set via the Aux 1/Aux 2 Send knobs on the Drum Control Panel) for external effects, and 14 individual audio output jacks (7 stereo pairs) that are never auto-routed but can be manually assigned per Drum channel via the Drum Output selector.

---

<a id="redrum-drum-computer-28"></a>
## 28. Redrum Drum Computer


The sampling procedure is generic across NN-19, NN-XT, Redrum and Kong - see the "Sampling" chapter.

REX files (music loops from ReCycle or bounced audio clips) can have individual slices loaded as samples in Redrum.

Redrum patterns are not part of the patch. To save a Redrum patch complete with patterns, place the Redrum in a Combinator and save the Combi patch.

If the Tempo track is used, Redrum follows it. Pattern changes automated in the main sequencer can happen at any position (see "Recording pattern automation").

Shuffle amount is set globally via the Global Shuffle control in the ReGroove Mixer.

With the Enable Pattern Section switch off, Redrum functions as a pure "sound module" - its internal pattern sequencer is disengaged, useful when controlling Redrum exclusively from the main sequencer or via MIDI.

Notes played into Redrum as a sound module take the pitch of the corresponding drum sound, with velocity depending on the device's "Dynamic" parameter.

Drum channel Mutes can be recorded live in the main sequencer like any other controller - useful for bringing drum sounds in/out of the mix live.

If using Redrum purely as a sound module (no pattern playback), deactivate "Enable Pattern Section" - otherwise its pattern sequencer starts automatically when the main sequencer runs.

---

<a id="dr-octo-rex-loop-player-29"></a>
## 29. Dr. Octo Rex Loop Player


Dr. Octo Rex plays back and manipulates files created in ReCycle (a separate Reason Studios product for slicing sampled loops into individual beat-samples, allowing tempo changes without pitch shift) or bounced from Single Take audio clips in Reason.

REX2 is the ReCycle file format for Mac/PC generated internally in Reason or by ReCycle 2.0+; unlike the original REX format, REX2 supports stereo files.

Pattern Automation recording is detailed in "Pattern automation recording details".

Playback, stop and Loop Slot selection can be controlled in real time from a MIDI keyboard: keys E0-B0 select Loop Slot 1-8 and start playback; loops play continuously one at a time until you press D#0 to stop, or click Run/Stop. Timing between key press and slot switching is set by the Trig Next Loop function.

The Note To Slot parameter is copied into generated clips as a Performance Controller so Dr. Octo Rex always knows which Note Slot the notes came from, and plays back the correct Loop Slot's slices automatically.

Use the Alter Notes function to scramble loop notes without destroying original loop timing.

A special REX edit lane displays slice notes by slice number instead of pitch.

Per-slice parameters are edited by selecting a slice and using the knobs below the waveform display; for editing one parameter across multiple slices at once, use Slice Edit Mode instead.

Pitch bend range and Mod destination are set on the synth parameter panel.

The Trig Next Loop parameter sets the timing for switching between Loop Slots.

Eight Loop Slot buttons sit in the center of the front panel - one REX loop per slot, loaded from the Loop Editor panel. Selecting a slot only chooses which loop plays via Run/Play; which slot the keyboard/sequencer notes control is set separately via Note To Slot.

The overall pitch-shift-by-envelope amount (positive or negative) is set for all REX files' pitch response to the Filter Envelope.

Filter Frequency is usually also controlled by the Filter Envelope, so changing it directly with the Freq slider may not behave as expected (see "Envelopes - General" in the Subtractor chapter for basic envelope concepts).

The rear panel's left section houses CV/Gate inputs and outputs (see "Routing Audio and CV").

---

<a id="europa-shapeshifting-synthesizer-30"></a>
## 30. Europa Shapeshifting Synthesizer


Loading/saving patches works like any other internal Reason device.

For monophonic playback, use "Retrig" or "Legato" mode rather than setting Voices to 1.

Select polyphonic play mode for up to 16 voices (set via the Voices control at center-right).

Set the Pitch Bend range for the "Pitch" wheel with the up/down buttons or by dragging on the display. The Pitch bend wheel bends note pitches and responds to incoming MIDI pitch bend from a master keyboard; "P.Range" sets the range.

The Mod wheel can control almost any Europa parameter - use it as a Source in any Modulation Source box, or route it via the Modulation Bus section to a chosen destination.

Use "Recording display movements in the sequencer" for tips on automating display movements.

The "Stretch" harmonics algorithm combined with certain oscillator settings can create realistic metallic sounds.

A special mode lets you manually draw waveforms in the Envelope 3/4 windows and crossfade between them with the Shape knob (see "Using the Envelope 3 and Envelope 4 curves as Sound Engine waveforms").

The FM Feedback waveform: a pure sinewave at Shape=0% fed back internally 1:1, filtered before feedback; modulating Shape from an LFO gives a similar result to FM FB Noise without Shape modulation.

User Wave options play back wavetables (grains) of an externally loaded sample (see "The User Wave and Mixer section"); "User Wave Smooth" crossfades within each grain for a smoother character. Shape sets playback position in the sample - modulate it (e.g. from a negative Envelope ramp) for continuous movement through the sample.

An internally fed-back sinewave at 1:1 modulates the waveform, same signal type as FM Feedback.

To make a formant static regardless of played note, modulate the Amount parameter with the "-KEY" (inverted) source at a fairly high value - especially useful with an acoustic instrument sample as User Wave.

A special mode lets you draw your own filter curve in the Envelope 4 window, controlling cutoff/center frequency with Freq and resonance with Reso (see "Using the Envelope 4 curve as a Spectral Filter curve").

The User Wave spectral filter mode uses FFT analysis of the loaded external sample; Freq transposes the formant up/down, Reso changes the filter's position within the sample.

Classic vocoder effect recipe: load a vocal/speech sample as User Wave, set Freq to 50%, Reso to 0%, KBD to 0%, then have an Envelope modulate Reso via the Modulation Bus using a positive ramp (inverted sawtooth) envelope at 100% amount.

The Harmonics section offers extensive modulation of the signal's partials, displayed in the Spectral Filter display for most algorithms.

The Harmonic Lag A-R algorithm is designed for use with the User Wave Spectral Filter algorithm to create vocoder effects - the Spectral Filter must be on for this to work.

With Phase Sync active in the Oscillator, all Unison signals get the same relative start phases each time you play the same note (original signal always at phase 0 degrees).

The User Wave and Mixer section is where you sample or load an external sample for use in the Oscillators and/or Spectral Filter; the Mixer mixes/pans the three Sound Engines before the Filter, Amp and Multi FX sections (see the "Sampling" chapter for sampling procedure and "Editing samples" for sample editing).

If the Filter is deactivated, the signal bypasses it and goes straight to the Amp section.

Use one of the Envelopes as a modulation source to create a Filter envelope (see "The Modulation Bus section").

The LFO section has three general-purpose LFOs assignable to parameters via the Modulation Bus section.

The Effects section has six effect modules, freely reorderable by drag and drop; most effect parameters are also available as Modulation Bus destinations.

The assignable CV inputs/outputs modulate from/to assigned Source and Destination parameters in the Modulation Bus section.

The main audio outputs auto-route to the first available Mix Channel when a new Europa device is created (a new Mix Channel is created automatically if none is available).

---

<a id="grain-sample-manipulator-31"></a>
## 31. Grain Sample Manipulator


Loading and saving patches works like any other internal Reason device.

Select polyphonic play for up to 12 voices, set via the Voices control at top right.

See "Global Position" for how to play through a sample "non-legato" or polyphonically in "sample playback legato" fashion, where new notes continue at the current playback position instead of restarting.

Set the Pitch Bend range for the "Pitch" wheel via up/down buttons or by dragging the display. The wheel bends note pitch and responds to incoming MIDI pitch bend; "Range" sets the amount.

With some playback algorithms (e.g. Spectral Grains), audible pitch depends on formant rather than pitch settings - for pitch bend to have an effect there, add a Pitch Wheel -> Formant routing in the Modulation Bus.

The Mod wheel can control almost any Grain parameter via the Modulation Bus section.

For monophonic playback, use "Retrig"/"Legato" modes rather than setting Voices to 1.

See the "Sampling" chapter for sampling setup and "Editing samples" for sample editing.

Motion modes: Freeze plays the sample at/around the Start marker with no End marker (silent if Tape algorithm is selected). End Freeze plays once from Start to End marker, then loops around the End marker (also silent past End with Tape algorithm). Envelope 1 mode plays back between Start/End according to the Envelope 1 curve, where the curve's minimum Y = Start position and maximum Y = End position - useful for looping the sample in sync with the sequencer using a straight upward ramp with Beat Sync active.

With the Tape playback algorithm, the Speed knob also affects pitch and can go to 0% ("stop") - useful for Tape Stop effects.

Root Key sets the sample's initial pitch; if Snap and Filter are both 0%, Root Key and Formant control pitch (Pitch controls and Pitch wheel then have no effect). Set Formant Kbd to 100% for the formant to track the keyboard musically.

The Long Grains algorithm plays fairly long grains of the original sample, so pitch follows Root Key plus the Pitch controls.

With Envelope 1 as Motion type, Speed and Pitch controls have no effect - the sample always plays at the same pitch regardless of note played.

With Spectral Grains, Pitch controls have no effect unless Snap or Filter is set to 100%.

The Effects section has six freely reorderable effect modules (drag and drop); most parameters are also Modulation Bus destinations.

Dragging to the Waveform Display always assigns the playback Position parameter; to assign Start or End Position instead, select the parameter from the list.

---

<a id="mimic-creative-sampler-32"></a>
## 32. Mimic Creative Sampler


A Mimic patch contains parameter settings for all used Slots - up to eight complete parameter setups. Loading/saving works like any other internal Reason device.

In Slice Mode, select one of the eight Slots, then slice a longer sample manually and/or automatically. Slices trigger chromatically from the keyboard (leftmost slice from note C1) without affecting the sample's original pitch.

Click a Slot button to select it.

"Global Position" lets new notes continue at the current playback position instead of restarting.

Set Pitch Bend range for the wheel via up/down buttons or dragging the display; "Pitch Range" sets the amount. With the Tape Stretch algorithm, pitch bending also affects playback speed.

Load/sample audio for the currently selected Slot; the Waveform display varies by Slot Mode.

Start and End markers cannot be set in reversed order - to play backwards, use the Reverse button instead.

When playing reversed, the looped region originates from the Start Marker and displays in transparent blue.

Sound varies by Stretch type; with Tape Stretch, the Speed knob also affects pitch and can go to 0% (stop) - useful for Tape Stop effects or static playback in other Stretch types.

With Tape stretch, a Loop X-Fade knob controls crossfade amount when Loop is active.

The Melody stretch type works well with Loop since it reduces clicks/pops at the loop point.

Slices are available even outside Slice Mode - useful for snapping the Start position when dragging, modulating, or automating it.

With Tape Stretch, pitch settings also affect playback speed.

LFO Scale lets you gradually introduce LFO modulation amount via the Mod Wheel.

Send knobs tap each Slot's output to the corresponding FX Send Out jacks on the rear panel, routable to external effects and then to a separate mixer/audio channel (Mimic has no FX Return jacks).

To avoid a lot of notes decaying simultaneously, shorten the Amp Envelope Release time and/or deactivate Play Thru in Slice Mode.

---

<a id="thor-polysonic-synthesizer-33"></a>
## 33. Thor Polysonic Synthesizer


This chapter assumes familiarity with common synth terminology - oscillators, waveforms, filters, envelopes. New users may want to read the "Subtractor Synthesizer" chapter first, which introduces these building blocks more simply.

Sections can be connected using the Modulation Bus section, not just the pre-defined routings - the pre-defined routings are just a quick, convenient way to connect the basic synth building blocks.

Oscillator types available: Analog, Wavetable, Phase Modulation, FM Pair, Multi, and Noise (see "The Oscillator section").

A pop-up menu offers the four available Filter types (see "Filter slots").

Thor has three open Filter slots: two in the Voice section (acting per-voice) and one in the Global section (global across all voices, see "Global Filter slot").

There are three Envelope generators in the Voice section - Amp, Filter, and Mod envelopes - each voice gets its own separate envelope. There's also an additional Global Envelope (see "Global Envelope").

---

<a id="subtractor-synthesizer-34"></a>
## 34. Subtractor Synthesizer


A combination of a multimode filter and a second, linkable, lowpass filter allows complex filtering effects (see "The Filter Section").

A unique Subtractor oscillator feature: create an extra waveform within one oscillator, offset its phase, and modulate that phase offset. Subtracting or multiplying a waveform with a phase-offset copy of itself creates complex new waveforms from existing ones.

When phase offset modulation is active, the oscillator creates a second copy of the waveform offset by the Phase knob amount, then subtracts or multiplies the two depending on the selected mode.

A notch (band reject) filter is the opposite of a bandpass filter - it cuts a narrow midrange band while letting frequencies above/below through; alone it doesn't dramatically alter timbre, but combined with a lowpass filter (Filter 2) it can produce soft yet "clear" timbres, especially noticeable at low Resonance settings.

Filter Frequency is usually also controlled by the Filter Envelope, so changing it directly with the Freq slider may not behave as expected.

A combination of Decay and Sustain generates envelopes that rise to maximum then gradually decrease to rest at an in-between level; Sustain is a level, the other envelope parameters are times. Release works like Decay but determines the fall-to-zero time after key release.

LFO 2 is polyphonic - each note gets an independent LFO cycle (unlike LFO 1, which always uses the same cycle for all notes) - useful for subtle cross-modulation "beating" effects and for modulation rates that vary across the keyboard (see Keyboard Tracking).

---

<a id="malstrm-synthesizer-35"></a>
## 35. Malström Synthesizer


See "The Oscillator section" for oscillator details. There's one amplitude envelope per oscillator and a common envelope for both filters (see "The amplitude envelopes" and "The Filter Envelope").

Malström's Graintables aren't all the same length, and the Index slider's 0-127 range does not reflect actual graintable length - regardless of whether a graintable has 3 or 333 grains, the Index slider always spans the whole table.

Pitch-shifting a segment (via re-sampling) changes harmonic content and timbre rather than perceived pitch, since the heard pitch is independent of the graintable's actual pitch - more or less of the segment waveform gets played back.

A looped graintable (Motion knob not fully left) follows one of two motion patterns; Motion knob speed is adjustable but the motion pattern itself is not.

Each oscillator has a standard ADSR envelope and Level control for volume. Unlike many synths, Malström's amplitude envelopes sit before the filter and routing sections in the signal path.

Mod:A can offset osc:A/B pitch, index start position, or harmonic content (playback of the graintable); Mod:B can affect motion speed of osc:A/B.

Five modes are available for shaping the sound, each with its own character.

Mod wheel can control the active graintable's index for osc:A/B (positive = forward, negative = backward) and/or the Shift parameter.

The two main stereo outputs connect to the two filters separately; true stereo output depends on routing and the Spread parameter (see "Routing").

External audio or Malström's own internal signal can be routed directly into the filters and shaper (see "Routing external audio to the filters").

---

<a id="monotone-bass-synthesizer-36"></a>
## 36. Monotone Bass Synthesizer


Loading/saving patches works like any other internal Reason device.

Set Pitch Bend range for the wheel via up/down buttons or by dragging the display; the wheel bends pitch and responds to incoming MIDI pitch bend, with "Range" setting the amount.

For LFO modulation to work, LFO modulation must already be set in the Oscillator and/or Filter sections.

Resonance controls the peak level at the currently set cutoff frequency.

The LFO section has one LFO that can control Oscillator pitch and/or Filter frequency - a classic vibrato/cyclic modulation tool.

The Envelope section is a standard ADSR usable for Oscillator FM and/or Filter Frequency modulation.

Main audio outputs auto-route to the first available Mix Channel when a new Monotone device is created (a new Mix Channel is created automatically if none is available).

---

<a id="id8-instrument-device-37"></a>
## 37. ID8 Instrument Device


The Piano category features a grand piano, an upright piano, a dance-oriented piano sound, and vibes.

See "Velocity mapping" for information about the velocity mapping of some of the sounds.

---

<a id="rytmik-drum-machine-38"></a>
## 38. Rytmik Drum Machine


## Introduction
The Rytmik Drum Machine is an eight-channel drum sample player designed for seamless integration of Reason Compact projects. It features a Distortion effect and a Low Cut + Hi Cut filter per drum channel, two shared send effects (Reverb and Delay), and a master section with a Master Compressor, Master Pitch, and a Master Filter.

## Panel overview
1. Patch selector (browse, load, save patches)
2. Sample playback and editing section (for the currently selected Drum Channel)
3. Distortion and Low Cut + Hi Cut Filter (for the currently selected Drum Channel)
4. Drum Channel sections (playback and selection)
5. Send Effects and Compressor section (global for all eight channels)

## Signal flow
Eight Sample Playback engines (one per Drum Channel), each with a Sample section (built-in samples, Sample Start/End, Pan, Pitch, Fade In/Out) -> a per-channel Distortion insert -> a per-channel Low Cut/Hi Cut Filter -> per-channel pan/volume -> optional sends to the two global Reverb/Delay effects (level set per channel) -> all eight channels plus sends mixed to stereo through a Master Compressor and Master Filter. Individual Drum Channel signals can instead be routed to separate outputs (post-Filter, bypassing Send Effects and Master FX) for external processing.

## Global controls
Loading/saving patches works like any other internal Reason device.

## Drum Channel sections
Click a Drum Channel button to audition its sample and select that channel. Via MIDI/On-screen Piano Keys, samples play back from key C0 to G0.
M(ute)/S(olo) buttons mute or solo a channel. Volume slider sets channel level (drag or click). Delay and Reverb knobs set send levels to the respective Send Effect.

## Sample Playback section (per selected Drum Channel)
Select samples via the triangular arrow buttons or the sample-name pop-up (eight sub-groups of sample types). All Rytmik samples are embedded in the device itself, so saving a patch always includes them (unlike other Reason sampler devices).
Sample Start/End: drag the handles sideways.
Pan: drag up/down, range 100L to 100R.
Pitch: drag up/down, range +/-1200 cents.
Fade In/Fade Out: drag up/down, shown graphically in the sample display.

## Insert Effects section
Distortion: transistor-type distortion; drag up/down to set input gain, range 0-100% (0 = dry/off); higher values overdrive the pre-amp.
Low Cut (highpass) / Hi Cut (lowpass) filter: removes rumble (Lo Cut) and/or hiss (Hi Cut). Each ranges 20 Hz to 25 kHz; drag the box or the corresponding side of the filter curve in the display. The two cutoffs can cross, which can drop the sample level to zero at extreme settings.

## The Master FX section
Delay: Stereo or Ping Pong mode (pop-up); tempo-synced Time divisions of 1/1, 1/2D, 1/1T, 1/2, 1/4D, 1/2T, 1/4, 1/8D, 1/4T, 1/8, 1/16D, 1/8T, 1/16 (hard-wired to sequencer tempo); Feedback sets repeat count, range 0-100% (0 = single repeat).
Reverb: stereo reverb with six algorithms - Room, Large Room, Culvert, Plate, Gated, Hall. Decay sets effect length (shown graphically). Low Cut/Hi Cut (20 Hz-25 kHz each) shape the reverb tone; crossed values can drop reverb level to zero.
Compressor: stereo, acts on the total mix of all Drum Channels, always active (set controls for no compression if desired). Threshold -60 dB to 0 dB (0 dB = no compression); lower threshold = more compression. Ratio 1:1 to 20:1 (1.00 = no compression); higher ratio = more even/less dynamic. Attack 0-200 ms (higher = slower response, preserves transients). Release 0-200 ms (short = pumping effect, long = smoother).
Master Pitch: +/-1200 cents, adjusts all channels equally.
Master Reverb: +/-100%, bipolar return-level control for the Reverb send (can attenuate or boost, but level never exceeds 0 dB).
Master Filter: +/-100% combined highpass/lowpass on the total mix; 0% = unfiltered.
Master Volume: -inf to 6.00 dB, sets total mix output level.

## Connections
CV connections are NOT stored in Rytmik patches - to save them, place Rytmik in a Combinator and save the Combi patch.
Drum Gate In responds to Note On/Off plus Velocity from another CV/Gate device; Drum Gate Out sends Note On/Off plus Velocity to control other CV/Gate devices.
Separate Outputs route individual Drum Channels externally for further processing; channels routed this way are automatically disconnected from Master FX (though they can still reach the Send Effects on the Main Outputs).
Main Output L & R auto-route to the first available Mix Channel when a new Rytmik device is created (a new one is created automatically if none is available).

---

<a id="radical-piano-39"></a>
## 39. Radical Piano


Loading/saving patches works like any other internal Reason device.

With the Low knob at zero (marked "S"), playing very softly produces no sound at all - useful for holding a chord and playing other keys to trigger the sympathetic resonance effect (see "Resonance").

The Ambience section has four reverb types plus a Level control.

The maximum pitch-shift range for the piano sound is +/-1 octave, assuming no Pitch Bend performance controller is used and Character is set to Natural. The Character setting and any Pitch CV modulation can reduce the effective Pitch Bend range.

A standard switch-type sustain pedal connected to your MIDI master keyboard's Sustain Pedal input controls Sustain On/Off; you can later edit Sustain values in note clips in the sequencer to set continuous values from 0-127 (see "Sustain").

---

<a id="klang-tuned-percussion-40"></a>
## 40. Klang Tuned Percussion


Set Pitch Bend range for the wheel via up/down buttons or by dragging the display; range control sits to the right of the Mod wheel.

If S.Start (Sample Start) in the Instruments section is at 0 ms, it cannot move back further; at 150 ms, it cannot move forward further.

If Cutoff in the Filter section is at 20 Hz, it cannot be lowered further; at 25 kHz, it cannot be raised further.

The standard ADSR envelope controls filter cutoff frequency modulation over time (characteristics detailed under Amp Envelope).

The Delay effect is routed as a send effect, with the Amount knob acting as an effect-return control - so a short note played with Amount at zero can still produce a delay effect if Amount is raised afterward, depending on Feedback.

The Reverb effect works the same way as a send effect with Amount as return control - a short note at Amount zero can still produce reverb if Amount is raised afterward, depending on the Time setting.

---

<a id="pangea-world-instruments-41"></a>
## 41. Pangea World Instruments


Set Pitch Bend range for the wheel via up/down buttons or by dragging the display; range control sits to the right of the Mod wheel. The wheel bends note pitch and responds to incoming MIDI pitch bend.

If S.Start (Sample Start) in the Instruments section is at 0 ms, it cannot move back further; at 150 ms, it cannot move forward further.

If Cutoff in the Filter section is at 20 Hz, it cannot be lowered further; at 25 kHz, it cannot be raised further.

The standard ADSR envelope controls filter cutoff frequency modulation over time (see Amp Envelope for characteristics).

The Delay effect is routed as a send effect, with Amount as an effect-return control - a short note at Amount zero can still trigger delay if Amount is raised afterward, depending on Feedback.

The Reverb effect works the same way - a short note at Amount zero can still trigger reverb if Amount is raised afterward, depending on the Time setting.

---

<a id="humana-vocal-ensemble-42"></a>
## 42. Humana Vocal Ensemble


Set Pitch Bend range for the wheel via up/down buttons or by dragging the display; range control sits to the right of the Mod wheel. The wheel bends note pitch and responds to incoming MIDI pitch bend.

If S.Start (Sample Start) in the Instruments section is at 0 ms, it cannot move back further; at 150 ms, it cannot move forward further.

If Cutoff in the Filter section is at 20 Hz, it cannot be lowered further; at 25 kHz, it cannot be raised further.

The standard ADSR envelope controls filter cutoff frequency modulation over time (see Amp Envelope for characteristics).

The Delay effect is routed as a send effect, with Amount as an effect-return control - a short note at Amount zero can still trigger delay if Amount is raised afterward, depending on Feedback.

The Reverb effect works the same way - a short note at Amount zero can still trigger reverb if Amount is raised afterward, depending on the Time setting.

(Humana shares its Instruments/Filter/Envelope/Delay/Reverb architecture with Pangea and Klang - all three are sample-playback "world/tuned percussion/vocal" instruments built on the same panel design.)

---

<a id="nn-xt-sampler-43"></a>
## 43. NN-XT Sampler


NN-XT's basic functions resemble its companion NN-19: load samples and build multi-sample patches by mapping samples across the keyboard, then shape the sound with a comprehensive set of synth-type parameters. Key differences: NN-XT can load presets and samples from SoundFont banks (see "Loading SoundFonts"), and can route different samples to different mixer channels for individual effect processing (see "Out").

Sampling procedure is generic across NN-19, NN-XT, Redrum and Kong (see the "Sampling" chapter).

SoundFont presets load via the patch browser; single SoundFont samples load via the sample browser.

REX files (loops from ReCycle or bounced audio clips) are primarily used in Dr. Octo Rex but also work in NN-XT; extensions: .rx2, .rcy, .rex.

Main panel controls globally modify parameters for all samples in a patch by the same amount. Aftertouch, expression pedal, or breath controller input (if your MIDI keyboard sends it) can modulate NN-XT parameters, assigned in the remote editor panel (see "The Modulation controls"); movements record as automation like any other performance controller.

Two knobs control filter parameters (filter must be on to have effect); one changes filter resonance (character/quality).

Three knobs control the Amplitude Envelope: one changes Decay (time to return to sustain level after full value is reached while the key is still held).

A separate knob controls Decay of the Modulation Envelope.

Clicking the (unlabeled) zone-group area selects all zones belonging to a group (see "Working with Grouping").

The keyboard-range guide is also used for setting root keys and auditioning loaded samples (see "About the Root Key" and "Auditioning samples").

Per-group parameters mostly relate to performance/playing style.

MIDI-based sample selection is velocity sensitive - zones with velocity ranges only trigger if the key is played within that range (see "Setting velocity range for a Zone").

Synth parameters occupy most of the remote editor panel; changes always apply to all selected zones. Selecting multiple zones and adjusting a parameter sets all of them; when selected zones have conflicting values, NN-XT shows a small "M" (multiple) symbol next to the parameter.

Copying settings between zones only copies synth parameters, not sample parameters (root key, velocity range, etc.).

After loading samples, the next step is usually adjusting key range, root note, and tuning so they play sensibly across the keyboard (see "Working with Key Ranges").

A slice is a snippet of sound within a REX file; browsing to a REX file and opening it like a folder reveals its slices as individual files, importable and treated like samples throughout the manual.

Clicking a sample plays it at root pitch, unprocessed (no synth parameters applied). Clicking a key on the keyboard guide plays the sample at that key's pitch with all processing applied, simulating velocity 100 - this can trigger multiple samples depending on overlapping key/velocity ranges.

Soloing a sample helps check how far from its root key it can be played before sounding "unnatural," useful when setting up key ranges.

Zone sorting only works within a group - zones from different groups can't be sorted relative to each other.

NN-XT has eight separate stereo output pairs; each zone can be assigned to one, so an 8-zone key map can have eight independent stereo outputs routed to separate mixer channels.

Unlike samplers where polyphony sets total simultaneous voices, NN-XT's polyphony setting determines the number of keys that can sound, regardless of how many voices each key triggers. (Activating a related mono button is not equivalent to setting polyphony to 1 - it can't be used for Legato or mono Retrig.)

Modulation/external control wheel knobs set how much they modulate a given parameter, e.g., Decay of the Modulation Envelope. The LFO 1 "scaling" knob determines how much the Modulation Wheel/External Controller affects the amounts already set by the three LFO 1 destination knobs (Pitch, Filter, Level) - e.g., to use the Mod Wheel to increase vibrato depth versus to decrease it, set the scaling knob's polarity accordingly.

Velocity can control Modulation Envelope Decay, Amplitude Envelope Attack, and Sample Start offset (so harder/softer playing shifts where the sample starts).

Amplitude Envelope Release works like Decay but determines the time to fall to zero after key release.

The Pitch section's envelope-to-pitch knob raises pitch when turned right, lowers when turned left, and has no effect at center. The equivalent Filter cutoff knob works the same way for cutoff frequency.

Most Amplitude Envelope parameters mirror the Modulation Envelope's (see "The Modulation Envelope").

NN-XT has two LFOs (LFO 1 and LFO 2); unlike normal oscillators, low-frequency oscillators generate a waveform/frequency for modulation, not audible sound. In one Rate mode, an LFO runs at the rate set for its group in the group section rather than its own Rate knob, so all zones in that group share the exact same modulation rate.

NN-XT has 16 audio output jacks (8 stereo pairs) on the back panel; the first pair auto-routes to the first available mixer channel when a new NN-XT device is created.

---

<a id="nn-19-sampler-44"></a>
## 44. NN-19 Sampler


The NN-19 is a sampler capable of recording and reproducing - but not editing - sound files.

Samplers are often used for more than playing "real instrument" samples: different sounds per key zone, complete verse/chorus vocals plus variations across "one note" key zones, or chord samples that play rhythmic figures at tempo to build song structures. In these uses, keys trigger samples rather than corresponding to pitch.

REX files (loops from ReCycle or bounced audio clips) can be loaded into NN-19 as complete patches or as individual sliced samples.

A new NN-19 device loads with a default patch; select "Reset Device" from the context/Edit menu to start from scratch. NN-19 needs a loaded patch, sample, or self-sampled sound (via "Sampling") to produce sound.

REX files are primarily used in Dr. Octo Rex but work in NN-19 too; extensions: .rx2, .rcy, .rex.

Sampling procedure is generic across NN-19, NN-XT, Redrum and Kong (see the "Sampling" chapter).

SoundFont samples are stored hierarchically (User Samples, Instruments, Presets, etc.); NN-19 can browse/load single SoundFont samples but not entire SoundFonts.

Loading a new sample into a zone that already had one replaces it in that zone and in sample memory - unless the old sample is also used by another zone, in which case it's kept. To remove a sample from a zone without removing it from memory, select "No Sample" with the Sample knob, or replace it with another.

A per-map tuning parameter can correct samples that are slightly out of tune with each other, by +/- half a semitone each; if all samples share the same tuning offset relative to the song, it's simpler to use the Sample Pitch controls in the Osc section directly instead.

Looping requires loop points set up in the audio file itself - NN-19 can't set loop points directly; that's done in the Edit Sample window or an external sample editor.

In a sample patch, the samples themselves are the "oscillators" - the main sound source, configured in the Osc section.

A pitch-by-envelope parameter sets how much the Filter Envelope affects overall sample pitch, with positive/negative values raising or lowering it.

Legato works best with monophonic sounds - set Polyphony to 1 to use it.

---

<a id="midi-out-device-45"></a>
## 45. MIDI Out Device


To play and/or record MIDI from your MIDI instrument into Reason, connect the instrument's MIDI Out to your computer's MIDI In as well (see "Recording MIDI Controller automation from the controlled MIDI instrument").

MIDI latency mainly occurs in the MIDI interface and connected MIDI instruments and is not something Reason can automatically compensate for (see "Moving clips" for related info).

---

<a id="quartet-chorus-ensemble-46"></a>
## 46. Quartet Chorus Ensemble


Loading/saving patches works like any other internal Reason device.

Mod Depth sets how much the LFO modulates delay time; at 0, delay time is static (unless Noise Mod is in use).

If both Mod Depth and Noise Mod are 0, the Width control has no effect.

Noise Mod amplitude-modulates the signal with lowpass-filtered noise, creating a "sparkling" effect; if both Noise Mod and Mod Depth are 0, Width has no effect.

An FFT-based noise-depth parameter controls a combination of noise amplitude and bandwidth applied to the signal's partials, with the result also depending on the Frequency Range parameter.

Random Phase randomly alters grain phase for a "bubbly" phase-cancellation effect, especially noticeable when Jitter is set low.

---

<a id="sweeper-modulation-effect-47"></a>
## 47. Sweeper Modulation Effect


Loading/saving patches works like any other internal Reason device.

One knob controls LFO modulation depth to the Frequency control of the Phaser, Flanger, and Filter sections. Another controls Modulator (Envelope Modulator / Audio Follower Modulator) depth to the same Frequency controls.

A separate knob controls LFO modulation depth to a built-in amplifier - bipolar, so negative values invert the modulation. Another controls Modulator depth to that same amplifier.

The LFO provides cyclic modulation of Phaser/Flanger/Filter Frequency and/or Volume; its Rate can sync to sequencer tempo and can itself be modulated by the Modulator.

Modulating LFO Rate while in SYNC mode forces the LFO to switch between sync divisions.

Envelope/loop playback starts as soon as audio is present in Sweeper, or can be triggered via Audio Trig or a rear-panel CV trig signal (Trig Envelope); Audio Trig and Trig Envelope can coexist.

---

<a id="alligator-triple-filtered-gate-48"></a>
## 48. Alligator Triple Filtered Gate


Like all effect devices, Alligator has a Bypass/On/Off switch and an input level meter (see "Common effect device features").

Select which of 64 built-in patterns plays back to control the gates (see "The built-in patterns" for a guide).

For a general introduction to filter types, see "The Filter Section" in the Subtractor chapter.

---

<a id="pulveriser-49"></a>
## 49. Pulveriser


Features and procedures common to all effect devices (Bypass/On/Off switch, etc.) are covered in "Common effect device features".

Filter options: a 24 dB/octave lowpass similar to Subtractor's LP24; a bandpass similar to Subtractor's BP12; a 12 dB/octave highpass similar to Subtractor's HP12; and a comb filter similar to Malström's "Comb +".

The LFO Rate range is very wide, reaching up into the audio frequency range; it can sync to sequencer tempo (Sync button), in which case the Rate knob sets sync resolution instead. Rate can also be modulated from the envelope follower in the Follower section.

---

<a id="the-echo-50"></a>
## 50. The Echo


Features common to all effect devices (Bypass On/Off, etc.) are covered in "Common effect device features". The Echo's Input Meter differs from the standard 7-segment LED meter elsewhere in Reason - it's a 3-segment meter (green/yellow/red, red = clipping).

Standard mode: input signal feeds continuously into the device (typical send/insert behavior).

Roll mode: the unprocessed (dry) signal passes through unaffected until you raise the Roll slider, which gradually suppresses Dry while raising Feedback and mixing delay/echo output into the Wet signal - useful for repeat, stutter, and glitch effects. Recommended: set Dry/Wet to (or near) Wet for Roll mode (see "Using the Roll function" for an example).

Setting Delay to Sync mode keeps repeats in sync with the loop, e.g. at 1/16th notes or another chosen resolution.

---

<a id="scream-4-sound-destruction-unit-51"></a>
## 51. Scream 4 Sound Destruction Unit


Common effect device features (Input meter, Bypass/On/Off switch, Signal Flow Graphs) are covered in "Common effect device features".

You don't have to route a whole drum kit through Scream - route individual outputs (bass drum, snare, toms) to a Spider Audio Merger, connect its merged output to Scream 4, then route that to a separate mixer channel, leaving hi-hats/cymbals unprocessed.

The Spider CV Merger and Splitter can invert and split the Auto CV output for extra flexibility.

---

<a id="bv512-vocoder-52"></a>
## 52. BV512 Vocoder


Typical vocoder setup (assumes a connected MIDI keyboard): the carrier needs high frequencies/harmonics - on Subtractor, a sawtooth-based sound with the filter fairly open works well as a simple, effective carrier (see "Choosing a carrier sound").

See "Recording audio from Mix Channel outputs" for recording Mix Channel output.

The individual band level connectors (CV) enable creative routing: cross-patch frequency bands so low frequencies in the modulator control high vocoder bands, extract CV signals to control synth parameters elsewhere, or base vocoding on CV from other devices instead of an audio modulator signal.

The Hold button "freezes" the current filter spectrum until deactivated - useful for sample & hold-like effects, stuttering, or garbled vocoder sounds.

The individual band level jacks on the back: the upper row outputs envelope-follower CV per frequency band; the lower jacks are CV inputs for controlling individual bandpass filters (this breaks the internal envelope-follower connection when patched).

---

<a id="rv7000-mk-ii-advanced-reverb-53"></a>
## 53. RV7000 Mk II Advanced Reverb


You typically don't want to hear the dry sound when using the Reverse effect (see "The Gate section").

Common effect device features (Input meter, Bypass/On/Off switch, Signal Flow Graphs) are in "Common effect device features".

In the Convolution algorithm, input signals are first summed to mono (except in Parallel Stereo Mode) then processed with the impulse response sample.

Changing some Convolution parameters recalculates the impulse response in real time, so modulating them can give unexpected results - CV modulation of RV7000 Mk II in Convolution mode is not recommended.

When combining the Gate function with Convolution, set Decay Mod to 0.

Stereo effects in the Stereo Mode alternatives require stereo samples/sampling in stereo (see the "Sampling" chapter).

---

<a id="neptune-pitch-adjuster-and-voice-synth-54"></a>
## 54. Neptune Pitch Adjuster and Voice Synth


Pitch correction controls include scale, correction speed, and a display showing Input Pitch, Target Note, and Catch Zone (see "Using pitch correction").

Pitch shifting parameters are covered in "Using pitch shifting (Transpose)".

Additional parameters define audio input characteristics (Input signal type), MIDI control (MIDI Input), and output level (Output Mixer section).

Catch Zones display as red horizontal boxes above each selected key on the virtual keyboard; a box turns green when the detected Input Pitch falls within its zone (see "Setting Catch Zone Size").

Wide Vibrato makes pitch detection ignore vibrato in the input audio (fixing wobbling notes/unwanted swoops caused by heavy vibrato); the vibrato can still be retained in the output by raising Preserve Expression.

A MIDI-enable option lets pitch correction be controlled via MIDI (see "Using manual pitch correction").

Four Scale Memory slots store Root Key, Scale, and Catch Zone settings for automation - similar to how Redrum stores which 16th-note buttons are active in a pattern. Automating Scale Memory slot selection from the Neptune sequencer track lets you switch pitch-correction characteristics through a song; settings save with the Song.

Preserve Expression controls how much input vibrato passes through at fast Correction Speed settings.

Receiving a MIDI note temporarily overrides Root Key/Scale/Catch Zone settings (Correction Speed and Preserve Expression stay active).

A Formant Shift setting can make pitch-adjusted vocals sound like the same person singing at the new pitch.

MIDI Input can route Note/Pitch Bend/Mod Wheel data either to the Pitch Adjust section (manual pitch-correction control) or to the Voice Synth (harmony-voice generation) - the routing choice determines which section responds.

Root Key and Scale are set via spin controls, or a custom scale by selecting individual notes on the keyboard display (see "Setting Root Key and Scale").

Edits to Root/Scale/Catch Zone auto-save into the selected Scale Memory slot and with the Song.

Catch Zone Size sets the input-pitch range corrected to specific notes.

Correction Speed sets how quickly pitch snaps to the target scale.

The Output Mixer slider sets total output volume for Pitch Adjust, Transpose and Formant sections to the L/R outputs.

CV inputs: Note (controls pitch of whichever of Pitch Adjust/Voice Synth is selected in MIDI Input, e.g. from a Matrix or RPG-8's Note CV out), Gate, Bend (pitch bend CV), and a Mod Wheel CV input (controls vibrato amount).

Left/Right outputs carry Pitch Adjust, Transpose and Formant audio; if Voice Synth Sep Output isn't connected, Voice Synth audio also routes to these main outputs.

Adjust Scale to fit the song key; override specific passages manually via MIDI when needed (see "Using automation for temporary pitch correction" and "Bouncing Mixer Channels").

---

<a id="softube-amps-55"></a>
## 55. Softube Amps


To use a Softube Amp as an insert effect while recording an audio track, you must monitor through Reason (see "Monitoring") - otherwise you won't hear the amp sound while recording.

Low latency matters here (see "Buffer Size settings"); good audio hardware/drivers can usually get down to a few milliseconds - comparable to standing a meter from a real guitar amp.

The front panel has a display area (Patch/Amp/Cabinet selectors) on top and standard amplifier tone controls below (see "Amp panel controls").

Common effect device features (Input meter, Bypass/On/Off, Signal Flow Graphs) are covered in "Common effect device features".

Loading/saving patches works like any other Reason device (see "Sounds, Patches and the Browser").

Any Amp model can be paired with any Cabinet + microphone model (see "About the Amp and Cabinet models").

---

<a id="audiomatic-retro-transformer-56"></a>
## 56. Audiomatic Retro Transformer


Designed mainly as an insert effect on individual tracks or the Master Inserts section; also works well as an insert on Parallel Channels in the Reason Mixer, letting you further sculpt the effect sound with the channel EQ and Compressor (see "Parallel Channels").

Use the Volume knob together with Gain to compensate for high input Gain settings.

A bipolar CV signal patched to the Transform CV input modulates the Transform parameter (positive increases it, negative decreases it).

A bipolar CV signal patched to the Dry/Wet CV input modulates the Dry/Wet control (zero modulation = current knob setting stays valid).

Effect type options include Tape, VHS, MP3, Wash, and PVC-style degradation.

---

<a id="channel-dynamics-compressor--gate-57"></a>
## 57. Channel Dynamics Compressor & Gate


## Introduction
This is the rack version of the Dynamics section in Reason's Main Mixer, mainly intended for the VST3 plugin version of Reason (which lacks the Main Mixer) but usable anywhere. It matches the channel strip version's specs plus adds Input Gain and Dry/Wet Mix controls.

## Global controls
Input Gain: +/-18.00 dB, affects the input signal regardless of whether Compressor/Gate are on.
Mix: blends dry and processed signal; <100% enables parallel processing (dry and effect output together).

## The Compressor section
Compressors reduce dynamic range, evening out loud/quiet differences for easier balancing, added punch and sustain. This compressor/limiter has soft-knee characteristics, switchable to peak limiting (instant reduction above threshold), plus automatic make-up gain.
On: activates the Compressor section.
Peak: switches detection from RMS to Peak (instant attack time) - suited to fast-attack sounds like drums.
Fast: fixed 3 ms reaction time for 20 dB gain reduction above Threshold.
Ratio: 1:1 (no reduction) to Infinite:1.
Threshold: -52 dB to 0 dB; signals below are unaffected, automatic make-up gain compensates based on Ratio and Threshold.
Release: 100 ms to 1000 ms; short = pumping effect, long = smoother.
Compressor Gain Reduction Meter: LED meter showing applied gain reduction.

## The Gate/Expander section
Gating/expansion attenuates signals below a threshold (opposite of compression) - useful for removing background noise or mic bleed (e.g., silencing tom mics between hits) and for "keying" effects. Ratios of 10:1+ are noise gating (fully silences below threshold).
On: activates the section.
Exp: switches Gate mode to Expander mode - less severe, more gradual gain reduction around Threshold (scaled rather than a fixed dB cut); Expander lets some signal through at lower volume rather than muting, effectively an "inverted compressor" that expands dynamic range. Range knob then sets expansion amount.
Hold: 0-4000 ms, time the gate stays fully open after signal falls below Threshold; Release only starts acting after Hold elapses.
Fast: lowers attack time from the normal 1.5 ms/40 dB to 100 microseconds/40 dB - useful for steep, percussive waveforms.
Range: 0 dB (no reduction) to -40 dB gain reduction below Threshold (controls expansion amount if Exp is on).
Threshold: -52 dB to 0 dB; closing threshold is slightly lower than opening threshold to avoid chattering near the set level.
Release: 100 ms to 1000 ms; fast = abrupt fade, long = slow fade-out.
Gate Gain Reduction Meter: LED meter for gating/expansion reduction.

## External Sidechain
Connect an external signal to the rear Sidechain Inputs to key the Compressor and/or Gate/Expander from it instead of the channel signal; a "Connected" LED lights when a cable is present. Example: trigger a synth-pad channel's gate from a drum loop for rhythmic chord effects.

## Connections
CV Outputs: Compressor Gain Reduction, and Gate Gain (high when gate is open, low when closed) - both usable to modulate other CV-capable devices.
Sidechain Input Left & Right: external sidechain signal input.
Input Left & Right: audio to process (mono signals connect only to L).
Output Left & Right: processed audio outputs.

---

<a id="channel-eq-equalizer-58"></a>
## 58. Channel EQ Equalizer


The "Q" parameter adjusts the bandwidth around the set center LMF (Low-Mid Frequency) Frequency - the higher the Q, the narrower the affected frequency range (except in "E" mode).

---

<a id="master-bus-compressor-59"></a>
## 59. Master Bus Compressor


## Introduction
This is the rack version of the Master Bus Compressor in Reason's Main Mixer, mainly for the VST3 plugin version (no Main Mixer there) but usable anywhere. It adds punch, cohesion, and general "glue" to a mix or bus - straightforward operation with make-up gain and program-adaptive Release. Matches the Master Section version's specs plus Input Gain and Dry/Wet Mix.

## Global controls
Mix: blend of dry/processed signal; <100% enables parallel processing.

## Compression controls
Input Gain: +/-18.00 dB.
Threshold: -30 dB to 0 dB; lower threshold = more compression.
Ratio: 2:1, 4:1, or 10:1 - e.g. 2:1 means a signal 2 dB above threshold outputs at 1 dB above.
Attack: 0.1, 0.3, 1, 3, 10, or 30 ms.
Release: 0.1, 0.3, 0.6, 1.2 s, or "Auto" (program-adaptive - longer after long peaks, shorter after short peaks).
Make Up: -5 dB to +15.00 dB, compensates for compression-caused level reduction.
Compressor Gain Reduction Meter: shows applied reduction in dB.

## External Sidechain
Connect an external signal to the rear Sidechain Inputs to key the compressor from it instead of the channel signal (e.g., a kick drum pattern triggering rhythmic pumping); a "Connected" LED lights when patched.

## Connections
Comp Gain Reduction: CV output of the gain reduction amount.
Sidechain Input Left & Right: external sidechain signal.
Input Left & Right: audio to process (mono connects only to L).
Output Left & Right: processed audio outputs.

---

<a id="synchronous-timed-effect-modulator-60"></a>
## 60. Synchronous Timed Effect Modulator


Loading/saving patches works like any other internal Reason device.

To replace an existing modulation curve anywhere in the loop, use the same method as changing a curve's amplitude, but choose any new curve shape freely, regardless of the existing one - this can be repeated at as many points in the loop as desired.

With the Sync button on, Time values step between tempo-relative divisions (1/1, 1/2, 1/4, 1/8, etc.).

With Ping Pong enabled, each delay repeat's stereo position alternates left/right; the Pan knob sets stereo width and the position of the initial repeat - full Left pans the first bounce hard Left then hard Right and so on; full Right reverses the order.

CV signals >0 patched to the Freeze inputs activate Freeze for the corresponding Modulation Curve; dropping to 0 or below deactivates it (see "FRZ (freeze) buttons").

A CV input can modulate the Master Level parameter, attenuable with its own knob.

---

<a id="the-mclass-effects-61"></a>
## 61. The MClass Effects


•

•

•

•

While the specific parameters for the MClass effect devices are described below, some features and procedures are common to all effect devices. Please, refer to “Common effect device features” for information about the Input meter, the Bypass/On/Off switch and Signal Flow Graphs on the effect devices.
---

<a id="half-rack-effects-62"></a>
## 62. Half-Rack Effects


| Mode

These allow you to control various effect parameters in real-time, from another device in the rack. See “Routing CV and Gate signals” for details about routing CV.

| Graph

•

4.

If you are unfamiliar with basic filter and envelope parameters, please refer to “Envelopes - General” in the Subtractor chapter for a description of these.

•

•

The PH-90 is a four-stage phaser, which means that there are four “notches” in the frequency response curve (this is a little like using four notch filters with different filter frequencies - see “Notch” in the Subtractor chapter for an explanation of notch filters).

•

•
---

<a id="the-combinator-63"></a>
## 63. The Combinator


Their internal order is not changed. Reason attempts to autoroute the first “input device” and first “output device” to the Combinator Mixer To/From Devices connectors - see “About internal and external audio connections”. Other connections are unchanged.

Please see “Adding devices to a Combi” for details about auto-routing.

The existing connections to the rack will be kept, so there may be external routing connections (see “About External Routing”). If there are, “External Routing” will be shown the Combinator name display (and on the back of the Combinator a LED indicator will be lit).

See “Key Mapping instrument devices” for details.

•

•

•

•

Double click on a control label, remove the current text and press [Enter]. Alternatively, uncheck “Show Label” in the Configuration panel in the Editor, see “Changing the appearance of the controls”).



1.

You can also control Combi parameters by connecting external CV modulation sources to any of the Source CV inputs on the back of the unfolded Editor panel, see “Wheel CV In and Source CV In”.

•

On the back of the Editor panel are CV Modulation Inputs for connecting external CV signals to modulate any of the parameters that are accessible in the Target section in the Editor, see “Wheel CV In and Source CV In”.

•

The Filter Reso parameter edited to have a reversed Range, as indicated by the light gray Range bar.

This means that you can create multi-function controls that operate simultaneously on several parameters. E.g. if you have two Subtractors and a Malström in a Combi you could create a “master” filter cutoff knob, that controls this parameter for all three devices. See “Controlling multiple Target parameters differently from a single Source control” for an example.



In this section you will find standard CV Pitch Bend and Mod Wheel modulation inputs, as well as eight modulation inputs which can be assigned as Sources in the Editor. Here you can connect external CV modulation sources for modulating any of the Target parameters in the Editor (see “Using Modulation Routing”).
---

<a id="pulsar-dual-lfo-64"></a>
## 64. Pulsar Dual LFO


#Rate

This controls the LFO rate. The Rate range in Pulsar is very wide and can reach way up in the audio frequency range. The rate is indicated by the lamp to the left above the Rate knob. The rate can also be synced to the sequencer tempo by clicking the Tempo Sync button below the Rate knob (see “Tempo Sync” below). In sync mode, the Rate knob controls the sync resolution.

The LFO 1 Rate can be modulated and/or synced by LFO 2, see “Rate (LFO 2 to LFO 1 Rate)” and “Sync”. The Rates can also be modulated from the Envelope, see “Envelope”. As a special feature, the Rates can also be controlled from a MIDI keyboard, see “KBD Follow”.

Here you set the output level of the LFO signal. The LFO 1 Level can be modulated by LFO 2, see “Level (LFO 2 to LFO 1 Level)”. The Levels can also be modulated by the Envelope, see “Envelope”.

Note that the total length of the cycle pair is always 2 regular cycles, which means that shuffling will work great also in Tempo Sync mode, see “Tempo Sync”.

#Lag

Click the Tempo Sync button to sync the LFO Rate to the sequencer tempo. This is great for creating animated effects in sync with the song’s tempo. In Tempo Sync mode, the Rate knob controls the sync resolution, see “Rate”.

If Tempo Sync is also active (see “Tempo Sync”) the LFO will continue to sync to the sequencer tempo. However, when you actually press a key or hit the Trig button will affect the LFO cycle start. In some situations this could be perceived as the LFO is losing sync but it’s not; it’s merely the LFO cycle start that is changing.

#Sync

#Trig

#Rate

#CV

#CV

A CV signal with a value > 0 present on this input will gate the Envelope (see “Envelope”). When the CV input signal decreases to zero or below, the gate is opened (deactivated).
---

<a id="rpg-8-arpeggiator-65"></a>
## 65. RPG-8 Arpeggiator


The various modes govern how the notes are arpeggiated. For example “Up” means from lowest note to highest note, Up+Down from lowest to highest note, then back down to lowest note again. For a description of all the modes see “Mode switch”.

If you play a new chord the arpeggio will continue to play, using the new notes. To stop the arpeggio, deactivate the Hold button or hit Stop on the transport. See “Hold On/Off”.

Straight, triplet and dotted note values are available. The arpeggiator can also be free running, i.e. not synced to tempo - see “Rate”.

If the knob is turned fully clockwise (“Tie”), the gate is always open (the notes will be played legato). If it is turned fully counter-clockwise, the gate is closed (no sound). See “Gate Length”.

With “1 Oct” selected the arpeggiated notes will be those that you press down on the keyboard. If “2 Oct” is selected the range will be expanded so that the arpeggiated notes play over two octaves, and so on - see “Octave range buttons”.

By using the Manual mode and varying the velocity for individual notes the arpeggio will become more animated and rhythmic. See “Velocity”.

You can also render the arpeggio output “to track” for full sequencer edit control of the notes generated by the RPG-8 - see “Rendering arpeggio notes to track”.

See “Pattern editor” for a description.



Depending on the situation, the above limitations may or may not be of concern. But there is a quick and effective solution to all above mentioned issues; the “Render Arpeggio Notes to Track” function (see “Rendering arpeggio notes to track”).

If you want to use separate simultaneous arpeggios, with each controlling one voice in a device, you have to use the “Arpeggio Notes to Track” function (see “Rendering arpeggio notes to track”) to separate Lanes in the target device track.

There is also a “Velocity CV” input at the back. If this is connected to a controller source (a LFO modulation output for example), the output will be a merge between the Velocity setting and the applied CV modulation by the LFO - see “CV Inputs”.

| Mode

#Rate

| Function

In addition to the above CV inputs, there is a “Start of Arpeggio Trig In” connector. This restarts the arpeggio figure from step 1 when this input receives a gate trigger. See “Triggering arpeggios” for a tip on how this can be used. If something is connected to this input the RPG-8 will not generate arpeggios unless a Gate trigger is received.
---

<a id="matrix-pattern-sequencer-66"></a>
## 66. Matrix Pattern Sequencer


•



Gate CV represents a note-on/off value, plus a level value (that could be likened to velocity).

If the Tempo track (see “Recording tempo automation”) is used, Matrix will follow this.

Bipolar curves are essential in some instances. If you want to use the Matrix to CV control the Pan parameter for a mixer channel for example, a unipolar curve would start at zero - which for Pan equals center position. This means that you would only be able to use the curve to pan in one direction from this center position. A bipolar curve however, will have the zero value in the middle, allowing you to draw pan curves in both directions. Bipolar curves can also be used for controlling parameters with positive and negative values.

Tied notes are also essential if you want to create typical TB-303 “Acid”-type lead lines - see “Programming “Acid Style” lead lines”.

In Reason, you can activate or deactivate shuffle individually for each pattern in a pattern device. However, the amount of shuffle is set globally with the Global Shuffle control in the ReGroove Mixer. The ReGroove Mixer is described in “The ReGroove Mixer”.

The Patterns play to the end before changing, so you won’t have worry too much over the “timing” of the pattern changes you input manually. When you are done, the sequencer track will contain pattern change data, and the patterns will automatically switch according to the order set while recording. More on recording pattern changes on “Recording pattern automation”.

2.

This parameter is used for modulating the output level (volume) of the synthesizer. Volume modulation is often referred to as Tremolo. You can use a unipolar curve (see “About Unipolar and Bipolar Curves”) for this example.

8.

If “Tie” (see “Using Tied Notes”) now is activated for a step, the note will be tied to the next and the pitch will continuously “glide” to the pitch of the following step.
---

<a id="mixer-142-67"></a>
## 67. Mixer 14:2


The four independent AUX Sends control the amount of channel signal that is to be sent to other devices - typically effect processors. The effect output is then normally returned to the Mixer via the AUX Return inputs (see “The Auxiliary Return Section”

) where it is mixed with the dry (non-processed) signal. If you create an effect device when the Mixer is selected, the effect is auto-routed to the first available Send/Return connectors. You can then control the amount of effect that is to be applied to any device connected to a Mixer channel via the corresponding AUX Send knob. The AUX Send outputs are taken post channel fader, but you have the option of selecting Pre-fader mode for AUX Send 4 (by clicking the “P” button next to the send so that it lights up). In that mode, the send level is independent of the channel fader.
---

<a id="the-line-mixer-62-68"></a>
## 68. The Line Mixer 6:2


## 
Introduction
The Line Mixer 6:2 allows you to control the level, stereo placement (Pan) and effect mix (AUX Send) of each connected audio device.
The Line Mixer is configured with 6 (stereo) input channels, which are combined and routed to the Left and Right Master outputs.
## 
Channel parameters
The channels are identical and contain an Auxiliary Send, Mute and Solo buttons, a Pan control, and a Level control:
|
Item
|
Description
Level control
This controls the output level of each corresponding channel, allowing you to set the desired mix (balance)
between different devices connected to the Line Mixer.
Channel label
Each channel in the mixer that has a device connected to it, displays a read-only label with the name of the
device.
Channel meter
The meter is a graphical representation of the channel output level. If the signal level pushes the meter into the range of the red area, try lowering either the output level of the device connected to the channel, or the Level control itself, to avoid distortion.
Pan control
Use this control to set the left/right position of the channel in the stereo field. [Ctrl]-click (Win) or the Pan knob to set Pan to the default “0” (center position).
Mute (M) and
Solo (S) Buttons
Clicking a channel’s Mute button silences the output of that channel. Click the button again to unmute the
channel.
Clicking a channel’s Solo button silences all other mixer channels, so that you only hear the soloed channel.
Several channels can be soloed at the same time. If this is the case, note that soloed channels can’t be muted with the Mute button. To mute one of several channels in solo mode you simply “unsolo” it.
Auxiliary (AUX) Effect Send
The AUX Send controls the amount of channel signal that is to be sent to other devices - typically effect
processors. The effect output is then normally returned to the Mixer via the AUX Return input where it is mixed with the dry (non-processed) signal. If you create an effect device when the Mixer is selected, the effect is auto-routed to the Send/Return connectors. You can then control the amount of effect that is to be applied to any
device connected to a Line Mixer channel via the AUX Send knob. The Send can be taken pre or post channel level - see
“Auxiliary (AUX) Send”
.
## 
The Auxiliary Return section
The AUX Return channels provide inputs for a connected send effect device. The Aux Return channels have a single level control on the front panel.
## 
Master level
The Master L/R fader controls the summed output level of all channels in the Mixer. Use this to change the relative level of all channels, to make fade-outs etc.
## 
Connections
All input and output connectors are as usual located on the back panel of the Line Mixer.
## 
Mixer Channel Connections
Each mixer channel features stereo left/right inputs for connecting audio devices.
Use the left input when manually connecting a mono signal source.
In addition, there is a Control Voltage (CV) input, for voltage controlling channel Pan from other devices.
## 
Auxiliary (AUX) Send
The Send connectors are used to connect to the inputs of effect devices.
To connect the send to a mono-input device, use the Left (Mono) output.
When a Send is connected to an effects device, the corresponding AUX Send knob determines the level of the signal sent to the effect device for each channel.
The Send Output can be taken Pre or Post channel level by using the switch to the left of the Send connectors.
## 
Auxiliary (AUX) Return
These are normally connected to the left and right outputs of effect devices.
## 
Master Left/Right Outputs
•
The Master outputs are auto-routed to the input pair of the first available Mix Channel device in the rack.
If no Mix Channel device is available, one will be automatically created when you create a Line Mixer device.
If used in a Combi, the Master Outs are normally connected to the “From Devices” connectors on the Combinator.
---

<a id="menu-and-dialog-reference-69"></a>
## 69. Menu and Dialog Reference


This menu item opens up the Preferences dialog. See “Preferences – General”, “Preferences – Audio”, “Preferences – MIDI”, “Preferences – Account”, “Preferences – Folders”, “Preferences – Sync” and “Preferences – Advanced” for detailed descriptions about the functions and settings in this dialog.

## New

When you select this, a new song appears. The exact contents of this song is determined by your Preferences settings (see “Default song”).

You can then save your song with a new name. See “Creating a new Song from a template” for more details.



See “Opening a Reason or Record Song” for more details.



See “Opening a Reason Demo Song” for more information.

## Save

•

This saves the active song document to disc. A standard Save As dialog appears requesting you to enter a file name and specify a location for the file on disk. The “Save As” command will also automatically optimize the song file size when applicable (see “Save and Optimize”).



See “Saving and optimizing a Song” for more details.

See “Including Song Information” for information.

See “About Self-Contained Songs” for more information.

See “Importing audio to the sequencer” for more information.

See “Importing Standard MIDI Files” for more information.

See “Exporting Standard MIDI Files” for more information.

See “Exporting Songs or parts of Songs” for more information.

See “Bouncing Mixer Channels” for information on how to bounce mixer channels.

## Undo

See “Undo and Redo” for more detailed information.

## Redo

See “Undo and Redo” for more detailed information.



















This will select all devices within the selected device’s Device Group. See “About selecting all devices in a Device Group”.

This function should be used if you want to rearrange devices, channel strips or sequencer tracks according to the order of the current selection. For example, if you want to rearrange the rack devices according to the current sequencer track order, you can select all sequencer tracks and then choose “Sort Selected Device Groups” to rearrange the rack devices. See “About the “Sort Selected Device Groups” function” for more examples.

See “The Combinator” for more details.

•

•

•

This allows you to create, and automatically route, one or several selected Main Mixer channel strips to a new or existing Output Bus for sub-mixing purposes. See “Creating an Output Bus”.

This allows you to create a parallel mixer channel for parallel processing purposes. See “Creating Parallel Channels”.

This disconnects and removes all Insert FX devices of a selected Mix Channel or Audio Track device in the rack, or of a selected channel in the Main Mixer. See “Deleting Insert effects” for more details.

REX files are music loops created in the ReCycle program or when editing audio clips inline in Reason (see “Bounce Clip to REX Loop”). The NN19 and NN-XT let you load REX files either as complete patches or individual REX slices as separate samples. The NN-Nano lets you load separate slices from REX files as individual samples.

3.

If the zone contained a sample prior to loading, this will be replaced, both in the zone and in the sample memory, unless the sample was also used by another key zone.

At least one of the zones must have a partial velocity range (see “Setting crossfading for a Zone”).

This function inserts an empty area between the locators in the main sequencer. All events after the left locator are moved to the right to “make room” for the inserted area. See “Inserting bars” for more information.

This function removes all material between the locators in the main sequencer. All events after the right locator are moved to the left to “fill out” the gap after the removed section. See “Removing bars” for more information.

## Edit

This opens the selected clip(s) in Edit mode in the sequencer. If multiple note clips are selected, they are opened for editing in Multi Lanes mode, see “Multi Lanes editing”.

The Bounce in Place function lets you bounce the sound generated from playing back note or audio clips, with any insert effects and channel strip coloration - but without Send FX and Master Section settings - to a new audio clip on a new audio track. See “Bounce in Place”.

It’s possible to bounce Audio Clips to new Song Samples. You could then edit the samples in the Edit Sample window and then load into a sampler device for playback. See “Bounce Clip(s) to New Sample(s)”.

This function allows you to export a selected audio clip as a WAV or AIFF file to disk. See “The “Bounce Clip to Disk” function”.

This function allows you to export the recording of a selected audio clip to an additional Comp Row. See “Bounce Clip(s) to New Recording(s)”.

This lets you bounce an open Single Take audio clip to a Rex file. The Rex file ends up on the Song Samples tab in the Tool Window. See “Bounce Clip to REX Loop”.

It’s possible to convert Single Take audio clips to note clips. This is especially useful for monophonic audio that can be opened in Pitch Edit mode. See “Bouncing audio to MIDI notes”.

This function allows you to choose which Stretch and Transpose Type to use for a selected Audio Clip. See “Opening audio clips for editing” for more information.

This lets you correct pitches of selected notes, or of all notes in an audio clip in Pitch Edit mode. See “Correcting pitches”.

This lets you reset the pitches of selected notes, or of all notes in an audio clip in Pitch Edit mode. See “Resetting pitches”.

This lets you split an open Single Take audio clip at the selected Slice Markers, and thus create several separate audio clips out of a bigger one. See “Split at Slices”.

This lets you split an open audio clip in Pitch Edit mode at the selected notes, and thus create several separate audio clips out of a bigger one. See “Splitting the clip at notes”.

This lets you undo all Slice Marker edits you made in an open Single Take audio clip and revert to the clip the way it was before you edited it. See “Revert All Slices”.

This lets you “undo” all edits you have made in Pitch Edit mode (similar to the “Revert Slices” function in Slice Edit mode). See “Reverting all notes”.

This function lets you decide if a selected audio clip should stretch and follow tempo changes in the song. When disabled, the audio clip doesn’t follow the song tempo. When enabled, the audio clip is stretched and follows the song tempo of the sequencer. See “About tempo changes and tempo automation of audio tracks”.

This function deletes all recordings that are not used in the selected clip - or anywhere else in the song. By using this function, the file size of the song can be reduced. See “Delete Unused Recordings”.

This function heals all selected audio clips that are affected by the Clip Safe function in the Propellerhead Balance audio interface. See “Recording using the Clip Safe function in Propellerhead Balance”.

This function deletes the Clip Safe signal from selected audio clips. The clips revert to being ordinary clips (no clipped waveform indication, and no healing button). See “Recording using the Clip Safe function in Propellerhead Balance”.

This function increases the overall audio level of selected Audio Clip(s) so that the loudest peak touches 0 dB. See “Normalizing audio clips”.

This function reverses selected Clip(s) and plays them back backwards, from the end to the start. See “Reverse” for information about reversing note and automation clips and “Reversing audio clips” for information about audio clips.

2.



•

Selecting “Crop Events To Clips” removes all such outside events from the selected clip(s). If tracks are selected in the track list, this function is performed on all clips on the selected track(s). See “About masked recordings and events” for more details.

See “Naming clips” for more information.

Allows you to select a color for the selected clip(s). See “Coloring clips” for more details.

See “About alien clips” for more information.

This lets you quantize note clips and Single Take audio clips, as well as selected notes in note clips, selected Slices in Single Take audio clips and selected notes in audio clips in Pitch Edit mode. See “Quantizing audio” and “Quantize”.

This lets you crossfade two partly overlapping audio clips. See “Crossfading audio clips” for more details.

This command is available when a sample is selected in the Song Samples location. Selecting Edit Sample opens the sample in the Edit Sample window. See “Editing samples” for more information.

This command is available when one or several samples are selected in the Song Samples location. Select this to create a duplicate of the selected sample. The duplicated sample is placed in the All Self-contained Samples and Unassigned Samples folders. Several selected samples can be duplicated in one go. See “Duplicating samples” for more details.

This command is available when one or several samples are selected in the Song Samples location. Select this to export the selected sample to disk. A dialog appears where you can select file format. Several selected samples can be exported in one go. See “Exporting samples” for more details.

This command is available when one or several samples are selected in the Song Samples location. Select this to permanently delete the selected sample(s) from the song. Note that samples from the Factory Soundbank and from ReFills will not be deleted from their original locations - only from the song document. Several selected samples can be deleted in one go. See “Deleting samples from a song” for more details.

This menu command is available when Keyboard Control Edit Mode is selected. It will open a dialog where you can assign a Keyboard Control for a selected parameter. See “Editing Keyboard Control” for more information.

This menu command is available when Keyboard Control Edit Mode is selected. It will remove the Keyboard Control mapping for a selected assigned parameter. See “Editing Keyboard Control” for more information.

This menu command is available when Keyboard Control Edit Mode is selected. It removes all keyboard mapping you have set up for the selected device. See “Editing Keyboard Control” for more information.

This menu command is available when Remote Override Edit Mode has been activated on the Options menu. It opens a dialog where you can assign a Remote Override for the selected parameter. See “Remote Override mapping”.

This menu command is available when Remote Override Edit Mode has been activated on the Options menu. It will remove the Remote Override mapping for a selected assigned parameter. See “Remote Override mapping”.

This menu command is available when Remote Override Edit Mode has been activated on the Options menu. It removes all Remote Override mapping you have set up for the selected device. See “Remote Override mapping”.

If the device you paste into is in the same song as the device you copied from, the operation will replace the existing overrides. See “Remote Override mapping”.

•

See “Cable appearance” for more details.

Here you can choose from a couple of different visual themes, i.e. how the user interface should be visually presented. The selected theme/color affects the Sequencer, Browser and Transport Panel areas. See “About different Themes”.

It’s possible to specify a certain song document which will automatically open as a “template” each time you select “New” from the File menu. The Default Song could be an empty document, a song you have created earlier, or a factory made Template song. See “Setting up a Default Song” for information on how to select Default Song.

•

•

The Sample Rate can be specified on the Audio tab in the Preferences dialog. See “Sample Rate settings for recording and playback” for more details.

The Buffer Size determines the Input and Output Latency of the audio. Generally, the smaller the Buffer Size, the lower the latency. However, too low a Buffer Size setting could result in clicks, pops, dropouts, etc. in the audio. Therefore, the Buffer Size should be set to an “optimal” value rather than to the lowest value. See “Buffer Size settings” for more information.

See “About latency” for more information.

If you are monitoring via an external mixer, and have selected “External” in the “Monitoring” section on the “Audio” page in Preferences (see “Monitoring”), there might be situations where you experience that the recorded audio is generally played back too early - or too late - in the song. This could be because the latency values reported to Reason by the audio card were not completely accurate.

See “Recording Latency Compensation” for information.

Active inputs and outputs will be also indicated with yellow and green LEDs in the Reason Hardware Interface - see “How Reason communicates with your audio hardware”.

See “Audio Basics” for more information on how Reason handles audio.

The “Render audio using audio card buffer size setting” function should be selected (checked) for best plugin performance. When selected, the audio batches are rendered internally according to the set Buffer size (see “Buffer size” above). For example, if you have a Buffer size of 512 Samples, each audio batch will be 512 samples internally. Raising the Buffer size will let Reason process larger audio batches in one go, which is often more efficient. Many plugins are also more efficient when doing larger audio batches. if you are using DSP-heavy VSTs (mastering effects, for example), these will run a lot smoother with this function selected.

Record enabling of audio tracks is done by clicking the Record Enable button on the track in the track list - see “Record enabling”.

Note that if you have selected “Standard” in the “Master Keyboard Input” section on the “MIDI” page in Preferences (see “The Master Keyboard Input setting”), selecting an audio track also automatically record enables it - and consequently enables monitoring in “Automatic” mode.

The surface designated as Master Keyboard cannot be locked to a specific device - it always follows the sequencer Master Keyboard Input. By selecting the Master Keyboard surface in the Attached Surfaces list and clicking this button allows you use Surface locking, although you will not be able to play the device. See “Locking a surface” in the Remote chapter for details.

See “Automatic set-up using the Easy MIDI Inputs function” for more details.

Please see “Authorizing a computer for long-term off-line use” for more information.

Here you can select the folders you want Reason to scan for VST plugins during each launch. See “Defining custom VST folders” for more information.

Here you can select where you want to locate the Scratch Disk Folder. The Scratch Disk Folder is a temporary storage for recorded audio files before they have been manually saved in a song document file. By default, Reason places the Scratch Disk folder in the system temp folder in your home directory. You can manually change the Scratch Disk folder location if you like. See “Changing Scratch Disk folder location” for more information.

This could be an external hardware sequencer or sequencer software that is installed on the same computer as Reason. See the chapter “Synchronization and Advanced MIDI” for more details.

As part of the MIDI Clock standard there are also options for sending out Start, Stop, Continue and Song Position Pointers, see “Using Reason as MIDI Clock Host”.

See the “Synchronization and Advanced MIDI” chapter for more information.

See “Adjusting for Latency” for more information.

See the “On-screen Piano Keys” chapter for information on how to use the On-screen Piano Keys.

You could then rename the track, device and channel strip afterwards if you like - see “Naming tracks”.

Depending on what type of device you create, the result can be different. See “Creating devices” for a complete description of what happens when you create different device types.

•

When this is activated, the program is synchronized to external MIDI Clock, as set up in the Preferences|Advanced dialog. The tempo setting on the Transport Panel is of no relevance; Reason plays in the tempo of the incoming MIDI Clock signals. See “Synchronization and Advanced MIDI” for more details.

When this is activated, the program can be synchronized to other Ableton Link-enabled devices on the same wireless network. See “Synchronization using Ableton Link” for more details.

When this is activated, the program is MIDI Clock Sync host and can control external applications/equipment. See “Synchronization and Advanced MIDI” for more details.

When this is activated, the computer’s keyboard keys can be used to control devices, as set up with the Keyboard Control Edit feature. See “Editing Keyboard Control” for more information.

Each device you select will show a yellow arrow symbol next to every parameter that can be assigned.

Another way to assign keyboard control commands is to have “Keyboard Control Edit Mode” deselected on the Options menu, and to right-click (Win) or [Ctrl]-click (Mac) the parameter you wish to keyboard control.

See “Editing Keyboard Control” for more information.

Another way to assign keyboard remote commands is to have “Remote Override Edit Mode” deselected on the Options menu, and to simply right-click (Win) or [Ctrl]-click (Mac) the parameter you wish to control.

See “Remote Override mapping” for more information.

See “Additional Remote Overrides...” for details.

See the “Locking a surface” for more details.

See “Cable appearance” for information on how to use this function.

A Device Group is a series of interconnected devices that “belong together”. A Device Group could, for example, be an instrument device connected via an effect device to a Mix Channel device. With the “Auto-group Devices and Tracks” option selected, moving/cutting/copying/duplicating and pasting a device in a device group will perform the operation on all devices in the device group. See “About Device Groups” for more details.

Select “Delay Compensation” to activate the built-in delay compensation, see “Activating the Delay Compensation”.

Select “Show CPU Load for Devices” to have the devices in the rack display how much CPU they use, see “Checking processing power for individual devices”.

When this is activated, the Tutorial area to the right in the song window is always shown - unfolded or folded, depending on if the area is open or minimized, see “The Tutorial area”.

Select if you want to change the zoom level (size) of the entire Reason application. Choose the desired zoom level on the sub-menu, see “Application Zoom”.

See “About drawing notes outside an open clip”, “About moving notes outside or between clips” and “Pasting events outside an open clip” for detailed examples.

This sends an All Notes Off MIDI command on the MIDI Out ports used by Reason. This function can be used if you are experiencing hanging notes when you are controlling external MIDI instruments from Reason. See “MIDI Out Device” for more information about MIDI controlling external equipment.

Selecting this brings up the manage Content window, where you can choose do download additional contents to Reason. See “Managing additional content”.

Selecting this brings up the Manage Plugins window, where you can manage your VST plugins. See “Managing VST plugins”.

Selecting this, or pressing [F4], will show or hide the floating On-screen Piano Keys window. See “On-screen Piano Keys” for information on how to use the On-screen Piano Keys window.

Selecting this, or pressing [F2], will show or hide the Spectrum EQ Window. See “The Spectrum EQ Window” for more information.

Selecting this, or pressing [Ctrl]+[F3], will show or hide the floating Recording Meter Window. See “The Recording Meter Window” for more information.

Selecting this brings up the Missing Sounds window. See “Handling Missing Sounds” for more information.

## Zoom

Selecting this brings up the manage Content window, where you can choose do download additional contents to Reason. See “Managing additional content”.

Selecting this brings up the Manage Plugins window, where you can manage your VST plugins. See “Managing VST plugins”.

Selecting this, or pressing [F4] will show or hide the floating On-screen Piano Keys window. See “On-screen Piano Keys” for information on how to use the On-screen Piano Keys window.

Selecting this, or pressing [F2], will show or hide the Spectrum EQ Window. See “The Spectrum EQ Window” for more information.

Selecting this, or pressing [Cmdl]+[F3], will show or hide the floating Recording Meter Window. See “The Recording Meter Window” for more information.

Selecting this brings up the Missing Sounds window. See “Handling Missing Sounds” for more information.
---

<a id="key-commands-70"></a>
## 70. Key Commands



## General keyboard shortcuts

- Maximize/restore Main Mixer: [F5]
- Maximize/restore Rack: [F6]
- Maximize/restore Sequencer: [F7] / [F5]+[F6] / [F5]+[F7] / [F6]+[F7]
- Detach/Attach Main Mixer: [Command]/[Ctrl]+[F5]
- Detach/Attach Rack: [Command]/[Ctrl]+[F6]
- View All in one window: [Command]/[Ctrl]+[F7] or [F5]+[F6]+[F7]
- Show/hide Spectrum EQ Window: [F2]
- Show/hide Browser: [F3]
- Show/Hide Recording Meter: [Command]/[Ctrl]+[F3]
- Show/hide On-screen Piano Keys window: [F4]
- Show/hide Tool window: [F8]
- Toggle Rack front/rear: [Tab]
- Create new Song: [Command]/[Ctrl]+[N]
- Open Song: [Command]/[Ctrl]+[O]
- Save Song: [Command]/[Ctrl]+[S]
- Save Song As: [Shift]+[Command]/[Shift]+[Ctrl]+[S] / [Command]/[Ctrl]+[W] / [Command]/[Ctrl]+[W]
- Import Audio File: [Command]+[Option]/[Shift]+[Ctrl]+[I]
- Quit (macOS only): [Command]+[Q]
- Exit (Windows only): [Alt]+[F4]
- Undo: [Command]/[Ctrl]+[Z]
- Redo: [Command]/[Ctrl]+[Y]
- Delete Devices and Tracks: [Del] or [Backspace]
- Select All: [Command]/[Ctrl]+[A]
- Route to > New Output Bus: [Command]/[Ctrl]+[G]
- Create Audio Track: [Command]/[Ctrl]+[T]
- Create Instrument: [Command]/[Ctrl]+[I]
- Create Instrument (Windows only): [Insert]
- Create Effect: [Command]/[Ctrl]+[F]
- Create Mix Channel: [Command]+[Shift]/[Ctrl]+[Shift]+[M]
- Browse Patches for selected device.: [Command]/[Ctrl]+[B]
- Toggle the “Reduce Cable Clutter” option: [K] / [Command]+[Shift]/[Ctrl]+[Shift]+[G]
- Toggle the “Follow Song” option: [F] / [Shift]+[Command]/[Shift]+[Ctrl]+[K] / [B]
- Hide Reason (macOS only): [Command]+[H]
- Minimize Reason (macOS only): [Command]+[M]
- Open Preferences (macOS only): [Command]+[,] / [Command]/[Ctrl]+[X] / [Command]/[Ctrl]+[C] / [Command]/[Ctrl]+[V]
- Open Help: [Command]+[?]/[F1]

## General modifier keys

- Disable auto-routing of device.: [Shift]+Create device
- Fold/unfold all devices.: [Option]/[Alt]+Fold/unfold device
- Fold/unfold all tracks.: [Option]/[Alt]+Fold/unfold track
- Select multiple devices/tracks/channels: [Command]/[Ctrl]+Select / [Shift]+Select
- Increase precision when making settings.: [Shift]+Move fader/knob
- Reset parameter to default value.: [Command]/[Ctrl]+Click fader/knob / [Option]/[Alt]+Create device

## Transport keyboard shortcuts

- Play
- Numeric keypad [Enter]: [Shift]+[Return] or numeric keypad [0]
- Go to start of Song: [,]/[.] on numeric keypad
- Toggle Stop/Play: [Spacebar]
- Record
- Rewind
- Numeric keypad [4]
- Fast Forward
- Numeric keypad [5]
- Go to Loop Start
- Go to Loop End
- Move forward one Bar
- Numeric keypad [8]
- Go back one Bar
- Numeric keypad [7]
- Tempo Up
- Numeric keypad [+]
- Tempo Down
- Numeric keypad [-]

## Sequencer keyboard shortcuts

- Toggle Arrange/Edit Mode.: [Shift]+[Tab] or [Command]/[Ctrl]+[E]
- Toggle Song/Blocks view.: [B]
- Select Arrow tool.: [Q]
- Select Pencil tool.: [W]
- Select Eraser tool.: [E]
- Select Razor tool.: [R]
- Select Mute tool: [T]
- Select Magnifying Glass tool.: [Y]
- Select Hand tool.: [U]
- Open selected clip for editing: [Return]
- Close open clip: [Esc]
- Quantize: [Command]/[Ctrl]+[K] / [Command]/[Ctrl]+[D]
- Join selected Clips on the same lane.: [Command]/[Ctrl]+[J]
- Merge Note Lanes on Tracks.: [Command]/[Ctrl]+[R] / [M]
- Snap on/off.: [S]
- Toggle Metronome click on/off: [C] or numeric keypad [9]
- Toggle Metronome Pre-count on/off: [Command]/[Ctrl] and [P]
- New Dub: [,] or numeric keypad [3]
- New Alt: [.] or numeric keypad [6]
- Loop on/off: [L] or numeric keypad [/] / [Command]/[Ctrl]+[L] / [P] / [X]
- Move Loop range one bar to the left: [Option]/[Alt]+[Shift] and up arrow key
- Move Loop range one bar to the right: [Option]/[Alt] and arrow up key. / [Option]/[Alt] and arrow down key.
- Horizontal zoom in: [H] or [Command]/[Ctrl]+[+]
- Horizontal zoom out: [G] or [Command]/[Ctrl]+[–]
- Vertical zoom in: [Command]+[Option]/[Ctrl]+[Alt]+[+]
- Vertical zoom out: [Command]+[Option]/[Ctrl]+[Alt]+[–] / [F]

## Sequencer keyboard shortcuts in Audio Edit Mode

- Select Speaker tool: [I]
- Change segment focus in Comp Mode.: [Esc] or [Return] / [Shift]+[Cmd]/[Shift]+[Ctrl]+[C]

## Sequencer modifier keys

- Select alternate tool in Toolbar: [Command]/[Alt] / [Option]/[Ctrl]
- Edit velocity of selected notes only: [Shift]+Move events/clips
- Copy data instead of moving it.: [Option]/[Ctrl]+Move data
- Set Left Locator in ruler.: [Option]/[Ctrl]+Click
- Set Right Locator in ruler.: [Command]/[Alt]+Click
- Set End Marker in ruler.: [Shift]+Click / [Shift]+Zoom with Magnifying Glass tool

## Sequencer modifier keys with mouse wheel

- Scroll horizontally.: [Shift]+Mouse wheel
- Zoom in/out vertically.: [Command]/[Ctrl]+Mouse wheel
- Zoom in/out horizontally.

## Sequencer modifier keys in Audio Edit Mode

- Fine-tune notes in Pitch Edit mode.

## Arrow keys

- Transpose selected notes in Edit mode: [Command]/[Ctrl]+ up/down arrow keys

## Save dialog keyboard shortcuts

- Cancel: [Command]+[.]/[Esc]
- Yes (save song): [Return]/[Y]
- No (do not save song): [Command]+[D]/[N]

## On-screen Piano Keys keyboard shortcuts

- Sustain: [Shift]
- Octave Down: [Z]
- Octave Up: [X]
- Velocity value = 1: [1]
- Velocity value = 14: [2]
- Velocity value = 28: [3]
- Velocity value = 42: [4]
- Velocity value = 56: [5]
- Velocity value = 70: [6]
- Velocity value = 84: [7]
- Velocity value = 98: [8]
- Velocity value = 112: [9]
- Velocity value = 127: [0]

## NN-19 modifier keys

- Audition sample.: [Option]/[Alt]+Click in keyboard display
- Edit selected sample: [Option]/[Alt]+Click the Sample button

## NN-XT keyboard shortcuts

- Remove zone(s) from key map.: [Delete] or [Backspace]
- Select All Zones: [Command]/[Ctrl]+[A]
- Copy selected Zone(s): [Command]/[Ctrl]+[C]
- Paste currently copied Zone(s): [Command]/[Ctrl]+[V]

## NN-XT modifier keys

- Set root note of sample with edit focus.
- Edit selected sample: [Option]/[Alt]+Click the Sample button

## Dr. Octo Rex keyboard shortcuts

- Cut Loop.: [Command]/[Ctrl]+[X]
- Copy Loop.: [Command]/[Ctrl]+[C]
- Paste Loop.: [Command]/[Ctrl]+[V]

## Dr. Octo Rex modifier keys

- Audition slice.: [Option]/[Alt]+Click slice in overview

## Redrum keyboard shortcuts

- Cut Pattern.: [Command]/[Ctrl]+[X]
- Copy Pattern.: [Command]/[Ctrl]+[C]
- Paste pattern.: [Command]/[Ctrl]+[V]
- Shift Pattern Left.: [Command]/[Ctrl]+[J]
- Shift Pattern Right.: [Command]/[Ctrl]+[K]
- Randomize Pattern.: [Command]/[Ctrl]+[R]
- Alter Pattern.: [Shift]+[Command]/[Shift]+[Ctrl]+[P]

## Redrum modifier keys

- Edit selected sample: [Option]/[Alt]+Click a Sample button

## Kong modifier keys

- Audition slice in Nurse Rex.: [Option]/[Alt]+Click slice in overview
- Toggle “Trig” for slice(s) in Nurse Rex: [Command]/[Ctrl]+ click in overview.
- Edit selected sample

## Matrix keyboard shortcuts

- Cut Pattern.: [Command]/[Ctrl]+[X]
- Copy Pattern.: [Command]/[Ctrl]+[C]
- Paste Pattern.: [Command]/[Ctrl]+[V]
- Shift Pattern Left.: [Command]/[Ctrl]+[J]
- Shift Pattern Right.: [Command]/[Ctrl]+[K]
- Shift Pattern Up.: [Shift]+[Command]/[Shift]+[Ctrl]+[U]
- Shift Pattern Down.: [Shift]+[Command]/[Shift]+[Ctrl]+[D]
- Randomize Pattern.: [Command]/[Ctrl]+[R]
- Alter Pattern.: [Shift]+[Command]/[Shift]+[Ctrl]+[P]

## Matrix modifier keys

- Allows you to draw lines and ramps.: [Shift]+Draw Key/Curve values
- Temporarily toggle Tie mode on/off.: [Shift]+Draw Gate

## RPG-8 keyboard shortcuts

- Shift Pattern Left.: [Command]/[Ctrl]+[J]
- Shift Pattern Right.: [Command]/[Ctrl]+[K]
- Randomize Pattern.: [Command]/[Ctrl]+[R]
- Alter Pattern.: [Shift]+[Command]/[Shift]+[Ctrl]+[P]

## MIDI Out Device keyboard shortcuts

- MIDI: Send All Notes Off: [!]

## Europa modifier keys

- Add/remove Envelope points.
- Erase points in “Edit Y-Pos” mode.

## Grain modifier keys

- Add/remove Envelope points.
- Erase points in “Edit Y-Pos” mode.

## Sweeper modifier keys

- Add/remove Envelope points.
- Erase Envelope points in “Edit” mode.

## Mimic modifier keys

- Set Start Marker
- Double click in the Waveform Display
- Set End Marker
- Preview Sample
- Set Loop Point (when Loop is active)
- Set Root Note
---
