# The Rack — managing devices
Source: Reason 12.7 Operation Manual, ch. 11 (whole chapter read). Tag: **Manual**.
Auto-routing rules are in `routing-and-main-mixer.md` Part 1 — not repeated here.

## Key idea: Device Group
- A Device Group = ONE source device (e.g. an instrument) + every device it feeds (effects, Mix Channel) + CV-only devices wired to it alone + their sequencer track and mixer strip.
- It is defined by CABLES, not by where devices sit in the rack.
- **Options › Auto-group Devices and Tracks** (Cmd+Shift+G): the group moves, copies, pastes and deletes as one block. Turn it ON for a tidy song.
- **Edit › Select All in Device Group** selects the whole chain.

## Creating
| Do | Result |
|---|---|
| Create an instrument | New sequencer track + Mix Channel, same name, Master Keyboard Input set to it (play at once) |
| Hold **Option** while creating an effect, mixer or Mix Channel | Also makes a sequencer track for it |
| Hold **Option** while creating an instrument | NO sequencer track (not when dragged from the Browser) |
| Hold **Shift** while creating | No auto-routing, no connections |
| Effect created with an Audio Track / Mix Channel selected | Goes into that strip's Insert FX |
| Effect created with an Instrument selected | Goes between the instrument and its Mix Channel |
| Effect created with a Mixer 14:2 / Line Mixer 6:2 selected | Goes on the first free Send FX jack |
- Option works in opposite directions: instruments already get a track, so Option removes it. Everything else has none, so Option adds one.
- New device lands just below the selected one (or at the bottom). With auto-group on, it won't land inside another group.
- Ways to create: double-click/drag from Browser palettes (Instruments / Effects / Utilities / Players), Create menu, rack-background Add Device icon, drop a patch file on the rack or Track List.
- A new patch-device gets browse focus, so the Browser shows its patches. (Preference: "New devices get browse focus".)

## Moving and re-ordering
- Drag by an empty bit of the panel. Orange line = drop spot. **Esc** while still holding the mouse = cancel.
- **Shift-drag** = move AND re-route (as if deleted and made fresh). This is how you change effect order in a chain.
- Moving rack order does NOT reorder tracks or mixer strips. Use **Edit › Sort Selected Device Groups**:
  - Tracks selected → rack and mixer follow track order.
  - Device Groups selected → tracks and mixer follow rack order.
  - Mixer strips selected → rack and tracks follow mixer order.
- Drag to the left/right edge of the rack = new rack column. Columns can't be empty.

## Replace, duplicate, copy
- **Replace**: drag a device from the palette onto an existing one (orange dim + replace icon). Same category only (instrument↔instrument, effect↔effect, player↔player). Utilities can't be replaced. New device inherits the routing. Works on Track List icons too.
- **Duplicate**: Option-drag, or Edit › Duplicate Devices and Tracks. Auto-group ON = whole group copied with cables and a new track. OFF = bare unconnected copy. Shift = try to auto-route.
- **Copy/Paste devices between songs**: preserves cables between the copied devices. Pasted below the selected device. Shift-paste = auto-route.
  - Handy for carrying a favourite instrument + insert chain from one song into another.

## Selecting
- Click, Shift-click to add/remove. Arrow keys step through the rack (Shift+arrow = range). Moving any knob selects its device.
- Master Keyboard Input tab (top-left of the selected-device border): click to play that device from the MIDI keyboard. On an effect with no track, it makes a track.

## Delete
- Backspace/Delete asks for confirmation. **Cmd+Backspace** = no alert. Cables to the device go; if it sat BETWEEN two devices, those two get reconnected.
- With auto-group on, deleting a Source or Mix Channel asks: device only, or the whole group with tracks and strips.
- Master Section and Hardware Interface cannot be deleted.
- A track can't exist without a device, but a device can exist without a track.

## Names
- Tape strip click = rename, max **16 characters**. Device, sequencer track and (for instruments) Mix Channel strip share the name.
- Mix Channel strip always shows the SOURCE device's name. Rename manually when one sampler/Kong has many outs going to separate Mix Channels (e.g. "Kick", "Snare").
- Send FX Return names in the mixer show the connected effect's name.

## View handling
- Rack Navigator (blue frame) scrolls; Page Up/Down/Home/End (rack needs Edit Focus — click in it); Shift+wheel = sideways.
- **F6** = rack fills the window (or double-click the header). **Cmd+F6** = detach rack to its own window (has its own Browser, **F3**).
- Selecting a track or clicking "Rack" under a mixer strip scrolls the rack to that device.
- **Fold/Unfold** button on each device. **Option-click** folds/unfolds the whole column. Folded devices still play and can be renamed/moved/patch-switched. Drag a cable onto a folded device and hold: it unfolds.

## For the project (**Guess**)
- A recipe's "Order of operations" can be built by Shift-dragging effects into place.
