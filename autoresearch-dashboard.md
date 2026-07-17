# Autoresearch Dashboard: beat-crew-variety

**Runs:** 8 / 60 | **Kept:** 2 | **Discarded:** 6 | **Crashed:** 0 | **Checks-failed:** 0
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
