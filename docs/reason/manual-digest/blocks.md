# Blocks: build sections once, reuse them (digest of Reason 12.7 manual, ch. 10)

Source: `~/.reason_voice/reason12_manual/full_chapters/10-working-with-blocks-in-the-sequencer.txt` (manual pp. 311-326). Digested 2026-09-30.
Tag: all **Manual**. Nothing tried or heard. Overlap check: 0 files in your notes mention Blocks. Index: [README](README.md)

## In one line
A **Block** is a short multi-track section (a verse, a chorus, usually 4-8 bars) you record once and place anywhere in the song. Same idea as a
drum machine "pattern", but for whole tracks. 32 Blocks per song.

## Set up
1. **Options > Enable Blocks** (new songs and template songs already have it on; a song saved without it needs this).
2. A **Blocks Track** appears above the Transport Track with a **Block button** and a **Song button**. Shortcut to toggle the view: **B**.
3. Block View and Song View share the same Track List, but the CLIPS are separate. You can put Song clips on top of Block clips.

## Make a Block
1. Click the **Block** button (Block View). Pick Block 1 to 32 from the drop-down in the Track List.
2. Rename: double-click the Block name on the Blocks Track.
3. **Length** = drag the **End Marker** in the ruler. Length always counts from the start of the ruler. Loop locators don't change it. It loops at the End Marker while you work.
4. Record and edit clips on tracks exactly like normal. Anything to the right of the End Marker is ignored when the Block plays in the song.
5. Color: Block Color palette (Blocks Track right-click menu or Edit menu). Track and clip colors stay as they were.

## Place Blocks in the song
1. Click the **Song** button. Pick the **Pencil**. A **Block selector** appears in the Inspector: choose the Block.
2. Draw a **Block Automation Clip** on the Blocks Track (or double-click with the Arrow tool for one snap-length clip, then drag to lengthen).
3. The Block's content shows ghosted on the tracks.
- Longer than the Block: the Block repeats (thin lines mark the repeats). 8-bar Block in a 20-bar clip = repeats at bars 9 and 17, the last 4 bars cut off.
- Shorter than a full multiple: the rest is masked (muted).
- **Block Offset**: dragging the clip's LEFT edge makes it start partway into the Block. Pattern tracks (Redrum) stay in step.
- **Swap the Block** in an existing clip: little triangle on the clip > pick another Block.

## Build an intro from ONE Block (the manual's example)
Copy the Block Automation Clip twice, resize the last one longer, then use the **Mute tool** on lanes inside each clip.
Clip 1 (8 bars): Piano + Bass. Clip 2 (8 bars): + Drums. Clip 3 (16 bars): all but Piano. One 8-bar Block gives a 32-bar build.
Mutes last exactly as long as that clip, so each different mute pattern needs its own clip.

## Turn Blocks into normal clips
- One clip: select the Block Automation Clip > Edit menu or its right-click > **Convert Block Automation to Song Clips**. Only unmuted clips are converted; the Block stays.
- All at once: Track List right-click > **Convert Block Automation to Song Clips**. The Blocks Track is then muted automatically (click **M** to bring it back).
- Copy and paste clips between Block View and Song View also works.

## Add variations on top
**Song clips beat Block data.** A normal clip on the same lane silences the Block underneath it. Manual's tip: arrange Blocks first, then record short
Song clips (a fill, a pickup, a one-bar change) over the top.

## Ideas for us (not built)
- Skill idea **reason-blocks**. Fits "64-bar song map" in `../demo-song-template-and-automation-ideas.md` (Intro / verse / hook as Blocks).
- Voice phrases to consider: "switch to block view", "make block 2 eight bars". Not checked whether the remote map can reach any of this.
