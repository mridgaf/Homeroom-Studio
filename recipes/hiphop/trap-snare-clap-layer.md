---
name: Trap Snare and Clap Layer
book: hip-hop
sounds_like: Mike WiLL Made-It layered clap and snare, "23"
accuracy: B
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), general layering technique, no producer session. Old project rated it A; re-rated to Homeroom's scale
tags: trap snare clap layer mike will made-it combinator nn-xt crack macro
technique: layer a body sound with a snap sound inside a Combinator and put the levels on knobs
---
# Trap Snare and Clap Layer — sounds like Mike WiLL Made-It

**Accuracy: B** — two samples stacked is a standard trick. The final sound depends on which two samples you pick. Assumes one dry clap (the body) and one snappy snare (the snap).

## The Chain
Combinator [NN-XT clap + NN-XT snare → Combinator mixer → MClass Equalizer → MClass Compressor] → mixer channel

## Steps
1. Make a Combinator and put two NN-XTs in it. Load the clap in the first and the snare in the second.
2. Clap NN-XT: pitch 0, filter fully open, amp envelope A 0, D 80 ms, S 0, R 50 ms (short, no tail).
3. Snare NN-XT: pitch 0 (or +2 semitones for crispness), high-pass filter at 120 Hz so it leaves the low body to the clap, amp envelope A 0, D 30 ms, S 0, R 30 ms.
4. In the Combinator's mixer: clap at 0 dB, snare at -4 dB (the snare is the helper, not the lead). Both centered.
5. MClass Equalizer on the Combinator output: +1 dB at 200 Hz (body), -2 dB at 1.5 kHz (removes honk), +3 dB at 6 kHz (crack), +2 dB shelf at 12 kHz (air).
6. MClass Compressor: ratio 6:1, attack 1 ms, release 80 ms, soft knee OFF, about 6 dB reduction on hits. The fast hard squeeze glues the two sounds into one hit.
7. Map four Combinator knobs: Rotary 1 = clap level, 2 = snare level, 3 = the 6 kHz crack, 4 = compressor threshold. Now you can retune per song from the front.

## Why this works
Two samples give you more control than one: the clap carries weight, the snare carries snap. Hard compression makes your ear hear one hit.

## Order of operations
Layer inside the Combinator first, then EQ and compress the combined sound together.

## Reason-specific trick
Save as "Trap Snare Layer.cmb". The same layering works for kicks (sub plus click) and hats (closed plus open).

## RE upgrade path
None required. The old notes named a Kuassa maximizer for a more metallic top. Unverified.

## Technique you just learned
Sample layering inside a Combinator with knob control.

## Reference
Mike WiLL Made-It — "23": https://www.youtube.com/results?search_query=Mike+WiLL+Made-It+23+official
