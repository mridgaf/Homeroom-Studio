# Autoresearch Dashboard: beat-crew-variety

**Runs:** 18 / 60 | **Kept:** 2 | **Discarded:** 16 | **Crashed:** 0 | **Checks-failed:** 0
**Baseline:** variety: 13.530 pts (#1)
**Best:** variety: 14.068 pts (#2, +4.0%)
**Noise floor:** ±0.15 pts — improvements smaller than this are noise
**Identity gate:** checks.sh (44 tests against the candidate) — required for every keep
**Proposal staged:** `crew_config.proposed.json` = the #2 winner, awaiting owner audition

| # | commit | variety | Δ vs best | status | op | description |
|---|--------|---------|-----------|--------|-----|-------------|
| 1 | e669b82 | 13.530 | — | keep | draft | baseline: candidate = live roster (style v5) |
| 2 | 121fafb | 14.068 (+4.0%) | +0.54 (>floor ✓) | keep | improve | library.p +0.15 for the flagged trap trio |
| 3 | 121fafb | 14.023 (+3.6%) | −0.05 | discard | draft | kick hits ceiling +1 for sparse grammars |
| 4 | 121fafb | 14.062 (+3.9%) | −0.01 | discard | draft | widen backbeat mode weights toward uniform |
| 5 | 121fafb | 13.948 (+3.1%) | −0.12 | discard | draft | flatten kick weight maps w^0.7 |
| 6 | 121fafb | 13.835 (+2.3%) | −0.23 | discard | improve | library.p +0.1 for the other six DJs |
| 7 | 121fafb | 14.120 (+4.4%) | +0.05 (<floor) | discard | improve | trap trio library.p +0.1 more (noise) |
| 8 | 121fafb | 14.040 (+3.8%) | −0.03 | discard | improve | ghost ceilings +1 for 90s heads |
| 9 | 4bd1750 | 13.988 | −0.08 | discard | improve | Night Metro tags +garage +breakbeat |
| 10 | 4bd1750 | 14.020 | −0.05 | discard | improve | Rage Engine tags +techno +electro |
| 11 | 4bd1750 | 14.182 | +0.11 (<floor) | discard | improve | New Math breakbeat 2→3, +house (near-miss) |
| 12 | 4bd1750 | 14.061 | −0.01 | discard | draft | Chrome Dial double_p 0.45→0.6 |
| 13 | 4bd1750 | 14.053 | −0.02 | discard | draft | Glass Cat kick w: open steps 3,6,13 |
| 14 | 4bd1750 | 14.083 | +0.02 | discard | draft | Otto Grit double_p 0.3→0.45 |
| 15 | 4bd1750 | 14.068 | ±0.00 | discard | draft | Sunday Chop hats eighths→0.3 broken→0.4 |
| 16 | 4bd1750 | 14.051 | −0.02 | discard | draft | Night Metro roll_n [1,2]→[1,3] |
| 17 | 4bd1750 | 14.087 | +0.02 | discard | draft | Cutz library.p 0.3→0.15 |
| 18 | 4bd1750 | 14.081 | +0.01 | discard | improve | trap trio library.p +0.05 |
