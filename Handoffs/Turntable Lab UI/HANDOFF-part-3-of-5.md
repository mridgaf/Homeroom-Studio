# Part 3 of 5 — The existing code and house rules (read from his folder 2026-11-05)

## Where things are (his Mac, folder `Homeroom Studio`)
- Main page: `tools/beat_machine.py`, the `_PAGE` template. Built 2026-11-01 as the black "Homeroom Chemistry" UI.
- Sketch page: `tools/sketch_ui/sketch.js` + `sketch.css`.
- Effects page ("Physics"): `sound_engine/static/` (`index.html`, `physics.js`, `physics.css`).
- Brand files: `brand/` (logo-chalk, logo-black, logo-white, logo-blue, README).
- Write-up of the last UI job: `UI Handoff/WRITE-UP-2026-11-01.md`. Decision log entry: `DECISIONS.md` "[2026-11-01] Homeroom Chemistry UI".
- Old page (backup): `sound_engine/static/index.pre-physics-2026-11-01.html`.
- Old mockup process: `.claude/skills/notebook-chalkboard-page/SKILL.md` (marked STALE for its look; the mockup process still applies).

## The current page has (kept from the last UI job)
Class tabs (Back of the Class / Legends), round portrait placeholders, pick order numbers,
Key, Number of beats (1-10), Style, Directions, tempo flask tied to the real tempo range (60-200),
Loops-only switch (changes colors and words), toolbar pop-ups (Pattern Library, Breaks, Saved Beats,
Famous Beats, Reference), beat cards with waveform, Pass/Fail, Sketch, Stems, Open Physics,
Elements tiles from `/stems`, bottom now-playing bar.

## Rules for any UI job here
- Look and layout only. KEEP every element id and server call the existing JS uses.
- Back up first, beside the file: `<name>.pre-<theme>-<date>.<ext>`.
- Mockups first, never the real page. Mockups go in `Front End Mockups/`; make them playable.
- The owner approves a numbered mockup, then it is built. Log it in `DECISIONS.md`.
- Serve mockups over http (a local file preview does not load css/js).
- Check at 1512x982 (his MacBook) and phone width; no sideways scroll.
- Never run `git commit` or `git push` unless he says so. A dirty `git status` is normal (see `expected-churn` skill).
- Tests before beats: run the full suite ONCE per session before any render, never at the same time as a render. Known minor failures can be ignored.
- The Dock icons must open the newest version.
- Read `DECISIONS.md` (not the archive) at the start. Log real decisions at the end.
- The 1% rule: if a project skill in `.claude/skills/` might apply, load it first.
- His Mac is not Linux. Anything that needs his `.venv`, the external drive `/Volumes/TBOTC 3`, or beat renders goes in Claude Code on the Mac, not the Cowork sandbox.
- Web research tool: Firecrawl (not TinyFish). If a page is blocked, stop, flag it, give him the direct link.
