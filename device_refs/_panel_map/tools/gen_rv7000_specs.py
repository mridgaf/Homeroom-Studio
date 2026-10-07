import json
def K(l,w,n,s,x,y,r=40,c="high",why=""): return [l,w,n,s,[x,y],[r,r],"K",c,why]
def B(l,w,n,s,x,y,hw=14,hh=14,c="high",why=""): return [l,w,n,s,[x,y],[hw,hh],"B",c,why]
def D(l,w,n,x,y,hw,hh,c="high",why=""): return [l,w,n,None,[x,y],[hw,hh],"D",c,why]
J=lambda l,w,x,y:[l,w,"J",[x,y],[22,22],""]
fr=[B("Bypass/On/Off","3-way device switch","Enabled",8,84,38,14,22),D("(LED column)","Input level meter","Input Peak Meter",86,100,10,32),
 D("ALL PLATE SP... tape","Device name tape","Device Name",293,28,78,12),D("(patch display)","Patch name display","Patch Name",295,60,100,12),
 B("(up arrow)","Load previous patch","Select Previous Patch",None,423,50,14,9),B("(down arrow)","Load next patch","Select Next Patch",None,423,70,14,9),
 B("(folder)","Open patch browser","",None,460,60),B("(disk)","Save patch","",None,497,60),
 B("(triangle)","Fold/unfold device","",None,55,50,8,8,"medium","tiny triangle under the top-left screw"),
 B("Remote Programmer (slot + arrow)","Show/hide the Remote Programmer section (see rv7000-programmer)","",None,215,102,40,18,"medium",""),
 B("EQ Enable","EQ section on/off (light shows on)","EQ On/Off",6,610,53,26,12),B("Gate Enable","Gate section on/off (light shows on)","Gate On/Off",7,610,96,26,12),
 K("Decay","Reverb tail length","Decay",1,888,72),K("HF Damp","High-frequency damping","HF Damp",2,993,72),K("HI EQ","High EQ amount","Hi EQ",3,1095,72),K("Dry - Wet","Balance dry and reverb","Dry/Wet",4,1265,72,42)]
bk=[D("(patch tape)","Device name tape (back)","Device Name",293,35,78,12)]
bk=[["ALL PLATE SP... tape","Device name tape (back)","D",[293,35],[78,12],""],
 ["Decay (trim)","Amount knob for Decay CV","K",[463,75],[18,18],"trim next to CV jack; matched by position"],["Decay (CV in)","CV input for Decay","J",[510,75],[17,17],""],
 ["HF Damp (trim)","Amount knob for HF Damp CV","K",[568,75],[18,18],"trim next to CV jack; matched by position"],["HF Damp (CV in)","CV input for HF Damp","J",[613,75],[17,17],""],
 ["Gate Trig (CV in)","Gate trigger input","J",[685,75],[17,17],""],
 J("Audio Input L","Audio input left",867,75),J("Audio Input R","Audio input right",927,75),J("Audio Output L","Audio output left",1010,75),J("Audio Output R","Audio output right",1070,75)]
json.dump(dict(device="RV7000 Advanced Reverb",slug="rv7000",prefix="RV7K",remote_scope="Propellerheads / RV7000 Advanced Reverb",front_raw="_captures_batchA/rv7000_front_raw.jpg",back_raw="_captures_batchA/rv7000_back_raw.jpg",out_dir=".",date="2026-10-07",front=fr,back=bk),open("tools/specs/rv7000.json","w"))
# Programmer, Reverb edit mode (only view captured so far)
pf=[B("Edit Mode","Cycle the programmer view: Reverb, EQ, Gate","Edit Mode",5,110,236,22,12),
 D("Reverb/EQ/Gate lights","Shows which edit mode is showing","Edit Mode Name",130,185,45,36,"medium","three lights + names"),
 B("(up/down arrows)","Step through patches","",None,146,103,16,22,"low","probably patch up/down like the main panel; confirm by hover"),B("(folder)","Open patch browser","",None,185,103,16,14,"medium",""),B("(waveform button)","Unknown (waveform icon); confirm by hover","",None,222,103,16,14,"low",""),
 D("(display)","Graph + parameter names/values for the current view","",880,135,540,112,"medium","display only")]
for i,(y) in enumerate((45,105,165,225)):
    pf.append(K(f"(left knob {i+1})","Soft knob beside the display","Soft Knob %d"%(i+1),9+i,292,y,18,"low","soft knob numbering (1-4 left, 5-8 right) is a guess; confirm by hover"))
    pf.append(K(f"(right knob {i+5})","Soft knob beside the display","Soft Knob %d"%(i+5),13+i,1442,y,18,"low","soft knob numbering (1-4 left, 5-8 right) is a guess; confirm by hover"))
json.dump(dict(device="RV7000 Advanced Reverb",slug="rv7000-programmer-reverb",prefix="RV7K",front_offsets={"K":4,"B":9,"D":3},remote_scope="Propellerheads / RV7000 Advanced Reverb",front_raw="_captures_batchA/rv7000_programmer-reverb_raw.jpg",back_raw="",out_dir=".",date="2026-10-07",front=pf,back=[]),open("tools/specs/rv7000-programmer-reverb.json","w"))
