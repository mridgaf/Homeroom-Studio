# Autoresearch: beat-crew variety (tune-then-audition)

> The metric is the sole arbiter. "This looks better" never drives a
> keep/discard — only a measured improvement that clears the noise floor
> does. And even a kept winner is only a PROPOSAL: nothing reaches the
> live `crew_config.json` until the owner's ears approve a sample batch.

## Objective
Tune the nine DJs' style numbers in a CANDIDATE copy of
`crew_config.json` so that composed beats land further apart —
rhythmically, in kick flavor, in backbeat mode, in timekeeper density —
while every character identity constraint still holds. The workload:
`pattern_gen.compose()` writes a fresh pattern per generation from each
DJ's grammar (per-step kick weights, backbeat/timekeeper mode weights,
kick flavors, guest palette, groove-library taste). Variety failures the
owner has actually reported: kick lines clustering within 1-2 moves
(seen in Night Metro / Rage Engine / New Math's last 10 rendered beats),
one kick flavor streaking, one skeleton mutated forever. Sparse styles
(Glass Cat, Night Metro) have the least room to move, so `worst_dj`
is tracked to stop the mean hiding a collapsed character.

What the knobs are (per DJ, in the candidate JSON):
- `grammar.kick`: `w` (16 step weights), `hits` [lo,hi], `double_p`
- `grammar.<snare|clap>`: `modes` weights, `ghosts` [lo,hi], `gcells`
- `grammar.<hat|snap>`: `modes` weights, `open_p`, `roll_n`
- `kick_flavors`: [weight, must, wants, choke-range] rows
  (HARD RULE: long-sustain 808 rows — must="808", hi>=1.2 s — keep
  weight <= 0.2; the streak-breaker and tests enforce it)
- `extras`: guest `p`, `nmax`, `pool`
- `library`: groove-seed `p`, genre `tags` weights

## Metrics
- **Primary**: variety (points, higher is better) — per-DJ mean of:
  capped min pairwise kick moves + 0.5·mean kick moves + 0.5·mean full-
  pattern moves + 0.5·distinct backbeat bars + 0.25·timekeeper density
  spread + 0.5·distinct kick flavors, over 12 composed variants.
- **Secondary**: worst_dj (the weakest character's score — a rising mean
  must not hide one DJ collapsing), seed_rate, guest_rate.
- **Noise floor**: 0.15 (stddev over 5 seeds of the unchanged baseline)

## Budget
- maxRuns: 60 | maxSeconds: none | targetMetric: none
- Per-experiment wall-clock cap: 300 s (perl alarm inside the harness)

## How to Run
`./autoresearch.sh [SEED]` — scores `experiments/crew_config.candidate.json`
compose-only (no audio, no sample library, temp pattern history; the
owner's live files are never touched). Outputs `METRIC name=number`.

## Files in Scope
- `experiments/crew_config.candidate.json` — THE ONLY FILE EXPERIMENTS
  EDIT. A tuned copy of the live roster; grammar numbers, kick flavors,
  extras, and library taste per DJ.

## Off Limits
- `autoresearch.sh`, `checks.sh`, `experiments/score_variety.py`,
  `tools/variety.py` — the eval harness is locked.
- `crew_config.json` (the LIVE roster — owner audition only),
  `tools/*.py`, `tests/*`, everything else in the repo.
- `~/.reason_voice/*` and `~/Documents/Samples/*` (the owner's state
  and beat library) — the harness never touches them; experiments must
  not either.

## Constraints
- `checks.sh` must pass for any keep: the engine's identity tests run
  WITH THE CANDIDATE LOADED (Cutz's backbeat anchors, Night Metro's
  halftime, New Math's quintuplets, the 808 rules, the variety floors).
  A candidate that wins the metric by destroying a character is
  `checks_failed`, never kept.
- All nine DJs stay in the file; no lane renames; timing DNA
  (`lanes` feel numbers) and stamps are not knobs.
- `extras.nmax` stays 1 — owner rule 2026-07-17: these are sparse BEDS
  for live playing, max ONE guest lane per beat. More guests would
  raise the metric and break the product.
- Deltas <= noise floor (0.15) are noise — discard.
- Ending state: the branch's final candidate is copied to
  `crew_config.proposed.json` with a plain-words summary of every kept
  change — the owner auditions a sample batch before anything merges.

## What's Been Tried
(updates as experiments accumulate)
