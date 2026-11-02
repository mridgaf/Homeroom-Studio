# Physics Effects Design Handoff — 2026-11-01

## Current request

Create **three full-screen design options** for the Homeroom Studio / Beat Lab Effects page.

The direction is clear:

- Use the **same chemistry-page visual design language on both pages**.
- The Beat page remains chemistry-themed.
- The Effects page must look like it belongs to that same product, but its **subject matter, terminology, diagrams, and symbols are physics-based**.
- Do not turn the Effects page into a separate dark/navy visual system.
- Do not add reference-track analysis.
- This task is for design mockups first; do not modify Beat Lab application code until a design is selected.

## Primary visual references

### Chemistry Beat page — visual system to preserve

`/var/folders/b9/c2h90xwj60gbp06lw3wq811w0000gn/T/codex-clipboard-e40d298d-d9b7-4a46-92bd-85050cafb5b7.png`

Preserve these qualities:

- Forest-green chalkboard background and subtle chalk markings
- Warm cream paper/worksheet cards with clips
- Orange highlight color, dark teal controls, restrained secondary colors
- Real wood shelves, drawers, and desktop surfaces
- Vintage school-science objects and tactile materials
- Narrow left navigation rail
- Mature, polished music-software density: fun and quirky, but not childish
- Compact player/queue hierarchy and clear current-selection emphasis

### Existing Effects page — functional layout reference only

`/var/folders/b9/c2h90xwj60gbp06lw3wq811w0000gn/T/codex-clipboard-6de6a001-ee48-44a2-a62d-be8705c0ac4e.png`

Retain its useful functions:

- Top beat transport and waveform
- Back to beats, Load audio, Browse beats, Send back, Sketch, Export
- Channels: Kick, Snare, Hats, Bass, Chords, Sample
- Channel volume/pan, mute/solo, A/B routing
- EQ and Compressor editing
- Effect selector/inventory
- Bus A, Bus B, Master, Dry/Wet, A/B comparison

Do **not** preserve its standalone dark/navy styling. Translate those functions into the chemistry page's chalkboard, paper, orange, teal, glass, and wood system.

## Three design options to render

### Option 1 — Physics Lab Bench

- Cream transport worksheet across the top
- Sound-source lab cards at left
- Two large graph-paper experiment cards in the center for EQ and compression
- Physics effects inventory on clipped cards at right
- Bus A, Bus B, and Master as wooden lab drawers across the bottom
- Symbols/objects: `y(x,t)`, frequency `f`, amplitude `A`, wavelength `λ`, phase `φ`, resonance, force vectors, oscilloscope, tuning fork, pendulum

### Option 2 — Wave Mechanics Classroom

- More strongly classroom-oriented composition
- Channels displayed as cream index cards in a vertical classroom file
- Oversized central graph-paper worksheet titled Frequency & Resonance / Force & Compression
- Effects list presented as a wooden card catalog
- Bottom signal routing built into the desk as three instrument bays
- Symbols/objects: `f = 1/T`, `λ = v/f`, harmonic series, springs, pendulums, prisms, wave interference diagrams
- Orange is primary; cyan is a restrained graph/measurement accent only

### Option 3 — Acoustics Field Notebook

- A distinct open-lab-notebook composition, not just another rearrangement of Option 1
- Left side: experimental apparatus and compact channel strip cards
- Center/right: large open cream notebook with tabbed physics domains such as Oscillation, Dynamics, Space/Time, Stereo/Phase
- Selected effect gets a large, legible experiment page with graph and controls
- Signal flow across the bottom uses a clean circuit/force-vector diagram integrated into the wooden desk
- Include the same complete functions as the existing Effects page
- Physics symbols should support navigation and meaning, not become decorative clutter

## Problems encountered

The image-generation service failed twice during rendering:

1. First generation ran for roughly three minutes, then returned `image generation failed: network error: error sending request`.
2. A retry began but remained in a running state without returning an image. It was deliberately terminated when the user requested this handoff.

No completed or approved mockup was produced in the interrupted session. The issue was tool/network reliability, not uncertainty about the design brief.

## Fastest restart path

1. Open both reference images and confirm their roles: Image 1 controls appearance; Image 2 controls Effects-page functions.
2. Generate the three mockups **serially**, not in parallel.
3. Use one concise prompt per option and allow up to 120 seconds for each initial call.
4. If a call yields a running cell, wait once. If it ends in a network error, retry that option once with a shorter prompt.
5. Save each successful image immediately before starting the next:
   - `physics-effects-option-1-lab-bench.png`
   - `physics-effects-option-2-wave-classroom.png`
   - `physics-effects-option-3-field-notebook.png`
6. Visually inspect each result for: chemistry-style continuity, physics-specific content, readable controls, full feature coverage, and absence of reference-track analysis.
7. Deliver all three together so the user can compare them.

## Repository boundary

Homeroom Studio is reference-only for the Beat Lab implementation. If the user later selects an option and asks to build it, write only in:

`/Users/johnsuhr/Desktop/Beat Lab Codex`

Before any implementation, verify `pwd`, Git root, current branch, and worktree state. Do not write Beat Lab implementation changes into the Homeroom Studio repository.
