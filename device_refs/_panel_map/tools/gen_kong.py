import json
# Kong Drum Designer. Three pictures: main panel (top part), "Drum and FX" section open (lower part), back panel (section open).
# Positions are picture pixels. Hover results come from Reason 12, 2026-10-08.
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
SEL="Remote item exists for Drum 1-16; this one physical knob/button acts on the SELECTED drum (Drum 1 when checked)"
NOSLOT="Remote item exists in Reason but is beyond the 48 knob slots of our remotemap (not mapped)"
NP="name from Remote list + printed label; NOT proven by tooltip"
def mk(): return [],{}
F,CF=mk(); V,CV=mk(); B,CB=mk(); P,CP=mk()
def f(L,C,label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why="",mode=None):
    L.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]+([mode] if mode else [])); C[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why="",name=None,slot=None,mode=None):
    B.append([label,what,typ,[x,y],[hw,hh],why,mode,name,slot]); CB[label]=chk
fm=lambda *a,**k:f(F,CF,*a,**k)
fv=lambda *a,**k:f(V,CV,*a,**k)
def fp(label,what,name,slot,x,y,hw,hh,*r,**k):
    f(P,CP,label,what,name,slot,(x-1270)*3,(y-180)*3,hw*3,hh*3,*r,**k)

# ---------------- main panel (kong_top_raw.jpg, 1568x728) ----------------
fm("(triangle)","Fold/unfold device",None,None,58,25,8,8,"B",NT,"medium")
fm("Patch display","Patch name display","Patch Name",None,272,46,185,17,"D",NT+" (display)","medium","Remote item 'Patch Name'; display gave no tooltip; name NOT proven")
fm("(up arrow)","Load previous patch","Select Previous Patch",None,483,36,14,9,"B",T("Select previous patch"))
fm("(down arrow)","Load next patch","Select Next Patch",None,483,56,14,9,"B",T("Select next patch"))
fm("(folder)","Open patch browser",None,None,519,46,15,15,"B",T("Browse patch"))
fm("(disk)","Save patch",None,None,556,46,15,15,"B",T("Save patch"))
fm("NOTE ON light","Note-on indicator light","Note On Indicator",None,112,86,9,9,"D",NT,"medium","Remote item 'Note On Indicator'; light gave no tooltip; NOT proven")
fm("KONG KIT tape","Patch name tape","Device Name",None,72,170,14,75,"D",T("Kong Kit")+" (patch name; 'Device Name' item not provable here)","medium","Remote item 'Device Name'; convention from earlier devices")
fm("PITCH BEND wheel","Pitch bend wheel","Pitch Bend",None,108,193,13,72,"S",T("Pitch Bend: 0")+" (hover the lower part of the wheel; centre showed nothing)","high","Remote item 'Pitch Bend'")
fm("MOD WHEEL","Modulation wheel","Mod Wheel",None,160,193,13,72,"S",T("Mod Wheel: 0")+" (hover the lower part of the wheel)","high","Remote item 'Mod Wheel'")
for r,y in enumerate((108,266,424,582)):
    for c,x in enumerate((690,846,1002,1158)):
        n=13-4*r+c
        fm(f"PAD {n}",f"Pad {n} (hit it with the mouse to play drum {n})",f"Pad {n} Hit Indication",None,x,y,70,62,"B",NT,"medium",f"Remote item 'Pad {n} Hit Indication' (hit light); pad gave no tooltip; NOT proven")
