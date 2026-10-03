import json
from PIL import Image, ImageDraw, ImageFont
F=[ # code, label on panel, what, reason_name, remote item?, knob slot, (cx,cy), half-size
("SCR4-F-B01","Bypass/On/Off","3-way device switch","Enabled",True,16,(96,42),(16,26)),
("SCR4-F-D01","(LED column)","Input level meter","Input Peak Meter",False,None,(96,105),(12,36)),
("SCR4-F-D02","EASYFUZZ tape","Device name tape (shows this device's name)","Device Name",False,None,(42,150),(14,80)),
("SCR4-F-B02","(triangle)","Fold/unfold device","",False,None,(42,46),(10,10)),
("SCR4-F-D03","EasyFuzz","Patch name display","Patch Name",False,None,(245,245),(105,17)),
("SCR4-F-B03","(up arrow)","Load previous patch","Select Previous Patch",False,None,(375,235),(17,9)),
("SCR4-F-B09","(down arrow)","Load next patch","Select Next Patch",False,None,(375,253),(17,9)),
("SCR4-F-B04","(folder)","Open patch browser","",False,None,(414,244),(17,18)),
("SCR4-F-B05","(disk)","Save patch","",False,None,(451,244),(17,18)),
("SCR4-F-B06","DAMAGE","Damage section on/off","Damage On/Off",True,14,(206,38),(12,12)),
("SCR4-F-K01","DAMAGE CONTROL","Amount of distortion","Damage Control",True,1,(250,118),(42,42)),
("SCR4-F-K02","(type selector)","Picks 1 of 10 damage types","Damage Type",True,2,(358,113),(32,32)),
("SCR4-F-D04","OVERDRIVE...SCREAM","Damage type list with lights (shows P1/P2 meaning)","",False,None,(625,112),(195,84)),
("SCR4-F-K03","P1","Parameter 1 (meaning depends on type)","Parameter 1",True,3,(543,236),(26,26)),
("SCR4-F-K04","P2","Parameter 2 (meaning depends on type)","Parameter 2",True,4,(665,236),(26,26)),
("SCR4-F-B07","CUT","Cut EQ on/off","Cut On/Off",True,15,(881,38),(12,12)),
("SCR4-F-S01","LO","Cut EQ low slider","Cut Lo",True,5,(868,150),(10,75)),
("SCR4-F-S02","MID","Cut EQ mid slider","Cut Mid",True,6,(905,150),(10,75)),
("SCR4-F-S03","HI","Cut EQ high slider","Cut Hi",True,7,(942,150),(10,75)),
("SCR4-F-B08","BODY","Body section on/off","Body On/Off",True,9,(1032,148),(12,12)),
("SCR4-F-K05","RESO","Body resonance","Body Resonance",True,12,(1068,198),(28,28)),
("SCR4-F-K06","SCALE","Body size (clockwise = smaller)","Body Scale",True,11,(1143,198),(28,28)),
("SCR4-F-K07","AUTO","How much the input level moves Body Scale (envelope follower)","Body Auto",True,13,(1218,198),(28,28)),
("SCR4-F-K08","TYPE","Body type A-E","Body Type",True,10,(1298,198),(32,32)),
("SCR4-F-K09","MASTER","Output volume","Master Level",True,8,(1458,198),(32,32)),
]
B=[ # code, panel label, what, reason cable-menu name, (cx,cy), half
("SCR4-B-J01","Damage Control (CV in)","CV input","Damage Control CV Input",(717,70),(14,14)),
("SCR4-B-K01","(trim)","Amount knob for J01","",(771,70),(14,14)),
("SCR4-B-J02","P1 (CV in)","CV input","Parameter 1 CV Input",(717,115),(14,14)),
("SCR4-B-K02","(trim)","Amount knob for J02","",(771,115),(14,14)),
("SCR4-B-J03","P2 (CV in)","CV input","Parameter 2 CV Input",(717,160),(14,14)),
("SCR4-B-K03","(trim)","Amount knob for J03","",(771,160),(14,14)),
("SCR4-B-J04","Scale (CV in)","CV input","Body Scale CV Input",(717,205),(14,14)),
("SCR4-B-K04","(trim)","Amount knob for J04","",(771,205),(14,14)),
("SCR4-B-J05","Auto CV Output","CV output from the Body envelope follower (follows input level)","Body Auto CV Output",(717,250),(14,14)),
("SCR4-B-J06","Input L","Audio input left","Left Input",(1030,165),(18,18)),
("SCR4-B-J07","Input R","Audio input right","Right Input",(1090,165),(18,18)),
("SCR4-B-J08","Output L","Audio output left","Left Output",(1030,240),(18,18)),
("SCR4-B-J09","Output R","Audio output right","Right Output",(1090,240),(18,18)),
]
font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",13) if __import__('os').path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else ImageFont.load_default()
OV={'SCR4-F-B01':'right','SCR4-F-D01':'below','SCR4-F-S02':'below','SCR4-F-B04':'below','SCR4-F-D02':'below','SCR4-F-B02':'right','SCR4-F-B09':'left'}
def draw(src,out,items,getpos):
    im=Image.open(src).convert("RGB");d=ImageDraw.Draw(im)
    for it in items:
        code,(cx,cy),(hw,hh)=it[0],*getpos(it)
        d.rectangle([cx-hw,cy-hh,cx+hw,cy+hh],outline=(255,0,170),width=2)
        t=code.split("-",1)[1]
        tw=d.textlength(t,font=font)
        x=max(0,min(im.width-tw-4,cx-tw/2));y=cy-hh-16 if cy-hh-16>0 else cy+hh+2
        m=OV.get(code)
        if m=="below": y=cy+hh+2
        if m=="right": x=cx+hw+3; y=cy-7
        if m=="left": x=cx-hw-tw-5; y=cy-7
        d.rectangle([x-2,y,x+tw+2,y+15],fill=(0,0,0));d.text((x,y),t,fill=(255,255,0),font=font)
    im.save(out)
    return im.size
