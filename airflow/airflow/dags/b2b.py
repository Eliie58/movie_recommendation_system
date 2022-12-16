"""
Dag to generate random b2b request files.
"""

import logging
from datetime import timedelta, datetime
import random
import os

import pandas as pd
from airflow.decorators import dag, task

logging.basicConfig(level=logging.INFO)

EPS = 0.1

OUTPUT_FOLDER = os.environ['B2B_FOLDER']
movies_df = pd.read_csv('data/movies.csv')


@dag(
    dag_id='b2b_generator',
    description='Generate b2b incoming files',
    schedule=timedelta(minutes=1),
    catchup=False,
    start_date=datetime(2021, 1, 1)
)
def generator():
    """
    Dag to generate random b2b request files.
    """
    @task
    def get_random_number_of_files() -> int:
        random_number_of_files = random.randint(1, 3)
        logging.info("Number of b2b files to generate : %s",
                     random_number_of_files)
        return random_number_of_files

    @task
    def generate_files(random_number_of_files: int):
        for _ in range(random_number_of_files):
            file_size = get_file_size()
            file_df = get_file_df(file_size)
            file_name = get_file_name()
            logging.info('Saving %s records to {file_name}')
            file_df.to_csv(file_name, index=False)

    # Task relationships
    random_number_of_files = get_random_number_of_files()
    generate_files(random_number_of_files)


def get_file_name() -> str:
    """
    Retun random file name with current timestamp.

    Return
    ------
    str
        Return file name with the current timestamp.
    """
    return f"{OUTPUT_FOLDER}/b2b_{datetime.now().strftime('%H%M%S%f')}.csv"


def get_file_size() -> int:
    """
    Get a random number between 10 and 120, with a probability
    EPS of number > 100.
    """
    if random.random() < EPS:
        return 100 + random.randint(1, 20)
    return 9 + random.randint(1, 90)


def get_file_df(file_size: int) -> pd.DataFrame:
    """
    Return Pandas dataframe of size {file_size} with movie prediction data.

    Parameter
    ---------
    file_size: int
        The number of rows in the file.

    Return
    ------
    pd.DataFrame
        Dataframe with the file data
    """
    generated_df = pd.DataFrame(columns=['User Id', 'Movie Id'])
    movies_sample = movies_df.sample(n=file_size, replace=False)
    for _, row in movies_sample.iterrows():
        generated_df = generated_df.append({'User Id': random.randint(
            1, 10000), 'Movie Id': row['movieId']}, ignore_index=True)
    return generated_df


# Run dag
generator()
