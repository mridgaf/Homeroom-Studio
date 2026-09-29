# How to read a Reason song's rack back (method notes)

Written 2026-09-29 from four demo songs (Street Phone, Airplane, Power, Qua z mo). Tags: **Seen** = on screen · **Manual** = manual place named · **Guess** = not confirmed. Nothing here was heard. This is the method behind the `reason-signal-flow` skill idea in [demo-song-skill-ideas.md](demo-song-skill-ideas.md).

## 1. Open and close safely (Seen)
- Demo files show "[Read-only]" in the title bar. Never save. Close with the window's red button and read the dialog before answering; for a demo that has only been looked at, no dialog appeared (five-plus times).
- Check the file's SHA-1 before opening and after closing. All four demos came back identical.
- Unfolding a device or scrolling is a view change, not a song edit.

## 2. Moving around (Seen)
| To do this | Do this |
|---|---|
| Switch view | Window > View Main Mixer / View Racks / View Sequencer |
| Flip rack front/back | Tab (or Options > Toggle Rack Front/Rear) |
| Scroll the rack | PageUp / PageDown (key name `pagedown`); arrow keys move between rack columns |
| Scroll the mixer sideways | Drag its bottom scrollbar (a mouse wheel over knobs can turn them; my slip) |
| See the whole song | Sequencer ZOOM button |

## 3. Read a cable by hover (Seen)
- Hover a jack for 2-3 seconds. Tooltip: "Connected to <device>: <jack>". An unconnected jack shows only its own name.
- Hover jacks, not cable bodies (two tries on bodies showed nothing).
- Take hover coordinates from a display screenshot; app-window screenshots use a different scale (1382x868 vs 1372x891) and the tooltip will not appear.
- Ctrl-click a jack lists every rack device, check on the connected one, asterisk on occupied jacks (Airplane). Needs real clicks.

## 4. The unfold trap (Seen)
- Batching several fold-triangle clicks fails: Reason auto-scrolls when an unfolded device ends below the window, so later clicks land on the wrong thing (my method error).
- Do one unfold click, then one screenshot, every time.
- Option-click on a fold triangle should unfold the whole column (**Manual [11] line 9103**); not tested.

## 5. Layout convention (Seen in Power and Street Phone; Guess that it always holds)
- A mixer strip sits directly above its instrument. Insert devices sit below it, labelled with the channel name. The last insert's output goes up to the strip ("From Insert FX").
- Channel to master has no cable (P-LAN, **Manual [16]**). Send effects go through the Master Section's FX Send/Return 1-8.
- So you can trace a channel by reading the labels top to bottom before hovering anything.

## 6. Cable colours (Manual [16])
Green = effects · red = instrument to mixer · yellow = CV · blue = Combinator.

## 7. What could not be done
- Mouse clicks were blocked while macOS Dictation was on (keys, hover and the app-window tools still worked).
- Inner cables of Combinators were read only where hovered; most were not traced.
- Whether a device does what its name says was never heard.
