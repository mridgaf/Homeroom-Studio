# Reason code — the translation brain

The toolkit that turns "how do I get that sound" into steps you can follow in
Reason 12. Recipes, device parameter maps, audio analysis. The recipe book
itself lives on the TBOTC 3 drive, not here — this folder is the machinery
that writes it, not the writing.

## This is one half of a pair

The other half is **~/Desktop/Homeroom Studio** — the Beat Machine, the crew,
the sample library tools. Same owner, same music, same house rules. They go
hand in hand; treat them as one body of work.

**Its names — all one project, don't treat them as separate:**
**Beat Generator = Beat Machine = Homeroom = Homeroom Studio = Homeroom Studios
= `~/Desktop/Homeroom Studio`.** The owner uses these interchangeably. If a
request names any of them, it means that folder.

- Its house rules and hard rules: `~/Desktop/Homeroom Studio/CLAUDE.md`
  **Read it at the start of any substantive session here.** It holds the
  drive-safety rules, the move-don't-delete rule, and the explain-like-I'm-five
  rule, all of which apply to this folder too.
- Its decision ledger: `~/Desktop/Homeroom Studio/DECISIONS.md`
- The shared skills are symlinked into `.claude/skills` here, so both folders
  see the same set. Edit them in either place — it's one directory.

## Hard rules that apply here

- **Explain like I'm five.** Plain words, paste-able commands, no untranslated
  jargon. This holds for every answer, not just the tutorials.
- **Move, never delete.** Any cleanup goes to one dated holding folder with a
  manifest. See the `safe-file-ops` skill.
- **No API key by design.** This toolkit does not call a paid model. Keep it
  that way — feed the recipe book, don't rebuild it as a service.
- **The recipe book is fed, not regenerated.** Recipes are tested and hand-
  confirmed one at a time; a bulk rewrite throws away what was verified by ear.

## What's in here

- `recipe.py` — builds a recipe brief, grounded in real device parameters
- `scan_rack.py` — reads a Reason rack; `--params` pulls canonical parameter
  names out of the Remote map files (46 devices, 3700+ names)
- `device_params.json`, `devices.json`, `calibration.json` — the extracted data
- `audio_analysis_pipeline.py` — before/after measurement for recipe testing
- `tests/` — `test_recipe.py`, `test_analysis.py`

## Verifying an audio recipe

Measure the **finished bounce**, before and after, and compare them as deltas —
not one file against absolute targets. The `audio-fix-verify` skill has the
full procedure and the failure it exists to prevent.
