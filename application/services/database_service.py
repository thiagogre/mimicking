from dataclasses import asdict

from application.ports import (
    AbstractDatabasePort,
    CreateTableParams,
    InsertParams,
    FindByIdParams,
    UpdateByIdParams,
)


class DatabaseService:
    def __init__(
        self,
        database_port: AbstractDatabasePort,
    ):
        self.database_port = database_port

    def init_db(self):
        logs_params = CreateTableParams(
            "logs",
            (
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("similarity", "REAL"),
                ("native", "TEXT"),
                ("student", "TEXT"),
                ("phrase", "TEXT"),
                ("phrase_index", "INTEGER"),
                ("date", "TEXT DEFAULT CURRENT_TIMESTAMP"),
            ),
        )
        phrase_index_params = CreateTableParams(
            "phrase_index",
            (
                ("id", "INTEGER PRIMARY KEY CHECK (id = 1)"),
                ("global_index", "INTEGER"),
                ("current_index", "INTEGER"),
            ),
        )
        default_phrase_index_params = CreateTableParams(
            "phrase_index",
            (
                ("id", "1"),
                ("global_index", 0),
                ("current_index", 0),
            ),
        )
        self.database_port.create_table(logs_params)
        self.database_port.create_table(phrase_index_params)
        self.database_port.insert_if_it_doesnt_exist(default_phrase_index_params)

    def close(self):
        self.database_port.close()

    def save(self, table_name, data):
        columns = asdict(data)
        params = InsertParams(
            table_name,
            columns,
        )
        self.database_port.insert(params)

    def get_indexes(self, table_name):
        params = FindByIdParams(table_name, "1")
        return self.database_port.findById(params)

    def update_index(self, table_name, global_index, current_index):
        params = UpdateByIdParams(
            table_name,
            "1",
            (
                ("id", "1"),
                ("global_index", global_index),
                ("current_index", current_index),
            ),
        )
        self.database_port.updateById(params)
