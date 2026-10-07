#!/usr/bin/env python3
"""record_checks.py <device.json> <checks.json>  — checks.json = {code: "what Reason showed"}; sets checked_2026_10_07."""
import json,sys
p,cj=sys.argv[1],sys.argv[2]
d=json.load(open(p)); ch=json.load(open(cj)); n=0
for c in d["controls"]:
    if c["code"] in ch:
        c["checked_2026_10_07"]=ch[c["code"]]; n+=1
json.dump(d,open(p,"w"),indent=2,ensure_ascii=False)
print(p,"recorded",n,"of",len(ch))
