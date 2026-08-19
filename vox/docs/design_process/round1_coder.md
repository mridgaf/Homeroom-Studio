# ROUND 1 — SOFTWARE ARCHITECTURE
## VOX: AI Vocal Processor — Coder's Design Document

**Author:** THE CODER
**Scope:** Module architecture, analysis/assistant subsystem, Python prototype spec, C++/JUCE port plan, real-time honesty audit, effort estimate.
**Prime directive:** *Prototype in Python, ship in C++. Design the Python so the port is a transliteration, not a rewrite.*

---

# 0. The One Rule That Makes This Work

Everything in the prototype lives in one of two buckets, and they have different rules:

| Bucket | Contents | Rules |
|---|---|---|
| **`stages/` — the signal path** | EQ, comp, de-ess, gate, sat, limiter, reverb, denoise… | Written in **"C++-shaped Python."** Explicit state members. Block-based `process(block)`. No `filtfilt`, no `np.roll` across block boundaries, no whole-file ops, no librosa. Must produce identical output for any block size. This code is *transliterated* to C++, line by line. |
| **`analysis/` + `assistant/` — the brain** | Feature extraction, profiling, decision rules | Allowed to use librosa, scipy, sklearn, whatever. Offline or lookahead-heavy is fine. Ports to C++ as a **rewrite**, but on the *analysis thread* where the rules are soft. |

If a piece of DSP can't be expressed in bucket 1, it doesn't ship in the real-time path. That single constraint kills 90% of the "the prototype sounded great but we can't ship it" failure mode.

---

# 1. MODULE ARCHITECTURE

## 1.1 The `Stage` interface (the spine)

One interface. Everything is a Stage — including the chain itself, the oversampler, and the parallel-path splitter. Composability by uniformity.

### C++ (canonical — the Python mirrors this exactly)

```cpp
// voxdsp/core/Stage.h  — ZERO JUCE dependency. Plain C++20.
namespace vox {

struct PrepareSpec {
    double sampleRate      = 48000.0;
    int    maxBlockSize    = 512;
    int    numChannels     = 2;
    int    oversampleFactor= 1;     // set by an enclosing Oversampler
};

// Non-owning view of interleaved-by-channel audio. Never allocates.
struct AudioBlock {
    float* const* channels;   // channels[ch][n]
    int numChannels;
    int numSamples;
    float* channel(int c) const noexcept { return channels[c]; }
};

// Read-only per-block context handed down the chain.
struct StageContext {
    int64_t   samplePosition;   // running stream position, for automation/analysis timestamps
    double    bpm;              // host tempo, 0 if unknown
    bool      isPlaying;
    AudioBlock* sidechain;      // external sidechain, nullptr if absent
    AnalysisBus* analysis;      // where stages PUBLISH measurements (never read decisions here)
};

class Stage {
public:
    virtual ~Stage() = default;

    // ---- Non-real-time. Allocation ALLOWED here and ONLY here. ----
    virtual void prepare(const PrepareSpec&) = 0;

    // ---- Real-time safe. Clears all internal state to a silent, well-defined
    //      condition. MUST NOT allocate. Called on transport jump / plugin reset. ----
    virtual void reset() noexcept = 0;

    // ---- Real-time. noexcept, no alloc, no locks, no syscalls, no logging. ----
    virtual void process(AudioBlock& io, const StageContext& ctx) noexcept = 0;

    // ---- Latency this stage adds, in samples AT THIS STAGE'S RATE.
    //      Must be constant between prepare() calls. ----
    virtual int latencySamples() const noexcept { return 0; }

    // ---- Parameter surface ----
    virtual ParamSet& params() noexcept = 0;

    // ---- Introspection ----
    virtual const char* typeId()  const noexcept = 0;   // "comp", "deess", ...
    virtual int         tailSamples() const noexcept { return 0; } // reverb/delay tails

    // ---- Bypass is handled by the CHAIN, not the stage (needs delay matching). ----
};

} // namespace vox
```

### Python mirror

```python
# vox/core/stage.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class PrepareSpec:
    sample_rate: float = 48000.0
    max_block_size: int = 512
    num_channels: int = 2
    oversample_factor: int = 1

@dataclass
class StageContext:
    sample_position: int = 0
    bpm: float = 0.0
    is_playing: bool = True
    sidechain: np.ndarray | None = None      # (ch, n) or None
    analysis: "AnalysisBus | None" = None

class Stage(ABC):
    type_id: str = "stage"

    @abstractmethod
    def prepare(self, spec: PrepareSpec) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...
    @abstractmethod
    def process(self, io: np.ndarray, ctx: StageContext) -> None:
        """io is float32 (num_channels, num_samples), modified IN PLACE.
        MUST NOT reallocate io. MUST NOT depend on num_samples."""
    def latency_samples(self) -> int: return 0
    def tail_samples(self) -> int: return 0
    @property
    @abstractmethod
    def params(self) -> "ParamSet": ...
```

**In-place, pre-shaped, `(ch, n)` float32 arrays.** Not `(n, ch)`. Not float64. Not "return a new array." This one decision is worth ~2 person-weeks at port time because it means the Python stage code already thinks in per-channel pointers.

Enforce it with a decorator in tests:

```python
# vox/core/stage.py
def rt_checked(fn):
    """Dev-mode wrapper: asserts no reallocation, no NaN/Inf, no shape change."""
    def wrapper(self, io, ctx):
        ptr, shp = io.__array_interface__['data'][0], io.shape
        fn(self, io, ctx)
        assert io.__array_interface__['data'][0] == ptr, f"{self.type_id} reallocated io"
        assert io.shape == shp
        assert np.isfinite(io).all(), f"{self.type_id} produced non-finite"
    return wrapper
```

## 1.2 Parameter system

Three layers, resolved per block. This is the key structure that makes "AI assistant" and "user knobs" coexist without fighting.

```
  user_value        (host/automation/GUI — atomic<float>, normalized 0..1)
      +
  assist_offset     (assistant proposal, in NATIVE units, delta or absolute)
      *
  assist_amount     (global 0..1 "Assist" macro — dial the AI in/out)
      ↓
  target_value      (native units, computed once per block)
      ↓  SmoothedValue ramp (per-sample or per-8-sample)
  current_value     (what the DSP actually reads)
```

```cpp
// voxdsp/core/Param.h
enum class ParamKind { Linear, Skewed, Logarithmic, Boolean, Choice };

struct ParamDesc {
    const char* id;            // "comp.threshold"  — stable, used in presets + host
    const char* name;          // "Threshold"
    const char* unit;          // "dB"
    float  min, max, def;
    ParamKind kind = ParamKind::Linear;
    float  skew = 1.0f;
    float  smoothMs = 20.0f;   // 0 => step (choices), 50-100ms for gain, 5ms for makeup
    bool   isAssistable = true;
    float  assistMin, assistMax; // assistant is NEVER allowed outside this narrower band
};

class Param {
public:
    void prepare(double sr) noexcept;                    // sets ramp length
    void setUserNormalized(float v) noexcept;            // ANY thread (atomic store)
    void setAssistTarget(float native) noexcept;         // analysis thread (atomic store)
    void setAssistAmount(float a) noexcept;

    // Called ONCE per block on the RT thread. Resolves the 3 layers.
    void updateBlock() noexcept {
        float user   = denormalize(userNorm.load(std::memory_order_relaxed));
        float assist = assistTarget.load(std::memory_order_relaxed);
        float amt    = assistAmount.load(std::memory_order_relaxed);
        float target = std::clamp(user + amt * (assist - user), desc.min, desc.max);
        smoother.setTargetValue(target);
    }
    float next() noexcept   { return smoother.getNextValue(); }  // per-sample
    float current() noexcept{ return smoother.getCurrentValue(); }
    bool  isSmoothing() const noexcept { return smoother.isSmoothing(); }
private:
    ParamDesc desc;
    std::atomic<float> userNorm{0}, assistTarget{0}, assistAmount{0};
    LinearSmoothedValue<float> smoother;
};
```

**Rules enforced by the framework, not by discipline:**
1. A stage may only read params through `Param::next()` / `current()`. Never a raw float member.
2. Any param that multiplies the signal (gain, mix, threshold-in-a-feedback-path) **must** have `smoothMs > 0`. Test asserts this.
3. Recomputing filter coefficients is expensive → coefficient-owning stages check `isSmoothing()` and only recompute when true, and only every N samples (control-rate = 16 or 32 samples). Codified in a `ControlRateUpdater` helper so every filter does it the same way.
4. `assistMin/assistMax` is a hard cage. The assistant physically cannot make a -18 dB EQ cut even if the rules say so. This is the difference between "smart" and "unpredictable," and unpredictable is what kills AI features in reviews.

`ParamSet` is a flat, ID-indexed array with a compile-time enum per stage type, plus a string→index map used only at preset-load/GUI time (never on RT thread).

## 1.3 Block-based processing & the Chain

```cpp
class Chain final : public Stage {
public:
    void prepare(const PrepareSpec& s) override {
        spec = s;
        for (auto& st : stages) st->prepare(s);
        rebuildLatency();               // allocates delay lines — fine, we're in prepare
    }
    void process(AudioBlock& io, const StageContext& ctx) noexcept override {
        for (size_t i = 0; i < stages.size(); ++i) {
            if (bypassed[i]) { bypassDelay[i].process(io); continue; } // latency-matched bypass!
            stages[i]->process(io, ctx);
        }
    }
    int latencySamples() const noexcept override { return totalLatency; }
private:
    void rebuildLatency() {
        totalLatency = 0;
        for (size_t i = 0; i < stages.size(); ++i) {
            int L = stages[i]->latencySamples();
            bypassDelay[i].setDelay(L);   // bypassing a stage must NOT change chain latency
            totalLatency += L;
        }
    }
};
```

