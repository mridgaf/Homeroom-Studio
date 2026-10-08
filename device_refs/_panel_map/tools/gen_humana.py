import json
# Humana Vocal Ensemble. One front picture, one back picture (same zoom frame: screen=70+px/1.63, 62+py/1.63).
NT="no tooltip in Reason (hovered 1.5 s)"
T=lambda s:'tooltip "%s"'%s
NOSLOT="Remote item exists but is beyond the 48 knob slots of our remotemap (not mapped)"
notes={}; back={}; inback=False
for ln in open("_captures_batchE/humana_notes.txt"):
    ln=ln.rstrip("\n")
    if ln=="BACK:": inback=True; continue
    p=ln.split("|",1)
    if len(p)==2: (back if inback else notes)[p[0]]=p[1]
def c(k,src=notes):
    v=src[k]
    return NT if v.startswith("(no tooltip") else T(v)
P=json.load(open("_captures_batchE/humana_pts.json"))
K=1.63; OX,OY=70,62
rows=[]; chk={}
def f(key,label,what,typ,hw,hh,name=None,slot=None,conf="high",why="",pos=None,ck=None):
    sx,sy=pos or P[key]
    x=round((sx-OX)*K); y=round((sy-OY)*K)
    if name and slot is None and not why: why=NOSLOT
    rows.append([label,what,name,slot,[x,y],[round(hw*K),round(hh*K)],typ,conf,why])
    chk[label]=ck or c(key)
