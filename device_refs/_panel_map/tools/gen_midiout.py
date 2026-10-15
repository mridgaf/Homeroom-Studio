import json
# MIDI Out Device. Front: screen = 420+px/1.3188, 466+py/1.3188. Back: screen = 455+px/1.3189, 466+py/1.3189.
# No Remote map / vocab entry -> no names/slots; tooltips only.
NT="no tooltip in Reason (hovered 1.3 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/midiout_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    if v.startswith("(no tooltip"): return NT
    return T(v)
K=1.3188; OX,OY=420,466
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(440,481))
f("pitchwheel","PITCH wheel","Pitch bend wheel","S",14,18,pos=(482,497))
f("modwheel","MOD wheel","Modulation wheel (sent as CC 1)","S",14,18,pos=(528,497))
f("tape","Name tape","Device name tape","D",40,8,conf=M,pos=(607,521))
f("noteled","NOTE light","Note-on indicator","D",5,5,conf=M,pos=(680,483))
f("midiled","MIDI light","MIDI-out indicator","D",5,5,conf=M,pos=(680,496))
f("progfield","PROGRAM field","Program number field","D",12,8,conf=M,pos=(818,484))
f("progup","PROGRAM arrow up","Program number up","B",6,5,conf=M,pos=(838,480))
f("progdn","PROGRAM arrow down","Program number down","B",6,5,conf=M,pos=(838,488))
f("progon","PROGRAM ON","Program change on/off","B",9,7,pos=(858,484))
f("chfield","MIDI CHANNEL field","MIDI channel number","D",12,8,pos=(818,502))
f("chup","MIDI CHANNEL arrow up","MIDI channel up","B",6,5,conf=M,pos=(838,498))
f("chdn","MIDI CHANNEL arrow down","MIDI channel down","B",6,5,conf=M,pos=(838,506))
f("devsel","MIDI DEVICE selector","MIDI output device menu (IAC Driver Bus 1 shown)","B",65,8,conf=M,pos=(770,520))
f("devarrow","MIDI DEVICE arrow","Opens the MIDI output device menu","B",8,8,conf=M,pos=(838,520))
f("cvon","CV IN ON","CV in to MIDI CC out on/off","B",9,8,pos=(892,484))
for k,l,y in (("grp12","1-2",482),("grp34","3-4",495),("grp56","5-6",508),("grp78","7-8",520)):
    f(k,"CV PANEL "+l,"Chooses which pair of CV inputs the panel shows ("+l+")","B",11,6,pos=(916,y))
for k,l,y in (("led12","1-2",482),("led34","3-4",495),("led56","5-6",508),("led78","7-8",520)):
    f(k,"CV PANEL "+l+" light","Light for CV panel "+l,"D",4,4,conf=M,pos=(936,y))
f("scale1","SCALE CV 1","CV 1 scale","K",12,12,pos=(993,497))
f("scale2","SCALE CV 2","CV 2 scale","K",12,12,pos=(993,515))
f("off1","OFFSET CV 1","CV 1 offset (tooltip reads 'CC 0: 0')","K",12,12,why="tooltip shows 'CC 0' not 'Offset'; name by position under OFFSET",conf=M,pos=(1029,497))
f("off2","OFFSET CV 2","CV 2 offset (tooltip reads 'CC 0: 0')","K",12,12,why="tooltip shows 'CC 0' not 'Offset'; name by position under OFFSET",conf=M,pos=(1029,515))
f("cc1","CC 1 assignment","CC number for CV 1","D",12,8,pos=(1080,497))
f("cc2","CC 2 assignment","CC number for CV 2","D",12,8,pos=(1080,515))
f("out1","CC OUTPUT 1 display","CC output level display, CV 1","D",38,7,conf=M,pos=(1135,497))
f("out2","CC OUTPUT 2 display","CC output level display, CV 2","D",38,7,conf=M,pos=(1135,515))
B=[];CB={}
BK=1.3189; BX,BY=455,466
def b(key,label,what,typ,sx,sy,hw=10,hh=10):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
b("gate","Gate CV In","Gate input (sequencer control); tooltip 'Gate CV In'","J",618,498)
b("cv","Pitch CV In","CV input (sequencer control, pitch); tooltip 'Pitch CV In'","J",618,520)
b("pbtrim","Pitch Bend CV trim","Amount for pitch bend CV","K",692,498,12,12)
b("pbjack","Pitch Bend CV In","CV input: pitch bend","J",715,498)
b("mwtrim","Mod Wheel CV trim","Amount for mod wheel CV","K",692,520,12,12)
b("mwjack","Mod Wheel CV In","CV input: mod wheel","J",715,520)
for i,(x,y) in enumerate(((913,498),(913,520),(969,498),(969,520),(1022,498),(1022,520),(1074,498),(1074,520))):
    b("cv%d"%(i+1),"CV %d In"%(i+1),"CV input %d (to MIDI CC out)"%(i+1),"J",x,y)
b("tape","Name tape (back)","Device name tape on the back","D",507,510,28,7)
b("fold","(triangle, back)","Fold/unfold device","B",441,481,8,8)
base=dict(device="MIDI Out Device",prefix="MIDO",remote_scope="none (no Remote map or vocab entry found); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="midi-out",front_raw="_captures_batchE/midiout_front_raw.jpg",back_raw="_captures_batchE/midiout_back_raw.jpg",front=rows,back=B),open("tools/specs/midi-out.json","w"))
json.dump(dict(device="MIDI Out Device",front=chk,back=CB,views={},view_titles={}),open("tools/checks/midi-out.json","w"),indent=0)
print(len(rows),len(B))
