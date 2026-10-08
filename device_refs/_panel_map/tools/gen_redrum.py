import json,sys
sys.path.insert(0,"/private/tmp/claude-501/-Users-johnsuhr-Desktop-Homeroom-Studio/390ae6d7-325b-421c-a051-4810f4083a39/scratchpad")
# Redrum Drum Computer. Front picture is the raw x2 (coordinates below are RAW px, doubled on the way in). Notes: _captures_batchE/redrum_hover_notes.txt
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists in Reason but is beyond the 48 knob slots of our remotemap (not mapped)"
SKIP="not hovered on this channel (no tooltip seen on this widget in channels 1-4)"
notes={}
for ln in open("_captures_batchE/redrum_hover_notes.txt"):
    p=ln.rstrip("\n").split("|",2)
    if len(p)==3: notes[(p[0],p[1])]=p[2]
F=[];CF={};B=[];CB={}
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why="",mode=None):
    F.append([label,what,name,slot,[x*2,y*2],[hw*2,hh*2],typ,conf,why]+([mode] if mode else [])); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why="",mode=None):
    B.append([label,what,typ,[x,y],[hw,hh],why,mode]); CB[label]=chk
def chk(key,pre="RF"):
    v=notes[(pre,key)]
    if v.startswith("(no tooltip"): return NT if "not hovered" not in v else v
    if v.startswith("(not hovered"): return SKIP
    return T(v) if not v.endswith(")") or "sample file name" not in v else T(v.replace(" (sample file name)",""))+" (the file name of the loaded sample)"
def cx(i): return 227+132.3*(i-1)
# ---- channels
for i in range(1,11):
    x=cx(i); p=lambda k:chk(f"c{i}_{k}")
    f(f"CH{i} MUTE",f"Mute drum {i}",f"Drum {i} Mute",None,x-40,18,14,9,"B",p("M"),"high",NOSLOT)
    f(f"CH{i} SOLO",f"Solo drum {i}",f"Drum {i} Solo",None,x,18,14,9,"B",p("S"),"high",NOSLOT)
    f(f"CH{i} PLAY",f"Play (trigger) drum {i}",f"Channel {i} Play",None,x+40,18,14,9,"B",p("PLAY"),"medium",f"tooltip says 'Trigger Drum {i}'; Remote item 'Channel {i} Play' matched by meaning, NOT proven")
    f(f"CH{i} sample name",f"Sample loaded on drum {i}",f"Channel {i} Sample",None,x,45,55,10,"D",p("NAME"),"medium",f"Remote item 'Channel {i} Sample'; tooltip shows the file name")
    f(f"CH{i} sample arrows",f"Previous / next sample on drum {i}",None,None,x-31,78,14,16,"B",T("Select previous sample")+" (upper half); "+T("Select next sample")+" (lower half, checked on drum 1)" if i==1 else T("Select previous sample")+" (upper half; lower half checked on drum 1 only)")
    f(f"CH{i} BROWSE",f"Browse samples for drum {i}",None,None,x+3,80,14,12,"B",p("FOLDER"))
    f(f"CH{i} SAMPLE (wave button)",f"Start sampling into drum {i}",None,None,x+38,80,14,12,"B",p("WAVE"))
    f(f"CH{i} S1",f"Send 1 amount, drum {i}",f"Drum {i} Send 1 Amount",None,x-35,126,13,13,"K",p("S1"),"high",NOSLOT)
    f(f"CH{i} S2",f"Send 2 amount, drum {i}",f"Drum {i} Send 2 Amount",None,x+35,126,13,13,"K",p("S2"),"high",NOSLOT)
    f(f"CH{i} light (top)",f"Light between S1 and S2, drum {i}",None,None,x-1,118,5,5,"D",p("LEDtop"),"low")
    f(f"CH{i} PAN",f"Pan, drum {i}",f"Drum {i} Pan",4*i,x,162,13,13,"K",p("PAN"))
    f(f"CH{i} LEVEL",f"Level, drum {i}",f"Drum {i} Level",4*i-3,x-27,222,19,19,"K",p("LEVEL"))
    f(f"CH{i} VEL (level)",f"How much velocity changes level, drum {i}",f"Drum {i} Vel to Level",None,x+37,222,13,13,"K",p("VEL_LEVEL"),"high",NOSLOT)
    f(f"CH{i} LENGTH",f"Length, drum {i}",f"Drum {i} Length",4*i-1,x-28,289,19,19,"K",p("LENGTH"))
    f(f"CH{i} DECAY/GATE",f"Decay or gate mode switch, drum {i}",f"Drum {i} Decay/Gate Mode",None,x+18,288,12,20,"B",p("SWITCH"),"high",NOSLOT)
    if i in (6,7):
        f(f"CH{i} PITCH",f"Pitch, drum {i}",f"Drum {i} Pitch",4*i-2,x-28,358,17,17,"K",p("PITCH"))
        f(f"CH{i} BEND",f"Pitch bend amount, drum {i}",f"Drum {i} Pitch Bend Amount",None,x+36,358,13,13,"K",p("BEND"),"high",NOSLOT)
        f(f"CH{i} RATE",f"Pitch bend rate, drum {i}",f"Drum {i} Pitch Bend Rate",None,x-28,431,13,13,"K",p("RATE"),"high",NOSLOT)
        f(f"CH{i} VEL (bend)",f"How much velocity changes pitch bend, drum {i}",f"Drum {i} Vel to Pitch Bend",None,x+36,431,13,13,"K",p("VEL_B"),"high",NOSLOT)
    else:
        f(f"CH{i} PITCH",f"Pitch, drum {i}",f"Drum {i} Pitch",4*i-2,x,358,19,19,"K",p("PITCH"))
        f(f"CH{i} light (pitch)",f"Light above the pitch knob, drum {i}",None,None,x,336,5,5,"D",p("LEDpitch"),"low")
        if i in (1,2,10):
            f(f"CH{i} TONE",f"Tone, drum {i}",f"Drum {i} Tone",None,x-28,431,19,19,"K",p("TONE"),"high",NOSLOT)
            f(f"CH{i} VEL (tone)",f"How much velocity changes tone, drum {i}",f"Drum {i} Vel to Tone",None,x+36,431,13,13,"K",p("VEL_TONE"),"high",NOSLOT)
        else:
            f(f"CH{i} START",f"Sample start, drum {i}",f"Drum {i} Sample Start",None,x-28,431,19,19,"K",p("START"),"high",NOSLOT)
            f(f"CH{i} VEL (start)",f"How much velocity changes sample start, drum {i}",f"Drum {i} Vel to Sample Start",None,x+36,431,13,13,"K",p("VEL_START"),"high",NOSLOT)
    f(f"CH{i} SELECT",f"Select drum {i} (edit its steps)",f"Select Drum {i}",None,x+18,488,22,9,"B",p("SELECT"),"medium","Remote item 'Select Drum %d'; button gave no tooltip; NOT proven"%i)
