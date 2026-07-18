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

### Runs 9-18: structured tag/grammar/library tuning experiments (all DISCARD)

All ten experiments fell below the variety threshold (14.219 = 14.068 + 0.15 floor).
Best approach remains Run 2: trap-trio library.p raise.

### Run 9: Night Metro library tags +garage +breakbeat — variety=13.988 (DISCARD)
- Result: worst_dj=12.020, delta vs best −0.08

### Run 10: Rage Engine library tags +techno +electro — variety=14.020 (DISCARD)
- Result: worst_dj=12.020, delta vs best −0.05

### Run 11: New Math breakbeat 2->3, +house tag — variety=14.182 (DISCARD)
- Result: worst_dj=12.020, delta vs best +0.11

### Run 12: Chrome Dial kick double_p 0.45->0.6 — variety=14.061 (DISCARD)
- Result: worst_dj=11.955, delta vs best −0.01

### Run 13: Glass Cat kick w: open steps (2->4, 1->3, 1->3) — variety=14.053 (DISCARD)
- Result: worst_dj=11.881, delta vs best −0.02

### Run 14: Otto Grit kick double_p 0.3->0.45 — variety=14.083 (DISCARD)
- Result: worst_dj=12.020, delta vs best +0.01

### Run 15: Sunday Chop hat modes (eighths 0.45->0.3, broken 0.25->0.4) — variety=14.068 (DISCARD)
- Result: worst_dj=12.020, delta vs best 0.00

### Run 16: Night Metro hat roll_n [1,2]->[1,3] — variety=14.051 (DISCARD)
- Result: worst_dj=12.020, delta vs best −0.02

### Run 17: Cutz library.p 0.3->0.15 — variety=14.087 (DISCARD)
- Result: worst_dj=12.020, delta vs best +0.02

### Run 18: trap trio library.p +0.05 fine step — variety=14.081 (DISCARD)
- Result: worst_dj=12.020, delta vs best +0.01

## Session Conclusion
All tag/grammar experiments produced no measurable improvement over Run 2's baseline.
Metric ceiling appears reached: variety plateau at ≈14.08, noise floor 0.15, so
no configuration in this neighborhood moves the needle. Next opportunity: changes
to KICK_BANK or the scoring harness itself (out of scope for crew_config.json tuning).
Run 20: discard mean=13.782 — New Math tags: breakbeat 2->3, +house
Run 21: discard mean=13.736 — Night Metro tags +garage +breakbeat
Run 22: discard mean=13.704 — Rage Engine tags +electro
### Run 23: Otto Grit tags +soul — 13.726 (DISCARD)
### Run 24: Crate Prophet tags +motown — 13.726 (DISCARD)
### Run 25: Chrome Dial tags +electro — 13.713 (DISCARD)
Run 23: discard mean=13.726 — Otto Grit tags +soul
Run 24: discard mean=13.726 — Crate Prophet tags +motown
Run 25: discard mean=13.713 — Chrome Dial tags +electro
Run 26: discard mean=13.710 — Glass Cat minimal weight 2->3
Run 27: discard mean=13.637 — Sunday Chop motown 2->3
Run 28: discard mean=13.752 — Cutz funk 1->2
Run 29: discard mean=13.694 — non-trio six DJs library.p +0.1
Run 30: discard mean=13.734 — trap trio library.p +0.05
Run 31: discard mean=13.789 — New Math jungle 1->2, dnb 1->2
Run 32: discard mean=13.758 — Night Metro cloud-rap 2->3
Run 33: discard mean=13.598 — Rage Engine drill 2->3
Run 34: discard mean=13.756 — Otto Grit lofi 3->4
Run 35: discard mean=13.714 — Crate Prophet soul 2->3
