#!/usr/bin/env bash
# Force-inject the owner's Sound Engine / audio-engine quality-loop rule
# every session, same mechanism as never-guess-sessionstart.sh and
# be-concise-sessionstart.sh. CLAUDE.md's "Sound Engine — quality loop"
# section has the full detail; this is the louder, harder-to-skip copy,
# not a replacement — the CLAUDE.md-only version wasn't enough (2026-08-09:
# a session ran the build-review-fix loop but skipped the required second
# re-review pass until the owner asked directly; that second pass then
# found 4 real bugs the first pass missed).
# Matcher: startup | resume | compact. Shared with ~/reason code via the
# .claude/hooks symlink there — edit only here, this is the real file.
set -uo pipefail

cat <<'EOF'
# AUDIO ENGINE QUALITY LOOP — active every response touching Sound Engine / audio-engine work

Standing owner rule (full spec: CLAUDE.md "Sound Engine — quality loop").
Before calling ANY audio-engine or Sound Engine work done, state out loud:

- **The loop ran in full**: build -> harsh-critic review -> fix -> a
  SECOND adversarial re-review by a fresh subagent -> confirm. One review
  pass is HALF the loop — work is not done until the second pass has run
  and come back clean, even when the first pass already found and fixed
  something.
- **Quality bar is production-grade**, not "it ran once." Every "done"
  claim needs the specific regression test for what was fixed AND a full
  project test-suite run, not just the touched file.
- **State current scope** before starting: which task/phase of
  docs/superpowers/plans/2026-08-08-sound-engine-mixer.md this touches,
  and what's already done vs. not started.

Still active if unsure. Only the owner, in chat, can waive it.
EOF
