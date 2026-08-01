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

## Archived history — 66 entries moved, nothing deleted

Everything up to and including 2026-07-25 now lives in
[`DECISIONS-ARCHIVE.md`](DECISIONS-ARCHIVE.md). It was ~50,000 tokens and
`CLAUDE.md` asks every session to read this file before doing anything, so
the old entries were being paid for on every single startup.

**Read the archive when** you need the reasoning behind something older than
2026-07-26, or when an entry below refers back to one. The one-line index of
what's in there is at the bottom of this file, so nothing is invisible —
just not loaded by default.

---

### 2026-07-31 Owner standing rule on sound + master EQ fixed + house ambience bed + chord bus governor
- NEW STANDING RULE from the owner, verbatim: "in order to have studio ready
  quality tracks. I want you to be able to use reverb and any other effect. as
  much as needed. for quality. and style and dj. It can even vary instrument to
  instrument. whatever will sound best. based on our experts' opinions. This
  overrules any other command where sound is concerned."
  Read as: effects in service of QUALITY are now mine to apply, per instrument
  and per DJ, and a quality floor is not a per-beat style choice.
  NOT read as permission to bake in DIRT — clean_renders (vinyl, wow, dust,
  saturation) stays ON, because 2026-07-18 he specifically wanted to add his
  own colour in Reason. Told him so plainly rather than deciding it silently;
  he can say the word if he wants those in play too.
- Fix 1, master() EQ (he approved this one explicitly): `m = 0.5*(L+R)` moved
  to AFTER the EQ. It was captured before, so the mid was rebuilt from a
  pre-EQ copy and the tone stage was discarded on everything centred.
  Verified: centred content now gets +2.51 dB air / -1.25 dB boxy-mid, where
  it previously got -0.009 dB. This stage had never applied to any beat.
- Fix 2, the actual reason beats sounded small: EVERY DJ's space list is a
  SINGLE lane — `["snare"]` or `["clap"]`. Chords, melodic parts, bongos,
  stamps and all guest colour printed bone dry, forever. Added a house
  ambience bed in render_crew_beat that runs regardless of the rolled space
  (including "dry", per the rule above): harmonic lanes get 1.4s/3200Hz at
  0.18 wet, colour lanes 0.5s/4200Hz at 0.10, both stereo. Explicitly skips
  kick, the sampled 808 and the tuned sub — low end stays dry and centred.
  The DJ's signature snare/clap treatment is untouched, so identity still
  comes from that.
- Fix 3, chord level: REVERTED my own 0.30 -> 0.55 change from earlier today.
  Measurement killed it — it shifted the whole distribution up 5.3 dB without
  narrowing the SPREAD, so a real batch came back ranging -2.5 dB (shouting)
  to -15.5 dB (inaudible) under the kick. An open-loop gain cannot hit a
  target when source samples vary that much. Replaced with a bus governor in
  render_crew_beat, mirroring the snare backstop that has existed since
  2026-07-18, targeting OWNER_TASTE["chord_bus_under_kick_db"] = 9.0 and
  clamped to +/-12 dB so a pathological sample can't be hauled up 30 dB with
  its own noise floor. chord_gain is back at the owner's 0.30.
- Measured on 5 real rendered beats (scratch dir, not his library):
    width      -9.6 to -14.9 dB S/M   (library before: -22 to -31)
    chord/kick -6.0 to -8.2 dB, SPREAD 2.2 dB  (library before: 19 dB spread)
    silent stems 0 of 60; peaks -5.6 to -6.4; low-end side ratio 0.014-0.041
    (all under the 0.05 mono-bass guard)
- Tests: 743 passed / 1 skipped, up from the 732 baseline. tests/
  test_audio_quality.py now also covers the mono-bass guard, the governor
  working within its range, and — separately — that the clamp REFUSES to
  rescue a hopeless sample, so nobody quietly loosens it later.
- One test was deliberately rewritten, not deleted: test_dry_beats_are_
  allowed_to_be_narrow encoded the OLD rule that dry means near-mono. The
  standing rule supersedes it; it now asserts the RELATIONSHIP (dry is still
  narrower than wet) instead of an absolute.
