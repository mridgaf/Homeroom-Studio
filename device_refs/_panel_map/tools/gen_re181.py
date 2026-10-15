import json
# RE 181 Mid/Side Audio Converter (Red Rock Sound RE). Front: screen=419+px/1.3063, 466+py/1.3063. Back: screen=453+px/1.3189, 466+py/1.3189.
NT="no tooltip in Reason (hovered 1.3 s)"
T=lambda s:'tooltip "%s"'%s
K=1.3063; OX,OY=419,466
rows=[]; chk={}; M="medium"
def f(label,what,typ,hw,hh,ck,pos,conf="high",why=""):
    sx,sy=pos
    rows.append([label,what,None,None,[round((sx-OX)*K),round((sy-OY)*K)],[round(hw*K),round(hh*K)],typ,conf,why]); chk[label]=ck
f("(left meter L input)","Input meter L (left unit)","D",24,8,NT,(475,489),M)
f("(left meter R input)","Input meter R (left unit)","D",24,8,NT,(475,514),M)
f("(left meter M output)","Output meter Mid (left unit)","D",24,8,NT,(551,489),M)
f("(left meter S output)","Output meter Side (left unit)","D",24,8,NT,(551,514),M)
f("(right meter M input)","Input meter Mid (right unit)","D",24,8,NT,(622,489),M)
f("(right meter S input)","Input meter Side (right unit)","D",24,8,NT,(622,514),M)
f("(right meter L output)","Output meter L (right unit)","D",24,8,NT,(1110,489),M)
f("(right meter R output)","Output meter R (right unit)","D",24,8,NT,(1110,514),M)
f("LISTEN Mid","Listen to the Mid input only (right unit)","B",9,8,T("Listen input Mid only"),(1000,489))
f("LISTEN Side","Listen to the Side input only (right unit)","B",9,8,T("Listen input Side only"),(1000,514))
f("RE 181 MSC 1 tape","Device name tape","D",30,7,NT+" (hovered at two spots)",(798,484),M)
f("(left unit CHECK lights)","CHECK lights (left unit)","D",14,8,NT,(520,489),M)
f("(right unit CHECK lights)","CHECK lights (right unit)","D",14,8,NT,(660,489),M)
B=[];CB={}
BK=1.3189; BX,BY=453,466
def b(label,what,ck,sx,sy,hw=9,hh=9):
    B.append([label,what,"J",[round((sx-BX)*BK),round((sy-BY)*BK)],[round(hw*BK),round(hh*BK)],""]); CB[label]=ck
b("Stereo In L","Stereo input, left (to Mid/Side out)",T("Audio In Left"),521,495)
b("Stereo In R","Stereo input, right",T("Audio In Right"),521,519)
b("M|S Out Mid","Mid output",T("Audio Out Mid"),586,495)
b("M|S Out Side","Side output",T("Audio Out Side"),586,519)
b("M|S In Mid","Mid input (to Stereo out)",T("Audio In Mid"),669,495)
b("M|S In Side","Side input",T("Audio In Side"),669,519)
b("Stereo Out L","Stereo output, left",T("Connected to AB12AudOut 1: Audio Input Left"),737,495)
b("Stereo Out R","Stereo output, right",T("Connected to AB12AudOut 1: Audio Input Right"),737,519)
base=dict(device="RE 181 Mid/Side Audio Converter",prefix="RE18",remote_scope="none (Rack Extension; no Remote map or vocab entry); names from tooltips only",date="2026-10-15",out_dir=".")
json.dump(dict(base,slug="re181-mid-side",front_raw="_captures_batchE/re181_front_raw.jpg",back_raw="_captures_batchE/re181_back_raw.jpg",front=rows,back=B),open("tools/specs/re181-mid-side.json","w"))
json.dump(dict(device="RE 181 Mid/Side Audio Converter",front=chk,back=CB,views={},view_titles={}),open("tools/checks/re181-mid-side.json","w"),indent=0)
print(len(rows),len(B))
