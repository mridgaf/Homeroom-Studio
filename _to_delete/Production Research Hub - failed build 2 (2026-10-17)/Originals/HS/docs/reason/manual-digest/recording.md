# Recording — audio (vocals), notes, automation
Source: Reason 12.7 Operation Manual, ch. 6 (whole chapter read, pp. ~140–174). Tag: **Manual**.
Mixer-side recording (Rec Source, sub-mix) is also in `routing-and-main-mixer.md` recipe I/J; the steps here are the fuller version.

## 1. Set up before you hit record
| Thing | What the manual says |
|---|---|
| Record Enable (red) | Audio: click it on the track. Any number of audio tracks at once. Instruments: only ONE note lane at a time (unless extra MIDI keyboards are locked to devices via Remote) |
| Record Enable Parameter Automation | Separate red button. Works on any number of tracks at once. Setting Master Keyboard Input to a track turns it on |
| Manual Rec (Track List) | Stops tracks auto-arming when selected. Use it when you move from recording audio to recording automation |
| Click (C) / Pre-count (Cmd+P) | 1–4 bars via Options. Manual tip: 3–4 bars for fast songs, 1–2 for slow. No pre-count with Ableton Link |
| Click Level | The click goes straight to the audio card, NOT through the mixer. A loud click can make the output meter clip |
| Save first | Manual: save the song before long or many audio recordings (shortens later save time) |

## 2. Input level (the vocal rule)
- Choose mono or stereo input + which interface input from the track's Audio Input drop-down.
- Aim for **about −12 dB** on the track Input Meter (first yellow LEDs) on a 24-bit interface. Raise a couple dB for 16-bit.
- Red clip LED stays lit until you click the meter. Never go past 0 dB.
- Set the level at the SOURCE (preamp / interface knob). The mixer channel strip does NOT change what is recorded.
- Recording Meter window (Windows menu › Show/Hide Recording Meter): big meter + tuner you can see from across the room.
- Built-in **Tuner** on the audio track (Enable Tuner button): for guitar, bass etc. The note must sustain a moment to be detected.
- Clip Safe is Balance-interface only (discontinued hardware). Skip.

