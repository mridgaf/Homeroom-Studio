> Copied 2026-10-11 from the claude.ai "Reason 12" project (chat: Hip-hop recipe book development priorities, 2026-05-14).
> STATUS CHANGED: the original said "Tested". Under Homeroom's rule it is THEORETICAL until you test it in a real session.
> Original text below, unchanged except this note.

# Recipe: Kick + 808 Relationship

**Book:** Hip-Hop
**Section:** 3 — Bass / Kick-Bass Relationship
**Filename:** `06-recipe-kick-808-relationship.md`
**Accuracy Rating:** A (90%+) — stock Reason 12 nails this. The technique is platform-agnostic; Reason's CV routing actually makes it cleaner than most DAWs.
**Verification Status:** Theoretical (was "Tested — widely documented technique, verified signal flow in Reason 12")
**Assumed source quality:** Clean kick sample (any decent one-shot, 24-bit, no pre-baked sidechain) and a clean 808 source (sine-based, recorded dry from Subtractor, Europa, or a sample with no built-in processing).

---

## The problem this recipe solves

Kick and 808 occupy the same frequency range (40–80 Hz fundamentals, harmonics overlapping up to ~250 Hz). Played together untreated, they either:
- **Mask each other** (phase cancellation, both feel weaker than they should), or
- **Sum destructively** (pumping, muddy low end, your kick disappears on small speakers)

You're not mixing two elements — you're mixing one low-end event that happens to have two sources. This recipe is how you make them behave as one.

There are three viable approaches. Build all three; pick per song.

---

## Approach 1 — Sidechain Ducking (most common, most flexible)

### Device chain

**On the 808 channel:**

```
[808 source] → [MClass Compressor] → [Mixer channel]
                      ↑
                      CV sidechain input from kick
```

### Routing (this is the Reason-specific part)

1. Flip the rack (Tab)
2. On the kick's Mix Channel, find the **Direct Out** on the back
3. Use a **Spider Audio Merger & Splitter** to split the kick: one copy goes to the mixer as normal, one copy feeds the sidechain
4. Patch the kick split into the **Sidechain Input** of the MClass Compressor on the 808 channel
5. On the MClass Compressor, enable **Sidechain** (the small button on the back panel)

### Exact settings — MClass Compressor on the 808

- **Ratio:** 4:1
- **Threshold:** -18 dB (adjust by ear; you want 4–6 dB of gain reduction on each kick hit)
- **Attack:** 0.1 ms (fastest — you want the duck to happen instantly)
- **Release:** 80–120 ms (longer release = more pumping feel; shorter = tighter)
- **Soft Knee:** ON
- **Sidechain:** ENABLED

### Why this order

The compressor is the only processor in this chain because we're isolating *one job*: duck the 808 when the kick hits. Any EQ or saturation goes *after* this on the 808 channel — you want the dynamic relationship locked before you shape tone.

### One-line why this works

The 808 gets out of the kick's way for the 100 ms when the kick's transient matters, then returns to full level — your ear hears both punches as a single low-end event.

---

## Approach 2 — Frequency Carving (no ducking, both elements at full volume)

Use this when the song needs the 808 to feel constant (trap with sustained 808 lines, where ducking would sound like a tremolo).

### Device chain

**On the kick channel:**
```
[Kick] → [MClass Equalizer] → [Mixer]
```

**On the 808 channel:**
```
[808] → [MClass Equalizer] → [Mixer]
```

### Exact settings

**Decide who owns what frequency range:**

- **Kick owns:** the transient and click (60–120 Hz fundamental, 2–5 kHz click)
- **808 owns:** the sub (30–55 Hz fundamental, sustained body)

**On the kick's MClass EQ:**
- **Lo Shelf:** -6 dB at 50 Hz (Q = 0.7) — cuts the kick's sub so the 808 owns it
- **Lo Mid:** +3 dB at 90 Hz (Q = 1.2) — boost the kick's body
- **Hi Mid:** +2 dB at 3 kHz (Q = 1.5) — emphasize the click

**On the 808's MClass EQ:**
- **Lo Shelf:** +2 dB at 40 Hz (Q = 0.7) — emphasize the sub
- **Lo Mid:** -4 dB at 90 Hz (Q = 1.5) — cut where the kick lives
- **Hi Cut:** roll off above 800 Hz (gentle slope) — 808 doesn't need top end if the kick is providing the click

### Why this order

EQ before anything else because we're surgically dividing the spectrum. Saturation or compression *after* EQ on each channel is fine and often desirable, but the spectral handshake has to happen first or you're just shaping mud.

