import numpy as np

from application.ports import AbstractSpeechSynthesisPort


class SpeechSynthesisStub(AbstractSpeechSynthesisPort):
    def __init__(self):
        self.saved_files = {}
        self.sampling_rate = 16000

    def execute(self, text: str, output_filename: str) -> None:
        self.saved_files[output_filename] = np.zeros(
            (self.sampling_rate * 5,), dtype=np.float32
        )
