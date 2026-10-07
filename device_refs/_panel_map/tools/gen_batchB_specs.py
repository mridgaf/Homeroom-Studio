"""Generates tools/specs/<slug>.json for Batch B devices (positions measured by eye from _captures_batchB pictures)."""
import json,sys
S={}
def F(label,what,name,pos,half,t,conf="high",why="",mode=None):
    r=[label,what,name,None,pos,half,t,conf,why]
    if mode: r.append(mode)
    return r
pb=lambda n,x,y,nm: F(f"Pattern {n}" if nm=="P" else nm,"","Pattern "+str(n) if nm=="P" else nm,[x,y],[17,21],"B")
rowsP=[(1,101,115),(2,138,115),(3,175,115),(4,212,115),(5,101,172),(6,138,172),(7,175,172),(8,212,172)]
mfront=[
 F("MATRIX 2 tape","Device name tape","Device Name",[46,120],[16,52],"D"),
 F("Pattern (switch)","Pattern Enable: turns pattern playback on/off at the next downbeat (light shows on)","Pattern Enable",[115,75],[27,11],"B"),
 F("Mute (light)","Mute light: lit when the Matrix track is muted in the sequencer",None,[237,75],[11,11],"D"),
]
for n,x,y in rowsP:
    mfront.append(F(f"Pattern {n}","Pattern button "+str(n)+" (selects pattern "+str(n)+" in the current bank)","Pattern "+str(n),[x,y],[17,21],"B",mode="in"))
for b,x in zip("ABCD",(101,138,175,212)):
    mfront.append(F(f"Bank {b}","Bank button "+b+" (pick the bank, then click a Pattern button)","Bank "+b,[x,229],[17,21],"B",mode="in"))
mfront+=[
 F("Run","Run: starts/stops this Matrix on its own, without the main sequencer","Run",[265,166],[20,28],"B"),
 F("Keys/Curve switch","Switches the upper pattern window between Keys (note pitch) and Curve (curve CV) editing",None,[327,62],[18,40],"B","medium","no Remote item for this switch in the vocab"),
 F("(Keys/Curve lights)","Lights show whether Keys or Curve is showing",None,[358,62],[10,26],"D","medium","display lights"),
 F("(octave slider 1-5)","5-way slider: picks which of five octaves the note row shows",None,[327,185],[18,50],"S","medium","no Remote item in the vocab",mode="left"),
 F("(octave arrows 1-5)","Arrows 1 to 5 beside the slider show the chosen octave",None,[362,186],[20,46],"D","medium","display",mode="right"),
 F("Tie","Tie: draw longer (tied) gate steps",None,[335,264],[18,11],"B","medium","no Remote item in the vocab"),
 F("(Curve/Keys pattern window)","Upper pattern window: note pitch (Keys) or curve values (Curve); click/drag to draw",None,[897,120],[466,90],"D","medium","edit area, hover-check by eye"),
 F("(Gate pattern window)","Lower pattern window: gate/velocity strips; click/drag to draw",None,[897,246],[466,26],"D","medium","edit area, hover-check by eye"),
 F("Steps (display)","Number of steps in the pattern (1 to 32)",None,[1417,47],[26,18],"D","medium","display",mode="left"),
 F("Steps (up/down arrows)","Raise or lower the number of steps",None,[1455,47],[13,22],"B","medium","no Remote item in the vocab",mode="below"),
 F("RESOLUTION","How fast the pattern plays relative to the tempo, 1/2 to 1/128","Resolution",[1416,168],[36,36],"K","medium","Remote item Resolution; the device has no knob slot in our remotemap"),
 F("Shuffle","Shuffle on/off for this pattern (amount is set by Global Shuffle in the ReGroove Mixer)","Pattern Shuffle",[1413,264],[40,11],"B","medium","Remote item Pattern Shuffle"),
]
mback=[
 ["MATRIX 2 tape","Device name tape (back)","D",[46,118],[16,52],""],
 ["Curve CV","Curve CV output","J",[150,105],[17,17],""],
 ["Note CV","Note CV output (pitch)","J",[239,105],[17,17],""],
 ["Gate CV","Gate CV output (on/off + velocity)","J",[330,105],[17,17],""],
 ["Bipolar/Unipolar switch","Curve CV range: Bipolar (zero in the middle) or Unipolar (zero at the bottom)","B",[430,105],[18,26],"no Remote item in the vocab"],
]
S["matrix"]=("Matrix Pattern Sequencer","MTRX",mfront,mback,"Propellerheads / Matrix Pattern Sequencer")

# ---- Spider Audio
sa_front=[F("SPIDER AUDIO 1 tape","Device name tape","Device Name",[638,28],[108,16],"D")]
_mt=["above","below","above","right"]; _mb=["left","below","below","right"]
for i,x in enumerate((545,577,610,643),1):
    sa_front.append(F(f"Merge input {i} L (light)",f"Lights when audio arrives at merge input {i}, left","Merge Input %d Left Activity"%i,[x,103],[11,11],"D",mode=_mt[i-1]))
    sa_front.append(F(f"Merge input {i} R (light)",f"Lights when audio arrives at merge input {i}, right","Merge Input %d Right Activity"%i,[x,140],[11,11],"D",mode=_mb[i-1]))
