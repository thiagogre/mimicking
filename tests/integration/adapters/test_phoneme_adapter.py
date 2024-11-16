import unittest

from adapters import PhonemeAdapter


class TestPhonemeAdapter(unittest.TestCase):
    def setUp(self):
        self.phoneme_adapter = PhonemeAdapter()

    def test_phonemes_property(self):
        """
        Scenario: Access phonemes property of PhonemeAdapter.
        Given that the PhonemeAdapter is initialized,
        When accessing the phonemes property,
        Then it should return the CMU dictionary.
        """
        phonemes = self.phoneme_adapter.phonemes
        word = "hello"

        self.assertIn(word, phonemes)
        self.assertEqual(phonemes[word][0], ["HH", "AH0", "L", "OW1"])


if __name__ == "__main__":
    unittest.main()
