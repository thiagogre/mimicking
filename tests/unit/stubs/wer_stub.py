from application.ports import AbstractWerPort


class WerStub(AbstractWerPort):
    def calculate_wer(self, phonemesX: str, phonemesY: str) -> float:
        if phonemesX == phonemesY:
            return 0.0
        else:
            return abs(len(phonemesX) - len(phonemesY)) / max(
                len(phonemesX), len(phonemesY)
            )
