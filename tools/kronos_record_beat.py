"""Play the Kronos 8-bar beat one lane at a time, record each from Kronos USB audio,
then add saturation to the kick and reverb to the snare and mix. Writes to
~/Desktop/Homeroom Auditions/. Usage: python tools/kronos_record_beat.py [drive_pct] [reverb_pct]
Percent = share of full scale: drive 100% = 30 dB, reverb 100% = fully wet.
"""
import datetime
import os
import sys
import time

import numpy as np
import sounddevice as sd
import soundfile as sf
from pedalboard import Distortion, Pedalboard, Reverb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kronos  # noqa: E402

SR, BPM, BARS = 48000, 90, 8
LANES = {"kick": ("kick", "kick2"), "snare": ("snare",), "rest": ("clap", "hat", "open")}


def take(lanes):
    secs = BARS * 4 * 60.0 / BPM + 2.5
    rec = sd.rec(int(secs * SR), samplerate=SR, channels=2, device="KRONOS _ USB _ L&R", dtype="float32")
    time.sleep(0.4)  # let the stream settle; beat() then waits 0.5 s itself
    kronos.beat(bpm=BPM, bars=BARS, kit=kronos.GM_KIT, lanes=lanes, lead=0.5)
    sd.wait()
    return rec


if __name__ == "__main__":
    drive = float(sys.argv[1]) / 100 if len(sys.argv) > 1 else 0.20
    wet = float(sys.argv[2]) / 100 if len(sys.argv) > 2 else 0.10
    kronos.play_gm_drums(16)
    time.sleep(1)
    stems = {k: take(v) for k, v in LANES.items()}
    n = min(len(x) for x in stems.values())
    stems = {k: v[:n] for k, v in stems.items()}
    kick = Pedalboard([Distortion(drive_db=30 * drive)])(stems["kick"].T, SR).T
    snare = Pedalboard([Reverb(room_size=0.5, wet_level=wet, dry_level=1.0)])(stems["snare"].T, SR).T
    dry = sum(stems.values())
    mix = kick + snare + stems["rest"]
    out_dir = os.path.expanduser("~/Desktop/Homeroom Auditions/Kronos Dirty Drums %s" % datetime.date.today())
    os.makedirs(out_dir, exist_ok=True)
    tag = "kick%d_snarereverb%d" % (round(drive * 100), round(wet * 100))
    for name, a in (("dirty_mix_" + tag, mix), ("dry_reference_" + tag, dry)):
        peak = float(np.abs(a).max())
        if peak > 0.89:
            a = a * (0.89 / peak)  # -1 dBFS ceiling
        sf.write(os.path.join(out_dir, name + ".wav"), a, SR, subtype="PCM_24")
        print(name, "peak before limit %.2f" % peak, "stem peaks", {k: round(float(np.abs(v).max()), 2) for k, v in stems.items()})
    print(out_dir)
