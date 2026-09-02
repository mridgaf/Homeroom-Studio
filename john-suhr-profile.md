# Profile — Built from 28 Cowork Sessions

*Compiled by reading the transcripts of every other Cowork session on this account (Aug 2026). This is a working profile grounded in observed behavior and stated preferences, not flattery — where a point is a guess rather than something directly evidenced, it's marked as such.*

## Main project: Homeroom Studio

The dominant thread across sessions, by far. This is a beat-generation software project built on a Mac (M2 Pro), living in a "Homeroom Studio" folder, likely paired with Reason 12 (a DAW) via a "reason-voice" voice-control layer. Key details pulled directly from transcripts:

- The system generates beats using a roster of 11+ named "DJ"/"Legend" personas (Fast Water, Half Light, New Math, etc.), each with a written personality (tempo, timing offsets, instrumentation quirks, mixing choices).
- You've done rigorous QA on it yourself — running scripted audits to check whether a DJ's *written* identity (e.g. "kick stays halftime," "no hat lane") actually survives the `compose()` function, and catching that some traits get overwritten while others (structural absences, timing offsets, mix settings) persist. This is genuine analytical/debugging thinking, not just prompting — you designed a way to falsify claims about your own generator rather than take them on faith.
- Strong, explicit preference for **real sampled audio over synthesized ("fake") instrument sounds**. You issued a formal spec reversing an earlier "don't use loops" instruction, requiring the system to sample trumpet/brass (and other instruments) from your own loop library, pitch-shift them across a range, and use multi-sample mapping instead of one sample stretched too far — and you insisted this multi-sample approach be a *firm requirement*, not a suggestion.
- You maintain a large personal sample/loop library across several external drives and cloud storage — includes a 24,513-file London Symphonic Strings pack, ~485 Cymatics melodic files, 116 loop CDs, several thousand drum-kit one-shots, and MIDI packs. You had Claude inventory this to figure out what real (non-fake) melodic source material you actually own before building a harmony engine.
- You've produced actual output too — e.g., a batch of 5 Tobe Nwigwe-style boom-bap loops (86–94 BPM, minor keys), and a 131-pattern General MIDI drum library organized by genre.
- You care about production authenticity beyond "does it sound okay" — asked for real stereo width (decorrelated reflections, Haas spread) vs. fake-sounding centered mixes, flagged that synthesized snares sound "cleaner" than a chopped breakbeat and wanted them roughed up.
- You had Claude package reusable "skills" out of this project's recurring patterns: safe-file-ops (move-don't-delete, never hard-delete), a MIDI validity checker, a drive-verification method for large slow drives, a safe macOS app-icon swap procedure, and beat-naming/output conventions.

## Other creative/business projects

- **A posthumous-memory / memorial-tech concept** — a physical marker (gravestone-adjacent) linked to a self-authored living message/playlist file, differentiated from existing players (Everplans, StoryFile, HereAfter AI, SafeBeyond) by being *self-curated* rather than survivor-assembled. You had Claude do real competitive/market research (funding history, bankruptcies, acquisition by a preneed funeral-marketing company) and pushed back hard yourself on the subscription pricing model once you saw the category's actual failure patterns — you're willing to kill your own idea's default structure when the evidence says it doesn't fit. Also ran trademark/name-collision checks on candidate names ("iTomb," "Tune Stone") and dropped both once conflicts turned up.
- **"King damned"** — a Peter Thiel-inspired villain character project, used for quote-book generation, villain rap/song composition, and monologue writing across specific tonal registers (sarcastic-motivational, nihilistic, megalomania/fear, etc.). Suggests an active satirical/creative-writing habit separate from music.
- **A band** — you have a Gmail account originally set up for the band that accumulated unrelated personal use over time; you're now working to purge it back to band-only.
- Self-identified role (in your own words, via the "customize Claude to your role" session): music, composing, poetry, digital design, plus marketing/promotion/management — i.e., an independent/self-managed artist handling both the creative and business sides alone.

