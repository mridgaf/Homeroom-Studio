import json
# Monotone. Front: screen = 415+px/1.3166, 245+py/1.3166. Back: screen = 450+px/1.3176, 248+py/1.3176.
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/monotone_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
K=1.3166; OX,OY=415,245
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,name,slot,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
SELF="Remote item exists but has no knob slot in our remotemap"
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(442,262))
f("led","(patch light)","Small light left of the patch display (purpose not verified)","D",6,6,conf="low",pos=(722,262))
f("patchdisp","Patch display","Patch name display","D",45,10,"Patch Name",conf=M,why="Remote item Patch Name, no knob slot",pos=(787,262))
f("patchprev","(patch prev arrow)","Previous patch","B",8,6,"Select Previous Patch",pos=(853,256))
f("patchnext","(patch next arrow)","Next patch","B",8,6,"Select Next Patch",pos=(853,268))
f("folder","(patch folder)","Browse patch","B",9,9,pos=(875,262))
f("disk","(patch disk)","Save patch","B",9,9,pos=(894,262))
f("tape","Patch name tape","Patch name tape","D",35,9,"Device Name",conf=M,why="Remote item 'Device Name'; tooltip shows the patch name; convention from earlier devices",pos=(1003,261))
f("master","MASTER","Master volume","K",16,16,"Volume",39,pos=(1169,262))
f("portsw","PORTAMENTO MODE switch","Portamento mode (Off / On / Auto)","B",8,13,"Portamento Mode",37,pos=(450,366))
f("portknob","PORTAMENTO","Portamento time","K",16,16,"Portamento",36,pos=(499,366))
f("retrig","RETRIG","Retrigger button","B",10,10,"ReTrig",38,pos=(533,363))
f("range","RANGE","Pitch wheel range spinner (semitones)","D",14,10,conf=M,pos=(468,413))
f("pitchwheel","PITCH wheel","Pitch bend wheel","S",10,28,"Pitch Bend",34,why="tooltip '(Pitch Bend)'",pos=(469,470))
f("filtamt","MOD FILT","How much the mod wheel opens the filter","K",10,10,pos=(516,414))
f("lfoamt","MOD LFO","How much the mod wheel adds LFO","K",10,10,pos=(537,414))
f("modwheel","MOD wheel","Modulation wheel","S",10,28,"Mod Wheel",25,why="tooltip '(Mod Wheel)'",pos=(527,470))
f("osc1wave","OSC 1 WAVE","Oscillator 1 waveform","K",16,16,"Osc1 Wave",30,pos=(587,367))
f("osc1oct","OSC 1 OCT","Oscillator 1 octave","K",16,16,"Osc1 Oct",29,pos=(587,412))
f("oscmix","OSC MIX","Mix between oscillator 1 and 2","K",22,22,"Osc Mix",28,pos=(644,382))
f("osc2wave","OSC 2 WAVE","Oscillator 2 waveform","K",16,16,"Osc2 Wave",33,pos=(703,367))
f("osc2oct","OSC 2 OCT","Oscillator 2 octave","K",16,16,"Osc2 Oct",31,pos=(702,412))
f("noise","NOISE","Noise level","K",16,16,"Noise",26,pos=(619,458))
f("detune","DETUNE","Oscillator detune","K",16,16,"Osc Detune",27,pos=(670,458))
f("pitchlfo","PITCH LFO (LFO under OSC)","LFO amount on pitch","K",16,16,"Pitch LFO Amt",35,pos=(594,502))
f("fmenv","FM ENV","Envelope amount on FM","K",16,16,"FM Env Amt",12,pos=(644,502))
f("osc2semi","OSC 2 SEMI","Oscillator 2 pitch in semitones","K",16,16,"Osc2 Pitch",32,pos=(695,502))
f("fdrive","FILTER DRIVE","Filter drive","K",16,16,"Filter Drive",15,pos=(764,370))
f("ffreq","FILTER FREQ","Filter frequency","K",22,22,"Filter Freq",17,pos=(819,361))
f("freso","FILTER RESONANCE","Filter resonance","K",16,16,"Filter Reso",21,pos=(874,370))
f("fenv","FILTER ENV","Filter envelope amount","K",16,16,"Filter Env Amount",16,pos=(764,414))
f("fkey","FILTER KEY","Filter keyboard tracking","K",16,16,"Filter Key Amt",18,pos=(819,414))
f("flfo","FILTER LFO","Filter LFO amount","K",16,16,"Filter LFO Amt",19,pos=(874,414))
for k,l,n,s,x,y in (("aA","AMP A","Amp Attack",1,929,415),("aD","AMP D","Amp Decay",2,958,395),("aS","AMP S","Amp Sustain",4,988,397),("aR","AMP R","Amp Release",3,1019,394)):
    f(k,l+" fader","Amplifier envelope "+n.split()[1].lower(),"S",8,36,n,s,why="slider: hover the handle (it moves with the value)",pos=(x,386))
