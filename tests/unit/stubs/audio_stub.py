from typing import *
import numpy as np

from shared.types import *
from application.ports import AbstractAudioPort


class AudioStub(AbstractAudioPort):
    def __init__(self, sampling_rate: SamplingRate):
        super().__init__(sampling_rate)
        self.saved_files = {}

    def load(self, filename: str) -> Tuple[Audio, SamplingRate]:
        audio = np.zeros((self.sampling_rate * 5,), dtype=np.float32)
        return audio, self.sampling_rate

    def beep(self, frequency: int, duration_in_seconds: float) -> None:
        print(f"Beep with frequency {frequency}Hz for {duration_in_seconds}s")

    def record(self, duration_in_seconds: float) -> Audio:
        num_samples = int(self.sampling_rate * duration_in_seconds)
        return np.zeros((num_samples,), dtype=np.float32)

    def save(self, filename: str, audio: Audio) -> None:
        self.saved_files[filename] = audio
        print(f"Audio saved to {filename}")

    def play(self, audio: Audio) -> None:
        print("Playing audio (mocked)")

    def get_duration_in_seconds(self, audio: Audio) -> float:
        return len(audio) / self.sampling_rate
