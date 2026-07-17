"""Local speech-to-text via faster-whisper. Nothing leaves your machine."""
import numpy as np


class Transcriber:
    def __init__(self, model_size: str = "small.en", device: str = "auto",
                 vocabulary: str = ""):
        from faster_whisper import WhisperModel  # deferred: slow import

        self.model = WhisperModel(model_size, device=device, compute_type="int8")
        # Biasing the decoder toward our command words and library names
        # ("Klang", "walkthrough", recipe titles) cuts mishearings at the
        # source instead of patching them afterward.
        self.initial_prompt = vocabulary[:800] or None

    def transcribe(self, audio: np.ndarray) -> str:
        if audio.size < 1600:  # <0.1 s: ignore accidental taps
            return ""
        segments, _info = self.model.transcribe(
            audio,
            language="en",
            beam_size=3,
            vad_filter=True,
            condition_on_previous_text=False,
            initial_prompt=self.initial_prompt,
        )
        text = " ".join(seg.text.strip() for seg in segments).strip()
        return text.lower()
