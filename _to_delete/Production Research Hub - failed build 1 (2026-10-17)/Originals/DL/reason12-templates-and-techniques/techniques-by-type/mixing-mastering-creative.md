# Mixing & Mastering — Unique & Surprising Techniques

## Sidechain Tool's three distinct modes — most producers only use one [Sourced]
Reason's dedicated Sidechain Tool device is built around three genuinely different behaviors, and it's easy to only ever touch the first one:
- **Auto Pump**: quick classic four-on-the-floor ducking, curve adjustable to fit your kick, rate adjustable for other rhythmic effects (including half-speed).
- **Band Mode**: ducks only a selected low or high frequency band rather than the full signal — useful when you want the pump feel without also thinning out unrelated frequency content.
- **Trigger mode**: the curve is triggered by *any* audio signal, MIDI note, or CV — not necessarily the actual kick drum you're ducking against. This is what makes the "ghost kick" and "unconventional trigger source" techniques below possible. [Source: Reason Studios, Sidechain Tool product page]

## The "ghost kick" trigger [Sourced — technique name only, video not transcribed]
A dedicated YouTube walkthrough on sidechaining in Reason includes a chapter specifically on creating a **silent, CV-only "ghost" kick drum** purely to drive sidechain ducking — i.e., a kick pattern that never makes sound itself, existing only to trigger the pump/duck effect on other elements. Useful when the audible kick pattern and the ducking rhythm you actually want don't match (e.g. a sparse audible kick but a denser ducking pulse for groove). The same video's chapter list also references **using Pulsar's own waveform to trigger sidechain compression** — i.e., an LFO device's output pattern (not a drum hit at all) driving the ducking rhythm, for a pump that isn't tied to any drum hit whatsoever. Both are named/scoped from the video's chapter markers, not independently verified by a full transcript — worth testing rather than assuming exact settings. [Source: YouTube, "How to Sidechain in Reason 10 Complete Guide"]

## Serial (not single-stage) compression as a general mixing principle [Sourced — detailed in pop-vocal.md]
The Yana Mahal vocal chain technique (full detail in `templates-by-genre/pop-vocal.md`) generalizes past vocals: two compressors each doing light work (2:1 ratio, ~2 dB reduction each) reads as more natural and more "glued" than one compressor doing the equivalent total reduction in a single stage. Worth trying on any bus that's sounding "squashed" under a single heavier compressor — split the same total gain reduction across two lighter stages instead of reaching for a gentler ratio on one.

## Width without smear: offset stereo delay instead of a stereo widener [Sourced]
Also from the vocal chain research, but a general mixing principle: rather than reaching for a dedicated stereo-widener plugin/device, sending a signal to **Ripley (Space Delay) on an Aux Send** and using its **Offset** knob to create a timing difference between left and right channels produces stereo spread described as beyond what "a standard delay can't touch" — while keeping the dry signal itself centered and upfront (because it's a send, not an insert). Applicable to any mono source that needs width without losing center focus — not just vocals.

## The DJ-style dual-range filter knob (cross-reference) [Sourced]
Full build in `combinator-workflow.md`: using Combinator 2's **Source Range** macro feature to make one rotary control low-pass frequency on one half of its travel and high-pass frequency on the other half (with a dead zone at center) — built from nothing but the stock Channel EQ. Filed here as a mixing/mastering-adjacent technique because it's genuinely useful as a creative transition tool (drops, breakdowns, DJ-style build-ups) beyond its original sound-design framing.

## Sources
- Reason Studios, "Sidechain Tool" product page — https://www.reasonstudios.com/devices/sidechain-tool
- YouTube, "How to Sidechain in Reason 10 Complete Guide" — https://www.youtube.com/watch?v=9_LlSd3xCW4
- Reason Studios, "How to Build a Vocal Chain in Reason 13" (serial compression, Ripley Offset) — https://www.reasonstudios.com/news/post/build-an-epic-vocal-chain-in-reason-13
