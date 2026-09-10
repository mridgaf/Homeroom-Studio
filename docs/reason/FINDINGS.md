# What Reason will let us control, and how — researched 2026-09-10

Read this before proposing anything about controlling Reason from the app. It
exists so nobody re-derives it, and so nobody falls back into the plan in
`reason_voice/HANDOFF.md`, which is superseded (see the end).

## Where the facts came from

| Source | On disk | Vintage |
|---|---|---|
| **Reason 12's own Remote data** — 182 factory `.remotemap` files | `/Applications/Reason 12.app/Contents/Resources/Remote/` | **current (12.7.4d3)** |
| Reason 7 Operation Manual + Help Files | `/Applications/Reason/Documentation/` | May 2013 |
| MIDI Implementation Chart (CC→parameter) | same folder | May 2013 |

`tools/reason_docs.py` extracts only the Help Files. The three smaller PDFs —
**MIDI Implementation Chart**, Key Commands, Installation Manual — have no
Help-File equivalent and are NOT in `reason_docs/`. Read them straight from
`/Applications/Reason/Documentation/English/` when needed.

`/Applications/Reason` is the **old Reason 7 install**, kept for its
documentation. Reason 12 ships no manual — its Help menu goes to the website.

**Use the 2013 manual to understand what a knob *does*. Use the Reason 12 factory
maps for what a parameter is *called*.** Never the other way round: the 2013 docs
predate Mimic, Europa, Quartet, Objekt and every Player device.

## The vocabulary

`tools/reason_vocab.py` parses those 182 files into
`docs/reason/remote-vocab.json`:

**148 devices, 11,503 parameters**, spelled exactly as Reason spells them.

```
$ python3 tools/reason_vocab.py --device "MClass Compressor"
MClass Compressor  (Propellerheads, 14 parameters)
    Adapt / Attack / Device Name / Enabled / Gain Meter / Input Gain /
    Output Gain / Peak Meter / Ratio / Release / Sidechain Active /
    Sidechain Solo / Soft Knee / Threshold
```

Re-run it after a Reason update — it's a snapshot, not a fixed truth.

**It is a lower bound, not a complete list.** It holds what factory control
surfaces happen to map, which is not everything a device exposes. Mimic proves
it: `Voice Formant 1` is present but 2–8 are absent, and `Filter KBD 1` is
missing entirely. **Absence from this file does not prove a parameter doesn't
exist** — only that no factory surface mapped it. Check the device in Reason
before concluding anything is missing.

**Exact spelling is the whole game.** A remotable item name that is slightly wrong
fails *silently*: Reason doesn't complain, the knob just never moves. Every name we
use gets copied from this file. None get typed from memory.

Not every entry in a `.remotemap` is a parameter — the same column also carries text
constants (`"Thresh"`), numeric constants, and mapping-variation assignments
(`Group=3`, `Shift=ShiftDown`). Those drive the *surface's* display, not the rack.
The parser filters them; `tests/test_reason_vocab.py` pins that.

## Three ways into Reason, worst to best

### 3. Remote Override — what HANDOFF.md proposed. Don't build on it.
Right-click any parameter → "Edit Remote Override Mapping" → learn a control.
Reaches anything. But the manual is explicit: *"the overrides will be saved with the
current song, but won't be there if you create a new song."* Every new song means
doing it all again. Fine as a manual convenience, wrong as a foundation.

### 2. Standard mapping — free, and already working
*"Reason parameters are standard-mapped to supported control surfaces. There is
nothing the user needs to set up."*

`DefaultMaps/Novation/Launchkey MK3.remotemap` is a factory file, so the owner's
Launchkey MK3 49 is natively supported. Its knobs already control whichever device
has Master Keyboard Input — Knob 5 already *is* the MClass Compressor's Attack. No
setup, every song, today. He may not know this.

Related and unused: `Cmd+Option+1..9` switches *mapping variation*, so the same 8
knobs reach a different set of parameters. And a surface can be **locked** to one
device (Options → Surface Locking), including the Main Mixer and the ReGroove Mixer,
so it stops following the sequencer. Both are saved with the song.

### 1. Our own control surface — the one to build
This is what `remote/` already is. The app sends a CC on IAC Bus 1; the codec turns
it into a named surface item; the `.remotemap` binds that item to a named parameter,
per device scope. It's exactly how the Launchkey's factory map works.

Today it carries ten buttons (patch next/prev, transport, track, undo/redo). A knob
is the same mechanism with a value instead of a press:

```
Scope   Propellerheads   MClass Compressor
Map     Knob 1    Threshold
Map     Knob 5    Attack
```

No learning. No per-song setup. Correct for Reason 12 because the names are copied
from Reason 12. And `README.md:68` already said this was possible — it was just
never followed up.

**The codec and map must stay in sync with `reason_voice/reason_control.py`, and
Reason only loads codecs at launch (full Cmd+Q restart).** See the
`reason-remote-bridge` skill; `tests/test_remote_bridge.py` guards the sync.

## Two more channels, noted and not used

- **External Control Bus** (Preferences → Advanced): 4 buses × 16 channels = 64
  devices addressed directly by raw MIDI CC, bypassing keyboard routing. Needs its
  own port (Bus 1 is taken by our surface), and the CC numbers come from the *2013*
  chart. Real, but it's the Reason 7 route. Keep as a fallback.
- **Keyboard Control** (Options → Enable Keyboard Control): computer keys →
  parameters, no MIDI at all. Limited to min/max toggling, so it suits switches, not
  knobs.

## What is still not proven

**Nothing here has moved a knob yet.** The next step is one device section in the
map, a Cmd+Q restart, one CC, and watching Attack move on screen. Until that
happens, this is a well-sourced plan and not a working feature.

Also unverified: whether Rack Extension scopes (`se.propellerheads.*`) behave the
same as built-in device scopes in a hand-written map. The factory maps use both
identically, which is good evidence, not proof.

## Superseded

`reason_voice/HANDOFF.md` build steps 4–7 — the Remote Override dial plan — and the
"8 generic dials on CC 30–37" idea from 2026-09-10. Both replaced by the route above.
The brief's other conclusions still stand, including that cable/patch routing cannot
be automated at all.

One correction to that brief: it states Mimic has no sidechain input and implies it
can't be reached. The first half is true. The second isn't — `se.propellerheads.Mimic`
is in the factory maps with 8 slots × 63 parameters each (489 items in total).
