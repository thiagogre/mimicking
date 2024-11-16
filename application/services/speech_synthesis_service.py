from application.ports import AbstractSpeechSynthesisPort, AbstractAudioPort


class SpeechSynthesisService:
    def __init__(
        self,
        speech_synthesis_port: AbstractSpeechSynthesisPort,
        audio_port: AbstractAudioPort,
    ):
        self.speech_synthesis_port = speech_synthesis_port
        self.audio_port = audio_port

    def execute(self, text, output_filename) -> None:
        self.speech_synthesis_port.execute(text, output_filename)
        audio, _ = self.audio_port.load(output_filename)
        self.audio_port.save(output_filename, audio)
