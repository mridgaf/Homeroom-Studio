# Buses, sends, parallel, and the master
Tags: **[Manual]** 12.7 manual. **[Web]** web source. **[Guess]** my idea, untested. Nothing here has been heard on our machine.
Cables and exact steps: `../manual-digest/routing-and-main-mixer.md` (Part 3, recipes A–J). This file is the "why and when".

## 1. Insert vs send
- **Insert** = the whole signal goes through the effect. Best for sound design on one part (EQ, compressor, amp, distortion). [Web: Record U]
- **Send** = the channel's send knob sets how much goes to a shared effect; the Master Section **Return** knob sets how much of the effect comes back. Best for reverb and delay, so many tracks share one effect. [Manual; Web]
- Send is post-fader by default (the channel fader also moves the send). **Pre** button = send ignores the fader. [Web: Record U]
- Reason has 8 Send FX on the Master Section. [Manual]

## 2. Building depth with reverb and delay [Web: Record U, 2006; still valid physics]
| Want | Do |
|---|---|
| Part sounds farther away | More send, lower fader |
| Part sounds closer | Less send, higher fader |
| Several parts feel in one room | Send them all to the SAME reverb |
| One part stands apart | Give it a different reverb or a delay |
| Reverb makes the mix muddy | Use the reverb's own EQ to cut lows/mids (RV7000 EQ page, Low EQ high and gain down) |
| Delay as "reverb" | A short multi-tap delay on a send gives a sense of space too |
- RV7000: Plate for vocals, Room for drums are the workhorses. Predelay 20–40 ms; HF Damp on; EQ-cut the tail. [device_refs/rv7000-mkii.md]
- The Echo: set Dry/Wet to 100 % on a send; use **Ducking** so repeats stay out of the way of the dry sound. [Web; device_refs/the-echo.md]

## 3. Buses
- **Output Bus (sub-mix):** select channels → create bus → one fader/EQ/compressor for the group. Use for drums, doubles, backing vocals, synth stack. [Manual; Web]
- Don't put the same effect on 12 channels; put it once on the bus. [Web]
- Record a bus or the master to audio with **Rec Source** (stems). [Manual ch. 6]

## 4. Parallel processing
- **Mix** knob on Channel Dynamics / Master Bus Compressor. Easiest. [device guides]
- **Parallel Channel** (Parallel Out jacks) for a heavy processed copy you blend in. [Manual]
- **Spider splitter**: clean path + effect-only paths (reverb, Scream) each on their own mixer channel. [Web: Ron Headback]
- Use for: drum smash, vocal body, bass grit (high band only). See `drums.md`, `vocals.md`, `bass-and-low-end.md`.

## 5. Master Section
- The Master Section strip has its own **bus compressor** and an **Insert FX** section; both process the whole mix. The rack **Master Bus Compressor** device is the same compressor with Input Gain and Mix added. [Manual ch. 17, 59] One forum user says mixing "into" the master chain from the beginning gives faster, better results. [Web: forum snippet (the forum page itself was blocked, I only saw the search snippet)]
- Starting point seen in a Facebook-group search snippet: ratio 2:1, attack 0.3 ms, release Auto. The device guide suggests 10–30 ms attack to let drums punch. These conflict; **listen**. [Web (low quality) vs device_refs]
- External sidechain input on the Master Bus Compressor lets you "focus" what drives it (e.g. filter the lows out of the key signal so the kick doesn't pump the whole mix). A 2012 Reason Studios video exists on this; I only saw its title and summary. [Web, unverified]
- Order that makes sense [Guess]: MClass Equalizer (Low Cut on) → Master Bus Compressor (1–3 dB) → MClass Stereo Imager → MClass Maximizer last.
- Reason Studios' own old position (2006): Reason is great for writing and mixing; do final mastering separately. [Web: "Mastering Mastering" snippet]

## 6. Workflow tips
- Pre-mix in Reason, bounce, final mix elsewhere (one user's habit). [Web]
- Hide the channel strip sections you don't need (Filters, EQ, Dynamics, Faders only) so every strip fits the screen. [Web: r/reasoners user]
- Gain stage: after any big EQ move, level-match before you judge. [Web: Yana Mahal]
- Save any good insert chain as an **Insert FX Patch** (.cmb). [Manual]

## 7. Version warning
The web is full of Reason **13 and 14** tutorials. They mention a Sidechain Tool, Gain Tool, Stereo Tool, Ripley, Track Panel, Rack per Track, Track Folders, RV-9. Those are **not in 12.7** (checked: none of the first four appear in the 12.7 manual). Use the 12.7 equivalents named in the other files, or ask if an upgrade matters.

## Sources (summaries only)
- Reason Studios, "Tools for Mixing: Reverb" (Record U), 2006 — https://www.reasonstudios.com/news/post/tools-for-mixing-reverb
- Reason Studios, "Getting Started in Reason 14" (for the Reason 14 feature list), 2026 — https://www.reasonstudios.com/news/post/reason-14-walkthrough
- r/reasoners "How do you mix vocals…" and "Need tips on mixing drums" threads (see vocals.md and drums.md)
