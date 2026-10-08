import json
F=[];B=[];CF={};CB={}
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why=""):
    B.append([label,what,typ,[x,y],[hw,hh],why]); CB[label]=chk
NOSLOT="Remote item exists in Reason but is beyond the 48 knob slots of our remotemap (not mapped)"
f("(triangle)","Fold/unfold device",None,None,40,35,8,8,"B",NT,"medium")
f("Bypass/On/Off","3-way device switch","Enabled",48,92,35,12,22,"B",T("Enabled: On"))
f("(meter lights)","Level lights",None,None,183,38,12,16,"D",T("Master")+" (tooltip text; no Remote item assigned)","medium","tooltip 'Master'; Remote has an 'Input Peak Meter' item but the match is NOT proven")
f("Patch display","Patch name display","Patch Name",None,748,38,160,16,"D",T("Pad Rhythmification"),"medium","Remote item 'Patch Name'; tooltip shows the patch name")
f("(up arrow)","Load previous patch","Select Previous Patch",None,1042,28,14,9,"B",T("Select previous patch"))
f("(down arrow)","Load next patch","Select Next Patch",None,1042,46,14,9,"B",T("Select next patch"))
f("(folder)","Open patch browser",None,None,1081,36,14,14,"B",T("Browse patch"))
f("(disk)","Save patch",None,None,1118,36,14,14,"B",T("Save patch"))
f("PAD RHYTHMIF tape","Patch name tape","Device Name",None,47,275,14,60,"D",T("Pad Rhythmification")+" (patch name; 'Device Name' item not provable here)","medium","Remote item 'Device Name'; convention from earlier devices")
f("Pattern ON","Pattern on/off button","Pattern Enable",41,140,127,22,20,"B",T("Pattern Enable"))
f("Pattern light","Pattern on light",None,None,183,127,10,10,"D",T("Pattern Enable"))
f("SHUFFLE","Pattern shuffle","Shuffle",44,131,172,22,20,"B",T("Shuffle"))
f("Pattern display","Pattern number (stepper)","Pattern",40,158,221,40,20,"D",T("Pattern: 1"))
f("Pattern up arrow","Next pattern",None,None,211,212,10,9,"B",NT)
f("Pattern down arrow","Previous pattern",None,None,211,232,10,9,"B",NT)
f("RESOLUTION","Pattern resolution","Resolution",42,172,312,30,30,"K",T("Resolution: 1/16"))
f("SHIFT","Pattern shift","Shift",43,172,408,30,30,"K",T("Shift: 0"))
for i,(y,yl) in enumerate(((137,140),(217,220),(298,298)),1):
    f(f"MANUAL GATE {i}",f"Manual gate {i} button","Gate %d Trig"%i,24+2*i,347,y,20,20,"B",T(f"Gate {i} Trig"))
    f(f"Gate {i} light",f"Gate {i} open light","Gate %d Open"%i,23+2*i,410,yl,10,10,"D",NT+"; Remote item 'Gate %d Open' is a 'flat' item; placed on this light, NOT proven"%i,"low","Remote item 'Gate %d Open'; likely this light; NOT proven"%i)
bands=(("HIGH PASS","High Pass",142,17,130),("BAND PASS","Band Pass",222,9,212),("LOW PASS","Low Pass",302,1,291))
tips={"HIGH PASS":("High Pass Filter On","High Pass LFO Amount: 22%","High Pass Frequency: 1.74 kHz","High Pass Resonance: 31%","High Pass Env Amount: -25%"),
"BAND PASS":("Band Pass Filter On","Band Pass LFO Amount: 22%","Band Pass Frequency: 376.3 Hz","Band Pass Resonance: 60%","Band Pass Env Amount: 19%"),
"LOW PASS":("Low Pass Filter On","Low Pass LFO Amount: 22%","Low Pass Frequency: 1.96 kHz","Low Pass Resonance: 16%","Low Pass Env Amount: 16%")}
for lab,pre,y,s0,yon in bands:
    t=tips[lab]
    f(f"{lab} ON",f"{pre} filter on/off",f"{pre} Filter On",s0,515,yon,24,14,"B",T(t[0]))
    f(f"{lab} LFO",f"{pre} filter: LFO amount",f"{pre} LFO Amount",s0+4,651,y,26,26,"K",T(t[1]))
    f(f"{lab} FREQ",f"{pre} filter frequency",f"{pre} Frequency",s0+1,729,y,26,26,"K",T(t[2]))
    f(f"{lab} RES",f"{pre} filter resonance",f"{pre} Resonance",s0+2,806,y,26,26,"K",T(t[3]))
    f(f"{lab} ENV",f"{pre} filter: envelope amount",f"{pre} Env Amount",s0+3,883,y,26,26,"K",T(t[4]))
