# Packaging Gap Analysis — one app, two doors

*What already exists for joining the beat generator and Reason Voice into one
product, what's actually missing, and a concrete punch list. Grounded in the
code as of 2026-07-25.*

**The one-line finding:** these are not two projects to merge — they are one
project with two front doors and no handoff between them. The merge work is a
launcher, a port, and about a dozen extra keys in a JSON file that already gets
written on every render. Everything else is already shared.

**The product goal (Wedge 2):** a beat that can walk you into your rack. The
generator makes a full in-key idea; Reason Voice already knows how to load
patches, run recipe walkthroughs, and open a session. Today the beat forgets
everything about itself the moment it lands on disk. Connect those and you have
the only tool in this category that goes *idea → execution coach* instead of
stopping at a WAV file.

---

## Part 1 — What already exists (more than expected)

| Capability | Where it lives | Reuse for the merge |
|---|---|---|
| Beat engine + web UI | `tools/beat_machine.py` (`run_web`, port 8770, stdlib `http.server`) | **Keep.** Already a browser UI with batch cards, stem racks, lane swapping. |
| Reason Voice + web UI | `reason_voice/server.py` (FastAPI + uvicorn + WebSocket, port 8765 via `config.yaml: web_port`) | **Keep.** Verified working end-to-end 2026-07-25. |
| **Per-beat manifest, already written** | `tools/beat_recipes.py` `save_recipe()` → `<beats root>/.recipes/NN.json` | **This is the seam.** It already stores `bpm`, `root_note`, `preset`, `kit_paths`, `stamp_paths`, `title`, `folder`, `date`. |
| MIDI export per beat | `write_midi(path.with_suffix(".mid"), ..., chords=midi_chords)` | Keep — the chords track is already channel 1, separate from drums. |
| Harmony brain | `tools/key_context.py`, `tools/harmony.py`, `progressions_config.json` | Keep — computes key, mode, romans, exact chord notes. |
| Reason session templates | `reason_voice/templates.py` (`TemplateLibrary.new_session`, `shutil.copy2` + `%Y-%m-%d %H.%M` stamp); the sessions folder default lives in `server.py` (`sessions_dir`, `~/Music/Reason 12/Sessions`) | **Keep — this is the landing pad.** Already makes a date-stamped copy, never overwriting the template. |
| Recipe library + cards | `recipes/**/*.md`, `reason_voice/recipes.py`, `/api/recipes` | Keep — the "how do I build this sound" half. |
| Voice intent grammar | `reason_voice/intents.py` (ordered regex) | Keep — where a "make me a beat" intent would go. |
| Shared foundation | one folder, one `.venv`, Python 3.9, `pytest` (487 green), `theory/`, `device_refs/`, `sample_library.py`, `brand/` | Nothing to do. This is why it's one product already. |

---

## Part 2 — The gaps (precise, code-grounded)

### Gap 1 — The manifest doesn't record the harmony

`_build_chords()` in `beat_machine.py` (around line 995) builds a `KeyContext`,
picks a progression, and produces chords with `roman` and `chord` labels for
every bar. **None of that reaches `save_recipe()`.** The two `save_recipe()`
calls (lines ~1473 and ~1604) persist `root_note` but no mode, no progression
name, no roman numerals, no chord spellings, no lane list.

Consequence: a beat on disk knows its tempo and its 808 root but not its key or
its chords. Reason Voice therefore cannot set up a session that matches it, and
nothing can print "here's why this progression feels epic."

The fix is additive keys on an existing dict — the lowest-risk change in this
document. Existing `.recipes/*.json` files stay valid; readers must tolerate the
new keys being absent on old beats (`load_recipe` already raises a friendly
error for missing files, so the missing-key path needs the same manners).

### Gap 2 — Two launchers, two ports, two UIs

