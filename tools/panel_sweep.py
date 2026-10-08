import sys,time,subprocess,json,re
sys.path.insert(0,"/Users/johnsuhr/Desktop/Homeroom Studio")
import numpy as np
from reason_voice.reason_control import ReasonControl
S="/private/tmp/claude-501/-Users-johnsuhr-Desktop-Homeroom-Studio/07f1e5b2-e7f0-4c6d-81e6-20f9ac10059c/scratchpad"
orig={};names={}
for l in open(S+"/listen.out"):
    m=re.match(r"(knob_\d+) \('(.*?)', '(.*?)'\) (\d+)",l)
    if m: orig[m.group(1)]=int(m.group(4)); names[m.group(1)]=(m.group(2),m.group(3))
def grab(tag):
    subprocess.run(["screencapture","-x",S+"/c.png"],check=True)
    subprocess.run(["sips","-z","891","1372","-s","format","bmp",S+"/c.png","--out",S+"/c.bmp"],check=True,capture_output=True)
    b=open(S+"/c.bmp","rb").read()
    off=int.from_bytes(b[10:14],"little");w=int.from_bytes(b[18:22],"little");h=int.from_bytes(b[22:26],"little",signed=True)
    bpp=int.from_bytes(b[28:30],"little")//8;rs=(w*bpp+3)//4*4
    a=np.frombuffer(b,dtype=np.uint8,offset=off,count=rs*abs(h)).reshape(abs(h),rs)[:,:w*bpp].reshape(abs(h),w,bpp)[:,:,:3].astype(int)
    if h>0:a=a[::-1]
    return a.sum(axis=2)//3
def clusters(d,thr=30,cell=12):
    ys,xs=np.where(d>thr)
    cells={}
    for y,x in zip(ys,xs): cells.setdefault((y//cell,x//cell),[]).append((y,x))
    seen=set();out=[]
    for c in cells:
        if c in seen: continue
        st=[c];seen.add(c);pts=[]
        while st:
            cy,cx=st.pop();pts+=cells[(cy,cx)]
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    n=(cy+dy,cx+dx)
                    if n in cells and n not in seen: seen.add(n);st.append(n)
        p=np.array(pts);out.append((int(p[:,1].min()),int(p[:,0].min()),int(p[:,1].max()),int(p[:,0].max()),len(pts)))
    return sorted(out,key=lambda r:-r[4])
rc=ReasonControl();time.sleep(0.5)
base=grab("base");res={}
for k in sorted(orig,key=lambda s:int(s[5:])):
    o=orig[k]
    rc.set_value(k,0 if o>63 else 127);time.sleep(0.9);a=grab("a")
    rc.set_value(k,o);time.sleep(0.9);b=grab("b")
    d=np.abs(a-b);cl=[c for c in clusters(d) if c[4]>=15]
    res[k]={"name":names[k][0],"orig_display":names[k][1],"changed_px":int((d>30).sum()),"clusters":cl[:4]}
    print(k,names[k][0],res[k]["changed_px"],cl[:3],flush=True)
fin=grab("fin");left=np.abs(fin-base)
print("restore diff px",int((left>30).sum()),clusters(left)[:5])
json.dump(res,open(S+"/sweep.json","w"),indent=1)
