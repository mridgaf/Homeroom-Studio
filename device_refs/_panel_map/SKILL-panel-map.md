---
name: panel-map
description: Map a Reason 12 device's front and back panels into the Panel Map (codes like SCR4-F-K03, labeled pictures, exact Reason names, MIDI slots, jack names, positions), or use the map to find, check or cable a control. Use when asked to map a device, continue the Panel Map plan, find where a knob/button/jack is, or make or check a cable in Reason.
---

# Panel Map

A coded map of every control on every Reason device, front and back, kept in
`device_refs/_panel_map/`. It's for Claude and Hermes; the owner never has to read it.
Read `PANEL-MAP.md` (rules + finished devices) and `PLAN.md` (phases) there first.
`scream-4.json` + its two pictures are the finished example. Match it.

## Hard rules
- Work ONLY in a new blank test song (File > New). Never touch his real songs. Never save.
- Every name comes from Reason itself (tooltips, cable menus), `docs/reason/remote-vocab.json`,
  the remotemap, or the manual (`~/.reason_voice/reason12_manual/full_chapters/`). Never from memory.
- The code is a nickname. Reason only accepts its own exact names, and a wrong one fails without warning.
- A device counts as done only when EVERY position has been checked in Reason (step 6).
- Undo any test change you make (cables: right-click > Disconnect; fold: click again).

## Codes
`DEVICE-SIDE-TYPE##`. DEVICE = short unique prefix (SCR4, ECHO, RV7K...). Check PANEL-MAP.md so it isn't
already used. SIDE: F/B. TYPE: K knob, B button/switch, S slider, J jack, D display.
Number left-to-right, top-to-bottom. Never reuse or renumber a published code. Add new ones at the end.

## Steps for one device
1. **Set up.** Reason granted for computer use, full-screen control on. File > New. Create > (category) > device.
   Click the Rack panel's detach arrow so the rack gets its own window. Click empty space, press Tab to flip.
2. **Pictures.** Full screenshot, then zoom on the device panel (front and back). Save as
   `<device>_front_raw.jpg` / `<device>_back_raw.jpg`. If the panel has views (tabs, pages,
   modules, folded state), take one picture per view and name the view in the codes' rows.
3. **Codes + boxes.** List every control. Write centre + half-size in picture pixels. Draw boxes
   and codes (copy the Scream 4 `build.py` approach: magenta box, yellow-on-black tag; move tags
   that overlap). Look at the result and fix any tag that covers another.
4. **Names.**
   - Remote names + knob slots: the device's `Scope` block in `remote/ReasonVoice.remotemap`.
     CC = 29 + slot; feedback CC = 77 + slot. Items in remote-vocab.json but not in our map are marked "not in our map".
   - Jack names: hover each jack (step 6) or right-click a jack of the opposite kind on another device and read this
     device's submenu.
5. **Manual check.** Read the device's chapter. Every "what it does" line must agree with it.
6. **Check every position in Reason.** Use `tools/to_screen.py` (match the panel's top-left and
   bottom-right corner screws in picture and on screen) to get each screen point, then hover it for 1.5 s and zoom:
   - Knobs/buttons/switches: the tooltip shows the exact name (+ value). It must match the row.
   - Sliders: hover the HANDLE (it moves with the value).
   - Jacks: empty = its name; cabled = "Connected to <device>: <jack>".
   - Back trims: "<input name>: <value>".
   - No tooltip (displays, fold triangle): check by eye, or by a click you undo.
   Record what Reason showed in `checked_<date>` for every row.
7. **Save + log.** Write `<device>.json`, both labeled pictures, and a section in PANEL-MAP.md. Add one line
   to the Devices table. Add a DECISIONS.md entry and update the hermes house project doc.

## Making a cable
Right-click the source jack > device (by rack name) > jack. Prove it: hover the jack
("Connected to ...") or reopen the menu (check marks + "Scroll to Connected Device").
`*` = jack already used. Grey = not allowed. Remove a cable with right-click > Disconnect.

## Traps found so far
- Keys and the Options menu only reach Reason when it's frontmost (full-screen control). Background clicks work, keys don't.
- A submenu stays open after Escape. Click empty black space beside the rack instead.
- Turning a map position into a screen point only holds while the rack doesn't scroll or change zoom. Take a new screenshot before each batch.

## Added 2026-10-07 (batch D effects session)
- **Hover trick:** jump the pointer straight onto a control and Reason often shows NO tooltip. Do two `mouse_move`s: first 4-5 px up-left, then onto the control, then wait 1.3 s. That got tooltips on nearly everything. Still none on lights, arrows, display buttons, some faders: record "no tooltip", never invent a name.
- **Zoom region** must be 320x60 or taller, starting at the pointer: tooltips near an edge get cut off ("Connected to Mix Channel: From Insert FX..."). Cabled-jack tooltips name the PARTNER jack, which also proves the partner's own jack name.
- **Screen mapping:** screen = panel_left + raw_x * scale (scale ~0.61-0.64 at this zoom). Measure from a fresh screenshot of that panel each time; Tab and scrolling shift it. Re-aim if a hover lands on the wrong control.
- **Stepped Remote items** (amp/cab model lights, SCALE MEMORY slots, preset buttons): every button shows the same tooltip (the Remote name). Put the knob slot on the first row only.
- **Tools:** write `tools/gen_<device>.py` (spec + check text per label), then `tools/finish_device.py <slug> "<status>"` builds the pictures and stamps `checked_` on every row; it refuses if any row has no check text. Extra views: `tools/specs/<slug>--<view>.json` + a `views` block in `tools/checks/<slug>.json`. Copy `gen_alligator.py` as the pattern.
- **name_check:** device name in the JSON must be the short vocab name ("Sweeper", not "Sweeper Modulation Effect"). Remotemap scopes with `se.propellerheads.` need a temp copy with that prefix stripped (`sed 's/\tse\.propellerheads\./\t/'`); never edit the real remotemap.
- **Never rewrite finished panel JSONs with json.dump:** it reformats ~20k lines. Add fields only to new files.
- `tools/panel_map_md.py` skips a device only if its picture row already exists (fixed: prefix "SYNC" collided with the word SYNC).
- Pillow is installed in `.venv` (needed by build_device.py).
- Remote has only 48 knob slots per device; controls past 48 get a name but slot None ("NOSLOT" note).
