# dags/daily_scraper_dag.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='daily_article_scraper',
    default_args=default_args,
    description='Scrape top 10 MoneyControl market articles with full content daily',
    schedule_interval='@daily',
    start_date=datetime(2025, 4, 26),
    catchup=False,
    tags=['scraper', 'moneycontrol', 'airflow']
) as dag:

    scrape_articles = BashOperator(
        task_id='scrape_and_store_articles',
        bash_command='python C:\Users\Hardik\OneDrive\Desktop\SEM 8\DA5402\PROJECT\scripts\scrape_articles.py'
    )

    scrape_articles
