from abc import ABC, abstractmethod
from typing import *


class AbstractPhonemePort(ABC):
    @property
    @abstractmethod
    def phonemes(self) -> Dict:
        pass
