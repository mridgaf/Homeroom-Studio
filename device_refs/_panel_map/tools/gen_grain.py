import json
# Grain Sample Manipulator. Views: main (top half), lower (envelopes/LFO/matrix/fx row), 5 fx panels, back.
NT="no tooltip in Reason (hovered 1.2 s)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists but is beyond the 48 knob slots of our remotemap (not mapped)"
INF="not hovered; same column/row pattern as the hovered row 1 (name inferred from table order)"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/grain_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
def mk(tr,hwscale):
    # tr: screen->picture px
    return tr
class View:
    def __init__(s,ox,oy,k): s.ox,s.oy,s.k=ox,oy,k; s.rows=[]; s.chk={}
    def f(s,key,label,what,sx,sy,typ,hw,hh,name=None,slot=None,conf="high",why="",chk=None,mode=None,rowname=None):
        x=round((sx-s.ox)*s.k); y=round((sy-s.oy)*s.k)
        if name and slot is None and not why: why=NOSLOT
        s.rows.append([label,what,name,slot,[x,y],[round(hw*s.k),round(hh*s.k)],typ,conf,why]+([mode] if mode else []))
        s.chk[label]=chk or c(key)
V0=View(70,62,1.2833); VL=View(70,100,1.6333)
FX={n:View(740,275,1.7615) for n in ("phsr","dist","eq","dly","rev")}
f=V0.f
f("fold","(triangle)","Fold/unfold device",95,77,"B",8,8,conf="medium")
f("patchdisp","Patch display","Patch name display",485,79,"D",135,12,"Patch Name",conf="medium",why="Remote item 'Patch Name'; no tooltip; NOT proven")
f("patcharrows","(patch arrows)","Previous / next patch",642,79,"B",8,12,"Select Previous Patch",why="tooltip is for the upper half; lower half = Select Next Patch, not hovered")
f("patchfolder","(patch folder)","Browse patch",666,79,"B",9,9)
f("patchdisk","(patch disk)","Save patch",689,79,"B",9,9)
f("tape","Patch name tape","Patch name tape",760,79,"D",40,8,"Device Name",conf="medium",why="Remote item 'Device Name'; convention from earlier devices")
f("voices","VOICES display","Number of voices",884,82,"D",14,10)
f("voicesarrows","(voices arrows)","Voices down/up",908,82,"B",7,12,conf="medium")
f("master","MASTER VOLUME","Master volume",993,78,"K",14,14,"Master Volume",48)
f("filename","Sample name display","Name of the loaded sample",200,123,"D",95,10)
f("samplearrows","(sample arrows)","Previous / next sample",315,123,"B",9,12,why="tooltip is for the upper half; lower half not hovered")
f("samplefolder","(sample folder)","Browse samples",338,123,"B",9,9)
f("samplerec","(sample record)","Start sampling",361,123,"B",9,9,"Record Sample",conf="medium",why="tooltip 'Start sampling'; Remote 'Record Sample' matched by meaning; NOT proven")
f("sampleedit","(sample edit pencil)","Edit sample",389,123,"B",9,9)
f("overview","Overview waveform","Whole-sample overview with the zoom window",680,123,"D",255,12)
f("preview","(preview button)","Preview the sample",979,123,"B",11,11)
f("waveform","Main waveform","Waveform display: start, end and playhead",530,215,"D",410,60,"Position",2,"low","Remote 'Position' (slot 2) matched by meaning; display gave no tooltip; NOT proven")
f("startmark","START marker","Sample start marker",127,165,"B",8,8,conf="medium")
f("endmark","END marker","Sample end marker",938,246,"B",8,8,"End Pos",None,"low","Remote 'End Pos' matched by meaning; no tooltip; "+NOSLOT)
f("ypos","DISPLAY Y POS slider","Waveform display vertical position",960,200,"S",6,40,conf="medium")
f("motionmenu","MOTION menu (Envelope 1)","Motion envelope menu",180,283,"D",28,10,"Motion",5,"low","Remote 'Motion' (slot 5) matched by meaning; menu gave no tooltip; NOT proven")
f("speed","SPEED","Motion speed",350,283,"K",17,17,"Speed",7)
f("jitter","JITTER","Motion jitter",452,283,"K",17,17,"Jitter",6)
f("globalpos","GLOBAL POSITION","Global position on/off",549,283,"B",9,9,"Global Position",None)
f("rootkey","ROOT KEY note","Root key note",763,283,"D",20,10)
f("rootfine","ROOT KEY fine tune","Root key fine tune",805,283,"D",20,10)
f("rootset","SET","Set root key from analysis",857,283,"B",14,10)
f("analyzed","ANALYZED","Analysed pitch of the sample",907,283,"D",36,10)
f("grainsmenu","LONG GRAINS menu","Grain algorithm menu",120,329,"D",12,8,"Algorithm",1,"medium","Remote 'Algorithm' (slot 1) matched by meaning; menu gave no tooltip; NOT proven")
f("grainsmenu","FORMANT (other grain mode)","Formant knob: not visible in Long Grains mode",120,329,"K",12,8,"Formant",8,"low","Remote 'Formant' (slot 8); the knob appears only in another grain algorithm which was NOT captured; row placed on the algorithm menu; NOT proven",chk="not hovered: control is not on screen in Long Grains mode")
f("panspread","PAN SPREAD","Grain pan spread",140,383,"K",17,17,"Pan Spread",46)
f("pitchjitter","PITCH JITTER","Grain pitch jitter",140,458,"K",17,17,"Pitch Jitter")
f("graindisp","Grain shape display","Grain window shape",307,388,"D",90,50)
f("grainlen","GRAIN LENGTH","Grain length",246,455,"K",17,17,"Grain Length",3)
f("rate","RATE","Grain rate / spacing",312,455,"K",17,17,"Rate-Spacing",4)
f("xfade","X-FADE","Grain crossfade",373,455,"K",17,17,"XFade")
f("pitchoct","PITCH OCT","Pitch octave",461,364,"K",14,14,"Oct",10)
f("pitchsemi","PITCH SEMI","Pitch semitone",506,364,"K",14,14,"Semi",11)
f("pitchtune","PITCH TUNE","Pitch fine tune",548,364,"K",14,14,"Tune",12)
f("pitchkbd","PITCH KBD","Pitch keyboard tracking",592,364,"K",14,14,"Pitch Kbd")
f("samplelevel","SAMPLE LEVEL","Sample level",653,364,"K",14,14,"Sample Level",9)
f("sampleroute1","SAMPLE to FILTER (upper)","Route sample to filter",684,361,"B",8,8,"Sample To Filter")
f("sampleroute2","SAMPLE to FILTER (lower)","Route sample to filter (second button of the pair)",684,374,"B",8,8,"Sample To Filter",why="second half of a two-button switch; tooltip same as upper")
f("oscpower","OSCILLATOR on","Oscillator on/off",445,421,"B",9,9,"Osc On",13)
f("oscoct","OSC OCT","Oscillator octave",468,458,"K",14,14,"Osc Oct")
f("oscwavedisp","OSC WAVEFORM display","Oscillator waveform",521,461,"D",26,16,"Osc Wave",14,"medium","Remote 'Osc Wave' (slot 14); display gave no tooltip; matched by meaning")
f("oscwavearrows","(osc waveform arrows)","Oscillator waveform prev/next",554,461,"B",8,14,conf="medium")
f("oscmod","OSC MOD","Oscillator mod amount",590,458,"K",14,14,"Osc Mod")
f("osclevel","OSC LEVEL","Oscillator level",653,458,"K",14,14,"Osc Level",15)
f("oscroute1","OSC to FILTER (upper)","Route oscillator to filter",684,448,"B",8,8,"Osc To Filter")
f("oscroute2","OSC to FILTER (lower)","Route oscillator to filter (second button)",684,461,"B",8,8,"Osc To Filter",why="second half of a two-button switch; tooltip same as upper")
f("filtermenu","FILTER type menu (LP 12dB)","Filter type menu",720,344,"D",18,9,"Filter Type",16,"medium","Remote 'Filter Type' (slot 16); menu gave no tooltip; matched by meaning")
f("filterfreq","FILTER FREQ","Filter frequency",748,390,"K",22,22,"Filter Freq",17)
f("filterreso","FILTER RESO","Filter resonance",813,391,"K",14,14,"Filter Reso",18)
f("filterenv2","FILTER ENV 2","Filter envelope 2 amount",723,456,"K",12,12,"Filter Env2",19)
f("filtervel","FILTER VEL","Filter velocity",775,456,"K",12,12,"Filter Vel")
f("filterkbd","FILTER KBD","Filter keyboard tracking",820,456,"K",12,12,"Filter Kbd",20)
f("ampA","AMP A","Amp attack",888,400,"S",6,32,"Amp Attack",21)
f("ampD","AMP D","Amp decay",912,400,"S",6,32,"Amp Decay",22)
f("ampS","AMP S","Amp sustain",937,400,"S",6,32,"Amp Sustain",23,"medium","no tooltip after 3 tries; Remote 'Amp Sustain' (slot 23) matched by position in the A-D-S-R row")
f("ampR","AMP R","Amp release",961,400,"S",6,32,"Amp Release",24)
f("ampgain","AMP GAIN","Amp gain",877,470,"K",14,14,"Amp Gain",25)
f("ampvel","AMP VEL","Amp velocity",929,470,"K",12,12,why="tooltip 'Amp Velocity'; no such Remote item")
f("amppan","AMP PAN","Amp pan",972,470,"K",12,12,why="tooltip 'Pan'; no such Remote item")
# --- lower view
f=VL.f
f("keymode","KEY MODE switch","Key mode (POLY/RETRIG/LEGATO)",113,150,"B",8,22,"Key Mode",None)
f("portamode","PORTA switch (OFF/ON/AUTO)","Portamento mode",113,205,"B",8,22,"Portamento Mode",None)
f("portatime","PORTA TIME","Portamento time",112,254,"K",12,12,"Portamento",47)
f("envtab1","ENVELOPE tab 1 (Motion)","Select envelope 1",375,124,"B",38,12,"Env Select",None,"medium","Remote 'Env Select' matched by meaning (one of the 4 tabs); tabs gave no tooltip; "+NOSLOT)
f("envtab2","ENVELOPE tab 2 (Filter)","Select envelope 2",510,124,"B",38,12,chk=NT)
f("envtab3","ENVELOPE tab 3","Select envelope 3",620,124,"B",38,12,chk=NT)
f("envtab4","ENVELOPE tab 4","Select envelope 4",733,124,"B",38,12,chk=NT)
f("envdisplay","Envelope display","Envelope editor",440,215,"D",200,60)
f("envpreset","PRESET","Envelope preset",201,175,"B",24,18)
f("envedit","EDIT Y-POS","Edit envelope y position",201,236,"B",24,18)
f("envsustain","SUSTAIN","Envelope sustain",677,174,"B",30,12,conf="medium")
f("envloop","LOOP","Envelope loop",677,213,"B",30,16,conf="medium")
f("envkeytrig","KEY TRIG","Envelope key trigger",677,250,"B",30,10,conf="medium")
f("lfotab1","LFO tab 1","Select LFO 1",866,124,"B",18,12,"LFO Select",None,"medium","Remote 'LFO Select' matched by meaning (one of the 3 tabs); "+NOSLOT)
f("lfotab2","LFO tab 2","Select LFO 2",918,124,"B",18,12,chk=NT)
f("lfotab3","LFO tab 3","Select LFO 3",971,124,"B",18,12,chk=NT)
f("lfowave","LFO WAVEFORM display","LFO waveform",857,175,"D",25,18,conf="medium")
f("lfowavearrows","(LFO waveform arrows)","LFO waveform prev/next",888,175,"B",8,18,conf="medium")
f("lfo1rate","LFO 1 RATE","LFO 1 rate",748,185,"K",18,18,"LFO 1 Rate",26,"medium","knob gave no tooltip (value is shown as text above it); Remote 'LFO 1 Rate' (slot 26); matched by meaning")
f("lfo1sync","LFO 1 BEAT SYNC","LFO 1 tempo sync",749,217,"B",30,8,"LFO 1 TempoSync",None,"medium","no tooltip; matched by meaning; "+NOSLOT)
f("lfo1bipolar","LFO 1 BIPOLAR","LFO 1 bipolar",722,233,"B",8,8,conf="medium")
f("lfo1global","LFO 1 GLOBAL","LFO 1 global",722,250,"B",8,8,"LFO 1 Global",None,"medium","no tooltip; matched by meaning; "+NOSLOT)
f("lfo2rate","LFO 2 RATE","LFO 2 rate",947,185,"K",18,18,"LFO 2 Rate",27,"medium","knob gave no tooltip (value is shown as text above it); Remote 'LFO 2 Rate' (slot 27); matched by meaning")
f("lfo2sync","LFO 2 BEAT SYNC","LFO 2 tempo sync",948,217,"B",30,8,"LFO 2 TempoSync",None,"medium","no tooltip; matched by meaning; "+NOSLOT)
f("lfo2keysync","LFO 2 KEY SYNC","LFO 2 key sync",921,233,"B",8,8,"LFO 2 KeySync",None,"medium","no tooltip; matched by meaning; "+NOSLOT)
f("lfo2global","LFO 2 GLOBAL","LFO 2 global",921,250,"B",8,8,"LFO 2 Global",None,"medium","no tooltip; matched by meaning; "+NOSLOT)
f("lfo2delay","LFO DELAY","LFO delay",864,224,"K",16,16,"LFO 1 Delay",None,"medium","no tooltip; the knob sits between the LFO 1 and LFO 2 panels; Remote 'LFO 1 Delay' / 'LFO 2 Delay' per selected LFO; NOT proven; "+NOSLOT)
f("pbrange","P.RANGE","Pitch bend range",118,309,"D",14,10,conf="high",why="tooltip 'Pitchbend Range'; no such Remote item in the vocab")
f("wheelP","PITCH wheel","Pitch bend wheel",115,370,"S",8,45,"Pitch Bend",None,"high","tooltip '(Pitch Bend)'; "+NOSLOT.replace("beyond the 48 knob slots","not on a knob slot"))
f("wheelM","MOD wheel","Mod wheel",147,370,"S",8,45,"Mod Wheel",None,"high","tooltip '(Mod Wheel)'; Remote item, not on a knob slot")
cols=(("src",225,"D",40,7,None),("k1",306,"K",9,7,"Dest1 Amt"),("dest1",360,"D",42,7,None),("k2",457,"K",9,7,"Dest2 Amt"),("dest2",510,"D",42,7,None),("k3",607,"K",9,7,"Scale Amt"),("scale",665,"D",36,7,None),("clr",711,"B",8,8,None))
rows_y=(304,321,338,354,370,386,402,419)
for r,y in enumerate(rows_y,1):
    for ck,x,typ,hw,hh,suf in cols:
        label="MOD %d %s"%(r,ck)
        nm=None
        if suf=="Dest1 Amt": nm="Mod%d Dest1 Amt"%r
        elif suf=="Dest2 Amt": nm="Mod%d Dest2 Amt"%r
        elif suf=="Scale Amt" and r<=3: nm="Mod%d Scale Amt"%r
        known={"k1":"mx_k1","k2":"mx_k2","k3":"mx_k3","src":"mx_src","dest1":"mx_dest1","dest2":"mx_dest2","scale":"mx_scale","clr":"mx_clear"}[ck]
        hov=(r==1)
        chk=c(known) if hov else INF
        VL.f(known,label,"Modulation matrix row %d: %s"%(r,ck),x,y,typ,hw,hh,nm,None,"high" if hov and ck in("k1","k2","k3") else "medium","" if hov else "inferred from pattern, not hovered",chk=chk)
