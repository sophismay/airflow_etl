from abc import ABC, abstractmethod
import csv

class DataLoader(ABC):

  @staticmethod
  @abstractmethod
  def load(self):
    pass


class CSVDataLoader(DataLoader):

  @staticmethod
  def load(path: str):
    #TODO: use DictReader and provide custom header names
    with open(path) as f:
      reader = csv.reader(f, delimiter=',')
      return reader