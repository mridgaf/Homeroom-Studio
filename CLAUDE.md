# Reason Voice — Project Handoff & v2 Rebuild Brief

## What this is
A push-to-talk voice interface for Reason 12 (DAW) on macOS. Hold a hotkey, speak,
release: browse patches, control transport, search a sound-recipe knowledge base,
and get walked through recipes step-by-step. All speech is processed locally
(faster-whisper). v0.3 works end-to-end and is verified on the owner's machine.

## Owner & machine facts (do not rediscover these)
- User: self-taught musician, technical background, NOT a developer. All
  instructions to the user must be single paste-able commands or double-clickable
  files. He runs commands in Terminal, sometimes pastes into the wrong window.
- Machine: older MacBook Pro, **system Python 3.9** (Command Line Tools).
  NO `X | Y` union syntax without `from __future__ import annotations`. Target 3.9.
- Project lives at: `~/Music/Reason 12/reason-voice 3` (space in path — always quote).
- Shell is bash (not zsh). macOS `sed` needs `-i ''`.
- His sound library is almost entirely **inside ReFills + Factory Sound Bank =
  sealed archives, cannot be indexed**. He owns ~2 loose patch files. The patch
  style-search feature is therefore nearly useless to him today; it only gains
  value as he saves his own patches. Deprioritize it in v2 UI.

## Architecture that WORKS — keep these layers
1. **Reason Remote bridge (do not rewrite, it was painful to get right):**
   - `remote/ReasonVoice.luacodec` — manifest. Reason REQUIRES:
     `remote_supported_control_surfaces()` returning a table with manufacturer,
     model, `source="ReasonVoice.lua"`, `in_ports`, **`out_ports` (mandatory)**,
     `has_keyboard`.
   - `remote/ReasonVoice.lua` — logic file with `remote_init()`,
     `remote.define_items` (10 buttons), `remote.define_auto_inputs`
     (CC 20–29 on any channel, 7f=press/00=release pairs).
   - `remote/ReasonVoice.remotemap` — **TAB-separated, first line
     `Propellerhead Remote Mapping File`, line 2 `File Format Version` TAB
     `1.0.0`.** Tabs are load-bearing; they get destroyed by copy-paste, so
     always write this file from a script, never by hand.
   - Install locations:
     `~/Library/Application Support/Propellerhead Software/Remote/Codecs/Lua Codecs/ReasonVoice/`
     and `.../Remote/Maps/ReasonVoice/`. Reason only reads codecs at launch
     (full Cmd+Q restart required).
   - Patch next/prev is mapped per-device-scope (Combinator, Kong, Redrum,
     SubTractor, Thor, Malström, NN19, NN-XT, Dr.REX, ID8, Alligator,
     Pulveriser, The Echo). Document-scope `Select ... for Target Device`
     items were NOT verified — that's why per-device scopes are used.
   - Python side sends CC via mido → macOS IAC Driver Bus 1 (user has it enabled).
   - The registered surface in Reason's prefs: Manufacturer/Model "ReasonVoice",
     input IAC Driver Bus 1. Already set up on his machine.
2. **Recipe knowledge base (keep the data format exactly):**
   - `recipes/**/*.md` with YAML frontmatter: name, book (rock|hip-hop),
     sounds_like, accuracy (A–D honesty rating), status (tested|theoretical),
     source, tags, technique. Body sections: `## The Chain`, `## Steps`
     (numbered — drives the voice walkthrough), `## Why this works`,
     `## Order of operations`, `## Reason-specific trick`, `## RE upgrade path`,
     `## Technique you just learned`, `## Reference`.
   - 14 recipes exist (5 rock, 7 hip-hop incl. 2 Doechii, 2 anti-recipe lists).
   - `device_refs/*.md` — 4 plain-language device guides.
   - `tools/make_recipe_pdfs.py` regenerates a printable PDF book from the .md
     files (reportlab). Keep working after any refactor.
3. **Loading found patches:** `open -a Reason <patchfile>` adds the device to the
   rack. Only channel besides MIDI. There is NO API to build device chains,
   route cables, or set knobs programmatically. Never promise that.

## Current v0.3 code (Python, works but UI is the weak part)
`reason_voice/`: `main.py` (loop + session state), `ptt.py` (pynput hotkey +
sounddevice), `transcribe.py` (faster-whisper small.en int8),
`intents.py` (ordered regex grammar — pattern order matters, reindex must
outrank recipe search), `recipes.py` (parser/search), `indexer.py` +
`search.py` (patch index, synonym-expanded scoring), `reason_control.py`
(mido CC map — MUST stay in sync with the .lua codec), `config.yaml`.
Launch: `ReasonVoice.command` (double-click, runs in Terminal).

## Why the owner wants a rebuild (his words: "clunky", "jumbled")
- Terminal UI confuses him: results look like "a few sentences", the
  list→"load two"→walkthrough flow is not discoverable, spoken feedback (`say`)
  overlaps, and typing commands into the app's window does nothing (he did this
  repeatedly — one-window model fails him).
- Multi-step install with three macOS permission dialogs was painful.
- No visual state: can't see if it's listening, what recipe is open, what step
  he's on.

## v2 product brief
Build a **single always-visible window** that shows:
listening state (idle/recording/thinking), transcript of what it heard,
the current recipe as a readable card (like the PDF layout), current step
highlighted during walkthrough, big clickable buttons duplicating every voice
command (voice optional, never required), and a browsable recipe list.
Everything clickable AND speakable.

**DECIDED — owner confirmed this shape; build it, don't re-ask:**
local web UI: Python backend (keep all existing modules) + FastAPI/Flask +
WebSocket, serving `http://localhost:port`, auto-opened in the browser by the
launcher. Rationale: (a) rich UI without new macOS permission fights for
key-listening — put push-to-talk as a BUTTON (click-and-hold / spacebar in the
page) so pynput/Input Monitoring can be dropped entirely; (b) mic can stay in
the Python process (sounddevice, already permitted for Terminal) — do NOT move
audio capture into the browser; (c) recipe cards render beautifully in HTML.
Avoid Electron (heavy) and avoid packaging with PyInstaller until the UI is
stable.

**Keep:** recipe .md format + all content, PDF generator, Remote bridge files
verbatim, mido CC map, faster-whisper. **Drop:** pynput global hotkey (replace
with in-page control), `say` spoken feedback by default (visual instead, toggle
in settings), the bare-terminal REPL.

**Migration constraints:** venv rebuild must use system python3 (3.9);
`pip install` inside `.venv`. Do not move the project folder (Remote files and
his muscle memory point at it). Test plan: `python -m pytest` isn't set up —
port the ad-hoc intent/recipe/search checks into `tests/test_intents.py` +
`tests/test_recipes.py` first, then refactor.

## Known open items
- All recipes are status: theoretical — as he tests them, flip to tested.
- Whisper "find something like this" often transcribed as "and something like
  this" — v2 should fuzzy-match intents, not just regex.
- `small.en` latency ~1s on his hardware; offer tiny.en toggle in UI settings.
