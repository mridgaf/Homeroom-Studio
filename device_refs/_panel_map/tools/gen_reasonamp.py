import json
F=[];B=[];CF={};CB={}
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why=""):
    B.append([label,what,typ,[x,y],[hw,hh],why]); CB[label]=chk
f("(triangle)","Fold/unfold device",None,None,50,37,8,8,"B",NT,"medium")
f("Bypass/On/Off","3-way device switch","Enabled",5,92,45,12,22,"B",T("Enabled: On"))
f("BRITISH DRIVE tape","Patch name tape","Device Name",None,87,180,14,50,"D",T("British Drive 3")+" (patch name; 'Device Name' item not provable here)","medium","Remote item 'Device Name'; convention from earlier devices")
for i,(n,x) in enumerate((("TWANG",405),("CRUNCH",447),("ROCK",488),("LEAD",529),("BYPASS",570))):
    f(f"AMP {n}",f"Amp model: {n.title()}","Amp Switch",1 if i==0 else None,x,45,18,18,"B",T("Amp Switch"),"high" if i==0 else "medium","all 5 lights show tooltip 'Amp Switch'; Remote item is stepped Twang..Bypass" if i else "")
f("Patch display","Patch name display","Patch Name",None,722,47,100,16,"D",T("British Drive 3"),"medium","Remote item 'Patch Name'; tooltip shows the patch name")
f("(up arrow)","Load previous patch","Select Previous Patch",None,860,35,14,9,"B",T("Select previous patch"))
f("(down arrow)","Load next patch","Select Next Patch",None,860,57,14,9,"B",T("Select next patch"))
f("(folder)","Open patch browser",None,None,897,47,14,14,"B",T("Browse patch"))
f("(disk)","Save patch",None,None,937,47,14,14,"B",T("Save patch"))
for i,(n,x) in enumerate((("BRIGHT",997),("ROOM",1038),("FAT",1079),("TIGHT",1120),("BYPASS",1161))):
    f(f"CAB {n}",f"Cabinet: {n.title()}","Cab Switch",4 if i==0 else None,x,45,18,18,"B",T("Cab Switch"),"high" if i==0 else "medium","all 5 lights show tooltip 'Cab Switch'; Remote item is stepped Bright..Bypass" if i else "")
f("Softube logo","Logo (decoration)",None,None,1512,48,50,14,"D",NT)
f("AMP logo","Logo (decoration)",None,None,775,145,110,55,"D",NT)
f("Red lamp","Red power lamp",None,None,313,330,36,36,"D",NT)
f("Boost switch","Boost on/off toggle","Boost",3,428,305,16,26,"B",T("Boost: Normal"))
f("Gate","Noise gate threshold","Gate",7,430,367,28,28,"K",T("Gate: 0.1"))
f("Gain","Amp gain","Gain",6,567,327,32,32,"K",T("Gain: 10.0"))
f("Bass","Bass","Bass",2,697,325,32,32,"K",T("Bass: 4.7"))
f("Mid","Mid","Mid",8,815,325,32,32,"K",T("Mid: 8.4"))
f("Treble","Treble","Treble",10,930,325,32,32,"K",T("Treble: 6.9"))
f("Poweramp Gain","Poweramp gain","Poweramp Gain",9,1055,325,32,32,"K",T("Poweramp Gain: 5.0"))
f("Level lights","Output level lights",None,None,1175,325,12,32,"D",NT)
f("Volume","Output volume","Volume",11,1255,325,34,34,"K",T("Volume: -3.0 dB"))
# back
b("(triangle) back","Fold/unfold device","D",50,37,8,8,NT)
b("BRITISH DRIVE tape (back)","Patch name tape (back)","D",1155,37,66,12,T("British Drive 3"))
b("(routing icon 1)","Routing icon","D",155,298,14,18,NT)
b("(routing icon 2)","Routing icon","D",187,298,14,18,NT)
b("Warning sticker","Sticker (decoration)","D",397,300,120,75,NT)
b("Input L","Audio input left","J",545,285,20,20,T("Connected to Big BBD Ensemble: Left Output")+" (cut off at edge); this jack's own name NOT read yet")
b("Input R","Audio input right","J",615,285,20,20,T("Connected to Big BBD Ensemble: Right Output")+" (cut off at edge); own jack name NOT read yet")
b("Output L","Audio output left","J",697,285,20,20,T("Connected to Smooth Bass: Main In Left")+"; this jack's own name NOT read yet")
b("Output R","Audio output right","J",763,285,20,20,T("Connected to Smooth Bass: Main In Right")+"; own jack name NOT read yet")
b("Gate CV In","CV input: gate","J",853,268,18,18,T("Gate CV"))
b("Gate CV trim","Amount for Gate CV","K",855,318,20,20,T("Gate CV: 127"),"trim under its CV jack; Remote has no item for it")
b("Gain CV In","CV input: gain","J",963,268,18,18,T("Gain CV"))
b("Gain CV trim","Amount for Gain CV","K",965,318,20,20,T("Gain CV: 127"),"trim under its CV jack; Remote has no item for it")
b("Volume CV In","CV input: volume","J",1066,268,18,18,T("Volume CV"))
b("Volume CV trim","Amount for Volume CV","K",1068,318,20,20,T("Volume CV: 127"),"trim under its CV jack; Remote has no item for it")
b("Ground screw (J)","Ground terminal (decoration)","D",1162,285,12,22,NT)
b("Fuse 1","Fuse cap (decoration)","D",1247,312,28,28,NT)
b("Fuse 2","Fuse cap (decoration)","D",1340,312,28,28,NT)
base=dict(device="ReasonAmp",prefix="RAMP",remote_scope="se.propellerheads.ReasonAmp",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="reasonamp",front_raw="_captures_batchD/softube-amp_front_raw.jpg",back_raw="_captures_batchD/softube-amp_back_raw.jpg",front=F,back=B),open("tools/specs/reasonamp.json","w"))
json.dump(dict(device="ReasonAmp",front=CF,back=CB),open("tools/checks/reasonamp.json","w"),indent=0)
print(len(F),len(B))
