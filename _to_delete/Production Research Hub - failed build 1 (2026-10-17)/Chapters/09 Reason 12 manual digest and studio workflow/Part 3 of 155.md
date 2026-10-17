# Chapter 09: Reason 12 manual digest and studio workflow
## Part 3 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- key-commands.md (piece 1 of 3) — Reason 12.7 Key Commands (digest)

(Next: Part 4 of 155)


=====================================================
SOURCE FILE: key-commands.md (piece 1 of 3)
ORIGINAL LOCATION: HS:docs/reason/manual-digest/key-commands.md
=====================================================

# Reason 12.7 Key Commands (digest)

Source: Reason 12.7 Operation Manual, ch. 70 (`~/.reason_voice/reason12_manual/full_chapters/70-key-commands.txt`).
Built by script from the manual text on 2026-09-30, then spot-checked. Where a wrapped line was joined, check the
manual page (1439-1466) before relying on it. In the Keys column the **Mac key is left of the slash, Windows right**.
Tag: all rows **Manual**; nothing here was tried on the owner's machine.

Index: [manual-digest README](README.md)

## General keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Maximize/restore Main Mixer | [F5] |
| Maximize/restore Rack | [F6] |
| Maximize/restore Sequencer | [F7] |
| Maximize Main Mixer and Rack in one window | [F5]+[F6] |
| Maximize Main Mixer and Sequencer in one window | [F5]+[F7] |
| Maximize Rack and Sequencer in one window | [F6]+[F7] |
| Detach/Attach Main Mixer | [Command]/[Ctrl]+[F5] |
| Detach/Attach Rack | [Command]/[Ctrl]+[F6] |
| View All in one window | [Command]/[Ctrl]+[F7] or [F5]+[F6]+[F7] |
| Show/hide Spectrum EQ Window | [F2] |
| Show/hide Browser | [F3] |
| Show/Hide Recording Meter | [Command]/[Ctrl]+[F3] |
| Show/hide On-screen Piano Keys window | [F4] |
| Show/hide Tool window | [F8] |
| Toggle Rack front/rear | [Tab] |
| Create new Song | [Command]/[Ctrl]+[N] |
| Open Song | [Command]/[Ctrl]+[O] |
| Save Song | [Command]/[Ctrl]+[S] |
| Save Song As | [Shift]+[Command]/[Shift]+[Ctrl]+[S] |
| Close active detached Rack or Mixer window | [Command]/[Ctrl]+[W] |
| Close Song (if the window containing the Sequencer is active) | [Command]/[Ctrl]+[W] |
| Import Audio File | [Command]+[Option]/[Shift]+[Ctrl]+[I] |
| Quit (macOS only) | [Command]+[Q] |
| Exit (Windows only) | [Alt]+[F4] |
| Undo | [Command]/[Ctrl]+[Z] |
| Redo | [Command]/[Ctrl]+[Y] |
| Delete Devices and Tracks | [Del] or [Backspace] |
| Delete Devices and Tracks (without warning). | [Command]/[Ctrl]+[Del] or [Command]/[Ctrl]+[Backspace] |
| Duplicate Devices and tracks, or selected clip(s), or selected comp row(s) in open audio clips, or selected note(s) in note clips, or selected automation point(s) in automation clips. | [Command]/[Ctrl]+[D] |
| Select All | [Command]/[Ctrl]+[A] |
| Route to > New Output Bus | [Command]/[Ctrl]+[G] |
| Create Audio Track | [Command]/[Ctrl]+[T] |
| Create Instrument | [Command]/[Ctrl]+[I] |
| Create Instrument (Windows only) | [Insert] |
| Create Effect | [Command]/[Ctrl]+[F] |
| Create Mix Channel | [Command]+[Shift]/[Ctrl]+[Shift]+[M] |
| Browse Patches for selected device. | [Command]/[Ctrl]+[B] |
| Toggle the “Reduce Cable Clutter” option | [K] |
| Toggle the “Auto-group Devices and Tracks” option | [Command]+[Shift]/[Ctrl]+[Shift]+[G] |
| Toggle the “Follow Song” option | [F] |
| Toggle the “Keep Events in Clip While Editing” option | [Shift]+[Command]/[Shift]+[Ctrl]+[K] |
| Toggle the Show Block/Song View option (when Blocks are on) | [B] |
| Hide Reason (macOS only) | [Command]+[H] |
| Minimize Reason (macOS only) | [Command]+[M] |
| Open Preferences (macOS only) Cut Track & Device (track selected in Track List), Cut Clip or Event (depending [Command]/[Ctrl]+[X] on current selection). Copy Track & Device (track selected in Track List), Copy Clip or Event (depend- [Command]/[Ctrl]+[C] ing on current selection). | [Command]+[,] |
| Paste Track & Device, Paste Clip or Event. | [Command]/[Ctrl]+[V] |
| Open Help | [Command]+[?]/[F1] |
| Switch to one of the 10 corresponding global Remote variations (or "keyboard shortcut variations"). | [Command]+[Option]/[Ctrl]+[Alt]+[1]...[0] |

