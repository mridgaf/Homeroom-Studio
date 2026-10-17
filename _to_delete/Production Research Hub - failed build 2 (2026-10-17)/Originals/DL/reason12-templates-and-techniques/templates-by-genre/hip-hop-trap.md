# Hip-Hop / Trap — Producer Templates

## Full project templates

### The "battle-ready" starter rack [Sourced]
A pattern used by competitive/timed beat producers, but it's the same logic any hip-hop producer uses to avoid rebuilding a rack every session: pre-load your go-to instruments, save as a `.reason` template, and load it instead of starting from an empty Rack.

- **Kong Drum Designer** loaded with your own kit ("battle kit") — not a factory preset kit, a kit you've built once and reuse.
- **Thor** pre-configured as a bass/808 starting patch.
- **Europa** pre-loaded with a melody patch.
- Mixer channels for each with basic EQ/compression already inserted, so you're mixing as you go instead of bolting it on at the end.

Time-boxed workflow the same source lays out (useful as a sanity-check pace even outside a battle context): drums ~4 min, bass ~3 min, melody ~4 min, arrangement ~2 min, mix/export ~1 min, after a ~1 min template load. [Source: Audeobox]

### The 808 patch (Thor), specifically [Sourced]
- Sine wave oscillator.
- Long amp envelope decay (2–5 seconds).
- A **fast pitch envelope routed to oscillator pitch** — this is what gives the classic 808 pitch-down "slide" on the attack, not a manually-drawn pitch bend.
- Light **Scream 4** distortion for harmonic content/grit.
- Programmed as a melodic (keygroup-style) instrument playing different notes to follow the chord progression, not a single fixed pitch.
[Source: Audeobox — "Beat Making in Reason"]

### Community rack templates (Reddit r/reason, "Song / Rack Starter Templates" thread) [Sourced]
Several working producers described their actual daily templates in this thread — worth treating as a small sample of real-world setups rather than one "correct" answer:

- **two_chalfonts**: a base template with two RV7000 reverbs (hall + room) wired to the mixer's sends/returns, an NN-XT with 4 of its outputs wired to 4 separate mix channels, plus master group channels for drums, bass, and music.
- **umbringer** (dance-leaning, but directly applicable to hip-hop/trap drum programming): one Kong per principal drum sound — kick, snare, clap, shaker, hi-hat, cymbals — each wrapped in its own Combinator with EQ/processing dialed in and saved with favorite drum timbres, plus a mastering Combinator already sitting at the end of the chain. Explicit caution from the same poster: leaning on templates too hard can flatten your own expression — build new synths/patches regularly, don't just recall the same rack forever.
- **m8k**: default drum kit + drum players mapped to the two Umpfs (Reason's user-remappable controller buttons), plus audio-in channels pre-wired to match a specific hardware interface's patchbay.
- **will_sherman**: pushes back on using *other people's* templates specifically — argues a template only pays off when you understand why each piece is wired the way it is, and that in Reason (unlike Cubase/DP-era workflows) a lean master-bus-insert template plus liberal use of the Favorites/preset system may be enough.

Takeaway: there's no single "pro hip-hop template" file being traded around — the pattern is: wrap each drum voice in its own tuned Combinator, keep a reusable reverb send pair, and put a mastering chain at the end by default. [Source: Reddit r/reason]

### Harald Austad's real workflow (platinum producer — Karpe Diem, Madcon, Jaa9 & OnklP) [Sourced]
Not a file template, but a documented step order from a working hip-hop-adjacent producer who does "90% of all the work" in Reason:
1. Start with drums (kick, snare, hats) to set tempo/feel.
2. Browse sounds/loops until something sparks a groove.
3. Add a melody — Austad favors electric bass and piano sounds, reaches for 808s specifically on hip-hop beats.
4. Build layer by layer, listening after each addition.
5. Arrange into intro/verse/drop structure.
6. Process every sound individually (EQ, compression, reverb, saturation) — he treats this as part of *writing*, not a cleanup pass at the end.

His stated production identity comes from *how* he processes sounds (saturation/warmth, Thor as a go-to synth) more than which devices he picks. [Source: Reason Studios artist interview]

## Mix/master-stage notes specific to this genre
- ReGroove Mixer with **MPC-style groove templates** applied to the drum track is called out specifically as effective for hip-hop — it reintroduces human-feeling shuffle/timing/velocity variance to programmed drums. [Sourced — Audeobox]
- High-pass the melodic/chord elements around 150 Hz to keep the low end clear for kick + 808/bass. [Sourced — Audeobox]
- Trap-specific: intricate hi-hat rolls are typically programmed at 1/32 resolution in the sequencer; Reason handles this natively. [Sourced — Audeobox]

## Sources
- Audeobox, "Beat Making in Reason: Complete Workflow from Drums to Export" — https://www.audeobox.com/learn/reason/beat-making-in-reason/
- Reason Studios, "How To Make Beats In Reason: A Producer's Step-By-Step Guide" (Harald Austad) — https://www.reasonstudios.com/news/post/harald-austad
- Reddit r/reason, "Song / Rack Starter Templates" — https://www.reddit.com/r/reason/comments/1cecm1m/song_rack_starter_templates/