fm("MASTER LEVEL","Master level","Master Level",None,1355,98,45,45,"K",T("Master Level: 100"),"high","Remote item 'Master Level'; no knob slot in our remotemap")
fm("Meter L","Output level lights, left",None,None,1447,92,7,36,"D",T("Master Level Output Left"),"medium","tooltip name; not a Remote item",mode="left")
fm("Meter R","Output level lights, right",None,None,1471,92,7,36,"D",T("Master Level Output Right"),"medium","tooltip name; not a Remote item",mode="right")
fm0=fm; fm=fp  # right-hand column goes on an enlarged picture
fm("PAD MUTE","Mute the selected pad","Pad 1 Mute",None,1320,237,28,12,"B",T("Pad 1 Mute")+" (selected pad was 1)","high","Remote has Pad 1-16 Mute; one button acts on the selected pad")
fm("PAD CLR","Clear all mutes and solos","Set all Mutes and Solos to Off",None,1372,237,24,12,"B",T("Set all Mutes and Solos to Off"))
fm("PAD SOLO","Solo the selected pad","Pad 1 Solo",None,1425,237,28,12,"B",T("Pad 1 Solo")+" (selected pad was 1)","high","Remote has Pad 1-16 Solo; one button acts on the selected pad")
fm("PAD SETTINGS Q","Quick Edit mode: Pad Mute/Solo",None,None,1480,237,11,11,"B",T("Quick Edit Mode: Pad Mute/Solo"))
for r,(row,y) in enumerate((("A B C",303),("D E F",332),("G H I",360))):
    for c,(g,x) in enumerate(zip(row.split(),(1366,1396,1425))):
        fm(f"GROUP {g}",f"Pad group {g} (selected pad joins it)",None,None,x,y,14,13,"B",T(f"Pad 1 Group {g}"),mode="in")
for lab,y in (("MUTE",303),("LINK",331),("ALT",360)):
    fm(f"GROUP {lab} light",f"Pad group mode light: {lab}",None,None,1440,y,8,8,"D",NT,mode="right")
fm("PAD GROUP Q","Quick Edit mode: Pad Group",None,None,1480,360,11,11,"B",T("Quick Edit Mode: Pad Group"))
for r,y in enumerate((430,459,487,516)):
    for c,x in enumerate((1337,1366,1396,1425)):
        n=13-4*r+c
        fm(f"ASSIGN {n}",f"Drum assignment: give the selected pad drum {n}",None,None,x,y,14,13,"B",T("Pad 1 Drum Assignment")+" (all 16 buttons show this same text)",mode="in")
fm("DRUM ASSIGNMENT Q","Quick Edit mode: Pad Hit/Drum Assignment",None,None,1480,516,11,11,"B",T("Quick Edit Mode: Pad Drum Assignment"))
for i,y in enumerate((579,603,629,654),1):
    fm(f"HIT TYPE {['I','II','III','IV'][i-1]}",f"Hit type {i} of the selected pad",None,None,1310,y,17,12,"B",T("Pad 1 Hit Type"),mode="in")
