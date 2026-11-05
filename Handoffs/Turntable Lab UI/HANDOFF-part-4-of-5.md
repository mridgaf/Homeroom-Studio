# Part 4 of 5 — Verified vs UNVERIFIED

## VERIFIED (actually read or run on 2026-11-05)
- The current main page is the Nov 1 black "Chemistry" UI, not the notebook/chalkboard (read `DECISIONS.md`, `UI Handoff/WRITE-UP-2026-11-01.md`, and viewed the approved mockup image).
- Design canvas: six playable options were published as a private canvas (A Chalk Class, B Notebook + Board, C Paper on the Wall, D Report Card, E Yearbook, F Locker Hall). Link: https://claude.ai/artifact/EDabdTrV1q3okz43sEYLnN . The owner was NOT shown to approve any of them. They were never opened or rendered by Claude (the canvas type says do not verify unless asked), so layout or script mistakes are possible.
- Copies of those six files are in `Reference - earlier options`. They are references only. They use fake data and invented names for new beats. The logo in them is `brand/logo-chalk.png`.
- A built-in "frontend-design" skill exists in Claude (it asks for deliberate, non-default type and color). It was loaded and applied to options E and F only.
- GitHub star counts for official web/graphics repos were pulled live today by search (bootstrap ~175k, three.js ~117.6k, d3 ~113.9k, material-ui ~99.3k, tailwindcss ~98.1k). shadcn-ui/ui did not appear in results, so its count is unknown.
- Community design-style repos exist (found in search, titles only, NOT opened): VoltAgent/awesome-claude-design, VoltAgent/awesome-design-md, bergside/awesome-design-skills, wilwaldon/Claude-Code-Frontend-Design-Toolkit, zhuyansen/awesome-claude-design-skills, rohitg00/awesome-claude-design, Leonxlnx/taste-skill.
- Tools named by articles (read via fetch, but repo links not confirmed): Impeccable, UI UX Pro Max, Skill UI, Playwright CLI, Superdesign.
- Sites an agency article praised for design (opened by nobody here): Awwwards, Gufram, B-Egg Farm, Spotify Design, Noomo Agency.

## UNVERIFIED — test before building on these
1. "A code-drawn bubbling beaker with smoke looks good enough." It was an estimate, never built. Falsify: build it and show the owner.
2. "CSS 3D / canvas can do the sleeve pull-out, the album flying to the turntable, the spinning record and tonearm." Likely, never built. Falsify: prototype it.
3. "three.js or WebGL is usable in the Beat Machine page." Not checked. Falsify: check whether the page can load the library locally (the page is served by Python; no internet may be assumed) and test speed on his M2 Pro.
4. "Face uploads need a small backend piece." Not checked. Falsify: read how `tools/beat_machine.py` serves files and where it could save images (it already serves `/brand`).
5. "The Design canvas can make heavy 3D/WebGL scenes." Not checked. The canvas pages run plain HTML/CSS/JS; the limits are unknown.
6. "The earlier Chemistry mockup was made by an image tool." Inferred from a README addressed to ChatGPT and the look of the picture. Not confirmed with the owner.
7. "Claude cannot make pictures." True of the tools that session had (no image generator was available). May differ in a new session; check the tool list.
8. The community repos and tools above may or may not improve results. No claim was tested.
9. Anime look: a code-only version may not reach "detailed anime" without art assets. Not tested.
