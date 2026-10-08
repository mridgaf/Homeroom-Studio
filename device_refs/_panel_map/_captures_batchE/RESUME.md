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

## 2026-10-08 resumed: EUROPA top-scroll hovers ALL DONE (LFO row = no tooltip, seen). LEFT: scroll down for matrix + effects row/panels, then back panel, then gen_europa.py + finish_device.py + name_check + panel_map_md.py. Reason state unchanged (Europa top at y~62).
europa_front_bottom_raw.jpg = zoom screen [70,100,1030,442] after scroll down 8 (1568x559; screen=70+px/1.6333, 100+py/1.6333). Matrix 8 rows.
Europa MATRIX hovers DONE (8 rows, knobs Mod N Dest1/Dest2/Scale Amt; text fields/arrows/X no tooltip). Matrix knob screen x 303/454/607, row y 304,320,337,353,370,386,402,419 (scrolled view). NEXT: fx tabs (y 286: PHSR 783, DIST 822, EQ 861, DLY 900, REV 938, COMP 977), fx panels, back.
Europa fx hovered: COMP, DLY, EQ. Next DIST (tab 822), PHSR (783), REV (938), tab buttons/ON/power, then back. fx screen pts: DIST slider 766,407 drive 853,372 tone 901,372 amt 950,372; PHSR slider 818,397 depth 857,351 rate 857,382 spread 857,411 amt 954,370; REV decay 868,350 size 806,392 damp 866,392 amt 926,392
Europa fx panels ALL hovered (dist, phsr, rev too). Left: fx tab/ON/power/master buttons hover, then Tab for back panel, gen_europa.py. Tooltip text sometimes clipped by my zoom; names clear.
Europa FRONT ALL DONE. Next: back panel (Tab key), then gen_europa.py + finish_device.py.
europa_back_raw.jpg = zoom screen [60,215,1000,810] (1372x869; screen=60+px/1.4596, 215+py/1.4596), rack scrolled so Europa back header y~222. Back hovers next: gate 242,510 cv 242,541 pbtrim 362,509 pbjack 390,510 mwtrim 362,541 mwjack 390,541 CVin 586 x y510/538/567/594; CVout 775; audio L 813,781 R 861,781
Europa ALL hovers DONE incl back (flipped back to front). Next: tools/gen_europa.py (model: gen_grain.py) + finish_device.py europa + name_check + panel_map_md.py.
Europa fx raws saved (573x353 = zoom screen [740,275,1000,435], k=2.2038). REV tab reselected. NEXT: write tools/gen_europa.py
Europa ENGINE II view: europa_eng2_raw.jpg (zoom screen [70,62,1030,812], 1232x962, same pts as engine I). Hover list eng_keys.json (43 keys). Needed because remotemap Osc2/Osc3 knobs slots 9-24 need rows. Then engine III.
Engine II hovers DONE (europa_eng2_notes.txt). Engine III next: click (147,294), capture raw, hover subset.
europa_eng3_raw.jpg saved; eng3 hovers subset next
Engine III subset hovered (europa_eng3_notes.txt). Engine I reselected. NEXT: add eng2/eng3 views to gen_europa.py, finish, name_check.
## 2026-10-08 EUROPA DONE (PARTIAL): europa.json 343 rows, name_check PASS, PANEL-MAP row added, DECISIONS entry written. NEXT: Malstrom.

## MALSTROM started: created below Europa via app_menu Create>Instruments>Reason Studios (then app_release before full-screen tools). malstrom_front_raw.jpg = zoom screen [70,62,1030,412] (1563x571; screen=70+px/1.628, 62+py/1.628), device top at y~62.
Malstrom pts: malstrom_pts.json / malstrom_keys.json; notes malstrom_notes.txt (first 36 keys done, fenvD/S retry). Use zoom width 240 for tooltips.
Malstrom hovers done through oscAindex (notes file); next from oscAshift (keys[58:]); wheels/fenvD/S gave no tooltip
Malstrom hovers through oscB and wheels/fenv done; remaining keys from shape_sine onward (keys[85:]). Faders need zoom region y..y+100 and approach from above, wait 2s.
## PAUSED by owner 2026-10-08 (said 'Pause') mid-MALSTROM. Done: malstrom_notes.txt through fAmode (Shaper + Filter A mode). LEFT: fAenv fAkbd fAres fAfreq filtBlight fBroute fB_lp12 fBmode fBenv fBkbd fBres fBfreq spread volume meter (pts in malstrom_pts.json; approach from above, zoom y..y+100), then back panel (Tab), gen_malstrom.py, finish_device, name_check, panel_map_md. Reason: Malstrom created below Europa (Europa engine I selected), test song unsaved, rack front view.
Malstrom FRONT hovers ALL DONE. Next: Tab for back panel, hover, gen_malstrom.py
Malstrom back hovers DONE (malstrom_back_raw.jpg = zoom screen [60,62,1030,410] 1568x563, screen=60+px/1.616,62+py/1.616). Next: Tab to front, gen_malstrom.py

