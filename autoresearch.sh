#!/bin/bash
# LOCKED EVAL HARNESS — autoresearch scores experiments/crew_config.candidate.json
# for compose-time variety. Do NOT edit during the loop.
set -euo pipefail
cd "$(dirname "$0")"
SEED="${1:-0}"
CAND="experiments/crew_config.candidate.json"
# fast pre-check: candidate must be valid JSON with the nine DJs
./.venv/bin/python - "$CAND" <<'EOF'
import json, sys
doc = json.load(open(sys.argv[1]))
djs = [k for k in doc if not k.startswith("_")]
assert len(djs) == 9, "candidate must keep all nine DJs"
EOF
# portable 300 s cap (macOS ships no `timeout`)
perl -e 'alarm 300; exec @ARGV' -- \
  ./.venv/bin/python experiments/score_variety.py "$CAND" "$SEED"
