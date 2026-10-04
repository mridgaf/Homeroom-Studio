# Homeroom Studios — implementation handoff

Implement this approved visual direction in the existing beat-maker application. Read the application and its instructions first, then work within its framework and existing services. The included design-reference.png is the latest visual reference. This package contains a design and requirements, not application source code or a working music-generation service.

## Visual direction

Preserve the charcoal page background, yellow ruled spiral notebook on the left, and wood-framed black/charcoal chalkboard on the right. Keep the tactile school/hip-hop feel without adding decorative clutter.

All notebook text, including Homeroom Studios, uses black weathered typewriter lettering. All chalkboard lettering uses imperfect, lightly weathered handwritten lettering. The selected lettering direction was specimen 4B: broad, angular, slightly condensed hip-hop handlettering with clipped edges and subtle distress. The rendered reference is rounder than that specimen; do not claim it is an exact font. Choose a licensed font or available assets, and keep readability at small sizes. Do not add underlines beneath headings or decorative yellow emphasis rays.

Apply consistent chalk grain and rough edges to text, outlines, dividers, numbers, logo, buttons, play circles, stars, erasers and stepper arrows. Eye outlines should match the rough white outline of Test; avoid mixing smooth vector borders with rough chalk borders. Weathering is subtle, not heavy grunge. Keep text as accessible live text and controls as real elements rather than a flattened image.

Use lime green sampled from the first waveform for Create, Get Schooled, the profile icon, tempo number and beat-count number. Create is an unfilled charcoal button with a green outline and green text. Stepper triangles are yellow, matching play circles and pass stars. BPM, control labels and outlines remain white. Waveform colors in the reference illustrate the palette, not mandatory audio state semantics.

## Layout details and intent

Top navigation: Create (replaces Make), Get Schooled (replaces Studio), and profile icon. Use existing destinations where available. Get Schooled's destination/content has not been defined; do not invent a product feature for it.

The chalkboard header must have TWO EQUAL-WIDTH columns. This applies to its internal header, not to notebook versus chalkboard. Some generated previews show unequal widths; implement equal widths intentionally.

Left header column is a face composed of functional controls:
- Tempo input is the left eye, showing 95 BPM in the example.
- Number of beats input is the right eye, showing 3 in the example.
- Equal eye-box sizes and a shared baseline; retain increment/decrement controls.
- Loops only checkbox is the nose: center the checkbox itself between and below the eyes. Put its label below it so text does not push the checkbox sideways. The latest generated image still has a side label; follow this centering intent.
- Test is the mouth: a small unfilled white chalk-outline rectangle with white lettering, centered below the nose.

Right header column contains the original central white face graphic, centered and scaled with balanced margins and a comparable visual footprint. Preserve the recognizable eyes, brow, nose, and rectangular mouth. Its mouth must have an opening at the center of the RIGHT edge so it resembles a squared C. Do not restore the wording above/below the logo or a solid black rectangular backing. Apply the same chalk wear. Request/use original logo source if available; the mockup is only a visual reference, not a pristine source asset.

Below the header, show the beat cards directly. No Results/Your Beats heading and no large batch/Favorites/DJ-folder tab buttons. Avoid retaining a large empty gap merely because the image removed a heading.

## Notebook controls

Preserve these controls and connect to existing data/options where available:
1. Homeroom Studios header.
2. The Back of the Class: crew selector; Otto Grit is the illustrated selection. This replaces The Crew, not an additional selector.
3. The Legends: signature-style selector; Choose a signature style placeholder.
4. Styles: style selector; Boom bap in the example.
5. Quick directions: preset selector. Do not reintroduce the large free-text Directions box.
6. Famous beats: existing reference/preset selector.
7. Key: selector; A minor in the example.
8. Reference track: upload/drop zone. Reference image shows MP3, WAV, M4A, maximum 50 MB. Verify backend-supported formats/limits before implementing that promise; show actual validation and errors.
9. Pattern library accordion: small notebook-grid/beat-mark icon.
10. Breaks accordion: crossed drumsticks over a small snare icon, not a record.
11. Find a saved beat accordion: crate of records with one record partly pulled out.

Remove Rhythm test bank entirely. Loops only belongs on the chalkboard, not the notebook. Do not invent extra options or rename labels to Honor Roll/Extra Credit/etc.; those were suggestions, not selected requirements.

## Removed or replaced — do not restore