## 3. Monitoring — the key vocal-chain fact
- The mixer channel (EQ, dynamics, insert FX, sends) is applied to what you HEAR, not to what is RECORDED to disk.
- So: you can monitor with compression and reverb on and still record the dry voice. Effects stay changeable later.
- Preferences › Audio › Monitoring: **Automatic** (armed = monitored, playback = not), **Manual** (you click Monitor), **External** (Reason never monitors; use the interface's direct monitor if latency is a problem).
- Latency too long? Monitor on the interface and set Reason to Manual/External.

## 4. Takes and comping
- **Loop-record**: set locators round the section, Loop on (L), go to left locator (the L button), Record. Each pass is stored as a **Comp Row** (Take). Earlier takes are silent but kept.
  - Last pass full length = Single Take clip (opens in Slice Edit; click Comp Edit). Stopped mid-clip = Comp Clip (opens in the Comp Editor).
  - Then pick best parts from each take. (Comp Editor steps are in `audio-editing.md`.)
- **Punch over an existing clip**: recording over it incorporates the old audio. Old = Take 1, new = Take 2 on Comp Rows, new part plays. Nothing erased. Fix a single line of a vocal this way.
- **Dub** (Transport button): new audio track copying the current track's settings INCLUDING channel strip and insert FX. Record stacked backing vocals/doubles, all play together.
- **New Alt**: same as Dub but MUTES the original. For alternative takes of the same part. Both work on the fly while recording.
- Lower the tempo to record a hard part. Audio stretches back to full tempo afterwards, pitch unchanged.

## 5. Record from inside Reason (resampling)
Steps in the manual for recording an instrument to audio:
1. Make the instrument track (so the keyboard plays it).
2. Make an audio track.
3. Press **Rec Source** on the instrument's Mix Channel in the rack.
4. On the audio track pick Stereo + that channel in the Select Audio Input list.
5. Select the INSTRUMENT track (Master Keyboard Input) and switch its Record Enable OFF.
6. Arm the AUDIO track only. Do NOT give it Master Keyboard Input.
7. Set level with the Mix Channel fader. Manual: instrument volume 0 dB + fader 0 dB is often best. Watch the audio track's Input Meter.
8. Record. Works for previously recorded note clips too.
- Same trick on an **Audio Track** device's Rec Source = re-record an audio track with its effects.
- **Output Bus** Rec Source = record a drum sub-mix.
- **Master Section** Rec Source + Solo the tracks you want + Stereo input = record a **stem** (e.g. 4 backing vocals panned and mixed to one track). Then un-solo and mute the originals so you don't hear them twice. You can ride faders live while recording.
- If you don't need live moves: **Bounce Mixer Channels** (see `audio-editing.md`/Song menu).

## 6. Notes
- Instrument track: arms itself and takes Master Keyboard Input. Clip edges snap to the nearest bar.
- Loop-record notes = each pass ADDS notes (layering a drum pattern).
- Delete/Backspace while recording a note clip = deletes it and starts a fresh one at the current position, still recording.
- Recording over a note clip adds notes. Starting before the clip and running into it makes a new clip that swallows the old one. Masked events inside the swallowed part are permanently deleted.
- Cleaner way to overdub: **Dub** (extra note lane, all play) or **New Alt** (extra lane, previous muted). With Loop on, Alt splits and mutes only the clip between locators.
- **Q Record** button quantizes as you play.
- Players can generate notes while you record (see `players.md`).

## 7. Automation recording
Two kinds:
| Kind | Where it lives | Use for |
|---|---|---|
| Performance controllers (pitch bend, mod wheel, sustain, aftertouch, breath, expression) | Inside the note clip, moves with it | Part of the performance |
| Track parameter automation | Own lane per parameter, own clips | Mixing and sound design (filter sweep, fade) |
- Optional middle path: Options › **Record Automation into Note Clip** records ANY instrument knob into the note clip (self-contained clip, less overview). Track automation wins if both exist for the same knob.
- Topmost note lane wins when two overlapping lanes automate the same controller.
- **Set the static value first** (the value the knob should have everywhere it isn't automated), then record the move. Clip ends → knob returns to the static value.
- Procedure: make sure the device has a track (Ctrl-click a knob › **Edit Parameter Automation** makes one for mix channels/effects) → arm Automation → Record → move knobs. One lane per knob appears. Master Keyboard Input is not needed.
- Click Stop again or the **Automation Override** light to show the green borders.
- Punch in: record again, and as soon as you move the knob the Override light comes on and new values replace old. Click Override to hand control back to the lane.
- Grab an automated knob during playback = Live mode override. Override light resets it.
- Mute one lane with its On button to hear the static value.
- Loop recording automation: each pass replaces the previous values.
- Spectrum EQ window moves can be recorded too.
- **Pattern automation** (Redrum, Matrix, Dr. Octo Rex): arm automation, pattern "Enable" on, set start pattern, record, change Bank/Pattern buttons slightly BEFORE the bar line (change lands on the next downbeat). No static value: where no pattern clip exists, the device is silent. Afterwards "Convert Pattern Track to Notes" or Copy Pattern to Track for editable notes.
- **Tempo automation**: Option-click the Tempo display (selects Transport track + creates lane), record while changing tempo. Audio clips stretch to follow unless Stretch is disabled for the clip.

## 8. Recipe: record a vocal (all from Manual rules)
1. Interface input → Audio Track, mono. Level at the preamp to about −12 dB peaks.
2. Monitoring Automatic (or interface direct if latency).
3. Put compressor/reverb on the channel strip for the singer's headphones. They are not recorded.
4. Click + 2-bar pre-count. Loop the chorus, sing 4–5 passes.
5. Comp the best lines. Fix single words by punching over that spot.
6. Backing vocals: **Dub** per layer, then a Master-Section stem if you need to free tracks.
