import json
def K(l,w,n,s,x,y,r=26,c="high",why=""): return [l,w,n,s,[x,y],[r,r],"K",c,why]
def B(l,w,n,s,x,y,hw=18,hh=14,c="high",why=""): return [l,w,n,s,[x,y],[hw,hh],"B",c,why]
def D(l,w,n,x,y,hw,hh,c="high",why="",s=None): return [l,w,n,s,[x,y],[hw,hh],"D",c,why]
J=lambda l,w,x,y:[l,w,"J",[x,y],[20,20],""]
KT=lambda l,w,x,y:[l,w,"K",[x,y],[20,20],"trim next to CV jack; Remote has no item for it"]
NT="no tooltip in Reason (hovered 2.5 s, nudged); name taken from Remote list, NOT proven by hover"
fr=[B("Bypass/On/Off","3-way device switch","Enabled",4,95,45,14,22),
 D("Patch display","Patch name display","Patch Name",785,40,100,16,"medium","Remote item 'Patch Name'; tooltip shows the patch name"),
 B("(up arrow)","Load previous patch","Select Previous Patch",None,957,32,14,9),B("(down arrow)","Load next patch","Select Next Patch",None,957,50,14,9),
 B("(folder)","Open patch browser","",None,995,40),B("(disk)","Save patch","",None,1033,40),
 B("(triangle)","Fold/unfold device","",None,52,41,8,8,"medium","tiny triangle top-left"),
 D("BASIC PHASING tape","Patch name tape","Device Name",None,1228,45,78,12,"medium","Remote item 'Device Name'; convention from earlier devices, not provable by tooltip") if False else D("BASIC PHASING tape","Patch name tape","Device Name",1228,45,78,12,"medium","Remote item 'Device Name'; convention from earlier devices, not provable by tooltip"),
 B("PHASER","Effect type: Phaser","Type",32,670,112,50,16),B("FLANGER","Effect type: Flanger","Type",None,786,112,50,16),B("FILTER","Effect type: Filter","Type",None,901,112,50,16),
 D("Stereo","Stereo / Dual Mono selector","Stereo Mode",1385,65,45,22,"medium",NT,30),
 K("LFO > Freq","LFO amount to Frequency","LFO Freq Mod",18,206,201),K("MOD > Freq","Modulator (envelope/follower) amount to Frequency","Env Freq Mod",6,206,312),
 K("Frequency","Phaser/flanger frequency","Freq",16,453,252,40),K("Bandwidth","Phaser bandwidth","Bandwidth",1,601,203),K("Feedback","Feedback amount","Feedback",10,601,313),
 D("Stages","Number of phaser stages (up/down)","Phaser Stages",745,250,42,34,"medium","no tooltip; name from Remote list",25),
 B("Polarity","Flip effect polarity","Polarity",26,881,214,34,16),B("Mute Dry","Mute the dry signal","Mute Dry",24,881,294,34,16),
 K("Spread","Stereo spread","Spread",29,1047,203),K("Dry/Wet","Balance dry and effect","DryWet",3,1047,313),K("Volume","Output volume","Volume",33,1171,253,40),
 K("LFO > Volume","LFO amount to Volume","LFO Amp Mod",17,1371,201),K("MOD > Volume","Modulator amount to Volume","Env Amp Mod",5,1371,312),
 B("LFO wave arrows","Pick LFO waveform (up/down)","LFO Wave",22,152,483,24,44,"medium",NT),K("LFO rate","LFO rate (Hz, or note value when synced)","LFO Rate",19,245,490,26),
 B("LFO SYNC","LFO tempo-sync on/off","LFO Sync",20,247,537,26,12,"medium",NT),K("Rate Mod","Modulator amount to LFO rate","Rate Mod",27,337,449,18),
 B("Envelope tab","Modulator type: Envelope","ModType",23,655,403,90,12),B("Audio Follower tab","Modulator type: Audio Follower","ModType",None,855,403,90,12),
 B("PRESET","Envelope preset menu","",None,415,450,36,22),B("EDIT","Envelope edit","",None,415,505,36,22),D("Envelope graph","Envelope shape","",800,490,330,52,"medium","display/editor"),
 B("LOOP","Loop the envelope","Env Loop",7,1204,406,42,12,"medium",NT),K("Env rate","Envelope time (s, or note value when synced)","Env Rate",8,1202,488,26),
 B("Env SYNC","Envelope tempo-sync on/off","BeatSync",2,1202,537,26,12,"low",NT+"; BeatSync vs Env Synced Rate is a guess (the SYNC button is BeatSync, Synced Rate is the same knob when sync is on)"),
 B("AUDIO TRIG OFF","Audio trigger on/off","Trig On",31,1372,444,40,14,"low",NT),D("LFO rate (synced)","LFO rate as a note value when SYNC is on (same spot as the LFO rate knob)","LFO Synced Rate",245,455,40,14,"low","same display as the LFO rate readout; shows only with SYNC on; NOT proven",21),D("Env rate (synced)","Envelope time as a note value when SYNC is on (same spot as the Env rate knob)","Env Synced Rate",1202,440,40,14,"low","same display as the Env time readout; shows only with SYNC on; NOT proven",9),K("Threshold","Audio trigger threshold","",None,1372,492,26,"medium",NT+"; Remote list has no threshold item")]
