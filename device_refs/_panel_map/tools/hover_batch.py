#!/usr/bin/env python3
"""Print a computer_batch action list (hover + zoom) for one device side.
Usage: hover_batch.py <device.json> <front|back> <x0> <y0> <scale> [pic_w pic_h]
Screen point = (x0 + pos_x*pic_w*scale, y0 + pos_y*pic_h*scale). Zoom region sits below-right of pointer."""
import json, sys
j = json.load(open(sys.argv[1])); side = sys.argv[2]
x0, y0, sc = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
pw = float(sys.argv[6]) if len(sys.argv) > 6 else 985; ph = float(sys.argv[7]) if len(sys.argv) > 7 else 207
view = sys.argv[8] if len(sys.argv) > 8 else None
acts = []; codes = []
for r in j["controls"]:
    if r["side"] != side: continue
    if view and r.get("view", "main panel") != view: continue
    x = round(x0 + r["pos"][0]*pw*sc); y = round(y0 + r["pos"][1]*ph*sc)
    acts += [{"action": "mouse_move", "coordinate": [x, y]}, {"action": "wait", "duration": 1.4},
             {"action": "zoom", "region": [max(0, x-30), y-4, x+290, y+52], "scale": 0.4}]
    codes.append(f'{r["code"]}@{x},{y}')
print(" ".join(codes)); print(json.dumps(acts, separators=(",", ":")))
