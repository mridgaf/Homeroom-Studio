# Template and automation ideas from the demo songs

Running list (started 2026-09-29, after step 00c). Requested by the owner mid-session: "Look for template ideas.
Automation ideas and skill ideas. Along with phrases." Skills and phrases live in their own lists:
[skill ideas](demo-song-skill-ideas.md) · [phrase ideas](demo-song-phrase-ideas.md). Nothing here is built.

**ASSUMING (correct me any time):** "template" = a reusable starting setup (a song, rack or mixer layout) that
could be saved as a Reason template or written up as a recipe card in `recipes/`.

Tags as in the song notes: **Seen** = on screen · **Manual** = manual place named · **Guess** = not confirmed.
Songs: [Street Phone](demo-song-notes.md) · [Airplane](demo-song-notes-airplane.md) · [Power](demo-song-notes-power.md). Nothing here was heard.

## A. Template ideas (setups worth reusing)

| Template | What it is | Came from | How sure |
|---|---|---|---|
| **Pump bus** | An Output Bus channel that several channels route to, with an insert Combinator holding a Synchronous "Long Sidechain" curve on Level. One place sets the pumping for the whole group | Airplane: 7 of 18 channels go to "Sidechain Bus"; Sidechain Bus FX Combinator holds the Synchronous | Seen. That it pumps: Guess, not heard |
| **Send-effects trio** | Master Section sends 1-3 feeding RV7000 "Plate", RV7000 "Room" and The Echo, each named for what it is; Street Phone adds a DDL-1 "Delay 3/16" on send 4 | Both songs | Seen |
| **Macro-knob instrument or effect box** | A Combinator whose four knobs and four buttons carry author labels: Airplane "Shift / Dirt / Width / Reverb Level" and "Hammer On / Compress / AM / Delay"; Street Phone PAD PROCESSOR "Filter Freq / Filter Rez / Reverb / Dly". The labels become automation lane names | Both songs | Seen |
| **Effect Combinator as channel insert** | A Combinator used as the insert FX of a mixer channel | Street Phone pad processor; Airplane Sidechain Bus FX | Seen |
| **Kick squash chain** | Kick drum, then a squash stage before the mixer: Redrum then Pulveriser 1 "SQUASH" (Airplane); Kong then Compressor then Combinator "KICK SQUASH" (Street Phone) | Both songs | Seen |
| **Name-everything rule** | Every device carries a label (KICK COMP, PAD PROCESSOR); the mixer channel, the rack label and the patch share a name, so a spoken "the pad" can be matched. Airplane mostly does this but drifts a little (mixer "Please Release" vs rack "Please Release Me") | Both songs | Seen |
| **Riser and crash track pair** | Two Thor "Stereo Noise Sweep [Run]" tracks with short clips about every 8 bars, plus a Crash audio track with hits at section starts | Airplane | Seen the clips. Risers and section changes: Guess |
| **Filtered intro and outro on the kick channel** | The Kick's own channel-strip low-pass and high-pass switched on by clips over the first 12 and last 4 bars | Airplane Kick lanes "LPF On/Off", "HPF On/Off" at about bars 1-13 and 61-65 | Seen lanes. What it sounds like: Guess |
| **64-bar song map** | Entries at about bars 1, 13, 21, 29, 45 and 61 with an outro at 61-65 | Airplane | Guess (sections read from where tracks enter) |
| **Master chain** | A master-bus Combinator plus a separate mastering EQ | Street Phone "MASTER SECT" Combinator, MClass EQ, "Default Mastering Suite"; Airplane "Master Section FX" Combinator | Seen (Airplane one only by name) |
| **Arp into macro instrument** | A Dual Arpeggio player in front of a Combinator patch, so one macro knob (Shift) can move the whole part | Airplane Norwegian Boy -LNB | Seen |
| **Pulsar as an oscillator** | A Combinator with no synth: Pulsar LFO 1 Audio Out feeds an ECF-42 filter, a second Pulsar's CV Out wobbles LFO 1's Rate, then mixer, Scream 4, RV7000; an RPG-8 arpeggiator on top | Airplane "Pulse Scream -LC" (wiring file, D3) | Seen the cables. How it sounds: not heard |
| **Double Malstrom "Kalimba" voice** | Two Malstrom synths (L and R) into a Line Mixer 6:2, then Pulveriser, The Echo, Compressor, all inside one Combinator with four macro knobs (Shift, Dirt, Width, Reverb Level) | Airplane "Norwegian Boy -LNB" (wiring file, D and D2) | Seen. What the knobs drive: Modulation Routing not opened |
| **Same master Combinator in both songs** | "Master Section FX": M EQ, Stereo Imager, M Comp, Maximizer inside a Combinator, knobs Loudness Curve, Compression, EQ Boost Freq, Master Gain | Airplane and Street Phone | Seen (left jacks read) |
| **Silent kick trigger for the bass duck** | A Redrum (pattern A1, steps 1-5-9-13, one kick sample) cabled from its channel 1 outputs into the Bass mixer channel's Side Chain Input, with the channel compressor's KEY lit. Nothing else in the mix plays it | Power "BASS SIDECHA..." Redrum | Seen wiring and KEY. That it pumps: not heard, and whether the Redrum runs is unknown (OPEN-ISSUES 41) |
| **Per-channel insert chain "Comp, EQ, Scream 4, EQ"** | Four inserts under the instrument, each labelled with the channel name (PIANO L COMP, PIANO L EQ, ...) and a Scream 4 in the middle | Power Piano L/R and Mal L/R | Seen. Order taken from the rack order; middle links not hovered |
| **Drum-machine character chain "Audiomatic, Pulveriser, EQ"** | Each Kong runs through an Audiomatic (Retro Transformer) then a Pulveriser, and Kong FX adds an EQ | Power Kong half / double / FX | Seen (Kong half fully hovered) |
| **RPG-8 into a synth by CV and gate** | An RPG-8 arpeggiator cabled to the Malstrom's Gate, CV, Mod Wheel and Pitch Wheel inputs, so an arp part plays the same bass patch | Power Bass arp to Bass | Seen by hover |
| **Send 5 on for every channel** | One shared Unison effect on send 5, on for all 13 channels, while send 4 (a second Echo) is on for none | Power mixer | Seen (levels not read) |
| **Own track for the vocal, own strip** | An Audio Track "Jayy vox comp" whose channel has sends 3 and 4 off | Power | Seen |
| **42-bar hook song at 84 BPM** | Intro 1-3, verse 3-11, hook 11-19, break 19-25, verse 25-29, final hook 29-40, echo tail 40-42 | Power | Guess (read from clip positions) |

