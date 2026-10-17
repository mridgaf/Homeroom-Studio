# Chapter 08: Reason panel map
## Part 22 of 44

_Front and back panel maps of Reason devices: every knob, button and jack, by device._

**In this part:**
- RESUME.md — Batch E (instruments), started 2026-10-08
- 00-INDEX.md — Panel Map index (read this first, then ONLY the chapter you need)
- a-b-12-audio-out-switch-pongasoft.md — a-b-12-audio-out-switch-pongasoft

(Next: Part 23 of 44)


=====================================================
SOURCE FILE: RESUME.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/_captures_batchE/RESUME.md
=====================================================

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
## SUBTRACTOR started: created below NN19, rack scrolled so top y=62. subtractor_front_raw.jpg = zoom [70,62,1030,412] 1563x571 (k=1.628). ALL front pts in subtractor_pts.json (screen). notes subtractor_notes.txt. Hovered through polyarrows. Next: range onward in pts order.
Subtractor hovered through c2_fm. Next o1phase.. (pts order). LED radios (atouch/expr/breath, o1x.., l1w*, l1d_*, l2d_*, md_*, f1m_*) to be marked 'not hovered pattern' unless time.
Subtractor hovered through ringmod. Next noiselight.. (pts order).
Subtractor hovered through mdbtn. Next f1freq.. (pts order).
Subtractor hovered through fenvicon (f2freq,f2level retry). Next aenv, velocity.
Subtractor FRONT hovers done (LED radios not hovered, pattern). Next: Tab back.
Subtractor back raw saved; back hovered through f2freq. Next: amp level, mod wheel, pitch wheel (y310,339,369; trim x308 jack x337), mod outs (496: 135,164,193), gate ins (676: 135,164,193), main out (822,139).
Subtractor ALL hovers done. Next: Tab to front, gen_subtractor.py (screen k=1.628 origin 70,62; back pts in this log).

## 2026-10-08 SUBTRACTOR DONE (PARTIAL): subtractor.json 160 rows, PASS. NEXT: Radical Piano (create below SubTractor), Monotone, Pangea, Klang, NN-XT, ID8.
## RADICAL PIANO started: created below SubTractor, rack scrolled so top y=66 (bottom 502). radicalpiano_front_raw.jpg = zoom [70,66,1030,502] (1565x712, k=1.63, origin 70,66). notes radicalpiano_notes.txt. Hovered header through patchdisp (micblend (535,189) tooltip cut: retry). Next: lower panel.
RadicalPiano hovered through pedal (lower panel). Next: EQ, ambience, output; then Tab back.
RadicalPiano FRONT hovers done. Back panel open now (Tab): hover next. Back pts screen: gate 273,212 cv 273,243 pitch trim 443,212 jack 470,212 mastervol trim 443,243 jack 470,243 audioin 669,212 outL 775,232 outR 825,232.
RadicalPiano ALL hovers done (back raw saved). Next Tab to front, gen_radicalpiano.py

## 2026-10-08 RADICAL PIANO DONE (PARTIAL): radical-piano.json 71 rows, PASS (scratch copy device name radicalpiano). Owner asked for SubTractor + Radical Piano only; STOPPED there. NEXT: Monotone, Pangea, Klang, NN-XT, ID8. Reason on FRONT view, Radical Piano top y=66. Reduce Cable Clutter (K) still ON.

