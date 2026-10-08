import json
# Europa Shapeshifting Synthesizer. Views: main (top, engine I shown), lower (matrix + effects row), 6 fx panels, back.
NT="no tooltip in Reason (hovered 1.3 s)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists but is beyond the 48 knob slots of our remotemap (not mapped)"
ENG="tooltip says 'Eng1'; Remote name is 'Osc1' (same control); engine I was selected"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/europa_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
pts=json.load(open("_captures_batchE/europa_pts.json"))
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
class View:
    def __init__(s,ox,oy,k): s.ox,s.oy,s.k=ox,oy,k; s.rows=[]; s.chk={}
    def f(s,label,what,sx,sy,typ,hw,hh,name=None,slot=None,conf="high",why="",chk=None):
        x=round((sx-s.ox)*s.k); y=round((sy-s.oy)*s.k)
        if name and slot is None and not why: why=NOSLOT
        s.rows.append([label,what,name,slot,[x,y],[round(hw*s.k),round(hh*s.k)],typ,conf,why])
        s.chk[label]=chk
V0=View(70,62,1.2833); VL=View(70,100,1.6333)
FX={n:View(740,275,2.2038) for n in ("phsr","dist","eq","dly","rev","comp")}
def g(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",chk=None):
    sx,sy=pts[key]
    V0.f(label,what,sx,sy,typ,hw,hh,name,slot,conf,why,chk or c(key))
g("fold","(triangle)","Fold/unfold device","B",8,8,conf="medium")
g("tape","Patch name tape","Patch name tape","D",40,8,"Device Name",conf="medium",why="Remote item 'Device Name'; convention from earlier devices; no tooltip")
g("patchdisp","Patch display","Patch name display","D",125,12,"Patch Name",conf="medium",why="Remote item 'Patch Name'; no tooltip; NOT proven")
g("patcharrows","(patch arrows)","Previous / next patch","B",8,12,"Select Previous Patch",why="tooltip is for the upper half; lower half = Select Next Patch, not hovered")
g("patchfolder","(patch folder)","Browse patch","B",9,9)
g("patchdisk","(patch disk)","Save patch","B",9,9)
for i in (1,2,3):
    g("eng%d"%i,"ENGINE %s button"%"I"*i if False else "ENGINE %s select"%("I","II","III")[i-1],"Select engine %d for editing"%i,"B",22,22,"OscSel" if i==1 else None,conf="medium",why="tooltip 'Engine Select'; Remote 'OscSel' matched by meaning (one item for all three buttons)" if i==1 else "same tooltip as engine I button")
for i in (1,2,3):
    g("eng%don"%i,"ENGINE %s ON"%("I","II","III")[i-1],"Engine %d on/off"%i,"B",7,7,"Osc%d On"%i,None,"medium" if i>1 else "high",(ENG if i==1 else "no tooltip; Remote 'Osc%d On' matched by meaning"%i)+"; "+NOSLOT if False else ((ENG+"; "+NOSLOT) if i==1 else "no tooltip; Remote 'Osc%d On' matched by meaning; "%i+NOSLOT))
for i in (1,2,3):
    g("eng%darrow"%i,"(engine %d arrow)"%i,"Engine %d arrow (send engine to the filter section)"%i,"B",7,7,conf="medium")
g("waveon","WAVE ON","Wave section on/off (engine I)","B",12,9,"Osc1 On",1,"high",ENG)
g("wavedisp","WAVE display","Wave shape display","D",70,36)
g("wavemenu","WAVE menu (Basic Analog)","Wave type menu","D",60,9,"Osc1 Wave",2,"medium","Remote 'Osc1 Wave' (slot 2); menu gave no tooltip; matched by meaning; NOT proven")
g("wavearrows","(wave arrows)","Wave previous/next","B",6,9,conf="medium")
g("oct","OCT","Engine I octave","K",11,11,why="tooltip 'Eng1 Oct'; no such Remote item")
g("semi","SEMI","Engine I semitone","K",11,11,"Osc1 Semi",3,"high",ENG)
g("tune","TUNE","Engine I fine tune","K",11,11,why="tooltip 'Eng1 Tune'; no such Remote item")
g("kbd","KBD","Engine I pitch keyboard tracking","K",11,11,why="tooltip 'Eng1 Pitch Kbd'; no such Remote item")
g("shape","SHAPE","Wave shape amount","K",20,20,"Osc1 Shape",None,"high",ENG+"; "+NOSLOT)
g("shapelfo","SHAPE mod amount","Shape modulation amount","K",9,9,"Osc1 Shape Amt",6,"high",ENG)
g("shapesrc","SHAPE mod source (LFO 1)","Shape modulation source","D",20,8,conf="medium")
g("shapevelo","SHAPE VELO","Shape velocity amount","K",9,9,"Osc1 Shape Vel",None,"high",ENG+"; "+NOSLOT)
g("phasesync","PHASE SYNC","Phase sync on/off","B",8,8,why="tooltip 'Eng1 SyncPhase'; no such Remote item")
for m in (1,2):
    g("mod%don"%m,"MODIFIER %d ON"%m,"Modifier %d on/off"%m,"B",7,7,"Osc1 Mod%d On"%m,None,"high",ENG+"; "+NOSLOT)
    g("mod%dmenu"%m,"MODIFIER %d menu"%m,"Modifier %d type menu"%m,"D",70,9,conf="medium")
    g("mod%damt"%m,"MODIFIER %d AMOUNT"%m,"Modifier %d amount"%m,"K",14,14,"Osc1 Mod%d Amt"%m,None,"high",ENG+"; "+NOSLOT)
    g("mod%dlfo"%m,"MODIFIER %d mod amount"%m,"Modifier %d modulation amount"%m,"K",9,9,"Osc1 Mod%d Mod"%m,None,"high",ENG+"; "+NOSLOT)
    g("mod%dsrc"%m,"MODIFIER %d mod source"%m,"Modifier %d modulation source"%m,"D",20,8,conf="medium")
g("sfon","SPECTRAL FILTER ON","Spectral filter on/off","B",7,7,"Osc1 Filter On",None,"high",ENG+"; "+NOSLOT)
g("sfdisp","SPECTRAL FILTER display","Spectral filter display","D",75,40)
g("sfmenu","SPECTRAL FILTER menu (HP 24)","Spectral filter type menu","D",70,8,conf="medium")
g("sffreq","SPECTRAL FILTER FREQ","Spectral filter frequency","K",20,20,"Osc1 Filter Freq",None,"high",ENG+"; "+NOSLOT)
g("sfreso","SPECTRAL FILTER RESO","Spectral filter resonance","K",14,14,"Osc1 Filter Reso",None,"high",ENG+"; "+NOSLOT)
g("sfkbd","SPECTRAL FILTER KBD","Spectral filter keyboard tracking","K",9,9,why="tooltip 'Eng1 Filter Kbd'; no such Remote item")
g("sfenv","SPECTRAL FILTER ENV mod amount","Spectral filter modulation amount","K",9,9,"Osc1 Filter Mod",None,"high",ENG+"; "+NOSLOT)
g("sfsrc","SPECTRAL FILTER mod source (ENV 1)","Spectral filter modulation source","D",20,8,conf="medium")
g("sfvelo","SPECTRAL FILTER VELO","Spectral filter velocity amount","K",9,9,why="tooltip 'Eng1 Filter Vel'; no such Remote item")
g("harmon","HARMONICS ON","Harmonics on/off","B",7,7,"Osc1 Harm On",None,"high",ENG+"; "+NOSLOT)
g("harmmenu","HARMONICS menu (Random Gain)","Harmonics type menu","D",70,8,conf="medium")
g("harmpos","HARMONICS POS","Harmonics position","K",14,14,"Osc1 Harm Pos",None,"high",ENG+"; "+NOSLOT)
g("harmamt","HARMONICS AMOUNT","Harmonics amount","K",14,14,"Osc1 Harm Amt",None,"high",ENG+"; "+NOSLOT)
g("unison","UNISON ON","Unison on/off","B",7,7,"Osc1 Unison On",8,"high",ENG)
g("unidisp","UNISON display","Unison display","D",45,28)
g("unimenu","UNISON menu (Normal)","Unison mode menu","D",35,8,"Osc1 Unison Mode",None,"medium","Remote 'Osc1 Unison Mode'; menu gave no tooltip; matched by meaning; "+NOSLOT)
g("unicount","UNISON COUNT","Unison voice count","K",11,11,why="tooltip 'Eng1 Count'; no such Remote item")
g("uniblend","UNISON BLEND","Unison blend","K",11,11,"Osc1 Blend",None,"high",ENG+"; "+NOSLOT)
g("unidetune","UNISON DETUNE","Unison detune","K",11,11,"Osc1 Detune",4,"high",ENG)
g("unispread","UNISON SPREAD","Unison spread","K",11,11,"Osc1 Spread",7,"high",ENG)
g("uwdisp","USER WAVE name display","Name of the user wave","D",55,9)
g("uwarrows","(user wave arrows)","Previous / next user wave","B",8,12,why="tooltip is for the upper half; lower half not hovered")
g("uwfolder","(user wave folder)","Browse user waves","B",9,9)
g("uwwave","(user wave sample)","Start sampling a user wave","B",9,9)
g("uwpencil","(user wave edit)","Edit user wave","B",9,9)
for i in (1,2,3):
    g("slider%d"%i,"LEVEL slider %s"%("I","II","III")[i-1],"Engine %d level"%i,"S",52,6,"Osc%d Level"%i,(5,13,21)[i-1],"high" if i==1 else "high",ENG.replace("Eng1","Eng%d"%i).replace("Osc1","Osc%d"%i).replace("engine I","engine %d"%i) if i>1 else ENG)
    g("pan%d"%i,"PAN %s"%("I","II","III")[i-1],"Engine %d pan"%i,"K",10,10,why="tooltip 'Eng%d Pan'; no such Remote item"%i)
    g("route%d"%i,"ENGINE %s to FILTER"%("I","II","III")[i-1],"Send engine %d to the filter"%i,"B",9,9,"Osc%d To Filter"%i,None,"high","tooltip 'Eng%d To Filter'; Remote 'Osc%d To Filter'; "%(i,i)+NOSLOT)
g("fmenu","FILTER type menu (MFB LP 12dB)","Filter type menu","D",65,8,"Filter Type",25,"medium","Remote 'Filter Type' (slot 25); menu gave no tooltip; matched by meaning; NOT proven")
g("fdrivebtn","FILTER DRIVE on","Filter drive on/off","B",12,6,conf="medium")
g("fdrive","FILTER DRIVE","Filter drive","K",11,11,"Filter Drive",28)
g("freso","FILTER RESO","Filter resonance","K",14,14,"Filter Reso",27)
g("ffreq","FILTER FREQ","Filter frequency","K",24,24,"Filter Freq",26)
g("fkbd","FILTER KBD","Filter keyboard tracking","K",9,9,"Filter Kbd",29)
g("fenv","FILTER mod amount","Filter modulation amount","K",9,9,"Filter Mod",30)
g("fsrc","FILTER mod source (ENV 1)","Filter modulation source","D",22,8,conf="medium")
g("fvelo","FILTER VELO","Filter velocity amount","K",9,9,why="tooltip 'Filter Velocity'; no such Remote item")
g("amppan","AMP PAN","Amp pan","K",11,11,"Pan",None,"high","tooltip 'Pan'; Remote 'Pan'; "+NOSLOT)
g("ampgain","AMP GAIN","Amp gain","K",11,11,"Amp Gain",35)
g("ampvelo","AMP VELO","Amp velocity","K",11,11,"Amp Velocity",36)
for k,l,n,s in (("ampA","A","Attack",31),("ampD","D","Decay",32),("ampS","S","Sustain",33),("ampR","R","Release",34)):
    g(k,"AMP "+l,"Amp "+n.lower(),"S",6,32,"Amp "+n,s)
g("master","MASTER VOLUME","Master volume","K",24,24,"Master Volume",48)
g("voices","VOICES display","Number of voices","D",14,10,why="tooltip 'Voices'; no such Remote item")
g("voicesarrows","(voices arrows)","Voices down/up","B",7,12,conf="medium")
g("keymode","KEY MODE switch","Key mode (POLY/RETRIG/LEGATO)","B",8,22,"Key Mode",None,"high","tooltip 'Key Mode'; "+NOSLOT)
g("portamode","PORTA switch (OFF/ON/AUTO)","Portamento mode","B",8,22,"Portamento Mode",None,"high","tooltip 'Portamento Mode'; "+NOSLOT)
g("portatime","PORTA TIME","Portamento time","K",14,14,"Portamento",47)
for i in (1,2,3,4):
    g("envtab%d"%i,"ENVELOPE tab %d"%i,"Select envelope %d"%i,"B",38,12,conf="medium")
g("preset","PRESET","Envelope preset","B",24,18)
g("editypos","EDIT Y-POS","Edit envelope y position","B",24,18)
g("envdisp","Envelope display","Envelope editor","D",200,60)
g("sustain","SUSTAIN","Envelope sustain","B",30,12,conf="medium")
g("loop","LOOP","Envelope loop","B",30,16,conf="medium")
g("keytrig","KEY TRIG","Envelope key trigger","B",30,10,conf="medium")
g("envrate","ENVELOPE RATE","Envelope rate (value shown as text above)","K",18,18,"Env 2 Rate",None,"medium","knob gave no tooltip; Remote 'Env 1..4 Rate' follow the selected envelope tab (envelope 2 was selected); NOT proven; "+NOSLOT)
g("envsync","ENVELOPE BEAT SYNC","Envelope tempo sync","B",30,8,conf="medium")
g("envbipolar","ENVELOPE BIPOLAR","Envelope bipolar","B",8,8,conf="medium")
g("envglobal","ENVELOPE GLOBAL","Envelope global","B",8,8,conf="medium")
for i in (1,2,3):
    g("lfotab%d"%i,"LFO tab %d"%i,"Select LFO %d"%i,"B",18,12,conf="medium")
g("lfowave","LFO WAVEFORM display","LFO waveform","D",25,18,conf="medium")
g("lfowavearrows","(LFO waveform arrows)","LFO waveform prev/next","B",8,18,conf="medium")
g("lforate","LFO RATE","LFO rate (value shown as text above)","K",18,18,"LFO 1 Rate",37,"medium","knob gave no tooltip; Remote 'LFO 1 Rate' (slot 37) is for LFO 1; NOT proven")
g("lfodelay","LFO DELAY","LFO delay","K",16,16,conf="medium")
g("lfosync","LFO BEAT SYNC","LFO tempo sync","B",30,8,conf="medium")
g("lfokeysync","LFO KEY SYNC","LFO key sync","B",8,8,conf="medium")
g("lfoglobal","LFO GLOBAL","LFO global","B",8,8,conf="medium")
g("prange","P.RANGE","Pitch bend range","D",14,10,why="tooltip 'Pitchbend Range'; no such Remote item")
g("wheelP","PITCH wheel","Pitch bend wheel","S",8,45,"Pitch Bend",None,"high","tooltip '(Pitch Bend)'; Remote item, not on a knob slot")
g("wheelM","MOD wheel","Mod wheel","S",8,45,"Mod Wheel",None,"high","tooltip '(Mod Wheel)'; Remote item, not on a knob slot")

# --- engine II / III views (per-engine controls; same positions as engine I)
ENG_DEF=[("waveon","WAVE ON","Wave section on/off","B",12,9,"On",(9,17)),("wavedisp","WAVE display","Wave shape display","D",70,36,None,None),("wavemenu","WAVE menu","Wave type menu","D",60,9,"Wave",(10,18)),("wavearrows","(wave arrows)","Wave previous/next","B",6,9,None,None),
("oct","OCT","Octave","K",11,11,None,None),("semi","SEMI","Semitone","K",11,11,None,None),("tune","TUNE","Fine tune","K",11,11,None,None),("kbd","KBD","Pitch keyboard tracking","K",11,11,None,None),
("shape","SHAPE","Wave shape amount","K",20,20,"Shape",(None,None)),("shapelfo","SHAPE mod amount","Shape modulation amount","K",9,9,"Shape Amt",(14,22)),("shapesrc","SHAPE mod source","Shape modulation source","D",20,8,None,None),("shapevelo","SHAPE VELO","Shape velocity amount","K",9,9,"Shape Vel",(None,None)),("phasesync","PHASE SYNC","Phase sync on/off","B",8,8,None,None),
("mod1on","MODIFIER 1 ON","Modifier 1 on/off","B",7,7,"Mod1 On",(None,None)),("mod1menu","MODIFIER 1 menu","Modifier 1 type menu","D",70,9,None,None),("mod1amt","MODIFIER 1 AMOUNT","Modifier 1 amount","K",14,14,"Mod1 Amt",(None,None)),("mod1lfo","MODIFIER 1 mod amount","Modifier 1 modulation amount","K",9,9,None,None),("mod1src","MODIFIER 1 mod source","Modifier 1 modulation source","D",20,8,None,None),
("mod2on","MODIFIER 2 ON","Modifier 2 on/off","B",7,7,"Mod2 On",(None,None)),("mod2menu","MODIFIER 2 menu","Modifier 2 type menu","D",70,9,None,None),("mod2amt","MODIFIER 2 AMOUNT","Modifier 2 amount","K",14,14,"Mod2 Amt",(None,None)),("mod2lfo","MODIFIER 2 mod amount","Modifier 2 modulation amount","K",9,9,None,None),("mod2src","MODIFIER 2 mod source","Modifier 2 modulation source","D",20,8,None,None),
("sfon","SPECTRAL FILTER ON","Spectral filter on/off","B",7,7,"Filter On",(None,None)),("sfdisp","SPECTRAL FILTER display","Spectral filter display","D",75,40,None,None),("sfmenu","SPECTRAL FILTER menu","Spectral filter type menu","D",70,8,None,None),("sffreq","SPECTRAL FILTER FREQ","Spectral filter frequency","K",20,20,"Filter Freq",(None,None)),("sfreso","SPECTRAL FILTER RESO","Spectral filter resonance","K",14,14,"Filter Reso",(None,None)),("sfkbd","SPECTRAL FILTER KBD","Spectral filter keyboard tracking","K",9,9,None,None),("sfenv","SPECTRAL FILTER mod amount","Spectral filter modulation amount","K",9,9,"Filter Mod",(None,None)),("sfsrc","SPECTRAL FILTER mod source","Spectral filter modulation source","D",20,8,None,None),("sfvelo","SPECTRAL FILTER VELO","Spectral filter velocity amount","K",9,9,None,None),
("harmon","HARMONICS ON","Harmonics on/off","B",7,7,"Harm On",(None,None)),("harmmenu","HARMONICS menu","Harmonics type menu","D",70,8,None,None),("harmpos","HARMONICS POS","Harmonics position","K",14,14,"Harm Pos",(None,None)),("harmamt","HARMONICS AMOUNT","Harmonics amount","K",14,14,"Harm Amt",(None,None)),
("unison","UNISON ON","Unison on/off","B",7,7,"Unison On",(16,24)),("unidisp","UNISON display","Unison display","D",45,28,None,None),("unimenu","UNISON menu","Unison mode menu","D",35,8,"Unison Mode",(None,None)),("unicount","UNISON COUNT","Unison voice count","K",11,11,None,None),("uniblend","UNISON BLEND","Unison blend","K",11,11,"Blend",(11,19)),("unidetune","UNISON DETUNE","Unison detune","K",11,11,"Detune",(12,20)),("unispread","UNISON SPREAD","Unison spread","K",11,11,"Spread",(15,23))]
E2={};E3={}
for fn,d in (("europa_eng2_notes.txt",E2),("europa_eng3_notes.txt",E3)):
    for ln in open("_captures_batchE/"+fn):
        p=ln.rstrip("\n").split("|",1)
        if len(p)==2: d[p[0]]=p[1]
ENGV={}
for n,(rn,E,roman) in {2:("2",E2,"II"),3:("3",E3,"III")}.items():
    v=View(70,62,1.2833); ENGV[n]=v
    for key,label,what,typ,hw,hh,suf,slots in ENG_DEF:
        sx,sy=pts[key]
        name=("Osc%d %s"%(n,suf)) if suf else None
        slot=slots[n-2] if slots else None
        if name and slot is None: why="tooltip 'Eng%d ...'; "%n+NOSLOT
        elif name: why="tooltip 'Eng%d ...'; Remote name is 'Osc%d ...'"%(n,n)
        else: why="no such Remote item"
        if key in E: chk=NT if E[key].startswith("(no tooltip") else T(E[key])
        else: chk="not hovered on engine %s; same position and tooltip pattern ('Eng%d ...') as engine I and the hovered controls"%(roman,n)
        v.f("ENG %s %s"%(roman,label),"Engine %s: %s"%(roman,what),sx,sy,typ,hw,hh,name,slot,"high" if key in E else "medium",why,chk=chk)
# --- lower view (matrix + effects row)
f=VL.f
cols=(("src",217,"D",40,7),("k1",303,"K",9,7),("dest1",352,"D",42,7),("up1",405,"B",5,7),("k2",454,"K",9,7),("dest2",505,"D",42,7),("up2",558,"B",5,7),("k3",607,"K",9,7),("scale",658,"D",36,7),("clr",709,"B",8,8))
for r,y in enumerate((304,320,337,353,370,386,402,419),1):
    for ck,x,typ,hw,hh in cols:
        nm={"k1":"mtx%d_amt1","k2":"mtx%d_amt2","k3":"mtx%d_scale"}.get(ck)
        chk=c(nm%r) if nm else NT+" (rows hovered: text fields, arrows and clear buttons gave no tooltip)"
        f("MOD %d %s"%(r,ck),"Modulation matrix row %d: %s"%(r,ck),x,y,typ,hw,hh,None,None,"high" if nm else "medium","tooltip '%s' ; no Remote item for the matrix"%notes[nm%r] if nm else "",chk=chk)
f("EFFECTS light","Effects section on/off (light)",750,287,"B",8,8,"Effect On",None,"medium","tooltip 'Effect On'; "+NOSLOT,chk=T("Effect On"))
f("EFFECTS power","Effects power button",750,306,"B",8,8,conf="medium",chk=NT)
for k,lab,x,nm,sl in (("phsr","PHSR",783,"Phaser On",None),("dist","DIST",822,"Dist On",38),("eq","EQ",861,"EQ On",None),("dly","DLY",900,"Delay On",40),("rev","REV",938,"Reverb On",44),("comp","COMP",977,"Comp On",None)):
    f(lab+" tab","Show the %s panel"%lab,x,286,"B",18,9,chk=NT)
    f(lab+" ON/OFF","%s effect on/off"%lab,x,306,"B",18,9,nm,sl,"medium","no tooltip; Remote '%s' matched by meaning"%nm+("" if sl else "; "+NOSLOT),chk=NT)
def fxr(view,label,what,sx,sy,typ,hw,hh,key,name=None,slot=None,why="",conf="high"):
    FX[view].f(label,what,sx,sy,typ,hw,hh,name,slot,conf,why,chk=c(key))
fxr("phsr","MOD FX type slider","Modulation effect type (chorus/flanger/phaser)",818,397,"S",12,30,"fx_phsr_type","Mod Effect Type" if False else None,None,"tooltip 'Mod Effect Type'; no such Remote item")
fxr("phsr","MOD FX DEPTH","Modulation effect depth",857,351,"K",12,12,"fx_phsr_depth",why="tooltip 'Mod Effect Depth'; no such Remote item")
fxr("phsr","MOD FX RATE","Modulation effect rate",857,382,"K",12,12,"fx_phsr_rate",why="tooltip 'Mod Effect Rate'; no such Remote item")
fxr("phsr","MOD FX SPREAD","Modulation effect spread",857,411,"K",12,12,"fx_phsr_spread",why="tooltip 'Mod Effect Spread'; no such Remote item")
fxr("phsr","MOD FX AMOUNT","Modulation effect amount",954,370,"K",14,14,"fx_phsr_amount","Mod Effect Amount")
fxr("dist","DIST type slider","Distortion type",766,407,"S",10,30,"fx_dist_type",why="tooltip 'Dist Type'; no such Remote item")
fxr("dist","DIST DRIVE","Distortion drive",853,372,"K",14,14,"fx_dist_drive",why="tooltip 'Dist Drive'; no such Remote item")
fxr("dist","DIST TONE","Distortion tone",901,372,"K",14,14,"fx_dist_tone",why="tooltip 'Dist Tone'; no such Remote item")
fxr("dist","DIST AMOUNT","Distortion amount",950,372,"K",14,14,"fx_dist_amount","Dist Amount",39)
fxr("eq","EQ FREQ","EQ frequency",810,376,"K",14,14,"fx_eq_freq","EQ Freq")
fxr("eq","EQ Q","EQ Q",862,374,"K",14,14,"fx_eq_q","EQ Q")
fxr("eq","EQ GAIN","EQ gain",917,374,"K",18,18,"fx_eq_gain","EQ Gain")
fxr("dly","DELAY SYNC","Delay tempo sync",797,351,"B",12,8,"fx_dly_sync","Delay Sync")
fxr("dly","DELAY TIME","Delay time (synced time when SYNC is on)",865,351,"S",60,8,"fx_dly_time","Delay Time",42,"tooltip with SYNC on says 'Delay Synced Time'; Remote 'Delay Time' (slot 42) is the unsynced version","medium")
fxr("dly","DELAY PING PONG","Delay ping pong",797,400,"B",12,8,"fx_dly_pingpong","Delay PingPong")
fxr("dly","DELAY PAN","Delay pan",852,394,"K",12,12,"fx_dly_pan","Delay Pan")
fxr("dly","DELAY FB","Delay feedback",905,394,"K",14,14,"fx_dly_fb","Delay FB",43,"tooltip name 'Delay Feedback'; Remote item is 'Delay FB'; matched by meaning","medium")
fxr("dly","DELAY AMOUNT","Delay amount",955,394,"K",14,14,"fx_dly_amount","Delay Amount",41)
fxr("rev","REVERB DECAY","Reverb decay",868,350,"S",60,8,"fx_rev_decay",why="tooltip 'Reverb Decay'; no such Remote item")
fxr("rev","REVERB SIZE","Reverb size",806,392,"K",14,14,"fx_rev_size","Reverb Size",46)
fxr("rev","REVERB DAMP","Reverb damp",866,392,"K",14,14,"fx_rev_damp","Reverb Damp")
fxr("rev","REVERB AMOUNT","Reverb amount",926,392,"K",14,14,"fx_rev_amount","Reverb Amount",45,"tooltip text was clipped in my capture after 'Reverb Amount'","medium")
for lab,x,y,nm,k in (("COMP ATTACK",840,361,None,"fx_comp_attack"),("COMP THRES",891,361,None,"fx_comp_thres"),("COMP RELEASE",840,400,None,"fx_comp_release"),("COMP RATIO",891,400,"Comp Ratio","fx_comp_ratio")):
    fxr("comp",lab,"Compressor "+lab.split()[1].lower(),x,y,"K",14,14,k,nm,None,"" if nm is None else NOSLOT)
# --- back
B=[];CB={}
def b(key,label,what,typ,px,py,hw=14,hh=14,why=""):
    B.append([label,what,typ,[px,py],[hw,hh],why]); CB[label]=c("b_"+key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",267,431)
b("cv","Seq Note In","Note CV input (sequencer)","J",267,477)
b("pbtrim","Pitch Bend CV trim","Amount for pitch bend CV","K",441,431)
b("pbjack","Pitch Bend CV In","CV input: pitch bend","J",482,431)
b("mwtrim","Mod Wheel CV trim","Amount for mod wheel CV","K",441,475)
b("mwjack","Mod Wheel CV In","CV input: mod wheel","J",482,477)
for i,y in enumerate((430,471,513,552),1): b("cvin%d"%i,"CV In %d"%i,"CV input %d (assignable as a modulation source)"%i,"J",769,y)
for i,y in enumerate((430,471,513,552),1): b("cvout%d"%i,"CV Out %d"%i,"CV output %d"%i,"J",1042,y)
b("audioL","Audio Out L","Audio output, left","J",1098,826,18,18)
b("audioR","Audio Out R","Audio output, right","J",1167,826,18,18)
base=dict(device="Europa",prefix="EURO",remote_scope="Propellerhead Software / se.propellerheads.Europa",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="europa",front_raw="_captures_batchE/europa_front_top_raw.jpg",back_raw="_captures_batchE/europa_back_raw.jpg",front=V0.rows,back=B),open("tools/specs/europa.json","w"))
views={"eng2":(ENGV[2],"_captures_batchE/europa_eng2_raw.jpg","Engine II selected: its per-engine controls"),"eng3":(ENGV[3],"_captures_batchE/europa_eng3_raw.jpg","Engine III selected: its per-engine controls"),"lower":(VL,"_captures_batchE/europa_front_bottom_raw.jpg","Lower half: modulation matrix and effects row (scrolled down)")}
for k,t in (("phsr","PHSR (modulation FX)"),("dist","DIST"),("eq","EQ"),("dly","DLY"),("rev","REV"),("comp","COMP")):
    views["fx"+k]=(FX[k],"_captures_batchE/europa_fx_%s_raw.jpg"%k,"Effects: %s tab"%t)
ck=dict(device="Europa",front=V0.chk,back=CB,views={},view_titles={})
OFF={"eng2":800,"eng3":900,"lower":100,"fxphsr":200,"fxdist":300,"fxeq":400,"fxdly":500,"fxrev":600,"fxcomp":700}
for name,(v,raw,title) in views.items():
    o=OFF[name]
    json.dump(dict(base,slug="europa-%s-view"%name,front_offsets={"K":o,"B":o,"D":o,"S":o},front_raw=raw,back_raw="",front=v.rows,back=[]),open("tools/specs/europa--%s.json"%name,"w"))
    ck["views"][name]=v.chk; ck["view_titles"][name]=title+" (picture europa-%s-view_front_labeled.png)"%name
json.dump(ck,open("tools/checks/europa.json","w"),indent=0)
print(len(V0.rows),len(B),{n:len(v.rows) for n,(v,_,_) in views.items()})
