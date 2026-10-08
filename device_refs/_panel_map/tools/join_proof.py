#!/usr/bin/env python3
"""Join the Panel Map with knob proof (docs/reason/calibration.json).

Read-only on the panel JSONs (rewriting them reformats ~20k lines): writes PROOF-STATUS.csv and prints a rollup.
Join keys: panel remote_scope == calibration device key; reason_name == param key.
"""
from __future__ import annotations
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PM = ROOT / "device_refs" / "_panel_map"
CAL = json.loads((ROOT / "docs/reason/calibration.json").read_text())


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


# calibration keys come as "Scream 4 Distortion" or "se.propellerheads.ChannelEQ"
CAL_BY_NORM = {}
for k in CAL:
    CAL_BY_NORM[norm(k.split(".")[-1] if k.startswith("se.") else k)] = k


def cal_key(scope):
    name = scope.split("/", 1)[-1].strip()
    if name.startswith("se."):
        name = name.split(".")[-1]
    n = norm(name)
    if n in CAL_BY_NORM:
        return CAL_BY_NORM[n]
    for cn, k in CAL_BY_NORM.items():  # panel "ChannelEQ" vs cal "ChannelEQ", prefix either way
        if cn.startswith(n) or n.startswith(cn):
            return k
    return None


def is_proven(entry):
    return bool(entry) and bool(entry.get("table"))


rows, rollup, matched = [], {}, set()
for f in sorted(PM.glob("*.json")):
    d = json.loads(f.read_text())
    ck = cal_key(d.get("remote_scope", d["device"]))
    params = CAL.get(ck, {}) if ck else {}
    if ck:
        matched.add(ck)
    n_map = n_proven = 0
    for c in d["controls"]:
        mapped = bool(c.get("mapped_in_our_remotemap"))
        entry = params.get(c.get("reason_name", ""))
        proven = is_proven(entry)
        n_map += mapped
        n_proven += mapped and proven
        flags = ",".join(k for k in ("lossy", "volatile", "flat", "toggle") if entry and entry.get(k))
        rows.append([d["device"], c["code"], c.get("reason_name", ""), mapped, proven, flags])
    status = ("mapped+proven" if n_proven and n_proven == n_map else
              "mapped, partly proven" if n_proven else
              "mapped, not proven" if n_map else "no remote map")
    rollup[d["device"]] = (status, n_map, n_proven, ck)

with open(PM / "PROOF-STATUS.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["device", "code", "reason_name", "mapped", "proven", "flags"])
    w.writerows(rows)

print("== panel-map devices ==")
for dev, (st, m, p, ck) in rollup.items():
    print(f"{dev:42s} {st:24s} mapped={m:3d} proven={p:3d} cal={ck}")
print("\n== proven, no panel map ==")
for k in CAL:
    if k not in matched:
        print(" ", k)
