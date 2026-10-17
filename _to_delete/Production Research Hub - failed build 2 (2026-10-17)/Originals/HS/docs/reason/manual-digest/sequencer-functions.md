# Sequencer Functions: tracks, lanes, tools, snap, transport
Source: Reason 12.7 Operation Manual, ch. 5 (whole chapter read, ends p. 134). Tag: **Manual**.
Recording is in `recording.md`. Clip moving/cutting is in `arranging.md`. Note/automation tools are in `note-and-automation-editing.md`. Audio is in `audio-editing.md`. Sections (Blocks) are in `blocks.md`.
Shortcuts marked (KC) are from the Key Commands chapter (`key-commands.md`), not ch. 5.

## 1. The nesting (one picture)
Track > Lane > Clip > Events (notes, audio, automation points). A clip is just a container. A lane plays ONE clip at a time.
- A device has at most ONE track. A track must have a device (except Transport and Blocks tracks).
- Track order is NOT rack order and NOT mixer order. Fix with Edit > **Sort Selected Device Groups** (see `rack.md`).

## 2. Track types: which one for which job
| Track | Lanes it can have | Use it for |
|---|---|---|
| Transport (always on top, cannot move or delete) | max 2: Time Signature, Tempo | Tempo and meter changes (steps in `recording.md` sec. 7) |
| Blocks (only if Options > Enable Blocks) | Block automation clips | Song sections (`blocks.md`) |
| Audio | ONE audio lane + mixer automation lanes | Vocals, loops, bounced audio. Many takes can sit inside one clip |
| Instrument (any device that takes notes) | MANY note lanes + automation lanes | Notes AND the instrument's knobs. Made automatically with the device |
| Automation ("non-instrument") | Automation lanes only, one per knob | Effects, Mix Channels, mixers, Spider. NOT made automatically |
| MIDI Out Device | Note lanes + CC automation | Playing outside gear. No audio inside Reason |
- Instrument created = track + Mix Channel made, but the Mix Channel gets NO track. To automate its fader or pan, make one.
- Make a track for an effect or Mix Channel: select it, then Edit > **Create Track for...**; or Option-click any knob on it; or Option-hold while creating an effect; or **Shift-click the SEQ button** under a mixer strip.
- New audio track: **Cmd+T**. Mono by default; pick Stereo Input in the track's Audio Input list and the mixer strip becomes stereo.
- New instrument with patch browser: **Cmd+I**.

## 3. Lanes: the real song-building trick
| Lane | Why add one |
|---|---|
| Note lane (Edit > New Note Lane, or Lanes + button) | Overdub without touching existing clips. Keep several takes side by side. Different groove (ReGroove) per drum or part. One lane per drum on a drum track |
| **Dub** / **Alt** (Transport) | Both make a new record-ready note lane on the fly. Alt also MUTES the previous lane (or just the clips between loop locators). Keys (KC): Dub **,**  Alt **.** |
| Automation lane | One per knob. Auto-made when you move a knob while recording, or Option-click a knob, or pick from the Track Parameter Automation list. Knob gets a green border |
| Pattern lane (Redrum, Matrix) | One per track. Holds bank + pattern changes only |
- Note lanes CAN be dragged to a new spot or onto another track. **Option-drag** copies a lane with its clips.
- Automation and pattern lanes CANNOT be moved or copied (but clips can move between lanes).
- Muting an automation lane FREEZES the knob at whatever value it had. Un-mute to get the automation back.
- Delete a lane = its clips go too. **Cmd+click** the X to skip the warning. Deleting an AUDIO track deletes its recordings (Undo is your safety net).
- Lane names (note lanes) can be renamed by double-click; they only show if you zoom vertically enough.

## 4. Track handling (speed list)
| Do | How |
|---|---|
| Select next/previous track | Up/Down arrows. Selecting a track also sets Master Keyboard Input (unless Preferences > MIDI is "Separated") |
| Reveal the device in the rack | Double-click the track's device icon |
| Resize height | Drag the track's bottom edge. Several selected = proportional. **Option** = all same height. -/+ Track Height buttons for all. Folded tracks can't resize |
| Fold / unfold | Triangle on the track handle. **Option-click** = all tracks. Folded tracks still allow select/move/copy of clips |
| Move a track | Drag its handle (red line shows the drop spot) |
| Duplicate track + device + clips | **Cmd+D**, or Option-drag the handle. Auto-group ON copies the whole device group. Auto-group OFF = unconnected copy: use Edit > Auto-route Device, or **Shift+Paste** |
| Copy a plain audio track with its effects | Use **Dub** or **Alt** (`recording.md` sec. 4) |
| Colour | Edit > Track Color. Mixer strip and rack device take the same colour. Options > Auto-color New Sequencer Tracks for automatic |
| Rename | Double-click the name. Also renames the device (and Mix Channel, unless you rename that on its own) |
| Mute / Solo track | M / S buttons. Master M and S at top clear them all. These are NOT the mixer's Mute/Solo |
| Delete | Delete key = track + device (alert). Edit > Delete Track(s) = track only, no alert. Cmd while deleting = whole group, no alert |

