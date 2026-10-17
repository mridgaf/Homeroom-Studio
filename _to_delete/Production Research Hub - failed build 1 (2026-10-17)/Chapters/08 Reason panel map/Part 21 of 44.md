# Chapter 08: Reason panel map
## Part 21 of 44

_Front and back panel maps of Reason devices: every knob, button and jack, by device._

**In this part:**
- PANEL-MAP.md (piece 21 of 21) — Panel Map — every knob, button, slider and jack, with a code
- INVENTORY.md — Panel Map inventory (Phase 2, 2026-10-03)
- PLAN.md — Panel Map — full build plan
- SKILL-panel-map.md — Panel Map
- RESUME.md — Batch A — FINISHED 2026-10-07 (17/17; nothing left to resume)
- KNOB-CHECK-TRIAL.md — Knob-check trial — Sweeper, 2026-10-07 (result: PARTLY WORKS)
- RESUME.md — Batch D (other stock effects) — PICTURES DONE 2026-10-07 (10/10 devices, front + back raw). Labeling/hover checks NOT started.
- SWEEPER-HOVER.md — Sweeper front, hover results 2026-10-07 (Phaser mode, Envelope view; song "untitled 2")

(Next: Part 22 of 44)


=====================================================
SOURCE FILE: PANEL-MAP.md (piece 21 of 21)
ORIGINAL LOCATION: HS:device_refs/_panel_map/PANEL-MAP.md
=====================================================

## Efektor Silencer Noise Gate (Kuassa) — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SILN-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip (fold arrow); checked by eye |
| SILN-F-B02 | BYPASS / ON / OFF | 3-way device switch | — | — | click only | tooltip "Enabled: On" |
| SILN-F-K01 | THRESHOLD | Gate threshold | — | — | click only | tooltip "Threshold: -oo dB" |
| SILN-F-K02 | ATTACK | Gate attack time | — | — | click only | tooltip "Attack: 2 ms" |
| SILN-F-K03 | DECAY | Gate decay time | — | — | click only | tooltip "Decay: 100 ms" |
| SILN-F-B04 | DUAL MONO | Dual mono on/off | — | — | click only | tooltip "Dual Mono On/Off" |
| SILN-F-B03 | Power button (red) | On / Bypass button (red power symbol) | — | — | click only | tooltip "On / Bypass" |
| SILN-F-D02 | SILENCER 1 tape | Device name tape | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| SILN-F-D01 | EFEKTOR SILENCER logo | Logo (no tooltip) | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| SILN-F-D03 | gate light grille | Small light grille next to the power button (no tooltip) | — | — | click only | no tooltip in Reason (hovered 1.3 s) |

## Efektor Silencer Noise Gate (Kuassa) — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SILN-B-J01 | Input L | Audio input, left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Chorus 1: Main Out Left" |
| SILN-B-J02 | Input R | Audio input, right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Chorus 1: Main Out Right" |
| SILN-B-J05 | Output L | Audio output, left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to RE 181 MSC 1: Audio In Left" |
| SILN-B-J06 | Output R | Audio output, right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to RE 181 MSC 1: Audio In Right" |
| SILN-B-J03 | (small jacks 1) | Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip) | — | — | cable: right-click jack > device > jack name | no tooltip in Reason (hovered 1.3 s) |
| SILN-B-J04 | (small jacks 2) | Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip) | — | — | cable: right-click jack > device > jack name | no tooltip in Reason (hovered 1.3 s) |
| SILN-B-J07 | (small jacks 3) | Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip) | — | — | cable: right-click jack > device > jack name | no tooltip in Reason (hovered 1.3 s) |
| SILN-B-J08 | (small jacks 4) | Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip) | — | — | cable: right-click jack > device > jack name | no tooltip in Reason (hovered 1.3 s) |
| SILN-B-D01 | SILENCER 1 tape (back) | Device name tape on the back | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s) |
| SILN-B-D02 | Power area (drawn) | Power socket (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s) |

