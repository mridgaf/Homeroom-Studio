import json
# Elements DS-LFO (AirRaid Audio Rack Extension). No Remote map -> no slots; tooltips only.
# Front: screen = 420+px/1.3138, 394+py/1.3138 (rack scrolled so DS-LFO top y~394). Back: screen = 450+px/1.3149, 394+py/1.3149.
NT="no tooltip in Reason (hovered 1.3 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/dslfo_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    if v.startswith("(no tooltip: check"): return "no tooltip (fold arrow); checked by eye"
    if v.startswith("(no tooltip"): return NT+(" at two offsets" if "twice" in v else "")
    return T(v)
K=1.3138; OX,OY=420,394
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(440,407))
f("patchdisp","Patch display","Patch name display","D",55,9,conf=M,pos=(786,415))
f("patchprev","(patch prev arrow)","Previous patch","B",7,5,pos=(855,411))
f("patchnext","(patch next arrow)","Next patch","B",7,5,pos=(855,420))
f("folder","(patch folder)","Browse patch","B",8,8,pos=(874,415))
f("disk","(patch disk)","Save patch","B",8,8,pos=(895,415))
f("tape","Patch name tape","Patch name tape (vertical, left edge)","D",8,32,conf=M,pos=(437,455))
for n,dx in ((1,0),(2,222)):
    f("l%dsync"%n,"LFO %d SYNC"%n,"LFO %d tempo sync on/off"%n,"B",7,6,conf=("high" if n==1 else M),why="" if n==1 else "no tooltip appeared (tried twice); function inferred by label and by LFO 1",pos=(532+dx,448))
    f("l%dmode"%n,"LFO %d MODE"%n,"LFO %d phase/spin mode on/off"%n,"B",7,6,conf=("high" if n==1 else M),why="" if n==1 else "no tooltip appeared (tried twice); function inferred by label and by LFO 1",pos=(591+dx,448))
    f("l%dshape"%n,"LFO %d SHAPE display"%n,"LFO %d waveform display"%n,"D",25,13,pos=(496+dx,490))
    f("l%dup"%n,"LFO %d SHAPE up"%n,"Next waveform","B",6,6,conf=M,pos=(527+dx,483))
    f("l%ddn"%n,"LFO %d SHAPE down"%n,"Previous waveform","B",6,6,conf=M,pos=(527+dx,497))
    f("l%dfreq"%n,"LFO %d FREQ"%n,"LFO %d frequency"%n,"K",17,17,pos=(574+dx,490))
    f("l%dphase"%n,"LFO %d PHASE/SPIN"%n,"LFO %d phase or spin"%n,"K",17,17,pos=(635+dx,490))
    f("l%doff"%n,"LFO %d OFFSET"%n,"LFO %d offset"%n,"K",17,17,pos=(697+dx,490))
f("mix","GLOBAL MIX 1+2","Mix between LFO 1 and LFO 2","K",17,17,pos=(1085,490))
f("amp","GLOBAL AMP","Overall amplitude of the LFOs","K",17,17,pos=(1148,490))
B=[];CB={}
BK=1.3149; BX,BY=450,394
def b(key,label,what,typ,sx,sy,hw=10,hh=10):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
for k,nm,x,y in (("f1","LFO 1 Frequency",551,443),("p1","LFO 1 Phase/Spin",551,469),("o1","LFO 1 Offset",551,498),("f2","LFO 2 Frequency",652,443),("p2","LFO 2 Phase/Spin",652,469),("o2","LFO 2 Offset",652,498),("mix","LFOs 1/2 Mix",753,470),("amp","LFOs 1+2 Amp",753,497)):
    kk={"mix":"mix","amp":"amp"}.get(k,k)
    kt={"mix":"mixt","amp":"ampt"}.get(k,k+"t"); kj={"mix":"mixj","amp":"ampj"}.get(k,k+"j")
    b(kt,nm+" CV trim","Amount for "+nm+" CV","K",x,y,13,13)
    b(kj,nm+" CV In","CV input: "+nm,"J",x+24,y)
for k,nm,x,y in (("c1La","LFO 1 Out Left A",951,443),("c1Ra","LFO 1 Out Right A",970,443),("c2La","LFO 2 Out Left A",951,471),("c2Ra","LFO 2 Out Right A",970,471),("cmLa","LFO 1/2 Mix Out Left A",951,498),("cmRa","LFO 1/2 Mix Out Right A",970,498),("c1Lb","LFO 1 Out Left B",1050,443),("c1Rb","LFO 1 Out Right B",1070,443),("c2Lb","LFO 2 Out Left B",1050,471),("c2Rb","LFO 2 Out Right B",1070,471),("cmLb","LFO 1/2 Mix Out Left B",1050,498),("cmRb","LFO 1/2 Mix Out Right B",1070,498)):
    b(k,nm,"CV output: "+nm,"J",x,y,9,9)
base=dict(device="Elements DS-LFO",prefix="DSLF",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="elements-ds-lfo",front_raw="_captures_batchE/dslfo_front_raw.jpg",back_raw="_captures_batchE/dslfo_back_raw.jpg",front=rows,back=B),open("tools/specs/elements-ds-lfo.json","w"))
json.dump(dict(device="Elements DS-LFO",front=chk,back=CB,views={},view_titles={}),open("tools/checks/elements-ds-lfo.json","w"),indent=0)
print(len(rows),len(B))
