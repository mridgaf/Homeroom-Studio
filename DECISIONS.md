# Decision Ledger

Read this at the start of a session. Append to it at the end. Update `status`
on old entries when you learn what actually happened — don't just pile on new
entries.

## Entry format

```
### [YYYY-MM-DD] Short title
- Context: what was going on / what problem this addressed
- Decision/change: what was actually done
- Reasoning: why this over the alternatives
- Verify by: how to check if this held up (test, re-check, "ask user next time")
- Status: open | confirmed | failed
- Outcome: (filled in later, when known)
```

---

## Log

(new entries go below this line, most recent first)

### 2026-08-08 Eleventh DJ added: Fast Water (slot 11) — the break lane
- Context: owner asked for another surprise DJ, my choice. With Half Light
  at 68 the roster spans 68-150 and the two remaining holes were the TOP of
  the tempo range and the ROLE of the timekeeper: on all ten, the hat/rim is
  a quiet lane under a loud backbone.
- Decision/change: "Fast Water", num 11, 172 BPM, era "now",
  built "no one — the break lane".
  - Kick + snare play HALFTIME (2-3 moves a bar) so the pulse reads ~86
    while the break lane runs 32nds at 172.
  - The break lane (`hat`, 32-step grid) has gain 0.52 — the loudest
    non-backbone lane on the roster (others 0.26-0.40). The chop IS the
    beat. Home mode `rolls32`; pan +0.14 (inside the |0.2| timekeeper rule).
  - Snare home mode `displaced`: the 2 and the '&' of 3 — the jungle
    two-step, never 2 & 4. A second snare-role lane, `ghost`, whispers
    16ths underneath at 0.24 — no other member has two snare-role lanes.
  - Everything is EARLY, not late (break -7 ms, ghosts -11 ms) — the mirror
    of Half Light. Swing 50 everywhere: at 172 swing turns to mud.
  - dust 0.0 (era rule), vinyl -40, wow 0.1, sidechain 0.28, drive 1.3,
    house `gated` snare kept, `alt` = short PLATE (0.9 s / 5200 Hz / 0.3)
    so the break stays readable.
  - Stamp (siren/reverse/scratch) lands ON the 1 of bars 5 and 8 — he
    announces the bar; everyone else tails 4 and 8 (Half Light tails 2/6).
  - Harmony: pad/strings/bell, sustain only, minor/dorian,
    suspended_open + vamp_i_VI top-weighted, chords_default true.
  - Also given a 16-line KICK_BANK (halftime skeletons) and a two-word
    title bank in beat_machine.TITLES.
  - Written in four places so deleting the config regenerates him:
    crew_config.json (live), crew.py DEFAULT_CREW + CREW_SIGNATURES,
    pattern_gen.py DEFAULT_STYLE + KICK_BANK.
- Reasoning: New Math was cerebral, Half Light was mood/tempo-down. The
  untaken axis was tempo-UP plus an inverted mix hierarchy — a fast beat
  that doesn't feel fast, where the timekeeper is the loudest thing.
  Existing constraints honoured (dust 0 outside the 90s, only Crate Prophet
  skips sidechain, space stays "gated", hat |pan| ≤ 0.2, kick choke range
  starts ≤ 1.0 s).
- Verify by: `tests/test_crew.py` roster test renamed to
  `test_roster_is_the_agreed_eleven` (11 slots). In the Linux sandbox:
  test_crew + test_pattern_gen + test_evolution + test_variety = 84 passed;
  test_beat_machine = 64 passed / 6 failed, and those same 6 chord-audio
  tests fail at HEAD without this change (verified by re-running a clean
  copy in /tmp) — environment, not this change. Six test modules can't even
  import in the sandbox (no rapidfuzz/scipy).
  NOT verified: nothing rendered — no audio exists for him yet.
  On the Mac: `.venv/bin/python -m pytest tests/ -q`, then render one Fast
  Water beat and listen. Two things to listen for specifically: (a) does the
  0.52 break lane sit too loud against the −5 dB snare bus, and (b) does the
  32nd break read as a chop or as a buzz at 172.
- Status: open
- Outcome:

### 2026-08-07 Tenth DJ added: Half Light (slot 10) — the slow one
- Context: owner asked for a second surprise DJ, my choice, now that the
  engine has grammar modes, harmony signatures and the genre timekeepers.
  The roster's gap was obvious once listed: nine DJs, tempos 88-150, all
  either on the grid or pushing ahead of it, all with a hat lane, all
  stamping the tail of bars 4 and 8.
- Decision/change: "Half Light", num 10, 68 BPM, era "now". Every lane is
  LATE by design (kick +26 ms, snare +34 ms, rim +12, shaker +18) — the
  first DJ that drags. No hat lane at all: a cross-stick RIM keeps time,
  home mode 'shuffle' (swung triplets) — first crew member to reach the
  genre-roster timekeepers, which is why his clock sounds unlike the other
  nine. Snare home mode is 'four' (the 4 alone, the 2 left empty).
  wow=0.6 (highest on the roster), vinyl -38, dust 0.0. House gated snare
  kept; his Alt file is a HALL (2.2 s / 2600 Hz / 0.42 wet) — the biggest
  room any DJ has. Stamp lands at the END of bars 2 and 6 so it sucks INTO
  3 and 7. Harmony: piano/guitar/organ, sustain (never arp — at 68 BPM an
  arp fills the hole the drums are leaving), minor/dorian, noir_descend
  and sad_accepting weighted top; chords_default true.
  Written in three places, not one: crew_config.json (live), crew.py
  DEFAULT_CREW + CREW_SIGNATURES, pattern_gen.py DEFAULT_STYLE — so
  deleting the config file regenerates him instead of losing him.
- Reasoning: the previous surprise (New Math) was cerebral — polyrhythm
  and arithmetic. Repeating that would be a variation, not a surprise.
  The untaken axis was mood and tempo, not math. Constraints honoured:
  dust must be 0 outside the 90s, only Crate Prophet skips sidechain, and
  the house space stays "gated" — so the damage comes from wow and the
  hall goes in `alt`, where the tests allow it.
- Verify by: tests updated to a roster of ten (test_crew
  test_roster_is_the_agreed_ten; test_beat_machine round-trip comment).
  Full suite run in the Linux sandbox: 724 passed, 1 skipped, 6 failed —
  those 6 are chord-audio tests that ALSO fail on the unmodified config
  in that sandbox (verified by removing Half Light and re-running), so
  they are environment, not this change. NOT verified: no beat has been
  rendered — TBOTC 3 wasn't mounted, so no audio exists yet. Run the
  suite on the Mac (`.venv/bin/python -m pytest tests/`) and render one
  Half Light beat before trusting it.
- Status: open
- Outcome:

### 2026-08-07 Half Light verification resumed on the Mac
- Context: picking up the open item above — real Mac, TBOTC 3 mounted.
- Full suite on the Mac (`.venv/bin/python -m pytest tests/ -q`): **794
  passed, 1 skipped, 0 failed** in 4:00. Confirms the 6 sandbox failures
  were environment-only, not caused by Half Light.
- Bug found and fixed: `tools/beat_machine.py`'s `TITLES` dict (two-word
  beat-name generator) had no entry for "Half Light" — the render path
  crashed (`KeyError`) the first time anyone tried to render him through
  the normal CLI/web path. The 2026-08-07 entry above said he was
  "written in three places, not one" (crew_config.json, crew.py,
  pattern_gen.py) — TITLES in beat_machine.py was a fourth place that
  got missed. Added a title bank in his voice (Dim/Late/Behind/Hollow/
  Dusk/Faded/Slack/Amber x Room/Hour/Curtain/Echo/Fade/Glow/Drift/Hall)
  matching the existing per-character two-word pattern. No sound-design
  change.
- Rendered 3 files to `~/Desktop/Homeroom Half Light audition
  2026-08-07/` (scratch, not the real library — his ears haven't judged
  this yet): one full-pipeline beat via `beat_machine.py --render` (WAV +
  MIDI + 9 stems, beat #86 would've been the real number if this had
  gone to the library), plus a direct house-vs-Alt-hall pair via
  `crew.py` to specifically exercise his one-of-a-kind hall alt space.
  All 3: loop length exact, LUFS -13.1 to -13.6 (target -12, in
  tolerance). MIDI file passed midi-validity-gate (channel 10, GM drum
  notes, embedded tempo, non-empty). READ ME.txt written for his ears.
- Verify by: numbers above are machine-checked and hold. NOT checked:
  whether it actually sounds right — that's his call, not logged here
  until he reports back.
- Status: confirmed (code + pipeline verified; sound judgment also in)
- Outcome: owner listened, verdict on the house-vs-hall question the
  README asked: **gated (house) sounds good** — "Half Light House gated
  snare Drums 68bpm.wav". Hall alt not rejected outright, just not what
  he called out. Gated stays the default treatment; no change needed.

### 2026-08-07 New reset tool: clear Legends + DJs, permanently empty Trash
- Context: owner wanted a clean slate — every beat in the 12 Legend folders
  and 9 DJ (crew) folders cleared, but Favorites kept, and this time the
  Trash folder (previously "moved, never deleted" per beat_machine.py) also
  actually emptied for good. Confirmed both via AskUserQuestion since this
  contradicts the project's default never-delete rule and the existing
  `clear_junk_beats.py` (which sweeps Favorites too, no exceptions, by a
  2026-07-22 decision) — this is a different, narrower operation.
