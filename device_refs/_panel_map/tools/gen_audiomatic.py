import json
F=[];B=[];CF={};CB={}
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why=""):
    B.append([label,what,typ,[x,y],[hw,hh],why]); CB[label]=chk
f("Bypass/On/Off","3-way device switch","Enabled",2,95,25,12,22,"B",T("Enabled: On"))
f("(triangle)","Fold/unfold device",None,None,40,20,8,8,"B",NT,"medium")
f("AUDIOMATIC 1 tape","Device name tape","Device Name",None,40,200,14,50,"D",T("Audiomatic 1")+" (device name)","medium","Remote item 'Device Name'; the tooltip shows the rack name 'Audiomatic 1'")
f("Input meter","Input level lights (6)",None,None,338,190,12,60,"D",NT)
f("Gain","Input gain","Input Gain",3,338,297,26,26,"K",T("Input Gain: 0.0 dB"))
f("(screen)","Picture screen that changes with the chosen preset",None,None,545,212,145,130,"D",NT,"medium","display only")
names=["Tape","Hi-Fi","Bright","Bottom","Spread","Radio","VHS","Vinyl","mp3","Psyche","Cracked","Gadget","Circuit","Wash","PVC","Eerie"]
for i,n in enumerate(names):
    f(f"Preset {n}",f"Preset button: {n}","Preset",4 if i==0 else None,[769,852,933,1014][i%4],[76,151,229,304][i//4],34,18,"B",T("Preset"),"high" if i==0 else "medium","all 16 buttons show the same tooltip 'Preset'; Remote item 'Preset' is stepped Tape..Eerie, so the 16 buttons are its 16 values" if i==0 else "same Remote item 'Preset' (one row carries the knob slot)")
f("Transform","Transform amount","Transform",5,1178,172,52,52,"K",T("Transform: 50%"))
f("Dry/Wet","Dry/wet balance","Dry Wet",1,1130,297,26,26,"K",T("Dry Wet: 100%")+" (hover spells 'Dry Wet'; read as 'Dry/Wet: 100%' from the zoom)")
f("Volume","Output volume","Volume",6,1225,297,26,26,"K",T("Volume: 0.0 dB"))
b("Transform CV trim","Amount for Transform CV","K",925,152,20,20,T("Transform CV Trim: 100%"),"trim next to CV jack; Remote has no item for it")
b("Transform CV In","CV input: Transform","J",980,152,18,18,T("Transform CV Input"))
b("Dry-Wet CV trim","Amount for Dry-Wet CV","K",1060,152,20,20,T("Dry Wet CV Trim: 100%"),"trim next to CV jack; Remote has no item for it")
b("Dry-Wet CV In","CV input: Dry-Wet","J",1115,152,18,18,T("Dry Wet CV Input"))
b("Audio In L","Audio input left","J",781,330,20,20,'cabled: tooltip "Connected to Pad Rhythmification: Left Ou..." (cut off); own jack name NOT read yet')
b("Audio In R","Audio input right","J",841,330,20,20,'cabled: tooltip "Connected to Pad Rhythmification: Right ..." (cut off); own jack name NOT read yet')
b("Audio Out L","Audio output left","J",1214,330,20,20,'cabled: tooltip "Connected to Vocoder 1: Left Carrier"; own jack name NOT read yet')
b("Audio Out R","Audio output right","J",1275,330,20,20,'cabled: tooltip "Connected to Vocoder 1: Right Carrier"; own jack name NOT read yet')
for i,y in enumerate((205,250,295,338,382)): b(f"(routing icon {i+1})","Routing icon","D",263,y,14,18,NT)
b("AUDIOMATIC 1 tape (back)","Device name tape (back)","D",30,190,14,50,T("Audiomatic 1"))
b("(triangle) back","Fold/unfold device","D",28,40,8,8,NT)
b("Speaker grille","Decoration (speaker grille)","D",540,255,140,125,NT)
base=dict(device="Audiomatic",prefix="AUDM",remote_scope="se.propellerheads.Audiomatic",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="audiomatic",front_raw="_captures_batchD/audiomatic_front_raw.jpg",back_raw="_captures_batchD/audiomatic_back_raw.jpg",front=F,back=B),open("tools/specs/audiomatic.json","w"))
json.dump(dict(device="Audiomatic",front=CF,back=CB),open("tools/checks/audiomatic.json","w"),indent=0)
