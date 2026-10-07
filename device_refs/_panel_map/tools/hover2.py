#!/usr/bin/env python3
"""hover2.py <device.json> <front|back> x0 y0 sx sy pw ph [skipcodes..] -> codes line + computer_batch actions (nudge-then-hover, tall zoom). sx/sy = screen px per picture px."""
import json,sys
j=json.load(open(sys.argv[1])); side=sys.argv[2]
x0,y0,sx,sy,pw,ph=[float(a) for a in sys.argv[3:9]]; skip=set(sys.argv[9:]) 
acts=[];codes=[]
for r in j["controls"]:
    if r["side"]!=side or r["code"] in skip: continue
    x=round(x0+r["pos"][0]*pw*sx); y=round(y0+r["pos"][1]*ph*sy)
    acts+=[{"action":"mouse_move","coordinate":[x+4,y+3]},{"action":"mouse_move","coordinate":[x,y]},{"action":"wait","duration":1.3},
           {"action":"zoom","region":[max(0,x-30),max(0,y-4),min(1372,x+300),min(891,y+86)],"scale":0.4}]
    codes.append(f'{r["code"]}@{x},{y}')
print(" ".join(codes)); print(json.dumps(acts,separators=(",",":")))
