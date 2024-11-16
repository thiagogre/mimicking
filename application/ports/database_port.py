from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *


@dataclass
class Id:
    id: Union[str, int]


@dataclass
class CreateTableParams:
    table_name: str
    columns: Tuple[Tuple[str, str], ...]


@dataclass
class InsertParams:
    table_name: str
    columns: Dict[str, Any]


@dataclass
class FindByIdParams:
    table_name: str
    id: Id


@dataclass
class UpdateByIdParams:
    table_name: str
    id: Id
    columns: Tuple[Tuple[str, str], ...]


class AbstractDatabasePort(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def create_table(self, params: CreateTableParams):
        pass

    @abstractmethod
    def insert_if_it_doesnt_exist(self, params: CreateTableParams):
        pass

    @abstractmethod
    def insert(self, params: InsertParams):
        pass

    @abstractmethod
    def findById(self, params: FindByIdParams):
        pass

    # @abstractmethod
    # def updateById(self, params: UpdateByIdParams):
    #     pass
