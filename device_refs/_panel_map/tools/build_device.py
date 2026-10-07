#!/usr/bin/env python3
"""Generic Panel Map builder (same logic as build_the-echo.py).
Usage: python3 build_device.py <spec.json>
spec: {device, slug, prefix, remote_scope, front_raw, back_raw, out_dir, date,
  front:[[label,what,reason_name|null,slot|null,[cx,cy],[hw,hh],type,confidence,why,label_mode?]],
  back:[[label,what,type,[cx,cy],[hw,hh],why,label_mode?]]}
Positions are picture pixels; saved as fractions. Label modes: above/below/left/right/in.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
spec = json.load(open(sys.argv[1]))
P = spec["prefix"]; date = spec.get("date", "2026-10-07")
FR = spec["front"]; BK = spec["back"]
fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(fp, 12) if os.path.exists(fp) else ImageFont.load_default()
def number(items, ti, pi, band=40, offs=None):
    cnt = dict(offs or {}); codes = {}
    order = sorted(range(len(items)), key=lambda i: (items[i][pi][1] // band, items[i][pi][0]))
    for i in order:
        t = items[i][ti]; cnt[t] = cnt.get(t, 0) + 1; codes[i] = (t, cnt[t])
    return codes
fc = number(FR, 6, 4, 40, spec.get("front_offsets")); bc = number(BK, 2, 3)
fcode = lambda i: f"{P}-F-{fc[i][0]}{fc[i][1]:02d}"
bcode = lambda i: f"{P}-B-{bc[i][0]}{bc[i][1]:02d}"
def draw(src, out, boxes):
    im = Image.open(src).convert("RGB"); d = ImageDraw.Draw(im)
    for code, (cx, cy), (hw, hh), mode in boxes:
        d.rectangle([cx-hw, cy-hh, cx+hw, cy+hh], outline=(255, 0, 170), width=2)
        t = code.split("-", 1)[1]; tw = d.textlength(t, font=font)
        opts = {"above": (cx-tw/2, cy-hh-15), "below": (cx-tw/2, cy+hh+2), "right": (cx+hw+3, cy-7), "left": (cx-hw-tw-5, cy-7), "in": (cx-tw/2, cy-7)}
        x, y = opts[mode or "above"]
        x = max(1, min(im.width-tw-4, x)); y = max(0, min(im.height-15, y))
        d.rectangle([x-2, y, x+tw+2, y+14], fill=(0, 0, 0)); d.text((x, y), t, fill=(255, 255, 0), font=font)
    im.save(out); return im.size
od = spec["out_dir"]; s = spec["slug"]
fb = [(fcode(i), r[4], r[5], r[9] if len(r) > 9 else None) for i, r in enumerate(FR)]
bb = [(bcode(i), r[3], r[4], r[6] if len(r) > 6 else None) for i, r in enumerate(BK)]
fs = draw(spec["front_raw"], f"{od}/{s}_front_labeled.png", fb)
bs = draw(spec["back_raw"], f"{od}/{s}_back_labeled.png", bb) if BK else (1, 1)
rows = []
for i, r in enumerate(FR):
    lab, what, name, k, (cx, cy), hs, t, conf, why = r[:9]
    rows.append(dict(code=fcode(i), side="front", panel_label=lab, what=what, reason_name=name or None,
        remote_item=bool(name), mapped_in_our_remotemap=k is not None or name in ("Select Previous Patch", "Select Next Patch", "Device Name"),
        knob_slot=k, cc=(29+k if k else None), feedback_cc=(77+k if k else None),
        pos=[round(cx/fs[0], 3), round(cy/fs[1], 3)],
        how=("voice/MIDI or click" if k else ("click only" if not name else "display/Remote item, not mapped")),
        **{f"checked_{date.replace('-', '_')}": "PENDING"}, confidence=conf, **({"confidence_reason": why} if why else {})))
for i, r in enumerate(BK):
    lab, what, t, (cx, cy), hs, why = r[:6]
    nm = r[7] if len(r) > 7 else None; sl = r[8] if len(r) > 8 else None
    extra = dict(reason_name=nm, remote_item=True, mapped_in_our_remotemap=sl is not None, knob_slot=sl, cc=(29+sl if sl else None), feedback_cc=(77+sl if sl else None)) if nm else {}
    rows.append(dict(code=bcode(i), side="back", panel_label=lab, what=what, reason_cable_menu_name=None, **extra,
        pos=[round(cx/bs[0], 3), round(cy/bs[1], 3)],
        how=("cable: right-click jack > device > jack name" if t == "J" else ("voice/MIDI or click" if nm and sl else "click/drag only (no Remote item)")),
        **{f"checked_{date.replace('-', '_')}": "PENDING"}, confidence="high" if t in ("J", "D") else "medium",
        **({"confidence_reason": why} if why else {})))
json.dump(dict(device=spec["device"], remote_scope=spec["remote_scope"], code_prefix=P,
    reason_version="12.7 (screenshots 2026-10-03)",
    pos_note="pos = [x,y] as fraction of the captured panel picture (0-1), not screen pixels. Measured by eye; check in Reason before trusting.",
    status="draft, unchecked", controls=rows), open(f"{od}/{s}.json", "w"), indent=1, ensure_ascii=False)
print(spec["device"], len(FR), len(BK), fs, bs)
