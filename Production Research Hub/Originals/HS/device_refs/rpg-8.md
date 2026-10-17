# RPG-8 Arpeggiator

Turns held notes/chords into arpeggios and sends them to an instrument via CV
(monophonic — one voice). Makes no sound itself. Has a 16-step rest pattern.
Source: Reason 12.7 Operation Manual, ch. 65, pp. 1343–1358.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Arpeggiator Enable**: on/off (off = plain MIDI-to-CV converter).
- **Mode**: Up, Up+Down, Down, Random, Manual (order you played).
- **Octave 1** / **Octave 2** / **Octave 3** / **Octave 4**: range of the arpeggio.
- **Insert Off** / **Insert Low** / **Insert High** / **Insert 3-1** / **Insert 4-2**: repeat-note variations.
- **Rate** / **Sync**: note value (1/2–1/128, dotted, triplet) or free 0.1–250 Hz.
- **Gate Length**: note length; full = "Tie" (legato).
- **Shuffle**: swing, amount set by ReGroove's global shuffle.
- **Single Note Repeat**: whether a single held note re-triggers.
- **Hold**: keeps arpeggiating after you let go (follows sustain pedal).
- **Octave Shift Up** / **Octave Shift Down**: ±3 octaves.
- **Velocity/Manual** / **Manual Velocity**: fixed velocity, or pass through what you played.
- **Pattern Enable** / **Pattern Length Up** / **Pattern Length Down**: 16-step rest pattern (rests don't skip notes).

## Handy
- Edit > "Arpeggio Notes to Track" renders the arp to real, editable notes on the instrument's track (then mute the Arp track).
- Recording on the Arp track records the chords you played, not the arp notes.

## Where it shines / falls short
Shines: instant arps and rhythmic riffs. Falls short: mono only — one arp voice per RPG-8.
