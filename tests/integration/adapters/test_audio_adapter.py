import unittest
import os
import numpy as np

from adapters import AudioAdapter


class TestAudioAdapter(unittest.TestCase):
    def setUp(self):
        self.sampling_rate = 8000
        self.audio_adapter = AudioAdapter(self.sampling_rate)
        self.test_audio = np.random.uniform(-1.0, 1.0, self.sampling_rate).astype(
            np.float32
        )
        self.test_file = "test_audio.wav"
        self.invalid_file = "non_existent_file.wav"
        self.duration_in_seconds = 0.5

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_valid_file(self):
        self.audio_adapter.save(self.test_file, self.test_audio)
        loaded_audio, sr = self.audio_adapter.load(self.test_file)
        self.assertEqual(sr, self.sampling_rate)
        self.assertEqual(len(loaded_audio), len(self.test_audio))

    def test_load_invalid_file(self):
        with self.assertRaises(RuntimeError) as context:
            self.audio_adapter.load(self.invalid_file)
        self.assertIn("Failed to load audio", str(context.exception))

    def test_play_audio(self):
        try:
            self.audio_adapter.play(self.test_audio)
        except Exception as e:
            self.fail(f"play() raised an unexpected exception: {e}")

    def test_play_invalid_audio(self):
        with self.assertRaises(RuntimeError) as context:
            self.audio_adapter.play("invalid_audio_data")
        self.assertIn("Failed to play audio", str(context.exception))

    def test_beep(self):
        try:
            self.audio_adapter.beep(
                frequency=440, duration_in_seconds=self.duration_in_seconds
            )
        except Exception as e:
            self.fail(f"beep() raised an unexpected exception: {e}")

    def test_beep_invalid_parameters(self):
        with self.assertRaises(RuntimeError) as context:
            self.audio_adapter.beep(frequency=440, duration_in_seconds=-1)
        self.assertIn("Failed to generate or play beep", str(context.exception))

    def test_save_audio(self):
        try:
            self.audio_adapter.save(self.test_file, self.test_audio)
            self.assertTrue(os.path.exists(self.test_file))
        except Exception as e:
            self.fail(f"save() raised an unexpected exception: {e}")

    def test_save_invalid_audio(self):
        with self.assertRaises(RuntimeError) as context:
            self.audio_adapter.save(self.test_file, "invalid_audio_data")
        self.assertIn("Failed to save audio", str(context.exception))

    def test_record_audio(self):
        try:
            recorded_audio = self.audio_adapter.record(self.duration_in_seconds)
            self.assertEqual(
                len(recorded_audio), self.sampling_rate * self.duration_in_seconds
            )
        except Exception as e:
            self.fail(f"record() raised an unexpected exception: {e}")

    def test_record_invalid_duration(self):
        with self.assertRaises(ValueError) as context:
            self.audio_adapter.record(-1)
        self.assertIn("Duration must be greater than 0", str(context.exception))

    def test_get_duration(self):
        duration = self.audio_adapter.get_duration_in_seconds(self.test_audio)
        self.assertAlmostEqual(
            duration, len(self.test_audio) / self.sampling_rate, places=2
        )


if __name__ == "__main__":
    unittest.main()
