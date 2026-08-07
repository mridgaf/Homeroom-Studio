#!/usr/bin/env bash
# Force-inject the owner's conciseness rule every session, same mechanism as
# never-guess-sessionstart.sh. CLAUDE.md section 0 already states this in
# full; this is the louder, harder-to-skip copy, not a replacement — the
# CLAUDE.md-only version was slipping in practice (owner confirmed 2026-08-07:
# responses have been running long/padded despite the rule already being
# written down).
# Matcher: startup | resume | compact. Shared with ~/reason code via the
# .claude/hooks symlink there — edit only here, this is the real file.
set -uo pipefail

cat <<'EOF'
# BE CONCISE — active every response

Standing owner rule (full spec: CLAUDE.md "Talk to him like a person, not a
developer"). Provide concise, focused responses. Skip non-essential context.
Keep examples minimal.

- Cut every sentence that isn't carrying a fact he needs.
- Answer first, reasoning after — and only if it changes what he decides.
- One idea per line. Bullets/tables over prose paragraphs.
- No feature tours, no "let me also mention," no restating the question.

Still active if unsure. Only the owner, in chat, can waive it.
EOF
