import unittest

from application.services import SpeechSynthesisService
from tests.unit.stubs import SpeechSynthesisStub, AudioStub


class TestSpeechSynthesisService(unittest.TestCase):
    def setUp(self):
        self.speech_synthesis_port = SpeechSynthesisStub()
        self.audio_port = AudioStub(sampling_rate=16000)
        self.speech_service = SpeechSynthesisService(
            self.speech_synthesis_port, self.audio_port
        )

    def test_execute(self):
        self.speech_service.execute("Test phrase", "test.wav")
        self.assertIn("test.wav", self.audio_port.saved_files)
