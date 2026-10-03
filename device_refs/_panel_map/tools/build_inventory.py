#!/usr/bin/env python3
"""Build device inventory from files only (no network, no outside knowledge)."""
import json, csv, re, collections
IN = '/home/claude/pmwork/in/'
OUT = '/home/claude/pmwork/out/'

def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())

# ---------- load sources ----------
vocab = json.load(open(IN + 'remote-vocab.json'))['devices']
by_name = collections.defaultdict(list)           # exact name -> [ids]
for vid, d in vocab.items(): by_name[d['name']].append(vid)

guides = open(IN + 'device_refs_list.txt').read().split()
chapters = []
for line in open(IN + 'chapter_pages.tsv'):
    p = line.rstrip('\n').split('\t')
    if len(p) >= 5: chapters.append((int(p[0]), p[1]))

# remotemap: scope blocks + knob counts
scopes = collections.OrderedDict(); cur = None
for line in open(IN + 'ReasonVoice.remotemap'):
    p = line.rstrip('\n').split('\t')
    if p[0] == 'Scope': cur = (p[1], p[2]); scopes[cur] = {'knobs': 0, 'maps': 0}
    elif p[0] == 'Map' and cur:
        scopes[cur]['maps'] += 1
        if re.fullmatch(r'Knob \d+', p[1]): scopes[cur]['knobs'] += 1

# panel map: rows in the Devices table whose Status contains "done"
panel_done = []
sect = False
for line in open(IN + 'PANEL-MAP.md'):
    if line.startswith('## '): sect = line.strip() == '## Devices'
    if sect and line.startswith('|') and 'done' in line.lower():
        panel_done.append(line.split('|')[1].strip())

# ---------- hand-written judged tables ----------
# Targets are vocab ids. Method (exact / prefix / judged) is computed below; the
# 'why' text is used for anything that is not exactly equal after normalisation.
V = lambda name: by_name[name]
GUIDE_MAP = {  # guide slug -> (vocab ids, why-if-judged)
 'alligator':(['Alligator'],''), 'audiomatic':(['se.propellerheads.Audiomatic'],''),
 'bv512':(['BV512 Digital Vocoder'],''), 'cf-101':(['CF-101 Chorus/Flanger'],''),
 'channel-dynamics':(['se.propellerheads.ChannelDynamics'],''), 'channel-eq':(['se.propellerheads.ChannelEQ'],''),
 'combinator':(['Combinator'],''), 'comp-01':(['COMP-01 Compressor/Limiter'],''),
 'd-11':(['D-11 Foldback Distortion'],''), 'ddl-1':(['DDL-1 Digital Delay Line'],''),
 'dr-octo-rex':(['Dr.REX Loop Player'],'guide slug "dr-octo-rex" vs vocab "Dr.REX Loop Player"; manual ch.29 is titled "Dr. Octo Rex Loop Player", sharing "Dr." and "Rex" - same device by name similarity'),
 'ecf-42':(['ECF-42 Envelope Controlled Filter'],''), 'europa':(['se.propellerheads.Europa'],''),
 'grain':(['se.propellerheads.Grain'],''), 'humana':(['se.propellerheads.Humana'],''),
 'id8':(['ID8 Instrument Device'],''), 'klang':(['se.propellerheads.Klang'],''),
 'kong':(['Kong Drum Designer'],''),
 'malstrom':(['Malstrom Graintable Synthesizer'],''),
 'master-bus-compressor':(['se.propellerheads.MasterCompressor'],'guide "Master Bus Compressor" vs vocab "MasterCompressor": different wording, same words Master+Compressor; ch.59 is "Master Bus Compressor"'),
 'matrix':(['Matrix Pattern Sequencer'],''),
 'mclass-compressor':(['MClass Compressor'],''), 'mclass-equalizer':(['MClass Equalizer'],''),
 'mclass-maximizer':(['MClass Maximizer'],''), 'mclass-stereo-imager':(['MClass Stereo Imager'],''),
 'mimic':(['se.propellerheads.Mimic'],''), 'mixer-14-2':(['Mixer 14:2'],''),
 'monotone':(['se.propellerheads.Monotone'],''), 'neptune':(['Neptune Pitch Adjuster'],''),
 'nn-19':(['NN19 Digital Sampler'],''), 'nn-xt':(['NN-XT Advanced Sampler'],''),
 'pangea':(['se.propellerheads.Pangea'],''), 'peq-2':(['PEQ-2 Two Band Parametric EQ'],''),
 'ph-90':(['PH-90 Phaser'],''), 'pulsar':(['se.propellerheads.Pulsar'],''),
 'pulveriser':(['Pulveriser'],''), 'quartet':(['se.propellerheads.Quartet'],''),
 'radical-piano':(['se.propellerheads.radicalpiano'],'vocab also has RadicalKeys/radicalkeys (different names); only "radicalpiano" matches the slug'),
 'redrum':(['Redrum Drum Computer'],''), 'rpg-8':(['RPG-8 Monophonic Arpeggiator'],''),
 'rv-7':(['RV-7 Digital Reverb'],''),
 'rv7000-mkii':(['RV7000 Advanced Reverb'],'guide "RV7000 Mk II" vs vocab "RV7000 Advanced Reverb": share "RV7000"; ch.53 title is "RV7000 Mk II Advanced Reverb"'),
 'scream-4':(['Scream 4 Distortion'],''), 'subtractor':(['SubTractor Analog Synthesizer'],''),
 'sweeper':(['se.propellerheads.Sweeper'],''), 'synchronous':(['se.propellerheads.Synchronous'],''),
 'the-echo':(['The Echo'],''), 'un-16':(['UN-16 Unison'],''),
 'thor':(['Thor Polysonic Synthesizer'],'vocab has two ids that differ only by case ("THOR..." 207 items, "Thor..." 369 items); attached to the "Thor" one, which is the exact-case name used in our remotemap'),
}
HARDWARE = ['audiobox-96','launchkey-mk3','yamaha-dtx400k','yamaha-emx66m','samson-servo-300']  # per task text
UNDECIDED_GUIDES = {'guitar-amps': 'File name only; no vocab device name or manual title says "guitar amp". Could cover Line 6 Guitar/Bass Amp, ReasonAmp/ReasonBassAmp, or ch.55 Softube Amps - cannot tell from files.'}
NEW_ROW_GUIDES = {'rytmik': 'Rytmik Drum Machine'}  # guide whose device is not in vocab; name from manual ch.38 title

