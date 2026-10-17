# Combinator & Workflow — Unique & Surprising Techniques

## The 8-way instant preset switcher [Sourced — detailed]
The most elaborate Combinator build documented in this research. What it does: lets you instantly switch between 8 different Audiomatic Retro Transformer presets — even automate or randomize the switching — with zero audible glitch, plus a clean dry/wet bypass so silence isn't the default state.

**Structure:**
1. A 14:2 Mixer with channels 1–8 faders held at 0 — volume on every channel is controlled *entirely* by CV, never the physical fader.
2. A **Directre Audio Router** splits the incoming audio into 8 identical parallel paths.
3. **8 separate Audiomatic Retro Transformer units**, each loaded with a different preset, all processing the same input simultaneously and continuously (this is what makes switching instant — nothing has to load or spin up, you're just choosing which already-processed signal to let through).
4. A **Kong** with its 16 pads relabeled per-preset, used purely as a trigger surface — not a drum machine here.
5. A dedicated "Sequencer" Thor (all synthesis disabled) used purely as a MIDI step sequencer — Run Mode set to Repeat/Random, gate length 100%, a front-panel Button wired via MBRS (`Button1: 100 > S.Trig`) to start/stop it — whose Note/Gate output drives Kong's pad triggers directly.
6. Kong's per-pad Gate Out CV cross-routes into the Mixer's Level CV inputs (with a deliberate offset — pads 1–4 → channels 5–8, pads 5–8 → channels 1–4) so each pad hit gates that channel's volume open instantly. (Full CV mechanism detail in `cv-routing.md`.)
7. **The bypass problem and its fix**: since audio only comes through when a pad is actively held/triggered, a second Thor ("Bypass Gate," all synthesis disabled) is used purely as an audio-through gate: MBRS lines `Audio In1: 100 > Audio Out1 : -100 > MIDI Gate` (and the mirrored line for channel 2). The **negative** MBRS amount on MIDI Gate is the key detail — it means unprocessed audio passes through *only when no gate is active*, and cuts the instant a gate fires. A Spider CV Merger taps the Sequencer Thor's own Gate/Velocity CV and feeds it into the Combinator's CV Input 1 (Unipolar), mapped in the Programmer to mute the bypass Line Mixer's channel exactly when a wet pad is active — preventing the dry signal from doubling up with the wet one.

Source's own framing of why this works: *"Since the audio is always going through all 8 Audiomatic devices, the switch from Pad to Pad is instantaneous... However, when no pad is pressed, you won't hear anything. So let's set up our Combinator so that if the Pads are not pressed, the original audio still passes through."* [Source: reason101.net]

**Why it's worth knowing even if you never build this exact patch**: the underlying pattern — run N parallel processing chains continuously, gate which one's audible via CV instead of switching/reloading — generalizes to any "instantly switchable" effect or instrument bank you want to build, at the cost of N times the CPU load of a single chain.

## Combinator 2's "Source Range" macro trick — a DJ-style performance filter from a plain EQ [Sourced]
Documented directly by Sound on Sound as a showcase of a genuinely new Reason 12 Combinator feature. Route audio through the stock **Channel EQ**, and use a single macro knob to control the cutoff frequency of *both* the low-pass and high-pass filter stages — but instead of one knob doing both at once across its whole travel, use **Source Range** to make the knob only adjust the low-pass frequency when turned anti-clockwise from center, and only the high-pass frequency when turned clockwise, with a neutral dead zone left in the middle to return easily to a clean signal. A companion button switches both filters on/off together. This is the same underlying mechanic as a Novation Circuit's hardware performance filter, built entirely from a stock EQ and macro mapping — no RE required. [Source: Sound on Sound, "Reason: Exploring The New Combinator"]

## Building instruments by combining and cross-fading, not layering [Sourced]
- **Key zone + velocity switching combined**: a single Combinator can hold a bass synth in the low register, a clean pad in the mid register, and a lead with velocity-sensitive filtering in the high register — three different instruments, three different behaviors, one MIDI track. [Source: Audeobox]
- **Parallel effects inside a Combinator**: a Spider Audio splitter inside the Combinator sends audio to multiple effects chains at once (e.g. one path through distortion, one through chorus), recombined via an internal mixer — richer than any single serial chain, and it saves/loads as one device. [Source: Audeobox]
- **Nesting**: Combinators can be nested inside Combinators for complex multi-layered instruments, but is explicitly flagged as hard to manage and CPU-heavy past about two levels deep — a real practical ceiling, not just theoretical. [Source: Audeobox]

## Reusing pieces of a rack without a formal Song Template [Sourced]
Song Templates are the obvious tool, but Reason has a second, less-used path for reusing *parts* of a project rather than a whole starting rack:
- **Combine + Edit → Combine** packages a selected group of devices into a single portable Combinator patch file — the standard way to save an effects chain, a modular sound construction, or an instrument combination for reuse elsewhere. But Combinators specifically **cannot** include mixer channels — they're device-only.
- For mixer channels and their associated sequencer tracks, the actual mechanism is **Copy Devices and Tracks / Copy Channels and Tracks** (the Edit menu's actual command names, not just "Copy") — Reason allows multiple Song files open simultaneously, so you literally copy a chunk of one project's mixer+rack+tracks and paste it into another open project. This is how a producer can maintain a "library" Song file full of pre-built building blocks (vocal chains, drum groups) without needing them to be formal Templates at all. [Source: Sound on Sound, "Reason: Boost Productivity With Templates"]

## A real producer's actual daily template, described in detail [Sourced]
Worth reading as a model of restraint rather than maximalism: Sound on Sound's own Simon Sherbourne describes moving *away* from a more elaborate input-channel setup (found monitoring fiddly) toward going straight into audio tracks with Input Monitoring enabled — his template got simpler over time, not more complex. His current template: a few hardware synths + guitar wired to a USB mixer's physical inputs, Kong loaded, Komplete Kontrol host present for NI integration, and one favorite RE instrument of the moment loaded and ready. The lesson generalizes: a template is allowed to change as your workflow simplifies, and "what's my current favorite device" is a legitimate thing to keep swapping in a personal template rather than something to over-fix. [Source: Sound on Sound]

## Sources
- reason101.net, "Creative Reason Projects" archive — http://www.reason101.net/category/creative-reason-projects/
- Sound on Sound, "Reason: Exploring The New Combinator" — https://www.soundonsound.com/techniques/reason-exploring-new-combinator
- Audeobox, "Reason Combinator Guide" — https://www.audeobox.com/learn/reason/combinator-guide/
- Sound on Sound, "Reason: Boost Productivity With Templates" — https://www.soundonsound.com/techniques/reason-boost-productivity-templates
