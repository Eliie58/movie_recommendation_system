import logging
from datetime import datetime
from datetime import timedelta
import os
import requests

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago





@dag(
    dag_id='prediction_job',
    description='make_predictions',
    tags=['read_newly_injested_data', 'make_predictions'],
    schedule=timedelta(minutes=5),
    start_date=days_ago(n=0, hour=1)
)

def ingest_data():
    @task
    def list_files_in_folder(folder_name):
        return os.listdir(folder_name)

    @task 
    def process_files(folder_name, files):
        for file in files:
            os.rename("output_data", "input_data.movie_id")
            df = pd.read_csv(os.path.join(folder_name, file))
            requests.post('http://localhost:8080/upload', json={'ids':df['movie_id'].to_list()})

    outputdir = 'output_data'
    files = list_files_in_folder(outputdir)
    process_files(outputdir, files)





ingest_data()