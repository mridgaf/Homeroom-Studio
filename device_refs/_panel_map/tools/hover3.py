#!/usr/bin/env python3
"""hover3.py <device.json> <front|back> x0 y0 sx sy pw ph chunk_size out_prefix : compact hover lists (small zoom), split in chunks. Writes <out>_<i>.json and <out>.codes"""
import json,sys
d=json.load(open(sys.argv[1])); side=sys.argv[2]
x0,y0,sx,sy,pw,ph=map(float,sys.argv[3:9]); n=int(sys.argv[9]); out=sys.argv[10]
rows=[r for r in d["controls"] if r["side"]==side]
codes=[];acts=[]
for r in rows:
    X=round(x0+r["pos"][0]*pw*sx); Y=round(y0+r["pos"][1]*ph*sy)
    codes.append((r["code"],X,Y))
    reg=[X-15,Y+70,X+235,Y+126] if r["code"].split("-")[-1].startswith("S") else [X-15,Y-4,X+235,Y+52]
    acts+=[{"action":"mouse_move","coordinate":[X+4,Y+3]},{"action":"mouse_move","coordinate":[X,Y]},{"action":"wait","duration":1.3},{"action":"zoom","region":reg,"scale":0.3}]
for i in range(0,len(codes),n):
    json.dump(acts[i*4:(i+n)*4],open(f"{out}_{i//n}.json","w"),separators=(",",":"))
json.dump(codes,open(out+".codes","w"))
print(len(codes),"hovers,",(len(codes)+n-1)//n,"chunks")