CH_MAP = {  # chapter number -> (vocab ids, why-if-judged, group?)
 27:(['Kong Drum Designer'],'',0), 28:(['Redrum Drum Computer'],'',0),
 29:(['Dr.REX Loop Player'],'title "Dr. Octo Rex Loop Player" vs vocab "Dr.REX Loop Player": same "Dr." / "Rex" / "Loop Player" words',0),
 30:(['se.propellerheads.Europa'],'',0), 31:(['se.propellerheads.Grain'],'',0), 32:(['se.propellerheads.Mimic'],'',0),
 33:(['Thor Polysonic Synthesizer'],'',0),
 34:(['SubTractor Analog Synthesizer'],'title "Subtractor Synthesizer" vs "SubTractor Analog Synthesizer": same word Subtractor + Synthesizer (case differs, "Analog" extra)',0),
 35:(['Malstrom Graintable Synthesizer'],'title "Malström Synthesizer" vs "Malstrom Graintable Synthesizer": diacritic differs, "Graintable" extra',0),
 36:(['se.propellerheads.Monotone'],'',0), 37:(['ID8 Instrument Device'],'',0),
 39:(['se.propellerheads.radicalpiano'],'',0), 40:(['se.propellerheads.Klang'],'',0),
 41:(['se.propellerheads.Pangea'],'',0), 42:(['se.propellerheads.Humana'],'',0),
 43:(['NN-XT Advanced Sampler'],'title "NN-XT Sampler" vs "NN-XT Advanced Sampler": "Advanced" extra',0),
 44:(['NN19 Digital Sampler'],'title "NN-19 Sampler" vs "NN19 Digital Sampler": hyphen and "Digital" differ',0),
 46:(['se.propellerheads.Quartet'],'',0), 47:(['se.propellerheads.Sweeper'],'',0), 48:(['Alligator'],'',0),
 49:(['Pulveriser'],'',0), 50:(['The Echo'],'',0),
 51:(['Scream 4 Distortion'],'title "Scream 4 Sound Destruction Unit" vs "Scream 4 Distortion": share "Scream 4"',0),
 52:(['BV512 Digital Vocoder'],'title "BV512 Vocoder" vs "BV512 Digital Vocoder": "Digital" extra',0),
 53:(['RV7000 Advanced Reverb'],'title "RV7000 Mk II Advanced Reverb" vs "RV7000 Advanced Reverb": "Mk II" extra',0),
 54:(['Neptune Pitch Adjuster'],'',0), 56:(['se.propellerheads.Audiomatic'],'',0),
 57:(['se.propellerheads.ChannelDynamics'],'',0), 58:(['se.propellerheads.ChannelEQ'],'',0),
 59:(['se.propellerheads.MasterCompressor'],'title "Master Bus Compressor" vs "MasterCompressor": "Bus" extra, spacing differs',0),
 60:(['se.propellerheads.Synchronous'],'',0),
 61:(['MClass Compressor','MClass Equalizer','MClass Maximizer','MClass Stereo Imager'],'group chapter "The MClass Effects": every vocab device whose name starts "MClass"',1),
 62:(['CF-101 Chorus/Flanger','COMP-01 Compressor/Limiter','D-11 Foldback Distortion','DDL-1 Digital Delay Line','ECF-42 Envelope Controlled Filter','PEQ-2 Two Band Parametric EQ','PH-90 Phaser','RV-7 Digital Reverb','UN-16 Unison'],
    'group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text',1),
 63:(['Combinator'],'',0), 64:(['se.propellerheads.Pulsar'],'',0),
 65:(['RPG-8 Monophonic Arpeggiator'],'title "RPG-8 Arpeggiator" vs "RPG-8 Monophonic Arpeggiator": "Monophonic" extra',0),
 66:(['Matrix Pattern Sequencer'],'',0), 67:(['Mixer 14:2'],'',0), 68:(['Line Mixer 6:2'],'',0),
 22:(['ReGroove Mixer'],'title "The ReGroove Mixer" vs "ReGroove Mixer": leading "The"',0),
}
NEW_ROW_CHAPTERS = {38:'Rytmik Drum Machine', 45:'MIDI Out Device', 55:'Softube Amps'}
CH_TITLE = dict(chapters)

