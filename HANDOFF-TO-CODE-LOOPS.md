# Handoff to Claude Code — Loops Mode

Paste the block below as your first message to Claude Code, working in the
`~/Desktop/Homeroom Studio` folder.

---

## Kickoff message (copy everything below)

> Read `LOOPS-MODE-GAP-ANALYSIS.md`, then `CLAUDE.md`, then the most recent
> entries in `DECISIONS.md`, before doing anything.
>
> The goal: a new, standalone "Loops" page — same DJs, same personalities —
> where each DJ hands me a usable melodic or drum loop instead of a full
> arranged beat, ready to drop into Reason. The full plan and reasoning are
> in the gap-analysis doc. Follow its **Part 4 punch list in order**.
>
> Rules to respect:
> - Run `pytest` first and tell me the baseline count before changing
>   anything. Keep it green after every step.
> - Target Python 3.9 (`from __future__ import annotations` for `X | Y`).
> - Do NOT touch `remote/` or anything in `reason_voice/`.
> - Do NOT change `compose()` or anything on the full-beat arrangement path.
>   This feature reads the same DJ configs and sample libraries but is a
>   separate page with its own new functions — see Part 4a for exactly which
>   existing hard rules stay untouched and why.
> - Step 0 is a test that proves loop mode never calls into the
>   arrangement-slot code (`_pin_bars_for_loop_voice`, `PREFER_MAX_SHIFT`
>   gating). Write and pass that test before anything else.
> - No DJ signature field (chord_source, key/mode weighting, genre tags)
>   should ever *exclude* a sound on this page — only weight toward it, on a
>   per-DJ roll defaulting to 50/50. See Part 3 and Part 4 step 2.
> - Stop and show me after each punch-list step so I can approve before you
>   move on. Don't batch steps.
>
> Start with step 0 (the boundary test), then step 1 (scored, non-excluding
> lookups) and step 2 (`pick_loop()`). Before wiring up any real audio
> rendering, show me `pick_loop()` running dry (just printing which file it
> picked and whether it was a taste-pick or a free-pick) across a few dozen
> rolls for one DJ, so I can see the 50/50-ish split is real before you
> build anything on top of it.

---

## Notes for you (the owner), not for Code

**Three things are flagged as open in the gap-analysis doc (Part 5 and
Part 6) that Code should raise with you, not decide alone:**

1. The loop filename/output-folder convention — I proposed one, but it's a
   guess, not a decision.
2. Whether a melodic loop defaults to whole or chopped.
3. The `"_loops"` bucket's `tonal` flag has never actually been read by any
   code before — worth Code proving it's populated correctly before either
   of you trusts it.

**The hard-rule scoping in Part 4a is the one thing to double-check.** I
scoped "no rules should hinder the DJs' sound choice" to apply only to this
new Loops page, and explicitly kept the existing hard rules (no drum loops
in beats, one-instrument-per-chord, 4-bar-if-loop) intact for the beat
builder. That's how I read your instruction — flag me if you meant
something broader.
