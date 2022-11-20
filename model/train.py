"""This module contains the functions used to train KNNBaseline model."""

import logging

import pandas as pd
from surprise import Dataset, Reader, KNNBaseline
import joblib


def build_model(data_path: str, model_path: str = 'models/model.joblib'):
    """
    Builds and presists a KNNBaseline model, from the input dataset.

    Parameters
    ----------
    data_path : str
        The path of the ratings csv dataset.

    Returns
    -------
    surprise.KNNBaseline
        The trained model.
    """
    dataset = load_dataset(data_path)
    model = train_model(dataset)
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


def train_model(dataset: Dataset) -> KNNBaseline:
    """
    Train a new KNNBaseline model using the passed Dataset.

    Parameters
    ----------
    dataset : surprise.Dataset
        The dataset to be used for training.

    Returns
    -------
    surprise.KNNBaseline
        The trained model.
    """
    trainset = dataset.build_full_trainset()
    model = get_new_model()
    model.fit(trainset)
    return model


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
    build_model('data/ratings.csv')
