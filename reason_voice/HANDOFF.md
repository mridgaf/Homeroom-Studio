# Reason Voice — flexible dial-control handoff brief

Read this first. Everything marked UNVERIFIED must be tested, not assumed.

## What we're building

A local, flexible parameter-control layer for the existing Reason Voice app — so the
user can say open-ended things like "give it more punch" or "turn down the threshold"
and have it actually turn the right knob in Reason, instead of only recognizing exact
pre-written phrases. This means adding a local-LLM intent-parsing step (running
entirely on the user's Mac, no cloud, no new spend) alongside the app's existing fast
deterministic regex parser, plus a reference-material knowledge base (`device_refs/`)
built from real Reason documentation so that model actually knows the terminology.

**Explicitly out of scope:** rack cable/patch-routing automation. This was
investigated at length and is structurally impossible — Reason's Remote/Lua
control-surface protocol (and every third-party controller built on it) can only ever
address a device's predefined parameters, never the rack's cable topology. Do not
revisit this; see VERIFIED below for the sourcing. Cable patches stay a one-time
manual action in Reason's GUI.

## The user

Producer, self-taught, works from a home studio. Wants direct, concise, factual
answers — no hedging, no cheerleading, no "rose-tinted glasses." Explicitly does not
want manual steps handed back when a tool could do them. Has caught and corrected
overpromising twice already in this project (was told plainly: "I think you're
overpromising. Check yourself." — and was right both times). Treat every capability
claim as something to verify against primary sources, not summarize from general
knowledge.

Machine: M2 Pro Mac, running everything locally by choice (already pays for Claude
Pro; explicitly does not want to add new subscription/API spend). Was exploring
Hermes Agent (Nous Research, self-hosted) as a free local "learning" layer parallel to
Claude — that's the origin of the "local LLM" idea here, but which specific piece of
software does the inference (full Hermes app vs. a direct local model call) is still
an open question, not a settled decision — see UNVERIFIED.

## Decisions made

- **Cable/patch routing automation: off the table, permanently.** Confirmed
  structurally impossible in Reason's own protocol. Not a limitation of this app —
  a limitation of Reason itself. Don't propose building around it.
- **Sidechain ducking (the motivating example) uses a one-time manual patch:** route
  the target instrument (e.g. Mimic, which has no sidechain input of its own) through
  an MClass Compressor or Maximizer (which do have a sidechain input), and feed the
  kick into that compressor's sidechain jack. This is a normal Reason rack action done
  once per song in the GUI — not something to automate, and not worth trying to.
- **Dial/parameter control IS automatable**, via Reason's built-in "Remote Override"
  system — right-click (Ctrl-click on Mac) any parameter → "Edit Remote Override
  Mapping" → move/send the MIDI CC you want bound to it. This works on any parameter
  on any device, regardless of whether that device or controller is on Reason's
  official supported-surface list. This is the real mechanism to build on.
- **Reuse the existing IAC MIDI bus.** `reason_control.py` already opens an IAC
  virtual MIDI port and sends fixed CC numbers for transport/patch commands. New CC
  numbers for dial control ride the same bus — no new MIDI infrastructure needed.
- **The existing regex intent parser stays.** It was built deliberately non-LLM
  (instant, deterministic, no round-trip) and that's still the right choice for
  commands that are used often and phrased consistently. The new local-LLM step is a
  *fallback* for open-ended phrasing, not a replacement.
- **Reference material comes from text documentation, not video.** Same information
  (Reason's official manual, Sound On Sound technique articles, forum threads),
  far less pipeline overhead, and it sidesteps a real constraint: the cloud session
  this brief was written in cannot reach YouTube or TikTok at all (org network
  policy blocks both) — text fetching has no such restriction.
- **That reference material has a home already designed into the code.**
  `recipes.py`/`main.py` expect a `device_refs/` folder (one markdown file per
  device/technique) and a `recipes/` folder. Neither exists on disk yet. Populate
  these rather than inventing a new storage scheme.

## VERIFIED

Checked directly — via the official Reason manual, official device docs, a
third-party technique article, and by reading the actual project code on the user's
Mac. Not inference, not general knowledge.

- Reason's Remote/Lua control-surface protocol can only ever address a device's
  predefined "Remotable Items" — confirmed via Reason Studios' own official 2006
  article, "Control Remote" (reasonstudios.com/news/post/control-remote). It never
  exposes rack cable/patch topology as a controllable item, by design.
- Sidechain compression in Reason is done by manually dragging a cable in the rack's
  rear view — confirmed via Sound On Sound's "Side-chain Compression In Reason"
  technique article.
- Mimic Creative Sampler has no sidechain/key input at all — confirmed via its
  official device docs (docs.reasonstudios.com/rackplugin14/mimic-creative-sampler):
  only Slot audio outs, FX Send Out (no FX Return), and CV/Gate.
- MClass Compressor and MClass Maximizer are standard Reason devices with dedicated
  sidechain input jacks.
- Reason has a general per-parameter "Remote Override" system, independent of any
  control-surface codec: right-click/Ctrl-click any parameter → "Edit Remote Override
  Mapping" → bind an incoming CC. Confirmed via the official Reason 12.7 manual,
  "Remote - Playing and Controlling Devices."
- Remote Overrides save **with the song**, not globally. A brand-new song starts
  with none of them. Confirmed same source. This means either redoing the mapping
  per song, or always starting from a template song that already has it saved.
- Checked two "deep Reason integration" hardware controllers — Nektar Panorama and
  MP MIDI's MP Controller (announced Jan 2026) — via their own marketing/docs pages
  (rekkerd.org, mpmidi.com/reason-studios-control, both fetched in full). Both
  operate purely through auto-following parameter/mixer/channel-strip control.
  Neither mentions cable/patch routing. Consistent with the Remote-protocol ceiling
  above — no hardware controller gets around it.
- `reason_voice/intents.py` (read in full, and grepped project-wide for
  "sidechain|route|cable|redrum|mimic"): zero real matches. It's a deterministic
  regex parser, not an LLM. There is currently no code path for anything like this.
- `reason_voice/reason_control.py` (read in full): exactly 10 fixed CC numbers for
  momentary transport/patch commands (`tap()` style — press, not a value), plus
  `open -a Reason <patchfile>` for loading patches. No continuous/value-based CC
  sending exists yet.
- Checked directly on the user's Mac (2026-09-10): `reason_voice/` currently has
  **no** `recipes/` folder, **no** `device_refs/` folder, and **no** `config.yaml`.
  These are code dependencies with defaults, not things already populated.
- `main.py`: `PROJECT_ROOT = Path(__file__).parent.parent` — one level **above** the
  `reason_voice` folder itself (i.e., in the parent "Homeroom Studio" folder).
  Defaults: `recipes_dir` = `PROJECT_ROOT/recipes`, `device_refs_dir` =
  `PROJECT_ROOT/device_refs`. Both are overridable via `config.yaml` keys of the
  same names.

## UNVERIFIED — test before building on these

- **Whether the full Hermes Agent app is the right vehicle for this, versus just
  calling a local model directly** (e.g. via Ollama or MLX) from within
  `reason_control.py`/`intents.py`. Hermes's documented strengths — persistent
  memory, a skills system, a Curator, a messaging gateway — are built for being a
  standalone chat agent, not necessarily a low-latency embedded command parser.
  Routing every dial command through the full Hermes app may add overhead a direct
  local inference call wouldn't. This has not been tested either way — don't assume
  Hermes is the right integration point just because it's the AI product the user
  was originally exploring.
- **What local model + quantization actually gives usable latency on this specific
  Mac (M2 Pro) for this specific task.** Qwen3.5-9B at Q4_K_M quantization was
  floated earlier as a fit for 8–16GB unified memory, but was never benchmarked for
  real-time-ish command parsing. "A few seconds" was the user's stated tolerance —
  confirm the chosen model actually lands there before building the rest around it.
- **Whether "Homeroom Studio" (the parent folder the code's defaults point at)
  already contains anything relevant.** It has never been connected to a session or
  inspected — only `reason_voice` and `ard app` have been. Don't assume it's empty
  or that it has useful content; check first.
- **How to handle copyrighted source text** (Reason's official PDF manual, forum
  posts, magazine articles) when building `device_refs/` entries. Treat these as
  sources to read and take original notes from — extract facts, terminology, and
  technique steps in your own words — not material to copy in bulk.
- **No implementation exists yet for any of this.** Everything above is analysis and
  confirmed constraints from a planning conversation, not working code. Don't report
  any of the build-order steps below as done until they've actually been run.

## Build order

1. **Resolve the two blocking open questions below with the user before writing any
   code or creating any folders.** Don't guess at folder placement or model choice.
2. Create `device_refs/` (and `recipes/` if the user wants it) in whichever location
   was chosen in step 1.
3. Populate `device_refs/` with a markdown reference file for the concrete motivating
   case already worked out: MClass Compressor's sidechain input, and the
   Mimic-through-compressor patch technique. Use this as the template for later
   entries — the format `recipes.py` expects is plain markdown with YAML frontmatter
   (see that file for the exact fields it parses).
4. Extend `reason_control.py`: add a value/increment-capable CC-send method distinct
   from the existing momentary `tap()`, and a small parameter→CC lookup table.
5. In Reason itself (manual, on the user's own machine): set up Remote Override
   mappings for whichever knobs get wired up first. Document each mapping (CC
   number, parameter, device) directly in that device's `device_refs/` entry so it
   isn't lost — remember these don't survive into new songs automatically.
6. Wire in a local-LLM fallback: when the regex parser in `intents.py` doesn't match
   anything, hand the phrase to the local model along with the available
   parameter/CC table (built from `device_refs/`) and let it pick a command. Keep
   this a fallback path — the fast regex path stays primary for anything it already
   handles.
7. Test end-to-end on the one real case before generalizing: say something
   open-ended about the Mimic/kick sidechain compressor and confirm the right knob
   actually moves in Reason.

## Reusable from prior work

| File | Keep/Discard | Why |
|---|---|---|
| `reason_control.py` | Keep, extend | Working IAC MIDI bridge; add a value-based send method alongside the existing `tap()` |
| `intents.py` | Keep, extend | Working deterministic parser; stays as the fast path, add new patterns plus a fallback-to-local-model branch |
| `recipes.py` | Keep, use as-is | Already parses exactly this kind of markdown reference content — just needs the folders it reads from to exist and be populated |
| `main.py` | Keep | Already wires `recipes`/`device_refs` in via config; may need a `config.yaml` added if the folder location changes |
| `server.py`, `static/` | Untouched | Web frontend, not part of this work — no changes needed |

## Open questions for the user

1. **(Blocking)** Where should `device_refs/`/`recipes/` actually live — connect the
   parent "Homeroom Studio" folder so it matches the code's built-in default, or
   redirect via a new `config.yaml` into `reason_voice/` itself to avoid connecting
   anything new? Ask before creating folders.
2. **(Blocking)** How should the local model actually be called — a direct call to a
   local model runtime (Ollama/MLX), or through the full Hermes Agent app? This
   changes the integration shape, so pick before writing the fallback code in step 6.
3. Beyond the Mimic/kick compressor example, which devices/parameters should get
   wired up first? Given both the regex patterns and the Remote Override mappings
   are hand-authored, scope this narrowly rather than trying to cover everything
   Reason has at once.

---

## UPDATE (2026-09-10) — local model stack is live and verified

Open question #2 at the bottom of this brief is now answered. Do not re-ask it.

### VERIFIED (actually run and confirmed working on the user's Mac)

- Homebrew, llama.cpp, and huggingface-cli installed.
- Model downloaded to `~/models/Qwen3.5-9B-Q4_K_M.gguf` (~5.3 GB).
- Working server command — this must be running or nothing below functions:
  `llama-server -m ~/models/Qwen3.5-9B-Q4_K_M.gguf -ngl 99 -c 65536 -np 1 -fa on --cache-type-k q4_0 --cache-type-v q4_0 --host 127.0.0.1`
  Serves an OpenAI-compatible API at `http://127.0.0.1:8080/v1`.
- Hermes Agent installed and configured in `~/.hermes/config.yaml` on a Blank Slate baseline:
  - `model.provider: custom`, `base_url: http://localhost:8080/v1`,
    `default: Qwen3.5-9B-Q4_K_M.gguf`, `api_mode: chat_completions`, context_length 65536.
  - Memory enabled: `memory.memory_enabled: true`, `user_profile_enabled: true`, AND
    `memory` removed from `agent.disabled_toolsets`. That toolset list is the real gate —
    flipping the booleans alone does not enable memory.
  - Skills enabled (present in `platform_toolsets.cli`, never in the disabled list).
  - Off by design: browser, web, code_execution, delegation, cronjob, image_gen, tts, stt,
    and the rest of the Blank Slate disabled list.
  - A pre-edit backup sits beside it as `config.yaml.bak.<epoch>`.
- End-to-end test passed: `hermes` → prompt → correct reply, status bar showing
  `Qwen3.5-9B-Q4_K_M`.

### Measured — and it settles the architecture question

That first working turn showed **7.97K of 65.5K context consumed before the user's prompt
was even counted**. That is Hermes' fixed system prompt plus tool schemas, sent on every
call. A background title-generation call also timed out on the same turn.

Conclusion, now measured rather than inferred: **do not route per-dial voice commands
through Hermes.** ~8K tokens of prefill per command on a local 9B model is far too slow for
"turn down the threshold." For the dial-control feature, call the llama.cpp server directly
at `http://127.0.0.1:8080/v1/chat/completions` with a small purpose-built prompt (the spoken
phrase plus the available parameter/CC table). Hermes stays in the picture for the separate,
latency-tolerant job it was actually wanted for: ingesting Reason documentation and building
up memory/knowledge over time.

### Still open

- Question #1 (where `device_refs/` and `recipes/` should live) is still unanswered. Ask the user.
- `llama-server` does not auto-start. It runs only while its Terminal window is open; after a
  reboot or a closed window it must be relaunched with the command above. Turning it into a
  launch-at-login service is unstarted work.
