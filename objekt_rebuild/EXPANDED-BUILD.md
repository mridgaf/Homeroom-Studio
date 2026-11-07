# Expanded VST build — 2026-11-06

Built artifact: `artifacts/expanded-2026-11-06/Objekt Rebuild.vst3`.

232 host parameters, 16 voices, per-stage resonator controls, fractional delays, noise envelope/modes, pickup approximation, external excitation, mono/legato/glide, MIDI performance controls, two LFOs, curve/macros/eight modulation buses, and reorderable effects. This pass also separates impact pulse frequency from hardness and exposes velocity-sensitive hardness. Existing parameter IDs retained; older states fill missing controls with defaults.

Validation: full CMake build; five assertion-enabled CTest suites passed (engine, processor, modulation, effects, offline tuner); packaged bundle ad-hoc signature verified. No new pluginval or DAW listening validation. Not installed over the previous plugin.

The tuner is an offline tested utility, not an editor feature. Generic editor remains. Exact audio parity remains unmeasured; user owns Reason 12 without Objekt. See vst3/REMAINING-GAPS.md for engine limitations. Factory presets/templates and proprietary nonlinearities are not reproduced.
