# Chapter 11: Sonic reference engine and AI assistant research
## Part 3 of 4

_Research on analyzing reference tracks, REAPER control, and AI production assistants; plus the equipment list._

**In this part:**
- ai-assistant-research-findings.md — AI production-assistant — GitHub & YouTube scan, verified
- github-research-prompt.md — Research task: GitHub scan for the AI production-assistant build
- youtube-research-prompt.md — Research task: YouTube scan for the AI production-assistant build
- HANDOFF_3.md — Sonic Reference Engine — handoff brief
- ai-assistant-research-findings.md — AI production-assistant — GitHub & YouTube scan, verified

(Next: Part 4 of 4)


=====================================================
SOURCE FILE: ai-assistant-research-findings.md
ORIGINAL LOCATION: HS:sonic/ai-assistant-research-findings.md
=====================================================

# AI production-assistant — GitHub & YouTube scan, verified

Every link below was checked by hand after the search — fetched the actual page, confirmed it exists, confirmed the numbers. One item was pulled for being unverifiable. Also cross-checked against your actual `Homeroom Studio` folder on your Mac, not just the cloud project docs — two things there changed the picture (see "What your own project already answers" at the bottom).

---

## GitHub — REAPER control (the missing "brain" bridge)

Your hand-written ReaScript bridge already works (19/19 plugins). These are all real, none of them are in your codebase yet. Ranked by how much traction/completeness they have:

