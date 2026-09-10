---
name: project-brief
description: Generate or update a dense handoff brief (a CLAUDE.md) that distills a project so a fresh session — this app or Claude Code — starts fully informed instead of re-deriving context. Use when the owner says "write this up for Claude Code", "make a handoff", "describe this project so I can hand it off", "update the brief", or when kicking a body of work over to another tool. Produces the four load-bearing sections — hard rules, what works / do-not-touch, current state, and machine/gear facts.
---

# Project Brief generator

The owner repeatedly hands work to Claude Code and doesn't want to re-explain
the project each time. A good brief is a dense fact sheet the next session
reads on its own — named `CLAUDE.md` so Claude Code loads it automatically
when placed in the project folder. It carries context so the receiving model
spends its tokens on the task, not on rediscovery.

The existing `CLAUDE.md` at the project root is the exemplar — match its
shape and density.

## What every brief must contain

1. **What this is** — one paragraph: what the project does and the end goal
   he was aiming for, in plain language.
2. **Owner & machine facts (do not rediscover)** — the constraints that waste
   time when relearned: system Python 3.9 (no 3.10+ syntax), quote paths with
   spaces, bash not zsh, the cloud/external drive reality, that he is not a
   developer and needs single paste-able commands or double-clickable files.
3. **Architecture that WORKS — keep these layers / DO NOT TOUCH** — the parts
   that were painful to get right (e.g. the Reason Remote bridge that took
   four tries) and must not be rewritten. Be specific about why.
4. **Current state** — what's done, what's queued, what's theoretical vs
   tested, so the next session doesn't redo finished work.
5. **Working rules** — verify before claiming done; use DECISIONS.md as
   cross-session memory; keep explanations plain and short.

## Workflow

1. Read the current `CLAUDE.md`, `DECISIONS.md`, and any relevant config
   before writing — build the brief from what's true now, not memory.
2. Write it as `CLAUDE.md` (or a dated copy if he wants to preserve the old
   one). Keep it terse — hard rules and facts, not prose padding.
3. Give him the one-step handoff: the file goes in the project folder, then
   in the Claude Code tab he picks that folder and says "Read CLAUDE.md, then
   <task>. Don't touch <the do-not-touch layer>."
4. If handing to Claude Code, remind him it shares the same subscription
   usage — it's a fresh focused session, not extra capacity.

## Honesty

A brief is only as current as the moment you wrote it. Flag anything you're
unsure is still true rather than freezing a guess into the file, and update
old entries when the state changes instead of stacking new ones.
