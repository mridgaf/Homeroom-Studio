"""Audition: the low end set up the way a hip-hop producer would (2026-09-23).

Owner: "set the sound up as standard hip-hop practices would go". What
changed, from-scratch beats only (the Loops page is untouched):
  * one bass per beat, by DJ style -- 808 DJs: his 808 plays the bass line,
    re-pitched onto each chord's root; everyone else: the bass line from his
    bass one-shots, no long 808
  * the kick is short whenever a bass plays; never an 808 kick on 808 beats
  * one bass note at a time (each new note cuts the last)
  * the bass line ducks under the kick as deep as the 808 (5 dB)
  * the kick stays on top of the low end even at true levels
  * chords / instruments cut below ~100-150 Hz
  * no machine-made tones (tuned sine sub, sine under the kick: gone)
  * the 808 re-pitch is in tune (Rubber Band; the old shifter ran up to
    ~3 semitones off on bass)

In-character seeds only (no free-for-all beats), so each folder is the
style it says. Renders to scratch; copies the wavs to the Desktop. Library,
sample history, pattern history and crew kit locks are all left untouched.

Fails loud: every beat must have exactly the bass its style calls for, the
kick must sit over every bass lane, the chord stems must be cut under the
bass, and the file count must be right. A WARNING means do not hand it over.

Run:  ./.venv/bin/python tools/make_low_end_audition.py
Out:  ~/Desktop/Homeroom Low End <today>/
"""
import random
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR
from make_drum_beats import build_shots
import beat_machine as bm
import beat_recipes
import crew
import pattern_gen

OUT = Path.home() / "Desktop" / f"Homeroom Low End {date.today()}"
FOLDERS = {
    "1 808 DJs": ["Night Metro", "Mustang", "Hitt Kid", "Memphis"],
    "2 Bass-line DJs": ["Otto Grit", "DJ Premium", "Doc Day", "No Alias"],
}
_LINE = re.compile(r"bass\d+$")

_real_render = bm.render_crew_beat
_parts = {}


def _keep_parts(name, kit, **kw):
    out = _real_render(name, kit, **kw)
    _parts["last"] = out[3] if len(out) > 3 else None
    return out


def _seed_in_character(start):
    """A seed whose beat is NOT a free-for-all beat."""
    s = start
    while True:
        random.seed(s)
        if not pattern_gen.free_beat(random.randrange(2, 10000)):
            return s
        s += 1


def _pk(stem):
    return float(np.abs(np.stack(stem)).max())


def _measure(rec, parts):
    lanes = rec["preset"]["lanes"]
    stems = parts["stems"]
    harm = rec.get("harmony") or {}
    line = sorted(ln for ln in lanes if _LINE.match(ln))
    has_808 = bool(harm.get("bass808")) or "bass" in lanes
    kind = "808" if has_808 else "bass line" if line else "none"
    two = ("bass" in lanes and bool(line)) or "sub" in lanes
    kick = _pk(stems["kick"]) if "kick" in stems else 0.0
    low = [ln for ln in stems if ln == "bass" or _LINE.match(ln)]
    over = max((20 * np.log10(_pk(stems[ln]) / kick)
                for ln in low if kick > 0 and _pk(stems[ln]) > 0),
               default=None)
    cut = []
    for ln, st in stems.items():
        if not ln.startswith("chord"):
            continue
        x = (st[0] + st[1]) / 2
        sp = np.abs(np.fft.rfft(x)) ** 2
        f = np.fft.rfftfreq(len(x), 1 / SR)
        tot = sp.sum()
        if tot > 0:
            cut.append(10 * np.log10(sp[f < 80].sum() / tot + 1e-30))
    roots = [c["chord"] for c in harm.get("chords", [])]
    return {"kind": kind, "two": two, "over": over,
            "chord_lows": max(cut) if cut else None, "roots": roots,
            "808": Path(harm["bass808"]).stem if harm.get("bass808") else ""}


