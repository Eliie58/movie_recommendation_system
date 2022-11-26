"""This module contains the functions used to train KNNBaseline model."""

import logging
from datetime import datetime
from statistics import mean

import pandas as pd
from surprise import Dataset, Reader, KNNBaseline
from surprise.model_selection import cross_validate
import mlflow
import joblib


def build_model(data_path: str,
                model_path: str = 'models/model.joblib',
                experiment_name: str = "movie_rec",
                tracking_uri='http://127.0.0.1:5000'):
    """
    Builds and presists a KNNBaseline model, from the input dataset.

    Parameters
    ----------
    data_path : str
        The path of the ratings csv dataset.
    model_path : str, optional
        The location where to store the trained model.
    experiment_name : str, optional
        The mlflow experiment name to use.
    tracking_uri : str, optional
        The mlflow tracking uri to use.

    Returns
    -------
    surprise.KNNBaseline
        The trained model.
    """
    dataset = load_dataset(data_path)
    model = train_model(dataset, experiment_name, tracking_uri)
    persist_model(model, model_path)


def load_dataset(data_path: str) -> Dataset:
    """
    Load the csv dataset from the input location into a surprise Dataset.

    Parameters
    ----------
    data_path : str
        The path of the ratings csv dataset.

    Returns
    -------
    surprise.Dataset
        The loaded dataset.
    """
    ratings_data = pd.read_csv(data_path)
    ratings_count = len(ratings_data)
    users_count = len(ratings_data['userId'].unique())
    movies_count = len(ratings_data['movieId'].unique())
    logging.info('Loaded Ratings dataset from %s.', data_path)
    logging.info('Number of ratings : %s.', ratings_count)
    logging.info('Number of unique users : %s', users_count)
    logging.info('Number of unique movies : %s', movies_count)
    reader = Reader(rating_scale=(
        ratings_data.rating.min(), ratings_data.rating.max()))
    return Dataset.load_from_df(ratings_data[['userId', 'movieId', 'rating']],
                                reader)


def train_model(dataset: Dataset,
                experiment_name: str = "movie_rec",
                tracking_uri='http://127.0.0.1:5000'
                ) -> KNNBaseline:
    """
    Train a new KNNBaseline model using the passed Dataset.

    Parameters
    ----------
    dataset : surprise.Dataset
        The dataset to be used for training.
    experiment_name : str, optional
        The mlflow experiment name to use.
    tracking_uri : str, optional
        The mlflow tracking uri to use.


    Returns
    -------
    surprise.KNNBaseline
        The trained model.
    """
    setup_mlflow()
    training_timestamp = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    with mlflow.start_run(run_name=f"model_{training_timestamp}"):
        trainset = dataset.build_full_trainset()
        model = get_new_model()
        model.fit(trainset)
        metrics = cross_validate(get_new_model(), dataset, measures=[
                                 "RMSE", "MAE"], cv=2)
        mlflow.log_metrics({key: mean(value)
                           for key, value in metrics.items()})
        mlflow.log_params(model.sim_options)
        mlflow.sklearn.log_model(model, "model")
        logging.info("Model saved in run %s",
                     mlflow.active_run().info.run_uuid)
    return model


def setup_mlflow(
        experiment_name: str = "movie_rec",
        tracking_uri: str = 'http://127.0.0.1:5000'):
    """
    Set mlflow experiment name and tracking uri.

    Parameters
    ----------
    experiment_name : str, optional
        The mlflow experiment name to use.
    tracking_uri : str, optional
        The mlflow tracking uri to use.

    """
    mlflow.set_tracking_uri(tracking_uri)
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        mlflow.create_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)


def get_new_model() -> KNNBaseline:
    """
    Get a new instance of KNNBaseline model.

    Returns
    -------
    surprise.KNNBaseline
        A new configured instance of KNNBaseline model.
    """
    sim_options = {"name": "pearson_baseline", "user_based": False}
    model = KNNBaseline(sim_options=sim_options)
    return model


def persist_model(model: KNNBaseline, path: str):
    """
    Save the model to the disk.

    Parameters
    ----------
    model : surprise.KNNBaseline
        The model to be persisted.
    path : str, optional
        The path used to store the model.
    """
    logging.info('Persisting the model to %s', path)
    joblib.dump(model, path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    build_model('data/ratings.csv')