## 2026-10-15 02:xx 2AM RUN: fresh test song (Reason had been closed; relaunched). Rack detached on 2nd monitor (PHL 241V8LB). MONOTONE created; front raw saved: zoom screen [415,245,1230,540] -> 1073x389 (k=1.3166, screen=415+px/k, 245+py/k). notes -> monotone_notes.txt (key|text). Queue after: Pangea, Klang, NN-XT, ID8, BV512.
Monotone FRONT hovers DONE. Next: Tab back, K, picture+hover, then gen_monotone.py
## 2026-10-15 MONOTONE DONE: monotone.json 70 rows, name_check PASS (stripped remotemap copy), in PANEL-MAP.md. NEXT: Pangea, Klang, NN-XT, ID8, BV512. Reason: fresh test song, rack detached on 2nd monitor (PHL 241V8LB, use switch_display), Monotone on BACK view, K state unknown (cables visible).
## 2026-10-15 PANGEA started: back raw saved (zoom screen [415,350,1230,570] 1072x290 k=1.3153, screen=415+px/k,350+py/k), back hovers DONE (pangea_notes.txt). Next: Tab front pic + hover.
Pangea FRONT raw saved: zoom [420,350,1215,572] 1047x293 (k=1.317, screen=420+px/k, 350+py/k). hovered header+left through levelmw. Next: instrument sel, bottom knobs, filter, amp, delay, reverb
## 2026-10-15 PANGEA DONE: pangea.json 66 rows, name_check PASS, in PANEL-MAP.md. NEXT: Klang, NN-XT, ID8, BV512. Reason: rack on 2nd monitor, Pangea on FRONT view.
## 2026-10-15 KLANG started (created below Pangea, rack scrolled so Klang tape y~551). klang_front_raw.jpg = zoom screen [420,531,1215,753] 1047x293 (k=1.317, screen=420+px/k, 531+py/k). Same layout as Pangea (dy=181). Hovered header+left. notes klang_notes.txt. TODO: Pangea RANGE spinner retry hovering (479,y) -> 'Pitch Bend Range: 2' probably (Klang showed that).
Klang FRONT hovers DONE. Next: Pangea range retry, then Tab back for Klang back pic+hover
## 2026-10-15 KLANG DONE: klang.json 66 rows PASS, in PANEL-MAP.md. Pangea range row fixed (tooltip 'Pitch Bend Range: 2'). NEXT: NN-XT, ID8, BV512. Reason: Klang on BACK view, rack scrolled.
## 2026-10-15 NN-XT started (created below Klang). nnxt_back_raw.jpg = zoom screen [420,395,1215,545] 1045x198 (k=1.3145, screen=420+px/k,395+py/k) with rack scrolled (NN-XT back top y~395). back hovers done through pitch wheel (nnxt_notes.txt). Next: gate inputs, 16 outputs, power switch; then Tab front (main panel + remote programmer: big).
NN-XT BACK hovers DONE (jacks+16 outs; power switch no tooltip). Next: Tab front.
NN-XT FRONT raw saved nnxt_front_raw.jpg zoom [420,392,1220,512] 1043x157 (k=1.3038, screen=420+px/k,392+py/k). Hovered through tape. Remote Editor (folded, below) NOT mapped (like Thor programmer). Next: Global controls knobs + IR display + master.
## 2026-10-15 NN-XT DONE (main panel + back; Remote Editor not mapped): nn-xt.json 66 rows PASS, in PANEL-MAP.md. NEXT: ID8, BV512. Reason: NN-XT on FRONT view, rack scrolled.
## 2026-10-15 ID8 DONE: id8.json 23 rows PASS, in PANEL-MAP.md. NEXT: BV512 (re-shoot pictures live), then check INVENTORY for rest (Rytmik, MIDI Out, Players, REs). Reason: ID8 on BACK view, rack scrolled.
## 2026-10-15 BV512 started (created below ID8). bv512_back_raw.jpg = zoom [420,394,1220,540] 1051x193 (k=1.3138, screen=420+px/k,394+py/k). BACK hovers DONE (32 band jacks 'Band N CV Out/In', shift, carrier, hold, modulator, outs) -> bv512_notes.txt BACK: section. Next: Tab front pic + hover.
## 2026-10-15 BV512 DONE: bv512.json 75 rows (no remotemap scope: names from vocab). Original queue (Monotone, Pangea, Klang, NN-XT, ID8, BV512) COMPLETE. NEXT (extra): Rytmik, MIDI Out Device, then third-party Rack Extensions (15, no Remote map), Players (5, not rack devices). Reason: BV512 on FRONT view, rack scrolled.
## 2026-10-15 RYTMIK started (created; no remotemap/vocab entry -> names from tooltips only). rytmik_front_raw.jpg zoom [420,172,1225,540] 1059x485 (k=1.3155, screen=420+px/k,172+py/k). Hovered header + sample readouts (no tooltips). Next: 8 channel strips (x offset 83 each) + master FX strip, then back.
Rytmik FRONT hovers DONE (strips 1-8, master). Pads select drum (verified). Next: Tab back pic+hover, gen_rytmik.py
## 2026-10-15 RYTMIK DONE: rytmik.json 110 rows (no remote map), in PANEL-MAP.md. NEXT: MIDI Out Device, then 15 third-party REs, then Players. Reason: Rytmik on BACK view, rack scrolled.
## 2026-10-15 MIDI OUT started: front/back raw saved (region [420,466,1220,540] and [455,466,1195,540]); hovers done; writing gen_midiout.py
## 2026-10-15 MIDI OUT DONE: midi-out.json PANEL-MAP.md updated. NEXT: 15 third-party REs, Players. Reason: MIDI Out on FRONT view.
## 2026-10-15 ELEMENTS DS-LFO DONE (RE 1 of 15). Remaining REs: Morfin XF (Groovy Melon), A/B 12 Audio Out Switch, A/B Audio & CV Switch, CVA-7, RE 181, RPSpec, Select CV Switch (utilities); Elements Splitter, kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser (effects). Then Players. Reason on BACK view.
## 2026-10-15 MORFIN XF DONE (RE 2 of 15). Remaining REs: A/B 12 Audio Out Switch, A/B Audio & CV Switch, CVA-7 (pongasoft); RE 181 (Red Rock Sound), RPSpec (Rob Papen), Select CV Switch (Robotic Bean); Elements Splitter (AirRaid), kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser. Then Players (5).
## 2026-10-15 A/B 12 AUDIO OUT DONE (RE 3 of 15; ab12-audio-out.json 105 rows). Remaining REs: A/B Audio & CV Switch, CVA-7 (pongasoft); RE 181, RPSpec, Select CV Switch; Elements Splitter, kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser. Then Players (5).
## 2026-10-15 A/B SWITCH DONE (RE 4 of 15). Remaining: CVA-7; RE 181, RPSpec, Select CV Switch; Elements Splitter, kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; Players.
## 2026-10-15 CVA-7 DONE (RE 5 of 15). Remaining: RE 181, RPSpec, Select CV Switch; Elements Splitter, kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; Players.
## 2026-10-15 RE 181 DONE (RE 6 of 15). Remaining: RPSpec, Select CV Switch; Elements Splitter, kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; Players.
## 2026-10-15 SELECT CV SWITCH DONE (RE 7 of 15). Remaining: RPSpec; Elements Splitter, kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; Players.
## 2026-10-15 RPSPEC DONE (RE 8 of 15; utilities REs finished). Remaining effects REs: Elements Splitter (AirRaid), kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; then Players.
## 2026-10-15 ELEMENTS SPLITTER DONE (RE 9 of 15). Remaining effects REs: kHs Chorus, Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; then Players (5). Menu paths: Create>Effects>kiloHearts / Kuassa / Softube(Saturation Knob listed under Reason Studios? check) / ThatMusicCompany.
kHs Chorus BACK raw saved (zoom [453,466,1193,540]); back hovers done: jack above each name = '<X> CV', knob below = '<X> CV: 127' (Delay, Depth, Rate, Spread, Mix); IN/OUT cabled (Splitter, RE 181); front next (Tab)
## 2026-10-15 kHs CHORUS DONE (RE 10 of 15). Remaining: Efektor Silencer, Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; Players.
## 2026-10-15 EFEKTOR SILENCER DONE (RE 11 of 15). Remaining: Softube Saturation Knob, Distort Chain, Mr OverDrive, T2 Phaser; Players.

## STOPPED 2026-10-15 (usage limit). Done tonight: Monotone, Pangea, Klang, NN-XT, ID8, BV512, Rytmik, MIDI Out, REs: DS-LFO, Morfin XF, A/B 12, A/B Switch, CVA-7, RE 181, Select CV, RPSpec, Elements Splitter, kHs Chorus, Efektor Silencer.
IN PROGRESS: Softube Saturation Knob. satknob_back_raw.jpg saved (zoom [453,392,1193,540]). Back hovers: Audio In L/R and Audio Out L/R = "Connected to ..." (cabled); name tape/Softube logo/screw icons no tooltip. FRONT not hovered yet (device is on FRONT view, top y~395: fold arrow, bypass switch, patch display, prev/next/folder/disk, SATURATION knob ~(560,475), SATURATION TYPE switch ~(708,490), light ~(603,438)).
LEFT: Saturation Knob front, Distort Chain, Mr OverDrive, T2 Phaser (Create>Effects>ThatMusicCompany), then Players (5, not rack devices). Test song "untitled" open, unsaved, rack on 2nd monitor.
Method per device: hover -> tools/gen_<x>.py -> finish_device.py -> panel_map_md.py.

=====================================================
SOURCE FILE: 00-INDEX.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/chapters/00-INDEX.md
=====================================================

# Panel Map index (read this first, then ONLY the chapter you need)

Chapters live beside this file: one `<device>.md` each (front + back tables). Rules and method are below.

Reference for Claude and Hermes. John doesn't need to read this. Plan: PLAN.md. Method: the `panel-map` skill.