def main():
    scratch = Path(tempfile.mkdtemp(prefix="low-end-"))
    root = scratch / "beats"
    root.mkdir()
    beat_recipes.HIST = scratch / "sample_history.json"
    pattern_gen.PAT_HIST = scratch / "pattern_history.json"
    if crew.LOCK.exists():
        shutil.copy2(crew.LOCK, scratch / "crew_kits.json")
    crew.LOCK = scratch / "crew_kits.json"
    bm.render_crew_beat = _keep_parts
    print("Scanning library for one-shots…")
    shots = build_shots()

    rows, warnings, n = [], [], 0
    try:
        for folder, names in FOLDERS.items():
            want = "808" if folder.startswith("1") else "bass line"
            (scratch / folder).mkdir()
            for name in names:
                n += 1
                random.seed(_seed_in_character(7000 + 100 * n))
                path, report = bm.generate([name], root=root, shots=shots)
                rec = beat_recipes.load_recipe(root,
                                               int(path.name.split()[0]))
                m = _measure(rec, _parts["last"])
                fn = f"{n} {name} {rec['preset']['bpm']}bpm.wav"
                shutil.copy2(path, scratch / folder / fn)
                rows.append((folder, fn, m))
                print(f"  {fn:34s} {m['kind']:9s} kick-over-bass "
                      f"{m['over'] if m['over'] is None else round(-m['over'], 1)}"
                      f" dB  chord lows {m['chord_lows'] and round(m['chord_lows'], 1)}")
                if m["kind"] != want:
                    warnings.append(f"{fn}: wanted {want}, got {m['kind']}")
                if m["two"]:
                    warnings.append(f"{fn}: TWO basses")
                if m["over"] is not None and m["over"] > crew.LOW_END_UNDER_DB + 0.1:
                    warnings.append(f"{fn}: a bass is {m['over']:+.1f} dB "
                                    "against the kick")
                if m["chord_lows"] is not None and m["chord_lows"] > -20:
                    warnings.append(f"{fn}: chords not cut under the bass "
                                    f"({m['chord_lows']:.1f} dB below 80 Hz)")
    finally:
        bm.render_crew_beat = _real_render

    got = len(list(scratch.glob("*/*.wav")))
    if got != sum(len(v) for v in FOLDERS.values()):
        warnings.append(f"expected {sum(len(v) for v in FOLDERS.values())} "
                        f"files, got {got}")
    if warnings:
        print("\nWARNING — do not hand this batch over:")
        for w in warnings:
            print("  " + w)
        print(f"(scratch kept at {scratch})")
        sys.exit(1)

    if OUT.exists():
        shutil.rmtree(OUT)              # only ever this script's own folder
    for folder in FOLDERS:
        shutil.copytree(scratch / folder, OUT / folder)
    (OUT / "READ ME.txt").write_text(readme(rows))
    shutil.rmtree(scratch)
    print(f"\n{len(list(OUT.glob('*/*.wav')))} files -> {OUT}")


def readme(rows):
    lines = [
        f"THE LOW END, SET UP LIKE A PRODUCER WOULD   {date.today()}",
        "=" * 60, "",
        "WHAT YOU ASKED",
        '  "Set the sound up as standard hip-hop practices would go" --',
        "  kick, 808 and bass working together the way a producer who",
        "  knows what they're doing would have them. Loops page untouched.",
        "",
        "WHAT CHANGED (every beat made from scratch)",
        "  - ONE bass per beat, by DJ style. Folder 1: the 808 IS the bass",
        "    line -- your 808, moved onto each chord's note. Folder 2: your",
        "    bass one-shots play the line, and there is no long 808.",
        "  - The kick is always short and punchy when a bass plays. On 808",
        "    beats the kick never comes from the 808 pile (no more 'kick",
        "    drum AND bass drum' stacked).",
        "  - One bass note at a time: each new note cuts the last one off.",
        "  - The bass line now ducks under the kick as deep as the 808.",
        "  - The kick stays on top of the low end, even at true levels.",
        "  - Chords and instruments are cut below the bass (under ~100-150",
        "    Hz), so the bass owns the bottom.",
        "  - No machine-made tones: the tuned sine sub and the sine layered",
        "    into Otto Grit's and Doc Day's kick are gone.",
        "  - The 808 is IN TUNE now. The old way of moving an 808 to a new",
        "    note was off by about a quarter of a semitone on average and",
        "    up to almost 3 semitones on some. Fixed.",
        "  - The track name 'bass drum' is now '808'.",
        "",
        "LISTEN FOR",
        "  Folder 1: does the 808 follow the chords and sound in tune? Is",
        "  the kick still clear on top of it?",
        "  Folder 2: does the bass line sit under the kick without mud? Do",
        "  the chords sound thinner than you want now that their bottom",
        "  is cut?",
        "",
        "THE BEATS",
    ]
    for folder, fn, m in rows:
        extra = f"808 '{m['808']}'" if m["808"] else m["kind"]
        lines.append(f"  {folder} / {fn}")
        under = ("" if m["over"] is None
                 else f"; peaks {-m['over']:.1f} dB under the kick")
        lines.append(f"      bass: {extra}{under}; chords: "
                     f"{', '.join(m['roots']) or 'none'}")
    lines += [
        "",
        "MEASURED (not heard)",
        "  Every beat: exactly one bass, of the kind its folder says.",
        "  Every bass lane peaks under the kick -- but by very different"
        "  amounts (listed per beat above). A long 808 has a lower peak"
        "  than a kick for the same loudness, so a big number is not"
        "  automatically too quiet. If one sounds too quiet, say which.",
        "  Every chord lane has",
        "  almost nothing left below 80 Hz. The script refuses to write",
        "  this folder if any of that fails.",
        "",
        "NOT CHECKED -- your ear",
        "  Whether the 808 following the chords feels right for each DJ,",
        "  whether the 120 Hz chord cut is too much or too little, and",
        "  whether the short kick takes away weight you liked. The duck",
        "  timing (90 ms) was left as it was.",
        "",
        "WHAT I NEED BACK",
        "  For each folder: keep it, or what to change.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
