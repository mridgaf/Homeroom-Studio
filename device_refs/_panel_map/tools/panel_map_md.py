#!/usr/bin/env python3
"""Add Batch A rows to PANEL-MAP.md: Devices-table rows (before '## Scream 4 — front') and sections (before '## Where each fact came from'). Skips anything already present."""
import json
order=[("cf-101","CF-101 Chorus/Flanger"),("comp-01","COMP-01 Compressor"),("d-11","D-11 Foldback Distortion"),("ddl-1","DDL-1 Digital Delay Line"),("ecf-42","ECF-42 Envelope Controlled Filter"),("peq-2","PEQ-2 Two Band Parametric EQ"),("ph-90","PH-90 Phaser"),("rv-7","RV-7 Digital Reverb"),("un-16","UN-16 Unison"),("mclass-compressor","MClass Compressor"),("mclass-equalizer","MClass Equalizer"),("mclass-maximizer","MClass Maximizer"),("mclass-stereo-imager","MClass Stereo Imager"),("rv7000","RV7000 Mk II Advanced Reverb")]
import sys
if len(sys.argv)>1: order=[tuple(a.split("|",1)) for a in sys.argv[1:]]
md=open("PANEL-MAP.md",encoding="utf-8").read()
rows=[];secs=[]
def cell(c):
    return str(c).replace("|","/").replace("\n"," ")
for slug,title in order:
    d=json.load(open(slug+".json")); pre=d["code_prefix"]
    if "| %s | %s_front_labeled.png"%(pre,slug) in md: continue
    n=len(d["controls"])
    rows.append("| %s | %s | %s_front_labeled.png | %s_back_labeled.png | %s.json | %s |"%(title,pre,slug,slug,slug,cell(d["status"])))
    for side,label in (("front","front"),("back","back")):
        cs=[c for c in d["controls"] if c["side"]==side]
        if not cs: continue
        t=["## %s — %s"%(title,label),"| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |","|---|---|---|---|---|---|---|"]
        for c in cs:
            rn=c.get("reason_name") or c.get("reason_cable_menu_name") or "—"
            sl="%s / CC %s"%(c["knob_slot"],c["cc"]) if c.get("knob_slot") is not None else "—"
            v=("[%s] "%c["view"] if c.get("view") and c["view"]!="main panel" else "")
            t.append("| %s | %s | %s | %s | %s | %s | %s |"%tuple(cell(x) for x in (c["code"],c["panel_label"],c["what"],rn,sl,c.get("how",""),v+str(c.get("checked_2026_10_07","")))))
        secs.append("\n".join(t))
if rows:
    md=md.replace("\n## Scream 4 — front","\n".join(rows[:0])+"\n".join([""]+rows)[1:]+"\n\n## Scream 4 — front",1) if False else md
    i=md.index("\n## Scream 4 — front")
    md=md[:i].rstrip("\n")+"\n"+"\n".join(rows)+"\n"+md[i:]
    j=md.index("\n## Where each fact came from")
    md=md[:j]+"\n"+"\n\n".join(secs)+"\n"+md[j:]
    open("PANEL-MAP.md","w",encoding="utf-8").write(md)
print("added",len(rows),"devices")
