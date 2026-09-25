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

## Still open

1. Why the bridge's Record button did nothing. The knobs work and the
   transport does not. Check the transport scope in `remote/ReasonVoice.remotemap`.
2. Only Scream 4 Damage Control was tested. Any knob the bridge maps should
   behave the same way, but that is not proven.
3. Sound was not checked. This test proved the lane exists, not how it sounds.

## Files
- `test_bass_Am_90bpm.mid`: 4-bar A-minor bass, 90 BPM, plus a CC74 ramp
- `sweep_test.py`: sweeps Knob 1 up and down over about 10 seconds. With `NO_TRANSPORT=1`, it only moves the knob
- `Run Sweep Test.command`: sweep plus the bridge's record/stop (the transport part did not work)
- `Run Sweep Only.command`: sweep only (this is the one that worked)
- `automation test 09 25 26.reason`: the proof song
