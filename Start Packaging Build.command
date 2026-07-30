#!/bin/bash
# Double-click me to hand the packaging job to Claude Code.
#
# What this does, so it's not a mystery box:
#   1. moves into this project folder
#   2. pulls the kickoff message out of HANDOFF-TO-CODE-PACKAGING.md
#      (so there's ONE copy of it — edit the .md, this follows)
#   3. copies it to the clipboard as a backup
#   4. starts Claude Code with it already asked
#
# If anything here fails it says so in plain words and stops. It never
# guesses.

cd "$(dirname "$0")" || exit 1

BRIEF="HANDOFF-TO-CODE-PACKAGING.md"

if [ ! -f "$BRIEF" ]; then
  echo
  echo "Can't find $BRIEF in this folder."
  echo "This launcher has to sit next to it. Nothing was started."
  echo
  read -p "Press Return to close."
  exit 1
fi

# Pull the block quoted with "> " under the Kickoff message heading.
PROMPT=$(sed -n '/^## Kickoff message/,/^## /p' "$BRIEF" \
         | sed -n 's/^> \{0,1\}//p')

if [ -z "$PROMPT" ]; then
  echo
  echo "Found $BRIEF but couldn't read the kickoff block out of it."
  echo "(The block is the part quoted with '>' under '## Kickoff message'.)"
  echo "Nothing was started."
  echo
  read -p "Press Return to close."
  exit 1
fi

# Backup: it's on the clipboard either way, so you can always paste it
# by hand if the automatic hand-off doesn't take.
printf '%s' "$PROMPT" | pbcopy 2>/dev/null \
  && echo "(The kickoff message is also on your clipboard — Cmd+V if needed.)"

# Find Claude Code. A double-clicked .command starts a bare shell that does
# NOT load ~/.zshrc or ~/.bash_profile, so `command -v claude` can come up
# empty even when it's installed fine. Look in the usual places too.
# (2026-07-25: this is exactly what bit the first version of this script.)
CLAUDE=""
if command -v claude >/dev/null 2>&1; then
  CLAUDE="$(command -v claude)"
else
  for c in "$HOME/.local/bin/claude" \
           "/opt/homebrew/bin/claude" \
           "/usr/local/bin/claude" \
           "$HOME/.claude/local/claude" \
           "$HOME/bin/claude"; do
    if [ -x "$c" ]; then CLAUDE="$c"; break; fi
  done
fi

if [ -z "$CLAUDE" ]; then
  echo
  echo "Couldn't find Claude Code on this Mac. Two possibilities:"
  echo
  echo "  1. It isn't installed. To install it, paste this in Terminal:"
  echo "       curl -fsSL https://claude.ai/install.sh | bash"
  echo
  echo "  2. It IS installed somewhere this script doesn't look. To find out,"
  echo "     paste this in Terminal and tell me what it prints:"
  echo "       which claude; ls ~/.local/bin/claude 2>/dev/null"
  echo
  echo "Either way, your kickoff message is on the clipboard — you can open"
  echo "Claude Code yourself and paste it. Nothing was started."
  echo
  read -p "Press Return to close."
  exit 1
fi

echo
echo "Starting Claude Code in: $(pwd)"
echo "Using: $CLAUDE"
echo "Job: the packaging punch list, step 0 first."
echo "Remember: one step at a time, and don't let it batch them."
echo

exec "$CLAUDE" "$PROMPT"
