# Handoff to Code: Answer melody + loop arrangement (drop-outs, fills)
## Part 1 of 4: what, why, scope, the owner, decisions

Read ALL four parts in order before doing anything. Each part ends with `=== END OF PART ===`.
If you did not see that line, you did not finish the part.
**Next:** Part 2 of 4.md (verified facts with code locations)

## Where this runs
Claude Code on the Mac (M2 Pro). It needs his `.venv`, the `/Volumes/TBOTC 3` drive, the full test suite (~1,456 tests, ~19 min) and renders. Not Cowork. Design-heavy: use a top model at high effort.

## What we're building (two phases, in this order)
**Phase A: an "answer" melody.** Today the beat's melodic parts are chord parts. The 2nd part ("lead" role) is only the chord's colour note (the 3rd/7th) moved up an octave, playing the SAME rhythm figure as the chords. Nothing plays a tune. Build a short melodic phrase that answers the chords: it plays in the gaps the chords leave, moves mostly by step in the key, lands on chord tones on strong beats, repeats a small motif with a change, and rests a lot.

**Phase B: arrangement inside the loop.** Drums already get small fills at phrase ends, and one DJ (Night Metro) has a drum drop-out. The melodic parts never change across the loop. Add musical moves: a short drop (chords/bass/melody stop for a beat or two before the loop restarts), a drum fill leading into bar 1, and an optional drop-out bar where only the kick and the bass, or only the chords, play.

## Why
- The bass groove (2026-10-19, kept by ear) fixed the layer with zero performance. The next most "AI/samey" thing, proven in code: no part plays a melody, and nothing in the melodic layer changes from bar 1 to bar 4.
- Production Research Hub Ch.04 Part 4 (synthesis, not sourced): "an unfilled hole at a phrase tail is scored FOR the soloist." These beats are for rappers. The melody must leave room for the vocal. **Sparse is the goal.**

## Out of scope (do NOT touch)
- The 808 rules (2026-09-23, confirmed by ear). The bass groove (just kept). Do not change `bass_rhythm.py` figures.
- Chord voicing, progressions, chord_rhythm figures.
- Song Sketch (`tools/song_sketch.py`, the 3:00 song from stems). Phase B is about the 4-bar loop itself. Ask the owner before touching Sketch (Part 4, Q3).
- Old beats: they must rebuild byte-for-byte (house rule). Stamp new beats only.

## The owner
- John. Not a programmer. Short, plain answers that lead with the conclusion.
- Do the work end to end. Never hand him steps you can do yourself.
- No guessing. Two readings that mean different work = BLOCKING question. Label anything not proven.
- Questions go as clickable options, and anything he must click goes LAST.
- **Never render beats unless his message asks for it.** This handoff's listening A/B counts only if his prompt asks for it.
- Tests before renders, never at the same time.
- He gave creative control on 2026-10-19 ("overrule old rules that keep this from sounding pro"). Do NOT overrule the 808 rules or "no machine tones". Log every overruled rule in DECISIONS.md, with the old rule quoted.
- Don't hunt problems in old beats.

## Decisions already made (with reasons)
1. **Melody first, arrangement second.** Each phase gets its own A/B. Two changes judged together can't be told apart.
2. **Stamp new beats only**, the way `chord_flow` and `bass_flow` are stamped in `add_bass_and_chords`. Suggested keys: `melody_flow` and `arrange_flow`.
3. **His samples only.** Never a synthesized tone (2026-07-25 and 2026-09-23 hard rules). One instrument per lane (`_one_instrument`).
4. **A loop/chip/MIDI-led beat gets no added melody.** theory/arrangement.md: "If a loop is playing, that's the one melodic part."
5. **Levels come only from written characters** (`groove.velocity`). No random wobble (2026-08-03).
6. **Copy the bass groove's buffer trick:** render the whole part as ONE loop-length, loop-safe buffer (`chord_synth.add_wrapped`), then cut it at the slot starts. That keeps phrases that cross a chord change, or the loop point, seamless.

=== END OF PART ===
