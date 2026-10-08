# Batch E (instruments), started 2026-10-08
Order: Kong, Redrum, Dr.REX, Mimic, Thor, Grain, Europa, Malstrom, Humana, NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8.
DONE: Kong 256, Redrum 330, Dr.REX 147, Mimic 174 rows (tools/gen_*.py, post_kong/post_mimic). name_check PASS (Mimic needs stripped remotemap copy: sed s/\tse\.propellerheads\./\t/). NEXT: Thor, Grain, Europa, Malstrom, Humana, NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8.
Method that works: Reason frontmost, full-screen control; hover each control (two mouse_moves, 1.2 s, zoom 320x60 below-right at scale 0.3); record text; write tools/gen_<dev>.py; run `.venv/bin/python tools/finish_device.py <slug> "<status>"`; name_check (no prefix strip needed for Propellerheads-scope devices); `python3 tools/panel_map_md.py "<slug>|<Title>"`.
Tall devices: scroll the rack 1 tick = top vs bottom; use separate views (specs/<slug>--<view>.json, front_offsets 100/200).
Crowded grids: re-crop upscaled 3x and use label mode "in" (see Kong padside view).
Reason state: "untitled 2" open, unsaved; Kong created after Quartet; Reduce Cable Clutter (K) is ON, press K at the end.

## STOPPED 2026-10-08 (usage limit)
Thor: IN PROGRESS. thor_front_raw.jpg saved; thor_pts.json (266 points, picture px; screen = 72+px/1.2887, 62+py/1.2887 with Programmer open, rack scrolled so Thor top at screen y~62); thor_notes.txt has first 33 results only. Points 33-66 were hovered but results NOT recorded (tooltips: Osc1 AM From Osc2, Osc1 Kbd/Oct/Semi/Tune, Osc1 Detune Amt: 37, Osc 1 Multi Wave, Osc2 Kbd/Oct/Semi/Tune, Osc2 Pos, Osc2 Wavetable Smooth X fade, Osc2 Sync To Osc1, Osc3 Sync To Osc1, Osc3 Sync BW, Master Level -19.1 dB). Thor back panel not photographed. Redo from point 33.
Done and finished: Kong, Redrum, Dr.REX, Mimic. Left: Thor, Grain, Europa, Malstrom, Humana, NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8.
Reason: test song "untitled 2" open, unsaved; Reduce Cable Clutter (K) left ON.
Thor FRONT hover DONE (matrix sampled only). Next: Thor back panel picture (Tab, K), then gen_thor.py + finish_device.py thor
Thor BACK pics saved: thor_back_raw.jpg (top, zoom region 60,60-1060,810, 1269x952), thor_back_bottom_raw.jpg (region 60,580-1060,720 after scroll down 3, 1568x220). Back hovers next.
Thor back hover: top-left + seq done; next modout + audio in/out (screen x 629/690/800/941, y 112/138/165/192 with rack scrolled so Thor header 'Sequencer Control' at y~82)
Thor BACK hover DONE (thor_back_notes.txt). Next: write tools/gen_thor.py, finish_device.py thor
Thor: Filter 2 enabled (Low Pass Ladder) in test song for view capture; RESET to Bypass at end

## 2026-10-08 later: THOR DONE (partial status): thor.json 329 rows, name_check PASS, 2 labeled pics + Filter 2 view. Filter 2 reset to Bypass. NEXT: Grain, Europa, Malstrom, Humana, NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8. Reduce Cable Clutter (K) still ON; Reason on FRONT view, Thor top at screen y~62 (rack scrolled).
Thor not mapped: Programmer panel (step sequencer, edit modes), matrix rows 2-7/9-11/13 hovered only by pattern.

