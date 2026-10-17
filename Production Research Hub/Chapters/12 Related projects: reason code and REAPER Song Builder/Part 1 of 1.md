# Chapter 12: Related projects: reason code and REAPER Song Builder
## Part 1 of 1

_The recipe-translation brain and the REAPER song builder, as described in their own notes._

**In this part:**
- CLAUDE.md — Reason code — the translation brain
- README.md — REAPER Song Builder

(Next: end of chapter)


=====================================================
SOURCE FILE: CLAUDE.md
ORIGINAL LOCATION: RC:CLAUDE.md
=====================================================

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

=====================================================
SOURCE FILE: README.md
ORIGINAL LOCATION: RSB:README.md
=====================================================

# REAPER Song Builder

Double-click **Start Song Builder.command**. A local page opens in your browser. Drop a Homeroom Song Sketch ZIP, edit or randomize the sections, and click **Create in REAPER**. The project and every WAV it needs are saved together in `~/Desktop/REAPER Song Builder Songs/`. Each build gets a new folder; existing projects are never replaced.

New Song Sketch ZIPs contain `source_stems/` and allow clean 2-, 4-, or 8-bar arrangements. Older ZIPs still work: the helper cuts their four rendered sections into reusable variations, although those sections already contain baked levels and effects. The page offers editable section order, length, variation, scene, drum breath, and fades. New ZIPs receive track volume envelopes for scenes and moves.

The helper opens the finished project in REAPER when REAPER is closed. If REAPER is already running, it leaves that session alone and shows the new project path. The helper does not touch the Homeroom beat library or an existing REAPER project.

Run the included checks with `/usr/bin/python3 -m unittest test_builder.py` from this folder. No packages need to be installed for the helper.

=== END OF PART ===
