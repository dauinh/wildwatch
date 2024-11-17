import sys
from airflow.models import Variable
sys.path.append(Variable.get("PROJ_DIR"))

from datetime import datetime, timedelta
import pandas as pd
import ast

import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

from scripts import extract_en_species


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
        python_callable=extract_en_species.main,
    )

    def transform():
        df = pd.read_csv('/opt/airflow/raw_data/EN.csv')

        def create_relationship_table(table, column, is_tuple=False, tuples=[]):
            table = df[['id', column]].copy()
            table[column] = table[column].apply(ast.literal_eval)
            table = table.explode(column).dropna().reset_index(drop=True)
            if is_tuple:
                table[tuples] = pd.DataFrame(table[column].tolist(), index=table.index)
            return table
        
        conser_act_df = create_relationship_table('conser_act_df', 'conservation_actions')
        habitats_df = create_relationship_table('habitats_df', 'habitats', is_tuple=True, tuples=['code', 'majorImportance', 'season']).drop('habitats', axis=1)
        locations_df = create_relationship_table('locations_df', 'locations', is_tuple=True, tuples=['origin', 'code']).drop('locations', axis=1)
        threats_df = create_relationship_table('threats_df', 'threats', is_tuple=True, tuples=['code', 'timing', 'scope', 'score', 'severity']).drop('threats', axis=1)
        main_df = df.drop(['conservation_actions', 'locations', 'habitats', 'threats'], axis=1)

        main_df.to_csv('/opt/airflow/processed_data/main.csv', header=True, index=False)
        habitats_df.to_csv('/opt/airflow/processed_data/habitats.csv', header=True, index=False)
        locations_df.to_csv('/opt/airflow/processed_data/locations.csv', header=True, index=False)
        conser_act_df.to_csv('/opt/airflow/processed_data/conservation_actions.csv', header=True, index=False)
        threats_df.to_csv('/opt/airflow/processed_data/threats.csv', header=True, index=False)

    transform_data = PythonOperator(
        dag=dag,
        task_id='transform_data',
        python_callable=transform,
    )

    def load():
        hook = S3Hook('s3_conn')
        bucket_name = 'wildwatchstorage'
        hook.load_file(filename='/opt/airflow/processed_data/main.csv', key='main.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/habitats.csv', key='habitats.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/locations.csv', key='locations.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/conservation_actions.csv', key='conservation_actions.csv', bucket_name=bucket_name, replace=True)
        hook.load_file(filename='/opt/airflow/processed_data/threats.csv', key='threats.csv', bucket_name=bucket_name, replace=True)

    load_data = PythonOperator(
        dag=dag,
        task_id='load_data_to_s3',
        python_callable=load
    )

    # Set dependencies between tasks
    extract_data >> transform_data >> load_data
