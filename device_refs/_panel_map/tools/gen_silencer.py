import json
# Efektor Silencer Noise Gate (Kuassa RE). Front: screen=419+px/1.3063, 466+py/1.3063. Back: screen=453+px/1.3081, 466+py/1.3081.
NT="no tooltip in Reason (hovered 1.3 s)"
T=lambda s:'tooltip "%s"'%s
K=1.3063; OX,OY=419,466
rows=[]; chk={}; M="medium"
def f(label,what,typ,hw,hh,ck,pos,conf="high",why=""):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why]); chk[label]=ck
f("(triangle)","Fold/unfold device","B",8,8,"no tooltip (fold arrow); checked by eye",(441,481),M)
f("BYPASS / ON / OFF","3-way device switch","B",6,10,T("Enabled: On"),(468,484))
f("THRESHOLD","Gate threshold","K",16,16,T("Threshold: -oo dB"),(532,497))
f("ATTACK","Gate attack time","K",16,16,T("Attack: 2 ms"),(601,497))
f("DECAY","Gate decay time","K",16,16,T("Decay: 100 ms"),(670,497))
f("DUAL MONO","Dual mono on/off","B",9,9,T("Dual Mono On/Off"),(1031,497))
f("Power button (red)","On / Bypass button (red power symbol)","B",9,9,T("On / Bypass"),(1167,482))
f("SILENCER 1 tape","Device name tape","D",30,6,NT,(1133,519),M)
f("EFEKTOR SILENCER logo","Logo (no tooltip)","D",100,20,NT,(785,507),M)
f("gate light grille","Small light grille next to the power button (no tooltip)","D",8,6,NT,(1169,497),M)
B=[];CB={}
BK=1.3081; BX,BY=453,466
def b(label,what,ck,sx,sy,hw=9,hh=9,typ="J"):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=ck
b("Input L","Audio input, left",T("Connected to Chorus 1: Main Out Left"),963,487)
b("Input R","Audio input, right",T("Connected to Chorus 1: Main Out Right"),988,487)
b("Output L","Audio output, left",T("Connected to RE 181 MSC 1: Audio In Left"),963,515)
b("Output R","Audio output, right",T("Connected to RE 181 MSC 1: Audio In Right"),988,515)
b("(small jacks 1)","Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip)",NT,1022,487,8,8)
b("(small jacks 2)","Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip)",NT,1042,487,8,8)
b("(small jacks 3)","Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip)",NT,1022,516,8,8)
b("(small jacks 4)","Small jacks near the INPUT/OUTPUT labels (not identified; no tooltip)",NT,1042,516,8,8)
b("SILENCER 1 tape (back)","Device name tape on the back",NT,780,482,28,7,"D")
b("Power area (drawn)","Power socket (no tooltip)",NT,1141,500,25,16,"D")
base=dict(device="Efektor Silencer Noise Gate",prefix="SILN",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="efektor-silencer",front_raw="_captures_batchE/silencer_front_raw.jpg",back_raw="_captures_batchE/silencer_back_raw.jpg",front=rows,back=B),open("tools/specs/efektor-silencer.json","w"))
json.dump(dict(device="Efektor Silencer Noise Gate",front=chk,back=CB,views={},view_titles={}),open("tools/checks/efektor-silencer.json","w"),indent=0)
print(len(rows),len(B))
