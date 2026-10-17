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
