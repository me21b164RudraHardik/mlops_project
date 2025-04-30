from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='daily_market_analysis',
    default_args=default_args,
    description='Daily analysis of market articles',
    schedule_interval='@daily',
    start_date=datetime(2025, 4, 30),
    catchup=False,
    tags=['analysis', 'market', 'nlp']
) as dag:

    run_analysis = BashOperator(
        task_id='analyze_market_articles',
        bash_command='python C:\Users\Hardik\OneDrive\Desktop\SEM 8\DA5402\PROJECT\data_analysis.py'
    )

    run_analysis
