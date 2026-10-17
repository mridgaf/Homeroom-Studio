# Mastering — Genre-Agnostic Template

Mastering is the one "genre" that's meant to work the same way regardless of what you made, so it gets its own file instead of being folded into each genre file.

## Core stock-device mastering chain [Sourced]
Reason's mastering-relevant stock suite has stayed structurally the same across versions: **MClass Equalizer → MClass Stereo Imager → MClass Compressor → MClass Maximizer**, used in the Rack like any other devices (not a special "mastering mode") and typically the last thing in the chain before export. This is Sound on Sound's own documented order and remains valid in Reason 12. [Source: Sound on Sound]

## Cross-check against your own project's master bus technique
Your Hip-Hop Recipe Book's kick-bass relationship recipe (file `06`) already establishes a compatible master-bus approach elsewhere in your system: a gentle compressor (2:1 ratio, slow attack) to glue the mix, followed by a limiter set to a **-0.3 dB ceiling**. That matches the general principle documented independently here (Audeobox's beat-making guide gives the identical -0.3 dB ceiling figure) — two independent sources landing on the same number is a reasonable signal that it's a sound default, not a coincidence worth ignoring. [Sources: Audeobox; your own project memory]

## Sequencing discipline (a real forum disagreement worth knowing about) [Sourced]
A ReasonTalk thread specifically debates whether it makes sense to produce/mix *through* a mastering-style chain from the start, versus adding mastering processing only after the mix is finished. The pushback recorded in the search results is blunt: *"mastering is something you do AFTER you produce and mix... why would you even need any master fx when you're producing?"* This directly supports the phased approach your own project already uses (master bus processing deferred until a body of recipes exists to glue together) — it's not just your working theory, it's a documented position other Reason producers hold too. [Source: ReasonTalk forum, snippet level]

## Template access mechanics in Reason (useful regardless of genre) [Sourced]
Reason ships **factory Song Templates** for specific scenarios including mastering, accessible via **File → New From Template**, separate from the "Default Song" that loads automatically on launch. To add your own mastering template to that list: open the New From Template menu → "Show Template Folder," and drop your own `.reason` file into the folder that opens (Mac: `~/Music/Reason/Template Song`; Windows: `%AppData%\Roaming\Propellerhead Software\Reason\Template Songs`). You cannot create subfolders inside that list, so if you build separate mastering templates per loudness target or genre, name the files distinctly rather than trying to organize them into folders. [Source: Sound on Sound, "Reason: Boost Productivity With Templates"]

## Sources
- Sound on Sound, "Mastering Reason 3 Mixes" (device order still applicable; MClass suite structurally unchanged) — https://www.soundonsound.com/reviews/reason-studios-reason-12 (device list cross-referenced against the Reason 12 review) and general mastering-chain search results
- Sound on Sound, "Reason: Boost Productivity With Templates" — https://www.soundonsound.com/techniques/reason-boost-productivity-templates
- Audeobox, "Beat Making in Reason" (master bus figures) — https://www.audeobox.com/learn/reason/beat-making-in-reason/
- ReasonTalk forum, "Producing through 'mastering' chain?" — search snippet, full thread not independently verified
- Your project memory: `/projects/019e27ff-05fd-7762-ada1-5c8c05a4fa84/overview.md` and `learnings-and-workflow.md`
