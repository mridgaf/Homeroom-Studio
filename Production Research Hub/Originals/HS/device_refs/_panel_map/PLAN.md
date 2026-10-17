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
