# Chapter 03: Mixing, routing and buses
## Part 4 of 4

_How to wire effects, buses and sends in Reason, plus the Reason 12 template and technique library (by genre and by type)._

**In this part:**
- lofi-hiphop.md — Lo-Fi Hip-Hop — Producer Templates
- mastering-universal.md — Mastering — Genre-Agnostic Template
- pop-vocal.md — Pop / Vocal-Forward — Producer Templates
- rock.md — Rock — Producer Templates
- techno-house.md — Techno / House — Producer Templates
- README.md — Built Patches — by Genre

(Next: end of chapter)


=====================================================
SOURCE FILE: lofi-hiphop.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/lofi-hiphop.md
=====================================================

# Lo-Fi Hip-Hop — Producer Templates

**Honesty check up front:** unlike the other genre files, I could not find Reason-specific, device-level lo-fi documentation. The lo-fi production content that exists online is almost entirely written for tape-plugin-centric or SP-404/sampler-centric workflows, not Reason. What follows is [Adapted] — general lo-fi production knowledge mapped onto specific Reason 12 stock devices, not pulled from a Reason-specific tutorial. Treat this file as more speculative than the others.

## The genre's core ingredients, and a Reason-stock way to get each one

**Tape saturation / warmth** [Adapted]
- **Scream 4** (Reason's stock distortion/damage device) has tape-style damage algorithms and is the natural stock substitute for a dedicated tape-emulation plugin. Light drive, low mix, inserted on the master bus or a drum bus rather than as a hard multiband effect.
- Layering a very light **MClass Compressor** with a slow attack after Scream 4 can help "glue" the saturation into the mix the way analog tape naturally compresses.

**Wow/flutter — pitch instability** [Adapted]
- A slow, low-depth **LFO routed to master bus pitch/tempo modulation** (or, per-instrument, to an oscillator's pitch CV input) recreates the "drifting" pitch of a real tape machine. This is the same *category* of trick documented in the CV-routing techniques file (`techniques-by-type/cv-routing.md`) — an LFO parked at a very slow, subtle rate feeding a pitch destination.
- Alternative: **Redrum or Kong pad pitch slightly detuned per-hit** (a couple of cents, randomized) rather than a global LFO, for a more "hand-played" imprecision than a smooth wobble.

**Vinyl crackle / dust / hiss** [Adapted]
- Reason's factory Sound Bank includes noise/vinyl/foley one-shot and loop samples (browsable in the factory library) that can be loaded into an **NN-XT** or **Kong NN-Nano** slot and layered under the mix at low volume, looped for the song's duration.
- **Grain**, loaded with a vinyl-crackle sample and set to Tape or Long Grains mode, can generate a continuous, non-repeating crackle bed rather than an obviously looping one-shot — this leans on the same Grain capabilities documented in `techniques-by-type/instruments-synths.md`.

**"Wrong speed" / detuned sample character** [Adapted]
- Load a chord/melody sample into **NN-XT** or **Mimic** and deliberately mis-set the Root Key relative to the sample's actual pitch, then transpose the track to compensate for the song's key — the resulting playback speed/pitch mismatch is the classic "chipmunk-slowed-down" lo-fi sample-flip character, done the same way lo-fi producers historically got it from hardware samplers.

**Drum sound and swing** [Adapted]
- ReGroove Mixer with a swung, MPC-style groove template (same device used for the hip-hop swing technique in the hip-hop file) — lo-fi hip-hop's laid-back feel leans on swing/timing looseness at least as much as it leans on filtering.
- A low-pass filter (MClass EQ, or Channel EQ's filter section) gently rolling off the drum bus above roughly 8–10 kHz softens transient harshness without sounding like an obvious effect.

## What I'd research next if this genre matters most to you
A more useful next step than more general web search would be: fetch/watch the two lo-fi tutorials that did surface (aimed at Logic Pro's stock plugins and general DAW-agnostic sampling workflow) and translate their specific plugin chains into Reason stock-device equivalents directly, rather than working from general lo-fi knowledge as I did here.

## Sources (general lo-fi production references, not Reason-specific)
- SampleRoll, "Lo-Fi Hip Hop Production: Sampling and Workflow" — https://sampleroll.com
- The Home Recording Studio, "Logic Pro Lo-Fi Hip-Hop Tutorial: Stock Plugins Only" — https://www.thehomerecordingstudio.com
- lofiweekly.com, "Using Tape Emulation Plugins for Hip Hop and Lofi Beats" — https://lofiweekly.com

=====================================================
SOURCE FILE: mastering-universal.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/mastering-universal.md
=====================================================

# Mastering — Genre-Agnostic Template

Mastering is the one "genre" that's meant to work the same way regardless of what you made, so it gets its own file instead of being folded into each genre file.

## Core stock-device mastering chain [Sourced]
Reason's mastering-relevant stock suite has stayed structurally the same across versions: **MClass Equalizer → MClass Stereo Imager → MClass Compressor → MClass Maximizer**, used in the Rack like any other devices (not a special "mastering mode") and typically the last thing in the chain before export. This is Sound on Sound's own documented order and remains valid in Reason 12. [Source: Sound on Sound]

## Cross-check against your own project's master bus technique
Your Hip-Hop Recipe Book's kick-bass relationship recipe (file `06`) already establishes a compatible master-bus approach elsewhere in your system: a gentle compressor (2:1 ratio, slow attack) to glue the mix, followed by a limiter set to a **-0.3 dB ceiling**. That matches the general principle documented independently here (Audeobox's beat-making guide gives the identical -0.3 dB ceiling figure) — two independent sources landing on the same number is a reasonable signal that it's a sound default, not a coincidence worth ignoring. [Sources: Audeobox; your own project memory]

## Sequencing discipline (a real forum disagreement worth knowing about) [Sourced]
A ReasonTalk thread specifically debates whether it makes sense to produce/mix *through* a mastering-style chain from the start, versus adding mastering processing only after the mix is finished. The pushback recorded in the search results is blunt: *"mastering is something you do AFTER you produce and mix... why would you even need any master fx when you're producing?"* This directly supports the phased approach your own project already uses (master bus processing deferred until a body of recipes exists to glue together) — it's not just your working theory, it's a documented position other Reason producers hold too. [Source: ReasonTalk forum, snippet level]

## Template access mechanics in Reason (useful regardless of genre) [Sourced]
Reason ships **factory Song Templates** for specific scenarios including mastering, accessible via **File → New From Template**, separate from the "Default Song" that loads automatically on launch. To add your own mastering template to that list: open the New From Template menu → "Show Template Folder," and drop your own `.reason` file into the folder that opens (Mac: `~/Music/Reason/Template Song`; Windows: `%AppData%\Roaming\Propellerhead Software\Reason\Template Songs`). You cannot create subfolders inside that list, so if you build separate mastering templates per loudness target or genre, name the files distinctly rather than trying to organize them into folders. [Source: Sound on Sound, "Reason: Boost Productivity With Templates"]

## Sources
- Sound on Sound, "Mastering Reason 3 Mixes" (device order still applicable; MClass suite structurally unchanged) — https://www.soundonsound.com/reviews/reason-studios-reason-12 (device list cross-referenced against the Reason 12 review) and general mastering-chain search results
- Sound on Sound, "Reason: Boost Productivity With Templates" — https://www.soundonsound.com/techniques/reason-boost-productivity-templates
- Audeobox, "Beat Making in Reason" (master bus figures) — https://www.audeobox.com/learn/reason/beat-making-in-reason/
- ReasonTalk forum, "Producing through 'mastering' chain?" — search snippet, full thread not independently verified
- Your project memory: `/projects/019e27ff-05fd-7762-ada1-5c8c05a4fa84/overview.md` and `learnings-and-workflow.md`

=====================================================
SOURCE FILE: pop-vocal.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/pop-vocal.md
=====================================================

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

=====================================================
SOURCE FILE: rock.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/rock.md
=====================================================

# Rock — Producer Templates

This is the thinnest-documented genre for Reason specifically — Reason's own marketing/tutorial output skews electronic/hip-hop, and rock-focused Reason content is scattered across older forum posts. I'm flagging confidence honestly rather than padding this out.

## Full project templates

### Hybrid hardware + guitar starter template (Sound on Sound, Simon Sherbourne's own daily template) [Sourced]
A real working producer's actual template, described in detail:
- Built around a Zoom 8-input USB mixer as the audio interface, with a few portable hardware synths connected.
- A guitar track fed from the Zoom's high-impedance input, with a go-to amp-sim Rack Extension inserted directly on that channel.
- He explicitly moved *away* from routing hardware synths/guitar through dedicated input channels bussed to audio tracks (found monitoring fiddly) and now goes straight into audio tracks with Input Monitoring enabled — a practical lesson on simplifying signal flow.
- Kong drum machine loaded and ready.
- Komplete Kontrol host for Native Instruments integration.
- Grain loaded as his "current favorite RE instrument" at time of writing.

This is a good model for a rock/live-instrument template specifically because it's built around *physical* inputs (guitar, hardware synths) rather than being purely in-the-box. [Source: Sound on Sound]

### Facebook community thread: "Reason templates for rock and roll recording" [Sourced — limited detail available]
Snippet-level detail only (full thread not fetchable): drums from a Reason drum kits ReFill triggered by an e-drum kit; guitars mic'd through a JCM800 head into a 4x12 cab with an SM57; bass recorded DI. Confirms the general pattern — Reason used as the DAW/mixer around externally-recorded/miked rock instrumentation rather than purely programmed instruments. [Source: Facebook, Reason Users group]

## Guitar-specific Combinator template
### Building a guitar amp Combinator [Sourced — description from video title/metadata; full walkthrough not text-fetchable]
Propellerhead's own product specialist (Mattias Häggström Gerdt) published a dedicated "Reason Sound Design" video on building a guitar amp Combinator — i.e., wrapping an amp-sim Rack Extension, cab sim, and pedal-style effects chain into one saved, reusable Combinator patch you drop on any guitar track. This is the same pattern as the hip-hop "wrap each voice in its own tuned Combinator" approach, applied to a guitar chain instead of a drum voice.

A ReasonTalk forum thread ("Combinator, am I missing something?") independently arrives at the same recommendation from a user's own workflow: *"create a Combinator with the internal routing connected ahead of time, and save it as your 'guitar' template."* (Full thread text was blocked from fetching after two attempts; this is from the search snippet.) [Sources: Reason Studios YouTube, ReasonTalk forum]

## Drum bus structure
### Multiband mixer default template [Sourced — title/description only]
A Reason Studios tutorial specifically breaks a drum signal into 4 parallel channels — low, mid, high, and a parallel (likely parallel-compressed) path — using the Multiband Mixer device as a splitting/summing template rather than a single insert. This is a rock/live-drum-appropriate technique (as opposed to a single-sample-source hip-hop kick) because it lets you shape frequency-dependent dynamics across a full mic'd kit. [Source: YouTube, Reason Studios channel — title/description level detail only]

## Honest gap
I did not find a documented "pro rock producer's full Reason template" with the level of device-by-device detail the hip-hop and pop sections have. If this genre matters enough to you, the next research step would be to actually fetch/watch the two video sources above rather than relying on titles, since Reason's rock-specific written documentation is sparse compared to its electronic/hip-hop coverage.

## Sources
- Sound on Sound, "Reason: Boost Productivity With Templates" — https://www.soundonsound.com/techniques/reason-boost-productivity-templates
- Facebook, Reason Users group, "Reason templates for rock and roll recording" — https://www.facebook.com/groups/reasonusers/posts/3347140178663634/
- YouTube, "How to build a guitar amp combinator - Reason Sound Design" — https://www.youtube.com/watch?v=_W85M4e5Glg
- ReasonTalk forum, "Combinator, am I missing something?" — https://forum.reasontalk.com/viewtopic.php?t=7531279 (fetch blocked; snippet only)
- YouTube, "Reason Studios Multiband Mixer Default Template Setup" — https://www.youtube.com/watch?v=EV2fUJbeVIk

=====================================================
SOURCE FILE: techno-house.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/templates-by-genre/techno-house.md
=====================================================

# Techno / House — Producer Templates

Like Rock, this genre has thinner Reason-specific documentation than Hip-Hop, Pop, or EDM/Future Bass. What's here is real but lighter on device-by-device detail.

## Deep house workflow [Sourced — description-level detail]
A Reason 14-era (directly applicable to 12) walkthrough covers a full deep house production pass: warm Rhodes-style electric piano chords, a "dusty," low-slung drum groove, jazzy plucked bass lines, and late-night atmospheric character as the genre's defining ingredients. [Source: YouTube, title/description level]

## Real producer's device list for a deep house track [Sourced]
From a Facebook thread describing an actual session: **Antidote** synth used for a pad and for the bass arpeggio; **Revival** synth used for a second bass layer and a pad. Both are Rack Extension synths (not part of the base Reason 12 install), so this is "if you own these REs" guidance rather than a stock-only template. Worth noting as a real example of how house producers lean on specific RE character synths for the genre's warm, slightly-imperfect analog-style tone. [Source: Facebook, Reason Users group]

## General workflow pattern (not Reason-specific, but consistent with how Reason producers describe their process elsewhere in this research) [Adapted]
Producer discussion elsewhere (r/edmproduction, r/TechnoProduction) repeatedly describes the same shape of workflow regardless of DAW: start from a single element — often a synth sequence/arpeggio rather than drums first — build outward from there, then arrange. This is the inverse of the hip-hop "drums first" pattern documented in the hip-hop file, and worth trying deliberately if a house/techno idea is feeling stuck starting from drums.

## Honest gap
I did not find a documented full Reason rack template for techno or house at the level of detail in the Pop/Vocal or EDM/Future Bass files. If this genre becomes a priority, the Antidote/Revival thread and the deep house video are the two threads worth pulling on further (the video specifically would need an actual watch-through, not just its title/description).

## Sources
- YouTube, "Deep House Production Workflow in Reason 14" — https://www.youtube.com/watch?v=E7y4Pzl7IyE
- Facebook, Reason Users group, "Reason stock devices in deep house production" — https://www.facebook.com/groups/361165013897141/posts/2866302826716668/
- Reddit r/edmproduction, "What's your production/arrangement workflow?" — https://www.reddit.com/r/edmproduction/comments/17j785o/whats_your_productionarrangement_workflow/
- Reddit r/TechnoProduction, "Workflow tips" — https://www.reddit.com/r/TechnoProduction/comments/ydwf3i/workflow_tips/

=====================================================
SOURCE FILE: README.md
ORIGINAL LOCATION: DL:reason12-templates-and-techniques/built-patches/README.md
=====================================================

# Built Patches — by Genre

This is different from `templates-by-genre/` and `techniques-by-type/`, which are *write-ups*. This folder holds the actual Reason files — `.cmb` Combinator patches and `.rns` song files — sorted into the genre folder they're most useful for, ready to drop into your Reason rack.

**Right now it holds patches I could find a real, working download link for during research** — not made up, not AI-generated placeholders. Every file below was actually downloaded and verified (unzipped, checked it's a genuine Reason patch file) before going in this folder. Each genre folder has its own `README.md` naming what's in it, where it came from, and how it connects to that genre's `templates-by-genre/<genre>.md` write-up.

As you and I build your own templates and Combinators going forward — the ones documented in the Recipe Book, or new ones — this is where they'll get added too, genre by genre, so this folder becomes a real working library over time instead of just a one-time research snapshot.

## What's in each folder right now

| Genre | Files | Source |
|---|---|---|
| `pop-vocal/` | `SlapGuruVOX5.cmb` | Reason Studios (Yana Mahal) |
| `hip-hop-trap/` | 2× Granular Drum Machine Combinators | Reason Studios (#ReasonQuickTip) |
| `edm-future-bass/` | `Wonderland.rns` | reason101.net |
| `techno-house/` | 2× Audiomatic Kong Switcher Combinators, 2× Granular Drum Machine Combinators | reason101.net / Reason Studios |
| `rock/` | — (none found yet) | — |
| `lofi-hiphop/` | — (none found yet) | — |
| `mastering-universal/` | — (none found yet — Reason's own factory Song Templates cover this via File → New From Template, see `templates-by-genre/mastering-universal.md`) | — |

A file placed in one genre folder is often genuinely useful in others too (the granular drum machine Combinators are duplicated into both `hip-hop-trap/` and `techno-house/` for that reason) — each folder's own README says which of its files are cross-genre.

=== END OF PART ===
