# Homeroom Studio — Effects page ("Sound of Science") wiring packet

You are designing a new front face for an existing, working page. The back end
stays exactly as it is. Your job is the look and layout only. Claude will wire
your design into the real app afterwards — follow these rules so that's easy.

## How it works (one paragraph)
A small Python server (`sound_engine/server.py`, FastAPI) runs on the owner's
Mac at `http://localhost:8767/`. It serves `index.html` plus the CSS/JS files
in this folder under `/static/…`, and a set of `/api/…` URLs the page calls.
The page loads a beat's stems (one audio file per sound: kick, snare, chords…),
shows a rack of channels, and lets him add effects with knobs. The server does
the heavy effect math and sends back processed audio; the page plays and mixes
it live with the Web Audio API. Plain HTML + CSS + vanilla JS, no build step.

The Beat Machine opens this page in the SAME tab as
`/?beat=<beat_id>&back=<beat machine address>`. "Send back" and "Sketch" return
there. One tab only — no pop-ups or new windows.

## Files in this folder
- `index.html` — the page layout (all the element ids).
- `app.js` — loading beats, the channel rack, knobs, playback, export.
- `effects.js` — effect panels and the base-layer switch.
- `science.js` — the "flask" theme (effects shown as lab flasks, buses A/B).
- `stutter-worklet.js` — live stutter audio code. Don't change it.
- `style.css`, `effects.css`, `science.css`, `Blackboard-Graffiti.woff2` — today's look.

## Rules that make porting easy
1. **Deliver HTML + CSS** (inline or separate files). Keep the three JS files
   working: change JS only where your layout truly needs it, and say where.
   No React/Vue/npm/build tools. Fonts from Google Fonts or a local file.
2. **Keep every `id` in `index.html`**, on an element of the same kind (a range
   slider stays a range slider, a button stays a button). Restyle and move
   them freely. Each knob comes as a pair: `lowDb` (the control) +
   `lowDbVal` (its number readout) — keep both.
3. **Use mock data, not invented endpoints.** If you need something new from
   the server, list it under "NEW BACK-END ASKS" at the end.
4. **Every action works by click.** Keyboard is an optional extra.
5. Put CSS colors in variables on `:root` so the theme can be swapped.
6. Don't remove a feature to simplify the design. If you think one should go,
   list it under "SUGGESTED CUTS" and keep it in the file anyway.

## Groups of ids (what each area is)
- Top / transport: `playBtn`, `stopBtn`, `loopToggle`, `fileName`, `bpmLine`,
  `wave`, `playDot`, `playWord`, `playStatus`, `backBtn`, `sendBackBtn`,
  `sketchBtn`, `exportBtn`, `exportStatus`.
- Load a beat: `dropzone`, `fileInput`, `browseBeatsBtn`, and the picker pop-up
  `beatPickerModal`, `beatPickerList`, `beatPickerWarning`, `beatPickerClose`.
- Channel rack / table: `channelList`, `channelRackTitle`, `lanes`, `stemSlot`,
  `tableView`, `tableHint`, `stable`, `tableKey`, `scard`, `bigTile`, `conn`,
  `p-stems`, `cA`, `cB` (buses A and B).
- Flask (selected effect slot): `p-flask`, `flaskTitle`, `flaskWho`,
  `flaskLevel` + `flaskLevelVal`, `flaskSlot`, `knobTarget`, `knobs`.
- Master: `dryWet` + `dryWetVal`, `holdBtn`, `baseBtn` (base clean-up on/off),
  `cleanBtn`.
- Effect knobs (control id → server setting):

| Effect | Controls → setting |
|---|---|
| EQ | `lowDb` low_db, `lowHz` low_hz, `midDb` mid_db, `midHz` mid_hz, `midQ` mid_q, `highDb` high_db, `highHz` high_hz |
| Compressor | `compThreshold` comp_threshold_db, `compRatio` comp_ratio, `compAttack` comp_attack_ms, `compRelease` comp_release_ms, `compMakeup` comp_makeup_db |
| Saturation | `satDrive` sat_drive_db, `satMix` sat_mix |
| Crunch | `crunchAmount` crunch_amount, `crunchMix` crunch_mix |
| Punch | `punchAmount` punch_amount, `punchMix` punch_mix |
| Reverb | `revSize` reverb_size_s, `revDamping` reverb_damping, `revWidth` reverb_width, `revWet` reverb_mix, `revDry` reverb_dry, `revFreeze` reverb_freeze |
| Delay | `dlyGrid` + `dlyGridInfo` (note-length picker), `dlyMs`/`dlyMsKnob` dly_time_s, `dlyFeedback` dly_feedback, `dlyMix` dly_mix |
| Stutter (beat repeat) | `brGrid` + `brGridInfo`, `brMs`/`brMsKnob` br_cell_s, `brRepeats` br_repeats, `brChance` br_chance, `brMix` br_mix |
| Space (convolution) | `convDrop` (drop a sound file), `convName`, `convMix` conv_mix, `convClear` |
| Width | `widthKnob` width |
| Chorus | `choRate` cho_rate_hz, `choDepth` cho_depth, `choMix` cho_mix |
| Phaser | `phsRate` phs_rate_hz, `phsDepth` phs_depth, `phsMix` phs_mix |

Every knob also has a `…Val` readout (e.g. `compRatioVal`).

## The server's URLs (the whole contract)
Errors come back as `{error: "plain words"}` with a 4xx status.

| Method + URL | Send | Get back |
|---|---|---|
| GET `/api/library/beats` | — | `{beats:[{beat_id, dj, display_name, bpm, stem_count}], warning}` |
| POST `/api/project/from-beat` | `{beat_id}` | project (below) |
| POST `/api/project/from-upload` | form field `file` (an audio file) | project |
| GET `/api/project/{id}/channel/{lane}/dry` or `/wet` | — | that channel's WAV, before / after effects |
| POST `/api/project/{id}/channel/{lane}/process` | `{gain_db, pan:-1..1, muted, solo, bus:"A"\|"B"\|"", …effect settings}` | `{ok}` — then fetch `/wet` again |
| POST `/api/project/{id}/bus/{A\|B}/process` | `{gain_db, …effect settings}` | `{ok}` |
| GET `/api/project/{id}/bus/{A\|B}/wet` | — | the bus WAV |
| POST / DELETE `/api/project/{id}/channel/{lane}/ir` | form field `file` / nothing | `{ok, ir_name}` (load / clear the Space sound) |
| POST `/api/project/{id}/base` | `{on: true\|false}` | `{ok, base_on}` |
| POST `/api/project/{id}/export?dry_wet=0..1` | — | `{path}` saved file |
| POST `/api/project/{id}/to-sketch?dry_wet=…` | — | `{ok, no}` → go to Beat Machine Song Sketch |
| POST `/api/project/{id}/send-back?dry_wet=…&back=…` | — | `{ok, no, back}` → go back to the Beat Machine |

Project = `{project_id, name, bpm, base_on, channels:[{lane_id, label,
sample_rate, length_samples, duration_s, fx:{…effect settings}}]}`.

Processing a channel takes up to a second or two: show a small busy state on
that channel, not the whole page.

## What to hand back
1. The HTML/CSS (with mock data so it previews on its own).
2. A list mapping each of your controls to the id above.
3. Any JS changes, "NEW BACK-END ASKS" and "SUGGESTED CUTS".
