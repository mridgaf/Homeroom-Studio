import json
# Radical Piano. One front picture + one back picture (same frame: screen = 70+px/1.63, 66+py/1.63).
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists but is beyond the 48 knob slots of our remotemap (not mapped)"
PAT="not hovered: same group as the hovered LED; tooltip is the group name"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/radicalpiano_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
K=1.63; OX,OY=70,66
rows=[]; chk={}
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None,ck=None):
    sx,sy=pos
    x=round((sx-OX)*K); y=round((sy-OY)*K)
    if name and slot is None and not why: why=NOSLOT
    rows.append([label,what,name,slot,[x,y],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=ck or c(key)
def px(x,y): return (OX+x/K,OY+y/K)
M="medium"
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(96,86))
f("tape","Patch name tape","Patch name tape","D",25,8,"Device Name",conf=M,why="Remote item 'Device Name'; tooltip shows the patch name; convention from earlier devices",pos=(348,100))
f("noteled","NOTE light","Note-on indicator","D",5,5,conf=M,pos=(107,122))
f("audioin","AUDIO IN light","Audio-input indicator","D",5,5,conf=M,pos=(157,122))
f("character","CHARACTER","Character (subdued to agitated)","K",20,20,"Character",3,pos=(231,220))
f("micblend","MICROPHONE BLEND","Mix between the two microphone sets","K",40,40,"Microphone and Instrument Blend",17,M,"tooltip begins 'Microphone and Instrument...' (cut off by the screen); Remote 'Microphone and Instrument Blend' (slot 17)",pos=(535,189))
LROWS=(138,165,192,219,246); NAMES=("VINTAGE MONO","AMBIENCE","FLOOR","JAZZ","CLOSE")
for r,(py,nm) in enumerate(zip(LROWS,NAMES)):
    xs=(607,637,667) if r>=3 else (637,667)
    for ci,x in enumerate(xs):
        hov=(r==4 and ci in (1,2))
        f("mic1a" if hov and ci==1 else "mic1b","MIC 1 LED %s %d"%(nm,ci+1),"Microphone 1 type: %s, position %d"%(nm.lower(),ci+1),"B",6,6,"Microphone 1 Type" if (r==0 and ci==0) else None,15 if (r==0 and ci==0) else None,M if (r==0 and ci==0) else "high","tooltip 'Microphone 1 Type' (one LED row stands for the whole group; slot is shared by all of them)" if (r==0 and ci==0) else "",pos=px(x,py),ck=T("Microphone 1 Type") if hov else PAT)
RROWS=LROWS
for r,(py,nm) in enumerate(zip(RROWS,NAMES)):
    xs=(892,922,952) if r>=3 else (892,922)
    for ci,x in enumerate(xs):
        hov=(r==3)
        f("mic2a","MIC 2 LED %s %d"%(nm,ci+1),"Microphone 2 type: %s, position %d"%(nm.lower(),ci+1),"B",6,6,"Microphone 2 Type" if (r==0 and ci==0) else None,16 if (r==0 and ci==0) else None,M if (r==0 and ci==0) else "high","tooltip 'Microphone 2 Type' (one LED row stands for the whole group; slot is shared by all of them)" if (r==0 and ci==0) else "",pos=px(x,py),ck=T("Microphone 2 Type") if hov else PAT)
f("volume","VOLUME","Master volume","K",16,16,"Master Volume",14,pos=(862,221))
f("patcharrows","(patch arrows)","Previous / next patch","B",8,12,"Select Previous Patch",why="tooltip is for the upper half; lower half = Select Next Patch, not hovered",pos=(374,286))
f("patchfolder","(patch folder)","Browse patch","B",9,9,pos=(398,286))
f("patchdisk","(patch disk)","Save patch","B",9,9,pos=(421,286))
f("patchdisp","Patch display","Patch name display","D",75,12,pos=(580,286),conf=M)
for key,lab,what,name,slot,pos,hw in (
 ("velhigh","VELOCITY RESPONSE HIGH","Velocity response high","Vel Response High",25,(127,359),16),
 ("vellow","VELOCITY RESPONSE LOW","Velocity response low","Vel Response Low",26,(127,416),16),
 ("velcurve","VELOCITY RESPONSE CURVE","Velocity response curve","Vel Response Curve",24,(127,470),16),
 ("cent","TUNE CENT","Tune in cents","Tune",22,(231,358),16),
 ("drift","TUNE DRIFT","Tune drift","Tune Drift",23,(231,416),16),
 ("resLevel","RESONANCE LEVEL","Sympathetic resonance level","Symp Res Level",20,(442,358),16),
 ("resRelease","RESONANCE RELEASE TIME","Sympathetic resonance release time","Symp Res Release Time",21,(442,416),16),
 ("envAttack","ENVELOPE ATTACK","Envelope attack (ms)","Env Attack",9,(547,358),16),
 ("envDecay","ENVELOPE DECAY CURVE","Envelope decay curve","Env Decay Curve",10,(547,416),16),
 ("envRelease","ENVELOPE RELEASE","Envelope release","Env Release",11,(547,470),16),
 ("keydown","MECHANICS KEY DOWN","Key-down noise level","Key Down Level",12,(653,358),16),
 ("keyup","MECHANICS KEY UP","Key-up noise level","Key Up Level",13,(653,416),16),
 ("pedal","MECHANICS PEDAL","Pedal noise level","Pedal Level",18,(653,470),16),
 ("eqhi","EQ HI GAIN","EQ high gain","EQ Hi Gain",5,(758,358),16),
 ("eqmid","EQ MID GAIN","EQ mid gain","EQ Mid Gain",7,(758,416),16),
 ("eqlo","EQ LO GAIN","EQ low gain","EQ Lo Gain",6,(758,470),16),
 ("ambLevel","AMBIENCE LEVEL","Ambience level","Ambience Level",1,(861,358),16),
 ("comp","OUTPUT COMP","Compression amount","Compression Amount",4,(968,358),16),
 ("width","OUTPUT WIDTH","Stereo width","Stereo Width",19,(968,416),16)):
    f(key,lab,what,"K",hw,hw,name,slot,pos=pos)
f("velx","VELOCITY X button","Velocity response X (reset)","B",9,9,pos=(151,363))
f("vels","VELOCITY S button","Velocity response S (reset)","B",9,9,pos=(103,419))
f("pedalmeter","SUSTAIN PEDAL meter","Sustain pedal position meter","D",10,40,pos=(336,420),conf=M)
f("eqlight","EQ on/off light","EQ on/off","B",7,7,"EQ On/Off",8,pos=(725,326))
for i,(nm,y) in enumerate((("SMALL ROOM",409),("LARGE ROOM",431),("HALL",453),("THEATER",474))):
    f("amb%d"%(i+1),"AMBIENCE TYPE: "+nm,"Ambience type "+nm.lower(),"B",7,7,"Ambience Type" if i==0 else None,2 if i==0 else None,M if i==0 else "high","tooltip 'Ambience Type' (one of four buttons; slot is shared)" if i==0 else "",pos=(839,y))
B=[];CB={}
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],""]); CB[label]=c(key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",273,212)
b("cv","Seq CV In","CV input (sequencer)","J",273,243)
b("pitch_trim","Pitch CV trim","Amount for pitch CV","K",443,212,14,14)
b("pitch_jack","Pitch CV In","CV input: pitch","J",470,212)
b("vol_trim","Volume CV trim","Amount for volume CV","K",443,243,14,14)
b("vol_jack","Volume CV In","CV input: master volume","J",470,243)
b("audioin","Audio In","Audio input","J",669,212,14,14)
b("outL","Audio Out L","Audio output, left","J",775,232,14,14)
b("outR","Audio Out R","Audio output, right","J",825,232,14,14)
base=dict(device="Radical Piano",prefix="RADP",remote_scope="Propellerhead Software / se.propellerheads.radicalpiano",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="radical-piano",front_raw="_captures_batchE/radicalpiano_front_raw.jpg",back_raw="_captures_batchE/radicalpiano_back_raw.jpg",front=rows,back=B),open("tools/specs/radical-piano.json","w"))
json.dump(dict(device="Radical Piano",front=chk,back=CB,views={},view_titles={}),open("tools/checks/radical-piano.json","w"),indent=0)
print(len(rows),len(B))
