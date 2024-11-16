import unittest

from adapters import DatabaseAdapter
from application.ports import (
    CreateTableParams,
    InsertParams,
    FindByIdParams,
    UpdateByIdParams,
)


class TestDatabaseAdapter(unittest.TestCase):
    def setUp(self):
        self.db_file = ":memory:"
        self.database_adapter = DatabaseAdapter(self.db_file)
        self.connection = self.database_adapter.connection
        self.cursor = self.database_adapter.cursor

        self.table_name = "phrases"
        self.column_name = "text"
        self.text = "This is a test"

    def tearDown(self):
        self.connection.close()

    def test_transactions(self):
        create_table_params = CreateTableParams(
            table_name=self.table_name,
            columns=[
                ("id", "INTEGER PRIMARY KEY"),
                (self.column_name, "TEXT"),
            ],
        )
        self.database_adapter.create_table(create_table_params)
        self.cursor.execute(f"SELECT {self.column_name} FROM {self.table_name}")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

        insert_table_params = InsertParams(
            table_name=self.table_name,
            columns={self.column_name: self.text},
        )
        self.database_adapter.insert(insert_table_params)
        find_params = FindByIdParams(table_name=self.table_name, id=1)
        result = self.database_adapter.findById(find_params)
        self.assertEqual(result[1], self.text)

        with self.assertRaises(RuntimeError) as context:
            self.database_adapter.insert_if_it_doesnt_exist(create_table_params)
            self.assertIn("Failed to insert into phrases", str(context.exception))

        update_params = UpdateByIdParams(
            table_name=self.table_name,
            id="1",
            columns=((self.column_name, "new test"),),
        )
        self.database_adapter.updateById(update_params)
        find_params = FindByIdParams(table_name=self.table_name, id=1)
        result = self.database_adapter.findById(find_params)
        self.assertEqual(result[1], "new test")

    def test_error_handling(self):
        """
        Scenario: Handle database errors gracefully.
        Given a faulty database operation,
        When the operation fails,
        Then the appropriate error should be raised.
        """

        with self.assertRaises(RuntimeError) as context:
            self.database_adapter.findById(
                FindByIdParams(table_name="nonexistent_table", id=1)
            )
            self.assertIn(
                "Failed to update record in nonexistent_table", str(context.exception)
            )


if __name__ == "__main__":
    unittest.main()