`Homeroom Studio.command` runs `tools/beat_machine.py` (port 8770).
`ReasonVoice.command` runs the Reason Voice server (port 8765). They are
separate processes serving separate pages with separate HTML, and one is
FastAPI while the other is stdlib `http.server`.

This is the actual source of the owner's "clunky / jumbled" complaint restated
one level up: he has to know which app does which job before he can start. It's
the same failure mode as the old terminal REPL — the tool asks him to hold a
mental model of its internals.

**Do NOT unify the servers.** Rewriting `beat_machine.run_web` into FastAPI (or
Reason Voice into stdlib) is a large refactor of 3,500 lines of working code for
zero user-visible gain. The two processes can stay two processes. What's missing
is one launcher that starts both and opens one page that links them.

### Gap 3 — No "open this beat in Reason" action

Even with a complete manifest, nothing acts on it. There is no code path that
reads `.recipes/NN.json` and turns it into a Reason session at that tempo with
that MIDI imported. `TemplateLibrary` does the closest thing (copy a template,
date-stamp it, open it) but knows nothing about beats.

Honest constraint that shapes this: **Reason has no device-creation or
song-authoring API** (documented in `CLAUDE.md` and the README). The only levers
are `open -a Reason <file>`, MIDI via the Remote bridge, and copying a
pre-existing template song. So "open this beat in Reason" can realistically
mean: copy a template song → open it → send the tempo over Remote → reveal the
beat's `.mid` in Finder for a manual drag. That last step is a manual drag, not
automation, and the UI must say so plainly rather than implying more.

---

## Part 3 — The seam (why this is closer than it looks)

`.recipes/NN.json` already exists, is already written on every render, is
already read back by the lane-swapping UI, and already has a
friendly-error-on-missing reader. It was built to let a beat be *re-rendered*.
It turns out to be exactly the right shape to let a beat be *explained* and
*handed to a DAW*.

So the merge does not need a new data format, a database, or an IPC channel
between the two servers. It needs more keys in a file that's already on disk,
and two readers of it. You are extending an existing concept, not inventing one
— the same situation as `ROOT_HZ` in the harmony build.

---

## Part 4 — Punch list

Ordered smallest-risk first. Each is a discrete, testable unit. Stop and show
the owner after each one.

0. **Guard the boundary.** Add a test asserting no module in `tools/` imports
   from `reason_voice/` (see Part 4a). Five lines, currently passing, protects
   the option of a non-Reason audience forever. Do it first so every later step
   is checked against it.

1. **Enrich the manifest.** Add to both `save_recipe()` call sites:
   `key` (root + mode), `progression` (name), `chords` (list of
   `{bar, roman, chord, notes}`), `lanes` (which lanes rendered),
   `chord_source` (strings / horns / loop / synth), `legend` codename only.
   **Never write `preset["built"]` or any real producer name into this file** —
   it's a sidecar that could ship with a beat (see Part 6). Test: render one
   beat, assert every new key is present and the romans match
   `harmony.compose()` for the same seed.

2. **Backfill reader tolerance.** Make every consumer of `load_recipe()` handle
   the new keys being absent (beats before this change). Test: load an old
   `.recipes/*.json` fixture and assert no `KeyError`.

3. **"Why this works" on the beat card.** In `beat_machine._dj_card` / the batch
   card, print the key, the progression, the romans, and one line of plain
   English pulled from `theory/progressions.md` for that progression. Pure
   read-and-display of step 1's data. This is the teaching feature and the
   cheapest visible win in the whole document.

4. **One launcher.** A single `Homeroom Studio.command` that starts both servers
   (Reason Voice on 8765, beat machine on 8770), waits for both to answer, and
   opens ONE page. Keep `ReasonVoice.command` working for the case where only
   the studio half is wanted. Test: launch, curl both ports, expect 200.

5. **Two tabs, one page.** Add a top-level MAKE / STUDIO switch. Simplest
   honest implementation: each page gets a link to the other, styled as a tab,
   using `brand/logo-blue.png` in the masthead on both so it reads as one app.
   Resist making one page iframe the other until the plain-links version has
   been lived with.

