#!/bin/bash
cd "$(dirname "$0")/../.."
NO_TRANSPORT=1 ./.venv/bin/python "experiments/automation-test-2026-09-25/sweep_test.py" 2>&1 | tee "experiments/automation-test-2026-09-25/sweep_only_log.txt"
