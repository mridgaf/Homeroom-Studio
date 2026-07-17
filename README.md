# Reason Voice

Push-to-talk speech control for Reason 12 on macOS. Hold a key, say "find a warm analog pad" or "next patch", release. Everything runs locally — speech never leaves your machine.

## How it works (and why it works this way)

Reason has no scripting API, so this uses the two channels Reason officially supports:

1. **Remote protocol.** A custom control-surface codec (`remote/ReasonVoice.luacodec`) listens on the Mac's built-in IAC virtual MIDI bus. The Python app sends CC messages; Reason's Remote map translates them into *Select Next/Prev Patch for Target Device*, transport, track targeting, undo/redo. This is the same mechanism hardware controllers use — reliable and version-safe.
2. **Patch files.** Style search scans your patch folders, builds an index, and loads a chosen result with macOS `open` — Reason creates the device with that patch in your open song.

## Setup

```bash
cd reason-voice
chmod +x install.sh && ./install.sh
```

Then the one-time manual steps the installer prints: enable the IAC Driver in Audio MIDI Setup, add the "ReasonVoice" control surface in Reason's preferences (input: IAC Driver Bus 1), and grant Microphone permission to Terminal. (Input Monitoring is no longer needed — v2 has no global hotkey.)

Edit `config.yaml` and list every folder that contains patches (your saves, sound packs, extracted ReFills).

## Run

Double-click **ReasonVoice.command**. A window opens in your web browser: hold the big **Talk** button (or the spacebar) while you speak, or click the buttons — every voice command has one. Recipes show as readable cards with the current walkthrough step highlighted, and there's a type-box that understands the same phrases as voice. The ⚙ settings has the spoken-feedback toggle (off by default) and a tiny.en/small.en speed switch.

The old terminal version still exists (`./.venv/bin/python -m reason_voice.main`, hold right Option to talk) but the web window is the intended way to run it now.

| Say | Does |
|---|---|
| "next patch" / "previous patch" | steps patches on the Remote-targeted device — works with the Factory Sound Bank |
| "play" / "stop" / "record" / "loop on" | transport |
| "next track" / "previous track" | moves the Remote target |
| "find a dirty acid bass" | searches your library, reads back top 5 |
| "load two" | loads result #2 into the rack |
| "load massive attack pad" | searches and loads the best match directly |
| "find something like this" | patches similar to the last one loaded |
| "find drum loops" / "bass samples" | browses loose audio on your drive, grouped into bins |
| "preview two" / "stop preview" | auditions a sample result without leaving the window |
| "more results" / "rebuild index" / "undo" / "quit" | what they say |

## The recipe brain (v0.2)

The app now carries a sound-recipe knowledge base merged from the Reason 12 Knowledge Project. Say "recipe for a trap 808" or "sounds like Phil Collins drums" — it finds the recipe, prints the full quick-format card (chain, exact settings, accuracy rating, transferable technique), and speaks a summary. Say "walk me through it" and it reads each step aloud; "next step" / "repeat" / "back step" / "done" navigate hands-free while you patch.

Recipes are markdown files in `recipes/` with YAML frontmatter (name, book, accuracy A–D, tested/theoretical status, tags, technique). Ten seed recipes ship (5 rock, 5 hip-hop, per the v3 Phase 1 plan) plus anti-recipe lists and four device references (`device_refs/` — try "what is Scream 4"). Add your own `.md` files and they're indexed on next start — that's the "Your Sound" section growing.

Two honest notes: every seed recipe is tagged **theoretical** — settings are principled but not session-verified; test them and edit the files (that's the design). And the app cannot build the chains for you — Reason has no device-creation API. It's a hands-free reference, plus patch loading and Remote control.

## Templates

Reason can't be scripted to build device chains, so a template is built once by hand: follow a recipe's walkthrough, then save the song (File → Save As…) — or just the chain as a Combinator patch — into the `templates/` folder, named after the recipe. From then on it shows in the Templates list and on the matching recipe's card. "New session from trap 808" (or the button) copies the template into `~/Music/Reason 12/Sessions` with a date stamp and opens the copy, so the original is never overwritten. Combinator templates load straight into the current song instead.

## Honest limitations

- **Factory Sound Bank isn't searchable.** It's a sealed archive; no tool can index it from outside Reason. Next/prev browsing covers it, search doesn't.
- **Loading a search result creates a new device** rather than replacing the patch on an existing one — that's how `open` behaves. To change sounds on an existing device, target it (click it in Reason) and use "next/previous patch".
- **Search quality = your file names.** The index reads folder and file names plus device type. Well-named sound packs search well; `Patch_047.zyp` doesn't. No audio-content analysis in v1.
- **Routing by voice is not in v1.** Rack cabling has no Remote items and no API; it would need fragile screen automation. Feasible as a v2 experiment, not something to rely on mid-session.
- **Remote item names** in `ReasonVoice.remotemap` match Reason 12's English strings. If a command doesn't fire, check the surface shows a green tick in Preferences > Control Surfaces, and that the map installed to `~/Library/Application Support/Propellerhead Software/Remote/Maps/ReasonVoice/`.

## Latency expectations

Push-to-talk release → action is roughly 0.5–1.5 s with `small.en` on Apple Silicon. Use `tiny.en` in `config.yaml` for ~2× faster transcription at some accuracy cost. MIDI commands themselves are instant.

## Extending

- New voice commands: add a regex in `reason_voice/intents.py`, a CC in `reason_control.py`, a matching input in the `.luacodec`, and a `Map` line in the `.remotemap`. Any Remote item Reason exposes (device knobs included) can be wired this way.
- Better search vocabulary: extend `SYNONYMS` in `reason_voice/search.py` with terms your libraries use.
