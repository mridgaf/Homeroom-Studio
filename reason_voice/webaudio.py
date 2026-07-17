"""Mic capture for the web UI.

The microphone stays in the Python process (Terminal already has the
permission) — the browser only sends start/stop over the WebSocket.
Returns 16 kHz mono float32, same contract as the old PushToTalk.
"""
import threading

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000


class WebRecorder:
    def __init__(self, max_seconds: float = 15.0):
        self.max_frames = int(SAMPLE_RATE * max_seconds)
        self._recording = threading.Event()
        self._frames = []
        self._stream = None

    def _callback(self, indata, frames, time_info, status):
        if self._recording.is_set():
            self._frames.append(indata.copy())
            if sum(len(f) for f in self._frames) >= self.max_frames:
                self._recording.clear()

    def start(self):
        """Begin capturing. Opens the input stream lazily on first use so the
        mic-in-use indicator only appears once he actually talks."""
        if self._stream is None:
            self._stream = sd.InputStream(
                samplerate=SAMPLE_RATE, channels=1, dtype="float32",
                callback=self._callback,
            )
            self._stream.start()
        self._frames = []
        self._recording.set()

    def stop(self) -> np.ndarray:
        self._recording.clear()
        if not self._frames:
            return np.zeros(0, dtype=np.float32)
        return np.concatenate(self._frames).flatten()