f("fold","(triangle)","Fold/unfold device","B",8,8,conf="medium")
f("patcharrows","(patch arrows)","Previous / next patch","B",8,12,"Select Previous Patch",why="tooltip is for the upper half; lower half = Select Next Patch, not hovered")
f("patchfolder","(patch folder)","Browse patch","B",9,9)
f("patchdisk","(patch disk)","Save patch","B",9,9)
f("patchdisp","Patch display","Patch name display","D",90,12,"Patch Name",None,"medium","tooltip shows the patch name text; Remote item 'Patch Name'; matched by meaning")
f("tape","Patch name tape","Patch name tape","D",40,8,"Device Name",conf="medium",why="Remote item 'Device Name'; tooltip shows the patch name; convention from earlier devices")
f("master","MASTER VOLUME","Master volume","K",14,14,"Master_Volume",32)
f("note","NOTE light","Note-on indicator","D",7,7,conf="medium")
f("rangedisp","RANGE display","Pitch bend range","D",14,8)
f("wheelP","PITCH wheel","Pitch bend wheel","S",8,42,"Pitch Bend",39,"medium","no tooltip; Remote 'Pitch Bend' (slot 39) matched by meaning")
f("wheelM","MOD wheel","Mod wheel","S",8,42,"Mod Wheel",33,"medium","no tooltip; Remote 'Mod Wheel' (slot 33) matched by meaning")
f("mw_sstart","MOD WHEEL to S.START","Mod wheel to sample start","K",14,14)
f("mw_ffreq","MOD WHEEL to F.FREQ","Mod wheel to filter cutoff","K",14,14)
f("mw_level","MOD WHEEL to LEVEL","Mod wheel to amp level","K",14,14,"ModWheel_to_Amp_Level",34)
f("sampledisp","Sample display","Vocal sample picture and syllable buttons","D",75,40,conf="medium")
f("samplemenu","Sample menu","Choose the vocal sample","D",75,8,"Instrument",31,"medium","no tooltip; Remote 'Instrument' (slot 31) matched by meaning; NOT proven")
f("s_start","S.START","Sample start","K",14,14,"SampleStart",46,"medium","tooltip 'Sample Start'; Remote 'SampleStart' (slot 46)")
f("s_oct","OCT","Octave","K",14,14,"Octave",35)
f("s_semi","SEMI","Semitone","K",14,14,"Semitune",47,"medium","tooltip 'Semitone'; Remote 'Semitune' (slot 47)")
f("s_fine","FINE","Fine tune","K",14,14,"Finetune",30)
f("filtlight","FILTER on/off light","Filter on/off","B",8,8,"Filter_On",24)
f("filttype","FILTER type menu (LP)","Filter type","D",30,8,"Filter_Type",28,"medium","no tooltip; Remote 'Filter_Type' (slot 28) matched by meaning")
f("cutoff","CUTOFF","Filter cutoff","K",16,16,"Filter_Cutoff",20,"medium","tooltip 'Filter Cutoff'; Remote 'Filter_Cutoff'")
f("reso","RESO","Filter resonance","K",16,16,"Filter_Reso",26,"medium","tooltip 'Filter Reso'; Remote 'Filter_Reso'")
f("fenv","ENV","Filter envelope amount","K",16,16,"Filter_Env",22,"medium","tooltip 'Filter Env'; Remote 'Filter_Env'")
f("fvel","VEL","Filter velocity","K",14,14,"Filter_Velocity",29,"medium","tooltip 'Filter Velocity'; Remote 'Filter_Velocity'")
f("fkbd","KBD","Filter key follow","K",14,14,"Filter_KeyFollow",23,"medium","tooltip 'Filter Key Follow'; Remote 'Filter_KeyFollow'")
f("fenvA","FILTER A","Filter attack","S",6,30,"Filter_Attack",19,"medium","tooltip 'Filter Attack'; Remote 'Filter_Attack'")
f("fenvD","FILTER D","Filter decay","S",6,30,"Filter_Decay",21,"medium","tooltip 'Filter Decay'; Remote 'Filter_Decay'")
f("fenvS","FILTER S","Filter sustain","S",6,30,"Filter_Sustain",27,"medium","tooltip 'Filter Sustain'; Remote 'Filter_Sustain'")
f("fenvR","FILTER R","Filter release","S",6,30,"Filter_Release",25,"medium","tooltip 'Filter Release'; Remote 'Filter_Release'")
f("ampvel","AMP VEL","Amp velocity","K",14,14,why="tooltip 'Amp Velocity'; no such Remote item")
f("ampA","AMP A","Amp attack","S",6,30,"Amp_Attack",1,"medium","tooltip 'Amp Attack'; Remote 'Amp_Attack'")
f("ampD","AMP D","Amp decay","S",6,30,"Amp_Decay",2,"medium","tooltip 'Amp Decay'; Remote 'Amp_Decay'")
f("ampS","AMP S","Amp sustain","S",6,30,"Amp_Sustain",4,"medium","no tooltip after 2 tries; Remote 'Amp_Sustain' (slot 4) matched by position in the A-D-S-R row")
f("ampR","AMP R","Amp release","S",6,30,"Amp_Release",3,"medium","tooltip 'Amp Release'; Remote 'Amp_Release'")
f("dlylight","DELAY on/off light","Delay on/off","B",8,8,"Delay_On",8,"medium","tooltip 'Delay On'; Remote 'Delay_On'")
f("dlytime","DELAY TIME","Delay time (synced time while SYNC is on)","K",14,14,"Synced_Delay_Time",48,"medium","tooltip 'Synced Delay Time' (SYNC was on); Remote 'Delay_Time' (slot 11) is the unsynced version, same knob")
f("dlyfb","DELAY FEEDBACK","Delay feedback","K",14,14,"Delay_Feedback",7,"medium","tooltip 'Delay Feedback'; Remote 'Delay_Feedback'")
f("dlysync","DELAY SYNC","Delay tempo sync","B",8,8,"Delay_Sync",10,"medium","tooltip 'Delay Sync'; Remote 'Delay_Sync'")
f("dlypp","DELAY PING PONG","Delay ping pong","B",8,8,"Delay_PingPong",9,"medium","tooltip 'Delay Ping Pong'; Remote 'Delay_PingPong'")
f("dlydamp","DELAY DAMP","Delay damp","K",14,14,"Delay_Damp",6,"medium","tooltip 'Delay Damp'; Remote 'Delay_Damp'")
f("dlyamt","DELAY AMOUNT","Delay amount","K",14,14,"Delay_Amount",5,"medium","tooltip 'Delay Amount'; Remote 'Delay_Amount'")
f("revlight","REVERB on/off light","Reverb on/off","B",8,8,"Reverb_On",43,"medium","tooltip 'Reverb On'; Remote 'Reverb_On'")
f("revtime","REVERB TIME","Reverb time","K",14,14,"Reverb_Time",45,"medium","tooltip 'Reverb Time'; Remote 'Reverb_Time'")
f("revpre","REVERB PRE-DELAY","Reverb pre-delay","K",14,14,"Reverb_PreDelay",44,"medium","tooltip 'Reverb Pre Delay'; Remote 'Reverb_PreDelay'")
f("revhi","REVERB HI DAMP","Reverb high damp","K",14,14,"Reverb_HighDamp",41,"medium","tooltip 'Reverb High Damp'; Remote 'Reverb_HighDamp'")
f("revlo","REVERB LO DAMP","Reverb low damp","K",14,14,"Reverb_LowDamp",42,"medium","tooltip 'Reverb Low Damp'; Remote 'Reverb_LowDamp'")
f("revamt","REVERB AMOUNT","Reverb amount","K",14,14,"Reverb_Amount",40,"medium","tooltip 'Reverb Amount'; Remote 'Reverb_Amount'")