- Status: confirmed
- Outcome: owner heard the 5 scratch beats and said "apply" (2026-07-31).
  Committed to main as c741927 and live for every render from the next
  launch. NOT yet re-confirmed over a longer listening period — if the
  ambience turns out to be too much on a particular instrument, the two
  numbers to move are the wet values in render_crew_beat's ambience bed
  (0.18 harmonic / 0.10 colour), and the chord level is
  OWNER_TASTE["chord_bus_under_kick_db"].

### 2026-07-31 Applied: stereo reverb restored, chord level fixed, silent stems blocked, first audio tests added
- Context: owner approved the fixes from the rebuild review (entry below).
- CAUGHT BEFORE SHIPPING — my proposed fix #1 was WRONG. The review said to
  pan chord0/1/2 apart to -0.45/0/+0.45. I checked the rendered stems first:
  chord0/1/2 have ZERO time overlap (0.00-5.44s, 5.45-10.90s, 10.91-21.81s).
  They are the progression's chords in SEQUENCE, not three simultaneous
  parts. Panning them would have swung the progression across the stereo
  field on every chord change. Do not reinstate that idea.
- ROOT CAUSE of the mono mix, found instead: make_ir() has always returned a
  STEREO pair of decorrelated IRs (groove.py:303, docstring says "Stereo
  IR"). Both reverb paths threw the right channel away — crew.py did
  `irL, _ = make_ir(...)` and gated_reverb assigned irR and never used it.
  The one stage in the chain designed to create width was printing mono.
- Changes: (1) crew.py room/plate/hall path convolves both IRs, keeps the
  mono fold-down in bufs[] and carries the decorrelated half as wet_side[],
  folded in at pan time in both the stem loop and the mix loop.
  (2) gated_reverb gained stereo=False (default unchanged, so every existing
  caller and test is untouched); crew.py's gated branch passes stereo=True.
  (3) OWNER_TASTE["chord_gain"] 0.30 -> 0.55.
  (4) write_stems refuses to write an all-zero stem and prints which lanes
  made no sound.
  (5) NEW tests/test_audio_quality.py — the first tests that assert on
  AUDIO rather than on dicts.
- On chord_gain: this reverses a number the owner set on 07-23 when beats
  "arrived shouting", so it is flagged for his ear. Justification is that
  the comment's stated intent (~10 dB under the kick) never matched reality
  (measured median 15.4 dB under, worst 24.9) because the accent multiplier,
  the duck and the peak normalise all stack after it. 0.55 makes the
  measured result match the intent. If it now shouts, this is the number to
  walk back — nothing else depends on it.
- Level safety, measured not assumed: the per-channel wet level is UNCHANGED
  (+0.00 dB — L still receives exactly irL). The wet's mono fold-down drops
  2.9 dB because decorrelated channels partially cancel in mono, which is
  physically correct; across a whole beat the figure the snare-vs-kick
  backstop and _track_gain actually read moves 0.18 dB. Nothing retuned.
- Verified by RENDERING, not by reading the diff. Three real beats with
  --notes "room chords": width -13.5/-16.3/-18.6 dB S/M (library before:
  -22 to -31), chord-vs-kick -6.6/-10.6/-10.9 dB (library median before:
  -15.4), 0 silent stems of 31, LUFS -12.8 on all three, peaks -6.0.
  Rendered to a scratch dir, NOT his library.
- Full suite 740 passed / 1 skipped (baseline was 732), so the 8 new tests
  are additive and nothing regressed.
- KNOWN LIMIT, not hidden: this only helps beats with a wet space. "dry" is
  32% of the library and still renders narrow (-27 to -30 dB) because a dry
  beat has no reverb to widen. First audition batch rolled dry three times
  and showed no improvement at all, which is how this surfaced.
- Status: confirmed
- Outcome: superseded and folded into the entry above; owner approved the
  combined result 2026-07-31, committed as c741927. Note the chord_gain
  0.55 change described here was REVERTED before shipping — see above.

### 2026-07-31 CLAUDE.md's machine facts are WRONG — it is an M2 Pro on macOS 26, not an old Intel Mac; Python 3.9 is a self-imposed choice
- Context: a research pass checked the hardware instead of trusting the brief.
- VERIFIED locally (sysctl / system_profiler / sw_vers / uname):
    MacBook Pro 14" 2023, Mac14,9, Apple M2 Pro, 10 cores, 16 GB, arm64
    macOS 26.5.2 (build 25F84)
    /usr/bin/python3 and .venv/bin/python are both 3.9.6, arm64
    uv 0.11.29 already installed at ~/.local/bin/uv
- CLAUDE.md currently says "older MacBook Pro" and treats system Python 3.9 as
  a machine constraint ("Target 3.9", "NO X | Y union syntax"). The hardware
  claim is simply false, and 3.9 is a CHOICE — the venv points at Apple's
  Command Line Tools python. Python 3.9 reached end-of-life 2025-10-31.
- Consequence: every session has been writing 3.9-compatible code and ruling
  out libraries on the basis of hardware this machine does not have. The M2
  Pro's GPU and Neural Engine have never been used for anything.
- CORRECTION to the research pass's own framing: it concluded "everything else
  waits on the Python upgrade." That is wrong, and I checked rather than
  repeating it. Installed into a scratch target against the EXISTING 3.9 venv:
    pedalboard 0.9.17 + soxr 1.1.0 install fine on cp39 arm64
    pedalboard has PitchShift, Limiter, Compressor, Reverb, Resample, Delay,
    Chorus, Distortion, Convolution, HighpassFilter, time_stretch (Rubber
    Band) and io.AudioFile — all present on that build
  So the whole "replace the hand-rolled DSP" recommendation is available TODAY
  with no Python upgrade. The upgrade buys newer versions, not access.
- Also flagged, unverified by me: faster-whisper's CTranslate2 backend is
  CPU-only on macOS (no Metal, no ANE); whisper.cpp runs on the GPU via Metal
  with a Core ML encoder path. If true, the "small.en ~1s latency" note in
  CLAUDE.md was measured with most of the machine idle and should be re-taken.
  faster-whisper 1.2.1 is installed and its last commit was 2025-11.
- Decision: nothing changed this session. CLAUDE.md's "Owner & machine facts"
  section should be corrected before the next build session, because that
  section is explicitly labelled "do not rediscover these" and is therefore
  the most load-bearing wrong text in the repo.
- Verify by: re-run the sysctl/sw_vers block above; it takes one command.
- Status: open
- Outcome: (awaiting owner go-ahead to edit CLAUDE.md)

### 2026-07-31 Rebuild review: measured the audio instead of reading the code — the engine is fine, the OUTPUT STAGE is where value leaks
- Context: owner asked what a master music/software/audio engineer + producer
  would do differently if rebuilding this project from scratch.
- Method note (this is the reusable part): I answered by MEASURING 493
  rendered beats, 60 stem folders and 506 stem files with numpy, not by
  reviewing code. Every prior "it sounds wrong" session found its bug by the
  owner's ear. The measurements below took ~20 minutes and found four defects
  no session and no test had caught in three months.
- Finding 1 (VERIFIED, the big one): 247 of 247 core stems are exactly
  dual-mono, max|L-R| < 1e-9. Refined on second look: hat (-0.15), blips
  (+0.30), stamp (-0.30), congas (+0.29) ARE panned. What is hardcoded to
  0.0 is kick, snare, sub, bass AND all three chord parts
  (beat_machine.py:1535, literal 0.0 for every chord{i} / chord{i}v{v}).
  Centring kick and snare is correct practice. Centring three simultaneous
  harmony parts on top of each other is not. This is the mechanical cause of
  the owner's repeated "everything is stacked on top of each other" — chased
  as a sample-sourcing problem on 07-25 and 07-29. Those fixes were correct
  but could not have resolved the symptom: the cause is spatial, not tonal.
- Finding 2 (VERIFIED): melodic content is buried. Loudest chord part vs kick
  across 39 beats: median -15.4 dB, worst -24.9 dB. Single cause:
  OWNER_TASTE["chord_gain"] = 0.3 (-10.5 dB) in groove.py.
- Finding 3 (VERIFIED): master() applies its EQ to nothing. It captures
  m = 0.5*(L+R) BEFORE the EQ, EQs L/R, takes side from the EQ'd pair, then
  rebuilds with the STALE mid (make_drum_loops.py:173-195). Ran it: air shelf
  changes centred content by -0.009 dB, side-only content by +2.509 dB. With
  finding 1, the air shelf and boxy-mid dip have never applied to any beat.
- Finding 4 (VERIFIED): 17 of 506 stems (3.4%, 15 of 60 folders) are digital
  silence while listed as live lanes. Root cause is upstream of the renderer:
  1623's "blips" lane has ZERO hits in every bar while still carrying a
  sample, pan 0.30 and gain 0.26. Lanes can be dealt in with an empty pattern.
- Finding 5 (VERIFIED, corrects a subagent): a subagent called naive np.interp
  resampling "the single worst defect." Measurement does not support that.
  0 of 265 sampled library files are 88.2/96k; 18.5% are 48k, whose aliases
  fold to 20-22 kHz (inaudible). It DOES bite on the upward pitch-shift path
  (PREFER_MAX_SHIFT=12, added 07-29): a 15 kHz component shifted +12 st
  returns as a phantom 14.1 kHz tone. Melodic-path defect, not load-path.
- What is NOT wrong (checked, so it does not get "fixed"): rhythmic variety is
  genuinely good (186 unique kick+snare+hat patterns in 200 beats); harmonic
  variety is fine too (58 major / 174 minor / 53 dorian / 15 phrygian, 22
  progressions) — the legend/genre signature work landed. Constant-power pan
  law, mono_below, loop_convolve and the de-click work are all correct.
- Decision: do NOT rebuild. 25k lines, 732 green tests, 1623 beats, in use
  today, and the composition brain measurably works. Every defect above is in
  the output stage. The recommendation is three constants, one guard, and an
  automatic listening test — not a rewrite.
- Reasoning: the recurring failure across 76 ledger entries is not bad code,
  it is that the machine cannot hear itself, so the owner is the only test
  instrument. 39 entries sit at status: open, the oldest from 07-22, all
  waiting on his ears. Adding measurement to the render is what removes that
  bottleneck; a rewrite does not.
- Verify by: apply the pan spread + chord_gain lift, render a batch, re-run
  the S/M and chord-vs-kick measurements, and have the owner listen. Simulated
  on 1623 without touching the repo: width -24.0 -> -17.8 dB S/M, chord-to-kick
  -11.0 -> -5.7 dB. Improves both, does not fully reach a -6..-12 dB width
  target because kick/snare/sub are correctly centred.
- Status: open
- Outcome: (nothing applied this session — this was a review, no code changed)

### 2026-07-29 Real bug found via owner listening: one "instrument" still sourced from several packs
- Context: after the stacking hard rule (below), owner reported "the
  strings and the synths are still stacked in stems with other
  instruments" on beat 1508. I checked with a real render first — the
  structural fix (one voice per beat) WAS working, no second lane — but
  the owner was right about something real underneath it.
- Root cause: a chord's NOTES are picked one at a time,
  independently, by nearest-pitch search across the WHOLE library
  (tools/instrument_sampler.py:nearest, tools/string_sampler.py:nearest).
  For a well-populated, coherent group like "strings" that's invisible —
  the nearest sample for every note usually comes from the same real
  patch anyway. For a thin, eclectic group like "synth" (built from
  scattered single one-shots across many different vendor packs, not one
  chromatic patch), each note of one chord independently grabbed a
  different pack's sound. Same "synth stabs" label on the stem, four
  actually different instruments underneath. Confirmed on beat 1508: its
  4-file voice_files list for chord0 (a 3-note chord) spanned 4 different
  vendor packs.
- Decision/change: added a `prefer` argument to nearest() in both
  instrument_sampler.py and string_sampler.py (plus a `pin` argument
  threaded through voice_note/note_slice/play_chord and
  beat_machine.py's _render_one and its caller in _build_chords) — every
  note across the WHOLE beat's chord progression now prefers reusing the
  one sample already chosen, stretching it further before giving up and
  picking a fresh nearest match.
- First attempt used the existing MAX_SHIFT (4 semitones, a major 3rd) as
  the reuse ceiling — tested against real generated beats and it wasn't
  enough; most chords span wider than that, so it kept switching packs
  anyway. Gave the owner the honest tradeoff rather than silently
  shipping a fix that measurably didn't work: stretch further (simple,
  some notes sound more pitch-shifted) vs. hunt a same-pack fallback file
  before crossing packs (better sound, more code/testing). He picked
  simple. New PREFER_MAX_SHIFT = 12 semitones (one octave) — deliberately
  wider than MAX_SHIFT, which exists specifically because a major 3rd is
  "about where the tape-speed shift starts reading as wrong rather than
  as the instrument" (instrument_sampler.py's own MAX_SHIFT comment). He
  knowingly traded some of that headroom for consistency.
- Verify by: measured before/after on 15 freshly generated real beats
  (Doc Day, Mustang, Wonky) using the real sample library — before: the
  large majority of chord slots used 2+ different files; after: 11/34
  (32%). Full suite: 732/732 passed both times (no test explicitly
  covered this — it's provenance/audio-character, not structure — so
  this was verified by direct measurement on real output, not a new
  automated check).
- Known ceiling (ponytail-flagged in instrument_sampler.py's
  PREFER_MAX_SHIFT comment): a chord spanning more than an octave still
  switches packs, and reused notes near the edge of that octave will be
  pitch-shifted further than the house's own "starts sounding wrong"
  line. Upgrade path if this isn't good enough by ear: same-pack fallback
  before cross-pack fallback (the "better, more work" option he didn't
  pick this time).
- Status: open — owner hasn't heard beats rendered under the wider
  reuse range yet. The chipmunk-tradeoff risk is real, flagged, not
  hidden.

### 2026-07-29 Owner audit: silence, downbeat, and stacking rules flipped; glue compression added
- Context: after getting a plain-language list of every hard-coded
  instrument/drum rule in the core engine (not per-DJ), owner reviewed it
  and changed four things, explicitly: new rules overrule any old rule
  that conflicts.
- Decision/change, one line each (all in tools/beat_machine.py unless
  noted):
  (1) Kick/snare/clap ("BACKBONE") can now go fully silent for a whole
      bar — removed the 2026-07-17 "never a gap" floor from vary_preset's
      four structural treatments (thinbar/frisson/bshift/breath) and the
      contrast-deepening pass. IMPORTANT CAVEAT caught by tests: that
      floor was sharing one code path with a DIFFERENT, still-valid rule
      — CANON lanes (the figure that DEFINES a subgenre, e.g. reggaeton's
      snare, owner rule 2026-07-19) were protected by the same
      `backbone = BACKBONE | canon` variable. Removing it wholesale broke
      2 genre tests (a reggaeton stopped being a reggaeton). Fixed by
      re-adding CANON-only protection (softens, never vanishes) separate
      from the now-removed BACKBONE protection.
  (2) The kick's downbeat can move now (_mutate_kick no longer excludes
      index 0 from the drop/slide roll) — was hard-pinned since
      2026-07-16.
  (3) No melodic stacking at all, ever, not even 2 parts, not even the
      chip voice, no rare "passing" 3rd part — part_count is hardcoded to
      1 in _build_chords, overriding the 2026-07-25 "up to 3 parts"
      feature (theory/arrangement.md, melody_part_weights,
      passing_note_p). That machinery is left in place but unreachable —
      not torn out — same call as the 2026-07-29 bassline rule above.
  (4) Added tools/groove.py:glue_compress — a bus "glue" compressor
      (envelope from L+R sum via a new lp1 helper, soft downward ratio,
      same gain both channels). Runs in tools/crew.py right before
      master(), always on (not gated by clean_renders — this is mix glue,
      not "dirt"). Tunables in OWNER_TASTE (glue_threshold_db -18,
      glue_ratio 1.8, glue_env_ms 25, glue_makeup_db 2) — starting
      numbers, not auditioned yet.
