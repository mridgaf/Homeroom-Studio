#!/usr/bin/env python3
"""Check a Panel Map device JSON against Reason's Remote vocabulary and our remotemap.

Usage: python3 name_check.py <device.json> <remote-vocab.json> <remotemap>
Exit 0 if no ERRORs, 1 otherwise.
"""
import json
import re
import sys

CODE_RE = re.compile(r"^[A-Z0-9]+-(F|B)-(K|B|S|J|D)\d{2,3}$")


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def parse_remotemap(path, device_name):
    """Return (found_scope, {slot: item}) for the device block."""
    found = False
    inblock = False
    knobs = {}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            parts = line.split("\t")
            if parts[0] == "Scope":
                inblock = len(parts) >= 3 and parts[2].strip() == device_name
                if inblock:
                    found = True
                continue
            if inblock and parts[0] == "Map" and len(parts) >= 2:
                m = re.match(r"^Knob (\d+)$", parts[1].strip())
                if m:
                    item = parts[3].strip() if len(parts) >= 4 else ""
                    knobs[int(m.group(1))] = item
    return found, knobs


def main(argv):
    if len(argv) != 4:
        print("Usage: python3 name_check.py <device.json> <remote-vocab.json> <remotemap>")
        return 2
    dev_path, vocab_path, map_path = argv[1:4]
    with open(dev_path, encoding="utf-8") as f:
        dev = json.load(f)
    with open(vocab_path, encoding="utf-8") as f:
        vocab = json.load(f)

    errors = []
    warns = []
    name = dev.get("device")
    prefix = dev.get("code_prefix")
    controls = dev.get("controls", [])

    # 8. device lookup
    items = None
    for v in vocab.get("devices", {}).values():
        if v.get("name") == name:
            items = list(v.get("items", []))
            break
    if items is None:
        errors.append("Device name %r not found in remote-vocab.json." % name)
    found_scope, knobs = parse_remotemap(map_path, name)
    if not found_scope:
        errors.append("No 'Scope' block for device %r in the remotemap." % name)

    seen = {}
    slots_in_rows = set()
    for c in controls:
        code = c.get("code")
        label = code if code else "(row with no code)"

        # 5. codes
        if not isinstance(code, str) or not CODE_RE.match(code):
            errors.append("%s: code %r does not match the code pattern." % (label, code))
        else:
            if code in seen:
                errors.append("%s: duplicate code." % code)
            seen[code] = True
            cp = code.split("-")
            if cp[0] != prefix:
                errors.append("%s: code prefix %r is not the device code_prefix %r." % (code, cp[0], prefix))
            side = c.get("side")
            want = {"front": "F", "back": "B"}.get(side)
            if want is None or cp[1] != want:
                errors.append("%s: side letter %r does not match row side %r." % (code, cp[1], side))

        # 6. pos
        pos = c.get("pos")
        if not (isinstance(pos, list) and len(pos) == 2 and all(is_num(x) and 0 <= x <= 1 for x in pos)):
            errors.append("%s: pos %r is missing or is not two numbers between 0 and 1." % (label, pos))

        # 7. checked_*
        ok = False
        for k, v in c.items():
            if k.startswith("checked_") and v is not None and str(v).strip() != "":
                ok = True
        if not ok:
            errors.append("%s: no non-empty checked_* field." % label)

        # 1. remote names
        rn = c.get("reason_name")
        if rn and c.get("remote_item") is True and items is not None and rn not in items:
            errors.append("%s: reason_name %r is not a Remote item of %s." % (label, rn, name))

        # 2. knob slots
        slot = c.get("knob_slot")
        if slot is not None:
            if not isinstance(slot, int) or isinstance(slot, bool):
                errors.append("%s: knob_slot %r is not a whole number." % (label, slot))
            else:
                slots_in_rows.add(slot)
                if slot not in knobs:
                    errors.append("%s: knob slot %d is not in the remotemap for this device." % (label, slot))
                elif knobs[slot] != rn:
                    errors.append("%s: remotemap maps Knob %d to %r but row reason_name is %r."
                                  % (label, slot, knobs[slot], rn))
                if c.get("cc") != 29 + slot:
                    errors.append("%s: cc is %r, expected %d (29 + slot %d)." % (label, c.get("cc"), 29 + slot, slot))
                if c.get("feedback_cc") != 77 + slot:
                    errors.append("%s: feedback_cc is %r, expected %d (77 + slot %d)."
                                  % (label, c.get("feedback_cc"), 77 + slot, slot))

    # 3. remotemap knobs without a row
    for slot in sorted(knobs):
        if slot not in slots_in_rows:
            errors.append("Remotemap Knob %d (%r) has no row with that knob_slot." % (slot, knobs[slot]))

    # 4. vocab items nobody mentions
    if items is not None:
        names = []
        for c in controls:
            for k in ("reason_name",):
                if isinstance(c.get(k), str):
                    names.append(c[k])
        for it in items:
            if not any(it in n for n in names):
                warns.append("Remote item %r is not mentioned by any row's reason_name." % it)

    print("Name check: %s (%s)" % (name, dev_path))
    print("Rows checked: %d; remotemap knobs: %d; Remote items: %s"
          % (len(controls), len(knobs), len(items) if items is not None else "n/a"))
    for w in warns:
        print("WARN:  " + w)
    for e in errors:
        print("ERROR: " + e)
    print("Result: %d error(s), %d warning(s). %s" % (len(errors), len(warns), "FAIL" if errors else "PASS"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