bk=[["BASIC PHASING tape","Patch name tape (back)","D",[1285,80],[78,12],""],
 KT("Freq CV Amt (trim)","Amount for Freq CV",497,215),["Freq CV In","CV input: Frequency","J",[546,217],[20,20],""],
 KT("Feedback CV Amt (trim)","Amount for Feedback CV",497,268),["Feedback/Reso CV In","CV input: Feedback/Reso","J",[546,268],[20,20],""],
 KT("Spread CV Amt (trim)","Amount for Spread CV",497,320),["Spread CV In","CV input: Spread","J",[546,321],[20,20],""],
 KT("DryWet CV Amt (trim)","Amount for Dry/Wet CV",497,372),["Dry/Wet CV In","CV input: Dry/Wet","J",[546,373],[20,20],""],
 ["Trig Envelope CV In","Trigger input for the envelope","J",[546,423],[20,20],""],
 ["LFO CV Out","LFO CV output","J",[912,217],[20,20],""],["Fol/Env CV Out","Follower/Envelope CV output","J",[912,268],[20,20],""],["Trigger CV Out","Trigger CV output","J",[912,321],[20,20],""],
 J("Audio Input L","Audio input left",579,510),J("Audio Input R","Audio input right",649,510),J("Audio Output L","Audio output left",897,510),J("Audio Output R","Audio output right",968,510),
 ["(routing icon 1)","Routing icon (no tooltip)","D",[1405,90],[14,18],"no tooltip"],["(routing icon 2)","Routing icon (no tooltip)","D",[1405,131],[14,18],"no tooltip"],["(routing icon 3)","Routing icon (no tooltip)","D",[1405,172],[14,18],"no tooltip"]]
base=dict(device="Sweeper",prefix="SWPR",remote_scope="se.propellerheads.Sweeper",date="2026-10-07",out_dir=".")
json.dump(dict(base,slug="sweeper",front_raw="_captures_batchD/sweeper_front_raw.jpg",back_raw="_captures_batchD/sweeper_back_raw.jpg",front=fr,back=bk),open("tools/specs/sweeper.json","w"))
ff=[K("Drive","Filter drive","Filter Drive",11,375,215,30),D("(Drive light)","Drive on light","",375,158,12,12,"medium","no tooltip"),
 K("Resonance","Filter resonance","Reso",28,640,215,30),B("Filter TYPE","Filter type menu (Notch 12 dB shown)","Filter Type",12,770,225,60,24)]
json.dump(dict(base,slug="sweeper-filter-view",front_offsets={"K":100,"B":100,"D":100},front_raw="_captures_batchD/sweeper_filter-view_raw.jpg",back_raw="",front=ff,back=[]),open("tools/specs/sweeper-filter-view.json","w"))
fo=[K("Gain In","Audio follower input gain","Follow Gain",14,467,468,30),K("Attack","Audio follower attack","Follow Attack",13,574,468,30),K("Release","Audio follower release","Follow Release",15,681,468,30),
 D("Follower graph","Follower display","",1125,475,310,60,"medium","display")]
json.dump(dict(base,slug="sweeper-follower-view",front_offsets={"K":200,"B":200,"D":200},front_raw="_captures_batchD/sweeper_follower-view_raw.jpg",back_raw="",front=fo,back=[]),open("tools/specs/sweeper-follower-view.json","w"))
