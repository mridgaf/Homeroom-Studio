# Draft wording: what I would put into the skills (nothing is applied yet)

Target file: `.claude/skills/reason-remote-bridge/SKILL.md` unless said otherwise.
Say "apply" and I put each block in; say what to change and I change it first.

---

## A. Replace rule 6 (it is wrong: it puts the arm button on each lane and says I never saw it)

> 6. **Arming a lane: the owner's steps (2026-09-30, then Seen).** Use these every time,
>    for any device or effect that can have a track:
>    1. Right-click the device > **Create Track for X**. Once a track exists the same
>       menu shows **Go to Track for X**; if that item is live, the track exists.
>    2. On that track's row, the button **just right of the S (solo) button** is the
>       record-arm. **Red = armed.** Read its colour before and after any click on it:
>       on 2026-09-30 I clicked a red one and disarmed it.
>    3. Start recording and move a knob. A lane **named after that knob** appears on
>       the track. Nothing appears until a knob moves during a recording.
>    If a lane does not record, look at the track row first (is it red?), then check
>    the lane exists, then check you are looking at the bars the sweep landed on (rule 11).
>    Seen 2026-09-30: with the track armed, a Filter Frequency lane on The Echo
>    recorded both a typed and a spoken sweep. The earlier belief that each lane has
>    its own button is dropped.

## B. Add to rule 8 (the microphone)

> **Microphone path proven 2026-09-30 (Softube Amp, The Echo).** He held the page's
> talk button: "make it twang." and "sweep the filter frequency down over 4 bars at
> 115" were heard word for word and ran. **He must hold the button the whole time he
> speaks;** a short tap loses the phrase and the app shows nothing new (no error).
> To see why a phrase is missing, run a watcher on the page's websocket
> (`ws://localhost:8765/ws`) and print status changes: recording > thinking > idle.
> A test that cannot move anything proves nothing: "gain up a bit" on a knob already
> at maximum was heard right but changed nothing. Pick a phrase that visibly moves.

## C. New rule 10: adding a device to the scratch song

> 10. **Add a device from Reason's own browser (Seen 2026-09-30).** Click the
>     browser's Effects (or Instruments) category, click the search box (click first;
>     typing before the box has focus goes nowhere), type part of the name, press
>     Return, then **double-click** the result. The Softube Amp ("Amp") was added this
>     way and then swept (Twang 0-25, Crunch 26-50, Rock 51-76, Lead 77-101,
>     Bypass 102-127). This replaces the 09-29 note that Create-menu presses added
>     nothing visible. A new device lands after the selected one; scroll the rack to it.

## D. New rule 11: where did the sweep land

> 11. **Before judging a sweep, know which bars it is on.** A move lands at the
>     playhead and Reason's sequencer view may be scrolled elsewhere (it sat at bar
>     98 while the song was at bar 1). Click the ruler to put the playhead on **empty
>     bars** (4 bars ahead of any other clip), note the bar number, and look at those
>     bars. Optional, the owner's idea: a short loop (about 5 bars) with Loop on and the
>     view zoomed to it, so the whole piece is always on screen. At the end of the
>     loop the playhead jumps back and the lane plays again from its start; that is
>     looping, not a failure. Not tried: recording while Loop is on may add a new
>     take each pass.

## E. New rule 12: the screen overlay

> 12. **Screen control puts an overlay over his whole screen.** While it is on he
>     cannot see or use the app page, so he cannot speak to it. Release it
>     (`release_full_control`) whenever he must look or talk, and ask again when I
>     need clicks. Overrides the earlier "never release" note.

## F. `OPEN-ISSUES.md` item 44 (add one line)

> 2026-09-30: adding a device from Reason's browser (search, double-click) worked
> under full-screen control; Create-menu presses were never the way. Cabling still
> not tried.

## G. `reason_voice` note, beside the Neptune fix (DECISIONS only, no skill)

> The model copies example wording from a device guide line: "~12 o'clock" came back
> as its answer. Write guide lines as plain direction ("turn UP for faster").

---

Not changed on purpose: no benchmark loop (these are corrections, not a new skill),
no change to `CLAUDE.md`.
