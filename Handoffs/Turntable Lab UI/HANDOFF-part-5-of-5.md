# Part 5 of 5 — Open questions, a suggested first step, kickoff

## Open questions for the owner (ask with clickable options; BLOCKING first)
1. **BLOCKING:** "Detailed Japanese animation like our style" — what is "our style"? (The Back of the Class logo? the Homeroom look? an anime he likes? something else?) Do not guess.
2. **BLOCKING:** What does he count as a "default" font or color? (Ask him to point at examples. He called the current black + orange/green/violet/blue page boring.)
3. Who makes the detailed art: Claude in code only, he makes pictures in ChatGPT or similar, a pre-made video/3D beaker, or a mix?
4. Which pages get this look: the main Beat Machine page only, or also Sketch and Effects (Physics)?
5. Where should uploaded DJ faces and album covers live, and should every DJ (all crew and Legends) get a sleeve? (There are 9 crew DJs and 12 Legends per the `beat-crew` skill; confirm the count in `crew_config.json` / `legends_config.json`.)
6. Which of the earlier options A-F, if any, did he like parts of?
7. Does he want the old school feel kept anywhere (notebook, chalkboard), or fully replaced?

## Suggested first step (a suggestion only; he decides)
Small enough to finish and check: ask questions 1-3 with clickable options, then make a few
PLAYABLE mockups in `Front End Mockups/` (served on his Mac, screenshotted, per the house process),
each showing: DJ sleeves, pull-out with face, album onto the turntable, science controls, and the
generating screen with the beaker. He picks a number. Only then build it into the real page (in Claude Code, ids kept).

## Do not do
- Do not choose fonts, colors, art style or layout for him without showing options.
- Do not touch beat sound, old beats, or git commits.
- Do not overwrite the existing page; back it up first.

## Kickoff prompt (paste into a new Claude session in this folder)
Read `Handoffs/Turntable Lab UI/HANDOFF.md` and all five parts. It is a brief for a new Beat Machine look
(laboratory + DJ turntables, anime style). No design decisions have been made. Start with Part 5, step
"Suggested first step": first tell me the cheapest model and effort and whether this is Cowork or Code,
then ask me the BLOCKING questions with clickable options before you make or choose anything.
