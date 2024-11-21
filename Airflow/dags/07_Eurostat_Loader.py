from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.decorators import dag, task, task_group

#pendulum required for timezonde aware dags
import pendulum

import pandas as pd
import time
from datetime import datetime
import requests
from io import BytesIO

@dag(
    #the data is published on wednesdays ... unspecified time.
    #so we will schedule oru DAG every thusday at 06:31

    schedule_interval = '31 06 * * 4', 

    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/London"), 
    
    catchup=False, 
    
    tags=["european_commission"],
    
    max_active_tasks=1

    )

def ingest_eurostat_data():
    
    @task()
    def start():
        start_task = EmptyOperator(
        task_id="start"
        )
        
    @task   
    def eurostat_ingest(**context):
        postgres_hook = PostgresHook(postgres_conn_id="db")
        
        #https://agriculture.ec.europa.eu/data-and-analysis/markets/overviews/market-observatories/crops/cereals-statistics_en

        url = 'https://circabc.europa.eu/sd/a/2f167193-3c01-46fb-b1da-a951cbb4b0db/cereals-eu-prices.xlsx'

        # Send a GET request to the URL
        response = requests.get(url)

        file_in_memory = BytesIO(response.content)
        

        # Read the 'Data' sheet from the .xls file starting from the 3rd row
        df = pd.read_excel(file_in_memory, sheet_name='Data', skiprows=1)

        df.to_sql('07_Eurostat_Wheat_Prices', postgres_hook.get_sqlalchemy_engine(), schema='raw',if_exists='replace', index=False)
        
    @task() 
    def end():
         start_task = EmptyOperator(
             task_id="end"
         )
    
    chain(  start(),
             eurostat_ingest(),
             end()
          )

ingest_eurostat_data()