f("avel","AMP VEL","Velocity amount on amplifier","K",16,16,pos=(1058,414))
f("chAmt","CHORUS AMOUNT","Chorus amount","K",22,22,"Chorus Amount",5,pos=(1111,361))
f("chRate","CHORUS RATE","Chorus rate","K",16,16,"Chorus Rate",6,pos=(1111,414))
f("chSpread","CHORUS SPREAD","Chorus spread","K",16,16,"Chorus Spread",7,pos=(1111,458))
f("dlAmt","DELAY AMOUNT","Delay amount","K",22,22,"Delay Amount",8,pos=(1169,361))
f("dlTime","DELAY TIME","Delay time","K",16,16,"Delay Time",11,pos=(1169,414))
f("dlFb","DELAY FEEDBACK","Delay feedback","K",16,16,"Delay Feedback",9,pos=(1169,458))
f("dlPP","DELAY PING PONG","Ping pong button","B",8,8,"Delay Pingpong",10,pos=(1169,495))
f("lfoRate","LFO RATE","LFO rate","K",16,16,"LFO Rate",23,pos=(783,502))
f("lfoWave","LFO SHAPE","LFO waveform","K",16,16,"LFO Wave",24,pos=(826,502))
f("eA","ENV A","Filter envelope attack","K",16,16,"Filter Attack",13,pos=(893,502))
f("eD","ENV D","Filter envelope decay","K",16,16,"Filter Decay",14,pos=(929,502))
f("eS","ENV S","Filter envelope sustain","K",16,16,"Filter Sustain",22,pos=(965,502))
f("eR","ENV R","Filter envelope release","K",16,16,"Filter Release",20,pos=(1000,502))
f("eV","ENV VEL","Velocity amount on filter envelope","K",16,16,pos=(1037,502))
B=[];CB={}
BK=1.3176; BX,BY=450,248
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
b("cv","Seq CV In","CV input (sequencer note)","J",645,339)
b("gate","Seq Gate In","Gate input (sequencer)","J",645,362)
for k1,k2,nm,y in (("pb","","Pitch Bend",386),("mw","","Mod Wheel",410)):
    b(k1+"trim",nm+" CV trim","Amount for "+nm.lower()+" CV","K",648,y,13,13)
    b(k1+"jack",nm+" CV In","CV input: "+nm.lower(),"J",672,y)
for k,nm,y in (("mix","Osc Mix",339),("fm","FM Env",363),("nz","Noise Level",387),("fr","Filter Freq",410),("rs","Filter Res",434)):
    b(k+"trim",nm+" CV trim","Amount for "+nm.lower()+" CV","K",774,y,13,13)
    b(k+"jack",nm+" CV In","CV input: "+nm.lower(),"J",799,y)
b("outL","Audio Out Left","Audio output, left","J",900,339,13,13)
b("outR","Audio Out Right","Audio output, right","J",900,363,13,13)
base=dict(device="Monotone",prefix="MONO",remote_scope="Propellerhead Software / se.propellerheads.Monotone",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="monotone",front_raw="_captures_batchE/monotone_front_raw.jpg",back_raw="_captures_batchE/monotone_back_raw.jpg",front=rows,back=B),open("tools/specs/monotone.json","w"))
json.dump(dict(device="Monotone",front=chk,back=CB,views={},view_titles={}),open("tools/checks/monotone.json","w"),indent=0)
print(len(rows),len(B))
