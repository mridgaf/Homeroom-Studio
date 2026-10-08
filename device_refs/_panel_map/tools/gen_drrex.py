import json
# Dr. Octo Rex (Remote name: Dr.REX Loop Player). Programmer section open. Notes: _captures_batchE/drrex_hover_notes.txt
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists in Reason but is beyond the slots of our remotemap (not mapped)"
notes={}
for ln in open("_captures_batchE/drrex_hover_notes.txt"):
    p=ln.rstrip("\n").split("|")
    if len(p)==3 and p[0]=="B": notes["B:"+p[1]]=p[2]
    elif len(p)==2: notes[p[0]]=p[1]
def c(k):
    v=notes[k]
    return NT if v.startswith("(no tooltip") else T(v)
F=[];CF={};B=[];CB={}
def f(label,what,name,slot,x,y,hw,hh,typ,k,conf="high",why="",mode=None,chk=None):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]+([mode] if mode else [])); CF[label]=chk or c(k)
def b(label,what,typ,x,y,hw,hh,k,why="",mode=None):
    B.append([label,what,typ,[x,y],[hw,hh],why,mode]); CB[label]=c("B:"+k)
# pts are screen px; picture = zoom of screen region x 72..1028, y 222..655 (scale 1.64)
S=lambda x,y:(round((x-72)*1.64),round((y-222)*1.64))
def sf(label,what,name,slot,sx,sy,hw,hh,typ,k,conf="high",why="",mode=None,chk=None):
    x,y=S(sx,sy); f(label,what,name,slot,x,y,round(hw*1.64),round(hh*1.64),typ,k,conf,why,mode,chk)
import json as _j
P={a:(x,y) for a,x,y in _j.load(open("_captures_batchE/drrex_pts.json"))}
def pf(label,what,name,slot,key,hw,hh,typ,conf="high",why="",mode=None,chk=None,nk=None):
    x,y=P[key]; f(label,what,name,slot,x,y,hw,hh,typ,nk or key,conf,why,mode,chk)
pf("(triangle top)","Fold/unfold device",None,None,"fold1",8,8,"B","medium")
pf("PITCH BEND wheel","Pitch bend wheel","Pitch Bend",None,"wheelP",12,60,"S",why="Remote item 'Pitch Bend'; no knob slot")
pf("MOD WHEEL","Modulation wheel","Mod Wheel",None,"wheelM",12,60,"S",why="Remote item 'Mod Wheel'; no knob slot")
pf("ACOUSTIC DR tape","Patch name tape","Device Name",None,"tape",44,16,"D","medium","Remote item 'Device Name'; convention from earlier devices")
pf("Patch display","Patch name display","Patch Name",None,"patchdisp",150,14,"D","medium","Remote item 'Patch Name'; display gave no tooltip; NOT proven")
pf("(patch up arrow)","Load previous patch","Select Previous Patch",None,"patchup",12,9,"B")
pf("(patch down arrow)","Load next patch","Select Next Patch",None,"patchdown",12,9,"B")
pf("(patch folder)","Open patch browser",None,None,"patchfolder",13,12,"B")
pf("(patch disk)","Save patch",None,None,"patchdisk",13,12,"B")
pf("NOTES TO SLOT knob","Notes to slot (MIDI notes pick the loop slot)","Notes to Slot",11,"notes2slot",20,20,"K",chk=NT+" (the lights beside the loop buttons show 'Notes to Slot')",why="slot 11")
for n in range(1,9):
    pf(f"LOOP BUTTON {n}",f"Play loop slot {n}",f"Select Loop {n}",n,f"loopbtn{n}",30,12,"B",chk=NT,mode="in")
    pf(f"LOOP {n} light",f"Notes-to-slot light, slot {n}",None,None,f"looplight{n}",6,6,"D",nk=f"looplight{n}",mode="left")
    pf(f"LOOP {n} name",f"Loop file name, slot {n}",None,None,f"loopname{n}",42,8,"D",chk=NT,mode="below")
