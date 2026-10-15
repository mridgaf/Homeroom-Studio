import json
# NN-XT. Front main panel only (Remote Editor below it is folded and NOT mapped). Front: screen = 420+px/1.3038, 392+py/1.3038. Back: screen = 420+px/1.3145, 395+py/1.3145.
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/nnxt_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
K=1.3038; OX,OY=420,392
rows=[]; chk={}
M="medium"
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None):
    sx,sy=pos
    rows.append([label,what,name,slot,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(442,408))
f("pitchwheel","PITCH wheel","Pitch bend wheel","S",8,28,"Pitch Bend",16,why="tooltip 'Pitch Bend'",pos=(470,448))
f("modwheel","WHEEL (mod wheel)","Modulation wheel","S",8,28,"Mod Wheel",13,why="tooltip 'Mod Wheel'",pos=(498,448))
f("xwheel","EXTERNAL CONTROL wheel","External controller wheel","S",8,28,"External Controller",4,why="tooltip 'External Controller'",pos=(525,448))
f("led_at","SOURCE AFTERTOUCH light","External control source: aftertouch","B",5,5,conf=M,pos=(549,427))
f("led_ex","SOURCE EXPRESSION light","External control source: expression","B",5,5,conf=M,pos=(549,438))
f("led_br","SOURCE BREATH light","External control source: breath","B",5,5,conf=M,pos=(549,449))
f("source","SOURCE button","Choose the external controller source","B",11,8,"External Controller Source",5,pos=(554,463))
f("noteon","NOTE ON light","Note-on indicator","D",6,6,"Note On Indicator",conf=M,why="Remote item Note On Indicator, no knob slot",pos=(631,480))
f("patchprev","(patch prev arrow)","Previous patch","B",7,5,"Select Previous Patch",pos=(635,413))
f("patchnext","(patch next arrow)","Next patch","B",7,5,"Select Next Patch",pos=(635,423))
f("folder","(patch folder)","Browse patch","B",8,8,pos=(655,417))
f("disk","(patch disk)","Save patch","B",8,8,pos=(675,417))
f("patchdisp","Patch display","Patch name display","D",50,10,"Patch Name",conf=M,why="Remote item Patch Name, no knob slot",pos=(749,417))
f("hq","HIGH QUALITY INTERPOLATION","High quality interpolation on/off","B",10,8,"High Quality Interpolation",9,pos=(725,483))
f("tape","Patch name tape","Patch name tape","D",40,9,"Device Name",conf=M,why="Remote item 'Device Name'; tooltip shows the patch name; convention from earlier devices",pos=(1058,407))
f("freq","FILTER FREQ","Filter frequency","K",17,17,"Filter Freq",7,pos=(872,443))
f("res","FILTER RES","Filter resonance","K",17,17,"Filter Res",8,pos=(911,443))
f("attack","AMP ENVELOPE ATTACK","Amp envelope attack","K",17,17,"Amp Env Attack",1,pos=(958,443))
f("decay","AMP ENVELOPE DECAY","Amp envelope decay","K",17,17,"Amp Env Decay",2,pos=(996,443))
f("release","AMP ENVELOPE RELEASE","Amp envelope release","K",17,17,"Amp Env Release",3,pos=(1036,443))
f("mdecay","MOD ENV DECAY","Mod envelope decay","K",17,17,"Mod Env Decay",12,pos=(1083,443))
f("ir","IR display","Small red display above MASTER VOLUME (purpose not verified)","D",12,8,conf="low",pos=(1157,422))
f("master","MASTER VOLUME","Master volume","K",17,17,"Master Volume",10,pos=(1156,449))
PARK="Remote vocabulary lists this name a second time (different capitalisation / item); no separate panel control; row parked beside the matching control; NOT proven"
def park(label,what,name,slot,pos,ck="not hovered: duplicate/parked Remote item with no separate panel control"):
    rows.append([label,what,name,slot,[round((pos[0]-OX)*K),round((pos[1]-OY)*K)],[round(5*K),round(5*K)],"B","low",PARK]); chk[label]=ck
park("(parked) External controller","Remote item 'External controller' (lowercase variant of slot 4)","External controller",6,(525,478))
park("(parked) Master volume","Remote item 'Master volume' (lowercase variant of slot 10)","Master volume",11,(1135,478))
park("(parked) Mod env Decay","Remote item 'Mod env Decay' (variant of slot 12)","Mod env Decay",14,(1083,478))
park("(parked) Mod wheel","Remote item 'Mod wheel' (lowercase variant of slot 13)","Mod wheel",15,(498,478))
park("(no panel control) Sample","Remote item 'Sample': no matching control on the NN-XT main panel (belongs to the Remote Editor, not mapped)","Sample",17,(800,478))
B=[];CB={}
BK=1.3145; BX,BY=420,395
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=c(key,back)
b("gate","Mono Gate In","Gate input (sequencer control)","J",483,443)
b("cv","Mono CV In","CV input (sequencer control)","J",483,465)
for k,nm,y in (("oscp","OSC Pitch",421),("fcut","Filter Cutoff",442),("fres","Filter Res",463),("lfo","LFO 1 Rate",484)):
    b(k+"_trim",nm+" mod trim","Amount for "+nm+" modulation","K",565,y,13,13)
    b(k+"_jack",nm+" mod In","Modulation input: "+nm,"J",589,y)
for k,nm,y in (("mvol","Master Volume",421),("pan","Pan",442),("mw","Mod Wheel",463),("pw","Pitch Wheel",484)):
    b(k+"_trim",nm+" mod trim","Amount for "+nm+" modulation","K",677,y,13,13)
    b(k+"_jack",nm+" mod In","Modulation input: "+nm,"J",701,y)
b("gateAmp","Amp Env Gate In","Gate input: amp envelope","J",797,443)
b("gateMod","Mod Env Gate In","Gate input: mod envelope","J",797,464)
XS=(886,914,945,974,1007,1035,1068,1095)
for i in range(16):
    b("out%d"%(i+1),"Audio Out %d"%(i+1),"Audio output %d"%(i+1)+(" (left)" if i==0 else " (right)" if i==1 else ""),"J",XS[i%8],438 if i<8 else 475,13,13)
b("power","Power switch (drawn)","Rocker switch drawn on the back panel (no tooltip)","B",1150,425,12,12)
base=dict(device="NN-XT Advanced Sampler",prefix="NNXT",remote_scope="Propellerheads / NN-XT Advanced Sampler",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="nn-xt",front_raw="_captures_batchE/nnxt_front_raw.jpg",back_raw="_captures_batchE/nnxt_back_raw.jpg",front=rows,back=B),open("tools/specs/nn-xt.json","w"))
json.dump(dict(device="NN-XT Advanced Sampler",front=chk,back=CB,views={},view_titles={}),open("tools/checks/nn-xt.json","w"),indent=0)
print(len(rows),len(B))
