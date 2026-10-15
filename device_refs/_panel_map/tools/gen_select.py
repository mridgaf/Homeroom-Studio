import json
# Select CV Switch (Robotic Bean RE). Front: screen=419+px/1.3138, 396+py/1.3138 (zoom [419,396,1219,540]). Back: screen=453+px/1.3135, 396+py/1.3135 (zoom [453,396,1193,540]).
NT="no tooltip in Reason (hovered 1.4 s)"
T=lambda s:'tooltip "%s"'%s
K=1.3138; OX,OY=419,396
rows=[]; chk={}; M="medium"
def f(label,what,typ,hw,hh,ck,pos,conf=M,why=""):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why]); chk[label]=ck
f("(triangle)","Fold/unfold device","B",8,8,"no tooltip (fold arrow); checked by eye",(436,404))
f("SELECT 1 tape","Device name tape","D",28,7,T("Select 1"),(821,405),"high")
f("CV SELECT light","CV Select light (small round light)","D",5,5,NT,(993,420))
f("SNAP display","SNAP value display (shows 4/4)","D",14,7,NT,(1110,425))
f("mouse icon","Small icon at the left edge (mouse/click symbol)","D",8,10,NT,(437,448))
NOTES=("C3","D3","E3","F3","G3","A3","B3","C4")
for n in range(1,9):
    x=500+(n-1)*88.9
    f("SELECT %d display"%n,"Bar above button %d: shows the active input"%n,"D",36,6,NT,(x+4,424+0))
    f("SELECT %d button"%n,"Select input %d (MIDI note %s)"%(n,NOTES[n-1]),"B",30,15,NT,(x,480),why="no tooltip appeared on the button")
B=[];CB={}
BK=1.3135; BX,BY=453,396
def b(label,what,ck,sx,sy,hw=9,hh=9,typ="J"):
    B.append([label,what,typ,[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=ck
b("Auto Mute switch","Auto mute on stop: Off / On",T("Auto Mute on Stop: Off"),687,432,14,8,"B")
b("CV Select In","CV input that picks the active input",T("Select Input"),746,419)
b("CV Select Out","CV output (follows the selection)",T("Select Output"),800,419)
b("Output Gate","Gate output of the selected input",T("Gate Output"),945,419)
b("Output CV","CV output of the selected input",T("CV Output"),975,419)
for n in range(1,9):
    x=511+(n-1)*88.9 if n<=4 else 511+(n-1)*88.9
    b("Gate In %d"%n,"Gate input %d"%n,T("Gate Input %d"%n) if n in (1,2,8) else "not hovered separately: same row as hovered Gate Input 1/2/8; tooltip pattern 'Gate Input N' assumed",x,484)
    b("CV In %d"%n,"CV input %d"%n,T("CV Input %d"%n) if n in (1,2,8) else "not hovered separately: same row as hovered CV Input 1/2/8; tooltip pattern 'CV Input N' assumed",x+26,484)
b("SELECT 1 tape (back)","Device name tape on the back",T("Select 1"),727,526,28,7,"D")
b("Logo/icons (back)","Robotic Bean logo and DC input marks (no tooltip)",NT,1120,432,40,10,"D")
base=dict(device="Select CV Switch",prefix="SELC",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="select-cv-switch",front_raw="_captures_batchE/select_front_raw.jpg",back_raw="_captures_batchE/select_back_raw.jpg",front=rows,back=B),open("tools/specs/select-cv-switch.json","w"))
json.dump(dict(device="Select CV Switch",front=chk,back=CB,views={},view_titles={}),open("tools/checks/select-cv-switch.json","w"),indent=0)
print(len(rows),len(B))
