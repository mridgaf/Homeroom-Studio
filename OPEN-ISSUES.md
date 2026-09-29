# Open Issues — in working order

Checked 2026-09-28 against the code and the ledger, not just the status labels.
Tick a box when it's done.
**This list goes stale** (he works in the app and other sessions). Before starting a step, check
the Mac for proof it's already done — CLAUDE.md §0h. To start one, tell Claude: "do step N".

**Who's needed:** 🤖 Claude alone · 👂 your ears · 🎹 you at Reason · 🗳️ a decision from you

**Why this order:** fix what's broken first, then the cheap cleanups that stop
repeat mistakes. Next, hear what's already built before building more on top
of it. Then finish the genre/Legend pass. The Reason work waits for a session
where you're at the machine.

---

## NEXT SESSION START HERE (owner 2026-09-29)

- [x] **00c. Do the same for the next demo song: `Carlstrom - Airplane.rsndemo`** (🤖, owner 2026-09-29:
  "when complete /compact then do the same with the next demo song"). Same rules as 00b. Use
  `docs/reason/demo-song-notes.md` as the template and keep the same tags (Seen / Manual / Guess);
  put its notes in `docs/reason/demo-song-notes-airplane.md` and append to the two lists. The lessons
  from 00b are in that file's section 4 and in the `explore-reason-song` row of
  `docs/reason/demo-song-skill-ideas.md`. `open -a "Reason 12" "<file>"` opens it in its own window;
  close it with the window's red button and read the dialog before answering Don't Save.
  (Reason may still hold the unsaved scratch song "Step 8 test copy 09 29 26": don't save or close it.)
  ✅ 2026-09-29: Airplane explored; notes in `docs/reason/demo-song-notes-airplane.md`, phrase list section F and
  two new skill rows added; new follow-ups are items 34-37 below. Closed with Don't Save; the demo file's SHA-1 is
  identical before and after. Not done: re-patching a cable, soloing, a deliberate sweep edit, Combinator Modulation
  Routing, and every check that needs ears. The jack pop-up menus (owner's tip) were looked at in a second visit once he approved screen control: see item 37.

- [x] **00b. Explore a demo song and learn from it** (🤖, owner 2026-09-29). ✅ 2026-09-29: Street Phone
  explored; notes in `docs/reason/demo-song-notes.md`, lists in `demo-song-phrase-ideas.md` and
  `demo-song-skill-ideas.md`; voice-app gaps are items 29-33 below. Not done: re-patching a cable,
  soloing, a deliberate sweep edit, Combinator Modulation Routing (see the "Not looked at" list in the notes).
  His words: "open and look at one of the demo songs. And see what you can learn from it. As far
  as how sweeps work and different components can be connected. And anything else that will be
  useful to know. ... play around in the demo song ... By being curious and messing with controls
  on various components and trying things."
  - **Song (his pick):** `~/Music/Reason 12/Demo Songs/Gabriel Gassi - Street Phone.rsndemo` (47 MB).
  - **"Sweeps" = MUSICAL sweeps (his pick):** filter sweeps and other knob moves recorded into
    the song over time (automation), and how they're set up. NOT calibrate.py.
  - Learn: how devices are cabled (Tab flips the rack to the back: audio, CV, gate), mixer
    inserts/sends, Combinators, automation lanes in the sequencer, anything else useful.
  - Play with it: turn knobs, re-patch, mute, solo, watch what changes. A `.rsndemo` can't be saved
    over; never Save, and answer "Don't Save" on close. Playing it in Reason is fine; no exports
    (no-render rule). Claude can't hear: go by screen and meters, and ask him (clickable) if a
    change needs ears.
  - Write what's learned to `docs/reason/demo-song-notes.md` (plain words), and add anything
    that changes how the voice app should work to OPEN-ISSUES.
  - Reason may still have the unsaved scratch song "Step 8 test copy 09 29 26" open; don't save it.

- [x] **00. First thing: list everything still open** for the Beat Machine AND Reason Voice.
  ✅ 2026-09-29: listed, checked on the Mac. Owner corrected scope: "reason voice not code"
  (the voice app in `reason_voice/`, NOT the `~/reason code` folder). New items from the
  check: 26, 27 below.

---

## Done 2026-09-28

- [x] **0. Change how the kick drums work.** ✅ 2026-09-28: he named the change himself (long kick gets a snap + 5 dB duck, 7 in 10; see DECISIONS.md top). First, explain to him ALL the rules about
  kick drums and bass drums: their names (kick / bass drum / 808 / boom / sub / bass),
  what each one is, and how each relates to the rest of the beat (levels, the kick as
  the anchor, the 808 with the kick, one bass sound per beat, the layered kick, flavors).
  Read the code for this, not just the ledger, then explain in plain words. He decides
  the change after hearing it. Don't change anything before he does.
  Start points: memory `no-machine-tones` (kick=bass drum, boom=808, bass=line),
  `tools/crew.py` (peak_ceiling_for, _LOW_END, kick anchor), `tools/pattern_gen.py`
  (kick flavors), `tools/beat_machine.py` (pair_kick_for, _roll_extra_fx kick layer).

---

## ✅ DONE 2026-09-28: "why do the beats all sound alike?" (heard, kept — DECISIONS.md "Why the last 147 beats")

His words: "look at all of the beats that have been rendered in the past two days and see
what's going on with the commonalities and why they sound so alike. And how to fix that."
- HE ASKED, so rule 0g (don't scan old beats) does not block this. Scope = beats rendered
  2026-09-26 to 2026-09-28 only (file dates in `/Volumes/TBOTC 3/Homeroom Rhythms/<name>/`).
- Read their recipes (`.recipes/NN.json`: kit_paths, lanes, harmony, chord voices, bpm, lock),
  count what repeats across DJs/genres (same sample files, same chord progressions/voices,
  same bass file, same drum patterns, same tempos, same effects). Numbers, not adjectives.
- Explain the causes in plain words, propose fixes as clickable options. Change nothing
  before he picks. Don't render (hard rule) unless he asks.
- Likely suspects to CHECK, not assume: shared house rules that override identities (house
  chord grammar for everyone, 30% free beats, 10% MIDI everywhere, all 11 instrument
  families in every chord_source at equal odds 09-25, synonyms on for everyone 09-25,
  own_soundbank narrowing to the same few files, one bass pool).

Then: finish step 14 (DJ Premium is half-done: DECISIONS.md top entry has the full plan).

## 1. Fix what's broken (🤖, no listening needed)

- [x] **1. Beat-making crashes on MIDI-chords-played-on-strings beats.** ✅ 2026-09-28: `_fig` moved
  above its first use. Crash reproduced on old code (seed 7), gone on new.
  Test: `test_midi_chords_played_on_strings_do_not_crash`.
- [x] **2. Apply the 5 skill fixes from 09-09.** ✅ 2026-09-28: legend-new-build skill (stamp step
  rewritten, one config file, roster test, no `dry` on snares, library re-counted: 4,386 pitched
  samples, 0 choir, 0 chip), `--words` added to `tools/legend_newbuild.py`, render command
  added to beat-output-conventions.
- [x] **3. Looperman download.** Handled by the owner's own daytime scheduled task (Looperman +
  sample grab). Do NOT run `Test Nightly Loops (5)`: owner 2026-09-28, "the test download won't
  work", already tried to fix it that day.

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

- [x] **11. Hear the 7 genres already auditioned:** ✅ 2026-09-28 heard, kept ("They sound good."). Acid Rap Bright, Acid Rap Detroit, Baltimore Club,
  Chiptune, Crunk, Detroit, Emo Hip Hop. Folders are in Homeroom Auditions.
  Ref: [genre_newbuild_status.json](genre_newbuild_status.json) · [DECISIONS.md:103](DECISIONS.md:103) · [DECISIONS.md:121](DECISIONS.md:121) · [DECISIONS.md:160](DECISIONS.md:160)
- [x] **12. Hear Legend Well Damn** ✅ 2026-09-28 heard, kept. (auditioned 09-26, not heard). Ref: `tools/legend_newbuild.py`
- [x] **13. ✅ 2026-09-28: he rendered + heard all 11 on the app, kept.** Audition the 11 genres that are built but not rendered:** G-Funk, Horror Rap, Houston Screw,
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
  🤖 Claude alone (checked 2026-09-29): time both models on a spoken test file; no Reason needed.
  Ref: [CLAUDE.md:136](CLAUDE.md:136)
- [ ] **27. "Turn it down 3 dB" doesn't work** (🤖). Knob nudges only take percent
  (`reason_voice/dial_llm.py` "only percentage nudges for now"). Found 2026-09-10, never built.
- [x] **28. Voice-dial fixes found wiring 23 effects + 14 instruments** (🤖, 2026-09-29). ✅ fixed 2026-09-29 (DECISIONS "Item 28 voice-dial fixes"); left: COMP-01 ratio, Neptune "faster", Softube Amp Switch re-sweep.
  All 37 are mapped, measured and phrase-tested; most phrases land right. Owner: "small
  details we can flag and finish once everything is wired." In order:
  1. **Hz vs kHz** (and ms vs s): "2 kHz" landed on 952 Hz (MClass EQ, Grain). The app doesn't
     convert when Reason's display changes units partway up the knob.
  2. **Jumps too far**: plain up/down/more/less/"a bit" sometimes goes to an end instead of a
     nudge. Pangea "filter cutoff down" → 20 Hz (silence). Also Europa, Radical Piano, CF-101,
     Neptune, Klang, DDL-1 "wetter".
  3. **Wrong knob**: "open the filter" → Resonance/Env Amount (SubTractor, ECF-42); "turn on X"
     → the amount instead of the switch (Maximizer soft clip, Neptune pitch adjust → bypass);
     Sweeper "resonance" → Feedback; Quartet/Softube Amp pick the other mode's knob.
  4. **Steps**: "up an octave" / "down 5 semitones" nudge by % instead of moving 1 octave / 5
     semitones (SubTractor, Thor, Mimic).
  5. **"down 6 dB" went TO -6 dB** instead of down by 6 (Channel Dynamics).
  6. **Switches shown as 0%/100%** don't answer to "on" (Synchronous); COMP-01 "16:1" refused.
  7. **Unnamed pickers**: RV-7 algorithm, ECF-42 mode report numbers only; need names added.
  8. Tidy: map_device.py maps meters (Maximizer Output Level); ID8 map is mostly preset buttons;
     check the "readings lost" warnings on Grain/Europa/Monotone/Humana (likely false alarms).
  Two-part asks ("boost 5 kHz by 2 dB") only do the first half: one knob per phrase, by design.

## 5a. New from the Street Phone demo song (00b, 2026-09-29)

Source for all of these: `docs/reason/demo-song-notes.md` and the phrase list beside it.

- [ ] **29. The voice app can't touch mixer channels** (🤖 then 🎹). Fact: `remote/ReasonVoice.remotemap`
  has no mixer scope, and `intents.py` has no mute or solo. Fact: Reason's own "Reason Master Section"
  map (in `docs/reason/remote-vocab.json`) names every channel's Mute, Solo, Level, Pan and FX1-FX8
  Send Level, plus "All Mutes Off" and "All Solo Off". Untried: whether locking the Master Section
  reaches all of them. Also needed: turning "the kick" into "Channel N".
- [ ] **30. The voice app can't turn Combinator knobs** (🤖 then 🎹). Fact: the remotemap's Combinator
  scope has only Patch Next/Prev (lines 17-19); Reason has Rotary 1-16 and Button 1-4. The knob
  labels ("Reverb", "Filter Freq") are set by each song's author, so a phrase like "more reverb on the
  pad" needs a per-song label list.
- [ ] **31. Automation by voice** (🗳️ decide first): "sweep the filter up over four bars" and similar.
  Fact: nothing in `reason_voice/` writes a move over time. Fact: the 09-25 test showed the bridge can
  write automation on a locked device that has its own sequencer track while Reason records.
  Decision for you: is it wanted?
- [ ] **32. Review the two lists** (🗳️): `docs/reason/demo-song-phrase-ideas.md` (phrases) and
  `docs/reason/demo-song-skill-ideas.md` (skills). Two skill ideas are marked "clear win": they are not
  built because your rule is to run the skill-creator benchmark loop for new skills.
- [ ] **33. `docs/reason/FINDINGS.md` disagrees with `experiments/automation-test-2026-09-25/RESULTS.md`**
  (🤖). FINDINGS (09-25 update) says Record over the bridge is "unproven"; RESULTS "Night 2" says
  Record and Play were fixed. Check which is current before editing either.

## 5c. New from the Airplane demo song (00c, 2026-09-29)

Source: `docs/reason/demo-song-notes-airplane.md`, phrase list section F.

- [ ] **34. Many devices of one type, one locked device** (🗳️ decide first). Fact: the bridge answers for the ONE
  device locked to ReasonVoice. Airplane has 4 Europas and 4 Grains; Street Phone has 5 ECF-42 filters. So "open
  the pad filter" can't pick which one. Decision for you: do you want a way to choose the device by its name?
  (Not checked: whether a script can switch the lock.)
- [ ] **35. Redrum pattern and Dr. Octorex have no voice-app scope** (🤖). Fact: the Redrum scope in
  `remote/ReasonVoice.remotemap` has no item with "pattern" in its name, and "Octo" appears nowhere in the remotemap,
  `calibration.json` or `remote-vocab.json`. Airplane automates Redrum "Pattern Select" on its Kick and Clap.
  Europa (Filter Mod), Grain (Filter Freq, Dist Amount) and Synchronous (Level and effect knobs) ARE mapped.
- [ ] **36. Listen to the Airplane "Sidechain Bus"** (👂). Fact: seven channels output to it, its Sidechain Input
  jacks have no cable, and a Synchronous "Long Sidechain" patch sits in its insert Combinator. Not known: whether
  that curve dips the sound on the beat or swells it. One listen at bar 45 onward, with and without the
  Combinator's Bypass FX, would settle it. Claude can't hear.
- [x] **37. Open the jack pop-up menus on the back of the rack** (🎹). ✅ 2026-09-29, after you approved screen
  control. Ctrl-click on a jack lists every device in the rack with a check mark on the connected one and an
  asterisk on jacks already cabled; hovering a jack gives a "Connected to ..." tooltip. Nothing was picked, the
  song was closed unchanged (SHA-1 identical). Found with it: no channel's Side Chain Input has a cable in
  Airplane, so its "sidechain" is all Synchronous curves. A wiring sample was then read by tooltip for both songs
  (Airplane: sends, returns, master, bus insert, five channel inputs; Street Phone: sends, returns, master chain); a full map of either
  song is not done. Details:
  `docs/reason/demo-song-notes-airplane.md` sections 3-5.

- [x] **38. Map Airplane's wiring fully** (🤖, owner 2026-09-29). ✅ `docs/reason/demo-song-wiring-airplane.md`. Not read:
  right jacks on a few devices, several inner cables of the Pulse Scream and Norwegian Boy Combinators, and Modulation
  Routing for both (see section E there).
- [ ] **39. Map Street Phone's wiring the same way** (🤖, owner picked "Map Street Phone too"). Done so far: sends,
  returns, master chain (notes section 6), and **every channel's insert chain** (notes sections 7, 7b, 7c: Kick, Clap,
  LambaBeat, Timbales, Bass Tonewheel, Organ 1, Organ 2, WarmPad, Guitar question, Pictures of Moments, Main Vox,
  Middle 8 Vox, Chorus Vox, Booomzzz; read by hover, left jacks only). Combinator insides started (notes section 8):
  Beat Process, Timb Process and Org 1 Squash read (devices and Modulation Routing). Still to do: the other ~15
  Combinators (Clap/Kick/Org 2 Squash, Organ 1/2, Bass Tonewheel, Pad Processor, Guitar question, Deluxe Vocal FX
  Chain, Pictures of Moments, Synth Processor, Toxic Vocal, Vocal Khaba, master ones), right-hand jacks, Neptune
  settings on Middle 8 Vox. First close showed a save dialog (answered Don't Save), the second did not; cause unknown
  (notes 8f). SHA-1 after both: `e377af37...` (unchanged).

- [x] **40. Explore a hip hop demo song: BLKMGK "Power"** (🤖, owner 2026-09-29: "find the other demo songs ... hip hop
  priority ... begin learning and wiring the first one alphabetically"). ✅ Only two demos were on the Mac (Airplane,
  Street Phone); reasonstudios.com lists ten, two hip hop (BLKMGK "Power", Qua z mo "I Just Wanna Be"). Owner said yes
  to downloading Power only (33 MB zip, `~/Downloads/Reason Demo Songs/`). Notes: `docs/reason/demo-song-notes-power.md`
  (arrangement, whole rack back read by hover, sends table, lanes). Closed unchanged (SHA-1 `704ee4ff...`).
- [ ] **41. Does the Power "Bass Sidechain" Redrum actually run?** (👂). Fact: a Redrum (pattern A1, steps 1-5-9-13, a
  bass-drum sample) has no sequencer track, its RUN button looked unlit with the transport stopped, and its output
  goes to the Bass channel's Side Chain Input (KEY lit). Not known: whether it plays and pumps the bass. Needs one
  short Play with the Bass compressor meter watched, or ears. I did not press Play (audible while you work).
- [x] **42. Second hip hop demo: Qua z mo "I Just Wanna Be"** (🤖, owner picked "Qua z mo next"). ✅ First pass:
  `docs/reason/demo-song-notes-quazmo.md` (30 tracks, 97.29 BPM, sub-mix buses, sends 4-6 = Delay 3/16, Scream 1, Scream 2,
  master Combinator hovered, "PAD FX" Combinator). Not done: Neptune devices, automation lanes, most channel cables.
  Closed unchanged (SHA-1 `290f75ff...`). Eight more demo songs are on the site (Rack Disco, Mountain, What's the Reason,
  700 Dreams, Purple Ribbons, Recall, Evolution, Metamorph, Bajo Caida); not downloaded, needs a yes.
- [ ] **43. Mouse clicks are blocked while macOS Dictation is on** (🤖). Fact: with the orange microphone dot showing,
  every display-scope click and scroll failed ("would land on Dictation"); hover, keyboard and the background app
  tools still worked (Tab flips the rack, PageUp/PageDown scroll it, arrow keys move between rack columns).
  Ctrl-click jack menus need clicks, so they were not possible in this visit.

## 5b. New from step 4 (👂)

- [x] **24. Hear the 4 new effects** (hall, wide hats, ratchet hits, layered kick) and the Loops-page lock. ✅ heard, kept 2026-09-28.
  Shares are first guesses: hall 10%, wide hats 20%, ratchet 15%, kick layer 15%.
  Ref: [tools/beat_machine.py](tools/beat_machine.py) `EXTRA_FX_P`
- [x] **25. Hear the long-kick snap + duck** (2026-09-28). ✅ heard, kept 2026-09-28. A kick that rings past 0.5 s gets a
  short kick's snap on top, its tail dips 5 dB under it, one hit at a time. 7 beats in 10.
  Rack row "kick snap". Not heard yet: the snap's level (matched to the long kick's peak) is a first guess.
  Ref: [tools/crew.py](tools/crew.py) `punch_long_kick`

## 6. Low value: whenever (🤖)

- [ ] **20. Better key detector.** It failed its test. Low value: instruments already read their
  pitch from the audio. Ref: [DECISIONS.md:56](DECISIONS.md:56)
- [ ] **21. VSCO Upright Piano + VSCO Organ skipped** (numbered file names). You have other pianos/organs.
  Ref: [DECISIONS.md:74](DECISIONS.md:74)
- [ ] **22. Faster parallel test run** (parked). Ref: [DECISIONS.md:2950](DECISIONS.md:2950)
- [ ] **23. Recipes: 25 theoretical, 2 tested.** Flip each as you try it. Ongoing, not a task.
  Ref: [CLAUDE.md:133](CLAUDE.md:133)
- [ ] **26. 14 loops from the 09-27 morning grab still unfiled** (👂): 13 have no name.
  `Nightly Loops/Unsorted 2026-09-27 morning/` (has a README). Checked there 2026-09-29.

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
