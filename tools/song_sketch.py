"""Song Sketch: turn one finished beat into a four-section arrangement.

Ported 2026-10-16 from the ChatGPT "Beat Lab Codex" experiment. The DSP is
song_sketch_dsp.py (unchanged). This file is the Homeroom side: it reads a
beat's stems, never touches them, and writes the result to
~/Desktop/Homeroom Auditions/Song Sketches/ so his library numbering is
never disturbed (house rule 0f).

Nothing here imports beat_machine (it often runs as __main__, so importing
it would load a second copy). The server hands in what it already knows.
"""
from __future__ import annotations

import json
import re
import zipfile
from datetime import datetime
from pathlib import Path

import numpy as np

import song_sketch_dsp as dsp
from make_drum_loops import SR, write_wav24

OUT_ROOT = Path.home() / "Desktop" / "Homeroom Auditions" / "Song Sketches"
FILES = {"sketch.wav": "audio/wav", "original.wav": "audio/wav",
         "stems-and-mix.zip": "application/zip",
         "recipe.json": "application/json"}
_ID = re.compile(r"^Beat \d+ \d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.\d{2}$")


def options():
    """What the page needs to draw its choices."""
    return {"roles": list(dsp.ROLES),
            "scenes": {k: {"name": v["name"], "description": v["description"]}
                       for k, v in dsp.SCENES.items()},
            "moves": dsp.MOVES,
            "presets": dsp.PRESETS}


def rows_for(rows):
    """Rack rows -> sketch stems. A row with no stem wav can't be played, and
    the DJ's producer tag (stamp) is left out so it isn't repeated every
    section."""
    out = []
    for r in rows:
        lane = r["lane"]
        if not r.get("stem") or lane.startswith("stamp"):
            continue
        out.append({"lane": lane, "label": r["label"],
                    "role": dsp.guess_role(f"{lane} {r['label']}")})
    return out


def build(no, bpm, rows, solo_audio, recipe, root=None):
    """Render the sketch. `rows` come from rows_for(); solo_audio(lane)
    returns that row's (L, R). Returns the saved folder's id + metadata."""
    lanes = [r["lane"] for r in rows]
    channels = {}
    for r in rows:
        got = solo_audio(r["lane"])
        if got is None:
            raise ValueError("No stem file for %s." % r["label"])
        channels[r["lane"]] = {"dry": (np.asarray(got[0], dtype=np.float32),
                                       np.asarray(got[1], dtype=np.float32)),
                               "sr": SR}
    recipe = dict(recipe)
    recipe["bpm"] = recipe.get("bpm") or bpm
    recipe["roles"] = {k: v for k, v in (recipe.get("roles") or {}).items()
                       if k in lanes}
    stems, mix, original, meta = dsp.render(channels, recipe)
    clean = dsp.validate_recipe(recipe, lanes, bpm)
    label = {r["lane"]: r["label"] for r in rows}
    root = Path(root or OUT_ROOT)
    token = "Beat %d %s" % (int(no), datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
    folder = root / token
    (folder / "stems").mkdir(parents=True)
    write_wav24(folder / "sketch.wav", mix[:, 0], mix[:, 1])
    write_wav24(folder / "original.wav", original[:, 0], original[:, 1])
    files = []
    for i, (lane, audio) in enumerate(stems.items(), 1):
        name = label.get(lane, lane)
        safe = re.sub(r"[^\w .()-]", "_", name)[:80].strip() or "stem"
        rel = "stems/%02d %s.wav" % (i, safe)
        write_wav24(folder / rel, audio[:, 0], audio[:, 1])
        files.append({"lane": lane, "file": rel})
    manifest = dict(beat=int(no), created=datetime.now().isoformat(timespec="seconds"),
                    recipe=clean, stem_files=files, **meta)
    (folder / "recipe.json").write_text(json.dumps(manifest, indent=1))
    (folder / "READ ME.txt").write_text(
        "HOMEROOM STUDIO / SONG SKETCH - beat %d\n"
        "%g BPM, 4/4, %d bars per section, 4 sections + %gs tail.\n\n"
        "sketch.wav is the arrangement. original.wav is the same beat looped, "
        "at the same level, for A/B.\n"
        "Drop ALL the stems into your DAW at time zero, unity gain, no "
        "normalising: they add up to sketch.wav. The echo/reverb return is "
        "its own stem.\n"
        "Pitch and speed are untouched. Mixer effects are not included.\n"
        "Echo exit: last beat feeds dotted-eighth repeats. Space bloom: last "
        "bar feeds a rising reverb. Drum breath: half a beat of silence.\n"
        % (int(no), clean["bpm"], clean["section_bars"], meta["tail_s"]))
    with zipfile.ZipFile(folder / "stems-and-mix.zip", "w",
                         compression=zipfile.ZIP_STORED) as z:
        for f in sorted(folder.rglob("*")):
            if f.is_file() and f.suffix != ".zip":
                z.write(f, f.relative_to(folder))
    return {"id": token, "folder": str(folder), "meta": meta}


def file_path(token, name, root=None):
    """Resolve a (token, name) from the browser to a real file, or None.
    Both are checked against fixed patterns, so no path ever comes from the
    client."""
    if not _ID.match(token or "") or name not in FILES:
        return None
    p = Path(root or OUT_ROOT) / token / name
    return p if p.is_file() else None
