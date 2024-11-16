import unittest
import numpy as np

from tests.unit.stubs import (
    AudioStub,
    TranscriptionStub,
    PhonemeStub,
    WerStub,
)
from application.services import TranscriptionService


class TestTranscriptionService(unittest.TestCase):
    def setUp(self):
        self.sampling_rate = 16000
        self.transcription_port = TranscriptionStub()
        self.audio_port = AudioStub(self.sampling_rate)
        self.phoneme_port = PhonemeStub()
        self.wer_port = WerStub()
        self.transcription_service = TranscriptionService(
            self.audio_port, self.transcription_port, self.phoneme_port, self.wer_port
        )

    def test_text_to_phonemes(self):
        phonemes = self.transcription_service._text_to_phonemes("test")
        self.assertEqual(phonemes, ["t"])

    def test_calculate_levenshtein(self):
        phonemesX = ["t"]
        phonemesY = phonemesX
        similarity = self.transcription_service._calculate_levenshtein(
            phonemesListX=phonemesX, phonemesListY=phonemesY
        )
        self.assertEqual(similarity, 0.0)

    def test_transcribe(self):
        audio = np.zeros((self.sampling_rate * 5,), dtype=np.float32)
        transcription = self.transcription_service.transcribe(audio)
        self.assertEqual(transcription, "transcription")

    def test_calculate_phoneme_similarity(self):
        similarity = self.transcription_service.calculate_phoneme_similarity(
            "text", "text"
        )
        self.assertEqual(similarity, 100)
