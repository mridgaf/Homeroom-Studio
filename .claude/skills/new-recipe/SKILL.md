---
name: new-recipe
description: Author a sound recipe for the Reason Voice recipe book — a step-by-step .md file that teaches how to build a specific sound in Reason 12, voice-walkthrough ready. Use whenever the user asks for a recipe ("recipes for JID's albums", "recipe for a Phil Collins snare", "how do I get that Burial sound — add it to the book"), asks to capture a sound/artist/album/genre as something the app can walk him through, or wants a recipe edited/extended. Even a vague "make me something that sounds like X" in a music context should use this.
---

# New Recipe

Write recipe `.md` files for the recipe book at
`/Users/johnsuhr/Desktop/Homeroom Studio/recipes/<book>/` (book =
`hiphop` or `rock`; create a new book folder only if asked). The app parses
these files — format errors break the voice walkthrough, so match the
anatomy exactly. Read one existing recipe first (e.g.
`recipes/hiphop/jid-dicaprio2-151-rum.md`) as a live template.

## File anatomy (all parts required)

YAML frontmatter:
```yaml
---
name: Short Evocative Name          # what he'll say to open it
book: hip-hop                       # or rock
sounds_like: Artist "Song" / era    # drives "sounds like X" search
accuracy: C                         # honesty rating, see below
status: theoretical                 # ALWAYS theoretical for new recipes
source: what the recipe is based on # interview? ear analysis? say which
tags: lowercase words for search    # artist, genre, devices, techniques
technique: one transferable lesson  # spoken at walkthrough end
---
```

Body sections, in this order, all `## ` headings:
`The Chain` (device signal path, use `→`), `Steps` (numbered — each number
is one spoken walkthrough step), `Why this works`, `Order of operations`,
`Reason-specific trick`, `RE upgrade path`, `Technique you just learned`,
`Reference` (use a YouTube search URL, never an invented link).

## The honesty system (this is the book's soul)

- **A** = documented from the actual session/producer. **B** = technique
  publicly documented, adapted to Reason. **C** = built by ear, educated
  inference. **D** = speculative.
- New recipes are `status: theoretical` — the app flips them to `tested`
  when he says "it worked". Never pre-claim tested.
- State the rating's reason in the body's opening line ("built by ear from
  the album, not from stems").
- Never promise automation Reason doesn't have: no API builds chains,
  routes cables, or sets knobs. The recipe teaches HIM to build it.

## House rules

- **ELI5 voice.** Self-taught musician, not an engineer. Every jargon term
  gets a plain-words translation in the same sentence. Numbers over
  adjectives: "Damage 25–40", not "some distortion".
- **His gear is part of the recipe.** Launchkey MK3 49: bass/melody played
  on the keys (hold-first-note-press-next = 808 glide), drums fingered on
  the pads (Shift + Pad Mode → Drum). Yamaha DTX400K: real sticks for
  grooves that need human looseness. Guitar parts: mic the Crate/Epiphone
  into the AudioBox, or DI + Scream 4. Say which and how.
- **Stock devices first** (SubTractor, Malström, Kong, Redrum, Scream 4,
  RV7000, MClass, The Echo, ReGroove, Klang, Combinator). Rack Extensions
  only in `RE upgrade path`.
- Steps: 5–9 of them. One action each — they're read aloud one at a time.
  A continuation line indented under a number folds into that step.
- End `Reason-specific trick` with a Combinator-saving suggestion when the
  chain is reusable ("save as X.cmb") — that feeds his template library.

## After writing

Run the parser check — it catches broken frontmatter and missing steps:
```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python -c "
from reason_voice.recipes import parse_recipe
from pathlib import Path
r = parse_recipe(Path('recipes/<book>/<file>.md'))
print(r.name, '| steps:', len(r.steps), '| accuracy:', r.accuracy)"
```
Steps must be ≥5. Then tell him the recipe appears after a restart of
Reason Voice, or say "recipe for <name>" if it's already running (library
loads at startup — restart needed). Never edit recipes he wrote or that
are marked `tested` unless he asks.
