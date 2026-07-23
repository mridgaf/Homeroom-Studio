---
name: safe-file-ops
description: Move-don't-delete safety pattern for any bulk file cleanup, purge, reset, "clear out", quarantine, or "collect these so I can delete them" task in this project. Use whenever a script would otherwise remove, overwrite, or mass-move the owner's beats, samples, recipes, or library files. Guarantees the operation is reversible — files go into ONE dated holding folder with a manifest, never straight to the trash. This is the house rule the existing tools/clear_junk_beats.py and tools/quarantine_banned.py already follow; match it for anything new.
---

# Safe File Ops — move, never delete

The owner is not a developer and runs these from a `.command` double-click on
a big, sometimes-flaky cloud/external drive. A destructive script that
guesses wrong is expensive and scary. So nothing this project writes ever
deletes his files. It **moves** them into one holding folder he can inspect
and trash himself. Think of it as sweeping into a labelled box, not throwing
in the bin — he decides when the box goes.

## The contract every cleanup script must honor

1. **Never call delete/unlink/rmtree on the owner's content.** Only
   `shutil.move`. The only thing a script may truncate is an append-only log
   it also snapshots first (see README.txt handling in `clear_junk_beats.py`).
2. **One dated destination**, e.g. `Cleared 2026-07-22/` or
   `_Flagged - Banned Samples/`, created under the library root — not
   scattered.
3. **Write a `manifest.txt`** in that folder recording, tab-separated, where
   every item came from (`number\trelative/original/path`). This is what makes
   the move reversible and auditable. Append with a dated header if the script
   can run more than once.
4. **`--dry-run` that moves nothing** and just lists what *would* move. Offer
   it first when unsure.
5. **Require typed `yes`** before moving (allow `--yes` to skip for power use).
   Print the count and the destination before asking.
6. **Handle name collisions** without clobbering — prefix `NN DUP ` like the
   existing scripts, never overwrite.
7. **Re-runnable and self-skipping** — skip the holding folder itself and the
   `.recipes` store on subsequent passes so it never re-moves its own output.
8. **Fail loud if the drive is missing** (`if not ROOT.exists(): print… return`)
   rather than creating an empty folder somewhere wrong. The cloud drive is
   not always mounted.

## Reuse

`scripts/safe_move.py` in this skill is a Python 3.9 helper that implements
the contract (dated folder + manifest + dry-run + typed confirm + DUP-safe).
Import it instead of re-deriving the logic:

```python
from safe_move import SafeMover
mover = SafeMover(root=ROOT, dest_label="Cleared")   # -> "Cleared 2026-07-22/"
mover.add(list_of_paths)                             # Path objects to move
mover.summary()                                      # prints count + destination
mover.run(dry_run=False, skip_confirm=False)         # asks "type yes", moves, writes manifest
```

Canonical live examples to copy from: `tools/clear_junk_beats.py` (full reset)
and `tools/quarantine_banned.py` (collect-by-criteria). If you touch either,
keep every guarantee above intact.

## Honesty

You usually can't execute the move from here — the `.venv` is macOS and this
sandbox is Linux. Syntax-check it, verify the *matching* logic read-only
against real files, and say plainly that the actual move is unverified until
he runs it on his Mac. Tell him to read the printed count before typing `yes`.
