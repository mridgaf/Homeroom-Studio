---
name: Gritty Rock Vocal
book: rock
sounds_like: 90s alt-rock lead vocal (Foo Fighters / grunge era)
accuracy: B
status: theoretical
source: dynamic mic (SM7B/SM58-ish), untreated or semi-treated room
tags: vocal grit rock lead saturation parallel distortion
technique: parallel saturation — grit without destroying intelligibility
---
# Gritty Rock Vocal — sounds like 90s alt-rock lead

**Accuracy: B** — the attitude is there; the last 10% is a real tube pre and a great room.

## The Chain
Channel strip (HPF + EQ + comp) → parallel Scream 4 (via Spider Audio) → RV7000 MkII plate (send)

## Steps
1. Channel strip: engage HPF at 80 Hz. EQ: cut 2–3 dB around 300 Hz (LMF), boost 2 dB at 3 kHz (HMF) for bite.
2. Channel strip compressor: ratio around 4:1, fast attack OFF, release medium. Aim for 4–6 dB gain reduction on loud phrases.
3. Split the vocal with a Spider Audio: path A dry, path B into Scream 4.
4. Scream 4: Damage type Tube, Damage ~35, P1 ~60, P2 ~50. Cut section: lows -20. Master level down so it sits UNDER the dry path.
5. Blend the Scream path in at roughly -10 dB relative to dry — you should feel it, not hear it as distortion.
6. Send to RV7000 MkII: algorithm Plate, decay 1.1 s, predelay 30 ms, HF damp on. Send level low — rock vocals stay dry-ish.

## Why this works
The dry path keeps consonants intact; the parallel Scream adds harmonics that read as "power" at mix level.

## Order of operations
Compress BEFORE the parallel split so both paths get a consistent level — otherwise the grit pumps.

## Reason-specific trick
Build the whole thing in a Combinator 2 and map one macro knob to the Scream path's level. That knob is now a "grit" control per song section.

## RE upgrade path
None needed at B. If you chase A: a tape/console emulation (e.g., Softube Tape, ~$99) rounds the top end.

## Technique you just learned
Parallel saturation: distort a copy, tuck it under the clean signal.
