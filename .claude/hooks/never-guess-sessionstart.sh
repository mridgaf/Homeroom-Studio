#!/usr/bin/env bash
# Force-inject the owner's "never guess" rule every session, at hook-level
# salience — same delivery mechanism as the ponytail plugin. The same rule
# sitting only in CLAUDE.md kept getting missed under the weight of
# everything else there (owner's own words: "guessing is happening all the
# time"), so this exists as a second, louder copy, not a replacement.
# Matcher: startup | resume | compact. Shared with ~/reason code via the
# .claude/hooks symlink there — edit only here, this is the real file.
set -uo pipefail

cat <<'EOF'
# NEVER GUESS — active every response

Standing owner rule (full spec + incident history: CLAUDE.md "Ambiguity:
stop and ask"). If two readings of an instruction would lead to different
work, that is BLOCKING — stop and ask, even when one reading looks obvious.

- Ask with the AskUserQuestion tool. A tool call, not a question buried in
  reply text — text questions get skimmed past.
- Never ask a question and then answer it yourself in the same turn.
- Label every open point: BLOCKING (nothing proceeds without an answer) or
  ASSUMING X (proceeding on a stated reading — correct me any time).
- A plan with a "you listen here" checkpoint means stop there. The next
  step being obvious is not permission to continue past it.

Still active if unsure. Only the owner, in chat, can waive it.
EOF
