# Next session: build the case groups (picked 2026-10-08, from run_round3.log)

Build these three first, each as its own small set of cases in gen_cases.py, in steps of 5%:

1. **Short names** (lo, mid, hi, reso, p1, "cut hi"): 3 of the 5 map-set move fails (M11, M13, M19). Each name: said alone, said with "cut"/"body", said with a value.
2. **Relative moves** ("down 20 percent", "up 10 percent"): C5 failed. Needs read, then math, then set. Start at 5-step values, targets 5 to 95.
3. **Refusal** (check LOOSENED 2026-10-08: any plain refusal passes, exact word not required; only 'printed a command / no answer' fails) (made-up names, CV-input knobs): only 5/10 started with the exact word, C9 too. Many phrasings per refusal type.
   **CABLES ARE NOT A REFUSAL (owner 2026-10-08):** you can cable anything to anything on the back panel by hovering the jacks (screen control, positions from the Panel Map). C8 ("cable from the body to the output") and the map-set cable case currently expect NOT POSSIBLE; that is wrong. Pull them out of the refusal group and make a separate cabling group (needs screen control, not knob.py).

Not a group, but fix alongside: Hermes prints the command instead of running it (C2, C5, M05, M14, M19).
