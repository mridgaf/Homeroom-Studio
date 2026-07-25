# Handoff to Claude Code — Packaging: one app, two doors

Paste the block below as your first message to Claude Code, working in the
`~/Desktop/Homeroom Studio` folder.

---

## Kickoff message (copy everything below)

> Read `PACKAGING-GAP-ANALYSIS.md`, then `CLAUDE.md`, then the most recent
> entries in `DECISIONS.md`, before doing anything.
>
> The goal: the beat generator and Reason Voice are already one project with two
> front doors and no handoff between them. Close that. The full plan and
> reasoning are in the packaging doc. Follow its **Part 4 punch list in order**.
>
> Rules to respect:
> - Run `pytest` first and tell me the baseline count before changing anything.
>   Keep it green after every step.
> - Target Python 3.9 (`from __future__ import annotations` for `X | Y`).
> - Do NOT touch `remote/`. Do NOT change either web server's framework. Do NOT
>   touch `_resolve_beats_root()`. The full don't-touch list is in Part 4.
> - No real producer names in `.recipes/*.json` — codenames only. See Part 5.
> - Stop and show me after each punch-list step so I can approve before you move
>   on. Don't batch steps.
>
> One boundary is non-negotiable and is explained in Part 4a: **`tools/` must
> never import from `reason_voice/`.** It's already true; step 0 adds the test
> that keeps it true. Reason is an optional layer on top of a DAW-neutral
> generator, not a dependency of it.
>
> Start with step 0 (the boundary test), then step 1 (enrich the manifest) and
> step 2 (reader tolerance for old beats). Then render one beat and show me its
> `.recipes/NN.json` with the key, progression, and roman numerals in it — that's
> the first proof it works.
>
> When we get to step 3, show me the plain-English "why this works" line before
> wiring it into the card, so I can read it and tell you if it sounds like a
> person wrote it.

---

## Notes for you (the owner), not for Code

**The MVP is steps 1–5.** That's one launcher, one page with two tabs, and beats
that explain their own chords. Steps 6–8 are the Reason integration and can wait
until you've used 1–5 for a week.

**Step 3 is the one to care about.** It's the cheapest step and it's the
teaching feature — the thing no competitor has. If you only ever approve one
item on this list, approve that one.

**That decision is now made (2026-07-25, Part 4a):** generator is the product,
Reason is an integration on top. You stay in Reason daily — nothing about your
own workflow changes — but the code never lets the generator depend on it, so
the broader-audience door stays open for free. Step 0 is the test that enforces
it.

**The one cost of that, flagged so it isn't a surprise later:** if you ever go
broad, the recipes and `device_refs/` are written in Reason vocabulary ("Scream
4 → RV7000"). The technique transfers to any DAW; the device names don't. That's
a writing job, not a coding job, and nobody has sized it.

**Two things Code should be made to prove, not claim:**
1. That old beats (pre-change `.recipes/*.json`) still load. Ask to see it load a
   real old one, not a fixture it wrote itself.
2. That the Reason tempo-set in step 7 actually works. Nobody has ever checked
   whether Reason 12 exposes tempo as a Remote item. If it doesn't, the honest
   answer is a button that opens the session and tells you to set the tempo — not
   a feature that silently does nothing.
