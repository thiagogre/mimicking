from dataclasses import dataclass


@dataclass
class PhraseModel:
    similarity: float
    native: str
    student: str
    phrase: str
    phrase_index: int
    native_audio_filename: str
    repeat_at: str
