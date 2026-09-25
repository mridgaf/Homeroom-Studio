---
name: safe-file-ops
description: Move-don't-delete safety pattern for any bulk file cleanup, purge, reset, "clear out", quarantine, or "collect these so I can delete them" task in this project. Use whenever a script would otherwise remove, overwrite, or mass-move the owner's beats, samples, recipes, or library files. Guarantees the operation is reversible — files go into ONE dated holding folder with a manifest, never straight to the trash. This is the house rule the existing tools/clear_junk_beats.py and tools/quarantine_banned.py already follow; match it for anything new.
---

# Safe File Ops — move, never delete (by default)

The owner is not a developer and runs these from a `.command` double-click on
a big, sometimes-flaky cloud/external drive. A destructive script that
guesses wrong is expensive and scary. So nothing this project writes ever
GUESSES its way into deleting his files. The default move is to **move**
suspect files into one holding folder he can inspect and trash himself.
Think of it as sweeping into a labelled box, not throwing in the bin — by
default, he decides when the box goes.

## The contract every cleanup script must honor

1. **Never call delete/unlink/rmtree on the owner's content on your own
   initiative or from a heuristic guess.** Only `shutil.move` (or `mv`) for
   anything a script or classifier decided was junk/unkeyed/misfiled. The
   only thing a script may truncate is an append-only log it also snapshots
   first (see README.txt handling in `clear_junk_beats.py`).
2. **One dated destination**, e.g. `Cleared 2026-07-22/` or
   `_Flagged - Banned Samples/` or `_Needs Key/` — created under the library
   root, not scattered.
3. **Write a `manifest.txt`** (or a short README, for a one-off interactive
   holding folder) in that folder recording where every item came from and
   why it's there. This is what makes the move reversible and auditable.
   Append with a dated header if the script can run more than once.
4. **`--dry-run` that moves nothing** and just lists what *would* move.
   Offer it first when unsure.
5. **Require typed `yes`** before moving (allow `--yes` to skip for power
   use). Print the count and the destination before asking.
   When Claude runs the move itself (the default — owner hard rule
   2026-09-25: if Claude can do it, Claude does it), ask ONE clickable
   yes/no with the count and destination, then run with `--yes`. Do not
   hand him the `.command` to double-click.
6. **Handle name collisions** without clobbering — prefix `NN DUP ` like the
   existing scripts (or `mv -n` for an ad hoc interactive move), never
   overwrite.
7. **Re-runnable and self-skipping** — skip the holding folder itself and
   the `.recipes` store on subsequent passes so it never re-moves its own
   output.
8. **Fail loud if the drive is missing** (`if not ROOT.exists(): print…
   return`) rather than creating an empty folder somewhere wrong. The cloud
   drive is not always mounted.

## When the owner himself says "delete it" — that's not a guess, honor it

Everything above is about a SCRIPT OR CLASSIFIER deciding what's junk —
that's a guess, and guesses that delete are too expensive to risk. It's a
completely different situation when the owner has just been shown a
specific, named holding folder (one you or he created) and directly says to
delete it ("delete this folder and everything in it, I don't want them").
That's not a guess — he looked at exactly what's there and made the call
himself. In that case:

- Don't re-route it into yet another holding folder, ask him to confirm
  again beyond what he already said, or otherwise soften an instruction
  that was already explicit and specific.
- On this project's device-bridge tools, deleting inside a connected folder
  is gated behind its own live permission prompt
  (`device_request_delete_permission`) that only fires when a person is
  actually there to answer it — that IS the "require typed yes" gate for an
  interactive session; you don't need a second one on top of it.
- Actually delete only what he named (the specific folder/files), verify
  it's gone, and log it in DECISIONS.md same as any other real decision —
  don't let an explicit delete go unlogged just because it's simple.
- This came up concretely on 2026-09-18: an unkeyed-loops holding folder
  (`_Needs Key`, built per this skill's pattern) was deleted outright on the
  owner's direct request minutes after being created. Freshly-downloaded
  web loops he decided he didn't want are exactly the kind of low-stakes
  content where "just delete it" is a normal, legitimate answer — don't
  treat it as a red flag or push back looking for a softer alternative.

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
he runs it on his Mac. Tell him to read the printed count before typing
`yes`. (This caveat is about the project's own Python tooling running
headless — an interactive session working through the device bridge, as in
the 2026-09-18 example above, can and should actually perform the
move/delete itself rather than handing back a script.)
