"""Specs for Channel EQ, Channel Dynamics, Master Bus Compressor (Batch A, last 3). Positions in picture pixels, by eye."""
import json
def K(l,w,n,s,x,y,r=34,c="high",why=""): return [l,w,n,s,[x,y],[r,r],"K",c,why]
def B(l,w,n,s,x,y,hw=24,hh=15,c="high",why=""): return [l,w,n,s,[x,y],[hw,hh],"B",c,why]
def D(l,w,n,x,y,hw,hh,c="high",why=""): return [l,w,n,None,[x,y],[hw,hh],"D",c,why]
def J(l,w,x,y): return [l,w,"J",[x,y],[22,22],""]
def T(l,w,x,y,hw=26,hh=26): return [l,w,"K",[x,y],[hw,hh],""]
def DB(l,w,x,y,hw=22,hh=22): return [l,w,"D",[x,y],[hw,hh],""]
def tape(t,y): return D(t+" tape","Device name tape (vertical)","Device Name",60,y,16,60)
def byp(slot,y=48): return B("Bypass/On/Off","3-way device switch","Enabled",slot,98,y,14,24)
S={}
S["channel-eq"]=("Channel EQ","CEQ",[
 byp(2,60),tape("CHANEQ 1",170),
 B("HPF ON","High-pass filter on/off","HPF On",11,220,155),K("HPF Hz","High-pass filter frequency","HPF Frequency",10,217,224,36),
 B("LPF ON","Low-pass filter on/off","LPF On",19,314,155),K("LPF kHz","Low-pass filter frequency","LPF Frequency",18,318,225,36),
 K("LF dB","Low shelf boost/cut","LF Gain",14,445,125),D("(LF light)","Light beside the LF dB knob","",508,120,12,12,"medium","meaning not confirmed"),
 B("LF Bell","Low band bell/shelf switch","LF Bell On",12,425,233),K("LF Hz","Low shelf frequency, 40 to 600 Hz","LF Frequency",13,520,222),
 K("LMF dB","Low-mid boost/cut","LMF Gain",16,627,123),D("(LMF light)","Light beside the LMF dB knob","",682,120,12,12,"medium","meaning not confirmed"),
 K("LMF Q","Low-mid width (Q)","LMF Q",17,746,122),K("LMF kHz","Low-mid frequency, 200 Hz to 2 kHz","LMF Frequency",15,683,222),
 B("E Mode","E (SSL-style) curves on/off","E Mode On",1,813,233),
 K("HMF dB","High-mid boost/cut","HMF Gain",8,888,123),D("(HMF light)","Light beside the HMF dB knob","",942,120,12,12,"medium","meaning not confirmed"),
 K("HMF Q","High-mid width (Q)","HMF Q",9,1007,122),K("HMF kHz","High-mid frequency, 0.6 to 7 kHz","HMF Frequency",7,950,222),
 K("HF dB","High shelf boost/cut","HF Gain",6,1185,123),D("(HF light)","Light beside the HF dB knob","",1114,124,12,12,"medium","meaning not confirmed"),
 K("HF kHz","High shelf frequency, 1.5 to 22 kHz","HF Frequency",5,1116,222),B("HF Bell","High band bell/shelf switch","HF Bell On",4,1210,233),
 K("Gain","Output gain","Gain",3,1388,222),D("(LED column)","Level meter lights","",1457,205,12,62,"medium","meaning not confirmed")],
 [DB("CHANEQ 1 tape","Device name tape (back, vertical)",60,170,16,60),
  T("HMF Gain CV trim","CV amount for HMF Gain",410,93),J("HMF Gain CV In","CV input for HMF Gain",458,95),
  T("HMF Freq CV trim","CV amount for HMF Frequency",410,136),J("HMF Freq CV In","CV input for HMF Frequency",458,138),
  T("HPF Freq CV trim","CV amount for HPF Frequency",190,193),J("HPF Freq CV In","CV input for HPF Frequency",238,195),
  T("LMF Gain CV trim","CV amount for LMF Gain",410,194),J("LMF Gain CV In","CV input for LMF Gain",458,196),
  T("LPF Freq CV trim","CV amount for LPF Frequency",190,237),J("LPF Freq CV In","CV input for LPF Frequency",238,239),
  T("LMF Freq CV trim","CV amount for LMF Frequency",410,237),J("LMF Freq CV In","CV input for LMF Frequency",458,239),
  J("Input L","Audio input left",1060,245),J("Input R","Audio input right",1116,245),
  J("Output L","Audio output left",1262,245),J("Output R","Audio output right",1318,245),
  DB("(routing icon 1)","Small icon at top right",1405,75,14,18),DB("(routing icon 2)","Small icon at right",1405,118,14,18)])