fs=draw("front_raw.jpg","scream-4_front_labeled.png",F,lambda it:(it[6],it[7]))
bs=draw("back_raw.jpg","scream-4_back_labeled.png",B,lambda it:(it[4],it[5]))
CC=lambda k: 29+k if k else None
rows=[]
for c,lab,what,name,mapped,k,(cx,cy),hs in F:
    rows.append(dict(code=c,side="front",panel_label=lab,what=what,reason_name=name or None,
      remote_item=bool(name),mapped_in_our_remotemap=mapped,knob_slot=k,cc=CC(k),feedback_cc=(77+k if k else None),
      pos=[round(cx/fs[0],3),round(cy/fs[1],3)],how=("voice/MIDI or click" if mapped else ("click only" if not name else "display/Remote item, not mapped"))))
for c,lab,what,name,(cx,cy),hs in B:
    rows.append(dict(code=c,side="back",panel_label=lab,what=what,reason_cable_menu_name=name or None,
      pos=[round(cx/bs[0],3),round(cy/bs[1],3)],how=("cable: right-click jack > device > jack name" if c.startswith("SCR4-B-J") else "click/drag only (no Remote item)")))
json.dump(dict(device="Scream 4 Distortion",remote_scope="Propellerheads / Scream 4 Distortion",code_prefix="SCR4",
  reason_version="12.7 (screenshots 2026-10-02, John's Mac)",
  pos_note="pos = [x,y] as fraction of the captured panel picture (0-1), not screen pixels. Measured by eye from one zoom level; not yet click-tested.",
  status="pilot - unverified clicks",controls=rows),open("scream-4.json","w"),indent=1,ensure_ascii=False)
print(len(F),len(B),fs,bs)
