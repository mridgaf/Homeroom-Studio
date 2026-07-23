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

## Current session (Mustang)

- goal: next legend = Mustang → checked HARMONY-IDENTITY-PROPOSAL first: he
  is NOT in it (only 4 legends were researched, all now built) → wrote the
  signature from general DJ Mustard knowledge and said so plainly in the
  `_note` + ledger rather than dressing it up as sourced.
- ladder check before adding anything: modes/progression slugs/arp path all
  already exist → the only new thing is `vamp_static_riff`, and only because
  Mustang is its first real consumer (prior sessions skipped it as config
  nothing read). No engine change at all this time.
- considered adding a notes-box word for the new slug → skipped: Dre's
  gfunk slug got no word either, and 6 of 14 slugs have none. YAGNI.
- rendered 6 (#890-895), stems showed synth-only + 5 arp/1 pad as designed,
  but the static-riff beat drew the held pad → rendered 3 more (#896-898) to
  try to catch static+arp; #897 drew static+pad AGAIN.
- suspected a seed correlation (prog seed v*419+5 vs rhythm seed v*733+11,
  and rhythm shares its exact seed expression with roll_swing) → simulated
  10k variants → 37.2% static+arp, no correlation, just a ~6% unlucky pair.
  Stopped rendering rather than chasing a roll; reported the gap instead.
- second render RESET last_batch to just [896,897,898] (set_last_batch, not
  append) → set it back to all 9 so the player shows the whole audition.
- MIDI gate FAILED all 9 → checked Timberline + J Dillo before blaming my
  own change; they failed identically → the gate predates chord beats and
  treats the deliberate channel-1 chords track as an error. Fixed the gate
  (require ≥1 ch10 note + GM range on ch10 only), verified with 3 synthetic
  bad files that it still catches real faults.
- owner: "Allow DJs to stay true to style. with the Kick." → reversal of
  yesterday's engine-wide clean-punch. Chose DELETION (drop _clean_punch +
  both call sites) over adding a per-DJ 808 exemption flag — every entry's
  kick_flavors weights already ARE the style statement, and Dre's clean
  lean is already encoded there (0.1 vs 0.75), so no special case needed.
- grepped both call sites again before declaring done (the odd-meter path
  rolls its own flavor — same trap as when the rule went in). Also caught a
  stale comment in beat_machine.py still naming the deleted function.
- first 3 renders came out 2 clean / 1 808 — WRONG for a 0.6/0.4 lean →
  read pattern_history.json instead of blaming the roll: flavor history
  stores a positional INDEX, and removing the filter changed what index 0
  means, so the streak-breaker read 9 phantom "808s in a row" and forced
  clean on #899/#900, then forced 808 on #901. All three were dictated, not
  rolled. Re-rendered #902-904 with the history back in the new index space
  → 1 clean / 2 808, matching the weights. Told him rather than passing off
  the first three as the answer.
- side win: the static-riff + arp combination I couldn't get to roll last
  turn landed 4 times across #899-903.
- left ADD_THE_ROOT_808 off — the root sub is a bass layer, not the kick
  flavor, and he named the kick only. Carried it as a question, not a guess.
- owner: "Add the root sub back." → flipped the flag. Verified by RENDERING
  (5 traditional beats to a scratch dir, fixed seeds) rather than reading the
  diff: 3 got the sub, and the 2 that didn't were exactly the long-808 kicks
  the guard is supposed to skip. Real stem + recipe root_note confirmed.
- rendered to a scratch --out dir, not the library — proving a flag works
  shouldn't leave beats he didn't ask for in his folders.
- found the feature had ZERO tests, which is why it silently went off and on
  in a day → added one, seeding `random` so the 3-in-4 roll is deterministic
  instead of a flaky "render until it lands" loop.
- also fixed a comment that had been wrong since the feature landed ("3 in 5"
  vs the code's 0.75).

## Previous session

- goal: move harmonic-identity work to the next legend now that Dre is
  approved → picked DJ Premium (lowest-risk of the 4 researched legends, zero
  new engine needed) → added signature block, 468 tests green, rendered
  #864-866 audition batch.
- owner approved Premium, said "do dillo" → added J Dillo signature (1:1
  minor/major roll per the proposal's own Dilla-isn't-minor-default
  correction, loop-source leaned 4:1) → rendered #867-869, mode hit both
  ways, 6/7 chord slots real loop samples → waiting on owner's ear.
- last researched legend after this is Timberline (Timbaland) — flagged its
  odd dual-tempo-range (90-100 vs 135-145) as needing a decision before
  building, not a default I should just pick silently.
- owner feedback on #867-869: didn't like the 8-bar A/B form ("completely
  changes halfway through"), wants shorter loops → no CLI knob for this
  (nbars/form roll purely inside pattern_gen.compose(), no direction-word
  hook), so rendered 8 (#870-877) and filtered by the report's own
  "N-bar loop" vs "N-bar A/B" line rather than adding a new flag for a
  one-off ask → kept the five 2/4-bar straight loops (870, 873-876),
  triage()'d the three 8-bar ones to Trash (871 8-bar loop, 872 + 877
  8-bar A/B), reset last_batch to just the 5 so the player shows exactly
  what was asked for.
- owner: "include a variation between these two beat lengths. for this DJ.
  No Long Beats." → made it permanent, not just a filter: new `bar_lengths`
  preset key in pattern_gen.compose() (pins the nbars roll to a fixed pool
  when set; unset = old 2/4/8 weighted default). J Dillo = [2,4]. 468 tests
  green, rendered #878-883, 3-and-3 split, zero 8-bar.
- owner: "Move on to Timberland [sic]. Allow for tempo variations in both.
  Suggested Tempos." → resolved the flagged dual-pocket fork: extended
  beat_machine.py's tempo-lean to accept a list of [lo,hi] pockets (rolls a
  pocket then a tempo inside it — a %-lean can't jump between two
  disconnected pockets from one base bpm). Timberline signature: phrygian,
  dark_menacing only, synth-only chord_source (rhythm-defined per the
  proposal, plain pad reads as the closest thing to a drone), tempo
  [[90,100],[135,145]] — the proposal's own two researched pockets, offered
  as the suggested tempos. 468 tests green, rendered #884-889: bpm hit both
  pockets (100/93 low, 139/135/136/138 high), all phrygian/dark_menacing,
  stems confirmed synth-only. This closes the 4-legend research proof set.

## Previous session (archived into DECISIONS.md 2026-07-23)

- goal: continue chord-synth integration → 3 Dre audition beats → traced the
  render, found the identity-blind seam (beat_machine ~L1017: random root,
  hardcoded minor, no chord_source) → wired a signature chooser instead of
  patching one call site.
- chose strings-as-source (built, never wired) over the deferred synth-lead
  voices → Dre is the proposal's pick precisely because he exercises strings.
- kept `signature` a deep-copied preset key (normalize_preset preserves unknown
  keys) → zero loader changes, no-signature path stays byte-identical.
- first render batch #842-844 looked all-synth-pad → was a stem-glob bug (Doc
  Day folder holds every beat's stems); real stems showed strings landing.
- but sustain family included legato (~2s) → tiled 4-5x on ~10s chords → dropped
  leg from ARTIC_FAMILY, retired #842-844 to Trash, re-rendered #845-847 clean.
- added only gfunk_minor_i_iv_v (Dre's slug); skipped the 2 slugs for
  G-funk/Miami as config nothing reads yet.
- owner feedback on #845-847: "847 out of key at the end, none sound like Dre."
  → FFT/nearest check proved pitches were correct (not a bug); root causes were
  #847's m7 (vamp_i_iv7) + the held-drone voice.
- fixed m7 (Dre = triads only), then asked direction → owner: "rhythmic riff".
- built arp as one buffer per chord (rhythm baked in) not multi-lane → keeps all
  the lane/bass/MIDI wiring + clean stems; gated on signature chord_rhythm=arp so
  every other identity's held chord is untouched.
- synth-arp (pluck) smears under beat reverb (onset detector saw 1), strings-arp
  stays crisp; raw arp verified rhythmic (16 onsets). Left pluck decay for the
  ear to judge rather than tuning blind. Re-rendered #848-850.
- owner's real favorites: #843 (m7, held, strings), #845 (gfunk, held, mixed
  voice), #849 (gfunk, arp, mixed voice) → the m7-removal and strings-only
  calls from last entry were WRONG per the owner's own ear; #847 was never
  about the chord quality. Reversed both, made rhythm+source a per-beat roll
  instead of picking one fixed answer.
- mid-task found a partial auto-edit already in the file (chord_rhythm roll +
  vary_preset tempo clamp — good, kept) but with stale values (90-93 not 90-96,
  strings-only not 2:1, m7 still missing) → chat instructions are the source of
  truth over an unreviewed file edit, corrected all three against what the
  owner actually typed.
- "constrain kick to clean-punch, ignore 808" — asked Dre-only vs engine-wide
  since engine-wide kills a real owner rule (2026-07-18 "add the root") and
  collides with G-funk/Memphis/Miami-bass's OWN 808 identity from yesterday's
  proposal doc → owner said engine-wide, proceeded (reaffirmed = decided).
- grepped every caller before declaring the kick filter done (ponytail
  discipline) → found _compose_odd (3/4, 6/8 path) rolls kick_flavors
  independently of compose()'s main path → would have shipped odd-meter beats
  still reaching 808 if I'd stopped at the first call site.
- checked how many DJs actually have a 2nd non-808 kick flavor to fall back on
  → ZERO, roster-wide (every style is one clean + one 808, never two clean) →
  "no 808" quietly also means "no kick variety" for literally everyone. Real
  finding, not hypothetical — flagged plainly, didn't hide it in the render.
- 2 of 5 rendered kicks had "808" IN THE FILENAME despite the clean-punch
  filter → looked like a possible leak → read crew._load_choked, confirmed
  every kick is hard-truncated to the flavor's 0.2-0.5s choke regardless of
  source file name/length → sample-pack branding, not a real miss. Verified by
  reading the choke code, not by trusting a tag or a noisy DSP heuristic (first
  attempt at measuring "is this really short" by decay-time was too noisy to
  trust; the choke code is the authoritative answer).
- test_pattern_gen.py had 2 tests asserting the OLD "808 reachable" behavior —
  rewrote both against the new verified reality rather than leaving them red;
  also had to fix my own bug in the rewrite (compose() mutates in place and
  returns notes only, not (preset, notes) — mis-unpacked a list as a tuple
  once, TypeError, fixed).
- rendered #859-863 last: tempo 96/90/93/96/90 (all in range), kick
  clean/short punch+knock on all 5, chord_rhythm 2 arp + 3 held, progressions
  4 gfunk + 1 vamp (m7 confirmed reachable again), chord source strings in all
  5 + synth-arp in 2. All LUFS -13.0, peaks -5.7 to -6.1 dBFS. Not yet
  committed — waiting on owner sign-off same as every batch this session.

(clear this section at the start of a new session, or archive worth-keeping
lines into DECISIONS.md's Reasoning field first)
