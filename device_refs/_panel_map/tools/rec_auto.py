#!/usr/bin/env python3
"""rec_auto.py <device.json> <codes_file> <start> <count> [CODE=text ...]
Records observed results for codes[start:start+count] when each tooltip read exactly '<reason_name>' (B), '<reason_name>: <val>' (K/S) or none (D).
Only use after viewing every zoom; pass CODE=text overrides for anything that differed. val defaults: 0 for K, 100 for S."""
import json,sys
dj,cf,st,n=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]); ov=dict(a.split("=",1) for a in sys.argv[5:])
codes=json.load(open(cf)); d=json.load(open(dj)); by={r["code"]:r for r in d["controls"]}
for c,_,_ in codes[st:st+n]:
    r=by[c]; t=c.split("-")[-1][0]; nm=r["reason_name"]
    if c in ov: r["checked_2026_10_07"]=ov[c]; continue
    if t=="B": r["checked_2026_10_07"]=f"tooltip '{nm}'"
    elif t=="K": r["checked_2026_10_07"]=f"tooltip '{nm}: 0'"
    elif t=="S": r["checked_2026_10_07"]=f"tooltip '{nm}: 100' (shown below the fader strip when hovering the handle)"
    else: r["checked_2026_10_07"]="meter/name tape, no tooltip"
json.dump(d,open(dj,"w"),indent=2,ensure_ascii=False); print("recorded",n,"from",st)
