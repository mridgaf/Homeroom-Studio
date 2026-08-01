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

## Current session (2026-07-31): "what would you rebuild differently?"

Owner asked for a ground-up rebuild critique from four expert angles. I
measured the rendered audio instead of only reading code. That changed the
answer.

- [considered] answering from code structure alone (4.5k-line monolith, 200KB
  of JSON config, hand-rolled numpy DSP) → all true, but style complaints, not
  evidence → reversed: measured the actual WAVs.
- [verified] 493 beats, 60 stem folders, 506 stem files, read with stdlib
  `wave` + numpy — `soundfile` is not even installed, confirming zero audio
  libraries in the venv.
- **[verified] 247/247 core stems (kick, snare, every chordN) are exactly
  dual-mono**, max|L−R| < 1e-9. Master-bus side energy sits 22–31 dB under
  mid. The mix is functionally mono. The owner's recurring "everything is
  stacked on top of each other" complaint is literal: every part occupies the
  identical point in the stereo field. Four sessions (2026-07-25, 2026-07-29)
  chased this as a *sample-sourcing* problem. Those fixes were correct on
  their own terms but could never resolve the symptom, because the cause is
  spatial, not tonal.
- [verified, and CORRECTED from my first reading] the mono result is not
  "nothing is panned." Read the real lane tuples in `.recipes/1623.json`:
  hat −0.15, blips +0.30, stamp −0.30, congas +0.29 — the garnish *is* panned.
  What sits at a hardcoded `0.0` is kick, snare, sub, bass **and all three
  chord parts** (`beat_machine.py:1535`, literal `0.0` for every `chord{i}`
  and `chord{i}v{v}`). Centring kick and snare is correct engineering practice;
  centring three simultaneous harmony parts on top of each other is the actual
  defect. Narrower claim, and the right one.
- **[verified] melodic content is buried**: loudest chord part vs kick across
  39 beats — median −15.4 dB, worst −24.9 dB. Traced to a single constant:
  `OWNER_TASTE["chord_gain"] = 0.3` (−10.5 dB) in `groove.py`, times an accent
  of 0.82–1.0.
- [verified] the silent-stem root cause is not a render fault: the `blips`
  lane in 1623 has **zero hits in every bar** (`----------------`) while still
  carrying a sample, a pan of 0.30 and a gain of 0.26. A lane can be dealt into
  the kit with an empty pattern and the renderer writes the empty stem anyway.
- [verified] simulated the two-line fix on 1623 without touching the repo:
  panning the three chord parts to −0.45/0/+0.45 and lifting chord_gain to
  0.55 moves whole-mix width from −24.0 to −17.8 dB S/M and the chord-to-kick
  gap from −11.0 to −5.7 dB. Improves both; does not fully reach a −6…−12 dB
  width target, because kick/snare/sub are correctly centred and dominate.
- **[verified] 17 of 506 stems (3.4%, 15 of 60 folders) are digital silence**
  (peak < 1e-6) while listed as live lanes. Checked 1623: `blips` carries a
  kit spec and gain 0.7 in `.recipes/1623.json` and appears in `lanes`, but
  `blips - Double Whip.wav` is all zeros. Not an intentional mute.
- [verified] tonal balance unmanaged: sub-60 Hz energy ranges 0.6% (1621) to
  70.4% (1622) beat to beat. No reference curve anywhere in the codebase.
