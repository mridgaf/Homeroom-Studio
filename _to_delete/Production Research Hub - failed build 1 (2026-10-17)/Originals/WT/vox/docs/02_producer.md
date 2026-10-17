# PRODUCER SPEC — Round 3 (hardened after 31 objections)

**Role:** Executive Producer / Sonic Director. Defines the RESULT and the pass/fail
numbers, not the DSP architecture.

**Round-3 job:** not adding scope — making every number in the document survive
arithmetic, physics, and a prior-art search. The round-2 adversary found six-of-eight
table rows self-contradictory, a de-ess target off by 15–20 dB, a transient-survival
criterion violated by the spec's own compressor, and two "nobody has this" claims that
are false and checkable in thirty seconds. Every blocking objection is applied; where
the adversary was factually wrong, that is stated explicitly rather than silently
overridden (see item 27 below — the only such case).

---

## Adversary objections and how each was resolved

| # | Objection | Resolution |
|---|---|---|
| 1 | §3 Δ vs mix / LUFS-S contradiction — six of eight table rows didn't add up | LUFS-S column deleted from the per-genre table. Vocal-bus loudness renamed **PG-Level** (Phrase-Gated Level), explicitly non-BS.1770-4-compliant. Only **ΔPG** (both sides measured identically) survives in §3 — structurally can't self-contradict since it's not derived by subtracting two independently-rounded columns. |
| 2 | Sibilance target off by 15–20 dB | Customer-facing target redefined as a **broadband loudness ratio** (+2 to +8 dB, default +4), unified across the whole document. The old band-limited 5–10 kHz figure becomes an internal detector calibration constant only, corrected to +12 to +20 dB. |
| 3 | Transient survival (§2 criterion 3) violated by the chain's own compressor/limiter | New **GUARD** module: freezes COMP B's and LIMIT's gain-computer output during tagged plosive windows, null-testable, residual target < 0.3 dB. |
| 4 | Spectral tilt −3 to −4 dB/oct is a mastering number imported onto a solo vocal | Restated −6 to −9 dB/oct measured on the vocal stem; removed as a control objective, kept only as a TARGET diagnostic. |
| 5 | Loudness metrics undefined on an intermittent (majority-silent) stem | PG-Level defined (phrase-gated, VAD-excluded breaths/gaps). LRA dropped from the vocal bus entirely, kept only for the full mix. |
| 6 | CONCORD's central claim had the sign of its own physics backwards; beat rates understated ~2x; prior art (Hermode Tuning, MTS-ESP, etc.) unnamed | Killed as a lead-vocal feature. Survives narrowly as **CONCORD-STACK**: intra-stack only, ET-bed auto-disable, confidence floor raised to 0.85, prior art named explicitly with the real residual claim (audio-domain retuning of already-captured performances vs. competitors' MIDI/synthesis-domain retuning). |
| 7 | POCKET's prior art (Groove Track, Beat Detective, Extract Groove, Revoice APT) not disclosed | Demoted from novel effect to plain convenience feature, off by default. Replaced in the novel-effects slot by **CHOIR** (session-wide identity bus). |
| 8 | ARBITER's SII-weighting claim is standardized broadcast tech (MPEG-H DE, Jünger, Linear Acoustic, Nugen) | Struck as a differentiator; still used internally, not claimed as ours. |
| 9 | ARBITER's ESTOI outer loop is unvalidated on sung material inside a musical bed | Gated behind a corpus-validation study (correlation ≥0.6 required); falls back to SII-static weighting otherwise; max duck hard-capped at 6 dB default. |
| 10 | Rap-lead HPF targets the wrong problem (808 lives at 40–60 Hz) | HPF corrected to 80–90 Hz/12–18 dB·oct. The real conflict (upward masking into 100–300 Hz) handled by ADAPT, dynamic cut 120–250 Hz keyed to the 808 stem via RELAY. |
| 11 | RESONANCE's round-2 "dynamic cuts" reintroduced a second real-time detector into the compressor's sidechain, undoing the module's own ordering argument | RESONANCE made genuinely static (re-analysed every 4–8 s, crossfaded, never threshold-triggered sample-to-sample). All dynamic/threshold-triggered EQ moved to ADAPT (post-comp). |
| 12 | RIDE's 3 dB/50 ms default is 60 dB/s — faster, not slower, than Vocal Rider, inverting the headline claim | Default corrected to ≤1 dB/50 ms; comparison to Vocal Rider restated as "to be measured on the corpus," not asserted. |
| 13 | §3 GR-total column undefined, arithmetic doesn't close | Split into two independent columns (Static/Ride gain, Comp+Limiter GR); neither required to sum to a printed total. |
| 14 | §3 crest column contradicts §2's universal 5–11 dB claim | Universal claim deleted from §2. Crest bounds are genre-dependent only. |
| 15 | Modulation index has no defined normalizer or reference distribution | Normalizer defined explicitly; 0.55/±15% threshold marked PROVISIONAL pending corpus. |
| 16 | ARBITER placed before SATURATE/LIMIT but analyses a pre-harmonics/pre-limiter signal | ARBITER redefined as not-an-insert: detector taps the chain's output AFTER LIMIT; gain applies to the instrumental bus. |
| 17 | DICTION's CVR measured at its own output, before TONE/ADAPT/SATURATE/LIMIT further alter it | CVR now measured only by TARGET, at final chain output. Redefined as fixed per-class-weighted, fixed-band, inventory-normalised. |
| 18 | RESTORE's de-reverb corrupts the DRR feature SEAM measures | Split into RESTORE-LOCAL (before SEAM) and RESTORE-GLOBAL (after SEAM). |
| 19 | §1 says sends are post-limiter; chain array says parallel to steps 13–16; BLOOM needs pre-limiter transient info | Resolved: sends tap POST-ADAPT / PRE-SATURATE, stated once, one signal flow. |
| 20 | SEAM's median-only target silently welds to the worst consistent mic position | Three target modes shipped: Median (default), Best-Segment, User-Nominated; chosen target shown in the segment map. |
| 21 | Fixed Hz constants for male/female fundamentals, wrong for the target market | Removed as constants; HPF corner keyed to measured per-section F0 minimum by default, fixed Hz kept only as a fallback. |
| 22 | Latency ceiling ≤15 ms unachievable given the phoneme classifier's needed right-context | Two committed modes: Tracking (≤10 ms) and Full Mix (≤120 ms). |
| 23 | "Never a gate — audible 100% of the time" is an unfalsifiable absolute | Restated as a measurable constraint: ≤2 dB GR in any 5 ms window during closing, room tone never closed below the measured noise floor. |
| 24 | DE-ESS SPLIT's relative-threshold claim is parity with the whole market | Narrowed to phoneme-class gating only; parity competitors named in the module text. |
| 25 | RESONANCE's "stops the category notching harmonics" claim is false as an absolute | Narrowed to an explicit F0-persistence-across-pitch-change test, must beat soothe2/DSEQ3 blind on the corpus before launch material. |
| 26 | RESTORE claimed as "largest gap on the board" vs. iZotope's own RX | Reframed as strategic necessity (CONDUCTOR-correctness), not a claim to beat RX. |
| 27 | §4 item 6 sidechain criticism vs. RELAY answering the same open question | **Adversary partially right, partially overstated** — evidence kept in the doc: Neutron/Relay already proves the discovery pattern works, so "industry-unsolved" was wrong; but Nectar's own Vocal Unmask specifically still requires a manual sidechain, which the objection itself states and which is not disputed. Softened to describe Vocal Unmask's curve as "largely static," and RELAY answers the open question directly. |
| 28 | §1 step 4's "/s/ slips past a 10–30 ms attack" mechanism attached to the wrong compressor stage | Rewritten to the detector-energy argument, timing mechanism correctly attributed to COMP B's 1–3 ms attack. |
| 29 | Breath depth default (16 dB) too deep for pop/R&B | Genre-linked: 6–10 dB intimate, 12–16 dB pop/rock, 16–20 dB rap; range extended to 4–30 dB. |
| 30 | Tight-double HPF "+20 Hz offset" and ad-lib "LPF if panned >60%" are non-sequiturs | Double HPF restated as a range (150–250 Hz). Ad-lib dulling is now an explicit Depth-send control, independent of pan. |

