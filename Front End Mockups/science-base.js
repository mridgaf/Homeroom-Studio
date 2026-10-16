// Shared behaviour for the Sound of Science mockups. Each page sets window.SCI first:
// { bus: "Beaker", knob: "dial"|"element", busNote: "...", cleanWord: "..." }
const SCI = window.SCI || {};
const FX = [["EQ","Eq","Bass + air lift"],["Compress","Cp","Squash + punch"],["Drive","Dr","Warmth"],["Width","Wd","Wider stereo"],
  ["Chorus","Ch","Thicken"],["Phaser","Ph","Sweeping whoosh"],["Echo","Ec","Repeats in time"],["Stutter","St","Beat repeat"],
  ["Reverb","Rv","Room / space"],["Convolve","Cv","Drop a sound in"]];
const STEMS = ["kick drum","snare","hats","percs","bass drum","chords","melody"];
const route = {"kick drum":"A","snare":"A","melody":"B"};

const pt=(r,a)=>[60+r*Math.cos(a*Math.PI/180),60+r*Math.sin(a*Math.PI/180)];
const arc=(a0,a1,r=46)=>{const[p,q]=pt(r,a0),[x,y]=pt(r,a1);return`M${p} ${q}A${r} ${r} 0 ${a1-a0>180?1:0} 1 ${x} ${y}`};

function drag(el,get,set){el.onpointerdown=e=>{const y0=e.clientY,v0=get();
  const mv=m=>set(Math.max(0,Math.min(100,v0+(y0-m.clientY)/1.5)));
  const up=()=>{removeEventListener("pointermove",mv);removeEventListener("pointerup",up)};
  addEventListener("pointermove",mv);addEventListener("pointerup",up)}}

function dialKnob([name,,tip],cls){
  const d=document.createElement("div");d.className="knob "+cls;let v=0,on=false;
  d.innerHTML=`<svg viewBox="0 0 120 120"><path class="dbg" d="${arc(135,405)}"/><path class="lit"/><line class="ptr" x1="60" y1="60" x2="60" y2="24"/><text class="pct" x="60" y="66">0%</text></svg>
  <div><div class="kn">${name}</div><div class="kt">${tip}</div><span class="sw">OFF</span></div>`;
  const draw=()=>{const e=135+270*v/100;d.querySelector(".lit").setAttribute("d",v?arc(135,e):"");
    d.querySelector(".ptr").setAttribute("transform",`rotate(${e-270} 60 60)`);d.querySelector(".pct").textContent=Math.round(v)+"%";
    d.classList.toggle("on",on);d.querySelector(".sw").textContent=on?"ON":"OFF"};
  d.querySelector(".sw").onclick=()=>{on=!on;draw()};
  drag(d.querySelector("svg"),()=>v,n=>{v=n;if(v>0)on=true;draw()});draw();return d}

// periodic-table tile: the fill level is the amount, drag up/down, click symbol to switch
function elementKnob([name,sym,tip],cls,i){
  const d=document.createElement("div");d.className="el "+cls;let v=0,on=false;
  d.innerHTML=`<span class="no">${i+1}</span><span class="amt">0%</span><b class="sym">${sym}</b><span class="nm">${name}</span><span class="tp">${tip}</span><i class="fill"></i><span class="sw">OFF</span>`;
  const draw=()=>{d.querySelector(".fill").style.height=v+"%";d.querySelector(".amt").textContent=Math.round(v)+"%";
    d.classList.toggle("on",on);d.querySelector(".sw").textContent=on?"ON":"OFF"};
  d.querySelector(".sw").onclick=e=>{e.stopPropagation();on=!on;draw()};
  drag(d,()=>v,n=>{v=n;if(v>0)on=true;draw()});draw();return d}

function busPage(id){
  const el=document.getElementById("p-"+id);if(!el)return;
  el.innerHTML=`<h1 class="nbtitle">${SCI.bus||"Bus"} ${id}</h1>
   <p class="nbsub">${SCI.busNote||"Everything sent here goes through these."} <b id="who${id}"></b></p>
   <div class="lvl">Level <input type="range" value="80"></div>
   <div class="${SCI.knob==="element"?"ptable":"kgrid"}"></div>
   <p style="margin-top:14px"><button class="paperbtn">${SCI.cleanWord||"Return to clean"} ${id}</button></p>`;
  const g=el.querySelector(".kgrid,.ptable");
  FX.forEach((f,i)=>g.append(SCI.knob==="element"?elementKnob(f,"bus"+id,i):dialKnob(f,"bus"+id)))}

function renderLanes(){
  const lanes=document.getElementById("lanes");lanes.innerHTML="";
  STEMS.forEach(s=>{const r=route[s]||"",l=document.createElement("div");l.className="lane";
    l.innerHTML=`<span>${s}</span><input type="range" value="${72+s.length%5*4}"><span class="pan">pan C</span><div class="ms"><span>M</span><span>S</span></div>
    <div class="routes"><button class="route A ${r=="A"?"on":""}">A</button><button class="route B ${r=="B"?"on":""}">B</button></div>`;
    l.querySelectorAll(".route").forEach(b=>b.onclick=()=>{const k=b.textContent;route[s]=route[s]===k?"":k;renderLanes()});
    lanes.append(l)});
  for(const k of "AB"){const who=STEMS.filter(s=>route[s]===k);
    const c=document.getElementById("c"+k);if(c)c.textContent=who.length+" stems";
    const w=document.getElementById("who"+k);if(w)w.textContent=who.length?"Holding: "+who.join(", "):"Empty — tap A/B on a stem."}}

const sl=document.getElementById("stemList");
if(sl)STEMS.forEach(s=>sl.insertAdjacentHTML("beforeend",`<div class="stemrow"><span>${s}</span><select><option>EQ 0 · Comp 0 · Verb 0</option></select></div>`));
busPage("A");busPage("B");renderLanes();
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab,.page").forEach(x=>x.classList.remove("on"));
  t.classList.add("on");document.getElementById("p-"+t.dataset.p).classList.add("on")});
