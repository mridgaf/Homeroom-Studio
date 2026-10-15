import json
# Elements Splitter 2 (AirRaid Audio RE, patch '3-Way Split'). Front: screen=419+px/1.3075, 392+py/1.3075. Back: screen=453+px/1.3081, 392+py/1.3081.
NT="no tooltip in Reason (hovered 1.2 s)"
T=lambda s:'tooltip "%s"'%s
K=1.3075; OX,OY=419,392
rows=[]; chk={}; M="medium"
def f(label,what,typ,hw,hh,ck,pos,conf="high",why=""):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why]); chk[label]=ck
f("(triangle)","Fold/unfold device","B",8,8,"no tooltip (fold arrow); checked by eye",(440,406),M)
f("BYPASS / ON / OFF","3-way device switch","B",6,10,T("Enabled: On"),(464,415))
f("Patch display","Patch name display","D",50,8,NT,(788,415),M)
f("(patch prev arrow)","Previous patch","B",7,5,T("Select previous patch"),(855,411))
f("(patch next arrow)","Next patch","B",7,5,T("Select next patch"),(855,420))
f("(patch folder)","Browse patch","B",8,8,T("Browse patch"),(875,415))
f("(patch disk)","Save patch","B",8,8,T("Save patch"),(895,415))
f("3-WAY SPLIT tape","Patch name tape (vertical)","D",8,30,T("3-Way Split")+" (seen on the back tape)",(437,462),M)
for band,xs,vals in (("LOW",(486,541,597),("Lo","Lo","Lo")),("MID",(763,819,875),("Mid","Mid","Mid")),("HIGH",(1042,1098,1154),("Hi","Hi","Hi"))):
    p=vals[0]
    f(band+" M/S","%s band mid/side balance"%band.lower(),"K",15,15,T(p+" Mid/Side: 100%"),(xs[0],490))
    f(band+" PAN","%s band pan"%band.lower(),"K",15,15,T(p+" Pan: 0.00"),(xs[1],490))
    f(band+" VOL","%s band volume"%band.lower(),"K",15,15,T(p+" Volume: 0.00 dB"),(xs[2],490))
f("LOW On","Low band on/off light-button","B",7,6,NT,(540,447),M,"no tooltip appeared (hovered at (540,448)); function by label")
f("LOW M","Low band mute","B",7,6,T("Lo Band Mute"),(562,447))
f("LOW S","Low band solo","B",7,6,T("Lo Band Solo"),(597,447))
f("MID M","Mid band mute","B",7,6,NT,(815,447),M,"no tooltip appeared; function by label and by LOW/HIGH")
f("MID S","Mid band solo","B",7,6,NT,(852,447),M,"no tooltip appeared; function by label and by LOW/HIGH")
f("HIGH On","High band on/off light-button","B",7,6,NT,(1095,447),M,"no tooltip appeared; function by label")
f("HIGH M","High band mute","B",7,6,T("Hi Band Mute"),(1117,447))
f("HIGH S","High band solo","B",7,6,T("Hi Band Solo"),(1152,447))
f("LO/MID 24dB","Lo/Mid crossover 24 dB slope enable","B",7,6,T("Lo X-Over 24 dB Enable"),(654,448))
f("LO/MID freq display","Lo/Mid crossover frequency display","D",25,8,T("Lo / Mid Display: 120.0 Hz"),(681,472))
f("LO/MID X-OVER","Lo/Mid crossover frequency","K",13,13,T("Lo / Mid Crossover: 17%"),(681,497))
f("MID/HI 24dB","Mid/Hi crossover 24 dB slope enable","B",7,6,T("Hi X-Over 24 dB Enable"),(933,448))
f("MID/HI freq display","Mid/Hi crossover frequency display","D",25,8,T("Mid / High Display: 2.00 kHz"),(960,472))
f("MID/HI X-OVER","Mid/Hi crossover frequency","K",13,13,T("Mid / Hi Crossover: 70%"),(960,497))
B=[];CB={}
BK=1.3081; BX,BY=453,392
def b(label,what,ck,sx,sy,hw=9,hh=9,typ="J"):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=ck
PAT="not hovered separately: same group as a hovered neighbour; tooltip pattern assumed"
b("Mid/Hi X-Over CV trim","Amount for mid/high crossover CV",T("Mid/Hi Band Crossover CV input: 127"),551,469,13,13,"K")
b("Mid/Hi X-Over CV In","CV input: mid/high crossover",PAT,575,469)
b("Lo/Mid X-Over CV trim","Amount for lo/mid crossover CV",PAT,551,498,13,13,"K")
b("Lo/Mid X-Over CV In","CV input: lo/mid crossover",T("Lo/Mid Band Crossover CV input"),575,498)
for band,tx,jx in (("Lo",652,676),("Mid",753,777),("Hi",853,877)):
    for nm,y,suf in (("M/S",443,"Mid/Side"),("Pan",470,"Pan"),("Vol",497,"Volume")):
        b("%s %s CV trim"%(band,nm),"Amount for %s band %s CV"%(band.lower(),nm),T("%s %s CV input: 127"%(band,suf)),tx,y,13,13,"K")
        b("%s %s CV In"%(band,nm),"CV input: %s band %s"%(band.lower(),nm),T("%s %s CV input"%(band,suf)),jx,y if nm!="Vol" else 497)
b("Sends -> X switch","Routing switch (X->Band / Band->X)",T("Routing (X->Band/Band->X)"),855,415,9,9,"B")
for band,y in (("Hi",414),("Mid",442),("Lo",470)):
    b("%s Send L"%band,"%s band audio send, left"%band,T("%s Band Audio Send L"%band),954,y)
    b("%s Send R"%band,"%s band audio send, right"%band,T("%s Band Audio Send R"%band),978,y)
    b("%s Return L"%band,"%s band audio return, left"%band,T("%s Band Audio Return L"%band),1054,y)
    b("%s Return R"%band,"%s band audio return, right"%band,T("%s Band Audio Return R"%band),1078,y)
b("Audio In L","Audio input, left",T("Connected to RPSpec 1: audio output main left"),954,498)
b("Audio In R","Audio input, right",T("Connected to RPSpec 1: audio output main right"),978,498)
b("Audio Out L","Audio output, left",T("Connected to RE 181 MSC 1: Audio In Left"),1054,498)
b("Audio Out R","Audio output, right",T("Connected to RE 181 MSC 1: Audio In Right"),1078,498)
b("3-WAY SPLIT tape (back)","Patch name tape on the back",T("3-Way Split"),468,462,8,28,"D")
b("(triangle, back)","Fold/unfold device",NT,441,405,8,8,"B")
base=dict(device="Elements Splitter",prefix="SPLT",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="elements-splitter",front_raw="_captures_batchE/splitter_front_raw.jpg",back_raw="_captures_batchE/splitter_back_raw.jpg",front=rows,back=B),open("tools/specs/elements-splitter.json","w"))
json.dump(dict(device="Elements Splitter",front=chk,back=CB,views={},view_titles={}),open("tools/checks/elements-splitter.json","w"),indent=0)
print(len(rows),len(B))
