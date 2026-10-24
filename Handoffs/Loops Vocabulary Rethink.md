# Loops side: rethink vocabulary, hooks and loop types (new chat, 2026-10-23)

**Owner's ask:** before any Loops-side settings are built, work out three things together.
1. **How the vocabulary (the listen-line words) and the hooks actually work together.** Which words reach which settings on the Loops side.
2. **Whether there are enough loop types.** What kinds of loops the engine can pick from versus what the research lines call for.
3. **How the other descriptive words (mood, texture, era, etc.) can change which loops are picked or how they are finished.** Right now they may do nothing there.

**Questions only, no building, no renders.**

## Already decided (this session)
- Research and the listen line are shared by both sides. Settings are built twice, at separate times: Original (MIDI + sound packs, gaps filled with London Symphonic Strings) and Loops (the "loops only" box on Make).
- Tracker has "Original settings" and "Loops settings" columns. The dj-rebuild skill has a "Two sides" section. DECISIONS.md entry: "Rebuilds split into Original side and Loops side".
- Still open: where Loops-side settings live (a `loops` block in each config entry sharing `listen`, or a separate file).

## Where to start reading
- `tools/loop_mode.py` (`pick_loop`, `apply_dj_finish`), `tests/test_loop_mode_boundary.py` (loop picking must stay out of arrangement code).
- `LOOPS-MODE-GAP-ANALYSIS.md` (history; its Part 0 correction says the real feature is the checkbox, not a page).
- `tools/flavor_tags.py` SYNONYM_GROUPS (the sound-word families), `sample_library.loops_scored()`, `melodic_loops.in_key_scored()`.
- Loop folders: the BOTC Sorted Loops folders on `/Volumes/TBOTC 3`. Do not scan recursively; use Finder-style counts.
- House rules: ask clickable questions, no guessing, never render unless he asks.