---

## Modules

### RELAY — Companion Bed-Sender + Session Discovery
Lightweight companion plugin on the instrumental bus (auto-insert by bus name-match)
broadcasting a low-bitrate internal downmix + analysis (4-band LTAS every 500 ms, beat/
downbeat, rolling chord track with confidence) to every vocal-strip instance via
inter-plugin messaging. Discovery via VST3 IProcessContextRequirements/Aux-bus data
where supported; AU/AAX fallback via shared-memory ring buffer keyed by session ID;
degrades to "manual sidechain send" only when neither exists, and says so explicitly.
Every module that needed a manual sidechain (ARBITER, CONCORD-STACK, CHOIR) discovers
it automatically. Params: auto-insert on bus match, broadcast enable, downmix quality,
discovery status readout, manual override, session scope.

### CONDUCTOR (the Assistant)
Full-file analysis (phoneme/syllable/pitch/loudness/section boundaries/source class/
damage) + bed pass via RELAY + target selection + per-section chain synthesis + closed
loop: render, measure against TARGET's metric set, coordinate-descent adjust (~20
params), repeat to convergence or 5 iterations. Drops any unvalidated metric (e.g.
ESTOI) from the loop with a visible notice rather than silently optimizing against it.
Params: Intent, Amount, Section-adaptivity, Character, Instrumental bed source, Relearn,
Report card, Lock individual modules against the loop.

