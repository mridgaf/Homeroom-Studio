# Handoff: "does not cut a marked beat twice" fails (2026-11-02)

## What fails
`tests/test_base_clean.py::test_sound_engine_does_not_cut_a_marked_beat_twice`

```
assert (not False and 1.3144557393779726 < 0.6)
```

## What it checks
A probe beat whose hat stem is a pure **20 Hz** tone is loaded into the Sound Engine
(`/api/project/from-beat`).
- Beat **without** the clean marker: the Sound Engine's base layer should cut the rumble, so wet/dry RMS must be **under 0.6**.
- Beat **with** the marker (`base_clean.MARKER` in the stems folder): left alone, so the ratio is over 0.9.

## What happens
On the unmarked beat, wet/dry = **1.31**. The 20 Hz is not cut. It comes out ~2.4 dB **louder**.
The failure is on the first assert, so the marker half never runs.

## Known
- Not caused by the 2026-11-01 changes (instrument solo audition, conftest Sound Engine temp folders).
  It fails the same way with the old `tests/conftest.py` and the sandbox off.
- Not a sandbox/permission error.

## Where to look
- `sound_engine/server.py`: `from-beat` loading, `pre_clean` flag, how `wet` is built for a channel.
- The base layer ("cuts rumble and centres bass on load"), plus `tools/base_clean.py`.
- Likely suspects: the low cut is off by default (see `index.pre-base-off-2026-10-31.html`, the base layer was switched off 2026-10-31?),
  or the wet chain gains up (level match / trim) without the high-pass running.
- Check `git log -p sound_engine/ tools/base_clean.py` since 2026-10-18 for the change that stopped the cut.

## First step
Decide which is true: (a) base layer off by design → update the test to match, or (b) the cut should still happen → fix the chain.
Ask the owner which before changing anything.
