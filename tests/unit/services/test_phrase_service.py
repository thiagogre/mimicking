import unittest

from application.models import PhraseModel
from application.services import DatabaseService, PhraseService
from tests.unit.stubs import DatabaseStub


class TestPhraseService(unittest.TestCase):
    def setUp(self):
        self.database_port = DatabaseStub()
        self.database_service = DatabaseService(self.database_port)
        self.phrase_service = PhraseService(self.database_service)
        self.database_port.connect()
        self.database_service.init_db()

    def test_save(self):
        phrase = PhraseModel(0.95, "native_phrase", "student_phrase", "Some phrase", 1)
        self.database_service.save("logs", phrase)
        logs_table = self.database_port.tables["logs"]
        self.assertEqual(len(logs_table), 1)

    def test_get_indexes(self):
        row = self.phrase_service.get_indexes()
        self.assertTupleEqual(row, (0, 0))

    def test_increment_indexes(self) -> None:
        self.phrase_service.increment_indexes()
        phrase_index_table = self.database_port.tables["phrase_index"]
        row = phrase_index_table[0]
        self.assertTupleEqual(row, ("1", 1, 1))
