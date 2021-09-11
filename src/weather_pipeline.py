from datetime import datetime, timedelta
import json

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator

from utils import _local_to_s3
from generate_data import get_data

# Config
BUCKET_NAME = Variable.get("BUCKET")

# DAG definition
default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime(2021, 8, 23),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "weather_pipeline",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    max_active_runs=1,
)

extract_weather_data = PythonOperator (
	dag=dag,
	task_id='extract_weather_data',
	python_callable=get_data,
	op_kwargs={
		"target_file": "/temp/weather_data.json",
		"input_cities_file": "../data/cities.json"
	},
)
weather_data_to_data_lake = PythonOperator (
	dag=dag,
    task_id="weather_data_to_data_lake",
    python_callable=_local_to_s3,
    op_kwargs={
        "file_name": "/temp/weather_data.json",
        "key": "raw/weather_data/{{ ds }}/weather_data.json",
        "bucket_name": BUCKET_NAME,
        #Toggle to true in prod
        "remove_local": "false",
    },
)


invoke_lambda_function = PythonOperator (
    dag = dag,
    task_id='invoke_lambda_function',
    python_callable=invoke_lambda_function,
    op_kwargs={
        "function_name": LAMBDA_FUCNTION_NAME
    },
)

extract_weather_data >> weather_data_to_data_lake >> invoke_lambda_function