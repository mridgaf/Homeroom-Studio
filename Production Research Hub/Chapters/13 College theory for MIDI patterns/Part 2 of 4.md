# Chapter 13: College theory for MIDI patterns
## Part 2 of 4

_Chord loops, modes, and voice leading, with exact notes._

**In this part:** the chord-loop library, mode colour notes, voice-leading rules, worked MIDI examples.
**Previous:** Part 1 of 4.md  **Next:** Part 3 of 4.md (rhythm and drums)

Source for all of this part unless marked: Open Music Theory (OMT), Pop and Jazz units. Berklee voice-leading rules are marked [Berklee].
Numbers use **C major / C minor** and **MIDI note numbers where middle C = 60**.

## 1. The chord-loop library (called "schemas" in OMT)
A schema is a stock chord pattern. It can be changed a little and still be recognised. Loops can **start on any chord** in the cycle (OMT calls this rotation).

| Name | Roman numerals | In C | Notes from OMT |
|---|---|---|---|
| Doo-wop | I–vi–IV–V | C Am F G | ii can replace IV. Rotation: IV–V–I–vi |
| Singer/songwriter | vi–IV–I–V (or I–V–vi–IV) | Am F C G | Same chords as minor: i–VI–III–VII. **The tonic is ambiguous.** The melody decides it. |
| Hopscotch | IV–V–vi–I | F G Am C | Minor: VI–VII–i–III. Swap V for VII to push toward minor. Root motion: step, step, skip. |
| Plagal | IV–I | F C | "Plagal sigh": IV–iv–I (F, Fm, C) |
| Double plagal | ♭VII–IV–I | Bb F C | Mixolydian flavour |
| Extended plagal | ♭VI–♭III–♭VII–IV–I | Ab Eb Bb F C | Chain of falling fourths |
| Subtonic shuttle | I–♭VII (or i–♭VII) | C Bb | Major tonic = mixolydian. Minor tonic = aeolian. |
| Aeolian shuttle | i–♭VII–♭VI–♭VII | Cm Bb Ab Bb | Really a shuttle between i and ♭VI |
| Aeolian cadence | ♭VI–♭VII–i (or I) | Ab Bb Cm (C) | Goal-oriented, not a loop. Often ends on a major tonic (picardy third). |
| Lament | i–♭VII–♭VI–V | Cm Bb Ab G | Falling bass C–Bb–Ab–G. Minor v instead of V gives aeolian. |
| Circle of fifths | vi–ii–V–I or i–iv–♭VII–♭III | Cm Fm Bb Eb | Roots fall by a fifth |
| Puff | I–iii–IV | C Em F | Builds phrases, usually NOT looped. I–III♯–IV (C E F) is the common twist. |
| Dorian shuttle | i–IV | Cm F | Major IV on a minor tonic = dorian. Can sound like ii–V to new ears. |
| Lydian shuttle / cadence | I–II♯ / II♯–IV–I | C D / D F C | Rare. Check the melody has the raised 4th (F♯). |
| 12-bar blues | see section 5 | | All dominant sevenths |

### Rules you can code from this table
- A loop is usually **4 chords, 4 bars** (one chord a bar). Puff and cadence schemas are phrase openers or endings, not loops.
- Never label a loop by chords alone. Singer/songwriter and hopscotch can each be major or minor. Choose the tonic with the **bass and melody**.
- A chord can be swapped for another with the **same job** (ii for IV; V for ♭VII). The loop is still recognised.

## 2. Modes (brightest to darkest) and their "colour note"
Order: Lydian, major, Mixolydian, Dorian, natural minor (aeolian), Phrygian, Locrian. Each step darker flips one note. [OMT, Hein]

| Mode (on C) | The one note that tells you | Signature chord | Where OMT says it shows up |
|---|---|---|---|
| Lydian | F♯ (raised 4) | D major (II♯) | Fleetwood Mac "Sara", Cee Lo "Forget You" |
| Major | none | | |
| Mixolydian | B♭ (lowered 7) | B♭ major (♭VII) | Kinks "Tired of Waiting", double plagal |
| Dorian | A (raised 6 against minor) | F major (IV) on Cm | Funk and disco: CHIC, Daft Punk "Get Lucky" |
| Aeolian | A♭ and B♭ | A♭ (♭VI) and B♭ (♭VII) | Gotye "Somebody That I Used to Know" |
| Phrygian | D♭ (lowered 2) | | Named; no pop schema in OMT |
| Locrian | D♭ and G♭ | | Rare; jazz over half-diminished chords |

**Listen test from OMT (3 questions):** 1) Is the tonic chord major or minor? 2) Is the 7th a whole step below tonic (lowered)? 3) For major tonic: raised 4th = Lydian. For minor tonic: raised 6th = Dorian.

**Pentatonic (OMT, Biamonte 2010):** five notes, no half steps (C D E G A). In rock/pop the scale supplies chord ROOTS, and the chords can be major, minor, or power chords. This gives deliberate "clashes" (E and E♭, A and A♭). That is normal in guitar music, not a mistake.

