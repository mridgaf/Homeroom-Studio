# DJ Rebuild tracker (Part 1 of 1)

Skill: `.claude/skills/dj-rebuild/SKILL.md`. ONE identity per session. Stages: not started -> line done -> settings done -> heard (only his ear closes one).

**Two sides (owner, 2026-10-23):** research and the listen line are shared. Settings are built twice, at separate times, in separate sessions: **Original** (MIDI + sound packs; gaps the research names get London Symphony strings) and **Loops** (the "loops only" box on Make). Each side has its own column and its own "heard".

**Original side rule (owner, 2026-10-24):** chord odds = MIDI 75 / chord loops 10 / sound packs 15 (research ratios inside the 15). MIDI notes play on the identity's researched instruments, never bell or pluck; London strings fill notes those can't reach. New research overrules old research and old rules: Code passes don't re-ask what the research settles. Pinned by tests/test_original_midi.py (add each new Original build to ORIGINAL_BUILT).

**DONE 2026-10-23:** the "Jazz out for everyone" Code pass (`Handoffs/Jazz out + Doc Day 2001/Part 1 of 2`) should be done first, so no rebuild has to fight the jazz coloring.

**Order** (Claude's suggestion; reorder freely): Doc Day, then G-Funk (it borders Doc Day), then the 5 producer pairs back to back so their eras are split on purpose, then the rest of the crew and Legends, then the 3 original "no one" DJs (need his input, not research), then the genres.

| # | Name | Group | Based on | Stage (research + line) | Original settings | Loops settings |
|---|---|---|---|---|---|---|
| 1 | Doc Day | Legend | Dr. Dre | settings done 2026-10-23 (not heard) | done 2026-10-23 (not heard); MIDI 75 / loop 10 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 2 | G-Funk | Genre | DJ Quik / Warren G / Above the Law (NOT Doc Day's surgical D | settings done 2026-10-23 (not heard) | done 2026-10-23 (not heard); MIDI 75 / loop 10 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 3 | Otto Grit | Crew | J Dilla | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 4 | J Dillo | Legend | J Dilla | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 5 | Cutz | Crew | DJ Premier | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 6 | DJ Premium | Legend | DJ Premier | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 7 | Chrome Dial | Crew | Timbaland | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 8 | Timberline | Legend | Timbaland | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 9 | Glass Cat | Crew | The Neptunes / Pharrell | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 10 | Farrow | Legend | Pharrell / N.E.R.D. (the live-band era) | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 11 | Sunday Chop | Crew | Kanye West | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 12 | Kane East | Legend | Kanye West / Yeezus (the industrial era) | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 13 | Crate Prophet | Crew | Pete Rock / Madlib | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 14 | Night Metro | Crew | Metro Boomin | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 15 | Rage Engine | Crew | Lex Luger | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 16 | Mustang | Legend | DJ Mustard | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 17 | Swish Beatz | Legend | Swizz Beatz | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 18 | Tenth Wonder | Legend | 9th Wonder (soul-chop era) | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 19 | DJ Hint | Legend | DJ Clue (the mixtape era) | settings done 2026-10-23 (not heard; no render; BPM single-source) | done 2026-10-23 (not heard); MIDI 75 / loop 10 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 20 | Just Flame | Legend | Just Blaze | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 21 | Razor | Legend | RZA | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 22 | Hitt Kid | Legend | Hit-Boy | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 23 | No Alias | Legend | No I.D. | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 24 | DJ Light Green | Legend | DJ Green Lantern (the 2013+ EDM/trap era) | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 25 | Well Damn | Legend | FnZ (Finatik N Zac) — the Denzel Curry Miami-bass era (ZUU/T | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 26 | New Math | Crew | Flying Lotus, Cosmogramma 2008-10 (owner pick 10-30) | settings done 2026-10-30 (not heard; no render) | done 2026-10-30 (not heard) | done 2026-10-30 (not heard) |
| 27 | Half Light | Crew | Earl Sweatshirt + the Alchemist 2018-23 (owner pick 10-30) | settings done 2026-10-30 (not heard; no render) | done 2026-10-30 (not heard) | done 2026-10-30 (not heard) |
| 28 | Fast Water | Crew | Atmospheric jungle: LTJ Bukem + Goldie 1994-96 (owner pick 10-30) | settings done 2026-10-30 (not heard; no render; break lane 13/100) | done 2026-10-30 (not heard) | done 2026-10-30 (not heard) |
| 29 | Memphis | Genre | Three 6 Mafia / DJ Paul | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 30 | Crunk | Genre | Lil Jon (through the hard, festival end — Turn Down for What | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 31 | Organized Noize | Genre | Organized Noize / Dungeon Family (Outkast, Goodie Mob) | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 32 | Houston Screw | Genre | DJ Screw / chopped and screwed | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 33 | Emo Hip Hop | Genre | Lil Peep / XXXTentacion | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 34 | Acid Rap Detroit | Genre | Esham — the 1989 Detroit acid rap that fathered horrorcore | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); 10-23 tracker said done, ledger showed it never was | done 2026-10-30 (not heard) |
| 35 | Acid Rap Bright | Genre | the 2013 Acid Rap lineage — bright, jazzy, gospel-leaning | settings done 2026-10-23 (not heard; no render; odds are Claude's picks) | done 2026-10-23 (not heard); MIDI 75 / loop 10 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 36 | Horror Rap | Genre | Gravediggaz / Brotha Lynch / the horrorcore lane | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
| 37 | Wonky | Genre | the LA beat scene — Flying Lotus, Hudson Mohawke, Rustie (NO | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 38 | Trip Hop | Genre | Massive Attack / Portishead / Tricky | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 39 | Baltimore Club | Genre | Baltimore club — Rod Lee, KW Griff, the Bmore 8-count | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard); 10-23 tracker said done, ledger showed it never was | done 2026-10-30 (not heard) |
| 40 | Miami Bass | Genre | Miami bass — 2 Live Crew, Magic Mike, the 808 electro lineag | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 41 | New Orleans Bounce | Genre | NO bounce — the Triggerman / Drag Rap lineage | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 42 | Reggaeton Alt | Genre | alternative reggaeton — the Tainy / experimental end of the  | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 43 | Detroit | Genre | post-Dilla Detroit — Black Milk, Apollo Brown, Danny Brown's | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 44 | Plug | Genre | plugg / pluggnb — MexikoDro, Kankan, the soft end of trap | settings done 2026-10-24 (not heard; no render; thin research) | done 2026-10-24 (not heard); MIDI 75 / loop 10 | done 2026-10-30 (not heard) |
| 45 | Chiptune | Genre | NES / Atari 2600 chip music — square leads, noise drums | settings done 2026-10-24 (not heard; no render) | done 2026-10-24 (not heard) | done 2026-10-30 (not heard) |