## Where each fact came from
- Pictures: screenshots of John's Reason 12.7, in a blank test song made from his template.
- Remote names: remote/ReasonVoice.remotemap (Scream 4 scope) and docs/reason/remote-vocab.json.
- Jack and control names: Reason's own tooltips and cable menus.
- What each control does: Reason 12.7 manual, chapter 51 (~/.reason_voice/reason12_manual/full_chapters/51-scream-4-sound-destruction-unit.txt). All 38 rows agree with it.
- Positions: measured from the picture, then every one hover-tested in Reason (2026-10-03).

## Not in our Remote map (Reason has them, our map doesn't send them)
- Select Previous/Next Patch (SCR4-F-B03/B09). "Select Patch Delta" is a Remote item with no control of its own on the panel (it steps patches by an amount), so it has no code. The trims (SCR4-B-K01–K04) have no Remote item at all.

## Still open
- Hermes doesn't have a copy yet (Phase 5).

=====================================================
SOURCE FILE: INVENTORY.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/INVENTORY.md
=====================================================

# Panel Map inventory (Phase 2, 2026-10-03)

Source of truth for what is INSTALLED: Reason 12.7's own Create menus, read 2026-10-03 (installed.csv).
inventory.csv = every device Reason has a Remote map for (148), most of which he does NOT own. Use it only to look up names.

## What he has
| Kind | Count | Notes |
|---|---|---|
| Reason-made (stock) | 63 | 19 instruments, 29 effects, 10 utilities, 5 players |
| Rack Extensions from other makers | 15 | 8 utilities, 7 effects (AirRaid, Groovy Melon, pongasoft, Red Rock Sound, Rob Papen, Robotic Bean, kiloHearts, Kuassa, Softube, ThatMusicCompany) |
| VST plugins | 15 | 5 instruments, 10 effects. Their controls live in a separate plugin window, not on a rack panel. Not part of the rack map unless John says so. |
| Always in every song | — | Hardware Interface, Master Section, Main Mixer. Not in the Create menus; map them too. |

