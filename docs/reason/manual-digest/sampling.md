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
