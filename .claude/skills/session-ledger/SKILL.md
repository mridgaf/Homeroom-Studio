---
name: session-ledger
description: Maintains a cross-session decision/outcome ledger (DECISIONS.md) so Claude doesn't repeat mistakes or forget prior reasoning between sessions, and verifies claims of "done" or "fixed" against reality before reporting them. Use this at the START of any substantive work session in a project that has a DECISIONS.md file — read it before doing anything else. Use it again at the END of a session that involved a real decision, a fix, a judgment call, or an unverified claim — append an entry. Also trigger this whenever about to report something as "fixed," "working," "done," or "resolved," even mid-session, to check whether that claim has actually been verified or is being asserted on faith.
---

# Session Ledger

Two jobs: (1) don't let claims of success go unverified, (2) don't let
sessions forget what previous sessions learned.

## At the start of a session

1. Check for `DECISIONS.md` in the project root (or wherever the project's
   `CLAUDE.md` points).
2. If it exists, read it — especially entries with `status: open` or
   `status: failed`. These are unresolved threads or known dead ends. Don't
   propose something already marked failed without acknowledging it was tried.
3. If it doesn't exist and the project seems like it'll have recurring
   sessions (multi-day project, ongoing collaboration), offer to create one
   from the template rather than assuming — don't impose it on a one-off task.

## Before claiming something is done

This is the part that matters most. Before saying "fixed," "this works,"
"done," or similar:

- If there's a mechanical way to check (run the test, run the code, reload
  the file, recompute the number) — do it. Don't infer success from writing
  the change.
- If there's no mechanical way to check (a physical repair, a piece of advice,
  a judgment call whose outcome plays out later) — say plainly that it's
  unverified, and log it as `status: open` with a note on how it could be
  checked later (by the user, next session, or never).
- Never let "should work" get reported as "works."

## During a multi-step problem: keep a live reasoning trace

The end-of-session entry in `DECISIONS.md` only captures a summary — it loses
the path: what was ruled out, what almost got concluded and got reversed. For
any problem that takes more than 2-3 steps to work through, jot short entries
to `SCRATCH.md` (template included in this kit) as you go, not just at the
end:

- One line per turning point: what was tried, what happened, what changed
  your mind. Not a full transcript — just the hinge points.
- Do this especially when you reverse course. "Tried X, didn't work, here's
  why" is exactly the thing that gets lost if only the final answer survives.
- `SCRATCH.md` is disposable/per-session. At session end, anything from it
  worth keeping long-term gets folded into the `DECISIONS.md` entry
  (particularly the `Reasoning` field) — then `SCRATCH.md` can be cleared for
  next time.

## At the end of a session

Append an entry to `DECISIONS.md` (format is at the top of that file) if the
session involved:
- a decision between real alternatives, not a trivial default
- a fix or change whose correctness isn't yet confirmed
- something that would be costly to re-litigate or re-discover next time

Skip logging for routine, low-stakes, or fully-verified-in-session work — the
ledger loses value if it's full of noise.

If an entry from a previous session can now be resolved (you verified it, the
user confirmed it, or it's since broken), update that entry's `status` and
`outcome` field in place rather than adding a duplicate.

## Failure mode to avoid

Don't turn this into busywork or a way to pad confidence. The point is
narrowly: catch claims that were never actually checked, and keep the next
session from repeating a discarded approach. If a session had nothing
decision-worthy in it, don't force an entry.