- Separate top-page Homeroom Studios wordmark and its yellow underline: brand heading now sits on the notebook in typewriter lettering.
- Notebook's former large THE BACK OF THE CLASS heading: replaced by Homeroom Studios; The Back of the Class now labels the crew selector.
- The Crew field label: replaced by The Back of the Class, retaining the selector.
- Blue notebook text/arrows/icons: replaced by black typewriter text and black worn icons.
- Large Directions multiline typing box and its label: removed. Quick directions remains.
- Rhythm test bank accordion and function: removed entirely.
- Notebook Loops only checkbox: moved into the chalkboard control face as its nose.
- Make My Beats wording and large filled yellow button: replaced by small unfilled white-outline Test button.
- Your Beats / Results heading and any heading underline: removed entirely.
- Large This batch, Favorites and DJ folder buttons/tabs: removed from the results area. Favorites storage/function remains through per-beat pass stars and saved-beat access.
- Separate trash button: unnecessary because the per-beat eraser performs fail / move to recoverable Trash. Trash storage/recovery is not removed.
- Decorative yellow whisker/emphasis rays around headings: removed.
- Words above and below the original face logo: hidden/removed. Central face graphic retained.
- Solid black rectangular logo backing: blended into the charcoal chalkboard, with no visible rectangle boundary.
- Small portion of the right vertical mouth stroke: removed to create the C-like opening.
- Original generic bottom icons: replaced with notebook/beat-grid, drumsticks/snare, and record-crate icons.
- Top Make navigation label and blue fill: replaced by green Create with unfilled green outline.
- Studio navigation wording: replaced by green Get Schooled.
- White tempo/count numbers and stepper triangles: numbers now green; triangles now yellow.
- Smooth chalkboard border/icon strokes: replaced by consistent subtly weathered chalk treatment, including eye boxes, card controls and logo.

## Functional behavior

Test submits the chosen configuration to the app's existing beat-generation workflow: crew, signature style, style, quick directions, famous-beat reference, key, reference audio, tempo, count and loops-only as supported by the current service. Preserve the service's actual semantics and validated limits. Disable duplicate submission while pending, show progress/loading, handle errors visibly, and present the generated beats. Never fake working generation or silently substitute sample results for real results. If backend/service is missing, separate a clearly labeled demo adapter from production and explain what credentials/service integration is needed without requesting secrets in chat.

Each beat card has:
- Stable beat identity/title; Beat 412/413/414 are examples, not hardcoded real results.
- Actual BPM, key, duration, waveform and playback progress.
- Play/pause control; coordinate audio so multiple cards do not unintentionally play simultaneously.
- Yellow star = PASS. Saves the beat to Favorites and persists that disposition. It may disappear from the review queue after pass, but queue behavior was not decided: follow existing application behavior, or ask if a new decision is necessary.
- White chalk eraser = FAIL. Sends the beat to Trash using recoverable deletion. Do not permanently delete audio. No separate trash-can button.
- Stems control: connect to existing stems workflow and show availability/pending/error states; do not fabricate stems.
- Overflow menu: retain only actions already needed in the application; do not duplicate a large favorite/trash button.

Ensure saved Favorites can be reached through Find a saved beat using existing saved-beat organization. Trash recovery access must remain available through an appropriate existing location; exact placement is not specified. A lightweight undo for fail is a reasonable implementation detail. Persist favorites/trash across reloads using the existing storage model. Preserve beat files and metadata.

## Implementation constraints and validation

Use semantic buttons, inputs, select controls and accessible names: Pass / Save to Favorites, Fail / Move to Trash, Play / Pause, etc. Do not rely only on colors or an unlabeled eraser to explain actions; supply accessible labels and hover/focus tooltips. Support keyboard use and visible focus. Retain the desktop two-panel composition, with a practical responsive layout for narrow screens rather than tiny illegible text.

Inspect existing code before choosing implementation details. Reuse current components, API contracts, routing and authentication. Do not replace functioning backend logic simply to match this design. Keep reference files intact and create editable project assets separately.

Verify generation submission/configuration, reference-file validation, playback, stems availability, persistent pass/fail actions, recoverable trash behavior, saved-beat access, responsive layout and keyboard interaction. Run appropriate existing checks, inspect the rendered UI against the reference, and report what works and what requires external integration. Verify equal header columns, centered checkbox nose, unfilled Test mouth, C opening in logo, matching weathering, green navigation/numbers, yellow arrows, and removal of Results and obsolete controls.

## Questions only if unresolved by the code

- Which existing routes should Create, Get Schooled and profile use?
- Where are original logo and font assets, and what usage licenses apply?
- Should passing a beat remove it from the current review queue?
- Where should users recover failed beats if the current app has no trash view?
- Which service provides generation/stems and which control values does it accept?

Proceed with all independent implementation work before asking for answers that only affect a small part of the app. Do not deploy or publish without authorization.