## Code format
`DEVICE-SIDE-TYPE##`, for example `SCR4-F-K03`.
- SIDE: F = front, B = back
- TYPE: K = knob, B = button/switch, S = slider, J = jack, D = display
- The code is only a nickname. To control something, use the **Reason name** column. Reason only accepts its own exact names, and a wrong name fails without any warning.
- MIDI: knob slot k is sent on CC 29+k, and its value comes back on CC 77+k (reason_voice/reason_control.py).
- pos = the control's centre as a fraction (0–1) of the labeled picture. To get a screen point, match the panel's corner screws on screen and in the picture (`tools/to_screen.py`). This works at any zoom.

## What Reason tells you (tested in Reason 12.7, 2026-10-02/03)
- **Hover = proof.** Hovering a control shows a tooltip with its exact name, and its value if it has one ("Damage Control: 70"). Nothing changes. This is how every position gets checked.
- Hovering a slider: the tooltip only shows on the **handle**, which moves with the value.
- Hovering an empty jack shows its name ("Right Output"). Hovering a cabled jack shows where the cable goes ("Connected to Room: Decay CV In").
- The hover name can differ from the Remote name (The Echo: hover "Diffusion Spread", Remote "Diffuse Spread"). Keep both; control with the Remote name.
- A back trim knob shows its input's name plus a value ("Damage Control CV Input: 127").
- Displays (meters, light lists) and the fold triangle show no tooltip.
- **Folded devices** become a thin strip, and the controls move. Unfold first (click the triangle).

## How to make a cable (proven 2026-10-02)
1. Right-click the source jack (its position comes from this map).
2. A menu lists every device in the song by its rack name, e.g. "EasyFuzz (Scream 4)". Each one opens a submenu with only the jacks that fit.
3. Click the target jack name. The menus are real Mac menus, readable as text.
4. Prove it: right-click the jack again. The target device and jack now have a ✓, "Scroll to Connected Device" appears, and "Disconnect" turns on. Or hover the jack: "Connected to <device>: <jack>".
- `*` after a jack name = that jack already has a cable. Grey = can't take this cable. Audio outputs also offer "Route to New Mix Channel".
- Undo a cable: right-click the jack, then **Disconnect**.

