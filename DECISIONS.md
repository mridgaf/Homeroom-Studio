# Decision Ledger

Read this at the start of a session. Append to it at the end. Update `status`
on old entries when you learn what actually happened — don't just pile on new
entries.

## Entry format

```
### [YYYY-MM-DD] Short title
- Context: what was going on / what problem this addressed
- Decision/change: what was actually done
- Reasoning: why this over the alternatives
- Verify by: how to check if this held up (test, re-check, "ask user next time")
- Status: open | confirmed | failed
- Outcome: (filled in later, when known)
```

---

## Log

(new entries go below this line, most recent first)

### 2026-07-23 Drum-loop lane REMOVED after one audition batch
- Context: owner heard the first loop-lane batch: "The drum loops cause
  problems. Exclude drum loops — there are enough drum sounds." The lane was
  only a day old (he'd asked for "Full loop" that morning).
- Decision/change: deleted the loop block from `_add_sample_lanes`, plus
  LOOP_LANE_P / LOOP_BPM_TOL and the now-dead "loop" notes-box mute word.
  Bass/808 and vox lanes are untouched and stay. KEPT the scanner's loop
  tagging (`_loops` bucket + bpm/tonal flags) on purpose: that tagging is what
  keeps a loop OUT of the one-shot drum roles, so removing it would send drum
  loops straight back into the drum lanes as choked hits — the opposite of
  what he asked. Nothing reads `_loops` now; it is the exclusion pile.
  Melodic/in-key loops are unaffected — they reach beats via the chords
  feature's own scanner, not this bucket.
- Reasoning: he named the cause (drum loops layered over a programmed kit) and
  the reason (enough drum sounds already). No knob to tune — the feature goes.
- Verify by: 469 tests green; renamed the phase-2 test to
  test_phase2_bass_and_vox_lanes_but_never_a_drum_loop — it still loads a
  bpm-matching loop pool and now asserts NO loop lane/stem appears, so this
  can't silently come back. 6 fresh Mustang renders: bass lanes present, zero
  loop lanes.
- Status: confirmed
- Outcome: 17 already-rendered beats still contain a loop lane (#950, 951,
  952, 953, 955, 957, 959, 960, 964, 966, 967, 970, 973, 974, 978, 979, 981).
  Left in place — they are his files and some may be keepers apart from the
  loop. Offered to move them to Trash (a reversible folder move) on his word.

### 2026-07-23 Phase 2 placement: bass/808, vox, and full-loop lanes
- Context: after the sourcing rework, owner said play loops as a "Full loop."
  Built the three phase-2 lanes (bass/808, vox, full loop) using the existing
  preload-audio-into-a-lane pattern the sub/chord lanes use.
- Decision/change:
  * Loops now TAGGED, not flattened. scan_packs marks a loop (LOOP folder or
    loop/bpm name) into a "_loops" bucket with its bpm + a `tonal` flag,
    instead of choking it into a drum role. New helper `_add_sample_lanes` in
    beat_machine (called after the chord block) adds up to three optional,
    per-beat-seeded lanes: LOOP (a bpm-matched PERCUSSIVE, ATONAL loop tiled
    loop-safe across the whole beat via fit_loop, gain 0.4), BASS (a sampled
    808 under the kick on non-chords beats — no tuning, no key to clash),
    VOX (a sparse chant/adlib on phrase accents). Rates SAMPLED_BASS_P .4 /
    VOX_LANE_P .3 / LOOP_LANE_P .35 — none in every beat. Notes box can mute
    each ("no loop/vox/bass").
  * Dropped the whole-drive indexer pass from build_shots entirely — with
    sourcing already restricted to the pack roots it was redundant AND, lacking
    the folder-aware loop/tonal tagging, it leaked drum loops ("808 Loop") into
    the one-shot bass pool. scan_packs is now the single source.
- Reasoning / two musicality bugs caught in audition, both fixed:
  (1) tonal loops (a "Synth_Lead...D#m") laid untuned over the beat clash —
  the loop lane is now PERCUSSIVE roles {perc,hat,bongo,fx} AND `not tonal`
  (a key or melodic word in the name = belongs to the in-key chord feature).
  (2) off-tempo loops drift (fit_loop doesn't time-stretch) — loop must be
  within ±6 bpm of the beat.
- Verify by: 469 tests green (added test_phase2_bass_vox_and_full_loop_lanes:
  forces the rolls on, asserts all three lanes + a loop stem land, and that
  the notes box mutes them). Live: 0 loop-named files leak into one-shot
  roles; 397 usable percussive/atonal/bpm-known loops, 21 keyed-percussion
  correctly excluded. Mustang #975-982 audition: clean loops (BIZKEL Perc/Hat
  Loop), real 808s (Cymatics Oracle 808), real adlibs (@hiheazy, OHH!),
  bass+vox+loop stems written, MIDI gate 8/8.
- Status: PARTLY FAILED — bass + vox confirmed and kept; the LOOP lane was
  rejected on audition the same day and removed (see the entry above this one)
- Outcome: pool sizes dropped from the earlier whole-drive numbers (clap
  345→77, snap 38→23, etc.) — that's the whole-drive name-token pass being
  removed per "only my folders"; those were loose off-pack matches. Real
  claps still 77 + open-soundbank means any lane can also pull perc's 1065.
  The loop lane lasted one batch: layering a loop over an already-programmed
  kit was the problem, exactly the clash risk flagged when it was designed.

### 2026-07-23 Sourcing rework: whitelist the folders + stop the one-shot rule
- Context: two owner directives (mid-turn, terse): (1) "Stop using the one shot
  rule." (2) "Only use samples from the folders I gave this session and ones
  already being used." Both are about SOURCING, not placement.
- Decision/change:
  (2) Whitelist — build_shots() sourced its name-token pass from
  `scan(FOLDERS=["/Volumes/TBOTC 3","~/Documents","~/Music"])`, i.e. the WHOLE
  drive, which could pull his own songs. Changed to `scan(load_roots())` — the
  pack roots in sample_packs.json, which ARE the given + already-used folders
  (this session's new packs were consolidated into one of them last entry).
  melodic_loops and string_sampler were already scoped to load_roots()/the
  strings folder, so no change there.
  (1) One-shot rule — in sample_library.scan_packs: dropped the LOOP_FILE_RE
  skip and the per-role MAX_SECS cap (replaced with a single SANITY_SECS=45 that
  only rejects full-length songs). Removed LOOP/FILL/BASS/VOCAL/VOX/ACAPELLA
  from EXCLUDE_DIR_WORDS. Added `bass` and `vox` as real roles (DIR_ROLES +
  SHOT_WORDS). In build_shots, dropped the `category != "one-shot"` filter.
  Instrument folders (MELOD/CHORD/SYNTH/KEY/PIANO/GUITAR/INSTRUMENT) stay
  excluded from the DRUM pool — melodic loops reach beats via their own scanner
  ("drums and melodic loops... before going further").
- Reasoning: both directives are pure sourcing; playback already chokes a
  sample to its lane length, so admitting loops/long files can't make a drum
  lane run long. Kept all safety filters (banned, BAND_TOKENS, /Claude Drum
  Beats/, non-audio).
- Verify by: 468 tests green (rewrote test_pack_scan_classifies_by_folder to
  the new spec — loops/long-tails now KEPT, added bass/vox coverage). Live
  scan: 6936 distinct files, **0 outside the whitelisted roots, 0 band-token
  (his-song) files, 0 banned**. Pools grew: bass 0→1056, vox 0→427, perc
  1343→1805, fx 654→860, crash 281→412, hat 789→971, kick 1053→1138, snare
  991→1056. Audition #946-948 (Cutz) rendered clean, LUFS -12.8/-13.2/-13.1,
  MIDI gate green.
- Status: confirmed (sourcing); placement OPEN
- Outcome: HONEST GAP — bass + vox are now in the LIBRARY but no lane USES them
  yet, and loops sitting in drum roles only play their choked attack. Making
  bass/808 and vox audible as their own lanes, and playing loops AS loops, is
  placement work (next step, audition-gated): (a) sampled 808/bass as an
  alternate to the synth root-sub on traditional beats (no tuning needed — plain
  beats have no key), (b) a sparse vox guest lane via the existing guest
  machinery, (c) a loop lane (reuse melodic_loops' tempo-fit) — the one real
  fork to confirm with him before building.

### 2026-07-23 Sound-library expansion, phase 1: Downloads packs consolidated onto TBOTC 3
- Context: owner wants his whole sample library active (he listed 37 folders),
  his own songs excluded as always. Decisions: option B (consolidate onto the
  external drive), commercial/ripped kits included ON PURPOSE (his call,
  confirmed twice), scope = drums + melodic loops now, bass/vox lanes later
  behind an audition.
- Decision/change: no new library folder and no config change — the existing
  scanned root "DAW Projects/Sample Packs - Downloads Backup" IS the
  consolidation point (it's literally the Downloads-packs backup). Verified 13
  of his 37 folders were already active; of the 7 Downloads folders, rsync
  dry-runs proved "reddit drum kits 2023" and "FREE giveaway collection 2022"
  are byte-complete on TBOTC already, and "808 3" duplicates "reddit.../808".
  Only true new material: Mike Zara's Stash (532 MB/1251 files) and Testing
  Drum Kit (13 MB/18 files) — COPIED (originals untouched) into the root,
  manifest appended at the destination.
- Reasoning: copying into the root the scanner already reads means zero code,
  zero config, no duplicate pool entries, and one obvious place to drop packs
  forever. Skipping the dupes matters because sample history keys on path —
  two paths to one sound would defeat anti-repetition.
- Verify by: pool counts before/after the copy: kick 743→1053, snare 701→991,
  clap 160→345, hat 609→789, perc 1125→1343, rim 88→174 (+1446 entries total,
  and entries traced to the two new packs = 1432+14, exactly the gain — the
  growth is all them, no accidental scope creep). Melodic loops 2013→2013:
  Zara's stash is drums-only, honest zero.
- Status: confirmed
- Outcome: 4 of Testing Drum Kit's 18 files didn't index — one is an .mp3
  (scanner reads wav/aif only; ffmpeg install is the known fix, deferred),
  rest lack drum tokens. Phase 2 (bass/808 + vox lanes) NOT started — owner
  wants audition first. His Downloads copies can now be deleted BY HIM if he
  wants; never by us.

### 2026-07-23 "Add the root" turned back ON — and finally given a test
- Context: the tuned-808 root sub (owner rule 2026-07-18) was switched off
  earlier the same day as collateral of the engine-wide 808 ban. That ban was
  reversed for the kick; I left this flag alone since he'd named the kick only,
  and asked. He said add it back.
- Decision/change: `beat_machine.ADD_THE_ROOT_808 = True`. The mechanism was
  flag-gated rather than deleted when it was retired, so it really was a
  one-line flip — nothing else needed restoring. Also corrected the stale
  comment above the call site: it claimed "about 3 in 5" (and DECISIONS once
  said 40%), but the roll has been `< 0.75` since the feature landed and was
  never edited — so it's 3 in 4 of traditional beats, and traditional is a
  quarter of a batch, ≈ 1 beat in 5 overall.
- Reasoning: he asked for it directly; the guards that make it behave (skip
  when the kick is already a long 808, skip on chords beats where harmony's
  own bass owns the low end) were untouched and still correct — more relevant
  now that 808 kicks are reachable again.
- Verify by: rendered 5 traditional beats to a scratch dir over fixed seeds.
  3 got the sub, 2 skipped — and both skips were the beats whose kick had
  rolled a long 808, which is exactly the documented "don't stack two subs"
  guard. Confirmed the real artifacts on one: stem file "sub - synth 808 sub,
  root Bb.wav" and `root_note: "Bb"` saved in the recipe.
- Status: confirmed
- Outcome: **the feature had NO test** — that's how it round-tripped off and
  on in one day with nothing noticing. Added
  `test_add_the_root_puts_a_tuned_sub_under_traditional_beats`: seeds `random`
  so the 3-in-4 roll is deterministic instead of "render until it lands",
  asserts the sub lane + the named stem + the recipe's root_note, and asserts
  a chords beat still skips it. 468 tests green.

### 2026-07-23 Kick flavor goes back to per-style — engine-wide clean-punch reversed
- Context: after hearing that Mustang's own identity line is "a sparse 808
  kick" and that the engine-wide clean-punch filter left every DJ exactly one
  kick sound, the owner said "Allow DJs to stay true to style. with the Kick."
  That reverses the engine-wide scope he chose earlier the same day (that call
  was made with the collision already flagged; this one is made with the
  consequence heard).
- Decision/change: deleted `pattern_gen._clean_punch` and CLEAN_PUNCH_TAGS
  and both call sites (compose() and the odd-meter `_compose_odd`, which rolls
  its flavor independently — the same second call site that nearly got missed
  when the rule went in). Each entry's declared `kick_flavors` weights govern
  again. Did NOT special-case Doc Day: his ear's verdict on Dre already lives
  in Doc Day's own weights (808 0.1 vs punch 0.75, ~12% 808), which is the
  right place for a style statement. Left `ADD_THE_ROOT_808 = False` alone —
  the root sub is a bass layer under the kick, not the kick flavor, and he
  named the kick only; flagged as an open question instead of assumed.
- Reasoning: deletion, not a new per-DJ exemption flag — the per-style data
  that expresses "true to style" already exists in every entry.
- Verify by: 467 tests green (one test net removed). Replaced the two tests
  asserting the old spec: `test_kick_flavor_follows_the_style_not_an_engine_
  wide_filter` now asserts 808 IS reachable and nothing outside the declared
  set appears, across both the main and odd-meter paths.
- Status: confirmed (mechanically; the sound is the owner's call)
- Outcome: #903 and #904 rendered with real 808 kicks (Punchy 808, Cymatics
  Oracle 808), #902 clean — 2:1, matching Mustang's declared 0.6/0.4.

### 2026-07-23 Flavor-index history went stale across the rule change — first 3 beats were not a fair sample
- Context: the first 3 beats after the reversal (#899-901) came out 2 clean /
  1 808, not the ~2:1 toward 808 that Mustang's weights imply. Checked
  pattern_history.json rather than assuming it was just an unlucky roll.
- Decision/change: no code change. Diagnosis confirmed from the history file:
  `remember_pattern` stores the flavor's POSITIONAL INDEX into whatever
  kick_flavors list was live at the time. Under the clean-punch filter that
  list had one entry, so 9 straight beats recorded fi=0. Removing the filter
  changed what index 0 MEANS (now the 808 entry), so the streak-breaker read
  nine "808s in a row" and zeroed the 808 out for #899 and #900, then zeroed
  clean for #901. All three flavors were dictated by stale history, not by the
  new rule. Re-rendered #902-904 once the history was back in the new index
  space; those are the real sample.
- Reasoning: it self-corrects after 2 beats, and the only thing that breaks it
  is changing a flavor list's SHAPE (not its weights — evolution.py only tunes
  weights, so the index stays meaningful). Storing an identity instead of an
  index would be the durable fix; not worth the diff for a one-off migration.
- Verify by: history now shows fi=0 (#901) then fi=1 (#900) — no streak, so
  the breaker is idle and weights govern. #902-904 came out 1 clean / 2 808.
- Status: confirmed
- Outcome: latent trap — the next time any entry's kick_flavors list gains or
  loses an entry, that DJ's next 2 beats get a dictated flavor. Note it there
  rather than debugging it fresh.

### 2026-07-23 MIDI validity gate was failing every chord beat — the gate was stale, not the beats
- Context: ran the house midi-validity-gate on the 9 new Mustang beats before
  delivering. All 9 FAILED ("8 note(s) not on channel 10"). Checked yesterday's
  Timberline batch and J Dillo's before assuming I'd broken something — those
  failed identically, so it predates Mustang.
- Decision/change: fixed the GATE, not the generator. `beat_recipes.write_midi`
  puts harmony's chord voicings on channel 1 **on purpose** (its own docstring:
  "not 10, so Reason doesn't read it as a drum hit") — correct behavior the gate
  was written before, back when every note in a beat file was a drum. New rule
  in check_midi.py: require ≥1 note on channel 10 and every channel-10 note
  inside GM 35-81; notes on other channels are counted as melodic and allowed.
  SKILL.md updated to match.
- Reasoning: root cause is in the checker. Making the generator satisfy the old
  rule would mean putting chords on the drum channel, which is actually wrong.
- Verify by: all 9 Mustang + all 20 earlier chord beats (Timberline, J Dillo)
  now PASS. Negative cases still caught, verified with 3 synthetic files: a
  melodic note ON channel 10 → fails GM-range; a file with only a chords track
  → "no drum notes on channel 10"; a missing tempo → fails.
- Status: confirmed
- Outcome: every chord beat delivered since 2026-07-22 (Dre, Premier, Dillo,
  Timberline batches) was handed over without a passing gate — no file was
  actually bad, the check was.

### 2026-07-23 Mustang (DJ Mustard) harmonic signature — 5th legend, first one NOT in the research doc
- Context: owner said move on to Mustang after Timberline closed the 4-legend
  research proof set (Dillo/Premium/Doc Day/Timberline).
- Decision/change: added a `signature` block to Mustang in legends_config.json.
  Flagged in its `_note` and here: **Mustang has no row in
  HARMONY-IDENTITY-PROPOSAL** — that doc only researched 4 legends and they're
  all built. This block is from general knowledge of DJ Mustard's records, so
  the owner's ear is the only check on it; there's no cited source behind it
  like the last four had. Contents: roots F/G/Bb, plain minor, chord_source
  synth-only (he builds in the box — no orchestral strings, no chopped soul
  loop), chord_rhythm arp-leaning 3:1 over held (the bright plucked ostinato is
  the giveaway; the arp path already exists from Dre's work), tempo 95-105.
  Progressions are the two most minimal shapes: `vamp_i_VI` (exists) and
  `vamp_static_riff` — a NEW 1-chord slug in progressions_config.json, held the
  whole loop so the riff and 808 carry it. That slug is the proposal's own
  defined third slug, skipped in earlier sessions only because nothing consumed
  it; Mustang is its first real consumer.
- Reasoning: data-only, no engine change, same audition-gated pattern as the
  previous four.
- Verify by: 468 tests green. Rendered #890-898 (9 beats). Tempo 95/95/97/97/
  100/103/103/105/105 — the full pocket, no clustering. Stems confirm the
  signature: every chord slot synth (zero strings/loop leakage), 7 of 9 arp
  and 2 held pads ≈ the 3:1 lean. LUFS -12.8 to -13.2, all render checks
  passed, MIDI gate green.
- Status: open
- Outcome: (pending owner listen. Two honest gaps: (1) the flagship combination
  — static riff WITH the plucked arp — never rolled: both static beats (#892,
  #897) happened to draw the held pad. Simulated 10k variants to check for a
  seed correlation and there is none, static+arp comes up 37.2%, it just missed
  twice (~6% luck). Another click should land it. (2) #893's bar swing is
  0.6 dB, under the 2.5 dB floor even after the contrast pass — it's a 2-bar
  loop, weakest of the batch.)

### 2026-07-23 Engine-wide clean-punch kick now visibly fights Mustang's own identity
- Context: yesterday's owner-reaffirmed rule constrains kicks to clean-punch
  engine-wide, ignoring 808. Every one of the 9 Mustang renders reported
  "kick: clean/short clean+tight" and the variety checker warned "one kick
  flavor ran 6 beats in a row."
- Decision/change: none — left the rule alone, flagging only. Mustang's own
  `listen` line is "a sparse **808 kick** that lands on the and-of-two pocket"
  and his kick_flavors weight 808 at 0.6 vs 0.4 clean, so the engine-wide
  filter removes his majority flavor and, since no DJ on the roster has two
  non-808 flavors, leaves him exactly one kick sound for every beat.
- Reasoning: the owner reaffirmed engine-wide deliberately last session with
  this collision already named; reversing it unasked would be overriding a
  decision he made with the tradeoff in view. But Mustang is the sharpest case
  yet — this is the first legend whose one-line identity IS the 808.
- Verify by: ask the owner after he hears #890-898 whether the kicks read as
  Mustard to him.
- Status: open
- Outcome: (needs his ear — a per-legend 808 exemption is the obvious fix if
  he agrees, but that's his call to make, not mine)

### 2026-07-23 Timberline (Timbaland) harmonic signature — resolved the dual-tempo-pocket fork
- Context: Timberline was flagged when Dillo was picked up ("its tempo is
  unusual, two ranges 90-100 and 135-145, so that one needs a decision on
  which pocket") rather than defaulted silently. Owner's answer: allow both,
  with variation — don't pick one.
- Decision/change: (a) beat_machine.py's vary_preset tempo-lean block only
  ever supported one contiguous pocket (a %-lean off the base bpm, clamped
  into a signature's [lo,hi]) — that can't reach a second, disconnected
  pocket from a single base bpm. Extended `signature.tempo` to also accept a
  list of [lo,hi] pairs: when it's a list-of-lists, roll a pocket first, then
  a tempo inside it, instead of leaning from the base. A single [lo,hi] pair
  (every other legend) is untouched — same code path as before. (b) Added
  Timberline's signature: roots D/E/G, phrygian (fixed, not weighted — the
  giveaway names Phrygian specifically, no "as often as" caveat like Dilla's
  mode), progression dark_menacing only (the proposal's table value; did NOT
  invent the vamp_static_riff drone slug since the table assigns that one to
  Miami Bass, not Timberline), chord_source synth-only — no strings/loop —
  since the proposal calls Timbaland rhythm- more than harmony-defined
  ("almost no chord movement," a single droning melody), and a plain pad
  reads closest to that. tempo = [[90,100],[135,145]], the proposal's own two
  researched pockets — used as the suggested tempos since I have no better
  source than that research.
- Reasoning: smallest change that generalizes (a type-check on the tempo
  field, not a Timberline-only branch), so any future dual-pocket identity
  gets it for free.
- Verify by: 468 tests green. Rendered #884-889 (6 beats): bpm landed
  100/93 (low pocket) and 139/135/136/138 (high pocket) — real spread inside
  both, not stuck at the edges. Every beat: phrygian key, dark_menacing
  progression, chord0/1 stems confirmed synth-pad-only (no loop/strings
  leaking in). LUFS -13.0/-12.8/-12.8/-12.7/-12.8/-12.9, all checks passed.
- Status: open
- Outcome: (pending owner listen; this closes out the 4-legend research
  proof set — Dre, Premier, Dillo, Timberline all have signatures now)

### 2026-07-23 J Dillo pinned to 2/4-bar only ("no long beats")
- Context: owner loved the 5-beat filtered batch (#870, 873-876) but named
  it as a rule, not a one-off: "include a variation between these two beat
  lengths. for this DJ. No Long Beats." — vary 2-bar/4-bar, never 8.
- Decision/change: pattern_gen.compose() had no per-DJ hook for loop length
  — nbars was always the engine-wide roll (2/4/8 weighted, or a hard 8 for
  genre entries). Added `bar_lengths` as an optional preset key: when set,
  it replaces the weighted roll with `rng.choice(bar_lengths)`; unset, the
  old behavior is untouched (every other DJ/genre). Set J Dillo's
  `bar_lengths: [2, 4]` in legends_config.json. The A/B "answer" form only
  ever triggers off `nbars == 8`, so excluding 8 from the pool also kills
  the A/B complaint as a side effect, not a separate fix.
- Reasoning: smallest change that generalizes — a new preset field instead
  of a J-Dillo-specific branch in compose(), so any future DJ that wants a
  pinned loop-length pool (or wants the old 2/4/8 spread) can just set or
  omit the key.
- Verify by: 468 tests green. Rendered #878-883 (6 beats): 3 landed 2-bar, 3
  landed 4-bar, zero 8-bar, zero A/B. LUFS -13.0/-13.0/-13.1/-13.1/-12.9/
  -13.0, all checks passed. last_batch pointed at all 6 for the player.
- Status: confirmed
- Outcome: (holds until the owner says otherwise; consider whether other
  legends want their own bar_lengths pin later, but not decided yet)

### 2026-07-23 J Dillo (Dilla) harmonic signature added — 3rd legend, owner approved moving on
- Context: owner approved DJ Premium's #864-866 batch and said to move on to
  Dilla next.
- Decision/change: added a `signature` block to J Dillo in legends_config.json
  — roots C/D/Bb, mode an even 1:1 minor/major weighted roll (the proposal's
  own research correction: Dilla is sample-dictated, skews major as often as
  minor, so a hard minor lock would be wrong for him specifically), existing
  progression slugs (nostalgic_jazz 2, dreamy 2, vamp_ii_V 1 — no new theory
  needed), chord_source loop-forward 4:1 over synth — heavier loop lean than
  Premier's 3:1 since Dilla's whole identity is the chopped soul/Rhodes
  sample, not just a color choice. No chord_rhythm/articulation override,
  same audition-first start as Dre and Premier.
- Reasoning: same low-risk/audition-gated pattern as the last two — data
  only, no engine changes, let the owner's ear judge before tuning.
- Verify by: 468 tests green. Rendered #867-869: 88/85/88 bpm (all in
  70-95), mode hit both major (#867, C major) and minor (#868 D minor, #869
  Bb minor) confirming the 1:1 roll works both ways, progressions dreamy/
  nostalgic_jazz/dreamy. Stems: 6 of 7 chord slots landed real chopped-loop
  samples (Oracle/Atlanta/Everything melody loops), 1 synth-pad floor
  fallback — matches the intended 4:1 lean. LUFS -13.0/-12.9/-13.1, all
  checks passed.
- Status: open
- Outcome: (pending owner listen to #867-869; last researched legend left is
  Timberline (Timbaland) — note its tempo is unusual, two ranges 90-100 and
  135-145, so that one needs a decision on which pocket before building it)

### 2026-07-23 DJ Premium (Premier) harmonic signature added — next legend after Dre
- Context: HARMONY-IDENTITY-PROPOSAL's plan was "roll the pattern to the other
  7 only after the Dre sound is approved" — the owner's #843/#845/#849 picks
  confirmed Dre. DJ Premium was the pick for next: it's one of the 4 legends
  the proposal actually researched, and unlike Dilla/Timbaland it needed zero
  new engine work (dorian mode and loop chord_source both already exist/work),
  so it's the lowest-risk next step.
- Decision/change: added a `signature` block to DJ Premium in
  legends_config.json — roots D/E/A, mode minor-leaning-dorian (2:1), existing
  progression slugs only (vamp_i_iv7, dark_menacing weighted 2, vamp_i_VI at
  1 — no new progressions_config.json entries needed), chord_source loop-
  forward 3:1 over synth (a chopped melodic loop reads as Premier's dark
  sample stab; synth stays the always-works floor per _source_order). No
  chord_rhythm or articulation override — started at the engine default
  (held/sustain), same as Dre did before owner-audition feedback picked arp.
- Reasoning: same audition-gated approach as Dre — add the data, render a
  small batch, let the owner's ear decide before tuning further, rather than
  guessing at a "stab" rhythm feel with no engine support for it yet.
- Verify by: 468 tests green (no new engine code, so no new tests). Rendered
  #864-866: 88/90/93 bpm (all in the 82-96 range), A dorian (vamp_i_iv7),
  D dorian (dark_menacing), E minor (vamp_i_iv7) — mode weighting hit both
  values across 3 beats. Stems confirm loop landed 5/6 chord slots (real
  chopped samples, e.g. "Oracle Classic Melody Loop... A Min Organ") and synth
  landed 1/6 as the floor fallback, matching the 3:1 intent. LUFS -13.0/-13.3/
  -12.9, all checks passed.
- Status: open
- Outcome: (pending owner listen to #864-866; roll to the next legend —
  J Dillo or Timberline — only after this one's approved, same as Dre)

### 2026-07-23 Dre tuning (best-of #843/845/849) + engine-wide clean-punch kicks
- Context: owner picked #843 (held, strings, vamp_i_iv7/m7), #845 (held, mixed
  strings+synth, gfunk), #849 (arp, mixed, gfunk) as the best representations —
  overturning the m7-removal and strings-only calls from the prior session. Also
  asked for: chord_rhythm to roll per beat, Dre tempo pinned 90-96, kick
  constrained to clean-punch, and explicitly "ignore previous push for 808" —
  confirmed via AskUserQuestion to mean ENGINE-WIDE, not Dre-only, after I
  flagged the bigger blast radius.
- Found mid-task: a partial auto-edit had already landed (chord_rhythm roll +
  a tempo clamp in vary_preset — both good, kept) but with wrong values versus
  what the owner then told me directly in chat (tempo 90-93 not 90-96, strings-
  only not strings-forward, m7 vamp still missing). Chat instructions win over
  an unreviewed auto-edit; corrected all three to match.
- Decision/change:
  (a) Doc Day signature: progressions back to gfunk(3):vamp_i_iv7(2) — the m7
      wasn't the real #847 problem, #843 proved the same vamp works held; chord_
      source strings(2):synth(1); chord_rhythm [arp(1),sustain(1)] rolls once
      per beat via _wpick; tempo [90,96].
  (b) NEW pattern_gen._clean_punch(flavors): drops every must="808" flavor,
      narrows to CLEAN_PUNCH_TAGS={punch,knock,clean,tight,hard}, graceful
      fallback (never empties a pool). Applied at BOTH places a kick flavor is
      rolled — the main compose() path AND _compose_odd (3/4 and 6/8) reached
      the same style["kick_flavors"] independently; only patching one would
      have left odd-meter beats still rolling 808 (found by grepping every
      caller before declaring it done, not by a later bug report).
  (c) beat_machine.ADD_THE_ROOT_808 = False: retires the 2026-07-18 "add the
      root" auto-808-sub-under-traditional-kick rule engine-wide. Mechanism
      (_root_sub, the sub-lane wiring) left in place, gated on the constant,
      not deleted — a one-line flip restores it. The recipe-rebuild path (an
      old beat's saved root_note reproducing its sub) is untouched — this only
      stops NEW renders from rolling a fresh one.
- Reasoning: root-cause fix at the one/two spots every kick roll routes
  through, not per-config edits — smaller diff, and (per ponytail) patching
  only the path a report names leaves siblings broken, which is exactly what
  _compose_odd would have been if I'd stopped after the first call site.
- Verify by: 468 tests green. Rewrote 2 tests that asserted the OLD "808
  reachable" behavior (test_pattern_gen.py) — a deliberate spec change, not a
  regression; added test_composed_kicks_are_never_808 (covers both compose()
  paths) and a signature-tempo-clamp test. Rendered #859-863: tempo all in
  90-96 (96/90/93/96/90), kick report "clean/short punch+knock" on all 5 (zero
  808 reachable, confirmed against DEFAULT_STYLE/genres_config: this collapses
  EVERY style in the roster to exactly one surviving kick flavor — none had a
  2nd non-808 flavor of their own — so the clean-punch rule also removes kick-
  flavor VARIETY roster-wide, not just 808 texture; flagged to owner, not
  hidden). chord_rhythm: 2 arp / 3 held (both reachable). progressions: 4
  gfunk / 1 vamp_i_iv7 (#862, Cm7 — the m7 IS back and reachable). chord
  source: strings in all 5, synth-arp in 2 (strings-forward, both reachable).
  All LUFS -13.0, peaks -5.7 to -6.1 dBFS. Note: 2 of 5 kick SAMPLES happen to
  have "808" in the filename (sample-pack branding, e.g. "Oracle 808") but
  crew._load_choked hard-truncates every kick to the flavor's 0.2-0.5s choke
  regardless of source file — verified by reading the choke code, not just
  trusting the tag.
- Status: open (kick-flavor-variety-roster-wide side effect flagged, not yet
  ruled on; everything else owner-confirmed via direct render inspection)
- Outcome: (pending owner listen to #859-863; pending owner call on whether
  DJs should get a 2nd clean/punch kick_flavors entry to restore variety)

### 2026-07-22 Dre chords: rhythmic arp + m7 removed (audition #845-847 feedback)
- Context: owner auditioned the first signature batch. Verdict on #847: "weird
  out of key chords at the end, none sound like Dre." Investigated with an FFT/
  nearest check: the pitches were CORRECT (every nearest pick in-key; rendered
  partials matched the chords) — NOT a tuning bug. Two real problems: (1) #847
  used vamp_i_iv7, whose m7 reads as "out of key" for a triad producer; (2)
  every beat played one HELD block chord per section — a drone — which never
  reads as Dre's rhythmic Still-D.R.E. figure even in the right key.
- Decision/change:
  (1) Dre signature progressions -> ["gfunk_minor_i_iv_v"] only (triads, no m7).
  (2) New chord_rhythm="arp" trait + engine: chord_synth.arp_riff sequences the
      chord tones as an ascending eighth-note arpeggio filling the section
      (loop-safe tail-wrap); chord_synth._pluck is the e-piano-ish step voice;
      string_sampler.note_slice is the strings step voice (cached, enveloped).
      beat_machine's strings/synth branches arp when the signature asks; the
      held chord stays the default for every other identity. Owner picked
      "rhythmic riff" over cleaner-pad / different-instrument when asked.
- Reasoning: kept it one lane / one buffer per chord (rhythm baked into the
  buffer) so the lane/bass/MIDI wiring and clean stems are untouched — the arp
  only changes what fills the buffer. Opt-in via the signature.
- Verify by: 466 tests green (+arp test). Re-rendered #848-850, all
  gfunk_minor_i_iv_v (Still D.R.E.) in C/F/G minor, LUFS -13.0, peak -5.9 dBFS;
  raw arp = 16 onsets vs 1 for the old drone. #845-847 retired to Trash. Strings-
  arp chords stay crisp through the mix; synth-arp (pluck) chords smear a bit
  under the beat reverb — flagged (a faster _pluck decay is the tweak if washy).
- Status: failed (partially) — owner's actual favorites (#843, #845, #849) were
  a mix of held AND arp, not arp-only, and #845 used the mixed strings+synth
  voice this entry moved away from. Superseded by the 2026-07-23 entry above,
  which restores both as a per-beat roll instead of a single fixed choice.
- Outcome: the m7 removal specifically did NOT hold — #843 (m7, held, strings)
  was one of the 3 favorites, so #847's problem wasn't the chord quality.

### 2026-07-22 Wired harmonic identity (signature) into chord synth; Dre audition
- Context: HARMONY-IDENTITY-PROPOSAL's recommended first step. Every "chords"
  beat was identity-blind (random root, always minor, mood-or-random
  progression, loop-else-pad voice, strings never used). Give Dr. Dre
  (Doc Day) a harmonic fingerprint and audition it before rolling to the rest.
- Decision/change:
  (a) progressions_config.json: added gfunk_minor_i_iv_v (i-iv-v all-minor,
      Still D.R.E. = Fm-Bbm-Cm). Only the slug Dre needs; the proposal's other
      two (vamp_i_IV9, vamp_static_riff) ship with G-funk/Miami later — adding
      them now would be config nothing reads.
  (b) legends_config.json Doc Day: additive `signature` block (roots F/G/C,
      mode minor; progressions gfunk 3 / vamp_i_iv7 2; chord_source strings 2 /
      synth 1; articulation sustain). No tempo block — bpm 93 already sits in
      the proposed 85-100 range, so a range would be dead config.
  (c) beat_machine.py chord block reads preset["signature"]: it picks
      root/mode/progression (a typed mood word still overrides), and a weighted
      chord_source rolls the voice per chord (_wpick/_source_order helpers) with
      the synth pad always the never-fails floor. No signature => byte-identical
      old behavior. Skips the melodic-loop scan unless an identity lists "loop".
  (d) string_sampler.by_articulation maps a signature's abstract articulation
      word to the vendor's tokens (sustain = sus/sustain/sustainff|mf|mp/susrel).
      Legato excluded on purpose: leg samples ~2s tile 4-5x (audible seams)
      across Dre's ~10s chords; true sustains run 7-9s (<=1 tile).
- Reasoning: the proposal's "almost no new engine" — one chooser over data that
  already exists. Dre first because his signature exercises the whole chain
  (new slug + strings + articulation). Wired strings-as-a-source (built but
  never connected) rather than the synth-lead voices the proposal defers.
- Verify by: 465 tests green (+ tests/test_signature.py for the pure helpers).
  Rendered 3 into the live library: #845 gfunk Fm (Still D.R.E., strings on
  iv/v), #846 gfunk Gm (all strings), #847 vamp Cm (all strings). All LUFS
  -13.0, peak -5.8 dBFS, no clip, checks passed. A first buggy batch (#842-844,
  pre-leg-fix, one came out all-pad) moved to Trash/Doc Day, not deleted.
- Status: confirmed (machinery held; voice/progression refined by ear — see the
  arp entry above)
- Outcome: owner auditioned #845-847. The signature plumbing worked, but two
  choices were wrong by ear: vamp_i_iv7's m7 ("out of key") and the held-drone
  voice ("none sound like Dre"). Both fixed in the arp entry above. Roll the
  pattern to the other 7 only after the Dre sound is approved.

### 2026-07-22 Strings sampler scaffolded + chords audition batch rendered
- Context: harmonizer "next steps" review. Steps 1-7 (key/progression/voicing/
  MIDI+loop ingestion/fit/render) all shipped; the remaining real-instrument
  seam is the 24.5k-file London Symphonic Strings library (gap-analysis Part 7).
- Decision/change: (a) rendered a 5-beat chords audition batch into the live
  library (#837-841, various DJs/mood words) + a `_strings audition/` folder with
  Am/Cmaj example chords, for the owner's ear. (b) Built tools/string_sampler.py
  as a note-by-note SAMPLER (scan/nearest/play_chord), distinct from the loop/
  phrase fitters — plays harmony.compose()'s exact MIDI notes, one close-mic
  sample per note. Note parsed as the single plausible-MIDI token in the
  filename, which also drops legato-transition files. play_chord peak-guards
  against pizz-transient clipping. Deliberately NOT wired into the render.
- Reasoning: strings need zero pitch-detection (note# in filename), so it's the
  lowest-risk instrument well. Wiring it into chord_synth is a taste call (when do
  strings beat a sampled loop / synth pad?) that wants the owner's ear on the
  audition first — build the proven seam, don't guess the priority order.
- Verify by: owner listens to #837-841 and the `_strings audition/` wavs; decide
  whether chopped melody-loops read as chords, and whether to wire strings in as
  a 3rd chord source (strings -> loop -> synth fallback). 462 tests green.
- Status: open

### 2026-07-22 chord_synth loop-pad substitution: allow melody role, chop loop-kind files
- Context: chord_synth.sample_pool originally only drew role="chord",
  kind="oneshot" melodic files as pad_voice stand-ins — a deliberately
  conservative first cut, flagged at the time as a judgment call rather than
  guessed silently. Owner asked to loosen it: allow melody role, and turn
  kind="loop" files into usable one-shots instead of excluding them.
- Decision/change: sample_pool now allows role in ("chord", "melody") — pool
  went 87 -> 703 candidates. Added melodic_loops.chop_onsets: a dependency-
  free onset detector (fast 10ms envelope vs. its own trailing 200ms floor,
  plus a noise gate) that slices a loop-kind file into individual clean,
  faded one-shot hits before fit_loop runs. loop_voice falls back to
  pad_voice if a loop-kind pick has no detectable onset.
- Reasoning: the original tempo-drift concern (fit_loop resamples pitch but
  can't stretch tempo, so tiling a whole rhythmic loop to an arbitrary chord
  duration could drift against the beat grid) doesn't apply to a single
  chopped-out hit — a lone hit carries no tempo of its own. Chopping resolves
  the concern instead of just avoiding it.
- Verify by: tests/test_melodic_loops.py (chop_onsets unit tests) and
  tests/test_chord_synth.py both green (452 total passing). Live-rendered two
  chords beats end to end and confirmed real sample stems landed in the right
  key/roman-numeral slot (e.g. "chord0 - sample: 120_Feefley G, Gm (i).wav").
  Still open: whether the chopped-hit audio quality holds up by ear across a
  wider variety of source loops — the owner hasn't auditioned a batch yet.
- Status: open
- Outcome: (pending owner listen-through)

### 2026-07-22 Paused the crew-variety autoresearch loop
- Context: the crew-variety autoresearch loop (autoresearch.md) had run 35
  experiments tuning crew_config.json's DJ style numbers. The Stop hook
  re-triggers it on every session in this directory unless paused explicitly.
- Decision/change: wrote .autoresearch-off (the loop's own designed safety
  valve — same file /autoresearch off would create) rather than editing the
  shared global hook script, since the hook is scoped by autoresearch.md's
  presence in cwd, not by anything global.
- Reasoning: config-tuning space in crew_config.json is exhausted — variety
  plateaued at ~14.08 against a 0.15 noise floor across two segments and 33
  experiments (see autoresearch.md's meta-review, experiments/worklog.md's
  Session Conclusion, both dated 2026-07-17). The worklog's own next step is
  engine content (more KICK_BANK skeletons, more reference grooves, new
  timekeeper modes), not more crew_config.json tuning — out of scope for this
  loop as specced.
- Verify by: piped a real hook payload through
  ~/.claude/hooks/autoresearch-stop.sh with .autoresearch-off present —
  confirmed it exits clean with no "block" decision.
- Status: confirmed
- Outcome: loop stays paused until a new objective is defined (e.g. a
  KICK_BANK/groove-library autoresearch segment) and /autoresearch is run to
  resume, which deletes the sentinel.
