# Arranging: clip handling, repeat tricks, bounce, insert/remove bars
Source: Reason 12.7 Operation Manual, ch. 7 (whole chapter read, ends p. 202). Tag: **Manual**.
Tracks, lanes, tools, Snap and locators are in `sequencer-functions.md`. Sections you reuse (Blocks) are in `blocks.md`. Comping and audio clip internals are in `audio-editing.md`.
(KC) = from the Key Commands chapter, `key-commands.md`.

## 1. The 10 moves that build a song fast
| Job | Do this |
|---|---|
| Make an empty clip | Double-click a lane with the arrow (length = Snap value, e.g. 1 bar). Double-click and drag right for longer. Or draw with the Pencil (**W**) |
| **Repeat a whole section** | Stop. Snap on, Snap = Bar (or section length). Select the clips (can be on many tracks). **Cmd+C**. Playhead jumps to the end of the selection. **Cmd+V**, then V again and again. Each paste lands right after the last |
| Quick copies in a row | **Cmd+D** on selected clips. Copies line up after each other, spaced by Snap |
| Drag a copy | **Option+drag** (cursor shows +). Copies on the same lane or another |
| Split anywhere | Razor (**R**) click. Notes that cross the cut stay whole |
| Split EVERY track at one spot | Razor click in the **Ruler**. Includes lanes scrolled out of view |
| Cut a hole out of the whole song | Razor click-drag in the Ruler. Releases = clips split at both ends |
| Silence a part without deleting | Mute tool (**T**) or select + **M** (M again to unmute) |
| Make the end of a part longer | Select clips, drag any resize handle. All selected grow the same amount |
| Change many clip lengths/positions at once | Inspector Position/Length boxes, or Match Values (sec. 7) |

## 2. Selecting
- Click a clip. Click empty space to deselect.
- Several: **Shift+click** on Mac [Ctrl+click on Windows]. Or drag a box with the arrow (anything touched is picked). Shift while boxing adds to what is already picked. **Cmd+A** = all.
- Arrow keys: Left/Right = previous/next clip on the lane. Up/Down = closest clip on the lane above/below. Shift+Left/Right = extend on the same lane.
- Selected note clips: open several together for Multi Lanes editing (`note-and-automation-editing.md`).

## 3. Resize = mask, nothing is deleted
- Shrinking a clip HIDES what falls outside. Notes, audio and automation are still inside and come back when you drag the edge out again. Masked events travel with the clip when moved, cut or copied.
- Note/automation clips show **white corners** where masked events sit. Audio clips show no sign.
- Masked notes turn blue in the open clip. A note that STARTS inside the clip still plays in full.
- Edge case: a masked controller/automation point just outside the clip still bends the curve toward it inside. Black-and-white points = still active.
- **Edit > Crop Events to Clips** permanently deletes everything outside the edges. Use only when you want it gone.
- Audio fades follow the clip edges when you resize.

## 4. Moving
| Do | How |
|---|---|
| Move on the lane | Drag (obeys Snap) |
| Move to another lane or track | Drag. **Shift** while dragging = straight up/down only (on Windows press Shift AFTER the mouse button) |
| Nudge by Snap value | **Cmd+Left/Right** (works with Snap off) |
| Nudge by a beat | **Cmd+Shift+Left/Right** |
| Nudge by a tick (240 per 16th) | **Cmd+Option+Left/Right**. Watch the Inspector, you will not see it |
| Cut then paste at playhead | Cut, move playhead, Paste. Lands on its ORIGINAL lane |
- Wrong lane type = **alien clip** (red stripes, plays nothing). Hover for the reason. A note clip on an automation lane is alien. An automation clip on a lane with a different range (e.g. -64..63 vs 0..127) is alien. Fix the range case with **Edit > Adjust Alien Clips to Lane**.
- Moving a note clip to another instrument: Pitch Bend, Mod Wheel, Sustain translate fine. Not every device answers Aftertouch/Expression/Breath (Malström does not). Odd recorded knob moves with no match are ignored.
- Paste into ANOTHER song: select a track there, set the playhead, paste. Missing tracks come in on empty Combinators. Pick a patch in that Combinator.