**Block-size independence is a hard invariant.** The framework provides a `BlockSlicer` for stages that internally need a fixed hop (FFT stages, ML stages):

```cpp
// Feeds an inner processor fixed-size hops regardless of host block size.
// Costs exactly `hopSize` samples of latency. No allocation in process().
template <int MaxHop>
class HopBuffer {
public:
    void prepare(int hop, int maxBlock);
    // Push arbitrary n samples; calls fn(float* hopBuf) whenever a full hop is ready;
    // pulls n processed samples out. Latency = hop.
    template <class Fn> void process(float* io, int n, Fn&& fn) noexcept;
};
```

Every FFT-based and ML-based stage is built on `HopBuffer`. That is the *only* sanctioned way to get a fixed internal rate. It guarantees block-size independence by construction.

## 1.4 State & reset semantics

Three distinct operations, frequently conflated, each a separate bug class:

| Op | When | Allocates? | Effect |
|---|---|---|---|
| `prepare(spec)` | sample rate / block size / channel count change; plugin load | **Yes** | Size all buffers for `maxBlockSize`; recompute all coefficients; implies `reset()` |
| `reset()` | transport locate, host reset, offline-render start, bypass→active | **No** | Zero all delay lines, filter states, envelope followers, FFT overlap buffers, ML hidden states. Params keep their values but smoothers **jump to target** (no ramp from stale value) |
| `setState(json)` | preset load, session restore | Yes (parse off-RT) | Params only. Never touches DSP state. Applied via the param FIFO so it's ramped, not stepped, if audio is running |

Reset must be *idempotent and complete*: `process(x); reset(); process(x)` must be bit-identical to `reset(); process(x)`. This is a golden test (§3.6) and it catches ~every uninitialized-state bug.

**Denormals:** `reset()` zeroing is not enough; IIR tails decay into denormal hell. Every recursive stage either (a) runs under FTZ/DAZ (`juce::ScopedNoDenormals` at the top of `processBlock`) or (b) injects a `1e-20` alternating-sign dither into the feedback path. We do **both** — FTZ is not guaranteed on all hosts/threads (AAX and some ARM paths have surprised people).

## 1.5 Latency reporting & compensation

Latency sources, all of which must be declared:

- Lookahead limiter / gate: `lookaheadSamples`
- Linear-phase EQ: `(fftSize - 1) / 2` or FIR taps/2
- FFT denoise / dereverb: `hopSize` (from `HopBuffer`) + any internal frame delay
- ML inference offloaded to a worker thread: `N * hopSize` where N is the queue depth (§4.5)
- Oversampling with FIR halfbands: filter group delay / factor
- True-peak limiter's 4x upsampler

Rules:

1. **`latencySamples()` is constant between `prepare()` calls.** Changing latency mid-stream causes hosts to glitch, re-scan, or silently misalign. If a user toggles "linear phase," we either (a) accept the click and call `setLatencySamples()` + the host's PDC re-negotiation, or (b) keep the max latency reserved and pad with delay. **We choose (b) for anything a user might automate, (a) for mode switches behind a confirm.**
2. **Parallel paths must be delay-aligned.** A `ParallelSplit` stage measures both branches' `latencySamples()` and inserts an integer `DelayLine` on the shorter one. Fractional latency (rare — only from IIR-based oversamplers) gets a Thiran allpass; we prefer to avoid it by choosing FIR halfbands for anything in a parallel path.
3. **Bypass is latency-matched** (see `Chain::rebuildLatency`). Both per-stage bypass and host bypass. Host bypass in JUCE: implement `getBypassParameter()` and hand the host a real parameter, then ramp in/out over ~10 ms *and* keep feeding the delay line so A/B is time-aligned.
4. **Report at the outermost rate.** A stage inside a 4x oversampler reports latency in oversampled samples; the `Oversampler` divides by 4 and adds its own filter delay.

## 1.6 Sample-rate agnosticism

Non-negotiable rules, enforced in code review and tests:

- No hard-coded sample counts. Everything is `ms → samples` at `prepare()` via `int msToSamples(float ms, double sr)`.
- All filter coefficients derived from normalized frequency `w = 2π f / sr`, with **explicit clamping**: `f = min(f, 0.45 * sr)`. Nyquist blowups at 44.1k on a 20 kHz air shelf is a classic shipped bug.
- Prefer **TPT / topology-preserving SVF** (Zavalishin) over Direct Form II biquads for anything modulated or at extreme frequencies. TPT is stable under modulation, has no coefficient-blowup at low frequency in float32, and behaves identically across sample rates. This costs a few percent CPU and saves a month.
- Envelope followers use `coeff = exp(-1 / (timeSec * sr))`, computed at prepare.
- **Nonlinear stages (saturation, compression knees) are NOT sample-rate agnostic** — aliasing changes with rate. They get oversampled to a *fixed effective rate* (≥192 kHz): factor = `ceil(192000 / sr)` rounded to a power of two. So 44.1/48 → 4x, 88.2/96 → 2x, 176.4/192 → 1x. This makes the plugin *sound the same* at every session rate, which is what users actually mean by "sample rate agnostic."
- Reverb/delay times in ms; modulation rates in Hz; nothing in "samples" in the preset format.

Golden test: render a 1 kHz sweep response at 44.1/48/88.2/96/192 and assert the magnitude responses agree within 0.25 dB up to 18 kHz.

## 1.7 Oversampling wrapper

A `Stage` decorator, so any stage can be oversampled without knowing it:

```cpp
class Oversampled final : public Stage {
public:
    Oversampled(std::unique_ptr<Stage> inner, int factor, Mode mode)
        : inner(std::move(inner)), factor(factor), mode(mode) {}

    void prepare(const PrepareSpec& s) override {
        os.initProcessing(s.maxBlockSize);            // JUCE dsp::Oversampling or our own
        PrepareSpec up = s;
        up.sampleRate       = s.sampleRate * factor;
        up.maxBlockSize     = s.maxBlockSize * factor;
        up.oversampleFactor = factor;
        inner->prepare(up);
    }
    void process(AudioBlock& io, const StageContext& ctx) noexcept override {
        auto up = os.processSamplesUp(io);            // no alloc; buffers preallocated
        inner->process(up, ctx);
        os.processSamplesDown(io);
    }
    int latencySamples() const noexcept override {
        return (int)os.getLatencyInSamples() + inner->latencySamples() / factor;
    }
private:
    std::unique_ptr<Stage> inner;
    Oversampling os;   // Mode::IIRPolyphase (low latency, phase distortion)
                       // Mode::FIREquiripple (linear phase, ~factor*32 samples latency)
};
```

Python mirror uses `scipy.signal.resample_poly` **only at prepare-time coefficient design**; the actual up/downsampling in the prototype must be a real polyphase FIR with persistent state across blocks, not `resample_poly` on the block (which zero-pads edges and will lie to you — see §5.4).

## 1.8 Analysis bus / sidechain (the assistant's nervous system)

This is the piece most vocal-plugin architectures get wrong. The rule:

> **RT thread writes measurements. Analysis thread writes decisions. Neither blocks the other. Ever.**

```cpp
// voxdsp/core/AnalysisBus.h
struct FeatureFrame {            // POD, trivially copyable, fixed size. ~256 bytes.
    int64_t samplePos;
    float   rmsDb, peakDb, truePeakDb;
    float   bandEnergyDb[24];    // Bark-ish bands, from the shared STFT
    float   f0Hz, f0Confidence;
    float   spectralCentroid, spectralFlatness, zcr;
    float   gainReductionDb[4];  // per dynamics stage, so the assistant sees its own effect
    uint32_t flags;              // VOICED | SIBILANT | BREATH | PLOSIVE | CLIPPED | SILENT
};

class AnalysisBus {
public:
    // ---- RT side ----
    void publish(const FeatureFrame& f) noexcept { fifo.tryPush(f); }  // drops on full. Fine.
    void publishGR(int stageSlot, float grDb) noexcept;                // atomic store

    // ---- Analysis-thread side ----
    bool pop(FeatureFrame& out) noexcept { return fifo.tryPop(out); }

    // ---- Decisions travel BACK via a separate FIFO of (paramIndex, value) ----
    void proposeParam(uint32_t paramIdx, float native) noexcept;       // analysis thread
    void drainProposals(ParamRegistry& reg) noexcept;                  // RT thread, once/block
private:
    SpscRing<FeatureFrame, 512> fifo;      // lock-free, preallocated, single producer/consumer
    SpscRing<ParamProposal, 256> proposals;
};
```

Key design points:

- **One shared STFT.** The analysis front-end computes a single 2048/512 STFT once per hop and every consumer (denoise, de-esser detector, feature extractor, GUI spectrum) reads from it. Computing four STFTs of the same signal is the #1 way vocal chains end up at 25% CPU.
- **Stages publish their own GR.** The assistant needs closed-loop feedback ("I asked for 4 dB of GR; I'm getting 9") — this is what turns a static rule table into something that actually converges.
- **Sidechain**: `StageContext::sidechain` is an optional external bus (host sidechain input). Internal sidechains (e.g. de-esser detector filter) are stage-local, not on the bus.
- **Dropping frames is correct behavior.** If the analysis thread stalls, the ring fills, `publish` drops. Audio never hiccups. The assistant just gets slightly stale statistics, which is fine because all its estimators are long-window anyway.

