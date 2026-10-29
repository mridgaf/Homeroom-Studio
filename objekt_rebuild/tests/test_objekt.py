import json
import math
import wave
from dataclasses import replace
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from objekt.config import ObjektConfig
from objekt.randomizer import randomize_config
from objekt.synth import ObjektSynth
from objekt.wav import write_wav


class ObjektPublicSeamTests(unittest.TestCase):
    """Public seams: config -> renderer -> float audio, and float audio -> WAV."""

    def setUp(self):
        self.sr = 24_000
        self.cfg = ObjektConfig.from_preset("glass_bell")

    def test_render_note_is_deterministic_finite_and_audible(self):
        synth = ObjektSynth(self.sr)
        a = synth.render_note(60, 0.85, 0.5, self.cfg, seed=17)
        b = synth.render_note(60, 0.85, 0.5, self.cfg, seed=17)
        self.assertEqual(a.shape, (12_000, 2))
        self.assertTrue(np.isfinite(a).all())
        self.assertGreater(float(np.max(np.abs(a))), 1e-4)
        np.testing.assert_allclose(a, b, atol=1e-7)

    def test_note_pitch_tracks_upward(self):
        synth = ObjektSynth(self.sr)
        low = synth.render_note(48, 0.8, 0.7, self.cfg, seed=2)[:, 0]
        high = synth.render_note(60, 0.8, 0.7, self.cfg, seed=2)[:, 0]
        window = np.hanning(len(low))
        freqs = np.fft.rfftfreq(len(low), 1 / self.sr)
        low_peak = freqs[int(np.argmax(np.abs(np.fft.rfft(low * window))))]
        high_peak = freqs[int(np.argmax(np.abs(np.fft.rfft(high * window))))]
        self.assertGreater(high_peak, low_peak * 1.65)

    def test_external_audio_can_excitate_the_model(self):
        synth = ObjektSynth(self.sr)
        impulse = np.zeros(6000, dtype=np.float32)
        impulse[0] = 1.0
        cfg = replace(
            self.cfg,
            exciter=replace(self.cfg.exciter, impact_level=0.0, noise_level=0.0, external_level=1.0),
        )
        out = synth.render_note(60, 1.0, 0.25, cfg, seed=3, external_audio=impulse)
        self.assertGreater(float(np.max(np.abs(out))), 1e-4)

    def test_randomizer_is_seeded_and_stays_in_safe_ranges(self):
        a = randomize_config(self.cfg, seed=99, amount=0.7)
        b = randomize_config(self.cfg, seed=99, amount=0.7)
        self.assertEqual(a, b)
        self.assertGreaterEqual(a.modal.decay, 0.03)
        self.assertLessEqual(a.modal.decay, 8.0)
        self.assertEqual(len(a.modal.ratios), 8)
        self.assertEqual(len(a.object1.ratios), 8)
        self.assertLessEqual(a.master_gain, 1.0)

    def test_write_wav_produces_stereo_pcm(self):
        synth = ObjektSynth(self.sr)
        audio = synth.render_note(60, 0.8, 0.15, self.cfg, seed=4)
        target = ROOT / "artifacts" / "test-output.wav"
        write_wav(target, audio, self.sr)
        with wave.open(str(target), "rb") as handle:
            self.assertEqual(handle.getnchannels(), 2)
            self.assertEqual(handle.getframerate(), self.sr)
            self.assertEqual(handle.getsampwidth(), 2)
            self.assertEqual(handle.getnframes(), len(audio))

    def test_factory_presets_are_loadable(self):
        preset_dir = ROOT / "presets"
        names = {p.stem for p in preset_dir.glob("*.json")}
        self.assertTrue({"glass_bell", "wood_mallet", "metal_plate", "imaginary_string"} <= names)
        for path in preset_dir.glob("*.json"):
            cfg = ObjektConfig.from_json(path)
            self.assertEqual(len(cfg.modal.ratios), 8)
            self.assertEqual(len(cfg.object1.ratios), 8)


if __name__ == "__main__":
    unittest.main()