## 5. Overlap rules
- A lane plays ONE clip at a time. To hear two at once, use separate note lanes or separate tracks.
- The clip that STARTS LATER wins where they overlap. A short clip dropped inside a long one plays: long part, short clip, rest of long.
- Same start and same length: the one moved last sounds, the other is silent.
- **Crossfade audio**: overlap two audio clips, select the later one, press **X** (or right-click > Crossfade). X again removes it. Drag the zone edges to resize (this resizes the clips). Drag the curve sideways for symmetry.

## 6. Join, merge, bounce
| Function | What it does |
|---|---|
| **Join Clips** (Cmd+J) | Same-lane clips become one. Gaps stay empty. DANGER: masked events between or under the joined clips are permanently deleted. The top clip wins in overlaps |
| Join OVERLAPPING audio | Nothing lost. Clips go on separate Comp Rows and are auto-comped. Fades in overlaps are removed. Clip Level resets to 0 dB, the old levels move to Comp Row levels |
| Join CROSSFADED audio | The crossfade zone is bounced to a new Comp Row. Result becomes stereo (two identical channels) even if the clips were mono |
| Muted clips | Cannot be joined |
| **Merge Note Lanes on Tracks** (Cmd+R, KC) | All lanes on the track collapse onto the TOP lane. Muted lanes/clips are left out. Works on several tracks at once |
| **Bounce in Place** (Edit or right-click; audio clips: Bounce > Bounce in Place) | Renders a clip to audio on a NEW audio track, with insert FX and channel strip, WITHOUT sends or the Master Section. Same position and length. Source clip is muted automatically. New track copies mixer settings and Output Bus routing |
- Bounce in Place jobs the manual lists: make audio from notes to chop or reverse (reverb tail played backwards), print effects, make samples for a sampler or a REX loop (Bounce > Bounce Clip(s) to New Sample(s) / to REX Loop in `audio-editing.md`).
- Bounce details: tail limit = 5 seconds after the last note-off or clip end. The tail may be hidden: drag the new clip's edge out to show it. Long notes that run past the clip edge are rendered fully (also hidden). Fully masked notes are not rendered. Source parameter automation IS included. Mono audio comes out stereo (post-pan).
- Several clips: same source track = same new track; different tracks = separate new tracks. Instrument split across several Mix Channels = one audio track per Mix Channel.
- Bounce in Place is DISABLED when the device does not have its own Mix Channel (e.g. it goes through a shared Mixer 14:2). Whole tracks: use Bounce Mixer Channels instead (`audio-editing.md`, `recording.md`).

## 7. Clean-up tools
| Tool | What it does |
|---|---|
| **Match Values** (button beside Position / Length / Fade / Level / Transpose in the Inspector) | Copies the TOP (or leftmost) selected clip's value to all selected. Position match stacks clips on the same start, so same-lane clips will overlap |
| Clip Fade handles / Level handle | Selected audio clip: drag top corners for fades, drag the middle handle up/down for level. Non-destructive. Obeys Snap |
| Add Labels to Clips | Names a clip. Double-click the label to rename. Remove Labels from Clips clears them |
| Clip Color | Default is Track Color. Override per clip. Colour-code Verse/Hook visually |
| Scale tempo by dragging | Arrow tool, hold **Option** over a clip resize handle, drag. Contents stretch with the clip (notes, automation, audio). Pattern clips only resize; the device pattern speed does NOT change. Numeric version = Scale Tempo in the Tool Window |
| Reverse clips | Edit > Reverse (note/automation: see `note-and-automation-editing.md`; audio: `audio-editing.md`) |

## 8. Insert or remove whole bars (song-level edits)
1. Set the Left and Right Locators round the gap (loop locators do this job here).
2. **Edit > Insert Bars Between Locators**: clips crossing the left locator are split. The part after the left locator is moved to start at the Right Locator. Result: empty bars between them for a new bridge or longer intro.
3. **Edit > Remove Bars Between Locators**: that range is cut out and the rest slides left. Notes and automation inside it are DELETED. Audio inside is NOT deleted: it is masked and moved forward on a Comp Row, still reachable in the Comp Editor.
- Affects ALL tracks and lanes at once. **[Guess]** do a Save As first when removing many bars. Undo is there too.

## 9. Ideas for us (**Guess**, not tried)
- Build a 64-bar skeleton: Razor in the Ruler at section boundaries, then colour clips per section.
- Make a drop: copy a verse, Insert Bars before the hook, paste.
- Print a finished synth part with Bounce in Place (source clip is muted for you). **[Guess]** this is the closest thing to "freezing"; the manual does not use that word and does not say it saves CPU.