- [verified] 732 tests pass in 97s and catch none of the above — they assert
  on dicts and code paths, never on audio properties. An earlier session did
  measure LUFS and peak once by hand (see #859-863 below), so the capability
  existed; it just never became a gate.
- [verified] no song structure: 4–8 bar loops only, no intro/verse/hook.
- [verified] autoresearch optimized *variety* for 35 runs, plateaued at 14.08
  against a 0.15 noise floor, shut itself off (`.autoresearch-off`). Goodhart:
  variety was measurable so it got optimized; musicality wasn't so it didn't.

### Code-audit findings (subagent), each re-verified by me before use
- **[verified myself] `master()` applies its EQ to nothing.**
  `make_drum_loops.py:173-195` captures `m = 0.5*(L+R)` BEFORE the EQ, EQs L/R,
  takes `side` from the EQ'd pair, then reconstructs `L,R = m+side, m-side`
  using the STALE pre-EQ mid. Ran it: on centred content the air shelf changes
  the tilt by **−0.009 dB**; on side-only content, **+2.509 dB**. Combined with
  the dual-mono finding above, the air shelf and boxy-mid dip have never
  audibly applied to any beat this project has rendered.
- **[verified myself, severity CORRECTED] naive `np.interp` resampling.** The
  subagent called the load path "the single worst defect." My measurement does
  not support that: 0 of 265 sampled library files are 88.2/96k and 18.5% are
  48k, whose aliases fold to 20–22 kHz — inaudible. Where it *does* bite is the
  **upward pitch-shift** path (`instrument_sampler._shift`, PREFER_MAX_SHIFT=12
  since 2026-07-29): a 15 kHz component shifted +12 st returns as a phantom
  14.1 kHz tone, and broadband bright material refills its top octave with
  fold-back instead of emptying it (−5.9 dB where a clean shift gives far more).
  That is the grainy top end on shifted hats/plucks — a melodic-path defect,
  not a load-path one. Reported at that severity, not the subagent's.
- [verified by the subagent, not re-run by me] swing is applied only when
  `res == 16` (`crew.py:972`), so the 32/24/20/12-step grids that
  `pattern_gen` emits for rolls32/quint20/triplets/shuffle/odd-meter get none —
  the config advertises swing as identity-defining and the renderer drops it
  for four of five grids. `glue_compress` has attack == release; `master_to_lufs`
  is a `tanh` waveshaper, not a limiter. `haas`, `kick_layer` and
  `transient_shape` are written, tested, and never wired into a render.
- [verified by the subagent] stems and mix are two independent sums of the same
  lane buffers (`crew.py:1049-1064` vs `:1067-1103`), diverging at four points;
  `_track_gain` is 44 lines of RMS reconciliation compensating for the fork.
  This is the mechanism behind three separate "stems don't match the track"
  reports (07-21, 07-23, 07-25), each patched downstream of the cause.
- [verified by the subagent] `crew.py:653-681` silently rewrites his
  `crew_config.json` on a STYLE_VERSION bump unless `_style_lock` is set —
  against the file's own "_readme" promise that editing a number sticks.

### The reframe this forced
Across 76 ledger entries the recurring failure is not bad code — it is that
**every real defect was found by the owner's ear, never by the machine.** The
system cannot hear itself. That is the one architectural thing worth changing,
and it does not require a rebuild.

- [considered] recommending a full ground-up rewrite → reversed: 25k lines,
  732 green tests, 1623 beats rendered, engine in use today. Every defect
  measured above lives in the *output stage* (pan, gain, silence, balance),
  not in the composition brain. Rewriting the brain to fix the mixer is the
  expensive wrong move.

## Previous session (phase 2 sourcing)

- owner moved to phase 2 (bass/vox lanes), then interrupted with two terse
  sourcing directives: "stop the one shot rule" + "only my folders (given +
  already used)". Treated those as the authoritative instruction; did NOT
  build bass/vox placement blind.
- directive 2 (whitelist): the whole-drive name-token scan (FOLDERS incl.
  "/Volumes/TBOTC 3" root) was the leak path to his songs → build_shots now
  scans load_roots() only. melodic_loops/string_sampler already scoped.
- directive 1 (one-shot rule): scan_packs dropped LOOP_FILE_RE + MAX_SECS cap
  (→ SANITY_SECS 45 only), un-excluded LOOP/FILL/BASS/VOX/VOCAL/ACAPELLA,
  added bass+vox roles; build_shots dropped the category==one-shot filter.
  Kept instrument folders excluded from the DRUM pool (melodic loops have
  their own scanner) + all safety filters.
- proved it: 6936 files, 0 outside the whitelist, 0 his-song, 0 banned.
  bass 0→1056, vox 0→427, all drum roles up. 468 tests green (rewrote the
  one v6 test that encoded the old one-shot spec). Cutz #946-948 audition
  clean + gated.
- deliberately STOPPED before placement: bass/vox are in the library but no
  lane uses them, and loops in drum roles only play their choked attack.
  Flagged (a) sampled-808 root-sub, (b) vox guest lane, (c) loop lane as the
  next audition-gated step — the loop-playback one is a real fork for him.

- owner: "Full loop" → built phase-2 placement: _add_sample_lanes in
  beat_machine adds bass/808, vox, and full-loop lanes (reuse the sub/chord
  preload pattern; render already ducks all non-kick lanes so they breathe).
- loops re-architected: scan_packs now TAGS loops into a "_loops" bucket with
  bpm + a tonal flag, instead of my earlier flatten-into-drum-roles. Loop lane
  = bpm-matched (±6, no time-stretch), PERCUSSIVE roles, ATONAL only.
- two musicality bugs caught by AUDITIONING (not reading the diff):
  (1) tonal loops (Synth_Lead...D#m) clashing → added the tonal filter (key or
  melodic word in name); (2) an "808 Loop" leaking into the bass one-shot pool
  → traced to the whole-drive INDEXER pass (no loop-tagging) → dropped it
  entirely (redundant now that sourcing = pack roots only). scan_packs is the
  sole source.
