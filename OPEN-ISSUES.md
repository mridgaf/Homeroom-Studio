# Open Issues — in working order

Checked 2026-09-28 against the code and the ledger, not just the status labels.
Tick a box when it's done. To start one, tell Claude: "do step N".

**Who's needed:** 🤖 Claude alone · 👂 your ears · 🎹 you at Reason · 🗳️ a decision from you

**Why this order:** fix what's broken first, then the cheap cleanups that stop
repeat mistakes. Next, hear what's already built before building more on top
of it. Then finish the genre/Legend pass. The Reason work waits for a session
where you're at the machine.

---

## ▶ NEXT SESSION STARTS HERE (owner, 2026-09-28)

- [ ] **0. Change how the kick drums work.** First, explain to him ALL the rules about
  kick drums and bass drums: their names (kick / bass drum / 808 / boom / sub / bass),
  what each one is, and how each relates to the rest of the beat (levels, the kick as
  the anchor, the 808 with the kick, one bass sound per beat, the layered kick, flavors).
  Read the code for this, not just the ledger, then explain in plain words. He decides
  the change after hearing it. Don't change anything before he does.
  Start points: memory `no-machine-tones` (kick=bass drum, boom=808, bass=line),
  `tools/crew.py` (peak_ceiling_for, _LOW_END, kick anchor), `tools/pattern_gen.py`
  (kick flavors), `tools/beat_machine.py` (pair_kick_for, _roll_extra_fx kick layer).

---

## 1. Fix what's broken (🤖, no listening needed)

- [ ] **1. Beat-making crashes on MIDI-chords-played-on-strings beats.**
  `_fig` is used before it's defined. Hit randomly by tests.
  Ref: [tools/beat_machine.py:2354](tools/beat_machine.py:2354) (defined at 2374)
- [ ] **2. Apply the 5 skill fixes from 09-09.** None were ever applied. They stop repeat
  mistakes in the genre/Legend builds coming up (step 7), e.g. "read the STAMP first"
  points at a lane that no longer plays. Gap #4 ("only bell instruments exist") is now
  out of date and needs rewriting, not copying.
  Ref: [DECISIONS.md:2780](DECISIONS.md:2780)
- [ ] **3. Prove the Looperman nightly download works end to end.** Login is fixed; the download
  itself hasn't been re-run. The drive is plugged in, so Claude can run it.
  Ref: [DECISIONS.md:7881](DECISIONS.md:7881)

## 2. One listening session: things already built (👂) — ✅ done 2026-09-28, kept

Hear these before anything new is stacked on them. Claude renders one small audition folder.

- [x] **4. Volume lock:** edit a beat; the other sounds should stay put. Ref: [DECISIONS.md:23](DECISIONS.md:23)
- [x] **5. Bass row:** picking a bass changes only the bass. Ref: [DECISIONS.md:64](DECISIONS.md:64)
- [x] **6. Note-by-note instruments** (Steinway, harp, pipe organ…). Tested on the Mac, never heard.
  Ref: [DECISIONS.md:74](DECISIONS.md:74)
- [x] **7. Low end:** one bass sound per beat, 808 with the kick, hip-hop standard levels.
  Ref: [DECISIONS.md:275](DECISIONS.md:275) · [DECISIONS.md:309](DECISIONS.md:309)
- [x] **8. "808 only" dirt now distorts the 808, not the kick** (Crunk, Mustang, Night Metro).
  Ref: [DECISIONS.md:113](DECISIONS.md:113)
- [x] **9. From-scratch muddy/harsh fix** (top end still ~5 dB brighter than Loops beats).
  Ref: [DECISIONS.md:550](DECISIONS.md:550)
- [x] **10. MIDI chord packs at 10% of beats.** Ref: [CLAUDE.md:137](CLAUDE.md:137)

## 3. Genre + Legend pass (👂 then 🤖)

- [ ] **11. Hear the 7 genres already auditioned:** Acid Rap Bright, Acid Rap Detroit, Baltimore Club,
  Chiptune, Crunk, Detroit, Emo Hip Hop. Folders are in Homeroom Auditions.
  Ref: [genre_newbuild_status.json](genre_newbuild_status.json) · [DECISIONS.md:103](DECISIONS.md:103) · [DECISIONS.md:121](DECISIONS.md:121) · [DECISIONS.md:160](DECISIONS.md:160)
