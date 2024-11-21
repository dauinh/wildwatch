import sys
from airflow.models import Variable
sys.path.append(Variable.get("PROJ_DIR"))

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

from scripts import extract, transform


with DAG(
    dag_id="en_species_etl",
    start_date=datetime(year=2024, month=11, day=1),
    schedule=timedelta(days=7*16),
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

    extract_en_species_data = PythonOperator(
        dag=dag,
        task_id='extract_en_species_data',
        python_callable=extract.en_species_main,
    )

    extract_code_description = PythonOperator(
        dag=dag,
        task_id='extract_code_description',
        python_callable=extract.code_description_main,
    )

    transform_en_species_data = PythonOperator(
        dag=dag,
        task_id='transform_en_species_data',
        python_callable=transform.transform_en_species_data,
    )

    def load_en_species():
        hook = S3Hook('s3_conn')
        bucket_name = 'wildwatchstorage'
        hook.load_file(filename='/opt/airflow/processed_data/en_main.csv', key='en_main.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/en_habitats.csv', key='en_habitats.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/en_locations.csv', key='en_locations.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/en_conservation_actions.csv', key='en_conservation_actions.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/en_threats.csv', key='en_threats.csv', bucket_name=bucket_name, replace=True)

    load_en_species_data = PythonOperator(
        dag=dag,
        task_id='load_en_species_data',
        python_callable=load_en_species
    )

    def load_code_description():
        hook = S3Hook('s3_conn')
        bucket_name = 'wildwatchstorage'
        hook.load_file(filename='/opt/airflow/processed_data/conservation_actions.csv', key='conservation_actions.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/habitats.csv', key='habitats.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/threats.csv', key='threats.csv', bucket_name=bucket_name, replace=True)

    load_code_description_data = PythonOperator(
        dag=dag,
        task_id='load_code_description_data',
        python_callable=load_code_description
    )

    # Set dependencies between tasks
    extract_en_species_data >> transform_en_species_data >> load_en_species_data
    extract_code_description >> load_code_description_data