sa_front.append(F("Split input L (light)","Lights when audio arrives at the splitter input, left","Split Input Left Activity",[755,103],[11,11],"D"))
sa_front.append(F("Split input R (light)","Lights when audio arrives at the splitter input, right","Split Input Right Activity",[755,140],[11,11],"D"))
sa_back=[["SPIDER AUDIO 1 tape","Device name tape (back)","D",[638,28],[108,16],""]]
for i,x in enumerate((148,204,259,313),1):
    sa_back.append([f"Merge input {i} L","Merger input "+str(i)+", left (L/Mono)","J",[x,82],[19,19],""])
    sa_back.append([f"Merge input {i} R","Merger input "+str(i)+", right","J",[x,142],[19,19],""])
sa_back+=[["Merge out L","Merger output, left","J",[396,82],[19,19],""],["Merge out R","Merger output, right","J",[396,142],[19,19],""],
 ["Split in A (L)","Splitter input, left (A)","J",[563,82],[19,19],""],["Split in B (R)","Splitter input, right (B)","J",[563,142],[19,19],""]]
for i,x in enumerate((645,699,755,810),1):
    sa_back.append([f"Split out {i} A (L)","Splitter output "+str(i)+", left (A)","J",[x,82],[19,19],""])
    sa_back.append([f"Split out {i} B (R)","Splitter output "+str(i)+", right (B)","J",[x,142],[19,19],""])
S["spider-audio"]=("Spider Audio Merger & Splitter","SPDA",sa_front,sa_back,"Propellerheads / Spider Audio Merger & Splitter")

# ---- Spider CV
scv_front=[F("SPIDER CV 1 tape","Device name tape","Device Name",[610,28],[108,17],"D")]
for i,x in enumerate((477,510,543,576),1):
    scv_front.append(F(f"Merge input {i} (light)",f"Lights when a CV signal arrives at merge input {i}","Merge Input %d Activity"%i,[x,142],[11,11],"D",mode=["above","above","above","above"][i-1]))
scv_front.append(F("Split A input (light)","Lights when a CV signal arrives at split A","Split A Input Activity",[684,114],[11,11],"D"))
scv_front.append(F("Split B input (light)","Lights when a CV signal arrives at split B","Split B Input Activity",[786,114],[11,11],"D"))
scv_back=[["SPIDER CV 1 tape","Device name tape (back)","D",[610,28],[108,17],""]]
for i,x in enumerate((75,134,195,257),1):
    scv_back.append([f"Merge trim {i}","Level knob for merge input "+str(i),"K",[x,95],[24,24],"trim above its input jack; matched by position"])
    scv_back.append([f"Merge input {i}","Merger CV input "+str(i),"J",[x if i!=2 else 135,148],[19,19],""])
scv_back+=[["Merge out","Merger CV output","J",[345,148],[19,19],""],
 ["Split A in","Split A input","J",[457,98],[19,19],""],["Split A out 1","Split A output","J",[509,98],[19,19],""],["Split A out 2","Split A output","J",[557,98],[19,19],""],
 ["Split A out 3","Split A output","J",[509,148],[19,19],""],["Split A inverted out","Split A inverted output (Inv)","J",[557,148],[19,19],""],
 ["Split B in","Split B input","J",[665,98],[19,19],""],["Split B out 1","Split B output","J",[717,98],[19,19],""],["Split B out 2","Split B output","J",[767,98],[19,19],""],
 ["Split B out 3","Split B output","J",[717,148],[19,19],""],["Split B inverted out","Split B inverted output (Inv)","J",[767,148],[19,19],""]]
S["spider-cv"]=("Spider CV Merger & Splitter","SPDC",scv_front,scv_back,"Propellerheads / Spider CV Merger & Splitter")

