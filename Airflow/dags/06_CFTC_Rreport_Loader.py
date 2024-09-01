from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.decorators import dag, task, task_group

#pendulum required for timezonde aware dags
import pendulum
from sodapy import Socrata

import pandas as pd
import threading
import time
from datetime import datetime

@dag(
    # every week on wednesday?
    # every Friday at 3:30 p.m. Eastern time.

    # Time zone aware DAGs that use cron schedules respect daylight savings time.
    # For example, a DAG with a start date in the US/Eastern time zone
    # with a schedule of 0 0 * * * will run daily at 04:00 UTC during daylight savings time
    # and at 05:00 otherwise.

    schedule_interval = '31 15 * * 5', 

    start_date=pendulum.datetime(2024, 1, 1, tz="US/Eastern"), 
    
    catchup=False, 
    
    tags=["cftc"],
    
    max_active_tasks=1

    )

def ingest_cftc_data():
    
    @task()
    def start():
        start_task = EmptyOperator(
        task_id="start"
        )
        
    @task   
    def cftc_ingest(**context):
        postgres_hook = PostgresHook(postgres_conn_id="db")
        commodity_code_dict = {'Wheat': '001602',
                                'Corn': '002602',
                                'Oilseed, Soybean': '005602',
                                'soybean Meal': '026603',
                                'Soybean Oil':'007601'}
        client = Socrata("publicreporting.cftc.gov", None)

        #https://dev.socrata.com/foundry/publicreporting.cftc.gov/kh3c-gbw2

        results = client.get("jun7-fc8e", select="\
                    report_date_as_yyyy_mm_dd, \
                    contract_market_name, \
                    cftc_market_code, \
                    cftc_commodity_code, \
                    commodity_name, \
                    pct_of_oi_comm_long_all,\
                    pct_of_oi_comm_short_all,\
                    pct_of_oi_noncomm_long_all,\
                    pct_of_oi_noncomm_short_all", 
                     where="(cftc_contract_market_code == '001602' OR \
                            cftc_contract_market_code == '002602' OR \
                            cftc_contract_market_code == '005602' OR \
                            cftc_contract_market_code == '026603' OR \
                            cftc_contract_market_code == '007601' ) \
                             AND \
                            (report_date_as_yyyy_mm_dd >= '1994-01-01T00:00:00.000')",
                     order="report_date_as_yyyy_mm_dd",
                     limit =50000)
        df = pd.DataFrame.from_records(results)
        df['report_date_as_yyyy_mm_dd'] = pd.to_datetime(df['report_date_as_yyyy_mm_dd'])

        df["pct_of_oi_comm_long_all"] = df["pct_of_oi_comm_long_all"].astype(float)
        df["pct_of_oi_comm_short_all"] = df["pct_of_oi_comm_short_all"].astype(float)
        df["pct_of_oi_noncomm_long_all"] = df["pct_of_oi_noncomm_long_all"].astype(float)
        df["pct_of_oi_noncomm_short_all"] = df["pct_of_oi_noncomm_short_all"].astype(float)

        df.to_sql('05_COT_Legacy_Combined_Report', postgres_hook.get_sqlalchemy_engine(), schema='raw',if_exists='replace', index=False)
        
    @task() 
    def end():
         start_task = EmptyOperator(
             task_id="end"
         )
    
    chain(  start(),
             cftc_ingest(),
             end()
          )

ingest_cftc_data()