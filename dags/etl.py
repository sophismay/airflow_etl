import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from dags.loader.dataloader import CSVDataLoader
from dags.config.constants import DataVars as dv
from dags.model.connection import PostgresConnection
import time

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('ta-remodel-post-table', default_args= default_args, schedule_interval= None)

pc_instance: PostgresConnection = PostgresConnection.get_instance()

read_data = PythonOperator(
    task_id= 'task_read_data',
    provide_context= True,
    python_callable= CSVDataLoader.load,
    params= {'path': dv.DATA_PATH },
    dag= dag
)


model_data = PythonOperator(
    task_id= 'task_model_data',
    provid_context= True,
    python_callable='',
    dag= dag
)

read_data >> model_data