# ---- Pulsar
def PK(l,w,n,x,y,r=28,c="high",why=""): return F(l,w,n,[x,y],[r,r],"K",c,why)
pu_front=[F("PULSAR 1 tape","Device name tape","Device Name",[44,125],[18,58],"D"),
 F("LFO 1 (rate lamp)","Lamp above the Rate knob; blinks at the LFO 1 rate",None,[102,38],[24,24],"D","medium","lamp"),
 PK("LFO 1 RATE","LFO 1 speed (tempo-sync step when Tempo Sync is on)","LFO1 Rate Free",159,125,54,"medium","Remote items LFO1 Rate Free (free) and LFO1 Rate Synced (synced); one knob"),
 F("LFO 1 waveform up","Next LFO 1 waveform","LFO1 Waveform",[278,66],[17,17],"B","medium","Remote item LFO1 Waveform belongs to the selector"),
 F("LFO 1 waveform display","Shows the LFO 1 waveform (click-drag up/down to change)","LFO1 Waveform",[277,125],[35,35],"D","medium","display"),
 F("LFO 1 waveform down","Previous LFO 1 waveform","LFO1 Waveform",[277,180],[17,17],"B","medium","Remote item LFO1 Waveform belongs to the selector"),
 PK("LFO 1 LEVEL","LFO 1 output level","LFO1 Level",388,125,54),
 F("ENV SYNC (LFO 1)","Envelope trigger also restarts LFO 1","LFO1 Env Sync",[100,226],[16,14],"B"),
 F("TEMPO SYNC (LFO 1)","LFO 1 follows the song tempo","LFO1 Tempo Sync",[100,258],[16,14],"B"),
 PK("PHASE (LFO 1)","Where in its cycle LFO 1 starts, 0-360 degrees","LFO1 Phase",268,238),
 PK("SHUFFLE (LFO 1)","Swing between pairs of LFO 1 cycles, 50-75%","LFO1 Shuffle",357,238),
 PK("LAG (LFO 1)","Smooths LFO 1 (lowpass)","LFO1 Lag",440,238),
 PK("RATE (LFO 2 to LFO 1)","How much LFO 2 changes LFO 1 rate (FM)","LFO2 to LFO1 Rate",548,70),
 PK("LEVEL (LFO 2 to LFO 1)","How much LFO 2 changes LFO 1 level (AM)","LFO2 to LFO1 Level",548,158),
 F("SYNC (LFO 1 to LFO 2)","Every new LFO 2 cycle restarts LFO 1","Sync LFO1 to LFO2",[582,243],[13,13],"B"),
 F("LFO 2 (rate lamp)","Lamp above the Rate knob; blinks at the LFO 2 rate",None,[656,40],[24,24],"D","medium","lamp"),
 PK("LFO 2 RATE","LFO 2 speed (tempo-sync step when Tempo Sync is on)","LFO2 Rate Free",712,125,54,"medium","Remote items LFO2 Rate Free (free) and LFO2 Rate Synced (synced); one knob"),
 F("LFO 2 waveform up","Next LFO 2 waveform","LFO2 Waveform",[833,66],[17,17],"B","medium","Remote item LFO2 Waveform belongs to the selector"),
 F("LFO 2 waveform display","Shows the LFO 2 waveform (click-drag up/down to change)","LFO2 Waveform",[833,125],[35,35],"D","medium","display"),
 F("LFO 2 waveform down","Previous LFO 2 waveform","LFO2 Waveform",[833,180],[17,17],"B","medium","Remote item LFO2 Waveform belongs to the selector"),
 PK("LFO 2 LEVEL","LFO 2 output level","LFO2 Level",944,125,54),
 F("ON/OFF (LFO 2)","Turn LFO 2 on or off","LFO2 Enabled",[650,226],[16,14],"B"),
 F("TEMPO SYNC (LFO 2)","LFO 2 follows the song tempo","LFO2 Tempo Sync",[650,258],[16,14],"B"),
 PK("PHASE (LFO 2)","Where in its cycle LFO 2 starts, 0-360 degrees","LFO2 Phase",827,238),
 PK("SHUFFLE (LFO 2)","Swing between pairs of LFO 2 cycles, 50-75%","LFO2 Shuffle",915,238),
 PK("LAG (LFO 2)","Smooths LFO 2 (lowpass)","LFO2 Lag",998,238),
 F("LFO2 TRIG","Every new LFO 2 cycle triggers the envelope","LFO2 Triggers Envelope",[1070,80],[16,14],"B"),
 F("(envelope lamp)","Lamp between LFO2 TRIG and TRIG; lit while the envelope runs",None,[1230,82],[22,22],"D","medium","lamp"),
 F("TRIG","Non-latching button that triggers the envelope","Trig",[1372,75],[30,30],"B"),
 PK("ATTACK","Envelope attack time (0.1 ms to 3 s)","Attack",1178,158),
 PK("RELEASE","Envelope release time (0 ms to 10 s)","Release",1285,158),
 PK("RATE (envelope to LFO 1)","How much the envelope changes LFO 1 rate","LFO1 Env Rate",1103,238,26),
 PK("LEVEL (envelope to LFO 1)","How much the envelope changes LFO 1 level","LFO1 Env Level",1180,238,26),
 PK("RATE (envelope to LFO 2)","How much the envelope changes LFO 2 rate","LFO2 Env Rate",1285,238,26),
 PK("LEVEL (envelope to LFO 2)","How much the envelope changes LFO 2 level","LFO2 Env Level",1363,238,26),
 PK("KBD FOLLOW","How much MIDI notes change the LFO rates (bipolar)","Keyboard Track",1443,142)]
def pj(l,w,x,y,t="J",r=15,why=""): return [l,w,t,[x,y],[r,r],why]
pu_back=[pj("PULSAR 1 tape","Device name tape (back)",92,125,"D",18)]
pu_back[0][4]=[18,55]
for lfo,xs in ((1,((140,176),(226,262),(313,349),(401,437))),(2,((676,714),(766,802),(855,891),(945,983)))):
    for nm,(kx,jx) in zip(("Rate","Phase","Shuffle","Level"),xs):
        pu_back.append(pj(f"LFO {lfo} {nm} (trim)",f"Amount knob for the LFO {lfo} {nm} CV input",kx,62,"K",18,"trim next to its CV jack; matched by position"))
        pu_back.append(pj(f"LFO {lfo} {nm} (CV in)",f"CV input: modulates LFO {lfo} {nm}",jx,62,"J",15))
for lfo,xs,ys in ((1,(212,266,320,374),(210,264,320,374)),(2,(749,804,859,917),(747,803,859,917))):
    for i,(x,y) in enumerate(zip(xs,ys),1):
        inv=" (inverted)" if i>=3 else ""
        pu_back.append(pj(f"LFO {lfo} CV out {i}{inv}",f"LFO {lfo} CV output {i}{inv}",x,176,"J",15))
        pu_back.append(pj(f"LFO {lfo} audio out {i}{inv}",f"LFO {lfo} audio output {i}{inv}",y,236,"J",18))
pu_back+=[pj("LFO 1+2 CV out","Combined LFO 1+2 CV output",553,150,"J",15),pj("LFO 1+2 audio out","Combined LFO 1+2 audio output",553,212,"J",18),
 pj("Envelope Gate In","CV/gate input that triggers the envelope",1143,170,"J",16),pj("Envelope CV Out","Envelope CV output",1312,170,"J",16)]
for _r in pu_back:
    if _r[2]=="K": _r.append("above")
    elif _r[2]=="J" and _r[3][1]==62: _r.append("below")
S["pulsar"]=("Pulsar Dual LFO","PULS",pu_front,pu_back,"se.propellerheads.Pulsar")

