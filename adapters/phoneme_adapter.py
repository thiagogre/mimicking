import nltk
import os
from typing import *

from settings import ROOT_DIR
from application.ports import AbstractPhonemePort


class PhonemeAdapter(AbstractPhonemePort):
    @property
    def nltk_data_path(self):
        return os.path.join(ROOT_DIR, "nltk_data")

    @property
    def phonemes(self) -> Dict:
        return self.cmudict

    def __init__(self):
        self._append_nltk_data_path()
        self._ensure_cmudict_downloaded()
        self.cmudict = nltk.corpus.cmudict.dict()

    def _append_nltk_data_path(self):
        if self.nltk_data_path not in nltk.data.path:
            nltk.data.path.append(self.nltk_data_path)

    def _ensure_cmudict_downloaded(self):
        try:
            nltk.data.find("corpora/cmudict.zip")
        except LookupError:
            nltk.download("cmudict", download_dir=self.nltk_data_path)