### RESTORE-LOCAL
Isolated-event repair only: declip (cubic/AR interpolation, oversampled), de-plosive
(sub-120 Hz transient >10 dB over vowel LF energy, event duration tagged 5–30 ms for
GUARD), de-click (<30 ms broadband, harmonicity <0.2, AR-model interpolation), de-hum
(auto f0 + harmonics notch). Does not touch global room/DRR character. Runs before SEAM.

### SEAM
Change-point detection (Bayesian online changepoint / CUSUM) on LTAS/DRR/noise-floor/F0
range, taps RESTORE-LOCAL output (pre-de-reverb) so DRR isn't corrupted. Three target
modes: Median (default), Best-Segment (quality heuristic), User-Nominated — chosen
target shown in the segment map. Per-segment minimum-phase matching filter (16–32
bands, ±6 dB clamp), broadband gain, room-decay nudge, noise-floor match. Targets: LTAS
deviation <1.5 dB RMS/1/3-oct, DRR variance <2 dB, both against the chosen target.

### RESTORE-GLOBAL
De-bleed and de-reverb, sequenced AFTER SEAM so global reduction applies to a
spectrally- and level-consistent welded signal. Mask-based STFT separation driven by a
vocal-vs-not classifier plus estimated RIR; late-reverb suppression by per-band
decay-rate estimation with a floor so it never gates.

### GUARD — Transient Preservation Path
Consumes RESTORE-LOCAL's plosive-event tag (onset + 5–30 ms duration) plus a 20 ms
tail. For that window, COMP B's and LIMIT's gain-computer output is FROZEN at the
pre-event level — detector keeps running, gain computer's output is held. 3 ms
equal-power crossfade on the gain-control signal only (null-testable: audio path is
byte-identical with GUARD disabled). Verified target: <0.3 dB residual vs. true
unattenuated over 0–15 ms.

### HPF + RESONANCE (static, pre-comp)
Genuinely static — no per-sample envelope follower, because that would reintroduce a
second detector ahead of the compressor. Per 4–8 s window: smoothed spectral envelope,
peaks >5 dB over neighbourhood, cross-referenced against tracked F0 (bin persists while
F0 moves >3 semitones = resonance; moves with F0 = protected harmonic). Up to 8 static
narrow (Q 4–10) cuts, −3 to −8 dB, re-analysed every 4–8 s with a 150 ms crossfade,
never modulated sample-to-sample. Zero boost path.

### DE-ESS SPLIT
Two phoneme-gated stages either side of the compressor. Sole surviving differentiator:
a hard phoneme-class gate — if the frame isn't {s, ʃ, z, ʒ, tʃ, dʒ, f}, the reducer
cannot fire, full stop. Customer target: broadband loudness ratio, +2 to +8 dB (default
+4). Stage A (pre-comp) reduces only enough to keep the compressor's detector within 3
dB of vowel-frame energy (1–3 dB typical); Stage B (post-comp) does the remainder,
split-band, spectral-tilt-preserving.

### RIDE
Syllable-nucleus level engine so the compressors only do 3–6 dB each. Detect nuclei
(vowel-class local energy maxima, 300 Hz–3 kHz), fit target level per section,
gain = piecewise-linear between nucleus centres, slew capped ≤1 dB/50 ms default
(0.5–3 range), held across inter-syllable gaps so breaths/tails aren't modulated.

### DUAL COMP (A slow / B fast)
Stage A: RMS/opto, 2:1–3:1, attack 10–30 ms, release 100–300 ms, 3–6 dB GR. Stage B:
peak/FET, 4:1–8:1, attack 1–3 ms, release 50–100 ms, 3–6 dB GR, gain computer frozen
during GUARD windows. GR modulation-spectrum display verifies A's energy sits below 2
Hz and B's between 2–10 Hz.

### DICTION (CVR engine)
Fixed per-class-weighted, fixed-band, phoneme-inventory-normalised consonant-to-vowel
ratio solver. Reported/measured number comes only from TARGET at final output — never
from here. Hard interlock with DE-ESS SPLIT (sibilant gain capped by the de-esser's
broadband target, one solver).

### TONE
Post-compressor additive EQ, outside every detector. Minimum-phase shelves/wide bells,
up to 8 bands, ±12 dB, F0-keyed defaults (presence 3–5 kHz, air 10–14 kHz, body
100–200 Hz).

### ADAPT
Sole home of every threshold-triggered dynamic EQ decision in the chain. Multiband
dynamic attenuation, per-band thresholds conditioned on F0 bin and phoneme class.
Local-flatness objective only ("no 1/3-oct band exceeds smoothed neighbours by >5 dB")
— NOT a tilt setpoint. Rap-specific: 120–250 Hz dynamic cut keyed to the 808 stem via
RELAY.

