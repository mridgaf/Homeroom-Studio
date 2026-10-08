#!/usr/bin/env python3
"""Build one device from a spec and stamp the hover results on it.
Usage: finish_device.py <slug> <status text>
Reads tools/specs/<slug>.json (spec for build_device.py) and tools/checks/<slug>.json
({"front": {label: text}, "back": {label: text}, "default_front": text?, "default_back": text?}).
Writes <slug>.json with checked_2026_10_07 on every row (missing label => error, so nothing is skipped).
Extra views: tools/specs/<slug>--<view>.json + same name in checks (key "views": {view: {label: text}}).
"""
import json, subprocess, sys, glob, os
slug, status = sys.argv[1], sys.argv[2]
py = sys.executable
chk = json.load(open(f"tools/checks/{slug}.json"))
def build(spec):
    subprocess.check_call([py, "tools/build_device.py", spec], stdout=subprocess.DEVNULL)
subprocess.check_call([py, "tools/build_device.py", f"tools/specs/{slug}.json"], stdout=subprocess.DEVNULL)
d = json.load(open(f"{slug}.json"))
missing = []
for c in d["controls"]:
    t = chk[c["side"]].get(c["panel_label"])
    if t is None: missing.append((c["side"], c["panel_label"])); continue
    c["checked_2026_10_07"] = t
    c["view"] = "main panel"
for sp in sorted(glob.glob(f"tools/specs/{slug}--*.json")):
    view = os.path.basename(sp)[len(slug) + 2:-5]
    subprocess.check_call([py, "tools/build_device.py", sp], stdout=subprocess.DEVNULL)
    vs = json.load(open(json.load(open(sp))["slug"] + ".json"))
    for c in vs["controls"]:
        t = chk["views"][view].get(c["panel_label"])
        if t is None: missing.append((view, c["panel_label"])); continue
        c["checked_2026_10_07"] = t
        c["view"] = chk["view_titles"][view]
        d["controls"].append(c)
    os.remove(json.load(open(sp))["slug"] + ".json")
if missing:
    print("MISSING check text:", missing); sys.exit(1)
d["device"] = chk.get("device", d["device"]); d["status"] = status
d["reason_version"] = "12.7 (screenshots 2026-10-07)"
json.dump(d, open(f"{slug}.json", "w"), indent=1, ensure_ascii=False)
print(slug, len(d["controls"]), "rows")
