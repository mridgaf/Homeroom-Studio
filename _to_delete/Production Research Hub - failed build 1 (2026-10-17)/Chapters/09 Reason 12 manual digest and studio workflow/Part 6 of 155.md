# Chapter 09: Reason 12 manual digest and studio workflow
## Part 6 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- patches-and-browser.md — Patches, Browser, Rack Extensions and VSTs
- players.md — Players: chords and arpeggios from single notes (digest of Reason 12.7 manual, ch. 12)
- rack.md — The Rack — managing devices
- remote-control.md — Remote — playing and controlling devices with hardware / keys
- sampling.md — Sampling in Reason (digest of Reason 12.7 manual, ch. 21)

(Next: Part 7 of 155)


=====================================================
SOURCE FILE: patches-and-browser.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/patches-and-browser.md
=====================================================

# Patches, Browser, Rack Extensions and VSTs
Source: Reason 12.7 Operation Manual, ch. 13 (Rack Extensions), ch. 14 (VST Plugins), ch. 15 (Sounds, Patches and the Browser). Whole chapters read. Tag: **Manual** unless marked **[Guess]**.
Creating/moving devices: `rack.md`. Combinator internals: `combinator.md`. Song/template saving, export: `export-and-performance.md`. Sampler loading: `sampling.md`.
**Not in the manual:** a Browser "tags" system. These chapters have no tag search, only name search, Favorites lists and Locations. Do not promise tag search.

## 1. What a patch is (and is not)
| Device | Patch holds | Does NOT hold |
|---|---|---|
| Subtractor, Thor, Malstrom, Europa | All panel settings | n/a |
| NN19, NN-XT, Mimic, Grain | Sample references, key mapping, panel settings | The samples themselves |
| Dr. Octo Rex | Which REX files per slot + settings | The REX files |
| Redrum / Kong kit | A whole drum kit: sample references + each sound's settings | Samples. Redrum patterns are separate and stay put when you load a kit |
| RV7000, Pulveriser, The Echo, Alligator, Scream 4, Softube amps | Panel settings | n/a |
| Combinator | Everything inside it, cables inside it, zones, modulation routing | Anything outside the Combi |
- Only Combi patches keep cable routing. Other patches never do.
- Devices inside a Combi are not saved as separate patches unless you save them from within the Combi.
- Mix Channel, Audio Track and Master Section use **Insert FX patches = effect Combinator patches (.cmb)**.
- Saving the SONG stores the actual settings, not links to patch files. Deleting a patch file later does not change the song. Samples are not stored unless the song is self-contained.

## 2. File types you will meet
| Extension | What |
|---|---|
| .cmb | Combinator (also Insert FX patches) |
| .zyp / .thor / .xwv | Subtractor / Thor / Malstrom |
| .smp / .sxt | NN19 / NN-XT |
| .drp / .drex | Redrum kit / Dr. Octo Rex |
| .kong / .drum | Kong whole kit / one Kong pad |
| .rv7 / .sm4 / .echo / .pulver / .gator | RV7000 / Scream 4 / The Echo / Pulveriser / Alligator |
| .repatch | Rack Extension (one extension for all RE devices) |
| .vstpreset / .fxp / .fxb | VST3 preset / VST2 program / VST2 bank |
| .rfl | ReFill |
| .reason (.rns older) | Song |
| .rx2 .rcy .rex | REX loops |
| .wav .aif .mp3 etc. | Audio. WAV/AIFF must NOT be floating point. Mac also reads .m4a, .aac, .caf, .mp4 and more |
| .sf2 | SoundFont. Samplers and Redrum load single presets/samples, not the whole bank |

