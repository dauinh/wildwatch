import sys
from airflow.models import Variable
sys.path.append(Variable.get("PROJ_DIR"))

from datetime import datetime, timedelta

import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from scripts.extract_en_species import main

with DAG(
    dag_id="en_species_etl",
    start_date=datetime(year=2024, month=11, day=1),
    schedule=timedelta(days=7*16),
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

    extract_data = PythonOperator(
        dag=dag,
        task_id='extract_data',
        python_callable=main,
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