- verified: 0 loop-named leaks into one-shot roles, 397 usable loops, Mustang
  #975-982 clean (BIZKEL perc/hat loops, Cymatics 808s, @hiheazy/OHH! adlibs),
  gate 8/8, 469 tests. Pool shrink (clap 345→77) is the whole-drive pass going
  away per "only my folders" — expected, not a regression.

- owner after hearing the loop batch: "drum loops cause problems, exclude
  them, there are enough drum sounds" → removed the loop lane outright (no
  knob to tune; he named cause + reason). Bass/vox lanes stay.
- deliberately KEPT the scanner's loop tagging even though nothing reads it:
  the tagging is what keeps loops OUT of the choked drum roles. Deleting it
  would have shoved drum loops back INTO the drum lanes — the exact opposite
  of the ask. The _loops bucket is now the exclusion pile.
- turned the phase-2 test into a regression guard: it still feeds a
  bpm-matching loop pool and asserts NO loop lane/stem, so the feature can't
  creep back. 469 green; 6 renders confirm bass present, zero loops.
- found 17 already-rendered beats carrying a loop lane — did NOT touch them
  (his files, may be keepers); listed them and offered a reversible move.

- owner: beats #1000/#1002 have "a weird vocal sound... doesn't show up in
  the stems" and worried it's from his own songs → checked the ACTUAL Stems
  folders on disk before touching any code. Real vox stem files existed
  ("Smoke vocal", "Scary Gary Vocal") — not his songs, just invisible to the
  app. Redirected from "leaked sample" panic to the real bug.
- root cause: spec_used (the recipe kit_spec everything reads: stems list,
  swap, kit_paths, history) snapshots preset["kit"] right after build_kit —
  BEFORE sub/chords/bass/vox ever run. Bass/vox rendered real audio (that
  path is preset["lanes"]/kit, untouched) but never wrote into preset["kit"],
  so the snapshot missed them entirely. Audio correct, bookkeeping stale.
- fix: bass/vox now register into preset["kit"] like any real sample lane;
  ONE generic refresh line after _add_sample_lanes re-derives spec_used +
  lane_parent from whatever's in preset["kit"] by then — not a bass/vox
  special case, so any future post-hoc lane gets this for free.
- deliberately did NOT extend the fix to sub/chordN (synthesized, no
  shots[role] to swap from — registering them would let a click "swap" into
  silence). Named that as a separate pre-existing gap, not silently patched.
- verified against the exact function the running app calls (_beat_stems),
  not just the data shape — confirmed bass/vox show up unlocked/swappable.
  469 tests green. Did not restore #1000/#1002 — owner already trashed them,
  fix is forward-looking only.

- owner: "control the volume for All sounds" → meant the synthesized lanes
  (sub, chordN) I'd deliberately left non-swappable last fix. Checked first:
  the trim MECHANISM already existed end-to-end (backend validates against
  preset["lanes"] not kit_spec; JS already renders a slider for locked
  rows, comment literally says so) — the ONLY gap was _beat_stems building
  its list from kit_spec+stamps only. One-line widen.
- did NOT stop at "looks right" — manually drove a real chords+bass+vox
  render through _beat_stems AND an actual rebuild to prove the slider
  really works end to end, not just that it appears.
- that verification caught TWO more bugs the fix made reachable for the
  first time: (2) sources["bass"]/["vox"] held a decorated display string
  ("vox: name") instead of the raw path every other lane uses → rebuild
  tried to reload a file literally named "vox: ....wav" and crashed. Fixed
  by matching the existing convention (sources[lane] = path). Bonus: this
  also fixed the "vox_" typo in stem filenames from earlier this session.
  (3) trimming a CHORD lane crashed outright (KeyError) — chord/bass-chord
  audio is synthesized, had ZERO rebuild-reconstruction path (pre-existing
  gap since 2026-07-22, just never reachable via the UI before today).
- for (3): considered reusing the already-rendered STEM file instead of
  regenerating → rejected, stems are already panned+ducked, reusing would
  double both. Considered persisting the typed notes-box override to
  guarantee exact rebuild match → rejected, that breaks the explicit house
  rule "notes box steers one click, never persisted." Went with: extract
  the chord-building block into _build_chords(), fully deterministic from
  variant (same trick _root_sub already uses), call from both generate()
  and swap_many. Disclosed the two narrow limits (typed override, library
  drift) in the docstring instead of silently risking them.
- caught the SUBTLE trap before shipping: does a SECOND sequential trim on
  the same chord lane stack, or does regenerating stomp it back to default?
  Tested explicitly (round1 +5dB, round2 +2dB → must multiply, not reset).
  First pass would have reset it; fixed by preserving existing gain when a
  lane row already exists, only refreshing pan/feel/bars/audio.
- 470 tests green, live numeric verification against the real library
  (0.8891 → 1.1194 across two rebuilds, matched exactly).

## Previous session (Mustang)

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