mix={"High Pass":(140,22,23,24,("17%","0%","9%","-27","75%")),"Band Pass":(220,14,15,16,("31%","0%","35%","2","70%")),"Low Pass":(300,6,7,8,("39%","0%","9%","27","75%"))}
for pre,(y,sd,sp,sv,tv) in mix.items():
    f(f"{pre} DRIVE",f"{pre} band: drive amount",f"{pre} Drive Amount",sd,1040,y,26,26,"K",T(f"{pre} Drive Amount: {tv[0]}"))
    f(f"{pre} PHASER",f"{pre} band: phaser amount",f"{pre} Phaser Amount",None,1117,y,26,26,"K",T(f"{pre} Phaser Amount: {tv[1]}"),"high",NOSLOT)
    f(f"{pre} DELAY",f"{pre} band: delay amount",f"{pre} Delay Amount",None,1194,y,26,26,"K",T(f"{pre} Delay Amount: {tv[2]}"),"high",NOSLOT)
    f(f"{pre} PAN",f"{pre} band: pan",f"{pre} Pan",sp,1277,y,26,26,"K",T(f"{pre} Pan: {tv[3]}"))
    f(f"{pre} VOLUME",f"{pre} band: volume",f"{pre} Volume",sv,1358,y,26,26,"K",T(f"{pre} Volume: {tv[4]}"))
f("DUCKING","Ducking amount","Ducking",47,1198,398,26,26,"K",T("Ducking: 0%"))
f("DRY PAN","Dry signal pan","Dry Pan",None,1277,398,26,26,"K",T("Dry Pan: 2"),"high",NOSLOT)
f("DRY VOLUME","Dry signal volume","Dry Volume",45,1358,398,26,26,"K",T("Dry Volume: 0%"))
f("MASTER","Master volume","Master Volume",46,1448,222,36,36,"K",T("Master Volume: 72%"))
for lab,n,x,s,tip in (("AMP ENV A","Amp Env Attack",140,31,"Amp Env Attack: 16%"),("AMP ENV D","Amp Env Decay",212,32,"Amp Env Decay: 61%"),("AMP ENV R","Amp Env Release",284,33,"Amp Env Release: 29%")):
    f(lab,"Amplitude envelope "+n.split()[-1].lower(),n,s,x,520,24,24,"K",T(tip))
f("LFO waveform display","LFO waveform (pick with the arrows)","LFO Waveform",38,418,520,36,22,"D",T("LFO Waveform: Triangle"))
f("LFO wave up arrow","Previous waveform",None,None,473,512,10,9,"B",NT)
f("LFO wave down arrow","Next waveform",None,None,473,533,10,9,"B",NT)
f("LFO FREQ","LFO frequency (note value when SYNC is on)","LFO Freq",37,541,520,26,26,"K",T("LFO Freq: 3/8"))
f("LFO SYNC","LFO tempo sync","LFOSync",39,607,500,14,14,"B",T("LFO Sync")+" (Remote name is 'LFOSync')")
for lab,n,x,s,tip in (("FILTER ENV A","Filter Env Attack",721,34,"Filter Env Attack: 9%"),("FILTER ENV D","Filter Env Decay",790,35,"Filter Env Decay: 39%"),("FILTER ENV R","Filter Env Release",862,36,"Filter Env Release: 27%")):
    f(lab,"Filter envelope "+n.split()[-1].lower(),n,s,x,520,24,24,"K",T(tip))
