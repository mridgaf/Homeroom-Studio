#!/usr/bin/env python3
# Select the 3 most recently created distinct versions per song; copy into stage folders.
from __future__ import annotations
import os, re, sys, hashlib, shutil, datetime
from collections import defaultdict

HOME = os.path.expanduser("~")
ROOTS = [
    f"{HOME}/Desktop/BOTC wav files",
    f"{HOME}/Desktop/botc 11 23 25",
    f"{HOME}/Desktop/botc macs",
    f"{HOME}/Desktop/Whole desktop",
    f"{HOME}/Downloads",
]
# Do NOT add "iCloud Drive (Archive) - 3/Desktop": same folder names, but strictly
# older (newest 2026-01-04 vs 2026-01-20 here) and full of dataless iCloud stubs
# (~880 bytes standing in for ~50 MB), which hash as garbage and force downloads.

# "botc" / "tbotc" / "botb" is the band name, not a song - never match it as a title.
DEST = f"{HOME}/Desktop/BOTC Library"
EXTS = {".wav", ".aif", ".aiff", ".mp3"}
KEEP = 3

# title -> regex. Order matters: first match wins.
TITLES = [
    ("Debbie",          r"debbie"),
    ("Bad Guys",        r"bad.?guys?|civil unrest|crack.rock.bad"),
    ("Mr Idgaf",        r"idgaf"),
    ("Bobby",           r"bobby|booby"),
    ("Mortal",          r"mortal"),
    ("WWJD",            r"wwjd"),
    ("Taking Over",     r"taking over|taking keep taking"),
    ("American Teens",  r"american teens"),
    ("Bang Boom Pow",   r"bang boom pow"),
    ("Alone Now",       r"alone now"),
    ("Dont Push It",    r"don'?t push it"),
    ("Mamma Said",      r"mamma said"),
    ("Can I Help You",  r"can i help you"),
]
TRACKER = {"Debbie", "Bad Guys", "Mr Idgaf", "Bobby", "Mortal", "WWJD"}

def title_of(name):
    low = name.lower()
    for t, pat in TITLES:
        if re.search(pat, low):
            return t
    return None

def stage_of(name):
    low = name.lower()
    if re.search(r"stem|hook|vocal|intro", low):      return "04 Stems"
    if re.search(r"master", low):                      return "01 Masters"
    if re.search(r"\binst\b|instrumental|linst|no ?vo?c", low): return "03 Instrumentals"
    return "02 Mixes"

STAGE_WORD = {"01 Masters": "master", "02 Mixes": "mix",
              "03 Instrumentals": "instrumental", "04 Stems": "stem"}

def sig(path):
    """size + head/tail hash: reliable for detecting byte-identical copies, cheap."""
    size = os.path.getsize(path)
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read(1 << 20))
        if size > (2 << 20):
            f.seek(-(1 << 20), os.SEEK_END)
            h.update(f.read(1 << 20))
    return (size, h.hexdigest())

def birth(path):
    st = os.stat(path)
    return getattr(st, "st_birthtime", st.st_mtime)

def main(apply_changes):
    seen = {}
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d.lower() != "archive"]
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() not in EXTS:
                    continue
                if not title_of(fn):
                    continue
                p = os.path.join(dirpath, fn)
                try:
                    s = sig(p)
                except OSError:
                    continue
                # keep the earliest-born instance of identical content
                if s not in seen or birth(p) < birth(seen[s]):
                    seen[s] = p

    songs = defaultdict(list)
    for p in seen.values():
        songs[title_of(os.path.basename(p))].append(p)

    # A bounce exported as .wav + .aif + .mp3 is ONE version, not three.
    # Collapse same-song/same-day/same-stage groups, preferring lossless.
    FMT_RANK = {".wav": 0, ".aif": 1, ".aiff": 1, ".mp3": 2}
    for t, paths in songs.items():
        groups = defaultdict(list)
        for p in paths:
            key = (datetime.date.fromtimestamp(birth(p)).isoformat(),
                   stage_of(os.path.basename(p)))
            groups[key].append(p)
        collapsed = []
        for key, g in groups.items():
            g.sort(key=lambda p: FMT_RANK.get(os.path.splitext(p)[1].lower(), 9))
            collapsed.append(g[0])
        songs[t] = collapsed

    picked, dropped = {}, {}
    for t, paths in songs.items():
        paths.sort(key=birth, reverse=True)
        picked[t] = paths[:KEEP]
        dropped[t] = paths[KEEP:]

    total_dupes = sum(1 for _ in ()) # placeholder
    lines = []
    for t in sorted(picked):
        mark = "*" if t in TRACKER else " "
        lines.append("%s %-16s (%d distinct versions, keeping %d)" % (mark, t, len(songs[t]), len(picked[t])))
        for p in picked[t]:
            d = datetime.date.fromtimestamp(birth(p)).isoformat()
            lines.append("      %s  %-18s <- %s" % (d, stage_of(os.path.basename(p)), p.replace(HOME, "~")))
    print("\n".join(lines))
    print("\n* = confirmed on tracker")
    print("distinct files: %d   songs: %d   copying: %d" %
          (len(seen), len(songs), sum(len(v) for v in picked.values())))

    if not apply_changes:
        print("\nDRY RUN - nothing written")
        return

    for sub in ["01 Masters", "02 Mixes", "03 Instrumentals", "04 Stems", "05 Archive"]:
        os.makedirs(os.path.join(DEST, sub), exist_ok=True)

    index = ["# BOTC Library", "",
             "Current best 3 versions per song, by file creation date.",
             "Originals untouched in their original folders.", ""]
    for t in sorted(picked):
        index.append("## %s%s" % (t, "" if t in TRACKER else "  (not confirmed on tracker)"))
        for p in picked[t]:
            d = datetime.date.fromtimestamp(birth(p)).isoformat()
            stage = stage_of(os.path.basename(p))
            ext = os.path.splitext(p)[1].lower()
            word = STAGE_WORD[stage]
            target = os.path.join(DEST, stage, "%s %s %s%s" % (t, d, word, ext))
            n = 2
            while os.path.exists(target):
                target = os.path.join(DEST, stage, "%s %s %s v%d%s" % (t, d, word, n, ext))
                n += 1
            shutil.copy2(p, target)
            index.append("- `%s/%s`  <- `%s`" % (stage, os.path.basename(target), p.replace(HOME, "~")))
        index.append("")
    with open(os.path.join(DEST, "INDEX.md"), "w") as f:
        f.write("\n".join(index))
    print("\nwrote %s" % DEST.replace(HOME, "~"))

if __name__ == "__main__":
    main("--apply" in sys.argv)
