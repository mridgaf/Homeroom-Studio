# Note and Automation Editing — the Tool Window toolbox
Source: Reason 12.7 Operation Manual, ch. 9 (read: Tool Window functions, velocity, reverse, multi-lane, automation editing, cleanup, pattern/tempo; Edit Mode layout skimmed, not digested). Tag: **Manual**.
Open the Tool Window with **F8** › "Sequencer Tools" tab. Option-click a fold arrow to fold/unfold all panes.
**Scope rule for every tool below:** it works on (a) selected notes in an open clip (Edit Mode), (b) all notes in selected clips, or (c) all notes in all clips on selected tracks (Song/Block view only).

## Toolbox (what each tool does and when to use it)
| Tool | What it does | Use it for |
|---|---|---|
| **Quantize** (Value, Amount %, Random) | Snaps note starts (and audio slices in Slice Edit) to a grid. Amount 100% = fully on grid, 50% = half-way. "T" values = triplets | Tighten a sloppy part but keep some feel at 50–75% |
| Quantize Random | Quantizes, then randomly offsets by ±N ticks | "Humanize" after a hard snap |
| Quantize to **Shuffle** | Moves to 16ths with every even 16th delayed; amount = ReGroove Global Shuffle | Match pattern devices (Redrum etc.) that have Shuffle on |
| **Q Rec** (Transport button) | Quantizes notes while you play. Audio cannot be quantized while recording | Live drum entry |
| **Pitch** (Transpose / Randomize) | Transposes notes by semitones. Randomize = random notes inside a range. Audio: non-destructive | Move a loop to a new key. Mixed note+audio selection in one go |
| **Note Lengths** (Add / Sub / Fixed) | Adds, subtracts or sets note length | Staccato everything (Fixed short), or lengthen pads |
| **Legato Adjustments** (Abut / Overlap / Gap by) | Stretches each note to touch/overlap the next, or opens a gap. Never moves starts | Smooth bass/lead lines, or tidy gaps |
| **Alter Notes** (Amount) | Randomly swaps positions among EXISTING note starts | Instant variations. Best on **Dr. Octo Rex slices**: rearranges the loop and keeps its feel |
| **Note Velocity** (Add / Fixed / Scale / Random) | Edits velocity (1–127) | See "velocity compress" below |
| **Extract Notes to Lanes** (Single Note / Note Range, Move or Duplicate) | Pulls chosen pitches into a new clip on a NEW lane | Split hats off a drum clip. Needed to give each drum its own ReGroove channel |
| **Explode** | One new lane per used pitch | Whole drum clip → one lane per drum in one click |
| **Scale Tempo** (Scale %, Double, Half, Scale to) | Compresses/stretches time of notes, automation, patterns and audio clips. Not time-signature automation | Half-time/double-time versions. Pick the audio Stretch type first |
| **Reverse** (graphical / musical) | Mirrors note and automation clips. Graphical = uses note lengths (note-offs become starts). Musical = only start positions mirrored | Reverse a riser or a fill. Audio clips reverse the actual sound |
| **Automation Cleanup** | Removes extra points. Also Preferences › General: Normal / Heavy / Maximum | Fix hundreds of points from a shaky knob move |
- **Velocity compress trick (manual):** Scale below 100 % + Add a positive value. Differences shrink, average stays. Scale above 100 % = more contrast between soft and hard notes.
- Edit velocity by hand on the Velocity Lane: Pencil click/drag; **Option(Mac)/Ctrl(Win) + Pencil = Line tool** for ramps or a flat level; **Shift** while drawing = only selected notes change (e.g. select hi-hats on the Drum lane, then shape only their velocity).
- Quantize only touches notes/slices. Automation events are untouched.

## Note Edit Modes
Auto-picked by the device: **Key** (piano roll, black/white key stripes), **Drum** (named lanes, Redrum/Kong), **REX** (Dr. Octo Rex slices). Switch with the Note Edit Mode button. Mixed selections may need Key mode to see the whole range.

## Multi Lanes editing
- Select several instrument tracks (or several note clips) and press Return / Edit. Turn **Multi Lanes** on.
- Selected lane's notes are red, others grey. Click a grey note to switch lane. Only the selected lane's notes move together.
- Useful with Extract/Move-to-New-Lane on drums.

## Moving, nudging
- Arrow keys nudge notes. Notes nudged outside an open clip become masked (still belong to the clip, not played).
- Razor tool splits notes. Moving notes between clips follows "outside the clip" rules (masking).

## Automation editing
- Automation clips = points joined by straight lines. Drag a line with the Arrow tool to make a CURVE. **Shift-click** a curve to straighten. Double-click a line to add a point. A flat line (same value) can't be curved.
- **Static Value** (the value outside clips) edits with the up/down buttons beside an open automation clip (Song view) or by double-click-typing.
- Double-click an automation clip to open it right in the Song/Block view. Esc closes. Extending a clip stretches first/last value to the edge, so a single Mute point can be moved/resized without opening it.
- Draw: Arrow double-click (hold and drag = series), Pencil click/drag, **Shift+Pencil click** = add a point on a line, **Option/Ctrl+Pencil** = a flat range (length = Snap value). Snap and Cleanup control point count.
- Stepped parameters (buttons, selectors, sustain) make steps, not ramps.
- Select all in clip = Cmd+A, then Delete.
- **Performance controllers** (mod wheel, pitch bend, aftertouch…) edit on lanes at the bottom of an open note clip. Add a lane with the Performance Controller Automation Selector. Any device panel knob can be added as a performance controller from the sub-menus.
- Tempo range displayed 60–250 BPM, real range 1–999.999 BPM. Double-click the 250 / 60 labels to widen. Time signature automation can only be drawn, not recorded.
- Audio Stretch types: **Allround** (chords/full mixes), **Melody** (one note at a time), **Vocal** (keeps formants, best for stretched/transposed voice). "Disable Stretch" on a clip to keep it out of tempo automation (dialogue, FX). Stretch has a quick preview then a background "Calc" high-quality pass.
- **Convert Pattern Automation to Notes** (Redrum/Matrix/Dr. Octo Rex): turns the pattern lane into a note lane, then turns the pattern lane off. Matrix: convert on the track of the device it plays, and consider disconnecting the Matrix afterwards or both will play.

## Ideas (**Guess**, untested here)
- Drum humanize: Explode → per-drum ReGroove channel → Quantize 75 % + Random 5 ticks.
- Dr. Octo Rex variation: duplicate the clip, Alter Notes at a low Amount.
