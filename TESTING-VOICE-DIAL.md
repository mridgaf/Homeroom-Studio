# Reason Voice dial — test checklist

Do these in order. Each block is one paste-able command or one physical action.
Anywhere it says **write down**, paste it back to me before we trust it.

This file is the whole job in one place — you can pick it up cold, in any
session, without me remembering anything.

## What's waiting to be tested

| Device | Controls | Sweep | Step |
|---|---|---|---|
| RV7000 Advanced Reverb | 16 | ~2 min | 3 |
| Kong Drum Designer | 48 — 16 pads x 3 | ~6 min | 4 |
| Redrum Drum Computer | 40 — 10 channels x 4 | ~5 min | 5 |
| Dr. Octo Rex Loop Player | 41 | ~5 min | 6 |
| Scream 4 / MClass Compressor | already working | — | 7 |

All four sweeps put every knob back where they found it. Total sitting-there
time is about 25 minutes, and you can stop after any one of them — each device
is independent.

**Nothing is committed.** All of this is sitting in your working tree; you
write the commits.

---

## Step 1 — Tests on the computer only (no Reason, ~7 min)

Nothing is plugged in yet. This just checks the code didn't break.

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python reason_voice/dial_llm.py
```

Expect: it prints OK and exits. Takes a second.

Then the full suite. **Run it alone** — no beats rendering at the same time.

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python -m pytest tests/ -q
```

Expect: `1115 passed, 2 failed, 3 skipped`, about 7 minutes. The 2
failures are in `test_beat_machine.py` and are old — not from this work.
I ran this on 2026-09-11 and got exactly that.

---

## Step 2 — Install the bridge (one time, covers all four new devices)

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./install.sh
```

Then **quit Reason completely (Cmd+Q)** and open it again. Not just close the
window — quit. Reason only reads the new files at startup.

---

## Step 3 — RV7000 reverb: lock and measure

1. Put an **RV7000 Advanced Reverb** in the rack.
2. Ctrl-click its front panel → **Lock to ReasonVoice**.
3. Run:

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python reason_voice/calibrate.py --device "RV7000 Advanced Reverb"
```

**Write down** what it prints. Three things I need to see:

- Did any knob come back as a **toggle** instead of a normal dial?
- Does the Edit Mode knob show **words** (Reverb / EQ / Gate) or bare numbers?
- Do the reverb type names match what your panel actually shows?

---

## Step 4 — Kong: lock and measure

Kong now covers **all 16 pads**, three controls each: **Level, Pitch Offset,
Decay Offset**. The drum-module and per-pad effect knobs are gone — see the
note at the bottom for why.

1. Put a **Kong Drum Designer** in the rack with a kit loaded.
2. Ctrl-click its panel → **Lock to ReasonVoice**.
3. Run:

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python reason_voice/calibrate.py --device "Kong Drum Designer"
```

**This one takes about 6 minutes** — 48 knobs instead of 16. It puts every knob
back where it found it. Let it finish.

**Write down** what it prints. Two things I need to see:

- Does Pitch Offset show **semitones** or a bare number?
- Does Decay Offset show a **time** or a percentage?

---

## Step 5 — Redrum: lock and measure

Redrum covers **all 10 channels**, four controls each: **Level, Pitch, Length,
Pan**. Length is Redrum's decay knob.

1. Put a **Redrum Drum Computer** in the rack with a kit loaded.
2. Ctrl-click its panel → **Lock to ReasonVoice**.
3. Run:

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python reason_voice/calibrate.py --device "Redrum Drum Computer"
```

**About 5 minutes** — 40 knobs. It puts every knob back where it found it.

**Write down** what it prints. Three things I need to see:

- Does **Pitch** show semitones or a bare number?
- Does **Length** show a time, a percentage, or a bare number?
- Flip one channel's **Decay/Gate** switch and run it again on that channel if
  you can be bothered — I need to know whether Length *reads* differently in
  Gate mode. It definitely *sounds* different. If it reads the same, nothing
  needs doing.

---

## Step 6 — Dr. Octo Rex: lock and measure

Rex covers **41 controls** — all eight loop slots, the run/loop-mode buttons,
and the whole synth section (pitch, amp envelope, filter, filter envelope,
LFO). Nothing slice-level: Reason does not let a control surface touch it.

1. Put a **Dr. Octo Rex Loop Player** in the rack and **load a loop into at
   least two slots** — otherwise the slot buttons have nothing to switch to
   and the sweep tells you nothing.
