from application.ports import AbstractPhonemePort


class PhonemeStub(AbstractPhonemePort):
    @property
    def phonemes(self):
        return {"test": ["t"]}
