from typing import *

from application.models import PhraseModel


class PhraseService:
    def __init__(self, database_service):
        self.database_service = database_service

    def save(self, phrase: PhraseModel) -> None:
        self.database_service.save("logs", phrase)

    def get_indexes(self) -> Tuple[int, int]:
        columns = self.database_service.get_indexes("phrase_index")
        return (columns[1], columns[2]) if columns else (0, 0)

    def increment_indexes(self) -> None:
        global_index, current_index = self.get_indexes()
        new_global_index = global_index + 1
        new_current_index = current_index + 1
        self.database_service.update_index(
            "phrase_index", new_global_index, new_current_index
        )

    def load_phrases_from_file(self, filename) -> List[str]:
        with open(filename, "r") as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]