pf("TRIG NEXT LOOP: BAR","Switch loops at the next bar","Trigger Next Setting",12,"trigBAR",8,8,"B",chk=NT+"; Remote 'Trigger Next Setting' covers BAR / BEAT / 1/16",why="slot 12 steps BAR/BEAT/1-16",mode="below")
pf("TRIG NEXT LOOP: BEAT","Switch loops at the next beat",None,None,"trigBEAT",8,8,"B",chk=NT,mode="below")
pf("TRIG NEXT LOOP: 1/16","Switch loops at the next 1/16",None,None,"trig16",8,8,"B",chk=NT,mode="below")
pf("ENABLE LOOP PLAYBACK","Loop playback on/off","Enable Loop Playback",14,"enable",9,9,"B")
pf("MUTE light","Mute light",None,None,"mutelight",5,5,"D",chk=NT)
pf("RUN","Run / stop loop playback","Run",13,"RUN",24,12,"B",chk=NT+"; Remote item 'Run' matched by label, NOT proven")
pf("GLOBAL TRANSPOSE display","Global transpose (semitones)","Transpose",16,"gtrans",26,15,"D",chk=T("Transpose: 0")+" (seen when hovering the arrows)",why="tooltip text 'Transpose: 0'")
pf("(global transpose arrows)","Global transpose up / down",None,None,"gtransarrow",9,16,"B",chk=T("Transpose: 0")+" seen on the display's lower edge; arrows themselves unproven",conf="medium")
pf("VOLUME","Master volume","Master Level",None,"VOLUME",28,28,"K",why="Remote item 'Master Level'; no knob slot in our remotemap")
pf("(triangle programmer)","Fold/unfold Programmer",None,None,"fold2",8,8,"B","medium")
pf("FOLLOW LOOP PLAYBACK","Programmer follows the playing loop","Follow Loop Playback",15,"follow",9,9,"B",nk="follow")
pf("SELECT SLICE BY MIDI","Pick slice by MIDI note",None,None,"slicemidi",9,9,"B",nk="slicemidi")
pf("(loop arrows)","Previous / next loop file",None,None,"selarrows",14,16,"B",chk=T("Select previous loop")+" (upper half; lower half not hovered)")
pf("(loop folder)","Browse loops",None,None,"selfolder",13,12,"B",nk="selfolder")
for n in range(1,9): pf(f"SELECT SLOT {n}",f"Select loop slot {n} in the Programmer","Selected Loop Slot",9 if n==1 else None,f"selbtn{n}",14,10,"B",conf="medium",why="Remote 'Selected Loop Slot' steps through 1-8 (slot 9); all 8 buttons show this tooltip",mode="in")
pf("SELECT SLOT (editor, slot 10)","Remote item 'Selected Loop in Editor': probably the same 8 slot buttons or the loop-file arrows; NOT proven which","Selected Loop in Editor",10,"selbtn1",14,10,"B",conf="low",why="Remote item 'Selected Loop in Editor' has a knob slot (10) but no hover proved which control it is; placed on slot button 1 as a stand-in",chk="not separately hovered: tooltip on these buttons reads 'Selected Loop Slot'; which control 'Selected Loop in Editor' drives was not proven",mode="above")
pf("COPY LOOP TO TRACK","Copy the loop to a sequencer track",None,None,"copyloop",26,10,"B")
pf("LOOP TRANSPOSE","Transpose of the selected loop","Loop Transpose",17,"looptrans",18,18,"K",nk="looptrans")
pf("LOOP LEVEL","Level of the selected loop","Loop Level",26,"looplevel",20,20,"K",nk="looplevel")
pf("File name display","Loop file name",None,None,"dispfile",120,12,"D",nk="dispfile")
pf("Loop info display","Tempo and length of the loop",None,None,"dispinfo",120,12,"D",nk="dispinfo")
pf("Keyboard strip","Shows which MIDI keys play which slice",None,None,"keyboard",125,18,"D",nk="keyboard")
pf("Waveform display","Loop waveform with slices",None,None,"wave",210,50,"D",nk="wave")
for key,lab in zip(["SLICE","PITCH","PAN","LEVEL","DECAY","REV","FFREQ","ALT","OUTPUT"],["SLICE","PITCH","PAN","LEVEL","DECAY","REV","F.FREQ","ALT","OUTPUT"]):
    pf(f"SLICE {lab} knob",f"Slice {lab.lower()} (edits the selected slice)",None,None,"k_"+key,16,16,"K",nk="k_"+key)
