from abc import ABC, abstractmethod
import csv
from csv import DictReader

class DataLoader(ABC):

  @staticmethod
  @abstractmethod
  def load(self):
    pass


class CSVDataLoader(DataLoader):

  @staticmethod
  def load(ds, **kwargs) -> DictReader:
    task_instance = kwargs['task_instance']
    path = kwargs['params']['path']
    field_names = ['country', 'pneumonia', 'ari', 'diarrhoea', 'nets', 'fever']
    with open(path) as f:
      reader = csv.DictReader(f, delimiter=field_names)
      f.close()
      return reader