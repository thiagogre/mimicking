from abc import ABC, abstractmethod


class AbstractWerPort(ABC):
    @abstractmethod
    def calculate_wer(self, phonemesX: str, phonemesY: str) -> float:
        pass