6. **Recipe refs on the beat card.** Given a beat's `chord_source` and legend,
   look up matching `recipes/**/*.md` and link them into the STUDIO tab. The
   recipe search already exists (`/api/recipes`); this is a query, not new
   search code.

7. **Export, two buttons side by side.**
   - **"Export stems + MIDI"** (generic, build this FIRST): copies the beat's
     WAV stems and `.mid` into a chosen folder with a plain README naming the
     key, bpm, and progression. Works for any DAW. Cheap — the files already
     exist, this is a copy plus a text file.
   - **"Set up in Reason"** (integration): reads `.recipes/NN.json`, copies a
     template song via `TemplateLibrary.new_session`, opens it, sends tempo over
     the Remote bridge, reveals the `.mid` in Finder. **The UI must state that
     importing the MIDI is a manual drag** — no API exists for it. Test: assert
     the copied session file appears and the original template is untouched.

   Build the generic one first even though the Reason one is the one that gets
   used daily. It's the smaller job, it can't fail on unverified Remote
   behaviour, and it's the thing that proves the boundary in Part 4a holds.

8. **Voice intent for generating.** Add a `make a <mood> <genre> beat at <bpm>`
   pattern to `intents.py` that calls the beat engine. Pattern order matters —
   it must not outrank the recipe-search or reindex patterns. Test: add cases to
   `tests/test_intents.py` asserting the new pattern doesn't steal existing
   phrases.

**MVP cut:** steps 0–5. That alone gives one app, one door, and a beat that
explains itself. Steps 6–8 are the Reason integration and can wait for the
owner's verdict on 0–5.

**Constraints (keep true):** Python 3.9 (`from __future__ import annotations`
for `X | Y`); quote the `Homeroom Studio` path (space); bash not zsh;
macOS `sed -i ''`; keep `pytest` green (487 baseline — run it first as a
baseline before touching anything).

**Do NOT touch:**
- `remote/` — the Reason bridge. Tabs in `.remotemap` are load-bearing and the
  codec was painful to get right. Nothing in this punch list requires changing
  it.
- The two web servers' frameworks. No FastAPI-ification of `beat_machine`, no
  stdlib-ification of `reason_voice`. Gap 2 explains why.
- `beats_root.json` resolution logic in `_resolve_beats_root()`. It exists
  because the library moves between drives and a hardcoded path once caused a
  silent restart of beat numbering.
- Anything that deletes or renames files in the beat library. Cleanup moves into
  a dated folder with a manifest and a typed `yes` (see the `safe-file-ops`
  skill).

---

## Part 4a — The portability boundary (owner decision, 2026-07-25)

**Decided:** Reason stays the daily driver for the foreseeable future, but the
option of a broader audience must stay open. So the shape is **demote, not
remove** — nothing Reason gets deleted, it just stops being load-bearing for the
generator.

**The one rule that buys the option, at zero cost:**

> `tools/` must never import from `reason_voice/`.

This is already true — `beat_machine.py` imports nothing Reason-related; the
only trace is the state path `~/.reason_voice/beat_machine_state.json` and one
comment. Adding a test that asserts it stays true is a five-line guard that
preserves a strategic option indefinitely. Do it in punch-list step 1.

Dependency direction is one-way: **`reason_voice/` may read the generator's
output; the generator must not know Reason exists.** Anything that needs both
(the tabs, the launcher) lives in the launcher/UI layer, not inside either half.

**What is genuinely Reason-only, for future reference** (this is the layer that
would simply not load for a non-Reason user — no rewrite required):