## 2026-10-08 MALSTROM DONE (PARTIAL): malstrom.json 148 rows, name_check PASS, PANEL-MAP row added, DECISIONS written. Reason on FRONT view, Malstrom top at screen y~62. NEXT: Humana (create below Malstrom via Create > Instruments > Reason Studios), NN19, SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8. Reduce Cable Clutter (K) still ON.
## HUMANA started: created below Malstrom; rack scrolled so Humana top y=62 (fits in one view, bottom y~318). humana_front_raw.jpg = zoom screen [70,62,1030,318] (1565x418, screen=70+px/1.63, 62+py/1.63). Notes humana_notes.txt key|text; pts humana_pts.json (screen). Done: top row + left block through mw_level. Next: wheels, sample display/menu, lower knobs, filter, amp, delay, reverb, then back.
Humana hovered through fkbd. Next: filter env faders (x 457/483/509/535 y~262), amp vel + faders (x 637/663/689/715), delay, reverb, back.
Humana hovered through delay (amp D/S/R no tooltip first try, retry). Next: reverb, back.
Humana FRONT hovers ALL DONE (ampD/R retried ok, ampS none). Next: Tab for back.
Humana ALL hovers done (back too; humana_back_raw.jpg same zoom region as front, screen=70+px/1.63,62+py/1.63). Flip back to front (Tab). Next: gen_humana.py + finish_device.py humana

## 2026-10-08 HUMANA DONE (PARTIAL): humana.json 74 rows, PASS. Reason on FRONT view, rack scrolled (Humana top y=62). NEXT: NN19 (create below Humana: Create > Instruments > Reason Studios > NN19 Digital Sampler; use app_menu with app="se.propellerheads.reason" then app_release), SubTractor, Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8. Remotemap block needs a row for EVERY knob slot (park rows for items with no panel control, see gen_humana.py). json device name must equal remotemap scope name (e.g. "Humana").
## NN19 started: created below Humana, rack scrolled so NN19 top y=62 (bottom ~412). nn19_front_raw.jpg = zoom screen [70,62,1030,412] (1563x571, screen=70+px/1.628, 62+py/1.628). ALL point coords for the front in nn19_pts.json (screen); notes nn19_notes.txt key|text in pts order. Hovered through lobw. Next: noteon.. (follow nn19_pts.json key order from noteon).
NN19 hovered through v_sstart (pts key order). Next: rangedisp, rangearrows, wheelP, wheelM, midisel.. keymap, lokey.., osc, lfo, filter, amp env, back.
NN19 hovered through loop (text readouts under display NOT hovered, skip). Next: sstart.. osc, lfo, filter, amp env, back.
NN19 hovered through destbtn. Next: filter (filtfreq..), amp env, then back.
NN19 front hovers DONE (several sliders no tooltip; by position). Next: Tab back panel + hover, gen_nn19.py
NN19 back hovers DONE (nn19_back_raw.jpg same frame as front). Still to hover: filter ON light (553,282) on front after Tab back. Then gen_nn19.py (remotemap block has Master Level slot32 w/o panel control: park).

## 2026-10-08 NN19 DONE (PARTIAL): nn19.json 116 rows, PASS. Reason on FRONT view, NN19 top at screen y=62. NEXT: SubTractor (create below NN19: app_menu app="se.propellerheads.reason" path Create>Instruments>Reason Studios>"SubTractor Analog Synthesizer", then app_release, scroll rack ~50px/tick), Radical Piano, Monotone, Pangea, Klang, NN-XT, ID8. 20 of 26 done... (Kong..NN19 = 7 instruments + 9 effects + earlier = see PANEL-MAP.md). Reduce Cable Clutter (K) still ON.
