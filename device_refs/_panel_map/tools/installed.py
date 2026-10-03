import csv,json,re
M={("Instrument","Reason Studios","stock"):["Dr. Octo Rex Loop Player","Europa Shapeshifting Synthesizer","Grain Sample Manipulator","Humana Vocal Ensemble","ID8 Instrument Device","Klang Tuned Percussion","Kong Drum Designer","Malström Graintable Synthesizer","MIDI Out Device","Mimic Creative Sampler","Monotone Bass Synthesizer","NN-XT Advanced Sampler","NN19 Digital Sampler","Pangea World Instruments","Radical Piano","Redrum Drum Computer","Rytmik Drum Machine","SubTractor Analog Synthesizer","Thor Polysonic Synthesizer"],
("Utility","Reason Studios","stock"):["Audio Track","Combinator","Line Mixer 6:2","Matrix Pattern Sequencer","Mix Channel","Mixer 14:2","Pulsar Dual LFO","RPG-8 Monophonic Arpeggiator","Spider Audio Merger & Splitter","Spider CV Merger & Splitter"],
("Player","Reason Studios","stock"):["Beat Map","Drum Sequencer","Dual Arpeggio","Note Echo","Scales & Chords"],
("Effect","Reason Studios","stock"):["Alligator Filter Gate","Audiomatic Retro Transformer","BV512 Digital Vocoder","CF-101 Chorus/Flanger","Channel Dynamics","Channel EQ","COMP-01 Compressor/Limiter","D-11 Foldback Distortion","DDL-1 Digital Delay Line","ECF-42 Envelope Controlled Filter","Master Bus Compressor","MClass Compressor","MClass Equalizer","MClass Maximizer","MClass Stereo Imager","Neptune Pitch Adjuster","PEQ-2 Two Band Parametric EQ","PH-90 Phaser","Pulveriser Demolition","Quartet Chorus Ensemble","RV-7 Digital Reverb","RV7000 MkII Reverb","Scream 4 Distortion","Softube Amp","Softube Bass Amp","Sweeper Modulation Effect","Synchronous Effect Modulator","The Echo","UN-16 Unison"],
("Utility","AirRaid Audio","RE"):["Elements DS-LFO"],("Utility","Groovy Melon","RE"):["Morfin XF Crossfader"],
("Utility","pongasoft","RE"):["A/B 12 Audio Out Switch","A/B Audio & CV Switch","CVA-7 CV Analyzer"],("Utility","Red Rock Sound","RE"):["RE 181 Mid/Side Audio Converter"],
("Utility","Rob Papen","RE"):["RPSpec Spectrogram"],("Utility","Robotic Bean","RE"):["Select CV Switch"],
("Effect","AirRaid Audio","RE"):["Elements Splitter"],("Effect","kiloHearts","RE"):["kHs Chorus"],("Effect","Kuassa","RE"):["Efektor Silencer Noise Gate"],
("Effect","Softube","RE"):["Softube Saturation Knob"],("Effect","ThatMusicCompany","RE"):["Distort Chain","Mr OverDrive","T2 Phaser"],
("Instrument","Applied Acoustics Systems","VST"):["Lounge Lizard Session 4 (VST3)","Strum Session 2 (VST3)","Ultra Analog Session 2 (VST3)"],
("Instrument","XLN Audio","VST"):["Addictive Drums 2 (VST3)","Addictive Keys (VST3)"],
("Effect","AIR Music Technology","VST"):["AIR Multiband Filterbank (VST3)"],("Effect","Atkinson Advanced Modeling, LLC","VST"):["Gateway (VST3)"],
("Effect","BOTC","VST"):["Vox (VST3)"],("Effect","Focusrite","VST"):["FAST Balancer (VST3)","fast-balancer (VST2)"],
("Effect","Newfangled Audio","VST"):["Obliterate (VST3)"],("Effect","Supertone","VST"):["Clear (VST3)"],("Effect","Techivation","VST"):["T-De-Esser (VST3)"],
("Effect","XLN Audio","VST"):["Addictive Trigger (VST3)","DS-10 Drum Shaper (VST3)"]}
inv={r['device_name']:r for r in csv.DictReader(open('inventory.csv'))}
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower().replace('ö','o'))
N={norm(k):k for k in inv}
# exact-after-normalising joins; plus a few hand joins that differ in wording (each listed)
HAND={"RV7000 MkII Reverb":"RV7000 Advanced Reverb","Pulveriser Demolition":None,"Neptune Pitch Adjuster":"Neptune Pitch Adjuster",
"Channel Dynamics":"ChannelDynamics","Channel EQ":"ChannelEQ","Master Bus Compressor":"MasterCompressor","Dr. Octo Rex Loop Player":"Dr.REX Loop Player",
"Alligator Filter Gate":"Alligator","NN19 Digital Sampler":"NN19 Digital Sampler"}
rows=[]
for (cat,maker,kind),names in M.items():
    for n in names:
        v=HAND.get(n) if n in HAND else N.get(norm(n))
        if v is None:
            for k in inv:  # vocab name is the start of the menu name (e.g. "Europa" / "Europa Shapeshifting Synthesizer")
                if len(norm(k))>=4 and norm(n).startswith(norm(k)): v=k;break
        r=inv.get(v,{})
        rows.append(dict(menu_name=n,category=cat,maker=maker,kind=kind,vocab_name=v or "",join=("hand" if n in HAND else ("exact" if N.get(norm(n)) else ("prefix" if v else "none"))),
          vocab_items=r.get('vocab_item_count',''),our_knobs=r.get('our_knob_count',''),guide=r.get('guide_file',''),manual=r.get('manual_chapter','')))
w=csv.DictWriter(open('installed.csv','w',newline=''),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
from collections import Counter
print(Counter(r['kind'] for r in rows), len(rows))
for r in rows:
    if r['kind']!='VST': print(f"{r['kind']:5} {r['menu_name'][:34]:34} -> {r['vocab_name'][:30]:30} [{r['join']}] guide={r['guide']} ch={r['manual'][:3]}")
