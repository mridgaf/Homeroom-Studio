# What the Reason demo songs' MIDI shows (2026-10-21)

Source: File > Export MIDI File from 6 songs (Power, Quazmo, Street Phone,
Airplane, Song Starter Trap, Song Starter Soul Hop). MIDI files live in
`/Volumes/TBOTC 3/Demo Song MIDI 2026-10-21/`.

## How to get at the data
- `.rsndemo` (demos AND the Song Starter templates): body is scrambled. Only
  the info card (tempo, length, blurb) is plain text. Cannot be parsed.
- Plain `.reason` songs (his own): fully readable chunks — devices, patch
  paths, every knob name, ReGroove settings.
- Fast route for any demo: open read-only in Reason > File > Export MIDI File.
  ~30 s per song. Gives notes + CC automation, all on channel 1, one track
  per lane, track names kept.

## Findings (all measured from the MIDI)
1. **Stacking = fullness.** One part is played by several instruments at once,
   same notes:
   - Power: chord stab on Piano L + Piano R + Mal L + Mal R (4 instruments,
     100% same notes). Bass riff on Bass arp + Wub M + Rave M + Wub R (4).
   - Quazmo: Strings + Air Vox, same chords (100%).
   - L/R pairs = two copies panned for width.
   - Our engine does the opposite on purpose: `_split_chord_roles` hands
     each note to ONE instrument ("No note is ever handed to two roles").
2. **Whole band shares one rhythm.** Power: bass = piano stab rhythm (92%
   same notes/onsets). Street Phone: kick, bass, both organs all on the
   same 3-3-2 cell (beats 0, 0.75, 1.5). The bass hits WITH the kick
   (182 shared onsets).
3. **Wide voicings with a hole in the middle.** Power: E3 alone, then
   E5-G5-B5 (top note 83). Street Phone: octave-doubled pairs
   (A#3 C#4 A#4 C#5); pad as wide 10ths (A#3-C#5). Engine caps chords at
   50-79 (D3-G5) in `harmony.py` VOICE_LO/HI, close voicings.
4. **Few notes, lots of repeats.** Power piano: 7 different pitches in
   2 minutes. Loops of 2-4 chords.
5. **Movement comes from knobs, not notes.** Velocity is flat on most
   sequenced parts (one value). The life is in CC automation: Airplane mod
   wheel 2,507 events on one synth; Street Phone filter (CC74) 974 on the
   beat; Quazmo piano volume rides 2,286. Engine has no filter/knob
   movement on melodic parts.
6. **Two drum layers at two speeds.** Power: "Kong half" (half-time) and
   "Kong double" (double-time) run together; plus a sliced drum loop (REX)
   on top of programmed drums in Power, Airplane, Trap, Soul Hop.
7. **Human feel only where a person played.** Quazmo piano: 88% off-grid,
   velocity 16-113, sustain pedal. Everything else on grid. Trap starter
   drums: velocity 4-127 (ghost notes).
8. Note ranges: bass 36-53, chords 45-84, leads 65-96. Pads hold 2-8 beats,
   bass/stabs 0.13-0.25 beat.
