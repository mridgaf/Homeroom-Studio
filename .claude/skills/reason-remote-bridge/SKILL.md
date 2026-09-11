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
- `remote.define_items` — 10 buttons + 48 knobs + one `Device` text item
- `remote.define_auto_inputs` —
  - buttons: CC 20–29 on any channel, as 7f=press / 00=release **pairs**
  - knobs: CC 30–77, `input="value", min=0, max=127`, ONE line each
    (`{pattern="b? 1e xx", name="Knob 1"}`) — no press/release pair
  - `Device` has `output="text"` and NO input: it is report-only
- **Write the knob items and their input lines out literally.** They look like
  an obvious `for` loop, and `tests/test_remote_bridge.py` reads this file as
  TEXT — a loop blanks its guards without failing anything.
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
| `.remotemap` | `File Format Version 1.3`, one document scope using `Select Next Patch for Target Device` | `1.0.0`, 17 per-device scopes |

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
Map     Device    Device Name
Map     Knob 1    Threshold
Map     Knob 5    Attack
```

A name that isn't spelled exactly as Reason spells it fails silently, like
everything else in this layer. Do not guess one; grep the factory maps.
`tests/test_remote_bridge.py::test_every_mapped_parameter_is_a_real_reason_parameter`
now checks every one against `docs/reason/remote-vocab.json` — run it before
believing a new block works.

**Every knob scope needs `Map Device ... Device Name`.** More than one device
has knob blocks now, and they share knob NUMBERS, not parameters. The app
identifies which one is locked from the parameter names Reason reports back
(`device_for_param()` in `dial_llm.py`); `Device Name` is a cold-start hint
only, because it is the rack LABEL and the owner can rename it. With neither
available the app refuses to move anything rather than read a Scream's knob
out of the compressor's calibration table.

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

One bus, not two: we send CC 30–77 and receive CC 78–125 + SysEx, so our own
echo off the IAC loopback is distinguishable and is ignored by CC number.

**The two ranges must never overlap**, and the budget is tighter than it
looks: 10 buttons + N knobs out + N knobs back inside 128 CCs caps the surface
at **59 knobs, ever**. That ceiling is why Kong reaches all 16 pads three
controls deep (48) and not six deep (96 — impossible). Widening the knob count
on 2026-09-11 moved the FEEDBACK range (60–75 → 78–125) to make room; knobs
1–16 kept their outgoing CCs so nothing already measured had to be re-swept.
`tests/test_remote_bridge.py::test_the_two_directions_never_share_a_cc` is the
guard — an overlap makes the app read its own echo as Reason's answer, which
is silent and corrupts the one table the dial trusts for real units.

**`displays` is keyed by knob SLOT and is never cleared — scan it NEWEST
first.** The devices are different widths (Kong 48, Redrum 40, Scream 16,
MClass 8), so after a wide sweep the high slots keep the previous device's
parameter names forever. Oldest-first identification then pins the device he
unlocked an hour ago and moves the right CC out of the WRONG calibration
table. `reason_control.py` re-inserts on every report so the dict stays in
report order; `_sync_device()` walks it reversed. Guard:
`tests/test_dial.py::test_the_device_is_read_from_the_newest_report_not_the_oldest`.

**Two devices can number the same copies.** Kong and Redrum BOTH spell
loudness `Drum N Level`, on channels 1-10. `device_for_param()` is a
uniqueness test over MAPPED parameters only, so the collision appeared the
moment Redrum's block was written and it makes those 10 names identify
nothing. It is survivable because `_sync_device()` scans every parameter
Reason has reported, not just the last one, and Kong's `Pitch Offset` /
`Decay Offset` and Redrum's `Pitch` / `Length` / `Pan` are unique — one move
of any of those pins the device for the session. **Check the overlap before
adding a device**: `set(vocab[a]) & set(vocab[b])` against the parameters you
intend to MAP, not the whole vocabulary. Wiring Redrum's Tone or Pan onto Kong
would widen this from 10 names to 26.
`tests/test_dial.py::test_kong_and_redrum_both_say_drum_n_level` states it so
it is found on purpose rather than in his song.

**Reason's Remote name is not the name on the panel.** Dr. Octo Rex is
`Dr.REX Loop Player` in every scope, vocab entry and `--device` argument — the
Reason 5 name never changed. Arturia's own factory map confirms it: that exact
scope is labelled "Dr. Octo REX" on the keyboard's LCD. Grep the factory maps
for the scope name; never type the panel name and assume.

**Before wiring a device, check what is REMOTABLE, not what is possible.**
The best techniques for a device are usually the ones a control surface cannot
touch. Dr. Octo Rex's famous moves are all slice-level — alt-group randomising,
sending one slice to a reverb through the rear slice outputs, drawing
modulation in Slice Edit Mode — and slice pitch, pan, level, decay, reverse,
alt group and slice output are **not remotable parameters at all**. Kong's
drum-module and per-pad-effect knobs are the same. Research the device first,
then intersect with `docs/reason/remote-vocab.json`, and design from what
survives. Designing from the technique list and discovering the gap afterwards
produces a map that promises moves Reason never performs.

**Copies are numbered in two places, and only one shape is safe to widen.**
Kong and Redrum put the number in the middle (`Drum 7 Level`); Dr. Octo Rex
puts it at the end (`Select Loop 3`). Both are N interchangeable things and
both need the number spoken. `copy_number()` covers both;
`numbered_copy()` stays prefix-only because `build_prompt()` splits on that
shape to hoist a shared note over the copies. And a name ending in a digit is
not automatically a copy: the RV7000's `Soft Knob 1` is the Algorithm picker.
`NOTE_ALIASES` is the exemption — an alias exists precisely to say Reason's
spelling is not the real identity.

**Never show the model an example form this device cannot honour.** Found
2026-09-11 wiring Alligator, and it had been live on all six earlier devices.
`build_prompt()` listed `{"knob":"knob_N","target":"Tape"}` — the named-setting
form — on every device, including ones where no knob has settings at all. The
model copies the SHAPE of an example: "shuffle it" came back as target
`"Shuffle"`, "open gate 2" as `"Open"`, and twice as the literal `"Tape"`. A
word that is not in the measured table resolves to nothing, so the knob never
moves and the phrase looks broken to him — a silent dead end, not an error.
The fix is the guard, not better wording: emit that example and its rule
sentence only when some knob on this device actually lists settings, and
otherwise say outright that a word is never valid.
`tests/test_dial.py::test_the_named_setting_example_only_appears_where_a_picker
_exists` asserts BOTH directions — withhold it on a device with no picker,
keep it on one that has a picker, or "give me a plate" stops working.

**The surface is FULL as of Alligator: 48 of 48.** Every device wider than
that now needs an explicit cut decision from him before anything is written —
Alligator had 61 remotable controls and 13 had to go. Ask in clickable options
with the tradeoff named, the way the delay-and-phaser cut was put. And note
the asymmetry with Dr. Octo Rex: Rex lost its best moves because Reason does
not expose them at all, Alligator lost 13 purely to the CC budget. Say which
kind of loss it is — "mouse only" is true for Alligator's delay and false for
Rex's slices.

**A knob whose TARGET moves is not volatile; only a knob whose MEANING moves
is.** Rex's `Loop Transpose` and `Loop Level` act on whichever slot is
selected in the editor, but semitones are semitones in every slot, so the
measured table stays true and marking them volatile would refuse real units
for nothing. `LFO1 Amount` IS volatile — how much of *what* depends on
`LFO1 Dest`, and pitch wobble and pan wobble are not the same units. A
targeting caveat belongs in the device guide; a units caveat belongs in
`VOLATILE`.

**A device that numbers its copies needs the number spoken.** Kong's
parameters are `Drum 7 Level`, and Reason never reports what is loaded on a
pad — so "make the snare louder" has no answer and the model will invent one.
`dial_llm.numbered_copy()` / `said_the_number()` refuse the move instead.
Anything else built the same way (Redrum channels, an NN-XT zone) inherits the
rule for free.

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

`remote.get_item_state(idx)` returns `text_value`: on most devices, the
parameter exactly as Reason shows it ("30 ms", "-20.0 dB", "4.06:1"). That
kills the whole curve-modelling problem. The manual gives *ranges* but not
tapers.

**But `text_value` is NOT human-readable on every device. Check, per device.**
Measured 2026-09-11: the MClass Compressor returns "30 ms"; Scream 4 returns
a bare `"4"` where its own panel reads **Tape**, `"2"` where it reads **C**,
and `-64..63` on the Cut bands instead of dB. A feature built on labels is
silently inert on a device like that.

So after every new `calibrate.py` sweep, **look at what came back** before
building on it. If it is bare numbers, add the labels to
`docs/reason/value_names.json` — device → parameter → list in value order,
sourced from the Operation Manual and CITED there.
`dial_llm.apply_value_names()` folds them in inside `load_calibration()`, so
the panel, the model prompt and `resolve()` all get them from one place. It
rewrites only the LABEL; measured positions are never touched.

`reason_voice/calibrate.py` sweeps each knob 0–127 and records what Reason
displays at every position into `docs/reason/calibration.json`. Look values up
in that table; never compute them.

Do not generalise one knob to another. Attack happens to be linear
(`ms = floor(1 + pos*99/127)`, exact on all 33 observed points) — that says
**nothing** about Ratio or Release. Measure each one.

### 4b. A knob whose meaning changes under you

Two devices now have controls that are not one control at all:

| Device | Control | Meaning set by | Reachable? |
|---|---|---|---|
| Scream 4 | Parameter 1, Parameter 2 | Damage Type | yes (a mapped knob) |
| RV7000 | Soft Knob 1 (the algorithm picker) | Edit Mode | yes (a mapped knob) |
| RV7000 | Soft Knob 2–8 | Edit Mode **and** the algorithm | yes, both |
| Kong | Drum N DM Pitch/Decay/Level/Variable | the drum module in the pad | **NO** |
| Kong | Drum N FX1/FX2 P1, P2 | the effect in that slot | **NO** |

**"Reachable" is the whole distinction.** Kong never tells a control surface
which module is loaded — it is not a remotable parameter, so there is nothing
to read and nothing to set.

A table measured on the wrong page is worse than no table — every lookup after
it is confidently wrong. Three rules, all enforced in code:

1. `VOLATILE` in `calibrate.py` marks them; the entry records `measured_with`.
2. `resolve()` refuses **real units** on them forever (a measured "30 ms" is
   true for one algorithm only). It allows a **named setting only when the
   entry also carries `requires`** — i.e. the app can put the device into that
   context and read back that it arrived. With no reachable context (Kong) a
   measured name could be a leftover from a module he has since swapped, so
   those knobs are percentage-only for good.
3. `REQUIRES` (`calibrate.py`) records the context the table is only true in
   (`requires: {"Edit Mode": "Reverb"}`). Before moving such a knob the app
   reaches that context and **reads it back**; if it cannot get there it moves
   NOTHING and says so. `_reach()` in `server.py`.

**Buttons may take a value or may only step — probe, never assume.** Scream 4's
Body/Damage/Cut On/Off take an absolute value (proven at the machine
2026-09-11). The RV7000's Edit Mode is also a button and may only advance. So
`calibrate.probe()` writes three values (0, 127, 127) before any sweep: if the
repeated write changes the reading, it is a toggle, and it is NOT swept — 128
writes to a toggle leave his patch somewhere random and "put it back where it
started" means nothing. `_reach()` covers both: direct write first, then press
round one full cycle, checking every time.

**When your own labels and Reason disagree, Reason wins.** Labels in
`value_names.json` are read out of the manual; a live `text_value` is what the
device is actually showing. Both `_showing()` and `calibrate.put()` fall back
to the table only when Reason reports a bare number.

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
