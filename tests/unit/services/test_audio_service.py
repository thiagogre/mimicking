import unittest
import numpy as np

from application.services import AudioService
from tests.unit.stubs import AudioStub


class TestAudioService(unittest.TestCase):
    def setUp(self):
        self.audio_port = AudioStub(sampling_rate=44100)
        self.audio_service = AudioService(audio_port=self.audio_port)

    def test_record_student_pronunciation(self):
        native_filename = "test_native_pronunciation.wav"
        student_filename = "test_student_pronunciation.wav"

        self.audio_port.saved_files[native_filename] = np.zeros(
            (self.audio_port.sampling_rate * 5,), dtype=np.float32
        )

        self.audio_service.record_student_pronunciation(
            native_filename, student_filename
        )

        self.assertIn(student_filename, self.audio_port.saved_files)

        native_audio = self.audio_port.saved_files[native_filename]
        student_audio = self.audio_port.saved_files[student_filename]
        self.assertEqual(
            len(student_audio),
            len(native_audio),
            "Recorded audio duration does not match native audio",
        )

    def test_load_and_play(self):
        filename = "test_audio.wav"

        self.audio_port.saved_files[filename] = np.zeros(
            (self.audio_port.sampling_rate * 3,), dtype=np.float32
        )

        self.audio_service.load_and_play(filename)

        audio_loaded = self.audio_port.saved_files[filename]
        self.assertIsNotNone(audio_loaded)
        self.assertEqual(
            len(audio_loaded),
            self.audio_port.sampling_rate * 3,
            "Loaded audio does not match expected duration",
        )


if __name__ == "__main__":
    unittest.main()
