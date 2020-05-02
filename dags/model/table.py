from typing import NamedTuple
from abc import ABC, abstractmethod
import uuid

class TableAttr(NamedTuple):
  id: str = str(uuid.uuid4())


class DocumentAttr(NamedTuple):
  id: str
  created_on: str
  modified_on: str


class Table(ABC):

  def __init__(self, attr):
    self._attr = attr

  def get_attributes(self):
    return self._attr

  @abstractmethod
  def get_insert_query(self):
    pass

  @property
  @abstractmethod
  def table_name(self):
    pass


class Supplement(Table):

  def __init__(self, attr: DocumentAttr):
    super().__init__(attr)

  def table_name(self):
    return 'supplement'

  def get_insert_query(self) -> str:
    at = self._attr
    query = "INSERT INTO ..."

    return query

  @staticmethod
  def get_unprocessed(topics):
    topics = ','.join(topics)
    query = ""

    return query