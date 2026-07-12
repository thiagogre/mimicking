from typing import *
from datetime import datetime, timedelta

from application.models import PhraseModel


class PhraseService:
    def __init__(self, database_service):
        self.database_service = database_service

    def __get_review_days(self, similarity: float) -> int:
        if similarity < 10:
            return 15
        elif similarity < 20:
            return 6
        elif similarity < 30:
            return 5
        elif similarity < 40:
            return 4
        else:
            return 1

    def _apply_repeat_at(self, phrase: PhraseModel) -> str:
        days = self.__get_review_days(phrase.similarity)
        phrase.repeat_at = (datetime.now() + timedelta(days=days)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def save(self, phrase: PhraseModel) -> None:
        self._apply_repeat_at(phrase)
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

    def get_expired_repeat_at(self):
        rows = self.database_service.get_expired_repeat_at(
            "logs", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return [
            (
                columns[0],
                columns[5],
                columns[6],
            )
            for columns in rows
        ]

    def invalidate_repeat_at(self, id):
        self.database_service.update_by_id(
            "logs",
            id,
            (
                (
                    "repeat_at",
                    (datetime.now() + timedelta(weeks=10000)).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                ),
            ),
        )