# resolve vocab keys (name or id) -> id. THOR/Thor names: 'Thor Polysonic Synthesizer' unique exact-case.
def resolve(key):
    if key in vocab: return key
    ids = by_name[key]
    assert len(ids) == 1, (key, ids)
    return ids[0]

rows = collections.OrderedDict()
for vid, d in vocab.items():
    rows[vid] = dict(device_name=d['name'], manufacturer=d['manufacturer'], in_remote_vocab='yes',
        vocab_item_count=len(d['items']), in_our_remotemap='no', our_knob_count='', guide_file='none',
        manual_chapter='none', panel_map_status='not started', notes=[])
    if len(by_name[d['name']]) > 1 or any(o != vid and vocab[o]['name'].lower() == d['name'].lower() for o in vocab):
        rows[vid]['notes'].append(f'vocab id "{vid}"; another vocab id has the same name ignoring case (kept as separate rows)')
    elif vid != d['name']:
        rows[vid]['notes'].append(f'vocab id "{vid}"')

judged = []   # (kind, source, device, how, reason)
def method(label, devname):
    a, b = norm(label), norm(devname)
    if a == b: return 'exact (same after ignoring case/punctuation)'
    if a.startswith(b) or b.startswith(a): return 'prefix (one name starts with the other)'
    return 'judged'
def record(kind, src, vid, why, label):
    m = method(label, vocab[vid]['name'])
    if not m.startswith('exact'):
        judged.append((kind, src, vocab[vid]['name'], m, why or 'one name is the start of the other'))
    return m

# remotemap join
unmatched_scopes = []
for (mf, nm), s in scopes.items():
    if nm in vocab and vocab[nm]['name'] != nm: vid = nm; how = 'scope name = vocab id'
    elif nm in vocab: vid = nm; how = 'scope name = vocab id and name'
    elif len(by_name.get(nm, [])) == 1: vid = by_name[nm][0]; how = 'scope name = vocab name'
    else: unmatched_scopes.append((mf, nm)); continue
    r = rows[vid]
    if vocab[vid]['manufacturer'] != mf: r['notes'].append(f'remotemap manufacturer "{mf}" differs from vocab "{vocab[vid]["manufacturer"]}"')
    r['in_our_remotemap'] = 'yes'; r['our_knob_count'] = s['knobs']
    r['notes'].append(f'remotemap: exact ({how}); {s["maps"]} Map lines total')
