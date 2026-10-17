---
name: reason-regroove
description: How to add swing, push/pull timing and human feel with Reason 12's ReGroove Mixer, step by step. Use when the owner asks for swing, shuffle, "loose", "laid back", "drunken kicks", "push the snare", MPC feel, or when a recipe says "use ReGroove" and he needs the steps. Source is the Reason 12.7 manual, ch. 22. Status DRAFT: not yet run through the skill-creator benchmark loop, nothing here has been heard.
---

# ReGroove: swing and feel

Source: Reason 12.7 Operation Manual, ch. 22 (`~/.reason_voice/reason12_manual/full_chapters/22-the-regroove-mixer.txt`).
Every number below is from the manual. Nothing was heard. No API sets these knobs for us (see CLAUDE.md); he or the
screen does it. A surface CAN be locked to the ReGroove Mixer (`docs/reason/FINDINGS.md`), untested.

## What it does, in one line
Changes when and how hard NOTES play (timing, velocity, length), live, without moving the notes in the clip.
**Note lanes only.** It does nothing to audio tracks.

## The steps (do them in this order)
1. Click the **Groove** button on the left of the Transport Panel. The ReGroove Mixer opens: 32 channels, 4 banks (A-D) of 8.
2. On the note lane you want to change, use the **Groove Select pop-up** and pick a channel. ("No Channel" = off.)
3. In the mixer, make sure that channel's **On** button is lit.
4. Turn the knobs (below) while the song plays. Use your ears, not your eyes.
5. To compare with the plain version: turn the channel's **On** off, or untick **Enabled** in the lane's pop-up.

## The knobs (per channel)
| Knob | Plain meaning | Numbers |
|---|---|---|
| **Shuffle** | Delays every other 16th note | 50% = straight. 66% = triplet swing. Below 50% = un-swings a swung beat (34% straightens a triplet feel) |
| **Slide** | Pushes the whole lane ahead of or behind the beat | -120 to +120 ticks (120 ticks = a 32nd note). Negative = rushes, positive = lays back |
| **Groove Amount** | Master strength of the loaded groove patch | 0% = nothing, 100% = full. Scales the four impacts below |
| **Groove patch** | A saved feel (.grov file) | Browse and step through with Next Patch |
| **Pre-Align** | Snaps notes to a rigid 16th grid first, so shuffle and slide land predictably | Non-destructive |
| **Global Shuffle** | Use the song-wide shuffle instead of this channel's own knob | Keeps the lane in step with Redrum, Matrix, RPG-8 and Dual Arpeggio, which only use Global Shuffle |

**Global Shuffle** knob (left side of the mixer) is the song-wide value. It also sets the swing of Redrum's own sequencer,
Matrix, RPG-8 and Dual Arpeggio. If the drums swing but a pattern device sits straight, check this knob.

## Groove Settings (click a channel's **Edit** button)
Four "impact" sliders, each scaled by Groove Amount:
- **Timing impact**: 100% = notes move exactly to the groove's positions, 50% = halfway, 200% = twice as far.
- **Velocity impact**: changes only the differences between notes (soft stays soft). Set Timing impact to 0 to take only the dynamics.
- **Note length impact**: mostly empty on drum grooves. Only the Bass-Comp patches carry length.
- **Random timing**: 0 to 120 ticks of random shift. Same every playback until you edit the clip.

## Moves that work (all from the manual's tips)
- **Split the kit into lanes first.** Kick, snare and hat on separate lanes, each to its own channel. One groove on everything sounds clumsy.
  Use Extract Notes to Lanes to split one lane.
- **Push or drag the snare**: snare lane to a channel with a small + (lay back) or - (push) Slide.
- **Clap doubling a snare**: send the clap to a channel with a little Random timing so the two stop sounding like one hit.
- **Same groove patch on several lanes at different Groove Amounts** beats different patches on each lane.
- **Rushing the first beat**: leave an empty bar at the start and set the Anchor Point to 2, or beat 1 has nowhere to move to.
- **Anchor Point**: tells ReGroove which bar the groove starts on. A time-signature change restarts every groove at that bar
  (add one with the same signature to force a restart).
- **Keep groove lengths as multiples** (1, 2, 4, 8 bars). A 3-bar and a 4-bar groove together repeat every 12.
- **Copy a channel**: Ctrl-click the patch name > Copy Channel, then Paste Channel on another. **Initialize Channel** resets one.

## Factory groove patches (Browse > Factory Sounds > ReGroove Patches)
| Folder | What it is |
|---|---|
| **MPC-60** | Timing from an Akai MPC-60. No velocity or length. Some use Random Timing |
| **Programmed** | Hand-made feels in **Hiphop** and **Pop-Rock** folders |
| **Vinyl** | Timing and velocity pulled from classic records |
| Drummer, Percussion, Bass-Comp | Session musicians. Only Bass-Comp has note length |

## Make it permanent, or make your own
- **Commit to Groove** (Edit menu or track menu): moves the notes to where they now play, so you can edit them. It applies to
  the WHOLE track. To keep one lane grooved, untick Enabled on it first, commit, then tick it back.
- **Your own groove**: select a clip, pick an unused channel in the Tool Window Groove tab, click **Get from clip**, then **Save Patch**.
  Best source clips: many 16th notes (gaps in the clip become gaps in the groove), similar velocities, an exact bar count
  (1, 2, 4...). You can pull one from a MIDI file or from a REX loop (Dr. Octo Rex "Copy Loop To Track").

## Recipes that rely on this
`recipes/hiphop/doechii-denial-is-a-river.md` (loose kicks, late snare), `recipes/hiphop/jid-never-story-music-box.md`
(drum bus, shuffle 55-60%, slide a few ticks late), `recipes/feelings/feels-warm-soulful.md`. Those recipes name ReGroove;
this file has the steps. The numbers in them are their authors' reading, not tested.

## Open
- Not yet through the skill-creator benchmark loop (owner's standing rule for new skills).
- Nothing here heard. Slide values in the recipes ("a few ticks") are unmeasured.
