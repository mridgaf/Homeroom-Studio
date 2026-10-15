#!/usr/bin/env python3
"""Write finished devices into chapters/ (one file per device) and add their rows to chapters/00-INDEX.md.
Usage (from device_refs/_panel_map): python3 tools/panel_map_md.py "<slug>|<Title>" ...
Skips a device whose chapter file already exists. Never touches PANEL-MAP.md."""
import json, os, re, sys
ROOT = "chapters"
INDEX = os.path.join(ROOT, "00-INDEX.md")
if len(sys.argv) < 2:
    sys.exit("usage: panel_map_md.py '<slug>|<Title>' ...")
order = [tuple(a.split("|", 1)) for a in sys.argv[1:]]

def cell(c):
    return str(c).replace("|", "/").replace("\n", " ")

idx = open(INDEX, encoding="utf-8").read()
added = 0
for slug, title in order:
    chapter = os.path.join(ROOT, slug + ".md")
    if os.path.exists(chapter):
        print("skip (chapter exists):", slug); continue
    d = json.load(open(slug + ".json", encoding="utf-8")); pre = d["code_prefix"]
    out = []
    for side in ("front", "back"):
        cs = [c for c in d["controls"] if c["side"] == side]
        if not cs: continue
        out += ["## %s — %s" % (title, side), "| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |", "|---|---|---|---|---|---|---|"]
        for c in cs:
            rn = c.get("reason_name") or c.get("reason_cable_menu_name") or "—"
            sl = "%s / CC %s" % (c["knob_slot"], c["cc"]) if c.get("knob_slot") is not None else "—"
            v = ("[%s] " % c["view"]) if c.get("view") and c["view"] != "main panel" else ""
            out.append("| %s |" % " | ".join(cell(x) for x in (c["code"], c["panel_label"], c["what"], rn, sl, c.get("how", ""), v + str(c.get("checked_2026_10_07", "")))))
        out.append("")
    open(chapter, "w", encoding="utf-8").write("\n".join(out))
    row = "| %s | %s | %s_front_labeled.png | %s_back_labeled.png | %s.json | %s | [%s.md](%s.md) |" % (title, pre, slug, slug, slug, cell(d["status"]), slug, slug)
    lines = idx.split("\n")
    last = max(i for i, l in enumerate(lines) if l.startswith("| ") and "_front_labeled" in l or l.startswith("| Device"))
    idx = "\n".join(lines[:last + 1] + [row] + lines[last + 1:])
    added += 1
open(INDEX, "w", encoding="utf-8").write(idx)
print("added", added, "devices")
