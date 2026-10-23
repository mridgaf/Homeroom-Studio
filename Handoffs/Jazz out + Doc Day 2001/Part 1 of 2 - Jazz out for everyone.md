# Jazz out for everyone (Part 1 of 2)

Do this part first, then Part 2. Run the full test suite ONCE, after both parts, alone. DO NOT RENDER (owner rule: only when he asks).

## Why
- Owner, 2026-10-23: "get rid of the jazz chord settings across the board for everybody... I've been wondering what the problem is."
- Owner pick (clickable): "Jazz out, keep movement."
- Source of the jazz: the 2026-10-19 deep chord pass (DECISIONS.md). Its depth/lean numbers were Claude's ASSUMING, never heard. It took plain chords from about 65% to about 13%.

## What to change (new beats only; old beats must rebuild exactly as made, which is the house pattern)
1. **Coloring off.** `signature.chord_color` for all 45 identities in legends_config.json, genres_config.json and crew_config.json: no 9/11/13/6-9/add9/add11/#11/b9 upgrades. (`harmony.colorize`; keep key_context.EXT_CHORDS in the code, just stop new beats using it.)
2. **Keep the movement.** For each of the 24 `deep_*` progressions in progressions_config.json, add a plain twin (e.g. `plain_*`): same roots, same order, simple chords only.
   - Extensions step down: min9/min11 -> min7 or minor; 9/13 -> dom7; maj9/6/9/maj7#11 -> maj7 or major; 7b9 -> dom7; add9/add11 -> the triad.
   - Keep: triads, 7ths, sus, dim/m7b5/dim7.
   - Leave the `deep_*` entries defined so old beats rebuild. Repoint every identity from each `deep_*` to its twin at the same weight.
3. **Don't touch:** chord_family, pattern_tags, chord rhythm work, the MIDI pack share (separate question), bass figures. The owner asked about chord settings only.
4. Back up first (`*.pre-jazz-out-2026-10-23.json`), and log it in DECISIONS.md.

## Prove it (numbers, not adjectives)
- Same measure as Oct 19: 100 picks per identity. Report the share of plain triads/7ths before and after, and the number of distinct progressions before and after (movement should stay about the same).
- Then go to Part 2.