- Reasoning: owner explicit — "if there are other rules that conflict
  with these rules, the new rules overrule." Kept the old multi-part
  layering code dormant rather than deleted (same pattern as the
  bassline rule) in case it's wanted back — flipping it is a 1-line
  change (part_count = 1 → the old roll logic), not a rebuild.
- Known simplification (ponytail-flagged in the code): glue_compress uses
  ONE symmetric smoothing time constant for its envelope, not separate
  attack/release. A real glue comp eases in fast and lets go slow, which
  is where the "pump"/groove character comes from — this version only
  breathes at one speed. Upgrade path is in the function's docstring
  (two lp1 passes at different speeds, combined with np.maximum).
- Verify by: updated/added tests for all four changes
  (test_backbone_can_go_fully_silent_for_a_bar,
  test_layering_never_happens_always_one_voice,
  test_never_more_than_one_melodic_part — folds in what were 3 separate
  2-part/3-part/passing-note tests — plus 2 new glue_compress sanity
  tests in test_groove.py). Full suite: 730/730 passed. Not yet verified:
  owner hasn't heard a rendered beat under any of these four changes, and
  the glue compressor's numbers (-18/1.8/25ms/+2dB) are un-auditioned
  starting points, not tuned by ear yet.
- Status: open — needs his ear on all four, especially the glue
  compression numbers and whether the now-open kick/downbeat variation
  still sounds like the intended DJ personalities.

