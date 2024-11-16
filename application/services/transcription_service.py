from typing import *

from application.ports import (
    AbstractAudioPort,
    AbstractTranscriptionPort,
    AbstractPhonemePort,
    AbstractWerPort,
)


class TranscriptionService:
    def __init__(
        self,
        audio_port: AbstractAudioPort,
        transcription_port: AbstractTranscriptionPort,
        phoneme_port: AbstractPhonemePort,
        wer_port: AbstractWerPort,
    ):
        self.transcription_port = transcription_port
        self.audio_port = audio_port
        self.phoneme_port = phoneme_port
        self.wer_port = wer_port

    def _text_to_phonemes(self, text: str) -> List[str]:
        words = text.split()
        phonemes_found = []
        for word in words:
            if word in self.phoneme_port.phonemes:
                phonemes_found += self.phoneme_port.phonemes[word][0]
        return phonemes_found

    def _calculate_levenshtein(
        self, phonemesListX: List[str], phonemesListY: List[str]
    ) -> float:
        return self.wer_port.calculate_wer(
            " ".join(phonemesListX), " ".join(phonemesListY)
        )

    def transcribe(self, filename: str) -> str:
        audio, sr = self.audio_port.load(filename)
        transcription = self.transcription_port.execute(audio, sr)
        return transcription.lower()

    def calculate_phoneme_similarity(self, native_text, student_text) -> float:
        native_phonemes = self._text_to_phonemes(native_text)
        student_phonemes = self._text_to_phonemes(student_text)

        if not len(student_phonemes) > 0:
            return 100

        if len(native_phonemes) > 0:
            phoneme_similarity = self._calculate_levenshtein(
                native_phonemes, student_phonemes
            )
            return phoneme_similarity * 100

        return 0.0
