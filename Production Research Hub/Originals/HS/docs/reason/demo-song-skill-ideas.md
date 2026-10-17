# Skill ideas from the demo songs (Street Phone, Airplane, Power, Qua z mo)

Running list (started 2026-09-29, step 00b). Skills worth having, found while exploring the demo.
Song details are in [demo-song-notes.md](demo-song-notes.md).

**Your rule for this session:** list first, build only the clear wins (small, reusable, already done by
hand in the demo).
**Why nothing is built yet:** your standing rule (memory `skill-benchmark-loop`) says a new skill goes
through skill-creator's benchmark loop (test prompts, with/without runs, review viewer, then your
feedback). That is a separate piece of work, not something to slip in at the end of an exploring
session. The two clear wins are marked below and are ready to start on your say-so.

Status: `idea` | `clear win, ready to build` | `built`

| Skill | One-line job | What triggers it | Status | Came from |
|---|---|---|---|---|
| **explore-reason-song** | Safely tour an open Reason song by screen: switch Mixer / Rack / Sequencer, unfold devices, expand automation lanes, read the transport, then close with Don't Save | "look at this song", "what's in this song", "learn from this demo" | **clear win, ready to build** | Everything I did by hand this session. Traps from this session, with how sure I am: Magnify tool zooms on double-click (seen, use the arrow); a second double-click on an automation clip may have changed its point (manual says it inserts one; I couldn't tell what happened), so open a clip once and click a point once; my playhead clicks landed on wrong bars because I mis-scaled coordinates (my error, so read the transport readout); a batch that stops mid-way leaves playback running (seen); never press a lane's X (manual); File > Close and Edit > Undo were greyed out while Reason wasn't the active app (seen), so close with the window's red button and read which document the dialog names first. **From Airplane (00c):** Window > View Main Mixer / View Racks / View Sequencer switches the view (Seen); Options > Toggle Rack Front/Rear flips to the back (Seen; a Tab keypress via the tool got "no verdict" twice, the menu worked); the mixer scrolls sideways by dragging its bottom scrollbar and the rack by dragging the blue box in its top-right map (Seen); the sequencer's ZOOM button fits the whole song and the two magnifiers at bottom left change track height, not the timeline (Seen); the small triangle at a device's top left folds it (Seen, needs a precise click); hover tooltips and the Ctrl-click jack menu need screen control (approved on a second visit): Ctrl-click via the display tools, Escape closes only sub-menus, a click on the window title bar closes the whole menu, and the list scrolls while the pointer rests on its bottom arrow (Seen). Closing a song with no changes gives no save dialog (Seen) |
| **reason-automation-lanes** | Read, open and explain automation: one lane per knob, clips with a cut corner, one-point clips holding a value, the Static Value, green borders, Automation Override, what M and X do | "how is this sweep made", "what is automated", "add a sweep" | **clear win (read side), ready to build**. The create side is from the manual only, not tried | Organ 1 filter clip opened by hand; override tested on the WarmPad fader; manual ch. 6 and 9 |
| reason-signal-flow | Read the back of the rack: cable colours (green effects, red instrument-to-mixer, yellow CV, blue Combinator), insert chains, shared effects on the Master Section's 8 sends, P-LAN having no cables, hover and "Scroll to Connected Device". **Also covers (merged from two earlier rows):** keyboard-only reading (Tab flips front/back, PageUp/PageDown scroll, arrow keys move between rack columns, hover a jack 2-3 s for "Connected to <device>: <jack>"; works while mouse clicks are blocked), and the layout convention (a channel strip sits directly above its instrument, inserts below it carry the channel's name, last insert goes up to the strip; Seen in Power and Street Phone, **Guess** that Reason always lays it out this way), plus the unfold trap (one unfold click per screenshot; batching misfires because Reason auto-scrolls) | "how is this connected", "where does this go", "map the rack" | **clear win (read side), ready to build**. Hover and Ctrl-click jack menu Seen (Airplane); whole rack read by keyboard and hover (Power, Qua z mo master and Pad FX, Street Phone channels). Needs screen control approved each session | Airplane, Power, Qua z mo, Street Phone back views; Manual [16] lines 11430-11500 and 11646-11660 |
| reason-combinator-macros | Read a Combinator's face (Rotary 1-4, Button 1-4, author labels), open its Devices and Editor, explain Modulation Routing (source to target, min/max, reversed, source range) | "what does this knob do", "what's inside this box" | idea. Modulation Routing itself not opened | KICK SQUASH and PAD PROCESSOR faces; manual ch. 63 |
| reason-mixer-by-master-section | Control any mixer channel by number through the Master Section map (Mute, Solo, Level, Pan, FX sends, All Mutes Off), and the channel-name-to-number step | "mute the kick", "more delay on the vocal" | idea (needs the app work in OPEN-ISSUES item 29 first) | Found in `remote-vocab.json` while checking the phrase list |
| song-to-phrase-gaps | Take the devices and lanes of an open song, look each up in the remotemap and calibration, and print what the voice app can and can't do | "what can the voice app do with this song" | idea. A small script plus a skill | The phrase list (A-E) was made by hand this way |
| reason-reference (update, not new) | Add a chapter-and-page pointer table to the existing skill: automation (ch. 6, 9), routing (16), main mixer and sends (17), Combinator (63), rack groups (11) | "look up how Reason does X" | idea. Small edit to an existing skill | The manual answered almost every "why" question I had |
| **reason-ducking-methods** | Explain the three ways a Reason song can "duck" or pump, and how to tell which one a song uses: (a) a compressor keyed by a cable in its Sidechain Input (Manual [17], lines ~12958-12991), (b) an Output Bus with a sidechain source (same place), (c) a Synchronous curve on Level, no cable (Airplane), (d) a Redrum used as a silent kick trigger cabled into a channel's Side Chain Input with KEY lit (Power Bass; check that the Redrum runs: RUN, pattern, no track; Seen wiring, not heard; OPEN-ISSUES 41) | "how is this sidechained", "why does it pump" | idea. Method (c) is Guess: the curve is Seen, the sound is not heard | Airplane: the channel and bus are both named "Sidechain Bus", but the Sidechain Input jacks are empty and the pumping device is a Synchronous "Long Sidechain" |
| **reason-output-bus-routing** | Read which channels feed which Output Bus: pink Output labels in the mixer, "Audio Output" on each rack device, red fader knob and "INPUT DISABLED, CHANNEL IS USED AS OUTPUT BUS" on the bus device's back | "what goes to this bus", "why is this pink" | idea. Small; done by hand in Airplane. Manual [17] "Output Busses" lines 12600-12660 | Airplane mixer and rack back |

