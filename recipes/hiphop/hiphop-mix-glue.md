---
name: Hip-Hop Mix Glue
book: hip-hop
sounds_like: a modern rap record — loud, controlled low end, vocal on top
accuracy: B
status: theoretical
source: balanced rough mix, 808 and vocal already sitting right
tags: master bus mix glue hip hop loud low end mclass
technique: mastering triage — low-end control first, loudness last
---
# Hip-Hop Mix Glue — master bus chain

**Accuracy: B** — same MClass honesty as the rock version: capable, characterless. No stock LUFS meter; grab a free VST3 meter (Youlean, $0). Streaming target ≈ -14 LUFS integrated; rap often masters hotter (-9 to -7) accepting platform turndown.

## The Chain
Master insert: MClass Equalizer → MClass Stereo Imager → MClass Compressor → MClass Maximizer

## Steps
1. MClass EQ: Lo Cut OFF (you need the sub!). Param 1: if the 808 is wooly, cut 1–2 dB around 250 Hz. Hi shelf +1 dB at 12 kHz for expensive-sounding air.
2. MClass Stereo Imager: LOW band (below ~150 Hz) width toward mono. Mono bass hits harder everywhere and survives club systems. High band width +10–20%, no more.
3. MClass Compressor: ratio 2:1, slow attack, Adapt release, 1–2 dB reduction. Even in loud rap masters, bus glue stays gentle — loudness comes next, not here.
4. MClass Maximizer: this genre leans on it harder — 3–5 dB of limiting is normal. Look Ahead ON, output -0.3. Listen for 808 distortion; if the sub farts, the limiter is fighting the low end — go back to step 2 and mono/tame the bass more.
5. Volume-matched A/B against a commercial rap reference. Check on earbuds AND anything with a subwoofer: two different low-end realities, both have to work.

## Why this works
Rap masters live or die on low-end management; every step here disciplines the sub before the limiter has to.

## Order of operations
Imager before compressor: mono-ing the bass changes energy the comp reacts to. Maximizer always dead last.

## Reason-specific trick
Save this whole master insert chain as a preset from the master section — every new song starts one click from your mastering baseline.

## RE upgrade path
For A: a modern true-peak limiter VST (many free/cheap) outperforms the 2004-era Maximizer at high limiting depths.

## Technique you just learned
Loudness is earned upstream — a limiter reveals low-end problems, it doesn't solve them.
