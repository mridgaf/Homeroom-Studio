---
name: Next One Vocal — Two-Stage Compression
book: hip-hop
sounds_like: Jay-Z "On to the Next One" (2009) lead vocal, Young Guru chain
accuracy: B
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), based on a published interview about the engineer's hardware chain, adapted to stock Reason. Old project rated it A; re-rated because the hardware is replaced by stock devices
tags: jay-z vocal chain young guru compression two stage eq de-ess reverb delay rap lead mclass pulveriser
technique: slow compressor for glue, fast compressor for peaks, cut before and boost after, ambience on sends
---
# Next One Vocal — sounds like Jay-Z, "On to the Next One"

**Accuracy: B** — the order and idea come from a documented hardware chain. Reason's stock devices only approximate each hardware stage. Biggest limit: the sound starts with a clean source. A cheap mic in an untreated room won't get there. Assumes a clean dry vocal from a decent condenser mic, no processing on the recording.

## The Chain
Channel input and high-pass → MClass Equalizer (cuts) → MClass Compressor (slow) → MClass Compressor (fast) → MClass Equalizer (boosts) → Pulveriser (de-ess workaround). Sends: RV7000 hall and The Echo quarter-note delay.

## Steps
1. Channel: set input gain so the loudest words peak around -6 dB. High-pass at 80 Hz.
2. EQ #1, cuts only: -2 dB shelf at 120 Hz, -3 dB at 250 Hz (Q 1.2, the usual vocal mud), and -2 dB at 1.5 kHz (Q 2) only if the voice sounds nasal.
3. Compressor #1, the slow one: ratio 2:1, attack 30 ms, release 250 ms, threshold -16 dB, set to RMS mode. Aim for 2–3 dB reduction on average. This is smooth level control you barely hear.
4. Compressor #2, the fast one: ratio 4:1, attack 8 ms, release 100 ms, threshold -10 dB, Peak mode. Catches loud peaks, 3–5 dB. The two together do about 6–8 dB.
5. EQ #2, boosts: +1 dB shelf at 100 Hz, +3 dB at 4 kHz (presence, pushes it forward), +2 dB shelf at 10 kHz (air).
6. De-ess last: Pulveriser Squash 30, filter high-pass around 5 kHz, narrow band. This is a workaround for the harsh "s" sounds. Check the original's Pulveriser filter settings against the device before trusting them.
7. Sends: RV7000 Hall, decay 1.4 s, predelay 25 ms, return EQ high-pass 250 Hz and low-pass 8 kHz, send at -20 dB. The Echo synced 1/4, feedback 20, ducking ON at 50, send at -22 dB. Both subtle, the vocal stays dry and forward.

## Why this works
Two compressors share the work, so neither pumps. Cutting before compression means the compressor isn't wasting effort on mud. Boosting after means the boosts don't get squashed.

## Order of operations
Cuts, slow comp, fast comp, boosts, de-ess. Reverb and delay on sends so you can change them without touching the dry vocal.

## Reason-specific trick
Put the inserts in a Combinator, knobs for each compressor threshold, the 4 kHz boost, and the de-ess amount. Save as "Rap Lead Vocal.cmb". Use the channel's input gain, not the fader, to change what the chain hears.

## RE upgrade path
None required. The old notes named some hardware-emulation REs and a pitch-correction device. Names and prices unverified, and Reason's own pitch device is Neptune, so check the exact name in your Reason.

## Technique you just learned
Two-stage serial compression with split EQ. It works on any lead vocal in any genre.

## Reference
Jay-Z — "On to the Next One": https://www.youtube.com/results?search_query=Jay-Z+On+to+the+Next+One+official+audio
