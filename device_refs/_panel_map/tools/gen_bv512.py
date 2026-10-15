import json
# BV512 Digital Vocoder. Front and back same frame: screen = 420+px/1.3138, 394+py/1.3138.
# No Scope block for BV512 in our remotemap -> no knob slots / CC; names come from remote-vocab.json 'BV512 Digital Vocoder' items (hover names noted per row).
NT="no tooltip in Reason (hovered 1.4 s)"
T=lambda s:'tooltip "%s"'%s
notes={}; back={}; inback=False
for ln in open("_captures_batchE/bv512_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
K=1.3138; OX,OY=420,394
rows=[]; chk={}
M="medium"
NOSCOPE="our remotemap has no Scope block for BV512 (no knob slot / CC); name is a Remote item from remote-vocab.json"
def f(key,label,what,typ,hw,hh,name=None,conf="high",why="",pos=None):
    sx,sy=pos
    if name and not why: why=NOSCOPE
    rows.append([label,what,name,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf=M,pos=(436,404))
f("switch","BYPASS / ON / OFF switch","3-way device switch","B",12,12,"Enabled",pos=(484,414))
f("bandcount","BAND COUNT knob (FFT / 32 / 16 / 8 / 4 band)","Number of vocoder bands","K",17,17,"Band Count",pos=(659,436))
f("vocoeq","VOCODER / EQUALIZER knob","Vocoder or equalizer mode","K",17,17,"Vocoder/Equalizer",why="tooltip is 'Vocoder/Equalizer'; "+NOSCOPE,pos=(659,487))
f("metC","C meter","Carrier level meter","D",5,35,"Source Peak Meter",conf="low",why="name picked by label (C = carrier); NOT proven. "+NOSCOPE,pos=(551,470))
f("metM","M meter","Modulator level meter","D",5,35,"Modulator Peak Meter",conf="low",why="name picked by label (M = modulator); NOT proven. "+NOSCOPE,pos=(566,470))
f("moddisp","MODULATION LEVELS display","Modulation levels display (top half of the screen)","D",125,22,conf=M,pos=(838,428))
for i in range(1,17):
    f("band%d"%i,"BAND %d LEVEL slider"%i,"Frequency band level adjust, band %d (hover the handle)"%i,"S",5,15,"Band Level %d"%i,why="tooltip is 'Band %d Level' (Remote name is 'Band Level %d'); slider: hover the handle; "%(i,i)+NOSCOPE,pos=(753+13.04*(i-1),494))
f("hold","HOLD","Hold button","B",11,11,"Hold",pos=(1011,423))
f("attack","ATTACK","Attack","K",15,15,"Attack",pos=(1074,433))
f("decay","DECAY","Decay","K",15,15,"Decay",pos=(1124,433))
f("led","(light above SHIFT)","Small red light above SHIFT (purpose not verified)","D",5,5,conf="low",pos=(1012,466))
f("shift","SHIFT","Formant shift","K",15,15,"Shift",pos=(1012,493))
f("hfemph","HF EMPH","High-frequency emphasis","K",15,15,"HF Emphasis",pos=(1074,493))
f("drywet","DRY/WET","Dry/wet mix","K",15,15,"Dry/Wet",pos=(1124,493))
f("tapef","VOCODER 1 tape","Device name tape","D",9,38,"Device Name",conf=M,why="Remote item 'Device Name'; tooltip shows the rack name; "+NOSCOPE,pos=(441,466))
B=[];CB={}
def b(key,label,what,typ,sx,sy,hw=10,hh=10):
    B.append([label,what,typ,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],""]); CB[label]=c(key,back)
for i in range(16):
    x=517.4+i*(802.9-517.4)/15
    b("bo%d"%(i+1),"Band %d CV Out"%(i+1),"CV output: band %d level"%(i+1),"J",x,440,8,8)
for i in range(16):
    x=517.4+i*(802.9-517.4)/15
    b("bi%d"%(i+1),"Band %d CV In"%(i+1),"CV input: band %d level"%(i+1),"J",x,469.4,8,8)
b("shiftjack","Shift CV In","CV input: shift","J",868,428)
b("shifttrim","Shift CV trim","Amount for shift CV","K",867,469,13,13)
b("carL","Carrier In Left","Carrier audio input, left","J",912,434)
b("carR","Carrier In Right","Carrier audio input, right","J",956,431)
b("hold","Hold In","Hold input","J",1027,428)
b("mod","Modulator In","Modulator audio input","J",1027,469,13,13)
b("outL","Audio Out Left","Audio output, left","J",913,508)
b("outR","Audio Out Right","Audio output, right","J",956,508)
b("fold","(triangle, back)","Fold/unfold device","B",443,417,8,8)
b("tape","VOCODER 1 tape (back)","Device name tape","D",441,466,9,38)
b("icon1","(icon, back top)","Small icon at the top left of the back (purpose not verified)","D",469,431,8,10)
b("icon2","(icon, back lower)","Small icon at the left of the back (purpose not verified)","D",469,449,8,10)
base=dict(device="BV512 Digital Vocoder",prefix="BV51",remote_scope="none in our remotemap; names from remote-vocab.json 'BV512 Digital Vocoder'",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="bv512",front_raw="_captures_batchE/bv512_front_raw.jpg",back_raw="_captures_batchE/bv512_back_raw.jpg",front=rows,back=B),open("tools/specs/bv512.json","w"))
json.dump(dict(device="BV512 Digital Vocoder",front=chk,back=CB,views={},view_titles={}),open("tools/checks/bv512.json","w"),indent=0)
print(len(rows),len(B))
