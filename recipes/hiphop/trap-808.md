---
name: Trap 808
book: hip-hop
sounds_like: Metro Boomin-era trap sub with knock
accuracy: B
status: theoretical
source: MIDI notes only — no audio source needed
tags: 808 sub bass trap knock boom subtractor pitch
technique: pitch envelope on a sine — the "knock" is a fast pitch drop, not a drum
---
# Trap 808 — sounds like modern trap sub

**Accuracy: B** — SubTractor builds a legit 808. The missing character is sample-specific distortion from the classic TR-808 bridged-T circuit; saturation gets close.

## The Chain
SubTractor → Scream 4 → MClass Compressor

## Steps
1. SubTractor: Osc 1 waveform 4 (sine). Polyphony 1, Legato ON, Portamento ~40 for the trap slide between notes.
2. Amp envelope: A 0, D 90+, S 0 for boom that decays — or S 80 for held 808s you gate with note length. R ~30.
3. The knock: Mod envelope → destination Osc Pitch, Amount ~40–55, A 0, D ~25, S 0. Every note now starts with a fast pitch drop — that transient IS the knock.
4. Filter 1: LP24, freq ~70%, no resonance. Just taming harmonics from the saturation to come.
5. Scream 4: Damage type Tape, Damage 25–40. This adds harmonics so the 808 is audible on phone speakers. More Damage = more mids = more "distorted 808" as a style choice.
6. MClass Compressor: ratio 4:1, fast attack, ~3 dB reduction — evens out note-to-note level so the sub is constant.
7. Play it low: F1–B1 range. Write the pattern, then tune 808 notes to the song key — an out-of-key 808 ruins everything above it.

## Why this works
An 808 is a sine with a pitch-drop transient; saturation folds sub energy up into audible mids.

## Order of operations
Scream before the compressor: saturation changes level dynamics, and the comp should even out the FINAL sound.

## Reason-specific trick
Combinator 2: map macro 1 to Scream Damage ("dirt"), macro 2 to Mod Env Amount ("knock"). Save as "My 808.cmb". Sidechain note: to duck it under the kick, use the channel compressor's sidechain input fed from the kick channel — Reason's mixer does this natively, no CV hacks needed.

## RE upgrade path
None needed. If you want instant variety, sample packs beat synthesis for exotic 808s.

## Technique you just learned
Transients can be synthesized with pitch envelopes — the same trick makes kicks, toms, and lasers.