pf("OSC PITCH: ENV.A","Osc pitch envelope amount","Osc Env Amount",20,"oscENVA",15,15,"K",nk="oscENVA")
pf("OSC PITCH: OCT","Osc octave","Osc Octave",18,"oscOCT",15,15,"K",nk="oscOCT")
pf("OSC PITCH: FINE","Osc fine tune","Osc Fine Tune",19,"oscFINE",15,15,"K",nk="oscFINE")
pf("MOD.WHEEL: F.FREQ","Mod wheel to filter frequency","Filter Freq Mod Wheel Amount",None,"mwFFREQ",15,15,"K",nk="mwFFREQ",why=NOSLOT)
pf("MOD.WHEEL: F.RES","Mod wheel to filter resonance","Filter Res Mod Wheel Amount",None,"mwFRES",15,15,"K",nk="mwFRES",why=NOSLOT)
pf("MOD.WHEEL: F.DECAY","Mod wheel to filter decay","Filter Decay Mod Wheel Amount",None,"mwFDECAY",15,15,"K",nk="mwFDECAY",why=NOSLOT)
pf("VELOCITY: F.ENV","Velocity to filter envelope amount","Filter Env Vel Amount",36,"velFENV",15,15,"K",nk="velFENV")
pf("VELOCITY: F.DECAY","Velocity to filter decay","Filter Decay Vel Amount",None,"velFDECAY",15,15,"K",nk="velFDECAY",why=NOSLOT)
pf("VELOCITY: AMP","Velocity to amp level","Amp Vel Amount",25,"velAMP",15,15,"K",nk="velAMP")
pf("SLICE EDIT MODE","Slice edit mode button",None,None,"sliceedit",18,10,"B",nk="sliceedit")
pf("PITCH BEND RANGE","Pitch bend range","Pitch Bend Range",None,"pbrange",26,15,"D",nk="pbrange",why=NOSLOT)
pf("POLYPHONY","Number of voices","Polyphony",None,"poly",26,15,"D",nk="poly",why=NOSLOT)
pf("FILTER ON","Filter on/off","Filter On/Off",27,"filtON",9,9,"B",nk="filtON")
for k,lab in (("NOTCH","Notch"),("HP12","HP 12"),("BP12","BP 12"),("LP12","LP 12"),("LP24","LP 24")):
    pf(f"FILTER MODE light {lab}",f"Filter mode light: {lab}",None,None,"fm_"+k,6,6,"D",nk="fm_"+k,mode="left")
