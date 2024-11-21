from TTS.api import TTS

from application.ports import AbstractSpeechSynthesisPort

"""
    models:
    tts_models/en/ljspeech/vits--neon
    tts_models/en/vctk/vits <- 256 M, 257 F, 270 F, 287 M, 293 F, 317 M, 360 F 
    
"""


class SpeechSynthesisAdapter(AbstractSpeechSynthesisPort):
    def __init__(self):
        self.tts = TTS(
            model_name="tts_models/en/vctk/vits",
            progress_bar=True,
            gpu=False,
        )

    def execute(self, text: str, output_filename: str) -> None:
        try:
            self.tts.tts_to_file(text=text, file_path=output_filename, speaker="p317")
        except Exception as e:
            raise RuntimeError(f"Failed to covert text to speech: {e}")
