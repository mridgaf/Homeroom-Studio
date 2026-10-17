---
name: Driven Rock Bass
book: rock
sounds_like: Royal Blood / Muse — distorted bass that still has low end
accuracy: B
status: theoretical
source: DI electric bass or synth bass, clean
tags: bass distortion drive rock split parallel low end
technique: frequency-split processing — distort the mids, protect the sub
---
# Driven Rock Bass — sounds like Royal Blood / Muse

**Accuracy: B** — the split trick gets you most of the way; a real fuzz pedal and amp has hair stock Reason can't fully fake.

## The Chain
Spider Audio split → path A: MClass EQ (lows only) → path B: Scream 4 + MClass EQ (mids/highs only) → merge → channel comp

## Steps
1. Split the bass with a Spider Audio into two mix channels: "Bass Sub" and "Bass Dirt".
2. Bass Sub channel: MClass Equalizer, lo shelf OFF, use Lo Cut off; enable Param 1 as low-pass stand-in — cut everything above ~250 Hz (Param 1: freq 250, gain -inf style deep cut, wide Q). Keep this path CLEAN. No distortion ever.
3. Bass Dirt channel: MClass EQ hi-pass — cut below 250 Hz (Lo Cut ON, then Param 1 cut at 180 Hz, -12 dB, medium Q).
4. Bass Dirt: Scream 4 after the EQ. Damage type Distortion, Damage 55–70, P1 to taste. Body section ON, type B, for cab-ish resonance.
5. Balance: dirt path about equal level with sub path; the distortion should carry the character, the sub carries the weight.
6. Merge both to a bass bus channel; bus compressor ratio 4:1, ~3 dB reduction, to glue the two paths into one instrument.

## Why this works
Distortion destroys low frequencies (intermodulation mud); splitting first means the sub never touches the dirt.

## Order of operations
EQ BEFORE Scream on the dirt path — what you feed a distortion changes what comes out far more than EQ-ing after.

## Reason-specific trick
Combinator 2 the whole rig; map macro 1 to Scream Damage, macro 2 to dirt-path level. Save as "Driven Bass.cmb" — this is your first "Your Sound" patch.

## RE upgrade path
For A-grade: a dedicated bass amp sim RE (Kuassa Cerberus, ~$49) replaces step 4's cab approximation.

## Technique you just learned
Frequency-split (multiband) processing with Spiders — works for guitars, drum busses, anything.