## Notes
- The first two are the ones I'd build first. `explore-reason-song` would have saved most of the wrong
  turns in this session.
- `reason-remote-bridge` already covers locking a device and the bridge's file formats. None of the
  ideas above overlap it.
- Only `reason-ducking-methods` needs a listening check (method (c) is a guess until someone hears the Airplane bus).

## Build-by-hand skills (2026-09-29, practice songs untitled 2 and 3)
Owner: many small skills in sets, not one big one, for Hermes to do these jobs in Reason. All Seen by doing, none heard by me, none built.

| Set | Skill | Job and trap |
|---|---|---|
| 1 Safe handling | open-close-demo-safely | hash before/after, red-button close, read dialog, never save |
| 1 | fresh-blank-song | Cmd-N, Select All, Delete Tracks and Devices, answer "Delete All in Group" |
| 1 | reason-control-methods | app_menu picks menu items by name (best); coordinate menu clicks flaky; right-click and real drags need the full-screen tools |
| 2 Reading | read-rack-by-hover | hover 3 s for "Connected to..." |
| 2 | read-insert-chains | strip above its inserts, named for the channel |
| 2 | read-combinator-routing | Editor, click each device row: Source, Target, Min/Max |
| 2 | unfold-one-at-a-time | one unfold per screenshot |
| 3 Building | create-devices-by-menu | Create > Instruments/Effects/Utilities; effects made with an instrument selected chain in |
| 3 | matrix-on-instrument | right-click instrument > Utilities > Matrix (auto-cabled), draw 16 notes, Run |
| 3 | redrum-pattern | click steps; needs a Pattern Select lane clip or it does not play |
| 4 Automation | make-automation-lane | right-click knob > Edit Automation |
| 4 | draw-lane-clip | pencil: press, move, release (plain drag does nothing; first stroke after a tool switch is swallowed) |
| 4 | shape-lane-curve | Edit Inline (sometimes needs a second click), pencil a curve |
| 4 | matrix-pattern-lane | Matrix "Pattern Enable" lane needs a clip |
| 4 | loop-to-lanes | drag right loop marker to end of lanes, Loop on; else lanes end and effects stop |
| 5 Traps | hands-off-when-owner-moves | owner rule: cursor moves, stop and watch |
| 5 | dictation-blocks-clicks | turn Dictation off first |
| 5 | classifier-no-verdict | retry once, then stop and report |

Build first: make-automation-lane, draw-lane-clip, loop-to-lanes, matrix-on-instrument, create-devices-by-menu. Not solid: live knob recording wrote no lanes; Redrum and Europa sounding not confirmed.
