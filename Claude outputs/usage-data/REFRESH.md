# Usage dashboard refresh (Part 1 of 1)
Owner chose MANUAL refresh (2026-11-02): only when he asks. No scheduled task.
Dashboard: https://claude.ai/artifact/CwgxrZHp6b4YQsVRJJubDu
Steps: 1) run extract.py in this folder (reads Homeroom Rhythms/.recipes + Homeroom Drum MIDI/Beats, writes usage.csv + beats.csv)
2) stage both CSVs, upload each as an artifact asset (one call each)
3) update datasets/usage and datasets/beats (source.url, updated.at; beats description count) with if_version
4) delete the old blobs. Do not touch files/index.html.
Build modes: Loops only / Original + loops / Original. "Original + loops" is always 0 (no beat mixes both).