### ARBITER
Not an insert in the vocal path — detector taps the fully processed vocal AFTER LIMIT;
gain applies to the instrumental bus fader via RELAY. Bark-band SII-weighted masking
(used internally, not claimed as novel) plus a conditional ESTOI outer loop, gated
behind a corpus-validation study (correlation ≥0.6), hard-capped max duck (default 6
dB). Gate: ≥40% less total instrumental GR than Three-Body UNMASK / sonible
learn:unmask at matched ESTOI, or the module is killed.

### SATURATE
8x–16x oversampled waveshaper bank, anti-derivative anti-aliasing + polyphase
resampling, auto gain-match within 0.2 dB.

### LIMIT
Lookahead peak limiter (1.5–5 ms), 4x oversampled true-peak detection, two-stage
release. Clipper mode: oversampled soft/hard clip, ADAA. GUARD freeze extends through
this stage.

### TARGET (measurement rig)
Always-on measurement, every metric's validation status shown. PG-Level (phrase-gated,
non-BS.1770-4-compliant, disclosed as such) on the vocal bus; strict BS.1770-4 I/S/M/LRA
on the full mix only. ΔPG vs mix is the only portable loudness number in §3. Modulation
index and ESTOI thresholds marked PROVISIONAL until corpus-validated.

---

## Novel Effects

### RESPIRE — Breath Normalizer
Every breath sits at a consistent, genre-linked distance under the phrase it precedes
(intimate 6–10 dB, pop/rock 12–16 dB, rap 16–20 dB); no breath removed, shortened, or
gated. Look-forward to the RMS of the FOLLOWING phrase, apply one constant gain per
breath (not an envelope) — no pumping, duration/shape survive untouched.

### BLOOM — Phrase-End Bloom Send
Narrowed to exactly the two things that are actually new: the last word of every phrase
gets +3 to +9 dB more reverb send over its final 250–600 ms (Bloom), and send drops on
fast rhythmic passages, rises on sustained notes (Sustain Bias). Everything else
(consonant/sibilant reject, return-side ducking) is documented internally as table
stakes. Taps POST-ADAPT / PRE-SATURATE so transient/phoneme info is intact.

### CONCORD-STACK — Intra-Stack Just Intonation (scope-restricted)
Cancels beating BETWEEN voices of a captured vocal stack by retuning to a shared just-
intonation lattice. Restricted to stack-internal use, auto-disabled when RELAY reports
a sustained ET instrument in the current section. Primary reference is the stack's own
≥3-voice consensus pitch, not an external chord estimator. Confidence floor 0.85.

### CHOIR — Session-Wide Vocal Identity Bus
Discovers every vocal-strip instance via RELAY, computes each track's identity
descriptor (LTAS, dynamic range, sibilance ratio, F0 range) after its own local
processing, and reports/suggests per-track corrective deltas toward a Lead-anchored
session target. Suggest-only by default — never silently auto-applied.

---

## Final signal chain (producer's ordering)

1. RESTORE-LOCAL
2. SEAM (analysis pre-de-reverb)
3. RESTORE-GLOBAL
4. POCKET (optional, off by default)
5. CONCORD-STACK (optional, off by default)
6. HPF + RESONANCE (static, pre-comp)
7. DE-ESS A (pre-comp)
8. RIDE
9. COMP A
10. COMP B (GUARD-protected)
11. DE-ESS B (post-comp)
12. DICTION
13. TONE
14. ADAPT
15. SATURATE
16. LIMIT
17. ARBITER (not an insert — sidechains the instrumental bus)
18. SENDS (BLOOM/RESPIRE, tap post-ADAPT/pre-SATURATE)
19. TARGET (always-on measurement)
20. CHOIR (optional, background, session-wide)

---

## Open questions for human (producer's list)

- Language coverage for the phoneme classifier — training-data languages undecided.
- Real-time vs. offline / ARA — still unresolved, determines DAW compatibility.
- Latency ceilings (Tracking ≤10 ms / Full Mix ≤120 ms) need human sign-off.
- CPU budget per instance, sized against RELAY/CHOIR's always-on background threads.
- Why was iZotope Dialogue Match discontinued? SEAM is funded provisionally pending an answer.
- Measurement rig / test corpus — top funding priority; a long list of numbers are PROVISIONAL pending it.
- ESTOI validation study — blocks ARBITER's outer loop; needs a named owner and go/no-go date.
- CHOIR prior-art verification — has not been exhaustively searched.
- POCKET — ship quietly as a utility, or cut from v1.
- EFFORT (vocal-effort morph) — R&D only, locked room, no public mention.
- Box contents parity — Nectar ships Melodyne Essential; we ship nothing comparable.
- Price and position — re-run against the narrowed module list.
- Gate/expander default-on for aggressive-source presets — workflow decision, not DSP.
