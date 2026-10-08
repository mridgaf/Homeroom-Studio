# Knob-check trial — Sweeper, 2026-10-07 (result: PARTLY WORKS)

Method: lock the surface to the device (right-click blank ear > "Lock ReasonVoice ReasonVoice 2 to This Device",
read the tick first) while a listener runs -> Reason announces EVERY Remote knob with its current value.
Then tools/panel_sweep.py moves each knob (CC 30+k-1), screenshots before/after, diffs, puts it back.

## What worked
- Lock announcement = all 33 Sweeper Remote names + slots + current values in one shot (Bandwidth "78.9 %" matched the hover tooltip).
- Sweep located ~20 of 33 on the panel on the first pass (Bandwidth, Frequency, Feedback, Dry/Wet, Spread, Volume, Polarity, Mute Dry,
  Stages, LFO->Freq, MOD->Freq, Rate Mod, LFO rate/wave/sync, Env loop/rate, Beat sync, Bypass). Positions are in the MCP screenshot frame
  (1372x891 = whole built-in display); screencapture and the MCP frame share it. Rack must not be scrolled during the sweep.
- Knobs that change the VIEW (Type, ModType, Filter Type) show up as huge diffs -> tells you which extra pictures a device needs.

## What did not work / still needs hover
- ~13 knobs gave only noise: controls hidden in the current mode (Filter/Audio Follower items) AND at least two that should be visible
  (LFO Amp Mod, Env Amp Mod = LFO/MOD->Volume?) — unexplained, check by hover.
- Header patch-name display flickers on every change: ignore clusters in the header band.
- Restore is approximate: continuous knobs land +-1 step (LFO 0.145->0.140 Hz, Loop 0.631->0.614 s). Stages needed a manual nudge.
- Does NOT cover jacks (no CC) or buttons without a Remote item: those stay hover / right-click.
- Side effect: first (unlocked) test moved Neptune's Catch Zone Size (surface was still locked to Neptune). Test song only.
- Pillow does not build on Python 3.9 here; script uses numpy + sips + screencapture instead.

## Verdict
Use it to find positions and confirm names/values for knobs (saves most of the hovering). Still hover: jacks, switches, anything the sweep misses.
