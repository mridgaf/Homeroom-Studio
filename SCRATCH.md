# Scratch (live reasoning trace)

Disposable. Cleared or overwritten each session. Purpose: capture the *path*
through a problem, not just the destination — so if I reverse course, the
reason is visible instead of lost.

One line per turning point. Not a transcript.

Format:
```
- [tried/considered] X → [result] → [kept / reversed because Y]
```

---

2026-09-14 — London strings + 70/30 freedom pass

- git: commit blocked → .git/index.lock (0 B, 09-13 18:23) held open read-only by the Claude app VM → moved to scratchpad → he pushed. Kept.
- Considered: strings "bog down" → measured 52,667 files / 4,263 on list / 5.8 s re-walk → he said never optimize for speed → dropped the cache idea. Reversed.
- Found: string_sampler pin (07-29) returned the pinned FILE + no pitch shift → C-E-G = C-C-C on 7 DJs. Verified on real list. Fix = pin section+style+mic, shift each note.
- Found: library recorded every other note → half-step off without shift. Folded into same fix.
- Style from vendor folder, not filename (Glissando files named sustain_*, SFX named 100_c) → kept 4 styles on his call.
- Kit sounds: open_soundbank made 14 DJs 100% random; he chose all 24 → 70/30.
- Low end: in-character rates kept; long 808 kick counts as the low sound (it was stacking with the 808 lane = lows on lows).
- Found in passing: _808_to_key "Bb".upper()="BB" → every Bb beat lost its 808. Fixed with key_context.pitch_class (it was in the low-end path being changed).
- Arps: planned a config edit for the 4 grammar DJs → did it in spec_for instead (ARP_CUT) → no config churn, no backup needed.
- test_one_instrument_plays_the_whole_beat went red: labels carry the figure ("bell stab"/"bell arp") → the guarantee is the instrument → _voices_of reads the first word. Not a weakening.
- Mutation checks: my first harness patched string_sampler.nearest but the test had imported nearest by name → false pass → patched the test module's name → red as expected. Trap 4.
- Started full suite, then saw collab_kit still legacy-open → killed at 27 tests, fixed, restarted. Tests must cover the rendering code. 1171 passed.
- Strings bench refused: premise "a = one file per chord" false (old pin re-picked >12 st) while the AUDIO said a = 1.0 of 3.5 notes → switched the premise to the audio ruler → delivered. Trap 4 again (proxy instead of output).
- Batch 2 outlier #96/#87 traced to pre-existing things (chip voice level, Night Metro breakdown dropping a chord's only trigger, build move) → named in README, not changed.