# ---- RPG-8
rf=[F("ARP 1 tape","Device name tape","Device Name",[44,205],[16,80],"D"),
 PK("VELOCITY","Fixed note velocity 1-127, or Manual (use played velocity) at the far right","Velocity/Manual",152,113,40,"medium","Remote has Manual Velocity and Velocity/Manual; hover shows which"),
 F("(Manual light)","Light beside MAN.: lit when Velocity is on Manual",None,[197,140],[8,8],"D","medium","light"),
 F("MIDI IN (light)","Lights when MIDI notes arrive",None,[319,76],[9,9],"D","medium","light"),
 F("HOLD","Hold: arpeggio keeps playing after you release the keys","Hold",[319,136],[44,18],"B"),
 F("(octave shift lights -3 to +3)","Seven lights show the octave shift, -3 to +3","Octave Shift",[227,204],[100,10],"D","medium","display; Remote item Octave Shift"),
 F("OCTAVE SHIFT (left arrow)","Shift the arpeggio down one octave","Octave Shift Down",[112,232],[28,12],"B"),
 F("OCTAVE SHIFT (right arrow)","Shift the arpeggio up one octave","Octave Shift Up",[346,232],[28,12],"B"),
 F("ON","Arpeggiator on/off","Arpeggiator Enable",[452,36],[44,18],"B"),
 PK("MODE","Arpeggio direction: Up, Up+Down, Down, Random, Manual","Mode",622,138,50),
 F("4 OCT","Octave range 4","Octave 4",[766,117],[42,11],"B"),F("3 OCT","Octave range 3","Octave 3",[766,144],[42,11],"B"),
 F("2 OCT","Octave range 2","Octave 2",[766,171],[42,11],"B"),F("1 OCT","Octave range 1 (just the played notes)","Octave 1",[766,197],[42,11],"B"),
 F("INSERT 4-2","Insert: adds notes in a 4-2 pattern","Insert 4-2",[885,90],[44,10],"B"),F("INSERT 3-1","Insert: adds notes in a 3-1 pattern","Insert 3-1",[885,117],[44,10],"B"),
 F("INSERT HI","Insert: adds the highest note","Insert High",[885,144],[44,10],"B"),F("INSERT LOW","Insert: adds the lowest note","Insert Low",[885,171],[44,10],"B"),
 F("INSERT OFF","Insert off","Insert Off",[885,197],[44,10],"B"),
 F("SYNC","Rate follows the song tempo","Sync",[447,305],[26,12],"B"),
 F("FREE","Rate runs free (not tied to tempo)",None,[521,305],[26,12],"B","medium","no separate Remote item; Sync covers the pair"),
 F("(rate display)","Shows the rate value, e.g. 1/16","",[483,343],[62,20],"D","medium","display"),
 PK("RATE","Arpeggio speed (note value when Sync is on)","Rate",627,322,52),
 F("(Rate light)","Light by the Rate knob: blinks at the rate",None,[584,396],[7,7],"D","medium","light"),
 PK("GATE LENGTH","Length of each note, 0 to Tie (legato)","Gate Length",757,324,38),
 F("SINGLE NOTE REPEAT","Repeat a single held note","Single Note Repeat",[886,315],[26,13],"B"),
 F("PATTERN","Pattern editor on/off","Pattern Enable",[995,30],[14,14],"B"),
 F("STEPS -","Fewer pattern steps","Pattern Length Down",[1357,31],[26,12],"B"),F("STEPS +","More pattern steps","Pattern Length Up",[1423,31],[26,12],"B")]
for i in range(16):
    rf.append(F(f"Pattern step {i+1}",f"Pattern step {i+1} on/off","Pattern Step %d"%(i+1),[round(996+29.3*i),80],[13,15],"B","medium","step button; hover to confirm numbering"))
rf+=[F("(pattern display)","Shows the notes the arpeggio plays (C-1 to C7)",None,[1215,230],[238,125],"D","medium","display"),
 F("SHUFFLE","Shuffle on/off","Pattern Shuffle",[991,385],[14,14],"B","medium","Remote has Pattern Shuffle and Shuffle; hover shows which")]
for _r in rf:
    if len(_r)==9:
        if _r[0].endswith(" OCT"): _r.append("left")
        elif _r[0].startswith("INSERT"): _r.append("right")
        elif _r[0].startswith("Pattern step"): _r.append("above" if int(_r[0].split()[-1])%2 else "below")
def rj(l,w,x,y): return [l,w,"J",[x,y],[14,14],"","right"]
rb=[["ARP 1 tape","Device name tape (back)","D",[44,205],[16,80],""]]
for l,y,nm in (("Gate Length",128,"Gate Length CV In"),("Velocity",173,"Velocity CV In"),("Rate/Resolution",218,"Rate/Resolution CV In"),("Octave Shift",264,"Octave Shift CV In")):
    rb.append([l+" (trim)","Amount knob for "+nm,"K",[356,y],[16,16],"trim next to its CV jack; matched by position","above"])
    rb.append(rj(nm,"CV input: "+nm,394,y))
rb.append(rj("Start of Arpeggio Trig In","Trigger input: restarts the arpeggio",394,310))
for l,x,y in (("Gate CV Out (velocity)",650,128),("Note CV Out",650,173),("Mod Wheel CV Out",650,218),("Pitch Bend CV Out",650,264),("Aftertouch CV Out",928,128),("Expression CV Out",928,173),("Breath CV Out",928,218),("Start of Arpeggio Trig Out",928,264),("Sustain Pedal Gate Out (pedal down = open)",928,310)):
    rb.append(rj(l,"Output: "+l,x,y))
