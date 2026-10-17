---
name: new-recipe
description: Research how a song, artist or sound was made, then write a "get close" recipe for it in stock Reason 12, voice-walkthrough ready, rated honestly, and run the build-and-test loop with the owner. Use whenever he asks for a recipe ("recipe for JID's album", "how do I get that Burial sound", "make me something that sounds like X", "find out how they made this"), wants a sound/artist/song/genre captured for the app, wants a recipe edited, extended, or tested.
---

# New Recipe

Write recipe `.md` files for the recipe book at
`/Users/johnsuhr/Desktop/Homeroom Studio/recipes/<book>/` (book =
`hiphop` or `rock`; create a new book folder only if asked). The app parses
these files — format errors break the voice walkthrough, so match the
anatomy exactly. Read one existing recipe first (e.g.
`recipes/hiphop/jid-dicaprio2-151-rum.md`) as a live template.

## Goal: get CLOSE and LEARN, not clone

The point of a recipe is the technique it teaches and a sound in the right
neighborhood. Never promise an exact match. Say what it gets (the feel) and
what it can't (the missing 20%).

## Workflow — do these in order, no shortcuts

1. **Check what exists first.** Search the book before writing anything:
   `python3 -c` with `RecipeLibrary('recipes','device_refs').search("<song or artist>")`
   (see "Running things" below). If a close recipe exists, extend or link to
   it instead of writing a duplicate. (2026-10-11: eight old recipes nearly
   duplicated ones already in the book.)
2. **Research how it was made.** Use TinyFish `search` then `fetch_content`
   (free, fast), falling back to WebSearch/WebFetch. Look for: producer or
   engineer interviews, Sound on Sound "Inside Track", gear lists, sample
   sources, tutorials for the exact track. Cap at about 6 sources. Write down
   for each claim whether it is **documented** (a named source says it) or
   **inferred** (you listened/reasoned). Never invent a quote, a setting or a
   link. Rule from evidence-tiering: documented fact, inference and guess stay
   labelled apart.
3. **Break the sound into parts** (3–5): drums, bass, lead/hook, vocal,
   space/FX. One recipe per part, or one combined recipe if they only make
   sense together.
4. **Map each part to stock Reason devices he owns.** Stock first. For every
   device and parameter you name, verify the spelling before you write it:
   `python3 tools/reason_vocab.py --device "<Device>"` for exact names, and grep
   the manual in `~/.reason_voice/reason12_manual/` for what a control does
   (match punctuation loosely, cite the page). If you cannot verify a name, write
   "(check this name in Reason)" in the step. Never type a parameter name from
   memory — a name that is slightly wrong fails silently. Never name a device
   as stock unless it is in the vocab file or the manual.
5. **Rate it honestly** with the A–D scale below, with the reason in the
   opening line. For a song recipe built from research and listening, C is the
   normal honest answer; A needs a documented session.
6. **Write the file** to the anatomy below.
7. **Check it** (parser + recipe tests), log it in `DECISIONS.md`, tell him
   it appears after a restart of Reason Voice.
8. **Test loop.** He builds it (or you guide the build), then says what
   happened: "worked", "too muddy", "can't find the knob". Edit the recipe
   from that. Flip `status: theoretical` to `tested` ONLY when he says it
   worked. A failed step gets fixed in the file, not explained away.

## Claude builds it in Reason (owner-confirmed: this works)

Claude can build any recipe in Reason itself, by taking control of the screen
(computer use): create devices, hover and click controls, set knobs, flip the
rack around and wire cables. The Panel Map gives the exact control and jack
names and positions, so this is a proven route, not an experiment.

- **How:** read the `computer-use` skill first, then the `panel-map` skill to
  find each control/jack (it also checks cables). `reason-mixer-chains`,
  `reason-drum-bus` and `reason-vocal-chain` give click-by-click routing.
- **Offer it every time.** After writing a recipe, ask (clickable options):
  "Want me to build this in Reason now?" If yes, build it step by step in the
  order of the recipe's Steps.
- **Check as you go.** Screenshot after each step. Confirm the cable/knob
  landed (panel map names) before the next step. If a step fights back, stop,
  say which step and what you saw, and fix the recipe or ask. Never report
  "built" for a step you didn't see land.
- **Build lessons (proven 2026-10-11, Tony Tone drums):**
  - Reason's menus work with `computer_app_menu` (Create > Effects > ...), but
    only while Reason is frontmost. Release app locks (`computer_app_release`)
    before display clicks. The Rack detaches to its own window, which may sit on
    the second monitor (`computer_switch_display`).
  - Select a Mix Channel first, then Create: the device lands in that channel's
    insert chain. Creating another while one is selected chains after it.
  - Setting a knob: drag fully down (to minimum), then drag UP a measured number
    of pixels; hover for the tooltip value. Full travel is about 67 px. Measured
    rates: EQ gain ~0.5 dB/px, Scream 4 values ~1.9/px, EQ frequency is
    logarithmic (~0.015 of its range per px). Compressor Attack/Release are
    uneven, so nudge and re-read the tooltip.
  - Band/section on-off LEDs are separate clicks (MClass EQ bands start off).
  - Kong: Drum Output selector under "Show drum and fx", then right-click the
    jack > "Route to New Mix Channel". Double-click a channel name to rename.
    Select channels (shift-click), Cmd+G makes the Output Bus.
  - Scream 4 loads with the EasyFuzz patch, not a neutral one: set the type,
    turn Body off, and set all values explicitly.
  - Panel Map has no mixer "Drive" control; do not promise one.
- **MIDI parts** (drums/bass/lead notes): write a .mid file and import it
  (File > Import MIDI File), or place the notes on screen.
- **Remote bridge** (`reason-remote-bridge`) can also move mapped controls.
- **After the build:** he listens. Only his "it worked" flips `theoretical` to
  `tested`. Claude building it does NOT count as tested.

## Running things (where the code actually runs)

`device_bash` may run in a Linux VM, not on his Mac, so `./.venv/bin/python`
may not exist there. If it doesn't: `pip install --break-system-packages
rapidfuzz pyyaml pytest`, then use `python3`, and run ONLY
`tests/test_recipes.py` (fast). Never start the full ~17-minute suite or a
beat render from here. Say in the report which Python ran the check.

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
- Reason has no scripting API, but Claude builds chains by driving the screen
  (see "Claude builds it in Reason"). The recipe still teaches HIM how, so
  he learns the technique.

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
Steps must be ≥5 (and ≤9). Also run `python3 -m pytest tests/test_recipes.py -q` (library must still parse). Append a short entry to `DECISIONS.md`. Then tell him the recipe appears after a restart of
Reason Voice, or say "recipe for <name>" if it's already running (library
loads at startup — restart needed). Never edit recipes he wrote or that
are marked `tested` unless he asks.
