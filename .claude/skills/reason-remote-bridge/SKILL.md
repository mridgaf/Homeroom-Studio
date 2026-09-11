---
name: reason-remote-bridge
description: The working Reason 12 Remote control-surface bridge — the exact file formats, mandatory keys, install paths, and device scopes that took several painful attempts to get right. Use whenever touching remote/ReasonVoice.luacodec, remote/ReasonVoice.lua, remote/ReasonVoice.remotemap, the mido CC map in reason_voice/reason_control.py, or anything about sending MIDI CC to Reason, patch next/prev, transport control, or the IAC Driver. Also use when Reason is not seeing the control surface, when a codec change appears to do nothing, when asked to add a new remotable control, when a knob will not move or Reason is not reporting values back, and before running any script that sends CC while Reason may be open.
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

## The return path: Reason → us (added 2026-09-10)

Sending CC is only half the bridge. Reason talks back, and every rule below was
found by something failing silently — same as the rest of this layer.

### 1. The device must be LOCKED. Selecting it does nothing.

Ctrl-click the device panel in Reason → **"Lock to ReasonVoice"**.

Control surfaces follow the sequencer's **Master Keyboard Input** (Operation
Manual ch.23, pp.587–606). An **effect device has no sequencer track**, so an
MClass Compressor can *never* hold Master Keyboard Input. Locking is the only
route to any effect. The lock saves with the song.

This cost a full failed test cycle: the Lua and the map were already correct
and verified identical in form to Reason's own factory codecs. The missing step
was not in the code. **If a knob will not move, check the lock before you read
a single line of Lua.**

### 2. The surface's MIDI **output** must be assigned

Reason → Preferences → Control Surfaces → ReasonVoice → **MIDI Output =
IAC Driver Bus 1**.

The `.luacodec` setup text used to say output could be left unassigned. That
was true before feedback existed and is **false now**. With it unassigned,
nothing comes back and it looks exactly like broken code.

One bus, not two: we send CC 30–37 and receive CC 60–67 + SysEx, so our own
echo off the IAC loopback is distinguishable and is ignored by CC number.

### 3. Reason reports a parameter ONLY when it CHANGES

This one has bitten twice. Three consequences, all counter-intuitive:

- **Writing a value the control already holds produces no report.** Soft Knee
  is a *button* sitting off, so writing position 0 first was silent and
  `calibrate.py` skipped the whole knob as dead. Fix: seed every sweep by
  driving to 127 first, so the first real write is guaranteed to be a change.
- **Nothing is volunteered on lock.** Confirmed 2026-09-10 against live Reason:
  after locking, the app knows *nothing* about any knob until that knob moves.
  A UI must show "unknown" and fill in, not invent positions.
- **Mid-sweep silence means "unchanged", not "no answer".** A 2-state control
  reports twice across 128 positions and says nothing in between. Carry the
  last reading forward rather than bailing.

Also: mido buffers input until it is collected. **Something has to poll**, or
the reports sit in the port and the app looks deaf.

### 4. `text_value` is Reason's own display — never model a taper

`remote.get_item_state(idx)` returns `text_value`: the parameter exactly as
Reason shows it ("30 ms", "-20.0 dB", "4.06:1"). That kills the whole
curve-modelling problem. The manual gives *ranges* but not tapers.

`reason_voice/calibrate.py` sweeps each knob 0–127 and records what Reason
displays at every position into `docs/reason/calibration.json`. Look values up
in that table; never compute them.

Do not generalise one knob to another. Attack happens to be linear
(`ms = floor(1 + pos*99/127)`, exact on all 33 observed points) — that says
**nothing** about Ratio or Release. Measure each one.

### 5. Before running anything that sends CC: check whether Reason is open

```bash
ps aux | grep -i "[R]eason 12"
```

If Reason is running with a device locked, **your test moves a knob in his
open song.** This happened on 2026-09-10 during a UI check — a real Attack knob
moved twice before anyone noticed Reason was up.

If it is running: say so before you send anything, capture the current position
first (`control.current(knob)`), and put it back when you are done. Never leave
his song changed by a test. Same house rule as `trial-edits-need-warning`,
applied to his session state instead of his files.

### The proof scripts, in the order you need them

| Script | Proves |
|---|---|
| `reason_voice/prove_knob.py` | a knob moves at all (run this first — it fails loudly if unlocked) |
| `reason_voice/prove_feedback.py` | Reason reports back, AND notices a knob moved by mouse |
| `reason_voice/calibrate.py` | what every position MEANS, written to `docs/reason/calibration.json` |

All three live in `reason_voice/`, **not** `tools/` — `tools/` is DAW-neutral
and `tests/test_boundary.py` fails if anything there imports `reason_voice`.