## 3. Browser basics
- **F3** shows/hides the Browser (Windows menu > Show/Hide Browser). Cmd+F6 detached rack gets its own Browser; browse focus can only be on one at a time.
- **Browse focus**: orange label at the top = the Browser is locked to the selected device/track and shows only its patches. Orange side bars appear on the device. A new device gets focus automatically (Preferences > General > "New devices get browse focus").
- Set it: select a device or track, click the folder button in the Browse Focus field. Clear it: click the rack background, click X on the label, or pick another track.
- Locations list (left): fixed ones are Reason Sounds, Orkester Sounds, Factory Sounds, Rack Extensions, This PC, Desktop, Song Samples. Add your own by dragging a folder/file/ReFill onto the list. Remove with Delete. Warning triangle = location missing.
- Put ALL ReFills in one folder and add that folder as a Location. Some ReFills split patches and samples into separate files; adding only one means samples won't be found.
- Un-synced cloud folders (Dropbox etc.) in Locations can make indexing very slow. Exclude them via the "Do not index these folders" preference.
- Columns: Name, Type, Modified, Size. Click a header to sort.

## 4. Loading patches (any one of these)
| Method | Detail |
|---|---|
| Double-click a patch | Loads into the device with browse focus |
| Up/Down arrow keys, or Load Previous/Next triangles | Steps through the list, loading each (folders skipped) |
| Select + Load button or Enter (not numpad) | Standard |
| Drag a patch onto a device panel or track-list icon | Dropping a different device's patch REPLACES the device (same category only; utilities can't be replaced) |
| Patch name display on the device | Click for a pop-up list of the patches in the current folder; has "Open Browser..." |
| Select Patch buttons on device | Step next/previous in the browse list |
| Edit > Browse Patches... (or device right-click) | Sets browse focus |
| Edit > Browse Insert FX Patches | On a Mix Channel/Audio Track/mixer channel: effect Combi patches only |
- **Revert** button appears after the first load. Gets back the original patch, even after cross-browsing.
- Careful on Redrum, NN19, NN-XT, Kong, Grain, Dr. Octo Rex: they have other Patch buttons for samples/loops. Use the one next to the patch name display.
- Panel edits after loading do not touch the file on disk.
- Patch stepping can also come from a MIDI keyboard's patch buttons (Remote).
- "Load Default Sound in New Devices" (Preferences > General, on by default): a new device loads a starter patch.

## 5. Search, cross-browsing, Favorites
- **Search**: Cmd+F jumps to the Search box. Results appear as you type. It searches the folder/location shown and everything under it, matching NAMES of files, folders and ReFills. In Factory Sound Bank, results are grouped: Instrument Patches, Effect Patches, Other Patches, Samples, Folders. Flat list with a Parent column. "Go to Parent Folder" in the root drop-down jumps to the real folder.
- **Cross-browsing**: open the Browser from a Subtractor, pick "Reason Factory Sound Bank" in the root drop-down, load a Malstrom patch: the Subtractor is replaced by a Malstrom on the same track. Track and Mix Channel names follow the patch name unless you renamed them.
  - Instruments only see instrument patches; effects only see effect patches. Insert FX browsing cannot cross.
  - Replacing can lose cables (an NN-XT's 16 outs into a Subtractor's 1; CV on the back panel). Only Sequencer Control CV/Gate survives. **Undo** restores them; browsing back does NOT.
- **Create > Create Instrument... / Create Effect...**: browse all patches with no starting device. Loading one builds the device, track, Mix Channel, names, and sets Master Keyboard Input. Good for "find me a pad".
- NN19 .smp and REX patches load into the device you browse from, else into an NN-XT. Create Instrument makes an NN19 for .smp and a Dr. Octo Rex for REX.
- **Favorites Lists**: star-icon folders of shortcuts to anything loadable (files stay where they are). Create with the "Create New Favorites Lists" button, rename by double-click, drag files in, reorder by drag (no header sorting), Delete removes the shortcut only. Do NOT put ReFills in them; use Locations.
  - To add several files at once, the device must have no browse focus.
  - **Live-set trick**: put chosen patches in a list, order them, load the first, save the song, then step with "next patch" on the device or a keyboard button.
- **Browse list**: the list memorised when you click Load. It drives Next/Previous and the name pop-up. After saving and reopening it shows as "Document Browse List" (flat, with Parent column). A Favorites list or search result can be the browse list, which controls what the next/previous buttons step through.
- Audition samples/loops: Play button, or **Auto** to play on select, and a level slider.
- Multi-select loads: Kong pads, NN-XT/NN19/NN-Nano samples, Dr. Octo Rex loops, many audio imports.