## Devices
| Device | Code | Front | Back | Data | Status | Chapter |
|---|---|---|---|---|---|---|
| Scream 4 Distortion | SCR4 | scream-4_front_labeled.png | scream-4_back_labeled.png | scream-4.json | **done** — all 38 checked in Reason, manual ch.51 checked | [scream-4.md](scream-4.md) |
| The Echo | ECHO | the-echo_front_labeled.png | the-echo_back_labeled.png | the-echo.json | **done** — 48/48 checked in Reason; manual ch.50 spot-checked; drafted by helper | [the-echo.md](the-echo.md) |
| CF-101 Chorus/Flanger | CF101 | cf-101_front_labeled.png | cf-101_back_labeled.png | cf-101.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [cf-101-chorus-flanger.md](cf-101-chorus-flanger.md) |
| COMP-01 Compressor | COMP01 | comp-01_front_labeled.png | comp-01_back_labeled.png | comp-01.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [comp-01-compressor.md](comp-01-compressor.md) |
| D-11 Foldback Distortion | D11 | d-11_front_labeled.png | d-11_back_labeled.png | d-11.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [d-11-foldback-distortion.md](d-11-foldback-distortion.md) |
| DDL-1 Digital Delay Line | DDL1 | ddl-1_front_labeled.png | ddl-1_back_labeled.png | ddl-1.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [ddl-1-digital-delay-line.md](ddl-1-digital-delay-line.md) |
| ECF-42 Envelope Controlled Filter | ECF42 | ecf-42_front_labeled.png | ecf-42_back_labeled.png | ecf-42.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual; ONE ASSUMING: GATE light (ECF42-F-D02) = Remote 'Trigger' (no tooltip, unproven) | [ecf-42-envelope-controlled-filter.md](ecf-42-envelope-controlled-filter.md) |
| PEQ-2 Two Band Parametric EQ | PEQ2 | peq-2_front_labeled.png | peq-2_back_labeled.png | peq-2.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [peq-2-two-band-parametric-eq.md](peq-2-two-band-parametric-eq.md) |
| PH-90 Phaser | PH90 | ph-90_front_labeled.png | ph-90_back_labeled.png | ph-90.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [ph-90-phaser.md](ph-90-phaser.md) |
| RV-7 Digital Reverb | RV7 | rv-7_front_labeled.png | rv-7_back_labeled.png | rv-7.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [rv-7-digital-reverb.md](rv-7-digital-reverb.md) |
| UN-16 Unison | UN16 | un-16_front_labeled.png | un-16_back_labeled.png | un-16.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [un-16-unison.md](un-16-unison.md) |
| MClass Compressor | MCMP | mclass-compressor_front_labeled.png | mclass-compressor_back_labeled.png | mclass-compressor.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual (picture tape reads M COMP 2; this song's instance reads M COMP 1) | [mclass-compressor.md](mclass-compressor.md) |
| MClass Equalizer | MEQ | mclass-equalizer_front_labeled.png | mclass-equalizer_back_labeled.png | mclass-equalizer.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [mclass-equalizer.md](mclass-equalizer.md) |
| MClass Maximizer | MMAX | mclass-maximizer_front_labeled.png | mclass-maximizer_back_labeled.png | mclass-maximizer.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [mclass-maximizer.md](mclass-maximizer.md) |
| MClass Stereo Imager | MSIM | mclass-stereo-imager_front_labeled.png | mclass-stereo-imager_back_labeled.png | mclass-stereo-imager.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [mclass-stereo-imager.md](mclass-stereo-imager.md) |
| RV7000 Mk II Advanced Reverb | RV7K | rv7000_front_labeled.png | rv7000_back_labeled.png | rv7000.json | done 2026-10-07: everything hover-checked; soft knobs (RV7K-F-K05..K12) numbered by position per owner, their names change by page; programmer EQ and Gate edit-mode views not captured; name_check PASS | [rv7000-mk-ii-advanced-reverb.md](rv7000-mk-ii-advanced-reverb.md) |
| Matrix Pattern Sequencer | MTRX | matrix_front_labeled.png | matrix_back_labeled.png | matrix.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Matrix (not added; out of scope) | [matrix-pattern-sequencer.md](matrix-pattern-sequencer.md) |
| Spider Audio Merger & Splitter | SPDA | spider-audio_front_labeled.png | spider-audio_back_labeled.png | spider-audio.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Spider Audio (not added; out of scope) | [spider-audio-merger-splitter.md](spider-audio-merger-splitter.md) |
| Spider CV Merger & Splitter | SPDC | spider-cv_front_labeled.png | spider-cv_back_labeled.png | spider-cv.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Spider CV (not added; out of scope) | [spider-cv-merger-splitter.md](spider-cv-merger-splitter.md) |
| Pulsar Dual LFO | PULS | pulsar_front_labeled.png | pulsar_back_labeled.png | pulsar.json | done 2026-10-07: every position hover-checked in Reason. Rack Extension; name_check cannot run: our remotemap has no Scope block for Pulsar (not added; out of scope) | [pulsar-dual-lfo.md](pulsar-dual-lfo.md) |
| RPG-8 Monophonic Arpeggiator | RPG8 | rpg-8_front_labeled.png | rpg-8_back_labeled.png | rpg-8.json | done 2026-10-07: all positions hover-checked in Reason; Pattern turned on briefly to read step tooltips, then off; name_check can't run (no RPG-8 Scope block in remotemap, not edited) | [rpg-8-monophonic-arpeggiator.md](rpg-8-monophonic-arpeggiator.md) |
| Line Mixer 6:2 | LNMX | line-mixer_front_labeled.png | line-mixer_back_labeled.png | line-mixer.json | done 2026-10-07: all 79 positions hover-checked in Reason; name_check: Remote items all matched, only error is no Line Mixer Scope block in remotemap (not edited) | [line-mixer-6-2.md](line-mixer-6-2.md) |
| Mixer 14:2 | MX14 | mixer-14-2_front_labeled.png | mixer-14-2_back_labeled.png | mixer-14-2.json | done 2026-10-07: all 324 positions hover-checked in Reason; name_check: Remote items all matched; only errors are no Mixer 14:2 Scope block in remotemap (not edited) and 3-digit codes K100-K102 failing the checker's 2-digit code pattern (codes kept, checker not edited) | [mixer-14-2.md](mixer-14-2.md) |
| Mix Channel | MXCH | mix-channel_front_labeled.png | mix-channel_back_labeled.png | mix-channel.json | done 2026-10-07: all 31 positions hover-checked in Reason. name_check can't pass: vocab lists this device as 'Reason Main Mixer Channel' (not 'Mix Channel') and the remotemap has no Scope block (not edited). Remote names used (Mute, Solo, Level, Pan, Bypass Insert FX, Channel Name) all appear in that vocab entry. Audio Output menu not opened (no tooltip). Insert FX slot was empty, so no insert-FX controls exist to map. Two tooltips cut off at the zoom edge (Bypass ... Off; Show in Spectrum EQ Window). | [mix-channel.md](mix-channel.md) |
| Combinator | COMB | combinator_front_labeled.png | combinator_back_labeled.png | combinator.json | done 2026-10-07: all 47 positions hover-checked in Reason (default Init Patch panel: Control 1-4, Switch 1-4). Unfolded Combinator mixer and the Programmer/Devices views are separate views, not mapped here. Selector dropdowns not opened. Orange light and green meters have no tooltip; their Remote item (Audio In/Out, Note On indicators) not confirmed, so left unnamed. name_check PASS (0 errors; 20 warnings: Remote items like Rotary 5-16, Run Pattern Devices, Bypass All FX have no control on this default panel; patch up/down arrows are one row named Select Next Patch, top half is Select Previous Patch). | [combinator.md](combinator.md) |
| Audio Track | AUDT | audio-track_front_labeled.png | audio-track_back_labeled.png | audio-track.json | done 2026-10-07: all 15 positions checked in Reason (11 front, 4 back). name_check: only errors are no vocab entry and no Scope block (Audio Track has no Remote map). Back has no jacks. Level fader checked on the handle. | [audio-track.md](audio-track.md) |
| Hardware Interface | HWIF | hardware-interface_front_labeled.png | hardware-interface_back_labeled.png | hardware-interface.json | done 2026-10-07: all 354 positions (207 front, 147 back) checked in Reason. Rack name seen in tooltips: 'Hardware Interface II'. Front meters name the right channel of each pair; D16, D40, D64 name other channels (recorded as seen). name_check: only the expected no-vocab/no-Scope errors. | [hardware-interface.md](hardware-interface.md) |
| Master Section | MSEC | master-section_front_labeled.png | master-section_back_labeled.png | master-section.json | done 2026-10-07: all 59 positions (13 front, 46 back) checked in Reason. Device name here is the rack Master Section panel; the remotemap 'Reason Master Section' scope is the mixer's channel Remote scope, so it does not apply. name_check: only the expected no-vocab/no-Scope errors. | [master-section.md](master-section.md) |
| Main Mixer | MMIX | main-mixer_front_labeled.png | — (mixer window has no back) | main-mixer.json | done 2026-10-07: ASSUMED view = Reason's Main Mixer window (F5), one representative channel strip (the Mix Channel strip) plus the master strip, stitched from 4 scroll slices (picture is 4 stacked slices, each 1362 px tall; overlaps repeat but each control is boxed once). Other channel strips repeat the same controls. All 168 positions hovered in Reason; faders, meters and displays show no tooltip in this window (recorded as seen). name_check: only the expected no-vocab/no-Scope errors. | [main-mixer.md](main-mixer.md) |
| Channel EQ | CEQ | channel-eq_front_labeled.png | channel-eq_back_labeled.png | channel-eq.json | done 2026-10-07: all 44 positions (25 front, 19 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'ChannelEQ'); 'what' lines spot-checked against manual ch.58. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). Rack Channel EQ attached itself to the Mix Channel's insert chain, so its audio jacks show cables. | [channel-eq.md](channel-eq.md) |
| Channel Dynamics | CDYN | channel-dynamics_front_labeled.png | channel-dynamics_back_labeled.png | channel-dynamics.json | done 2026-10-07: all 33 positions (22 front, 11 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'ChannelDynamics'); 'what' lines spot-checked against manual ch.57. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). | [channel-dynamics.md](channel-dynamics.md) |
| Master Bus Compressor | MBC | master-bus-compressor_front_labeled.png | master-bus-compressor_back_labeled.png | master-bus-compressor.json | done 2026-10-07: all 23 positions (13 front, 10 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'MasterCompressor'); 'what' lines spot-checked against manual ch.59. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). | [master-bus-compressor.md](master-bus-compressor.md) |
| Sweeper Modulation Effect | SWPR | sweeper_front_labeled.png | sweeper_back_labeled.png | sweeper.json | done 2026-10-07 except two rows (Claude, hover-checked in Reason 12; LFO/Env synced-rate readouts SWPR-F-D05/D06-type rows NOT hovered): Phaser+Envelope main view, Filter view, Audio Follower view, back panel. NOT shown: Flanger view (same controls as Phaser minus Bandwidth/Stages). 7 front controls and 3 back icons give no tooltip (recorded as seen); the 4 audio jacks are cabled so their own names are unread (null). Device Name / BeatSync / Trig On / Stereo Mode / LFO Wave / LFO Sync / Env Loop assignments rest on the Remote list, not a tooltip. | [sweeper-modulation-effect.md](sweeper-modulation-effect.md) |
| Synchronous Effect Modulator | SYNC | synchronous_front_labeled.png | synchronous_back_labeled.png | synchronous.json | done 2026-10-07 (Claude, hover-checked in Reason 12): front (all positions), back (all positions). Display controls (TOOL, RATE, SPEED, FREE, tracks, FRZ/KILL, MASTER OFFSET, PHASE, DIM, MOD CTRL, 10 MOD knobs) give NO tooltip and have no Remote item. Delay Time (ms) row and the 4 audio jack names are unproven (see rows). | [synchronous-effect-modulator.md](synchronous-effect-modulator.md) |
| Audiomatic Retro Transformer | AUDM | audiomatic_front_labeled.png | audiomatic_back_labeled.png | audiomatic.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. No Patch Name item (device has no patch browser). 16 preset buttons all read tooltip 'Preset'. Audio jack names unread (cabled). | [audiomatic-retro-transformer.md](audiomatic-retro-transformer.md) |
| Neptune Pitch Adjuster | NEPT | neptune_front_labeled.png | neptune_back_labeled.png | neptune.json | done 2026-10-07 except noted (Claude, hover-checked in Reason 12): all front and back positions. Remote has case-variant duplicate items (Midi Destination, Mod wheel, Vibrato rate, pitch bend) and 'Pitch Adjust Amount' with no known panel control: rows are placeholders, NOT proven. Faders PITCHED SIGNAL / VOICE SYNTH and 12 note keys give no tooltip. Audio jack names unread (cabled). | [neptune-pitch-adjuster.md](neptune-pitch-adjuster.md) |
| Pulveriser | PULV | pulveriser_front_labeled.png | pulveriser_back_labeled.png | pulveriser.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. Follow (flat Remote item) placed on the follower light, NOT proven. Waveform arrows, light LEDs, routing icons give no tooltip. Audio jack names unread (cabled). | [pulveriser.md](pulveriser.md) |
| Quartet Chorus Ensemble | QRTT | quartet_front_labeled.png | quartet_back_labeled.png | quartet.json | done 2026-10-07 (Claude, hover-checked in Reason 12): BBD main view (pictured), Chorus, FFT and Grain modes, back panel. Stereo selector, FFT Start/End handles give no tooltip (names from Remote list). Audio jack names unread (cabled). Set back to BBD mode. | [quartet-chorus-ensemble.md](quartet-chorus-ensemble.md) |
| Alligator Filter Gate | ALGT | alligator_front_labeled.png | alligator_back_labeled.png | alligator.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. Controls past slot 48 (band Phaser/Delay amounts, Dry Pan, Delay and Phaser sections) have Remote names but no slot in our remotemap. Gate Open lights (flat items), meter lights, pattern/LFO arrows give no usable tooltip. Audio jack names unread (cabled). | [alligator-filter-gate.md](alligator-filter-gate.md) |
| Softube Amp (ReasonAmp) | RAMP | reasonamp_front_labeled.png | reasonamp_back_labeled.png | reasonamp.json | done 2026-10-07 (Claude, hover-checked in Reason 12; rack name 'Softube Amp', Remote name ReasonAmp): all front and back positions. Amp/Cab model lights all show one tooltip each. Lamp, logos, level lights, fuses, ground screw give no tooltip. Audio jack names unread (cabled). | [softube-amp-reasonamp.md](softube-amp-reasonamp.md) |
| Softube Bass Amp (ReasonBassAmp) | RBAS | reasonbassamp_front_labeled.png | reasonbassamp_back_labeled.png | reasonbassamp.json | done 2026-10-07 (Claude, hover-checked in Reason 12; rack name 'Softube Bass Amp', Remote name ReasonBassAmp): all front and back positions. Amp/Cab model lights each show one tooltip. Both patch arrows read 'Select previous patch' in this pass (not told apart). Level lights, fuses, vent, labels give no tooltip. Audio jack names unread (cabled). | [softube-bass-amp-reasonbassamp.md](softube-bass-amp-reasonbassamp.md) |
| Kong Drum Designer | KONG | kong-drum-designer_front_labeled.png | kong-drum-designer_back_labeled.png | kong-drum-designer.json | done 2026-10-08 (Claude, hover-checked in Reason 12): main panel, enlarged right column, Drum and FX section (Drum 1 / Bass Drum state) and back panel. The 16 drum modules differ; only Drum 1 pictured. LCD knobs (offsets, sends, pan, tone, level) gave no tooltip; names from the Remote list. Rows K301-K345 are aliases of the one LCD knob for Drum 2-16. | [kong-drum-designer.md](kong-drum-designer.md) |
| Redrum Drum Computer | REDR | redrum-drum-computer_front_labeled.png | redrum-drum-computer_back_labeled.png | redrum-drum-computer.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front (10 channels + pattern section) and back. Channels 1-4 fully hovered; channels 5-10 hovered except the two small lights and SELECT (no tooltip seen on channels 1-4). Step buttons, SELECT, lights, patch/sample displays gave no tooltip: names from the Remote list. | [redrum-drum-computer.md](redrum-drum-computer.md) |
| Dr. Octo Rex Loop Player | DREX | dr-rex-loop-player_front_labeled.png | dr-rex-loop-player_back_labeled.png | dr-rex-loop-player.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front with Programmer open, and back. Loop buttons, loop-name displays, lamps, RUN, filter-mode lights, LFO wave/dest lights gave no tooltip: names from the Remote list. Remote slot 10 'Selected Loop in Editor' has no proven control (stand-in row, low confidence). Lower half of loop-file arrows and Trigger-Next BAR/BEAT/1/16 buttons not separately proven. | [dr-octo-rex-loop-player.md](dr-octo-rex-loop-player.md) |
| Mimic Creative Sampler | MIMC | mimic_front_labeled.png | mimic_back_labeled.png | mimic.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front (Slot 1 selected) and back. Menus, modes, slot tabs, envelope D/S sliders, wheels, markers gave no tooltip: names from the Remote list. Remote has Slot 1-8 versions of every control; one physical control serves all; rows K301-K335 are aliases for slots 2-8. Slot 43 'Algorithm' placed on the stretch menu (low confidence). Some knobs (Start/Pitch/Pan mod amounts, Filter Kbd/Vel, Send 2, wheels) have tooltip names but no Remote item. | [mimic-creative-sampler.md](mimic-creative-sampler.md) |
| Thor Polysonic Synthesizer | THOR | thor_front_labeled.png | thor_back_labeled.png | thor.json | PARTIAL 2026-10-08: front+back+Filter 2 view hovered; matrix rows other than 1, 8, 12 inferred from pattern; Programmer panel + step sequencer panel not mapped | [thor-polysonic-synthesizer.md](thor-polysonic-synthesizer.md) |
| Grain Sample Manipulator | GRAN | grain_front_labeled.png | grain_back_labeled.png | grain.json | PARTIAL 2026-10-08: front (top + lower views + 5 effect panels) and back hovered; matrix rows 2-8 inferred from row 1; other grain algorithm modes (Formant knob) and LFO 3 not captured | [grain-sample-manipulator.md](grain-sample-manipulator.md) |
| Europa Shapeshifting Synthesizer | EURO | europa_front_labeled.png | europa_back_labeled.png | europa.json | PARTIAL 2026-10-08: front (engine I, 2 other engine views, lower view, 6 effect panels) and back hovered; engine III hovered on 10 of 43 controls (rest by pattern); LFO 2/3 and envelopes 1/3/4 tabs not opened; Europa displays/menus give no tooltip | [europa-shapeshifting-synthesizer.md](europa-shapeshifting-synthesizer.md) |
| Malstrom Graintable Synthesizer | MALS | malstrom_front_labeled.png | malstrom_back_labeled.png | malstrom.json | PARTIAL: all front and back controls hovered; front mapped from one picture | [malstrom-graintable-synthesizer.md](malstrom-graintable-synthesizer.md) |
| Humana Vocal Ensemble | HUMA | humana_front_labeled.png | humana_back_labeled.png | humana.json | PARTIAL: all front and back controls hovered; syllable buttons in the sample display not mapped | [humana-vocal-ensemble.md](humana-vocal-ensemble.md) |
| NN19 Digital Sampler | NN19 | nn19_front_labeled.png | nn19_back_labeled.png | nn19.json | PARTIAL: all front and back controls hovered; sample-name/key text readouts under the keymap not mapped | [nn19-digital-sampler.md](nn19-digital-sampler.md) |
| SubTractor Analog Synthesizer | SUBT | subtractor_front_labeled.png | subtractor_back_labeled.png | subtractor.json | PARTIAL: all front and back controls hovered; radio LED rows and the two display text fields not hovered | [subtractor-analog-synthesizer.md](subtractor-analog-synthesizer.md) |
| Radical Piano | RADP | radical-piano_front_labeled.png | radical-piano_back_labeled.png | radical-piano.json | PARTIAL: all knobs, buttons and back jacks hovered; mic LED groups hovered once per group | [radical-piano.md](radical-piano.md) |
| Monotone Bass Synthesizer | MONO | monotone_front_labeled.png | monotone_back_labeled.png | monotone.json | mapped 2026-10-15; every position hovered in Reason (range spinner, fold arrow, patch display, small light: no tooltip) | [monotone-bass-synthesizer.md](monotone-bass-synthesizer.md) |
| Pangea World Instruments | PANG | pangea_front_labeled.png | pangea_back_labeled.png | pangea.json | mapped 2026-10-15; every position hovered in Reason (fold arrow, NOTE light, range spinner, instrument dropdown, filter type menu: no tooltip) | [pangea-world-instruments.md](pangea-world-instruments.md) |
| Klang Tuned Percussion | KLNG | klang_front_labeled.png | klang_back_labeled.png | klang.json | mapped 2026-10-15; every position hovered in Reason (fold arrow, NOTE light, instrument dropdown, filter type menu: no tooltip) | [klang-tuned-percussion.md](klang-tuned-percussion.md) |
| NN-XT Advanced Sampler | NNXT | nn-xt_front_labeled.png | nn-xt_back_labeled.png | nn-xt.json | main panel + back mapped 2026-10-15; every position hovered in Reason; NN-XT Remote Editor (folded sample editor) NOT mapped | [nn-xt-advanced-sampler.md](nn-xt-advanced-sampler.md) |
| ID8 Instrument Device | ID8 | id8_front_labeled.png | id8_back_labeled.png | id8.json | mapped 2026-10-15; every position hovered in Reason (category/parameter displays, sound list, tape, back power switch: no tooltip). Remote items Category Name, Preset, Sound, Sound Name, Select Next/Previous Preset/Sound have no proven panel control | [id8-instrument-device.md](id8-instrument-device.md) |
| BV512 Digital Vocoder | BV51 | bv512_front_labeled.png | bv512_back_labeled.png | bv512.json | mapped 2026-10-15; every position hovered in Reason (fold arrows, meters, display, small light, back icons: no tooltip). No Scope block in our remotemap, so no knob slots/CC; names from remote-vocab.json. Only 16 of the 32 Remote band levels are on the panel | [bv512-digital-vocoder.md](bv512-digital-vocoder.md) |
| Rytmik Drum Machine | RYTM | rytmik_front_labeled.png | rytmik_back_labeled.png | rytmik.json | mapped 2026-10-15 (main panel with KICK selected + back); every position hovered in Reason (sample readouts, waveform/filter displays, faders, pads: no tooltip). No Remote map for Rytmik: no slots/CC. Other drums' sample section views not mapped separately | [rytmik-drum-machine.md](rytmik-drum-machine.md) |
| MIDI Out Device | MIDO | midi-out_front_labeled.png | midi-out_back_labeled.png | midi-out.json | mapped 2026-10-15; every position hovered in Reason (wheel-side lights, arrows, device menu, tape: no tooltip). No Remote map: no slots/CC. Device menu not opened | [midi-out-device.md](midi-out-device.md) |
| Elements DS-LFO (AirRaid) | DSLF | elements-ds-lfo_front_labeled.png | elements-ds-lfo_back_labeled.png | elements-ds-lfo.json | mapped 2026-10-15 (AirRaid Rack Extension, no Remote map); every position hovered in Reason (fold arrow, shape arrows, LFO 2 SYNC/MODE: no tooltip) | [elements-ds-lfo-airraid.md](elements-ds-lfo-airraid.md) |
| Morfin XF Crossfader (Groovy Melon) | MORF | morfin-xf_front_labeled.png | morfin-xf_back_labeled.png | morfin-xf.json | mapped 2026-10-15 (Groovy Melon Rack Extension, no Remote map); every position hovered in Reason (fold arrow: no tooltip). Fade-type light ring not mapped separately | [morfin-xf-crossfader-groovy-melon.md](morfin-xf-crossfader-groovy-melon.md) |
| A/B 12 Audio Out Switch (pongasoft) | AB12 | ab12-audio-out_front_labeled.png | ab12-audio-out_back_labeled.png | ab12-audio-out.json | mapped 2026-10-15 (pongasoft Rack Extension, no Remote map); front: every knob hovered, buttons/displays/A-B/lights no tooltip. Back: A1/B1 gate jacks hovered, other gate jacks by row pattern (marked) | [a-b-12-audio-out-switch-pongasoft.md](a-b-12-audio-out-switch-pongasoft.md) |
| A/B Audio & CV Switch (pongasoft) | ABSW | ab-switch_front_labeled.png | ab-switch_back_labeled.png | ab-switch.json | mapped 2026-10-15 (pongasoft RE, no Remote map); back jacks all hovered; front knob/light tooltips partly ambiguous (marked) | [a-b-audio-cv-switch-pongasoft.md](a-b-audio-cv-switch-pongasoft.md) |
| CVA-7 CV Analyzer (pongasoft) | CVA7 | cva-7_front_labeled.png | cva-7_back_labeled.png | cva-7.json | mapped 2026-10-15 (pongasoft RE, no Remote map); front all hovered; back: CV In/trim/aux outs hovered, CV Out slider/jack 1-4 by row pattern (marked) | [cva-7-cv-analyzer-pongasoft.md](cva-7-cv-analyzer-pongasoft.md) |
| RE 181 Mid/Side Audio Converter | RE18 | re181-mid-side_front_labeled.png | re181-mid-side_back_labeled.png | re181-mid-side.json | mapped 2026-10-15 (Red Rock Sound RE, no Remote map); back jacks all hovered; front: only the two LISTEN buttons have tooltips, rest are meters/lights | [re-181-mid-side-audio-converter.md](re-181-mid-side-audio-converter.md) |
| Select CV Switch (Robotic Bean) | SELC | select-cv-switch_front_labeled.png | select-cv-switch_back_labeled.png | select-cv-switch.json | mapped 2026-10-15 (Robotic Bean RE, no Remote map); back: all named by tooltip (jacks 3-7 by pattern, marked); front buttons/displays have no tooltips | [select-cv-switch-robotic-bean.md](select-cv-switch-robotic-bean.md) |
| RPSpec Spectrogram (Rob Papen) | RPSP | rpspec_front_labeled.png | rpspec_back_labeled.png | rpspec.json | mapped 2026-10-15 (Rob Papen RE, no Remote map); 4 front controls have tooltips; view icons/mode/readouts have none and were not clicked; back jacks cabled (own names not read) | [rpspec-spectrogram-rob-papen.md](rpspec-spectrogram-rob-papen.md) |
| Elements Splitter (AirRaid) | SPLT | elements-splitter_front_labeled.png | elements-splitter_back_labeled.png | elements-splitter.json | mapped 2026-10-15 (AirRaid RE 'Elements Splitter 2', no Remote map); nearly all hovered; a few On/M/S buttons gave no tooltip (marked); a few CV jacks by neighbour pattern (marked) | [elements-splitter-airraid.md](elements-splitter-airraid.md) |
| kHs Chorus (kiloHearts) | KHSC | khs-chorus_front_labeled.png | khs-chorus_back_labeled.png | khs-chorus.json | mapped 2026-10-15 (kiloHearts RE, no Remote map); every position hovered in Reason (tape/logo: no tooltip) | [khs-chorus-kilohearts.md](khs-chorus-kilohearts.md) |
| Efektor Silencer Noise Gate (Kuassa) | SILN | efektor-silencer_front_labeled.png | efektor-silencer_back_labeled.png | efektor-silencer.json | mapped 2026-10-15 (Kuassa RE, no Remote map); front all hovered; back audio jacks hovered, 4 small jacks near INPUT/OUTPUT labels had no tooltip and are not identified | [efektor-silencer-noise-gate-kuassa.md](efektor-silencer-noise-gate-kuassa.md) |


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
SOURCE FILE: a-b-12-audio-out-switch-pongasoft.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/chapters/a-b-12-audio-out-switch-pongasoft.md
=====================================================

