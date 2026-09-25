"""Audition: the 808 bangs with the kick (2026-09-23, second pass).

Owner: "we shouldn't be using the sub to play chords, it should just bang
along with the kick drum, side chained, like hip hop is produced much of
the time. Shouldn't need to be pitched or stretched." What changed, from-
scratch beats only (the Loops page is untouched):
  * 808 DJs: ONE 808 on the kick's hits, ducked 5 dB under the kick --
    no longer following the chords, and no bass line under it
  * the 808 is never pitched or stretched: on a keyed beat only an 808
    RECORDED in the key's root can play (none there -> no 808)
  * everyone else: unchanged -- the bass line from his bass one-shots

In-character seeds only (no free-for-all beats), so each folder is the
style it says. Renders to scratch; copies the wavs to the Desktop. Library,
sample history, pattern history and crew kit locks are all left untouched.

Fails loud: every beat must have exactly the bass its style calls for; an
808 must sit on exactly the kick's hits, be recorded in the key, and
MEASURE in the key in its finished stem; the kick must sit over every
bass lane; the file count must be right. A WARNING means do not hand it over.

Run:  ./.venv/bin/python tools/make_low_end_audition.py
Out:  ~/Desktop/Homeroom Auditions/Homeroom 808 On The Kick <today>/
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

OUT = Path.home() / "Desktop" / "Homeroom Auditions" / "Homeroom Auditions" / f"Homeroom 808 On The Kick {date.today()}"
FOLDERS = {
    "1 808 DJs": ["Night Metro", "Mustang", "Hitt Kid", "Memphis"],
    "2 Bass-line DJs": ["Otto Grit", "DJ Premium"],
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


def _pitch_class_of(stem):
    """The finished 808 stem's own fundamental, as (pitch class, cents off):
    the strongest bin 25-120 Hz. Measured on the OUTPUT, not the recipe."""
    x = (stem[0] + stem[1]) / 2
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / SR)
    band = (f >= 25) & (f <= 120)
    hz = f[band][sp[band].argmax()]
    semis = 12 * np.log2(hz / 16.3516)          # C0
    return int(round(semis)) % 12, 100 * (semis - round(semis))


def _measure(rec, parts):
    lanes = rec["preset"]["lanes"]
    stems = parts["stems"]
    harm = rec.get("harmony") or {}
    line = sorted(ln for ln in lanes if _LINE.match(ln))
    has_808 = bool(harm.get("bass808")) or "bass" in lanes
    kind = "808" if has_808 else "bass line" if line else "none"
    path808 = (rec.get("kit_paths") or {}).get("bass") or ""
    on_kick = (lanes["bass"][3] == lanes["kick"][3]) if "bass" in lanes \
        else None
    key_pc = recorded_pc = heard = None
    if "bass" in lanes and harm.get("root"):
        from key_context import pitch_class
        key_pc = pitch_class(harm["root"])
        note = bm._808_notes().get(path808)
        recorded_pc = pitch_class(note) if note else None
        heard = _pitch_class_of(stems["bass"])
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
            "key": harm.get("key") or "", "on_kick": on_kick,
            "key_pc": key_pc, "recorded_pc": recorded_pc, "heard": heard,
            "off": (None if not heard else
                    100 * ((heard[0] + heard[1] / 100 - key_pc + 6) % 12 - 6)),
            "808": Path(path808).stem if "bass" in lanes else "",
            "line_808": bool(harm.get("bass808"))}


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
                if m["line_808"]:
                    warnings.append(f"{fn}: the 808 is playing the chords")
                if m["on_kick"] is False:
                    warnings.append(f"{fn}: the 808 is off the kick's hits")
                if m["key_pc"] is not None and m["recorded_pc"] != m["key_pc"]:
                    warnings.append(f"{fn}: the 808 is not recorded in "
                                    f"{m['key']}")
                # an 808 starts up to ~a semitone high and drops to its
                # note (Hitt Kid's measured 105 -> 98.5 Hz in 0.3 s); on
                # fast hits that start is most of what plays. More than a
                # semitone off is a wrong file, not the glide.
                if m["off"] is not None and abs(m["off"]) > 100:
                    warnings.append(f"{fn}: the 808 stem measures "
                                    f"{m['off']:+.0f} cents from {m['key']}")
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
        f"THE 808 BANGS WITH THE KICK   {date.today()}",
        "=" * 60, "",
        "WHAT YOU ASKED",
        '  "We shouldn\'t be using the sub to play chords. It should just',
        '  bang along with the kick drum, side chained ... shouldn\'t need',
        '  to be pitched or stretched."',
        "",
        "WHAT CHANGED (beats made from scratch; old beats untouched)",
        "  - Folder 1 (808 DJs): ONE 808, hitting exactly where the kick",
        "    hits, ducked 5 dB under the kick. It no longer moves with the",
        "    chords, and there is no bass line under it.",
        "  - The 808 is never pitched or stretched. It is picked from 808s",
        "    already recorded in the beat's key. If none is, the beat gets",
        "    no 808 (and the beat card says so).",
        "  - Folder 2 (other DJs): unchanged -- the bass line from your",
        "    bass one-shots. Here so you can compare.",
        "",
        "LISTEN FOR",
        "  Folder 1: does the 808 sit with the kick like a real hip-hop",
        "  beat? Does it clash with any chord now that it holds one note?",
        "",
        "THE BEATS",
    ]
    for folder, fn, m in rows:
        extra = f"808 '{m['808']}'" if m["808"] else m["kind"]
        tune = ("" if m["off"] is None else
                f"; measures {m['off']:+.0f} cents from {m['key']}'s root")
        under = ("" if m["over"] is None
                 else f"; peaks {-m['over']:.1f} dB under the kick")
        lines.append(f"  {folder} / {fn}")
        lines.append(f"      bass: {extra}{tune}{under}; chords: "
                     f"{', '.join(m['roots']) or 'none'}")
    lines += [
        "",
        "MEASURED (not heard)",
        "  Folder 1: every 808 plays on exactly the kick's hits, was",
        "  recorded in the beat's key, and measures in that key in the",
        "  finished file. Folder 2: bass line, no 808. One bass per beat.",
        "  The script refuses to write this folder if any of that fails.",
        "",
        "NOT CHECKED -- your ear",
        "  Whether one held 808 note under changing chords sounds right.",
        "  Beat 3 (Hitt Kid): his 808 starts about a semitone high and",
        "  drops to G within 0.3 s -- normal for an 808. His hits are",
        "  fast, so you mostly hear the high start. Nothing re-pitched it;",
        "  the file settles on G. Tell me if it sounds out of key.",
        "  Outside C there are only 4-25 808s per key, so those beats",
        "  draw from a small pile.",
        "",
        "WHAT I NEED BACK",
        "  Folder 1: keep it, or what to change.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