rb.append(["(CV modulation in use light)","Lit when a CV input is cabled and modulating","D",[393,370],[8,8],"light","below"])
S["rpg-8"]=("RPG-8 Monophonic Arpeggiator","RPG8",rf,rb,"Propellerheads / RPG-8 Monophonic Arpeggiator")

# ---- Line Mixer 6:2 (coords measured on the 1549-wide view, scaled to the 1568-wide picture)
K=1.0123
def X(x): return round(x*K)
lf=[F("LINE MIXER 1 tape","Device name tape","Device Name",[X(1390),32],[70,13],"D")]
for n in range(1,7):
    o=(n-1)*175.5
    lf+=[F(f"Ch {n} AUX",f"Channel {n} aux send amount (to the Aux Send jacks)",f"Channel {n} Aux Send",[X(97+o),40],[20,20],"K"),
     F(f"Ch {n} PAN",f"Channel {n} pan (left to right)",f"Channel {n} Pan",[X(211+o),40],[18,18],"K"),
     F(f"Ch {n} LEVEL",f"Channel {n} volume",f"Channel {n} Level",[X(158+o),60],[28,28],"K"),
     F(f"Ch {n} Mute",f"Channel {n} mute button",f"Channel {n} Mute",[X(86+o),96],[11,10],"B",mode="left"),
     F(f"Ch {n} Solo",f"Channel {n} solo button",f"Channel {n} Solo",[X(110+o),96],[11,10],"B",mode="right"),
     F(f"(Ch {n} meter)",f"Channel {n} level meter",f"Channel {n} Peak Meter",[X(211+o),97],[10,20],"D",mode="above"),
     F(f"Ch {n} name tape",f"Channel {n} name label (type your own name)",f"Channel {n} Name",[X(145+o),127],[68,12],"D",mode="below")]
lf+=[F("AUX RETURN","Level of the signal coming back in at the Aux Return jacks","Aux Return Level",[X(1155),36],[20,20],"K"),
 F("MASTER","Master volume of the mixer","Master Level",[X(1355),90],[26,26],"K"),
 F("(Master meter L)","Master output meter, left","Master Left Peak Meter",[X(1409),95],[8,36],"D",mode="left"),
 F("(Master meter R)","Master output meter, right","Master Right Peak Meter",[X(1440),95],[8,36],"D",mode="right")]
lb=[["LINE MIXER 1 tape","Device name tape (back)","D",[X(1393),32],[80,13],""]]
for n in range(1,7):
    o=(n-1)*174.3
    lb+=[[f"Ch {n} in L",f"Channel {n} audio input, left (L/Mono)","J",[X(118+o),67],[17,17],""],
     [f"Ch {n} in R",f"Channel {n} audio input, right","J",[X(118+o),108],[17,17],""],
     [f"Ch {n} Pan CV trim",f"Amount knob for the Channel {n} Pan CV input","K",[X(208+o),73],[16,16],"no Remote item in the vocab"],
     [f"Ch {n} Pan CV in",f"Channel {n} pan CV input","J",[X(208+o),110],[13,13],""]]
lb+=[["Aux Pre/Post","Aux send taken before (Pre) or after (Post) the channel fader","B",[X(1156),90],[14,24],""],
 ["Aux Send L","Aux send output, left","J",[X(1212),63],[17,17],""],["Aux Send R","Aux send output, right","J",[X(1212),103],[17,17],""],
 ["Aux Return L","Aux return input, left","J",[X(1268),63],[17,17],""],["Aux Return R","Aux return input, right","J",[X(1268),103],[17,17],""],
 ["Master Out L","Master output, left","J",[X(1357),117],[17,17],""],["Master Out R","Master output, right","J",[X(1409),117],[17,17],""]]
S["line-mixer"]=("Line Mixer 6:2","LNMX",lf,lb,"Propellerheads / Line Mixer 6:2")

# ---- Mixer 14:2 (coords from the 1568x575 zoom)
mf=[F("MIXER 1 tape","Device name tape","Device Name",[45,250],[14,80],"D")]
for n in range(1,15):
    o=(n-1)*91.0
    mf+=[F(f"Ch {n} AUX 1",f"Channel {n} aux send 1",f"Channel {n} Aux 1 Send",[round(95+o),52],[17,17],"K",mode="right"),
     F(f"Ch {n} AUX 2",f"Channel {n} aux send 2",f"Channel {n} Aux 2 Send",[round(131+o),83],[17,17],"K",mode="right"),
     F(f"Ch {n} AUX 3",f"Channel {n} aux send 3",f"Channel {n} Aux 3 Send",[round(97+o),117],[17,17],"K",mode="left"),
     F(f"Ch {n} AUX 4",f"Channel {n} aux send 4",f"Channel {n} Aux 4 Send",[round(131+o),150],[17,17],"K",mode="right"),
     F(f"Ch {n} P (aux 4 pre)",f"Channel {n} aux 4 Pre Fader on/off: send 4 is taken before the fader when on",f"Channel {n} Aux 4 Pre Fader On/Off",[round(82+o),152],[10,10],"B",mode="left"),
     F(f"Ch {n} EQ on",f"Channel {n} EQ on/off",f"Channel {n} EQ On/Off",[round(82+o),185],[10,10],"B",mode="above"),
     F(f"Ch {n} TREBLE",f"Channel {n} treble amount",f"Channel {n} Treble Amount",[round(113+o),222],[19,19],"K",mode="right"),
     F(f"Ch {n} BASS",f"Channel {n} bass amount",f"Channel {n} Bass Amount",[round(113+o),278],[19,19],"K",mode="right"),
     F(f"Ch {n} Mute",f"Channel {n} mute",f"Channel {n} Mute",[round(82+o),330],[11,11],"B",mode="above"),
     F(f"Ch {n} Solo",f"Channel {n} solo",f"Channel {n} Solo",[round(121+o),330],[11,11],"B",mode="above"),
     F(f"Ch {n} PAN",f"Channel {n} pan (left to right)",f"Channel {n} Pan",[round(113+o),367],[19,19],"K",mode="right"),
     F(f"Ch {n} fader",f"Channel {n} volume fader",f"Channel {n} Level",[round(111+o),437],[17,30],"S",mode="above"),
     F(f"(Ch {n} meter)",f"Channel {n} level meter",f"Channel {n} Peak Meter",[round(143+o),485],[9,80],"D",mode="below"),
     F(f"Ch {n} name tape",f"Channel {n} name label (type your own name)",f"Channel {n} Name",[round(81+o),485],[11,75],"D",mode="below")]
