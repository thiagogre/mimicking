from abc import ABC, abstractmethod

from shared.types import *


class AbstractAudioPort(ABC):
    def __init__(self, sampling_rate: SamplingRate):
        self.sampling_rate = sampling_rate

    @abstractmethod
    def load(self, filename: str) -> Tuple[Audio, SamplingRate]:
        pass

    @abstractmethod
    def beep(self, frequency: int, duration_in_seconds: float) -> None:
        pass

    @abstractmethod
    def record(self, duration_in_seconds: float) -> Audio:
        pass

    @abstractmethod
    def save(self, filename: str, audio: Audio) -> None:
        pass

    @abstractmethod
    def play(self, audio: Audio) -> None:
        pass

    @abstractmethod
    def get_duration_in_seconds(self, audio: Audio) -> float:
        pass