1. **[shiehn/total-reaper-mcp](https://github.com/shiehn/total-reaper-mcp)** — 55 stars, 102 commits. Claims 600+ tools, near-total ReaScript coverage, tiered "tool profiles" so an LLM isn't handed everything at once. The most ambitious of the bunch.
2. **[dschuler36/reaper-mcp-server](https://github.com/dschuler36/reaper-mcp-server)** — 103 stars, 14 forks. Smaller scope but purpose-built for exactly your use case: reads .RPP project files, lists installed plugins, and runs audio analysis (peaks, frequency, stereo image, loudness vs streaming targets) for mixing feedback through Claude Desktop. Didn't turn up in the first pass — found it while double-checking a cached search result. **Installed 2026-08-31** — see `experiments/reaper-mcp-server-dschuler36/`.
3. **[bonfire-systems/reaper-mcp](https://github.com/bonfire-systems/reaper-mcp)** — 126 stars, 13 commits. The one already flagged as "unverified, treat as a lead" in your project notes. 58 tools across project/MIDI/FX/mixing/mastering/render/analysis.
4. **[yura9011/scythe_mcp_reaper](https://github.com/yura9011/scythe_mcp_reaper)** — 0 stars, brand new. Different angle: music-theory-aware generation (scales, chord progressions, procedural bass/drum patterns) plus direct Lua execution in REAPER. Worth a look only for the generative angle, not as a bridge replacement.
5. **[Aavishkar-Kolte/reaper-daw-mcp-server](https://github.com/Aavishkar-Kolte/reaper-daw-mcp-server)** — 7 stars. Its own description: "chat with any LLM... the AI agent will understand their musical intentions and make the necessary changes to their REAPER project in real-time" — that's close to word-for-word your brief. Small, unproven, but exactly the shape.

**Reality check:** none of these are obviously better than the bridge you already have working. The honest reason to try one is if its *analysis* tools (loudness/spectrum/stereo checks) save you from writing that part yourself — not to replace the read/write/render loop, which you've already proven.

## GitHub — other pieces

6. **[sergree/matchering](https://github.com/sergree/matchering)** — 2.6k stars, actively maintained. The established reference-matching engine: feed it a target and a reference, it matches RMS, frequency response, peaks, and stereo width. Use its *analysis*, not its auto-correct — genuinely new to your project, nothing like it exists in your codebase.
7. **[Caparrini/mixref](https://github.com/Caparrini/mixref)** — 2 stars, small but on-target: LUFS/true-peak/spectral A/B comparison CLI with JSON output, built by a producer for producers.
8. **[endolith/waveform-analysis](https://github.com/endolith/waveform-analysis)** — 285 stars. Proper THD+N calculator (notches the fundamental, measures what's left). Relevant to the harmonic-metric problem your `analyzer.py` already ran into.
9. **[ZFTurbo/Music-Source-Separation-Training](https://github.com/ZFTurbo/Music-Source-Separation-Training)** — 1.4k stars, active, MIT code. Modern alternative to Demucs (BS-RoFormer, Mel-Band RoFormer) that often separates bass more cleanly. One caveat your own `vox` project's engineering notes already flagged for Demucs — model weights trained on MUSDB18-HQ carry a non-commercial data license; code is MIT but check before assuming the weights are yours to use commercially. Doesn't matter for personal studio use, matters if this ever becomes a product.
10. **[spotify/pedalboard](https://github.com/spotify/pedalboard)** — **you already have this.** It's a dependency in your `vox` project (`vox/src/vox/dsp/pedalboard_modules.py`). Their own code comments flag two real limits: don't use `pedalboard.Limiter` or `pedalboard.Distortion` (both listed as unsuitable), and `pedalboard.Reverb`'s decay floor won't go below ~0.53s. Skip it as a "new find" — you've already hit its edges.
11. **[mclemcrew/MixAssist](https://github.com/mclemcrew/MixAssist)** — 16 stars. Small dataset of 431 real producer-mentor mixing conversations plus 114 mixes with their actual EQ/compression settings. Exactly the "ground truth" category your sonic engine's open questions list is missing — worth a look as a sanity-check set, not as your own ground truth (that has to come from your ear on your material).
12. **[ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp)** — 2.9k stars, the most-forked "LLM reads/writes a live DAW" pattern that exists, just not for your DAW. Worth skimming the tool design, not the code.

**Dropped:** `danielrosehill/Claude-Audio-Production-Plugin` — real repo, but it's ffmpeg-based podcast/voice tooling with no plugin or parameter control. Doesn't touch your barrier.

**If you only look at one thing:** `dschuler36/reaper-mcp-server`. It's the closest match to what your comparator.py needs next (real audio analysis feeding into Claude), it has real traction (103 stars), and it costs you an afternoon to read, not weeks to build. **Update:** installed 2026-08-31 — read-only by design, and its analysis reads pre-FX source files, not what your plugin chain produces. Good second opinion, not a replacement for the render-and-remeasure loop.

---

## YouTube — verified real, titles and channels confirmed

**REAPER + Claude, already wired together:**
- [Giving REAPER a Brain with Claude MCP & ReaScript](https://www.youtube.com/watch?v=4FTXPUpy4zE) — closest match to your exact stack. Description links to working code.
- [How to setup AI MCP server for Reaper DAW (music studio)](https://www.youtube.com/watch?v=5bxSzpGexmo) — install/config walkthrough.
- [Reaper DAW AI agent (MCP Claude)](https://www.youtube.com/watch?v=fn0ln5HUzvA) — second working example, different tool-call design.

**Same pattern, other DAWs (architecture reference only):**
- [Control FL Studio with Claude AI via MCP Servers](https://www.youtube.com/watch?v=2ZtvPF9SAy0)
- [Claude AI & MCPs Music Production in Ableton Live](https://www.youtube.com/watch?v=pnOPZsRuRPY)
- [SnappySnap + Claude AI: A Virtual Collaborator Inside Your DAW](https://www.youtube.com/watch?v=SAmDRL28RKk) — worth watching for how it phrases feedback to the user, since that's your comparator's job too.

**The ceiling of chat-only, no automation:**
- [ChatGPT is The BEST "Plugin" for Mixing Vocals](https://www.youtube.com/watch?v=Kw190r0kBII) — advice-only, no DAW write-back. Shows exactly the gap your "step 5 closes the loop" design is meant to avoid repeating.
- [AI THAT LIVES IN YOUR DAW?? — Meet Meaw: Assist](https://www.youtube.com/watch?v=SZpT7npBjZE) — a commercial mixing-assistant plugin. Useful as "what a polished black-box version looks like," and your brief explicitly rules that shape out.

**Supporting your open problems:**
- [Stem separation tools comparison: Spleeter vs Moises vs Demucs](https://www.youtube.com/watch?v=8knoEaLmEYo) — direct audible comparison, watch specifically for bass/low-end artifacts.
- [EQ matching to a reference by ear](https://www.youtube.com/watch?v=h4OaKYsB7cc) and [Saturation vs. EQ: two ways to get brighter sounds](https://www.youtube.com/watch?v=pEke_GkrP6Y) — both are exactly the "named mechanism" reasoning your comparator needs to produce automatically.

**If you only watch one thing:** the first one — *Giving REAPER a Brain with Claude MCP & ReaScript*. Same stack you're on, already working, links to real code.

---

## What your own project already answers

Checked your Mac folder directly, not just the synced docs:

- **The comparator is already built.** `sonic/HANDOFF.md` shows `comparator.py` done and proven 13/13 by `prove_comparator.py` on synthetic bass. The cloud copy of this doc had gone stale saying "NOT BUILT" — that copy has since been refreshed to match this one.
- **The brightness-metric bug is fixed** — replaced spectral centroid with a band-energy-ratio measure (`analyzer.brightness()`), sine control went 6/7 → 7/7.
- **The top blocker hasn't moved:** every number the comparator has produced so far is synthetic. It still needs one real reference track / your attempt / what failed, from you, before anything above matters.
- **`pedalboard` isn't a new find** — it's already a dependency in your `vox` project, with two known limits already documented there (skip its Limiter and Distortion modules; Reverb decay won't go under ~0.53s).
- **No trace of `matchering`, `total-reaper-mcp`, `dschuler36`, or `scythe_mcp_reaper` anywhere in your codebase** — confirmed genuinely new, not something already tried and dropped.

=====================================================
SOURCE FILE: github-research-prompt.md
ORIGINAL LOCATION: HS:sonic/github-research-prompt.md
=====================================================

# Research task: GitHub scan for the AI production-assistant build

You are researching on behalf of a solo producer building a custom AI "production buddy" — read the background below, then search GitHub and report back. Use WebSearch/WebFetch to actually search — do not answer from memory alone, since repo activity and existence changes.

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

Skip anything generic (tutorials-only repos, "awesome lists" with nothing new, dead repos with zero commits in 2+ years) unless genuinely nothing better exists in that category. End with a 3-5 line "if I only look at one thing" recommendation. Verify every repo you cite actually exists (fetch the page or check via search) before including it — do not include a repo from memory alone.

=====================================================
SOURCE FILE: youtube-research-prompt.md
ORIGINAL LOCATION: HS:sonic/youtube-research-prompt.md
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

## What to search for
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

Skip generic "10 mixing tips" content with nothing specific to AI-assisted or scripted workflows. If a video mentions a tool or plugin not already covered by a parallel GitHub-focused search, call that out clearly since it's the kind of thing text search alone would miss. End with a 3-5 line "if I only watch one thing" recommendation. Verify every video you cite actually exists (check via search) before including it — do not include a video from memory alone.

=====================================================
SOURCE FILE: HANDOFF_3.md
ORIGINAL LOCATION: DL:HANDOFF_3.md
=====================================================

# Sonic Reference Engine — handoff brief

Read this first. It carries decisions, verified results, and known-unverified claims
from the design session. Everything marked UNVERIFIED must be tested, not assumed.

---

## What we're building

A production assistant that:

1. Takes a **reference track** the user likes.
2. Isolates the part he cares about (usually the bassline).
3. Measures it, measures **his** attempt at the same part, and describes the gap
   in plain language with a **named mechanism** — "that's saturation, not EQ."
4. Suggests settings **on plugins he actually owns**.
5. Applies them in the DAW, **re-renders, re-measures, and corrects itself**.

Step 5 is what separates this from every advice-only tool. The loop must close.

**Explicitly out of scope:** push-button "make mine sound like that." Not achievable.
The user stays in the loop making calls. Do not build toward autonomy.

---

## The user

- Non-technical explanations only. Short answers. No hedging, no flattery.
- Produces in **Reason 12**, does not use many factory sounds — he likes the rack
  and the routing, not the library.
- Mac: **Apple Silicon M2**. Demucs runs on MPS.
- Hardware: PreSonus AudioBox 96, Novation Launchkey MK3, Yamaha DTX400K,
  Yamaha EMX66M, Samson Servo 300, assorted guitar amps.
- **Plugin inventory is UNKNOWN.** Ask for it. Nothing downstream works without it.
- He has abandoned several previous attempts because results were unsatisfying.
  Ship something that produces a real, checkable result early.

---

## Decisions made

**DAW: REAPER** (~$60). Chosen for one reason: ReaScript can both read/write every
plugin parameter *and* render audio back to disk. That second half is what lets the
system grade its own work. Reason cannot hand audio back, which is why it can't be
the engine — though he can keep creating in Reason via the Reason Rack Plugin on a
REAPER track.

**Do not buy plugins yet.** REAPER's stock set (ReaEQ, ReaComp, ReaXcomp, etc.) is
free, documented, and cleanly addressable. Prove the loop, then buy for real gaps.

**Stack:** Python, numpy/scipy/soundfile, Demucs for stem separation. No GPU needed.

---

## VERIFIED result — read this before writing any analysis code

`analyzer.py` and `prove.py` are included. `prove.py` synthesizes one bass note through
five treatments (clean, soft saturation, asymmetric saturation, hard clipping, bitcrush)
and checks whether the measurements separate them.

**Run A — pure sine input: 6/7 checks passed.**
The distortion metrics work. Hard clipping read +85 dB odd-dominant. Asymmetric
saturation read +0.6 dB (even harmonics present — the "warm" signature). Bitcrush was
the only treatment flagged inharmonic. THD ranked correctly.

**Run B — realistic sawtooth bass: 3/7 checks passed. Every distortion metric failed.**
Hard clipping measured *lower* THD than the clean signal.

**Why, and this is the central design constraint:**
A real bass already carries ~82% harmonic content before you touch it. Saturation adds
no measurable harmonics on top of that — it compresses, so *relative* harmonic levels
go down. The source's own timbre drowns the effect.

**Consequences:**

- **Never score a sound in isolation.** "This bass is 24% THD, therefore it's clipped"
  is meaningless on real music. Absolute distortion metrics are noise.
- **The comparator is the product, not the analyzer.** Always diff two harmonic
  ladders. The *tilt* of the difference is the signal, not the numbers.
- Referencing isn't a feature of this system. It's the only thing that functions.

**Known bug in the current analyzer:** spectral centroid is used as a brightness proxy,
but saturation sustains the low fundamental on a decaying note and pulls centroid
*down*. Failed in both runs. Measure centroid on the sustain portion, or replace with
band-energy ratios.

---

## UNVERIFIED — test before building on these

- **Reason Rack Plugin parameter exposure.** Claimed from a third-party blog, not
  Reason's docs. Unknown how parameters are exposed to a host, or how many. If it's a
  small fixed bank requiring manual assignment, the Reason-inside-REAPER plan gets
  materially worse. Test early.
- **`bonfire-systems/reaper-mcp`** (~123 stars, 11 commits) was recommended off its
  README. Never run. Treat as a lead, not a dependency. Writing a thin ReaScript
  bridge directly may be cleaner.
- **"Griminess = odd harmonics through 2–3kHz"** was one hypothesis stated too
  confidently. Could equally be bitcrushing, layered noise, amp/cab coloration, tape,
  or a dirty DI. Let the measurements decide, per-case.
- **Stem separation damages the evidence.** A Demucs bass stem carries bleed and
  artifacts, and mastering already reshaped it. Quantify how much this distorts the
  measurements before trusting them.
- **Soloed ≠ in the mix.** The reference bass sounds grimy *against those drums*.
  Matching it soloed can produce something wrong in his mix.

---

## Build order

1. **Comparator** — diff two analyses, output plain-language gap + named mechanism.
   This is the product. Build it before anything else.
2. **Stem pipeline** — Demucs wrapper, MPS on M2. Measure the artifact cost.
3. **Plugin inventory** — scan REAPER's FX list via ReaScript, build JSON of every
   plugin with parameter names and what each knob does sonically. This is the piece
   missing from all his previous attempts, and it's what makes "using the tools at my
   disposal" mean anything.
4. **REAPER bridge** — set parameters, render, re-analyze. Closes the loop.
5. **Brain** — Claude with the above as tools; recipe files as memory.

---

## Reusable from his old `reason_voice` project

Located at `~/Desktop/Homeroom Studio/reason_voice`.

| Keep | Why |
|---|---|
| `recipes.py` | Markdown+YAML recipe format with `accuracy`, `status`, `technique`, `sounds_like`. Correct schema for a knowledge base. Keep the format even if the code is rewritten. |
| `search.py` | Fuzzy + synonym-expanded search |
| `indexer.py` | Drive scanning, tokenizing |
| `crates.py` | Saved collections |
| `static/` | Working web UI |

| Discard | Why |
|---|---|
| `reason_control.py` | 10 MIDI CCs + `open -a Reason`. Dead end. |
| `intents.py` | Regex keyword matching. Replace with an LLM tool-call loop. |
| `midi_ptt.py`, `templates.py` | Reason-specific |

Note: that project had **no LLM in it at all** and no evaluation of whether its advice
was good. Both gaps must be closed here.

---

## Open questions for the user

1. **What plugins do you own?** Blocking everything.
2. **One real case** — a track, the bassline, what you tried, why it failed.
3. **How will you know it's working?** There is currently no ground truth. His old
   recipes had an `accuracy` field he filled in by ear after the fact, which means
   there's no way to tell whether a change improves the system or degrades it.
   Establish a small test set early.

=====================================================
SOURCE FILE: ai-assistant-research-findings.md
ORIGINAL LOCATION: DL:ai-assistant-research-findings.md
=====================================================

# AI production-assistant — GitHub & YouTube scan, verified

Every link below was checked by hand after the search — fetched the actual page, confirmed it exists, confirmed the numbers. One item was pulled for being unverifiable. Also cross-checked against your actual `Homeroom Studio` folder on your Mac, not just the cloud project docs — two things there changed the picture (see "What your own project already answers" at the bottom).

---

## GitHub — REAPER control (the missing "brain" bridge)

Your hand-written ReaScript bridge already works (19/19 plugins). These are all real, none of them are in your codebase yet. Ranked by how much traction/completeness they have:

1. **[shiehn/total-reaper-mcp](https://github.com/shiehn/total-reaper-mcp)** — 55 stars, 102 commits. Claims 600+ tools, near-total ReaScript coverage, tiered "tool profiles" so an LLM isn't handed everything at once. The most ambitious of the bunch.
2. **[dschuler36/reaper-mcp-server](https://github.com/dschuler36/reaper-mcp-server)** — 103 stars, 14 forks. Smaller scope but purpose-built for exactly your use case: reads .RPP project files, lists installed plugins, and runs audio analysis (peaks, frequency, stereo image, loudness vs streaming targets) for mixing feedback through Claude Desktop. Didn't turn up in the first pass — found it while double-checking a cached search result.
3. **[bonfire-systems/reaper-mcp](https://github.com/bonfire-systems/reaper-mcp)** — 126 stars, 13 commits. The one already flagged as "unverified, treat as a lead" in your project notes. 58 tools across project/MIDI/FX/mixing/mastering/render/analysis.
4. **[yura9011/scythe_mcp_reaper](https://github.com/yura9011/scythe_mcp_reaper)** — 0 stars, brand new. Different angle: music-theory-aware generation (scales, chord progressions, procedural bass/drum patterns) plus direct Lua execution in REAPER. Worth a look only for the generative angle, not as a bridge replacement.
5. **[Aavishkar-Kolte/reaper-daw-mcp-server](https://github.com/Aavishkar-Kolte/reaper-daw-mcp-server)** — 7 stars. Its own description: "chat with any LLM... the AI agent will understand their musical intentions and make the necessary changes to their REAPER project in real-time" — that's close to word-for-word your brief. Small, unproven, but exactly the shape.

**Reality check:** none of these are obviously better than the bridge you already have working. The honest reason to try one is if its *analysis* tools (loudness/spectrum/stereo checks) save you from writing that part yourself — not to replace the read/write/render loop, which you've already proven.

## GitHub — other pieces

6. **[sergree/matchering](https://github.com/sergree/matchering)** — 2.6k stars, actively maintained. The established reference-matching engine: feed it a target and a reference, it matches RMS, frequency response, peaks, and stereo width. Use its *analysis*, not its auto-correct — genuinely new to your project, nothing like it exists in your codebase.
7. **[Caparrini/mixref](https://github.com/Caparrini/mixref)** — 2 stars, small but on-target: LUFS/true-peak/spectral A/B comparison CLI with JSON output, built by a producer for producers.
8. **[endolith/waveform-analysis](https://github.com/endolith/waveform-analysis)** — 285 stars. Proper THD+N calculator (notches the fundamental, measures what's left). Relevant to the harmonic-metric problem your `analyzer.py` already ran into.
9. **[ZFTurbo/Music-Source-Separation-Training](https://github.com/ZFTurbo/Music-Source-Separation-Training)** — 1.4k stars, active, MIT code. Modern alternative to Demucs (BS-RoFormer, Mel-Band RoFormer) that often separates bass more cleanly. One caveat your own `vox` project's engineering notes already flagged for Demucs — model weights trained on MUSDB18-HQ carry a non-commercial data license; code is MIT but check before assuming the weights are yours to use commercially. Doesn't matter for personal studio use, matters if this ever becomes a product.
10. **[spotify/pedalboard](https://github.com/spotify/pedalboard)** — **you already have this.** It's a dependency in your `vox` project (`vox/src/vox/dsp/pedalboard_modules.py`). Their own code comments flag two real limits: don't use `pedalboard.Limiter` or `pedalboard.Distortion` (both listed as unsuitable), and `pedalboard.Reverb`'s decay floor won't go below ~0.53s. Skip it as a "new find" — you've already hit its edges.
11. **[mclemcrew/MixAssist](https://github.com/mclemcrew/MixAssist)** — 16 stars. Small dataset of 431 real producer-mentor mixing conversations plus 114 mixes with their actual EQ/compression settings. Exactly the "ground truth" category your sonic engine's open questions list is missing — worth a look as a sanity-check set, not as your own ground truth (that has to come from your ear on your material).
12. **[ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp)** — 2.9k stars, the most-forked "LLM reads/writes a live DAW" pattern that exists, just not for your DAW. Worth skimming the tool design, not the code.

**Dropped:** `danielrosehill/Claude-Audio-Production-Plugin` — real repo, but it's ffmpeg-based podcast/voice tooling with no plugin or parameter control. Doesn't touch your barrier.

**If you only look at one thing:** `dschuler36/reaper-mcp-server`. It's the closest match to what your comparator.py needs next (real audio analysis feeding into Claude), it has real traction (103 stars), and it costs you an afternoon to read, not weeks to build.

---

## YouTube — verified real, titles and channels confirmed

**REAPER + Claude, already wired together:**
- [Giving REAPER a Brain with Claude MCP & ReaScript](https://www.youtube.com/watch?v=4FTXPUpy4zE) — closest match to your exact stack. Description links to working code.
- [How to setup AI MCP server for Reaper DAW (music studio)](https://www.youtube.com/watch?v=5bxSzpGexmo) — install/config walkthrough.
- [Reaper DAW AI agent (MCP Claude)](https://www.youtube.com/watch?v=fn0ln5HUzvA) — second working example, different tool-call design.

**Same pattern, other DAWs (architecture reference only):**
- [Control FL Studio with Claude AI via MCP Servers](https://www.youtube.com/watch?v=2ZtvPF9SAy0)
- [Claude AI & MCPs Music Production in Ableton Live](https://www.youtube.com/watch?v=pnOPZsRuRPY)
- [SnappySnap + Claude AI: A Virtual Collaborator Inside Your DAW](https://www.youtube.com/watch?v=SAmDRL28RKk) — worth watching for how it phrases feedback to the user, since that's your comparator's job too.

**The ceiling of chat-only, no automation:**
- [ChatGPT is The BEST "Plugin" for Mixing Vocals](https://www.youtube.com/watch?v=Kw190r0kBII) — advice-only, no DAW write-back. Shows exactly the gap your "step 5 closes the loop" design is meant to avoid repeating.
- [AI THAT LIVES IN YOUR DAW?? — Meet Meaw: Assist](https://www.youtube.com/watch?v=SZpT7npBjZE) — a commercial mixing-assistant plugin. Useful as "what a polished black-box version looks like," and your brief explicitly rules that shape out.

**Supporting your open problems:**
- [Stem separation tools comparison: Spleeter vs Moises vs Demucs](https://www.youtube.com/watch?v=8knoEaLmEYo) — direct audible comparison, watch specifically for bass/low-end artifacts.
- [EQ matching to a reference by ear](https://www.youtube.com/watch?v=h4OaKYsB7cc) and [Saturation vs. EQ: two ways to get brighter sounds](https://www.youtube.com/watch?v=pEke_GkrP6Y) — both are exactly the "named mechanism" reasoning your comparator needs to produce automatically.

**If you only watch one thing:** the first one — *Giving REAPER a Brain with Claude MCP & ReaScript*. Same stack you're on, already working, links to real code.

---

## What your own project already answers

Checked your Mac folder directly, not just the synced docs:

- **The comparator is already built.** Your local `sonic/HANDOFF.md` (dated 40 minutes later than the copy synced to this project) shows `comparator.py` done and proven 13/13 by `prove_comparator.py` on synthetic bass. The cloud copy of this doc still says "NOT BUILT" — that's stale, not current. Worth re-syncing that doc.
- **The brightness-metric bug is fixed** — replaced spectral centroid with a band-energy-ratio measure (`analyzer.brightness()`), sine control went 6/7 → 7/7.
- **The top blocker hasn't moved:** every number the comparator has produced so far is synthetic. It still needs one real reference track / your attempt / what failed, from you, before anything above matters.
- **`pedalboard` isn't a new find** — it's already a dependency in your `vox` project, with two known limits already documented there (skip its Limiter and Distortion modules; Reverb decay won't go under ~0.53s).
- **No trace of `matchering`, `total-reaper-mcp`, `dschuler36`, or `scythe_mcp_reaper` anywhere in your codebase** — confirmed genuinely new, not something already tried and dropped.

=== END OF PART ===
