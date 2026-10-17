---
name: Next One Lead Hook — Mangled Synth
book: hip-hop
sounds_like: Jay-Z & Swizz Beatz "On to the Next One" (2009), the chopped Justice "D.A.N.C.E." hook
accuracy: C
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), built from web research about Justice's sound, not from the real session. Old project also rated it C
tags: jay-z swizz beatz on to the next one justice dance lead hook thor scream bitcrush chop dr octo rex stab
technique: build a plain synth source, then wreck it on purpose and chop it into rhythmic stabs
---
# Next One Lead Hook — sounds like the chopped Justice hook

**Accuracy: C** — honest ceiling. The real hook is a chopped audio sample of a Justice track, and you can't synthesize the exact sound. This gets the family: narrow-pulse analog synth, distorted, bit-crushed. Next to the record it sounds like a cousin, not a twin. In a full mix it gets much closer.

## The Chain
Thor (two pulse oscillators) → Scream 4 (Digital) → MClass Equalizer → The Echo → MClass Stereo Imager → MClass Compressor → mixer channel. Bounce the Thor part, chop it in Dr. Octo Rex.

## Steps
1. Thor, oscillators: both Analog mode, Square/Pulse. Osc 1 pulse width 25, Osc 2 width 30 with detune +7 cents, octave 4. Osc 3 off. (Check exact parameter names against docs/reason/remote-vocab.json.)
2. Thor, filter and envelopes: Low Pass Ladder filter, frequency 78, resonance 35, drive 40. Quick filter envelope decay (35) so each note plucks. Amp envelope A 0, D 30, S 75, R 25. Chorus on, subtle.
3. Play short stabs in groups of three in A minor, A3 → C4 → E4, with a rest in the pattern. Bounce it to audio (Bounce in Place).
4. Chop: load the bounce into Dr. Octo Rex, slice it, and trigger slices out of order. Reverse one slice now and then, and drop one down a fifth.
5. Wreck it: Scream 4 Digital, Damage 55, then MClass Equalizer: -8 dB shelf at 150 Hz, -4 dB at 350 Hz, +6 dB at 3 kHz, -4 dB shelf at 8 kHz.
6. Movement: The Echo synced to 1/8 dotted, feedback 25, ducking ON at 40, mix 25%.
7. Stereo and glue: MClass Stereo Imager, low width 0, high width 130, crossover 600 Hz (keeps the lows centered). Compressor 4:1, attack 8 ms, release 60 ms, 4–6 dB reduction.

## Why this works
The Thor patch gives the raw tone, the Scream and EQ break it and push the mids so it cuts through, the echo adds motion, and mono lows keep it out of the 808's way.

## Order of operations
Distort first, shape after. Echo after the EQ so the repeats are already filtered. Compressor last so levels stay steady.

## Reason-specific trick
Wrap Thor and the chain in a Combinator. Knobs: Scream Damage, Thor filter decay, Echo feedback, compressor threshold. Save as "Mangled Lead.cmb". The chopping step matters as much as the patch.

## RE upgrade path
Europa can layer an FM-style bell for the missing bell sound, and it's stock. The old notes also named other synths and prices. Unverified.

## Technique you just learned
Wreck-then-shape sound design, and mono lows with wide highs.

## Reference
Jay-Z — "On to the Next One": https://www.youtube.com/results?search_query=Jay-Z+On+to+the+Next+One+official+audio
Justice — "D.A.N.C.E." live version: https://www.youtube.com/results?search_query=Justice+D.A.N.C.E.+live+version