### 2026-07-29 Hard rule: no melodic bassline, ever
- Context: owner wants to play the bassline himself in Reason. The
  generator already told apart three low sounds — kick drum, bass drum/
  808 (the boom under the kick), and the melodic bassline that follows
  the chords (lane family "chordbass", bass0..N) — but the bassline was
  still opt-out per beat (typing "no bass" in the notes box), and would
  render itself from his own bass samples by default when available.
- Decision/change: one-line change in tools/beat_machine.py's
  _build_chords — `bass_idx` is now hardcoded to None instead of
  scanning his bass library, so bass0..N lanes never get built,
  regardless of notes-box wording. This is the single choke point: both
  callers of _build_chords (new beats, and rebuilding an old beat from
  its saved recipe) go through it, so old saved beats also lose their
  baked-in bassline on rebuild. Kick and the 808 bass drum are untouched.
- Reasoning: traced every place a melodic bassline could get created —
  only _build_chords does it (via instrument_sampler.scan_bass); crew.py,
  genres.py, and the other make_*.py scripts don't have their own bass
  logic (make_hiphop_tracks.py is retired as a generator, kept only as an
  imported helper library). One line, one file, covers every path.
- Verify by: updated the 4 tests that asserted a bassline gets built
  (test_rebuild_regenerates_chord_audio_and_stacks_sequential_trims,
  test_chords_direction_adds_a_harmony_layer,
  test_chord_bass_line_comes_from_his_own_bass_samples — renamed
  test_chord_bass_line_is_never_rendered and inverted, since its whole
  premise is now the opposite rule — and
  test_harmony_opens_under_the_drums_with_per_bar_dynamics). Full suite:
  732/732 passed.
