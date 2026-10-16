# Art Class: Loops mockup (test run, owner unavailable)

Files: loops-art-class.html (open via http server; needs house-style.css + logo-chalk.png beside it), loops-art-class.png (1512x1250), loops-art-class-phone.png (headless Chrome cannot go narrower than ~500px, so the right edge is cropped there; not a real overflow, but not truly verified at 390).

## What I did
- Read the skill, copied assets/house-style.css and both chalk filters unchanged. Same two-column notebook | chalkboard, wood frame + tray, tabs sticking out of the notebook, logo on the board, doodles, same top nav (added a "Loops" tab).
- Theme = art class. Notebook = "Sketchbook No. 8" (Sketch / Palette / Gallery tabs: setup, key+tempo, past loops). Board = "Art Class: Loops", with "The canvas": 5 lanes (drum, lead, bass, chords, FX, from tools/loop_lanes.py) as 8 bar-stripes in paint colours; click a stripe to "repaint" (swap that lane's loop), mute/solo, a moving playhead. Buttons: Paint it! (= make), Frame it (= save), Repaint all, Wipe the board (= trash). Plain meanings in the footnote, per the skill.
- Doodles on the board: brush, palette, triangle. Blue-ink colour key on the notebook.
- Interactive: tabs flip, play moves the playhead, stripe click swaps the loop name, mute/solo toggle.
- Not touched: any real file, any server, no audio rendered, no commit.

## Questions I would have asked (assumed answers)
1. Is "Loops" its own page/tab, or the "Loops only" checkbox view inside Make? ASSUMED: its own page tab in the nav, holding the same settings as the Make page's Loops-only mode.
2. Which lanes? ASSUMED the 5 in loop_lanes (drum, lead, bass, chords, FX); percussion/vocal lanes exist in code but are not shown.
3. Do I keep the notebook yellow ruled? ASSUMED yes (house look); art feel comes from the dab colours, ink doodles and board, not new paper.
4. Is the one-click "repaint a lane" button real today? ASSUMED it matches the existing per-lane swap (beat_machine.py ~line 4276); mockup only.
5. Gallery data (2830 Dusty Sunday etc.) is invented placeholder text.
6. Offer 3 directions? Task said "a mockup", so one. ASSUMED OK.
