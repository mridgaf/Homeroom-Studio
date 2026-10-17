# Audio Editing in the Sequencer (digest of Reason 12.7 manual, ch. 8)

Source: `~/.reason_voice/reason12_manual/full_chapters/08-audio-editing-in-the-sequencer.txt` (manual pp. 203-254). Digested 2026-09-30.
Tag: all **Manual**. Nothing here was tried or heard. Index: [README](README.md)
Overlap check: your notes mention Slice Edit only for Dr. Octo Rex slices (`device_refs/dr-octo-rex.md`) and Pitch Edit in one line
(`device_refs/neptune.md`). The audio-clip tools below are not written up anywhere else.

## The 3 ways to edit an audio clip (double-click the clip, or select it and press Return)
| Mode | For | Opens by default when the clip is |
|---|---|---|
| **Slice Edit** | Fix timing: move/stretch the detected hits (slices). Quantize audio. Turn it into a REX loop | Single Take with **Allround** or **Melody** stretch type |
| **Pitch Edit** | Fix or change the pitch of single-voice audio (vocals) | Single Take with **Vocal** stretch type |
| **Comp Edit** | Pick the best parts of several takes and join them | A **Comp** clip (made from several takes) |
Buttons for all three are in the Toolbar. Close an open clip with **Esc**. Cmd+E opens it in its default mode.
**Order of work:** comp first, then slice or pitch edit. Doing slices first and comping after wastes the slice work.

## First, set the Stretch and Transpose Type (Edit menu or the clip's right-click menu)
| Type | Use for | Formants |
|---|---|---|
| **Allround** | Full mixes, chords, anything with several notes at once | Move with the pitch |
| **Melody** | One note at a time (bass, lead) | Move with the pitch |
| **Vocal** | Voice | Kept, so the voice keeps its character |
Wrong type = bad-sounding stretch. **Enable Stretch** must be ticked on the clip (right-click menu) or stretch and quantize do nothing.
Reason also stretches twice: a quick version you hear at once, then a high-quality version in the background (the **Calc** meter on the Transport shows progress).

## Slice Edit: fix the timing of a recording
- Reason finds the hits and draws white **Slice Markers**. Drag a marker to move that hit; the audio each side stretches. Pitch does not change.
- **Speaker tool** (or hold Cmd with the Arrow tool): click a slice to hear it alone. It bypasses the mixer.
- Several markers at once: select them, drag the **Slice Group Handle**. A selected range stretches "accordion style" if you drag a marker inside it.
- Nudge with Cmd+Left/Right (snap step), +Shift (beat), +Option (tick). Turn Snap off (**S**) for fine moves. You can't drag a marker past its neighbour.
- **Quantize audio**: select markers, set Value (Amount, Random) in the Tool Window or Transport, Apply. Choosing **Shuffle** uses the ReGroove Global Shuffle value.
  Only the markers nearest the grid move; two markers never land on the same spot. Audio can be quantized only after recording, not while recording.
- **Split at Slices**: cuts the clip into separate clips at the chosen markers (to reverse one hit, or bounce each to a sample).
- **Revert All Slices**: puts every marker back.
- **Bounce Clip to REX Loop**: set markers where you want slices, trim the clip to a whole beat, then Edit > Bounce > Bounce Clip to REX Loop.
  The REX file lands in Song Samples > All Self-contained Samples. Double-click it to open it in a new Dr. Octo Rex. It exports as `.rx2`.
  To use it in another sampler, un-self-contain the song first.

## Pitch Edit: vocal tuning (opens a clip as "Vocal" type automatically)
| Move | How |
|---|---|
| Snap every note to the nearest exact pitch | Select notes (or none = all), click **Pitch Correct**, or Shift+Cmd+C. **Reset** undoes it |
| Change a note's pitch | Drag it up or down. Transpose switch: **Snap** (absolute semitones), **Jump** (default, keeps your fine tuning), **Fine** (cents). Shift+Cmd while dragging = fine |
| Hear the note while dragging | **Monitor** button (a steady reference tone) |
| Straighten wobble or vibrato | Lower the note's **Drift** handle (100% = untouched, 0% = no drift). **Preserve Expression** keeps small natural movements |
| Smooth the jump between two notes | **Transition** handle. Only matters after you've changed pitches. Max 200 ms, or half the note if it is under 400 ms |
| Change tone without changing pitch | **Formant** in the Inspector: -1 to +1 octave in 0.01 semitone steps. Down = deeper, up = brighter |
| Per-note level | Note Level handle, or Inspector: -inf to +18 dB |
| Move a note's timing | Drag its handle in the Clip Overview (neighbours stretch). Option-drag a note line to move the start WITHOUT moving the audio |
| Split / join notes | **Razor** splits, **Eraser** joins (the notes are re-analyzed) |
| Everything numeric | Inspector: Position, Note, Fine-tune (1 cent steps), Drift, Preserve, Transition, Formant, Level. **Match Value (=)** copies one note's setting to the others |
| Undo everything | **Revert All Notes** re-analyzes the clip from scratch |
Quantize in Pitch Edit moves note STARTS, not drum-style hits. Related device: Neptune (`device_refs/neptune.md`).

