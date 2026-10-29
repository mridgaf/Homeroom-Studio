# Reconstruction Parity Ledger

Legend: **implemented**, **approximation**, **not implemented**, **requires reference unit**.

| Area | Status | Notes |
|---|---|---|
| Impact exciter | approximation | Level, velocity, pulse brightness, hardness, and diffusion-like taps work. Exact pulse model, separate Click, and Diffuse Shape/Time curves are unknown. |
| Noise exciter | approximation | Color, Static, Random Pulse, Pulse, envelope, delay, rate, and color work. White/Noise Pulse/LP Noise are represented by nearby modes, not exact curves. |
| External stereo input | implemented | Mono/stereo arrays can excite each rendered voice. Reason key-mode behavior is outside the offline renderer. |
| Exciter parametric EQ | not implemented | Current prototype colors noise and applies global EQ only. |
| Modal 1-8 filters | approximation | Eight stable tuned resonators, ratios, gain, pan, decay, decay scaling, tuning, and key tracking work. |
| Modal Pickup | not implemented | Drive/Symmetry model is undocumented. |
| Object 1/2 delay arrays | approximation | Eight fractional feedback delays per object with ratios, gain, pan, decay, damping, dispersion, collision, pitch deformation, coupling, polarity, and routing. |
| Object Input Mix | implemented | Direct exciter and previous-stage amounts are independently configurable. |
| Trigger position | not implemented | Requires a topology hypothesis or reference measurements. |
| Coupling Off/On/X-Over | approximation | Continuous all-stage coupling is implemented. Exact Off/On/X-Over modes and crossover filter are not. |
| Three-band feedback damping | approximation | One-pole feedback damping is implemented; full low/mid/high/slope topology is not. |
| Mixer | approximation | Per-section level and pan work. Delay-line Width is represented by per-stage stereo pans. Exciter direct mix is not exposed. |
| EQ | approximation | Low/high shelves work; parametric mid is not exposed. |
| Distortion | approximation | Saturating waveshaper only; six proprietary modes are not cloned. |
| Compressor | approximation | Static stereo compression works; attack/release detector is simplified. |
| Delay | approximation | Ping-pong time/feedback/mix work; tempo sync and automation-tail semantics are absent. |
| Reverb | approximation | Algorithmic stereo comb reverb works; published types/controls are not matched. |
| Reorderable effects | not implemented | Fixed order: EQ -> distortion -> compressor -> delay -> reverb. |
| LFOs/Curve/Macros | not implemented | Configuration and per-sample modulation engine remain future work. |
| 8-bus modulation matrix | not implemented | Static patch parameters are available through Python/JSON. |
| Randomizer | implemented | Deterministic amount-limited randomization with safe ranges; section buttons are not in the CLI. |
| Polyphony | implemented | Real-time eight-voice MIDI engine plus offline overlapping event rendering. |
| Mono/Legato/Portamento | not implemented | Current VST3 uses standard retriggered polyphonic note handling. |
| Tuner Analyze/Fix | not implemented | Spectral analysis can be added, but matching Reason's multi-parameter Fix requires reference behavior. |
| VST3 | implemented | Native arm64 VST3, generic editor, 16 automatable parameters, four programs, state restore, zero reported latency; pluginval strictness 10 and REAPER host render passed. |
| Rack Extension/AU/AAX | not implemented | VST3 is the only packaged format in this build. |
| Factory patches/templates | intentionally not copied | Four original clean-room presets are included. |
| Exact parameter curves | requires reference unit | Manual ranges alone do not establish tapers or nonlinear mappings. |
| Exact audio parity | requires reference unit | Needs controlled sweeps and recordings from a licensed Objekt installation. |

## Completion definition for this batch

The **clean-room VST3 instrument** is complete for this phase when the DSP and processor tests pass, the installed bundle passes pluginval strictness 10 including editor, automation, state restoration, thread-safety, and parameter fuzzing, and a real host discovers, loads, saves, and renders the instrument. Exact product parity remains a separate phase requiring measurements from an installed licensed Objekt device.