if unmatched_scopes: raise SystemExit(f'UNMATCHED SCOPES {unmatched_scopes}')
for r in rows.values():
    if r['in_our_remotemap'] == 'no': r['our_knob_count'] = 0

# guides
hardware_found = []; undecided = []
extra = collections.OrderedDict()   # rows not in vocab
for g in guides:
    slug = g[:-3]
    if slug in GUIDE_MAP:
        ids, why = GUIDE_MAP[slug]
        for key in ids:
            vid = resolve(key); r = rows[vid]
            m = record('guide', g, vid, why, slug)
            r['guide_file'] = g
            r['notes'].append(f'guide: {m}' + (f' - {why}' if why else ''))
    elif slug in HARDWARE: hardware_found.append(g)
    elif slug in NEW_ROW_GUIDES: pass
    elif slug in UNDECIDED_GUIDES: undecided.append((g, UNDECIDED_GUIDES[slug]))
    else: raise SystemExit('unclassified guide ' + g)
for g, nm in NEW_ROW_GUIDES.items():
    assert g + '.md' in guides
    extra[nm] = dict(device_name=nm, manufacturer='unknown', in_remote_vocab='no', vocab_item_count=0,
        in_our_remotemap='no', our_knob_count=0, guide_file=g + '.md', manual_chapter='none',
        panel_map_status='not started', notes=[f'not in remote-vocab; name taken from manual ch.38 title; guide joined by judged match: slug "{g}" vs title "{nm}" (prefix)'])
    judged.append(('guide', g + '.md', nm, 'prefix (one name starts with the other)', 'no vocab device; row created from manual chapter title'))

# chapters
for n, title in chapters:
    if n in CH_MAP:
        ids, why, grp = CH_MAP[n]
        for key in ids:
            vid = resolve(key); r = rows[vid]
            m = record('chapter', f'ch.{n} {title}', vid, why, title) if not grp else None
            if grp:
                m = 'judged'; judged.append(('chapter', f'ch.{n} {title}', vocab[vid]['name'], 'judged (group chapter)', why))
            r['manual_chapter'] = f'{n} {title}'
            r['notes'].append(f'chapter: {m}' + (' - via chapter title' if grp else '') + (f' - {why}' if why and not grp else ''))
            if grp and n == 62: r['notes'].append('chapter 62 membership unverified (see report)')
    elif n in NEW_ROW_CHAPTERS:
        nm = NEW_ROW_CHAPTERS[n]
        if nm in extra:
            extra[nm]['manual_chapter'] = f'{n} {title}'; extra[nm]['notes'].append(f'chapter: exact (title = name)')
        else:
            note = {55: 'group chapter "Softube Amps" (via chapter title). No vocab device name says Softube, so which devices it covers is unknown; no vocab/guide joined. Row represents the chapter only.',
                    45: 'not joined to any vocab device (possible vocab "externalmidiinstrument" not asserted); row represents the chapter only.'}[n]
            extra[nm] = dict(device_name=nm, manufacturer='unknown', in_remote_vocab='no', vocab_item_count=0,
                in_our_remotemap='no', our_knob_count=0, guide_file='none', manual_chapter=f'{n} {title}',
                panel_map_status='not started', notes=[note])

# panel map
for name in panel_done:
    ids = by_name.get(name, [])
    if len(ids) == 1:
        rows[ids[0]]['panel_map_status'] = 'done'; rows[ids[0]]['notes'].append(f'panel map: done (PANEL-MAP.md Devices table row "{name}", exact vocab name)')
    else: raise SystemExit('panel-map device not matched: ' + name)

