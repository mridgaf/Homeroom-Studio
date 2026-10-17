# Combinator

A container that saves a whole chain — instruments, effects, mixers, and the
cables between them — as one patch (a "Combi", `.cmb`). Its front-panel knobs
and buttons are "virtual": each one can be wired to any number of parameters on
the devices inside.
Source: Reason 12.7 Operation Manual, ch. 63, pp. 1305–1332.

## When you'd use it
- Saving a finished recipe chain (e.g. bass + Scream 4 + EQ) as one patch you can reload.
- Layers and splits: several instruments played together, by key or velocity zone.
- Multi-effects: an effect chain saved as an Effect Combi, droppable into a mixer insert.
- One-knob macros: one Rotary moves several parameters at once, in different directions.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Rotary 1** … **Rotary 16**: the virtual knobs. Do nothing until mapped in the Editor's Modulation Routing. Their moves record as automation.
- **Button 1** / **Button 2** / **Button 3** / **Button 4**: virtual switches, same idea.
- **Mod Wheel** / **Pitch Bend**: passed to every instrument inside; each device decides what its wheel does.
- **Run Pattern Devices**: starts/stops Matrix/Redrum-style pattern devices inside. Pressing Play does this automatically.
- **Bypass All FX**: bypasses every insert effect inside, turns off send effects.
- **Select Next Patch** / **Select Previous Patch**: browse Combis.
- **Enabled**: bypass/on/off.

## How mapping works (Editor → Modulation Routing)
- Pick a device on the left, then per row: **Source** (a panel control) → **Target** (any parameter of that device) → **Min/Max**.
- Min above Max = reversed: turning the knob up turns the target down.
- **Source Range**: make a knob act only over part of its travel (e.g. 50–100%).
- Same knob can hit several devices — select another device and map it again.
- Quick way: right-click any parameter on an inner device → assign to a Combinator control.

## Rules worth knowing
- **Keep cables inside.** Anything wired straight to a device outside the Combi is "External Routing" and is NOT saved with the patch. Go through the To/From Devices jacks.
- 8 stereo "From Devices" inputs on the built-in mixer; out of room → add a Line Mixer 6:2.
- Devices you add inside a Combi get no sequencer track (hold Option when creating to get one).
- Combine existing devices: select them (Shift-click) → Edit > Combine. Edit > Uncombine undoes it.
- Panel can be 1U–6U, up to 32 knobs/faders + 32 buttons; custom backdrop images (3770 px wide).

## For the voice bridge
The bridge can only turn knobs Reason exposes for a device. A Combinator's
Rotary 1–16 can be pointed at ANY parameter inside it, so wrapping a device in a
Combi is the way to automate controls the bridge has no direct map for.
(Today the bridge maps only patch next/prev on the Combinator — not its knobs.)

## Where it shines / falls short
Shines: turning a recipe into a one-click, tweakable instrument. Falls short:
nothing inside is scriptable from outside except through those virtual controls.

## Pairs well with
Everything. Spider Audio for parallel chains inside, Line Mixer 6:2 for more inputs.
