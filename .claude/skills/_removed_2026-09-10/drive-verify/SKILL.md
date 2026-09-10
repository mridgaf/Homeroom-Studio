---
name: drive-verify
description: Trustworthy way to verify files exist or a backup is complete on the owner's big, slow cloud/external drives (TBOTC 3, Botc 1, ~200k files). Use whenever asked "is it all there?", "did the backup finish?", "are my Reason songs on the other drive?", or before reporting that files are missing. Prevents the classic failure — recursive searches silently time out on huge/slow drives and report false "empty" results — by checking Finder size + folder item counts instead.
---

# Drive Verify — don't trust a search on a huge slow drive

## The trap (learned the hard way, 2026-07)

On the owner's large external/cloud drives, recursive glob searches
(`DAW Projects/**/*.reason`) **silently time out and return nothing** — which
reads as "the files are missing" when they're actually there. A folder-wide
count showed 209,178 files on TBOTC 3 while a targeted search of a subfolder
came back empty seconds after the same pattern had shown it full. The tooling
was lying, not the drive. **Never raise a "backup failed / files missing"
alarm based on a recursive search of these drives.** If a targeted search
comes back empty, suspect the timeout first.

## The reliable checks (do these instead)

1. **Compare used size in Finder.** Click the source drive, press ⌘I (Get
   Info), note **Used**. Do the same on the backup drive. If the backup is
   equal-or-larger, every byte made it across. (Slightly larger is normal —
   pre-existing content or filesystem overhead.)
2. **Compare item counts on the folder that matters.** Open the specific
   folder on both drives (e.g. Reason songs) and confirm the item counts
   match. Matching counts on the folder you care about + equal-or-greater
   total size = a complete, intact backup.
3. **Spot-check openability.** Open a couple of the actual project folders on
   the backup and confirm they're there and open. If the folder you worked
   hardest on came through intact, the rest almost certainly did.

## Honesty about certainty

Matching size + item count proves the **bytes and file count** are there. It
does **not** guarantee every single file opens uncorrupted — you can have the
right total with one bad file. For that last bit of certainty, a clone app
(Carbon Copy Cloner / SuperDuper) with its verify pass checksums every file —
far more trustworthy than squinting at the drive through search tools. Say
this plainly rather than implying a search-based "all good."
