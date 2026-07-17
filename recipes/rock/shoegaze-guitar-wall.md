---
name: Shoegaze Guitar Wall
book: rock
sounds_like: My Bloody Valentine / Slowdive wash
accuracy: C
status: theoretical
source: DI electric guitar, clean; works better with two takes
tags: guitar shoegaze wall reverb wash chorus wide ambient
technique: reverb INTO distortion — the wash becomes part of the tone
---
# Shoegaze Guitar Wall — sounds like MBV / Slowdive

**Accuracy: C** — honest flag: real shoegaze is a fuzz pedal, a Jazzmaster, and reverse-reverb pedals into a loud amp. Stock Reason approximates the wash, not the bloom. This gets you "dreamy wide wall," not Loveless.

## The Chain
Double-tracked guitar → CF-101 chorus → RV7000 (100% wet) → Scream 4 → wide panning

## Steps
1. Record the part twice (real doubles, not a copy). Pan take 1 hard left, take 2 hard right.
2. Each side: CF-101 Chorus/Flanger — rate low (~30), feedback 0, delay ~40, sync off. Subtle movement, not seasick.
3. Here's the trick, per side: RV7000 as an INSERT set 60–80% wet, Hall, decay 4 s, THEN Scream 4 after it.
4. Scream 4: Damage type Fuzz, Damage 45–60. Because the reverb feeds the fuzz, the tail distorts and smears into the tone. That's the shoegaze move.
5. Roll off highs after: channel EQ high shelf -3 dB at 8 kHz. Shoegaze walls are dark, not bright.
6. Both sides to a guitar bus; bus comp 2:1, slow attack, 2 dB reduction, just to stop the wall from swallowing the snare.

## Why this works
Normal chains distort then reverberate (clean tail). Reversing the order makes the reverb tail itself distort — a continuous sustaining wall.

## Order of operations
That reversal IS the recipe. Reverb → distortion. Non-negotiable here.

## Reason-specific trick
Automate the RV7000 dry/wet from verse (30%) to chorus (80%) via a Combinator macro for the "the chorus just opened up" effect.

## RE upgrade path
This is a D→C rescue by stock. For a real B: a proper fuzz + reverse reverb RE or VST (Reason 12 runs VST3 — free options: Airwindows fuzz, Valhalla Supermassive, $0).

## Technique you just learned
Effect-order inversion: putting time-based effects BEFORE gain effects changes the instrument, not just the polish.