- Status: confirmed — verified by test suite; owner hasn't heard a
  rendered beat under the new rule yet.


---

## Index of archived entries (full text in `DECISIONS-ARCHIVE.md`)

| date | entry | status |
|---|---|---|
| 2026-07-25 | One stack becomes up to three separate PARTS | open |
| 2026-07-25 | Tracks stopped playing — three bugs behind one symptom | open |
| 2026-07-25 | Kick drum, bass drum and bass are three different things | open |
| 2026-07-25 | Reason demoted, not removed — portability boundary set | open |
| 2026-07-25 | Packaging decided: one app two doors; brief written (PACKAGING-GAP-ANALYSIS.md) | open |
| 2026-07-25 | Reason Voice v2 web UI verified working end-to-end (first real check) | confirmed |
| 2026-07-24 | Chip voice added to Farrow ("Pharaoh") — checked it's real | open |
| 2026-07-24 | Pre-07-23 upgrade — FINAL BATCH: last 3 legends, backlog CLOSED | open |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 4: ALL 18 GENRES NOW SIGNED | open |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 3 (3 soul/orchestral legends + 1 genre) | open |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 2 (4 genres that had NO signature) | open |
| 2026-07-24 | Key parser missed the "<Key>Maj/<Key>Min" spelling — synth | confirmed |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 1 of the backlog (4 identities) | open |
| 2026-07-24 | Chiptune was inaudible — chords never rendered unless the | confirmed |
| 2026-07-24 | First four legends WERE skimmed — audited, deepened; modes | open |
| 2026-07-24 | All nine DJs get harmony; harmony joins evolution; 4 silent | open |
| 2026-07-24 | New Math deepened — "arithmetic you can hear" (my design) | open |
| 2026-07-24 | Chiptune: the ONE sanctioned synth exception, + a recipe | open |
| 2026-07-24 | G-Funk reweighted after "does not read sunnier" — plus the | confirmed |
| 2026-07-24 | Genre harmony: 6 of 17 styles given a researched signature | partly |
| 2026-07-24 | The click at the end of samples — TWO real defects, both fixed | open |
| 2026-07-23 | ALL melodic instruments are sampled now; every synth deleted | open |
| 2026-07-23 | Brass is SAMPLED now — synth horn deleted, multi-sample built | open |
| 2026-07-23 | Volume control for every sound — one feature request, three bugs found chasing it | confirmed |
| 2026-07-23 | Bug fix: bass/vox lanes played but were invisible to the recipe (his "weird vocal" re | confirmed |
| 2026-07-23 | Drum-loop lane REMOVED after one audition batch | confirmed |
| 2026-07-23 | Phase 2 placement: bass/808, vox, and full-loop lanes | partly |
| 2026-07-23 | Sourcing rework: whitelist the folders + stop the one-shot rule | confirmed |
| 2026-07-23 | Sound-library expansion, phase 1: Downloads packs consolidated onto TBOTC 3 | confirmed |
| 2026-07-23 | "Add the root" turned back ON — and finally given a test | confirmed |
| 2026-07-23 | Kick flavor goes back to per-style — engine-wide clean-punch reversed | confirmed |
| 2026-07-23 | Flavor-index history went stale across the rule change — first 3 beats were not a fai | confirmed |
| 2026-07-23 | MIDI validity gate was failing every chord beat — the gate was stale, not the beats | confirmed |
| 2026-07-23 | Mustang (DJ Mustard) harmonic signature — 5th legend, first one NOT in the research d | open |
| 2026-07-23 | Engine-wide clean-punch kick now visibly fights Mustang's own identity | open |
| 2026-07-23 | Timberline (Timbaland) harmonic signature — resolved the dual-tempo-pocket fork | open |
| 2026-07-23 | J Dillo pinned to 2/4-bar only ("no long beats") | confirmed |
| 2026-07-23 | J Dillo (Dilla) harmonic signature added — 3rd legend, owner approved moving on | open |
| 2026-07-23 | DJ Premium (Premier) harmonic signature added — next legend after Dre | open |
| 2026-07-23 | Dre tuning (best-of #843/845/849) + engine-wide clean-punch kicks | open |
| 2026-07-22 | Dre chords: rhythmic arp + m7 removed (audition #845-847 feedback) | failed |
| 2026-07-22 | Wired harmonic identity (signature) into chord synth; Dre audition | confirmed |
| 2026-07-22 | Strings sampler scaffolded + chords audition batch rendered | open |
| 2026-07-22 | chord_synth loop-pad substitution: allow melody role, chop loop-kind files | open |
| 2026-07-22 | Paused the crew-variety autoresearch loop | confirmed |
| 2026-07-23 | Closed harmony-signature research for all 12 legends | open |
| 2026-07-23 | Wired No Alias's harmony signature + rendered audition batch | confirmed |
| 2026-07-23 | Wired Swish Beatz's harmony signature + rendered audition batch | confirmed |
| 2026-07-23 | Wired Razor's harmony signature + rendered audition batch | open |
| 2026-07-23 | Corrected a false "alt field" assumption; wired 3 more legends | open |
| 2026-07-23 | Built the two missing instrument engines (lead synth + scratch) | open |
| 2026-07-23 | Wired Just Flame — all 12 legends now have a signature | open |
| 2026-07-23 | Skills-compliance check found a real gap (midi-validity-gate) | confirmed |
| 2026-07-23 | Horn tone REJECTED on audition; Just Flame parked; demos built | open |
| 2026-07-25 | Packaging step 0 — the portability boundary was NOT already true | confirmed |
| 2026-07-25 | Packaging step 1 — manifest carries the harmony; a second name leak found | confirmed |
| 2026-07-25 | Packaging step 2 — old recipes: nothing to fix, so it got a test instead | confirmed |
| 2026-07-25 | Packaging step 3 — "why this works" on the beat card | open |
| 2026-07-25 | Packaging step 4 — one launcher starts both halves | confirmed |
| 2026-07-25 | Packaging step 5 — MAKE / STUDIO tabs; MVP (steps 0-5) complete | open |
| 2026-07-25 | Owner's first verdict on the MVP -> three changes shipped | open |
| 2026-07-25 | "No instruments, only drums" -> chords_default roster-wide; logo shared | open |
| 2026-07-25 | Chord voices: his samples only, one instrument per beat, layering | open |
| 2026-07-25 | Real 8-bit sounds preferred over the synth chip; float-WAV bug | open |
| 2026-07-25 | "Where are my instruments" — the LABEL was the bug; synth bass removed | open |
| 2026-07-25 | Chord stems removable, 1 dB arrows, and a mix that opens quiet | open |
