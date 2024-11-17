"""
S3 Connection Test
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook
from datetime import datetime, timedelta

with DAG(
    dag_id='s3_conn_dag',
    start_date=datetime(2024, 11, 1),
    schedule_interval='@once'
) as dag:
    
    def upload(filename, key, bucket_name):
        hook = S3Hook('s3_conn')
        hook.load_file(filename=filename, key=key, bucket_name=bucket_name)
    
    upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload,
        op_kwargs={
            'filename': '/opt/airflow/processed_data/main.csv',
            'key': 'main.csv',
            'bucket_name': 'wildwatchstorage'
        }
    )