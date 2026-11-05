---
name: notebook-chalkboard-page
description: The Homeroom Studios house page look (yellow ruled spiral notebook on the left, wood-framed chalkboard on the right) and the mockup → owner pick → build process that produced the Beat Machine, Reason Voice and Sound of Science (Effects) pages. Use whenever the owner asks to redesign, re-skin, theme, restyle or "make it look like the beat generator" for any page or app in this project, asks for mockups of a page, wants a new page/room added to the app family, or asks to change the notebook, chalkboard, tabs, knobs or theme of an existing page — even if he only says "make it match" or "school style".
---

# Notebook + chalkboard pages

Three pages already share this look and the owner judges every new page against them. The live Beat Machine (`tools/beat_machine.py`, the CSS block after "homeroom layer") is the reference. When in doubt, match it, not a mockup.

## The look (copy it, don't reinvent it)

`assets/house-style.css` has the tokens and the pieces: palette, notebook paper, rings, flip-out tabs, wood frame with chalk tray, chalk buttons and lanes. `assets/chalk-filters.svg.html` has the two SVG filters (`#chalk`, `#chalk-text`) that give every outline and letter its rough chalk edge. Paste both into the new page, then add only what is new.

What he has approved, and why each piece matters:
- **Two near-equal columns**: `1fr | 1.1fr`. He asked for balance. A skinny notebook beside a huge board read as lopsided.
- **Notebook (left)**: yellow ruled paper, red margin line, spiral rings, typewriter font (Special Elite), ink-black text. It holds settings and pages.
- **Chalkboard (right)**: #141414 board, full 16–18px wood frame on all four sides plus a chalk tray at the bottom. He circled a missing frame side once. Text is Patrick Hand in chalk white, accents lime #9be22d and sun-yellow #f6e04b.
- **Band logo**: The Back of the Class mark (`/brand/logo-chalk.png`) sits on the board somewhere. He asks for it every time.
- **Tabs that stick out of the notebook's right edge** for extra pages (Stems / Flask A / Flask B). Clicking one flips the notebook page instead of opening a new screen, which keeps things uncluttered.
- **Theme words over function words**: the Science page says "Lab lock", "Control ⇄ Experiment", "Reset experiment", "Flask". Keep the plain meaning in a tooltip or subtitle so nothing gets confusing.
- **Fill empty paper with doodles** (formulas, scrawl in blue ink, themed sketches) rather than leaving blank space. He liked that. Check the bottom half of the notebook in particular: forms are short, so the lower half of the pad is usually empty unless you fill it on purpose.

## The process (it is the part that saves rework)

1. **Ask before drawing** when a choice changes the build: what replaces what, what each side holds, what is kept. Use clickable options, recommendation first (house rule 0b: never guess).
2. **Mockups first, never the real page.** Write them to `Front End Mockups/` as self-contained HTML. Use a shared `*-base.css/js` when making several variants. Make them interactive (drag knobs, flip tabs) so he can play. Offer about 3 distinct directions when he asks for options.
3. **Show them where he is.** He often follows over Remote Control, where the Browser pane is invisible. Serve the folder with the `mockups` entry in `.claude/launch.json` (port 8799). Take full-size pictures with headless Chrome:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,960 --virtual-time-budget=4000 --screenshot="<abs path>.png" "http://localhost:8799/<file>.html"`
   Read each PNG yourself before sending it with SendUserFile, and re-shoot and re-read after every fix: the last picture is the one he judges, and overlapping text is the usual thing a quick look misses. Add a `#hash` deep link to shoot an opened state. Annotated screenshots come back with green circles; every circled thing is a change request.
4. **He approves a numbered mockup.** Copy the approved picture into `Front End Mockups/` with "approved" in the name if he hands you one.
5. **Build the real page**:
   - Back up first: `index.pre-<theme>-<date>.html` and the JS beside it (house backup convention).
   - **Keep every element id the existing JS uses.** Old controls nobody sees go into a collapsed "Fine tune" drawer, not the bin. That is how the Effects page kept every slider working.
   - Put layout in a new `<theme>.css` + `<theme>.js`. Let the layout JS call the existing functions (and wrap them if it must, e.g. `renderChannelList`) so sound and server paths stay the tested ones.
   - Check at his MacBook width (1512×982) and at phone width (no sideways scroll). Look for text running out of the frame. The board is half the old width, so strips and players need `flex-wrap`.
6. **Verify, then log**: the page's own tests and the browser console must show no errors. Add a DECISIONS.md entry naming the mockup number. Update the page's memory file.

## Traps already hit

- The preview pane shows local .html as a static snapshot, so relative CSS/JS/images don't load. Serve over http.
- `preview_start` can't run the project venv (macOS blocks `.venv/pyvenv.cfg`). Start real servers from Bash in the background. The Sound Engine's no-browser switch is `SOUND_ENGINE_NO_BROWSER=1`.
- A CSS `display:grid/flex` rule beats the `hidden` attribute. Keep `[hidden]{display:none!important}`.
- Headless Chrome can't load a beat into the live Sound Engine (the audio decode never finishes). Shoot the empty page, and use the pane's zoom for loaded views.
- Stem labels look like `"kick drum - goodgas_roomkick"`. Show the part before `" - "` and put the full name in a tooltip.
