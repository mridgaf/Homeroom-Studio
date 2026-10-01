# Export, song files, and performance (CPU / crackle)
Source: Reason 12.7 Operation Manual, ch. 19 (Song File Handling), ch. 20 (Importing and Exporting Audio), ch. 25 (Optimizing Performance). Whole chapters read. Tag: **Manual** unless marked **[Guess]**.
Recording to audio and Rec Source: see `recording.md`. Bounce/stem via Master Section: `recording.md` section 5. Mixer routing: `routing-and-main-mixer.md`. Plugin delay problems: `delay-compensation.md`.

## 1. Export the mix (File menu)
| Command | What it saves | Range |
|---|---|---|
| **Export Song as Audio File...** | Mix of all active tracks | Song start to the End Position Marker |
| **Export Loop as Audio File...** | Same mix | Left Locator to Right Locator |
- Steps: set End Marker (or locators) > pick command > choose folder, name, format (**AIFF, WAV or MP3**) > Save > pick Sample Rate, Bit Depth, Dither in "Export Audio Settings" > OK.
- The file comes from **Outputs 1 and 2 of the Hardware Interface only**. Anything on other outputs is left out.
- Put the End Marker / Right Locator late enough for reverb and tails to die away, or the file ends with a hard cut.
- Tempo (and tempo automation) is written INTO the file. Import it into another Reason song and it stretches to that song's tempo.
- If high-quality stretching is still running (CALC light on the Transport), export waits and shows a progress bar.

## 2. The three settings in "Export Audio Settings"
| Setting | What it is FOR |
|---|---|
| Sample Rate | Speed of the file. The manual does not list the choices **[Guess: the usual 44.1/48/96 kHz; check the dialog]** |
| Bit Depth | Resolution. 16-bit is the lowest the manual mentions. Higher keeps more detail for later mastering **[Guess]** |
| Dither | Tick it when exporting at **16-bit**. Adds a tiny noise so quiet sounds stay clean when dropping from high resolution. Reason's dither has noise shaping. Only offered at 16-bit |
- MP3 settings (bit rate etc.) are not described in these chapters.
- No "normalize" box in Export Song/Loop. Normalize exists in Bounce Mixer Channels (below) and, for single audio clips, as Edit › Normalize Clips (see `audio-editing.md`).

## 3. Stems: Bounce Mixer Channels (File > Bounce Mixer Channels...)
Records each ticked channel on its own, then saves files or puts them on new tracks.
| Option | Choices and meaning |
|---|---|
| Mixer Channels list | Tick channels. Master Section and the 8 FX Returns are never pre-ticked. Tick FX Returns to bounce reverbs/delays on their own. Check All / Uncheck All buttons |
| Apply Mixer Settings: **All** | Insert FX, level, pan. Mono channels come out as stereo |
| Apply Mixer Settings: **All except fader section** | Insert FX and EQ/dynamics kept; level, pan, width, mute NOT applied. Mono stays mono. Master: keeps master compressor, not the fader |
| Apply Mixer Settings: **None** | Raw device sound, before the channel strip |
| **Normalize** | Scales each file so its loudest peak is 0 dB. Useful before using stems elsewhere |
| Range to Bounce | **Song** (to End Marker) or **Loop** (locators) |
| Bounce to: **Audio Files on Disk** | One file per channel in a new folder "Bounced <song name>". Pick File Type, Sample Rate, Bit Depth, Dither |
| Bounce to: **New Tracks in Song** | New Audio Tracks, named "<channel> (Bounced)". Always song sample rate, 32-bit float. File format boxes are greyed out |
| Mute Original Channels | Only with New Tracks. Mutes the sources after. Does NOT touch Master or FX Returns |
| Copy original channel settings | With "None" + New Tracks: copies the old strip settings to the new tracks |
| Export Tempo Track (.MID) | Only with Audio Files on Disk + Song range. Saves tempo/tempo automation as a .MID named after the song |
- Same-name channels get "-01" etc. added to the file name.
- Stems carry tempo data too, so they re-import in time.
- Recipe, "all stems for a mastering friend" **[Guess assembled from the above]**: tick all channels + Master > Apply "All" > Normalize OFF if you want to keep true levels > Song > Audio Files on Disk > WAV.

## 4. Other bounces (Edit menu, one clip selected)
| Command | Result |
|---|---|
| **Bounce Clip to Disk...** | One audio clip to AIFF/WAV. After clip level and fades, WITHOUT mixer settings |
| Bounce Clip to New Sample | Song Sample you can load into a sampler (see `sampling.md`) |
| Bounce Clip to New Recording | New Comp Row at top of the clip. Non-destructive "flatten". Ignores clip level and fades |
| Bounce Clip to REX Loop | Only on a Single Take clip open for inline edit. Makes a REX loop for Dr. Octo Rex |
- "Bounce in Place" also exists (per-clip to a new track); the details are in the audio-editing chapter, see `audio-editing.md`.

