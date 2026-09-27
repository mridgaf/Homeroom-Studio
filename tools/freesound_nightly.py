#!/usr/bin/env python3
"""Freesound nightly - downloads 60 loops, moves to role folders, cleans up."""
import os, sys, shutil
from pathlib import Path
from datetime import datetime

LOOPS_LIB = os.getenv("LOOPS_LIB_ROOT", "/Volumes/TBOTC 3/Sample Packs/BOTC Sorted Loops")
TEMP_DIR = Path(os.path.expanduser("~/Desktop/Homeroom Studio/Nightly Loops/.freesound_temp"))
ROLES = ["Melody", "Chords", "Bass", "Drums", "Vocals"]

def log_summary(date_str, filed, skipped):
    """Write summary—only file written is this log."""
    summary = f"""Freesound nightly - {date_str}
Filed: {sum(filed.values())} loops
  - Melody: {filed.get('Melody', 0)}
  - Chords: {filed.get('Chords', 0)}
  - Bass: {filed.get('Bass', 0)}
  - Drums: {filed.get('Drums', 0)}
  - Vocals: {filed.get('Vocals', 0)}
Skipped: {len(skipped)}
"""
    log_path = Path(os.path.expanduser("~/Desktop/Homeroom Studio/Nightly Loops/freesound.log"))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(summary)
    print(summary)

def guess_role(filename):
    """Guess role from filename."""
    name_lower = filename.lower()
    if any(x in name_lower for x in ["drum", "kick", "snare", "hihat", "perc"]):
        return "Drums"
    if any(x in name_lower for x in ["bass", "sub"]):
        return "Bass"
    if any(x in name_lower for x in ["chord", "pad", "string", "piano", "key"]):
        return "Chords"
    if any(x in name_lower for x in ["vocal", "voice"]):
        return "Vocals"
    return "Melody"

def cleanup_temp():
    """Delete temp folder completely."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

def process_downloads():
    """Move downloaded files from temp to role folders, delete temp."""
    if not os.path.isdir(LOOPS_LIB):
        print(f"Drive not found: {LOOPS_LIB}")
        cleanup_temp()
        return
    
    print(f"Freesound nightly - {datetime.now().strftime('%Y-%m-%d')}")
    
    # Create role directories
    for role in ROLES:
        (Path(LOOPS_LIB) / role).mkdir(parents=True, exist_ok=True)
    
    filed = {role: 0 for role in ROLES}
    skipped = []
    
    # Process temp folder: move (not copy) each file to role folder
    if TEMP_DIR.exists():
        for file in TEMP_DIR.glob("*.wav"):
            role = guess_role(file.name)
            dest = Path(LOOPS_LIB) / role / file.name
            try:
                shutil.move(str(file), str(dest))  # Move, don't copy
                filed[role] += 1
            except Exception as e:
                skipped.append(f"{file.name}: {e}")
    
    cleanup_temp()  # Remove temp folder entirely
    log_summary(datetime.now().strftime('%Y-%m-%d'), filed, skipped)

if __name__ == "__main__":
    process_downloads()