allrows = list(rows.values()) + list(extra.values())
cols = ['device_name','manufacturer','in_remote_vocab','vocab_item_count','in_our_remotemap','our_knob_count','guide_file','manual_chapter','panel_map_status','notes']
with open(OUT + 'inventory.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in allrows:
        r = dict(r); r['notes'] = '; '.join(r['notes']); w.writerow(r)

# ---------- report ----------
PH = {'Propellerhead Software', 'Propellerheads'}
inv = [r for r in allrows if r['in_remote_vocab'] == 'yes']
mf = collections.Counter(r['manufacturer'] for r in inv)
L = []
L.append('# Device inventory report\n\nBuilt by build_inventory.py from the files in /home/claude/pmwork/in only. Being in remote-vocab means "Reason has a Remote map for it", not that the owner has it.\n')
L.append('## Counts\n')
L.append(f'- Rows in inventory.csv: {len(allrows)} ({len(inv)} from remote-vocab ids + {len(extra)} not in remote-vocab: {", ".join(extra)})')
L.append(f'- In remote-vocab: {len(inv)} (one row per vocab id; vocab file says device_count = {json.load(open(IN+"remote-vocab.json"))["device_count"]})')
L.append(f'- Made by Propellerheads / Propellerhead Software (manufacturer strings in the file; "Reason Studios" does not appear in the file): {sum(v for k,v in mf.items() if k in PH)}; other makers: {sum(v for k,v in mf.items() if k not in PH)}')
L.append(f'- With our guide: {sum(r["guide_file"]!="none" for r in allrows)} rows ({len(guides)} guide files total: {sum(r["guide_file"]!="none" for r in allrows)} joined, {len(hardware_found)} hardware, {len(undecided)} undecided)')
L.append(f'- With our remotemap scope: {sum(r["in_our_remotemap"]=="yes" for r in allrows)} (of {len(scopes)} scopes in the file; all {len(scopes)} matched a vocab entry)')
L.append(f'- With a manual chapter: {sum(r["manual_chapter"]!="none" for r in allrows)}')
L.append(f'- Panel map done: {sum(r["panel_map_status"]=="done" for r in allrows)} ({", ".join(panel_done)}); all others not started')
L.append('\n## Guides that matched no Reason device (hardware)\n')
L += [f'- {g}' for g in hardware_found]
L.append('\n(Classified as hardware from the task statement: launchkey-mk3, yamaha-*, samson-*, audiobox-96. No vocab name or chapter title matches any of them.)')
L.append('\n## Remote-vocab manufacturers (device count = vocab ids)\n')
L.append('| Manufacturer | Devices |\n|---|---|')
L += [f'| {k} | {v} |' for k, v in mf.most_common()]
L.append('\n## Judged name matches (everything not exactly equal after ignoring case/punctuation)\n')
L.append('Method labels: "prefix" = one normalised name starts with the other (still a judgment, listed for completeness); "judged" = names differ in wording. All other joins (remotemap scopes, exact guide/chapter names) were exact.\n')
L.append('| Kind | Source | Joined to (vocab name) | Method | Reason |\n|---|---|---|---|---|')
for k, s, d, m, why in judged: L.append(f'| {k} | {s} | {d} | {m} | {why} |')
L.append('\n## Could not decide\n')
for g, why in undecided: L.append(f'- Guide {g}: {why}')
L.append('- Manual ch.55 Softube Amps: group chapter whose members cannot be read from the files; kept as its own row (manufacturer unknown) and NOT joined to ReasonAmp / ReasonBassAmp / Line 6 Guitar Amp / Line 6 Bass Amp.')
L.append('- Manual ch.62 Half-Rack Effects: title lists no devices. Assigned to the 9 hyphen-coded vocab devices (CF-101, COMP-01, D-11, DDL-1, ECF-42, PEQ-2, PH-90, RV-7, UN-16) by name pattern only; membership is a guess until checked against the chapter text.')
L.append('- Manual ch.45 MIDI Out Device: not joined to any vocab device; a vocab entry "externalmidiinstrument" exists but nothing in the files links them. Chapter row stands alone.')
L.append('- Manual ch.38 Rytmik Drum Machine: no vocab entry; guide rytmik.md joined to it by name (prefix) only. Manufacturer unknown.')
L.append('- Duplicate-name vocab ids (kept as separate rows, not merged): ' + '; '.join(
    f'{a} / {b}' for a, b in [(x, y) for x in vocab for y in vocab if x < y and vocab[x]['name'].lower() == vocab[y]['name'].lower()]) + '. Guide/chapter attached only to "Thor Polysonic Synthesizer" (exact-case name in our remotemap) and to radicalpiano; the other-case ids have none.')
L.append('- Names that look like they might be the same product but are different vocab names and were NOT merged: "Dr.REX Loop Player" vs chapter 29 (merged, see judged table); RadicalKeys / radicalkeys / radicalpiano (only radicalpiano joined); Reason Document / Reason Master Section etc. are in our remotemap but have no guide or chapter - whether they are rack devices is not stated in the files.')
L.append('- Chapters 17 (The Main Mixer) and others were not joined to "Reason Main Mixer Channel"/"Reason Master Section" vocab entries; nothing in the files ties them.')
open(OUT + 'inventory_report.md', 'w').write('\n'.join(L) + '\n')
print(len(allrows), 'rows')
