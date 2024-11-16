from application.ports import AbstractAudioPort


class AudioService:
    def __init__(self, audio_port: AbstractAudioPort):
        self.audio_port = audio_port

    def record_student_pronunciation(
        self,
        native_pronounce_filename: str,
        student_pronounce_filename: str,
    ) -> None:
        native_audio, _ = self.audio_port.load(native_pronounce_filename)
        audio_duration = self.audio_port.get_duration_in_seconds(native_audio)
        self.audio_port.beep(frequency=1000, duration_in_seconds=0.2)
        student_audio = self.audio_port.record(audio_duration)
        self.audio_port.beep(frequency=1000, duration_in_seconds=0.2)
        self.audio_port.save(student_pronounce_filename, student_audio)

    def load_and_play(self, filename: str) -> None:
        audio, _ = self.audio_port.load(filename)
        self.audio_port.play(audio)
