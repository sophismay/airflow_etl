from abc import ABC, abstractmethod
from typing import List
from airflow.hooks.postgres_hook import PostgresHook
import absl.logging as logger

class Connection(ABC):
  def __init__(self):
    super().__init__()

  @staticmethod
  @abstractmethod
  def get_instance(self):
    pass

  @abstractmethod
  def get_connection(self):
    pass

  @abstractmethod
  def close(self):
    pass


class PostgresConnection(Connection):

  __instance = None
  __postgres_conn_id: str = 'postgres_rds'
  __schema: str = 'database_schema'

  def __init__(self):
    self.connection = PostgresHook(PostgresConnection.__postgres_conn_id,
                                   PostgresConnection.__schema)\
                                    .get_conn()
    try:
      self.__cursor = self.connection.cursor()
      if PostgresConnection.__instance:
        raise Exception("Error. Singleton Class here!")
      PostgresConnection.__instance = self
      super().__init__()
    except Exception as e:
      logger.warning('Exception while connecting to PostgresDB : {}'.format(e))

  @staticmethod
  def get_instance(self):
    if not PostgresConnection.__instance:
      PostgresConnection.__instance = PostgresConnection()
    return PostgresConnection.__instance

  def get_connection(self):
    return self.connection

  def execute_query(self, query=None):
    if query is None:
      raise ValueError("Query MUST be provided")
    try:
      self.__cursor.execute(query)
    except Exception as e:
      logger.warning("Exception executing query {}".format(e))
      logger.info("query failed: {}".format(query))

  def execute_queries(self, queries=List[str], batch_size=500) -> None:
    if queries is None:
      raise ValueError("Queries MUST be provided")
    if batch_size > 1000:
      raise ValueError("Maximum batch size is 1000")
    try:
      count = 0
      for query in queries:
        self.__cursor.execute_query(query)
        count += 1
        if count >= batch_size:
          self.__commit_queries()
          count = 0
      self.__commit_queries()
    except Exception as e:
      logger.warning("Exception executing queries: {} ".format(e))

  def fetch_many(self, query):
    # naming the __cursor for the origin table to force the library to create a server __cursor
    # __cursor = self.connection.__cursor("serverCursor")
    # get the records in batches
    queried_records = []
    try:
      self.__cursor.execute(query)
      while True:
        records = self.__cursor.fetchmany(size=500)
        if not records:
          break
        queried_records.extend(records)
    except Exception as e:
      raise Exception("Postgres connection exception : %s " % e)
    finally:
      self.__cursor.close()
    logger.info("{} records fetched.".format(len(queried_records)))

    return queried_records

  def __commit_queries(self):
    self.connection.commit()

  def close(self):
    self.connection.close()