## Comp Edit: make one perfect take from many
- Every take recorded in Loop Mode (or recorded over an existing clip) is a **Comp Row**: newest on top. Only one plays at a time unless you comp.
- If a **Single Take Mode** button is down, click it to deselect before adding cuts.
- **Razor tool**: click a Comp Row = cut there and use that row from that point on; click the **Silence Row** = silence from that point (cut breaths and noise);
  click the **Cut Row** = cut without changing the take. **Swipe** the Razor along a row to assign a whole segment. Hold Option while clicking to first duplicate the row.
- Change which take plays in a segment: double-click that row between the cut lines. Or Cmd+Up/Down; Cmd+Option+Shift+Left/Right moves segment focus.
- **Crossfades** at cuts: select the cut and drag its Crossfade Handle right (all the way left removes it). Match Value copies one crossfade to every cut.
- **Move a cut**: drag its handle (the recording stays put, only the mask moves). Two cuts can't share a spot.
- **Fix a take's timing**: select the row, drag it, or type the **Recording Offset** (240 ticks per 16th, 16 subticks per tick). Nudge with Cmd+arrows.
- **Row Level** fader per take; **Transpose** per row in the Inspector.
- **Bounce** button: joins the comp into one new recording (marked "(bounced)"), and the clip becomes Single Take. Needed before Slice Edit or stretch.
- **Delete Unused Recordings** shrinks the file, but it is permanent. Then File > **Save and Optimize** to actually shrink the song file.

## Functions that work on any audio clip
| Function | What it does |
|---|---|
| **Normalize Clips** | Makes a new top row "(normalized)" with the peak at 0 dB. Originals kept. Boosts noise too |
| **Reverse** | New top row "(reversed)". Originals kept |
| **Transpose clip** | Up or down 12 semitones in 1-cent steps, non-destructive, Inspector. Works on chords too |
| **Scale Tempo** | Option-drag a clip's resize handle: the audio stretches to fit the new length. Slices follow |
| **Bounce > Bounce Clip(s) to New Sample(s)** | Makes Song Samples you can open in the Edit Sample window and load into a sampler (see [sampling](sampling.md)) |
| **Bounce > Bounce Clip to Disk** | Exports one clip as WAV/AIFF for outside editing |
| **Bounce > Bounce Audio Clips To MIDI** | Single Take audio becomes a note clip on a new Subtractor track. **Vocal** type gives real pitches. **Allround/Melody** gives all notes on C3 = a rhythm. Handy for **drums to MIDI** (then move the notes onto the right pads) |
| Drag a Single Take clip onto an Instrument track | Same MIDI conversion in one move (one instrument track per audio track, right below it) |

## Match an imported loop to the song tempo
- Files exported or bounced from Reason carry their tempo, so they stretch to fit by themselves.
- A loop with a steady but unknown tempo: (1) **Disable Stretch** on the clip, (2) change the song tempo until it matches the loop (use the click), (3) set the clip length to the loop,
  (4) **Bounce Clip to New Recording** (stores that tempo), (5) **Enable Stretch**, (6) set the song tempo back. Or just use Scale Tempo.

## Ideas for us (not built)
- Skill idea **reason-audio-editing** (or three small ones: slice, pitch, comp). Highest value for you: **drums to MIDI**, **audio to REX**, **vocal pitch edit**, **comping takes**.
- Pairs with [sampling](sampling.md) and `device_refs/dr-octo-rex.md`.
- Not checked: the Key Commands for Comp/Slice modes in [key-commands](key-commands.md) (covered there).