## 6. Saving patches
- Click the **Save Patch** button on the device, choose name and place. On Mac extensions are not required; keep them if the file may be used on Windows.
- **Option+click Save Patch (Alt on Windows)** = overwrite the same file silently. Be sure.
- **You cannot save into a ReFill.** Save modified ReFill patches to a normal folder with a new name.
- **Copy Patch / Paste Patch** (Edit or right-click): copy settings between same-type devices, even across songs. Includes sample references.
- **Insert FX <-> Combinator**: Edit > "Copy Channel Settings -> Insert FX", select an empty Combinator, Edit > Paste Patch. Reverse: Copy Patch on the Combinator, select the channel, Edit > "Paste Channel Settings: Insert FX".
- **Reset Device** (Edit or right-click): default values; on samplers/Redrum/Kong/Dr. Octo Rex also clears sample/REX references.
- For the project **[Guess]**: a recipe step like "save this as a patch" maps to Save Patch > own folder (not a ReFill), then add it to a Favorites list.

## 7. ReFills
- A .rfl is a big sound package (patches, samples, REX, SoundFonts, demo songs), like a ROM card. Samples are stored at about half size, lossless.
- Built in: three ReFills "Reason Sounds", "Orkester Sounds", "Factory Sounds". Reason tells you which ReFills a song needs.
- Browsed like folders. Read-only for saving. Samples from ReFills can be self-contained into a song but not un-self-contained.
- Missing ReFill/sample: **Missing Sounds** window appears (reopen from Windows > Show Missing Sounds Window). Buttons: Download ReFill/R.E., Search Folder, Search Locations, Replace. Missing sounds show with an asterisk (*) on the panel. Ignoring them gives silent pads/zones/loops.

