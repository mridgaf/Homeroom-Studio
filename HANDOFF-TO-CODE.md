# Handoff to Claude Code — Beat Generator: add harmony

Paste this as your first message to Claude Code, working in the
`~/Desktop/Homeroom Studio` folder.

---

## Kickoff message (copy everything below)

> Read `BEAT-GENERATOR-GAP-ANALYSIS.md` and `CLAUDE.md` in this folder before
> doing anything.
>
> The goal: this drum engine should also generate **in-key chords and bass** from
> my own sample library — not just drums. The full plan and reasoning are in the
> gap-analysis doc. Follow its **Part 4 punch list in order**.
>
> Rules to respect:
> - Run `pytest` first and confirm it's green before changing anything. Keep it
>   green after every step.
> - Target Python 3.9 (`from __future__ import annotations` for `X | Y`).
> - Do NOT touch the `remote/` Reason bridge.
> - Build MIDI ingestion first (safest), then melodic loops, then audio fitting.
> - Stop and show me after each punch-list step so I can approve before you move on.
>
> Start with step 1 (the KeyContext) and step 4 (MIDI ingestion). Show me a
> generated in-key chord progression from one of my MIDI packs as the first proof
> it works.

---

## Two things still open (tell Claude Code, or decide first)

1. **Full sample-library inventory is NOT done.** Only the Cymatics packs in
   "2022 sample packs" were scanned. The other libraries — "Sample Packs -
   Downloads Backup", "Function Loops", "Live loop cds", "London Symphonic
   Strings" — have not been counted. More melodic material = better output.
2. **The "legends" question.** `legends_config.json` names real producers. Decide
   keep-internal / rename / drop before anything ships publicly. Not a blocker for
   building.
