import sqlite3
from application.ports.database_port import *


class DatabaseAdapter(AbstractDatabasePort):
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        try:
            return sqlite3.connect(self.db_file)
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Failed to connect to the database: {e}")

    def close(self):
        try:
            self.connection.close()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Failed to close the database connection: {e}")

    def create_table(self, params: CreateTableParams):
        try:
            column_definitions = ", ".join(
                [f"{col_name} {col_type}" for col_name, col_type in params.columns]
            )

            self.cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {params.table_name} (
                {column_definitions}
            )
            """
            )
            self.connection.commit()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Failed to create table {params.table_name}: {e}")

    def insert_if_it_doesnt_exist(self, params: CreateTableParams):
        try:
            col_names = ", ".join([str(col[0]) for col in params.columns])
            col_values = ", ".join([str(col[1]) for col in params.columns])

            self.cursor.execute(
                f"INSERT OR IGNORE INTO {params.table_name} ({col_names}) VALUES ({col_values})"
            )
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            raise RuntimeError(
                f"Integrity error while inserting into {params.table_name}: {e}"
            )
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Failed to insert into {params.table_name}: {e}")

    def insert(self, params: InsertParams):
        try:
            col_names = ", ".join(params.columns.keys())
            placeholders = ", ".join(["?"] * len(params.columns))
            col_values = list(params.columns.values())

            self.cursor.execute(
                f"INSERT INTO {params.table_name} ({col_names}) VALUES ({placeholders})",
                col_values,
            )
            self.connection.commit()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Failed to insert into {params.table_name}: {e}")

    def findById(self, params: FindByIdParams):
        try:
            self.cursor.execute(
                f"SELECT * FROM {params.table_name} WHERE id = {params.id}"
            )
            columns = self.cursor.fetchone()
            return columns if columns else ()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Failed to find record in {params.table_name}: {e}")

    def updateById(self, params: UpdateByIdParams):
        try:
            column_definitions = ", ".join(
                [
                    (
                        f"{col_name} = {col_value}"
                        if isinstance(col_value, (int, float))
                        else f"{col_name} = '{col_value}'"
                    )
                    for col_name, col_value in params.columns
                ]
            )

            self.cursor.execute(
                f"UPDATE {params.table_name} SET {column_definitions} WHERE id = {params.id}"
            )
            self.connection.commit()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(
                f"Failed to update record in {params.table_name}: {e} UPDATE {params.table_name} SET {column_definitions} WHERE id = {params.id}"
            )