## Name joins (menu name -> Reason's Remote name)
- Exact or near-exact for most. Hand joins (wording differs): RV7000 MkII Reverb -> RV7000 Advanced Reverb, Dr. Octo Rex -> Dr.REX Loop Player, Channel Dynamics/EQ -> ChannelDynamics/ChannelEQ, Master Bus Compressor -> MasterCompressor, Alligator Filter Gate -> Alligator, Pulveriser Demolition -> Pulveriser.
- PROBABLE, confirm in Reason while mapping: Scales & Chords -> ScalesAndChords, Dual Arpeggio -> Arpeggio, Softube Amp -> ReasonAmp, Softube Bass Amp -> ReasonBassAmp, Mix Channel -> Reason Main Mixer Channel.
- No Remote map found: Audio Track, Drum Sequencer, all 15 third-party Rack Extensions (no Remote map for them in Reason's files, so tooltips are the only name source).

## Settled from the manual
- Ch.62 Half-Rack Effects covers all 9: CF-101, COMP-01, D-11, DDL-1, ECF-42, PEQ-2, PH-90, RV-7, UN-16 (each named as a heading in the chapter text).
- Ch.55 covers Softube Amp + Softube Bass Amp (chapter text).
- device_refs/guitar-amps.md is about his physical amps (hardware), like audiobox-96, launchkey-mk3, samson-servo-300, yamaha-*.

## Proposed batch order (counts)
- A. Simple fixed effects (18): Half-rack 9, MClass 4, The Echo, RV7000, Channel EQ, Channel Dynamics, Master Bus Compressor.
- B. Other stock effects (10): Alligator, Audiomatic, BV512, Neptune, Pulveriser, Quartet, Softube Amp, Softube Bass Amp, Sweeper, Synchronous.
- C. Mixing & utilities (13): Mix Channel, Audio Track, Mixer 14:2, Line Mixer 6:2, Spider Audio, Spider CV, Matrix, Pulsar, RPG-8, Combinator (outer panel), Hardware Interface, Master Section, Main Mixer.
- D. Instruments (19) — several with views (Kong pads, Thor, Europa, Mimic, Grain, Redrum).
- E. Players (5).
- F. Third-party Rack Extensions (15).

=====================================================
SOURCE FILE: PLAN.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/PLAN.md
=====================================================

# Panel Map — full build plan

Goal: every Reason device John uses gets a coded front + back map (pictures, codes, exact Reason names, MIDI slots, cable-menu jack names, positions), so Claude and Hermes can find, turn, click and cable anything. For Claude and Hermes only; John never has to read it.

Proven so far (2026-10-02): Scream 4 mapped (37 controls). One cable made by map position alone and confirmed by Reason's check marks.

## House rules for every phase
- Work only in a NEW blank test song. Never touch his real songs. Never save over anything.
- Every fact comes from a source: Reason's own menus, remote-vocab.json, the remotemap, or the manual. Never from memory.
- A device is "done" only when its click-test passes (step 4.6 below).
- Log each finished device in PANEL-MAP.md and DECISIONS.md.

## Phase 0 — Finish the standard (Scream 4)
1. Click-test all 37 positions (jacks by right-click; knobs/buttons: find a method that proves the spot without leaving any change behind).
2. Read Auto CV Output's exact menu name.
3. Check the patch arrow direction.
4. Check the table against the Reason 12 manual (needs ~/.hermes opened to this session).
5. Write a "panel-map" skill: the exact same steps for every device, so any session does it the same way.

## Phase 1 — Build helpers (so most of the work is done by scripts, not eyes)
1. Position helper: map position -> screen point, using the panel's corner screws. (Done by hand once; make it a script.)
2. Jack harvester: right-click each jack, read the menu text through the Mac accessibility system. That gives Reason's exact jack names with no picture-reading.
3. Name checker: every Remote item in remote-vocab.json for that device has a code, and no name is misspelled.
4. Idea to test (not promised): find jacks automatically by matching their look (every jack looks the same), so only knobs/buttons need placing by eye.

## Phase 2 — Inventory
1. List every device he has: stock (about 55 guides in device_refs) plus Rack Extensions (Create menus show about 14 other makers in Effects alone; Instruments, Utilities and Players not counted yet).
2. Mark which panels change (Kong modules, Combinator, Thor, Europa, Mimic and others) — those need one picture per view.
3. Order by how often he uses them (from his songs) and how hard they are.

## Phase 3 — Batches (same steps every device)
- Batch A: simple fixed effects (Echo, RV7000, DDL-1, CF-101, PH-90, MClass set, etc.)
- Batch B: mixer, Mix Channel, Combinator outer panel, utilities (Spider, Matrix, RPG-8)
- Batch C: instruments with one view (SubTractor, Malström, NN-19, ID8, Dr. Octo Rex...)
- Batch D: devices with changing panels (Kong, Thor, Europa, Mimic, Combinator custom panels, Redrum)
- Batch E: Rack Extensions, in his order of use

## Phase 4 — Per-device steps (every device, every time)
1. New blank song, add the device.
2. Front + back pictures at the same zoom.
3. Place codes + boxes. Save labeled pictures.
4. Fill names: Remote names from files, jack names from the harvester.
5. Run the name checker.
6. Click-test: every jack by right-click. Knobs/buttons: method decided in Phase 0 (hover tooltip, if Reason shows one — not verified yet; or a nudge read back through the Remote bridge, then put back).
7. Save + log.

## Phase 5 — Hermes
1. Copy the maps into Hermes's notes.
2. Re-run the Round 1 picture questions with and without the map; compare scores.
3. Cable test for Hermes (needs its computer control turned on and John's yes).

## Phase 6 — Upkeep
- Re-check a device's map when Reason updates or he buys a new Rack Extension.

## Where John is needed
- Mac permission prompts (screen control, folder access).
- A yes before Hermes gets computer control.
- Nothing else.

=====================================================
SOURCE FILE: SKILL-panel-map.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/SKILL-panel-map.md
=====================================================

---
name: panel-map
description: Map a Reason 12 device's front and back panels into the Panel Map (codes like SCR4-F-K03, labeled pictures, exact Reason names, MIDI slots, jack names, positions), or use the map to find, check or cable a control. Use when asked to map a device, continue the Panel Map plan, find where a knob/button/jack is, or make or check a cable in Reason.
---

# Panel Map

A coded map of every control on every Reason device, front and back, kept in
`device_refs/_panel_map/`. It's for Claude and Hermes; the owner never has to read it.
Read `chapters/00-INDEX.md` first (rules, device table, links). Then open ONLY the chapter for the device you need (`chapters/<device>.md`). `PLAN.md` has the phases. The old `PANEL-MAP.md` is now a pointer; do not edit it.
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
7. **Save + log.** Write `<device>.json`, both labeled pictures, and a chapter file `chapters/<device>.md` (made by `tools/panel_map_md.py`) and one line in `chapters/00-INDEX.md`. Add one line
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

=====================================================
SOURCE FILE: RESUME.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/_captures_batchA/RESUME.md
=====================================================

# Batch A — FINISHED 2026-10-07 (17/17; nothing left to resume)

## Done
- Raw front + back pictures for 14 devices, taken in test song "untitled 4" (unsaved):
  CF-101, COMP-01, D-11, DDL-1, ECF-42, PEQ-2, PH-90, RV-7, UN-16,
  MClass Compressor, MClass Equalizer, MClass Stereo Imager, MClass Maximizer, RV7000 MkII.
- RV7000: main panel + back + Remote Programmer in Reverb edit mode only (EQ and Gate edit modes not captured; the programmer is a multi-view section).
- Backs were shot with Reduce Cable Clutter ON (K key) and nothing selected, so other devices' cables are see-through.

## Not done
- Channel EQ, Channel Dynamics, Master Bus Compressor: not created or captured yet.
- No labeling yet (helpers), no hover checks, nothing added to PANEL-MAP.md.
- Hover checks need the devices still in "untitled 4". If that song is closed, re-create the devices in a new test song first; positions are then found again from a fresh screenshot.

## Reason state left behind
- "untitled 4" open and unsaved, with all 15 devices above.
- Reduce Cable Clutter is ON (Options menu / K key). Switch it back off when Batch A is finished.

## Inputs for helpers (also in Claude's workspace, gone when the session ends)
- Remote scopes: remote/ReasonVoice.remotemap. Names: docs/reason/remote-vocab.json.
- Manual chapters: ~/.reason_voice/reason12_manual/full_chapters/ 53, 57, 58, 59, 61, 62.

=====================================================
SOURCE FILE: KNOB-CHECK-TRIAL.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/_captures_batchD/KNOB-CHECK-TRIAL.md
=====================================================

# Knob-check trial — Sweeper, 2026-10-07 (result: PARTLY WORKS)

Method: lock the surface to the device (right-click blank ear > "Lock ReasonVoice ReasonVoice 2 to This Device",
read the tick first) while a listener runs -> Reason announces EVERY Remote knob with its current value.
Then tools/panel_sweep.py moves each knob (CC 30+k-1), screenshots before/after, diffs, puts it back.

## What worked
- Lock announcement = all 33 Sweeper Remote names + slots + current values in one shot (Bandwidth "78.9 %" matched the hover tooltip).
- Sweep located ~20 of 33 on the panel on the first pass (Bandwidth, Frequency, Feedback, Dry/Wet, Spread, Volume, Polarity, Mute Dry,
  Stages, LFO->Freq, MOD->Freq, Rate Mod, LFO rate/wave/sync, Env loop/rate, Beat sync, Bypass). Positions are in the MCP screenshot frame
  (1372x891 = whole built-in display); screencapture and the MCP frame share it. Rack must not be scrolled during the sweep.
- Knobs that change the VIEW (Type, ModType, Filter Type) show up as huge diffs -> tells you which extra pictures a device needs.

## What did not work / still needs hover
- ~13 knobs gave only noise: controls hidden in the current mode (Filter/Audio Follower items) AND at least two that should be visible
  (LFO Amp Mod, Env Amp Mod = LFO/MOD->Volume?) — unexplained, check by hover.
- Header patch-name display flickers on every change: ignore clusters in the header band.
- Restore is approximate: continuous knobs land +-1 step (LFO 0.145->0.140 Hz, Loop 0.631->0.614 s). Stages needed a manual nudge.
- Does NOT cover jacks (no CC) or buttons without a Remote item: those stay hover / right-click.
- Side effect: first (unlocked) test moved Neptune's Catch Zone Size (surface was still locked to Neptune). Test song only.
- Pillow does not build on Python 3.9 here; script uses numpy + sips + screencapture instead.

## Verdict
Use it to find positions and confirm names/values for knobs (saves most of the hovering). Still hover: jacks, switches, anything the sweep misses.

=====================================================
SOURCE FILE: RESUME.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/_captures_batchD/RESUME.md
=====================================================

# Batch D (other stock effects) — PICTURES DONE 2026-10-07 (10/10 devices, front + back raw). Labeling/hover checks NOT started.

## Devices + notes
- alligator (tall; front has ~55 controls), audiomatic, bv512, neptune, pulveriser, quartet, softube-amp, softube-bass-amp, sweeper, synchronous.
- Multi-view gaps: Quartet (4 Ensemble modes, shot in BBD), Sweeper (Phaser/Flanger/Filter modes + Audio Follower view; shot in Phaser + Envelope), Synchronous (3 tracks, shot as-is).
- Neptune has no Remote map; Softube Amp/Bass Amp -> ReasonAmp / ReasonBassAmp (probable, confirm).

## Not done
- No labeling (helpers), no hover checks (needs devices still in test song "untitled 2"), nothing in PANEL-MAP.md.
- If "untitled 2" is closed: re-create the 10 devices in a new test song, then positions come from a fresh screenshot.

## Reason state
- "untitled 2" open, unsaved, 25+ devices. Reduce Cable Clutter switched back OFF at the end (2026-10-07). Rack left on front view.

=====================================================
SOURCE FILE: SWEEPER-HOVER.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/_captures_batchD/SWEEPER-HOVER.md
=====================================================

# Sweeper front, hover results 2026-10-07 (Phaser mode, Envelope view; song "untitled 2")
Screen point = (90+(x-42)*0.618, 449+(y-82)*0.624) from sweeper_front_raw.jpg pixel (x,y). Rack must not be scrolled.
Seen in Reason (tooltip text = Remote name unless noted):
- Bypass switch (raw 95,45): "Enabled: On"
- Preset display (785,40): "Basic Phasing" (name shown; tooltip cut off)
- Patch arrows (957,40): "Select previous patch" (hover on lower arrow area)
- PHASER / FLANGER / FILTER buttons (670/786/901,112): "Effect Type"  -> Remote "Type"
- LFO>Freq knob (206,201): "LFO Freq Mod: 84.1 %"
- MOD>Freq knob (206,312): "Env Freq Mod: 0.0 %"
- Frequency (453,252): "Freq: 790.0 Hz" (cut off, read as seen)
- Bandwidth (601,203): "Bandwidth: 79.5 %"
- Feedback (601,313): "Feedback: 83.9 %"
- Polarity (881,214): "Polarity"
- Mute Dry (881,294): "Mute Dry"
- Spread (1047,203): "Spread: 20.5 %"
- Dry/Wet (1047,313): "Dry-Wet: 100.0 %"  (hover says Dry-Wet, Remote name is DryWet)
- Volume (1171,253): "Volume: -6.4 dB"
- LFO>Volume (1371,201): "LFO Amp Mod: 0.0 %"
- MOD>Volume (1371,312): "Env Amp Mod: 0.0 %"
- LFO rate knob (245,490): "LFO Rate: 15.0 %"
- Rate Mod knob (337,449): "Rate Mod: 0.0 %"
- Envelope / Audio Follower tabs (655/855,403): "Modulator Type"
- Env rate knob (1202,488): "Env Rate: 50.4 %"
NO tooltip after 2.5 s and a nudged approach (record as seen, name unproven by hover):
- Stages display (745,250) (tooltip cut off in zoom, not read), LFO wave arrows (152,442), LFO SYNC (247,537),
  LOOP (1204,406), Env SYNC (1202,537), Threshold knob (1372,492), Stereo selector (1385,60).
NOT DONE: Flanger and Filter views, Audio Follower view, Audio Trig, back panel jacks, labeled pictures, sweeper.json.

=== END OF PART ===
