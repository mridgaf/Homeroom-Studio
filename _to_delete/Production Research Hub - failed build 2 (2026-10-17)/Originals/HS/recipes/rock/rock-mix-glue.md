---
name: Rock Mix Glue
book: rock
sounds_like: a finished rock record instead of separate tracks
accuracy: B
status: theoretical
source: a balanced rough mix hitting the master around -6 dB peaks
tags: master bus glue mix compression mclass full mix
technique: bus compression — slow attack, fast release, barely working
---
# Rock Mix Glue — master bus chain

**Accuracy: B** — MClass does the job; the missing 10% is the character of an SSL G-comp. Honest note: Reason 12 has no LUFS meter — load a free VST3 meter (Youlean Loudness Meter, $0) for streaming targets.

## The Chain
Master insert: MClass Equalizer → MClass Compressor → MClass Maximizer

## Steps
1. MClass Equalizer: Lo Cut ON (30 Hz rumble gone). Param 1: +1 dB at 100 Hz wide Q if the mix feels thin. Hi Shelf +1 dB at 10 kHz. That's it — master EQ is a nudge, not a fix.
2. MClass Compressor: ratio 2:1, attack SLOW (~35 ms so transients punch through), release fast or Adapt ON. Threshold until you see 1–2 dB reduction on the loud sections. Never more.
3. Listen with it bypassed vs in. The "in" version should feel slightly more like one performance. If it sounds squashed, back the threshold off.
4. MClass Maximizer: input gain until limiting shows 1–3 dB on peaks, Look Ahead ON, output -0.3 dB. Loudness comes from the mix, not this box.
5. A/B against a commercial rock reference at MATCHED volume (turn yours up/down till equal loudness) — louder always sounds "better" and lies to you.

## Why this works
1–2 dB of slow-attack compression makes tracks rise and fall together — the "glue" is shared gain movement.

## Order of operations
EQ before comp: fix tonal balance first so the compressor reacts to the mix you want, not the mud you're about to cut.

## Reason-specific trick
Put the chain in the master section's insert slot (SSL master bus), not on a separate channel — it stays with the song file.

## RE upgrade path
For A: an SSL-style bus comp emulation (Softube, ~$99) adds the nonlinear character MClass lacks.

## Technique you just learned
Glue compression: the compressor you barely hear working.
