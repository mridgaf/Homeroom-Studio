"""Add (or replace) one device's knob block in remote/ReasonVoice.remotemap.

    .venv/bin/python reason_voice/map_device.py "The Echo"
        every usable control Reason's factory maps list, in their order
    .venv/bin/python reason_voice/map_device.py "The Echo" "Delay Time" "Feedback"
        just these, in this order (Knob 1, Knob 2, ...)

Why a script and not an edit: the map is TAB-separated, and copy-paste turns
tabs into spaces, which Reason ignores without a word. Names come only from
Reason's own factory maps (docs/reason/remote-vocab.json) -- a name that is
almost right also fails without a word. See the reason-remote-bridge skill.

Then: ./install.sh, and a full Cmd+Q restart of Reason (it reads maps at launch).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REMOTEMAP = ROOT / "remote" / "ReasonVoice.remotemap"
VOCAB = ROOT / "docs" / "reason" / "remote-vocab.json"
MAX_KNOBS = 48          # the codec defines 48; the CC budget caps it (skill)

# Not knobs: the patch browser, the rack label, and read-only meters/lights.
# Whole words: "LED" is inside "Enabled", "Meter" inside "Parameter".
NOT_A_KNOB = re.compile(r"Device Name|Patch Name|Select (Next|Previous) Patch|"
                        r"Select Patch Delta|\bMeter\b|\bLED\b|\bIndicator\b", re.I)


def find_device(name, vocab):
    """Match the scope id ("se.propellerheads.Sweeper") or its display name."""
    for key, d in vocab.items():
        if name in (key, d.get("name")):
            return key, d
    raise SystemExit("No device called %r in Reason's factory maps." % name)


def block(manufacturer, model, items, has_patches):
    lines = ["Scope\t%s\t%s" % (manufacturer, model)]
    if has_patches:
        lines += ["Map\tPatch Next\t\tSelect Next Patch",
                  "Map\tPatch Prev\t\tSelect Previous Patch"]
    lines.append("Map\tDevice\t\tDevice Name")
    lines += ["Map\tKnob %d\t\t%s" % (i, p) for i, p in enumerate(items, 1)]
    return lines


def write_block(text, model, new_lines):
    """Replace the device's existing Scope block, or append a new one."""
    lines = text.rstrip("\n").split("\n")
    start = next((i for i, ln in enumerate(lines)
                  if ln.startswith("Scope\t") and ln.split("\t")[2] == model), None)
    if start is None:
        lines += [""] + new_lines
    else:
        end = start + 1
        while end < len(lines) and lines[end].strip():
            end += 1
        lines[start:end] = new_lines
    return "\n".join(lines) + "\n"


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    vocab = json.loads(VOCAB.read_text())["devices"]
    model, dev = find_device(argv[0], vocab)
    known = dev["items"]
    wanted = argv[1:] or [i for i in known if not NOT_A_KNOB.search(i)]
    unknown = [p for p in wanted if p not in known]
    if unknown:
        raise SystemExit("Not in Reason's factory maps for %s: %s" % (model, unknown))
    if len(wanted) > MAX_KNOBS:
        raise SystemExit("%s has %d controls; the surface holds %d. Pick the cut "
                         "with the owner first." % (model, len(wanted), MAX_KNOBS))
    has_patches = {"Select Next Patch", "Select Previous Patch"} <= set(known)
    new = block(dev["manufacturer"], model, wanted, has_patches)
    REMOTEMAP.write_text(write_block(REMOTEMAP.read_text(), model, new))
    print("%s: %d knobs mapped." % (model, len(wanted)))


if __name__ == "__main__":
    main(sys.argv[1:])