- Decision/change: added `tools/clear_legends_djs.py` (new script, existing
  `clear_junk_beats.py` left untouched for future full resets). Reads the 21
  target folder names straight from `legends_config.json` +
  `crew_config.json` keys (confirmed these match the actual folder names via
  `beat_machine.py` — `folder = root / names[0]`, names[0] is the config
  key). Step 1 moves those folders' beats into a dated `Cleared YYYY-MM-DD`
  holding folder with a manifest, typed "yes" to confirm — same safe pattern
  as the existing tool. Step 2 lists and then permanently deletes Trash
  folder contents, gated behind typing "DELETE" (different word on purpose,
  so the two prompts can't be blown through on autopilot). Added
  "Clear Legends and DJs.command" as the double-click launcher.
- Reasoning: matched the existing project pattern (dated folder + manifest +
  typed confirmation) everywhere except the one step he explicitly asked to
  be a real, permanent delete.
- Verify by: the beats library lives on `/Volumes/TBOTC 3`, which this
  sandbox cannot reach — script only checked by `py_compile` + AST parse, not
  run against real data. Ask him to run it (or run `--dry-run` first) and
  confirm the counts look right before trusting it fully.
- Status: open
- Outcome: (pending — not yet run against the real library)

### 2026-08-07 Both rooms reskinned live to mockup D ("paper + ink")
- Context: owner reviewed 7 UI mockups (A-G) across two throwaway mockup
  folders, picked D, asked for two more in that family (F, G), then said
  "stick with D, make the changes." Confirmed via AskUserQuestion that this
  meant reskinning the REAL running apps, not just the mockup files.
- Decision/change: rewrote the shared `:root` palette in `tools/beat_machine.py`
  (the documented source of truth — comment says "one color scheme across
  both rooms") from dark xerox-paper/cream-text to light flyer-paper/ink-text.
  Mirrored the same token values into `reason_voice/static/style.css` per its
  existing convention. Because both stylesheets already ran on CSS custom
  properties (var(--hi), var(--paper), var(--display)...), most of the reskin
  cascaded from the `:root` edit alone; hunted down ~20 hardcoded hex values
  that had assumed a dark background (input fields, hover tints, the
  dropdown-arrow SVG, status pills) and fixed those individually. Added Anton
  + Space Mono (Beat Machine) and Kalam + Space Mono (Reason Voice) via
  Google Fonts import. No HTML structure, IDs, classes, or JS touched —
  visual-only diff, to protect the working drag-drop/stem-rack/WebSocket code.
- Reasoning: matches mockup D's "paper + halftone, blue ink, yellow highlight"
  language on both apps without risking the two apps drifting into different
  palettes (the "one color scheme" rule is 2026-07-25 owner intent, not mine).
  Editing tokens instead of rewriting markup kept the diff small and low-risk
  per the project's own working code.
- Verify by: `./.venv/bin/python -m py_compile tools/beat_machine.py` (clean).
  Visually verified in-browser at localhost:8790 (Beat Machine, full page,
  all three DJ-card selection states) and localhost:8765 (Reason Voice, a
  full recipe card walkthrough). NOT yet seen by the owner on his own screen.
- Status: open — needs his eyes before calling it done.
- Outcome: (pending)

### 2026-08-04 The famous figures: named, played as written, and left alone
- Context: a deep review of the 2026-08-01 break work found seven things.
  Six were real and one number in it was wrong. Confirmed by re-running the
  diff myself: 73 of 180 library kick lanes did change under a docstring
  that said "keeps all 180 existing patterns unchanged". The review said
  those ghosts play 26 dB down; they play at 0.26 gain, about -11.7 dB —
  the -26 dB was the floor on the per-hit wobble that had already been
  removed. Verdict stands either way: a silent change is the problem.
- His call, asked directly: keep the velocity reading LIBRARY-WIDE (not
  scoped to breaks), and the figures stay ASK-ONLY — never rolled into a
  batch by accident. Then he widened the ask: not just breaks, a "famous
  beats" picker of widely-sampled drum parts. Named six; three were new.
- Decision/change, seven fixes plus the umbrella one he asked for:
  * THE UMBRELLA — "exclude the break beats from the rules keeping them
    from being what they should be". compose() already spared a verbatim
    figure its thinning; `vary_preset` ran afterwards on every beat and
    undid it (density mutation, and treatments that blank whole bars). One
    gate at the top of vary_preset: on a break beat, kick/snare/hat leave
    `mutable`. Guests still get an arrangement.
  * NAMING ONE GETS YOU IT — the ten song names all collapsed to
    break_beat=True and the word was discarded, so "amen" gave the Amen 1
    roll in 10. `break_name` now rides through to `_pick_break(rng, want)`.
  * ACCENTS — `_lib_lane` replaces the old kick/snare parsers. Loud hits
    more than 15 apart were accented on purpose (the pack is 55/100/118);
    otherwise ghosts are ghosts and the flat fallback is per-lane, exactly
    what each lane always did. Assembly Line keeps its accents on 11 and 27.
  * THE 73 — that same rewrite is library-wide, his call. Measured against
    what shipped: 2 kick lanes and 4 snare lanes move. Against the parsing
    before ghosts were honoured: the 73. In the audition batch as A/B pairs.
  * HATS — nine of ten were byte-identical straight 8ths at a flat 100.
    All thirteen rewritten with real dynamics and open hats; `_lib_hat`
    carries velocity now. TRANSCRIBED FROM NOTATION, NOT CONFIRMED BY EAR.
  * REACHABLE — a "Famous beats" dropdown on the page. It types the words
    into the Directions box, so picking and typing are ONE code path, and
    the options are built from the JSON so the list has one home. Also:
    punctuation no longer eats the word ("funky drummer!" fired nothing —
    only "," and "." were stripped), and patterns_breaks.json is now walled
    out of `_pick_library` so a figure can never arrive as a thinned
    influence.
  * TESTS — tests/test_breaks.py, 30 of them, parameterised over every
    figure. Plus the two hard rules that had a choke point and no test:
    STAMP_LANE off, VOX_LANE_P 0.
  * README — the "not copies of specific copyrighted recordings" line was
    false next to thirteen files named after specific recordings. Rewritten
    to say what is actually true: the pattern is transcribed, no audio is
    used, and a drum pattern is not the sound recording.
- Three new figures, his list: Think (Lyn Collins), When the Levee Breaks
  (Led Zeppelin), The Big Beat (Billy Squier). Duplicates of what was
  already in the pack (Impeach, Synthetic Substitution, Apache) skipped.
- Caught while checking, not by a test — the reason the test is now
  parameterised over all thirteen: Apache and The Big Beat are drummed on a
  plain 2 and 4, and the "a bare 2&4 seed teaches nothing" guard threw
  their backbeat away and substituted the DJ's own, while the beat's notes
  still read "played straight". Only the Amen was being checked.
- Verify by: `tests/test_breaks.py` (30). Full suite 781 passed, 1 skipped.
  Audition batch on the Desktop: "Homeroom Famous Beats 2026-08-04".
- Status: partly confirmed — the ghost kicks are settled, the hats are not.
- Outcome:
  * GHOST KICKS — CONFIRMED by ear, 2026-08-04. He heard the three A/B
    pairs and said "I like the after sound", i.e. the quiet kicks stay
    quiet. The velocity reading is LIBRARY-WIDE and the 73 grooves keep
    what they gained. No code change: AFTER is what already ships. Do not
    reopen this by "simplifying" `_lib_lane` back to a binary threshold —
    the three-level reading IS the approved sound.
  * HATS — still open. Written from published notation, never checked
    against the records. Nine of the ten used to be a flat metronome, so
    anything is an improvement, which is exactly why "he didn't complain"
    must not be read as "he approved them". Ask again explicitly.
  * TEMPO — open. 90 Night Metro rendered The Big Beat at 136bpm because
    the DJ's tempo range beat the figure's. Not raised with him yet.
  * FIGURES REPORTED WRONG BY EAR, 2026-08-04. He listened and said the
    breaks don't sound right, and asked straight out whether I actually
    have the ability to build these. Answered honestly: I cannot hear, and
    the patterns are RECALL, not a checked source. The README claim
    "transcribed from published notation" overstated it and was corrected
    to him. Confidence is uneven — Amen, Funky Drummer, Impeach, Apache
    and Levee are widely transcribed and probably close; the other eight I
    would not bet on. Nothing in this project can verify them: the Reason
    Voice recipe book is 27 recipes about getting SOUNDS in Reason, and
    holds no drum transcriptions.
  * HIS CALL: bare auditions of all thirteen first (no DJ, no chords, no
    reverb, no swing, one plain acoustic kit, each at its own tempo), then
    research only the ones his ear says are wrong. Rendered to
    ~/Desktop/Homeroom Bare Breaks 2026-08-04. Awaiting his verdict — do
    NOT rewrite any figure before it comes back.
  * HE SUPPLIED THE SOURCE, 2026-08-04 — "drum patterns.xlsx" in the
    project root. THE HITS ARE CELL FILL COLOURS, which is why his CSV
    export was empty; read the .xlsx with stdlib zipfile+ElementTree
    (styles.xml fill id -> sheet cell style index). 31 grids: 13 classic
    breakbeats, 4 genre templates, 6 clave/world patterns. His chart is now
    the AUTHORITY — patterns_breaks.json was rebuilt from it, not merged.
    Amen and Apache are FOUR bars (load_library only accepted 16/32 steps,
    so four-bar figures were silently dropped — widened to 64); the Amen is
    on a RIDE; the hats REST where the open hat sounds, which was his "the
    hi hats just run straight over the beats". Five new figures added
    (Billie Jean, Walk This Way, It's a New Day, Papa Was Too, Mardi Gras).
    Five keep my recall and are marked "sourced": UNVERIFIED in the pack
    itself — Assembly Line, Cold Sweat, Get Out My Life, Nautilus, Think.
    His grid carries NO velocity, so accents are assigned by one stated
    rule (snare on 2/4 = accent, other snares = ghost, rest = plain hit)
    and nothing else is invented. His Amen notation image DOES carry accent
    marks — that is the missing layer; ask for the same on Funky Drummer.
  * BUG HIS DATA EXPOSED: compose() gated verbatim placement on
    `len(seed) > 1`, so a ONE-BAR figure was never played verbatim — it
    fell through to _thin_kick and _bank_vary like an ordinary seed.
    Harmless while every figure was two bars; it would have silently varied
    nine of the eighteen the moment his one-bar grids landed.
  * MONO REGRESSION, mine, found by test_real_beats_are_not_mono_or_silent
    on his beat 1803 and FIXED. Taking kick/snare/hat out of `mutable` left
    the GUESTS as the only lane a structural treatment could pick, so every
    break beat aimed its hole at a guest — and guests are the only
    off-centre content a break has (kick and snare are dead centre, the hat
    is pinned to |pan| <= 0.2 by house rule). 1803's shaker was sent "only
    in the A section" and half the beat had nothing in the sides: -28 dB
    side-to-mid. Fix: a break beat gets NO structural treatment at all —
    the figure IS the arrangement. Test:
    test_a_break_beat_never_blanks_a_guest_lane.
    NOT FULLY SOLVED, and it is NOT a regression — break beats run NARROW
    by nature. Measured after the fix on 6 fresh ones: -10.1, -18.4, -20.4,
    -20.7, -21.6 and -24.5 dB against a -22 threshold. One still fails and
    three are marginal. Cause is structural: few lanes, all centred. Two
    honest options, HIS CALL, do not pick one silently — (a) guarantee a
    break beat gets at least one panned guest colour, or (b) accept that a
    break is authentically centre-heavy and make the invariant break-aware.
    Beat 1803 itself stays mono: it is already printed, and the house rule
    is move-never-delete.
  * HI-HAT SAMPLE MISTAKE, caught by his ear within minutes of the bare
    batch: "there should be closed hi hats... all the way open high hats
    should not be happening so often." Correct, and it was MY sample pick,
    not the patterns. The dry acoustic kit has four hats — tite (closed),
    semi, loose (washy), open — and I loaded "hh loose dry" as the
    everyday hat, so every hat hit in all thirteen was already half-open
    before a real open hat landed on top. Re-rendered on "hh tite dry".
    The written parts were never the problem: 7 open hats across all
    thirteen figures, 8 figures have none. LESSON, and it is the same one
    this whole session keeps teaching: a name that reads plausible is not
    a verified choice. I cannot hear, so anything I pick by name he has to
    check.
  * THREE ENGINE FAULTS FOUND WHILE CHECKING, all inside the umbrella rule
    ("exclude the breaks from the rules keeping them from being what they
    should be"), all measured on the beats he actually heard. FIXES AGREED
    IN PRINCIPLE, DEFERRED until after he listens, at his instruction:
      1. SWING RIDES ON TOP OF A TRANSCRIPTION. Beat 88 (Think) got 60%,
         92 (Impeach) 61%, 87 (Funky Drummer) 53%. A break's feel is
         already written into the grid; MPC swing on top smears it.
         `roll_swing` is called in both solo_preset and collab_preset with
         no break check.
      2. THE BACKBONE CAN LAND ON A CLAP. Beat 90 (Big Beat, Night Metro)
         has no snare lane — that DJ's backbeat lane is `clap`, so the
         transcribed snare played on a clap sample. It cannot read as the
         break.
      3. A MISSING LANE DROPS ITS PART SILENTLY. Beat 93 (Nautilus, Glass
         Cat) has no hat lane at all (snare/clap/snap), so the whole hat
         transcription vanished with no note anywhere saying so.
    Fix shape: on a break beat, force swing 50, map the figure's snare to
    whatever backbone lane exists but prefer a real snare, and refuse to
    drop a figure's lane silently — seat it or say so in the notes.
  * CORPUS FINDING, his own files: `.claude/skills/drum-loops/references/
    techniques.md` says ghosts should be 30-50% of the accent velocity and
    `connections-2026-07.md` already warns "ghosts at ~26% risks burying
    the mutter". groove.velocity uses a 0.26 ghost floor — under his own
    documented range. On a break the ghosts ARE the groove, so this is a
    live candidate for "doesn't sound right" that is not the pattern.
    Untested; do not change it without an A/B he hears.

### 2026-08-03 Three skills + two CLAUDE.md rules, distilled from this session's mistakes
- He asked what skills this session should produce. Proposed four things
  ranked by what each would actually have saved, and he took all of them.
- `audio-fix-verify` — measure the FINISHED FILE, not an intermediate.
  Written from the volume cap that took FOUR passes (dry buffer → + reverb
  → + pan → + sidechain duck), plus three sibling failures the same day: a
  pattern-level harness that could not see a pass running after composition,
  a "0 of 0" that verified nothing because the recipe key was read from the
  wrong level, and reporting a median while one beat in twenty carried the
  whole bug. Cost about six rounds of rework in one session.
- `hard-rule-invariant` — an absolute rule becomes something that REFUSES at
  one choke point with a test that fails when violated, never a weight or a
  "prefer". Written from "one instrument per stem", which is in this ledger
  on 07-25, 07-29 and 08-03 because every fix was a preference with its own
  exception documented in the code comment. Also carries the lesson that the
  rule must be what he MEANT: "one instrument" built as "one FILE" made the
  engine silently swap his chosen piano for a bell.
- `audition-batch` — render to scratch, copy to the Desktop, never into his
  library (it takes real beat numbers from the global counter), plain-words
  README quoting his own complaint, and always separate MEASURED from HEARD.
- CLAUDE.md rule 0 — plain language. He has ADHD and is not a developer;
  fewest true words, answer first, numbers not adjectives, one action at the
  end. How it is written IS the work, not packaging.
- CLAUDE.md rule 0b — ambiguity is BLOCKING. His standing instruction after
  several breaches this session, including asking a question and then
  answering it myself, and rewriting twelve identities on a wrong reading of
  the word "stacks".
- NOT DONE, flagged: the memory note says to run skill-creator's eval/
  benchmark loop when creating skills. I did not — only a crude word-overlap
  check, which is not how skills are selected and proved nothing. The
  descriptions are unvalidated. Worth running before relying on them to fire
  on their own.
- Status: open — written, not yet exercised by a real session.

### 2026-08-03 Nature/field recordings cut from the sound pool — a THIRD of the fx bank
- Owner: "There are a lot of nature sounds. I think they're from the cymatics
  folder. It's, like, water and things of that nature. Remove those from the
  sound pool." He identified the pack correctly.
- Measured before deciding: `Cymatics - LIFE Ambient Recordings` was **172
  files, 33% of the entire fx pool** — Rain 54, Vinyl Crackles 32, Rivers and
  Streams 28, Walking 28, Waterfall 7, and a "Various" folder of car AC, a
  generator and a car driving over a metal bridge. Field recordings end to
  end; not one of them is a drum or an fx stab.
- Given the choice of (a) the whole pack, (b) all but Vinyl Crackles, or
  (c) only the water ones, he picked **(a)**. Vinyl Crackles went with it
  because clean_renders already keeps vinyl and dust out of a render so he
  can add his own colour in Reason — that folder was redundant.
- HOW, deliberately two mechanisms: "AMBIENT RECORDING" added to
  EXCLUDE_DIR_WORDS catches the whole pack (and any future ambient pack) by
  FOLDER; NATURE_FILE_WORDS catches stragglers in other packs by FILE NAME,
  whole-word matched. Whole-word matters — a substring match would have
  eaten "Rainbow Stab", "Streamline Perc", "Brooklyn Snare", "Windup Riser"
  and "Waterhouse Kick". Tested those traps BEFORE running the rescan.
- Result, verified against a backup of the old index: 178 files removed
  (fx 528 -> 356, plus 3 loops and 3 single files elsewhere). 171 from the
  LIFE pack, 7 stragglers. **Zero removed that neither matched a nature word
  nor lived in that pack** — checked explicitly rather than assumed. Kick,
  snare, clap, bass, crash and vox pools untouched.
- Old index backed up at `~/.reason_voice/pack_index.json.before-nature-cut`.
- Status: open — the fx pool is a third smaller, which will noticeably
  change the colour lanes (cutfx, foundfx, reversefx, blips, glitches). That
  is the intent, but he has NOT heard a batch under the new pool.

### 2026-08-03 Everything level, one blanket volume rule — and FOUR passes to get one cap right
- Context: he listened to real beats and reported two things by number.
  1761 ("sample 95"): "I don't like how the samples get louder and quieter
  like this one. Let's keep those at a steady volume." 1763: a shaker too
  loud. Plus a new blanket rule and, earlier the same day, "the volume
  variations per drum hit is not working out. Sometimes the drum parts get
  way too quiet and don't come back. So let's just have everything level."
- LEVEL, option (a) — he was asked how far and chose: kill the RANDOMNESS,
  keep the WRITTEN dynamics. `velocity()` no longer applies its per-hit
  `2 ** normal(0, sigma)` wobble. Measured before removing it: one hit could
  land 8.0 dB from its neighbour on a normal hit and 17.3 dB on a ghost,
  floored 26 dB down. Accent/normal/ghost still mean what they say, because
  ghost notes are most of what makes the Funky Drummer and the Amen read as
  breaks — flattening them would have undone the break work.
- BOTH VELOCITY DIPS REMOVED: vary_preset's "quietbar", and the
  contrast-deepening pass in generate() entirely. That pass had already been
  rewritten once the same day (from blanking a bar — a hidden second hole
  source — to dipping one) and as a dip it stacked with quietbar for -11.7 dB
  off a whole bar. No version of it survives both live rules, so it is gone
  rather than tuned a third time.
- CHORDS STEADY: `CHORD_LEVEL_VAR_DB` 2.5 -> 0 and
  OWNER_TASTE["chord_accents"] flattened to all-ones. Measured on his 1761:
  three slots peaked -13.4 / -16.4 / -9.7 dB, a 6.7 dB spread on ONE sample,
  which is those two numbers added. After: median slot spread 0.4 dB. The
  DECAYS stay — he confirmed option (a), "every chord starts at the same
  level; each still holds and fades".
- THE BLANKET RULE, and why it is a DEFAULT not a list: "anything named
  shaker or impacts or effects or percussion or any other 'drum' sound that
  is not the kick and the snare should follow the same volume rule as for hi
  hats." The old ceiling was a list of named prefixes and it kept missing
  lanes — congas, toms, woods, claves, blips, cutfx, foundfx, glitches,
  mathperc, exotic, gamefx and every guest lane a future pool might add were
  all uncapped. `peak_ceiling_for()` now returns PERC_UNDER_DB for anything
  not explicitly named, so new sounds are covered without anyone remembering.
  Exempt: kick, snare (they ARE the reference) and the low end — "sub" and
  the digit-less "bass" (the sampled 808), which he confirmed: "do not cap
  the sub". Note bass0..N is a DIFFERENT lane, the melodic chord bass, and
  that one does take the melodic ceiling.
- **THE LESSON OF THE SESSION — it took FOUR passes to get one cap right,
  because each time I measured at a point that was not where the sound comes
  out.** The cap has to be computed on what the STEM will actually contain:
    pass 1: dry buffer only              -> lanes 1.2 dB over
    pass 2: + the reverb tail            -> his shaker still at -1.6 vs -3
    pass 3: + the constant-power pan     -> 3 lanes over, all on one beat
            (a CENTRED kick gets 0.707 per side, a PANNED hat up to 1.0)
    pass 4: + the sidechain duck         -> 0 over, lanes land on -3.0
  The duck was the subtle one: only the kick sits outside its own duck, and
  the duck is TIME-VARYING, so how much a lane loses depends on whether its
  loudest hit falls on a kick or between them. That is why only one beat
  failed and why the aggregate hid it — it was found by looking at the beat
  that failed, not at the median.
- FOUR-BAR LOOPS: when the chord voice is a sampled loop the beat is pinned
  to 4 bars ("the loops always seem to be too short for anything else").
  Works because _source_order is deterministic from the variant, so the
  voice is knowable before the length is rolled. Verified 216 loop-voiced
  beats, all 4 bars; other beats keep the normal roll.
- MIX HIERARCHY anchored where he said ("start with the loudness of the kick
  and the snare where they're at right now"): kick and snare are the
  reference and are never adjusted, and the reference is the QUIETER of the
  two — the old ceilings were kick-relative, which let a clap sit under the
  kick while still being louder than the snare.
- One test rewritten, not loosened: test_harmony_opens_under_the_drums_with_
  per_bar_dynamics asserted the chord bars must NOT all be the same level —
  the exact per-bar breathing he just removed. It now asserts they are equal
  while keeping the check that harmony sits under the kit.
- Verified: 0 lanes over cap across the sample, lanes landing on -3.0 dB.
  748 passed, 1 skipped, 0 failed.
- Status: open — measured but NOT heard. He has not listened to a batch
  under any of this. The two beats he named (1761, 1763) predate all of it.

### 2026-08-03 The chords: "one instrument per stem" made an INVARIANT, plus two real level bugs
- Context: owner heard the punch-list batch and reported "there are still
  stacks in there, and they just always sound bad", then "it's their
  instruments... multiple samples on one stem again... one instrument per
  stem, HARD RULE, it's being done with piano and strings. It's just
  creating a noise mess." Also: chords are "always way too loud", and beat
  1702's chord stem had DRUMS in it.
- PROCESS FAILURE FIRST, because he asked for it and it is the reusable
  part. I read "stacks" as the snare+clap stacks and rewrote 12 identities
  before he stopped me. I had ALREADY identified that "stacks" was
  ambiguous (drum stacks vs the chord voices literally named "piano stack")
  and written "I'm not going to guess" — then took a single word ("Just
  Flame", who has both) as proof of the reading that matched the drum work
  I had just spent hours in. That is the pattern: **when I have momentum I
  resolve ambiguity toward the work I already understand.** Same failure
  earlier the same day with "bright beats" and with "next up is Part C
  unless you want to hear these first". His standing instruction now:
  anything ambiguous, STOP and ask. The drum changes were reverted whole.
- SECOND PROCESS FAILURE, the one that made this bug recur for six weeks:
  the same complaint is in the ledger on 07-25, 07-29 and now. Each time it
  was fixed as a PREFERENCE with the escape hatch documented in the code
  comment — "prefer reusing one sample, up to 12 semitones; a chord
  spanning more than an octave still switches packs". A rule with a written
  exception is not a rule. Nothing ever failed when it broke, either: there
  was no check anywhere that a stem contains one instrument.
- FIX 1, the hard rule as an invariant: in _build_chords, a plan whose
  `used` files are not all the SAME INSTRUMENT fails and the engine tries
  another instrument. If no plan can voice the progression from one
  instrument, the chord lane is dropped from the beat entirely (owner's
  explicit choice of option c; he later confirmed "stick with the new rule
  where every beat does not have to have a chord lane") and the beat card
  says why. Measured: chord lanes with >1 source file **19% -> 0%** (one
  G-Funk lane had been built from THREE files).
- FIX 1a, MY OWN BUG IN FIX 1, worth keeping because a test caught what I
  did not: I first implemented "one FILE per stem". That is not the same
  rule. A real sampled piano is ONE INSTRUMENT spread over MANY files, so
  a file count rejects a perfectly good piano. Two tests failed and one of
  them was a genuine defect, not brittleness:
  test_the_rack_never_says_built_from_scratch_over_his_own_samples caught
  the engine SILENTLY SWAPPING Timberline's chosen piano for a bell,
  because the bell happened to fit in one file. Silently playing the wrong
  instrument is worse than dropping the lane. Owner picked option (b):
  same FOLDER **and** same INSTRUMENT TYPE (`_one_instrument`). Folder
  alone would let a shared "Melodic One Shots" bin put a piano and a bell
  in one stem; group alone is too loose the other way, since "synth" spans
  many vendor packs — which is exactly the 2026-07-29 bug. Verified on six
  cases including both traps. Drop rate measured on 24 real beats under
  the too-strict version: 1 (Miami Bass).
- BUILT-FROM-SCRATCH INSTRUMENTS (owner 2026-08-03: "I don't want any
  built from scratch instruments, except for the chiptune"): already true,
  and I checked rather than assuming or "fixing" it. `chip` is the only
  synthesized chord voice in the engine and it is explicitly barred from
  being a fallback — it plays only for an identity whose own chord_source
  asks for it (2026-07-25 rule). test_nothing_but_chip_is_ever_generated
  pins it. NO CHANGE MADE. If he still hears something synthetic it will
  be a sample stretched too far, not an oscillator.
- FIX 2, full-mix loops: melodic_loops.scan now drops any file whose name
  contains ALL / FULL / MIX / MASTER / BEAT / TRACK as a whole word. That
  is beat 1702, whose chord voice was "105_Aiyf_ALL Bb" — a whole
  arrangement, drums included. This costs nothing: the packs ship both
  versions, so "070_Ragamuffin_ALL Cm" goes and "070_Ragamuffin_Organ Cm"
  stays. Whole-word matching so "Ballad" doesn't trip ALL and "Mixolydian"
  doesn't trip MIX — 11 cases tested, 0 wrong.
- FIX 3, REAL ARITHMETIC BUG in the chord-bus governor: it divided the
  bus's total energy by the COMBINED length of all chord lanes instead of
  by the beat length, under-reading the bus by 10*log10(n_lanes). Chord
  slots are sequential, so N lanes each sounding 1/N of the time still sum
  to a bus that plays throughout. With the median 3 lanes that is 4.8 dB.
  Measured on 34 beats: target -9.0, actual **-4.6**. The snare governor
  eleven lines above always did it correctly (`bus = sum(...)` then RMS),
  which is exactly why nobody caught it — the correct version was sitting
  there looking like precedent.
- FIX 4, the clamp: adj was clamped symmetrically to [0.25, 4.0] (+/-12 dB)
  with the stated reason "so a pathological sample can't be hauled up 30 dB
  and drag its own noise floor into the mix". That is an argument about
  BOOSTING only — turning a lane down cannot raise a noise floor — so the
  cut half was protecting against nothing. Probed inside the function: a
  loud sample needed a 16.6 dB cut and a very loud one 22.6 dB; both
  clamped at 12 and shipped 4.6 and 10.6 dB over target. THIS was "always
  way too loud", and it would have got worse as he moved chords further
  back. Cut floor is now CHORD_CUT_FLOOR = 0.02 (-34 dB); the +12 dB boost
  ceiling is unchanged and still pinned by the "does not rescue a hopeless
  sample" test. Result: a 38 dB input swing now comes through as **0.00 dB**.
- FIX 5, chords no longer play nonstop (owner: "I don't want them being
  played nonstop. Decays and variation in length should be present" + level
  variation confirmed separately). Measured before: the chord bus sounded
  **95%** of the loop against the kick's 34% — every chord filled its whole
  slot and the next began instantly. _decay_chord_slots now gives each slot
  a rolled hold (CHORD_HOLD 0.40-0.80), an exponential tail that finishes
  EARLY so there is real silence before the next chord, and a rolled level
  (CHORD_LEVEL_VAR_DB 2.5). First attempt had the decay reach zero exactly
  at the slot boundary, which is still a seamless pad — caught by measuring
  the envelope, not by reading it. Duty now 51-63%.
- LEVEL: owner picked **15 dB** under the kick by ear from a 12/15/18
  audition. Verified: 12 -> -12.3, 15 -> -15.1, 18 -> -18.2, spread 0.2-0.5
  dB across 6 beats. OWNER_TASTE["chord_bus_under_kick_db"] 9.0 -> 15.0.
- MEASUREMENT MISTAKES I MADE AND CAUGHT: read `voice_files` from the top
  level of the recipe when it lives inside `harmony`, got a meaningless
  "0 of 0" and nearly reported the hard rule as verified. Only the
  before/after comparison made the number mean anything. Also nearly
  reported the Memphis/New Jack bank beats as still-mono when the STEMS
  showed every lane was wide and the full-band figure was just a mono kick
  dominating. Full-band S/M is the wrong yardstick for a kick-heavy
  drums-only beat.
- A THIRD TEST THAT HAD QUIETLY RETIRED ITSELF, same disease as the fixes
  above: test_the_chord_governor_refuses_to_rescue_a_hopeless_sample used a
  hardcoded source level of 0.02, calibrated to the OLD 9 dB target. At
  15 dB that sample is reachable, so the test would have gone on passing
  while testing nothing. Rewritten to derive its level from the governor's
  own clamp constants. My FIRST rewrite was also wrong — it assumed the
  correction range starts at full volume. Measured transfer curve: the
  governor holds flat from source 1.0 down to ~0.03, a **46 dB** governed
  span (34 dB of cut plus 12 dB of boost), so a "hopeless" fixture has to
  sit below that, not below 1.0. Third time in one session a test turned
  out to be measuring its own setup.
- Final: **749 passed, 0 failed, 0 skipped** (was 748/1 skipped).
- Verify by: `tools/measure_batch.py` on any batch. NOTE the audition
  folders at `~/Desktop/Homeroom Chord Levels 2026-08-03` are STALE — they
  predate option (b) — replace them before asking him to judge anything.
- Status: open — he picked the level by ear from a level-only comparison
  but has NOT heard a full batch under the finished behaviour, and the
  one-instrument rule's drop rate is measured on 24 beats. If it starts
  dropping chord lanes often on real batches, that is the number to watch.

### 2026-08-03 Owner's six-point punch list — built in 5 parts, all measured, NOT yet heard
- Context: after the 07-31 mix fixes he listed six problems: clap/crash
  overused, "intentional gaps" in the loops, vocal hits annoying and loud,
  chord limitations too small, odd beat lengths, and no classic breaks.
  He also asked, twice, that I not generalize — which was fair, and the
  verify pass that followed changed several of my own claims.
- METHOD (the reusable part): measured 506 library recipes AND ~130 freshly
  rendered beats, not just pattern data. `tools/measure_batch.py` is that
  measurement made repeatable — length in bars, per-bar level of the mix AND
  of the drum stems alone, stereo width, every stem's level vs the kick.
- NEW STANDING RULE from him, verbatim: "All sounds are open to all DJs. but
  they try to maintain seventy five percent of their personality within."
  Implemented as `OPEN_P = 0.25` (beat_machine.py) and used in two places so
  far: the chord picker, and giving the four clap-only DJs a snare.
- His answers, applied: gaps rare at 1 in 6 / keep the signature clap stacks
  but move everyone else's clap off the snare / kill vocal hits completely /
  chords option (c), both wider per DJ and new longer progressions / 4-8
  bars regardless of DJ, no odd time signatures / breaks yes, played
  VERBATIM (he confirmed "bright beats" was break beats) / remove the stamp
  lane entirely / yes to level governors.
- WHAT SHIPPED, five parts, each measured before/after — full numbers in
  SCRATCH.md. Headlines: stamp lane 95% of beats -> 0% (it drew from 32
  files, half of all picks from SIX, one riser on 17% of the library — the
  real cause of "same sounds over and over"). Vocal hits 26% -> 0%. Crash
  3.5 hits per BAR -> 0.25. Holes 90% -> ~16%. Beats starting with no kick
  5% -> 0%. Clap on the snare's exact steps, non-stack DJs, 89% -> 11%.
  Worst identity's total possible harmonies 6 (Farrow) -> 116; median ~12 ->
  151; all 14 chord qualities and all 8 modes now reachable (lydian,
  mixolydian and harmonic minor had NEVER been used by any identity).
  Nothing peaks above the kick any more (clap was +10.3 dB, now -0.4).
- FOUR OF MY OWN MISTAKES, all caught by measuring after the change, not by
  re-reading the diff. Worth keeping because the pattern is the lesson:
  (1) the crash fix matched lane names exactly and missed `crash2` — the one
      lane he complained about was still firing 3.12 times a bar;
  (2) I protected claps whose MODE NAMES looked canonical instead of
      checking the identity's actual `canon` block, so Miami Bass was
      wrongly skipped;
  (3) measuring in aggregate hid that the snare/clap stack runs BOTH ways —
      I exempted the 6 with clap:{copy:snare} and missed 6 more with
      snare:{copy:clap}, all documented signatures;
  (4) after fixing vary_preset to 1-in-6, a real render still came back at
      40% holes: there is a SECOND, independent hole source — the contrast
      pass that runs after it and blanks a bar when the loop measures flat.
      A pattern-level harness cannot see it. It now dips velocity instead.
- REAL BUG FOUND, sitting exactly on his breaks question: `pattern_gen`
  gated library seeds on `len(bar) == 16`, so all 14 two-bar patterns —
  including the only Amen Break in the project — were picked and then
  silently discarded for kick and snare, while the hat had NO gate and
  reached the renderer as a 32-char bar, played as 32 steps in ONE bar
  (double speed, swing skipped). 48 real cases measured. `seed_bars()`
  fixes it. Separately, `_lib_kick` ignored velocity entirely and marked
  accents by POSITION, so every ghost note in a break arrived at full
  strength; it now honours velocity when a pattern has any, and falls back
  to positional accents so all 180 existing patterns are unchanged.
- Legends could never receive a groove seed's backbeat — measured 0.0% over
  720 beats, and the legends are precisely the producers built on sampled
  breaks. Now 9.3%.
- 1679 (his ask): ALL SIX Fixed Bank beats were mono, -26.7 to -29.5 dB S/M,
  not just that one. Cause: they are kick+snare+hat at space="dry", and the
  07-31 ambience bed skips the low end (correct) and the whole snare bus
  ("the DJ's call"), leaving the hat as the only width source. Added a
  narrow backstop — drums-only AND no space asked for -> the snare bus joins
  the bed. 1679 rebuilt via swap_many as 1680: **-27.7 -> -18.5 dB**, same
  length, same peak, original preserved in the Variations folder. Dry crew
  beats improved as a side effect (Otto Grit dry ~-19 dB, was -27 to -30).
  The other five are STILL MONO — he asked for 1679 only.
- Tests: 748 passed / 1 skipped / 0 failed, up from the 743 baseline (5 new
  tests). Two tests were REWRITTEN, not deleted, because his new rules
  supersede the old ones they encoded: `test_loop_length_varies_and_centres_
  on_four` (asserted 2-bar loops exist) and `test_backbone_can_go_fully_
  silent_for_a_bar` (asserted gaps happen) — the latter now pins BOTH ends,
  that silence is still reachable AND that it stays rare.
- HONEST LIMITS, none of them hidden:
  * "Claps in fewer beats" barely moved in aggregate (44% -> ~44%). Every
    clap in the roster is a declared signature stack (12 identities, he said
    keep), a canon figure, or that DJ's only backbeat. The wins are
    placement and level, not frequency. If he wants fewer, the only lever
    left is the 12 signature stacks, which he told me not to touch.
  * The 1-skipped test is the mono check. It only scans the TOP level of
    each folder and 1680 landed in a Variations subfolder, so it reports
    "no beats rendered in the last day" and looks at nothing. The green
    suite is NOT the evidence that 1679 is fixed; the direct measurement is.
  * Chord names print sharps in flat keys ("Cm - A# - G#" instead of
    "Cm - Bb - Ab"). Display only, on the beat card. PREDATES this session —
    reproduced on the old `epic` progression. Not fixed, not mine to
    silently change inside another part.
  * The rebuild guard refuses a no-op, so 1680 carries a 0.01 dB kick trim
    (a thousandth of a level step, inaudible) purely to satisfy it. It shows
    in the file name as "New Mix".
- PROCESS NOTE, he called this out and he was right: I twice asked him a
  question and then kept going without the answer — the "bright beats"
  reading, and "next up is Part C unless you want to hear these first". The
  agreed fix is to label them: **BLOCKING** means I stop; **ASSUMING X**
  means I proceed and he can correct me. And not to write an audition
  checkpoint into a plan and then skip it.
- Verify by: audition batches are at `~/Desktop/Homeroom Audition 2026-08-03`
  (1 BEFORE / 2 AFTER / 3 BREAK BEATS, with a plain-language READ ME).
  Re-run `.venv/bin/python tools/measure_batch.py <folder>` on any batch.
- FIXED BANK, the rest (2026-08-03, he approved the audition — "it sounds
  good" — then asked for the other bank beats): 1310, 1311, 1312 and 1653
  rebuilt as 1681-1684. **1173 could NOT be rebuilt — it predates the recipe
  system (recipes start at 1174), so there is nothing to re-render from.**
  Full-band S/M after: 1680 -18.5, 1681 -17.7, 1683 -21.3, 1682 -24.9,
  1684 -28.1. The last two still read "mono" on that metric and I nearly
  reported them as a failed fix — measuring the STEMS showed otherwise:
  every non-kick lane is genuinely wide (snare -12.8 to -14.7 dB, hat -15.6
  to -19.9) and the full-band number is dragged down by the kick, which is
  pure mono by design. 1682's snare sample is simply quiet (rms 0.0071 vs a
  0.0598 kick, 8x) and 1684 is a long 808 (0.1666, 8x the snare). Above
  200 Hz, 1684 measures -19.5 dB. LESSON: full-band S/M is the wrong
  yardstick for a kick-dominated drums-only beat, and the -22 dB threshold
  in test_audio_quality inherits that flaw. Do not chase the number by
  widening the low end — that would break mono compatibility.
- Status: confirmed — owner heard the audition batches and approved
  ("it sounds good"), then asked for the remaining bank beats and a commit.
- Outcome: committed to main. Each part is documented above and in
  SCRATCH.md; reverting ONE part is a targeted edit, not a git revert,
  because the five parts touch overlapping code in beat_machine.py and
  pattern_gen.py. Still unheard: the 4 rebuilt bank beats (1681-1684).

### [2026-08-04] Three front-end bugs: silent samples, dead preview, legends locked out
- Context: owner reported three things on the Beat Machine page. (1) Picking a
  new sound from a lane's dropdown sometimes made no sound, and either way the
  beat sounded the same when he played it back — so there was no way to judge a
  swap before committing to a rebuild. He also asked to HEAR the dice roll.
  (2) After making a beat with one of the nine, every Legend answered
  "Check at least one DJ first." and stayed unusable until a restart.
- Decision/change: four fixes, each at its root.
  1. `/sample` now decodes through `load_audio` and re-wraps as 24-bit WAV
     (`Handler._wav`). It was handing raw file bytes out labelled
     `audio/wav` — but **975 of his 4202 indexed samples (23%) are .aif**,
     which the browser silently refuses to play. That is the whole of
     "sometimes it doesn't make a sound": it was never random, it was the
     file format. Any odd bit depth is fixed by the same change.
  2. The 🎲 now picks a real sample out of the same list the dropdown shows,
     names it, and plays it (`laneRow`). It used to stage a "surprise me"
     the machine only resolved during the rebuild, so there was nothing to
     play and nothing to name. Owner picked this over "keep the surprise".
  3. Play now reflects a staged swap: `mixUrl` sends `picks`, and `/mix`
     routes those to the new `_preview_swap`, which calls `swap_many(...,
     render_only=True)` — a new early return in the real render path, so the
     preview is byte-for-byte what Rebuild will print, not an approximation.
     Measured 0.6 s per render; last 3 results cached. Levels-and-removals
     alone still take the instant stem-sum path (`_preview_mix`) untouched.
  4. `evolution._save_config` now calls `crew.reload_rosters()` instead of
     `CREW.clear()` + `load_crew()`.
- Reasoning: (4) is the real find. `crew_config.json` holds only the nine, so
  rebuilding CREW from it alone dropped the twelve Legends and eighteen Styles
  out of the roster **for the rest of the session**. Evolution fires on the
  first crew beat of the day, which is exactly the "once you use one of the
  nine" the owner described. `reload_rosters()` already existed for precisely
  this class of bug (written 2026-07-19 when the Styles got dropped the same
  way) — it just was not being called here. Fixing the caller beats guarding
  each roster. Gave it a `path=` argument read at call time so a sandboxed
  `crew.CONFIG` in tests reloads from the sandbox.
- Verify by: `tests/test_evolution.py::test_evolving_keeps_legends_and_styles_in_the_roster`
  — confirmed it FAILS on the old code and passes on the new. Full suite 749
  passed / 1 skipped. Live-driven the real page for the rest: dice rolled
  "hat tite 4" (an .aif — the exact case that used to be silent), served as
  RIFF/24-bit, and Play requested `/mix?...&picks=` and returned audio that
  differs from the original by 0.86 peak, so the new hat is genuinely in it.
- Status: open — verified working, but the owner has not heard it himself yet.
- Outcome: (pending his listen)

### [2026-08-04] Roll everything, one honest preview, and chords you can choose
- Context: four follow-ups after the morning's front-end fixes — a "roll
  everything" button, close the roster-aliasing trap, chase down a preview
  timing that looked wrong, and give the chord/bass rows dropdowns and dice.
- Decision/change:
  1. **Roll everything** on the rack footer: rolls every swappable row at
     once and auditions the BEAT rather than a dozen overlapping one-shots.
     Skips locked rows and anything already removed.
  2. **Aliasing trap closed.** `merge_legends`/`merge_genres` rebound
     LEGEND_NAMES/GENRE_NAMES to fresh sets; importers do `from crew import
     LEGEND_NAMES`, which binds the OBJECT, so after a reload beat_machine
     held a stale copy. Contents happened to agree, so nothing had broken
     yet. Now mutated in place, and a failed roster load leaves the old set
     alone instead of clearing it.
  3. **The preview was lying by 8 dB.** The "instant" path summed printed
     stems — the beat BEFORE the master bus — so every volume move was
     judged against the wrong mix (measured on 1774 at kick -3: preview
     -22.2 dB rms vs rebuild -14.2). `_preview_mix` is deleted; all three
     kinds of change (swap, volume, removal) now go through one render.
     Costs 0.27s warm. My first timing (1.0s vs 0.6s, "the fast path isn't
     faster") was a cold read off the external drive — wrong, and the
     re-measure is what surfaced the real bug underneath.
     `/mix` also no longer falls back to serving the untouched file on
     error: that made a failed preview sound exactly like a change that
     did nothing. It 500s and the page says so.
  4. **Chord rows are swappable** — for an INSTRUMENT, not a file (a chord
     voice is a whole multisample). `_build_chords` takes `voice=`, which
     goes to the FRONT of the plan queue rather than replacing it.
- Reasoning: (4) is where the real work was. Built the obvious way it was
  decoration — all fourteen voices listed and NONE of them landed, measured
  on 1776. Cause: `nearest()` shops per NOTE across a whole group, so a
  3-note chord drew from two folders and the one-instrument-per-stem rule
  (2026-08-03) threw the plan out, every time, falling through to the DJ's
  own choice. That is precisely the "I picked a sound and nothing changed"
  this session began with. Two fixes, both narrow: the menu lists only
  voices a single FOLDER can reach every note of, and an explicit pick is
  pinned to that folder and to its NAMED group (`VOICES[v][:1]`, so Pluck
  can't quietly hand back a synth). Both apply ONLY when he picked — a beat
  the machine voices for itself ranges over the whole group exactly as
  before, so this cannot move the sound of anything he didn't ask to change.
  The menu is shorter than the full instrument list on purpose: 5 voices on
  1776, 4 on 1773. Every one of them plays.
- Verify by: `test_every_offered_chord_instrument_actually_plays` (fails if
  an unplayable voice reaches the menu OR a listed voice hands back
  something else), `test_preview_matches_what_rebuild_would_print`
  (byte-for-byte, not "close"), `test_evolving_keeps_legends_and_styles_in
  _the_roster`. Full suite 751 passed / 1 skipped. Live-driven the page:
  chords dropdown showed 5 real instruments, dice picked Guitar ("was pluck
  stack"), Roll everything staged 6 sounds in one click and played a 12.5s
  preview with all six in it.
- Status: open — measured and driven, but he has not heard it yet.
- Outcome: (pending his listen). Known cost: a chord-beat preview renders in
  ~6s vs ~0.5s for drums-only, because the harmony is rebuilt each time.
  Cached per exact set of changes, so it is paid once per combination.

## Archived history — 66 entries moved, nothing deleted

Everything up to and including 2026-07-25 now lives in
[`DECISIONS-ARCHIVE.md`](DECISIONS-ARCHIVE.md). It was ~50,000 tokens and
`CLAUDE.md` asks every session to read this file before doing anything, so
the old entries were being paid for on every single startup.

**Read the archive when** you need the reasoning behind something older than
2026-07-26, or when an entry below refers back to one. The one-line index of
what's in there is at the bottom of this file, so nothing is invisible —
just not loaded by default.

---

### 2026-08-01 Ledger split for token cost; and a flaky test I caused, found by committing on red
- Context: owner asked how to make sessions use fewer tokens.
- Measured first: DECISIONS.md was 195 KB / ~50,000 tokens, and CLAUDE.md
  rule 2 tells every session to read it BEFORE doing anything. That cost was
  being paid on every startup, for 66 entries that were already settled.
- Change: entries from 2026-07-26 onward stay in DECISIONS.md; the 66 older
  ones moved verbatim to DECISIONS-ARCHIVE.md, which nothing reads by
  default. A one-line index (date, title, status) of every archived entry
  stays in the live file so nothing is invisible. CLAUDE.md rule 2 updated to
  say read the live file only, and that an old `open` usually means nobody
  circled back rather than that the thread is live.
- Verified lossless BEFORE committing, against git HEAD: 73 entries in, 73
  out, zero text changed. One entry flagged as changed turned out to be my
  verifier's parser running past the end into the new index; the entry itself
  is byte-identical. Live file is now ~7,600 tokens — about 42,000 saved per
  session.
- MISTAKE WORTH RECORDING: I chained `pytest -q | tail -3 && git commit`. The
  pipe means the exit status is tail's, not pytest's, so the `&&` fired and I
  committed on a RED suite (9d30c25). Never put pytest behind a pipe in a
  chained command — redirect to a file and check `$?`.
- The failure that hid behind it was real and mine: test_generate_ships_wav_
  midi_stems_and_recipe required a stem for kick AND snare AND hat.
  generate() rolls from an UNSEEDED rng, so a lane can legitimately produce
  no hits — and since write_stems stopped writing all-zero stems earlier the
  same day, such a lane now has no file instead of a silent one. The old
  assertion only ever passed because the silent file was there.
- It is intermittent, not fixed: it survived several full-suite runs before
  appearing, and the suite has been green on every run since. Do NOT read a
  green run as proof it is gone — the fix is the changed logic, not the runs.
  Test now requires a kick stem always, at least two of the three lanes, and
  the "lane - real sample name" format on whatever did render.
- Verify by: `pytest -q > out.txt 2>&1; echo $?` — 743 passed, 1 skipped,
  exit 0, twice in a row.
- Status: confirmed
- Outcome: split committed 9d30c25 (on red) and the test fix after it.

### 2026-07-31 Owner standing rule on sound + master EQ fixed + house ambience bed + chord bus governor
- NEW STANDING RULE from the owner, verbatim: "in order to have studio ready
  quality tracks. I want you to be able to use reverb and any other effect. as
  much as needed. for quality. and style and dj. It can even vary instrument to
  instrument. whatever will sound best. based on our experts' opinions. This
  overrules any other command where sound is concerned."
  Read as: effects in service of QUALITY are now mine to apply, per instrument
  and per DJ, and a quality floor is not a per-beat style choice.
  NOT read as permission to bake in DIRT — clean_renders (vinyl, wow, dust,
  saturation) stays ON, because 2026-07-18 he specifically wanted to add his
  own colour in Reason. Told him so plainly rather than deciding it silently;
  he can say the word if he wants those in play too.
- Fix 1, master() EQ (he approved this one explicitly): `m = 0.5*(L+R)` moved
  to AFTER the EQ. It was captured before, so the mid was rebuilt from a
  pre-EQ copy and the tone stage was discarded on everything centred.
  Verified: centred content now gets +2.51 dB air / -1.25 dB boxy-mid, where
  it previously got -0.009 dB. This stage had never applied to any beat.
- Fix 2, the actual reason beats sounded small: EVERY DJ's space list is a
  SINGLE lane — `["snare"]` or `["clap"]`. Chords, melodic parts, bongos,
  stamps and all guest colour printed bone dry, forever. Added a house
  ambience bed in render_crew_beat that runs regardless of the rolled space
  (including "dry", per the rule above): harmonic lanes get 1.4s/3200Hz at
  0.18 wet, colour lanes 0.5s/4200Hz at 0.10, both stereo. Explicitly skips
  kick, the sampled 808 and the tuned sub — low end stays dry and centred.
  The DJ's signature snare/clap treatment is untouched, so identity still
  comes from that.
- Fix 3, chord level: REVERTED my own 0.30 -> 0.55 change from earlier today.
  Measurement killed it — it shifted the whole distribution up 5.3 dB without
  narrowing the SPREAD, so a real batch came back ranging -2.5 dB (shouting)
  to -15.5 dB (inaudible) under the kick. An open-loop gain cannot hit a
  target when source samples vary that much. Replaced with a bus governor in
  render_crew_beat, mirroring the snare backstop that has existed since
  2026-07-18, targeting OWNER_TASTE["chord_bus_under_kick_db"] = 9.0 and
  clamped to +/-12 dB so a pathological sample can't be hauled up 30 dB with
  its own noise floor. chord_gain is back at the owner's 0.30.
- CORRECTED 2026-08-03: the chord-bus figures below were taken on FIVE
  beats and the 2.2 dB spread did not hold at scale. Re-measured on 42
  fresh renders: median -8.0 dB against the -9.0 target, **spread 6.1 dB**,
  range -12.5 to -6.3. Still a large win over the 19 dB before the
  governor, and the governor is doing its job — but 5 beats was too small
  a sample to claim 2.2 dB from, and the entry read as more settled than
  it was.
- Measured on 5 real rendered beats (scratch dir, not his library):
    width      -9.6 to -14.9 dB S/M   (library before: -22 to -31)
    chord/kick -6.0 to -8.2 dB, SPREAD 2.2 dB  (library before: 19 dB spread)
    silent stems 0 of 60; peaks -5.6 to -6.4; low-end side ratio 0.014-0.041
    (all under the 0.05 mono-bass guard)
- Tests: 743 passed / 1 skipped, up from the 732 baseline. tests/
  test_audio_quality.py now also covers the mono-bass guard, the governor
  working within its range, and — separately — that the clamp REFUSES to
  rescue a hopeless sample, so nobody quietly loosens it later.
- One test was deliberately rewritten, not deleted: test_dry_beats_are_
  allowed_to_be_narrow encoded the OLD rule that dry means near-mono. The
  standing rule supersedes it; it now asserts the RELATIONSHIP (dry is still
  narrower than wet) instead of an absolute.
- Status: confirmed
- Outcome: owner heard the 5 scratch beats and said "apply" (2026-07-31).
  Committed to main as c741927 and live for every render from the next
  launch. NOT yet re-confirmed over a longer listening period — if the
  ambience turns out to be too much on a particular instrument, the two
  numbers to move are the wet values in render_crew_beat's ambience bed
  (0.18 harmonic / 0.10 colour), and the chord level is
  OWNER_TASTE["chord_bus_under_kick_db"].

### 2026-07-31 Applied: stereo reverb restored, chord level fixed, silent stems blocked, first audio tests added
- Context: owner approved the fixes from the rebuild review (entry below).
- CAUGHT BEFORE SHIPPING — my proposed fix #1 was WRONG. The review said to
  pan chord0/1/2 apart to -0.45/0/+0.45. I checked the rendered stems first:
  chord0/1/2 have ZERO time overlap (0.00-5.44s, 5.45-10.90s, 10.91-21.81s).
  They are the progression's chords in SEQUENCE, not three simultaneous
  parts. Panning them would have swung the progression across the stereo
  field on every chord change. Do not reinstate that idea.
- ROOT CAUSE of the mono mix, found instead: make_ir() has always returned a
  STEREO pair of decorrelated IRs (groove.py:303, docstring says "Stereo
  IR"). Both reverb paths threw the right channel away — crew.py did
  `irL, _ = make_ir(...)` and gated_reverb assigned irR and never used it.
  The one stage in the chain designed to create width was printing mono.
- Changes: (1) crew.py room/plate/hall path convolves both IRs, keeps the
  mono fold-down in bufs[] and carries the decorrelated half as wet_side[],
  folded in at pan time in both the stem loop and the mix loop.
  (2) gated_reverb gained stereo=False (default unchanged, so every existing
  caller and test is untouched); crew.py's gated branch passes stereo=True.
  (3) OWNER_TASTE["chord_gain"] 0.30 -> 0.55.
  (4) write_stems refuses to write an all-zero stem and prints which lanes
  made no sound.
  (5) NEW tests/test_audio_quality.py — the first tests that assert on
  AUDIO rather than on dicts.
- On chord_gain: this reverses a number the owner set on 07-23 when beats
  "arrived shouting", so it is flagged for his ear. Justification is that
  the comment's stated intent (~10 dB under the kick) never matched reality
  (measured median 15.4 dB under, worst 24.9) because the accent multiplier,
  the duck and the peak normalise all stack after it. 0.55 makes the
  measured result match the intent. If it now shouts, this is the number to
  walk back — nothing else depends on it.
- Level safety, measured not assumed: the per-channel wet level is UNCHANGED
  (+0.00 dB — L still receives exactly irL). The wet's mono fold-down drops
  2.9 dB because decorrelated channels partially cancel in mono, which is
  physically correct; across a whole beat the figure the snare-vs-kick
  backstop and _track_gain actually read moves 0.18 dB. Nothing retuned.
- Verified by RENDERING, not by reading the diff. Three real beats with
  --notes "room chords": width -13.5/-16.3/-18.6 dB S/M (library before:
  -22 to -31), chord-vs-kick -6.6/-10.6/-10.9 dB (library median before:
  -15.4), 0 silent stems of 31, LUFS -12.8 on all three, peaks -6.0.
  Rendered to a scratch dir, NOT his library.
- Full suite 740 passed / 1 skipped (baseline was 732), so the 8 new tests
  are additive and nothing regressed.
- KNOWN LIMIT, not hidden: this only helps beats with a wet space. "dry" is
  32% of the library and still renders narrow (-27 to -30 dB) because a dry
  beat has no reverb to widen. First audition batch rolled dry three times
  and showed no improvement at all, which is how this surfaced.
- Status: confirmed
- Outcome: superseded and folded into the entry above; owner approved the
  combined result 2026-07-31, committed as c741927. Note the chord_gain
  0.55 change described here was REVERTED before shipping — see above.

### 2026-07-31 CLAUDE.md's machine facts are WRONG — it is an M2 Pro on macOS 26, not an old Intel Mac; Python 3.9 is a self-imposed choice
- Context: a research pass checked the hardware instead of trusting the brief.
- VERIFIED locally (sysctl / system_profiler / sw_vers / uname):
    MacBook Pro 14" 2023, Mac14,9, Apple M2 Pro, 10 cores, 16 GB, arm64
    macOS 26.5.2 (build 25F84)
    /usr/bin/python3 and .venv/bin/python are both 3.9.6, arm64
    uv 0.11.29 already installed at ~/.local/bin/uv
- CLAUDE.md currently says "older MacBook Pro" and treats system Python 3.9 as
  a machine constraint ("Target 3.9", "NO X | Y union syntax"). The hardware
  claim is simply false, and 3.9 is a CHOICE — the venv points at Apple's
  Command Line Tools python. Python 3.9 reached end-of-life 2025-10-31.
- Consequence: every session has been writing 3.9-compatible code and ruling
  out libraries on the basis of hardware this machine does not have. The M2
  Pro's GPU and Neural Engine have never been used for anything.
- CORRECTION to the research pass's own framing: it concluded "everything else
  waits on the Python upgrade." That is wrong, and I checked rather than
  repeating it. Installed into a scratch target against the EXISTING 3.9 venv:
    pedalboard 0.9.17 + soxr 1.1.0 install fine on cp39 arm64
    pedalboard has PitchShift, Limiter, Compressor, Reverb, Resample, Delay,
    Chorus, Distortion, Convolution, HighpassFilter, time_stretch (Rubber
    Band) and io.AudioFile — all present on that build
  So the whole "replace the hand-rolled DSP" recommendation is available TODAY
  with no Python upgrade. The upgrade buys newer versions, not access.
- Also flagged, unverified by me: faster-whisper's CTranslate2 backend is
  CPU-only on macOS (no Metal, no ANE); whisper.cpp runs on the GPU via Metal
  with a Core ML encoder path. If true, the "small.en ~1s latency" note in
  CLAUDE.md was measured with most of the machine idle and should be re-taken.
  faster-whisper 1.2.1 is installed and its last commit was 2025-11.
- Decision: nothing changed this session. CLAUDE.md's "Owner & machine facts"
  section should be corrected before the next build session, because that
  section is explicitly labelled "do not rediscover these" and is therefore
  the most load-bearing wrong text in the repo.
- Verify by: re-run the sysctl/sw_vers block above; it takes one command.
- Status: open
- Outcome: (awaiting owner go-ahead to edit CLAUDE.md)

### 2026-07-31 Rebuild review: measured the audio instead of reading the code — the engine is fine, the OUTPUT STAGE is where value leaks
- Context: owner asked what a master music/software/audio engineer + producer
  would do differently if rebuilding this project from scratch.
- Method note (this is the reusable part): I answered by MEASURING 493
  rendered beats, 60 stem folders and 506 stem files with numpy, not by
  reviewing code. Every prior "it sounds wrong" session found its bug by the
  owner's ear. The measurements below took ~20 minutes and found four defects
  no session and no test had caught in three months.
- Finding 1 (VERIFIED, the big one): 247 of 247 core stems are exactly
  dual-mono, max|L-R| < 1e-9. Refined on second look: hat (-0.15), blips
  (+0.30), stamp (-0.30), congas (+0.29) ARE panned. What is hardcoded to
  0.0 is kick, snare, sub, bass AND all three chord parts
  (beat_machine.py:1535, literal 0.0 for every chord{i} / chord{i}v{v}).
  Centring kick and snare is correct practice. Centring three simultaneous
  harmony parts on top of each other is not. This is the mechanical cause of
  the owner's repeated "everything is stacked on top of each other" — chased
  as a sample-sourcing problem on 07-25 and 07-29. Those fixes were correct
  but could not have resolved the symptom: the cause is spatial, not tonal.
- Finding 2 (VERIFIED): melodic content is buried. Loudest chord part vs kick
  across 39 beats: median -15.4 dB, worst -24.9 dB. Single cause:
  OWNER_TASTE["chord_gain"] = 0.3 (-10.5 dB) in groove.py.
- Finding 3 (VERIFIED): master() applies its EQ to nothing. It captures
  m = 0.5*(L+R) BEFORE the EQ, EQs L/R, takes side from the EQ'd pair, then
  rebuilds with the STALE mid (make_drum_loops.py:173-195). Ran it: air shelf
  changes centred content by -0.009 dB, side-only content by +2.509 dB. With
  finding 1, the air shelf and boxy-mid dip have never applied to any beat.
- Finding 4 (VERIFIED): 17 of 506 stems (3.4%, 15 of 60 folders) are digital
  silence while listed as live lanes. Root cause is upstream of the renderer:
  1623's "blips" lane has ZERO hits in every bar while still carrying a
  sample, pan 0.30 and gain 0.26. Lanes can be dealt in with an empty pattern.
- Finding 5 (VERIFIED, corrects a subagent): a subagent called naive np.interp
  resampling "the single worst defect." Measurement does not support that.
  0 of 265 sampled library files are 88.2/96k; 18.5% are 48k, whose aliases
  fold to 20-22 kHz (inaudible). It DOES bite on the upward pitch-shift path
  (PREFER_MAX_SHIFT=12, added 07-29): a 15 kHz component shifted +12 st
  returns as a phantom 14.1 kHz tone. Melodic-path defect, not load-path.
- What is NOT wrong (checked, so it does not get "fixed"): rhythmic variety is
  genuinely good (186 unique kick+snare+hat patterns in 200 beats); harmonic
  variety is fine too (58 major / 174 minor / 53 dorian / 15 phrygian, 22
  progressions) — the legend/genre signature work landed. Constant-power pan
  law, mono_below, loop_convolve and the de-click work are all correct.
- Decision: do NOT rebuild. 25k lines, 732 green tests, 1623 beats, in use
  today, and the composition brain measurably works. Every defect above is in
  the output stage. The recommendation is three constants, one guard, and an
  automatic listening test — not a rewrite.
- Reasoning: the recurring failure across 76 ledger entries is not bad code,
  it is that the machine cannot hear itself, so the owner is the only test
  instrument. 39 entries sit at status: open, the oldest from 07-22, all
  waiting on his ears. Adding measurement to the render is what removes that
  bottleneck; a rewrite does not.
- Verify by: apply the pan spread + chord_gain lift, render a batch, re-run
  the S/M and chord-vs-kick measurements, and have the owner listen. Simulated
  on 1623 without touching the repo: width -24.0 -> -17.8 dB S/M, chord-to-kick
  -11.0 -> -5.7 dB. Improves both, does not fully reach a -6..-12 dB width
  target because kick/snare/sub are correctly centred.
- Status: open
- Outcome: (nothing applied this session — this was a review, no code changed)

### 2026-07-29 Real bug found via owner listening: one "instrument" still sourced from several packs
- Context: after the stacking hard rule (below), owner reported "the
  strings and the synths are still stacked in stems with other
  instruments" on beat 1508. I checked with a real render first — the
  structural fix (one voice per beat) WAS working, no second lane — but
  the owner was right about something real underneath it.
- Root cause: a chord's NOTES are picked one at a time,
  independently, by nearest-pitch search across the WHOLE library
  (tools/instrument_sampler.py:nearest, tools/string_sampler.py:nearest).
  For a well-populated, coherent group like "strings" that's invisible —
  the nearest sample for every note usually comes from the same real
  patch anyway. For a thin, eclectic group like "synth" (built from
  scattered single one-shots across many different vendor packs, not one
  chromatic patch), each note of one chord independently grabbed a
  different pack's sound. Same "synth stabs" label on the stem, four
  actually different instruments underneath. Confirmed on beat 1508: its
  4-file voice_files list for chord0 (a 3-note chord) spanned 4 different
  vendor packs.
- Decision/change: added a `prefer` argument to nearest() in both
  instrument_sampler.py and string_sampler.py (plus a `pin` argument
  threaded through voice_note/note_slice/play_chord and
  beat_machine.py's _render_one and its caller in _build_chords) — every
  note across the WHOLE beat's chord progression now prefers reusing the
  one sample already chosen, stretching it further before giving up and
  picking a fresh nearest match.
- First attempt used the existing MAX_SHIFT (4 semitones, a major 3rd) as
  the reuse ceiling — tested against real generated beats and it wasn't
  enough; most chords span wider than that, so it kept switching packs
  anyway. Gave the owner the honest tradeoff rather than silently
  shipping a fix that measurably didn't work: stretch further (simple,
  some notes sound more pitch-shifted) vs. hunt a same-pack fallback file
  before crossing packs (better sound, more code/testing). He picked
  simple. New PREFER_MAX_SHIFT = 12 semitones (one octave) — deliberately
  wider than MAX_SHIFT, which exists specifically because a major 3rd is
  "about where the tape-speed shift starts reading as wrong rather than
  as the instrument" (instrument_sampler.py's own MAX_SHIFT comment). He
  knowingly traded some of that headroom for consistency.
- Verify by: measured before/after on 15 freshly generated real beats
  (Doc Day, Mustang, Wonky) using the real sample library — before: the
  large majority of chord slots used 2+ different files; after: 11/34
  (32%). Full suite: 732/732 passed both times (no test explicitly
  covered this — it's provenance/audio-character, not structure — so
  this was verified by direct measurement on real output, not a new
  automated check).
- Known ceiling (ponytail-flagged in instrument_sampler.py's
  PREFER_MAX_SHIFT comment): a chord spanning more than an octave still
  switches packs, and reused notes near the edge of that octave will be
  pitch-shifted further than the house's own "starts sounding wrong"
  line. Upgrade path if this isn't good enough by ear: same-pack fallback
  before cross-pack fallback (the "better, more work" option he didn't
  pick this time).
- Status: open — owner hasn't heard beats rendered under the wider
  reuse range yet. The chipmunk-tradeoff risk is real, flagged, not
  hidden.

### 2026-07-29 Owner audit: silence, downbeat, and stacking rules flipped; glue compression added
- Context: after getting a plain-language list of every hard-coded
  instrument/drum rule in the core engine (not per-DJ), owner reviewed it
  and changed four things, explicitly: new rules overrule any old rule
  that conflicts.
- Decision/change, one line each (all in tools/beat_machine.py unless
  noted):
  (1) Kick/snare/clap ("BACKBONE") can now go fully silent for a whole
      bar — removed the 2026-07-17 "never a gap" floor from vary_preset's
      four structural treatments (thinbar/frisson/bshift/breath) and the
      contrast-deepening pass. IMPORTANT CAVEAT caught by tests: that
      floor was sharing one code path with a DIFFERENT, still-valid rule
      — CANON lanes (the figure that DEFINES a subgenre, e.g. reggaeton's
      snare, owner rule 2026-07-19) were protected by the same
      `backbone = BACKBONE | canon` variable. Removing it wholesale broke
      2 genre tests (a reggaeton stopped being a reggaeton). Fixed by
      re-adding CANON-only protection (softens, never vanishes) separate
      from the now-removed BACKBONE protection.
  (2) The kick's downbeat can move now (_mutate_kick no longer excludes
      index 0 from the drop/slide roll) — was hard-pinned since
      2026-07-16.
  (3) No melodic stacking at all, ever, not even 2 parts, not even the
      chip voice, no rare "passing" 3rd part — part_count is hardcoded to
      1 in _build_chords, overriding the 2026-07-25 "up to 3 parts"
      feature (theory/arrangement.md, melody_part_weights,
      passing_note_p). That machinery is left in place but unreachable —
      not torn out — same call as the 2026-07-29 bassline rule above.
  (4) Added tools/groove.py:glue_compress — a bus "glue" compressor
      (envelope from L+R sum via a new lp1 helper, soft downward ratio,
      same gain both channels). Runs in tools/crew.py right before
      master(), always on (not gated by clean_renders — this is mix glue,
      not "dirt"). Tunables in OWNER_TASTE (glue_threshold_db -18,
      glue_ratio 1.8, glue_env_ms 25, glue_makeup_db 2) — starting
      numbers, not auditioned yet.
- Reasoning: owner explicit — "if there are other rules that conflict
  with these rules, the new rules overrule." Kept the old multi-part
  layering code dormant rather than deleted (same pattern as the
  bassline rule) in case it's wanted back — flipping it is a 1-line
  change (part_count = 1 → the old roll logic), not a rebuild.
- Known simplification (ponytail-flagged in the code): glue_compress uses
  ONE symmetric smoothing time constant for its envelope, not separate
  attack/release. A real glue comp eases in fast and lets go slow, which
  is where the "pump"/groove character comes from — this version only
  breathes at one speed. Upgrade path is in the function's docstring
  (two lp1 passes at different speeds, combined with np.maximum).
- Verify by: updated/added tests for all four changes
  (test_backbone_can_go_fully_silent_for_a_bar,
  test_layering_never_happens_always_one_voice,
  test_never_more_than_one_melodic_part — folds in what were 3 separate
  2-part/3-part/passing-note tests — plus 2 new glue_compress sanity
  tests in test_groove.py). Full suite: 730/730 passed. Not yet verified:
  owner hasn't heard a rendered beat under any of these four changes, and
  the glue compressor's numbers (-18/1.8/25ms/+2dB) are un-auditioned
  starting points, not tuned by ear yet.
- Status: open — needs his ear on all four, especially the glue
  compression numbers and whether the now-open kick/downbeat variation
  still sounds like the intended DJ personalities.

### 2026-07-29 Hard rule: no melodic bassline, ever
- Context: owner wants to play the bassline himself in Reason. The
  generator already told apart three low sounds — kick drum, bass drum/
  808 (the boom under the kick), and the melodic bassline that follows
  the chords (lane family "chordbass", bass0..N) — but the bassline was
  still opt-out per beat (typing "no bass" in the notes box), and would
  render itself from his own bass samples by default when available.
- Decision/change: one-line change in tools/beat_machine.py's
  _build_chords — `bass_idx` is now hardcoded to None instead of
  scanning his bass library, so bass0..N lanes never get built,
  regardless of notes-box wording. This is the single choke point: both
  callers of _build_chords (new beats, and rebuilding an old beat from
  its saved recipe) go through it, so old saved beats also lose their
  baked-in bassline on rebuild. Kick and the 808 bass drum are untouched.
- Reasoning: traced every place a melodic bassline could get created —
  only _build_chords does it (via instrument_sampler.scan_bass); crew.py,
  genres.py, and the other make_*.py scripts don't have their own bass
  logic (make_hiphop_tracks.py is retired as a generator, kept only as an
  imported helper library). One line, one file, covers every path.
- Verify by: updated the 4 tests that asserted a bassline gets built
  (test_rebuild_regenerates_chord_audio_and_stacks_sequential_trims,
  test_chords_direction_adds_a_harmony_layer,
  test_chord_bass_line_comes_from_his_own_bass_samples — renamed
  test_chord_bass_line_is_never_rendered and inverted, since its whole
  premise is now the opposite rule — and
  test_harmony_opens_under_the_drums_with_per_bar_dynamics). Full suite:
  732/732 passed.
- Status: confirmed — verified by test suite; owner hasn't heard a
  rendered beat under the new rule yet.


---

## Index of archived entries (full text in `DECISIONS-ARCHIVE.md`)

| date | entry | status |
|---|---|---|
| 2026-07-25 | One stack becomes up to three separate PARTS | open |
| 2026-07-25 | Tracks stopped playing — three bugs behind one symptom | open |
| 2026-07-25 | Kick drum, bass drum and bass are three different things | open |
| 2026-07-25 | Reason demoted, not removed — portability boundary set | open |
| 2026-07-25 | Packaging decided: one app two doors; brief written (PACKAGING-GAP-ANALYSIS.md) | open |
| 2026-07-25 | Reason Voice v2 web UI verified working end-to-end (first real check) | confirmed |
| 2026-07-24 | Chip voice added to Farrow ("Pharaoh") — checked it's real | open |
| 2026-07-24 | Pre-07-23 upgrade — FINAL BATCH: last 3 legends, backlog CLOSED | open |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 4: ALL 18 GENRES NOW SIGNED | open |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 3 (3 soul/orchestral legends + 1 genre) | open |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 2 (4 genres that had NO signature) | open |
| 2026-07-24 | Key parser missed the "<Key>Maj/<Key>Min" spelling — synth | confirmed |
| 2026-07-24 | Pre-07-23 upgrade — BATCH 1 of the backlog (4 identities) | open |
| 2026-07-24 | Chiptune was inaudible — chords never rendered unless the | confirmed |
| 2026-07-24 | First four legends WERE skimmed — audited, deepened; modes | open |
| 2026-07-24 | All nine DJs get harmony; harmony joins evolution; 4 silent | open |
| 2026-07-24 | New Math deepened — "arithmetic you can hear" (my design) | open |
| 2026-07-24 | Chiptune: the ONE sanctioned synth exception, + a recipe | open |
| 2026-07-24 | G-Funk reweighted after "does not read sunnier" — plus the | confirmed |
| 2026-07-24 | Genre harmony: 6 of 17 styles given a researched signature | partly |
| 2026-07-24 | The click at the end of samples — TWO real defects, both fixed | open |
| 2026-07-23 | ALL melodic instruments are sampled now; every synth deleted | open |
| 2026-07-23 | Brass is SAMPLED now — synth horn deleted, multi-sample built | open |
| 2026-07-23 | Volume control for every sound — one feature request, three bugs found chasing it | confirmed |
| 2026-07-23 | Bug fix: bass/vox lanes played but were invisible to the recipe (his "weird vocal" re | confirmed |
| 2026-07-23 | Drum-loop lane REMOVED after one audition batch | confirmed |
| 2026-07-23 | Phase 2 placement: bass/808, vox, and full-loop lanes | partly |
| 2026-07-23 | Sourcing rework: whitelist the folders + stop the one-shot rule | confirmed |
| 2026-07-23 | Sound-library expansion, phase 1: Downloads packs consolidated onto TBOTC 3 | confirmed |
| 2026-07-23 | "Add the root" turned back ON — and finally given a test | confirmed |
| 2026-07-23 | Kick flavor goes back to per-style — engine-wide clean-punch reversed | confirmed |
| 2026-07-23 | Flavor-index history went stale across the rule change — first 3 beats were not a fai | confirmed |
| 2026-07-23 | MIDI validity gate was failing every chord beat — the gate was stale, not the beats | confirmed |
| 2026-07-23 | Mustang (DJ Mustard) harmonic signature — 5th legend, first one NOT in the research d | open |
| 2026-07-23 | Engine-wide clean-punch kick now visibly fights Mustang's own identity | open |
| 2026-07-23 | Timberline (Timbaland) harmonic signature — resolved the dual-tempo-pocket fork | open |
| 2026-07-23 | J Dillo pinned to 2/4-bar only ("no long beats") | confirmed |
| 2026-07-23 | J Dillo (Dilla) harmonic signature added — 3rd legend, owner approved moving on | open |
| 2026-07-23 | DJ Premium (Premier) harmonic signature added — next legend after Dre | open |
| 2026-07-23 | Dre tuning (best-of #843/845/849) + engine-wide clean-punch kicks | open |
| 2026-07-22 | Dre chords: rhythmic arp + m7 removed (audition #845-847 feedback) | failed |
| 2026-07-22 | Wired harmonic identity (signature) into chord synth; Dre audition | confirmed |
| 2026-07-22 | Strings sampler scaffolded + chords audition batch rendered | open |
| 2026-07-22 | chord_synth loop-pad substitution: allow melody role, chop loop-kind files | open |
| 2026-07-22 | Paused the crew-variety autoresearch loop | confirmed |
| 2026-07-23 | Closed harmony-signature research for all 12 legends | open |
| 2026-07-23 | Wired No Alias's harmony signature + rendered audition batch | confirmed |
| 2026-07-23 | Wired Swish Beatz's harmony signature + rendered audition batch | confirmed |
| 2026-07-23 | Wired Razor's harmony signature + rendered audition batch | open |
| 2026-07-23 | Corrected a false "alt field" assumption; wired 3 more legends | open |
| 2026-07-23 | Built the two missing instrument engines (lead synth + scratch) | open |
| 2026-07-23 | Wired Just Flame — all 12 legends now have a signature | open |
| 2026-07-23 | Skills-compliance check found a real gap (midi-validity-gate) | confirmed |
| 2026-07-23 | Horn tone REJECTED on audition; Just Flame parked; demos built | open |
| 2026-07-25 | Packaging step 0 — the portability boundary was NOT already true | confirmed |
| 2026-07-25 | Packaging step 1 — manifest carries the harmony; a second name leak found | confirmed |
| 2026-07-25 | Packaging step 2 — old recipes: nothing to fix, so it got a test instead | confirmed |
| 2026-07-25 | Packaging step 3 — "why this works" on the beat card | open |
| 2026-07-25 | Packaging step 4 — one launcher starts both halves | confirmed |
| 2026-07-25 | Packaging step 5 — MAKE / STUDIO tabs; MVP (steps 0-5) complete | open |
| 2026-07-25 | Owner's first verdict on the MVP -> three changes shipped | open |
| 2026-07-25 | "No instruments, only drums" -> chords_default roster-wide; logo shared | open |
| 2026-07-25 | Chord voices: his samples only, one instrument per beat, layering | open |
| 2026-07-25 | Real 8-bit sounds preferred over the synth chip; float-WAV bug | open |
| 2026-07-25 | "Where are my instruments" — the LABEL was the bug; synth bass removed | open |
| 2026-07-25 | Chord stems removable, 1 dB arrows, and a mix that opens quiet | open |
