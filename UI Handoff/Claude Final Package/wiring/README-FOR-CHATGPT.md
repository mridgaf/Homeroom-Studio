# Homeroom Studio (Beat Machine) — UI wiring packet

You are designing a new front face for an existing, working app. The back end
stays exactly as it is. Your job is the look and layout only. Claude will wire
your design into the real app afterwards — follow these rules so that's easy.

## How the app works (one paragraph)
A small Python server (`tools/beat_machine.py`) runs on the owner's Mac at
`http://127.0.0.1:8770/`. It serves ONE web page and a set of URLs the page
calls with `fetch()`. All audio is made on the server; the page only sends
choices and plays the WAV files it gets back. No framework, no build step:
plain HTML + CSS + vanilla JS in one file.

## Files in this folder
- `current-page-template.html` — today's whole page (HTML, CSS and JS). Words
  like `__CREW__` are filled in by the server before sending (see below).
  Read its `<script>` to see exactly how each button calls the server.
- `sketch.js` / `sketch.css` — the Song Sketch board, loaded by the page.

## Rules that make porting easy
1. **Deliver one self-contained HTML file** (inline CSS + JS is fine) plus any
   images. No React/Vue/npm/build tools. Fonts from Google Fonts only.
2. **Keep every element `id` listed below**, on an element of the same kind
   (input stays input, select stays select). Restyle and move them freely.
3. **Keep the `__PLACEHOLDER__` words** exactly where the content should go.
4. **Use mock data, not invented endpoints.** If you need something new from
   the server, write it in a list called "NEW BACK-END ASKS" at the end — don't
   invent a URL silently.
5. **Every action must work by click.** Voice and keyboard are optional extras.
6. Put CSS colors in variables on `:root` so the theme can be swapped.
7. Don't remove a feature to simplify the design. If you think one should go,
   list it under "SUGGESTED CUTS" and keep it in the file anyway.

## Placeholders the server fills
| Placeholder | Becomes |
|---|---|
| `__CREW__` `__LEGENDS__` `__GENRES__` | rows of clickable DJ / Legend / genre cards |
| `__CREWCOUNT__` | the word "nine" etc. |
| `__KEYOPTS__` | `<optgroup>/<option>` list for the key dropdown, value like `"A minor"` |
| `__TEMPOLO__` `__TEMPOHI__` | tempo min / max numbers |
| `__LIBGENRES__` `__LIBBREAKS__` `__BREAKS__` | `<option>` lists for the pattern library |
| `__LIBRARYJSON__` | JSON `{genre: [pattern names]}` |

## Element ids the script uses (keep them)
Make panel: `go` (Make button), `tempo`, `key`, `count`, `notes`, `loopsonly`
(checkbox), `quick`, `famous`, `hosthint`, `refdrop` + `reffile` + `refline`
(drop-a-song-to-match box).
Library: `libgenre`, `libpattern`, `libgo`, `libbreak`, `libbreakgo`.
Pull an old beat: `pullno`, `pullgo`, `pullmsg`.
Player / list: `tracklist`, `viewsrc`, `empty`, `emptytext`.
Status: `work` + `worktext` (busy banner), `toast` (undo pop-up).
Per-beat cards, stem rows, knobs and dropdowns are built by the script — see
the `laneRow` and `loadBatch` functions in the template for their class names.

## The server's URLs (the whole contract)
All JSON replies have `ok: true|false`; on false there is `error` (plain words
to show the owner).

**Read (GET)**
| URL | Returns |
|---|---|
| `/batch` | `{beats:[{no, label, loc, se_id, theory}]}` — the current batch |
| `/folder?loc=favorites\|trash\|dj` | same shape, beats in that folder |
| `/peaks?no=N&n=150` | `{seconds, peaks:[0..1,…]}` waveform for drawing |
| `/stems?no=N` | `{stems:[{lane, label, role, sample, pack, locked, can_swap, why, stem, pan, loop}]}` one row per sound |
| `/candidates?no=N&lane=snare` | `{candidates:[{path, name, pack, current,…}], bpm}` choices for a row's dropdown |
| `/audio?no=N` | the beat WAV |
| `/stem?no=N&lane=snare&db=0` | one sound on its own (WAV) |
| `/mix?no=N&trims=lane:dB,…&pans=lane:-1..1,…&drop=lane,…&picks={json}` | the beat as currently set, not saved (WAV) |
| `/sample?no=N&lane=L&path=P` | preview one choice from the dropdown (WAV) |
| `/pull?no=N` | adds an old beat to the list → `{no}` |
| `/sketch-info?no=N` | Song Sketch board data |
| `/brand?name=FILE` | logo image |

**Do (POST, JSON body)**
| URL | Body | Does |
|---|---|---|
| `/make` | `{names:[dj names], tempo, key, count:1-10, notes, loops_only}` | makes new beats |
| `/library` | `{genre, name}` | makes a beat from a library pattern → `{no}` |
| `/triage` | `{number, dest:"fav"\|"trash"\|"dj"}` | moves a beat (never deletes) → `{loc}` |
| `/rebuild` | `{number, picks:{lane:path}, trims:{lane:dB}, pans:{lane:-1..1}, drops:[lane], fx}` | new beat from the rack settings → `{no, se_id}` |
| `/chunk` | same as rebuild, no `fx` | saves a version into the beat's Chunks folder → `{count, file}` |
| `/effects-stage` | same as chunk | readies the mix for the Effects page → `{se_id}` |
| `/engine-up` | `{}` | starts the Effects engine |
| `/ban` | `{number, lane, choice}` | never use this sound again (may reply `asked:true` with a question) |
| `/sketch` | `{no, lanes, recipe, src}` | renders a Song Sketch |
| `/reference` | raw audio file bytes, header `X-Ext: .mp3` | measures a song → `{bpm, root, mode, alt_root, alt_mode}` |

Making a beat takes 10–60 seconds: the design needs a clear busy state.
Audio plays through the Web Audio API in the current page, and the Effects
page opens in the SAME tab (owner rule: one tab only, no pop-ups).

## What to hand back
1. The HTML file (with mock data so it previews on its own).
2. A list mapping each of your buttons/inputs to the id or URL above.
3. "NEW BACK-END ASKS" and "SUGGESTED CUTS", if any.
