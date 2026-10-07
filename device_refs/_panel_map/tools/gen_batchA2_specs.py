"""Specs for MClass devices (Batch A). Positions in picture pixels, by eye."""
import json
def K(l,w,n,s,x,y,r=42,c="high",why=""): return [l,w,n,s,[x,y],[r,r],"K",c,why]
def B(l,w,n,s,x,y,hw=14,hh=14,c="high",why=""): return [l,w,n,s,[x,y],[hw,hh],"B",c,why]
def D(l,w,n,x,y,hw,hh,c="high",why=""): return [l,w,n,None,[x,y],[hw,hh],"D",c,why]
def base(slotE,tape,ty=120):
    return [B("Bypass/On/Off","3-way device switch","Enabled",slotE,84,38,14,22),
            D("(LED column)","Input level meter","Peak Meter",86,100,10,32,"medium","vocab item 'Peak Meter' assumed by position"),
            D(tape+" tape","Device name tape","Device Name",282,ty,80,12)]
def J(l,w,x,y): return [l,w,"J",[x,y],[22,22],""]
def tb(tape,x=275,y=113): return [tape+" tape","Device name tape (back)","D",[x,y],[80,12],""]
def io(ix=(423,480),ox=(552,610),y=80):
    return [J("Audio Input L","Audio input left",ix[0],y),J("Audio Input R","Audio input right",ix[1],y),J("Audio Output L","Audio output left",ox[0],y),J("Audio Output R","Audio output right",ox[1],y)]
S={}
S["mclass-compressor"]=("MClass Compressor","MCMP",base(8,"M COMP 2")+[
 K("INPUT GAIN","Level into the compressor","Input Gain",4,465,75,44),K("THRESHOLD","Level above which compression starts","Threshold",1,590,75,44),
 B("SOFT KNEE","Soft knee on/off","Soft Knee",2,657,75),K("RATIO","Compression ratio, 1:1 to infinity:1","Ratio",3,770,75,46),
 D("GAIN (meter)","Gain reduction meter, 0 to -20 dB","Gain Meter",870,68,20,45),
 B("ACTIVE (sidechain)","Sidechain on/off (light shows on)","Sidechain Active",None,1010,38,12,12),B("SOLO (sidechain)","Listen to the sidechain signal","Sidechain Solo",None,1012,82,12,12),
 K("ATTACK","How fast compression kicks in","Attack",5,1118,75,44),K("RELEASE","How fast compression lets go","Release",6,1217,75,44),
 B("ADAPT RELEASE","Adaptive release on/off","Adapt",None,1281,75),K("OUTPUT GAIN","Level out of the compressor","Output Gain",7,1380,75,44)],
 [tb("M COMP 2")]+io()+[J("Sidechain In L","Sidechain input left",727,80),J("Sidechain In R","Sidechain input right",788,80),J("Gain Reduction CV Out","CV output following the gain reduction",876,80)])
S["mclass-maximizer"]=("MClass Maximizer","MMAX",base(2,"M MAXIMIZER 1")+[
 K("INPUT GAIN","Level into the maximizer","Input Gain",3,425,75,44),B("LIMITER","Limiter on/off","Limiter Enable",4,500,26,12,12),
 B("4ms LOOK AHEAD","Look ahead on/off","Look Ahead Enable",5,546,73),D("GAIN (meter)","Gain reduction meter, 0 to -20 dB","Gain Meter",630,70,20,48),
 B("ATTACK (FAST/MID/SLOW)","Attack speed: 3 buttons, pick one","Attack Speed",1,718,77,16,42,"medium","3 buttons act as one control"),
 B("RELEASE (FAST/SLOW/AUTO)","Release speed: 3 buttons, pick one","Release Speed",9,795,77,16,42,"medium","3 buttons act as one control"),
 K("OUTPUT GAIN","Level out of the maximizer","Output Gain",6,905,75,44),B("SOFT CLIP","Soft clip on/off","Soft Clip Enable",11,983,26,12,12),
 K("AMOUNT (Soft Clip)","How much soft clipping","Soft Clip Amount",10,1050,75,42),
 B("PEAK / VU","Output meter mode: Peak or VU","Output Level Meter Mode",None,1148,72,14,36,"medium","2 buttons act as one control"),
 D("OUTPUT LEVEL L","Output level meter, left bar","Output Level Left",1330,62,150,10,"medium","left/right bars matched by order"),D("OUTPUT LEVEL R","Output level meter, right bar","Output Level Right",1330,83,150,10,"medium","left/right bars matched by order")],
 [tb("M MAXIMIZER 1")]+io())
