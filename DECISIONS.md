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
