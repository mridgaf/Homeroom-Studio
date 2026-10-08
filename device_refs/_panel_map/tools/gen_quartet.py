import json
NT="no tooltip in Reason (hovered 1.3 s, approached from 5 px away)"
T=lambda s:'tooltip "%s"'%s
def mk():
    return [],{}
F,CF=mk();B,CB=mk()
def f(label,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    F.append([label,what,name,slot,[x,y],[hw,hh],typ,conf,why]); CF[label]=chk
def b(label,what,typ,x,y,hw,hh,chk,why=""):
    B.append([label,what,typ,[x,y],[hw,hh],why]); CB[label]=chk
f("Bypass/On/Off","3-way device switch","Enabled",14,95,40,12,22,"B",T("Enabled: On"))
f("(triangle)","Fold/unfold device",None,None,48,38,8,8,"B",NT,"medium")
f("(lights)","Level lights",None,None,95,92,12,16,"D",NT)
f("Patch display","Patch name display","Patch Name",None,668,37,100,16,"D",T("Big BBD Ensemble"),"medium","Remote item 'Patch Name'; tooltip shows the patch name")
f("(up arrow)","Load previous patch","Select Previous Patch",None,957,30,14,9,"B",T("Select previous patch"))
f("(down arrow)","Load next patch","Select Next Patch",None,957,48,14,9,"B",T("Select next patch"))
f("(folder)","Open patch browser",None,None,995,37,14,14,"B",T("Browse patch"))
f("(disk)","Save patch",None,None,1032,37,14,14,"B",T("Save patch"))
f("BIG BBD ENSE tape","Patch name tape","Device Name",None,1218,40,80,12,"D",T("Big BBD Ensemble")+" (patch name; 'Device Name' item not provable here)","medium","Remote item 'Device Name'; convention from earlier devices")
f("Stereo","Stereo / Dual Mono selector","Stereo Mode",28,1385,62,45,22,"D",NT,"medium","name from Remote list; NOT proven by tooltip")
f("CHORUS","Ensemble mode: Chorus","Effect Select",13,610,121,48,16,"B",T("Effect Select")+"; clicked, view changed, set back to BBD")
f("BBD","Ensemble mode: BBD","Effect Select",None,728,121,48,16,"B",T("Effect Select"))
f("FFT","Ensemble mode: FFT","Effect Select",None,843,121,48,16,"B",T("Effect Select")+"; clicked, view changed, set back to BBD")
f("GRAIN","Ensemble mode: Grain","Effect Select",None,960,121,48,16,"B",T("Effect Select")+"; clicked, view changed, set back to BBD")
for lab,name,slot,x,tip in (("BBD Delay","BBD Delay",1,381,"BBD Delay: 7.23 ms"),("BBD Mod Depth","BBD Depth",2,547,"BBD Depth: 53.5 %"),("BBD Mod Rate","BBD Rate",5,704,"BBD Rate: 1.53 Hz"),("BBD Noise Mod","BBD Noise",4,861,"BBD Noise: 0.0 %"),("BBD Width","BBD Width",6,1018,"BBD Width: 89.5 %"),("BBD Dry/Wet","BBD DryWet",3,1178,"BBD DryWet: 100.0 %")):
    f(lab,lab,name,slot,x,210,40,40,"K",T(tip))
# back
b("(triangle) back","Fold/unfold device","D",52,38,8,8,NT)
b("BIG BBD ENSE tape (back)","Patch name tape (back)","D",1280,42,80,12,T("Big BBD Ensemble"))
for i,y in enumerate((50,95,138)): b(f"(routing icon {i+1})","Routing icon","D",1400,y,14,18,NT)
for lab,x,xj,tt,tj in (("Mod Depth",795,843,"Depth CV Amt: 100.0 %","Depth CV Input"),("Width",935,983,"Width CV Amt: 100.0 %","Width CV Input"),("DryWet",1055,1105,"DryWet CV Amt: 100.0 %","DryWet CV Input")):
    b(f"{lab} CV trim",f"Amount for {lab} CV","K",x,105,20,20,T(tt),"trim next to CV jack; Remote has no item for it")
    b(f"{lab} CV In",f"CV input: {lab}","J",xj,107,18,18,T(tj))
b("Audio In L","Audio input left","J",577,220,20,20,T("Connected to Basic Pulverisation: Left Out...")+" (cut off); own jack name NOT read yet")
b("Audio In R","Audio input right","J",647,220,20,20,T("Connected to Basic Pulverisation: Right O...")+" (cut off); own jack name NOT read yet")
b("Audio Out L","Audio output left","J",895,220,20,20,T("Connected to British Drive 3: Main In Left")+"; this jack's own name NOT read yet")
b("Audio Out R","Audio output right","J",965,220,20,20,T("Connected to British Drive 3: Main In Right")+"; this jack's own name NOT read yet")
base=dict(device="Quartet",prefix="QRTT",remote_scope="se.propellerheads.Quartet",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="quartet",front_raw="_captures_batchD/quartet_front_raw.jpg",back_raw="_captures_batchD/quartet_back_raw.jpg",front=F,back=B),open("tools/specs/quartet.json","w"))
views={}
# Chorus view
vf=[];vc={}
def g(lab,what,name,slot,x,y,hw,hh,typ,chk,conf="high",why=""):
    vf.append([lab,what,name,slot,[x,y],[hw,hh],typ,conf,why]); vc[lab]=chk
