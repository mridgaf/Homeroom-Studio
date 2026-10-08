#!/usr/bin/env python3
"""Mimic: one physical knob serves slots 1-8; remotemap gives each slot its own knob slot. Add alias rows for slots 2-8."""
import json
d=json.load(open("mimic.json"))
base={c["panel_label"]:c for c in d["controls"] if c["side"]=="front"}
kinds=(("AMP GAIN","Amp Gain",0),("PITCH SEMI","Pitch Semi",1),("FILTER FREQ","Filter Freq",2),("START marker","Start Pos",3),("AMP ENV D","Amp Decay",4))
n=300
for s in range(2,9):
    for lab,nm,off in kinds:
        src=base[lab]; slot=5*(s-1)+1+off; n+=1
        d["controls"].append(dict(code=f"MIMC-F-K{n}",side="front",panel_label=f"{lab} (as Slot {s})",what=f"{nm} of slot {s}: same physical control as {src['code']}, aimed at slot {s} when that slot is selected",
          reason_name=f"{nm} {s}",remote_item=True,mapped_in_our_remotemap=True,knob_slot=slot,cc=29+slot,feedback_cc=77+slot,pos=src["pos"],how="voice/MIDI or click",
          checked_2026_10_07="not separately hovered: same control as %s (slot %d must be selected first). Name+slot from the remotemap and Remote list"%(src["code"],s),
          confidence="medium",confidence_reason="alias of the one control; no own box in the picture",view="main panel"))
json.dump(d,open("mimic.json","w"),indent=1,ensure_ascii=False); print(len(d["controls"]),"rows")
