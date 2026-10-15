import json
# Rytmik Drum Machine. Main panel (KICK selected). Front: screen = 420+px/1.3155, 172+py/1.3155. Back: screen = 455+px/1.3171, 178+py/1.3171.
# No Remote map / vocab for Rytmik -> no names/slots; tooltips are the only name source.
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/rytmik_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    if v.startswith("(no tooltip"): return v[1:].replace(")","",1) if False else NT+(v[v.index(")")+1:] if ")" in v and v.index(")")<len(v)-1 else "")
    return T(v)
K=1.3155; OX,OY=420,172
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(441,188))
f("patchdisp","Patch display","Patch name display","D",45,10,conf=M,pos=(788,188))
f("patchprev","(patch prev arrow)","Previous patch","B",7,5,pos=(888,184))
f("patchnext","(patch next arrow)","Next patch","B",7,5,pos=(888,193))
f("folder","(patch folder)","Browse patch","B",8,8,pos=(907,188))
f("disk","(patch disk)","Save patch","B",8,8,pos=(927,188))
f("tape","Patch name tape","Patch name tape","D",40,9,conf=M,pos=(1065,188))
f("wave","WAVEFORM display","Waveform of the selected drum's sample","D",245,58,conf=M,pos=(695,265))
f("startmark","(start marker)","Sample start marker (small triangle, top left of waveform)","D",6,6,conf="low",pos=(453,211))
f("endmark","(end marker)","Sample end marker (small triangle, right edge of waveform)","D",6,6,conf="low",pos=(938,322))
f("filterdisp","FILTER display","Filter curve of the selected drum","D",120,55,conf=M,pos=(1065,270))
f("samplearrowL","SAMPLE arrow left","Previous sample","B",7,7,conf=M,pos=(492,344))
f("samplename","SAMPLE name","Sample name of the selected drum","D",45,8,conf=M,pos=(570,344))
f("samplearrowR","SAMPLE arrow right","Next sample","B",7,7,conf=M,pos=(648,344))
for k,l,w,x in (("pan","PAN","Pan of the selected drum",743),("pitch","PITCH","Pitch of the selected drum (cents)",795),("fadein","FADE IN","Sample fade in",846),("fadeout","FADE OUT","Sample fade out",896),("dist","DISTORTION","Distortion amount",1005),("lowcut","LOW CUT","Low cut frequency",1066),("hicut","HI CUT","Hi cut frequency",1120)):
    f(k,l+" value","%s (value field)"%w,"D",22,8,conf=M,pos=(x,344))
PADX=(488,570.5,653,735.5,819,901,984,1066); NAMES=("KICK","SNARE","HIHAT","CYMBAL","TOM","CLAP","PERC","PERC")
for n in range(1,9):
    dx=83*(n-1)
    f("d%ddelay"%n,"DRUM %d DELAY"%n,"Drum %d delay send"%n,"K",13,13,pos=(468+dx,373))
    f("d%dreverb"%n,"DRUM %d REVERB"%n,"Drum %d reverb send"%n,"K",13,13,pos=(468+dx,412))
    f("d%dm"%n,"DRUM %d MUTE"%n,"Drum %d mute"%n,"B",10,8,pos=(468+dx,453))
    f("d%ds"%n,"DRUM %d SOLO"%n,"Drum %d solo"%n,"B",10,8,pos=(468+dx,475))
    f("d%dfader"%n,"DRUM %d fader"%n,"Drum %d level fader (no tooltip; value not shown)"%n,"S",8,45,conf=M,why="slider: hover the handle; no tooltip appears",pos=(496+dx,396))
    f("d%dpad"%n,"PAD %d %s"%(n,NAMES[n-1]),"Selects drum %d (%s) for the sample section above"%(n,NAMES[n-1]),"B",30,8,why="click verified: KICK -> SNARE -> KICK changed the sample section" if n<=2 else "same kind of pad button as pads 1-2 (click verified there)",pos=(PADX[n-1],497))
f("mpitch","MASTER FX PITCH","Master pitch (cents)","K",13,13,pos=(1131,371))
f("mreverb","MASTER FX REVERB","Master reverb","K",13,13,pos=(1131,411))
f("mfilter","MASTER FX FILTER","Master filter","K",13,13,pos=(1131,450))
f("mfader","MASTER FX fader","Master level fader (no tooltip)","S",8,45,conf=M,pos=(1158,396))
f("mpad","MASTER FX pad","Master FX strip button","B",30,8,conf=M,pos=(1150,497))
B=[];CB={}
BK=1.3171; BX,BY=455,178
def b(key,label,what,typ,sx,sy,hw=10,hh=10):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
GX=(530,555,581,606,644,669,694,720); SX=(815,840,864,889,927,952,977,1002)
for i in range(8): b("gi%d"%(i+1),"Gate In %d"%(i+1),"Gate input, drum %d"%(i+1),"J",GX[i],445,9,9)
for i in range(8): b("go%d"%(i+1),"Gate Out %d"%(i+1),"Gate output, drum %d"%(i+1),"J",GX[i],467,9,9)
for i in range(8): b("sl%d"%(i+1),"Sep Out %d Left"%(i+1),"Separate output %d, left (mono): tooltip '%s'"%(i+1,back["sl%d"%(i+1)]),"J",SX[i],447,11,11)
for i in range(8): b("sr%d"%(i+1),"Sep Out %d Right"%(i+1),"Separate output %d, right: tooltip '%s'"%(i+1,back["sr%d"%(i+1)]),"J",SX[i],471,11,11)
b("mainL","Main Out Left","Main audio output, left","J",1086,447,12,12)
b("mainR","Main Out Right","Main audio output, right","J",1111,447,12,12)
b("tape","Name tape (back)","Name tape on the back panel","D",474,340,9,30)
b("fold","(triangle, back)","Fold/unfold device","B",441,187,8,8)
base=dict(device="Rytmik Drum Machine",prefix="RYTM",remote_scope="none (no Remote map or vocab entry found); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="rytmik",front_raw="_captures_batchE/rytmik_front_raw.jpg",back_raw="_captures_batchE/rytmik_back_raw.jpg",front=rows,back=B),open("tools/specs/rytmik.json","w"))
json.dump(dict(device="Rytmik Drum Machine",front=chk,back=CB,views={},view_titles={}),open("tools/checks/rytmik.json","w"),indent=0)
print(len(rows),len(B))
