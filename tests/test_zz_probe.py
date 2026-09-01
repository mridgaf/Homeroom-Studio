from pathlib import Path
import pytest
from test_beat_machine import machine_env, _wav_pool          # noqa: F401
import beat_machine


def _tree(root):
    return sorted(str(f.relative_to(root)) for f in root.rglob("*")
                  if f.suffix == ".wav" or (f.is_dir() and
                                            f.name.endswith("Chunks")))


def test_triage_orphans_chunks(machine_env):
    root, shots = machine_env
    p, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(p.name.split()[0])
    r1 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["kick"])
    beat_machine.triage(no, "fav", root)
    r2 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["hat"])
    print("\nfolder1:", r1["folder"])
    print("folder2:", r2["folder"])
    print("same?", r1["folder"] == r2["folder"])
    for f in _tree(root):
        print("  ", f)


def test_rebuild_orphans_chunks(machine_env):
    root, shots = machine_env
    p, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(p.name.split()[0])
    r1 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["kick"])
    beat_machine.swap_many(no, {"kick": None}, root=root, shots=shots)
    r2 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["hat"])
    print("\nfolder1:", r1["folder"])
    print("folder2:", r2["folder"])
    print("same?", r1["folder"] == r2["folder"])
    for f in _tree(root):
        print("  ", f)


def test_error_paths(machine_env):
    root, shots = machine_env
    p, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(p.name.split()[0])
    from beat_recipes import load_recipe
    spec = sorted(load_recipe(root, no)["kit_spec"])
    print("\nlanes:", spec)
    # nothing staged at all
    for label, kw in (("nothing staged", {}),
                      ("drop everything", {"drops": spec})):
        try:
            beat_machine.save_chunk(no, root=root, shots=shots, **kw)
            print(label, "-> NO ERROR (!)")
        except Exception as e:
            print(label, "->", type(e).__name__, e)
        d = beat_machine.chunk_dir(no, root)
        print("   folder exists?", d.exists(),
              sorted(f.name for f in d.glob("*")) if d.exists() else "")


def test_naming_edges(machine_env):
    root, shots = machine_env
    p, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(p.name.split()[0])
    # trim on a lane that is also dropped: swap_many discards the trim,
    # save_chunk still counts it
    r = beat_machine.save_chunk(no, root=root, shots=shots,
                                drops=["kick"], trims={"kick": 3})
    print("\ndrop+trim same lane ->", r["file"], "|", r["changed"])
    # 0 dB trim on a valid lane alongside a drop
    r2 = beat_machine.save_chunk(no, root=root, shots=shots,
                                 drops=["snare"], trims={"hat": 0})
    print("drop + 0dB trim ->", r2["file"], "|", r2["changed"])
    # a pick equal to what's already there = not a swap for swap_many
    from beat_recipes import load_recipe
    rec = load_recipe(root, no)
    cur = rec["kit_paths"].get("hat")
    if cur:
        try:
            r3 = beat_machine.save_chunk(no, root=root, shots=shots,
                                         picks={"hat": cur},
                                         drops=["snare"])
            print("no-op pick + drop ->", r3["file"], "|", r3["changed"])
        except Exception as e:
            print("no-op pick + drop ->", type(e).__name__, e)


def test_chunk_of_a_chunk_and_renames(machine_env):
    root, shots = machine_env
    p, _ = beat_machine.generate(["Otto Grit"], root=root, shots=shots)
    no = int(p.name.split()[0])
    r1 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["kick"])
    d = Path(r1["folder"])
    (d / "notes.txt").write_text("hi")           # non-wav file
    r2 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["hat"])
    print("\nafter non-wav:", r2["file"], "count", r2["count"])
    # he renames one
    (d / "02 No Kick.wav").rename(d / "Verse.wav")
    r3 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["snare"])
    print("after rename:", r3["file"], "count", r3["count"])
    print("files:", sorted(f.name for f in d.glob("*")))
    # he deletes the middle one
    (d / "03 No Hat.wav").unlink()
    r4 = beat_machine.save_chunk(no, root=root, shots=shots, drops=["perc"]
                                 if "perc" in beat_machine.load_recipe(
                                     root, no)["kit_spec"] else ["hat"])
    print("after delete:", r4["file"], "count", r4["count"])
    print("files:", sorted(f.name for f in d.glob("*")))
