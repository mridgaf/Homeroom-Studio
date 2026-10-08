import json
F=[];B=[];CF={};CB={}
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why="",name=None,slot=None):
    r=[label,what,typ,[x,y],[hw,hh],why]
    if name: r+=[ "high",name,slot]
    B.append(r); CB[label]=chk
# header
f("Bypass/On/Off","3-way device switch","Enabled",18,72,45,12,22,"B",T("Enabled: On"))
f("(triangle)","Fold/unfold device",None,None,40,23,8,8,"B",NT,"medium")
f("Patch display","Patch name display","Patch Name",None,1015,45,100,16,"D",T("Default Synchronous"),"medium","Remote item 'Patch Name'; tooltip shows the patch name")
f("(up arrow)","Load previous patch","Select Previous Patch",None,1210,35,12,9,"B",T("Select previous patch"))
f("(down arrow)","Load next patch","Select Next Patch",None,1210,53,12,9,"B",T("Select next patch"))
f("(folder)","Open patch browser",None,None,1245,45,14,14,"B",T("Browse patch"))
f("(disk)","Save patch",None,None,1280,45,14,14,"B",T("Save patch"))
f("INPUT meter","Input level light",None,None,1398,45,14,14,"D",NT)
f("DEFAULT SYN tape","Patch name tape","Device Name",None,100,645,12,50,"D",T("Default Synchronous")+" (patch name; 'Device Name' item not provable here)","medium","Remote item 'Device Name'; convention from earlier devices")
# display
for i,x in enumerate([221,291,361,433,504,574,645,716,787]):
    f(f"TOOL {i+1}",f"Wave shape tool {i+1} (draws the shape on the selected track)",None,None,x,123,32,16,"B",NT)
f("FREE","Free-run mode (no tempo sync)",None,None,873,122,32,16,"B",NT)
for i,(lab,x) in enumerate(zip(["1/64","1/32","1/16T","1/16","1/8T","1/8","1/4","1/2","1/1"],[218,290,361,433,504,574,645,716,787])):
    f(f"RATE {lab}",f"Wave rate {lab}",None,None,x,165,32,16,"B",NT)
for lab,x in (("2",944),("1",985),("0.5",1027)):
    f(f"SPEED x{lab}",f"Speed multiplier x{lab}",None,None,x,166,18,14,"B",NT)
f("MASTER OFFSET","Master offset knob",None,None,1180,126,12,12,"K",NT,"medium")
f("MASTER OFFSET value","Master offset readout",None,None,1230,126,14,12,"D",NT)
f("PHASE","Phase knob",None,None,1180,168,12,12,"K",NT,"medium")
f("DIM","Dim knob",None,None,1313,168,12,12,"K",NT,"medium")
for i,(y,col) in enumerate(((237,"yellow"),(303,"magenta"),(370,"blue"))):
    f(f"TRACK {i+1}",f"Select track {i+1} ({col})",None,None,150,y,28,30,"B",NT)
for i,y in enumerate((217,287,356)):
    f(f"TRACK {i+1} FRZ",f"Freeze track {i+1}",None,None,1330,y,28,12,"B",NT)
    f(f"TRACK {i+1} KILL",f"Kill track {i+1}",None,None,1330,y+31,28,12,"B",NT)
f("Wave display","Curve drawing/preview area for the 3 tracks",None,None,740,300,560,100,"D",NT,"medium","display only")
f("MOD CTRL","Show/hide the modulation controls row",None,None,118,440,30,10,"B",NT,"medium")
for i,x in enumerate([233,346,459,570,683,794,907,1019,1132,1244]):
    f(f"MOD {i+1}",f"Modulation amount knob {i+1} (above the main knob {i+1})",None,None,x,440,14,14,"K",NT,"medium")
# knob row
for lab,what,name,slot,x,tip in [("Dist Amount","Distortion amount","Dist Amount",12,237,"Dist Amount: 50%"),("Dist Character","Distortion character","Dist Character",13,348,"Dist Character: 50%"),
 ("Filter Freq","Filter frequency","Filter Freq",19,459,"Filter Freq: 75%"),("Filter Resonance","Filter resonance","Filter Reso",22,571,"Filter Reso: 0%"),
 ("Delay Amount","Delay amount","Delay  Amount",1,684,"Delay Amount: 50%"),("Delay Time","Delay time (note value when Sync is on)","Delay Synched Time",9,795,"Delay Synced Time: 3/16"),
 ("Delay Feedback","Delay feedback","Delay Feedback",2,908,"Delay Feedback: 50%"),("Reverb Amount","Reverb amount","Reverb Amount",27,1020,"Reverb Amount: 50%"),
 ("Reverb Decay","Reverb decay","Reverb Decay",29,1132,"Reverb Decay: 50%"),("Level","Level (In/Out switch below)","Level",24,1245,"Level: 0.0 dB")]:
    f(lab,what,name,slot,x,490,32,32,"K",T(tip))
