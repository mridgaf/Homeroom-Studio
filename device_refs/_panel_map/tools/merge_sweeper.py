import json
NT="no tooltip in Reason (hovered 1.5-2.5 s)"
T=lambda s:'tooltip "%s"'%s
front={"Bypass/On/Off":T("Enabled: On"),"Patch display":T("Basic Phasing"),"(up arrow)":T("Select previous patch"),"(down arrow)":T("Select next patch"),
"(folder)":T("Browse patch"),"(disk)":T("Save patch"),"(triangle)":NT,"BASIC PHASING tape":T("Basic Phasing")+" (tooltip is the patch name; 'Device Name' item not provable here)",
"PHASER":T("Effect Type")+"; clicked, view changed, set back to Phaser","FLANGER":T("Effect Type")+"; clicked, view changed, set back","FILTER":T("Effect Type")+"; clicked, view changed, set back",
"Stereo":NT,"LFO > Freq":T("LFO Freq Mod: 84.1 %"),"MOD > Freq":T("Env Freq Mod: 0.0 %"),"Frequency":T("Freq: 798.2 Hz"),"Bandwidth":T("Bandwidth: 79.5 %"),"Feedback":T("Feedback: 83.9 %"),
"Stages":NT,"Polarity":T("Polarity"),"Mute Dry":T("Mute Dry"),"Spread":T("Spread: 20.5 %"),"Dry/Wet":T("Dry-Wet: 100.0 %")+" (hover spells Dry-Wet; Remote name is DryWet)","Volume":T("Volume: -6.4 dB"),
"LFO > Volume":T("LFO Amp Mod: 0.0 %"),"MOD > Volume":T("Env Amp Mod: 0.0 %"),"LFO wave arrows":NT,"LFO rate":T("LFO Rate: 15.0 %"),"LFO SYNC":NT,"Rate Mod":T("Rate Mod: 0.0 %"),
"Envelope tab":T("Modulator Type")+"; clicked the other tab and back","Audio Follower tab":T("Modulator Type")+"; clicked, view changed, set back","PRESET":NT,"EDIT":NT,"Envelope graph":NT,"LOOP":NT,
"Env rate":T("Env Rate: 50.4 %"),"Env SYNC":NT,"AUDIO TRIG OFF":NT,"Threshold":NT,"LFO rate (synced)":"not hovered: readout under the LFO rate knob (SYNC is off; the synced note value is not showing); name NOT proven","Env rate (synced)":"not hovered: readout under the Env rate knob (SYNC off); name NOT proven"}
filt={"Drive":T("Filter Drive: 29.9 %"),"(Drive light)":NT,"Resonance":T("Reso: 78.0 %"),"Filter TYPE":T("Filter Type: Ladder LP 24dB")+" (while the panel display read 'Notch 12 dB': recorded as seen)"}
fol={"Gain In":T("Follow Gain: 0.00 dB"),"Attack":T("Follow Attack: 11 ms"),"Release":T("Follow Release: 110 ms"),"Follower graph":NT}
back={"BASIC PHASING tape":T("Basic Phasing"),"Freq CV Amt (trim)":T("Freq CV Amt: 100.0 %"),"Freq CV In":T("Freq CV Input"),"Feedback CV Amt (trim)":T("Feedback CV Amt: 100.0 %"),
"Feedback/Reso CV In":T("Feedback CV Input"),"Spread CV Amt (trim)":T("Spread CV Amt: 100.0 %"),"Spread CV In":T("Spread CV Input"),"DryWet CV Amt (trim)":T("DryWet CV Amt: 100.0 %"),
"Dry/Wet CV In":T("DryWet CV Input"),"Trig Envelope CV In":T("Trig CV In"),"LFO CV Out":T("LFO CV Output"),"Fol/Env CV Out":T("Env CV Output"),"Trigger CV Out":T("Trig CV Output"),
"Audio Input L":'cabled: tooltip "Connected to Default Synchronous: Le(ft...)" cut off; this jack\'s own name NOT read yet',"Audio Input R":'cabled: tooltip "Connected to Default Synchronous: Rig(ht...)" cut off; own name NOT read yet',
"Audio Output L":'cabled: tooltip "Connected to Smooth Bass: Main Out L(...)" cut off; own name NOT read yet',"Audio Output R":'cabled: tooltip "Connected to Smooth Bass: Main Out R(...)" cut off; own name NOT read yet',
"(routing icon 1)":NT,"(routing icon 2)":NT,"(routing icon 3)":NT}
# note: Audio Input L/R hovered at x=421,464 gave "Smooth Bass" and Output gave "Default Synchronous" in that order (L-in,R-in -> Smooth Bass; L-out,R-out -> Synchronous)
back["Audio Input L"]='cabled: tooltip "Connected to Smooth Bass: Main Out L" (cut off at edge); own jack name NOT read yet'
back["Audio Input R"]='cabled: tooltip "Connected to Smooth Bass: Main Out R" (cut off at edge); own jack name NOT read yet'
back["Audio Output L"]='cabled: tooltip "Connected to Default Synchronous: Le..." (cut off); own jack name NOT read yet'
back["Audio Output R"]='cabled: tooltip "Connected to Default Synchronous: Rig..." (cut off); own jack name NOT read yet'
ROW=0
def load(slug,checks,view):
    d=json.load(open(slug+".json")); out=[]
    for c in d["controls"]:
        k="checked_2026_10_07"
        c[k]=checks[c["panel_label"]]
        if view: c["view"]=view
        out.append(c)
    return d,out
main,mc=load("sweeper",{**front,**back},None) if False else (None,None)
d=json.load(open("sweeper.json"))
for c in d["controls"]:
    c["checked_2026_10_07"]=(front if c["side"]=="front" else back)[c["panel_label"]]
    c["view"]="main panel (Phaser, Envelope view)" if c["side"]=="front" else "main panel"
for slug,checks,view,pic in (("sweeper-filter-view",filt,"Filter view (Filter button; picture sweeper-filter-view_front_labeled.png)",None),("sweeper-follower-view",fol,"Audio Follower view (picture sweeper-follower-view_front_labeled.png)",None)):
    e=json.load(open(slug+".json"))
    for c in e["controls"]:
        c["checked_2026_10_07"]=checks[c["panel_label"]]; c["view"]=view
        d["controls"].append(c)
d["status"]=("done 2026-10-07 (Claude, hover-checked in Reason 12): Phaser+Envelope main view, Filter view, Audio Follower view, back panel. "
 "NOT shown: Flanger view (same controls as Phaser minus Bandwidth/Stages). 7 front controls and 3 back icons give no tooltip (recorded as seen); "
 "the 4 audio jacks are cabled so their own names are unread (null). Device Name / BeatSync / Trig On / Stereo Mode / LFO Wave / LFO Sync / Env Loop assignments rest on the Remote list, not a tooltip.")
d["reason_version"]="12.7 (screenshots 2026-10-07)"
json.dump(d,open("sweeper.json","w"),indent=1,ensure_ascii=False)
print(len(d["controls"]))