fxy=286
f("fxpower","EFFECTS power","Effects section on/off",753,305,"B",8,8,"Effect On",None,"medium","no tooltip on the lower power button; the upper light gave 'Effects On'. Remote 'Effect On' matched; "+NOSLOT,chk=NT+"; the upper light (753,286) showed tooltip \"Effects On\"")
for k,lab,x,nm,sl in (("phsr","PHSR",783,"Phaser On",None),("dist","DIST",822,"Dist On",28),("eq","EQ",861,"EQ On",None),("comp","COMP",900,"Comp On",32),("dly","DLY",938,"Delay On",35),("rev","REV",977,"Reverb On",39)):
    f("fxtab_"+k,lab+" tab","Show the %s panel"%lab,x,286,"B",18,9,chk=NT)
    f("fxon_"+k,lab+" ON/OFF","%s effect on/off"%lab,x,307,"B",18,9,nm,sl,"medium","no tooltip; Remote '%s' matched by meaning"%nm+("" if sl else "; "+NOSLOT),chk=NT)
f("compattack","COMP ATTACK","Compressor attack",842,360,"K",14,14,"Comp Attack")
f("compthres","COMP THRES","Compressor threshold",893,360,"K",14,14,"Comp Threshold",33)
f("comprelease","COMP RELEASE","Compressor release",842,402,"K",14,14,"Comp Release")
f("compratio","COMP RATIO","Compressor ratio",893,402,"K",14,14,"Comp Ratio",34)
# --- fx views
f=FX["phsr"].f
f("mod_type","MOD FX type slider","Modulation effect type (chorus/flanger/phaser)",819,391,"S",12,30,"Mod Effect Type",43)
f("mod_depth","MOD FX DEPTH","Modulation effect depth",858,355,"K",12,12,"Mod Effect Depth")
f("mod_rate","MOD FX RATE","Modulation effect rate",858,381,"K",12,12,"Mod Effect Rate",45)
f("mod_spread","MOD FX SPREAD","Modulation effect spread",858,407,"K",12,12,"Mod Effect Spread")
f("mod_amt","MOD FX AMOUNT","Modulation effect amount",951,373,"K",14,14,"Mod Effect Amount",44)
f=FX["dist"].f
f("dist_type","DIST type slider","Distortion type",766,406,"S",10,30,why="tooltip 'Dist Type'; no such Remote item")
f("dist_drive","DIST DRIVE","Distortion drive",854,374,"K",14,14,"Dist Drive",30)
f("dist_tone","DIST TONE","Distortion tone",906,373,"K",14,14,"Dist Tone",31)
f("dist_amt","DIST AMOUNT","Distortion amount",951,374,"K",14,14,"Dist Amount",29)
f=FX["eq"].f
f("eq_freq","EQ FREQ","EQ frequency",809,375,"K",14,14,"EQ Freq")
f("eq_q","EQ Q","EQ Q",863,374,"K",14,14,"EQ Q")
f("eq_gain","EQ GAIN","EQ gain",918,375,"K",18,18,"EQ Gain")
f=FX["dly"].f
f("dly_sync","DELAY SYNC","Delay tempo sync",797,350,"B",12,8,"Delay Sync")
f("dly_time","DELAY TIME","Delay time (synced time when SYNC is on)",885,350,"S",60,8,"Delay Time",37,"medium","tooltip with SYNC on says 'Delay Synced Time'; Remote 'Delay Time' (slot 37) is the unsynced version")
f("dly_pp","DELAY PING PONG","Delay ping pong",797,400,"B",12,8,"Delay PingPong")
f("dly_pan","DELAY PAN","Delay pan",854,401,"K",12,12,"Delay Pan")
f("dly_fb","DELAY FB","Delay feedback",906,396,"K",14,14,"Delay FB",38,"medium","tooltip name 'Delay Feedback'; Remote item is 'Delay FB'; matched by meaning")
f("dly_amt","DELAY AMOUNT","Delay amount",952,396,"K",14,14,"Delay Amount",36)
f=FX["rev"].f
f("rev_decay","REVERB DECAY","Reverb decay",885,349,"S",60,8,"Reverb Decay",41)
f("rev_size","REVERB SIZE","Reverb size",808,394,"K",14,14,"Reverb Size",42)
f("rev_damp","REVERB DAMP","Reverb damp",863,393,"K",14,14,"Reverb Damp")
f("rev_amt","REVERB AMOUNT","Reverb amount",922,394,"K",14,14,"Reverb Amount",40)
# --- back
B=[];CB={}
k=1.404
def b(key,label,what,typ,px,py,hw=14,hh=14,why=""):
    B.append([label,what,typ,[px,py],[hw,hh],why]); CB[label]=c(key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",234,250)
b("cv","Seq Note In","Note CV input (sequencer)","J",234,295)
b("pbtrim","Pitch Bend CV trim","Amount for pitch bend CV","K",404,247)
b("pbjack","Pitch Bend CV In","CV input: pitch bend","J",441,250)
b("mwtrim","Mod Wheel CV trim","Amount for mod wheel CV","K",404,292)
b("mwjack","Mod Wheel CV In","CV input: mod wheel","J",441,295)
for i,y in enumerate((250,290,330,368),1): b("cvin%d"%i,"CV In %d"%i,"CV input %d (assignable as a modulation source)"%i,"J",718,y)
for i,y in enumerate((250,290,330,368),1): b("cvout%d"%i,"CV Out %d"%i,"CV output %d"%i,"J",981,y)
b("audioL","Audio Out L","Audio output, left","J",1014,572,18,18)
b("audioR","Audio Out R","Audio output, right","J",1081,572,18,18)
# --- write specs/checks
base=dict(device="Grain",prefix="GRAN",remote_scope="Propellerhead Software / se.propellerheads.Grain",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="grain",front_raw="_captures_batchE/grain_front_top_raw.jpg",back_raw="_captures_batchE/grain_back_raw.jpg",front=V0.rows,back=B),open("tools/specs/grain.json","w"))
views={"lower":(VL,"_captures_batchE/grain_front_bottom_raw.jpg","Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down)"),
 "fxphsr":(FX["phsr"],"_captures_batchE/grain_fx_phsr_raw.jpg","Effects: PHSR (modulation FX) tab"),
 "fxdist":(FX["dist"],"_captures_batchE/grain_fx_dist_raw.jpg","Effects: DIST tab"),
 "fxeq":(FX["eq"],"_captures_batchE/grain_fx_eq_raw.jpg","Effects: EQ tab"),
 "fxdly":(FX["dly"],"_captures_batchE/grain_fx_dly_raw.jpg","Effects: DLY tab"),
 "fxrev":(FX["rev"],"_captures_batchE/grain_fx_rev_raw.jpg","Effects: REV tab")}
ck=dict(device="Grain",front=V0.chk,back=CB,views={},view_titles={})
OFF={"lower":100,"fxphsr":200,"fxdist":300,"fxeq":400,"fxdly":500,"fxrev":600}
for name,(v,raw,title) in views.items():
    o=OFF[name]
    json.dump(dict(base,slug="grain-%s-view"%name,front_offsets={"K":o,"B":o,"D":o,"S":o},front_raw=raw,back_raw="",front=v.rows,back=[]),open("tools/specs/grain--%s.json"%name,"w"))
    ck["views"][name]=v.chk; ck["view_titles"][name]=title+" (picture grain-%s-view_front_labeled.png)"%name
json.dump(ck,open("tools/checks/grain.json","w"),indent=0)
print(len(V0.rows),len(B),{n:len(v.rows) for n,(v,_,_) in views.items()})
