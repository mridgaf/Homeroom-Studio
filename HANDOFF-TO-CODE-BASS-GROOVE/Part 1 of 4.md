# Handoff to Code: Bass groove (bass performance grammar)
## Part 1 of 4: what, why, scope, the owner, decisions

Read ALL four parts in order before doing anything. Each part ends with `=== END OF PART ===`.
If you did not see that line, you did not finish the part.
**Next:** Part 2 of 4.md (verified facts with code locations)

## What we're building
A **bass performance grammar** for the sampled bass line, `tools/bass_rhythm.py`. It does for the bass what `tools/chord_rhythm.py` (2026-09-05) did for chords. Today the bass line plays **one note per chord slot**: the chord root, struck once on the slot's first bar and held for the whole slot. It has no rhythm, no lock with the kick, no passing notes, no ghost notes and no swing. That is a big, code-proven reason beats sound "simple / samey / AI."

The goal is per-identity bass figures (see Part 3): kick-locked, root-fifth, octave, walking with a chromatic approach, push (anticipation), funk with ghost notes, and the old hold kept as one option. They are baked into the slot buffer the same way chord_rhythm bakes chord figures, swung with the KICK lane's feel so the bass and drums lock together.

## Out of scope (do NOT touch)
- **The 808.** Owner ruling 2026-09-23 ("808 bangs with the kick, one note, never pitched") was confirmed by ear, and `OWN_808_RHYTHM_P` (2026-09-28) was the owner's own later tweak. Leave all 808 code alone.
- Drum generation (`pattern_gen`, `groove.py`). It already has MPC swing, Dilla per-lane offsets, velocity humanization and ghost notes. (An earlier chat message wrongly implied the engine plays on a dead grid. It doesn't; only a test script did.)
- Chords, progressions and voicing (deep chord pass 2026-10-19 is fresh; let him hear it first).
- Old beats: they must rebuild byte-for-byte as they were made (house rule).

## The owner
- John. Mac M2 Pro 16GB. Not a programmer. Wants short, plain, no-jargon answers that lead with the conclusion.
- Do the work end to end. Never hand him manual steps you can do yourself.
- No guessing or assuming. Label anything not proven. Push back if he's wrong.
- At the start of every task, say the cheapest model/effort that fits and whether chat, Cowork or Code fits.
- Questions go as clickable options (skill `clickable-questions`), and anything he must click goes LAST.
- Don't show download/click options for things already done.
- Every .md you write is split into parts like this one.
- 2026-10-19 he gave **creative control** for this work: "any old rules that keep you from making this as creative and pro sounding as you can make it, you get to overrule." Use it, but do NOT overrule the by-ear-confirmed 808 rules, and log every rule you overrule in DECISIONS.md with the old rule quoted.
- Don't hunt problems in old beats (standing rule).

## Decisions already made (with reasons)
1. **Bass first**, not more progressions. Reason: there are 79 progressions, and the 2026-10-19 deep chord pass raised the progressions in use from 38 to 62, yet the owner still hears sameness. The bass is the layer with zero performance logic.
2. **Bake the figure inside the slot buffer** (like chord_rhythm), and keep the lane's bar string as a single `X`. Reason: the lane's `X` triggers the whole slot buffer, so extra X's would retrigger the blob (chord_rhythm header explains this).
3. **Stamp new beats only**: `preset.setdefault("bass_flow", bass_rhythm.FLOW_VERSION)` in `add_bass_and_chords`, the same way `chord_flow` is stamped. `_build_chords` uses the new path only when `preset.get("bass_flow")`. Reason: rebuilds and A/B benches call `_build_chords` with the saved preset, so old beats keep their sound.
4. **Bass swing = the kick lane's feel** (offset, swing; small jitter). Reason: bass and kick should move as one unit; the 808 branch already copies kick swing.
5. **Levels come from written characters** via `groove.velocity` (X accent, x normal, o soft, . ghost). Never add random level wobble on top (owner rule 2026-08-03, enforced in chord_rhythm).
6. **Monophonic**: each bass note is cut at the next hit.
7. **MIDI export shows the real line**: a separate `bass` track in `write_midi`, so Reason gets the performance instead of a held root.

=== END OF PART ===
