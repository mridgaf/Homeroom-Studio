"""Drum-MIDI validity gate (Python 3.9, uses mido — already in the project venv).

Checks each .mid: at least one drum note on channel 10 (index 9), every
channel-10 note inside the GM drum range, an embedded tempo, and a time
signature. Prints a PASS/FAIL table and exits non-zero if any file fails, so
it can gate delivery.

Notes on OTHER channels are allowed and counted separately: since 2026-07-22
a "chords" beat writes harmony.py's voicings as a real polyphonic track on
channel 1 on purpose (beat_recipes.write_midi — "not 10, so Reason doesn't
read it as a drum hit"). Failing those was this gate being older than the
feature, not a bad file.

Usage:
    ./.venv/bin/python check_midi.py <file.mid | folder> [more...]
    ./.venv/bin/python check_midi.py ~/Documents/Samples/"Claude Drum Beats"
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import mido
except ImportError:
    print("mido not installed in this environment. In the project venv:")
    print('  ./.venv/bin/pip install mido')
    sys.exit(2)

GM_DRUM_MIN = 35
GM_DRUM_MAX = 81
DRUM_CHANNEL = 9  # zero-indexed channel 10


def gather(paths):
    files = []
    for p in paths:
        p = Path(p).expanduser()
        if p.is_dir():
            files.extend(sorted(p.rglob("*.mid")))
        elif p.suffix.lower() == ".mid":
            files.append(p)
    return files


def check(path):
    """Return (ok, problems[]) for one .mid file."""
    problems = []
    try:
        mid = mido.MidiFile(str(path))
    except Exception as e:  # noqa: BLE001 - report any parse failure plainly
        return False, ["won't parse: {}".format(e)]

    notes = 0            # drum notes: channel 10
    melodic = 0          # deliberate non-drum content (the chords track)
    out_of_range = 0
    has_tempo = False
    has_timesig = False

    for msg in mid:
        if msg.type == "set_tempo":
            has_tempo = True
        elif msg.type == "time_signature":
            has_timesig = True
        elif msg.type == "note_on" and msg.velocity > 0:
            if msg.channel != DRUM_CHANNEL:
                melodic += 1
                continue
            notes += 1
            if not (GM_DRUM_MIN <= msg.note <= GM_DRUM_MAX):
                out_of_range += 1

    if notes == 0:
        problems.append("no drum notes on channel 10 ({})".format(
            "{} melodic note(s) only".format(melodic) if melodic
            else "silent file"))
    if out_of_range:
        problems.append("{} note(s) outside GM drum range 35-81".format(out_of_range))
    if not has_tempo:
        problems.append("no embedded tempo")
    if not has_timesig:
        problems.append("no time signature")

    return (not problems), problems


def main(argv):
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    files = gather(args)
    if not files:
        print("No .mid files found in:", ", ".join(args))
        return 2

    failed = 0
    for f in files:
        ok, problems = check(f)
        mark = "PASS" if ok else "FAIL"
        print("{}  {}".format(mark, f.name))
        if not ok:
            failed += 1
            for pr in problems:
                print("       - {}".format(pr))

    print("\n{} file(s): {} passed, {} failed."
          .format(len(files), len(files) - failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
