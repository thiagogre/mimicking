from application.ports import AbstractTranscriptionPort
from shared.types import *


class TranscriptionStub(AbstractTranscriptionPort):
    def __init__(self):
        pass

    def execute(self, audio: Audio, sampling_rate: SamplingRate) -> str:
        return "Transcription"
