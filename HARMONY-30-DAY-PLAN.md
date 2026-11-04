# Harmony review, last 30 days: Original side (2026-11-03)

**Status: proposal. Nothing changed. Drums are not touched by anything here.**

## What I read
- **Data:** 896 Original-side beats made 2026-10-04 to 11-03 (the `.recipes/*.json` files on TBOTC 3; loops-only beats left out).
- **Split out:** the 156 beats made after the 10-31 "one chord" rule, since those show what the machine does **today**.
- **Not used:** the "DJ Ingredient Charts" artifact. It shows config settings (kit words), not 30 days of real output.
- **Not heard:** I didn't render or listen to anything.

## What shows up too much

| # | Weird thing | Numbers | Why it sounds off |
|---|---|---|---|
| 1 | **Sharp spelling everywhere** | 55% of beats have chords named with sharps, like A#m or G#. The code always spells notes with sharps (`key_context.spell`). | In F minor (the #1 key) the chords show as **A#m, C#, D#** when they should read **Bbm, Db, Eb**. The sound is right, but the names look wrong. |
| 2 | **Odd scales** | Today: phrygian 11%, harmonic minor 9%, phrygian dominant 6%, lydian 5% = **31% of beats**. | These scales contain the "weird" notes: the note just above home (b2), the raised 7th and the #4. The Hub says rap mostly lives in minor and dorian, with phrygian used for menace. |
| 3 | **Happy keys on a rap machine** | major + mixolydian + lydian = 30% of today's beats. | Hub ch.4: "Major keys read as cheerful, which fights most rap vocals." |
| 4 | **Free beats roll ANY scale** | 30% of beats (15% for Legends) leave the DJ's character and pick from all 8 scales at equal odds (`_roll_key`, open roll). | That's how a Doc Day beat lands in lydian. It's a big source of #2. |
| 5 | **Sharp-side roots** | C#, D#, G#, A#, F#, B = 23% of today's beats. In the configs, 20 DJ root entries use sharps and only 11 use flats. | Hip-hop leans to C, D, G and F minor plus the flat keys (Eb, Ab, Bb). |
| 6 | **The vamp: one chord, every beat** | 100% of today's beats play a single chord. Before 10-31 it was 19%. | This was your rule ("no chord changes in such a short pattern"). It also stopped out-of-key chord notes: there are **0** now, down from 18% of chord notes before. A real loop machine still uses a 2-chord move (i–bVI, i–iv) on a good share of beats. |
| 7 | **Chord sound spread thin** | About 25 voices (piano stab, wood stab, organ comp…), each 1–3% of beats. | No DJ sounds like himself. Every beat draws a different instrument. |
| 8 | **Strange melody instruments** | Bell is the #1 melody group today (13%), even though MIDI notes are supposed to skip bell. Also showing: Dan Tranh, folk harp, ocarina, saxello, kalimba, Clavisynth. | Folk and world instruments sitting on rap beats. |
| 9 | **No melody on half** | 53% of today's beats have no melody. | Probably fine. I'm flagging it, not proposing a change. |

Before the one-chord rule, the worst offenders for off-key notes were the named progression tables (21% of notes outside the key) and colored chords like 7b9, maj7#11 and 13 (28–32% outside).

## Proposed changes (harmony only, new beats only, stamped like every other flow)

1. **Spell flats in flat keys.** F, Bb, Eb, Ab, Db minor and C minor show Bb, Eb and Ab instead of A#, D# and G#. Names and the UI change. The audio doesn't. *(tiny)*
2. **Rename sharp roots in the configs:** A# → Bb, D# → Eb, G# → Ab. Same pitch, readable names. *(tiny)*
3. **Scale diet for rap.** Default odds: minor 55, dorian 20, phrygian 10, harmonic minor 5, major/mixolydian 10. Lydian and phrygian dominant only for identities whose research names them. *(config + test)*
4. **Free beats stay rap-shaped.** The open roll picks from the same weighted rap set in #3, not all 8 scales evenly. *(one line in `_roll_key`)*
5. **Bring back a 2-chord move on some beats** (your call, see question): on about 35% of beats, allow i–bVI, i–iv, i–bVII or i–v with every note in the key and no halfway switch. The rest stays one chord.
6. **Give each DJ 2–4 home voices** for chords (from their research) instead of the 25-way spread. *(config)*
7. **Melody: drop folk/world instruments and bell** unless a DJ's research names them. Keep piano, Rhodes/EP, guitar, synth lead, strings, flute. *(config + filter)*
8. **Melody notes:** keep to minor pentatonic + the 2nd on the strong beats. No raised 7th or #4 in melodies unless the scale is that DJ's own. *(small)*

