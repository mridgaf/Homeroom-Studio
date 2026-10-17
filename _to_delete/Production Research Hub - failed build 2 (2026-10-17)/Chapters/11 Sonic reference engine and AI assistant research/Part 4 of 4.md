# Chapter 11: Sonic reference engine and AI assistant research
## Part 4 of 4

_Research on analyzing reference tracks, REAPER control, and AI production assistants; plus the equipment list._

**In this part:**
- youtube-research-prompt.md — Research task: YouTube scan for the AI production-assistant build
- github-research-prompt.md — Research task: GitHub scan for the AI production-assistant build

(Next: end of chapter)


=====================================================
SOURCE FILE: youtube-research-prompt.md
ORIGINAL LOCATION: DL:youtube-research-prompt.md
=====================================================

# Research task: YouTube scan for the AI production-assistant build

You are researching on behalf of a solo producer building a custom AI "production buddy" — read the background below, then search YouTube (and report what you find) for anything relevant.

## The build, in plain terms
The goal: chat with an AI, hand it a reference track, and have it (1) isolate the part he cares about — usually the bassline — (2) measure it against his own attempt, (3) explain the gap in plain language with a named cause ("that's saturation, not EQ" — not just "make it different"), (4) suggest settings on plugins he already owns, (5) actually turn those dials in the DAW, re-render, re-measure, and correct itself. Explicitly NOT wanted: a one-click "make mine sound like that" black box. He wants explanations, not magic, and stays in the loop making the final calls.

## Current stack (already decided, don't relitigate)
- DAW: REAPER, driven by ReaScript (reads/writes plugin parameters, renders audio to disk).
- Python, numpy/scipy/soundfile, Demucs for stem separation. Mac Apple Silicon M2, no GPU.
- No LLM tool-calling loop built yet — that piece is missing.
- A prior attempt used Reason 12 with a thin MIDI bridge and hit a wall — Reason has no scripting API, so that path is dead.

## Known open problems (useful to flag matches against, but this is an open-ended scan — don't limit yourself to these)
1. No reliable way yet to score whether a change actually improved a sound (no ground-truth test set).
2. Distortion/harmonic metrics only work as a comparison between two tracks, not scored alone.
3. Whether Demucs stem separation quietly distorts what's being measured is unknown.
4. No working example yet of an LLM actually driving a DAW end-to-end (propose → apply → re-check).

## What to search for on YouTube
- AI-assisted mixing/mastering workflows (chat-driven, plugin-driven, or otherwise)
- REAPER ReaScript automation walkthroughs — anyone scripting parameter changes or render-and-analyze loops
- Voice- or chat-controlled DAW setups
- Producers/engineers building "match this reference track" tooling, even informally
- Claude/GPT/LLM + music production case studies or demos
- Reviews or comparisons of Demucs / stem separation quality for mixing use (not just remixing for fun)
- Anything showing a practical technique for identifying "what makes this sound X" by ear or by tool, that could sharpen the plain-language explanations this system needs to give

## How to report back
Short, plain-English, non-technical. For each video worth mentioning (aim for 6-12):
- Title + link + channel
- One line: what it shows
- One line: the actual takeaway for this build (a technique, a tool name, a gotcha to avoid)

Skip generic "10 mixing tips" content with nothing specific to AI-assisted or scripted workflows. If a video mentions a tool or plugin not already covered by a parallel GitHub search, call that out clearly since it's the kind of thing text search alone would miss. End with a 3-5 line "if I only watch one thing" recommendation.

=====================================================
SOURCE FILE: github-research-prompt.md
ORIGINAL LOCATION: DL:github-research-prompt.md
=====================================================

# Research task: GitHub scan for the AI production-assistant build

You are researching on behalf of a solo producer building a custom AI "production buddy" — read the background below, then search GitHub and report back.

## The build, in plain terms
The goal: chat with an AI, hand it a reference track, and have it (1) isolate the part he cares about — usually the bassline — (2) measure it against his own attempt, (3) explain the gap in plain language with a named cause ("that's saturation, not EQ" — not just "make it different"), (4) suggest settings on plugins he already owns, (5) actually turn those dials in the DAW, re-render, re-measure, and correct itself. Step 5 — closing the loop — is what makes this different from a normal advice bot. Explicitly NOT wanted: a one-click "make mine sound like that" black box. He stays in the loop and wants explanations, not magic.

## Current stack (already decided, don't relitigate)
- DAW: REAPER — chosen because ReaScript can both read/write every plugin parameter AND render audio to disk, which is what lets the system grade its own work. Confirmed working: 19/19 owned plugins scriptable.
- Python, numpy/scipy/soundfile, Demucs for stem separation. No GPU (Mac Apple Silicon M2, disk space is the tight constraint, not CPU).
- No LLM tool-calling loop is built yet — that's the "brain" piece still missing.
- A prior project (Reason 12 + a 67-line MIDI bridge) hit a wall: Reason has no scripting API at all, can't read the rack, can't set plugin parameters, can't verify anything happened. That's why the move to REAPER.

## Known open problems (useful to flag matches against, but don't limit your search to these — this is an open-ended scan for anything that could help)
1. No ground-truth test set — no reliable way yet to score whether a change actually improved the sound.
2. Distortion/harmonic metrics are unreliable scored in isolation on real (non-sine) audio — differencing two tracks works, scoring one alone doesn't.
3. Stem separation (Demucs) may be distorting the very thing being measured — unquantified.
4. One repo, `bonfire-systems/reaper-mcp`, was flagged early as a possible ReaScript bridge but never actually tested — worth a fresh, honest look (is it maintained, does it do what a hand-rolled bridge already does, is it worth switching to).
5. No LLM-as-brain implementation yet — Claude or similar calling tools to read measurements, propose settings, and drive the DAW.

## What to search for on GitHub
Cast a wide net, but prioritize things that are usable, not just similar in spirit:
- REAPER / ReaScript automation bridges or MCP servers
- LLM tool-calling agents that control a DAW, plugin host, or synth
- Reference-track / mix-comparison / "match this sound" analysis tools
- Harmonic, spectral, or timbral analysis libraries aimed at music production (not generic audio ML)
- Stem separation alternatives or quality improvements to Demucs
- Self-correcting render → analyze → adjust loops (any domain — the pattern matters even outside audio)
- Ground-truth / eval frameworks for audio or mix quality
- Claude/Anthropic (or other LLM) + music production integration examples

## How to report back
Short, plain-English, non-technical. For each repo worth mentioning (aim for 8-15, ranked by usefulness):
- Name + link
- One line: what it does
- One line: how it could plug into this build, or which known problem above it addresses (if any)
- A red flag if there is one (abandoned, unmaintained, no license, toy project)

Skip anything generic (tutorials-only repos, "awesome lists" with nothing new, dead repos with zero commits in 2+ years) unless genuinely nothing better exists in that category. End with a 3-5 line "if I only look at one thing" recommendation.

=== END OF PART ===
