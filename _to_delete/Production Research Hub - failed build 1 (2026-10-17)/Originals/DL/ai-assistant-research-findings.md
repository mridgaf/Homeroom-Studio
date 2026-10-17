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