fm("HIT TYPE display","Hit type name display",None,None,1392,593,64,30,"D",NT+" (display)","medium")
fm("HIT TYPE Q","Quick Edit mode: Pad Hit Assignment",None,None,1480,654,11,11,"B",T("Quick Edit Mode: Pad Hit Assignment"))
fm=fm0
fm("(drum patch arrows)","Previous / next drum patch (up arrow = previous, down arrow = next)",None,None,127,351,17,17,"B",T("Select Previous Drum Patch")+" on the upper half; "+T("Select Next Drum Patch")+" on the lower half")
fm("(drum folder)","Open drum patch browser",None,None,164,351,17,17,"B",T("Browse Drum Patch"))
fm("(drum disk)","Save drum patch",None,None,201,351,17,17,"B",T("Save Drum Patch"))
fm("(drum sample button)","Create a sample player by sampling","Quick Sample",None,238,351,17,17,"B",T("Create Sample Player by Sampling"),"medium","Remote item 'Quick Sample'; match to this button is by meaning, NOT proven")
fm("Drum name display","Name of the selected drum's patch",None,None,275,410,155,20,"D",NT+" (display)","medium")
fm("DRUM number","Selected drum number",None,None,475,432,34,32,"D",NT+" (display)","medium")
fm("(sample loading bar)","Sample loading progress bar","Sample Loading Progress",None,525,410,9,20,"D",NT,"low","Remote item 'Sample Loading Progress'; probably this bar; NOT proven")
fm("OFFSET PITCH","Pitch offset of the selected drum","Drum 1 Pitch Offset",2,150,484,22,22,"K",NT+"; again 2-3 s, still none","medium",SEL+". Name from Remote list + label; NOT proven by tooltip")
fm("OFFSET DECAY","Decay offset of the selected drum","Drum 1 Decay Offset",3,150,553,22,22,"K",NT,"medium",SEL+". "+NP)
fm("SEND BUS FX","Send to Bus FX of the selected drum","Drum 1 Bus FX Send",None,232,484,22,22,"K",NT,"medium",SEL+". "+NP+". "+NOSLOT)
fm("SEND AUX 1","Send to Aux 1 of the selected drum","Drum 1 Aux 1 Send",None,232,553,22,22,"K",NT,"medium",SEL+". "+NP+". "+NOSLOT)
fm("SEND AUX 2","Send to Aux 2 of the selected drum","Drum 1 Aux 2 Send",None,296,553,22,22,"K",NT,"medium",SEL+". "+NP+". "+NOSLOT)
fm("PAN","Pan of the selected drum","Drum 1 Pan",None,377,484,22,22,"K",NT,"medium",SEL+". "+NP+". "+NOSLOT)
fm("TONE","Tone of the selected drum","Drum 1 Tone",None,377,553,22,22,"K",NT,"medium",SEL+". "+NP+". "+NOSLOT)
fm("LEVEL","Level of the selected drum","Drum 1 Level",1,473,527,38,38,"K",NT+"; again 3 s, still none","medium",SEL+". Name from Remote list + label; NOT proven by tooltip")
fm("Q PITCH/DECAY","Quick Edit mode: Drum Pitch/Decay Offset",None,None,169,629,10,10,"B",T("Quick Edit Mode: Drum Pitch/Decay Offset"))
fm("Q SENDS","Quick Edit mode: Drum Sends",None,None,315,629,10,10,"B",T("Quick Edit Mode: Drum Sends"))
fm("Q PAN/LEVEL","Quick Edit mode: Drum Pan/Level",None,None,397,629,10,10,"B",T("Quick Edit Mode: Drum Pan/Level"))
fm("Q TONE/LEVEL","Quick Edit mode: Drum Tone/Level",None,None,534,629,10,10,"B",T("Quick Edit Mode: Drum Tone/Level"))
fm("SHOW DRUM AND FX","Open / close the Drum and FX section",None,None,131,674,32,17,"B",T("Show Drum And FX"))

# ---------------- Drum and FX section (kong_dm_fx_raw.jpg, 1232x953) ----------------
DMV="Drum module of the SELECTED drum (Drum 1 = PM Bass Drum when checked). The module and FX shown change with the drum."
fv("DM ON","Drum module on/off","Drum 1 DM On",None,82,527,14,9,"B",T("Drum 1 DM On"),"high",DMV)
fv("DM menu arrow","Drum module menu",None,None,113,527,14,9,"B",NT,"medium",mode="below")
fv("DM PITCH","Drum module pitch","Drum 1 DM Pitch",None,122,573,26,26,"K",T("Drum 1 DM Pitch: 0"),"high",DMV+" "+NOSLOT)
fv("DM TUNE 1","Bass drum tune 1 (module-only knob)",None,None,205,573,26,26,"K",T("Tune 1: 107"),"high",DMV+" No Remote item.")
fv("DM TUNE 2","Bass drum tune 2 (module-only knob)",None,None,283,573,26,26,"K",T("Tune 2: 60"),"high",DMV+" No Remote item.")
fv("DM BEND AMOUNT","Bass drum bend amount (module-only knob)",None,None,364,573,26,26,"K",T("Bend Amount: 57"),"high",DMV+" No Remote item.")
fv("DM DAMP","Bass drum damp (this module's variable knob)","Drum 1 DM Variable",None,444,573,26,26,"K",T("Drum 1 DM Variable: 82")+" (printed label DAMP)","high",DMV+" "+NOSLOT)
fv("DM DECAY","Drum module decay","Drum 1 DM Decay",None,524,573,26,26,"K",T("Drum 1 DM Decay: 28"),"high",DMV+" "+NOSLOT)
fv("DM DENSITY","Beater density (module-only knob)",None,None,123,668,26,26,"K",T("Beater Density: 102"),"high",DMV+" No Remote item.")
fv("DM SHELL LEVEL","Shell level (module-only knob)",None,None,524,668,26,26,"K",T("Shell Level: 33"),"high",DMV+" No Remote item.")
fv("DM TONE","Beater tone (module-only knob)",None,None,122,750,26,26,"K",T("Beater Tone: 75"),"high",DMV+" No Remote item.")
fv("DM BEATER LEVEL","Beater level (module-only knob)",None,None,122,830,26,26,"K",T("Beater Level: 64"),"high",DMV+" No Remote item.")
fv("DM LEVEL","Drum module level (dark knob)","Drum 1 DM Level",None,524,830,26,26,"K",T("Drum 1 DM Level: 100"),"high",DMV+" "+NOSLOT)
fv("FX1 ON","FX 1 on/off","Drum 1 FX1 On",None,598,527,14,9,"B",T("Drum 1 FX1 On"),"high",NOSLOT)
fv("FX1 menu arrow","FX 1 menu",None,None,628,527,14,9,"B",NT,"medium",mode="below")
for i,y in enumerate((553,574,594,613),1):
    fv(f"FX1 HIT {['I','II','III','IV'][i-1]}",f"FX 1 enable for hit type {i}",None,None,611,y,12,10,"B",T(f"Drum 1 FX1 Enable Hit {i}"),"high","tooltip name; not a Remote item",mode="left")
