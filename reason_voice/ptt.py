"""Push-to-talk audio capture.

Hold the configured hotkey, speak, release. Returns 16 kHz mono float32 audio.
Requires macOS Input Monitoring permission for the terminal running this app.
"""
import queue
import threading

import numpy as np
import sounddevice as sd
from pynput import keyboard

SAMPLE_RATE = 16000

KEY_ALIASES = {
    "right_option": keyboard.Key.alt_r,
    "left_option": keyboard.Key.alt_l,
    "right_cmd": keyboard.Key.cmd_r,
    "f13": keyboard.Key.f13,
    "f14": keyboard.Key.f14,
    "f15": keyboard.Key.f15,
    "caps_lock": keyboard.Key.caps_lock,
}


class PushToTalk:
    """Blocks in wait_for_speech() until a full press-record-release cycle."""

    def __init__(self, hotkey: str = "right_option", max_seconds: float = 15.0):
        self.key = KEY_ALIASES.get(hotkey)
        if self.key is None:
            raise ValueError(
                f"Unknown hotkey '{hotkey}'. Options: {', '.join(KEY_ALIASES)}"
            )
        self.max_seconds = max_seconds
        self._recording = threading.Event()
        self._done = queue.Queue()
        self._frames = []
        self._listener = keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release
        )
        self._listener.daemon = True
        self._listener.start()

    def _on_press(self, key):
        if key == self.key and not self._recording.is_set():
            self._frames = []
            self._recording.set()

    def _on_release(self, key):
        if key == self.key and self._recording.is_set():
            self._recording.clear()
            self._done.put(True)

    def _callback(self, indata, frames, time_info, status):
        if self._recording.is_set():
            self._frames.append(indata.copy())

    def wait_for_speech(self) -> np.ndarray:
        """Block until the user finishes a push-to-talk utterance."""
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            callback=self._callback,
        ):
            # Wait for press
            while not self._recording.is_set():
                sd.sleep(30)
            # Wait for release (or timeout)
            try:
                self._done.get(timeout=self.max_seconds)
            except queue.Empty:
                self._recording.clear()
        if not self._frames:
            return np.zeros(0, dtype=np.float32)
        return np.concatenate(self._frames).flatten()
