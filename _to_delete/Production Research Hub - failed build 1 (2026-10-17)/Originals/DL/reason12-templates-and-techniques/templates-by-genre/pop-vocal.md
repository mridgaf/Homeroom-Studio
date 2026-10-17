# Pop / Vocal-Forward — Producer Templates

This is the best-documented genre in this whole research pass — Reason Studios published a full, detailed, device-by-device vocal chain walkthrough from an outside artist/producer. Reproduced here in enough detail to actually build it.

## The full vocal chain template: Yana Mahal's "SLAP GURU" method (Reason 13, works identically in Reason 12) [Sourced]

Official Reason Studios tutorial, built around gain staging discipline, serial (not single-stage) compression, and send-based space rather than insert reverb.

**Chain order, device by device:**

1. **Gain Tool** (Utilities folder) — first in the chain, always. Adjust the raw recording level to sit comfortably against the instrumental. Rule stated explicitly: *any time you make a big change later (heavy EQ cut, big boost) and lose volume, add another Gain Tool to match the original level* — so you're judging changes on quality, not just perceived loudness.
2. **MClass Equalizer** — subtractive/surgical pass:
   - Low shelf around **150 Hz**, cut 6–8 dB, to remove rumble and P-pops.
   - "Sweep technique" to find mud: boost a narrow (high-Q) band and sweep it through **300–500 Hz**; wherever it sounds boxy/honky, flip that boost into a subtle ~3 dB cut instead.
3. **Channel EQ** (the analog-console-modeled one) — added *after* the surgical EQ, specifically for character rather than correction:
   - High-pass around **60 Hz** (this filter's slope is described as unusually musical, keeps the low end tight without sounding thin).
   - Presence boost, wide Q, in the **3–4 kHz** range, to help the vocal cut through a dense mix.
   - "Air" boost, 3–4 dB, at **8 kHz and above**, for a brighter/breathier top end.
4. **Serial compression — two stages, light touch each** (the core technique of this whole chain):
   - Stage 1, Channel Dynamics: 2:1 ratio, only ~2 dB gain reduction, Peak mode, fast release — catches the sharpest transients only.
   - Stage 2, MClass Compressor: another 2:1 ratio, another ~2 dB reduction — described as "gluing" the performance rather than controlling peaks.
   - Explicit reasoning given: one compressor doing all the work tends to sound squashed; two compressors each doing a little work sounds more consistent *and* more natural.
5. **Stereo Tool** — vocals are usually recorded mono; this adds width while specifically preserving the center image (unlike a generic stereo widener that can weaken the center).
6. **Ripley (Space Delay), on an Aux Send, not an insert** — keeps the dry vocal upfront while the effect "floats" around it. The specific trick: use Ripley's **Offset** knob to create a timing difference between left and right sides — described as producing stereo spread "a standard delay can't touch."

**Missing on purpose:** no de-esser is built into this chain, so it works without requiring third-party plugins. If you add one, the stated placement is *before* the compressors, so "S" sounds don't trigger the compression too hard.

**Packaged as a Combinator** with 8 labeled macro knobs: Rumble & Mud, Presence & Air, Parallel Comp, Tape & Dist, and an Octave Down knob described as adding "a distorted octave-down pitch for a thick, modern trap vocal vibe" — i.e. the same chain doubles as a hip-hop vocal-processing Combinator with one knob turned. [Source: Reason Studios, official tutorial + downloadable Combinator]

## Older but still-relevant vocal mix technique reference [Sourced — light detail]
An earlier Reason Studios tutorial ("Professional Vocal Mix Techniques") covers the same ground at a higher level: getting a vocal to sit forward in the mix, natural-sounding tuning correction, and balancing effects so they're felt rather than obviously heard. Useful as a second opinion/gut-check against the Yana Mahal chain above, though it doesn't give the same device-by-device specificity. [Source: Reason Studios]

## Community ask (unmet, as of the Reddit thread) [Sourced]
A Reddit thread on r/reason specifically asked for a ready-made vocal chain template (EQ, compression, effects, "all ready to go") and a separate drum template — nobody in that thread pointed to one. The Yana Mahal chain above is the closest thing to that community ask that actually exists as an official, downloadable artifact. [Source: Reddit r/reason]

## Sources
- Reason Studios, "How to Build a Vocal Chain in Reason 13" (Yana Mahal) — https://www.reasonstudios.com/news/post/build-an-epic-vocal-chain-in-reason-13
- Reason Studios, "Tutorial: Professional Vocal Mix Techniques" — https://www.reasonstudios.com/news/post/professional-vocal-mix-techniques
- Reddit r/reason, "Song / Rack Starter Templates" — https://www.reddit.com/r/reason/comments/1cecm1m/song_rack_starter_templates/
