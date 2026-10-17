---
name: Trap Drum Bus
book: hip-hop
sounds_like: Metro Boomin / 21 Savage trap drums, "Bank Account"
accuracy: B
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), general technique, no producer session. Old project rated it A; re-rated to Homeroom's scale
tags: trap drum bus metro boomin 21 savage kick clap hats glue mclass pulveriser parallel
technique: tone-shape the whole drum group first, THEN glue it, with a little parallel grit
---
# Trap Drum Bus — sounds like Metro Boomin / 21 Savage

**Accuracy: B** — a standard, well-known bus chain adapted to Reason, not a documented session. Assumes decent samples already: punchy kick, crisp clap, dry hats, each on its own track.

## The Chain
All drums → one bus channel → MClass Equalizer → MClass Compressor → Pulveriser (mixed in quietly, about 20%) → master

## Steps
1. Send kick, clap, hats and percussion to one bus channel (the "bus" is one channel that all the drums share, so you treat them together).
2. MClass Equalizer, kick weight: boost +2 dB at 60 Hz, Q 1.2.
3. Same EQ, mud and snap: cut -3 dB at 350 Hz (Q 1.4) to clear the boxy sound, boost +1.5 dB at 5 kHz (Q 0.8) for clap snap, and +1 dB shelf at 10 kHz.
4. MClass Compressor: ratio 2.5:1, attack 10 ms (lets the hit through first), release 100 ms, soft knee ON. Set the threshold so the needle moves 2–3 dB on hits, then raise the output back to the level you started with.
5. Pulveriser for grit: Squash 25, Dirt 15, filter open, volume matched. Blend it in so it's only about 20% of the sound. Dirt adds extra high tones that make the kick and clap thicker without flattening the hit.
6. Check it by muting the Pulveriser. You should lose "thickness" but not the punch. If you lose punch, lower Squash.

## Why this works
EQ first fixes the tone of the whole group, so the compressor reacts to a balanced sound and not a 350 Hz pile-up. The quiet grit adds harmonics without squashing the hits.

## Order of operations
EQ before compressor so it isn't reacting to mud. Grit last and parallel so the dry hit stays intact.

## Reason-specific trick
The bus channel's own Channel Dynamics can do the compression if you want one fewer device. The MClass shows more on its meter. Save the whole chain as "Trap Drum Bus.cmb".

## RE upgrade path
None required. The old notes suggested Softube Saturation Knob on the clap channel for extra crack. Unverified, check it exists in your Reason before relying on it.

## Technique you just learned
Bus-level EQ before glue compression. Works on any drum bus in any genre.

## Reference
21 Savage — "Bank Account": https://www.youtube.com/results?search_query=21+Savage+Bank+Account+official
