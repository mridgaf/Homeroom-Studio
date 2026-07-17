# Crew tuning proposal — awaiting your ears

The autoresearch loop tuned a COPY of the roster. Your live
`crew_config.json` has not moved. This file says what won and how to
audition it.

## What the winner changes (one change so far, 8 runs in)

**Night Metro, Rage Engine, and New Math dig the record crates more**
— their groove-library seed chance rises 0.35/0.35/0.40 → 0.50/0.50/0.55.

Why: these three were the DJs whose recent rendered beats clustered
(kick lines within 1-2 moves — the variety scorer caught it). Their
halftime/wall grammars have the fewest legal kick placements, so their
own freestyle rolls repeat; seeding more beats from trap/drill/garage
reference grooves breaks the cluster. Numerically: variety 13.53 →
14.07 (+4%), the weakest DJ's score up the same, and all 44 identity
tests still pass with the tuned roster loaded.

Also learned (and NOT applied): raising the same knob for the other six
DJs made variety WORSE — their genre pools are smaller, so seeds repeat
and their own grammars are richer. The tuning is trap-trio-only.

## How to audition it

Render a scratch batch from the proposed roster (nothing touches your
library or the live config):

    cd "$HOME/Music/Reason 12/reason-voice 3"
    REASON_VOICE_CONFIG="$PWD/crew_config.proposed.json" \
      ./.venv/bin/python tools/beat_machine.py \
      --render "Night Metro" --count 3 --out "$HOME/Desktop/Audition Batch"

(repeat for Rage Engine and New Math). If your ears approve:

    cp crew_config.proposed.json crew_config.json

If not, say what's off — the loop keeps tuning with your verdict as a
constraint, or the proposal just gets deleted.

## APPROVED 2026-07-17
Owner auditioned beats 86-88 (Audition Batch) and approved. The change
is live in crew_config.json and journaled per DJ (rollback-able with
`tools/evolution.py --rollback "<Name>"` like any evolution).
