import json
# Morfin XF Crossfader (Groovy Melon Rack Extension). No Remote map; tooltips only.
# Front: screen = 420+px/1.3038, 464+py/1.3038. Back: screen = 455+px/1.3162, 465+py/1.3162.
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/morfin_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    return T(v)
K=1.3038; OX,OY=420,464
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(440,475))
f("chA","SELECT A","Channel A input select (pair 1-4)","K",17,17,pos=(493,503))
f("volA","VOLUME A","Channel A volume","K",17,17,pos=(560,503))
f("phA","PHASE INVERT A (Ø)","Channel A phase invert switch","B",7,10,pos=(602,515))
f("xfade","CROSSFADER A-B","Crossfader (hover the handle)","S",12,10,why="slider: hover the handle (it moves with the value)",pos=(704,500))
f("phB","PHASE INVERT B (Ø)","Channel B phase invert switch","B",7,10,pos=(807,515))
f("volB","VOLUME B","Channel B volume","K",17,17,pos=(850,503))
f("chB","SELECT B","Channel B input select (pair 1-4)","K",17,17,pos=(917,503))
f("type","FADE TYPE knob (CP/SQ/GT/AB/DIP/TRNS/SQRT/LIN/ST/MT)","Crossfade curve type","K",22,22,pos=(1022,502))
f("tape","MORFIN XF 1 tape","Device name tape","D",30,8,conf=M,pos=(1124,522))
B=[];CB={}
BK=1.3162; BX,BY=455,465
def b(key,label,what,typ,sx,sy,hw=10,hh=10):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
for n,x in ((1,623),(2,649),(3,674),(4,700)):
    b("i%dL"%n,"Input %d Left"%n,"Audio input %d, left"%n,"J",x,490)
    b("i%dR"%n,"Input %d Right"%n,"Audio input %d, right"%n,"J",x,514)
b("oL","Output Left / Mono","Audio output, left (mono)","J",813,491)
b("oR","Output Right","Audio output, right","J",813,514)
b("xjack","Crossfader CV In","CV input: crossfader","J",926,489)
b("xtrim","Crossfader CV trim","Amount for crossfader CV","K",921,517,12,12)
b("cvA","CV Output A","CV output A","J",951,489)
b("cvB","CV Output B","CV output B","J",951,517)
b("tape","MORFIN XF 1 tape (back)","Device name tape on the back","D",502,482,30,7)
base=dict(device="Morfin XF Crossfader",prefix="MORF",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="morfin-xf",front_raw="_captures_batchE/morfin_front_raw.jpg",back_raw="_captures_batchE/morfin_back_raw.jpg",front=rows,back=B),open("tools/specs/morfin-xf.json","w"))
json.dump(dict(device="Morfin XF Crossfader",front=chk,back=CB,views={},view_titles={}),open("tools/checks/morfin-xf.json","w"),indent=0)
print(len(rows),len(B))
