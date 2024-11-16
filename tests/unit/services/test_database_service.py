import unittest

from application.services import DatabaseService
from application.models import PhraseModel
from tests.unit.stubs import DatabaseStub


class TestDatabaseService(unittest.TestCase):
    def setUp(self):
        self.database_port = DatabaseStub()
        self.database_service = DatabaseService(self.database_port)
        self.database_port.connect()
        self.test_init_db_creates_tables()

    def tearDown(self):
        self.database_service.close()

    def test_init_db_creates_tables(self):
        self.database_service.init_db()
        self.assertIn("logs", self.database_port.tables)
        self.assertIn("phrase_index", self.database_port.tables)

    def test_save_inserts_data(self):
        phrase = PhraseModel(0.95, "native_phrase", "student_phrase", "Some phrase", 1)
        self.database_service.save("logs", phrase)
        logs_table = self.database_port.tables["logs"]
        self.assertEqual(len(logs_table), 1)
        self.assertEqual(logs_table[0][0], phrase.similarity)
        self.assertEqual(logs_table[0][1], phrase.native)
        self.assertEqual(logs_table[0][2], phrase.student)
        self.assertEqual(logs_table[0][3], phrase.phrase)
        self.assertEqual(logs_table[0][4], phrase.phrase_index)

    def test_get_indexes_returns_correct_data(self):
        index_data = self.database_service.get_indexes("phrase_index")
        self.assertEqual(index_data, ("1", 0, 0))

    def test_update_index_updates_data(self):
        self.database_service.update_index(
            "phrase_index", global_index="5", current_index="3"
        )
        updated_index = self.database_service.get_indexes("phrase_index")
        self.assertEqual(updated_index, ("1", "5", "3"))


if __name__ == "__main__":
    unittest.main()
