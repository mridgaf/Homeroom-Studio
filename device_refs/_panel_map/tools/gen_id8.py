import json
# ID8. Front: screen = 420+px/1.3063, 466+py/1.3063. Back: screen = 455+px/1.3068, 462+py/1.3068.
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/id8_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
K=1.3063; OX,OY=420,466
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,name,slot,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("pitch","PITCH wheel","Pitch bend wheel","S",14,18,"Pitch Bend",6,why="tooltip 'Pitch Bend'",pos=(487,500))
f("mod","MOD wheel","Modulation wheel","S",14,18,"Mod Wheel",3,why="tooltip 'Mod Wheel'",pos=(531,500))
f("catprev","(category up arrow)","Previous category","B",8,8,"Select Previous Category",pos=(572,491))
f("catnext","(category down arrow)","Next category","B",8,8,"Select Next Category",pos=(572,511))
f("catdisp","Category display","Instrument category name (Piano shown)","D",70,22,"Category",1,M,"Remote item 'Category'; the arrows at its left step through categories; display itself has no tooltip",pos=(670,502))
for i,(nm,y) in enumerate((("Grand",483),("Upright",495),("Dance",508),("Vibes",521))):
    f("list%d"%(i+1),"SOUND LIST "+nm,"Sound list row: "+nm,"B",40,6,conf=M,pos=(800,y))
for i,(nm,y) in enumerate((("A",482),("B",495),("C",508),("D",521))):
    f("snd"+nm.lower(),"SOUND "+nm+" button","Sound "+nm+" button","B",7,6,"Sound "+nm,pos=(860,y))
f("p1","PARAMETER 1","Parameter 1 knob (what it does depends on the sound)","K",14,14,"Parameter 1",4,pos=(916,487))
f("p1disp","PARAMETER 1 name","Name of Parameter 1 (Delay shown)","D",25,8,conf=M,pos=(975,485))
f("p2","PARAMETER 2","Parameter 2 knob (what it does depends on the sound)","K",14,14,"Parameter 2",5,pos=(916,517))
f("p2disp","PARAMETER 2 name","Name of Parameter 2 (Chorus shown)","D",25,8,conf=M,pos=(975,517))
f("vol","VOLUME","Volume","K",17,17,"Volume",20,pos=(1057,500))
f("tape","Patch name tape","Name tape","D",25,8,"Device Name",conf=M,why="Remote item 'Device Name'; no tooltip on ID8",pos=(1120,477))
B=[];CB={}
BK=1.3068; BX,BY=455,462
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
b("outL","Audio Out Left / Mono","Audio output, left (mono)","J",799,503,12,12)
b("outR","Audio Out Right","Audio output, right","J",840,503,12,12)
b("power","Power switch (drawn)","Rocker switch drawn on the back panel (no tooltip)","B",1070,487,10,14)
b("tape","Name tape (back)","Name tape on the back panel","D",1035,523,28,8)
base=dict(device="ID8 Instrument Device",prefix="ID8",remote_scope="Propellerheads / ID8 Instrument Device",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="id8",front_raw="_captures_batchE/id8_front_raw.jpg",back_raw="_captures_batchE/id8_back_raw.jpg",front=rows,back=B),open("tools/specs/id8.json","w"))
json.dump(dict(device="ID8 Instrument Device",front=chk,back=CB,views={},view_titles={}),open("tools/checks/id8.json","w"),indent=0)
print(len(rows),len(B))
