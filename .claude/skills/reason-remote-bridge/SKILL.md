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
- `remote.define_items` — 10 buttons
- `remote.define_auto_inputs` — CC 20–29 on any channel, as 7f=press / 00=release
  pairs

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
