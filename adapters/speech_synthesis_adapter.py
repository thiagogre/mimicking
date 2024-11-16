from TTS.api import TTS

from application.ports import AbstractSpeechSynthesisPort


class SpeechSynthesisAdapter(AbstractSpeechSynthesisPort):
    def __init__(self):
        self.tts = TTS(
            model_name="tts_models/en/ljspeech/tacotron2-DDC",
            progress_bar=True,
            gpu=False,
        )

    def execute(self, text: str, output_filename: str) -> None:
        try:
            self.tts.tts_to_file(text=text, file_path=output_filename)
        except Exception as e:
            raise RuntimeError(f"Failed to covert text to speech: {e}")
