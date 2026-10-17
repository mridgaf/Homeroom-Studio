# Chapter 10: Skills that carry production knowledge
## Part 3 of 6

_The saved skills (beat crew, drum loops, recipes, Reason reference, plus older style/gear skills) that hold production rules and producer styles._

**In this part:**
- SKILL.md (piece 2 of 2) — The Beat Crew
- SKILL.md — New Recipe

(Next: Part 4 of 6)


=====================================================
SOURCE FILE: SKILL.md (piece 2 of 2)
ORIGINAL LOCATION: HS:.claude/skills/beat-crew/SKILL.md
=====================================================

## The Drone Machine layer (spec landed 2026-07-16)

`~/Downloads/dj-drone-machine-spec.md` is the reference doc; all four of
its new features are BUILT (tools/beat_recipes.py + beat_machine.py):

- **Every beat ships as WAV + MIDI + stems.** Same basename `.mid` next
  to the wav, per-lane 24-bit stems in a "NN … Stems" subfolder (vinyl
  bed is its own stem; stems are un-glued — the WAV is the reference).
- **Recipes + swap flow.** Each render saves `<root>/.recipes/NN.json`.
  "Same beat, different snare" = `swap(NN, "snare")` — web page card or
  `--swap NN --lane snare`. Pattern/groove/other sounds locked, new
  numbered file, nothing overwritten. Only beats from 2026-07-16 on.
- **Anti-repetition persists across sessions.**
  `~/.reason_voice/sample_history.json` remembers the last 6 picks per
  DJ per lane and feeds the avoid set; stamps exempt. Hard rule.
- **Collabs are 50/50** (owner override 2026-07-16 — supersedes the
  spec doc's 80/20 AND the old host-carries-it recipe): the four jobs
  (kick, backbeat, timekeepers, color) are dealt 2-2 between the
  parents, each lane keeping its parent's pattern, groove, and drum
  taste; mix flavor averaged, kick_dist follows the kick's parent, both
  stamps ride. First-checked DJ still names the folder.

Tests for all of it live in `tests/test_beat_machine.py`.

NOTE (2026-07-18): the swap flow now files results into song-family
folders and the lane list is dynamic — see the two sections above.

## Loops only: FIVE LANES (owner spec 2026-09-16, confirmed by ear)

The "Loops only" box on the Make page. Code: `tools/loop_lanes.py` (pools,
tempo, stretch, picks) + `_pick_loop_bed` and the loops branches in
`generate` / `_beat_stems` / `_lane_candidates` / `swap_many` in
`beat_machine.py`. Full spec in DECISIONS.md "Loops-only beats: FIVE
LANES". Do not re-ask any of it:

- Lanes: `kick` = full drum loop (name kept, since the mix bus anchors to
  kick), `leadloop` (guitar, synth, orchestral, melodies, keys),
  `bassloop`, `fxloop`, and lane 5 = chords / perc / vocals / fx2 at 25% each.
- Tempo = the drum loop's BPM (from its name, else worked out from its
  length). Everything else is time-stretched to it, and pitch NEVER shifts.
  Always 8 bars.
- Key: 50% of beats match key LABELS on lead, bass and chords (unlabeled
  loops still allowed). The other 50% ignore key.
- FX: 1–2 hits, random bars, never side by side, each cut to 1 bar.
  Risers under 10% of FX picks.
- Swaps: a dropdown per lane grouped by folder, NO dice, no Roll
  everything. Play previews it and Rebuild prints a new numbered beat,
  the same as the stem rack.
- One DJ at a time. The first fill is random but leans on the DJ's taste.

## Project state

Folders + Beat Machine (2026-07-15): all beats reorganized into per-DJ
subfolders; `tools/beat_machine.py` is his self-serve jukebox. Double-
clicking "Beat Machine.command" opens it as a LOCAL WEB PAGE in his
browser (stdlib http.server on 127.0.0.1:8770, `run_web()`) — NOT a Tk
window: macOS ships the deprecated Tk 8.5.9 which fails to paint plain
tk widgets AND ttk widgets on his machine (verified 2026-07-15 via
screenshots), so the native-GUI path was abandoned. The page has a
checkbox per DJ (JS tracks click ORDER so the first-checked DJ hosts and
the beat lands in their folder — his original spec), tempo override,
how-many-beats 1-10, notes box logged to README; 1 checked = solo, 2+ =
collab. CLI test mode still works: `--render "Name,Name" --tempo N
--count N --notes "..." --out DIR`. It applies the standing rules itself (gated/dry by file-number
parity, ~10% no-sidechain, New Math boom bap on odd variants). Batch
scripts now skip files found ANYWHERE under the beats root (rglob) and
only touch README/journal when they actually rendered something.
Batch 5 delivered (2026-07-15): files 68-85 via `tools/make_two_each.py`
(school findings applied: frisson builds, B-section timbre shifts;
Roughness 808 and swung-club-kick debuts; engine gained grid_accent for
20/32 grids, tempo-scaled gate hold, and groove.roughness_am).
Batch 3 delivered (2026-07-15): files 41-67 via
`tools/make_three_each.py` (3 per member, gated/dry alternating,
New Math boom-bap 2-of-3, Crate's three = the no-sidechain renders).
Checkpoint 4 delivered (2026-07-15): files 21-40 rendered via
`tools/make_the_twenty.py` (2 per member, beat B = that character's one
evolution, + 2 collabs with both parents' stamps). Snap Church retired
that day (owner: too close to Night Metro/Rage Engine) — New Math holds
slot 9. The 13 "Proto" files and the Alt snare-space questions
(Otto/Cutz/Crate gated vs room; Glass Cat gated vs dry) still await his
verdicts. NEVER re-render or overwrite existing beat files unless he
explicitly asks (owner rule 2026-07-15) — batch scripts must skip
existing paths. Tests: `tests/test_crew.py` must stay green
(`./.venv/bin/python -m pytest tests/ -q` from the Homeroom Studio root).

## Honesty

You cannot hear the renders — verify numerically (duration, LUFS −8ish,
RMS sanity, per-bar levels) and say so plainly. His ears are QA: describe
what changed in plain words and let him judge. Regeneration is cheap —
offer variants instead of arguing.

=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:.claude/skills/new-recipe/SKILL.md
=====================================================

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

=== END OF PART ===