## 5. Toolbar tools (keys work in Song and Edit view)
| Key | Tool | Job |
|---|---|---|
| **Q** | Selection (arrow) | Select, move, resize. Default |
| **W** | Pencil | Draw clips and notes. Edits velocity |
| **E** | Eraser | Delete clips/notes. Drag a box to delete many |
| **R** | Razor | Split clips and notes. Also makes cuts when comping audio |
| **T** | Mute | Click clips to mute them (lanes inside Block clips too) |
| **Y** | Magnifier | Click = zoom in. Option+click = out. Drag a box to zoom to it |
| **U** | Hand | Drag to scroll |
- **Hold Cmd (Mac) [Alt on Windows]** = temporary swap to the "alternate" tool. Arrow <-> Pencil. Eraser -> Pencil. Razor -> Pencil. Mute -> Razor. Magnifier <-> Hand. In an open audio clip, Arrow becomes Speaker (listen to a slice) or Razor (comp cut).
- Zoom keys (KC): **H** in, **G** out, **Z** zoom to selection (horizontal), **Shift+Z** both ways. **F** = Follow Song.

## 6. Snap (the grid)
- **S** turns Snap on/off. Pick the note value in the drop-down. Choose **Relative** (moves in steps from where the clip was) or **Absolute** (lands on the nearest grid line).
- Snap affects: moving, drawing, splitting, nudging, comp cuts, slice markers, the playhead and locators, and the shortest note you can draw. Locators ALWAYS snap absolute.
- **Grid** value = changes by itself with zoom (Bar down to 1/128).
- TWO separate Snap settings: one for arranging (Song/Block view), one for editing an open clip. Manual tip: Bar for arranging, 1/16 for editing. Each can be turned off separately.
- Nudge clips (KC/ch.7): **Cmd+Left/Right** = one Snap step, works even with Snap off. Add Option = 1 tick, Shift = 1 beat.

## 7. Ruler, locators, loop, transport
| Do | Keys / how |
|---|---|
| Set Left Locator | **Option+click** the ruler [Ctrl+click on Windows] |
| Set Right Locator | **Cmd+click** the ruler [Alt+click on Windows] |
| Set Song End Marker | **Shift+click** the ruler |
| Loop = exactly the selected clips | **Cmd+L**. Same + start playing in loop: **P** |
| Loop on/off | **L** |
| Play / stop | **Space**. Stop = **Shift+Return** (also numpad 0) |
| Record | **Cmd+Return** |
| Click on/off | **C**. Pre-count on/off: **Cmd+P** |
| Go to loop start/end (KC) | **Option+Left/Right** (numpad 1 / 2) |
- Drag the FLAGS in the ruler, not the lines. Or type numbers into the position boxes.
- Loop rules: start playing left of the right locator = it loops. Start to the RIGHT of it = loop ignored, plays on. Locators in reversed order = plays to R, jumps to L, and skips what is between, then plays on un-looped.
- **Stop twice** = go to song start (first press goes back to where you started playing). Preferences > General > "Return to last start position on stop" changes that.
- Numpad keys (rewind 4, forward 5, +/- tempo, bar back/forward 7/8) need a number pad. A MacBook has none. **[Guess]** an external number pad or the on-screen buttons are the fix.
- Song End Marker (E) marks where the song ends (Shift+click the ruler to place it). **[Guess]** it controls where an export stops, so keep it a bar past the last note so tails survive.

## 8. Tempo and meter
- Tempo range 1.000 to 999.999 BPM. **Tap** button: averages 2 to 16 taps, resets after 2 seconds of silence, detects 30 to 999.999 BPM.
- Signatures from 1/2 up to 16/16 (1/2-16/2, 1/4-16/4, 1/8-16/8, 1/16-16/16).
- Resolution: 240 ticks per 16th note (960 per quarter) when editing. A `*` in the tick box = a sub-tick position from live recording. **Cmd+click the `*`** snaps it to the nearest tick.
- **Q Record** quantizes notes as you play (value from the Quantize drop-down). **Quantize** button fixes selected clips afterwards.

## 9. Inspector and Match Values
- The Inspector (above the arrange area) shows Position and Length of the selected clip, and for audio clips also Fade In, Fade Out, Level and Transpose. It hides while the Pencil is active.
- **Match Values** buttons next to each box copy the TOP (or leftmost) selected clip's value to all selected. Details in `arranging.md`.

## Not in this chapter
Chase / playback settings, freeze, and consolidate do not appear in ch. 5 or ch. 7. Bounce functions are in `arranging.md` (Bounce in Place) and `audio-editing.md` (Bounce Mixer Channels, bounce to sample). **[Guess]** Reason has no "freeze" command; Bounce in Place plus muting the source clip is the nearest thing described.
Zooming/scrolling/navigator sections are referenced but not included in this extract of ch. 5. Zoom keys above come from the Key Commands chapter.