## 5. Importing audio
- **File > Import Audio File...** (Cmd+Option+I on Mac). Several files at once = one new track each, in the order selected.
- Or drag from the Browser to the track list (new tracks) or onto an audio track (clips one after another, respects Snap).
- Formats, sample rates and bit depths can be mixed freely. Reason converts quietly.
- Different sample rate from your interface: instant low-quality version plays first, high-quality one is built in the background (CALC light), then it swaps in.
- Files with tempo data auto-stretch to the song tempo. Unknown tempo: use the Scale Tempo tool/Tool Window.
- **REX files become plain audio on import** (slice info lost). To keep slices, load into Dr. Octo Rex instead.
- With an audio clip open in the Comp Editor, import adds new Comp Rows named "<file> (Imported)".
- Save the song BEFORE importing many or large files (saves faster later).
- **File > Import MIDI File...** into an empty song: one ID8 per track, Type 1 = a track per MIDI track, Type 0 = a track per channel, tempo and controllers come along.
- **File > Export MIDI File...**: Type 1, all on channel 1, up to End Marker. Notes and controllers only, no sounds.

## 6. Saving and song files (ch. 19)
| Do | Menu | Notes |
|---|---|---|
| Save | Cmd+S | Settings are saved in the song, not as links to patches |
| Save As | Cmd+Shift+S | Also optimizes the file |
| **Save and Optimize** | File menu | Removes empty gaps left by deleted takes (shrinks file). Slow with lots of audio. Manual: Save while working, Optimize as the last step |
| Song Self-Contain Settings... | File menu | Tick samples/REX files to pack INTO the song for another computer. ReFill samples can be packed but not unpacked. Packed samples are compressed about 50% (lossless) |
| New from Template | File menu | Factory templates; add your own by putting songs in the Template Songs folder (File > New from Template > Show Template Folder) |
| Default Song | Preferences > General > Default Song > "Template" + folder icon | Every File > New opens that song. Untick "Load last song on startup" or that wins |
| Song Information... | File menu | Window-title text, notes, 256x256 JPEG splash, links |
- Scratch Disk: unsaved audio and analysis data live there until you save. Change in Preferences > Folders > Scratch Disk Folder > Change (restart the computer).
- Power cut mid-recording: reopen the song; "orphan audio streams" alert offers to recover the audio onto a new track. Only audio comes back, not new instrument tracks in unsaved songs.
- Song size: around 1 GB for a recording-heavy song is normal. Keep 20 GB or more free.
- Alternative to self-contain: bounce channels to audio so the song sounds the same anywhere.

## 7. Crackles, clicks, dropouts: fix in this order
1. Watch the **DSP meter** (Transport). Near full = breakup is coming.
2. **Options > Show CPU Load for Devices**: % on each device's top right corner. Mix Channels show the sum of the chain. Find the hog.
3. **Preferences > Audio > Buffer Size** slider: raise it a notch at a time while the song plays. Big gain from 64-256; little above 1024.
4. Lower the **sample rate** in Preferences > Audio (quick rescue, per the manual).
5. Preferences: **Max audio threads** (Default = physical cores; on Apple M1 = performance cores). If it stutters, step down one at a time from the top. Fewer threads leaves room for other apps.
6. Tick **"Render audio using audio card buffer size setting"** for best plug-in speed (heavy VSTs). Unticked = fixed 64-sample chunks like Reason 10.2, only wanted for tight feedback/CV loops. Old songs with feedback routing may sound different.
7. Quit other apps and background tasks. Keep only ONE song open.
8. **Bounce heavy instrument tracks to audio** (section 3, New Tracks) then delete the instrument. This is the manual's version of "freeze". There is no separate Freeze command in these chapters.

Latency tradeoff: smaller buffer = snappier playing but more strain. Set low to record, higher to mix **[Guess on workflow; manual only says raise it when clicks appear]**.

## 8. Cheap-CPU habits (manual list, trimmed)
- One reverb on a Send FX bus instead of many inserts. **RV-7 is far lighter than RV7000**; RV-7 "Low Density" lighter still.
- Use mono where the source is mono (connect only Left). Mono samples also halve RAM.
- Switch OFF unused channel-strip parts (EQ, filters, dynamics, inserts, input gain) and delete unused Mix Channels/devices.
- One sampler playing many samples beats many samplers with one each.
- Turn off High Quality Interpolation unless you hear a difference.
- Unused filter (cutoff fully open) = disable it. 12 dB lowpass is lighter than 24 dB.
- Polyphony: set to the exact number of notes needed AND shorten release. Lowering polyphony alone does nothing. "Low BW" button saves CPU, often unheard on bass.
- Subtractor: skip Osc 2, Phase mode, Noise, Filter 2, FM when not needed. Malstrom: use Osc A only, one filter, no shaper if you can. Redrum: leave Tone on channels 1, 2, 9 at zero.
- D-11 Foldback is lighter than Scream 4.
- Out of RAM (samples): close other songs and apps, use mono samples, lower sample rates.

## 9. Recording latency compensation (ch. 25)
- Preferences > Audio > **Recording Latency Compensation**: only matters when NOT monitoring through Reason (External, or Manual with Monitor off). Reason shifts the take earlier by input+output latency.
- Never needed with Monitoring = Automatic.
- Takes land early: enter a negative value. Late: positive.
- If monitoring through Reason, the singer is expected to play slightly ahead; no compensation.
