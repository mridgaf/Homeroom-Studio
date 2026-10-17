# Players: chords and arpeggios from single notes (digest of Reason 12.7 manual, ch. 12)

Source: `~/.reason_voice/reason12_manual/full_chapters/12-working-with-players.txt` (manual pp. 343-372). Digested 2026-09-30.
Tag: all **Manual**. Nothing tried or heard. Overlap check: your notes have 0 files on Scales & Chords or Note Echo; Dual Arpeggio appears only inside song notes. Index: [README](README.md)

## What a Player is
A device that sits above an Instrument in the rack and turns the MIDI going in into different MIDI going out (chords, arpeggios, echoes, drum patterns).
It cannot exist alone; creating one with no instrument makes an ID8. Works with any instrument (built-in, Rack Extension, VST).

## Create / order / manage
- Rack: drag from the Players palette (under Utilities in the Browser) above an Instrument; or select the instrument and double-click the Player; or right-click the instrument > Create > Players.
- **Chained Players run top to bottom.** Reorder by dragging. Rename, replace and delete like any device. Players can live inside Combinators, or attach to a Combinator from outside.

## Common buttons (top of the Player stack)
| Button | Does |
|---|---|
| **Fold** | Folds all Players on that instrument |
| **Bypass All** | Sends your keyboard straight to the instrument |
| **Direct Record** | Records the notes the Players MAKE (chords, arps) instead of the notes you play. On playback they bypass the Players, so it sounds the same as when you recorded |
| **Send to Track** | Renders the Player output of the notes already in the clip into a NEW clip on a new lane. Originals between the locators are muted and cut. Bypass All turns on |
Default recording (Direct Record off): you record your own notes and the Player processes them live on playback.

## The Players in this chapter
### Scales & Chords
- **Scales section:** Key (12) and Scale. Presets: Major, Minor, Lydian, Mixolydian, Spanish, Dorian, Phrygian, Harmonic Minor, Melodic Minor, Major Pentatonic, Minor Pentatonic, Hemi Pentatonic, Chromatic, plus **Custom** (click the keys; saved with the song and the patch). Key and scale can be automated.
- **Filter Notes** off (default): wrong notes are moved to the nearest scale note (the lower one if tied). On: wrong notes go silent.
- **Chords** on: one note makes a chord in the scale. **Notes** knob = 1 to 5 notes. Playing several notes makes several chords (shared notes play once).
- **Inversion** knob (only useful below the Notes value), **Open Chords** (spreads notes by octaves), **Add Oct Up / Oct Down / Color** (Color adds the 9th for 3 notes, 11th for 4, 13th for 5; all three can be on), **Alter** (momentary: turns one chord note so a major goes minor or the reverse).
- Use it to write single notes in a clip and let the Player build the chords.
### Note Echo (a MIDI delay)
- **Step Length** 0 to 1000 ms (synced: 1/128 up to 1/2). **Step Length 0 = all repeats at once = chords.**
- **Repeats** 1 to 16, **Velocity** 10% to 200% per step, **Pitch** -12 to +12 semitones per step. Click the green circles in the display to mute repeats (also the dry first note).
- Too many repeats with a big Pitch value can leave the instrument's range: the rest go silent.
- Comes with ready-made chord patches: Browse Patch > **Chords** folder.
### Dual Arpeggio
- Two identical arpeggiator sections with Rate, Octave, Direction, Steps, Pattern, Velocity and Gate Length. (Details in the chapter, manual pp. 350-360; the shuffle comes from ReGroove Global Shuffle.) The CV inputs can take a Pulsar for random or long patterns.
### Beat Map (Rack Extension)
- A Player that makes drum patterns from built-in beats and algorithms; made for Kong, Rytmik or Umpf. **Not checked whether you own it.**

## Recipes from the manual (Tips & Tricks)
1. **Scale-correct arpeggio from one note:** instrument > Scales & Chords first > Dual Arpeggio second. Key and Scale set, Chords on, Notes = 4. Play single notes.
2. **Arpeggiated chords:** instrument > Dual Arpeggio first > Scales & Chords second. Chords on, Notes = 3. Play chords.
3. **Parallel chords (same shape on every note, like a minor 9th):** Note Echo: Step Length 0, Repeats max, Pitch +1, then click off the repeats you don't want. Play single notes. Add a Dual Arpeggio after it for arps.
4. **See what the chain is playing:** put a Scales & Chords LAST, Scale = Chromatic, Filter Notes and Chords off. The keyboard display shows the notes.

## Ideas for us (not built)
- Skill idea **reason-players**. Phrases: "make that a four-note chord", "arp it", "put it in D minor".
- Pairs with the chord work in the Beat Machine (`CLAUDE.md`: MIDI chord packs, chord sources). Whether Reason Players could audition chord progressions from the Beat Machine MIDI was NOT checked.
