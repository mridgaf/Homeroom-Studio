#!/bin/bash
# Correctness gate: a candidate config may only be KEPT if the engine's
# identity tests still pass WITH THAT CANDIDATE LOADED. This is what
# stops the variety metric from being gamed into chaos — style
# constraints (Cutz's backbeat, Night Metro's halftime, New Math's
# quintuplets...), the roster shape, the 808 rules, and the variety
# floors must all hold for the tuned crew.
set -euo pipefail
cd "$(dirname "$0")"
export REASON_VOICE_CONFIG="$PWD/experiments/crew_config.candidate.json"
# portable 300 s cap (macOS ships no `timeout`)
perl -e 'alarm 300; exec @ARGV' -- \
  ./.venv/bin/python -m pytest \
  tests/test_pattern_gen.py tests/test_crew.py tests/test_variety.py -q
