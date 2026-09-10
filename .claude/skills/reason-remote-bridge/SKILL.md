---
name: reason-remote-bridge
description: The working Reason 12 Remote control-surface bridge — the exact file formats, mandatory keys, install paths, and device scopes that took several painful attempts to get right. Use whenever touching remote/ReasonVoice.luacodec, remote/ReasonVoice.lua, remote/ReasonVoice.remotemap, the mido CC map in reason_voice/reason_control.py, or anything about sending MIDI CC to Reason, patch next/prev, transport control, or the IAC Driver. Also use when Reason is not seeing the control surface, when a codec change appears to do nothing, or when asked to add a new remotable control.
---

# Reason Remote bridge

**DO NOT REWRITE THIS LAYER.** It works, and it was painful to get right. The
rules below are all load-bearing — each one was found by something failing
silently.

## The three files

### `remote/ReasonVoice.luacodec` — the manifest
Reason REQUIRES `remote_supported_control_surfaces()` to return a table with:

- `manufacturer`
- `model`
- `source = "ReasonVoice.lua"`
- `in_ports`
- **`out_ports` — mandatory.** Omitting it makes Reason ignore the codec with
  no error.
- `has_keyboard`

### `remote/ReasonVoice.lua` — the logic
- `remote_init()`
- `remote.define_items` — 10 buttons + 8 knobs
- `remote.define_auto_inputs` —
  - buttons: CC 20–29 on any channel, as 7f=press / 00=release **pairs**
  - knobs: CC 30–37, `input="value", min=0, max=127`, ONE line each
    (`{pattern="b? 1e xx", name="Knob 1"}`) — no press/release pair
- Knobs are per-device: which parameter "Knob 5" moves is decided by the
  `Scope` block in the .remotemap, not by the codec. Parameter names are
  **copied verbatim** from Reason 12's own factory maps in
  `/Applications/Reason 12.app/Contents/Resources/Remote/DefaultMaps/` —
  never invented, never guessed.

### `remote/ReasonVoice.remotemap` — the mapping
- **TAB-separated.** Tabs are load-bearing.
- First line: `Propellerhead Remote Mapping File`
- Second line: `File Format Version` TAB `1.0.0`

**Always write this file from a script, never by hand.** Copy-paste destroys
the tabs and the failure is silent.

## Install locations

```
~/Library/Application Support/Propellerhead Software/Remote/Codecs/Lua Codecs/ReasonVoice/
~/Library/Application Support/Propellerhead Software/Remote/Maps/ReasonVoice/
```

**Reason only reads codecs at launch.** A full Cmd+Q restart is required — not
just closing the song. If a codec edit seems to have done nothing, this is why.

## Device scopes

Patch next/prev is mapped **per-device-scope**: Combinator, Kong, Redrum,
SubTractor, Thor, Malström, NN19, NN-XT, Dr.REX, ID8, Alligator, Pulveriser,
The Echo.

Document-scope `Select ... for Target Device` items were **NOT verified** —
that is precisely why per-device scopes are used instead. Don't "simplify" to
document scope without testing it in Reason first.

## Python side

- Sends CC via `mido` → macOS **IAC Driver Bus 1** (the owner has it enabled).
- The CC map lives in `reason_voice/reason_control.py` and **MUST stay in sync
  with the .lua codec.** Changing one without the other breaks the bridge
  quietly.
- Registered surface in Reason's prefs: Manufacturer/Model `ReasonVoice`,
  input IAC Driver Bus 1. Already set up on his machine.

## Hard limit — never promise otherwise

`open -a Reason <patchfile>` adds a device to the rack. That is the **only**
channel besides MIDI. There is **NO API** to build device chains, route cables,
or set knobs programmatically.

## The repo copies are authoritative now (2026-09-10)

Until this date `remote/` held an **older draft that had never installed
successfully**, while the working files existed only under `~/Library`. `git log`
showed `remote/` untouched since the initial commit — the bridge was fixed by hand
in the install location and never copied back.

`install.sh` would have overwritten the working codec with that draft. What differed:

| File | The draft in the repo | The working file |
|---|---|---|
| `.luacodec` | held `remote_init` (the logic) | holds `remote_supported_control_surfaces` (the manifest) |
| `.lua` | **absent** | holds the logic |
| `.remotemap` | `File Format Version 1.3`, one document scope using `Select Next Patch for Target Device` | `1.0.0`, 13 per-device scopes |

The draft is kept, clearly labelled, in
`remote/_installed_backup_2026-09-10/superseded_repo_draft/`. Do not reinstall it.

`tests/test_remote_bridge.py` now guards all four silent failure modes — CC drift
between the `.lua` and `reason_control.py` (press *and* release lines), a missing
mandatory codec key, tabs turned into spaces, and a command the map doesn't cover.
All four were confirmed by mutation — but NOT by the session that wrote them,
which claimed so falsely; an independent audit did it afterwards, against
copies held in memory. If you change these guards, mutation-test them yourself
and do not trust this paragraph.

**Rule: edit `remote/` in the repo, then run `install.sh`. Never edit inside
`~/Library` and leave the repo behind — that is exactly how this happened.**

## Adding knobs: copy the names, never invent them

Reason 12 ships its own Remote data at:

```
/Applications/Reason 12.app/Contents/Resources/Remote/   (578 files)
```

`DefaultMaps/**/*.remotemap` are the factory maps for every supported surface —
**11,503 device+parameter pairs across 148 devices**, in Reason 12's own spelling
(verify with `python3 tools/reason_vocab.py`, which prints the count it derives —
do not trust this number, re-derive it).
`Launchkey MK3.remotemap` is the owner's actual keyboard and the best single source.

To make a knob controllable, add a value item to the codec and a per-device section
to `ReasonVoice.remotemap`, taking the remotable item name **verbatim** from a
factory map:

```
Scope   Propellerheads   MClass Compressor
Map     Knob 1    Threshold
Map     Knob 5    Attack
```

A name that isn't spelled exactly as Reason spells it fails silently, like
everything else in this layer. Do not guess one; grep the factory maps.

This is the supported route. **Remote Override** (right-click a knob → learn) also
works but saves *with the song*, so it must be redone in every new song — do not
build on it. `reason_voice/HANDOFF.md` proposed exactly that; it is superseded.
