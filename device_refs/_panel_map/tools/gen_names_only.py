#!/usr/bin/env python3
"""Names-only Panel Map skeletons for devices that are proven (calibration.json)
but have no Panel Map yet. No pictures, no positions, no codes: those need Reason
open (hover check). Output: device_refs/_panel_map/names_only/<slug>.json
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(__file__).resolve().parents[3]
PM = ROOT / "device_refs" / "_panel_map"
CAL = json.loads((ROOT / "docs/reason/calibration.json").read_text())
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
have = {norm(json.loads(f.read_text())["remote_scope"].split(" / ")[-1].split(".")[-1]) for f in PM.glob("*.json")}
out = PM / "names_only"; out.mkdir(exist_ok=True)
n = 0
for scope, params in CAL.items():
    short = scope.split(".")[-1] if scope.startswith("se.") else scope
    if norm(short) in have or any(norm(short).startswith(h) or h.startswith(norm(short)) for h in have):
        continue
    slug = re.sub(r"[^a-z0-9]+", "-", short.lower()).strip("-")
    ctr = []
    for name, e in params.items():
        k = int(e["knob"].split("_")[1]) if e.get("knob") else None
        ctr.append(dict(reason_name=name, knob_slot=k, cc=29 + k if k else None,
            feedback_cc=77 + k if k else None, proven=bool(e.get("table")),
            range=[e.get("min_display"), e.get("max_display")], unit=e.get("unit"),
            flags=[f for f in ("lossy", "volatile", "flat", "toggle") if e.get(f)]))
    (out / f"{slug}.json").write_text(json.dumps(dict(device=short, remote_scope=scope,
        status="names only: from calibration.json. No picture, no positions, no codes yet (needs Reason hover check)",
        controls=ctr), indent=1, ensure_ascii=False) + "\n")
    n += 1; print(slug, len(ctr), "over CC127!" if any((c["cc"] or 0) > 127 for c in ctr) else "")
print(n, "devices")
