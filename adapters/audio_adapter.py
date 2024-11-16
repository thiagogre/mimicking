import librosa
import librosa.display
import numpy as np
import sounddevice as sd
import soundfile as sf

from application.ports import AbstractAudioPort
from shared.types import *


class AudioAdapter(AbstractAudioPort):
    def __init__(self, sampling_rate: SamplingRate):
        super().__init__(sampling_rate)

    def load(self, filename: str) -> Tuple[Audio, SamplingRate]:
        try:
            audio, sr = librosa.load(filename, sr=self.sampling_rate)
            return audio, sr
        except Exception as e:
            raise RuntimeError(f"Failed to load audio from {filename}: {e}")

    def play(self, audio: Audio) -> None:
        try:
            sd.play(audio, self.sampling_rate)
            sd.wait()
        except Exception as e:
            raise RuntimeError(f"Failed to play audio: {e}")

    def beep(self, frequency: int, duration_in_seconds: float) -> None:
        try:
            t = np.linspace(
                0,
                duration_in_seconds,
                int(self.sampling_rate * duration_in_seconds),
                endpoint=False,
            )
            beep_sound = 0.5 * np.sin(2 * np.pi * frequency * t)
            self.play(beep_sound)
        except Exception as e:
            raise RuntimeError(f"Failed to generate or play beep: {e}")

    def save(self, filename: str, audio: Audio) -> None:
        try:
            sf.write(
                filename, audio, self.sampling_rate, format="WAV", subtype="PCM_16"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to save audio to {filename}: {e}")

    def record(self, duration_in_seconds: float) -> Audio:
        if duration_in_seconds <= 0:
            raise ValueError("Duration must be greater than 0")

        total_samples = int(self.sampling_rate * duration_in_seconds)
        frames = []

        stream = sd.InputStream(
            samplerate=self.sampling_rate, channels=1, dtype="float32"
        )
        try:
            with stream:
                while len(frames) * 1024 < total_samples:
                    frame, _ = stream.read(1024)
                    if frame.size > 0:
                        frames.append(frame.copy())
        except Exception as e:
            raise RuntimeError(f"Failed to record audio: {e}")

        if not frames:
            raise RuntimeError("No audio frames were captured during recording")

        audio = np.concatenate(frames)[:total_samples]  # Trim to exact length
        return audio

    def get_duration_in_seconds(self, audio: Audio) -> float:
        return librosa.get_duration(y=audio, sr=self.sampling_rate)