### One-line why this works

You're not fighting for the same frequencies because you've assigned them — kick gets the punch zone, 808 gets the sub zone, no overlap means no masking.

---

## Approach 3 — Hybrid (the pro move)

Most commercial hip-hop mixes use **both** approaches together. Light sidechain (2–3 dB of duck) plus light frequency carving. This is the recipe to default to once you understand the other two.

### Device chain — on the 808

```
[808] → [MClass Equalizer] → [MClass Compressor w/ sidechain from kick] → [Mixer]
```

### Settings

- **EQ:** same as Approach 2 but less aggressive — Lo Mid cut on 808 at -2 dB instead of -4 dB
- **Compressor:** same as Approach 1 but threshold higher — aim for only 2–3 dB of gain reduction
- **Order matters:** EQ first to remove the overlap, then comp to handle the residual transient conflict

### One-line why this works

Frequency carving handles the steady-state conflict; sidechain handles the transient conflict. You get the best of both without the artifacts of either taken to extremes.

---

## Combinator wrapper (do this once, reuse forever)

Wrap the 808 chain (EQ + sidechain comp) in a **Combinator 2**. Assign macros:

- **Rotary 1:** Sidechain Amount (mapped to compressor Threshold, inverted — turn up = more duck)
- **Rotary 2:** Sub Emphasis (mapped to EQ Lo Shelf gain)
- **Rotary 3:** Kick Pocket (mapped to compressor Release — turn up = longer pocket)
- **Rotary 4:** Mud Cut (mapped to EQ Lo Mid gain, inverted — turn up = more cut at 90 Hz)
- **Button 1:** Sidechain bypass (for A/B-ing the ducking)

Save as `KickPocket_808Bus.cmb`. This is the patch you reach for on every hip-hop song from now on.

---

## What if the source is bad?

**If the 808 has pre-baked sidechain or built-in saturation:** This recipe gets less effective. The fix is to use a cleaner 808 source. Subtractor with a single sine oscillator, slight pitch envelope on the amp envelope's first 30 ms for the click, is a clean starting point. Recipe `07` will cover this when we build it.

**If the kick has a long tail:** Gate it first. Add an **MClass Equalizer with Hi Cut** before the Spider split, or use a separate kick sample with a tighter envelope. A kick with a 200ms tail will sidechain the 808 way too long and you'll hear pumping.

---

## Honest limits

- **No multiband sidechain in stock Reason.** All three approaches duck or carve the *whole* 808 signal. If you want to duck only the 60–120 Hz range of the 808 (leaving its sub intact), you can't do that with stock devices without parallel routing tricks that get unwieldy.
- **Fix:** **Kilohearts Multipass** (Kilohearts, ~$149) does true multiband sidechain compression. If you do a lot of trap or hip-hop, this is the single most valuable RE for kick-808 work. Alternative: **FabFilter Pro-MB** (FabFilter, ~$199) — more expensive, more transparent, same job.
- **No look-ahead on MClass Compressor.** The 0.1 ms attack is the fastest you'll get. For 99% of kicks this is fine. For very sharp transient kicks (think tightly programmed trap kicks with a sub-millisecond attack), you'll hear a tiny bit of the 808 punching through before the duck kicks in.
- **Fix:** **Kilohearts Faturator** (Kilohearts, ~$59) or any RE with look-ahead, OR just trim the kick sample by 1-2 ms so its transient is slightly later than the grid — works fine and is free.

(Prices are from May 2026 and unverified now.)

---

## Technique taught

**Dynamic and spectral resource allocation between competing low-frequency sources.** This same approach works for kick + bass guitar in rock, kick + synth bass in electronic, and floor tom + bass in any genre. The principle: when two sources fight for the same frequency range, you either (1) duck one out of the way in time, (2) divide the spectrum so they don't overlap, or (3) do both gently. Reason's CV sidechain routing via Spider is one of the cleanest implementations of (1) in any DAW.

---

## Test it

Load a kick and an 808 playing the same rhythm. A/B with the Combinator bypassed vs. engaged. The bypassed version should sound muddy, smaller, less defined. The engaged version should feel like one weapon, not two.

If it doesn't, the most common culprits in order:
1. Sidechain isn't actually patched (check the back panel, the CV cable should be visible)
2. 808 source has its own sub-bass enhancer running — disable it
3. Kick's tail is too long — gate or shorten it
4. Threshold too low (over-ducking) or too high (no duck audible)
