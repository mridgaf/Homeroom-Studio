# Dormant Features — running list

*Living document. Things in this project that are built but switched off,
built but frozen on old settings, or talked about but never built. Plain
short descriptions, updated as more turn up — not a one-time snapshot.*

Last updated: 2026-09-03

---

## Locked (frozen on old settings, protecting hand edits)

**Drum pattern variety, for 8 of 9 DJs — `extras` / `kick_flavors` / `library`**
Same root cause as the drum-pattern lock you just had me fix, but only
partly fixed. `crew_config.json` has a switch (`_style_lock`) that stops
the engine's newer settings from overwriting the file automatically. I
fixed the RHYTHM part (`grammar`) today. I did NOT touch three other
parts — how often/what extra percussion sounds get added (`extras`), which
kick type gets picked (`kick_flavors`), how often a reference groove gets
borrowed (`library`) — because those have drifted in BOTH directions: the
live file has hand-added extra sounds the code doesn't know about, AND the
code has number tweaks the live file never got. Fixing it blind could
erase real hand-tuning either way. Needs a closer look, DJ by DJ, before
touching it.

---

## Not implemented (the idea exists, no code does it yet)

**Tempo ranges per DJ**
Research gives every DJ an ~8-10 BPM range (Otto Grit 86-96, etc). Every
beat still renders at exactly ONE fixed number per DJ — it never varies.

**Crate Prophet: a 2nd hit stacked right under the snare**
Pete Rock's own words: sometimes a tambourine or 2nd snare fires WITH the
main snare hit for extra thickness. There's no way right now to lock a
sound to fire exactly with another lane's hits — guest sounds always play
on their own separate rhythm.

**Chrome Dial: hats getting busier as they lead into a snare hit**
Research says his hi-hats/percussion build up right before each snare hit
and thin out after. Right now a pattern's "busyness" is picked once per
bar, not shaped around where the snare lands.

---

## Built, but switched off or unused

**`kick_sub_reinforce()` — Otto Grit's kick weight** *(built today)*
A quiet low tone added under his sampled kick for extra weight, based on
his engineer's own account of how Dilla's records were made. Built,
tested, wired to a switch (`sub_layer`) — nobody's kick uses it yet.
Waiting on your a/b/c.

**4 mix effects — EQ, echo, chorus, phaser**
All four built, tested, and you already approved how they sound (a
6-DJ listening test each). None of them plays on ANY DJ's beats yet —
you asked for these one DJ at a time, and that pass hasn't started.

**`haas()` — makes hats/percussion sound wider (stereo)**
Built and tested. Nothing in the project calls it.

**`transient_shape()` — makes a drum hit sound sharper or softer**
Built and tested. Nothing in the project calls it.

**`ratchet_times()` — fast stutter/roll hits (like a hi-hat machine-gun
roll, but on any drum)**
Built and tested. Nothing in the project calls it.

**"hall" reverb — the biggest, longest room sound available**
Built. Only ONE DJ (Half Light) can ever reach it. Every other DJ's
random room-sound roll skips right over it.

**Vocal one-shot lane** (`VOX_LANE_P` in beat_machine.py)
A chance to drop in a short vocal-style sound. Set to 0% — you turned
it off on 2026-08-01.

**A second "stamp" mechanism** (`STAMP_LANE` in beat_machine.py)
A different, separate way of adding a signature one-shot sound, built
into the older genre-style beat path (not the DJ-crew path, which
already has its own working stamp system). Switched off.

**3 leftover settings that do nothing** (`dilla_snare`, `sidechain_prob`,
`snare_space` in groove.py)
Old global on/off switches from before decisions got made per-DJ
instead. Nothing reads them anymore except a test checking they still
equal themselves.

**An alternate final mix chain** (`engine_master`, mentioned in
DECISIONS.md 2026-09-02)
A different way of finishing/mastering every beat, approved by ear once
on a side branch back on 2026-08-08. That branch's code isn't part of
this project folder anymore, so it's not something sitting dormant in
today's code — it's a decision that was made once and never carried
over. Would need to be rebuilt and A/B'd against today's mix chain if
you want to revisit it.

---

*New finds get added here as I come across them — this list isn't the
result of one big search, it's what's turned up along the way.*