---

# 2. THE ANALYSIS / ASSISTANT SUBSYSTEM
### (a.k.a. what "AI" actually means here)

**Position statement, stated plainly:** 80% of the perceived intelligence is *measurement + calibrated rules + good reference targets*. Maybe 20% is neural nets, and those nets do narrow, well-posed jobs (denoise mask estimation, dereverb mask estimation, pitch tracking, voice-class classification). Anything that markets itself as "AI mixes your vocal" and is actually an end-to-end net is either not shipping or not good. We build the rigorous thing.

## 2.1 Signal front-end (shared by everything)

- **Frame:** 2048 samples @ 48 kHz (42.7 ms), hop 512 (10.7 ms), Hann analysis. For OLA reconstruction (denoise/dereverb) use √Hann analysis + √Hann synthesis with hop = N/4 (COLA-satisfying).
- **Rate normalization:** all analysis runs at a canonical **48 kHz internal analysis rate**, resampled from the host rate once. Removes an entire class of "the de-esser is tuned for 48k" bugs. (The *audio path* runs at host rate; only the *analysis* is resampled.)
- **Band mapping:** 24 Bark-ish bands + a 1/3-octave (31-band) view. Bark for perceptual decisions, 1/3-octave for user-facing display and EQ matching.
- **Voice-activity gating:** every long-term statistic is accumulated **only over frames flagged VOICED or ONSET**, never over silence. Averaging in the silence is why naive auto-EQ tools produce garbage on sparse takes.

## 2.2 Feature catalogue (rigorous definitions)

### F1. Long-Term Average Spectrum (LTAS)
Energy-mean of `|X(k,t)|²` over voiced frames, in 1/3-octave bands, normalized so that band energy sums to the total, expressed in dB relative to broadband. **Voiced frames only.** Also keep `LTAS_p10` and `LTAS_p90` per band (percentiles over time) — the *spread* tells you whether a resonance is constant (static EQ) or intermittent (dynamic EQ). This distinction is the single highest-value feature in the whole system.

### F2. Loudness (ITU-R BS.1770-4)
K-weighting (a −4 dB high-shelf at ~1.68 kHz + 2nd-order highpass at ~38 Hz), mean-square over 400 ms blocks with 75% overlap.
- **LUFS-M** (400 ms), **LUFS-S** (3 s), **LUFS-I** (gated: absolute −70 LUFS gate, then relative −10 LU gate).
- **LRA** (loudness range, 10th–95th percentile of gated short-term).
- **True peak** via 4x oversampled (or 192 kHz-equivalent) polyphase interpolation, per BS.1770 Annex 2.

Purpose: output gain staging, makeup gain, limiter ceiling, and the "match target loudness" behavior.

### F3. Crest factor & dynamics profile
- `CF(t) = truePeakDb(400ms window) − rmsDb(400ms window)`, computed per 100 ms hop over voiced frames.
- Report `CF_p50`, `CF_p90`, and **`LRA_S`** = p95−p10 of LUFS-S.
- Also: **short-term crest** (10 ms peak vs 100 ms RMS) — separates "dynamic performance" (high LRA, moderate CF) from "peaky/plosive/transient" (high short CF).

Purpose: compressor ratio, threshold, attack/release, and the split between the slow leveler and the fast peak comp.

