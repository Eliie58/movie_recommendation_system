"""
DAG for reading validated b2b requests and calling api.
"""

import logging
from datetime import timedelta
import os
from typing import List
import json
import requests

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

logging.basicConfig(level=logging.INFO)

INPUT_FOLDER = os.environ['PREDICTION_FOLDER']
OUTPUT_FOLDER = os.environ['OUTPUT_FOLDER']
API_URL = os.environ['API_URL']


@dag(
    dag_id='prediction_job',
    description='make_predictions',
    tags=['read_newly_injested_data', 'make_predictions'],
    schedule=timedelta(minutes=1),
    catchup=False,
    start_date=days_ago(n=0, hour=1)
)
def ingest_data():
    """
    DAG for reading validated b2b requests and calling api.
    """
    @task
    def list_files_in_folder():
        return os.listdir(INPUT_FOLDER)

    @task
    def process_files(files):
        for file in files:
            logging.info('Processing %s', file)
            movies_df = pd.read_csv(os.path.join(INPUT_FOLDER, file))
            resp = requests.post(f'{API_URL}/upload',
                                 json={
                                     'ids': movies_df['Movie Id'].tolist()},
                                 timeout=60)
            content = json.loads(resp.text)
            output_results(movies_df, content, file)
            logging.info(content)
            os.remove(os.path.join(INPUT_FOLDER, file))

    files = list_files_in_folder()
    process_files(files)


def output_results(movies_df: pd.DataFrame, content: List, file: str):
    """
    Write prediction output to file
    """
    data = []
    for index, row in movies_df.iterrows():
        prediction = content[index]
        predicted_movies = sorted(
            prediction['values'], key=lambda x: x['score'], reverse=True)
        data.append([row['User Id'],
                     row['Movie Id'],
                     prediction["movie"]["title"],
                     prediction['id'],
                     prediction['time_stamp'],
                     predicted_movies[0]["score"],
                     predicted_movies[0]["movie_id"],
                     predicted_movies[0]["movie"]["title"],
                     predicted_movies[1]["score"],
                     predicted_movies[1]["movie_id"],
                     predicted_movies[1]["movie"]["title"],
                     predicted_movies[2]["score"],
                     predicted_movies[2]["movie_id"],
                     predicted_movies[2]["movie"]["title"],
                     predicted_movies[3]["score"],
                     predicted_movies[3]["movie_id"],
                     predicted_movies[3]["movie"]["title"]
                     ])
    pd.DataFrame(data, columns=[
        "User Id",
        "Movie Id",
        "Movie Title",
        "Prediction Id",
        "Timestamp",
        "Prediction #1 Score",
        "Prediction #1 Movie Id",
        "Prediction #1 Movie Title",
        "Prediction #2 Score",
        "Prediction #2 Movie Id",
        "Prediction #2 Movie Title",
        "Prediction #3 Score",
        "Prediction #3 Movie Id",
        "Prediction #3 Movie Title",
        "Prediction #4 Score",
        "Prediction #4 Movie Id",
        "Prediction #4 Movie Title"
    ]).to_csv(f'{OUTPUT_FOLDER}/{file}', index=False)


ingest_data()
