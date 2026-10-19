# Chapter 13: College theory for MIDI patterns
## Part 4 of 4

_The emotion map (graded), a checklist of testable rules, and the source links._

**In this part:** what each device "means," with who said it; rules a script could test; links.
**Previous:** Part 3 of 4.md

## 1. Emotion map
Two tiers. **Tier A** = said by cited music-theory scholars in OMT. **Tier C** = one professor's common-practice shorthand (Hein). Use Tier C as a starting colour only.

### Tier A (cited)
| Device | What it does | Source in OMT |
|---|---|---|
| Plagal sigh IV–iv–I (in C: F, Fm, C; the top line falls A→A♭→G) | Nostalgia, sentimentality. A half step down into the tonic pulls strongly. | Williams and Lehman, via blues-schemas chapter. Example: Green Day "Wake Me Up When September Ends" |
| Aeolian cadence ♭VI–♭VII–I(i) | Success, heroism, fanfare ("Mario cadence"). Often with a major final chord. | Modal-schemas chapter. Fellowship theme, Super Mario, Final Fantasy |
| Lament i–♭VII–♭VI–V | Descending minor line; lament since Purcell and Bach | Classical-schemas chapter |
| Dorian shuttle i–IV | Funk and disco. Tonic stays put; the upper notes wobble. | Modal-schemas chapter |
| Lydian cadence II♯–IV–I | Smooth chromatic line (F♯ to F to E in the top voice). Rare; liked for the chromatic motion. | Modal-schemas chapter. "Forget You" |
| Fragile tonic (home chord weakened, e.g. inverted) | Vulnerability, loneliness, sensitivity | Spicer 2017, via tonics chapter |
| Emergent tonic (home chord withheld until the chorus) | Triumph, overcoming. "Let It Go" shows the chorus finally landing on A♭. | Spicer 2017 |
| Absent tonic (never played, only implied by the melody) | A disconnect; "constant partying vs. real life" in the example | Spicer 2017. "Last Friday Night" |
| Singer/songwriter and hopscotch loops | **Tonal ambiguity**: major or minor depends on how it is approached | Four-chord-schemas chapter, Richards 2017 |
| Major III♯ in I–III♯–IV (C E F) | Chromatic line G→G♯→A in the top voice; can sound like a deceptive resolution | Puff-schemas chapter. Radiohead "Creep" |
| Bare shuttle I–♭VII | Open, unresolved, loop-friendly | Modal-schemas chapter |

Careful: OMT says these meanings are **tendencies** (often tied to the lyric). They are not laws. For instrumental beats there is no lyric, so the same chord can read differently.

### Tier C (Hein, uncited; his own comment says there are no references)
| Scale | Mood word |
|---|---|
| Major | happy; majestic or sentimental when slow |
| Mixolydian | bluesy, rock |
| Lydian | ethereal, dreamy, futuristic |
| Dorian | hip, sophisticated, jazzy ("for hip-hop, Dorian") |
| Natural minor | sentimental, tragic |
| Phrygian | Spanish / flamenco |
| Locrian | very dark and unstable |
| Blues scale | bluesy; works over major and minor |
| Whole-tone | dreamy, underwater |
| Chromatic | freefalling, anxious |

## 2. Testable rules (a script can check these)
Every line is from Part 2 or 3. "T" means a test can be written.
1. T: In a chord loop, every upper voice moves **≤ 4 semitones** between chords, and common tones stay in the same voice (Berklee).
2. T: The root is the lowest note (bass) and may leap (OMT/Berklee).
3. T: Extensions (9, 11, 13) are above the 7th (OMT).
4. T: For seventh chords, the 5th may be missing; the 3rd, 7th and root may not (OMT).
5. Not coded: low-register spacing. The guideline is sourced (Hoffmann, Funnell), but its number table is a chart image that has not been transcribed yet. No number is used until it is read and checked.
6. T: Chord changes start on step 0 of a bar (or step 8 for half-bar changes).
7. T: A backbeat exists: snare/clap on steps 4 and 12 (or step 8 in half-time).
8. T: Kick on step 0 of at least every second bar (Berklee, OMT).
9. T: Loops are 2, 4 or 8 bars.
10. Ear-only: does a chord-loop label match the melody's tonic? (singer/songwriter, hopscotch).
11. Ear-only: does a "lydian" loop actually have the raised 4th in the melody?
12. Dembow: unconfirmed, excluded from the generator.

## 3. How this could plug into Homeroom Studio
Built (first version): `tools/theory_loops.py` uses the schema list, voice-leading rules 1-2, 6-9 and the drum table, then checks its own files. Other options still open:
- A **schema list** (Part 2 section 1) as the chord source, instead of free-form chords.
- A **voice-leading checker** (rules 1–4 above) run on every chord track before it is written.
- A **drum-pattern table** (Part 3 section 2) for the groove library.
- **Emotion tags** from Tier A only, so a beat can ask for "heroic" or "nostalgic" and get a schema.

## 4. Source links (all free)
- Open Music Theory v2: https://viva.pressbooks.pub/openmusictheory/
  - Pop: /chapter/intro-to-pop-schemas/, /4-chord-schemas/, /blues-based-schemas/, /classical-schemas/, /puff-schemas/, /modal-schemas/, /pentatonic-harmony/, /fragile-absent-and-emergent-tonics/, /drumbeats/, /rhythm-and-meter-in-pop-music/
  - Jazz: /jazz-voicings/, /ii-v-i/, /substitutions/, /chord-scale-theory/, /blues-harmony/, /swing-rhythms/
  - Other: /modal-mixture/, /intro-to-diatonic-modes-and-the-chromatic-scale/, /hypermeter/, /metrical-dissonance/ (fetched; hypermeter used; metrical-dissonance not summarised here)
- Berklee Online, voice leading: https://online.berklee.edu/takenote/voice-leading-paradigms-for-harmony-in-music-composition/
- Berklee College, hip-hop production: https://college.berklee.edu/bt/news/essential-features-of-hip-hop-production-tempo-instrumentation-rhythmic-feel-and-sonic-density
- Ethan Hein: https://www.ethanhein.com/wp/2010/scales-and-emotions/ and https://www.ethanhein.com/wp/2021/modes-from-light-to-dark-around-the-chromatic-circle/
- MIT OCW 21M.301 calendar: https://ocw.mit.edu/courses/21m-301-harmony-and-counterpoint-i-spring-2005/pages/calendar/
- Papers cited by OMT (not read): Biamonte 2010 (https://doi.org/10.1525/mts.2010.32.2.95), Spicer 2017 (http://mtosmt.org/issues/mto.17.23.2/mto.17.23.2.spicer.html), McClimon 2017 (http://mtosmt.org/issues/mto.17.23.1/mto.17.23.1.mcclimon.html), Richards 2017 (http://mtosmt.org/issues/mto.17.23.3/mto.17.23.3.richards.html)
- Originals: exact copies of the text fetched for the 20 OMT chapters, the MIT calendar and the Berklee Online voice-leading article are in `Originals/CT/`. The Berklee hip-hop article and the two Hein pages are linked above only (not saved).

=== END OF PART ===
