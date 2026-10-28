import json,glob,os,re,sys,collections,csv,struct
base=os.path.expanduser('~/mnt/Homeroom Rhythms/.recipes')
out=os.path.expanduser('~/mnt/Homeroom Studio/Claude outputs/usage-data')
NN=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def nn(n): return f"{NN[n%12]}{n//12-1}"
def pc(n): return NN[n%12]
def base_(p): return os.path.splitext(os.path.basename(p))[0] if p else None
recs={}
for f in glob.glob(base+'/*.json'):
    try: recs[os.path.splitext(os.path.basename(f))[0]]=json.load(open(f))
    except Exception: pass
def kind(r):
    p=r['preset']
    if p.get('legend'): return 'Legend'
    if p.get('genre'): return 'Genre'
    return 'Crew DJ / early'
def mode(r):
    kp=r.get('kit_paths',{})
    hasloop=any(k in kp for k in('bassloop','leadloop','chordloop','percloop','vocalloop','fxloop'))
    if r.get('loops_only'): return 'Loops only'
    return 'Original + loops' if hasloop else 'Original'
agg=collections.Counter()
beats=[]
def add(cat,item,r,m,n=1):
    if item is None or item=='': return
    agg[(cat,str(item),r['folder'],kind(r),m,r['date'][:7])]+=n
for rid,r in recs.items():
    m=mode(r); h=r.get('harmony') or {}
    beats.append([rid,r['folder'],kind(r),m,r['date'],r['bpm'],h.get('key',''),h.get('progression',''),h.get('rhythm','')])
    for l in r.get('lanes') or []: add('Lane (instrument slot)',re.sub(r'v\d$','',l),r,m)
    for lane,p in r.get('kit_paths',{}).items():
        b=base_(p)
        if lane.endswith('loop') or lane.startswith('loop') or lane in('percloop','vocalloop','fxloop2'): add('Loop',f"{lane}: {b}",r,m)
        elif lane in('kick','snare','clap','hat','closed_hat','open_hat','snap','kicklayer','kickpunch','ride'): add('Drum sample '+lane,b,r,m)
        else: add('Other one-shot sample',f"{lane}: {b}",r,m)
    if h:
        add('Key',h.get('key'),r,m); add('Chord progression',h.get('progression'),r,m); add('Chord rhythm pattern',h.get('rhythm'),r,m)
        for c in h.get('chords',[]):
            v=c.get('voice') or ''
            add('Chord voice (full)',v,r,m); add('Chord voice (family)',v.split(' ')[0],r,m)
            add('Chord name',c.get('chord'),r,m); add('Chord function',c.get('roman'),r,m)
            for n in c.get('notes',[]): add('Chord note (with octave)',nn(n),r,m); add('Chord note (name only)',pc(n),r,m)
            if c.get('bass') is not None: add('Bass note (with octave)',nn(c['bass']),r,m); add('Bass note (name only)',pc(c['bass']),r,m)
        for bf in h.get('bass_figures') or []: add('Bass pattern',bf,r,m)
        for vf in (h.get('voice_files') or {}).values():
            for p in vf: add('Chord instrument sample',base_(p),r,m)
        if h.get('bass_file'): add('Bass sound',base_(h['bass_file']),r,m)
        if h.get('bass808'): add('808 sound',base_(h['bass808']),r,m)
        fl=h.get('flow') or {}
        if fl.get('voicing'): add('Chord voicing style',fl['voicing'],r,m)
        mel=h.get('melody')
        if mel:
            add('Melody instrument',mel.get('instrument','').split('/')[-1],r,m)
            add('Melody instrument group',mel.get('group'),r,m)
            for nt in mel.get('notes',[]):
                add('Melody note (with octave)',nn(nt[3]),r,m); add('Melody note (name only)',pc(nt[3]),r,m)
        for mv in (h.get('arrangement') or {}).get('moves',[]): add('Arrangement move',mv.get('kind'),r,m)
    g=r['preset'].get('chord_grammar') or {}
    for fg in g.get('figures',[]): add('Chord figure type',fg[0],r,m)
    for k,v in (r['preset'].get('grammar') or {}).items():
        for md in v.get('modes',[]) if isinstance(v,dict) else []: add(f'Drum pattern mode ({k})',md[0],r,m)
    if r['preset'].get('break_name'): add('Break sample',r['preset']['break_name'],r,m)
# drum MIDI
def midi_notes(path):
    d=open(path,'rb').read(); c=collections.Counter()
    if d[:4]!=b'MThd': return c
    ntr=struct.unpack('>H',d[10:12])[0]; pos=14
    for _ in range(ntr):
        if d[pos:pos+4]!=b'MTrk': break
        ln=struct.unpack('>I',d[pos+4:pos+8])[0]; t=d[pos+8:pos+8+ln]; pos+=8+ln; i=0; run=0
        while i<len(t):
            while t[i]&0x80: i+=1
            i+=1; s=t[i]
            if s==0xFF: i+=2+t[i+1] if t[i+1]<128 else 3+t[i+1]; continue
            if s in(0xF0,0xF7):
                i+=1; l=0
                while t[i]&0x80: l=(l<<7)|(t[i]&0x7f); i+=1
                l=(l<<7)|t[i]; i+=1+l; continue
            if s&0x80: run=s; i+=1
            else: s=run
            hi=s&0xF0; nb=1 if hi in(0xC0,0xD0) else 2
            if hi==0x90 and t[i+1]>0: c[t[i]]+=1
            i+=nb
    return c
GM={35:'Kick 2',36:'Kick',37:'Side stick',38:'Snare',39:'Clap',40:'Snare 2',41:'Low tom',42:'Closed hat',43:'Tom',44:'Pedal hat',45:'Tom',46:'Open hat',47:'Tom',48:'Hi tom',49:'Crash',50:'Hi tom',51:'Ride',54:'Tambourine',56:'Cowbell',69:'Shaker',70:'Maracas'}
owners=sorted({r['folder'] for r in recs.values()},key=len,reverse=True)
mm=0
for f in glob.glob(os.path.expanduser('~/mnt/Homeroom Drum MIDI/Beats/*.mid')):
    nm=os.path.basename(f); num=nm.split(' ')[0]
    o=next((x for x in owners if nm[len(num)+1:].startswith(x)),'Unknown')
    r=recs.get(num)
    k=kind(r) if r else 'Unknown'; m=mode(r) if r else 'Unknown'
    mon=r['date'][:7] if r else 'Unknown'
    try: cn=midi_notes(f)
    except Exception: continue
    mm+=1
    for n,c in cn.items(): agg[('Drum MIDI hits',f"{n} {GM.get(n,'Other')}",o,k,m,mon)]+=c
    for n in cn: agg[('Drum MIDI notes used (beats)',f"{n} {GM.get(n,'Other')}",o,k,m,mon)]+=1
with open(out+'/usage.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['category','item','owner','kind','mode','month','count'])
    for k,v in sorted(agg.items()): w.writerow(list(k)+[v])
with open(out+'/beats.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['id','owner','kind','mode','date','bpm','key','progression','chord_rhythm']); w.writerows(beats)
print(len(recs),len(agg),mm, os.path.getsize(out+'/usage.csv'),os.path.getsize(out+'/beats.csv'))
print(collections.Counter(c[0] for c in agg).most_common(60))