### F4. Sibilance energy
- `S(t) = 10·log10( Σ_{5k..10k} |X|² / Σ_{300..5k} |X|² )` in dB.
- A frame is **SIBILANT** when `S(t) > S_p50 + 6 dB` **AND** `zcr > 0.15` **AND** `f0Confidence < 0.4` **AND** `flatness > 0.3`. (Multi-criteria, because energy alone fires on bright vowels and cymbal bleed.)
- Extract: fraction of frames sibilant, **peak sibilant band center** (argmax of the 4–12 kHz spectrum averaged over sibilant frames — this is what sets the de-esser center frequency; it differs by 2 kHz between voices and *that's the whole trick*), the sibilant-frame band-level distribution `S_p50 / S_p90 / S_p99`.

### F5. Noise floor
Martin's **minimum statistics**: per band, track the minimum of a smoothed periodogram over a 1.5 s sliding window, with the standard bias-compensation factor. Yields `noiseFloorDb[band]` and a broadband `noiseFloorLufs`. Fall back to the 5th percentile of per-band energy for the offline path. Also derive **SNR** = `speechLevelDb − noiseFloorDb` per band.

Purpose: gate threshold, denoise strength (per band!), and a hard veto — if SNR < 12 dB, the assistant must NOT push high-shelf air, because it would amplify hiss. Encoding vetoes like this is what separates a usable assistant from a demo.

### F6. Reverb tail / room estimate
Two estimators, cross-checked:
1. **Envelope decay (Schroeder-lite):** find speech offsets (energy drops >12 dB in <60 ms), backward-integrate the following 400 ms per band, fit a line to the −5..−25 dB region → **RT60 per band** (clamped 0.1–2.0 s; low confidence if <8 usable offsets).
2. **Envelope-spectrum / DRR proxy:** ratio of energy in the first 20 ms after an onset to the 20–150 ms window → **direct-to-reverberant ratio** proxy.

Purpose: dereverb amount, whether to add reverb at all, and pre-delay/size of the added reverb (matching the room you're in is bad; contrasting with it is good). Also a veto: RT60 > 0.8 s in the 500 Hz band ⇒ dereverb before any compression, because compression makes room tails louder.

### F7. Pitch & vibrato
**pYIN** (offline, probabilistic YIN with Viterbi) or **CREPE-tiny via ONNX** (real-time capable, ~1.5 ms/frame on one core) for `f0(t)` + confidence.
Derived stats over voiced frames: `f0_median`, `f0_p05/p95`, semitone range, **voiced fraction**, **vibrato rate** (peak of the FFT of the f0 contour in 3–8 Hz) and **vibrato depth** (cents), and **note-transition speed** (median |Δf0| across note boundaries).

Purpose: pitch-correction retune speed (fast vibrato ⇒ slower retune, or the vibrato gets eaten — the #1 complaint about auto-tune presets), key/scale suggestion, voice-class classification, and de-esser/EQ frequency scaling.

### F8. Formants
LPC on pre-emphasized (`1 − 0.97 z⁻¹`) voiced frames, order `2 + sr/1000` (≈ 26 at 48k... in practice we downsample to 16 kHz for LPC and use order 18). Root-solve → `F1..F4` + bandwidths. Report medians and IQRs over voiced frames.

Purpose — and this is the differentiator:
- **Scale EQ node frequencies to the voice, not to fixed Hz.** "Boxiness" isn't at 300 Hz; it's near `F1_median × 1.3`. "Presence" isn't at 3 kHz; it's near `F3_median`. Two singers can be 400 Hz apart on the same descriptor.
- **Formant-preserving pitch shift** needs the envelope anyway.
- **Voice class** (weight/brightness) for target-curve selection.

### F9. Breath detection
Frame features: low energy (−45..−25 dB rel. speech), high spectral flatness (>0.4), no F0 (conf < 0.25), centroid 1–4 kHz, slow attack (envelope rise > 40 ms), duration 80–600 ms. Score = weighted sum, then hysteresis + median filtering over 5 frames, then merge into segments.
Ship this as a **small GBM/logreg classifier** trained on hand-labeled data (this is a real, tractable ML win — ~500 labeled breaths gets you >92% F1) rather than pure thresholds. Falls back to the thresholds if the model isn't loaded.

Purpose: breath control (attenuate N dB, not gate — gating breaths sounds unnatural), and *excluding* breaths from all other statistics.

### F10. Plosive detection
Energy burst with: band-limited energy `<120 Hz` rising >10 dB in <20 ms, LF/HF ratio spike >15 dB, at a speech onset, duration <150 ms. Also detect DC-ish excursions (mean over 10 ms exceeding 2% of full scale).

Purpose: places and times a dynamic HPF / transient-triggered LF cut rather than a static 100 Hz HPF that thins the whole vocal.

### F11. Resonance detection (the "surgical EQ" feature)
1. Take `LTAS` in dB over a fine (1/12-octave) grid.
2. Compute a smooth baseline: cepstral liftering (keep first ~30 quefrency bins) or a 1-octave-wide moving median.
3. `excess(f) = LTAS(f) − baseline(f)`.
4. Peak-pick `excess` with prominence > 3 dB; estimate Q from the −3 dB width of the peak in the excess curve.
5. For each peak, compute **intermittency** = `LTAS_p90(f) − LTAS_p50(f)`. If > 5 dB ⇒ **dynamic** EQ node (it only resonates on certain notes); else ⇒ **static** node.
6. Rank by `prominence × bandWeight(f)` where `bandWeight` up-weights 150–500 Hz (mud/box) and 2–5 kHz (harsh) — the bands that actually hurt.
7. Emit at most **4** nodes. Never more. More than four surgical cuts is a mixing engineer's tell for "the tool is guessing."

### F12. Misc / integrity
Clipping (consecutive samples ≥ 0.999, or true-peak > 0 dBTP), DC offset, channel correlation (is the "stereo" file actually mono?), estimated original bandwidth (detect an MP3 lowpass at 15/16 kHz — changes the air-band strategy entirely), hum detection (peaks at 50/60 Hz + harmonics).

## 2.3 The `VocalProfile` (the analysis output contract)

```python
@dataclass
class VocalProfile:
    schema: str = "vox.profile/1"
    sr: float; duration_s: float; channels: int
    # loudness
    lufs_i: float; lufs_s_p10: float; lufs_s_p95: float; lra: float
    true_peak_db: float; clipped_pct: float; dc_offset: float
    # dynamics
    crest_p50: float; crest_p90: float; short_crest_p90: float
    # spectrum
    ltas_third_octave_db: list[float]     # 31 bands, normalized
    ltas_p90_minus_p50_db: list[float]    # intermittency per band
    resonances: list[Resonance]           # f, gain_excess_db, q, intermittency, dynamic:bool
    band_snr_db: list[float]
    noise_floor_lufs: float; hum_hz: float | None; bandwidth_hz: float
    # sibilance
    sibilant_frac: float; sibilant_center_hz: float
    sibilance_p50_db: float; sibilance_p90_db: float; sibilance_p99_db: float
    # room
    rt60_by_band_s: list[float]; rt60_confidence: float; drr_proxy_db: float
    # voice
    f0_median_hz: float; f0_p05: float; f0_p95: float; voiced_frac: float
    vibrato_rate_hz: float; vibrato_depth_cents: float; note_transition_ms: float
    formants_hz: list[float]              # F1..F4 medians
    voice_class: str                      # "low-male"|"male"|"female"|"high-female"|"spoken"|"rap"
    # events
    breaths: list[Segment]; plosives: list[Segment]
    # meta
    confidence: dict[str, float]          # per-feature confidence 0..1
```

Every field carries a confidence. **Low confidence ⇒ the assistant does nothing** for the params that depend on it. Doing nothing is a valid, and often correct, output.

## 2.4 Feature → parameter mapping (the decision layer)

Implemented as a **rule set with explicit formulas, guard bands, and a confidence gate**, in `assistant/rules.py`. Not a black box. Every decision emits a rationale string that the UI can display ("Cutting 3.2 dB at 412 Hz — resonance 5.1 dB above your voice's baseline, present in 34% of frames").

Concrete table (initial calibration; these numbers get tuned against a listening panel, but they must *start* as explicit numbers, not vibes):

| Target parameter | Formula | Guard |
|---|---|---|
| `hpf.freq` | `clamp(0.7 * f0_p05, 50, 120)` Hz; if plosive count/min > 3, add a *dynamic* LF cut instead of raising the static HPF | never above 120 Hz |
| `gate.threshold` | `noise_floor_lufs + 8 dB` | clamp [−70, −32] dBFS; hysteresis 6 dB; **disabled if SNR > 40 dB** (nothing to gate) |
| `gate.range` | `min(SNR_broadband − 6, 18)` dB | never full mute — mute sounds worse than noise |
| `denoise.amount` | `clamp((30 − SNR_dB) / 20, 0, 1)`, per-band scaled by `band_snr` | hard cap 0.7 in v1; over-denoised vocals are instantly recognizable |
| `dereverb.amount` | `clamp((RT60_500 − 0.25) / 0.55, 0, 1) * rt60_confidence` | 0 if `rt60_confidence < 0.5` |
| `eq.node[i]` (surgical) | from F11: `f = peak.f`, `Q = clamp(peak.q, 2, 8)`, `gain = −min(peak.excess − 2, 6)` dB; `dynamic = peak.intermittency > 5 dB` | max 4 nodes; total cut ≤ 12 dB summed |
| `eq.tone` (tonal) | Match `LTAS` to `target_curve[voice_class, style]` using **≤3** low-order shapes (low shelf, one broad bell, high shelf), solved by weighted least squares on the 1/3-octave error with a smoothness penalty | each move ≤ ±4 dB; **air shelf vetoed if band_snr(>10k) < 12 dB or bandwidth < 16 kHz** |
| `deess.freq` | `sibilant_center_hz` (typ. 5.5–9 kHz) | clamp [4.5k, 11k] |
| `deess.threshold` | set so predicted GR at `sibilance_p90` equals `target_gr` where `target_gr = clamp((sibilance_p90 − sibilance_p50) − 4, 2, 8)` dB | max GR cap 10 dB |
| `leveler.*` (slow) | ratio `2:1`, attack 30 ms, release 300 ms, threshold set so predicted GR at `LUFS-S p50` = `clamp((LRA − 6)/2, 0, 6)` dB | GR cap 8 dB |
| `comp.ratio` (fast) | `clamp(1 + (crest_p90 − 8) / 6, 1.5, 4.0)` | — |
| `comp.threshold` | Newton-solve on the measured level histogram so that **90th-percentile GR = target**, `target = clamp((crest_p90 − 10) * 0.6, 2, 6)` dB | GR cap 10 dB |
| `comp.attack` | `clamp(note_transition_ms * 0.4, 3, 30)` ms — faster material ⇒ faster attack | — |
| `comp.release` | `clamp(60000 / (bpm * 2), 80, 400)` ms if tempo known, else `clamp(LRA * 30, 100, 400)` | — |
| `sat.drive` | `clamp((6 − crest_p90/2), 0, 4)` dB; more drive for already-dense sources is wrong — this *reduces* drive when the source is peaky | mix ≤ 40% |
| `pitch.retune_speed` | `clamp(40 − vibrato_depth_cents * 0.6, 5, 60)` ms; scale key/scale from detected f0 histogram | off by default; opt-in |
| `breath.reduction` | `−6 dB` if breath density > 8/min, else `−3 dB` | never > −12 dB, never a hard gate |
| `reverb.predelay` | `clamp(note_transition_ms * 0.5, 15, 60)` ms; `size` chosen to *contrast* recorded RT60 | 0 if `dereverb.amount > 0.5` |
| `out.gain` | `target_lufs − lufs_i_after_chain` (measured on a second pass / rolling in RT) | — |
| `limiter.ceiling` | `−1.0 dBTP` default, `−0.3` for "mastered" style | — |

**Ordering matters and is part of the rules**: the assistant runs a *staged solve* — (1) integrity/repair (gate, denoise, dereverb, hum, plosive), (2) subtractive EQ, (3) dynamics, (4) tonal EQ, (5) saturation/character, (6) space, (7) output/limiting. Each stage re-measures the signal after the previous stages are applied (in the prototype: literally re-render; in the plugin: use the analysis bus's post-stage taps). This closed loop is what makes it converge rather than stack up compounding errors.

**ML models, precisely scoped:**

| Model | Job | Size | Where it runs | In audio path? |
|---|---|---|---|---|
| `denoise_mask` | per-band gain mask from noisy magnitude spectrum (GRU/CRN, DeepFilterNet-class) | 1–3 M params | RT worker thread, `HopBuffer` | **Yes** — latency-bearing |
| `dereverb_mask` | same shape, reverb suppression | 1–3 M | RT worker thread | **Yes** |
| `pitch` (CREPE-tiny) | f0 + confidence | 0.5 M | analysis thread | No |
| `voice_class` | 6-way classification from LTAS + formants + f0 | tiny (GBM) | analysis thread | No |
| `breath_plosive` | frame classification | tiny (GBM) | analysis thread | No |
| *(stretch)* `target_curve` | learned per-style EQ target from a pro-vocal corpus | it's a lookup table + regression | analysis thread | No |

The **target curves** are data, not magic: average LTAS of N professionally-mixed vocals per (voice_class × style), stored as 31-band `.npz`. This is the highest-ROI "AI" asset in the product and it costs a data-collection effort, not a research effort.

---

# 3. PYTHON PROTOTYPE — CONCRETE SPEC

## 3.1 File tree

```
vox/
├── pyproject.toml
├── README.md
├── vox/
│   ├── __init__.py
│   ├── core/                       # ==== PORTS 1:1 TO C++ ====
│   │   ├── stage.py                # Stage ABC, PrepareSpec, StageContext, rt_checked
│   │   ├── params.py               # ParamDesc, Param, ParamSet, LinearSmoothedValue
│   │   ├── chain.py                # Chain, ParallelSplit, latency-matched bypass
│   │   ├── bus.py                  # AnalysisBus, FeatureFrame, SpscRing (list-backed here)
│   │   ├── hopbuffer.py            # fixed-hop adapter (block-size independence)
│   │   ├── oversample.py           # Oversampled decorator, polyphase FIR w/ state
│   │   ├── delay.py                # DelayLine (integer + Thiran allpass)
│   │   └── dsp/
│   │       ├── svf.py              # TPT state-variable filter (LP/HP/BP/notch/shelf/bell)
│   │       ├── biquad.py           # RBJ coeffs (design only; SVF is the runtime)
│   │       ├── envelope.py         # attack/release followers, RMS, peak, log-domain
│   │       ├── detector.py         # sidechain detector w/ filters
│   │       ├── fft.py              # STFT/ISTFT with persistent OLA state (NOT librosa)
│   │       ├── window.py
│   │       └── truepeak.py         # BS.1770 4x polyphase true-peak meter
│   ├── stages/                     # ==== PORTS 1:1 TO C++ ====
│   │   ├── trim.py  hpf.py  gate.py
│   │   ├── denoise.py  dereverb.py  deplosive.py  debreath.py
│   │   ├── eq_static.py  eq_dynamic.py  deesser.py
│   │   ├── leveler.py  comp.py  limiter.py
│   │   ├── saturate.py  pitch.py  doubler.py  delay_fx.py  reverb.py
│   │   └── registry.py             # type_id -> class, for preset loading
│   ├── analysis/                   # ==== REWRITTEN in C++, analysis thread ====
│   │   ├── frontend.py             # the ONE shared STFT + resample to 48k
│   │   ├── loudness.py             # BS.1770-4 (own impl, not pyloudnorm — we must port it)
│   │   ├── spectrum.py             # LTAS, percentiles, band mapping, resonance detection
│   │   ├── dynamics.py             # crest, LRA
│   │   ├── sibilance.py
│   │   ├── noise.py                # Martin minimum statistics
│   │   ├── room.py                 # RT60 / DRR
│   │   ├── pitch.py                # pYIN + CREPE-onnx backend
│   │   ├── formants.py             # LPC
│   │   ├── events.py               # breath / plosive / sibilant segmentation + classifier
│   │   └── profile.py              # VocalProfile dataclass + aggregate()
│   ├── assistant/
│   │   ├── rules.py                # the §2.4 table, as code
│   │   ├── targets.py              # target LTAS curves, style definitions
│   │   ├── solver.py               # EQ-match least squares; threshold Newton-solve
│   │   ├── stagedsolve.py          # the 7-phase closed-loop re-measure solve
│   │   └── explain.py              # rationale strings
│   ├── io/
│   │   ├── preset.py               # JSON schema (pydantic), load/save/migrate
│   │   ├── audio.py                # soundfile wrappers, SR conversion, dithering
│   │   └── report.py               # HTML/plot report for A/B review
│   ├── models/                     # .onnx files + loader
│   │   └── loader.py
│   └── cli.py                      # typer app
├── presets/
│   ├── default.json
│   ├── styles/{modern-pop,rap,podcast,rock,rnb,voiceover}.json
│   └── targets/ltas_{voiceclass}_{style}.npz
├── tests/
│   ├── conftest.py
│   ├── assertions.py               # objective audio assertions (§3.6)
│   ├── golden/
│   │   ├── inputs/*.wav            # small, licensed/synthetic
│   │   ├── expected/*.wav
│   │   ├── expected/*.profile.json
│   │   └── manifest.json           # input, preset, tolerances, per-case
│   ├── test_framework_invariants.py  # block-size, reset, latency, SR — runs on EVERY stage
│   ├── test_stage_*.py
│   ├── test_analysis_*.py
│   ├── test_assistant_rules.py
│   └── test_golden_render.py
└── tools/
    ├── make_golden.py              # regenerate expected/ (gated behind an explicit flag)
    ├── bench.py                    # per-stage µs/sample, to sanity-rank CPU cost
    ├── export_onnx.py
    ├── build_targets.py            # build target LTAS curves from a reference corpus
    └── xcheck_cpp.py               # diff Python render vs C++ `voxrender` output
```

## 3.2 Dependencies

```toml
[project]
requires-python = ">=3.11"
dependencies = [
  "numpy>=1.26",
  "scipy>=1.11",
  "soundfile>=0.12",
  "onnxruntime>=1.17",
  "pydantic>=2.6",
  "typer>=0.12",
]
[project.optional-dependencies]
analysis = ["librosa>=0.10", "scikit-learn>=1.4"]   # analysis/ ONLY
dev = ["pytest>=8", "pytest-xdist", "matplotlib", "hypothesis", "ruff", "mypy"]
```

**Hard policy, enforced by a test:** `vox/core/**` and `vox/stages/**` may import only `numpy` and stdlib. A test walks the AST of those files and fails on any other import. This is the single cheapest guarantee that the port is a transliteration.

```python
# tests/test_framework_invariants.py
FORBIDDEN_IN_RT = {"librosa", "sklearn", "scipy", "pandas", "torch", "onnxruntime"}
def test_rt_modules_are_portable():
    for p in Path("vox/core").rglob("*.py"), Path("vox/stages").rglob("*.py"):
        ...  # ast.parse, collect Import/ImportFrom, assert root not in FORBIDDEN_IN_RT
```
(scipy is permitted at *prepare/design* time only, behind a `_design.py` module that the runtime never calls — or simpler: forbid it outright and hand-code the coefficient math, since we have to hand-code it in C++ anyway. **Recommendation: forbid it outright.** Writing RBJ coefficients by hand is 40 lines and it's 40 lines you'd write in C++ next month regardless.)

## 3.3 CLI

```
vox analyze  IN.wav [--sr 48000] [-o profile.json] [--report report.html]
vox assist   profile.json --style modern-pop [--intensity 0.8] [-o preset.json] [--explain]
vox render   IN.wav -p preset.json -o OUT.wav
             [--block 512] [--sr 48000] [--os 4] [--seed 0] [--trace trace.npz]
vox auto     IN.wav --style modern-pop -o OUT.wav      # analyze|assist|render in one shot
vox ab       IN.wav -p a.json -p b.json -o ab/         # renders + null test + diff report
vox measure  OUT.wav                                    # LUFS/TP/LRA/spectrum of a render
vox golden   [--update] [--filter test_name]            # run/refresh the regression suite
vox bench    -p preset.json --block 64 --dur 30         # per-stage timing profile
```

`--block` is a first-class, load-bearing flag. **Every render in CI runs at multiple block sizes and the outputs must match.** `--trace` dumps the per-block param values and per-stage GR to an npz for plotting — this is how you debug an assistant that "did something weird at 0:47."

## 3.4 Preset / config JSON format

Versioned, flat, stage-list. Same file loads in Python and C++ (the C++ side parses it with a small hand-rolled or `nlohmann::json` reader; the *plugin* stores this exact JSON inside its ValueTree, so presets are portable both ways from day one).

```json
{
  "schema": "vox.preset/1",
  "name": "Modern Pop — Female",
  "created": "2026-08-13T00:00:00Z",
  "assist": { "amount": 1.0, "profileRef": "profile.json", "style": "modern-pop" },
  "chain": [
    { "id":"trim",   "type":"trim",   "bypass":false, "params":{"gain_db": 0.0} },
    { "id":"hpf",    "type":"hpf",    "bypass":false, "params":{"freq_hz": 78.0, "slope": 12} },
    { "id":"gate",   "type":"gate",   "bypass":false,
      "params":{"threshold_db": -48.0, "range_db": 14.0, "attack_ms": 2.0,
                "hold_ms": 40.0, "release_ms": 120.0, "lookahead_ms": 3.0} },
    { "id":"dn",     "type":"denoise","bypass":false,
      "params":{"amount": 0.35, "model": "denoise_v1", "band_bias_db": [0,0,-2, "..."]} },
    { "id":"eqs",    "type":"eq_static","bypass":false,
      "params":{"nodes":[
        {"kind":"bell","freq_hz":412,"gain_db":-3.2,"q":4.5},
        {"kind":"bell","freq_hz":2870,"gain_db":-2.1,"q":3.0}]} },
    { "id":"eqd",    "type":"eq_dynamic","bypass":false,
      "params":{"nodes":[{"freq_hz":238,"q":5.0,"threshold_db":-24,"range_db":-5}]} },
    { "id":"deess",  "type":"deesser","bypass":false,
      "params":{"freq_hz": 7200, "q": 2.5, "threshold_db": -28.0,
                "ratio": 4.0, "max_gr_db": 8.0, "mode": "split"} },
    { "id":"lev",    "type":"leveler","bypass":false,
      "params":{"threshold_db":-26,"ratio":2.0,"attack_ms":30,"release_ms":300} },
    { "id":"cmp",    "type":"comp",   "bypass":false,
      "params":{"threshold_db":-18,"ratio":3.0,"knee_db":6,"attack_ms":8,
                "release_ms":180,"makeup_db":3.0,"mix":1.0} },
    { "id":"sat",    "type":"saturate","bypass":false,
      "params":{"drive_db":2.0,"mix":0.25,"mode":"tube"}, "oversample": 4 },
    { "id":"eqt",    "type":"eq_static","bypass":false,
      "params":{"nodes":[{"kind":"highshelf","freq_hz":9000,"gain_db":2.4,"q":0.7}]} },
    { "id":"rev",    "type":"reverb", "bypass":false,
      "params":{"mix":0.12,"size":0.4,"predelay_ms":32,"damp_hz":6000} },
    { "id":"lim",    "type":"limiter","bypass":false,
      "params":{"ceiling_dbtp":-1.0,"lookahead_ms":2.0,"release_ms":80} }
  ],
  "meta": { "target_lufs": -14.0, "rationale": { "eqs.nodes[0]": "412 Hz resonance, +5.1 dB over baseline, 34% of frames" } }
}
```

Rules: no derived values stored (no sample counts, no coefficients); unknown keys are preserved on round-trip (forward compat); `schema` drives a migration chain `migrate_1_to_2(d)`.

## 3.5 Golden-file regression harness

`tests/golden/manifest.json` drives everything:

```json
{ "cases": [
  { "name": "female_pop_dry", "input": "inputs/female_pop_dry.wav",
    "preset": "presets/styles/modern-pop.json",
    "expected_audio": "expected/female_pop_dry.wav",
    "expected_profile": "expected/female_pop_dry.profile.json",
    "tolerances": { "spectral_db": 0.35, "lufs": 0.1, "true_peak": 0.1,
                    "sample_rms_db": -70, "profile_rel": 0.02 },
    "block_sizes": [1, 31, 64, 128, 512, 1024, 4096],
    "sample_rates": [44100, 48000, 96000] } ] }
```

Inputs: a small set of **synthetic + short licensed** clips, each 5–15 s, checked into git (WAV, 48k/24-bit, ~10 MB total). Include deliberately adversarial cases: heavy sibilance, loud plosives, roomy recording, hiss, clipped input, near-silence, a pure sine, an impulse, DC, and a mono file in a stereo container.

## 3.6 Objective audio assertions (`tests/assertions.py`)

These are the actual quality gate. Sample-exact comparison is used *within* Python; **cross-language** comparison uses spectral tolerances.

```python
def assert_block_size_invariant(chain_factory, x, sizes=(1,31,64,128,512,4096), tol_db=-140):
    """THE most valuable test in the suite. Catches every state-across-blocks bug."""
    ref = render(chain_factory(), x, block=512)
    for b in sizes:
        y = render(chain_factory(), x, block=b)
        assert rms_db(y - ref) < tol_db, f"block {b} differs at {rms_db(y-ref):.1f} dB"

def assert_reset_idempotent(stage, x):
    a = render_stage(stage, x); stage.reset(); b = render_stage(stage, x)
    assert np.array_equal(a, b)

def assert_reported_latency(stage, tol=0):
    """Impulse in, measure group delay via cross-correlation peak, compare to declaration."""
    y = render_stage(stage, impulse(8192))
    measured = int(np.argmax(np.abs(np.correlate(y, impulse(8192), 'full'))) - 8191)
    assert abs(measured - stage.latency_samples()) <= tol

def assert_bypass_is_null(chain, x, tol_db=-120):
    """All stages bypassed => output == input, delayed by reported latency, sample-exact."""

def assert_no_zipper(stage, x, param, v0, v1, tol_db=-60):
    """Step a param mid-render; assert max |Δsample| over the step is bounded and
    the difference signal has no energy above 8 kHz beyond `tol_db`."""

def assert_spectrum_within(y, ref, tol_db=0.35, fmax=18000, weight="bark"):
    """Band-limited, Bark-weighted LTAS comparison. THE cross-language gate."""

def assert_finite_and_bounded(y, peak=4.0)                  # no NaN/Inf/blowup
def assert_no_denormal_hazard(stage)                        # tail decays below 1e-30 in <5 s
def assert_lufs_within(y, target, tol=0.1)
def assert_true_peak_below(y, ceiling_dbtp=-1.0, tol=0.05)
def assert_sr_response_match(stage_factory, rates, tol_db=0.25, fmax=18000)
def assert_gr_within(trace, stage_id, p90_target, tol_db=1.0)  # assistant closed-loop check
def assert_profile_close(a, b, rel=0.02)                    # analysis stability
def assert_assistant_monotone(profile, key, direction)
    """Property test: more noise in => denoise.amount must not decrease.
       More sibilance => de-ess GR must not decrease. Etc. Hypothesis-driven."""
```

Plus **property-based tests via Hypothesis** on the assistant: generate random plausible `VocalProfile`s, assert every emitted param is inside its `assistMin/assistMax` cage, that no NaN escapes, and that the monotonicity relations hold. This catches rule regressions far better than golden files.

**CI:** on every PR — full pytest matrix, the AST import-policy test, block-size invariance across all stages, golden renders. Goldens are regenerated only via `tools/make_golden.py --i-really-mean-it` in a dedicated PR with audible-diff plots attached.

---

# 4. C++ / JUCE PORT PLAN

## 4.1 Repo layout

```
vox-plugin/
├── CMakeLists.txt                # CPM/FetchContent: JUCE, Catch2, onnxruntime, nlohmann_json
├── CMakePresets.json
├── libs/voxdsp/                  # NO JUCE. Pure C++20. This is the port target.
│   ├── include/vox/{Stage,Param,Chain,AnalysisBus,HopBuffer,...}.h
│   ├── src/core/  src/stages/  src/analysis/  src/assistant/
│   └── tests/                    # Catch2, mirrors tests/assertions.py
├── apps/voxrender/               # offline CLI renderer — SAME CLI as `vox render`
├── plugin/
│   ├── PluginProcessor.{h,cpp}   # JUCE wrapper, APVTS, latency, bypass, state
│   ├── PluginEditor.{h,cpp}
│   ├── ui/                       # spectrum, GR traces, assist view
│   └── AssistantThread.{h,cpp}   # the non-RT worker
├── models/*.onnx
├── ci/                           # pluginval, notarization, installers
└── .github/workflows/ci.yml
```

**`voxdsp` has zero JUCE dependency.** Consequences: it compiles in 8 seconds, it's unit-testable without a plugin host, it's fuzzable, and if JUCE's licensing or API changes we're not hostage. JUCE lives only in `plugin/`. This costs maybe 3 days of writing our own `SmoothedValue`/`Oversampling`/`AudioBlock` equivalents and is worth it ten times over.

## 4.2 What maps 1:1 (transliteration, ~1–3 days per stage)

- `core/stage.py` → `Stage.h` (already isomorphic by design)
- `core/params.py` → `Param.h/cpp` (atomics replace plain floats; smoothing identical)
- `core/chain.py`, `hopbuffer.py`, `delay.py`, `oversample.py` → direct
- `core/dsp/svf.py`, `envelope.py`, `detector.py`, `truepeak.py` → direct; these are 50–150 line files with explicit state
- **All of `stages/`** — because we forced them to be written block-based, in-place, with explicit state, using only numpy scalar-ish ops. The transliteration is mechanical: `self.z1` → `float z1_`, `for n in range(N)` → `for (int n = 0; n < N; ++n)`.
- The preset JSON reader/writer (same schema, same keys)
- The assertion suite → Catch2, and `tools/xcheck_cpp.py` diffs `vox render` vs `voxrender` on every golden case with a 0.35 dB Bark-weighted spectral tolerance and a −70 dB sample-RMS tolerance.

The honest reality: even "1:1" stages take 1–3 days each because of float32 vs float64 differences, SIMD, denormal handling, and the coefficient-update-rate optimization. Budget accordingly.

## 4.3 What must be rewritten for real time

| Python thing | Why it can't ship | C++ approach |
|---|---|---|
| Any `np.*` temp array in `process()` | allocation | Preallocated scratch in `prepare()`; a per-instance `ScratchArena` (bump allocator over a fixed buffer) handed to stages |
| whole-signal FFT | non-causal | `HopBuffer` + persistent OLA state |
| `scipy.signal.filtfilt` | zero-phase = non-causal | Either causal IIR (accept phase) or FIR linear phase with declared latency |
| `librosa.stft(center=True)` | pads = looks into the future/past | Our own causal STFT |
| `resample_poly` per block | edge effects | Polyphase FIR with persistent history |
| Two-pass loudness normalization | needs the whole file | Rolling BS.1770 + a slow output-gain servo (or offline "learn" mode) |
| `onnxruntime.InferenceSession.run()` | allocates, thread pool, dynamic shapes | `IoBinding` + preallocated `Ort::Value`s, fixed shapes, 1 intra-op thread, arena pre-extended, prewarmed (§4.5) |
| Assistant re-rendering the file 7 times | obviously | Rolling estimators on the analysis thread + post-stage taps on the analysis bus |
| Python dict param lookup | hashing on RT thread | Compile-time enum index into a flat array |
| Exceptions / `assert` | RT-unsafe | `noexcept` everywhere in `process`; asserts compiled out; a debug-only RT-violation checker |

**The RT rules, written down and enforced:**
1. `process()` is `noexcept`. No `new`/`delete`/`malloc`/`std::vector::resize`/`std::string`/`std::function` (use `FunctionRef`)/`std::shared_ptr` copy.
2. No mutexes. Cross-thread: `std::atomic` (relaxed where correct) + SPSC rings + a `SpinLockGuard` *only* for the GUI-read snapshot, never on the RT side.
3. No file I/O, no logging, no `printf`, no `rand()`, no `std::chrono` in hot loops.
4. `juce::ScopedNoDenormals` at the top of `processBlock`.
5. Everything sized in `prepareToPlay(sr, maxBlockSize)`; **assume the host lies about `maxBlockSize` and defensively handle a larger block by looping in chunks** (Pro Tools AudioSuite, some offline renders, and Logic's freeze do exactly this).
6. Enforcement: build a Linux CI job with **clang RealtimeSanitizer** (`[[clang::nonblocking]]` on `process`) — this catches allocations and locks automatically. Where rtsan isn't available, ship a debug-build `RTChecker` that overrides `operator new` and asserts if the current thread is flagged as RT.

## 4.4 Lookahead buffers

Every lookahead stage (limiter, gate, de-esser in some modes, transient handling) uses a common pattern: a preallocated circular delay of `lookaheadSamples` on the *audio*, with the *detector* running on the undelayed signal.

```cpp
class Lookahead {
public:
    void prepare(int maxSamples, int numCh);        // allocates ONCE
    void setLookahead(int n) noexcept;              // n <= maxSamples, no alloc
    void pushAndPop(AudioBlock& io) noexcept;       // delays audio in-place
    int  latency() const noexcept { return n_; }
};
```

Lookahead is **fixed at prepare time**, not automatable, because changing it changes plugin latency. Users get a discrete 0/1/2/5 ms choice behind a mode switch, and we reserve max latency for the whole chain so switching never renegotiates PDC mid-playback.

## 4.5 ML inference in a real-time context (the hard part, honestly)

Two classes of model, two entirely different treatments.

**Class A — assistant/analysis models** (pitch, classifiers, voice class): run on the `AssistantThread` at normal priority. ONNX Runtime with defaults is fine. Latency of hundreds of ms is irrelevant. This is easy and should not be conflated with Class B.

**Class B — in-path models** (denoise, dereverb masks): these touch the audio. Options, ranked:

1. **Preferred: run on a dedicated worker thread with a fixed hop pipeline.**
   - RT thread → `HopBuffer` → push a magnitude frame into an SPSC ring → worker thread runs inference → pushes a gain mask back → RT thread applies the mask to the *delayed* spectrum.
   - Added latency = `hopSize × queueDepth`. With hop 256 @48k and depth 2 ⇒ **10.7 ms**. Declared via `setLatencySamples`. Deterministic.
   - **Fallback on underrun is mandatory:** if the mask isn't ready, apply the previous mask (or a smoothed identity). Audio never waits. A visible "ML overloaded" indicator, not a dropout.
   - Worker thread priority: *above normal, below RT*. Never `SCHED_FIFO` — you don't want to preempt the host's audio thread.

2. **Acceptable for small models: run inline on the RT thread.** Only if measured **99.9th-percentile** inference time < 15% of the block period across the whole target hardware matrix. For a 128-sample block at 48 kHz that's 2.67 ms period ⇒ 400 µs budget. A 1M-param GRU at 100 frames/s is roughly 200–600 µs/frame on a modern core — *borderline*. And it's not the mean that kills you, it's the tail. **Measure the p99.9, not the mean.** I would not ship inline inference for anything above ~300 k params.

3. **For small recurrent nets: skip ONNX entirely, use RTNeural** (or hand-rolled). RTNeural does compile-time-sized GRU/LSTM/Dense/Conv1D with zero allocation, is genuinely RT-safe, and is 2–5x faster than ORT for small models because there's no graph-execution overhead. **Recommendation: RTNeural for anything ≤ ~500 k params, ONNX Runtime only for the larger conv U-nets.**

**ONNX Runtime RT-safety checklist** (all of these are required, and every one of them is a bug we'd otherwise ship):
```cpp
Ort::SessionOptions o;
o.SetIntraOpNumThreads(1);
o.SetInterOpNumThreads(1);
o.SetExecutionMode(ORT_SEQUENTIAL);
o.SetGraphOptimizationLevel(ORT_ENABLE_ALL);
o.DisableCpuMemArena();                 // or pre-extend it; default arena GROWS = allocates
o.AddConfigEntry("session.use_env_allocators", "1");
// Fixed shapes only. Dynamic axes => reallocation on every shape change.
// IoBinding with pre-allocated input/output Ort::Values backed by OUR buffers:
Ort::IoBinding bind{session};
bind.BindInput ("mag",  inputValue);    // wraps our float* — no copy, no alloc
bind.BindOutput("mask", outputValue);
// Prewarm: run 50 inferences at construction so lazy init + page faults happen off-RT.
```
Even with all that, I would **not** put `session.Run()` on the audio thread without RealtimeSanitizer proving it clean, and even then the worker-thread design (option 1) is what ships.

**Model loading is not RT-safe** and takes 50–500 ms. Load on a background thread at construction; the audio path uses a bypass/identity mask until `modelReady.load()` is true. Preset changes that swap models must not stall audio.

**Platform note:** we ship CPU inference only in v1. CoreML/DirectML/CUDA execution providers add 10–100 ms of unpredictable latency and driver-dependent failure modes. Not worth it for 1–3M param models that run in 300 µs on CPU.

## 4.6 JUCE wrapper specifics

- **Formats:** VST3 + AU (macOS) + Standalone for v1. AAX in v1.1 (requires PACE signing, an Avid dev account, and ~2–3 weeks of its own integration/QA — do not bundle it into the v1 estimate). AUv3/iOS: no. VST2: no (licensing closed).
- **Parameters:** `AudioProcessorValueTreeState` for host-visible params. **Internal DSP does not read APVTS on the RT thread** — a `ParamRegistry` mirrors APVTS into a flat POD array of `std::atomic<float>`, updated by APVTS listeners. Avoids APVTS's tree traversal in the hot path.
- **Assistant params are NOT host parameters** by default (they'd flood automation lanes). The *result* of the assistant is written into the host params so automation/undo work, but as a single "Apply Assist" gesture (`beginChangeGesture`/`endChangeGesture` batched), not continuously. Continuous "learn" mode writes to a separate non-automatable layer. This is a UX decision with a hard architectural consequence — decide it now.
- **State:** `getStateInformation` writes the §3.4 preset JSON embedded in a ValueTree + a schema version. Migration on load.
- **Channel configs:** mono→mono, mono→stereo, stereo→stereo, plus an optional sidechain bus. `isBusesLayoutSupported` must reject everything else explicitly or Logic's AU validation fails in creative ways.
- **Editor:** open/close must not touch DSP state. GUI reads a triple-buffered snapshot of meters/spectrum published by the RT thread; never a lock.

## 4.7 Build & CI

- **CMake 3.24+**, JUCE via `FetchContent` pinned to a tag. `CMakePresets.json` for `debug`, `release`, `asan`, `rtsan`.
- **GitHub Actions matrix:** macOS-14 (arm64 + x86_64 → universal binary via `CMAKE_OSX_ARCHITECTURES`), Windows Server 2022 (MSVC x64), Ubuntu 22.04 (for sanitizers + the headless golden tests).
- Jobs: (1) build all formats; (2) Catch2 unit tests; (3) **pluginval strict level 10** on VST3 + AU; (4) ASan/UBSan Linux; (5) **RealtimeSanitizer** on `voxdsp` process paths; (6) **golden cross-check** — `voxrender` vs the checked-in Python goldens with spectral tolerance; (7) **CPU benchmark** with a regression gate (fail if any stage's µs/sample regresses > 10% vs the baseline in `bench/baseline.json`).
- **Signing/notarization** on macOS (Developer ID + `notarytool`), Authenticode on Windows. Installers: `pkgbuild`/`productbuild` on mac, WiX or Inno on Windows.
- **Nightly**: long-run soak (2 hours of continuous processing with random param automation and random block sizes) checking for NaN, drift, memory growth, and denormal-induced CPU creep. This catches things nothing else does.

---

# 5. WHERE THE PYTHON PROTOTYPE WILL LIE TO US

Every one of these has cost a real audio team real months. Listed with the mitigation, because "be aware of it" is not a mitigation.

**5.1 Allocation is free.** Every numpy op allocates. In Python you'll happily write `y = np.tanh(x * g) * m` inside a "process" function. In C++ that's three heap allocations per block per stage, and on the RT thread it's a dropout waiting for a page fault. *Mitigation:* `rt_checked` decorator asserting no reallocation of `io`; a `--strict-rt` render mode that wraps numpy's allocator and counts allocations per block, failing if > 0 for in-place-capable stages. Realistically we allow scratch buffers but require them to be **preallocated in `prepare()` as instance members**, exactly like C++. Test: assert every stage's `prepare` allocates and its `process` does not (via `tracemalloc` deltas).

**5.2 Block size doesn't exist.** The single biggest lie. Offline you process a 30-second array. Every state-across-block bug — uninitialized filter memory, OLA misalignment, envelope discontinuity, lookahead off-by-one — is invisible. *Mitigation:* `assert_block_size_invariant` runs on **every stage in CI**, including block size **1** and prime sizes like 31 and 127. Non-negotiable.

**5.3 Non-causality is invisible.** `scipy.signal.filtfilt` is zero-phase and looks into the future. `np.roll`, `librosa.stft(center=True)`, `scipy.signal.resample`, any `[::-1]`, any percentile over the whole file, any `np.max(x)` normalization — all of these use information a real-time plugin does not have. They will sound *better* than anything shippable, and you will chase that sound for a month. *Mitigation:* forbid `filtfilt` and `center=True` in `stages/`; the import-policy test blocks scipy from `stages/` entirely. Any lookahead must be an explicit `Lookahead` object that reports latency, so the cost is visible in the preset and in the tests.

**5.4 Edge effects are hidden.** `resample_poly`, `stft`, and friends pad the array edges. Over a 30-second render that's 0.001% of samples. In a plugin, *every block boundary is an edge* if you use those functions per-block. *Mitigation:* our own `fft.py` and polyphase resampler with persistent history buffers, and a test that renders a continuous sine in blocks and asserts THD+N < −100 dB (any edge discontinuity shows up as broadband noise instantly).

**5.5 Denormals don't hurt.** Python/numpy on x86 usually runs with denormals enabled and you won't notice, because you're not running 40 IIR filters × 8 instances in real time. In the plugin, a reverb tail decaying into denormals can be a **100x** slowdown and a sudden CPU spike 10 seconds after the singer stops. *Mitigation:* the nightly soak test; explicit denormal-flush in every recursive stage regardless of FTZ; and `assert_no_denormal_hazard` checking that tails reach exactly 0.0 (not 1e-300) within 5 s.

**5.6 float64 vs float32.** numpy defaults to float64. Filters that are perfectly stable in double can be marginally unstable in float32, especially low-frequency biquads at 96 kHz (that's the classic: a 30 Hz HPF at 192 kHz in Direct Form II float32 is numerically garbage). *Mitigation:* the prototype uses **float32 throughout the audio path** (`dtype=np.float32`, enforced by the `rt_checked` wrapper), TPT/SVF topologies rather than DF-II, and a stability test sweeping filter frequency from 10 Hz to 0.45·SR at every supported rate asserting bounded output.

**5.7 CPU cost is unknowable.** Python tells you *nothing* about whether the chain fits. numpy FFT is FFTW-class SIMD; your first C++ FFT probably isn't. Conversely, a Python loop is 100x slower than the C++ it becomes, so slow Python code may be cheap and fast Python code (big vectorized ops) may be expensive. *Mitigation:* `tools/bench.py` gives only an **ordinal ranking** of stage cost, never an absolute budget. Set the real budget in C++ early: build `voxrender` and the plugin skeleton in **week 3**, not month 6, and put a CPU regression gate in CI from the first stage. State the target explicitly: **< 4% of one core per instance at 48 kHz / 128-sample blocks on an M1 / Ryzen 5000**, so 16 instances fit in a session.

**5.8 Parameter changes are free and instantaneous.** In the prototype you set `comp.threshold = -18` once and render. In the plugin, users automate it, the assistant moves it continuously, and every un-smoothed param produces zipper noise; every coefficient recomputation costs CPU. *Mitigation:* `assert_no_zipper` on every continuous param; a `--automate` render mode that modulates every param with an LFO during the golden render and asserts no HF artifacts; the `smoothMs > 0` requirement enforced by a test over the param registry.

**5.9 Threading doesn't exist.** The prototype is single-threaded and deterministic. The plugin has an RT thread, a GUI thread, an assistant thread, and an ML worker thread, with real races, real priority inversion, and real memory-ordering bugs. Nothing in the prototype rehearses this. *Mitigation:* build the `AnalysisBus` with the same SPSC-ring API in Python **even though it's pointless there** — so the assistant is written against a "measurements arrive as a stream, decisions go back as a stream" model from day one, not against "I have the whole file." Then the C++ threading is a mechanical substitution rather than an architectural change. Also: TSan in CI, and a fuzz test that hammers `setState`/`prepare`/`process`/editor-open from multiple threads.

**5.10 The assistant sees the whole file.** Offline, the assistant computes percentiles over 3 minutes of audio. In the plugin's real-time "learn" mode it has seen 8 seconds and the singer hasn't hit the loud chorus yet. Decisions will differ, and the plugin's will look worse. *Mitigation:* implement **both modes in the prototype from the start** — `--assist-mode offline` and `--assist-mode streaming --window 10s` — and make the golden tests assert that streaming converges to within a stated tolerance of offline after N seconds. Design the estimators to be **online-capable** (exponentially-weighted quantile estimators like P²/t-digest, Martin minimum statistics, rolling BS.1770) rather than batch percentiles. If a feature can't be estimated online, either it's offline-only (fine, label it) or it's not in the product.

**5.11 Latency is free.** Offline, adding 4096 samples of lookahead costs nothing and sounds great. In a plugin it's 85 ms and the singer can't track to it. *Mitigation:* every preset carries its total latency; a test asserts the default preset's latency is **< 15 ms** (a hard product constraint for tracking) and that a "low latency" mode exists at **< 5 ms** with the linear-phase/ML/lookahead stages auto-swapped for causal alternatives. Design the low-latency variants *now*, not after the sound is locked.

**5.12 Host reality.** Bypass ramping, transport jumps, offline bounce running at 100x with different block sizes, sample-rate changes mid-session, freeze/unfreeze, plugin state restored while audio is running, Pro Tools AudioSuite handing you a 40-million-sample buffer, Logic calling `prepareToPlay` twice with different block sizes before playing a note, VST3 wanting silent-flags handling for tails. None of this exists in Python. *Mitigation:* pluginval level 10 in CI from week 4, plus a manual DAW compatibility matrix that is scheduled work, not a hope.

**5.13 Numerical divergence between Python and C++ is guaranteed.** Different FFT libs, different `exp`/`tanh` implementations, different rounding, SIMD reassociation. Sample-exact cross-language equality is **not achievable** and chasing it wastes weeks. *Mitigation:* decide the tolerance up front — cross-language gate is **Bark-weighted spectral difference < 0.35 dB up to 18 kHz** and **sample-level RMS difference < −70 dB**. Anything failing that is a real bug; anything passing it is not worth investigating.

**5.14 ONNX behaves differently.** `onnxruntime` in Python with default settings uses a thread pool, a growing memory arena, and dynamic shapes. The RT-safe configuration (§4.5) is a *different execution path* and can produce slightly different numerics and dramatically different timing. *Mitigation:* the Python prototype must load models with the **exact same restricted SessionOptions** the plugin will use, and a test asserts fixed input shapes.

**5.15 Everything sounds better on your own clean 24-bit studio recording.** *Mitigation:* the golden input set deliberately includes bad sources — phone recordings, room-y, clipped, MP3-transcoded, over-compressed. The assistant must degrade gracefully on all of them, and the vetoes in §2.4 exist precisely for this.

---

# 6. EFFORT ESTIMATE — BRUTALLY HONEST

Assumptions: senior engineers who have shipped audio plugins before; the Python prototype exists and its DSP is *sonically approved* before porting starts (if it isn't, add 30% for re-tuning in C++); "shippable" means it survives pluginval L10, the DAW matrix, and a 200-user beta.

## 6.1 C++ plugin, full-scope v1

| Area | Person-weeks | Notes |
|---|---:|---|
| Core framework (`voxdsp`: Stage/Param/Chain/HopBuffer/Oversampling/AnalysisBus/latency) | 5 | Front-loaded, unblocks everything |
| EQ (static + dynamic, TPT, up to 8 bands, spectrum-accurate) | 3.5 | |
| De-esser (split-band + wideband modes) | 2 | |
| Gate / expander with lookahead | 1.5 | |
| Leveler + compressor (2 units, program-dependent release, knee) | 3 | |
| True-peak limiter (lookahead, multi-stage release) | 2.5 | Deceptively hard to make transparent |
| Saturation + oversampling integration | 2 | |
| HPF / trim / metering / utility | 1 | |
| Spectral denoise (mask apply + ML integration + spectral-gate fallback) | 5 | |
| Dereverb | 4 | |
| De-plosive / de-breath (dynamic, event-triggered) | 1.5 | |
| Doubler / widener | 2 | |
| Delay | 2 | |
| Reverb (algorithmic FDN, actually good) | 5 | "Actually good" is the expensive word |
| **Pitch correction (real-time, formant-preserving, low latency)** | **10** | Genuinely hard. This is a product on its own. High variance: 8–16. |
| Analysis subsystem in C++ (all of §2.2, online estimators) | 6 | |
| Assistant rules + staged solve + streaming mode + explanations | 4 | |
| ONNX/RTNeural integration, worker threading, prewarm, fallbacks | 4 | |
| Preset/state/versioning/migration/factory presets | 2 | |
| Plugin wrapper: formats, buses, bypass, sidechain, host quirks | 3 | |
| **UI** (Nectar-class: spectrum, GR traces, assist view, node editing, resizing, dark/light, accessibility) | **16** | Consistently the most underestimated. 16 is optimistic if the design is ambitious. |
| Test infrastructure: Catch2, golden cross-check, RT-safety, benchmarks | 5 | |
| CI, signing, notarization, installers | 3 | |
| Performance work: profiling, SIMD, cache, CPU-budget hunting | 4 | |
| DAW compatibility matrix + bug bash (Logic, Live, Cubase, Reaper, Studio One, FL) | 5 | |
| Beta feedback, bug fixing, sonic re-tuning | 6 | |
| **Subtotal** | **103** | |
| **Risk buffer (+25%)** — integration, unknowns, "the compressor doesn't sound right yet" | **26** | |
| **TOTAL** | **~129 person-weeks** | |

### What that means in calendar time

- **1 senior dev:** ~2.5 years. Don't.
- **4 people** (2 DSP, 1 UI, 1 ML/infra, with the DSP leads splitting the plugin wrapper): parallelism is imperfect — call it 70% efficiency ⇒ `129 / (4 × 0.7) ≈ 46 weeks` ≈ **11 months to v1.0**, of which the last ~2 months is beta and hardening.
- **6 people:** efficiency drops to ~60% ⇒ ~36 weeks ≈ **8–9 months**. Adding people past 6 does not help; the DSP work has hard serial dependencies.

Plus the Python prototype phase itself: **8–12 person-weeks** before porting begins (framework 2, stages 4, analysis 3, assistant 2, tests 1.5). This is cheap and it is the highest-leverage money in the project. Do not skip it, do not rush it, and do not start the C++ before the sound is approved — but *do* stand up the C++ skeleton + CI in parallel from week 3, because a CI harness that arrives in month 6 is worthless.

Plus data/model work, which is a separate track and separate people: collecting and labeling a vocal corpus, training denoise/dereverb, building the target LTAS curves — **10–16 person-weeks**, largely parallelizable, and it *gates* the assistant's quality more than any code does.

## 6.2 The trimmed v1 I would actually ship

Cut pitch correction, reverb, delay, and doubler from v1 (ship them in 1.1/1.2). Keep: repair (gate/denoise/dereverb/deplosive/debreath), EQ (static + dynamic), de-esser, leveler + comp, saturation, limiter, and the full assistant. That is *already* a strong, differentiated product — and "assistant that actually measures your voice and explains itself" is a better wedge against Nectar than a longer feature list.

`103 − 10 − 5 − 2 − 2 = 84`, minus ~4 weeks of UI scope ⇒ **~80 + 25% ≈ 100 person-weeks** ⇒ **~9 months with 4 people**, or **~7 months with 5**.

## 6.3 The honest strategic note

iZotope Nectar 4 represents roughly 15 years of accumulated DSP, a mature ML pipeline, a large licensed training corpus, and a deep catalogue of tuned presets. We will not out-feature it in one release. What we *can* do in one release is be **better at one thing**: an assistant that is transparent, bounded, explains every move in plain language, and never does something stupid on a bad recording — because Nectar's Assistant is a black box and that is its most-criticized aspect. Architecture-wise, that means the `explain.py` / rationale path and the `assistMin/assistMax` cages are **product features, not debug tooling**, and they should be treated as first-class from day one.

Any estimate below ~80 person-weeks for a shippable, DAW-compatible, AAA-quality vocal processor is fiction. Anyone quoting 6 person-weeks for "the DSP" has not shipped a limiter that survives Pro Tools.
