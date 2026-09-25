# Automation recording test — 2026-09-25 (run overnight by Claude)

## Answer: YES. The bridge can write automation lanes, including on effects.

Open `automation test 09 25 26.reason` in this folder. The **EasyFuzz** track
(the Scream 4) has a **Damage Control** automation lane. Its shape rises, then
falls: the exact sweep the script sent. Nobody touched a knob.

## What was tested, step by step

| Step | Result |
|---|---|
| Import `test_bass_Am_90bpm.mid` (File > Import MIDI File) | Worked. One track, an ID8 on it, tempo set to 90 |
| CC74 ramp inside that MIDI file | Came in as a "Controller #74" lane, but as an **alien clip** (striped). The ID8 has no control for CC74, so it does nothing. The manual warns about exactly this |
| Add Scream 4 after the bass (Create > Effects) | Worked. It dropped in wired after the ID8 |
| Lock Scream 4 to ReasonVoice | Worked (right-click panel > "Lock ReasonVoice ReasonVoice 2 to This Device") |
| Script taps Record over the bridge | **Did NOT start recording.** The knob moved, but the transport did not. The Record/Stop buttons in the bridge are unproven |
| Record from Reason's own record button, script moves the knob, Scream 4 has NO track | Knob moved, **nothing recorded** |
| Same, after right-click > "Create Track for EasyFuzz" | **Automation lane recorded.** Success |

## The rule this proves

An effect only records automation if it has its own sequencer track.
Right-click the effect > **Create Track for [name]** first. After that,
anything the bridge moves on a locked device lands as an automation lane.

## Night 2 (same date): Record button fixed

| Step | Result |
|---|---|
| Bridge Play, before fix | Did nothing. So ALL bridge buttons were dead, not just Record |
| Cause | The codec read each button as two fixed lines (`7f` press / `00` release). Reason accepted the file but ignored them |
| Fix | One line per button, the way Reason's own Launchkey codec does it (`b? 16 xx`). Installed, Reason restarted |
| Bridge Play, after fix | Played (moved to bar 3) |
| Bridge Stop x2 | Stopped and went back to bar 1 |
| Bridge Record + sweep of 3 more Scream 4 knobs | 3 new lanes: Parameter 1, Cut Lo, Body Resonance, one after another |

Your unsaved "untitled 4" was saved as a copy before the restart:
`untitled 4 - safety copy before restart 09 25 26.reason` (this folder).

Then RV7000 (Decay, HF Damp, Dry/Wet) and MClass Compressor (Threshold, Ratio,
Attack): all 6 lanes recorded. Each effect needed Create Track + Lock first.

Kong (instrument): Drum 1 Level recorded. Drum 1 Pitch Offset and Decay Offset
did NOT record, tried twice. Cause unknown.

Redrum: Drum 1 Level, Pitch, Length, Pan — all 4 recorded.
Dr. REX: Filter Freq, Filter Res, Loop Level — all 3 recorded.

## FOR YOUR REVIEW (knobs that did not make a lane)
| Device | Knob | Tries | What happened |
|---|---|---|---|
| Kong | Drum 1 Pitch Offset | 2 | Reason reported a value, no lane |
| Kong | Drum 1 Decay Offset | 1 | Reason reported a value, no lane |

Still open: sound not checked.

## Files
- `test_bass_Am_90bpm.mid`: 4-bar A-minor bass, 90 BPM, plus a CC74 ramp
- `sweep_test.py`: sweeps Knob 1 up and down over about 10 seconds. With `NO_TRANSPORT=1`, it only moves the knob
- `Run Sweep Test.command`: sweep plus the bridge's record/stop (works since the night-2 fix)
- `multi_knob_test.py 3 5 12`: bridge Record, sweeps those knobs one after another, Stop
- `Run Sweep Only.command`: sweep only (this is the one that worked)
- `automation test 09 25 26.reason`: the proof song
