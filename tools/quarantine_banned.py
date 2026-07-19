"""Collect every beat that used a banned sample into ONE folder so the
owner can delete them in a single drag (owner 2026-07-18: "any song that
used that sound should be collected in the same folder so it's easy for
me to delete").

Which sounds are banned lives in banned_samples.json (repo root), matched
as case-insensitive substrings — so one entry "Bang boom Pow" catches
every date/master variant of that band song.

A beat is flagged if EITHER record says it used a banned sample:
  - its recipe  (.recipes/NN.json -> kit_paths + stamp_paths), reliable
    for beats made since 2026-07-16;
  - the README.txt source log, for everything older (resolved to a
    numbered file on disk by the inline number, or by title + bpm).

For each flagged beat the WAV, its .mid, and its "NN … Stems" folder are
MOVED into "_Flagged - Banned Samples/" under the beats root. Nothing is
deleted: a manifest.txt records where every item came from, so the move
is fully reversible, and deleting the folder is the owner's call. Safe to
re-run — add names to banned_samples.json and run it again.

Usage:  ./.venv/bin/python tools/quarantine_banned.py [--dry-run]
"""
import re
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
from make_drum_beats import banned_substrings, is_banned

ROOT = Path("~/Documents/Samples/Claude Drum Beats").expanduser()
DEST_NAME = "_Flagged - Banned Samples"
NUM_RE = re.compile(r"^(\d+) ")


def beat_number(name):
    m = NUM_RE.match(name)
    return int(m.group(1)) if m else None


def index_on_disk(dest):
    """number -> {"wavs":[], "mids":[], "stems":[]}, skipping the quarantine
    folder and the recipe store."""
    idx = {}
    for p in ROOT.iterdir():
        if p.name in (DEST_NAME, ".recipes") or not p.is_dir():
            continue
        for f in p.rglob("*"):
            if dest in f.parents:
                continue
            no = beat_number(f.name)
            if no is None:
                continue
            slot = idx.setdefault(no, {"wavs": [], "mids": [], "stems": []})
            if f.is_dir() and f.name.endswith("Stems"):
                slot["stems"].append(f)
            elif f.suffix == ".wav":
                slot["wavs"].append(f)
            elif f.suffix == ".mid":
                slot["mids"].append(f)
    return idx


def flag_from_recipes(banned):
    """number -> offending sample name, from recipe kit/stamp paths."""
    flagged = {}
    rdir = ROOT / ".recipes"
    for jf in sorted(rdir.glob("*.json")) if rdir.exists() else []:
        if not jf.stem.isdigit():
            continue
        try:
            data = json.loads(jf.read_text())
        except (OSError, ValueError):
            continue
        paths = {}
        paths.update(data.get("kit_paths", {}))
        paths.update(data.get("stamp_paths", {}))
        for src in paths.values():
            if src and is_banned(src, banned):
                flagged[int(jf.stem)] = src           # full path
                break
    return flagged


def why_str(offending, banned):
    """Readable 'what it used': the file name, plus its parent folder when
    the name alone doesn't show the banned word (the Ableton session
    slices are named 0004 2-Audio.wav but live in a bang-boom-pow folder)."""
    p = Path(offending)
    if any(b in p.name.lower() for b in banned):
        return p.name
    return f"{p.name}  (from {p.parent.name}/)"


SRC_RE = re.compile(r"^\s+([A-Za-z][\w]*)(?: now)?:\s*(.+?)\s*$")
NEW_HEAD_RE = re.compile(r"^(\d+) .+\.wav\s+->")
OLD_HEAD_RE = re.compile(r"^(.+?) \((\d+)bpm\)\s*[—-]\s*$")


def flag_from_readme(banned, disk):
    """number -> offending sample name, parsed from README.txt blocks."""
    flagged = {}
    readme = ROOT / "README.txt"
    if not readme.exists():
        return flagged
    cur_no = cur_title = cur_bpm = None
    hit = None

    def resolve(no, title, bpm):
        if no is not None:
            return no
        if not title:
            return None
        tl, want = title.lower(), f"{bpm}bpm"
        for n, slot in disk.items():
            for w in slot["wavs"]:
                nm = w.name.lower()
                if tl in nm and want in nm:
                    return n
        return None

    def close(no, title, bpm, hit):
        if hit is None:
            return
        n = resolve(no, title, bpm)
        if n is not None and n not in flagged:
            flagged[n] = hit

    for line in readme.read_text(errors="replace").splitlines():
        mnew = NEW_HEAD_RE.match(line)
        mold = OLD_HEAD_RE.match(line)
        if mnew or mold:
            close(cur_no, cur_title, cur_bpm, hit)
            hit = None
            if mnew:
                cur_no, cur_title, cur_bpm = int(mnew.group(1)), None, None
            else:
                cur_no = None
                cur_title, cur_bpm = mold.group(1).strip(), mold.group(2)
            continue
        ms = SRC_RE.match(line)
        if ms and hit is None:
            val = ms.group(2).split(" | ")[0]
            if is_banned(val, banned):
                hit = val
    close(cur_no, cur_title, cur_bpm, hit)
    return flagged


def main():
    dry = "--dry-run" in sys.argv
    banned = banned_substrings()
    if not banned:
        print("banned_samples.json is empty — nothing to collect.")
        return
    dest = ROOT / DEST_NAME
    disk = index_on_disk(dest)

    flagged = {}
    for no, name in flag_from_recipes(banned).items():
        flagged.setdefault(no, name)
    for no, name in flag_from_readme(banned, disk).items():
        flagged.setdefault(no, name)

    print(f"Blocklist: {', '.join(banned)}")
    print(f"{len(flagged)} beat(s) used a banned sample.\n")
    if not flagged:
        return

    moved, missing, rows = 0, [], []
    for no in sorted(flagged):
        slot = disk.get(no)
        if not slot or not (slot["wavs"] or slot["stems"] or slot["mids"]):
            missing.append(no)
            continue
        items = slot["wavs"] + slot["mids"] + slot["stems"]
        label = (slot["wavs"] or slot["stems"] or slot["mids"])[0].name
        why = why_str(flagged[no], banned)
        print(f"  {no:>3}  {label}")
        print(f"       used: {why}")
        for f in items:
            rows.append((no, why, str(f.relative_to(ROOT))))
            if not dry:
                dest.mkdir(parents=True, exist_ok=True)
                target = dest / f.name
                if target.exists():
                    target = dest / f"{no} DUP {f.name}"
                shutil.move(str(f), str(target))
                moved += 1

    if missing:
        print(f"\n  (no files on disk for beat #: "
              f"{', '.join(map(str, missing))} — already gone)")

    if dry:
        print(f"\nDRY RUN — would move {len(rows)} item(s) into "
              f"{dest.name}/. Re-run without --dry-run to do it.")
        return

    manifest = dest / "manifest.txt"
    with manifest.open("a") as m:
        m.write(f"\n# collected {datetime.now():%Y-%m-%d %H:%M} "
                f"(blocklist: {', '.join(banned)})\n")
        for no, why, rel in rows:
            m.write(f"{no}\t{why}\t{rel}\n")
    print(f"\nMoved {moved} item(s) into {dest.name}/  "
          f"(covering {len(flagged) - len(missing)} beats).")
    print(f"Manifest: {manifest}")
    print("Delete that folder whenever you're ready — nothing else "
          "references it.")


if __name__ == "__main__":
    main()
