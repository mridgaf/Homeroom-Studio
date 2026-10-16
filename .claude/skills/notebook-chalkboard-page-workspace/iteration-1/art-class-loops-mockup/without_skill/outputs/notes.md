# Loops "art class" mockup - notes

## What I did
- Looked at the live beat page (Front End Mockups/live-page-2026-10-03.jpg) and the CSS in tools/beat_machine.py (Homeroom Studios layer) for the "school style": charcoal page, ruled spiral notebook left, wood-framed board right, hand-lettered headings, big tab buttons top right.
- Kept that same skeleton (same header, 2:3 split, spiral rings, wood frame, same tab row) so it still reads as the same school. Swapped the subject to art class:
  - Notebook -> white drawing-paper sketchbook, pencil type, blue marker title.
  - Chalkboard -> cork gallery wall in the same wood frame; loops are paper cards pinned with masking tape.
  - Loop kinds (melodic / drum / bass / chopped) are paint-pot swatches; each kind keeps one paint colour on its card.
  - Waveform = coloured paint block with white bars; "Paint my loops" is the Make button.
  - Tabs: Make | Loops (active) | Studio.
- Content comes from the Loops docs (HANDOFF-TO-CODE-LOOPS.md): DJ/Legends/Styles pickers, key/mode, bars, directions, reference track, and a "picked by taste" vs "free pick" tag (the 50/50 roll).
- Files: loops-art-class-mockup.html (self-contained, no server needed), loops-art-class-mockup.png (1500x1000 headless Chrome). No server started. Nothing outside this folder touched. No audio/beats rendered.

## Questions I would have asked (and what I assumed)
1. Is "Loops" its own tab, or a section inside Make (today it is a "Loops only" checkbox)? ASSUMED: its own tab, as the task says "the Loops part".
2. Keep the beat page's chalk/lime colours, or new colours? ASSUMED: new paint colours (red/blue/yellow/green) on the same charcoal page; wood frame kept.
3. Which loop kinds belong on the page? ASSUMED: melodic, drum, bass, chopped (from the gap-analysis doc; "chopped vs whole" is listed there as still open).
4. Bars choices 1/2/4/8? ASSUMED, sample values only.
5. Fonts: live page uses Special Elite / Patrick Hand / Blackboard Graffiti, which may need loading. ASSUMED: system fallbacks (Marker Felt, American Typewriter) for the mockup; fine for a picture, swap in real fonts when built.
6. All names, numbers and loops are sample data.

## Not done / limits
- Static picture only: buttons do nothing. Not responsive below ~1100px.
- Did not read the notebook-chalkboard-page skill (as instructed).