## General modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Duplicate (copy) the selected item and its corresponding components. | [Option]/[Ctrl]+drag and drop device/track/mixer channel |
| Disable auto-routing of device. | [Shift]+Create device |
| Fold/unfold all devices. | [Option]/[Alt]+Fold/unfold device |
| Fold/unfold all tracks. | [Option]/[Alt]+Fold/unfold track |
| Select multiple devices/tracks/channels | [Command]/[Ctrl]+Select |
| Select range of multiple devices/tracks/channels | [Shift]+Select |
| Select multiple clips/events in the Sequencer range of clips/events on a single Lane in the Sequencer) | [Shift]/[Ctrl]+Select (Windows only: [Shift]+Select to select a |
| Increase precision when making settings. | [Shift]+Move fader/knob |
| Reset parameter to default value. | [Command]/[Ctrl]+Click fader/knob |
| Prevent creation of Sequencer-track for devices that normally will get a track. Create Sequencer-track for devices that normally will not get a track. | [Option]/[Alt]+Create device |
| Create a parameter automation lane for the parameter. | [Option]/[Alt]+Click device fader/knob/button |

## Transport keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Play | Numeric keypad [Enter] |
| Stop, Go to start position, Go to start of Song. | [Shift]+[Return] or numeric keypad [0] |
| Go to start of Song | [,]/[.] on numeric keypad |
| Toggle Stop/Play | [Spacebar] |
| Record | [Command]/[Ctrl]+[Return] or numeric keypad [*] |
| Rewind | Numeric keypad [4] |
| Fast Forward | Numeric keypad [5] |
| Go to Loop Start | [Option]/[Alt] and left arrow key, or numeric keypad [1] |
| Go to Loop End | [Option]/[Alt] and right arrow key, or numeric keypad [2] |
| Move forward one Bar | Numeric keypad [8] |
| Go back one Bar | Numeric keypad [7] |
| Tempo Up | Numeric keypad [+] |
| Tempo Down | Numeric keypad [-] |

## Sequencer keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Toggle Arrange/Edit Mode. | [Shift]+[Tab] or [Command]/[Ctrl]+[E] |
| Toggle Song/Blocks view. | [B] |
| Select Arrow tool. | [Q] |
| Select Pencil tool. | [W] |
| Select Eraser tool. | [E] |
| Select Razor tool. | [R] |
| Select Mute tool | [T] |
| Select Magnifying Glass tool. | [Y] |
| Select Hand tool. | [U] |
| Open selected clip for editing | [Return] |
| Close open clip | [Esc] |
| Quantize | [Command]/[Ctrl]+[K] |
| Duplicate Track & Device (device or track selected). | [Command]/[Ctrl]+[D] |
| Join selected Clips on the same lane. | [Command]/[Ctrl]+[J] |
| Merge Note Lanes on Tracks. | [Command]/[Ctrl]+[R] |
| Mute/Unmute selected Clips or selected Notes in an open Note Clip. | [M] |
| Snap on/off. | [S] |
| Toggle Metronome click on/off | [C] or numeric keypad [9] |
| Toggle Metronome Pre-count on/off | [Command]/[Ctrl] and [P] |
| New Dub | [,] or numeric keypad [3] |
| New Alt | [.] or numeric keypad [6] |
| Loop on/off | [L] or numeric keypad [/] |
| Set Loop Locators to encompass all selected clips Set the Left and Right Loop Locators to encompass selected clips and start play- [P] back in Loop Mode. | [Command]/[Ctrl]+[L] |
| Crossfade selected (partly) overlapping audio clips | [X] |
| Transpose selected notes up/down in octave steps | [Shift]+[Command]/[Shift]+[Ctrl] and up/down arrow keys |
| Move Loop range one bar to the left | [Option]/[Alt]+[Shift] and up arrow key |
| Move Loop range one bar to the right | [Option]/[Alt]+[Shift] and down arrow key |
| Move current Loop range one loop length to the left. | [Option]/[Alt] and arrow up key. |
| Move current Loop range one loop length to the right. | [Option]/[Alt] and arrow down key. |
| Horizontal zoom in | [H] or [Command]/[Ctrl]+[+] |
| Horizontal zoom out | [G] or [Command]/[Ctrl]+[–] |
| Vertical zoom in | [Command]+[Option]/[Ctrl]+[Alt]+[+] |
| Vertical zoom out | [Command]+[Option]/[Ctrl]+[Alt]+[–] |
| Zoom To Selection/Show All (e.g. selected clips) | [Z] (horizontal only), [Shift]+[Z] (horizontal and vertical) |
| Follow Song on/off (auto-scrolling Arrange/Edit pane) | [F] |

## Sequencer keyboard shortcuts in Audio Edit Mode

| Function | Keys (Mac / Windows) |
|---|---|
| Select Speaker tool | [I] |
| Change Comp Row assignment in the segment with focus in Comp Mode up/down arrow keys | [Command]+[Option]+[Shift]/[Ctrl]+[Alt]+[Shift] and |
| Change segment focus in Comp Mode. left/right arrow keys | [Command]+[Option]+[Shift]/[Ctrl]+[Alt]+[Shift] and |
| Exit Slice Edit mode for Single Take audio clips | [Esc] or [Return] |
| Correct note pitch(es) in Pitch Edit Mode. | [Shift]+[Cmd]/[Shift]+[Ctrl]+[C] |

## Sequencer modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Select alternate tool in Toolbar | [Command]/[Alt] |
| Toggle Pencil/Line tool (velocity edit lane only). | [Option]/[Ctrl] |
| Edit velocity of selected notes only Create automation lane for parameter. If device has no track, a track will also be [Option]/[Alt]+Click knob/fader/button created. | [Shift]+click/draw with Pencil tool on Velocity lane |
| Add automation event exactly on the automation line | [Shift]+click with Pencil tool in the open automation clip. |
| Restrict movement direction to either horizontal or vertical. | [Shift]+Move events/clips |
| Zoom in/out horizontally on the Edit/Arrange pane. Zoom in/out horizontally on the Edit/Arrange pane. (Drag sideways to scroll hor- [Shift]+Drag up/down in Song Navigator frame izontally at the same time) | [Shift]+Drag any of the Song Navigator handles sideways |
| Copy data instead of moving it. | [Option]/[Ctrl]+Move data |
| Set Left Locator in ruler. | [Option]/[Ctrl]+Click |
| Set Right Locator in ruler. | [Command]/[Alt]+Click |
| Set End Marker in ruler. Switch to zoom out with the Magnifying Glass tool instead of zoom in (with either [Option]/[Ctrl]+Click the Magnifying Glass- or the Hand tool selected). | [Shift]+Click |
| Limit movement to one direction only. Horizontal or vertical. | [Shift]+Drag with Hand tool or Eraser tool |
| Disable vertical zooming. Horizontal zoom only. | [Shift]+Zoom with Magnifying Glass tool |

## Sequencer modifier keys with mouse wheel

| Function | Keys (Mac / Windows) |
|---|---|
| Scroll horizontally. | [Shift]+Mouse wheel |
| Zoom in/out vertically. | [Command]/[Ctrl]+Mouse wheel |
| Zoom in/out horizontally. | [Shift]+[Command]/[Shift]+[Ctrl]+Mouse wheel |

## Sequencer modifier keys in Audio Edit Mode

| Function | Keys (Mac / Windows) |
|---|---|
| Switch from Arrow tool to Cut (Razor) tool on the comp rows in an open audio clip | [Command]/[Altl] |
| Switch from Arrow tool to Speaker tool on the comp rows in an open audio clip | [Command]+[Shift]/[Alt]+[Shift] |
| Duplicate the Comp Row and create a new Cut or Segment in the duplicated Comp | [Command]+[Option]/[Ctrl]+[Alt] and click or swipe on |
| Row. | Comp Row |
| Fine-tune notes in Pitch Edit mode. the note pane. | [Shift]+[Command]/[Shift]+[Alt]-drag notes up/down on |

## Arrow keys

| Function | Keys (Mac / Windows) |
|---|---|
| Select next device up or down (rack selected), select next track up or down (track list selected), select clip on next/previous lane (Arrange view selected). Select next/previous clip on lane (Arrange view selected), select next/previous Arrow left/right keys value field (Position displays). | Arrow up/down keys |
| Nudge selection one Snap unit back/forward in the sequencer. | [Command]/[Ctrl]+Arrow left/right keys |
| Nudge selection one Beat back/forward in the sequencer. | [Shift]+[Command]/[Shift]+[Ctrl]+Arrow left/right keys |
| Nudge selection one Tick back/forward in the sequencer. | [Option]+[Command]/[Alt]+[Ctrl]+Arrow left/right keys |
| Transpose selected notes in Edit mode Save dialog keyboard shortcuts These key commands can be used in the save dialog that appears if you close a song document that contains un- | [Command]/[Ctrl]+ up/down arrow keys |

## Save dialog keyboard shortcuts (when closing an unsaved song)

| Function | Keys (Mac / Windows) |
|---|---|
| Cancel | [Command]+[.]/[Esc] |
| Yes (save song) | [Return]/[Y] |
| No (do not save song) On-screen Piano Keys keyboard shortcuts | [Command]+[D]/[N] |

## On-screen Piano Keys shortcuts (window open, set to “Computer Keys”)

| Function | Keys (Mac / Windows) |
|---|---|
| Sustain | [Shift] |
| Octave Down | [Z] |
| Octave Up | [X] |
| Velocity value = 1 | [1] |
| Velocity value = 14 | [2] |
| Velocity value = 28 | [3] |
| Velocity value = 42 | [4] |
| Velocity value = 56 | [5] |
| Velocity value = 70 | [6] |
| Velocity value = 84 | [7] |
| Velocity value = 98 | [8] |
| Velocity value = 112 | [9] |
| Velocity value = 127 | [0] |

## NN-19 modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Audition sample. | [Option]/[Alt]+Click in keyboard display |
| Edit selected sample | [Option]/[Alt]+Click the Sample button |

## NN-XT keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Remove zone(s) from key map. | [Delete] or [Backspace] |
| Select All Zones | [Command]/[Ctrl]+[A] |
| Copy selected Zone(s) | [Command]/[Ctrl]+[C] |
| Paste currently copied Zone(s) | [Command]/[Ctrl]+[V] |

## NN-XT modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Audition sample. In sample column, at root pitch and unprocessed. In keyboard column, at corresponding pitch and with processing applied. | [Option]/[Alt]+Click in sample column or keyboard column |
| Set root note of sample with edit focus. | [Command]/[Ctrl]+Click in keyboard column |
| Edit selected sample | [Option]/[Alt]+Click the Sample button |

## Dr. Octo Rex keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Cut Loop. | [Command]/[Ctrl]+[X] |
| Copy Loop. | [Command]/[Ctrl]+[C] |
| Paste Loop. | [Command]/[Ctrl]+[V] |

## Dr. Octo Rex modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Audition slice. | [Option]/[Alt]+Click slice in overview |
| Reset slice(s) to default parameter value in Slice Edit Mode | [Command]/[Ctrl]+ click/click and drag in overview. |

## Redrum keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Cut Pattern. | [Command]/[Ctrl]+[X] |
| Copy Pattern. | [Command]/[Ctrl]+[C] |
| Paste pattern. | [Command]/[Ctrl]+[V] |
| Shift Pattern Left. | [Command]/[Ctrl]+[J] |
| Shift Pattern Right. | [Command]/[Ctrl]+[K] |
| Randomize Pattern. | [Command]/[Ctrl]+[R] |
| Alter Pattern. | [Shift]+[Command]/[Shift]+[Ctrl]+[P] |

## Redrum modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Enter “Hard” note when programming Pattern. | [Shift]+Click Pattern Step button |
| Enter “Soft” note when programming Pattern. | [Option]/[Alt]+Click Pattern Step button |
| Edit selected sample | [Option]/[Alt]+Click a Sample button |

## Kong modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Audition slice in Nurse Rex. | [Option]/[Alt]+Click slice in overview |
| Toggle “Trig” for slice(s) in Nurse Rex | [Command]/[Ctrl]+ click in overview. |
| Edit selected sample | [Option]/[Alt]+Click the Sample button in the NN-Nano |

## Matrix keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Cut Pattern. | [Command]/[Ctrl]+[X] |
| Copy Pattern. | [Command]/[Ctrl]+[C] |
| Paste Pattern. | [Command]/[Ctrl]+[V] |
| Shift Pattern Left. | [Command]/[Ctrl]+[J] |
| Shift Pattern Right. | [Command]/[Ctrl]+[K] |
| Shift Pattern Up. | [Shift]+[Command]/[Shift]+[Ctrl]+[U] |
| Shift Pattern Down. | [Shift]+[Command]/[Shift]+[Ctrl]+[D] |
| Randomize Pattern. | [Command]/[Ctrl]+[R] |
| Alter Pattern. | [Shift]+[Command]/[Shift]+[Ctrl]+[P] |

## Matrix modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Allows you to draw lines and ramps. | [Shift]+Draw Key/Curve values |
| Temporarily toggle Tie mode on/off. | [Shift]+Draw Gate |

## RPG-8 keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| Shift Pattern Left. | [Command]/[Ctrl]+[J] |
| Shift Pattern Right. | [Command]/[Ctrl]+[K] |
| Randomize Pattern. | [Command]/[Ctrl]+[R] |
| Alter Pattern. | [Shift]+[Command]/[Shift]+[Ctrl]+[P] |

## MIDI Out Device keyboard shortcuts

| Function | Keys (Mac / Windows) |
|---|---|
| MIDI: Send All Notes Off | [!] |

## Europa modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Add/remove Envelope points. | [Command]/[Ctrl]+Click in the Envelope display |
| Freehand drawing of Envelope curves in “Edit Y-Pos” mode. | [Command]/[Ctrl]+Click in the Envelope display |
| Erase points in “Edit Y-Pos” mode. | [Shift]+[Command]/[Shift]+[Ctrl]+Drag in the Envelope display |

## Grain modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Add/remove Envelope points. | [Command]/[Ctrl]+Click in the Envelope display |
| Freehand drawing of Envelope curves in “Edit Y-Pos” mode. | [Command]/[Ctrl]+Click in the Envelope display |
| Erase points in “Edit Y-Pos” mode. | [Shift]+[Command]/[Shift]+[Ctrl]+Drag in the Envelope display |

## Sweeper modifier keys

| Function | Keys (Mac / Windows) |
|---|---|
| Add/remove Envelope points. | [Command]/[Ctrl]+Click in the Envelope display |
| Freehand drawing of Envelope curves in “Edit” mode. | [Command]/[Ctrl]+Click in the Envelope display |
| Erase Envelope points in “Edit” mode. | [Shift]+[Command]/[Shift]+[Ctrl]+Drag in the Envelope display |


=== END OF PART ===