fv("FX1 waveform icon","Shows the FX 1 tone waveform",None,None,688,550,15,12,"D",NT,"medium")
fv("FX1 PITCH","FX 1 tone: pitch (first FX knob)","Drum 1 FX1 P1",None,662,590,22,22,"K",T("Drum 1 FX1 P1: 6"),"high",DMV+" "+NOSLOT)
fv("FX1 ATTACK","FX 1 tone: attack",None,None,620,703,22,22,"K",T("Attack: 20"),"high","No Remote item.")
fv("FX1 DECAY","FX 1 tone: decay (second FX knob)","Drum 1 FX1 P2",None,684,703,22,22,"K",T("Drum 1 FX1 P2: 59"),"high",NOSLOT)
fv("FX1 BEND DEC","FX 1 tone: bend decay",None,None,620,768,22,22,"K",T("Bend Decay: 25"),"high","No Remote item.")
fv("FX1 BEND","FX 1 tone: bend",None,None,684,768,22,22,"K",T("Bend: 0"),"high","No Remote item.")
fv("FX1 SHAPE","FX 1 tone: shape",None,None,620,832,22,22,"K",T("Shape: 67"),"high","No Remote item.")
fv("FX1 LEVEL","FX 1 tone: level",None,None,684,832,22,22,"K",T("Level: 72"),"high","No Remote item.")
fv("FX2 ON","FX 2 on/off","Drum 1 FX2 On",None,740,527,14,9,"B",T("Drum 1 FX2 On"),"high",NOSLOT)
fv("FX2 menu arrow","FX 2 menu",None,None,770,527,14,9,"B",NT,"medium",mode="below")
fv("FX2 blank plate","FX 2 slot (empty: 'Blank Plate')",None,None,793,685,58,36,"D",NT+" (slot empty)","medium")
fv("BUS FX ON","Bus FX on/off","Bus FX On",None,912,527,14,9,"B",T("Bus FX On"),"high",NOSLOT)
fv("BUS FX menu arrow","Bus FX menu",None,None,942,527,14,9,"B",NT,"medium",mode="below")
fv("BUS FX lights","Bus FX indicator lights",None,None,996,526,22,6,"D",NT,"medium")
fv("BUS FX blank plate","Bus FX slot (empty: 'Blank Plate')",None,None,967,685,58,36,"D",NT+" (slot empty)","medium")
fv("MASTER FX ON","Master FX on/off","Master FX On",None,1054,527,14,9,"B",T("Master FX On"),"high",NOSLOT)
fv("MASTER FX menu arrow","Master FX menu",None,None,1084,527,14,9,"B",NT,"medium",mode="below")
fv("MASTER FX lights","Master FX indicator lights",None,None,1140,526,22,6,"D",NT,"medium")
fv("COMP AMOUNT","Master compressor: amount",None,None,1108,617,28,28,"K",T("Amount: 29"),"high","No Remote item.")
fv("COMP ATTACK","Master compressor: attack (first Master FX parameter)","Master FX P1",None,1077,725,22,22,"K",T("Master FX P1: 67"),"high",NOSLOT)
fv("COMP RELEASE","Master compressor: release (second Master FX parameter)","Master FX P2",None,1141,725,22,22,"K",T("Master FX P2: 67"),"high",NOSLOT)
fv("COMP MAKE UP GAIN","Master compressor: make-up gain",None,None,1108,822,28,28,"K",T("Make Up Gain: 25"),"high","No Remote item.")
fv("COMP icon","Compressor corner icon",None,None,1161,870,10,10,"D",NT,"low")
fv("BUS FX TO MASTER FX","Level from Bus FX to Master FX","Level Bus FX to Master FX",None,999,907,14,14,"K",T("Level from Bus FX to Master FX: 100"),"high",NOSLOT)
fv("PITCH BEND RANGE","Pitch bend range of the selected drum",None,None,293,907,14,14,"K",T("Drum 1 Pitch Bend Range: 6"),"high","tooltip name; not a Remote item")
fv("DRUM OUTPUT menu","Which output the selected drum plays to (shows 'Master FX')",None,None,730,907,85,10,"D",NT,"medium")

