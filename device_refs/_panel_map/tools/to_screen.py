"""Panel Map helper: turn a control's map position into a screen point.
Give the panel's top-left and bottom-right corner screws, both in the picture
(pixels) and on screen. Linear fit; works at any zoom."""
import json,sys
def make(pic_tl,pic_br,scr_tl,scr_br,pic_size):
    sx=(scr_br[0]-scr_tl[0])/(pic_br[0]-pic_tl[0]); sy=(scr_br[1]-scr_tl[1])/(pic_br[1]-pic_tl[1])
    def f(pos):
        px,py=pos[0]*pic_size[0],pos[1]*pic_size[1]
        return round(scr_tl[0]+(px-pic_tl[0])*sx), round(scr_tl[1]+(py-pic_tl[1])*sy)
    return f
if __name__=="__main__":
    d=json.load(open(sys.argv[1])); side=sys.argv[2]
    pic_tl,pic_br,scr_tl,scr_br=[tuple(map(float,a.split(","))) for a in sys.argv[3:7]]
    size=tuple(map(float,sys.argv[7].split(",")))
    f=make(pic_tl,pic_br,scr_tl,scr_br,size)
    for r in d["controls"]:
        if r["side"]==side: print(r["code"],*f(r["pos"]),r.get("reason_name") or r.get("reason_cable_menu_name"))
