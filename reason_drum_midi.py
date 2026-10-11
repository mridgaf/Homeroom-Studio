#!/usr/bin/env python3
"""Pull ONLY the drum MIDI out of every beat: python3 reason_drum_midi.py [NN ...]
Writes /Volumes/TBOTC 3/Homeroom Drum MIDI/{Beats,Favorites}/<same name>.mid
One drum track, same tempo as the beat, notes moved to the Kong's pad layout (36-51).
No sounds, no stems. Originals are never touched. Skips existing files (safe to re-run)."""
import sys,os,glob,struct
H=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(H,"reason_package.py")).read()
exec("import os,struct\n"+src[src.index("def vlq"):src.index("PADS=")])   # parse/build helpers
R="/Volumes/TBOTC 3"
if not os.path.isdir(R): R=os.path.expanduser("~/mnt/TBOTC 3")
RH=os.path.join(H,"..","Homeroom Rhythms"); OUT=os.path.join(R,"Homeroom Drum MIDI")
# drum tracks -> Kong pad note (pads 1-16 = notes 36-51)
G={'kick':36,'snap':37,'snare':38,'clap':39,'perc':40,'shaker':41,'hat':42,'rims':43,'rim':43,'bongo':44,
 'congas2':45,'tablas':45,'toms':46,'big toms':46,'tamb':47,'cowbell':48,'crash':49,'crash2':49,'cymbals':49,
 'claves':50,'timbales':51,'club perc':51,'live perc':51,'mathperc':51,'brushes':51}
def go(only):
    n_ok=n_skip=n_none=0; notes={}
    for d in sorted(os.listdir(RH)):
        p=os.path.join(RH,d)
        if d.startswith(('.','_To Delete')) or d=='Trash' or not os.path.isdir(p): continue
        sub="Favorites" if d=="Favorites" else "Beats"
        for m in sorted(glob.glob(os.path.join(p,"*.mid"))):
            b=os.path.basename(m)
            if only and b.split(" ")[0] not in only: continue
            dst=os.path.join(OUT,sub,b)
            if os.path.exists(dst): n_skip+=1; continue
            div,tr=parse(m); ev=[]; used={}
            for name,e0 in tr:
                if name not in G: continue
                note=G[name]
                if note in used and used[note]!=name:           # two parts want one pad: next free pad
                    free=[x for x in range(36,52) if x not in used and x not in G.values()] or [x for x in range(36,52) if x not in used]
                    note=free[0]
                used[note]=name
                for t,e in e0:
                    if e[0]&0xF0 in(0x90,0x80): e=bytes([e[0]&0xF0|9,note,e[2]])
                    ev.append((t,e))
            if not used: n_none+=1; continue
            os.makedirs(os.path.dirname(dst),exist_ok=True)
            tracks=[build(None,tr[0][1]),build("drums",ev)]
            open(dst,'wb').write(b'MThd'+struct.pack('>IHHH',6,1,len(tracks),div)+b''.join(tracks)); n_ok+=1
    pads={}
    for k,v in G.items(): pads.setdefault(v,[]).append(k)
    open(os.path.join(OUT,"README.txt"),'w').write("Drum MIDI only. One drum track per beat, same tempo as the beat.\nNotes follow the Kong pad layout (pad 1 = note 36):\n"+"\n".join(f"  pad {v-35:>2} (note {v}) = "+" / ".join(k) for v,k in sorted(pads.items()))+"\nKick, snap, snare, clap, perc, shaker and hat are on the same pad in every beat.\nLoop-only beats have no drum MIDI, so they are not in this folder.\n")
    print("written",n_ok,"skipped(existing)",n_skip,"no drums",n_none)
if __name__=="__main__": os.makedirs(OUT,exist_ok=True); go(set(sys.argv[1:]))