## 8. Rack Extensions (REs)
- Extra devices (instruments, effects, utilities, from Reason Studios and third parties). Behave like built-in devices: cables, CV, Combinator-able, automatable, remotable.
- Try = 30-day full trial, once per device. After it ends the RE disappears from menus but stays installed.
- **Reason 12.7+: install and manage in the Reason Companion app** (Authorizer is deprecated). In Reason: Window > Rack Extensions opens it. Devices tab: Filter box, Update all, Install all, per-device Install/Update/Uninstall. Reason+ REs are listed at the top, your purchases under "My Rack Extensions".
- Using a licensed RE needs the authorized computer or an internet connection. Not available in Demo Mode.
- They appear in the Create menu and Browser palettes, Reason Studios devices first, then by maker A-Z. "Show/hide RE" button hides third-party ones.
- RE patches: Browser > Locations > "Rack Extensions" > open the device folder. Or press the device's folder button. Files are .repatch.
- **Missing RE** (friend's song, expired trial): alert on open, then a silent "Missing Device" placeholder (effects bypass, sends go silent). Safe to save and send back; settings come back intact when the RE is there. "View in web shop" on the placeholder, restart Reason after installing.

## 9. VST plugins (Reason standalone)
| Fact | Detail |
|---|---|
| Versions | 64-bit VST3 and VST2 (2.4), Windows and Mac, from Reason 12.5 |
| **Reason Rack Plugin** | **VSTs are NOT supported there.** Standalone Reason only |
| Limits | Multitimbral VSTs only get MIDI channel 1. VSTs that output MIDI are not supported |
| Install | Use the plugin's own installer. Reason scans at every launch (restart after installing) |
| Mac scan folders | Library/Audio/Plug-ins/VST and ~/Library/Audio/Plug-ins/VST (VST2); Library/Audio/Plug-Ins/VST3 (as the manual spells them) |
| Custom folders | Preferences > Folders tab: tick boxes, Add (folder must already exist), Remove; restart |
| Licensing | Done by each plugin maker, not Reason's authorizer |
| Where they show | Browser Instruments / Effects palettes (analysis plugins in Utilities). Gold **VST3** label, blue **VST2** label, REs have none. Show/hide buttons plus a Duplicates toggle |

- A VST lives in a **Plugin Rack Device** (container, like a Combinator): audio ins/outs, 8 CV modulation inputs, CV Programmer, sidechain on effects (inputs 3-4). Instruments get a Mix Channel and track automatically; effects don't.
- Click **Open** (or the image) to get the **Plugin Window**: floating, several at once. Top icons: **Keep open**, **Automate**, **Remote**, **Screenshot** (camera: replaces a generic panel image in the Browser and device).
- Effect Off/Bypass does NOT stop the VST using CPU. The device **On/Off button** (far right) disables it and cuts the load.
- Auto-routing: stereo instrument = Out 1/2 to Mix Channel L/R; mono = Out 1 to L. Mono-in/mono-out effect in a stereo path only connects left; a stereo effect in a mono path becomes mono-in/stereo-out.
- Shift-fine-tune and Cmd-reset on knobs usually do NOT work in VST windows (maker-defined). An on-screen keyboard in a VST can audition but cannot record to the sequencer.
- Presets: VST3 .vstpreset through the Browse Patch button; VST2 programs from the patch-name list or the Prog up/down buttons (shown only when programs are loaded). Song save embeds all VST data, so no separate preset save needed.
- Automate: arm parameter automation and move knobs while recording; or click **Automate** then the parameter; or the Track Parameter Automation popup; some VSTs offer right-click > Automate.
- CV modulation: each of 8 slots has a CV input, bipolar Amount (-100 to 100), a destination parameter and a Base Value. Quick way: flip rack (Tab), cable a CV source to CV In 1, flip back, click **Learn**, click the VST parameter.
- Remote: **Remote** button > click the parameter > "Learn from control surface input" > turn a knob > OK. Clear via the same button.
- Can go into a Combinator (all VST parameters listed in the Combi Programmer).
- **Missing VST**: empty Plugin Rack Device, silent (effects bypass). Safe to save and return.
- **Window > Manage Plugins**: list with Manufacturer, Name, Type, Device Type, Status. Enable/Disable button. Status: Enabled, Disabled, **Could not load**, **Crashed** (auto-disabled after a crash/hang; enable to retry at next restart). Use it to switch off a plugin that crashes Reason.
- Windows only: tick "Auto-scale" in Manage Plugins if panels look tiny, then reload the plugin.
- Rack Extensions in the Rack Plugin: not covered in these chapters **[Guess: check Reason Studios docs before promising]**.

=====================================================
SOURCE FILE: players.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/players.md
=====================================================

# Players: chords and arpeggios from single notes (digest of Reason 12.7 manual, ch. 12)

Source: `~/.reason_voice/reason12_manual/full_chapters/12-working-with-players.txt` (manual pp. 343-372). Digested 2026-09-30.
Tag: all **Manual**. Nothing tried or heard. Overlap check: your notes have 0 files on Scales & Chords or Note Echo; Dual Arpeggio appears only inside song notes. Index: [README](README.md)

## What a Player is
A device that sits above an Instrument in the rack and turns the MIDI going in into different MIDI going out (chords, arpeggios, echoes, drum patterns).
It cannot exist alone; creating one with no instrument makes an ID8. Works with any instrument (built-in, Rack Extension, VST).

## Create / order / manage
- Rack: drag from the Players palette (under Utilities in the Browser) above an Instrument; or select the instrument and double-click the Player; or right-click the instrument > Create > Players.
- **Chained Players run top to bottom.** Reorder by dragging. Rename, replace and delete like any device. Players can live inside Combinators, or attach to a Combinator from outside.

## Common buttons (top of the Player stack)
| Button | Does |
|---|---|
| **Fold** | Folds all Players on that instrument |
| **Bypass All** | Sends your keyboard straight to the instrument |
| **Direct Record** | Records the notes the Players MAKE (chords, arps) instead of the notes you play. On playback they bypass the Players, so it sounds the same as when you recorded |
| **Send to Track** | Renders the Player output of the notes already in the clip into a NEW clip on a new lane. Originals between the locators are muted and cut. Bypass All turns on |
Default recording (Direct Record off): you record your own notes and the Player processes them live on playback.

## The Players in this chapter
### Scales & Chords
- **Scales section:** Key (12) and Scale. Presets: Major, Minor, Lydian, Mixolydian, Spanish, Dorian, Phrygian, Harmonic Minor, Melodic Minor, Major Pentatonic, Minor Pentatonic, Hemi Pentatonic, Chromatic, plus **Custom** (click the keys; saved with the song and the patch). Key and scale can be automated.
- **Filter Notes** off (default): wrong notes are moved to the nearest scale note (the lower one if tied). On: wrong notes go silent.
- **Chords** on: one note makes a chord in the scale. **Notes** knob = 1 to 5 notes. Playing several notes makes several chords (shared notes play once).
- **Inversion** knob (only useful below the Notes value), **Open Chords** (spreads notes by octaves), **Add Oct Up / Oct Down / Color** (Color adds the 9th for 3 notes, 11th for 4, 13th for 5; all three can be on), **Alter** (momentary: turns one chord note so a major goes minor or the reverse).
- Use it to write single notes in a clip and let the Player build the chords.
### Note Echo (a MIDI delay)
- **Step Length** 0 to 1000 ms (synced: 1/128 up to 1/2). **Step Length 0 = all repeats at once = chords.**
- **Repeats** 1 to 16, **Velocity** 10% to 200% per step, **Pitch** -12 to +12 semitones per step. Click the green circles in the display to mute repeats (also the dry first note).
- Too many repeats with a big Pitch value can leave the instrument's range: the rest go silent.
- Comes with ready-made chord patches: Browse Patch > **Chords** folder.
### Dual Arpeggio
- Two identical arpeggiator sections with Rate, Octave, Direction, Steps, Pattern, Velocity and Gate Length. (Details in the chapter, manual pp. 350-360; the shuffle comes from ReGroove Global Shuffle.) The CV inputs can take a Pulsar for random or long patterns.
### Beat Map (Rack Extension)
- A Player that makes drum patterns from built-in beats and algorithms; made for Kong, Rytmik or Umpf. **Not checked whether you own it.**

## Recipes from the manual (Tips & Tricks)
1. **Scale-correct arpeggio from one note:** instrument > Scales & Chords first > Dual Arpeggio second. Key and Scale set, Chords on, Notes = 4. Play single notes.
2. **Arpeggiated chords:** instrument > Dual Arpeggio first > Scales & Chords second. Chords on, Notes = 3. Play chords.
3. **Parallel chords (same shape on every note, like a minor 9th):** Note Echo: Step Length 0, Repeats max, Pitch +1, then click off the repeats you don't want. Play single notes. Add a Dual Arpeggio after it for arps.
4. **See what the chain is playing:** put a Scales & Chords LAST, Scale = Chromatic, Filter Notes and Chords off. The keyboard display shows the notes.

## Ideas for us (not built)
- Skill idea **reason-players**. Phrases: "make that a four-note chord", "arp it", "put it in D minor".
- Pairs with the chord work in the Beat Machine (`CLAUDE.md`: MIDI chord packs, chord sources). Whether Reason Players could audition chord progressions from the Beat Machine MIDI was NOT checked.

=====================================================
SOURCE FILE: rack.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/rack.md
=====================================================

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

=====================================================
SOURCE FILE: remote-control.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/remote-control.md
=====================================================

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

=====================================================
SOURCE FILE: sampling.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/sampling.md
=====================================================

# Sampling in Reason (digest of Reason 12.7 manual, ch. 21)

Source: `~/.reason_voice/reason12_manual/full_chapters/21-sampling.txt` (manual pp. 541-566). Digested 2026-09-30.
Tag: all **Manual**. Nothing here was tried or heard. Index: [README](README.md)
Overlap check: your recipes and device guides do not have these steps (only passing mentions in demo-song notes). `recipes/hiphop/lofi-sample-chop.md`
does not use the Sample button or Edit Sample window.

## The big idea
Any of **NN-XT, NN-19, Redrum, Kong, Europa, Grain, Mimic, RV7000 Mk II** has a **Sample button**. Click it (or click and HOLD it) and Reason records
whatever is arriving at the Hardware Interface's **Sampling Inputs**. That can be a mic, OR **the output of any device in the rack**. That second
one is resampling: play a synth, sample it into a sampler, chop it.

## Step by step: sample something already in the rack (resample)
1. Go to the Hardware Interface at the top of the rack and press **Tab** to flip it to the back.
2. Cable the source device's audio out to the **Sampling Input L (and R for stereo)**. Only L or only R = mono.
3. Set the level: use the **Output Level on the source device** and watch the **Big Meter** set to the Sampling Inputs. Stay under 0 dB.
4. Click the **Sample button** on the target device. (In Redrum, use the Sample button of the drum channel you want.) Click once and stop it
   with **Stop Sampling**, or hold it and release to stop.
5. Play the source. The waveform draws as audio arrives. Leading silence is skipped automatically.
6. The sample lands in the device, named "Sample n", and in the Browser under **Song Samples > Assigned Samples**.

## Step by step: sample a mic or instrument
Same, but in step 2 cable an **Audio Input** of the Hardware Interface (set under Preferences > Audio) to the Sampling Input. Adjust level on the
pre-amp or instrument. Monitor buttons: **Monitor** (always hear the input), **Auto** (hear it only while sampling); the Monitor knob changes
only what you hear, not what is recorded.

## Hard numbers
| Fact | Value |
|---|---|
| Sample file format | WAV |
| Bit depth | Fixed at **16-bit** |
| Sample rate | Whatever Preferences > Audio is set to. Changing it later does not change pitch or speed |
| Buffer length | **30 seconds**. After that the play head loops and starts erasing the start. **Restart Sampling** erases and starts over (not available with click-and-hold) |

## Edit Sample window (select a sample in Song Samples > Edit, or Option-click a device's Sample button)
Undo/redo (10 steps here only), **Crop**, **Normalize** (to 0 dB; boosts noise too; works on the whole sample or a highlighted part), **Reverse**,
**Fade In/Out** (highlight a zone, click the button), **Loop mode** (none, Loop Forward, Forward + Backward), **Crossfade Loop** (smooths clicks at the loop
point; makes the loop locators snap to good spots), **Set Start/End**, **Set Loop**, **Snap Start/End To Transients**, **Root Key** (set the real note
so a sampler transposes it correctly), **Name**, **Save** or **Cancel**.
- Loop tips from the manual: loop where volume and tone stay steady; very short loops sound static; try Forward + Backward if Forward clicks.
- Saving an edit to a ReFill/Factory sample saves a copy, with the same name, in All Self-contained Samples.
- Renaming only changes the name; it does not make a copy.

## The Song Samples location in the Browser
| Folder | Holds |
|---|---|
| **Assigned Samples** | Samples loaded in devices, one sub-folder per device |
| **Unassigned Samples** | Samples you removed from a device (still in the song; can be loaded again) |
| **All Self-contained Samples** | Everything you recorded or duplicated. Stored INSIDE the song file when you save, so no loose files to track |
Buttons: Edit, **Import** (sends the sample to an audio track in the sequencer), Play, Auto, Volume. Right-click: Edit, Duplicate, Export, Delete.

## Rules to remember
- **Duplicate** a Factory/ReFill sample to edit it. The copy can live only inside the song; it **cannot be exported** to disk. Factory/ReFill originals cannot be exported or deleted.
- **Export** (own samples only) gives WAV or AIFF and three choices: crop and render loop crossfades, crop, or **raw** (no start/end markers, crossfade removed, so it
  can sound different elsewhere).
- Deleting a sample you recorded erases it for good unless you exported it first.
- Load a sample into a device: **Browse Sample** button on the device > Song Samples > pick > Load (or double-click).

## Ideas for us (not built)
- Skill idea **reason-sampling**: resample a device into NN-XT/Kong/Redrum, set Root Key, loop, save. Pairs with `device_refs/nn-xt.md`, `kong.md`, `redrum.md`, `mimic.md`.
- Our Beat Machine makes WAVs outside Reason. Importing them is a different path (File > Import Audio, ch. 20), not sampling.

=== END OF PART ===
