import unittest
import os

from adapters import SpeechSynthesisAdapter


class TestSpeechSynthesisAdapter(unittest.TestCase):
    def setUp(self):
        self.speech_synthesis_adapter = SpeechSynthesisAdapter()
        self.test_file = "test_audio.wav"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_execute_valid_tts(self):
        text = "Hello, this is a test."
        self.speech_synthesis_adapter.execute(text, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

    def test_execute_invalid_tts(self):
        with self.assertRaises(RuntimeError) as context:
            self.speech_synthesis_adapter.execute("", "")
        self.assertIn("Failed to covert text to speech", str(context.exception))


if __name__ == "__main__":
    unittest.main()
