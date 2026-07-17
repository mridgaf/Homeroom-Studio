# Worklog: beat-crew variety autoresearch

Session started 2026-07-17. Goal: tune the candidate roster
(`experiments/crew_config.candidate.json`) for compose-time variety;
winners staged as a proposal for owner audition, live config untouched.

## Data summary (become-one-with-the-workload pass)
- Engine: `pattern_gen.compose()` — per-DJ grammar → fresh pattern per
  generation. Kick starts from a curated bank skeleton 75% of the time
  or a groove-library seed (per-DJ `library.p`, wired 2026-07-17), else
  freestyles from the 16 step weights. Repeat guards: compose-time
  `_too_close` (<3 moves) + render-time `kick_seen` on final patterns.
- Variety scorer findings on the real library (2026-07-17): Night
  Metro, Rage Engine, New Math had kick lines within 1-2 moves across
  their last 10 rendered beats (pre-final-guard renders). Sparse
  halftime grammars have the fewest legal kick placements → least
  headroom; that is where tuning should help most.
- Sanity gate: crippling the candidate (no seeds/guests, one mode,
  2-hit kicks) drops variety 13.53 → 10.05. Metric responds correctly.
- Noise floor: stddev 0.15 over seeds 1-5 (13.423..13.757).

### Run 1: baseline (candidate = live config) — variety=13.530 (KEEP)
- Timestamp: 2026-07-17
- What changed: nothing; candidate is a byte copy of the live roster
  (style v5, groove library wired, all nine DJs).
- Result: variety=13.530, worst_dj=11.656, seed_rate=0.398,
  guest_rate=0.528
- Insight: worst_dj ≈ 2 pts under the mean — the sparse styles drag.
- Next: draft structurally different directions before greedy tuning —
  (a) raise sparse DJs' kick `hits` ceilings by 1, (b) flatten the top
  of each kick `w` map, (c) raise `library.p` across the board,
  (d) widen backbeat mode weights toward uniform.

## Key Insights
- (accumulates)

## Next Ideas
- Per-DJ `library.p` raise for the three flagged trap-side DJs first.
- Backbeat `ghosts` ceilings +1 for the 90s heads.
- `extras.nmax` 1→2 where taste allows (owner rule caps ONE guest lane
  in the sparse-bed era — check constraint before trying).

### Run 2: library.p +0.15 trap trio — variety=14.068 (KEEP)
- What changed: Night Metro / Rage Engine / New Math library.p 0.35/0.35/0.40 → 0.50/0.50/0.55
- Result: +0.54 vs baseline (3.6× floor); worst_dj 11.66→12.02; checks 44/44
- Insight: the flagged clustering DJs benefit most from external seeds.

### Runs 3-8: drafts + refinements (all DISCARD)
- hits ceiling +1 (−0.05), backbeat widening (−0.01), w^0.7 flatten (−0.12),
  library.p for other six (−0.23!), trap trio +0.1 more (+0.05, noise), ghosts +1 (−0.03)
- Insight (meta): the metric is kick-dominated; library seeding helps only
  DJs with big genre pools + sparse grammars. Six-DJ raise HURT — small
  pools repeat seeds. Backbeat/ghost knobs barely move the metric.

## Key Insights
- Groove-library seeding is the highest-leverage variety knob, but ONLY
  for the trap trio. Don't generalize it.
- Kick-centric metric: backbeat/ghost knobs need their own weight if we
  ever want to tune them (would require harness change = re-baseline).

## Next Ideas
- Genre tag weights: give Night Metro garage/breakbeat tags (bigger pool).
- KICK_BANK is code, not config — out of scope, but a config-side "bank
  skip" probability (use freestyle more) could be proposed as an engine knob.
- extras pool additions per DJ (new_color-style) — small metric effect
  expected but cheap.
