---
name: Kick and 808 Relationship
book: hip-hop
sounds_like: any modern hip-hop low end where kick and 808 hit together
accuracy: B
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), widely used technique adapted to Reason, no producer session. Old project rated it A and Tested; re-rated and set to theoretical
tags: kick 808 sidechain duck low end eq carving combinator mclass compressor spider mud sub
technique: when two sounds fight for the same low notes, duck one in time, split the frequencies, or do both gently
---
# Kick and 808 Relationship — make them hit as one

**Accuracy: B** — the three methods are standard. The exact numbers are starting points to adjust by ear. Assumes a clean kick one-shot and a clean sine-based 808 with no built-in sidechain or saturation.

## The Chain
Kick → mixer. 808 → MClass Equalizer → MClass Compressor (sidechain fed by the kick) → mixer. Wrap the 808 chain in a Combinator.

## Steps
1. Why you're doing this: kick and 808 both live around 40–80 Hz. Together untreated they mask each other and the low end turns muddy or the kick disappears on small speakers.
2. Method 1, duck the 808 (most common). Flip the rack (Tab). Split the kick with a Spider Audio Merger & Splitter: one copy to the mixer, one into the Sidechain input of the MClass Compressor on the 808. Turn the compressor's Sidechain button ON.
3. Compressor settings for the duck: ratio 4:1, threshold about -18 dB until you see 4–6 dB reduction on each kick, attack 0.1 ms, release 80–120 ms, soft knee ON. The 808 gets out of the way for a split second on each kick.
4. Method 2, split the frequencies (use when the 808 sustains and ducking would sound wobbly). Kick EQ: -6 dB shelf at 50 Hz, +3 dB at 90 Hz, +2 dB at 3 kHz. 808 EQ: +2 dB shelf at 40 Hz, -4 dB at 90 Hz, roll off above 800 Hz.
5. Method 3, both gently (the usual default). EQ the 808 like Method 2 but with a -2 dB cut at 90 Hz, then compress with only 2–3 dB of duck. Put the EQ first and the compressor after.
6. Wrap the 808 EQ and compressor in a Combinator. Knobs: Rotary 1 = duck amount, 2 = sub boost, 3 = release, 4 = mud cut at 90 Hz, Button 1 = bypass so you can A/B.
7. Check: play the same rhythm with the Combinator bypassed and on. Bypassed should sound smaller and muddier. If not, check the cable is really patched, the 808 has no built-in enhancer, and the kick tail isn't too long.

## Why this works
Ducking handles the moment of the hit, frequency splitting handles the steady sound. Together your ear hears one low-end event.

## Order of operations
EQ first to remove overlap, compressor after to handle what's left. Don't shape tone before the duck is set.

## Reason-specific trick
Save as "KickPocket 808 Bus.cmb". Stock Reason can only duck the whole 808, not just part of it. If the kick has a long tail, shorten the sample or tighten it with a gate first, otherwise the 808 pumps too long.

## RE upgrade path
Only a multiband sidechain would fix the "whole 808 ducks" limit. The old notes named Kilohearts Multipass and FabFilter Pro-MB, with prices from May 2026. Unverified, check before buying anything.

## Technique you just learned
Sharing a crowded frequency range between two sources. The same moves work for kick plus bass guitar, kick plus synth bass, floor tom plus bass.

## Reference
Any modern trap track, solo the kick and 808 to hear the duck: https://www.youtube.com/results?search_query=kick+808+sidechain+tutorial
