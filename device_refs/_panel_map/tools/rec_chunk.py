#!/usr/bin/env python3
"""rec_chunk.py <device.json> <codes_file> <start_index> : reads observed strings (one per line) from stdin, applies to codes[start..]; also sets reason_cable_menu_name for jacks when a line starts with 'J:' ('J:name' -> tooltip name)."""
import json,sys
dj,cf,st=sys.argv[1],sys.argv[2],int(sys.argv[3])
codes=json.load(open(cf)); d=json.load(open(dj)); lines=[l.rstrip("\n") for l in sys.stdin if l.strip()]
by={r["code"]:r for r in d["controls"]}
for i,l in enumerate(lines):
    code=codes[st+i][0]; r=by[code]
    if l.startswith("J:"):
        nm=l[2:]; r["reason_cable_menu_name"]=nm; r["checked_2026_10_07"]=f"tooltip '{nm}' (empty jack)"
    else: r["checked_2026_10_07"]=l
json.dump(d,open(dj,"w"),indent=2,ensure_ascii=False); print("recorded",len(lines),"from",st)
