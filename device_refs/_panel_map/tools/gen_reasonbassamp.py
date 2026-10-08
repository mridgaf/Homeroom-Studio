import json
F=[];B=[];CF={};CB={}
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why=""):
    B.append([label,what,typ,[x,y],[hw,hh],why]); CB[label]=chk
f("(triangle)","Fold/unfold device",None,None,52,38,8,8,"B",NT,"medium")
f("Bypass/On/Off","3-way device switch","Enabled",5,92,45,12,22,"B",T("Enabled: On"))
f("(speaker slots)","Decoration (vent slots)",None,None,222,70,80,45,"D",NT)
for i,(n,x) in enumerate((("MODERN",455),("VINTAGE",497),("BYPASS",538))):
    f(f"AMP {n}",f"Amp model: {n.title()}","Amp Switch",1 if i==0 else None,x,65,18,18,"B",T("Amp Switch"),"high" if i==0 else "medium","all 3 lights show tooltip 'Amp Switch'; Remote item is stepped Modern..Bypass" if i else "")
f("Patch display","Patch name display","Patch Name",None,722,67,100,16,"D",T("Smooth Bass"),"medium","Remote item 'Patch Name'; tooltip shows the patch name")
f("(up arrow)","Load previous patch","Select Previous Patch",None,858,57,14,9,"B",T("Select previous patch"))
f("(down arrow)","Load next patch","Select Next Patch",None,858,76,14,9,"B",T("Select previous patch")+" (second hover also read 'Select previous patch'; the down arrow's own text was not told apart; Remote item 'Select Next Patch' is by position)","medium","tooltip read 'Select previous patch' on both arrows in this pass; NOT told apart")
f("(folder)","Open patch browser",None,None,897,67,14,14,"B",T("Browse patch"))
f("(disk)","Save patch",None,None,937,67,14,14,"B",T("Save patch"))
for i,(n,x) in enumerate((("DARK",995),("BRIGHT",1036),("ROOM",1077),("BYPASS",1118))):
    f(f"CAB {n}",f"Cabinet: {n.title()}","Cab Switch",3 if i==0 else None,x,65,18,18,"B",T("Cab Switch"),"high" if i==0 else "medium","all 4 lights show tooltip 'Cab Switch'; Remote item is stepped Dark..Bypass" if i else "")
f("Softube logo","Logo (decoration)",None,None,1385,63,60,16,"D",NT)
f("SMOOTH BASS tape","Patch name tape","Device Name",None,47,235,14,60,"D",T("Smooth Bass")+" (patch name; 'Device Name' item not provable here)","medium","Remote item 'Device Name'; convention from earlier devices")
f("Drive","Drive","Drive",4,222,280,42,42,"K",T("Drive: 7.0"))
f("Bass","Bass","Bass",2,413,280,42,42,"K",T("Bass: 5.5"))
f("Middle","Middle","Middle",7,571,280,42,42,"K",T("Middle: 2.5"))
f("Mid Freq","Mid frequency (1 to 5)","Mid Freq",6,710,285,28,28,"K",T("Mid Freq: 1")+" (read as 'Mid Freq: 1')")
f("Treble","Treble","Treble",8,872,280,42,42,"K",T("Treble: 5.0"))
f("ULTRA LO","Ultra Lo switch","Ultra Lo",10,352,363,18,18,"B",T("Ultra Lo"))
f("ULTRA HI","Ultra Hi switch","Ultra Hi",9,817,363,18,18,"B",T("Ultra Hi"))
f("Level lights","Output level lights",None,None,1438,270,10,38,"D",NT)
f("Volume","Output volume","Volume",11,1325,280,42,42,"K",T("Volume: -8.2 dB"))
f("VOLUME label","Label bar under Volume (decoration)",None,None,1325,367,90,10,"D",NT)
b("(triangle) back","Fold/unfold device","D",50,37,8,8,NT)
b("SMOOTH BASS tape (back)","Patch name tape (back)","D",1155,27,66,12,T("Smooth Bass"))
b("(routing icon 1)","Routing icon","D",108,215,14,18,NT)
b("(routing icon 2)","Routing icon","D",108,260,14,18,NT)
b("Drive CV In","CV input: drive","J",207,180,18,18,T("Drive CV"))
b("Drive CV trim","Amount for Drive CV","K",270,180,20,20,T("Drive CV: 127"),"trim next to CV jack; Remote has no item for it")
b("Volume CV In","CV input: volume","J",380,180,18,18,T("Volume CV"))
b("Volume CV trim","Amount for Volume CV","K",445,180,20,20,T("Volume CV: 127"),"trim next to CV jack; Remote has no item for it")
b("Input L","Audio input left","J",210,283,20,20,T("Connected to British Drive 3: Main Out Le(ft)")+" (cut off); this jack's own name NOT read yet")
b("Input R","Audio input right","J",298,283,20,20,T("Connected to British Drive 3: Main Out Rig(ht)")+" (cut off); own jack name NOT read yet")
b("Output L","Audio output left","J",381,283,20,20,T("Connected to Basic Phasing: Left Input")+"; this jack's own name NOT read yet")
b("Output R","Audio output right","J",468,283,20,20,T("Connected to Basic Phasing: Right Input")+"; own jack name NOT read yet")
b("Fuse 1","Fuse cap (decoration)","D",868,135,30,30,NT)
b("Fuse 2","Fuse cap (decoration)","D",966,135,30,30,NT)
b("Vent grille","Decoration (vent)","D",1270,215,160,150,NT)
b("Warning label","Sticker (decoration)","D",855,285,130,85,NT)
base=dict(device="ReasonBassAmp",prefix="RBAS",remote_scope="se.propellerheads.ReasonBassAmp",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="reasonbassamp",front_raw="_captures_batchD/softube-bass-amp_front_raw.jpg",back_raw="_captures_batchD/softube-bass-amp_back_raw.jpg",front=F,back=B),open("tools/specs/reasonbassamp.json","w"))
json.dump(dict(device="ReasonBassAmp",front=CF,back=CB),open("tools/checks/reasonbassamp.json","w"),indent=0)
print(len(F),len(B))