## A/B 12 Audio Out Switch (pongasoft) — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AB12-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip (fold arrow); checked by eye |
| AB12-F-D05 | AB12AUDOUT 1 tape | Device name tape (vertical, left edge) | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D01 | A1 display | Name display for output A1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K01 | A1 VOLUME | Volume of output A1 | — | — | click only | tooltip "Volume [A1]: 0.00 dB" |
| AB12-F-B02 | A1 button | Switch button for output A1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D06 | A2 display | Name display for output A2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K05 | A2 VOLUME | Volume of output A2 | — | — | click only | tooltip "Volume [A2]: 0.00 dB" |
| AB12-F-B06 | A2 button | Switch button for output A2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D11 | A3 display | Name display for output A3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K10 | A3 VOLUME | Volume of output A3 | — | — | click only | tooltip "Volume [A3]: 0.00 dB" |
| AB12-F-B10 | A3 button | Switch button for output A3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B03 | A4 button | Switch button for output A4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K02 | A4 VOLUME | Volume of output A4 | — | — | click only | tooltip "Volume [A4]: 0.00 dB" |
| AB12-F-D02 | A4 display | Name display for output A4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B07 | A5 button | Switch button for output A5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K06 | A5 VOLUME | Volume of output A5 | — | — | click only | tooltip "Volume [A5]: 0.00 dB" |
| AB12-F-D07 | A5 display | Name display for output A5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B11 | A6 button | Switch button for output A6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K11 | A6 VOLUME | Volume of output A6 | — | — | click only | tooltip "Volume [A6]: 0.00 dB" |
| AB12-F-D12 | A6 display | Name display for output A6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D03 | B1 display | Name display for output B1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K03 | B1 VOLUME | Volume of output B1 | — | — | click only | tooltip "Volume [B1]: 0.00 dB" |
| AB12-F-B04 | B1 button | Switch button for output B1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D09 | B2 display | Name display for output B2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K08 | B2 VOLUME | Volume of output B2 | — | — | click only | tooltip "Volume [B2]: 0.00 dB" |
| AB12-F-B08 | B2 button | Switch button for output B2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D13 | B3 display | Name display for output B3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K12 | B3 VOLUME | Volume of output B3 | — | — | click only | tooltip "Volume [B3]: 0.00 dB" |
| AB12-F-B15 | B3 button | Switch button for output B3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B05 | B4 button | Switch button for output B4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K04 | B4 VOLUME | Volume of output B4 | — | — | click only | tooltip "Volume [B4]: 0.00 dB" |
| AB12-F-D04 | B4 display | Name display for output B4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B09 | B5 button | Switch button for output B5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K09 | B5 VOLUME | Volume of output B5 | — | — | click only | tooltip "Volume [B5]: 0.00 dB" |
| AB12-F-D10 | B5 display | Name display for output B5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B16 | B6 button | Switch button for output B6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K13 | B6 VOLUME | Volume of output B6 | — | — | click only | tooltip "Volume [B6]: 0.00 dB" |
| AB12-F-D14 | B6 display | Name display for output B6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D08 | A / B indicator lights | Shows which bank is active (A or B light) | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K07 | A/B big knob | Bank switch knob (no tooltip) | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B12 | MODE SELECT Single | Mode select: Single / Multi / Instr (tooltip 'Mode Select' on all three) | — | — | click only | tooltip "Mode Select" |
| AB12-F-B13 | MODE SELECT Multi | Mode select: Single / Multi / Instr | — | — | click only | tooltip "Mode Select" |
| AB12-F-B14 | MODE SELECT Instr | Mode select: Single / Multi / Instr | — | — | click only | tooltip "Mode Select" |
| AB12-F-B17 | SOFTEN | Soften (smooths switching) | — | — | click only | tooltip "Soften" |
| AB12-F-D15 | SINGLE OV light | Single override light | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D16 | BANK OV light | Bank override light | — | — | click only | no tooltip in Reason (hovered 2 s) |

