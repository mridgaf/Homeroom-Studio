import json
# Klang. Front: screen = 420+px/1.317, 350+py/1.317. Back: screen = 415+px/1.3153, 350+py/1.3153.
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/klang_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") or v.startswith("(no tooltip:") else T(v)
K=1.317; OX,OY=420,350
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,name,slot,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(441,367))
f("patchdisp","Patch display","Patch name display","D",85,10,"Patch Name",conf=M,why="Remote item Patch Name, no knob slot",pos=(880,370))
f("patchprev","(patch prev arrow)","Previous patch","B",7,6,"Select Previous Patch",pos=(740,366))
f("patchnext","(patch next arrow)","Next patch","B",7,6,"Select Next Patch",pos=(740,376))
f("folder","(patch folder)","Browse patch","B",8,8,pos=(760,371))
f("disk","(patch disk)","Save patch","B",8,8,pos=(780,371))
f("tape","Patch name tape","Patch name tape","D",40,9,"Device Name",conf=M,why="Remote item 'Device Name'; tooltip shows the patch name; convention from earlier devices",pos=(1030,369))
f("master","MASTER VOLUME","Master volume","K",16,16,"Master_Volume",26,pos=(1159,371))
f("note","NOTE light","Note-on indicator","D",6,6,conf=M,pos=(467,414))
f("range","RANGE","Pitch wheel range spinner","D",14,8,conf=M,pos=(484,443))
f("pitchwheel","PITCH wheel","Pitch bend wheel","S",8,32,"Pitch Bend",30,why="tooltip '(Pitch Bend)'",pos=(480,510))
f("modwheel","MOD wheel","Modulation wheel","S",8,32,"Mod Wheel",27,why="tooltip '(Mod Wheel)'",pos=(507,510))
f("sstartmw","S. START (mod wheel)","Mod wheel amount on sample start","K",13,13,pos=(547,441))
f("ffreqmw","F. FREQ (mod wheel)","Mod wheel amount on filter cutoff","K",13,13,pos=(547,484))
f("levelmw","LEVEL (mod wheel)","Mod wheel amount on amp level","K",13,13,"Mod Wheel to Amp Level",28,pos=(547,525))
f("instrument","INSTRUMENT picture","Instrument picture","D",45,38,"Instrument",25,M,"tooltip 'Instrument: Struck Grand Piano'; the dropdown below it selects the instrument",pos=(648,455))
f("instsel","INSTRUMENT selector","Instrument name dropdown","B",55,8,conf=M,pos=(645,503))
f("sstart","S. START","Sample start","K",13,13,"SampleStart",37,pos=(603,534))
f("oct","OCT","Octave","K",13,13,"Octave",29,pos=(633,534))
f("semi","SEMI","Semitune","K",13,13,"Semitone" if False else "Semitune",38,pos=(663,534))
f("fine","FINE","Finetune","K",13,13,"Finetune",24,pos=(693,534))
f("fon","FILTER ON","Filter on/off","B",6,6,"Filter_On",18,pos=(742,414))
f("ftype","FILTER TYPE","Filter type menu (LP shown)","B",22,8,"Filter_Type",22,conf=M,pos=(815,414))
f("fcut","FILTER CUTOFF","Filter cutoff","K",15,15,"Filter_Cutoff",14,pos=(754,443))
f("freso","FILTER RESO","Filter resonance","K",15,15,"Filter_Reso",20,pos=(797,443))
f("fenv","FILTER ENV","Filter envelope amount","K",15,15,"Filter_Env",16,pos=(841,443))
for k,l,n,s,x in (("fA","FILTER A","Filter_Attack",13,743),("fD","FILTER D","Filter_Decay",15,763),("fS","FILTER S","Filter_Sustain",21,787),("fR","FILTER R","Filter_Release",19,809)):
    f(k,l+" fader","Filter envelope "+n.split("_")[1].lower(),"S",7,40,n,s,why="slider: hover the handle (it moves with the value)",pos=(x,517))
f("fvel","FILTER VEL","Velocity amount on filter","K",13,13,"Filter_Velocity",23,pos=(841,490))
f("fkbd","FILTER KBD","Filter key follow","K",13,13,"Filter_KeyFollow",17,pos=(841,535))
f("avel","AMP VEL","Velocity amount on amp","K",13,13,pos=(904,444))
for k,l,n,s,x in (("aA","AMP A","Amp_Attack",2,892),("aD","AMP D","Amp_Decay",3,915),("aS","AMP S","Amp_Sustain",5,936),("aR","AMP R","Amp_Release",4,958)):
    f(k,l+" fader","Amp envelope "+n.split("_")[1].lower(),"S",7,40,n,s,why="slider: hover the handle (it moves with the value)",pos=(x,517))
