# Sample Browser mockup - notes

## What I did
- Read the live Sound of Science page CSS (sound_engine/static/effects.css, science.css, index.html) to copy the house look: dark page, Homeroom Studios header + app tabs, yellow ruled spiral notebook on the left with side tabs, wood-framed chalkboard with tray on the right.
- Built ONE self-contained file: `sample-browser-mockup.html` (no JS needed except a fake waveform). Screenshot: `sample-browser-mockup.png` (1600x1100, headless Chrome).
- Notebook (left): title, search box, filter chips, folder tree with counts, side tabs (Folders / Sounds / Favorites).
- Chalkboard (right): breadcrumb title, player (play button, name, details, waveform), actions (Favorite / Show in Finder / Use in a beat), list of samples with play dots, length, root note, star.
- Added a fourth "Samples" tab in the top nav so it reads as a new room.
- Touched nothing outside this outputs folder. No servers left running, no beats or audio rendered, no drive scan, no commit.

## Why
- Notebook = where you choose (folders, search). Board = what you hear and use. Same split as the beat generator.
- Chalk-style filters (the wobbly chalk SVG effect) from the real pages were left out to keep the mockup simple.

## Questions I would have asked (and what I assumed)
1. Which folders show in the tree? Assumed: the three BOTC Sorted folders (loops, MIDI, drums-style groups) only, per memory "sorted folders are the only source". Folder names and counts in the mockup are INVENTED.
2. Are the sample names real? Assumed no - placeholders ("Dusty Boom Kick 03"). Real names come from the library index.
3. What does "Use in a beat" do? Assumed: placeholder button, behaviour undecided. Needs your call.
4. Should it play audio in the page? Assumed yes (click a row to preview), like the batch player. Not built.
5. Folder-tree vs tabs: assumed tabs Folders / Sounds (by type) / Favorites. Say if you want different ones.
6. "Show in Finder" and "Favorite" assumed useful; drag-to-Reason not included.
7. Reason-sealed ReFill samples cannot be browsed (sealed archives) - assumed only loose files are shown.
8. Screenshot was taken from file:// so web fonts (Google Fonts) loaded online; offline it would fall back to system fonts.

## Not done
- No real page built, no server route, no Dock icon. Mockup only, as asked.
