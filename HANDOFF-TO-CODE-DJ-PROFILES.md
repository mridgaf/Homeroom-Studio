# Handoff to Claude Code — wire in the DJ production-profile research

Paste the block below as your first message to Claude Code, working in the
`~/Desktop/Homeroom Studio` folder.

---

## Kickoff message (copy everything below)

> Read `CLAUDE.md`, the most recent entries in `DECISIONS.md`, and
> `.claude/skills/drum-loops/references/techniques.md` before doing anything.
>
> There's a new file at the project root: `dj_production_profiles.json`. It's
> per-persona production research for all 9 crew personas (Otto Grit, Cutz,
> Crate Prophet, Chrome Dial, Glass Cat, Sunday Chop, Night Metro, Rage Engine,
> New Math), researched against each persona's real reference artist (from
> `crew_config.json`'s `built` field) and cross-referenced against what's
> already implemented. Each persona has 5 categories — tempo_swing,
> drum_layering, harmonic_tendencies, arrangement_structure, mix_character —
> each with a `rules` list (short imperative statements) and a `grounded_in`
> string citing the exact `crew_config.json` field/value it matches or
> extends. Some personas also carry extra notes (`gear_note`, `workflow_note`,
> `background_note`, etc.) — quotes and technique details from primary
> sources that didn't fit the fixed schema.
>
> **Part 0 — gap analysis first, no code changes yet.** For each persona, walk
> its `rules` against the current implementation in `crew_config.json`,
> `tools/crew.py`, `tools/groove.py`, and `techniques.md`. Most rules already
> match what's live (that's what `grounded_in` is pointing at — treat those as
> confirmation, not work). Pull out only the real deltas: a rule that isn't
> reflected in the running code, or that sharpens/corrects something already
> there (there's at least one known correction already made in the profile
> itself — Cutz's early sampler — check the `sources` field for it and any
> others). Write the delta list as a short punch list, same shape as
> `BEAT-GENERATOR-GAP-ANALYSIS.md` / `PACKAGING-GAP-ANALYSIS.md`, and show it
> to me before touching any code.
>
> Rules to respect:
> - Run `pytest` first and tell me the baseline count before changing
>   anything. Keep it green after every step.
> - Target Python 3.9 (`from __future__ import annotations` for `X | Y`).
> - Do NOT touch the `remote/` Reason bridge.
> - A confirmed rule gets wired in the same way `techniques.md`'s numbers were
>   wired into `groove.py`: a documented, testable function or constant, not a
>   loose comment. If a delta is genuinely `[contested]` or a judgment call
>   (like the Dilla snare-direction question already flagged in
>   `techniques.md`), render both and let my ears decide — don't silently
>   pick one.
> - `dj_production_profiles.json` and its `sources` cite real producer names —
>   that's fine, it's an internal research file like `techniques.md`, not
>   shipped output. Keep the existing house rule: no real producer names land
>   in `.recipes/*.json` or anything public-facing. Codenames only there.
> - Stop and show me after each punch-list step so I can approve before you
>   move on. Don't batch steps.
>
> Start with Part 0. Once I approve the punch list, start with whichever item
> is cheapest to prove — render one beat per touched persona, before/after,
> so I can hear the delta.

---

## Notes for you (the owner), not for Code

**What this is:** the output of a research pass (Sept 2026, TinyFish-sourced —
real interviews and engineer commentary, not summaries) done one persona at a
time against each crew member's actual reference artist. It's meant to sit
alongside `techniques.md` as a second research reference — `techniques.md` is
cross-persona/engine-wide, `dj_production_profiles.json` is per-persona.

**Why Part 0 comes first:** most of this file is already true in the running
engine — `crew_config.json` was the ground truth the research was built
against, not the other way around. The real value is the small number of
places research turned up something the engine doesn't do yet, or a detail
that sharpens something it already does. Making Code find those deltas
explicitly, and show you the list before writing anything, keeps this from
turning into a rewrite of code that's already tuned by ear.

**One correction already caught:** Cutz's (DJ Premier's) early sampler is an
Akai S900, not an E-mu S950 — the file's own `sources` notes this fix. Worth
checking whether that distinction matters anywhere in code (gear character
modeling) or if it's just documentation.
