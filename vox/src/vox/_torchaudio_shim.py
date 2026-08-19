"""
Compatibility shim: deepfilternet 0.5.6's df/io.py imports
`torchaudio.backend.common.AudioMetaData`, which was removed from torchaudio
>=2.1's public API. We never call df.io.load_audio/save_audio (we feed numpy
arrays straight from our own I/O), so a minimal stand-in dataclass is enough
to satisfy the import. Import this module before anything imports `df`.
"""
import sys
import types


def install():
    if "torchaudio.backend.common" in sys.modules:
        return
    backend_mod = types.ModuleType("torchaudio.backend")
    common_mod = types.ModuleType("torchaudio.backend.common")

    class AudioMetaData:
        def __init__(self, sample_rate=0, num_frames=0, num_channels=0,
                     bits_per_sample=0, encoding=""):
            self.sample_rate = sample_rate
            self.num_frames = num_frames
            self.num_channels = num_channels
            self.bits_per_sample = bits_per_sample
            self.encoding = encoding

    common_mod.AudioMetaData = AudioMetaData
    backend_mod.common = common_mod
    sys.modules["torchaudio.backend"] = backend_mod
    sys.modules["torchaudio.backend.common"] = common_mod


install()