| Reason-only | Portable as-is | Portable in principle, Reason-flavoured in practice |
|---|---|---|
| `remote/` (Lua codec, remotemap) | the entire beat engine | `recipes/**/*.md` — the *format* is generic, the *content* says "Scream 4 → RV7000" |
| `reason_control.py` (CC map) | whisper transcribe + push-to-talk | `device_refs/` — same problem |
| `indexer.py` / `search.py` (`.thor`, `.repatch`, `.cmb` patch formats) | `intents.py` grammar | |
| `templates.py` (Reason song files) | `theory/` | |

**The real cost of going broad later is content, not code.** The technique in a
recipe transfers to any DAW (distortion before reverb, and why). The device and
knob names don't. That's a writing job of unknown size — flagged now so it isn't
discovered as a surprise at the moment someone decides to ship.

**What a non-Reason user would get today, with no further work:** the generator,
the harmony, the "why this works" teaching card, and stems + MIDI export. That's
already a coherent product. The Reason layer is a bonus tier on top, not a
prerequisite. Keep it that way and the audience question stays cheap to answer
in either direction.

---

## Part 5 — Marketing consequences of the shape (decide before step 5)

- **The generator is DAW-agnostic; Reason Voice is Reason-12-on-macOS only.**
  Package them as co-equal halves and the wide product inherits the narrow
  one's audience. Recommended framing: the beat engine is *the product*, Reason
  Voice is *an integration* — the first of potentially several. This costs
  nothing to adopt now and is expensive to reverse after the UI says otherwise.
- **The teaching angle is the differentiator, not the harmony.** Atlas / XO /
  Playbeat are drums-only, and none of them explain themselves. "Every beat
  comes with the theory of why it works" is a claim no competitor can make
  cheaply, and it agrees with the name (Homeroom) by accident of good luck.
  Punch-list step 3 is the whole feature.
- **The `autoresearch` loop is the rarest thing here.** An engine that proposes
  its own changes and takes the owner's ear as the fitness function, with
  per-DJ rollback, is not a normal consumer-tool feature. "It learns your ear"
  is both a story and a roadmap item.
- **The best hook is the one that can't ship.** Real producer names stay
  internal (settled 2026-07-22, `legends_config.json` `_readme`). "Sounds like
  Pharrell" is what would sell this and is exactly what must not appear in a
  file name, stem, title, screenshot, or landing page. Step 1 adds a new file
  that travels with beats — that's a new leak surface, hence the explicit rule.

---

## Part 6 — Honest unknowns

- **The manifest becomes a shipping artifact.** Once `.recipes/NN.json` carries
  the legend and chord data, it's a file that could travel alongside a beat.
  Audit it against the legends rule before any beat leaves the machine.
- **"One app" is a claim about his head, not the code.** Whether two tabs
  actually fix "jumbled" can only be settled by the owner using it. Log a
  check-back after step 5; don't mark it confirmed on the basis of it running.
- **Tempo over Remote is unverified.** The bridge does transport and patch
  stepping. Whether a tempo *set* is exposed as a Remote item in Reason 12 has
  not been checked in any session. Step 7 must verify before promising it, and
  fall back to "open the session and set the tempo yourself" if not.
- **Distribution is untouched by this document.** Everything above improves the
  tool for its one current user. Shipping to a stranger is a separate and much
  harder problem: bundling Python 3.9 + faster-whisper, three macOS permission
  dialogs, and a user who does not own this sample library. Do not confuse
  finishing this punch list with having a shippable product.
- **This analysis reads the code, not a running merged build.** Ports 8765 and
  8770, `save_recipe`'s current keys, `_build_chords` at line 994, `run_web`,
  `_dj_card`, `_resolve_beats_root`, and `TemplateLibrary.new_session` were each
  grepped and confirmed present in source this session. Nothing was launched
  and **`pytest` was NOT run** — the analysis ran in a Linux sandbox where the
  macOS `.venv` binary doesn't execute, so the "487 green" figure is carried
  over from `DECISIONS.md`, not re-verified. Establish the real baseline with
  one `pytest` pass on the owner's machine before starting.