f("DELAY TIME","Delay time (note value when SYNC is on)","Delay Time",None,1003,520,26,26,"K",T("Delay Time: 1/8"),"high",NOSLOT)
f("DELAY SYNC","Delay tempo sync","DelaySync",None,1070,500,14,14,"B",T("Delay Sync")+" (Remote name is 'DelaySync')","high",NOSLOT)
f("DELAY FEEDBACK","Delay feedback","Delay Feedback",None,1140,520,26,26,"K",T("Delay Feedback: 35%"),"high",NOSLOT)
f("DELAY PAN","Delay pan","Delay Pan",None,1225,520,26,26,"K",T("Delay Pan: -2"),"high",NOSLOT)
f("PHASER RATE","Phaser rate","Phaser Rate",None,1347,520,26,26,"K",T("Phaser Rate: 28%"),"high",NOSLOT)
f("PHASER FBK","Phaser feedback","Phaser Feedback",None,1428,520,26,26,"K",T("Phaser Feedback: 29%"),"high",NOSLOT)
# back
b("PAD RHYTHMIF tape (back)","Patch name tape (back)","D",57,260,14,60,T("Pad Rhythmification"))
for i,y in enumerate((165,218,272),1):
    b(f"Gate {i} CV In",f"CV input: gate {i} (MIDI note)","J",117,y,18,18,T(f"Gate {i} CV In"))
for lab,tt,tj,ty,jy in (("High Pass Freq","High Pass Filter Freq CV Amount: 50%","High Pass Filter Freq CV In",160,165),("Band Pass Freq","Band Pass Filter Freq CV Amount: 50%","Band Pass Filter Freq CV In",216,218),("Low Pass Freq","Low Pass Filter Freq CV Amount: 50%","Low Pass Filter Freq CV In",272,272),("LFO Rate","LFO Rate CV Modulation Amount: 50%","LFO Rate CV In",338,340)):
    b(f"{lab} CV trim",f"Amount for {lab} CV","K",407,ty,20,20,T(tt),"trim next to CV jack; Remote has no item for it")
    b(f"{lab} CV In",f"CV input: {lab}","J",451,jy,18,18,T(tj))
for i,y in enumerate((165,218,273),1): b(f"Gate {i} CV Out",f"CV output: gate {i}","J",780,y,18,18,T(f"Gate {i} CV Out"))
b("LFO CV Out","CV output: LFO","J",780,342,18,18,T("LFO CV Out"))
for lab,y,pre in (("High Pass",157,"High Pass"),("Band Pass",238,"Band Pass"),("Low Pass",318,"Low Pass")):
    b(f"{lab} Channel L","Separate output left","J",1077,y,20,20,T(f"{pre} Channel Left Output"))
    b(f"{lab} Channel R","Separate output right","J",1153,y,20,20,T(f"{pre} Channel Right Output"))
b("Audio In L","Audio input left","J",1300,80,20,20,T("Connected to MasterComp 1: Left Output")+"; this jack's own name NOT read yet")
b("Audio In R","Audio input right","J",1385,80,20,20,T("Connected to MasterComp 1: Right Output")+" (cut off at edge); own jack name NOT read yet")
b("Main Out L","Main output left","J",1300,397,20,20,T("Connected to Audiomatic 1: Left Input")+"; this jack's own name NOT read yet")
b("Main Out R","Main output right","J",1385,397,20,20,T("Connected to Audiomatic 1: Right Input")+"; this jack's own name NOT read yet")
base=dict(device="Alligator",prefix="ALGT",remote_scope="Propellerheads / Alligator",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="alligator",front_raw="_captures_batchD/alligator_front_raw.jpg",back_raw="_captures_batchD/alligator_back_raw.jpg",front=F,back=B),open("tools/specs/alligator.json","w"))
json.dump(dict(device="Alligator",front=CF,back=CB),open("tools/checks/alligator.json","w"),indent=0)
print(len(F),len(B))
