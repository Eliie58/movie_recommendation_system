
"""
DAG to move files from b2b input folder, to prediction input folder,
and run great expectations for data quality validation.
"""

import logging
from datetime import timedelta
from typing import List
import os
import shutil

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import great_expectations as gx

logging.basicConfig(level=logging.INFO)

INPUT_FOLDER = os.environ['B2B_FOLDER']
VALIDATION_FOLDER = os.environ['VALIDATION_FOLDER']
OUTPUT_FOLDER = os.environ['PREDICTION_FOLDER']
REJECT_FOLDER = os.environ['REJECT_FOLDER']
context = gx.get_context()


@dag(
    dag_id='injestion_job',
    description='Ingest data from a file',
    tags=['get_data', 'injest_data'],
    schedule=timedelta(minutes=5),
    catchup=False,
    start_date=days_ago(n=0, hour=0)
)
def ingest_data():
    """
    Data Ingestion DAG
    """
    @task
    def get_input_files() -> List:
        logging.info('Getting files under %s', INPUT_FOLDER)
        return os.listdir(INPUT_FOLDER)

    @task
    def validate_files(input_files: List):
        valid_files = []
        invalid_files = []

        for file in input_files:
            shutil.copy2(f'{INPUT_FOLDER}/{file}',
                         f'{VALIDATION_FOLDER}/to_validate.csv')
            results = context.run_checkpoint('movies_checkpoint')
            # Handle result of validation
            if not results["success"]:
                logging.info('File %s failed validation. %s', file, results)
                invalid_files.append(file)
            else:
                valid_files.append(file)
            os.remove(f'{VALIDATION_FOLDER}/to_validate.csv')

        return {OUTPUT_FOLDER: valid_files, REJECT_FOLDER: invalid_files}

    @task
    def move_files_to_folder(folder: str, files: List):
        """
        Move files from INPUT_FOLDER to provided folder

        Parameter
        ---------
        folder: str
            The target folder
        files: list
            List of file to be moved
        """
        for file in files[folder]:
            logging.info('Moving %s from %s to %s', file,
                         INPUT_FOLDER, folder)
            os.rename(f'{INPUT_FOLDER}/{file}', f'{folder}/{file}')
        return True

    input_files = get_input_files()
    file_validation_result = validate_files(input_files)
    move_files_to_folder(OUTPUT_FOLDER, file_validation_result)
    move_files_to_folder(REJECT_FOLDER, file_validation_result)


ingest_data()
