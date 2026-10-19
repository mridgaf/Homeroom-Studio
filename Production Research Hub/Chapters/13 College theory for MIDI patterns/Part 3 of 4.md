# Chapter 13: College theory for MIDI patterns
## Part 3 of 4

_Drum grooves, syncopation, swing, tempo, and phrase length, as step grids._

**In this part:** drum patterns written as 16-step bars, tresillo and syncopation recipes, swing, tempo ranges, phrase length.
**Previous:** Part 2 of 4.md  **Next:** Part 4 of 4.md (emotion map and checklist)

Sources: Open Music Theory (OMT) Pop unit and Jazz unit; Berklee College article (Alexander, 2022) where marked.
**How to read the grid:** one bar of 4/4 = 16 steps, numbered 0–15. Beat 1 = step 0, beat 2 = step 4, beat 3 = step 8, beat 4 = step 12. Odd steps are the "e" and "a" 16ths. Step 2 = the "and" of beat 1.
**Drum note numbers** below are General MIDI standard (kick 36, snare 38, clap 39, closed hat 42, open hat 46, ride 51, crash 49). They are NOT from the college sources; they are the standard drum map, channel 10.

## 1. The backbeat is the anchor (OMT)
- Most pop and hip-hop in 4/4 has a **backbeat**: the snare (or a clap/snap) on beats 2 and 4 = steps 4 and 12.
- In the basic beat the snare is the most stable layer. Change the kick and the cymbals first. Keep the backbeat to stay recognisable.
- The backbeat can be a clap or snap instead of a snare. Layering several backbeat sounds is normal in hip-hop and electronic music.
- The "boom-bap" beat is this same kick/snare alternation.

## 2. Pattern library (steps in a 16-step bar)
| Name | Kick (36) | Snare/clap (38/39) | Hats (42) | Source note |
|---|---|---|---|---|
| Basic rock / boom-bap | 0, 8 | 4, 12 | every 8th: 0,2,4,6,8,10,12,14 | OMT: kick on 1 and 3, backbeat on 2 and 4, 8th hats |
| 16th hats | 0, 8 | 4, 12 | every step 0–15 | OMT: 8th or 16th hats are the common choices |
| Four on the floor | 0, 4, 8, 12 | 4, 12 (or none) | off-beats 2,6,10,14 | OMT: Blondie "Heart of Glass" uses off-beat hats |
| Half-time | 0 (plus syncopated extras) | 8 only | 8th or 16th | OMT: snare only on beat 3 |
| Double-time | 0, 8 | 2, 6, 10, 14 | 16ths | OMT: backbeat on the 2nd 8th of every beat |
| Dembow | NOT USED | NOT USED | n/a | OMT says kick on all 4 beats and snare on the last two hits of a tresillo. Exact steps are unconfirmed (sources conflict), so no grid is given and the generator skips it. |
| Simple 3/4 | 0 (+ tresillo kicks) | beat 3 | 8th | OMT: in triple meter the snare waits for beat 3 |
| Compound 4 (12/8 feel) | beats 1 and 3 | beats 2 and 4 | the 3-part beat division | OMT, e.g. "If You Don't Know Me by Now" |

### Kick rules
- OMT: **syncopation lives more in the kick than in the snare.** Kendrick Lamar's "HUMBLE." has a steady clap backbeat and a very syncopated kick.
- But the kick **still lands on the downbeat of each bar** (OMT on HUMBLE.). Berklee agrees: kick patterns "move playfully but usually commit to a solid hit on the first beat of a one- or two-bar phrase."
- A hat pattern with slightly "lazy swing" gives the movement (Berklee). No swing amount is given in the sources, so none is invented here.

### Feel names (OMT)
- **Normal feel:** tempo 80–160 BPM. The kick/snare spacing is the pulse you tap.
- **Half-time / double-time:** the drums run at half or twice the speed of the pulse you feel. Same tempo, different weight.
- Southern hip-hop often reads as 80 or 160 BPM at once. (Berklee)
- **Cymbal roles:** hi-hat usually keeps the pulse; ride is the common alternative; crash is for slow or aggressive grooves. (OMT)

## 3. Tempo ranges (Berklee, Alexander 2022)
| Style | BPM |
|---|---|
| Old-school East Coast | 100–120 |
| Early West Coast | 90–100, later 90–120 |
| Southern | 80 or 160 (both readings are valid) |
These are descriptions of history, not rules. Use them as starting points.

## 4. Syncopation recipes (OMT)
**Straight syncopation.** Take equal notes. Cut the first one in half. Shift every later note **early by that half**.
- Beat level (four quarter notes): note 1 is an 8th on step 0, then notes land on **steps 2, 6, 10**, each a quarter long. All on off-beats.
- 16th level (four 8th notes): same idea, one 16th earlier.
- To hear it as syncopation, nothing falls on the counting beats for a few notes.

**Tresillo (3+3+2).** Split 8 sixteenths into 3+3+2. Hits on steps **0, 3, 6** (of each 2-beat cell). Other orders also work: 3+2+3 = steps 0, 3, 5; 2+3+3 = steps 0, 2, 5. It is "a fake triplet." OMT says it is **more common than real triplets** in pop.
- **Double tresillo:** 3+3+3+3+2+2 across 16 sixteenths = hits on steps 0, 3, 6, 9, 12, 14 (U2 "Electric Co.").
- Do not mix up tresillo (3+3+2) with real triplets (3 even hits per beat). Choose one on purpose.

**Chord rhythm on a loop.** In "Sultans of Swing" (lament loop) the two middle chords are syncopated and shorter, to leave room for a seventh at the end that turns the loop around. So a loop's chords do not need equal lengths.

## 5. Swing (OMT Jazz)
- Swing eighths: the first 8th is about **twice as long** as the second (2:1, like a triplet).
- **Faster tempo = straighter. Slower tempo = more swing.** The ratio varies by player and tune.
- Standard swing drums: ride on the swung 8ths, hi-hat closes on beats 2 and 4.
- Chord changes land on **beat 1** (sometimes beat 3). Changing chords on beat 2 or 4 is unusual.
- Swing in MIDI: for a 480-ticks-per-beat file, a straight off-beat 8th sits at tick 240; a 2:1 swung one sits at 320. (This conversion is arithmetic, not from the sources.)

## 6. Phrase length (OMT Rhythm unit)
- Bars group in **twos and fours** (4-bar and 8-bar phrases). Groups of three bars are possible but rare.
- People stop feeling meter when a pulse is too short (about a tenth of a second) or too long (a few seconds).
- Practical rule: **loop length 4 bars, section length 8 or 16 bars**, and use a 3-bar group only as a deliberate surprise.

## 7. Song shape (OMT Form, pop)
- Verse–chorus form: verses change their words; choruses repeat words and music. Choruses are where loops usually stay put.
- Bridges "emphasize non-tonic harmonies and commonly end on the dominant."
- Prechorus: often V or IV chords that **withhold the tonic** to build energy (OMT "Let It Go" analysis).

=== END OF PART ===
