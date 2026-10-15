import json
# kHs Chorus (kiloHearts RE). Front: screen=419+px/1.3063, 466+py/1.3063. Back: screen=453+px/1.3081, 466+py/1.3081.
NT="no tooltip in Reason (hovered 1.3 s)"
T=lambda s:'tooltip "%s"'%s
K=1.3063; OX,OY=419,466
rows=[]; chk={}; M="medium"
def f(label,what,typ,hw,hh,ck,pos,conf="high",why=""):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why]); chk[label]=ck
f("(triangle)","Fold/unfold device","B",8,8,"no tooltip (fold arrow); checked by eye",(441,481),M)
f("BYPASS / ON / OFF","3-way device switch","B",6,10,T("Enabled: On"),(467,483))
f("DELAY","Delay time","K",15,15,T("Delay: 4.0 ms"),(547,513))
f("DEPTH","Modulation depth","K",15,15,T("Depth: 4.0 ms"),(624,513))
f("RATE","Modulation rate","K",15,15,T("Rate: 0.60 Hz"),(699,513))
f("SPREAD","Stereo spread","K",15,15,T("Spread: 100%"),(776,513))
f("TAPS","Taps switch (3 / 2)","S",6,12,T("Taps: 2"),(870,513))
f("MIX","Dry/wet mix","K",15,15,T("Mix: 100%"),(1028,513))
f("CHORUS 1 tape","Device name tape","D",30,6,NT,(1120,500),M)
f("kHs logo","kiloHearts logo (no tooltip)","D",15,8,NT,(1150,522),M)
B=[];CB={}
BK=1.3081; BX,BY=453,466
def b(label,what,ck,sx,sy,hw=9,hh=9,typ="J"):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=ck
for nm,x in (("Delay",610),("Depth",662),("Rate",712),("Spread",763),("Mix",852)):
    b(nm+" CV In","CV input: "+nm.lower(),T(nm+" CV"),x,495)
    b(nm+" CV trim","Amount for "+nm.lower()+" CV",T(nm+" CV: 127"),x-1,520,12,12,"K")
b("Audio In L","Audio input, left",T("Connected to 3-Way Split: Main Audio Send L"),898,493)
b("Audio In R","Audio input, right",T("Connected to 3-Way Split: Main Audio Send R"),898,516)
b("Audio Out L","Audio output, left",T("Connected to RE 181 MSC 1: Audio In Left"),999,494)
b("Audio Out R","Audio output, right",T("Connected to RE 181 MSC 1: Audio In Right"),999,516)
b("(back vent)","Ventilation-grille drawing (no control)",NT,1070,500,30,25,"D")
b("CHORUS 1 tape (back)","Device name tape on the back",T("Chorus 1"),508,477,28,7,"D")
base=dict(device="kHs Chorus",prefix="KHSC",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="khs-chorus",front_raw="_captures_batchE/khs_front_raw.jpg",back_raw="_captures_batchE/khs_back_raw.jpg",front=rows,back=B),open("tools/specs/khs-chorus.json","w"))
json.dump(dict(device="kHs Chorus",front=chk,back=CB,views={},view_titles={}),open("tools/checks/khs-chorus.json","w"),indent=0)
print(len(rows),len(B))