## B. Automation ideas (patterns for moves over time)

| Idea | What it does | Came from | How sure |
|---|---|---|---|
| **Hold a value with a one-point clip** | A clip with one point holds that value for its length; outside clips the parameter sits at its static value | Street Phone Organ 1 filter clips; Manual [6] lines 4380-4389 | Seen and Manual |
| **End-of-section filter lift** | A short clip near a section end that rises from the resting value: Mushi "Filter Freq" 2 bars at bars 43-45 (three points, rising), with a "Dist Amount" clip about a bar later | Airplane | Seen the shape. That it lifts the filter: Guess |
| **Switch lanes as long clips** | On/Off lanes ("LPF On/Off", "HPF On/Off", "FX1 Send On/Off") where a clip is the "on" stretch. "FX1 Send On/Off" has a short clip at about bars 21-22: a one-bar throw to the Plate | Airplane Kick | Seen lanes. The one-bar-throw reading: Guess |
| **Pattern automation** | Redrum "Pattern Select" clips ("A1" blocks) switch patterns on the bar. Manual [6] line 4512: pattern lanes have no static value, and where there is no clip the device stops | Airplane Kick and Clap | Seen and Manual |
| **One lane per macro knob** | A Combinator knob lane ("Shift", bars 29-45) moves everything wired to that knob at once, one curve instead of many | Airplane Norwegian Boy | Seen |
| **Mod Wheel lanes** | "(Mod Wheel)" lanes on the three Europas (about bars 9-13, 13-20, 45-61). What they drive inside Europa: not looked at | Airplane | Seen lanes only |
| **Level lane on a channel** | A "Level" lane on a mixer-style row: Kick bars 29-45 | Airplane | Seen |
| **Automate the modulation, not the sound** | Synchronous already loops a curve on the beat, so the song only needs to change its settings (Level, filter) instead of drawing many volume dips | Airplane Synchronous | Seen the device. How the composer used it: Guess |
| **Lane name equals parameter name** | The lane is named by the parameter ("Filter Mod", "Filter Freq", "Dist Amount", "Pattern Select"); the voice app's Europa and Grain scopes already have "Filter Mod", "Filter Freq", "Dist Amount" | Airplane and `remote/ReasonVoice.remotemap` | Seen |
| **Voice-written sweep** | "Sweep the filter up over four bars" would write a clip like the Mushi one. Proven by hand for a device with its own track while recording (`experiments/automation-test-2026-09-25/RESULTS.md`); nothing in `reason_voice/` writes it. OPEN-ISSUES 31 | Both songs | Seen (bridge test) and file facts |
| **Channel-strip HPF lift** | A short clip on a mixer channel's "HPF Frequency" lane (Drum loop, about bars 25-29), the channel's high-pass knob getting a green frame | Power | Seen the lane and the green frame. Direction: not read |
| **Echo throw at the end** | A short "Dry/Wet Balance" clip on an echo device over the last two bars (about 40-42) | Power "Jayy echo" | Seen the lane. What it sounds like: not heard |

## B2. Things this exploring taught about method (worth reusing)

| Idea | Detail | How sure |
|---|---|---|
| **Read wiring by hover** | Hover a jack, wait 2 seconds: tooltip "Connected to <device>: <jack>". Works on jacks, not on cable bodies (two tries) | Seen |
| **Read wiring by menu** | Ctrl-click a jack: full device list, check on the connected device, asterisk on occupied jacks in each sub-menu | Seen |
| **Jump the rack with RACK** | The RACK button under a mixer channel scrolls the rack to that device | Seen |
| **Find every keyed sidechain in one pass** | Open one jack menu and hover each channel: an asterisk beside "Side Chain Input L/R" means a real cable. Airplane has none | Seen |

## C. What each template or automation idea would need
- **Recipe cards:** a card needs `recipes/**/*.md` frontmatter and the section list from CLAUDE.md. Good first cards: "Pump without a
  sidechain cable (Synchronous)", "Filter riser (Grain filter and distortion)", "Kick squash", "Sub-mix bus".
- **Reason templates:** a Reason song saved as a template would hold the rack; that is for the owner to do in Reason.
- **Checking:** each "Guess" above needs ears, or a look at the parameter values in the clip.
