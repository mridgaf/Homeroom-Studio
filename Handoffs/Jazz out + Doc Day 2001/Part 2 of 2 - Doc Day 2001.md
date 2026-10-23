# Doc Day 2001 settings (Part 2 of 2)

Do Part 1 (jazz out) first. It already turns off Doc Day's jazz coloring and repoints his deep loops.

Done in Cowork, 2026-10-23:
- Doc Day's `listen` line in legends_config.json is rewritten for the 2001 era, in the engine's own words. Each phrase maps to one setting; the map is at the end of Doc Day's `_research_note`.
- Research: `Claude outputs/Dr Dre 2001 research transcript.md` (Part 11 compares the research to the current settings).
- Backups: legends_config.pre-doc-day-2001-2026-10-23.json (original), legends_config.pre-doc-day-vocab-2026-10-23.json (before the second rewrite).
- Logged in DECISIONS.md (two entries, 2026-10-23).

To do (use the dj-rebuild skill, Part 4; the listen line is the top rule):
1. Make the settings match the line, phrase by phrase:
   - "90-95 BPM, home 94" -> signature.tempo [90, 95], bpm 94
   - "minor key" -> key.mode minor (replaces dorian/mixolydian)
   - "i to v, iv to i, or one chord held" -> progressions lead with vamp_i_v7, vamp_i_iv7, vamp_static_riff (G-funk ones out or down)
   - "sparse claps for percussion" -> a clap lane, grammar sparse; tambourine/shaker/cowbell lane out
   - "bass follows the kick" -> bass figure "kick" leads
   - "piano ... short staccato stabs" + "strings held" -> chord figures stab + sustain
   - Chord odds, owner's pick MIDDLE GROUND: piano and strings get a bigger share for Doc Day only, other families stay possible. Exception to the 2026-09-25 equal-families rule. Any weight number is your pick: say so.
   - "closed tight hats in eighths" -> hat grammar eighths is only 0.5 now, so raise it so the line holds most of the time (any number is your pick: say so)
   - "bass follows the kick": list his electric-bass / bassline samples (instrument folders on TBOTC 3). 2001 bass is live electric bass, not 808. If he owns none, report it. Don't fake it with the 808
   - MIDI chord packs (his share is about 1 beat in 4): owner has no preference. Leave the share, but CHECK whether MIDI chords follow his vamp loops and report the answer
   - Swing: no reference audio, owner skipped measuring. legend_swing stays 50
   - Already matching, leave alone: space dry, glue, transient, sub_layer, closed hat tags, kick tags thump/hard (a test pins them), snare_locked_24 ("NEVER leaves 2 and 4")
2. Check tags against real filenames: legend_newbuild.py --tags.
3. Run tools/identity_survival.py --dj "Doc Day" --legends. Any phrase in the line that survives less than half the time gets fixed or reported.
4. Run the full test suite ONCE, alone (covers Parts 1 and 2).
5. DO NOT RENDER. Owner rule: never render unless he asks. Report what changed (numbers) and ask him whether he wants an old-vs-new audition.