# ---------------- back panel, section open (kong_back_full_raw.jpg, 1176x1011) ----------------
b("KONG KIT tape (back)","Patch name tape (back)","D",33,165,14,40,NT)
b("Sequencer Control Gate In","Gate input from a sequencer","J",146,188,12,12,T("Sequencer Control Gate In"))
b("Sequencer Control CV In","CV (note) input from a sequencer","J",208,188,12,12,T("Sequencer Control CV In"))
b("Master Volume trim","Amount for Master Volume CV","K",127,295,13,13,T("Master Volume In: 127"),"trim next to CV jack; no Remote item")
b("Master Volume In","CV input: master volume","J",167,295,12,12,T("Master Volume In"))
b("Pitch Wheel trim","Amount for Pitch Wheel CV","K",127,334,13,13,T("Pitch Wheel In: 127"),"trim next to CV jack; no Remote item")
b("Pitch Wheel In","CV input: pitch wheel","J",167,334,12,12,T("Pitch Wheel In"))
b("Mod Wheel trim","Amount for Mod Wheel CV","K",127,374,13,13,T("Mod Wheel In: 127"),"trim next to CV jack; no Remote item")
b("Mod Wheel In","CV input: mod wheel","J",167,374,12,12,T("Mod Wheel In"))
for lab,x in (("Send 1 Left",97),("Send 1 Right",142),("Send 2 Left",212),("Send 2 Right",258)):
    s,side=lab.split()[1],lab.split()[2]
    b(f"Aux {lab}",f"Aux send {s} output, {side.lower()}","J",x,467,15,15,T(f"Send {s} Audio Out {side}"))
b("(Show Drum and FX)","Open / close the Drum and FX section","B",120,546,30,12,T("Show Drum And FX"))
for r,(yi,yo) in enumerate(((104,135),(228,259),(352,383),(475,506))):
    for c,x in enumerate((390,512,636,760)):
        n=13-4*r+c
        b(f"Pad {n} Gate In",f"Gate input: pad {n}","J",x,yi,11,11,T(f"Pad {n} Gate In"),mode="left")
        b(f"Pad {n} Gate Out",f"Gate output: pad {n}","J",x,yo,11,11,T(f"Pad {n} Gate Out"),mode="left")
for n,(x,y) in zip(range(3,17),((1031,144),(1079,144),(915,209),(962,209),(1031,209),(1079,209),(915,274),(962,274),(1031,274),(1079,274),(915,339),(962,339),(1031,339),(1079,339))):
    b(f"Audio Out {n}",f"Separate audio output for drum {n}","J",x,y,16,16,T(f"Audio Out {n}"))
