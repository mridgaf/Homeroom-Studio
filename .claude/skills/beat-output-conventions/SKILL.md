---
name: beat-output-conventions
description: House conventions for how generated beats and loops are named, paired with recipes, and sourced from the owner's own samples — so new output slots cleanly into his library and the cleanup/quarantine tools keep working. Use whenever this project renders beats, loops, packs, or experiments to disk. Covers file naming (NN Name Drums NNNbpm), the matching .recipes/NN.json pairing, numbering, real-sample sourcing, and running the MIDI gate before delivery. Does NOT impose any musical style — style is specified per request.
---

# Beat Output Conventions

How output is written to disk, so it fits the library instead of creating
orphans. This is about **file plumbing, not sound.** There is deliberately no
default genre, tempo, artist, or "house style" here — every beat's style is
whatever he asks for that time (owner decision 2026-07-23). If he doesn't
specify, ask; don't assume.

## BEFORE you render anything (hard rule, owner 2026-09-09)

**The full suite runs once per session, before the first render.**
```
./.venv/bin/python -m pytest tests/ -q
```
~1036 tests, ~6-8 min. Later renders that session don't repeat it unless
code changed.

**Never render while it is running.** Both read beats off the external
drive and starve each other — the suite crawls, the render slows, and the
suite looks hung when it isn't. Tests finish, THEN you render.

Why it exists: on 2026-09-09 a new legend was rendered three times before
the suite was ever run, and three roster assertions in `tests/test_crew.py`
had been failing the whole time — one of them since 2026-09-07, unnoticed.
The renders also ran on top of a background suite, which is what made it
take 6m28 and produce nothing readable. Full rule in CLAUDE.md §0d.

## Naming

- Pattern: `NN Name Drums NNNbpm.wav` — the number `NN` orders it, the word
  `Drums` routes it to the drums bin, and `NNNbpm` powers tempo search.
- **Never put "Claude" in a beat/loop filename** — the output folder name
  carries the branding; files are just the name.
- Experiments: `Experiment NN <Idea> Drums NNNbpm.wav`.

## Recipe pairing (this is what the cleanup tools depend on)

- Each numbered beat has a matching recipe at `.recipes/NN.json` recording how
  it was made (`kit_paths`, `stamp_paths`, etc.). Write it whenever you render
  a beat.
- `tools/clear_junk_beats.py` and `tools/quarantine_banned.py` key off the
  leading number (`^(\d+) `) to move a beat **and** its `.recipes/NN.json`
  together. If naming or the recipe pairing drifts, those tools create orphans
  (recipe JSONs with no beat, or beats they can't classify). Keep them in sync.
- Numbering is handled by `beat_machine.next_number()` (floors at 85, scans
  existing numbered .wav files for the max). Don't hand-number.

## Sourcing — use his real kit, not synth fallbacks

- Sample-based beats go through `tools/make_drum_beats.py`, which sequences
  **his** one-shot library (`tools/sample_library.py`). Always use a **real
  808 kick sample** (`musts={"kick": "808"}`) and real sampled snares — never
  synth fallbacks — for these.
- The pure synth engine is `tools/make_drum_loops.py` (see the `drum-loops`
  skill); that one is intentionally synthesized. Pick the engine the request
  implies; when he says "use my samples", it's `make_drum_beats.py`.
- Output roots: beats → `~/Documents/Samples/Claude Drum Beats`, loops →
  `~/Documents/Samples/Claude Drum Loops`, where Reason Voice indexes them.

## Before you hand it over

Run the **midi-validity-gate** skill on every `.mid` rendered (channel 10, GM
notes, embedded tempo). Don't report beats as ready until it passes. And say
plainly you can't hear them — describe what changed and let his ears judge.
