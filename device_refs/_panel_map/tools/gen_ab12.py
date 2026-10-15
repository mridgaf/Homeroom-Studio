import json
# A/B 12 Audio Out Switch (pongasoft Rack Extension). No Remote map; tooltips only.
# Front: screen = 419+px/1.3182, 392+py/1.3182. Back: screen = 453+px/1.3193, 392+py/1.3193.
T=lambda s:'tooltip "%s"'%s
NT="no tooltip in Reason (hovered 2 s)"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/ab12_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    if v.startswith("(no tooltip"): return NT
    return T(v)
K=1.3182; OX,OY=419,392
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(437,405))
f("tape","AB12AUDOUT 1 tape","Device name tape (vertical, left edge)","D",8,30,conf=M,pos=(437,460))
ROWY=(422,466,508)
for bank,xs in (("A",(499,556,585,630,659,698)),("B",(919,979,1007,1053,1082,1120))):
    # order: left group = display, knob, button for rows 1-3; right group = button, knob, display for rows 4-6
    for r in range(3):
        y=ROWY[r]; n=r+1
        f("disp%s%d"%(bank,n),"%s%d display"%(bank,n),"Name display for output %s%d"%(bank,n),"D",32,8,conf=M,pos=(xs[0] if bank=="A" else xs[0],y))
        f("knob%s%d"%(bank,n),"%s%d VOLUME"%(bank,n),"Volume of output %s%d"%(bank,n),"K",12,12,pos=(xs[1],y))
        f("btn%s%d"%(bank,n),"%s%d button"%(bank,n),"Switch button for output %s%d"%(bank,n),"B",11,11,pos=(xs[2],y))
    for r in range(3):
        y=ROWY[r]; n=r+4
        f("btn%s%d"%(bank,n),"%s%d button"%(bank,n),"Switch button for output %s%d"%(bank,n),"B",11,11,pos=(xs[3],y))
        f("knob%s%d"%(bank,n),"%s%d VOLUME"%(bank,n),"Volume of output %s%d"%(bank,n),"K",12,12,pos=(xs[4],y))
        f("disp%s%d"%(bank,n),"%s%d display"%(bank,n),"Name display for output %s%d"%(bank,n),"D",32,8,conf=M,pos=(xs[5],y))
f("ab","A / B indicator lights","Shows which bank is active (A or B light)","D",20,10,conf=M,pos=(820,463))
f("abknob","A/B big knob","Bank switch knob (no tooltip)","K",15,15,conf=M,pos=(820,463))
f("modesel","MODE SELECT Single","Mode select: Single / Multi / Instr (tooltip 'Mode Select' on all three)","B",9,8,pos=(788,494))
f("modesel","MODE SELECT Multi","Mode select: Single / Multi / Instr","B",9,8,pos=(819,494))
f("modesel","MODE SELECT Instr","Mode select: Single / Multi / Instr","B",9,8,pos=(849,494))
f("soften","SOFTEN","Soften (smooths switching)","B",11,8,pos=(809,523))
f("ov1","SINGLE OV light","Single override light","D",5,5,conf=M,pos=(873,518))
f("ov2","BANK OV light","Bank override light","D",5,5,conf=M,pos=(873,528))
B=[];CB={}
BK=1.3193; BX,BY=453,392
def b(key,label,what,typ,sx,sy,hw=9,hh=9):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
XS=(519,543,567,592,616,641,667,692,717,742,767,791)
names=["A1","A2","A3","A4","A5","A6","B1","B2","B3","B4","B5","B6"]
for i,n in enumerate(names): b("L"+n,"Audio Out %s Left (mono)"%n,"Audio output %s, left/mono"%n,"J",XS[i],433)
for i,n in enumerate(names): b("R"+n,"Audio Out %s Right"%n,"Audio output %s, right"%n,"J",XS[i],458)
for i,n in enumerate(names):
    b("giA1" if n=="A1" else ("giB1" if n=="B1" else "giA1"),"Gate In %s"%n,"Gate input %s"%n,"J",XS[i],484)
    if n not in ("A1","B1"): CB["Gate In %s"%n]="not hovered separately: same row as hovered "+("Gate In [A1]" if n[0]=="A" else "Gate In [B1]")+"; tooltip pattern 'Gate In [%s]' assumed"%n
for i,n in enumerate(names):
    b("goA1" if n=="A1" else ("goB1" if n=="B1" else "goA1"),"Gate Out %s"%n,"Gate output %s"%n,"J",XS[i],508)
    if n not in ("A1","B1"): CB["Gate Out %s"%n]="not hovered separately: same row as hovered "+("Gate Out [A1]" if n[0]=="A" else "Gate Out [B1]")+"; tooltip pattern 'Gate Out [%s]' assumed"%n
b("mainL","Main Audio In Left","Main audio input, left","J",848,433,11,11)
b("mainR","Main Audio In Right","Main audio input, right","J",848,459,11,11)
b("cvsingle","CV In (single mode)","CV input for single mode","J",851,517)
b("kbd","Keyboard Single switch","Keyboard control of single mode: Disabled / Enabled","B",8,12,)
B[-1][3]=[round((886-BX)*BK),round((517-BY)*BK)]
b("vcf","Volume Change Filter switch","Volume change filter Off / On","B",10,14)
B[-1][3]=[round((991-BX)*BK),round((439-BY)*BK)]
b("cvbank","CV Banks In","CV input for banks","J",967,512)
b("bankmap","CV Banks mapping switch","Bank CV mapping: Unipolar / Bipolar / Note","B",10,14)
B[-1][3]=[round((991-BX)*BK),round((505-BY)*BK)]
b("qr","QR code","pongasoft QR code (no tooltip)","D",20,20); B[-1][3]=[round((1099-BX)*BK),round((512-BY)*BK)]
b("power","Power switch (drawn)","Power connector area (no tooltip)","D",18,14); B[-1][3]=[round((1150-BX)*BK),round((515-BY)*BK)]
b("tape","AB12AUDOUT 1 tape (back)","Device name tape on the back","D",30,8); B[-1][3]=[round((1141-BX)*BK),round((421-BY)*BK)]
b("fold","(triangle, back)","Fold/unfold device","B",8,8); B[-1][3]=[round((476-BX)*BK),round((405-BY)*BK)]
base=dict(device="A/B 12 Audio Out Switch",prefix="AB12",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="ab12-audio-out",front_raw="_captures_batchE/ab12_front_raw.jpg",back_raw="_captures_batchE/ab12_back_raw.jpg",front=rows,back=B),open("tools/specs/ab12-audio-out.json","w"))
json.dump(dict(device="A/B 12 Audio Out Switch",front=chk,back=CB,views={},view_titles={}),open("tools/checks/ab12-audio-out.json","w"),indent=0)
print(len(rows),len(B))
