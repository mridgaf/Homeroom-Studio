import json
# Malstrom Graintable Synthesizer. One front picture (whole panel fits), one back picture.
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists but is beyond the 48 knob slots of our remotemap (not mapped)"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/malstrom_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
P=json.load(open("_captures_batchE/malstrom_pts.json"))
class View:
    def __init__(s,ox,oy,k): s.ox,s.oy,s.k=ox,oy,k; s.rows=[]; s.chk={}
    def f(s,key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",chk=None,pos=None):
        sx,sy=pos or P[key]
        x=round((sx-s.ox)*s.k); y=round((sy-s.oy)*s.k)
        if name and slot is None and not why: why=NOSLOT
        s.rows.append([label,what,name,slot,[x,y],[round(hw*s.k),round(hh*s.k)],typ,conf,why])
        s.chk[label]=chk or c(key)
V=View(70,62,1.628); f=V.f
f("fold","(triangle)","Fold/unfold device","B",8,8,conf="medium")
f("patchdisp","Patch display","Patch name display","D",60,12,conf="medium")
f("patcharrows","(patch arrows)","Previous / next patch","B",8,12,"Select Previous Patch",why="tooltip is for the upper half; lower half = Select Next Patch, not hovered")
f("patchfolder","(patch folder)","Browse patch","B",9,9)
f("patchdisk","(patch disk)","Save patch","B",9,9)
f("tape","Patch name tape","Patch name tape (vertical, left edge)","D",8,40,"Device Name",conf="medium",why="Remote item 'Device Name'; convention from earlier devices; NOT hovered",pos=(97,215),chk="not hovered")
# Modulator A
f("modAlight","MOD A on/off light","Modulator A on/off","B",6,6,why="no such Remote item")
f("modAdisp","MOD A curve display","Modulator A curve","D",22,18,"Modulator A Curve",43,"medium","tooltip 'Modulator A Curve'; Remote 'Modulator A Curve' (slot 43); display is also the curve selector")
f("modAarrows","(MOD A curve arrows)","Modulator A curve prev/next","B",8,12,conf="medium")
f("modA1shot","MOD A 1-SHOT","Modulator A one shot","B",14,7)
f("modAsync","MOD A SYNC","Modulator A tempo sync","B",14,7)
f("modArate","MOD A RATE","Modulator A rate","K",14,14,"Modulator A Rate",42)
f("modApitch","MOD A PITCH","Modulator A amount to pitch","K",14,14,"Modulator A To Pitch",44)
f("modAindex","MOD A INDEX","Modulator A amount to index","K",14,14)
f("modAshift","MOD A SHIFT","Modulator A amount to shift","K",14,14)
f("modAswitch","MOD A A/B switch","Modulator A target (osc A / osc B)","B",8,14)
# Modulator B
f("modBlight","MOD B on/off light","Modulator B on/off","B",6,6)
f("modBdisp","MOD B curve display","Modulator B curve","D",22,18)
f("modBarrows","(MOD B curve arrows)","Modulator B curve prev/next","B",8,12,conf="medium")
f("modB1shot","MOD B 1-SHOT","Modulator B one shot","B",14,7)
f("modBsync","MOD B SYNC","Modulator B tempo sync","B",14,7)
f("modBrate","MOD B RATE","Modulator B rate","K",14,14,"Modulator B Rate",45)
f("modBmotion","MOD B MOTION","Modulator B amount to motion","K",14,14)
f("modBvol","MOD B VOL","Modulator B amount to level","K",14,14)
f("modBfilter","MOD B FILTER","Modulator B amount to filter","K",14,14,"Modulator B To Filter",46,"medium","tooltip 'Modulator B To Filter'; Remote 'Modulator B To Filter' (slot 46)")
f("modBmodA","MOD B MOD:A","Modulator B amount to modulator A","K",14,14)
f("modBswitch","MOD B A/B switch","Modulator B target (osc A / osc B)","B",8,14)
# Filter env
f("fenvA","FILTER ENV A","Filter envelope attack","S",6,30,"Filter Env Attack",34)
f("fenvD","FILTER ENV D","Filter envelope decay","S",6,30,"Filter Env Decay",35,"medium","no tooltip after retries; matched by position in the A-D-S-R row")
f("fenvS","FILTER ENV S","Filter envelope sustain","S",6,30,"Filter Env Sustain",36,"medium","no tooltip after retries; matched by position in the A-D-S-R row")
f("fenvR","FILTER ENV R","Filter envelope release","S",6,30,"Filter Env Release",37)
f("fenvinv","FILTER ENV INV","Filter envelope invert","B",12,7)
f("fenvamt","FILTER ENV AMT","Filter envelope amount","K",14,14,"Filter Env Amount",38)
# Left block
f("polydisp","POLYPHONY display","Number of voices","D",14,10)
f("polyarrows","(polyphony arrows)","Voices down/up","B",7,12,conf="medium")
f("legato","LEGATO","Legato on/off","B",14,8)
f("noteon","NOTE ON light","Note-on indicator","D",5,5,conf="medium")
f("porta","PORTAMENTO","Portamento time","K",14,14,"Portamento",47)
f("vel_lvlA","VELOCITY lvl:A","Velocity to level A","K",14,14)
f("vel_lvlB","VELOCITY lvl:B","Velocity to level B","K",14,14)
f("vel_fenv","VELOCITY f.env","Velocity to filter envelope","K",14,14)
f("vel_atk","VELOCITY atk","Velocity to attack","K",14,14)
f("vel_shift","VELOCITY shift","Velocity to shift","K",14,14)
f("vel_mod","VELOCITY mod","Velocity to modulation","K",14,14)
f("velswitch","VELOCITY A/B switch","Velocity target (osc A / osc B)","B",8,14)
f("rangedisp","RANGE display","Pitch bend range","D",14,10)
f("rangearrows","(range arrows)","Pitch bend range down/up","B",7,12,conf="medium")
f("wheelP","PITCH wheel","Pitch bend wheel","S",8,42,"Pitch Bend",None,"high","tooltip '(Pitch Bend)'; Remote item, not on a knob slot")
f("wheelM","MOD wheel","Mod wheel","S",8,42,"Mod Wheel",None,"high","tooltip '(Mod Wheel)'; Remote item, not on a knob slot")
f("mw_index","MOD WHEEL index","Mod wheel to index","K",14,14)
f("mw_shift","MOD WHEEL shift","Mod wheel to shift","K",14,14)
f("mw_filter","MOD WHEEL filter","Mod wheel to filter","K",14,14)
f("mw_mod","MOD WHEEL mod","Mod wheel to modulation","K",14,14)
f("mwswitch","MOD WHEEL A/B switch","Mod wheel target (osc A / osc B)","B",8,14)
# Oscillators
for X,n0 in (("A",1),("B",13)):
    p="osc"+X
    f(p+"light","OSC %s on/off light"%X,"Oscillator %s on/off"%X,"B",6,6,"Oscillator %s On/Off"%X,n0,pos=P["oscAlight" if X=="A" else "oscBlight"],chk=c("oscAlight" if X=="A" else "oscBlight"))
    f(p+"disp","OSC %s wavetable display"%X,"Oscillator %s graintable name"%X,"D",60,12,conf="medium")
    f(p+"arrows","(OSC %s table arrows)"%X,"Oscillator %s graintable prev/next"%X,"B",8,14,conf="medium")
    f(p+"motion","OSC %s MOTION"%X,"Oscillator %s motion"%X,"K",14,14,"Oscillator %s Motion"%X,n0+2)
    f(p+"index","OSC %s INDEX slider"%X,"Oscillator %s index"%X,"S",70,7,"Oscillator %s Index"%X,n0+1,conf="medium",why="tooltip 'Oscillator %s Index'; position is the horizontal slider next to MOTION"%X,pos=(P[p+"index"][0]+0,P[p+"index"][1]),chk=c(p+"index"))
    f(p+"shift","OSC %s SHIFT"%X,"Oscillator %s shift"%X,"K",14,14,"Oscillator %s Shift"%X,n0+3)
    f(p+"oct","OSC %s OCTAVE"%X,"Oscillator %s octave"%X,"K",14,14,"Oscillator %s Octave"%X,n0+4)
    f(p+"semi","OSC %s SEMI"%X,"Oscillator %s semitone"%X,"K",14,14,"Oscillator %s Semi"%X,n0+5)
    f(p+"cent","OSC %s CENT"%X,"Oscillator %s cent"%X,"K",14,14,"Oscillator %s Cent"%X,n0+6)
    for lab,key,nm,off in (("A","atk","Attack",8),("D","dec","Decay",9),("S","sus","Sustain",10),("R","rel","Release",11)):
        f(p+key,"OSC %s %s"%(X,lab),"Oscillator %s envelope %s"%(X,nm.lower()),"S",6,30,"Oscillator %s %s"%(X,nm),n0+off)
    f(p+"vol","OSC %s VOL"%X,"Oscillator %s level"%X,"S",6,30,"Oscillator %s Gain"%X,n0+7,"medium","tooltip 'Oscillator %s Gain'; Remote 'Oscillator %s Gain' (slot %d)"%(X,X,n0+7))
f("oscAroute","OSC A to SHAPER","Route oscillator A to shaper","B",8,8)
f("oscBroute1","OSC A to FILTER B","Route oscillator A to filter B","B",8,8)
f("oscBroute2","OSC B to FILTER B","Route oscillator B to filter B","B",8,8)
# Shaper
f("shapelight","SHAPER on/off light","Shaper on/off","B",6,6,"Shaper On/Off",39)
for k,l in (("sine","sine"),("sat","saturate"),("clip","clip"),("quant","quant"),("noise","noise")):
    f("shape_"+k,"SHAPER type: "+l,"Shaper type "+l,"B",6,6,chk=NT)
f("shapemode","SHAPER mode","Shaper mode (steps the type)","B",14,8,"Shaper Mode",40)
f("shapeamt","SHAPER AMT","Shaper amount","K",14,14,"Shaper Amount",41)
# Filter A (LED rows re-placed from the picture; first-pass points were off)
f("filtAlight","FILTER A on/off light","Filter A on/off","B",6,6,"Filter A On/Off",25)
for i,(k,l) in enumerate((("lp12","lp 12"),("bp12","bp 12"),("combp","comb +"),("combm","comb -"),("am","am"))):
    f("fA_"+k,"FILTER A mode: "+l,"Filter A mode "+l,"B",6,6,pos=(849,198+i*13),chk=NT)
f("fAmode","FILTER A mode","Filter A mode button","B",14,8,"Filter A Mode",26)
f("fAenv","FILTER A ENV","Filter A envelope on/off","B",14,7,"Filter A Env",29)
f("fAkbd","FILTER A KBD","Filter A keyboard tracking on/off","B",14,7)
f("fAres","FILTER A RES","Filter A resonance","K",14,14,"Filter A Resonance",28)
f("fAfreq","FILTER A FREQ","Filter A frequency","K",22,22,"Filter A Freq",27)
# Filter B
f("filtBlight","FILTER B on/off light","Filter B on/off","B",6,6,"Filter B On/Off",30)
f("fBroute","FILTER B to SHAPER","Route filter B to shaper","B",8,8)
for i,(k,l) in enumerate((("lp12","lp 12"),("bp12","bp 12"),("combp","comb +"),("combm","comb -"),("am","am"))):
    f("fB_lp12","FILTER B mode: "+l,"Filter B mode "+l,"B",6,6,pos=(736,312+i*13),chk=NT)
f("fBmode","FILTER B mode","Filter B mode button","B",14,8,"Filter B Mode",31)
f("fBenv","FILTER B ENV","Filter B envelope on/off","B",14,7)
f("fBkbd","FILTER B KBD","Filter B keyboard tracking on/off","B",14,7)
f("fBres","FILTER B RES","Filter B resonance","K",14,14,"Filter B Resonance",33)
f("fBfreq","FILTER B FREQ","Filter B frequency","K",22,22,"Filter B Freq",32)
f("spread","SPREAD","Stereo spread amount","K",14,14)
f("volume","VOLUME","Master level","K",14,14,"Master Level",48)
f("meter","Level meter","Output level meter","D",6,22,pos=(902,363),chk=NT)

# auto-name: a hovered tooltip that equals a Remote item (case-insensitive) becomes the row's reason_name (no slot)
import re as _re
def _walk(o):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from _walk(v)
    elif isinstance(o,list):
        for v in o: yield from _walk(v)
    elif isinstance(o,str): yield o
_v=json.load(open("../../docs/reason/remote-vocab.json"))
def _find(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if "Malstrom" in str(k) and isinstance(v,(dict,list)): return v
            r=_find(v)
            if r is not None: return r
    elif isinstance(o,list):
        for v in o:
            r=_find(v)
            if r is not None: return r
VOC={s.lower():s for s in _walk(_find(_v))}
for r in V.rows:
    if r[2] is None:
        m=_re.match(r'tooltip "(.*)"$',V.chk[r[0]])
        if m and m.group(1).lower() in VOC:
            r[2]=VOC[m.group(1).lower()]; r[3]=None
            if not r[8]: r[8]=NOSLOT
# --- back (picture px; screen = 60+px/1.616, 62+py/1.616; pts are picture px read from the saved picture)
B=[];CB={}
def b(key,label,what,typ,px,py,hw=14,hh=14,why=""):
    B.append([label,what,typ,[px,py],[hw,hh],why]); CB[label]=c(key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",302,120)
b("cv","Seq CV In","Note CV input (sequencer)","J",302,180)
b("ampenv","Amp Env Gate In","Gate input for the amp envelope","J",302,296)
b("filterenv","Filter Env Gate In","Gate input for the filter envelope","J",302,355)
for key,lab,y in (("pitch","Pitch",118),("filter","Filter",169),("index","Index",220),("shift","Shift",271),("level","Level",322),("modamt","Mod Amount",373)):
    b(key+"_jack" if key!="modamt" else "modamt_jack",lab+" Mod In","Modulation input: "+lab.lower(),"J",480,y)
    b(key+"_trim" if key!="modamt" else "modamt_trim",lab+" Mod trim","Amount for "+lab.lower()+" modulation input","K",533,y+0)
b("modwheel_jack","Mod Wheel Mod In","Modulation input: mod wheel","J",480,425)
b("modwheel_trim","Mod Wheel Mod trim","Amount for mod wheel modulation input","K",533,425)
b("pwheel_jack","Pitch Wheel Mod In","Modulation input: pitch wheel","J",480,476)
b("pwheel_trim","Pitch Wheel Mod trim","Amount for pitch wheel modulation input","K",533,476)
b("modA_out","Mod A Out","Control output: modulator A","J",660,117)
b("modB_out","Mod B Out","Control output: modulator B","J",660,168)
b("fenv_out","Filter Env Out","Control output: filter envelope","J",660,218)
b("left","Main Out L (Filter A)","Audio output left (filter A)","J",895,125,16,16)
b("right","Main Out R (Filter B)","Audio output right (filter B)","J",895,175,16,16)
b("oscA_out","Osc A Out","Oscillator A audio output","J",895,303,16,16)
b("oscB_out","Osc B Out","Oscillator B audio output","J",895,352,16,16)
b("shaper_in","Shaper/Filter A In","Audio input to shaper / filter A","J",1190,125,16,16)
b("filterB_in","Filter B In","Audio input to filter B","J",1190,175,16,16)
base=dict(device="Malstrom Graintable Synthesizer",prefix="MALS",remote_scope="Propellerheads / Malstrom Graintable Synthesizer",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="malstrom",front_raw="_captures_batchE/malstrom_front_raw.jpg",back_raw="_captures_batchE/malstrom_back_raw.jpg",front=V.rows,back=B),open("tools/specs/malstrom.json","w"))
json.dump(dict(device="Malstrom Graintable Synthesizer",front=V.chk,back=CB,views={},view_titles={}),open("tools/checks/malstrom.json","w"),indent=0)
print(len(V.rows),len(B))
