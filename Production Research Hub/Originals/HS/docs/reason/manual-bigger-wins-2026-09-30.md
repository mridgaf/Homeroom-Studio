# Bigger wins found in the Reason 12.7 manual (2026-09-30)

How I looked: listed all 70 manual chapters, searched your skills, notes, recipes and device guides for each topic, and read
the chapters where you had nothing. Tag **Manual** = read in the Reason 12.7 manual. None of this has been tried in Reason
or heard. Nothing is built. Not looked at yet: Key Commands (ch 70), Delay Compensation (18), Sampling (21), Audio Editing (8).

Full digests now live in [manual-digest/](manual-digest/README.md). The ReGroove skill is drafted at `.claude/skills/reason-regroove/SKILL.md`.

## 1. Players: chords and arpeggios from single notes (ch 12)  -- NOTHING in your notes
You have 0 files on Scales & Chords or Note Echo. Dual Arpeggio only appears inside song notes, never as a how-to.

| Piece | What it does | Tag |
|---|---|---|
| **Scales & Chords** | Pick a Key (12) and Scale (13 presets + a custom one you click in). Turn on **Chords**: one played note makes a chord that fits the scale. Notes knob = 1 to 5 notes. Wrong notes snap to the nearest right note (or go silent with Filter Notes on). Key and scale can be automated, so a song can change key | Manual |
| Chord extras | Inversion knob, Open Chords (spreads the notes), Add Oct Up / Oct Down / Color (adds the 9th, 11th or 13th), Alter (momentary: turns a major chord minor and the reverse) | Manual |
| **Note Echo** | A MIDI delay. Parallel chords (a shape that stays the same on every note, like a minor 9th): Step Length 0, Repeats max, Pitch +1, then click off the repeats you don't want | Manual |
| **Chain order matters** | Scales & Chords above Dual Arpeggio = scale-correct arpeggio from a single note. Dual Arpeggio above Scales & Chords = arpeggiated chords. Top device runs first | Manual |
| **Direct Record** | Records the notes the Player makes, not the notes you played. **Send to Track** renders them into a new clip, so you can edit them | Manual |
| Monitor trick | Scales & Chords last in the chain, Scale = Chromatic, Chords and Filter Notes off: shows what the chain is playing | Manual |

Skill idea: **reason-players** (small). Not checked: whether you own Beat Map (a Rack Extension Player in the same chapter).

## 2. ReGroove: how to actually use it (ch 22)  -- your recipes say "use ReGroove" but never say how
Recipes `doechii-denial-is-a-river`, `jid-never-story-music-box` and `feels-warm-soulful` all rely on it. No file has the steps.

- Open it with the **Groove button** on the Transport Panel (32 channels, 4 banks A-D of 8). Manual
- Send a note lane to a channel with the **Select Groove pop-up** on the lane. Only note lanes work, not audio. Manual
- Each channel has **Shuffle**, **Slide** (push a lane ahead of or behind the beat), **Groove Amount** and a groove patch. Manual
- **Global Shuffle: 50% = straight, 66% = triplet swing.** It also swings Redrum, Matrix, RPG-8 and Dual Arpeggio. Manual
- Compare with and without: turn the channel's On button off. Manual
- **Anchor Point** starts the groove at a later bar (for a pickup or intro). A time-signature change restarts the groove. Manual

Skill idea: **reason-regroove** (small). It would make the three recipes above walkable by voice.

## 3. Blocks: build sections once, reuse them (ch 10)  -- 0 files
- 32 Blocks, each usually 4-8 bars (a verse, a chorus). Reuse them anywhere in the song. Manual
- Block View and Song View share the same tracks but keep separate clips. Manual
- Block Automation Clips place a Block in the song and can mute lanes for that one use, which gives variations. Manual
- New songs have Blocks on. A song saved without them needs Options > **Enable Blocks**. Manual
- Linear clips can sit on top of Block data to override a bar here and there. Manual

Skill idea: **reason-blocks** (small). Fits the "64-bar song map" idea in `demo-song-template-and-automation-ideas.md`.

## Not worth adding
Osmium shows up in the device list file but has no chapter in this manual, so nothing to write from.
