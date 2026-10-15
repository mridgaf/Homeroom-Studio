import json
# RPSpec Spectrogram (Rob Papen RE). Front: screen=419+px/1.3175, 246+py/1.3175 (zoom [419,246,1219,540]). Back: screen=453+px/1.3176, 248+py/1.3176.
NT="no tooltip in Reason (hovered 1.4 s)"
T=lambda s:'tooltip "%s"'%s
K=1.3175; OX,OY=419,246
rows=[]; chk={}; M="medium"
def f(label,what,typ,hw,hh,ck,pos,conf=M,why=""):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why]); chk[label]=ck
f("(triangle)","Fold/unfold device","B",8,8,"no tooltip (fold arrow); checked by eye",(441,260))
f("RPSPEC 1 tape","Device name tape","D",30,7,NT,(547,275))
f("Mode display (Left/Right)","Analysis mode display (Left/Right shown); label under it reads Mode","D",35,8,NT,(753,275),why="clicking not tried (would change the mode)")
f("BOOST","Boost (input gain of the display)","K",13,13,T("Boost: 0.0 dB"),(852,274),"high")
f("HOLD","Hold amount","K",13,13,T("Hold: 0%"),(895,274),"high")
f("RELEASE","Release amount","K",13,13,T("Release: 0%"),(936,274),"high")
f("FREEZE","Freeze the display","B",8,8,T("Freeze Spectrogram"),(975,274),"high")
f("RPSPEC logo","Logo (no tooltip)","D",60,12,NT,(1059,275))
f("Rob Papen signature","Signature (no tooltip)","D",30,12,NT,(1165,275))
f("View icon 1 (wave)","View selector icon: waveform/spectrum line","B",12,8,NT,(474,333))
f("View icon 2 (bars)","View selector icon: bars","B",12,8,NT,(501,333))
f("View icon 3 (steps)","View selector icon: steps","B",12,8,NT,(523,333))
f("View icon 4 (line)","View selector icon: line","B",12,8,NT,(546,333))
f("Selected Freq readout","Selected frequency readout","D",50,8,NT,(710,333))
f("Max Freq readout","Highest frequency readout","D",50,8,NT,(905,333))
f("Balance slider (-1 .. +1)","Stereo balance indicator bar (-1 left, +1 right)","S",55,8,NT,(1106,333),why="hovered at centre; no tooltip")
f("Spectrum display","Spectrum screen with dB scale (+20..-60) and frequency scale (20Hz..20kHz)","D",380,100,NT,(800,430))
f("Frequency scale","Frequency labels 20Hz..20kHz","D",380,8,NT,(800,313),M)
f("dB scale","dB labels +20..-60","D",14,100,NT,(447,440),M)
B=[];CB={}
BK=1.3176; BX,BY=453,248
def b(label,what,ck,sx,sy,hw=9,hh=9,typ="J"):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=ck
b("Input Left","Audio input, left (cabled)",T("Connected to RE 181 MSC 1: Audio Out Mid")+"; jack's own name not read (right-click menu not opened)",538,490)
b("Input Right","Audio input, right (cabled)",T("Connected to RE 181 MSC 1: Audio Out Side")+"; jack's own name not read",575,490)
b("Output Left","Audio output, left (cabled)",T("Connected to RE 181 MSC 1: Audio In Left")+"; jack's own name not read",1011,490)
b("Output Right","Audio output, right (cabled)",T("Connected to RE 181 MSC 1: Audio In Right")+"; jack's own name not read",1047,490)
b("Power area (drawn)","Power cable socket (no tooltip)",NT,1127,490,16,14,"D")
b("RPSPEC 1 tape (back)","Device name tape on the back",NT+" (hover missed; position by eye)",473,390,8,28,"D")
b("Credits text","Credits text and warning label (printed, not controls)",NT,800,400,330,60,"D")
base=dict(device="RPSpec Spectrogram",prefix="RPSP",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="rpspec",front_raw="_captures_batchE/rpspec_front_raw.jpg",back_raw="_captures_batchE/rpspec_back_raw.jpg",front=rows,back=B),open("tools/specs/rpspec.json","w"))
json.dump(dict(device="RPSpec Spectrogram",front=chk,back=CB,views={},view_titles={}),open("tools/checks/rpspec.json","w"),indent=0)
print(len(rows),len(B))
