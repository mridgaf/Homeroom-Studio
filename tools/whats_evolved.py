"""What did the beat engine change about itself today?

tools/evolution.py makes ONE bounded change per DJ, the first time that
DJ is featured in a day, and writes it straight into crew_config.json —
a TRACKED file. So `git status` comes back dirty after he makes beats,
every time, by design.

This answers the only question that matters when that happens: is this
diff the engine, or did a person edit the config? Every value the engine
touched today prints here with its old -> new. Anything in the diff that
is NOT in this output was edited by a person.

Built 2026-09-04, after the same benign diff was reported as a problem
twice in one session. See the `expected-churn` skill.

    ./.venv/bin/python tools/whats_evolved.py

Read-only. Undo one with: tools/evolution.py --rollback "Name"
"""
import json, os, datetime
p = os.path.expanduser("~/.reason_voice/crew_journal.json")
day = datetime.date.today().isoformat()
j = json.load(open(p))
rows = [(d, e) for d, v in j.items() for e in v if e.get("date") == day]
if not rows:
    print("no evolution today (%s) — a crew_config diff is NOT the engine" % day)
for d, e in rows:
    print("%-14s %s" % (d, e.get("change", "?")))
    for path, old, new in e.get("delta", []):
        print("%-14s   %s: %s -> %s" % ("", ".".join(map(str, path)), old, new))