f("dlon","DELAY ON","Delay on/off","B",6,6,"Delay_On",9,pos=(1001,415))
f("dltime","DELAY TIME","Delay time (shows synced note value when SYNC is on)","K",15,15,"Delay_Time",12,M,"when SYNC is on the tooltip reads 'Synced Delay Time' (Remote item Synced_Delay_Time, slot 39, same knob)",pos=(1011,444))
f("dlfb","DELAY FEEDBACK","Delay feedback","K",15,15,"Delay_Feedback",8,pos=(1054,444))
f("dlsync","DELAY SYNC","Delay tempo sync","B",8,8,"Delay_Sync",11,pos=(1012,489))
f("dlpp","DELAY PING PONG","Ping pong","B",8,8,"Delay_PingPong",10,pos=(1053,489))
f("dldamp","DELAY DAMP","Delay damping","K",15,15,"Delay_Damp",7,pos=(1011,536))
f("dlamt","DELAY AMOUNT","Delay amount","K",17,17,"Delay Amount",6,pos=(1054,536))
f("rvon","REVERB ON","Reverb on/off","B",6,6,"Reverb_On",34,pos=(1107,415))
f("rvtime","REVERB TIME","Reverb time","K",15,15,"Reverb_Time",36,pos=(1116,444))
f("rvpre","REVERB PRE-DELAY","Reverb pre-delay","K",15,15,"Reverb_PreDelay",35,pos=(1159,444))
f("rvhi","REVERB HI DAMP","Reverb high damping","K",15,15,"Reverb_HighDamp",32,pos=(1116,490))
f("rvlo","REVERB LO DAMP","Reverb low damping","K",15,15,"Reverb_LowDamp",33,pos=(1159,490))
f("rvamt","REVERB AMOUNT","Reverb amount","K",17,17,"Reverb Amount",31,pos=(1159,536))
rows.append(["(synced) DELAY TIME","Same knob as DELAY TIME: Remote item for the time when SYNC is on","Synced_Delay_Time",39,[round((1011-OX)*K),round((444-OY)*K)+2],[round(15*K),round(15*K)],"K","medium","same physical knob as DELAY TIME; its tooltip reads 'Synced Delay Time' when SYNC is on"]); chk["(synced) DELAY TIME"]=T("Synced Delay Time: 3/16")
rows.append(["(no panel control) Aftertouch","Remote item 'Aftertouch': no matching control on the Klang panel","Aftertouch",1,[round((467-OX)*K),round((470-OY)*K)],[round(5*K),round(5*K)],"B","low","Remote vocabulary item; no matching control seen on the panel; row parked beside the wheels; NOT proven"]); chk["(no panel control) Aftertouch"]="not hovered: Remote item with no matching panel control"
B=[];CB={}
BK=1.3153; BX,BY=415,350
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",565,469)
b("cv","Seq CV In","CV input (sequencer note)","J",565,501)
b("pbtrim","Pitch Bend CV trim","Amount for pitch bend CV","K",663,469,13,13)
b("pbjack","Pitch Bend CV In","CV input: pitch bend","J",686,469)
b("mwtrim","Mod Wheel CV trim","Amount for mod wheel CV","K",663,501,13,13)
b("mwjack","Mod Wheel CV In","CV input: mod wheel","J",686,501)
b("cotrim","Filter Cutoff CV trim","Amount for filter cutoff CV","K",766,493,13,13)
b("cojack","Filter Cutoff CV In","CV input: filter cutoff","J",790,493)
b("retrim","Filter Resonance CV trim","Amount for filter resonance CV","K",837,493,13,13)
b("rejack","Filter Resonance CV In","CV input: filter resonance","J",860,493)
b("lvtrim","Amp Level CV trim","Amount for amp level CV","K",907,493,13,13)
b("lvjack","Amp Level CV In","CV input: amp level","J",930,493)
b("outL","Audio Out L / Mono","Audio output, left (mono)","J",1033,469,14,14)
b("outR","Audio Out R","Audio output, right","J",1082,469,14,14)
base=dict(device="Klang",prefix="KLNG",remote_scope="Propellerhead Software / se.propellerheads.Klang",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="klang",front_raw="_captures_batchE/klang_front_raw.jpg",back_raw="_captures_batchE/klang_back_raw.jpg",front=rows,back=B),open("tools/specs/klang.json","w"))
json.dump(dict(device="Klang",front=chk,back=CB,views={},view_titles={}),open("tools/checks/klang.json","w"),indent=0)
print(len(rows),len(B))