## Technical profile

- **Genuinely low general computer literacy**, by your own explicit statement ("explain to me like I don't know much about technology... because I don't"). Evidenced repeatedly: needed basic explanations of what Chrome profiles are, what a git "commit" button does ("explain it like I'm five"), what happens when you leave old Cowork sessions open, and needed screenshot-by-screenshot hand-holding to get the Claude Code CLI installed and to distinguish the shell prompt (`$`) from the in-app prompt (`>`) — that distinction alone caused a long troubleshooting session.
- Despite that, you're running a **legitimately technical project**: Python scripts, pytest suites (724+ tests), git, a `.venv`, JSON config files, GM MIDI validation, checksummed drive backups. You don't write the code yourself — you direct Claude Code/Cowork to do it, but you read output critically and push back on it (e.g., rejecting an unverified "HOME MODE" audit column because the assistant admitted it couldn't tell "never happened" from "not logged" apart).
- You explicitly asked about running work more cheaply via lightweight subagents — cost-conscious about token usage, not just throwing spend at the problem.
- You use **both Cowork and Claude Code CLI** for the same project, handing off between them with dense `CLAUDE.md` briefing files so the CLI side doesn't burn tokens re-deriving context.
- Manages a real, nontrivial storage/backup operation: multiple external drives (named "Botc 1," "TBOTC 3"), a cloud drive, careful byte-identical/checksum verification before trusting a backup, and explicit anti-data-loss instincts (you asked for "move to a dated folder," not delete, as the default cleanup pattern, and required a typed confirmation step for anything irreversible).
- Account/identity sprawl: two Gmail accounts + one Hotmail, spread across three Chrome profiles, with Apple ID also tied to the Hotmail address — actively working through consolidating this.

## Working style / what you actually want from Claude

- You state directly (and it shows in these transcripts) that you don't want appeasement — you want facts, and you want disagreement when you're wrong rather than politeness. Several transcripts show the assistant explicitly flagging uncertainty rather than papering over it (e.g., "I don't trust this number yet," "my earlier alarm was wrong, here's why "), which is the behavior pattern you seem to reinforce and get good results from.
- You ask for **plain language explicitly and repeatedly** — not just once. You've told Claude flat out to "keep things simple," "explain like I'm five," and to skip jargon (music-business jargon banned in the villain-quote project too, interestingly — a pattern of wanting authenticity over polish/corporate voice, in both software and creative writing).
- You give tightly scoped, written instructions on iterative work rather than loose asks — the sampling-spec session is a good example: you dictated the exact "do not" boundaries and asked for it saved as a durable `.md` file specifically because your project has previously drifted when the same instruction wasn't written down (loop policy flip-flopped across iterations and confused the coding agent).
- You favor **irreversible-action safety rails** — typed "yes"/"DELETE" confirmations, move-not-delete patterns, checksummed verification before trusting anything — a consistent thread across the beat-cleanup, backup, and skill-building sessions.
- Cross-session consistency: multiple sessions independently reconstruct or hand off the same project state, suggesting you actively manage continuity between Claude sessions yourself (as opposed to expecting memory that isn't there) — which lines up with the "how do I manage multiple sessions" question you asked directly.

## Honest gaps / things not established

- No demographic info (age, location, occupation outside music) surfaced in these transcripts.
- The "band" is mentioned but never named, and no genre/scale info came up.
- No indication of who "King damned" content is for (personal writing, a project pitch, comedy) — just that it's satire aimed at a Thiel-like tech-founder archetype.
- I did not see any conversation resembling a "project" (per your framing, this covers 28 non-project chat sessions) — if you have separate Projects with more/different history, I have no visibility into those from here.

---

*Source: `list_sessions` / `read_transcript` across all 28 local Cowork sessions visible to this account, read in full on 2026-08-11.*
