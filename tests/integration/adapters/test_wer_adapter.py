import unittest

from adapters import WerAdapter


class TestWerAdapter(unittest.TestCase):
    def setUp(self):
        self.wer_adapter = WerAdapter()

    def test_calculate_wer_exact_match(self):
        """
        Scenario: Calculate WER when both strings are identical.
        Given two identical strings,
        When calculate_wer is called,
        Then the result should be 0.0 (no errors).
        """
        phonemesX = "this is a test"
        phonemesY = "this is a test"
        result = self.wer_adapter.calculate_wer(phonemesX, phonemesY)
        self.assertEqual(result, 0.0)

    def test_calculate_wer_partial_match(self):
        """
        Scenario: Calculate WER with partial match.
        Given two strings with some differences,
        When calculate_wer is called,
        Then the result should reflect the word error rate.
        """
        phonemesX = "this is a test"
        phonemesY = "tis isa test"
        result = self.wer_adapter.calculate_wer(phonemesX, phonemesY)
        self.assertGreater(result, 0.6)

    def test_calculate_wer_no_match(self):
        """
        Scenario: Calculate WER when there is no match.
        Given two completely different strings,
        When calculate_wer is called,
        Then the result should be 1.0 (all words are incorrect).
        """
        phonemesX = "this is a test"
        phonemesY = "completely different string"
        result = self.wer_adapter.calculate_wer(phonemesX, phonemesY)
        self.assertEqual(result, 1.0)

    def test_calculate_wer_empty_input(self):
        """
        Scenario: Calculate WER with empty input.
        Given one or both strings are empty,
        When calculate_wer is called,
        Then the result should raise a ValueError.
        """
        phonemesX = ""
        phonemesY = "this is a test"
        with self.assertRaises(ValueError):
            self.wer_adapter.calculate_wer(phonemesX, phonemesY)

        phonemesX = "this is a test"
        phonemesY = ""
        with self.assertRaises(ValueError):
            self.wer_adapter.calculate_wer(phonemesX, phonemesY)

        phonemesX = ""
        phonemesY = ""
        with self.assertRaises(ValueError):
            self.wer_adapter.calculate_wer(phonemesX, phonemesY)


if __name__ == "__main__":
    unittest.main()