**Not touched:** kicks, snares, hats, perc, drum timing, drum kits, 808 lane, mix.

## Deeper research (TinyFish, 2026-11-03): only what changes the plan

1. **One chord is a style, not the default.** Producer guides match the chord count to the mood:
   - one chord = dark trap or drill
   - two chords (1-4, 1-5, 1-6) = catchy, melodic or soul
   - 1-7-6 = emotional
   - 1-6-5 = the hip-hop staple

   **Change to #5:** let each DJ's style decide. Dark DJs (Night Metro, Rage Engine, Razor, Memphis…) keep one chord. Soul and melodic DJs (Sunday Chop, No Alias, Tenth Wonder, Glass Cat…) get mostly two-chord loops. The every-note-in-key rule stays either way.
2. **How to make one chord not boring:** drop the middle note (root + fifth only, "hollow and cold"), move one note up or down an octave, and add one scale note that steps back home. **Add to #5:** dark one-chord beats lean on root + fifth.
3. **Harmonic minor and phrygian are spice, not the base.** Guides say start in natural minor; harmonic minor is "tense, Spanish-leaning" and phrygian is "menace". This backs up #3.
4. **Flat keys come from the samples.** Horn-heavy soul and funk records sit in flat keys, so F minor, Bb minor and Eb minor show up on sample-style beats. This backs up #1 and #2: use flat names for those keys.
5. **Gomez-Peck dissertation (2023), read from your PDF, ch.1 pp.55-59, using Adams 2020.** Real hip-hop beats come in three harmony types. It gives no percentages.
   - **Repetitive** = one chord (a pedal). Valid, and almost always closed on tonic.
   - **Oscillating** = two chords, called "a special and particularly common format". The two roots are a **2nd, 3rd or 4th apart**. The most common pair is **i–iv** (plagal). Examples: Dr. Dre "Xxxplosive" and "Bang Bang", Gang Starr "Just To Get A Rep", A Tribe Called Quest "Check the Rhime", De La Soul "The Magic Number". Most are "open" (the loop ends on the NON-tonic chord, so it pulls back to the start).
   - **Expansional** = 3 or 4 chords, "three or four are the most common". Four chords follow tonic → pre-dominant → dominant → tonic. Three end on the dominant. Many use a **lament bass** that steps down from 1 through ♭7 to ♭6 or 5 (Kanye "Stronger", Snoop "Who Am I", 2Pac "Tradin War Stories").
   - Loops are most often **1, 2 or 4 bars**.

   **Changes to #5:** (a) The two-chord move should be **i–iv first** (then i–bVII, i–bIII). My earlier "i–bVI" list was too narrow. (b) Make the 2-chord loop **open**: it ends on the non-tonic chord. (c) If a 3–4 chord loop is ever allowed again, give it a lament-bass or tonic–subdominant–dominant shape, not a random walk. (d) Loop length 1, 2 or 4 bars is already how the machine works. No change.

## Sources
- [Songen: five types of trap melody (2026)](https://songen.app/blog/how-to-make-trap-melodies/)
- [Meshplugins: hip-hop key and tempo (2026)](https://shop.meshplugins.com/blogs/the-hidden-sauce/hip-hop-key-and-tempo)
- Gomez-Peck, *Form in Hip-Hop Music: Sections, Songs, and History* (CUNY, 2023), your PDF in this folder, ch.1 pp.55-59, building on Kyle Adams, "Harmonic, Syntactic, and Motivic Parameters of Phrase in Hip-Hop", Music Theory Online (2020).
- Production Research Hub ch.4 Music theory, parts 1–2: rap lives in minor, dorian and phrygian; major fights rap vocals; phrygian i–bII is the villain move.
- [Billboard / Hit Songs Deconstructed](https://www.billboard.com/?p=8099843): minor keys rose to 62% of top-10 hits by 2017, tied to hip-hop's rise.
- [ChartCipher via PressReader](https://www.pressreader.com/philippines/the-freeman/20240320/281668259962577): hip-hop tends to favor minor tonalities.
- [Hooktheory chord-progression analysis](https://salu133445.github.io/pdf/chord_progression_analysis_report.pdf): the top minor 4-chord loop is i–bVI–bVII–i (Cm–Ab–Bb–Cm, which the corpus spells G#/A#).
- [Ethan Hein, Theory for Producers](https://ethanhein.substack.com/p/theory-for-producers): producers often work in flat keys like Eb minor.
- Outside data was thin and one site contradicted itself, so the scale odds in #3 are my judgment from the Hub plus these sources, not a measured dataset.
