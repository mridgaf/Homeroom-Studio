#!/usr/bin/env python3
"""Package one beat for Reason: python3 reason_package.py 3374
Makes Homeroom WAVs/Packages/<beat>/ with: one merged drum MIDI (Kong pad notes),
the beat's own drum one-shots, the non-drum stem WAVs, and a README with the pad map.
Read-only on originals. Reason can't be scripted, so the Kong pads are loaded by hand."""
import sys,os,json,glob,shutil,struct
R="/Volumes/TBOTC 3"
if not os.path.isdir(R): R=os.path.expanduser("~/mnt/TBOTC 3")  # sandbox mount
def mp(p): return p.replace("/Volumes/TBOTC 3",R)
RH=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","Homeroom Rhythms")
def vlq(n):
    b=[n&0x7f]; n>>=7
    while n: b.append((n&0x7f)|0x80); n>>=7
    return bytes(reversed(b))
def rvlq(d,i):
    v=0
    while True:
        c=d[i]; i+=1; v=(v<<7)|(c&0x7f)
        if not c&0x80: return v,i
def parse(f):
    d=open(f,'rb').read(); n,div=struct.unpack('>HH',d[10:14]); i=14; tr=[]
    for _ in range(n):
        L=int.from_bytes(d[i+4:i+8],'big'); t_=d[i+8:i+8+L]; i+=8+L
        j=0;t=0;run=None;ev=[];name=None
        while j<len(t_):
            dt,j=rvlq(t_,j); t+=dt; s=t_[j]
            if s==0xFF:
                ty=t_[j+1]; l,k=rvlq(t_,j+2); data=t_[k:k+l]; j=k+l
                if ty==3: name=data.decode('latin1')
                elif ty!=0x2F: ev.append((t,b'\xff'+bytes([ty])+vlq(l)+data))
                continue
            if s&0x80: run=s; j+=1
            ln=1 if run>>4 in(0xC,0xD) else 2
            ev.append((t,bytes([run])+t_[j:j+ln])); j+=ln
        tr.append((name,ev))
    return div,tr
def build(name,ev):
    out=b''; last=0
    if name: nb=name.encode(); out+=vlq(0)+b'\xff\x03'+vlq(len(nb))+nb
    for t,e in sorted(ev,key=lambda x:x[0]): out+=vlq(t-last)+e; last=t
    out+=vlq(0)+b'\xff\x2f\x00'
    return b'MTrk'+len(out).to_bytes(4,'big')+out
PADS=list(range(36,52))
ROLE={'kick':36,'snap':37,'snare':38,'clap':39,'perc':40,'mathperc':41,'hat':42}
SLOTS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'Reason Template','Slots')
def silence(path):
    import wave
    w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100); w.writeframes(b'\0'*4*4410); w.close()
def fill(pkg,drum,role,kit,stems):
    """Put this beat's sounds into the fixed file names the Reason template points at."""
    os.makedirs(SLOTS,exist_ok=True)
    byNote={role[n]:mp(kit[n]) for n,_ in drum}
    for i,note in enumerate(PADS):
        dst=os.path.join(SLOTS,f"Pad{i+1:02d}.wav")
        if note in byNote: shutil.copy(byNote[note],dst)
        else: silence(dst)
    st=sorted(f for f in glob.glob(os.path.join(stems,"*.wav")) if os.path.basename(f).split(" - ")[0].replace("kick drum","kick") not in kit)
    if len(st)>8: print("WARNING: more than 8 stems, only first 8 go in the template"); st=st[:8]
    for i in range(8):
        dst=os.path.join(SLOTS,f"Stem{i+1}.wav")
        if i<len(st): shutil.copy(st[i],dst)
        else: silence(dst)
def main(num):
    rec=json.load(open(os.path.join(RH,".recipes",f"{num}.json")))
    mid=glob.glob(os.path.join(RH,"*",f"{num} *.mid"))[0]; folder=os.path.dirname(mid)
    stems=glob.glob(os.path.join(folder,f"{num} * Stems"))[0]
    base=os.path.basename(mid)[:-4]; bpm=rec['bpm']
    div,tr=parse(mid); kit=rec['kit_paths']
    drum=[(n,ev) for n,ev in tr if n in kit]
    free=[p for p in PADS if p not in ROLE.values()]; role={}
    for n,_ in drum: role[n]=ROLE.get(n) or free.pop(0)
    ev=[]
    for n,e0 in drum:
        for t,e in e0:
            if e[0]&0xF0 in(0x90,0x80): e=bytes([0x99 if e[0]&0xF0==0x90 else 0x89,role[n],e[2]])
            ev.append((t,e))
    pkg=os.path.join(R,"Homeroom WAVs","Packages",f"{num} {rec['title'] if 'title' in rec else base} {bpm}bpm")
    os.makedirs(os.path.join(pkg,"Drum samples"),exist_ok=True)
    tracks=[build(None,tr[0][1]),build("drums",ev)]
    open(os.path.join(pkg,f"{num} Drums (Kong) {bpm}bpm.mid"),'wb').write(b'MThd'+struct.pack('>IHHH',6,1,len(tracks),div)+b''.join(tracks))
    lines=[]
    for n,e0 in drum:
        src=kit[n]; shutil.copy(mp(src),os.path.join(pkg,"Drum samples"))
        note=role[n]; lines.append(f"Pad {PADS.index(note)+1} (note {note}): {n} = {os.path.basename(src)}")
    for f in glob.glob(os.path.join(stems,"*.wav")):
        if os.path.basename(f).split(" - ")[0].replace("kick drum","kick") not in kit: shutil.copy(f,pkg)
    open(os.path.join(pkg,"README.txt"),'w').write(f"{base}\nTempo {bpm} BPM (the MIDI sets it; stems are whole bars at that tempo, do not stretch).\nDrums: one Kong, load these onto its pads:\n"+"\n".join(lines)+"\nOther WAVs: drop on audio tracks at bar 1.\n")
    fill(pkg,drum,role,kit,stems)
    print(pkg); print("\n".join(lines))
main(sys.argv[1])
