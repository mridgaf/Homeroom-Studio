---
name: Upfront Rap Vocal
book: hip-hop
sounds_like: modern rap vocal — dry, close, every word intelligible
accuracy: B
status: theoretical
source: condenser or SM7B, quiet room, rapper 4-6 inches off the mic
tags: vocal rap hip hop upfront dry compression delay throw
technique: serial compression — two compressors doing 3 dB each beat one doing 6
---
# Upfront Rap Vocal — modern dry rap chain

**Accuracy: B** — honest gap: stock Reason has no de-esser. If your source is sibilant, that's the weak link (fix below).

## The Chain
Channel strip (HPF + EQ + comp #1) → MClass Compressor (#2) → DDL-1 throw (send) → RV7000 tiny room (send)

## Steps
1. Channel strip HPF: 90 Hz. Rap vocals carry no useful info below that; the 808 owns it.
2. Channel EQ: cut 2 dB at 400 Hz (boxiness), boost 1.5 dB at 5 kHz (presence). Less is more — modern rap vocals are clean, not scooped.
3. Channel comp: ratio 3:1, medium attack, ~3 dB reduction. First stage catches phrases.
4. MClass Compressor: ratio 4:1, fast attack, another ~3 dB. Second stage catches syllables. Two gentle stages sound transparent; one 6 dB stage sounds squeezed.
5. De-ess workaround: MClass EQ between the comps, cut 3–4 dB at 6–8 kHz narrow Q, ONLY if esses hurt. Crude but stock. (Real fix: free VST3 de-esser — Techivation T-De-Esser, $0.)
6. DDL-1 on a send: 1/4 note sync, feedback ~25, pan it. Automate the send up on the last word of a line — the classic "throw".
7. RV7000 on a send: Room, decay 0.4 s, barely audible. Rap vocals read "dry" but a touch of room stops the sterile-booth feel.

## Why this works
Serial compression controls dynamics invisibly; the dryness keeps the voice in front of the beat instead of inside it.

## Order of operations
EQ cut before compression — otherwise the comps react to the 400 Hz mud you were going to remove anyway.

## Reason-specific trick
Automate the DDL-1 send in the sequencer lane rather than riding it live — draw a spike on the throw word. Perfectly repeatable.

## RE upgrade path
De-esser is the one real hole; free VST3 fills it. No RE purchase justified.

## Technique you just learned
Serial compression: split the workload across stages.
