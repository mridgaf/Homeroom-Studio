#!/usr/bin/env python3
"""Add the 45 alias rows for Drum 2-16 (slots 4-48). One physical LCD knob serves all 16 drums; the remotemap
gives each drum its own slot, so each slot needs a row. They share the LCD knob's position and have no box in the picture."""
import json
d = json.load(open("kong-drum-designer.json"))
base = {c["panel_label"]: c for c in d["controls"] if c["view"] == "main panel" and c["side"] == "front"}
kinds = (("LEVEL", "Level", 0, "K"), ("OFFSET PITCH", "Pitch Offset", 1, "K"), ("OFFSET DECAY", "Decay Offset", 2, "K"))
n = 300
for drum in range(2, 17):
    for lab, nm, off, t in kinds:
        src = base[lab]; slot = 3 * (drum - 1) + 1 + off; n += 1
        d["controls"].append(dict(code=f"KONG-F-K{n}", side="front", panel_label=f"{lab} (as Drum {drum})",
            what=f"{src['what'].split(' of ')[0]} of drum {drum}: same physical knob as {src['code']}, aimed at drum {drum} when that drum is selected",
            reason_name=f"Drum {drum} {nm}", remote_item=True, mapped_in_our_remotemap=True, knob_slot=slot, cc=29 + slot, feedback_cc=77 + slot,
            pos=src["pos"], how="voice/MIDI or click", checked_2026_10_07=f"not separately hovered: same knob as {src['code']} (drum {drum} must be selected first). Name+slot from the remotemap and Remote list",
            confidence="medium", confidence_reason="alias of the one LCD knob; no own box in the picture", view="main panel"))
json.dump(d, open("kong-drum-designer.json", "w"), indent=1, ensure_ascii=False)
print(len(d["controls"]), "rows")