S["mclass-stereo-imager"]=("MClass Stereo Imager","MSIM",base(1,"M STEREO 1")+[
 K("LO BAND (width)","Low band stereo width, mono to wide","Low Width",5,630,75,42),B("LO BAND ACTIVE","Low band on/off (light shows on)","Low Band Active",4,773,57,12,12),
 D("(Lo width meter)","Low band width meter","Low Width Meter",640,122,88,13),
 K("X-OVER FREQ","Where the low and high bands split, 100 Hz to 6 kHz","X-Over Frequency",8,870,72,40),
 B("HI BAND ACTIVE","High band on/off (light shows on)","High Band Active",2,968,57,12,12),K("HI BAND (width)","High band stereo width, mono to wide","High Width",3,1100,75,42),
 D("(Hi width meter)","High band width meter","High Width Meter",1100,122,88,13),
 B("SOLO (HI/LO/NORMAL)","Solo mode: 3 buttons, pick one","Solo Mode",7,1250,79,16,36,"medium","3 buttons act as one control")],
 [tb("M STEREO 1")]+io()+[J("Separate Out L","Separate output left",727,80),J("Separate Out R","Separate output right",788,80),
  ["Hi Band / Lo Band switch","Which band the Separate Out carries","B",[838,82],[14,22],"","", "Separate Out Mode",6]])
EQ=[B("Bypass/On/Off","3-way device switch","Enabled",1,97,38,14,22),D("(LED column)","Input level meter","Peak Meter",87,100,10,32,"medium","vocab item 'Peak Meter' assumed by position"),
 D("MEQ 1 tape","Device name tape (vertical)","Device Name",60,135,14,58),D("(EQ display)","Frequency response graph, 39 Hz to 20 kHz, +/-18 dB","",472,155,335,92,"medium","display only"),
 B("LO CUT","Low cut on/off","Low Cut Enable",6,852,26,12,12)]
cols=[("LO SHELF","Low Shelf",933,1010,7,8,9,10),("PARAM 1","Parametric 1",1078,1153,11,12,13,14),("PARAM 2","Parametric 2",1220,1300,15,16,17,18),("HI SHELF","Hi Shelf",1365,1443,2,3,4,5)]
for lab,nm,ex,kx,se,sf,sg,sq in cols:
    EQ+=[B(lab+" (button)",nm+" on/off",nm+" Enable",se,ex,26,12,12),K(lab+" FREQ",nm+" frequency",nm+" Frequency",sf,kx,72,36),
         K(lab+" GAIN",nm+" boost/cut",nm+" Gain",sg,kx,157,32),K(lab+" Q",nm+" width (Q)",nm+" Q",sq,kx,238,36)]
S["mclass-equalizer"]=("MClass Equalizer","MEQ",EQ,[["MEQ 1 tape","Device name tape (back, vertical)","D",[57,135],[14,52],""]]+io((558,618),(735,795),207))
for slug,(dev,pre,fr,bk) in S.items():
    json.dump(dict(device=dev,slug=slug,prefix=pre,remote_scope="Propellerheads / "+dev,front_raw=f"_captures_batchA/{slug}_front_raw.jpg",
      back_raw=f"_captures_batchA/{slug}_back_raw.jpg",out_dir=".",date="2026-10-07",front=fr,back=bk),open(f"tools/specs/{slug}.json","w"))
