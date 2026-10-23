# Chiptune: research transcript, 2026-10-23 (Part 1 of 1)

Fresh research for this genre only. Scope: NES / Famicom first (two squares, triangle, noise), with the Atari 2600 (TIA) as the second chip. Not C64 SID, not Game Boy-only, not "fakebit" synthwave. Owner away; no questions asked (see ASSUMING in the Code handoff).
Tags: [CONFIRMED] = 2+ sources or the person themselves. [UNSURE] = one secondary source, or sources disagree. NOT FOUND = nobody published it.
Tools: WebSearch and WebFetch for pages; the built-in browser for SongBPM (search box, short scripts). 

## Hardware, in plain words
| Fact | Tag | Sources |
|---|---|---|
| NES has 5 channels: 2 pulse (square), 1 triangle, 1 noise, 1 DPCM sample channel | [CONFIRMED] | Wikipedia Ricoh 2A03; nesdev APU page; Linus Akesson; Anamanaguchi interview coverage |
| Pulse duty cycles 12.5 / 25 / 50 / 75% change the tone | [CONFIRMED] | nesdev APU; DDRKirby (uses 25%: "rich and trebly without being too nasal" is his sense, paraphrased) |
| Triangle has no volume control; sounds an octave below a pulse; buzzy | [CONFIRMED] | Wikipedia 2A03; nesdev APU |
| Noise channel (shift register) is the usual hat/cymbal/kick/snare source; the DPCM channel does heavier snares and kicks in some games (SMB3, Kirby's Adventure) | [CONFIRMED] | Wikipedia 2A03; Akesson; DDRKirby; nesdev tips |
| Only about three sounds sound at once for a melody-bass-drum texture (Kondo: "three sounds") | [UNSURE] | Iwata Asks, seen only through a search summary (page failed a certificate check) |
| Atari 2600 TIA: only 2 voices, 5-bit pitch (32 values) so many notes are out of tune; noise and "buzz" tones serve as hat, snare, kick | [CONFIRMED] | Wikipedia TIA; qotile 2600 music guide (Paul Slocum); David Crane quote via AtariAge summary |

## Track table
Credits: [CONFIRMED] where two sources agree. BPM/key from SongBPM unless noted. SongBPM and GetSongBPM both read Spotify data, so they are NOT independent of each other.

| Track | Credit | BPM | Key | Tag |
|---|---|---|---|---|
| Super Mario Bros. ground theme (1985) | Koji Kondo | 100 (Wikipedia, Mario Wiki); SongBPM 99 | C major (Wikipedia, Mario Wiki, SongBPM) | BPM and key [CONFIRMED]. Latin / swing rhythm with syncopation (Wikipedia SMB theme); Kondo drew on T-Square "Sister Marian". |
| Mega Man 2, Dr. Wily Stage 1 (1988) | Takashi Tateishi ("Ogeretsu Kun"), with Manami Matsumae (Wikipedia MM2) | 180 (SongBPM, GetSongBPM) | A (SongBPM) | BPM [UNSURE] (one data origin); song reused for Stage 2 for memory (Wikipedia, Siliconera) |
| Mega Man 2, Metal Man Stage | Tateishi | 150 (SongBPM, original); a cover is 135 | A#/Bb | [UNSURE] one source |
| Castlevania, Vampire Killer (1986) | Kinuyo Yamashita + Satoe Terashima (credit "James Banana") | 128 and 129 (two SongBPM listings), 129 (fan MIDI on midishow, 29 s) | D (SongBPM); fan MIDI says C major | BPM [CONFIRMED] about 128-129; key [UNSURE] (sources disagree) |
| DuckTales, The Moon (1989) | Hiroshige Tonomura (Wikipedia); SongBPM lists Yoshihiro Sakaguchi | 180 (original listing and Jake Kaufman cover both 180) | C#/Db (original listing) | BPM [CONFIRMED]; credit [UNSURE] (Wikipedia vs SongBPM). A leaked prototype was slower (Wikipedia) |
| DDRKirby(ISQ), Face Your Destiny (Level 2), from "Unlock Everything" | DDRKirby(ISQ) | 150 (his own article; levels 100 / 150 / 180) | Dm-Gm-Bb-C | [CONFIRMED] by the artist; this is "fakebit" in FL Studio, noted in his article |
| Chipzel, a modern Game Boy example | Niamh Houston | she wants "around 160" (Cyclic Defrost) | - | [UNSURE] one interview |

Overworld Zelda NES: SongBPM returned only cover or SNES-era entries (122-170, messy). NOT FOUND for the NES original. Contra Jungle: SongBPM returned unrelated songs. NOT FOUND.
Pattern: NES tracks cluster at **100, 128-129, 150, 180**. Median of those five: 150. The engine has 126.

## Tempo
100-180 [CONFIRMED] (five tracks plus DDRKirby's levels). Faster stages and boss themes sit at 150-180; calmer overworld themes at about 100. Older config note carried "usually uptempo" from MusicRadar 2025; I did not reopen that page this session [UNSURE].

## Swing
NES music is sequenced on a 60 Hz frame clock, so it is mechanically straight. The one swing claim found is the Super Mario ground theme ("swing rhythm", Wikipedia). Swing % of any track: NOT FOUND. The existing genre_swing 50 (straight) is consistent with the hardware. [UNSURE]

## Drums
- Noise channel plays kick, closed hat and snare as short noise bursts at different pitches (DDRKirby). [CONFIRMED]
- Noise "is typically used for cymbals and hi-hats", complex snare hits go to the sample channel (Akesson). [CONFIRMED]
- The triangle can do a downward pitch slide as a pitched kick or fill; a Mega Man trademark, "not used on a majority of the songs" (DDRKirby). [UNSURE, one source]
- Atari 2600: "noise" (AUDC 8) for hats, "buzz" for kicks, snare by tuning noise; drums usually sit on the bass voice (qotile guide). [CONFIRMED with TIA Wikipedia for the noise types]
- Chipzel: "I always start with the basics like kick and snare." [CONFIRMED by herself, one person]
- Kick and snare grid: NOT FOUND as a published pattern. Common knowledge says backbeat; no source cited. The existing config is backbeat-heavy.

## Instruments, ranked by what the sources name
1. **Arpeggio standing in for chords**: fast, repeated chord-tone steps. NES composers use it because there are too few voices; confirmed by nesdev forum threads, AllMusic style note (via search summary), Slocum's 2600 guide ("step through chord tones on one voice"), Wikipedia Chiptune ("quick arpeggios are the usual way to simulate polyphony"). [CONFIRMED]
2. **Pulse (square) lead** with duty-cycle tone changes: Wikipedia Chiptune, nesdev, DDRKirby. [CONFIRMED]
3. **Second pulse as echo or staccato support**: a softer, later, slightly detuned repeat of the melody, or short staccato harmony (DDRKirby). [UNSURE, one source; Slocum describes echo on the 2600 too, so [CONFIRMED] as a technique]
4. **Triangle as the bass**, "only on bass notes, a common NES practice" (Akesson, nesdev tips, DDRKirby); Anamanaguchi's Berkman says their triangle waves are an homage to Mega Man (Game Developer). [CONFIRMED]
5. Noise drums (above).
Not in the sources: piano, strings, brass, organ, guitar, choir, pads, wood, bells, vocal chops, vinyl. Real-instrument chord voices are NOT part of the sound.

## Key and chords
Super Mario ground theme: C major (confirmed). Moon: SongBPM C#. Vampire Killer: D by SongBPM, C major by a fan MIDI, and described elsewhere as "spooky minor-key" (AV Club via search summary, single source). DDRKirby's example is minor: Dm-Gm-Bb-C. Verdict: **major AND minor both appear; no source gives a ratio.** [UNSURE]. Chord moves are usually plain triads (arpeggiated), nothing jazzy; no source mentions 7ths or extensions. 

## Bass
Triangle line, often a repeating figure over the chord roots (DDRKirby: repeating bass over i-iv-VI-VII). Each note is short or held per step; no source gives a figure name. On the 2600 the bass shares a voice with drums (Slocum). [CONFIRMED that the bass is a plain, low, single-note line]

## Mix and arrangement
- Dry. The chip has no reverb; "echo" is the second pulse channel playing the same notes later (DDRKirby; Slocum for 2600). [CONFIRMED]
- Rough, aliased, buzzy: the triangle's stepped shape gives a "buzzing quality" (Wikipedia 2A03); the 2600 is out of tune by design (Wikipedia TIA). [CONFIRMED]
- Short loops reused for memory reasons: Wily Stage 1 plays in Stage 2 (Wikipedia, Siliconera); Metroid's Tanaka wanted music that blurs into sound effects (Retrovolve via search summary).
- Sparse sounds: Chipzel: "fill in the gaps with your head" (Cyclic Defrost). One source.

## Who carries it (people who worked in the sound)
| Person | What they said | Source |
|---|---|---|
| Takashi Tateishi (Mega Man 2) | Wanted a band feel as if guitar played it; early drafts "too cute" so he wrote cooler music; influences Mezzoforte and YMO | Brave Wave interview; Wikipedia MM2; SEM interview ("melodies that people could hum") |
| Koji Kondo (Super Mario Bros.) | Wrote the ground theme on a small keyboard; sped it up when the game changed; used Latin rhythm | Wikipedia SMB theme |
| Hip Tanaka (Metroid, Famicom/Game Boy hardware) | Helped design the Famicom audio hardware; "perfect amount of machine noise to resonate with the music" | VGC interview |
| Kinuyo Yamashita (Castlevania) | Composed what felt "natural and fitting"; also made the sound data (engineering role) | SEM interview; Time Extension |
| Niamh Houston / Chipzel | Starts with kick and snare; calls chiptune "the simplest form of music"; likes about 160 BPM | Cyclic Defrost |
| Peter Berkman / Anamanaguchi | Writes with an NES; triangle waves are a Mega Man homage; NES-composers-trying-metal sub-boss theme | Game Developer |
| Paul Slocum / David Crane (Atari 2600) | Drums on the bass voice; out-of-tune notes are the hardware | qotile guide; AtariAge summary |

## Current settings vs research
| Item | Now | Research | Verdict |
|---|---|---|---|
| bpm | 126 | 100 / 128 / 150 / 180; median 150 | LOW end; owner pick (Code handoff) |
| chord_rhythm | arp | arpeggio replaces chords | MATCH |
| chord_source | synth, bell, choir, guitar, horns, organ, pad, piano, pluck, strings, wood each 0.182, midi 0.667 | only synth-like square plucks; nothing in the sources for the 8 non-synth families | **MISMATCH**: 9 instruments the research never names hold 1.64 of 2.67 of the odds (61 percent; midi 25 percent) |
| chord_family | bright_funk (funk/octave bass) | plain triangle line | **MISMATCH** |
| space | dry | no reverb | MATCH |
| genre_swing | 50 | straight hardware | MATCH |
| hat modes | eighths 40, sixteenths 35, sparse 25 | noise hat steps | OK (75 percent steady) |
| kit perc tags | block, click, noise | noise channel | OK |
| kick/snare grammar | backbeat | not published | leave |
| key/mode | major 3, lydian 1, mixolydian 1 | major and minor both appear | **GAP**: no minor at all |
| progressions | many jazz-flavored `plain_*` entries (e.g. plain_secondary, plain_gospel_walk) beside uplifting/epic | plain triads | partly OK; see handoff |
| dust / allow_dirt | 0.25 light crunch | sources say rough and noisy | owner pick of 2026-09-24, left |

## Engine note: chip sounds and the no-machine-tones rule
The engine has a chord voice named `chip` (instrument_sampler VOICES "chip": his own 8-bit files, regex CHIP_RE). His library has **0 chip files** (re-measured 2026-09-26 in DECISIONS: "0 choir, 0 chip"). With 0 files it falls to `tools/chip_synth.py`, a synthesized oscillator. The owner's 2026-09-23 rule bans machine tones, and 2026-09-20 "chip banned for all DJs". So Chiptune stays on `synth` (sampled synth, pluck and pad from his own banks) with `chord_fallback` [bell, pluck]. Nothing in this rebuild turns `chip` on. The genre's real chip character has to come from his sampled synth/pluck/bell material arpeggiated plus noise-like drum samples. Say so out loud to him; it is a limit of his library, not of the research.

## Quality bar
- Sources opened this session (10+ yes): Wikipedia Chiptune, Ricoh 2A03, Mega Man 2, TIA, Super Mario Bros. theme, Kinuyo Yamashita, Vampire Killer (page had no music info), Chipzel, DuckTales; nesdev APU wiki; nesdev tips; Brave Wave (Tateishi); Square Enix Music (Tateishi, Yamashita); Video Games Chronicle (Tanaka); Time Extension (Yamashita); DDRKirby(ISQ) article; Cyclic Defrost (Chipzel); Game Developer (Anamanaguchi); Nintendo World Report (Kaufman, no technique); qotile 2600 music guide; Linus Akesson; SongBPM (5 searches). About 22 pages.
- Seen only through search-engine summaries (not opened): Iwata Asks (certificate error), Inverse/Siliconera/Rockman Corner (Tateishi), Retrovolve/GoNintendo (Tanaka), AtariAge/David Crane, AllMusic style note, Babyaud, midishow, Mario Wiki, Hooktheory, AV Club Castlevania history, Collins "Tuning the Terrible Twos".
- 5+ tracks with credits: yes (6 plus DDRKirby and Chipzel notes).
- BPM from 2 sources: Mario (100), Vampire Killer (128-129), Moon (180 and cover) yes; Wily 1 two listings but one data origin; Metal Man one.
- 2+ people: yes (Tateishi, Kondo, Tanaka, Yamashita, Chipzel, Berkman, Slocum).
- Bar met: yes, with the BPM-independence caveat above.

## Blocked or failed links
- tunebat.com (Cloudflare) not tried. getsongbpm.com song page: 403. iwataasks.nintendo.com: certificate error. musicradar.com article URL I guessed: 404 (a prior session quoted it; I could not reopen it). Wikipedia "Super Mario Bros. (soundtrack)": 404.
- Nothing needs the owner to open, except if he wants the Iwata Asks page: https://iwataasks.nintendo.com/interviews/wii/super-mario-all-stars/0/3

## Source list
https://en.wikipedia.org/wiki/Chiptune | https://en.wikipedia.org/wiki/Ricoh_2A03 | https://en.wikipedia.org/wiki/Mega_Man_2 | https://en.wikipedia.org/wiki/Television_Interface_Adaptor | https://en.wikipedia.org/wiki/Super_Mario_Bros._theme | https://en.wikipedia.org/wiki/Kinuyo_Yamashita | https://en.wikipedia.org/wiki/Chipzel | https://en.wikipedia.org/wiki/DuckTales_(video_game) | https://www.nesdev.org/wiki/APU | https://www.nesdev.org/nt2/tips-tricks.htm | https://bravewave.net/interviews/takashi-tateishi | https://squareenixmusic.com/features/interviews/takashitateishi.shtml | https://squareenixmusic.com/features/interviews/kinuyoyamashita.shtml | https://www.videogameschronicle.com/features/interviews/the-original-game-boy-sounds-the-best-a-very-nerdy-conversation-with-legendary-nintendo-composer-hip-tanaka | https://www.timeextension.com/news/2026/09/i-feel-very-fortunate-castlevanias-kinuyo-yamashita-celebrates-40-years-of-the-vampire-slaying-classic | https://ddrkirby.com/articles/nes-chiptunes-unlock-everything/nes-chiptunes-unlock-everything.html | https://www.cyclicdefrost.com/2015/03/niamh-houston-chipzel-listen-to-the-blips-and-blops-and-fill-in-the-gaps-with-your-head-interview-by-jason-richardson/ | https://www.gamedeveloper.com/audio/interview-anamanaguchi-s-guide-to-i-scott-pilgrim-the-game-i-s-soundtrack | https://www.qotile.net/files/2600_music_guide.txt | https://www.linusakesson.net/music/platform-hopping/index.php | https://www.nintendoworldreport.com/interview/28011/nwr-interview-jake-kaufman | https://songbpm.com (searches for each track)
