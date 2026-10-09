# Message for Hermes: Scream 4 knob test

Paste the block below into the Hermes chat (homeroom-studio profile), once.
Then send the cases one at a time, in order, as John says each one.

---

You control knobs on the Scream 4 Distortion device in Reason 12. Reason Voice
(running on this Mac) relays the moves. Rules:

1. Work out the knob yourself. Look up the device's knob names in
   ~/Desktop/Homeroom Studio/remote/ReasonVoice.remotemap (the block that starts
   with "Scope ... Scream 4 Distortion"). Knob N = the name on its "Knob N" line.
   Do not guess. If the name is not there, say NO SUCH CONTROL.
2. Pick the value yourself, 0 to 127. Off = 0, on = 127, half = 64.
3. Send each move with this one command in the terminal:
   cd "$HOME/Desktop/Homeroom Studio" && ./.venv/bin/python reason_voice/hermes_knob_test/send_move.py knob_N VALUE
   Replace knob_N and VALUE. Send only one move per case.
4. Do NOT use any other route (no "dial", "text", or phrase commands). Those let
   Reason Voice guess for you, which is what this test is checking.
5. If the thing cannot be done with a knob (for example, drawing a cable), reply
   with exactly: NOT POSSIBLE, then one short reason. Do not send any move.
6. After each case, reply with the knob name and the value you sent, in one line.
   Nothing else.

---

## The cases (John sends these one at a time, in this order)

1. Turn the body off.
2. Turn the body back on.
3. Set the master level to half.
4. Turn the high cut all the way down.
5. Turn the master level down 20 percent.
6. Turn the body scale up a lot.
7. Turn the damage on.
8. Make a cable from the body to the output.
9. Turn the flux capacitor up.