for i,(kx,ky,tx,ty) in enumerate(((1390,50,1415,88),(1442,125,1415,160),(1390,195,1415,230),(1442,265,1415,297)),1):
    mf+=[F(f"Return {i} level",f"Level of aux return {i}",f"Aux {i} Return Level",[kx,ky],[17,17],"K",mode="above"),
         F(f"Return {i} name tape",f"Name label for aux return {i}",f"Aux {i} Return Name",[tx,ty],[66,12],"D",mode="below")]
mf+=[F("MASTER fader","Master volume fader","Master Level",[1415,437],[17,30],"S",mode="above"),
 F("(Master meter L)","Master output meter, left","Master Left Peak Meter",[1380,485],[8,80],"D",mode="below"),
 F("(Master meter R)","Master output meter, right","Master Right Peak Meter",[1452,485],[8,80],"D",mode="below")]
mb=[["MIXER 1 tape","Device name tape (back)","D",[45,248],[14,78],""]]
for n in range(1,15):
    x=round(132+(n-1)*55.9)
    mb+=[[f"Ch {n} in L",f"Channel {n} audio input, left (L/Mono)","J",[x,97],[17,17],""],
     [f"Ch {n} in R",f"Channel {n} audio input, right","J",[x,147],[17,17],""],
     [f"Ch {n} Level CV in",f"Channel {n} level CV input","J",[x,207],[12,12],""],
     [f"Ch {n} Level CV trim",f"Amount knob for Channel {n} level CV","K",[x,252],[16,16],"no Remote item in the vocab"],
     [f"Ch {n} Pan CV in",f"Channel {n} pan CV input","J",[x,309],[12,12],""],
     [f"Ch {n} Pan CV trim",f"Amount knob for Channel {n} pan CV","K",[x,355],[16,16],"no Remote item in the vocab"]]
for i,x in enumerate((1080,1136,1191,1247),1):
    mb+=[[f"Aux {i} send L",f"Aux {i} send output, left (L/Mono)","J",[x,97],[17,17],""],[f"Aux {i} send R",f"Aux {i} send output, right","J",[x,147],[17,17],""],
     [f"Aux {i} return L",f"Aux {i} return input, left (L/Mono)","J",[x,227],[17,17],""],[f"Aux {i} return R",f"Aux {i} return input, right","J",[x,277],[17,17],""],
     [f"Aux {i} chain in L",f"Chaining Aux {i} send input, left (L/Mono)","J",[x,388],[17,17],""],[f"Aux {i} chain in R",f"Chaining Aux {i} send input, right","J",[x,438],[17,17],""]]
mb+=[["Master out L","Master output, left","J",[1361,97],[17,17],""],["Master out R","Master output, right","J",[1417,97],[17,17],""],
 ["Master Level CV in","Master level CV input","J",[1390,198],[12,12],""],["Master Level CV trim","Amount knob for Master level CV","K",[1390,243],[16,16],"no Remote item in the vocab"],
 ["Chain master L","Chaining master input, left","J",[1361,395],[17,17],""],["Chain master R","Chaining master input, right","J",[1417,395],[17,17],""],
 ["EQ switch (Compatible/Improved)","Picks the EQ type: Compatible (like the old mixer) or Improved","B",[118,422],[10,22],"no Remote item in the vocab"]]
S["mixer-14-2"]=("Mixer 14:2","MX14",mf,mb,"Propellerheads / Mixer 14:2")