## 3. Borrowed chords (mode mixture) [OMT chromaticism + jazz]
- Borrow from the **parallel minor** into a major key. The chord quality changes, the job does not.
- Most useful: iv (Fm) for IV, ♭VI (A♭), ♭VII (B♭), ♭III (E♭), ii-half-diminished (Dø7).
- Once mixture starts it usually **stays until the harmony moves on** (if the first predominant chord is borrowed, the next one is too).
- Cleanest borrowed note is the 6th: A→A♭. "Most effective when it involves lowered 6."
- Picardy third: a minor piece ending on a major tonic.
- Tonic and dominant: I→i is common; V→v is rare and usually means a real key change.

## 4. Voice-leading rules (the smooth-chords rules)
Two independent sources agree: OMT jazz ("lazy voices") and Berklee Online.

1. **Keep common tones in the same voice.** Notes shared by two chords do not move. [Berklee, OMT]
2. **Move other voices by step** (1–2 semitones) if possible. [Berklee, OMT]
3. **No upper voice moves more than a third** (3–4 semitones). [Berklee]
4. **The bass may leap** (fourths, fifths). Upper voices stay smooth. [OMT, Berklee "independent bass"]
5. **Leaps are for contrast**, used sparingly, best inside one chord. [OMT]
6. **Spacing copies the harmonic series:** wide intervals low, close intervals high. Close notes in a low register sound muddy. [OMT]
7. **Doubling:** double the bass or the root. [OMT]
8. **The 5th can be dropped.** The root and 7th should not be. [OMT]
9. **Extensions (9, 11, 13) go on top**, above the 7th. A 13 placed below the 7th sounds like a 6. [OMT]
10. **Parallel motion is fine in pop, rock, jazz** (every voice moving the same way). The strict "contrary motion" habit is classical. [Berklee]
11. **Guide tones:** triads use 3 and 5; seventh chords use 3 and 7 (omit the 5th). Listeners "hear" the missing 5th. [Berklee]

### Worked example A: pop loop I–V–vi–IV in C (verified by script)
| Chord | Bass (root) | Upper voices (MIDI) | Notes |
|---|---|---|---|
| C | 36 | 55, 60, 64 | G C E |
| G | 43 | 55, 59, 62 | G stays; C→B (−1); E→D (−2) |
| Am | 45 | 57, 60, 64 | G→A (+2); B→C (+1); D→E (+2) |
| F (over A) | 41 (or 45) | 57, 60, 65 | A stays; C stays; E→F (+1) |
Back to C: moves −2, 0, −1. **Biggest move anywhere: 2 semitones.**
Put the bass an octave or two lower than the upper voices. Keep it on the root (it may leap).

### Worked example B: jazz ii–V–I with 3–7 voices (verified by script)
| Chord | Lower voice | Upper voice | Optional top (9th/13th) |
|---|---|---|---|
| Dm7 | C4 = 60 (7th) | F4 = 65 (3rd) | E5 = 76 (9th) |
| G7 | B3 = 59 (3rd) | F4 = 65 (7th) | E5 = 76 (13th) |
| Cmaj7 | B3 = 59 (7th) | E4 = 64 (3rd) | D5 = 74 (9th) |
Roots in the bass: D2 = 38, G2 = 43, C2 = 36.
Lines: lower voice 60→59→59, upper voice 65→65→64. This is the "3rd of one chord becomes the 7th of the next" pattern from OMT.

### Worked example C: 12-bar blues voicing (3rds and 7ths)
| Chord | Voices (MIDI) |
|---|---|
| C7 | 58 (B♭), 64 (E) |
| F7 | 57 (A), 63 (E♭) |
| G7 | 59 (B), 65 (F) |
C7→F7 moves both voices down 1. F7→G7 moves both up 2. OMT: blues root motion is by fifth and step, so voices stay smooth.

## 5. Jazz and blues building blocks (OMT Jazz unit)
- **ii–V–I:** mi7–7–ma7 in major, ø7–7–mi7 in minor. A ii–V can stand alone and still sound like a ii–V.
- **Turnaround:** I–vi–ii–V. Variant: swap vi for a dominant on the same root (A7), and add its ii in front (Em7–A7).
- **Tritone substitution:** replace a dominant with the dominant a tritone away (G7→D♭7). Works best going **to I**. It creates a chromatic bass line (D♭ → C).
- **Safe borrowed colours in jazz:** ii-half-diminished for ii7, and ♭9 on V7.
- **12-bar blues:** bars 1–4 I; 5–6 IV; 7–8 I; 9 V; 10 IV; 11–12 I. All chords dominant sevenths. Plagal motion (IV–I) closes phrases. Variants: 16-bar blues; minor blues (i7 and iv7 minor, V stays dominant, ii–V–I in the last phrase); jazz blues (adds ii–Vs).
- **Chord-scale (Berklee-taught):** m7 = Dorian, dominant 7 = Mixolydian, maj7 = Ionian or Lydian. Put chord tones on the downbeats. OMT warns it can make solos choppy and ignores bebop chromatic notes.

=== END OF PART ===
