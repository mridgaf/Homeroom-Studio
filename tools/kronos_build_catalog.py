"""Turn Korg's KRONOS Voice Name List text into tools/kronos_programs.json.

One-off. Needs the PDF turned into text first (pypdf is NOT in the project venv):
    pypdf: ''.join(page.extract_text()) with "[page N]" markers between pages.
Usage: python tools/kronos_build_catalog.py <voice_name_list.txt>
"""
import json
import os
import re
import sys

# Korg bank map (MIDI Implementation, Bank Map = KORG): Bank Select LSB per bank.
BANK_LSB = {"INT-A": 0, "INT-B": 1, "INT-C": 2, "INT-D": 3, "INT-E": 4, "INT-F": 5,
            "USER-A": 8, "USER-B": 9, "USER-C": 10, "USER-D": 11, "USER-E": 12,
            "USER-F": 13, "USER-G": 14, "USER-AA": 15, "USER-BB": 16, "USER-CC": 17,
            "USER-DD": 18, "USER-EE": 19, "USER-FF": 20, "USER-GG": 21}
# Korg prints 100-127 as "A0100" or "F 100", so allow 3-4 digits with an optional space
LINE = re.compile(r"^([A-G]{1,2}) ?(\d{3,4}) (.+)$")
HEAD = re.compile(r"((?:INT|USER)-[A-G]{1,2}) \[")


def build(text_path):
    out = []
    for page in open(text_path).read().split("[page ")[1:]:
        lines = page.split("\n")
        head = "\n".join(lines[:6])
        m = HEAD.search(head)
        # Programs are PDF pages 12-28; Combinations (6-11) reuse the same bank names
        pageno = int(page.split("]", 1)[0])
        if not m or not 12 <= pageno <= 28 or m.group(1) not in BANK_LSB:
            continue
        bank = m.group(1)
        for ln in lines:
            p = LINE.match(ln)
            if p:
                out.append({"bank": bank, "lsb": BANK_LSB[bank], "pc": int(p.group(2)),
                            "text": p.group(3)})
    return out


if __name__ == "__main__":
    progs = build(sys.argv[1])
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kronos_programs.json")
    # ensure_ascii=False: house convention, avoids phantom diffs
    json.dump(progs, open(dest, "w"), ensure_ascii=False, indent=0)
    print(len(progs), "programs ->", dest)
