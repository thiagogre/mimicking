from dataclasses import dataclass
from typing import *

from application.ports import (
    AbstractDatabasePort,
    CreateTableParams,
    InsertParams,
    UpdateByIdParams,
    FindByIdParams,
)


class DatabaseStub(AbstractDatabasePort):
    def __init__(self):
        self.tables = {}
        self.connected = False

    def connect(self):
        self.connected = True

    def close(self):
        self.connected = False

    def create_table(self, params: CreateTableParams):
        if not self.connected:
            raise RuntimeError("Database is not connected")

        self.tables[params.table_name] = []

    def insert_if_it_doesnt_exist(self, params: InsertParams):
        if not self.connected:
            raise RuntimeError("Database is not connected")

        if self.tables.get(params.table_name) is None:
            raise ValueError(f"Table {params.table_name} does not exist")

        for row in self.tables.get(params.table_name):
            if row:
                return

        col_values = tuple(col[1] for col in params.columns)
        self.tables[params.table_name].append(col_values)

    def insert(self, params: InsertParams):
        if not self.connected:
            raise RuntimeError("Database is not connected")

        if self.tables.get(params.table_name) is None:
            raise ValueError(f"Table {params.table_name} does not exist")

        col_values = tuple(params.columns.values())
        self.tables[params.table_name].append(col_values)

    def findById(self, params: FindByIdParams):
        if not self.connected:
            raise RuntimeError("Database is not connected")

        if self.tables.get(params.table_name) is None:
            raise ValueError(f"Table {params.table_name} does not exist")

        for row in self.tables[params.table_name]:
            if row[0] == params.id:
                return row

        return ()

    def updateById(self, params: UpdateByIdParams):
        if not self.connected:
            raise RuntimeError("Database is not connected")

        if self.tables.get(params.table_name) is None:
            raise ValueError(f"Table {params.table_name} does not exist")

        col_values = tuple(col[1] for col in params.columns)

        for i, row in enumerate(self.tables[params.table_name]):
            if row[0] == params.id:
                self.tables[params.table_name][i] = col_values
                return

        raise ValueError("Record with given ID not found")
