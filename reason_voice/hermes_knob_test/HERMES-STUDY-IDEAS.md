# Ideas: Hermes studying on its own

Logged while building round 2 (2026-10-08). Nothing here is built unless marked BUILT.

1. **Map → test cases, automatically (BUILT: gen_cases.py).** Every mapped device can make its own quiz.
   Hermes could run it nightly with no one there: the judge reads Reason's reply, so no human scoring.
   Needs: device locked + Reason open. The 21 other mapped devices only need their json path.
2. **Failures grow the word list.** knob.py's ALIAS (high→hi, volume→level) is hand-made. Each time
   find says NO SUCH CONTROL on a real control, log the words. Owner OKs new pairs (his rule: synonyms are his call).
3. **Self-check loop is free.** set already reads back the value. A drill: Hermes sets random %s,
   compares what Reason reports, learns which knobs don't land (stepped ones like Damage Type).
4. **Stepped controls need their step table.** Damage Type (10), Body Type (5), Enabled (3-way) were
   skipped. A sweep (bridge skill already has one: calibration.json) records which raw value = which step.
   Hermes could then say "set damage type to tape" instead of a percent.
5. **Score file Hermes can read.** results.md is a log for people. A small json score per case id
   (pass count, last fail reason) lets Hermes pick its own weakest cases to drill.
6. **Mixed phrasing from one case.** Same target, said 3 ways ("the hi", "high cut", "top of the cut EQ").
   Generator can make variants; tests the word-matching, not just the knob.
7. **Hide answers from the study run.** The judge's cases file has the right knob in it. Hermes's tools
   must never read it (rule: "do not open other files"), or the quiz is just copying.
8. **Mistakes become rules, automatically.** Round 2's one real fail (C2: searched "body back") became
   one rule line. A study loop could propose the rule from the failing transcript; owner approves.
9. **Grade the words, not just the knob (BUILT: wording check in run_typed.py).** C8 moved nothing
   but said the wrong thing. A quiz that only checks knobs misses this.
10. **Every case starts from a known state (BUILT: "start" field).** C7 "passed" because damage was
   already on. Unattended study needs this or it learns from fake passes.
11. **Hermes drops the ball between two steps.** Most real fails: it ran find, then replied with the
   next command instead of running it. Fewer steps per case = fewer drops. A drill could repeat just
   the hand-off until it sticks, or the tool could do find+set in one call.
12. **Back-to-back cases leak.** M23 "passed" because M22 already left the knob there. Unattended quizzes
   must shuffle and reset each case, or Hermes gets credit for nothing.
