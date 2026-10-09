"""Hermes's helper: send ONE knob move to the Scream 4 knobs.

    ./.venv/bin/python reason_voice/hermes_knob_test/send_move.py knob_9 0

knob_1 to knob_16 come from the Scream 4 block of remote/ReasonVoice.remotemap
(Knob 1 = Damage Control ... Knob 16 = Enabled). Value is 0 to 127.
"""
import asyncio
import json
import sys

import websockets

URL = "ws://localhost:8765/ws"


async def send(knob, value):
    async with websockets.connect(URL) as ws:
        await ws.send(json.dumps({"type": "command", "command": "dial_set",
                                  "args": {"knob": knob, "value": value}}))
    await asyncio.sleep(0.3)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    knob = sys.argv[1]
    if not (knob.startswith("knob_") and knob[5:].isdigit() and 1 <= int(knob[5:]) <= 16):
        sys.exit("knob must be knob_1 to knob_16")
    try:
        value = int(sys.argv[2])
    except ValueError:
        sys.exit("value must be a whole number from 0 to 127")
    if not 0 <= value <= 127:
        sys.exit("value must be 0 to 127")
    asyncio.run(send(knob, value))
    print("sent %s = %d" % (knob, value))
