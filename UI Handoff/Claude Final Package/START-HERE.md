# Homeroom Studios — approved visual handoff

Implement the three approved views using the supplied existing wiring. This package contains design mockups and source references, not an implemented or tested redesign. The owner approved this visual direction; do not reopen design exploration.

## Design references

1. `mockups/01-beat-generator.png`: approved Chemistry beat generator.
2. `mockups/02-song-sketch.png`: latest Sketch revision, with contrasting waveform/background colors.
3. `mockups/03-physics-effects.png`: latest Physics Effects revision, with balanced colors.
4. `mockups/01b-loops-only-state.png`: alternate state of the MAIN page, not a fourth page.

Generator, Sketch workspace and Physics Effects are distinct views. Effects navigates in the SAME browser tab, never a popup. Sketch uses the existing openSketch flow. Physics should feel like another class in the same unit as Chemistry.

## Visual requirements

- Matte black/near-black panels and subtle black chalkboard texture. No beige or green-gray panel backgrounds.
- Refined ivory collegiate serif HOMEROOM wordmark, smaller tracked STUDIOS beneath, restrained HS shield. No distressed collage, random slogans or decorative clutter.
- Four accent hues: orange #FF5A12, electric green #7CFF32, violet #A66CFF, blue #4E8DFF. No teal or yellow. Match perceived colors in references; check actual contrast in implementation.
- Distribute accents deliberately across groups. Sketch waveform blocks use DIFFERENT palette colors for backgrounds and waveform marks: orange/blue, violet/green, blue/orange, green/violet. Keep each lane's mapping consistent across sections. Avoid same-hue light/dark waveforms.
- Loops Only visibly changes accent roles using the SAME palette: green leads instead of orange; violet/blue utility accents shift. Include explicit toggle state and mode label so color is not the only indicator. Preserve musical data when switching the UI state; use existing generation semantics.

## Main page behavior

- Two character tabs exactly: The Back of the Class / The Legends. Portrait circles are placeholders for the owner's eventual character images.
- Number of beats is a numeric control with up/down arrows, range 1–10.
- Tempo uses the flask visualization with a numeric BPM value and +/- controls. Its liquid/scale must agree with the actual BPM; generated image scales are illustrative and sometimes inaccurate.
- Keep beat rows compact; small cover art approximately half the original large mockup size. Playback, current beat and queue stay close.
- Pass and Fail icons replace heart/trash for beat triage. Retain existing favorite/trash-folder semantics; Fail must not permanently delete audio. Label controls/accessibility names clearly.
- Selecting a beat updates the nearby element table and its metadata. Compact periodic-style instrument tiles accommodate varying counts with scrolling. Show actual role/source and actual tempo, key, meter, bars and duration where available; mockup counts and labels are examples.
- Reference upload is a small utility action, not a large prominent panel. Preserve Pattern Library, Breaks, Saved Beats, Famous Beats, Style and Directions.
- Open Physics navigates to the separate Effects page. No embedded effects rack on the main page.

## Wiring and implementation boundaries

Read `wiring/README-FOR-CHATGPT.md` for generator IDs, placeholders and endpoints; `wiring/sketch.js` and `sketch.css` for the current Sketch workflow; and `wiring/Effects page/README-FOR-CHATGPT.md` for Effects controls and endpoints. Source files are reference snapshots. Preserve backend contracts, all existing features, IDs and control types. Use plain HTML/CSS/vanilla JS, not a framework migration. Put colors in CSS variables.

The actual source contract takes precedence over incidental invented controls in generated images. In particular, Sketch currently has one combined Echo/reverb amount and cell move checkboxes; the mockup's separate sliders and copy/clear widgets are NOT authorization for new backend features. Preserve the existing behavior and adapt the presentation. Arrangement preset names, scenes and roles come from real data. Likewise do not invent Effects parameters based on mockup knobs. Preserve all actual settings, value readouts, load/browse, transport, buses, master, Send back, Sketch and Export actions.

Do not treat rendered graph curves, durations, knob values, filenames or sound counts as reliable data. Bind to real state; retain generation/render errors and per-channel processing feedback. Fix inconsistent mockup numbers rather than reproducing them.

This handoff authorizes no deployment, deletion or repository migration. Confirm the intended implementation checkout with the owner before code changes: prior project boundary is Beat Lab Codex for implementation, Homeroom Studio for reference. This package was requested in Homeroom's UI Handoff folder as a design delivery.

## Review checklist

- All original generator, library, reference, triage and Sketch actions still work.
- Count limits, tempo controls and character tabs behave correctly.
- Selected-beat information follows selection and supports additional instruments.
- Normal and Loops Only themes use the same four colors with clear state labels.
- Sketch arrangement controls, roles, section changes, render, A/B playback and download remain functional.
- Effects routing, parameter readouts, dry/wet, optional base cleanup, export and same-tab return work.
- Check readability, keyboard focus, click targets and overflow with many sounds. Keep live UI verification separate from audio/listening approval.
