import json, re
# SubTractor Analog Synthesizer. One front picture + one back picture (same frame: screen=70+px/1.628, 62+py/1.628).
NT="no tooltip in Reason (hovered 1.5-3 s)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists but is beyond the 48 knob slots of our remotemap (not mapped)"
LED="not hovered: LED of a radio group; the button/knob that steps the group carries the Reason name"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/subtractor_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
P=json.load(open("_captures_batchE/subtractor_pts.json"))
K=1.628; OX,OY=70,62
rows=[]; chk={}
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None,ck=None):
    sx,sy=pos or P[key]
    x=round((sx-OX)*K); y=round((sy-OY)*K)
    if name and slot is None and not why: why=NOSLOT
    rows.append([label,what,name,slot,[x,y],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=ck or (c(key) if key in notes else LED)
M="medium"
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M)
f("patchdisp","Patch display","Patch name display","D",70,12,conf=M)
f("patcharrows","(patch arrows)","Previous / next patch","B",8,12,"Select Previous Patch",why="tooltip is for the upper half; lower half = Select Next Patch, not hovered")
f("patchfolder","(patch folder)","Browse patch","B",9,9)
f("patchdisk","(patch disk)","Save patch","B",9,9)
f("tape","Patch name tape","Patch name tape","D",8,40,"Device Name",conf=M,why="Remote item 'Device Name'; tooltip shows the patch name; convention from earlier devices")
f("noteon","NOTE ON light","Note-on indicator","D",5,5,conf=M)
f("legato","LEGATO","Key mode LEGATO light","B",5,5)
f("retrig","RETRIG","Key mode RETRIG light","B",5,5)
f("mode","KEY MODE button","Key mode (steps LEGATO/RETRIG)","B",10,7,"Key Mode",None)
f("porta","PORTAMENTO","Portamento time","K",14,14,"Portamento",47)
f("lobw","LO BW","Low bandwidth on/off","B",7,7)
f("poly","POLYPHONY display","Number of voices","D",14,10)
f("polyarrows","(polyphony arrows)","Voices down/up","B",7,12,conf=M)
f("range","RANGE display","Pitch bend range","D",14,10)
f("rangearrows","(range arrows)","Pitch bend range down/up","B",7,12,conf=M)
f("wheelP","PITCH wheel","Pitch bend wheel","S",9,40,"Pitch Bend",None)
f("wheelM","MOD wheel","Mod wheel","S",9,40,"Mod Wheel",None)
for k,l in (("atouch","A.TOUCH"),("expr","EXPR"),("breath","BREATH")): f(k,l,"Ext mod source "+l,"B",5,5)
f("extmod","EXT MOD button","Choose ext mod source","B",10,7,"Ext Mod Select",None)
for k,l,w in (("c1_ffreq","F.FREQ","Filter frequency"),("c1_fres","F.RES","Filter resonance"),("c1_lfo","LFO1","LFO1 amount"),("c1_phase","PHASE","Phase difference"),("c1_fm","FM","FM amount")):
    f(k,"MOD WHEEL "+l,"Mod wheel to "+w.lower(),"K",14,14)
for k,l,w in (("c2_ffreq","F.FREQ","Filter frequency"),("c2_lfo","LFO1","LFO1 amount"),("c2_amp","AMP","Amp level"),("c2_fm","FM","FM amount")):
    f(k,"EXT MOD "+l,"Ext modulation to "+w.lower(),"K",14,14)
for o,n0 in (("o1",0),("o2",5)):
    X=o[1]
    if o=="o2": f("o2light","OSC 2 on/off light","Oscillator 2 on/off","B",7,7,"Osc2 On/Off",5)
    f(o+"phase","OSC %s PHASE"%X,"Oscillator %s phase difference"%X,"K",14,14)
    f(o+"wave","OSC %s WAVEFORM display"%X,"Oscillator %s waveform"%X,"D",16,12,"Osc%s Wave"%X,1 if o=="o1" else 6,M,"tooltip 'Osc%s Wave'; Remote 'Osc%s Wave'"%(X,X))
    f(o+"wavearr","(OSC %s waveform arrows)"%X,"Oscillator %s waveform prev/next"%X,"B",7,12,conf=M)
    f(o+"oct","OSC %s OCT"%X,"Oscillator %s octave"%X,"D",16,12,"Osc%s Octave"%X,2 if o=="o1" else 7,M,"tooltip 'Osc%s Octave'; Remote 'Osc%s Octave'"%(X,X))
    f(o+"semi","OSC %s SEMI"%X,"Oscillator %s semitone"%X,"D",20,12,"Osc%s Semitone"%X,3 if o=="o1" else 8,M,"tooltip 'Osc%s Semitone'"%X)
    f(o+"cent","OSC %s CENT"%X,"Oscillator %s fine tune"%X,"D",22,12,"Osc%s Fine Tune"%X,4 if o=="o1" else 9,M,"tooltip 'Osc%s Fine Tune'"%X)
    f(o+"mode","OSC %s MODE"%X,"Oscillator %s phase mode"%X,"B",10,7)
    f(o+"kbd","OSC %s KBD TRACK"%X,"Oscillator %s keyboard tracking"%X,"B",8,7)
f("o1x","OSC 1 PHASE MODE: x","Osc 1 phase mode x","B",5,5)
f("o1dash","OSC 1 PHASE MODE: -","Osc 1 phase mode -","B",5,5)
f("o1o","OSC 1 PHASE MODE: o","Osc 1 phase mode o","B",5,5)
f("o2x","OSC 2 PHASE MODE: x","Osc 2 phase mode x","B",5,5)
f("o2dash","OSC 2 PHASE MODE: -","Osc 2 phase mode -","B",5,5)
f("o2o","OSC 2 PHASE MODE: o","Osc 2 phase mode o","B",5,5)
f("o1fm","FM AMOUNT","FM amount","K",14,14,"FM Amount",11)
f("o1mix","OSC MIX","Oscillator mix","K",14,14,"Osc Mix",10)
f("ringmod","RING MOD","Ring modulation on/off","B",8,8,"Ring Mod",12,M,"tooltip 'Ring Mod'; Remote 'Ring Mod'")
f("noiselight","NOISE on/off light","Noise on/off","B",7,7,"Noise On/Off",13)
f("noisedecay","NOISE DECAY","Noise decay","K",14,14,"Noise Decay",15)
f("noisecolor","NOISE COLOR","Noise color","K",14,14,"Noise Color",16)
f("noiselevel","NOISE LEVEL","Noise level","K",14,14,"Noise Level",14)
f("lfo1sync","LFO 1 SYNC","LFO tempo sync","B",8,8,"LFO Sync Enable",43)
f("lfo1rate","LFO 1 RATE","LFO 1 rate","K",14,14,"LFO1 Rate",40)
f("lfo1amt","LFO 1 AMOUNT","LFO 1 amount","K",14,14,"LFO1 Amount",41)
for i in range(6): f("l1w%d"%(i+1),"LFO 1 WAVE %d"%(i+1),"LFO 1 waveform %d"%(i+1),"B",5,5)
f("l1wbtn","LFO 1 WAVEFORM button","LFO 1 waveform (steps through)","B",10,7,"LFO1 Wave",39)
for n in ("osc12","osc2","ffreq","fm","phase","mix"): f("l1d_"+n,"LFO 1 DEST: "+n,"LFO 1 destination "+n,"B",5,5)
f("l1dbtn","LFO 1 DEST button","LFO 1 destination (steps through)","B",10,7,"LFO1 Dest",42)
for n in ("osc12","phase","ffreq2","amp"): f("l2d_"+n,"LFO 2 DEST: "+n,"LFO 2 destination "+n,"B",5,5)
f("l2dbtn","LFO 2 DEST button","LFO 2 destination (steps through)","B",10,7,"LFO2 Dest",46)
f("l2rate","LFO 2 RATE","LFO 2 rate","K",14,14,"LFO2 Rate",44)
f("l2amt","LFO 2 AMOUNT","LFO 2 amount","K",14,14,"LFO2 Amount",45)
f("l2kbd","LFO 2 KBD","LFO 2 keyboard tracking","K",14,14)
f("l2delay","LFO 2 DELAY","LFO 2 delay","K",14,14)
for k,l,sl in (("A","A",35),("D","D",36),("S","S",None),("R","R",None)):
    nm={"A":"Mod Env Attack","D":"Mod Env Decay","S":"Mod Env Sustain","R":"Mod Env Release"}[k]
    f("menv"+k,"MOD ENV "+l,"Modulation envelope "+nm.split()[-1].lower(),"S",6,28,nm,sl,M,"tooltip '%s'"%nm)
f("menvamt","MOD ENV AMT","Modulation envelope gain","K",14,14,"Mod Env Gain",38)
f("menvicon","MOD ENV INVERT","Modulation envelope invert","B",12,10)
for n in ("osc1","osc2","mix","fm","phase","freq2"): f("md_"+n,"MOD ENV DEST: "+n,"Mod envelope destination "+n,"B",5,5)
f("mdbtn","MOD ENV DEST button","Mod envelope destination (steps through)","B",10,7,"Mod Env Dest",37)
f("f1freq","FILTER 1 FREQ","Filter 1 frequency","S",6,40,"Filter Freq",18)
f("f1res","FILTER 1 RES","Filter 1 resonance","S",6,40,"Filter Res",19)
f("f1link","FILTER LINK","Link filter 1 and 2 frequency","B",8,8)
f("f1kbd","FILTER KBD","Filter keyboard tracking","K",14,14,"Filter Kbd Track",20)
f("f1type","FILTER TYPE button","Filter 1 type (steps through)","B",10,7,"Filter Type",17)
for n,l in (("notch","NOTCH"),("hp12","HP 12"),("bp12","BP 12"),("lp12","LP 12"),("lp24","LP 24")): f("f1m_"+n,"FILTER TYPE: "+l,"Filter 1 type "+l,"B",5,5)
f("f2light","FILTER 2 on/off light","Filter 2 on/off","B",7,7,"Filter2 On/Off",21)
f("f2freq","FILTER 2 FREQ","Filter 2 frequency","S",6,40,"Filter2 Freq",22,M,"no tooltip after 2 tries; Remote 'Filter2 Freq' matched by position")
f("f2res","FILTER 2 RES","Filter 2 resonance","S",6,40,"Filter2 Res",23)
f("f2level","LEVEL","Master level","S",6,40,"Master Level",48,M,"tooltip 'Master Level'; Remote 'Master Level'")
for k,l,nm,sl in (("A","A","Filter Env Attack",25),("D","D","Filter Env Decay",26),("S","S","Filter Env Sustain",27),("R","R","Filter Env Release",28)):
    f("fenv"+k,"FILTER ENV "+l,"Filter envelope "+nm.split()[-1].lower(),"S",6,28,nm,sl,M,"tooltip '%s'"%nm)
f("fenvamt","FILTER ENV AMT","Filter envelope amount","K",14,14,"Filter Env Amount",24)
f("fenvicon","FILTER ENV INVERT","Filter envelope invert","B",12,10)
for k,l,nm,sl,cf,w in (("A","A","Amp Env Attack",30,"high",""),("D","D","Amp Env Decay",31,"high",""),("S","S","Amp Env Sustain",32,M,"no tooltip after 2 tries; matched by position in the A-D-S-R row"),("R","R","Amp Env Release",33,"high","")):
    f("aenv"+k,"AMP ENV "+l,"Amp envelope "+nm.split()[-1].lower(),"S",6,28,nm,sl,cf,w)
for k,l,w,nm,sl in (("v_amp","AMP","Velocity to amp level","Amp Vel Amount",34),("v_fm","FM","Velocity to FM amount",None,None),("v_menv","M.ENV","Velocity to mod envelope",None,None),("v_phase","PHASE","Velocity to phase difference",None,None),("v_freq2","FREQ 2","Velocity to filter 2 frequency",None,None),("v_fenv","F.ENV","Velocity to filter envelope amount","Filter Env Vel Amount",29),("v_fdec","F.DEC","Velocity to filter decay",None,None),("v_mix","MIX","Velocity to osc mix",None,None),("v_aatk","A.ATK","Velocity to amp attack",None,None)):
    f(k,"VELOCITY "+l,w,"K",14,14,nm,sl)
# auto-name: hovered tooltip equal to a Remote item (case-insensitive) becomes reason_name (no slot)
def _walk(o):
    if isinstance(o,dict):
        for v in o.values(): yield from _walk(v)
    elif isinstance(o,list):
        for v in o: yield from _walk(v)
    elif isinstance(o,str): yield o
def _find(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if "ubTractor" in str(k) and isinstance(v,(dict,list)): return v
            r=_find(v)
            if r is not None: return r
    elif isinstance(o,list):
        for v in o:
            r=_find(v)
            if r is not None: return r
VOC={s.lower():s for s in _walk(_find(json.load(open("../../docs/reason/remote-vocab.json"))) or [])}
for r in rows:
    if r[2] is None:
        m=re.match(r'tooltip "(.*)"$',chk[r[0]])
        if m and m.group(1).lower() in VOC:
            r[2]=VOC[m.group(1).lower()]; r[3]=None
            if not r[8]: r[8]=NOSLOT
# back (screen coords)
B=[];CB={}
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],""]); CB[label]=c(key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",190,135)
b("cv","Seq CV In","Note CV input (sequencer)","J",190,164)
for i,(key,lab) in enumerate((("pitch","Osc Pitch"),("phase","Osc Phase"),("fm","FM Amount"),("f1freq","Filter 1 Freq"),("f1res","Filter 1 Res"),("f2freq","Filter 2 Freq"),("level","Amp Level"),("mw","Mod Wheel"),("pw","Pitch Wheel"))):
    y=(135,164,193,222,251,281,310,339,369)[i]
    b(key+"_trim",lab+" Mod trim","Amount for %s modulation input"%lab.lower(),"K",308,y,14,14)
    b(key+"_jack",lab+" Mod In","Modulation input: "+lab.lower(),"J",337,y)
b("menv_out","Mod Env Out","Modulation output: mod envelope","J",496,135)
b("fenv_out","Filter Env Out","Modulation output: filter envelope","J",496,164)
b("lfo_out","LFO 1 Out","Modulation output: LFO 1","J",496,193)
b("ampgate","Amp Env Gate In","Gate input: amp envelope","J",676,135)
b("fgate","Filter Env Gate In","Gate input: filter envelope","J",676,164)
b("mgate","Mod Env Gate In","Gate input: mod envelope","J",676,193)
b("out","Audio Out","Audio output (mono)","J",822,139,14,14)
base=dict(device="SubTractor Analog Synthesizer",prefix="SUBT",remote_scope="Propellerheads / SubTractor Analog Synthesizer",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="subtractor",front_raw="_captures_batchE/subtractor_front_raw.jpg",back_raw="_captures_batchE/subtractor_back_raw.jpg",front=rows,back=B),open("tools/specs/subtractor.json","w"))
json.dump(dict(device="SubTractor Analog Synthesizer",front=chk,back=CB,views={},view_titles={}),open("tools/checks/subtractor.json","w"),indent=0)
print(len(rows),len(B))
