// Live Stutter for a flask (bus). A bus has no buffer to pre-render a
// stuttered copy from, so this repeats its input as it plays. It is the
// same cut as server.py _beat_repeat: in each picked cell the first
// `slice` samples pass through and are kept, the rest of the cell repeats
// them. Only past samples are ever needed, so it adds no delay.
// app.js sends the grid (cell edges in context samples, which cells are
// picked — worked out with brCellIsPicked, so there is ONE copy of that
// hash in the browser) and the playhead (frame the beat's sample 0 sits on).
class Stutter extends AudioWorkletProcessor {
  constructor() {
    super();
    this.grid = null;   // { cell, slice, picked[] }
    this.play = null;   // { zero, len, loop }
    this.headK = -1;    // cell whose head is recorded
    this.port.onmessage = e => {
      if ("grid" in e.data) {
        this.grid = e.data.grid;
        this.head = [new Float32Array(this.grid ? this.grid.slice : 1),
                     new Float32Array(this.grid ? this.grid.slice : 1)];
      }
      if ("play" in e.data) this.play = e.data.play;
      this.headK = -1;
    };
  }

  process(inputs, outputs) {
    const inp = inputs[0], out = outputs[0];
    const g = this.grid, p = this.play;
    for (let c = 0; c < out.length; c++)  // pass-through unless a cell says so
      if (inp[c] || inp[0]) out[c].set(inp[Math.min(c, inp.length - 1)]);
    if (!g || !p || !inp.length) return true;
    // samples outer, channels inner: a block can cross into a new cell, and
    // the head of that cell must belong to the cell on BOTH channels
    for (let i = 0; i < out[0].length; i++) {
      let pos = currentFrame + i - p.zero;
      if (p.loop) pos = ((pos % p.len) + p.len) % p.len;
      if (pos < 0 || pos >= p.len) continue;
      // cell edges are round(k * cell), the same rule buildRepeatBuffer uses
      let k = Math.floor(pos / g.cell);
      if (pos < Math.round(k * g.cell)) k--;
      else if (pos >= Math.round((k + 1) * g.cell)) k++;
      if (!g.picked[k]) continue;
      const j = pos - Math.round(k * g.cell);
      if (j < g.slice) {
        for (let c = 0; c < out.length; c++) this.head[c & 1][j] = out[c][i];
        this.headK = k;
      } else if (this.headK === k) {
        for (let c = 0; c < out.length; c++) out[c][i] = this.head[c & 1][j % g.slice];
      }
      // joined mid-cell (play from a pause, a seek) = no head yet, so the
      // rest of that one cell passes through untouched
    }
    return true;
  }
}
registerProcessor("stutter", Stutter);
