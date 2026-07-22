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