## 2026-10-08 GRAIN started (created below Thor, patch "Vergon 6", default). grain_front_top_raw.jpg = zoom of screen [70,62,1030,812] (1232x962; screen = 70+px/1.2833, 62+py/1.2833) with Grain top at screen y~62. Grain is tall: next capture scrolled down for matrix/effects (bottom half), then back. Hover results -> grain_notes.txt (key|text).
Grain hovers done through xfade; coordinates = screen coords in full screenshot (Grain top y=62). Next: pitch row, oscillator, filter, amp, env/lfo, effects, matrix
Grain top half hovered through LFO. Next: scroll down, effects row + effect panels, matrix, wheels, then back
grain_front_bottom_raw.jpg = zoom screen [70,100,1030,442] after scrolling down 8 ticks (1568x559; screen = 70+px/1.6333, 100+py/1.6333). Grain bottom edge at screen y~442
Grain: matrix row 1 (Env 3) done; columns: k1=Dest1 Amt, k2=Dest2 Amt, k3=Scale Amt (tooltips 'ModN DestM Amt'). Next: effects tabs + compressor + other effect panels, then back panel
Grain: effects row+compressor done. Next: click each fx tab (PHSR/DIST/EQ/DLY/REV) at screen y 286: x 783,822,861,938,977, capture + hover knobs; then back panel
Grain fx panels raw: grain_fx_{phsr,dist,eq,dly,rev}_raw.jpg (458x282 = zoom screen [740,275,1000,435] x1.7615). Currently REV tab selected; set back to COMP (861?? no: COMP tab x=900,y=286) at end.
Grain fx hovered: REV, DLY, EQ done. Next DIST (tab x=822) and PHSR (x=783) panels (positions in RESUME context: DIST slider 766,406 drive 854,374 tone 906,373 amt 951,374; PHSR slider 819,391 depth 858,355 rate 858,381 spread 858,407 amount 951,373), then back panel
Grain FRONT hovers DONE (compressor tab reselected). Next: back panel (Tab key; Reason frontmost) then gen_grain.py
grain_back_raw.jpg = zoom screen [70,62,1030,700] (1348x896; screen = 70+px/1.404, 62+py/1.404)
Grain ALL hovers done (front, 5 fx views, back; back notes in grain_notes.txt after 'BACK:'). Next: tools/gen_grain.py + finish_device.py grain

## 2026-10-08 later: GRAIN DONE (PARTIAL): grain.json 213 rows, name_check PASS (use stripped remotemap: sed 's/\tse\.propellerheads\./\t/'; write it to scratchpad not /tmp). Pictures: grain_front/back_labeled + grain-lower-view + 5 fx views. Grain's compressor tab left selected. NEXT: Europa, Malstrom, Humana, NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8. Reduce Cable Clutter (K) still ON. Create > Instruments > Reason Studios submenu lists them all; new device goes below the selected one.

## EUROPA started: europa_front_top_raw.jpg = zoom screen [70,62,1030,812] (1232x962; screen=70+px/1.2833, 62+py/1.2833; Europa header at y~62). europa_pts.json = SCREEN coords (top scroll). Hover notes -> europa_notes.txt (key|text).
Europa hovers done through harmon (see europa_notes.txt); next harmmenu, harmpos, harmamt, unison, user wave, filter, amp
Europa hovers done through portatime; next envtab3/4, preset, editypos, envdisp, sustain, loop, keytrig, envrate.. lfo*, prange, wheels; then scroll for matrix/fx

## PAUSED by owner 2026-10-08 (said "pause") mid-EUROPA.
Done: Thor, Grain (both PARTIAL, logged in PANEL-MAP.md). Europa: created below Grain; europa_front_top_raw.jpg + europa_pts.json (screen coords) + europa_notes.txt hold hovers through lfowave. LEFT for Europa: lfowavearrows, lforate, lfodelay, lfosync, lfokeysync, lfoglobal, prange, wheelP, wheelM (pts in europa_pts.json), then scroll down for matrix + effects row/panels, then back panel, then gen_europa.py + finish_device.py + name_check + panel_map_md.py.
Then: Malstrom, Humana, NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8.
Reason state: test song "untitled 2" unsaved, front view, Reduce Cable Clutter (K) ON, full-screen control granted this session.