## A/B 12 Audio Out Switch (pongasoft) — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AB12-B-J01 | Audio Out A1 Left (mono) | Audio output A1, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A1] Output Left" |
| AB12-B-J02 | Audio Out A2 Left (mono) | Audio output A2, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A2] Output Left" |
| AB12-B-J03 | Audio Out A3 Left (mono) | Audio output A3, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A3] Output Left" |
| AB12-B-J04 | Audio Out A4 Left (mono) | Audio output A4, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A4] Output Left" |
| AB12-B-J05 | Audio Out A5 Left (mono) | Audio output A5, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A5] Output Left" |
| AB12-B-J06 | Audio Out A6 Left (mono) | Audio output A6, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A6] Output Left" |
| AB12-B-J07 | Audio Out B1 Left (mono) | Audio output B1, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B1] Output Left" |
| AB12-B-J08 | Audio Out B2 Left (mono) | Audio output B2, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B2] Output Left" |
| AB12-B-J09 | Audio Out B3 Left (mono) | Audio output B3, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B3] Output Left" |
| AB12-B-J10 | Audio Out B4 Left (mono) | Audio output B4, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B4] Output Left" |
| AB12-B-J11 | Audio Out B5 Left (mono) | Audio output B5, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B5] Output Left" |
| AB12-B-J12 | Audio Out B6 Left (mono) | Audio output B6, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B6] Output Left" |
| AB12-B-J14 | Audio Out A1 Right | Audio output A1, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A1] Output Right" |
| AB12-B-J15 | Audio Out A2 Right | Audio output A2, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A2] Output Right" |
| AB12-B-J16 | Audio Out A3 Right | Audio output A3, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A3] Output Right" |
| AB12-B-J17 | Audio Out A4 Right | Audio output A4, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A4] Output Right" |
| AB12-B-J18 | Audio Out A5 Right | Audio output A5, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A5] Output Right" |
| AB12-B-J19 | Audio Out A6 Right | Audio output A6, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A6] Output Right" |
| AB12-B-J20 | Audio Out B1 Right | Audio output B1, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B1] Output Right" |
| AB12-B-J21 | Audio Out B2 Right | Audio output B2, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B2] Output Right" |
| AB12-B-J22 | Audio Out B3 Right | Audio output B3, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B3] Output Right" |
| AB12-B-J23 | Audio Out B4 Right | Audio output B4, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B4] Output Right" |
| AB12-B-J24 | Audio Out B5 Right | Audio output B5, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B5] Output Right" |
| AB12-B-J25 | Audio Out B6 Right | Audio output B6, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B6] Output Right" |
| AB12-B-J27 | Gate In A1 | Gate input A1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In [A1]" |
| AB12-B-J29 | Gate In A2 | Gate input A2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A2]' assumed |
| AB12-B-J31 | Gate In A3 | Gate input A3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A3]' assumed |
| AB12-B-J33 | Gate In A4 | Gate input A4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A4]' assumed |
| AB12-B-J35 | Gate In A5 | Gate input A5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A5]' assumed |
| AB12-B-J37 | Gate In A6 | Gate input A6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A6]' assumed |
| AB12-B-J39 | Gate In B1 | Gate input B1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In [B1]" |
| AB12-B-J41 | Gate In B2 | Gate input B2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B2]' assumed |
| AB12-B-J43 | Gate In B3 | Gate input B3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B3]' assumed |
| AB12-B-J45 | Gate In B4 | Gate input B4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B4]' assumed |
| AB12-B-J47 | Gate In B5 | Gate input B5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B5]' assumed |
| AB12-B-J49 | Gate In B6 | Gate input B6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B6]' assumed |
| AB12-B-J28 | Gate Out A1 | Gate output A1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out [A1]" |
| AB12-B-J30 | Gate Out A2 | Gate output A2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A2]' assumed |
| AB12-B-J32 | Gate Out A3 | Gate output A3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A3]' assumed |
| AB12-B-J34 | Gate Out A4 | Gate output A4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A4]' assumed |
| AB12-B-J36 | Gate Out A5 | Gate output A5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A5]' assumed |
| AB12-B-J38 | Gate Out A6 | Gate output A6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A6]' assumed |
| AB12-B-J40 | Gate Out B1 | Gate output B1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out [B1]" |
| AB12-B-J42 | Gate Out B2 | Gate output B2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B2]' assumed |
| AB12-B-J44 | Gate Out B3 | Gate output B3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B3]' assumed |
| AB12-B-J46 | Gate Out B4 | Gate output B4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B4]' assumed |
| AB12-B-J48 | Gate Out B5 | Gate output B5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B5]' assumed |
| AB12-B-J50 | Gate Out B6 | Gate output B6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B6]' assumed |
| AB12-B-J13 | Main Audio In Left | Main audio input, left | — | — | cable: right-click jack > device > jack name | tooltip "Audio Input Left" |
| AB12-B-J26 | Main Audio In Right | Main audio input, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio Input Right" |
| AB12-B-J52 | CV In (single mode) | CV input for single mode | — | — | cable: right-click jack > device > jack name | tooltip "CV in Switch State (single)" |
| AB12-B-B04 | Keyboard Single switch | Keyboard control of single mode: Disabled / Enabled | — | — | click/drag only (no Remote item) | tooltip "Keyboard (Single)" |
| AB12-B-B02 | Volume Change Filter switch | Volume change filter Off / On | — | — | click/drag only (no Remote item) | tooltip "Volume Change Filter" |
| AB12-B-J51 | CV Banks In | CV input for banks | — | — | cable: right-click jack > device > jack name | tooltip "CV in" |
| AB12-B-B03 | CV Banks mapping switch | Bank CV mapping: Unipolar / Bipolar / Note | — | — | click/drag only (no Remote item) | tooltip "Bank CV Mapping: Bipolar" |
| AB12-B-D02 | QR code | pongasoft QR code (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 2 s) |
| AB12-B-D03 | Power switch (drawn) | Power connector area (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 2 s) |
| AB12-B-D01 | AB12AUDOUT 1 tape (back) | Device name tape on the back | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 2 s) |
| AB12-B-B01 | (triangle, back) | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip (fold arrow); checked by eye |

=== END OF PART ===
