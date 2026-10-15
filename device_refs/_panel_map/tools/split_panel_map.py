#!/usr/bin/env python3
"""One-time lossless split of PANEL-MAP.md into chapters/ (00-INDEX.md + one file per device).
Run from device_refs/_panel_map. Does not touch PANEL-MAP.md; it only reads it and checks the result."""
import re, os, collections
md = open("PANEL-MAP.md", encoding="utf-8").read().split("\n")
heads = [i for i, l in enumerate(md) if l.startswith("## ")]
devices_i = next(i for i in heads if md[i] == "## Devices")
first_dev = next(i for i in heads if re.match(r"## .+ — (front|back)$", md[i]))
tail_i = next(i for i in heads if md[i].startswith("## Where each fact came from"))

header = md[:devices_i]
table = md[devices_i:first_dev]
tail = md[tail_i:]
body = md[first_dev:tail_i]

# group sections by device title
secs = collections.OrderedDict()
cur = None
for l in body:
    m = re.match(r"## (.+) — (front|back)$", l)
    if m:
        cur = m.group(1)
        secs.setdefault(cur, [])
    secs[cur].append(l)

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

# code prefix of a section = prefix of its first table row's code
def prefix(lines):
    for l in lines:
        m = re.match(r"\| ([A-Z0-9]+)-[FB]-", l)
        if m:
            return m.group(1)

os.makedirs("chapters", exist_ok=True)
by_prefix = {}
for t, lines in secs.items():
    name = slug(t) + ".md"
    open("chapters/" + name, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")
    by_prefix.setdefault(prefix(lines), []).append(name)

# index: header + table with a Chapter column + tail
out = []
for l in table:
    if l.startswith("| Device |"):
        out.append(l + " Chapter |")
    elif l.startswith("|---"):
        out.append(l + "---|")
    elif l.startswith("| "):
        code = l.split("|")[2].strip()
        ch = by_prefix.get(code, [])
        out.append(l + " " + (", ".join("[%s](%s)" % (c, c) for c in ch) or "—") + " |")
    else:
        out.append(l)
idx = ["# Panel Map index (read this first, then ONLY the chapter you need)",
       "", "Chapters live beside this file: one `<device>.md` each (front + back tables). Rules and method are below.", ""]
open("chapters/00-INDEX.md", "w", encoding="utf-8").write(
    "\n".join(idx + header[2:] + out + [""] + tail).rstrip("\n") + "\n")

# lossless check: every row of the original body is in exactly one chapter
orig_rows = [l for l in body if l.startswith("| ")]
new_rows = []
for t in secs:
    new_rows += [l for l in open("chapters/%s.md" % slug(t), encoding="utf-8").read().split("\n") if l.startswith("| ")]
assert orig_rows == new_rows, "row mismatch"
unlinked = [c for c in {l.split("|")[2].strip() for l in table if l.startswith("| ") and not l.startswith("| Device")} if c not in by_prefix]
print("chapters:", len(secs), "rows:", len(orig_rows), "table devices w/o chapter:", sorted(unlinked))
