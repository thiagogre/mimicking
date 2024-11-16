from abc import ABC, abstractmethod

from shared.types import *


class AbstractTranscriptionPort(ABC):
    @abstractmethod
    def execute(self, audio: Audio, sampling_rate: SamplingRate) -> str:
        pass
