import json
# A/B Switch (pongasoft RE). Front: screen = 419+px/1.3063, 466+py/1.3063. Back: screen = 453+px/1.3189, 466+py/1.3189.
T=lambda s:'tooltip "%s"'%s
NT="no tooltip in Reason (hovered 1.4 s)"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/abswitch_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    if v.startswith("(no tooltip"): return NT
    return T(v)
K=1.3063; OX,OY=419,466
rows=[]; chk={}; M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(437,478))
f("title","A/B Switch title","Title text (no tooltip)","D",30,8,conf=M,pos=(486,478))
f("audioknob","AUDIO SWITCH knob","Audio switch knob: chooses A or B","K",20,20,conf=M,why="tooltip 'Switch Audio A & B' appeared while hovering the knob/A-B area; exact source of the text not isolated",pos=(572,503))
f("audioA","AUDIO A light","Audio A active light","D",5,5,conf=M,pos=(622,487))
f("audioB","AUDIO B light","Audio B active light","D",5,5,conf=M,pos=(622,516))
f("audioA","AUDIO A name field","Name field for audio A","D",28,6,conf=M,pos=(680,487))
f("audioB","AUDIO B name field","Name field for audio B","D",28,6,conf=M,pos=(680,516))
f("soften","SOFTEN","Soften (smooths switching)","B",10,7,pos=(743,486))
f("wave","wave icon","Small waveform icon (no tooltip)","D",10,8,conf=M,pos=(743,519))
f("tape","ABSWITCH 1 tape","Device name tape","D",28,7,conf=M,pos=(820,497))
f("cvknob","CV SWITCH knob","CV switch knob: chooses A or B","K",20,20,conf=M,why="tooltip 'Switch CV A & B' appeared while hovering the knob/A-B area; exact source not isolated",pos=(921,503))
f("cvA","CV A light","CV A active light","D",5,5,conf=M,pos=(958,487))
f("cvB","CV B light","CV B active light","D",5,5,conf=M,pos=(958,516))
f("cvA","CV A name field","Name field for CV A","D",28,6,conf=M,pos=(1030,487))
f("cvB","CV B name field","Name field for CV B","D",28,6,conf=M,pos=(1030,516))
f("cvB","pongasoft logo/QR","Logo and small code (no tooltip)","D",18,12,conf=M,pos=(1115,520))
B=[];CB={}
BK=1.3189; BX,BY=453,466
def b(key,label,what,typ,sx,sy,hw=9,hh=9):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
for k,nm,x in (("aIL","Audio A In L/Mono",591),("aIR","Audio A In R",625),("bIL","Audio B In L/Mono",665),("bIR","Audio B In R",691),("oL","Audio Out L/Mono",732),("oR","Audio Out R",759)):
    b(k,nm,"Audio jack: "+nm,"J",x,503)
b("actrl","Audio CV Control In","CV input that switches the audio","J",792,503)
b("cA","CV A In","CV input A","J",945,509)
b("cB","CV B In","CV input B","J",998,509)
b("cO","CV Out","Switched CV output","J",1051,509)
b("cctrl","CV Control In","CV input that switches the CV","J",1092,503)
b("power","Power area (drawn)","Power cable area (no tooltip)","D",1147,520,16,12)
b("tape","ABSWITCH 1 tape (back)","Device name tape","D",486,478,28,7)
b("fold","(triangle, back)","Fold/unfold device","B",437,481,8,8)
base=dict(device="A/B Audio & CV Switch",prefix="ABSW",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="ab-switch",front_raw="_captures_batchE/abswitch_front_raw.jpg",back_raw="_captures_batchE/abswitch_back_raw.jpg",front=rows,back=B),open("tools/specs/ab-switch.json","w"))
json.dump(dict(device="A/B Audio & CV Switch",front=chk,back=CB,views={},view_titles={}),open("tools/checks/ab-switch.json","w"),indent=0)
print(len(rows),len(B))
