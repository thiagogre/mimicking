import unittest
import numpy as np
import librosa

from adapters import TranscriptionAdapter


class TestTranscriptionAdapter(unittest.TestCase):
    def setUp(self):
        self.transcription_adapter = TranscriptionAdapter()
        self.filename = "tests/integration/adapters/audios/test.wav"

    def test_execute_valid_transcription(self):
        audio, sampling_rate = librosa.load(self.filename, sr=None)
        self.assertTrue(isinstance(audio, np.ndarray))

        transcription = self.transcription_adapter.execute(audio, sampling_rate)
        self.assertIsInstance(transcription, str)
        self.assertTrue("test" in transcription.lower())

    def test_execute_invalid_transcription(self):
        with self.assertRaises(RuntimeError) as context:
            self.transcription_adapter.execute("", "")
        self.assertIn("Failed to transcribe text", str(context.exception))


if __name__ == "__main__":
    unittest.main()
