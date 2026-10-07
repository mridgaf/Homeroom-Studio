"""Generates tools/specs/<slug>.json for Batch A half-rack devices (positions measured by eye from _captures_batchA pictures)."""
import json
def common(tapeX,tapeW,tape):
    return [["Bypass/On/Off","3-way device switch","Enabled",None,[37,45],[13,20],"B","high",""],
     ["(LED column)","Input level meter","Peak Meter",None,[37,130],[9,42],"D","medium","vocab item 'Peak Meter' assumed by position"],
     [tape+" tape","Device name tape","Device Name",None,[tapeX,38],[tapeW,15],"D","high",""]]
def front(slotE,tapeX,tapeW,tape,rest):
    c=common(tapeX,tapeW,tape); c[0][3]=slotE; return c+rest
def jacks(iny,outy,xs=(585,655)):
    return [["Left (In)","Audio input left","J",[xs[0],iny],[22,22],""],["Right (In)","Audio input right","J",[xs[1],iny],[22,22],""],
            ["Left (Out)","Audio output left","J",[xs[0],outy],[22,22],""],["Right (Out)","Audio output right","J",[xs[1],outy],[22,22],""]]
def trim(label,x,y): return ["(trim)","Amount knob for "+label,"K",[x,y],[20,20],"trim next to CV jack; matched by position"]
def cv(label,x,y): return [label+" (CV in)","CV input for "+label,"J",[x,y],[17,17],""]
def tapeb(tape,x,y,w=105): return [tape+" tape","Device name tape (back)","D",[x,y],[w,16],""]
def K(l,w,n,s,x,y,r=34,c="high",why=""): return [l,w,n,s,[x,y],[r,r],"K",c,why]
S={}
S["ecf-42"]=("ECF-42 Envelope Controlled Filter","ECF42",front(3,505,82,"FILTER 1",[
 ["GATE (light)","Gate light: lights when the envelope is triggered (display)","",None,[722,38],[14,14],"D","medium","likely tied to Remote 'Trigger'; confirm by hover"],
 K("FREQ","Filter frequency","Frequency",5,163,125),K("RES","Filter resonance","Resonance",8,255,125),
 K("ENV.AMT","How far the envelope moves the filter","Env Amount",4,345,125),K("VEL.","How much note velocity opens the filter","Velocity",11,437,125),
 ["BP12/LP12/LP24 lights + MODE","MODE button: cycles filter type BP 12, LP 12, LP 24 (lights show which)","Mode",6,[505,122],[22,50],"B","medium","button and its three lights boxed together"],
 K("A (Envelope)","Envelope attack","Attack",1,622,125),K("D (Envelope)","Envelope decay","Decay",2,712,125),
 K("S (Envelope)","Envelope sustain","Sustain",9,805,125),K("R (Envelope)","Envelope release","Release",7,895,125)]),
 [tapeb("FILTER 1",293,38),trim("Freq CV",82,152),cv("Freq",131,152),trim("Decay CV",212,152),cv("Decay",260,152),trim("Res CV",340,152),cv("Res",388,152),
  ["Env. Gate (CV in)","Gate input for the envelope","J",[483,152],[17,17],""],
  ["Left (In)","Audio input left","J",[580,150],[22,22],""],["Right (In)","Audio input right","J",[651,150],[22,22],""],
  ["Left (Out)","Audio output left","J",[734,150],[22,22],""],["Right (Out)","Audio output right","J",[806,150],[22,22],""]])
S["peq-2"]=("PEQ-2 Two Band Parametric EQ","PEQ2",front(1,485,108,"EQ 1",[
 ["(EQ display)","Frequency response graph, 31 Hz to 16k, +18 to -18 dB (display)","",None,[297,128],[182,38],"D","medium","display only"],
 K("A FREQ","Band A frequency","Filter A Freq",2,678,60,32),K("A Q","Band A width (Q)","Filter A Q",4,780,60,32),K("A GAIN","Band A boost/cut","Filter A Gain",3,880,60,32),
 K("B FREQ","Band B frequency","Filter B Freq",5,678,150,32),K("B Q","Band B width (Q)","Filter B Q",8,780,150,32),K("B GAIN","Band B boost/cut","Filter B Gain",6,880,150,32),
 ["B (button)","Band B on/off (light shows on)","Filter B On/Off",7,[576,142],[14,30],"B","high",""]]),
 [cv("Freq 1",92,102),cv("Freq 2",220,102),trim("Freq 1 CV",90,158),trim("Freq 2 CV",220,158),tapeb("EQ 1",368,155,108)]+jacks(82,138))
S["ph-90"]=("PH-90 Phaser","PH90",front(1,500,80,"PHASER 1",[
 K("FREQ","Phaser frequency","Frequency",3,163,125),K("SPLIT","Split of the phase stages","Split",7,305,125),K("WIDTH","Stereo width","Width",8,445,125),
 K("RATE","LFO speed","Rate",6,580,125),["SYNC","LFO tempo sync on/off (light shows on)","LFO Sync Enable",5,[669,122],[14,32],"B","high",""],
 K("F. MOD","How much the LFO moves the frequency","Frequency Modulation",4,763,125),K("FEEDBACK","Feedback amount","Feedback",2,887,125)]),
 [tapeb("PHASER 1",275,38),trim("Freq CV",103,150),cv("Freq",151,150),trim("Rate CV",228,150),cv("Rate",275,150),
  ["Left (In)","Audio input left","J",[500,150],[22,22],""],["Right (In)","Audio input right","J",[573,150],[22,22],""],
  ["Left (Out)","Audio output left","J",[686,150],[22,22],""],["Right (Out)","Audio output right","J",[757,150],[22,22],""]])
S["rv-7"]=("RV-7 Digital Reverb","RV7",front(5,487,108,"REVERB 1",[
 ["(algorithm display)","Shows the reverb type (Hall, etc.)","",None,[163,128],[98,22],"D","medium","display"],
 ["(up/down arrows)","Step through reverb types","Algorithm",1,[285,128],[18,26],"B","medium","Remote 'Algorithm' assumed to be this selector; confirm by hover"],
 K("SIZE","Room size","Size",6,438,125),K("DECAY","Reverb tail length","Decay",3,588,125),K("DAMP","High-frequency damping","Damping",2,737,125),K("DRY/WET","Balance dry and reverb","Dry/Wet",4,882,125)]),
 [cv("Decay",92,102),trim("Decay CV",90,158),tapeb("REVERB 1",368,155,108)]+jacks(85,138,(583,653)))
S["un-16"]=("UN-16 Unison","UN16",front(3,490,108,"UNISON 1",[
 ["16/8/4 lights + VOICE COUNT","VOICE COUNT button: cycles 16, 8, 4 voices (lights show which)","Voice Count",4,[308,115],[22,56],"B","medium","button and its three lights boxed together"],
 K("DETUNE","Detune amount","Detune",1,618,125,36),K("DRY/WET","Balance dry and unison signal","Dry/Wet",2,886,125,36)]),
 [cv("Detune",95,102),trim("Detune CV",95,158),tapeb("UNISON 1",372,155)]+jacks(85,138))
for slug,(dev,pre,fr,bk) in S.items():
    json.dump(dict(device=dev,slug=slug,prefix=pre,remote_scope="Propellerheads / "+dev,front_raw=f"_captures_batchA/{slug}_front_raw.jpg",
      back_raw=f"_captures_batchA/{slug}_back_raw.jpg",out_dir=".",date="2026-10-07",front=fr,back=bk),open(f"tools/specs/{slug}.json","w"),indent=0)
