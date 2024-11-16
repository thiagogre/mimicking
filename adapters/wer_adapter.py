from jiwer import wer

from application.ports import AbstractWerPort


class WerAdapter(AbstractWerPort):
    def __init__(self):
        self.wer = wer

    def calculate_wer(self, phonemesX: str, phonemesY: str) -> float:
        """
        0 - 20%: Excellent - Very close to the native pronunciation.
        20 - 40%: Good - Some minor mispronunciations but generally understandable.
        40 - 60%: Fair - Noticeable errors; pronunciation may sound foreign but is mostly understandable.
        60% and above: Poor - Significant pronunciation issues, making the pronunciation difficult to understand.
        """
        if not phonemesX or not phonemesY:
            raise ValueError("Input strings must not be empty.")
        return self.wer(phonemesX, phonemesY)