for lab,name,slot,x,tip in (("Chorus Delay","Chorus Delay",7,395,"Chorus Delay: 5.08 ms"),("Chorus Mod Depth","Chorus Depth",8,560,"Chorus Depth: 50.0 %"),("Chorus Mod Rate","Chorus Rate",11,730,"Chorus Rate: 0.71 Hz"),("Chorus Feedback","Chorus Feedback",10,895,"Chorus Feedback: 0.0 %"),("Chorus Width","Chorus Width",12,1063,"Chorus Width: 100.0 %"),("Chorus Dry/Wet","Chorus DryWet",9,1222,"Chorus DryWet: 100.0 %")):
    g(lab,lab,name,slot,x,218,38,38,"K",T(tip))
json.dump(dict(base,slug="quartet-chorus-view",front_offsets={"K":100,"B":100,"D":100},front_raw="_captures_batchD/quartet_chorus-view_raw.jpg",back_raw="",front=vf,back=[]),open("tools/specs/quartet--chorus.json","w")); views["chorus"]=vc
vf=[];vc={}
g("FFT Size","FFT size slider (1 to 4)","FFT Size",18,402,228,38,12,"S",T("FFT Size: 3"))
g("FFT Mod Depth","FFT mod depth","FFT Depth",15,565,218,38,38,"K",T("FFT Depth: 50.0 %"))
g("Frequency Range start","Frequency range start handle","FFT Start",19,667,220,14,24,"S",NT+" (handle)","medium","name from Remote list; NOT proven by tooltip")
g("Frequency Range end","Frequency range end handle","FFT End",17,958,220,14,24,"S",NT+" (handle)","medium","name from Remote list; NOT proven by tooltip")
g("Frequency Range display","Frequency range display",None,None,810,220,150,24,"D",NT,"medium","display only")
g("FFT Width","FFT width","FFT Width",20,1062,218,38,38,"K",T("FFT Width: 100.0 %"))
g("FFT Dry/Wet","FFT dry/wet","FFT DryWet",16,1220,218,38,38,"K",T("FFT DryWet: 100.0 %"))
json.dump(dict(base,slug="quartet-fft-view",front_offsets={"K":200,"B":200,"D":200,"S":200},front_raw="_captures_batchD/quartet_fft-view_raw.jpg",back_raw="",front=vf,back=[]),open("tools/specs/quartet--fft.json","w")); views["fft"]=vc
vf=[];vc={}
g("Phase RND","Grain random phase on/off","Grain Phase",25,287,228,16,14,"B",T("Grain Random Phase")+" (Remote name is 'Grain Phase')")
g("Grain Size","Grain size slider","Grain Size",26,432,228,14,14,"S",T("Grain Size: 50.0 %"))
g("Grain Mod Depth","Grain mod depth slider","Grain Depth",22,580,228,14,14,"S",T("Grain Depth: 40.0 %"))
g("Grain Jitter","Grain jitter slider","Grain Jitter",24,750,228,14,14,"S",T("Grain Jitter: 50.0 %"))
g("Grain Density","Grain density slider","Grain Density",21,920,228,14,14,"S",T("Grain Density: 60.0 %"))
g("Grain Width","Grain width","Grain Width",27,1062,218,38,38,"K",T("Grain Width: 100.0 %"))
g("Grain Dry/Wet","Grain dry/wet","Grain DryWet",23,1220,218,38,38,"K",T("Grain DryWet: 100.0 %"))
json.dump(dict(base,slug="quartet-grain-view",front_offsets={"K":300,"B":300,"D":300,"S":300},front_raw="_captures_batchD/quartet_grain-view_raw.jpg",back_raw="",front=vf,back=[]),open("tools/specs/quartet--grain.json","w")); views["grain"]=vc
json.dump(dict(device="Quartet",front=CF,back=CB,views=views,view_titles=dict(chorus="Chorus mode (picture quartet-chorus-view_front_labeled.png)",fft="FFT mode (picture quartet-fft-view_front_labeled.png)",grain="Grain mode (picture quartet-grain-view_front_labeled.png)")),open("tools/checks/quartet.json","w"),indent=0)
print(len(F),len(B))
