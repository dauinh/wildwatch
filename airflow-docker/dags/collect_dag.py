import os
import csv
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

from .collect import extract_en_species

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(7)
}

dag = DAG(
    dag_id='extract_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=30),
)

def extract():
    with open('raw_data/EN.csv', 'w') as f:
        writer = csv.writer(f)
        fields = ['id', 'conservation_actions', 'habitats', 'locations', 'population_trend', 'possibly_extinct', 'possibly_extinct_in_the_wild', 'sis_taxon_id', 'estimated_area_of_occupancy', 'estimated_extent_of_occurence', 'taxon', 'threats', 'url']
        writer.writerow(fields)

extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=extract,
    dag=dag,
)

def finish_message():
    print('Extracted successfully!')

message = PythonOperator(
    task_id='extract_message',
    python_callable=finish_message,
    dag=dag
)

extract_data >> message