import os
import csv
from datetime import datetime, timedelta

import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="sample_extract",
    start_date=datetime(year=2024, month=1, day=1, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:
    def extract():
        with open('raw_data/EN.csv', 'w') as f:
            writer = csv.writer(f)
            fields = ['id', 'conservation_actions', 'habitats', 'locations', 'population_trend', 'possibly_extinct', 'possibly_extinct_in_the_wild', 'sis_taxon_id', 'estimated_area_of_occupancy', 'estimated_extent_of_occurence', 'taxon', 'threats', 'url']
            writer.writerow(fields)

    extract_data = PythonOperator(
        dag=dag,
        task_id='extract_data',
        python_callable=extract,
    )

    def finish_message():
        print('Extracted successfully!')

    message = PythonOperator(
        dag=dag,
        task_id='message',
        python_callable=finish_message,
    )

    # Set dependencies between tasks
    extract_data >> message