NOP="not hovered: Remote item with no matching control on the Humana panel (Humana has a single filter and no oscillators)"
f("dlytime","DELAY TIME (unsynced)","Delay time while SYNC is off","K",14,14,"Delay_Time",11,"medium","same knob as DELAY TIME; Remote 'Delay_Time' is the unsynced version",pos=(778,150),ck="not hovered: same knob, shown in unsynced mode")
for i,(nm,sl) in enumerate((("Filter 1 Frequency",12),("Filter 1 Mode",13),("Filter 1 Resonance",14),("Filter 1 To Filter 2",15),("Filter 2 Frequency",16),("Filter 2 Mode",17),("Filter 2 Resonance",18),("Osc 1 Filter Select",36),("Osc 2 Filter Select",37),("Osc 3 Filter Select",38))):
    f("filttype","(no panel control) "+nm,"Remote item '%s': no matching control on the panel"%nm,"B",5,5,nm,sl,"low","Remote vocabulary item shared with other Reason Studios synths; the Humana panel has no such control; row parked in the FILTER section; NOT proven",pos=(448+i*12,308),ck=NOP)
B=[];CB={}
def b(key,label,what,typ,sx,sy,hw=11,hh=11):
    B.append([label,what,typ,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],""]); CB[label]=c(key,back)
b("gate","Seq Gate In","Gate input (sequencer)","J",245,198)
b("cv","Seq Note In","Note CV input (sequencer)","J",245,235)
b("pb_trim","Pitch Bend CV trim","Amount for pitch bend CV","K",361,196,14,14)
b("pb_jack","Pitch Bend CV In","CV input: pitch bend","J",389,196)
b("mw_trim","Mod Wheel CV trim","Amount for mod wheel CV","K",361,235,14,14)
b("mw_jack","Mod Wheel CV In","CV input: mod wheel","J",389,235)
b("cutoff_trim","Cutoff CV trim","Amount for filter cutoff CV","K",484,226,14,14)
b("cutoff_jack","Cutoff CV In","CV input: filter cutoff","J",513,226)
b("reso_trim","Reso CV trim","Amount for filter resonance CV","K",569,226,14,14)
b("reso_jack","Reso CV In","CV input: filter resonance","J",597,226)
b("level_trim","Level CV trim","Amount for amp level CV","K",653,226,14,14)
b("level_jack","Level CV In","CV input: amp level","J",681,226)
b("outL","Audio Out L/Mono","Audio output, left / mono","J",804,198,14,14)
b("outR","Audio Out R","Audio output, right","J",863,198,14,14)
base=dict(device="Humana",prefix="HUMA",remote_scope="Propellerhead Software / se.propellerheads.Humana",date="2026-10-08",out_dir=".")
json.dump(dict(base,slug="humana",front_raw="_captures_batchE/humana_front_raw.jpg",back_raw="_captures_batchE/humana_back_raw.jpg",front=rows,back=B),open("tools/specs/humana.json","w"))
json.dump(dict(device="Humana",front=chk,back=CB,views={},view_titles={}),open("tools/checks/humana.json","w"),indent=0)
print(len(rows),len(B))
