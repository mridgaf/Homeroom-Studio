# CV & Routing — Unique & Surprising Techniques

## Freezing/holding any CV value in place [Sourced — detailed]
Reason's CV system has no native "sample and hold a fader position" function. This technique builds one, using a vocoder as an unlikely CV-freeze utility.

**Core insight**: the BV512 Vocoder's Modulation input can be "held" (frozen mid-value) — something raw CV signals can't do on their own. So the trick converts CV → Audio → back to CV specifically to pass it through that hold-capable stage.

**The chain**: Fader CV output → **Thor** (converts CV to Audio internally; Thor's Modulation Bus Routing scales this conversion — a routing amount of **39** is the specific value cited as correctly scaling it) → **BV512 Vocoder**'s Modulation input → BV512 Band 1 output (now converted back to CV) → your actual destination (e.g. SubTractor's Amp or Pitch parameter). A toggle button, mapped through a Combinator, drives BV512's Hold function — while held, the CV value at that instant stays locked regardless of what the Fader does afterward.

**Practical use beyond a single fader**: the same chain freezes *any* CV signal at an arbitrary moment — e.g., freezing an LFO's value at whatever point it happened to be at when you hit the button, turning a moving modulation into a static one on demand.

**Refinement**: a community contributor (credited as "Eric Kloeckner" in the source) simplified the original two-Thor / two-toggle-button version down to 2 Thors and a single toggle button. **Multi-function fader**: using two parallel BV512 chains (each independently held via its own toggle) lets one physical Fader control two completely different destination parameters, switched by which toggle is active — effectively doubling your physical control surface without more hardware. [Source: reason101.net]

## Kong pads used as a CV/gate crossbar switch [Sourced — detailed]
This is really a Combinator-building technique that lives on CV routing — see `combinator-workflow.md` for the full macro-wiring context. The CV mechanism itself: Kong's per-pad **Gate Out CV** was cross-routed directly into a Mixer's **Level CV inputs**, so a pad hit gates that mixer channel's volume open *instantly* — no crossfade ramp, no audible click — because the audio path itself never stops, only the gate opens/closes. This is the mechanism that made an 8-way instant preset-switcher (built from 8 parallel Audiomatic Retro Transformer units) actually feel instant rather than crossfaded. [Source: reason101.net]

## Shelob (4×20 audio splitter RE) repurposed as a crossfader and a group-mute bank [Sourced]
- **Song-level crossfades**: a Combinator button flips Channel A off / Channel B on simultaneously, with a Combinator rotary mapped to Shelob's global 0–20 second **Fade** knob to set crossfade length — turns a plain splitter into a full fade-in/fade-out utility, suggested specifically for use on Master Outs or pre-dithering.
- **Grouped independent mute banks from one input**: feed a signal into Channel 1, enable **Stripe** (auto-broadcasts that signal to channels 2–4 with no extra cabling), then use each channel's own Pass-Through switch to toggle that channel's *entire output group* independently. The global Stripe switch can also kill/restore channels 2–4 all at once as a master group toggle. In the device developer's own words (quoted in the source): *"Put your input into Channel 1, and turn on Stripe... Now you can turn each Channel off/on either as a Channel group with its Pass Switch... and you can turn all Channels 2, 3 and 4 on and off simultaneously via the Stripe switch!"* [Source: reason101.net]

## Kong-as-keyboard's octave-shift CV fan-out [Sourced — cross-reference]
The full technique lives in `drums.md` (it's fundamentally a Kong/drum-controller idea), but the CV mechanism is worth knowing on its own: a Thor used purely as a 1-step "step transposer" converts a pad-hit into a transpose CV value, which is then fanned out to 13 separate NN-XT instruments' Oscillator Pitch CV inputs via three daisy-chained Spider CV Merger/Splitters. The general pattern — "one trigger becomes a transpose signal, fanned out via Spiders to many devices at once" — generalizes well beyond that specific 13-NN-XT build. [Source: reason101.net]

## Official CV/Gate documentation baseline [Sourced]
Reason's own operation manual frames CV/Gate routing plainly, as the foundation the tricks above all build on: connecting multiple outputs from instruments together, sidechaining, and using CV to modulate or control a parameter on one device *from* another device entirely. Worth reading if the above techniques feel unfamiliar — they're all extensions of this base capability, not exotic hacks requiring anything beyond stock Reason. [Source: Reason Studios operation manual]

## Sources
- reason101.net, "Creative Reason Projects" archive — http://www.reason101.net/category/creative-reason-projects/
- Reason Studios, "Routing Audio and CV" (Rack Plugin 12 Operation Manual) — https://docs.reasonstudios.com/rackplugin12/routing-audio-and-cv