# ---- Mix Channel (coords from the 1568x141 zoom, measured directly in picture px, no scaling)
XM=lambda v:v
mcf=[
 F("(fold triangle)","Fold triangle: folds the device up to a thin strip",None,[XM(40),XM(33)],[9,7],"B","medium","no tooltip, no Remote item"),
 F("Mix Channel name","Channel name label (type your own name)","Channel Name",[XM(185),XM(36)],[XM(62),XM(15)],"D","medium","tooltip shows the channel name"),
 F("Show Insert FX","Opens/closes the insert FX slot under the strip (drop an effect device there)",None,[XM(112),XM(115)],[XM(17),XM(11)],"B","medium","no Remote item"),
 F("MUTE","Mutes this channel","Mute",[XM(343),XM(34)],[XM(22),XM(17)],"B","high"),
 F("SOLO","Solos this channel","Solo",[XM(398),XM(34)],[XM(22),XM(17)],"B","high"),
 F("BYPASS","Bypasses the insert FX","Bypass Insert FX",[XM(371),XM(86)],[XM(26),XM(12)],"B","high"),
 F("Level fader","Channel level (horizontal fader)","Level",[XM(680),XM(36)],[XM(34),XM(16)],"S","high",mode="below"),
 F("PAN","Channel pan (left to right)","Pan",[XM(836),XM(36)],[XM(21),XM(21)],"K","high",mode="below"),
 F("SEQ","Shows this channel's sequencer track",None,[XM(913),XM(35)],[XM(18),XM(14)],"B","medium","no Remote item",mode="below"),
 F("MIX","Shows this channel's mixer strip",None,[XM(960),XM(35)],[XM(18),XM(14)],"B","medium","no Remote item",mode="below"),
 F("Spectrum EQ button","Shows this channel in the Spectrum EQ window",None,[XM(1020),XM(35)],[XM(33),XM(17)],"B","medium","no Remote item",mode="below"),
 F("(level meter)","Channel level meter",None,[XM(1237),XM(31)],[XM(172),XM(12)],"D","medium","no tooltip; Remote item unknown for this device"),
 F("AUDIO OUTPUT menu","Pick where the channel's sound goes (Master Section or another bus)",None,[XM(1130),XM(86)],[XM(235),XM(13)],"B","medium","no tooltip; opens a menu, not clicked"),
 F("REC SOURCE","Rec Source: marks this channel as a recording source",None,[XM(1386),XM(120)],[XM(9),XM(9)],"B","medium","no Remote item"),
]
mcb=[
 ["(fold triangle)","Fold triangle (back)","B",[XM(40),XM(33)],[9,7],"no tooltip, no Remote item"],
 ["Mix Channel name","Channel name box (back)","D",[XM(198),XM(35)],[XM(100),XM(18)],"tooltip shows the channel name"],
 ["Show Insert FX","Opens/closes the insert FX slot","B",[XM(125),XM(108)],[XM(17),XM(11)],"no Remote item"],
 ["(output-bus light)","Lit when the channel is used as an output bus (its input is then disabled)","D",[XM(456),XM(79)],[XM(8),XM(8)],"no tooltip"],
 ["Input L","Audio input, left (L/Mono)","J",[XM(498),XM(57)],[XM(17),XM(17)],""],
 ["Input R","Audio input, right","J",[XM(498),XM(100)],[XM(17),XM(17)],""],
 ["Parallel out L","Parallel (pre-insert) output, left","J",[XM(620),XM(57)],[XM(17),XM(17)],""],
 ["Parallel out R","Parallel (pre-insert) output, right","J",[XM(620),XM(100)],[XM(17),XM(17)],""],
 ["Sidechain in L","Sidechain input, left","J",[XM(748),XM(57)],[XM(17),XM(17)],""],
 ["Sidechain in R","Sidechain input, right","J",[XM(748),XM(100)],[XM(17),XM(17)],""],
 ["KEY","Sidechain Key on/off","B",[XM(845),XM(70)],[XM(17),XM(15)],"tooltip Sidechain Key On/Off"],
 ["Gain Reduction CV out","CV output that follows the dynamics gain reduction","J",[XM(900),XM(63)],[XM(12),XM(12)],""],
 ["(insert FX slot)","Slot for an insert effect device","D",[XM(1050),XM(75)],[XM(120),XM(45)],"no tooltip"],
 ["Direct out L","Direct output, left","J",[XM(1228),XM(57)],[XM(17),XM(17)],""],
 ["Direct out R","Direct output, right","J",[XM(1228),XM(100)],[XM(17),XM(17)],""],
 ["(breaks internal mixer routing)","Label: using Direct Out breaks the internal mixer routing","D",[XM(1340),XM(33)],[XM(70),XM(16)],"no tooltip"],
 ["(Audio Output display)","Shows where the channel is routed (Master Section)","D",[XM(1358),XM(105)],[XM(75),XM(12)],"no tooltip"],
]
S["mix-channel"]=("Mix Channel","MXCH",mcf,mcb,"Propellerheads / Mix Channel")

