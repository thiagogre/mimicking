from TTS.api import TTS
import torch

from application.ports import AbstractSpeechSynthesisPort

"""
    models:
    tts_models/en/ljspeech/vits--neon
    tts_models/en/jenny/jenny
    tts_models/en/vctk/vits <- 256 M, 257 F, 270 F, 287 M, 293 F, 317 M, 360 F 
    
"""


class SpeechSynthesisAdapter(AbstractSpeechSynthesisPort):
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(
            model_name="tts_models/en/jenny/jenny",
            progress_bar=True,
        ).to(device=self.device)

    def execute(self, text: str, output_filename: str) -> None:
        try:
            self.tts.tts_to_file(text=text, file_path=output_filename)
        except Exception as e:
            raise RuntimeError(f"Failed to covert text to speech: {e}")
