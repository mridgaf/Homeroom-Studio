import json,os
from PIL import Image, ImageDraw, ImageFont
P="ECHO"
# name, panel label, what, reason_name, knob_slot, (cx,cy),(hw,hh), type, confidence, conf_reason
FR=[
("Bypass/On/Off","3-way device switch","Enabled",9,(204,62),(10,22),"B","high",""),
("(triangle)","Fold/unfold device","",None,(42,35),(8,6),"B","medium","tiny triangle under the top-left screw"),
("Input","Input level meter (3 LEDs: green, yellow, red = clipping)","Input Peak Meter",None,(1354,62),(10,19),"D","high",""),
("WARM ECHO tape","Device name tape (shows this device's name)","Device Name",None,(36,292),(14,80),"D","high",""),
("Warm Echo","Patch name display","Patch Name",None,(805,63),(220,18),"D","high",""),
("(up arrow)","Load previous patch","Select Previous Patch",None,(1051,52),(15,9),"B","high",""),
("(down arrow)","Load next patch","Select Next Patch",None,(1051,73),(15,9),"B","high",""),
("(folder)","Open patch browser","",None,(1090,63),(14,16),"B","high",""),
("(disk)","Save patch","",None,(1128,63),(14,16),"B","high",""),
("NORMAL/TRIGGERED/ROLL","Mode switch, 3 positions: Normal, Triggered, Roll","Input Mode",15,(228,177),(10,28),"B","high",""),
("TRIG","Trigger button; opens the input gate while held (Triggered mode only)","Trig",25,(313,265),(18,18),"B","high",""),
("0 ... ROLL","Roll slider; slide 0 to full Roll for stutter/repeat (Roll mode only)","Roll Enabled",23,(270,349),(62,14),"S","medium","Remote name is 'Roll Enabled' (on/off style) but panel control is the Roll slider; only roll-related item, matched by elimination. Needs Reason check."),
("TIME","Delay time (1-1000 ms, or note values with Sync)","Delay Time",1,(422,177),(46,46),"K","high",""),
("OFFSET R (Delay)","Right channel delay time offset","Right Ch Time Offset",22,(510,180),(33,33),"K","medium","Two knobs are both printed OFFSET R; the Delay-section one matched to Time Offset and Feedback-section one to Feedback Offset (from manual section placement)."),
("KEEP PITCH","Keep pitch fixed when delay time changes","Keep Pitch",16,(396,264),(11,11),"B","high",""),
("SYNC","Tempo sync for Time and Offset R","Sync",24,(488,265),(12,12),"B","high",""),
("PING-PONG","Ping-pong on/off (repeats alternate left and right)","Ping-Pong Mode",19,(420,322),(11,11),"B","high",""),
("PAN","Ping-pong stereo width and first-repeat side","Ping-Pong Pan",20,(510,322),(33,33),"K","high",""),
("FEEDBACK","Amount of echo fed back (number of repeats)","Feedback",11,(642,177),(46,46),"K","high",""),
("OFFSET R (Feedback)","Right channel feedback offset (bipolar)","Right Ch Feedback Offset",21,(733,178),(33,33),"K","medium","See other OFFSET R knob; matched by section."),
("DIFFUSION (button)","Diffusion on/off","Diffuse On",3,(598,270),(11,11),"B","high",""),
("SPREAD","Diffusion spread (how wide the smear is)","Diffuse Spread",4,(642,322),(33,33),"K","high",""),
("AMOUNT (Diffusion)","Diffusion amount","Diffuse Amount",2,(733,322),(33,33),"K","high",""),
("DRIVE","Amount of the selected limiter/distortion","Drive Amount",5,(863,182),(33,33),"K","high",""),
("TYPE (LIM/OVDR/DIST/TUBE)","Color type switch, 4 positions","Drive Type",6,(931,177),(10,30),"B","high",""),
("FILTER (button)","Filter on/off","Filter On",13,(820,270),(12,12),"B","high",""),
("FREQ","Filter frequency","Filter Frequency",12,(863,322),(33,33),"K","high",""),
("RESO","Filter resonance","Filter Resonance",14,(955,322),(33,33),"K","high",""),
("ENV","Pitch bend of repeats, down or up (bipolar)","Envelope",10,(1085,182),(33,33),"K","high",""),
("WOBBLE","Random tape-speed wobble","Wobble",26,(1177,182),(33,33),"K","high",""),
("RATE","LFO speed","LFO Rate",18,(1085,322),(33,33),"K","high",""),
("AMOUNT (LFO)","LFO amount","LFO Amount",17,(1177,322),(33,33),"K","high",""),
("DRY/WET","Balance between dry and echo signal","Dry/Wet Balance",7,(1305,182),(44,44),"K","high",""),
("DUCKING","Lowers echo while input is playing","Ducking",8,(1305,322),(33,33),"K","high",""),
]
BK=[
("Trig (CV in)","Gate input for the Trig function","J",(431,149),(15,15),""),
("Roll (CV in)","CV input for Roll amount","J",(431,203),(15,15),""),
("Delay Time (CV in)","CV input for delay time","J",(431,257),(15,15),""),
("Filter Freq (CV in)","CV input for filter frequency","J",(431,311),(15,15),""),
("(trim)","Amount knob for Delay Time CV","K",(386,257),(17,17),""),
("(trim)","Amount knob for Filter Freq CV","K",(386,311),(17,17),""),
("Breakout Output L","Feedback loop send, left","J",(868,132),(21,21),""),
("Breakout Output R","Feedback loop send, right","J",(944,132),(21,21),""),
("Main Input L","Audio input left","J",(1092,132),(21,21),""),
("Main Input R","Audio input right","J",(1165,132),(21,21),""),
("Breakout Input L","Feedback loop return, left","J",(868,322),(21,21),""),
("Breakout Input R","Feedback loop return, right","J",(944,322),(21,21),""),
("Main Output L","Audio output left","J",(1092,322),(21,21),""),
("Main Output R","Audio output right","J",(1168,322),(21,21),""),
]
fp="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font=ImageFont.truetype(fp,12) if os.path.exists(fp) else ImageFont.load_default()
# numbering: per type, sort by row band then x
def number(items,ti,pi,band=40):
    cnt={};codes={}
    order=sorted(range(len(items)),key=lambda i:((items[i][pi][0]>=700) if pi==3 else 0,items[i][pi][1]//band,items[i][pi][0]))
    for i in order:
        t=items[i][ti];cnt[t]=cnt.get(t,0)+1;codes[i]=(t,cnt[t])
    return codes
fc=number(FR,6,4); bc=number(BK,2,3,40)
fcode=lambda i:f"{P}-F-{fc[i][0]}{fc[i][1]:02d}"
bcode=lambda i:f"{P}-B-{bc[i][0]}{bc[i][1]:02d}"
# label placement overrides: code-less hints by index
OVF={}
def draw(src,out,boxes):
    im=Image.open(src).convert("RGB");d=ImageDraw.Draw(im);placed=[]
    for code,(cx,cy),(hw,hh),mode in boxes:
        d.rectangle([cx-hw,cy-hh,cx+hw,cy+hh],outline=(255,0,170),width=2)
        t=code.split("-",1)[1];tw=d.textlength(t,font=font)
        opts={"above":(cx-tw/2,cy-hh-15),"below":(cx-tw/2,cy+hh+2),"right":(cx+hw+3,cy-7),"left":(cx-hw-tw-5,cy-7),"in":(cx-tw/2,cy-7)}
        x,y=opts[mode or "above"]
        x=max(1,min(im.width-tw-4,x));y=max(0,min(im.height-15,y))
        d.rectangle([x-2,y,x+tw+2,y+14],fill=(0,0,0));d.text((x,y),t,fill=(255,255,0),font=font)
    im.save(out);return im.size
import sys
MODEF=json.load(open("out/labelmodes.json")) if os.path.exists("out/labelmodes.json") else {}
fb=[(fcode(i),r[4],r[5],MODEF.get(fcode(i))) for i,r in enumerate(FR)]
bb=[(bcode(i),r[3],r[4],MODEF.get(bcode(i))) for i,r in enumerate(BK)]
fs=draw("in/the-echo_front_raw.jpg","out/the-echo_front_labeled.png",fb)
bs=draw("in/the-echo_back_raw.jpg","out/the-echo_back_labeled.png",bb)
CC=lambda k:29+k if k else None
rows=[]
for i,(lab,what,name,k,(cx,cy),hs,t,conf,why) in enumerate(FR):
    mapped=k is not None
    r=dict(code=fcode(i),side="front",panel_label=lab,what=what,reason_name=name or None,remote_item=bool(name),
      mapped_in_our_remotemap=mapped or name in("Select Previous Patch","Select Next Patch","Device Name"),
      knob_slot=k,cc=CC(k),feedback_cc=(77+k if k else None),
      pos=[round(cx/fs[0],3),round(cy/fs[1],3)],
      how=("voice/MIDI or click" if mapped else ("click only" if not name else "display/Remote item, not mapped")),
      checked_2026_10_03="PENDING",confidence=conf)
    if why:r["confidence_reason"]=why
    rows.append(r)
for i,(lab,what,t,(cx,cy),hs,why) in enumerate(BK):
    c=bcode(i);j=t=="J"
    r=dict(code=c,side="back",panel_label=lab,what=what,reason_cable_menu_name=None,
      pos=[round(cx/bs[0],3),round(cy/bs[1],3)],
      how=("cable: right-click jack > device > jack name" if j else "click/drag only (no Remote item)"),
      checked_2026_10_03="PENDING",confidence="high" if j else "medium")
    if not j:r["confidence_reason"]="trim knob next to CV jack; matched by position"
    rows.append(r)
json.dump(dict(device="The Echo",remote_scope="Propellerheads / The Echo",code_prefix=P,
  reason_version="12.7 (screenshots 2026-10-03)",
  pos_note="pos = [x,y] as fraction of the captured panel picture (0-1), not screen pixels. Measured by eye from one zoom level; not yet click-tested.",
  status="draft by helper, unchecked",controls=rows),open("out/the-echo.json","w"),indent=1,ensure_ascii=False)
print(len(FR),len(BK),fs,bs)
