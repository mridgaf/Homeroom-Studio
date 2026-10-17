# Remote — playing and controlling devices with hardware / keys
Source: Reason 12.7 Operation Manual, ch. 23 (whole chapter read). Tag: **Manual**.
Not the same as the project's "Remote bridge" (voice → Reason). That is in `.claude/skills/reason-remote-bridge`. This is Reason's built-in way to map real knobs and keys.

## Setup (Preferences › MIDI tab)
- **Easy MIDI Inputs** (default): every MIDI in-port is auto-connected. Gives notes + mod wheel, pitch bend, sustain only. Untick "Enabled" for a port you don't want (e.g. a drum machine that sends clock/notes). Easy inputs cannot be locked to a device.
- **Known surface**: Auto-detect Surfaces, or Add manually (Manufacturer › Model). Read the picture's text: some surfaces need a preset. Add MIDI Output only if the surface has motor faders/displays. Use **Find** + wiggle a control to pick the port.
- **Not listed**: use "Other" › MIDI Control Keyboard / MIDI Control Surface (program the controller to send the CCs from the MIDI Implementation Chart) / MIDI Keyboard (No Controls) / Multichannel versions (no auto-map, use Remote Override).
- **Master Keyboard** = the ONE surface with keys that plays the track having Master Keyboard Input. First keyboard added becomes it. "Make Master Keyboard" / "Use No Master Keyboard" buttons.

## How it behaves
- **Standard mapping**: by default every surface FOLLOWS Master Keyboard Input. Select a Subtractor track → the knobs control Subtractor; select NN-XT → knobs control NN-XT. Nothing to set up. Same in every new song.
- **Mapping variations**: more parameters than knobs → Cmd+Option+1…10 (top row numbers, not keypad) switches the set (1 = default), e.g. filter / oscillators / LFOs. Resets to 1 when you change device.
- **Lock a surface to a device** (so it never follows the track):
  - Options › **Surface Locking…** pick surface, pick device (or "Follow Master Keyboard"), optionally lock a mapping variation.
  - Or Ctrl-click a device › "Lock to <surface>" (tick/untick).
  - A surface can lock to ONE device; several surfaces can lock to the same one. Can also lock to the **Main Mixer** (levels/pans) or the **ReGroove Mixer**. Saved with the song. Master keyboard can't be locked.
  - Extra keyboards locked to devices are record-enabled automatically → play several instruments at once.
- **Ideal rig (manual's words)**: master keyboard with controls + extra surfaces locked to the Main Mixer and to key devices; one fader bank for mixing, one for the synth.

## Remote Override (map ANY knob to ANY parameter)
- Saved WITH THE SONG only (standard mapping is built in).
- Quick: **double-click** a parameter in Remote Override Edit Mode → rotating lightning bolt → move the control. Esc to cancel.
- Or: Ctrl-click a parameter › **Edit Remote Override Mapping…** → choose surface+control or tick **Learn From Control Surface Input**. Keys of a keyboard can be mapped as on/off buttons (Note Number field).
- **Options › Remote Override Edit Mode** shows what's mappable (blue arrows), standard mappings (yellow knobs) and overrides (lightning bolt). While it's on you can't play normally. Hover for a tooltip showing which control. Esc leaves it.
- Transport panel items can be mapped too.
- Clear one: Ctrl-click › Clear Remote Override Mapping. Clear all for a device: "Clear All Remote Override Mappings for Device".
- Copy / Paste overrides between devices of the SAME type, and from Transport panel to another song.
- **Additional Remote Overrides…** (Options menu) maps functions you can't click on: Target Previous/Next Track (move Master Keyboard Input up/down the Track List), Target Track Delta (jog wheel), Select (Previous/Next) Patch for Target Device (browse patches of whatever you're playing), Keyboard Shortcut Variation select, Undo/Redo, Document Name on the surface display.

## Computer keyboard control (no MIDI)
- Options › **Enable Keyboard Control**, then **Keyboard Control Edit Mode** (yellow arrows) or Ctrl-click a parameter › Edit Keyboard Control Mapping. Press the key (Shift+key allowed).
- Not allowed: Space, Tab, Enter, keypad, function keys (except F2, F3).
- Only toggles on/off or min↔max. Multi-selector buttons cycle options. Doesn't work for ReGroove Mixer. Main Mixer strip knobs: Ctrl-click each (no edit mode).

## Template trick
Standard mapping needs no saving. For custom overrides: save a song with just the devices + overrides (no notes), put it in the Template Songs folder, and start new songs from it.

## Other MIDI paths (mentioned, not detailed here)
External Control Bus inputs (Preferences › Sync, MIDI In device) = direct MIDI to individual devices from another sequencer. MIDI Clock sync for tempo. Details are in ch. 24.

## For the project (**Guess**)
- Remote Override + Learn is a hands-free way to map a MIDI knob to a Combinator Rotary (see `combinator.md`), then the Rotary to many parameters. One physical knob → macro.
- Target Next/Previous Patch is the same job the voice bridge's patch next/prev does, but from hardware.