# ---- Combinator outer panel (1568x415 zoom, picture px measured directly, no scaling)
cof=[
 F("(fold triangle)","Fold triangle: folds the Combinator up to a thin strip",None,[41,29],[9,8],"B","medium","no tooltip, no Remote item"),
 F("Bypass/On/Off switch","Bypass / On / Off switch for the whole Combinator","Enabled",[78,29],[11,24],"B","high","tooltip 'Enabled: On'"),
 F("Combinator 1 name tape","Device name label","Device Name",[213,40],[76,13],"D","high","tooltip shows the device name"),
 F("(orange LED)","Small orange light next to the Editor button",None,[333,29],[8,8],"D","low","no tooltip; could be a Remote indicator, not confirmed"),
 F("Editor (Show Programmer)","Opens the Programmer (where the knobs get mapped)",None,[399,29],[40,19],"B","high","tooltip 'Show Programmer'"),
 F("Devices (Show Devices)","Shows the devices inside the Combinator",None,[485,29],[40,19],"B","high","tooltip 'Show Devices'"),
 F("(green meters)","Small green meters left of the patch name",None,[567,32],[19,21],"D","low","no tooltip; could be Audio In/Out indicators, not confirmed"),
 F("Patch name display","Shows the loaded patch name","Patch Name",[860,33],[190,19],"D","medium","tooltip shows the patch name"),
 F("Patch up/down arrows","Select previous (top half) / next (bottom half) patch","Select Next Patch",[1155,31],[20,24],"B","medium","two halves: top = Select previous patch, bottom = Select next patch (both tooltips seen)"),
 F("Browse patch (folder)","Opens the patch browser",None,[1193,31],[17,17],"B","high","tooltip 'Browse patch'"),
 F("Save patch (disk)","Saves the patch",None,[1230,31],[17,17],"B","high","tooltip 'Save patch'"),
 F("PITCH wheel","Pitch bend wheel, passed to all instruments inside","Pitch Bend",[117,162],[15,70],"S","high","tooltip 'Pitch Bend: 0'",mode="right"),
 F("MOD wheel","Mod wheel, passed to all instruments inside","Mod Wheel",[183,162],[15,70],"S","high","tooltip 'Mod Wheel: 0'",mode="right"),
 F("Control 1","Rotary 1: virtual knob, does nothing until mapped in the Programmer","Rotary 1",[523,122],[42,42],"K","high","tooltip 'Control 1: 64'"),
 F("Control 2","Rotary 2: virtual knob","Rotary 2",[695,122],[42,42],"K","high","tooltip 'Control 2: 64'"),
 F("Control 3","Rotary 3: virtual knob","Rotary 3",[867,122],[42,42],"K","high","tooltip 'Control 3: 64'"),
 F("Control 4","Rotary 4: virtual knob","Rotary 4",[1038,122],[42,42],"K","high","tooltip 'Control 4: 64'"),
 F("Switch 1","Button 1: virtual switch","Button 1",[522,214],[26,14],"B","high","tooltip 'Switch 1'"),
 F("Switch 2","Button 2: virtual switch","Button 2",[695,214],[26,14],"B","high","tooltip 'Switch 2'"),
 F("Switch 3","Button 3: virtual switch","Button 3",[867,214],[26,14],"B","high","tooltip 'Switch 3'"),
 F("Switch 4","Button 4: virtual switch","Button 4",[1038,214],[26,14],"B","high","tooltip 'Switch 4'"),
 F("Mixer fold arrow","Unfolds the built-in Combinator mixer (not mapped here)",None,[43,323],[8,9],"B","medium","no tooltip; the unfolded mixer is a separate view, not mapped"),
 F("(mixer channel lights 1-16)","Lights showing which of the 8 stereo inputs of the Combinator mixer are in use",None,[783,312],[245,14],"D","medium","no tooltip"),
]
_sl={"Rotary 1":1,"Rotary 2":2,"Rotary 3":3,"Rotary 4":4,"Button 1":5,"Button 2":6,"Button 3":7,"Button 4":8}
for _r in cof:
    if _r[2] in _sl: _r[3]=_sl[_r[2]]
cob=[
 ["(fold triangle)","Fold triangle (back)","B",[41,30],[9,8],"no tooltip, no Remote item"],
 ["Editor (Show Programmer)","Opens the Programmer","B",[107,63],[40,19],"tooltip 'Show Programmer'"],
 ["Devices (Show Devices)","Shows the devices inside","B",[107,104],[40,19],"tooltip 'Show Devices'"],
 ["Gate In","Sequencer Control: Mono Gate Input","J",[216,62],[15,15],""],
 ["CV In","Sequencer Control: Mono CV Input","J",[216,102],[15,15],""],
 ["Control CV In 1 trim","Amount knob for Control CV In 1","K",[437,66],[19,19],"no Remote item in the vocab"],
 ["Control CV In 3 trim","Amount knob for Control CV In 3","K",[437,104],[19,19],"no Remote item in the vocab"],
 ["Control CV In 1","Control CV input 1","J",[485,66],[14,14],""],
 ["Control CV In 3","Control CV input 3","J",[485,104],[14,14],""],
 ["Control 1 selector","Picks which Combinator control the top-left CV input drives (shows Control 1)","D",[597,64],[82,14],"no tooltip; dropdown not opened"],
 ["Control 3 selector","Picks which control the lower-left CV input drives (shows Control 3)","D",[597,104],[82,14],"no tooltip; dropdown not opened"],
 ["Control CV In 2 trim","Amount knob for Control CV In 2","K",[715,66],[19,19],"no Remote item in the vocab"],
 ["Control CV In 4 trim","Amount knob for Control CV In 4","K",[715,104],[19,19],"no Remote item in the vocab"],
 ["Control CV In 2","Control CV input 2","J",[762,66],[14,14],""],
 ["Control CV In 4","Control CV input 4","J",[762,104],[14,14],""],
 ["Control 2 selector","Picks which control the top-right CV input drives (shows Control 2)","D",[875,64],[82,14],"no tooltip; dropdown not opened"],
 ["Control 4 selector","Picks which control the lower-right CV input drives (shows Control 4)","D",[875,104],[82,14],"no tooltip; dropdown not opened"],
 ["Combinator 1 name tape","Device name label (back)","D",[1117,66],[80,14],""],
 ["(name strip)","Dark strip under the name tape","D",[1115,104],[100,8],"no tooltip"] ,
 ["Input L","Combi Input Left","J",[1266,104],[17,17],""],
 ["Input R","Combi Input Right","J",[1322,104],[17,17],""],
 ["Output L","Combi Output Left","J",[1415,104],[17,17],""],
 ["Output R","Combi Output Right","J",[1473,104],[17,17],""],
 ["Mixer fold arrow","Unfolds the built-in Combinator mixer (back)","B",[43,323],[8,9],"not mapped here"],
]
S["combinator"]=("Combinator","COMB",cof,cob,"Propellerheads / Combinator")
only=sys.argv[1:] 
for slug,(dev,pre,fr,bk,scope) in S.items():
    if only and slug not in only: continue
    json.dump(dict(device=dev,slug=slug,prefix=pre,remote_scope=scope,front_raw=f"_captures_batchB/{slug}_front_raw.jpg",
      back_raw=f"_captures_batchB/{slug}_back_raw.jpg",out_dir=".",date="2026-10-07",front=fr,back=bk),open(f"tools/specs/{slug}.json","w"),indent=0)
    print("spec",slug)
