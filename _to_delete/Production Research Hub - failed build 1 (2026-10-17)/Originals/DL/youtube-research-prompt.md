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
