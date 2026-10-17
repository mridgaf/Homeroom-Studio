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