b("Main Audio Out L","Main audio output, left","J",970,447,16,16,T("Main Audio Out Left")+" (jack was empty)")
b("Main Audio Out R","Main audio output, right","J",1018,447,16,16,T("Main Audio Out Right")+" (jack was empty)")
b("Bus FX Audio In L","Audio input into Bus FX, left","J",87,822,18,18,T("Bus FX Audio Input Left"))
b("Bus FX Audio In R","Audio input into Bus FX, right","J",136,822,18,18,T("Bus FX Audio Input Right"))
b("Bus FX Parameter 1 trim","Amount for Bus FX parameter 1 CV","K",246,801,13,13,T("Bus FX Parameter 1 In: 127"),"trim next to CV jack; no Remote item")
b("Bus FX Parameter 1 In","CV input: Bus FX parameter 1","J",282,803,12,12,T("Bus FX Parameter 1 In"))
b("Bus FX Parameter 2 trim","Amount for Bus FX parameter 2 CV","K",246,868,13,13,T("Bus FX Paramater 2 In: 127")+" (Reason's own spelling 'Paramater')","trim next to CV jack; no Remote item")
b("Bus FX Parameter 2 In","CV input: Bus FX parameter 2","J",282,869,12,12,T("Bus FX Paramater 2 In")+" (Reason's own spelling 'Paramater')")
b("Bus FX to Master FX Level","Level from Bus FX to Master FX (back copy)","K",378,806,26,26,NT+" (the front knob of the same name did show a tooltip)")
b("Breakout Output L","Breakout output to an external effect, left","J",504,822,18,18,T("To External FX Output Left"))
b("Breakout Output R","Breakout output to an external effect, right","J",554,822,18,18,T("To External FX Output Right"))
b("Breakout Input L","Breakout input from an external effect, left","J",678,822,18,18,T("From External FX Input Left"))
b("Breakout Input R","Breakout input from an external effect, right","J",726,822,18,18,T("From External FX Input Right"))
b("Master FX Parameter 1 trim","Amount for Master FX parameter 1 CV","K",860,801,13,13,T("Master FX Parameter 1 In: 127"),"trim next to CV jack; no Remote item")
b("Master FX Parameter 1 In","CV input: Master FX parameter 1","J",896,803,12,12,T("Master FX Parameter 1 In"))
b("Master FX Parameter 2 trim","Amount for Master FX parameter 2 CV","K",860,868,13,13,T("Master FX Parameter 2 In: 127"),"trim next to CV jack; no Remote item")
b("Master FX Parameter 2 In","CV input: Master FX parameter 2","J",896,869,12,12,T("Master FX Parameter 2 In"))

base=dict(device="Kong Drum Designer",prefix="KONG",remote_scope="Propellerheads / Kong Drum Designer",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="kong-drum-designer",front_raw="_captures_batchE/kong_top_raw.jpg",back_raw="_captures_batchE/kong_back_full_raw.jpg",front=F,back=B),open("tools/specs/kong-drum-designer.json","w"))
json.dump(dict(base,slug="kong-drum-designer-dmfx-view",front_offsets={"K":100,"B":100,"D":100,"S":100},front_raw="_captures_batchE/kong_dm_fx_raw.jpg",back_raw="",front=V,back=[]),open("tools/specs/kong-drum-designer--dmfx.json","w"))
json.dump(dict(base,slug="kong-drum-designer-padside-view",front_offsets={"K":200,"B":200,"D":200,"S":200},front_raw="_captures_batchE/kong_pad_side_raw.jpg",back_raw="",front=P,back=[]),open("tools/specs/kong-drum-designer--padside.json","w"))
json.dump(dict(device="Kong Drum Designer",front=CF,back=CB,views=dict(dmfx=CV,padside=CP),view_titles=dict(padside="Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)",dmfx="Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)")),open("tools/checks/kong-drum-designer.json","w"),indent=0)
print(len(F),len(V),len(P),len(B))
