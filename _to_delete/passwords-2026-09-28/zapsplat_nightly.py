#!/usr/bin/env python3
"""Zapsplat nightly - top-rated loops."""
import os, shutil
from pathlib import Path
from datetime import datetime

LOOPS_LIB = os.getenv("LOOPS_LIB_ROOT", "/Volumes/TBOTC 3/Sample Packs/BOTC Sorted Loops")
TEMP_DIR = Path(os.path.expanduser("~/Desktop/Homeroom Studio/Nightly Loops/.zapsplat_temp"))
ROLES = ["Melody", "Chords", "Bass", "Drums", "Vocals"]

def guess_role(filename):
    name_lower = filename.lower()
    if any(x in name_lower for x in ["drum", "kick", "snare", "perc"]): return "Drums"
    if any(x in name_lower for x in ["bass", "sub"]): return "Bass"
    if any(x in name_lower for x in ["chord", "pad", "string", "piano"]): return "Chords"
    if any(x in name_lower for x in ["vocal", "voice"]): return "Vocals"
    return "Melody"

def process():
    for role in ROLES:
        (Path(LOOPS_LIB) / role).mkdir(parents=True, exist_ok=True)
    
    filed = {role: 0 for role in ROLES}
    if TEMP_DIR.exists():
        for file in TEMP_DIR.glob("*.wav"):
            role = guess_role(file.name)
            dest = Path(LOOPS_LIB) / role / file.name
            shutil.move(str(file), str(dest))
            filed[role] += 1
        shutil.rmtree(TEMP_DIR)
    
    log = f"Zapsplat nightly - {datetime.now().strftime('%Y-%m-%d')} (top-rated)\nFiled: {sum(filed.values())} loops\n  - Melody: {filed.get('Melody', 0)}\n  - Chords: {filed.get('Chords', 0)}\n  - Bass: {filed.get('Bass', 0)}\n  - Drums: {filed.get('Drums', 0)}\n  - Vocals: {filed.get('Vocals', 0)}\n"
    Path(os.path.expanduser("~/Desktop/Homeroom Studio/Nightly Loops/zapsplat.log")).write_text(log)
    print(log)

if __name__ == "__main__":
    process()
