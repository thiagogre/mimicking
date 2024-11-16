from abc import ABC, abstractmethod


class AbstractSpeechSynthesisPort(ABC):
    @abstractmethod
    def execute(self, text: str, output_filename: str) -> None:
        pass