f("Delay Time (ms)","Delay time in ms (same knob as Delay Time; shows when Sync is off)","Delay Time",11,795,520,30,10,"D","not hovered: same knob as Delay Time; its Remote name 'Delay Time' (ms) NOT proven by tooltip (tooltip read 'Delay Synced Time' because Sync is on)","low","same spot as the Delay Time knob; NOT proven")
f("Dist type","Distortion type slider (Dist 1 / Dist 2 / Lo-Fi / Ring Mod)","Dist Type",16,205,605,12,34,"S",T("Dist Type: Dist 1"))
f("Post Filter","Put the filter after the distortion","Dist Post Filter",15,333,588,14,14,"B",T("Dist Post Filter"))
f("Filter type","Filter type slider (HP / BP / LP / Comb)","Filter Type",23,430,605,12,34,"S",T("Filter Type: LP"))
f("Lag","Filter lag knob","Filter Lag",20,570,592,20,20,"K",T("Filter Lag: 0%"))
f("Keep Pitch","Keep pitch when delay time changes","Delay Keep Pitch",3,669,588,14,14,"B",T("Delay Keep Pitch"))
f("Sync","Delay tempo sync","Delay Tempo Sync",10,795,588,14,14,"B",T("Delay Tempo Sync"))
f("Ping Pong","Ping-pong delay","Delay Ping Pong",6,669,625,14,14,"B",T("Delay Ping Pong"))
f("Roll","Delay roll (hold feedback)","Delay Roll",7,907,588,14,14,"B",T("Delay Roll"))
f("Delay Send/Return","Delay as send or return effect","Delay SendReturn",8,794,665,24,12,"B",T("Delay Send/Return: Send"))
f("Pan","Delay pan","Delay Pan",5,907,650,20,20,"K",T("Delay Pan: 50%"))
f("Reverb Size","Reverb size","Reverb Size",32,1020,592,20,20,"K",T("Reverb Size: 50%"))
f("Reverb Damp","Reverb damping","Reverb Damp",28,1130,592,20,20,"K",T("Reverb Damp: 20%"))
f("Reverb Send/Return","Reverb as send or return effect","Reverb SendReturn",31,1075,665,24,12,"B",T("Reverb Send/Return: Return"))
f("Level In/Out","Level knob works on In or Out","Level InOut",25,1245,665,24,12,"B",T("Level In/Out: Out"))
f("Dry/Wet","Dry/wet balance","DryWet",17,1375,592,20,20,"K",T("Dry/Wet: 100%"))
f("Master Level","Master output level","Master Level",26,1375,698,28,28,"K",T("Master Level: 0.0 dB"))
f("DIST","Distortion section on/off","Dist On",14,290,748,60,26,"B",T("Dist On"))
f("FILTER","Filter section on/off","Filter On",21,516,748,60,26,"B",T("Filter On"))
f("DELAY","Delay section on/off","Delay On",4,795,748,60,26,"B",T("Delay On"))
f("REVERB","Reverb section on/off","Reverb On",30,1075,748,60,26,"B",T("Reverb On"))
# back
for r,y in ((1,452),(2,501),(3,551)):
    b(f"Curve {r} CV trim","Amount for Curve %d CV"%r,"K",303,y,20,20,T(f"Curve {r} CV Amount: 100%"),"trim next to CV jack; Remote has no item for it")
    b(f"Curve {r} CV In","CV input: curve %d"%r,"J",345,y,18,18,T(f"Curve {r} CV In"))
    b(f"Freeze {r} CV In","CV input: freeze track %d"%r,"J",498,y,18,18,T(f"Freeze {r} CV In"))
    b(f"Curve {r} CV Out","CV output: curve %d"%r,"J",672,y,18,18,T(f"Curve {r} CV Out"))
    b(f"Curve {r} Inverted CV Out","CV output: inverted curve %d"%r,"J",848,y,18,18,T(f"Curve {r} Inv CV Out"))
b("Master Level CV trim","Amount for Master Level CV","K",458,600,20,20,T("Master Level CV Amount: 100%"),"trim next to CV jack; Remote has no item for it")
b("Master Level CV In","CV input: master level","J",500,600,18,18,T("Master Level CV In"))
b("Audio In L","Audio input left","J",984,494,20,20,T("Connected to Basic Phasing: Left Output")+"; this jack's own name NOT read yet")
b("Audio In R","Audio input right","J",1041,494,20,20,T("Connected to Basic Phasing: Right Output")+"; this jack's own name NOT read yet")
b("Audio Out L","Audio output left","J",1134,494,20,20,'cabled: tooltip "Connected to Mix Channel: From Insert FX..." (cut off); own jack name NOT read yet')
b("Audio Out R","Audio output right","J",1191,494,20,20,'cabled: tooltip "Connected to Mix Channel: From Insert FX..." (cut off); own jack name NOT read yet')
for i,y in enumerate((432,467,503,538,573)): b(f"(routing icon {i+1})","Routing icon","D",115,y,14,18,NT)
b("DEFAULT SYN tape (back)","Patch name tape (back)","D",997,143,66,12,T("Default Synchronous"))
b("(triangle) back","Fold/unfold device","D",45,143,8,8,NT)
base=dict(device="Synchronous",prefix="SYNC",remote_scope="se.propellerheads.Synchronous",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="synchronous",front_raw="_captures_batchD/synchronous_front_raw.jpg",back_raw="_captures_batchD/synchronous_back_raw.jpg",front=F,back=B),open("tools/specs/synchronous.json","w"))
json.dump(dict(device="Synchronous",front=CF,back=CB),open("tools/checks/synchronous.json","w"),indent=0)
print(len(F),len(B))