S["channel-dynamics"]=("Channel Dynamics","CDYN",[
 byp(7),tape("CHANDYN 1",170),
 B("Comp ON","Compressor on/off","Comp On",2,221,45),B("Comp Peak","Compressor peak detection on/off","Comp Peak On",3,317,113),B("Comp Fast","Compressor fast attack on/off","Comp Fast On",1,519,113),
 K("Input Gain","Level into the compressor, -18 to +18 dB","Input Gain",15,198,215),K("Ratio","Compression ratio, 1 to infinity","Comp Ratio",4,318,215),
 K("Thresh (comp)","Level above which compression starts","Comp Threshold",6,426,215),K("Release (comp)","How fast compression lets go","Comp Release",5,525,215),
 D("(Comp light column)","Compressor gain reduction lights","",603,185,12,45,"medium","meaning not confirmed"),
 B("Gate ON","Gate/expander on/off","Gate On",11,683,45),B("Exp.","Expander instead of gate on/off","Gate Exp On",8,737,113),
 K("Hold","Gate hold time, 0 to 4 s","Gate Hold",10,855,110),B("Gate Fast","Gate fast release on/off","Gate Fast On",9,954,113),
 K("Range","Gate range, 0 to 40 dB","Gate Range",12,741,215),K("Thresh (gate)","Level below which the gate closes","Gate Threshold",14,853,215),K("Release (gate)","How fast the gate closes","Gate Release",13,953,215),
 D("(Gate light column)","Gate activity lights","",1052,185,12,45,"medium","meaning not confirmed"),
 D("Connected (light)","Sidechain cable connected light","",1303,160,10,10),D("Active (light)","Sidechain active light","",1303,188,10,10),
 B("Sidechain","Sidechain on/off","Sidechain",17,1300,220,18,12),K("Mix","Dry/wet mix","Mix",16,1432,193,36)],
 [DB("CHANDYN 1 tape","Device name tape (back, vertical)",60,160,16,60),
  J("Comp Gain Reduction CV Out","CV output following compressor gain reduction",296,186),J("Gate Gain CV Out","CV output following gate gain",296,227),
  J("Sidechain In L","Sidechain input left",1262,95),J("Sidechain In R","Sidechain input right",1320,95),
  J("Input L","Audio input left",1060,235),J("Input R","Audio input right",1117,235),
  J("Output L","Audio output left",1262,235),J("Output R","Audio output right",1320,235),
  DB("(routing icon 1)","Small icon at top right",1405,60,14,18),DB("(routing icon 2)","Small icon at right",1405,102,14,18)])
S["master-bus-compressor"]=("Master Bus Compressor","MBC",[
 byp(2),tape("MASTERCOMP 1",170),
 K("Threshold","Level above which compression starts, -30 to 0 dB","Threshold",9,449,82),K("Ratio","Compression ratio, 2 to 10","Ratio",6,443,208),
 K("Input Gain","Level into the compressor, -18 to +18 dB","Input Gain",3,220,208),
 D("(VU meter)","Gain reduction meter, 0 to 20 dB","",640,128,100,55,"medium","meter shows no tooltip"),
 K("Attack-ms","Attack time, 0.1 to 30 ms","Attack",1,838,82),K("Release-sec","Release time, 0.1 to 1.2 s or AUTO","Release",7,840,208),
 K("Make-Up","Make-up gain, -5 to +15 dB","Make-Up Gain",4,1063,208),
 D("Connected (light)","Sidechain cable connected light","",1300,155,10,10),D("Active (light)","Sidechain active light","",1300,181,10,10),
 B("Sidechain","Sidechain on/off","Sidechain",8,1298,213,18,12),K("Mix","Dry/wet mix","Mix",5,1430,190,36)],
 [DB("MASTERCOMP 1 tape","Device name tape (back, vertical)",60,165,16,60),
  J("Comp Gain Reduction CV Out","CV output following gain reduction",296,212),
  J("Sidechain In L","Sidechain input left",1262,95),J("Sidechain In R","Sidechain input right",1320,95),
  J("Input L","Audio input left",1060,235),J("Input R","Audio input right",1117,235),
  J("Output L","Audio output left",1262,235),J("Output R","Audio output right",1320,235),
  DB("(routing icon 1)","Small icon at top right",1405,60,14,18),DB("(routing icon 2)","Small icon at right",1405,102,14,18)])
for slug,(dev,pre,fr,bk) in S.items():
    json.dump(dict(device=dev,slug=slug,prefix=pre,remote_scope="Propellerhead Software / "+dev,front_raw=f"_captures_batchA/{slug}_front_raw.jpg",
      back_raw=f"_captures_batchA/{slug}_back_raw.jpg",out_dir=".",date="2026-10-07",front=fr,back=bk),open(f"tools/specs/{slug}.json","w"))
