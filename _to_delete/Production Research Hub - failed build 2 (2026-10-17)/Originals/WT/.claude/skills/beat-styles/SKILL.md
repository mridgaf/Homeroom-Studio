---
name: beat-styles
description: Make beats in one of the seventeen subgenre styles — Memphis, Crunk, Organized Noize, Houston Screw, Emo Hip Hop, Acid Rap Detroit, Acid Rap Bright, Horror Rap, Wonky, Trip Hop, Baltimore Club, Miami Bass, New Orleans Bounce, G-Funk, Reggaeton Alt, Detroit, Plug. Use whenever the user names a subgenre or scene rather than a person ("make me a Baltimore club beat", "something reggaeton", "a screwed Houston beat", "give me bounce", "horrorcore", "plugg", "trip hop", "Miami bass", "emo rap", "crunk", "G-funk", "wonky", "acid rap"), asks for a beat that follows a genre strictly or authentically, asks what styles/subgenres are available, or asks about the dembow, the Baltimore 8-count, the Triggerman, or any style's canon figure. For the named DJ characters (Otto Grit, Night Metro…) and the Legends (J Dillo, DJ Premium…) use beat-crew instead.
---

# The Styles — the subgenre roster

Seventeen subgenres in their own box on the Beat Machine page, built
2026-07-19. Same engine as the crew and the Legends (`CREW` holds all
three rosters), but where the nine are loose characters and the Legends
chase one producer's likeness, these chase a SCENE.

Roster lives in `tools/genres.py` + `genres_config.json` (editable, same
contract as `crew_config.json`; delete it to regenerate). Read
[beat-crew](../beat-crew/SKILL.md) first — everything about rendering,
the library path, stems/MIDI, triage, swaps and the notes box is shared
and is NOT repeated here.

| # | Style | Built on | BPM | Density |
|---|-------|----------|-----|---------|
| 22 | Memphis | Three 6 Mafia / DJ Paul | 140 | home |
| 23 | Crunk | Lil Jon, the hard festival end | 140 | sparse |
| 24 | Organized Noize | Dungeon Family / Outkast | 95 | home |
| 25 | Houston Screw | DJ Screw | 66 | sparse |
| 26 | Emo Hip Hop | Lil Peep / XXXTentacion | 150 | home |
| 27 | Acid Rap Detroit | Esham, the 1989 lineage | 92 | sparse |
| 28 | Acid Rap Bright | the 2013 jazzy lineage | 88 | home |
| 29 | Horror Rap | Gravediggaz / Brotha Lynch | 90 | sparse |
| 30 | Wonky | Flying Lotus / Hudson Mohawke | 86 | sparse |
| 31 | Trip Hop | Massive Attack / Portishead | 88 | sparse |
| 32 | Baltimore Club | Rod Lee / KW Griff | 130 | busy |
| 33 | Miami Bass | 2 Live Crew / the 808 electro line | 138 | busy |
| 34 | New Orleans Bounce | the Triggerman lineage | 100 | busy |
| 35 | G-Funk | DJ Quik / Warren G / Above the Law | 94 | home |
| 36 | Reggaeton Alt | the Tainy / experimental dembow | 92 | home |
| 37 | Detroit | Black Milk / Apollo Brown / Danny Brown | 93 | home |
| 38 | Plug | plugg / pluggnb — MexikoDro, Kankan | 140 | sparse |

## The owner decisions behind the roster (2026-07-19)

- **Three picks overlapped rosters he already had**, so they are aimed
  deliberately AWAY from the character that covers them: **Detroit** at
  the post-Dilla street side, not the drunk swing Otto Grit and J Dillo
  own; **G-Funk** at the Quik/Warren G bounce, not Doc Day's surgical
  Dre pocket; **Wonky** at the LA beat scene, not Dilla-adjacent.
- **"Acid rap" is two unrelated things**, so it is two buttons: the 1989
  Esham Detroit lineage that fathered horrorcore, and the bright jazzy
  2013 lineage.
- **"Southern hip hop" split four ways** (Miami bass and NO bounce were
  asked for separately): Crunk — with the harder *Turn Down for What*
  edge, not just 2003 crunk — Memphis, Organized Noize, Houston Screw.
- **Genre fidelity beats the house sparse-bed rule in this box.** He
  plays over the top, so crew beats lean sparse; Baltimore club, bounce
  and Miami bass are dense by definition, so each style DECLARES its own
  density and the engine honours it.

## THE RULE THAT GOVERNS THIS ROSTER

> **"The genres do not have to follow any of the rules, so they stay
> true to the genre."** — owner, 2026-07-19

That is not a loophole, it is the design. The crew's variety machinery
exists to stop nine characters repeating themselves; applied to a
subgenre it measures **fidelity as if it were drift** and quietly
destroys the style. Every exemption below exists because it was caught
doing exactly that. **Do not "fix" these by re-applying a crew rule.**

- **canon lanes** — each style names the lanes carrying the figure that
  DEFINES it. `compose()` places them verbatim from that style's
  authentic variants; `vary_preset` gives them the gentle anchor wander
  it gives the kick, never the drop/add mutation.
- **the sameness guard is skipped entirely** (`pattern_gen.compose`). It
  compares a mode+flavor signature, so on a style whose modes are fixed
  by design it kept rerolling the flavor — it dragged Baltimore club's
  10/90 kick split to 42/58 and put a long 808 where a club kick goes.
