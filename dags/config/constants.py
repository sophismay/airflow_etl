from typing import NamedTuple
import os

DATA_PATH: str = os.environ['DATA_PATH']


class DataVars(NamedTuple):
  DATA_PATH: str = DATA_PATH