- [ ] **12. Hear Legend Well Damn** (auditioned 09-26, not heard). Ref: `tools/legend_newbuild.py`
- [ ] **13. Audition the 11 genres that are built but not rendered:** G-Funk, Horror Rap, Houston Screw,
  Memphis, Miami Bass, New Orleans Bounce, Organized Noize, Plug, Reggaeton Alt, Trip Hop, Wonky.
  Then hear them. Ref: [genre_newbuild_status.json](genre_newbuild_status.json)
- [ ] **14. Build the last 2 Legends: DJ Premium and No Alias** (not started). 11 of 14 confirmed.
  Ref: `tools/legend_newbuild.py`

## 4. Decisions only you can make (🗳️) — ✅ done 2026-09-28: both built (see DECISIONS.md top)

- [x] **15. Loops-page beats:** changing the kick or hat still re-levels the other sounds.
  Lock them like from-scratch beats, or leave them? Ref: [DECISIONS.md:23](DECISIONS.md:23)
- [x] **16. 4 effects built but never used:** hall reverb (one-line fix), haas widener, kick
  layering, ratchet rolls. Pick any, or none. Ref: [DECISIONS.md:5779](DECISIONS.md:5779)

## 5. Reason control session (🎹, you at the machine with Reason open)

- [ ] **17. Finish "Step 8":** one look at the Dr. Octo Rex panel confirms its 5 unconfirmed names.
  Ref: [DECISIONS.md:1495](DECISIONS.md:1495) · [DECISIONS.md:1641](DECISIONS.md:1641)
- [ ] **18. Prove RV7000, Kong, Redrum, Alligator in real Reason.** Redrum and Kong both answer
  to "Level"; sort that out here.
  Ref: [DECISIONS.md:1999](DECISIONS.md:1999) · [DECISIONS.md:1903](DECISIONS.md:1903) · [DECISIONS.md:1858](DECISIONS.md:1858) · [DECISIONS.md:1739](DECISIONS.md:1739)
- [ ] **19. Re-measure voice speed on the M2** (the small/tiny model switch already exists).
  Ref: [CLAUDE.md:136](CLAUDE.md:136)

## 5b. New from step 4 (👂)

- [ ] **24. Hear the 4 new effects** (hall, wide hats, ratchet hits, layered kick) and the Loops-page lock.
  Shares are first guesses: hall 10%, wide hats 20%, ratchet 15%, kick layer 15%.
  Ref: [tools/beat_machine.py](tools/beat_machine.py) `EXTRA_FX_P`

## 6. Low value: whenever (🤖)

- [ ] **20. Better key detector.** It failed its test. Low value: instruments already read their
  pitch from the audio. Ref: [DECISIONS.md:56](DECISIONS.md:56)
- [ ] **21. VSCO Upright Piano + VSCO Organ skipped** (numbered file names). You have other pianos/organs.
  Ref: [DECISIONS.md:74](DECISIONS.md:74)
- [ ] **22. Faster parallel test run** (parked). Ref: [DECISIONS.md:2950](DECISIONS.md:2950)
- [ ] **23. Recipes: 25 theoretical, 2 tested.** Flip each as you try it. Ongoing, not a task.
  Ref: [CLAUDE.md:133](CLAUDE.md:133)

---

## Already done or dropped (checked 2026-09-28)

- [x] Volume changing when you edit one sound: fixed 2026-09-27. [DECISIONS.md:23](DECISIONS.md:23)
- [x] Kick type 15% → 38%: fixed for Legends 2026-09-19; crew DJs kept on purpose (your call).
  [tools/pattern_gen.py:1399](tools/pattern_gen.py:1399)
- [x] Chorus/phaser "never switched on": they ARE on for 7 DJs (Otto Grit, Glass Cat, Sunday Chop,
  Night Metro, New Math, Half Light, Fast Water). [crew_config.json](crew_config.json)
- [x] Transient shaping: now in use (was one of the 5 unused effects).
- [x] Whisper "find something like this": fuzzy matching is in.
  [reason_voice/intents.py:111](reason_voice/intents.py:111)
- [x] Faster speech-model switch: in the app's settings. [reason_voice/server.py:106](reason_voice/server.py:106)
- [x] Chord flow: you heard it and kept it (09-26). [DECISIONS.md:42](DECISIONS.md:42)
- [x] ~~Rage Engine narrowing stereo~~: dropped. You skipped the mono test on 09-26 (old beats, rule 0g).
  [DECISIONS.md:4852](DECISIONS.md:4852)

**Not checked one by one:** about 25 older "not heard" entries from 09-03 to 09-07 (per-DJ passes,
float-WAV recovery, low end −10%). Most are likely covered by later builds you have heard.
Open one by name if it still matters.