- **the flavor streak-breaker is skipped.** The long decaying 808 IS
  Miami bass and IS a screw beat; breaking the streak pulled an 80/20
  lean to 57/43.
- **swing is pinned** per style (`genre_swing`), guests included — the
  crew's guest lanes coin-flip to straight 50, which reads as a mistake
  inside a 62%-swung Wonky beat.
- **the declared space survives.** The beat normally rolls its own
  gated/dry/room/plate; a style keeps what it declares, because trip hop
  lives in that plate and club is dry.
- **tempo leans half as far** (±2%, not ±5%) — 130 is club, 124 isn't.
- **no odd meter or exotic grids**; **no engine-driven evolution** (a
  genre is a tradition, not a career); **kick banks never cross-pollinate
  INTO a style** (the loose nine may still borrow a style's book).
- **the contrast floor never fires.** Baltimore club, Miami bass and
  bounce do not rise and fall — that flatness is the style.
- **the RMS sanity floor widens to −21 dB for sparse styles.** A screw
  beat is 2-4 kicks a bar over a 29-second loop at 66 BPM; its average
  sits near −19 while LUFS, peak and duration are all exactly right.

What they DO keep: the whole sound-variation set (fresh sample picks,
cross-session anti-repetition, per-beat kick sustain, one locked stamp,
open sound bank), the mix chain (−12 LUFS, −4 dBFS peaks, snare/perc bus
trims), and the rule that timekeepers stay subtle (|pan| ≤ 0.2) so his
voice owns the mids.

## The canon figures

The rhythms that ARE these styles, in `tools/genres.py`. Step 0 is the
downbeat; capitals are full velocity, lowercase 0.72, "." a ghost.

- **Reggaeton Alt** — `snare` the dembow `---X--X----X--X-` (hits 3, 6,
  11, 14) over `kick` on 1 and 3. Two mirrored tresillo cells: kick, +3,
  +6, kick, +3, +6.
- **Baltimore Club** — `kick` the 8-count `X--x--x-X--x--x-` (0 +3 +6,
  8 +11 +14) with `clap` `----X--X--X-X---` pushing the "a" of 2 and the
  "&" of 3. **The Bmore kick is a doubled tresillo — the same cell
  reggaeton puts on its snare, twice as fast on the kick.** That kinship
  is real, not a coincidence, and it is why both live in this roster.
- **Miami Bass** — `kick` the electro figure out of the Planet Rock
  lineage, with the long 808 filling the gaps.
- **New Orleans Bounce** — `snare` the Triggerman answer
  `----X--X----X-xx`: backbeat plus the stutter at the top of 4 that the
  whole style calls and responds to.

Everything not in canon still rolls free, which is where the variety
comes from. Held by `tests/test_genres.py::test_no_two_beats_are_the_same_beat`
(28 beats per style, no duplicate whole-kit fingerprint).

## New grammar the roster added

In `pattern_gen.py`, gated so only these styles reach them:

- backbeat modes **dembow**, **club**, **bounce**, **stomp**
- timekeeper modes **triplets**, **trip_rolls** (24-step triplet grid in
  4/4 — six per beat), **shuffle**, **drive16**
- `crew.grid_accent` gained the res-24 metric accent for that grid

## Honest limitations

- **Baltimore club and NO bounce are break-based genres** (the Sing Sing
  / Think break; Triggerman) and `sample_library.py` rejects loops
  outright — one-shots only. These figures are reconstructed hit by hit.
  They read as the genre; they do not have the glued-break character of
  the real thing.
- **The lo-fi styles are not currently dirty.** Memphis, Horror Rap,
  Acid Rap Detroit, Trip Hop and Detroit all declare dust and vinyl, but
  `OWNER_TASTE["clean_renders"] = True` (his 2026-07-18 rule — "I want
  the beats clean", he adds color in Reason) strips every dirt stage at
  render time. The numbers are stored and correct, so this is a one-flag
  change per style if he ever wants baked grit — but baked dirt is
  irreversible, so it stays off until he says otherwise. **Ask before
  flipping it.**

## Collabs

Allowed with anyone and they use the LOOSE crew rules — collaborating IS
stepping out of character, same as the Legends. `collab_preset` builds a
fresh preset and never copies `_canon`, so a Baltimore Club × Otto Grit
beat is a genuine hybrid, not a club beat with a guest.

## Gotchas

- **Anything that rebuilds `CREW` must call `crew.reload_rosters()`**,
  not re-merge by hand. test_evolution's sandbox teardown restored only
  the nine and the Legends, which silently dropped this roster for every
  test module that ran afterwards. One call means a fourth roster can't
  reintroduce that bug.
- The Beat Machine server holds loaded code — after any engine change,
  kill the process on port 8770 so his next launch reloads.
- Tests: `./.venv/bin/python -m pytest tests/ -q` from the Homeroom Studio
  root must stay green (375 passing as of 2026-07-19).

## Honesty

You cannot hear the renders — verify numerically (duration, LUFS ≈ −12,
peak ≈ −4 dBFS, RMS sanity, canon figures intact) and say so plainly.
His ears are QA. Regeneration is cheap — offer variants instead of
arguing.
