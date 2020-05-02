from abc import ABC, abstractmethod
from dags.loader.dataloader import CSVDataLoader


class Parser(ABC):
  def __init__(self):
    super().__init__()

  @abstractmethod
  def get_dir_path(self):
    pass

  @abstractmethod
  def parse(self, dir_path: str, schema: str):
    pass


class CSVParser(Parser):
  def __init__(self, loader: CSVDataLoader):
    self.loader = loader
    super().__init__()

  def parse(self, dir_path: str, schema: str):
    pass