2. Ctrl-click its panel → **Lock to ReasonVoice**.
3. Run:

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python reason_voice/calibrate.py --device "Dr.REX Loop Player"
```

That device name looks wrong and isn't — Reason still calls Octo Rex
`Dr.REX Loop Player` when it talks to a control surface.

**About 5 minutes.** Twelve of these are buttons, and the script probes each
one before sweeping so it never writes 128 values to a switch.

**Write down** what it prints. Four things I need to see:

- Does **Trigger Next Setting** print words (Bar / Beat / 1/16) or numbers?
- Does **Transpose** and **Loop Transpose** show semitones or bare numbers?
- Does **Filter Mode** print the filter names (Notch, HP, BP, LP12, LP24)?
- Did the eight **Select Loop** buttons probe as switches or as values? The
  script says which.

---

## Step 7 — Start the app and talk to it

Double-click **`ReasonVoice.command`**. It opens in your browser.

If a change seems to do nothing: the old copy is still running. Quit it and
double-click again.

Now lock one device at a time and say these.

### RV7000 (lock the reverb)

| Say | Should happen |
|---|---|
| "make the tail longer" | Decay goes up |
| "damp the highs" | HF Damp moves |
| "more wet" | Dry/Wet goes toward wet |
| "turn the gate on" | GATE button lights |
| "give me a plate" | Flips to Reverb page first, then picks Plate |
| "make it a spring reverb" | Same, lands on Spring |
| "set the decay to 4 seconds" | A real time value lands |

### Kong (lock the drum machine)

**Say the pad NUMBER.** Reason never tells the app which pad holds the snare,
so it will not guess — it refuses instead of moving the wrong drum.

| Say | Should happen |
|---|---|
| "turn up pad 5" | Pad 5 Level up |
| "turn up pad five" | Same — the word works too |
| "tune drum 9 down" | Pad 9 Pitch Offset down |
| "make pad 12 ring longer" | Pad 12 Decay Offset up |
| "give pad 3 a longer tail" | Pad 3 Decay Offset up |
| "quieter on pad 8" | Pad 8 Level down |
| "turn up pad sixteen" | Pad 16 Level up |
| "make the snare louder" | **Refuses and moves nothing.** That is the right answer, not a bug — it does not know which pad the snare is on |

Check a **high pad number** (14, 15, 16) especially. Those run on knob slots
that did not exist before today.

### Redrum (lock the drum machine)

**Say the channel NUMBER.** Redrum will not tell the app which sample is on
which channel, so "the snare" is a guess and it refuses to guess.

| Say this | Should happen |
|---|---|
| "turn up drum 3" | Channel 3 Level up |
| "turn up channel three" | Same — the word works too |
| "tune drum 7 down" | Channel 7 Pitch down |
| "make drum 4 ring longer" | Channel 4 Length up |
| "push drum 2 to the left" | Channel 2 Pan left |
| "quieter on drum 10" | Channel 10 Level down |
| "make the snare louder" | **Refuses and moves nothing.** Right answer, not a bug |

**One thing to watch.** Kong and Redrum both call loudness "Drum 3 Level". If
the app has only ever seen a Level move it cannot tell which of the two is
locked, and it will say so instead of moving anything. Touch a Pitch, Length
or Pan once and it knows for the rest of the session. Tell me if this bites
you in normal use and I will fix it properly.

### Dr. Octo Rex (lock the loop player)

**Say the slot NUMBER.** Rex will not tell the app which loop is in which
slot, so "the drum loop" is a guess and it refuses to guess.

| Say this | Should happen |
|---|---|
| "go to loop 3" | Switches to slot 3 |
| "switch to loop three" | Same — the word works too |
| "change the loop" | **Refuses and moves nothing.** Right answer, not a bug |
| "gate the loop" / "make it stutter" | Amp Env Decay down, Sustain low |
| "make it swell in" | Amp Env Attack up |
| "give it that scratch sound" | Osc Env Amount up — the vinyl-pitch knob |
| "make it swoop on every hit" | Filter Env Amount up |
| "pitch the loop down" | Transpose down |
| "stop the loop" | Run off |

**Two things to watch.**

**Loop Transpose and Loop Level move whichever slot is selected in the
editor**, not necessarily the one playing. If one of them seems to do nothing,
that's why.

**The best-known Octo Rex tricks are mouse-only** — alt-group randomising,
sending just the snare slices to a reverb, drawing modulation in Slice Edit
Mode. Reason does not expose anything slice-level to a control surface at all,
so the app can't reach them and won't pretend it can.

### Old devices — quick check nothing broke

Lock a **Scream 4** and say "turn the body off". Lock an **MClass Compressor**
and say "set the attack to 30 milliseconds". Both were working before; this is
just making sure the new devices didn't disturb them.

---

## Two things I got wrong, stated plainly

**1. I said you could say "make the snare louder". You can't.** When I offered
you the 16-pad option I described it that way, and it isn't true — you have to
say the pad number. Reason never reports what is loaded on a pad, so naming
drums would mean the app guessing, and guessing moves a drum you didn't mean.
I made it refuse instead.

If you want names to work, I need one thing from you: which pad holds what in
the kit you actually use. Tell me and I'll wire it — but only for a kit layout
you confirm, never a guessed one.

**2. Kong lost depth to gain reach.** There are 48 knob slots and 16 pads, and
that 48 is near a hard ceiling (59, set by how many MIDI CC numbers exist).
Three controls per pad was the most that fits. Tone, Pan, Bus FX Send and the
drum-module/effect knobs are no longer reachable by voice on any pad.

## Known rough edge

A vague phrase like "turn it up" tends to go to the **top** of the range rather
than nudging. Undo fixes it. Tell me if it grates and I'll retune it.

Ambiguous phrases can pick the wrong one of the three. "Shorten pad 1" landed
on Level instead of Decay in testing (9 of 10 phrases were right). Saying
"make pad 1 shorter" or "less decay on pad 1" is more reliable.
