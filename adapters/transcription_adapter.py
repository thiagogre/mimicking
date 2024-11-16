import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from application.ports import AbstractTranscriptionPort
from shared.types import *


class TranscriptionAdapter(AbstractTranscriptionPort):
    def __init__(self):
        self.processor = Wav2Vec2Processor.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    def execute(self, audio: Audio, sampling_rate: SamplingRate) -> str:
        try:
            input_values = self.processor(
                audio, sampling_rate=sampling_rate, return_tensors="pt"
            ).input_values
            logits = self.model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
            return transcription
        except Exception as e:
            raise RuntimeError(f"Failed to transcribe text: {e}")