pf("FILTER MODE button","Step through filter modes","Filter Mode",30,"filtMODE",10,10,"B",nk="filtMODE")
pf("FILTER FREQ slider","Filter frequency","Filter Freq",28,"filtFREQ",9,40,"S",nk="filtFREQ")
pf("FILTER RES slider","Filter resonance","Filter Res",29,"filtRES",9,40,"S",nk="filtRES")
pf("FILTER ENV AMOUNT slider","Filter envelope amount","Filter Env Amount",31,"fenvAMT",8,40,"S",nk="fenvAMT")
pf("FILTER ENV A slider","Filter envelope attack","Filter Env Attack",32,"fenvA",8,40,"S",nk="fenvA")
pf("FILTER ENV D slider","Filter envelope decay","Filter Env Decay",33,"fenvD",8,40,"S",nk="fenvD")
pf("FILTER ENV S slider","Filter envelope sustain","Filter Env Sustain",34,"fenvS",8,40,"S",nk="fenvS")
pf("FILTER ENV R slider","Filter envelope release","Filter Env Release",35,"fenvR",8,40,"S",nk="fenvR")
pf("LFO SYNC","LFO tempo sync","LFO Sync Enable",41,"lfoSYNC",9,9,"B",nk="lfoSYNC")
for n in range(1,7): pf(f"LFO wave light {n}",f"LFO waveform light {n}",None,None,f"wavelight{n}",6,6,"D",nk=f"wavelight{n}",mode="left")
pf("LFO WAVEF. button","Step through LFO waveforms","LFO1 Wave",39,"WAVEF",14,10,"B",nk="WAVEF")
pf("LFO RATE","LFO rate","LFO1 Rate",37,"lfoRATE",16,16,"K",nk="lfoRATE")
pf("LFO AMOUNT","LFO amount","LFO1 Amount",38,"lfoAMT",16,16,"K",nk="lfoAMT")
for k,lab in (("OSC","OSC"),("FILTER","FILTER"),("PAN","PAN")): pf(f"LFO DEST light {lab}",f"LFO destination light: {lab}",None,None,"dest"+k,6,6,"D",nk="dest"+k,mode="right")
pf("LFO DEST. button","Step through LFO destinations","LFO1 Dest",40,"DEST",14,10,"B",nk="DEST")
pf("AMP ENV A slider","Amp envelope attack","Amp Env Attack",21,"aenvA",8,40,"S",nk="aenvA")
pf("AMP ENV D slider","Amp envelope decay","Amp Env Decay",22,"aenvD",8,40,"S",nk="aenvD")
pf("AMP ENV S slider","Amp envelope sustain","Amp Env Sustain",23,"aenvS",8,40,"S",nk="aenvS")
pf("AMP ENV R slider","Amp envelope release","Amp Env Release",24,"aenvR",8,40,"S",nk="aenvR")
# back (picture 1557 x 242): positions in picture px
Q={a:(x,y) for a,x,y in json.load(open("_captures_batchE/drrex_back_pts.json"))}
names={"mv":"Amp Level (master volume)","mw":"Mod Wheel","pw":"Pitch Wheel","fc":"Filter cutoff","fr":"Filter resonance","op":"Osc pitch"}
for k,nm in names.items():
    x,y=Q[k+"K"]; b(f"{nm} CV trim",f"Amount for {nm} CV","K",x,y,14,14,k+"K","trim next to CV jack; no Remote item")
    x,y=Q[k+"J"]; b(f"{nm} CV In",f"CV input: {nm}","J",x,y,13,13,k+"J")
for k,(lab,wh) in {"modV1":("Filter Env Mod Out","CV output: filter envelope (voice 1)"),"modLFO":("LFO Mod Out","CV output: LFO"),"gateOut":("Slice Gate Out","Gate output: slices"),"gateAmp":("Amp Env Gate In","Gate input: amp envelope"),"gateFilt":("Filter Env Gate In","Gate input: filter envelope")}.items():
    x,y=Q[k]; b(lab,wh,"J",x,y,13,13,k)
for n in range(1,9):
    x,y=Q[f"slice{n}"]; b(f"Slice Out {n}",f"Separate audio output for slice {n}","J",x,y,16,16,f"slice{n}")
x,y=Q["mainL"]; b("Main Out L","Main output, left","J",x,y,16,16,"mainL")
x,y=Q["mainR"]; b("Main Out R","Main output, right","J",x,y,16,16,"mainR")
x,y=Q["hq"]; b("HIGH QUALITY INTERPOLATION","High quality interpolation on/off","B",x,y,10,10,"hq","Remote item 'High Quality Interpolation'")
x,y=Q["lowbw"]; b("LOW BANDWIDTH","Low bandwidth on/off","B",x,y,10,10,"lowbw","Remote item 'Low Bandwidth On/Off'")
x,y=Q["tape"]; b("ACOUSTIC DR tape (back)","Patch name tape (back)","D",x,y,42,14,"tape")
base=dict(device="Dr.REX Loop Player",prefix="DREX",remote_scope="Propellerheads / Dr.REX Loop Player",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="dr-rex-loop-player",front_raw="_captures_batchE/drrex_front_raw.jpg",back_raw="_captures_batchE/drrex_back_raw.jpg",front=F,back=B),open("tools/specs/dr-rex-loop-player.json","w"))
json.dump(dict(device="Dr.REX Loop Player",front=CF,back=CB),open("tools/checks/dr-rex-loop-player.json","w"),indent=0)
print(len(F),len(B))
