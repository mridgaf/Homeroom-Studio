import json
# CVA-7 CV Analyzer (pongasoft RE). Front: screen=419+px/1.3188, 394+py/1.3188. Back: screen=453+px/1.3189, 394+py/1.3189.
T=lambda s:'tooltip "%s"'%s
NT="no tooltip in Reason (hovered 1.3 s)"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/cva7_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    if v.startswith("(no tooltip"): return NT
    return T(v)
K=1.3188; OX,OY=419,394
rows=[]; chk={}; M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(435,405))
f("tape","CVA-7 1 tape","Device name tape (vertical)","D",8,28,conf=M,pos=(436,462))
f("cvdisp","CV display","Current CV value display","D",32,12,conf=M,pos=(517,466))
f("maxmin","MAX / MIN display","Highest and lowest CV seen","D",32,22,conf=M,pos=(532,503))
f("scale","RAW / % / INT switch","Number scale of the displays: Raw, Percent, Integer","S",8,20,pos=(573,470))
f("reset","RESET","Reset the min/max readings","B",10,10,pos=(573,513))
f("auto","AUTO knob (OFF..10s)","Automatic min/max reset time","K",16,16,pos=(649,475))
f("kbled","AS GATE / AS NOTE button","Keyboard-view light button (tooltip 'Keyboard')","B",8,8,conf=M,why="tooltip 'Keyboard' on the red light next to AS GATE / AS NOTE",pos=(707,417))
f("roll","KEYBOARD / piano roll","Piano-key strip at the left of the screen","D",20,40,conf=M,pos=(708,470))
f("graphview","GRAPH SCREEN","CV graph screen","D",150,50,conf=M,pos=(895,460))
f("live","LIVE VIEW button","Live view button","B",24,20,pos=(1099,435))
f("graph","GRAPH button","Graph on/off (red light)","B",8,8,pos=(1155,417))
f("color","COLOR button","Colour mode light","B",8,8,pos=(1155,457))
f("zoom","ZOOM","Graph zoom","K",15,15,pos=(1101,491))
f("gscale","SCALE","Graph scale","K",13,13,pos=(1155,497))
B=[];CB={}
BK=1.3189; BX,BY=453,394
def b(key,label,what,typ,sx,sy,hw=9,hh=9,why=""):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],why]); CB[label]=c(key,back)
b("cvin","CV In","CV input","J",657,458)
b("trim","CV In trim","Amount for CV input","K",657,503,13,13)
for i,x in enumerate((728,752,775,799)):
    b("out1" if i==0 else "out1","CV Out %d slider (type)"%(i+1),"CV output %d type slider: Passthrough / Inverse / Unipolar / Bipolar"%(i+1),"S",x,478,7,28)
    CB["CV Out %d slider (type)"%(i+1)]=T("CV Out Type [3]: Passthrough") if i==2 else "not hovered separately: same row as hovered slider 3 (tooltip pattern 'CV Out Type [N]')"
for i,x in enumerate((728,752,775,799)):
    b("out1","CV Out %d jack"%(i+1),"CV output %d"%(i+1),"J",x,456)
    CB["CV Out %d jack"%(i+1)]=T("CV Out [1]") if i==0 else "not hovered separately: same row as hovered jack 1 (tooltip pattern 'CV Out [N]')"
b("auxcv","Aux Out CV","Aux CV output","J",947,457)
b("auxmax","Aux Out Max","Aux output: highest value","J",947,481)
b("auxmin","Aux Out Min","Aux output: lowest value","J",947,505)
b("tape","CVA-7 1 tape (back)","Device name tape","D",517,457,28,7)
base=dict(device="CVA-7 CV Analyzer",prefix="CVA7",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="cva-7",front_raw="_captures_batchE/cva7_front_raw.jpg",back_raw="_captures_batchE/cva7_back_raw.jpg",front=rows,back=B),open("tools/specs/cva-7.json","w"))
json.dump(dict(device="CVA-7 CV Analyzer",front=chk,back=CB,views={},view_titles={}),open("tools/checks/cva-7.json","w"),indent=0)
print(len(rows),len(B))