# ---- master + bottom
r=lambda k:chk(k,"RB2")
f("MASTER LEVEL","Master level","Master Level",48,118,38,18,18,"K",r("MASTER"))
f("(patch display)","Patch name display","Patch Name",None,190,537,95,12,"D",NT+" (display)","medium","Remote item 'Patch Name'; display gave no tooltip; NOT proven")
f("(patch arrows)","Previous / next patch","Select Previous Patch",None,105,570,14,16,"B",T("Select previous patch")+" (upper half); "+T("Select next patch")+" (lower half)","high","upper half = Select Previous Patch; lower half = Select Next Patch (also a Remote item)")
f("(patch folder)","Open patch browser",None,None,145,574,14,12,"B",r("PATCHFOLDER"))
f("(patch disk)","Save patch",None,None,181,574,14,12,"B",r("PATCHDISK"))
f("HIGH QUALITY INTERPOLATION","High quality interpolation on/off","High Quality Interpolation",None,96,623,10,10,"B",r("HQ"),"high",NOSLOT)
f("CHANNEL 8-9 EXCLUSIVE","Drums 8 and 9 cut each other off (open / closed hat)","Channel 8 and 9 Exclusive",None,96,672,10,10,"B",r("EXCL89"),"high",NOSLOT)
f("ENABLE PATTERN SECTION","Pattern section on/off","Enable Pattern Section Playback",None,335,528,10,10,"B",r("ENABLE"),"high",NOSLOT)
f("MUTE light","Mute light",None,None,337,590,5,5,"D",r("MUTELIGHT"),"medium")
f("PATTERN","Pattern on/off","Pattern Enable",47,455,527,10,10,"B",r("PATTERN"))
pos=[(461,564),(495,564),(529,564),(562,564),(461,600),(495,600),(529,600),(562,600)]
for n,(x,y) in enumerate(pos,1):
    f(f"PATTERN {n}",f"Pattern {n} button",f"Pattern {n}",None,x,y,14,13,"B",T("Pattern Select"),"medium",f"tooltip 'Pattern Select' (same on all 8); Remote item 'Pattern {n}' matched by position, NOT proven",mode="in")
