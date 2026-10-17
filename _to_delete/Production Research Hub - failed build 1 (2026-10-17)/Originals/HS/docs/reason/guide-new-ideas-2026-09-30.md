# What is NEW in Reason12_HomeroomStudio_Guide.md (checked 2026-09-30)

Source: [Reason12_HomeroomStudio_Guide.md](Reason12_HomeroomStudio_Guide.md). I compared all 29 tips with the skills,
`docs/reason/` notes, `device_refs/` and the Reason 12.7 manual. Nothing below is built or added to a skill yet.
Tags: **Manual** = confirmed in the Reason 12.7 manual. **Unverified** = only the guide says so.

## A. New, and confirmed in the manual (worth adding)

| Idea | The real steps (from the manual, not the guide) | Where it could go | Status |
|---|---|---|---|
| **Make every new song start from your own setup** | Reason menu > Preferences > General tab > "Default Song" > click **Template** > folder icon > pick your song. Untick "Load last song on start-up" or it won't work. Also: File > New from Template > pick one; File > New from Template > Show Template Folder opens the folder where your own songs can be dropped to appear in that menu | New small skill `reason-default-song`, or a section in the template ideas list | Manual |
| **Map any one knob to any one parameter, in one song** | Right-click (Ctrl-click on Mac) the parameter > "Edit Remote Override Mapping" > turn on "Learn From Control Surface Input" > move the knob. Or double-click the parameter, then move the knob. A lightning bolt shows it is mapped. Esc leaves learn mode. "Clear Remote Override Mapping" removes it | New section in `reason-remote-bridge` (it does not mention overrides): a hand-made map for one-off jobs, next to our own `.remotemap` | Manual. I did not check whether it saves with the song |
| **Color tracks** | Edit > Track Color (or the track's right-click menu). It also colors the Audio Track/Mix Channel device and the mixer strip. New clips on that track take the color. The manual also lists an "Auto-color Tracks and Channels" option | One line in `fresh-blank-song` or the template list | Manual |

## B. Not added: you already have it

| Guide tip | Already covered in |
|---|---|
| 9, 12, 29 Combinators, name everything | `demo-song-template-and-automation-ideas.md` (macro-knob box, name-everything rule); skill idea `reason-combinator-macros` |
| 4, 5 Drum and bass chains, sidechain | same file (kick squash chain, pump bus, silent kick trigger, per-channel chain); `drum-loops` skill |
| 13 Edit automation | skill idea `reason-automation-lanes`; hold-a-value clip idea |
| 15 Surface locking | `reason-remote-bridge` rule 4 and `FINDINGS.md` |
| 2, 19 Keyboard control, MIDI keyboard | `FINDINGS.md` (Keyboard Control, Launchkey MK3 factory map) |
| 18 Control surfaces | `FINDINGS.md`, `device_refs/launchkey-mk3.md` |
| 21 CV routing | `demo-song-notes*.md`, skill idea `reason-signal-flow` |
| 22 Parallel processing / sends | "Send-effects trio" and "Pump bus" ideas |
| 23 Master chain | "Master chain" and "Same master Combinator" ideas |
| 16 Naming templates | `Song Starter - Trap` style already in use |
| 8, 10, 11, 27, 28 | Too general to be a skill (color is in table A) |

## C. Conflicts: the guide is wrong or disagrees with you. Do NOT add these

- Guide step 1 says **File > Song Information > Save as Default Song**. That menu item does not exist. Song Information only holds notes. Use the Preferences steps in table A.
- Guide tip 17 puts Mac templates in `Library/Application Support/Propellerhead Software/...`. The manual says the **Template Songs folder in the Music folder** (File > New from Template > Show Template Folder). Your notes already say `~/Music/Reason 12/Template Songs/`.
- Guide tip 15 says **Remote > Settings > Lock Surface**. Not in the manual. Your 2026-09-29 rule: do NOT use Options > Surface Locking; use the device's right-click "Lock ... to This Device".
- Guide tip 2 says map keys to pitch bend, mod wheel and LFO. `FINDINGS.md` says Keyboard Control only toggles switches (min/max), not knobs. Keep the `FINDINGS.md` version.

## D. Not verified, so not added

- **Gamepad control** (tips 3 and 20): needs a third-party app called "Universal Controller MIDI" and a PS5 or Xbox pad. The manual says nothing about it, and I don't know if you own a pad. Idea only, until you say you want it.
- **Live performance rack** (tip 7): you are a studio producer; skip unless you start gigging.