f("PATTERN SELECT (1-8 as one control)","Pick pattern 1-8 within the bank","Pattern Select in Bank",41,512,582,56,32,"B",T("Pattern Select")+" (same text on all 8 buttons)","medium","one Remote knob steps through the 8 pattern buttons; box around all 8")
for l,x in zip("ABCD",(461,495,529,562)):
    f(f"BANK {l}",f"Bank {l} button",f"Bank {l}",None,x,657,14,13,"B",T("Bank Select")+" (same text on all 4)","medium",f"Remote item 'Bank {l}' matched by position, NOT proven",mode="in")
f("BANK SELECT (A-D as one control)","Pick bank A-D","Bank Select",42,512,657,56,14,"B",T("Bank Select")+" (same text on all 4 buttons)","medium","one Remote knob steps through banks A-D; box around all 4")
f("RUN","Run / stop the pattern","Run",43,369,648,42,22,"B",T("Play")+" (tooltip says Play; button is labelled RUN)")
f("STEPS display","Pattern length (steps) display",None,None,679,553,28,16,"D",T("Pattern Length: 16"))
f("STEPS arrows","Pattern length up / down",None,None,719,556,10,18,"B",NT+" (upper half hovered; lower half also none)","medium")
f("RESOLUTION","Pattern resolution","Resolution",46,833,552,28,28,"K",T("Resolution: 1/16"))
f("SHUFFLE","Pattern shuffle on/off","Shuffle",44,969,549,9,9,"B",T("Pattern Shuffle"))
f("EDIT STEPS switch","Which 16 steps you edit (1-16 / 17-32 / 33-48 / 49-64)","Edit Steps",None,1062,550,12,22,"B",T("Edit Steps Select"),"high",NOSLOT)
f("DYNAMIC switch","Accent level to enter (hard / medium / soft)","Edit Accent",None,1220,550,12,22,"B",T("Edit Accent"),"high",NOSLOT)
f("FLAM knob","Flam amount","Flam Amount",45,1398,549,16,16,"K",T("Flam Amount: 64"))
f("FLAM button","Flam entry mode",None,None,1454,549,9,9,"B",T("Edit Flam"))
for i in range(16):
    x=631+53.93*i
    f(f"STEP {i+1}",f"Step {i+1} button (toggles the step for the selected drum)",f"Selected Drum Toggle Step {i+1}",None,x,651,22,22,"B",chk(f"STEPBTN{i+1}","RB2"),"medium",f"Remote item 'Selected Drum Toggle Step {i+1}'; button gave no tooltip; NOT proven",mode="above")
    f(f"STEP {i+1} light",f"Step {i+1} light","Selected Drum Step %d"%(i+1),None,x,609,5,5,"D",(NT if i+1 in (1,5,9,16) else SKIP),"low",f"Remote item 'Selected Drum Step {i+1}' probably this light; NOT proven",mode="above")
# ---- back (raw 1565x762)
xs=[107,195,284,372,460,548,637,724,812,900]
BK=lambda k:notes[("RB",k)]
for i,x in enumerate(xs,1):
    b(f"Ch {i} Left",f"Audio output, channel {i} left (or mono)","J",x,143,16,16,T(BK(f"c{i}L")))
    b(f"Ch {i} Right",f"Audio output, channel {i} right","J",x,196,16,16,T(BK(f"c{i}R")))
    b(f"Gate Out {i}",f"Gate output, channel {i}","J",x,245,12,12,T(BK(f"c{i}GO")))
    b(f"Gate In {i}",f"Gate input, channel {i}","J",x,291,12,12,T(BK(f"c{i}GI")))
    b(f"Pitch {i} CV In",f"Pitch CV input, channel {i}","J",x,336,12,12,T(BK(f"c{i}CV")))
    b(f"Pitch {i} CV trim",f"Amount for pitch CV, channel {i}","K",x,383,16,16,T(BK(f"c{i}TR")),"trim under the CV jack; no Remote item")
b("Send Out 1","Send output 1","J",1105,160,18,18,T("Send 1"))
b("Send Out 2","Send output 2","J",1180,160,18,18,T("Send 2"))
b("Stereo Out Left","Stereo output, left","J",1367,160,18,18,T("Left"))
b("Stereo Out Right","Stereo output, right","J",1443,160,18,18,T("Right"))
b("Sample Memory display","Sample memory display","D",1012,543,38,16,NT)
base=dict(device="Redrum Drum Computer",prefix="REDR",remote_scope="Propellerheads / Redrum Drum Computer",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="redrum-drum-computer",front_raw="_captures_batchE/redrum_front_2x.jpg",back_raw="_captures_batchE/redrum_back_raw.jpg",front=F,back=B),open("tools/specs/redrum-drum-computer.json","w"))
json.dump(dict(device="Redrum Drum Computer",front=CF,back=CB),open("tools/checks/redrum-drum-computer.json","w"),indent=0)
print(len(F),len(B))
